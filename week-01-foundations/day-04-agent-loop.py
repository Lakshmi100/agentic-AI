# week-01-foundations/day-04-agent-loop.py
from llm import call_llm
from tools import get_current_time, calculator , TOOLS, TOOL_FUNCTIONS
# ... get_current_time, calculator, TOOLS, TOOL_FUNCTIONS same as Day 3 ...

MAX_ITERATIONS = 10   # NOT decoration. Models can loop forever on impossible
# tasks — this is the money-and-sanity fuse.

def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        out = call_llm(messages, tools=TOOLS)
        print(f"\n--- iteration {iteration} | stop_reason: {out['stop_reason']}")

        if out["stop_reason"] != "tool_use":
            return out["text"]              # model is done — final answer

        # model requested tools: append its full turn first
        messages.append({"role": "assistant", "content": out["raw_content"]})

        # execute ALL requested calls this turn — not just the first
        results = []
        for call in out["tool_calls"]:
            fn = TOOL_FUNCTIONS[call["name"]]
            result = fn(**call["input"])
            print(f"    {call['name']}({call['input']}) -> {result}")
            results.append({
                "type": "tool_result",
                "tool_use_id": call["id"],
                "content": result,
            })

        # ALL results go back in ONE user message (API requirement)
        messages.append({"role": "user", "content": results})

    return f"Stopped: hit MAX_ITERATIONS ({MAX_ITERATIONS}) without a final answer."


if __name__ == "__main__":
    #print("FINAL:", run_agent("What is 1234 * 5678, and what time is it right now?"))
    #print("FINAL:", run_agent("Take 15 times 23, then multiply that result by 2."))
    #print("FINAL:", run_agent("what is (15 * 23) * 2   "))
    #print("FINAL:", run_agent("What is the weather in Chennai Tamilnadu "))
    print("FINAL:", run_agent("What is the Weather for 30004"))
    
    