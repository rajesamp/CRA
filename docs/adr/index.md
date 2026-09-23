# Architecture Decision Records — ChangeRiskAdvisor

Lives in the CRA repo (github.com/rajesamp/CRA). Statuses flip from Proposed to
Accepted as each decision is implemented.

| ADR | Decision | Status |
|---|---|---|
| [ADR-001](adr-001-google-adk.md) | Google ADK over LangGraph / raw Gemini API | Proposed |
| [ADR-002](adr-002-rag-stack.md) | ChromaDB + FunctionTool over Vertex Knowledge Engine | Proposed |
| [ADR-003](adr-003-memory.md) | DatabaseSessionService + `user:` state over Memory Bank | Proposed |
| [ADR-004](adr-004-guardrails.md) | ADK callbacks over separate classifier layer | Proposed |
| [ADR-005](adr-005-mcp-vs-functiontools.md) | FastMCP server over plain FunctionTools | Proposed |
| [ADR-006](adr-006-deployment.md) | Hardened Cloud Run over ADK Agent Runtime | Proposed |

Format: MADR-lite (Status / Context / Decision / Alternatives / Consequences).
Template: [adr-template.md](adr-template.md). Running notes live in
[architecture-journal.md](architecture-journal.md).
