from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="cra_hello",
    model="gemini-2.5-flash",
    instruction=(
        "You are the ChangeRiskAdvisor (CRA) hello agent. "
        "Reply in one short sentence and state you are not yet wired to tools."
    ),
)
