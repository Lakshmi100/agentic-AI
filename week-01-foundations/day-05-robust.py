# week-01-foundations/day-05-robust.py
import time
import logging
from anthropic import APIError, APITimeoutError, RateLimitError
from llm import call_llm
from tools import TOOLS, TOOL_FUNCTIONS

# --- structured logging: one line per meaningful step ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("agent")

MAX_ITERATIONS = 10
MAX_API_RETRIES = 4


def call_llm_with_retry(messages, tools=None):
    """Layer 1+2: retry transient API failures with exponential backoff."""
    for attempt in range(1, MAX_API_RETRIES + 1):
        try:
            return call_llm(messages, tools=tools)
        except (RateLimitError, APITimeoutError, APIError) as e:
            if attempt == MAX_API_RETRIES:
                log.error(f"API failed after {MAX_API_RETRIES} attempts: {e}")
                raise
            wait = 2 ** (attempt - 1)          # 1s, 2s, 4s, 8s
            log.warning(f"API error (attempt {attempt}): {e} — retrying in {wait}s")
            time.sleep(wait)


def execute_tool(call):
    """Layer 3: a tool failure is INFORMATION, not a crash.
    Catch, package the error as the result, hand it back to the model."""
    name, args = call["name"], call["input"]
    try:
        result = TOOL_FUNCTIONS[name](**args)
        log.info(f"tool ok: {name}({args}) -> {result}")
        return str(result)
    except Exception as e:
        log.warning(f"tool FAILED: {name}({args}) -> {type(e).__name__}: {e}")
        # this string goes back to the model AS the tool_result
        return f"ERROR: {type(e).__name__}: {e}"


def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        log.info(f"--- iteration {iteration}")
        out = call_llm_with_retry(messages, tools=TOOLS)

        if out["stop_reason"] != "tool_use":
            log.info("model produced final answer")
            return out["text"]

        messages.append({"role": "assistant", "content": out["raw_content"]})

        results = []
        for call in out["tool_calls"]:
            result_text = execute_tool(call)     # never raises past here
            results.append({
                "type": "tool_result",
                "tool_use_id": call["id"],
                "content": result_text,
            })

        messages.append({"role": "user", "content": results})

    return f"Stopped: hit MAX_ITERATIONS ({MAX_ITERATIONS})."


#if __name__ == "__main__":
#    print("FINAL:", run_agent("What is 1234 * 5678?"))
if __name__ == "__main__":
    print("FINAL:", run_agent("What is 10 divided by 0?"))