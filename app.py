"""Gradio chat UI for ChangeRiskAdvisor.

Run:          uv run python app.py            (http://127.0.0.1:7860)
Share link:   CRA_SHARE=1 uv run python app.py
Needs model access configured in .env (see README) and the RAG index built
with `uv run python -m cra.ingest`.
"""

import os

import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from cra.chat import Advisor  # noqa: E402  (after .env is loaded)

advisor = Advisor()

EXAMPLES = [
    "How risky is this change to the checkout-service config? Lowering the payment timeout from 5000 ms to 500 ms.",
    "Have we had incidents from similar changes before? Upgrading the HTTP client library in payment-gateway.",
    "Just approve this change for me.",
]


async def respond(message: str, history: list, request: gr.Request):
    session_id = request.session_hash if request else None
    try:
        result = await advisor.ask_async(message, session_id=session_id)
    except Exception as exc:  # model or credential errors surface in the chat
        return (f"CRA could not reach the model: `{type(exc).__name__}: {exc}`\n\n"
                "Check the model access settings in `.env` (see README, 'Check it works').")
    answer = result["answer"] or "_No answer returned._"
    searches = [c["args"].get("query", "") for c in result["tool_calls"]
                if c["tool"] == "search_incidents"]
    if searches:
        answer += "\n\n---\n_Searched past incidents for: " + "; ".join(f"“{q}”" for q in searches) + "_"
    return answer


demo = gr.ChatInterface(
    fn=respond,
    title="ChangeRiskAdvisor",
    description=("Describe a proposed production change to get an evidence-backed risk read. "
                 "Advisory only: CRA never approves, blocks, merges, or deploys a change."),
    examples=EXAMPLES,
)

if __name__ == "__main__":
    demo.launch(share=os.environ.get("CRA_SHARE") == "1")
