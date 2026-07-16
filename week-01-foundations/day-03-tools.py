# week-01-foundations/day-03-tools.py
from datetime import datetime
from llm import call_llm
from tools import get_current_time, calculator , TOOLS, TOOL_FUNCTIONS

# --- the real functions (the model NEVER touches these) ---

def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression: str) -> str:
    # NOTE: eval() is a deliberate security hole — Week 10 fixes it properly.
    return str(eval(expression))

# --- their schemas (what the model sees INSTEAD of the code) ---

TOOLS = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "calculator",
        "description": "Evaluates a basic arithmetic expression, e.g. '2 + 2 * 10'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The arithmetic expression to evaluate."}
            },
            "required": ["expression"],
        },
    },
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculator": calculator,
}

# --- one round trip ---

#question = "What time is it right now?"
question = "What is 1234 times 5678?"
messages = [{"role": "user", "content": question}]

out = call_llm(messages, tools=TOOLS)
print("stop_reason:", out["stop_reason"])
print("tool_calls:", out["tool_calls"])

if out["stop_reason"] == "tool_use":
    # 1. append the model's FULL turn — raw_content, not just text.
    #    (its turn may contain narration text AND the tool request together)
    messages.append({"role": "assistant", "content": out["raw_content"]})

    # 2. execute each requested tool for real
    results = []
    for call in out["tool_calls"]:
        fn = TOOL_FUNCTIONS[call["name"]]
        result = fn(**call["input"])          # Day 2's ** unpacking again!
        print(f"executed {call['name']}({call['input']}) -> {result}")
        results.append({
            "type": "tool_result",
            "tool_use_id": call["id"],        # <-- must match the request's id
            "content": result,
        })

    # 3. hand the results back as a single user message, then call again
    messages.append({"role": "user", "content": results})
    final = call_llm(messages, tools=TOOLS)
    print("FINAL:", final["text"])
else:
    print("Model answered directly:", out["text"])