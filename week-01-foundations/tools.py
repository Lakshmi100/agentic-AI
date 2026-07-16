# tools/ functions moved in this tools.py
from datetime import datetime
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