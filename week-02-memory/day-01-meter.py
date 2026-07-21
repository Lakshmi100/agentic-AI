# week-02-memory/day-01-meter.py
from llm import call_llm

messages = []
cumulative_input = 0   # the number that tells the real story

while True:
    user_input = input("you: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})
    out = call_llm(messages , max_tokens = 1024)

    in_toks  = out["usage"]["input_tokens"]
    out_toks = out["usage"]["output_tokens"]
    cumulative_input += in_toks

    # --- the meter line ---
    flag = "  ⚠️ TRUNCATED" if out["stop_reason"] == "max_tokens" else ""
    print(f"  [meter] in={in_toks}  out={out_toks}  cumulative_input_billed={cumulative_input}{flag}")

    print("claude:", out["text"])
    messages.append({"role": "assistant", "content": out["text"]})