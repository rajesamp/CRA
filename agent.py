from pathlib import Path

from google.adk.agents import LlmAgent

try:
    from .cra.rag import search_incidents
except ImportError:  # imported as a top-level module (tests, scripts)
    from cra.rag import search_incidents

INSTRUCTION = (Path(__file__).parent / "cra" / "prompts" / "system_prompt.md").read_text()

root_agent = LlmAgent(
    name="change_risk_advisor",
    model="gemini-2.5-flash",
    description="Advisory-only pre-deployment change-risk assessment with cited evidence.",
    instruction=INSTRUCTION,
    tools=[search_incidents],
)
