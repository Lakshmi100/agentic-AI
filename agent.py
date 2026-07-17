# agent.py
import time
import logging
from llm import call_llm

log = logging.getLogger("agent")


class Agent:
    """A reusable agent: register tools, then .run(question).
    Consolidates Days 1-5 — statelessness, tool calling, the bounded loop,
    and robustness — into one reusable unit."""

    def __init__(self, system=None, max_iterations=10, max_api_retries=4):
        self.system = system
        self.max_iterations = max_iterations
        self.max_api_retries = max_api_retries
        self._schemas = []      # the model's view of the tools
        self._functions = {}    # your code's view of the tools

    def register_tool(self, schema: dict, fn):
        """Co-locate the two faces of a tool. schema is what the model sees;
        fn is what actually runs. Registered together so they can't drift."""
        self._schemas.append(schema)
        self._functions[schema["name"]] = fn

    # --- Day 5: robust API call ---
    def _call_with_retry(self, messages):
        for attempt in range(1, self.max_api_retries + 1):
            try:
                return call_llm(
                    messages,
                    system=self.system,
                    tools=self._schemas or None,
                )
            except Exception as e:
                if attempt == self.max_api_retries:
                    log.error(f"API failed after {self.max_api_retries}: {e}")
                    raise
                wait = 2 ** (attempt - 1)
                log.warning(f"API error (attempt {attempt}): {e} — retry in {wait}s")
                time.sleep(wait)

    # --- Day 5: tool failure is information, not a crash ---
    def _execute_tool(self, call):
        name, args = call["name"], call["input"]
        try:
            result = self._functions[name](**args)
            log.info(f"tool ok: {name}({args}) -> {result}")
            return str(result)
        except Exception as e:
            log.warning(f"tool FAILED: {name}({args}) -> {type(e).__name__}: {e}")
            return f"ERROR: {type(e).__name__}: {e}"

    # --- Days 1,3,4: the bounded agent loop ---
    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]

        for iteration in range(1, self.max_iterations + 1):
            log.info(f"--- iteration {iteration}")
            out = self._call_with_retry(messages)

            if out["stop_reason"] != "tool_use":
                return out["text"]

            messages.append({"role": "assistant", "content": out["raw_content"]})

            results = []
            for call in out["tool_calls"]:
                results.append({
                    "type": "tool_result",
                    "tool_use_id": call["id"],
                    "content": self._execute_tool(call),
                })
            messages.append({"role": "user", "content": results})

        return f"Stopped: hit max_iterations ({self.max_iterations})."