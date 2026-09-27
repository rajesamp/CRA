"""Run one question through the CRA agent and collect the answer and tool calls.

Shared by the Gradio app (app.py) and the evidence script
(scripts/run_evidence.py).
"""

import asyncio
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

APP_NAME = "cra"
USER_ID = "raj-sam"


class Advisor:
    """Holds one ADK runner; each session_id is a separate conversation."""

    def __init__(self, agent=None):
        if agent is None:
            from agent import root_agent as agent
        self.runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
        self._sessions: set[str] = set()

    async def _ensure_session(self, session_id: str):
        if session_id not in self._sessions:
            await self.runner.session_service.create_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=session_id
            )
            self._sessions.add(session_id)

    async def ask_async(self, question: str, session_id: str | None = None) -> dict:
        session_id = session_id or uuid.uuid4().hex
        await self._ensure_session(session_id)
        message = types.Content(role="user", parts=[types.Part(text=question)])
        answer, tool_calls = [], []
        async for event in self.runner.run_async(
            user_id=USER_ID, session_id=session_id, new_message=message
        ):
            for part in (event.content.parts if event.content else None) or []:
                if part.function_call:
                    tool_calls.append({"tool": part.function_call.name,
                                       "args": dict(part.function_call.args or {})})
                elif part.text and event.author != "user":
                    answer.append(part.text)
        return {"session_id": session_id, "answer": "".join(answer).strip(),
                "tool_calls": tool_calls}

    def ask(self, question: str, session_id: str | None = None) -> dict:
        return asyncio.run(self.ask_async(question, session_id))
