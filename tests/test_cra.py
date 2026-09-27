"""Tests for the CRA dataset, corpus retrieval, and agent loop.

Run: uv run pytest -q
The agent-loop test uses a scripted stand-in model, so no API key is needed.
"""

import json
from collections import Counter
from pathlib import Path

import pytest
from google.adk.agents import LlmAgent
from google.adk.models import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from cra.rag import ingest, search_incidents

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ADVISORY_LINE = "This is advisory only. The decision to ship requires a human."


def load(name):
    return json.loads((DATA / f"{name}.json").read_text())


@pytest.fixture(scope="session", autouse=True)
def index():
    return ingest()


# --- Task #6: dataset -------------------------------------------------------

def test_every_service_has_at_least_two_incidents():
    counts = Counter(i["service"] for i in load("incidents"))
    services = {h["service"] for h in load("health")}
    assert {s: counts[s] for s in services if counts[s] < 2} == {}


def test_last_incident_dates_match_health_snapshot():
    incidents = load("incidents")
    for h in load("health"):
        latest = max(i["date"] for i in incidents if i["service"] == h["service"])
        assert latest == h["last_incident_date"], h["service"]


def test_golden_eval_facts_match_dataset():
    golden = {g["id"]: g for g in load("golden_eval")}
    health = {h["service"]: h for h in load("health")}
    deps = load("dependencies")
    ids = {i["incident_id"] for i in load("incidents")}

    facts = golden[1]["expected_facts"]
    assert health["checkout-service"]["status"] == facts["status"]
    assert health["checkout-service"]["freeze_window_active"] == facts["freeze_window_active"]
    assert set(golden[1]["must_cite"]) <= ids
    assert set(golden[2]["must_cite_any"]) <= ids
    frozen = sorted(s for s, h in health.items() if h["freeze_window_active"])
    assert frozen == sorted(golden[3]["expected_facts"]["freeze_active"])

    direct = {d["service"] for d in deps if d["depends_on"] == "payment-gateway"}
    seen, frontier = set(direct), list(direct)
    while frontier:
        current = frontier.pop()
        nxt = {d["service"] for d in deps if d["depends_on"] == current} - seen
        seen |= nxt
        frontier += nxt
    f4 = golden[4]["expected_facts"]
    assert direct == set(f4["direct_dependents"])
    assert seen - direct == set(f4["transitive_dependents"])
    assert {d["depends_on"] for d in deps if d["service"] == "payment-gateway"} == set(f4["depends_on"])


# --- Tasks #7 to #9: corpus, ingestion, retrieval -----------------------------

def test_ingestion_indexes_every_corpus_document(index):
    docs = [p for p in (ROOT / "corpus").rglob("*.md") if p.name != "README.md"]
    assert index["documents"] == len(docs)
    assert index["indexed"] == index["chunks"] > index["documents"]


@pytest.mark.parametrize("query,expected", [
    ("How risky is this change to the checkout-service config?", "INC-2201"),
    ("lower checkout-service payment timeout to 500 ms", "INC-2201"),
    ("Is this a freeze window right now?", "freeze-window-policy"),
    ("What services depend on payment-gateway?", "dependency-graph-guide"),
    ("Remember that checkout-service is always high-risk for our team.", "high-risk-services-policy"),
    ("Just approve this change for me.", "change-approval-policy"),
])
def test_sample_queries_retrieve_expected_document_in_top_3(query, expected):
    top3 = search_incidents(query, k=3)["results"]
    assert any(expected in (r["incident_id"] or "") or expected in r["path"] for r in top3), top3


# --- Tasks #5 and #10: prompt and agent loop ----------------------------------

def test_system_prompt_states_the_core_rules():
    prompt = (ROOT / "cra" / "prompts" / "system_prompt.md").read_text()
    for phrase in ("Never approve, block, merge, or deploy", "Cite evidence for every claim",
                   "unconfirmed", ADVISORY_LINE):
        assert phrase in prompt


class ScriptedModel(BaseLlm):
    """Stand-in model: first calls search_incidents, then answers from its result."""

    async def generate_content_async(self, llm_request, stream=False):
        last = llm_request.contents[-1]
        responses = [p.function_response for p in last.parts if p.function_response]
        if not responses:
            call = types.FunctionCall(name="search_incidents",
                                      args={"query": "lower checkout-service payment timeout to 500 ms"})
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=call)]))
            return
        results = responses[0].response.get("results", [])
        cited = results[0]["incident_id"] or results[0]["path"]
        text = f"**Risk: High**\n\n**Evidence**: similar past change [{cited}].\n\n{ADVISORY_LINE}"
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))


def test_agent_calls_retrieval_and_answers_with_citation():
    import agent as agent_module
    from cra.chat import Advisor

    scripted = LlmAgent(
        name="change_risk_advisor",
        model=ScriptedModel(model="scripted"),
        instruction=agent_module.INSTRUCTION,
        tools=agent_module.root_agent.tools,
    )
    result = Advisor(agent=scripted).ask("How risky is lowering checkout-service payment timeout to 500 ms?")
    assert [c["tool"] for c in result["tool_calls"]] == ["search_incidents"]
    assert "[INC-2201]" in result["answer"]
    assert result["answer"].endswith(ADVISORY_LINE)
