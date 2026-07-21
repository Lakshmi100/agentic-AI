# week-02-memory/day-02-window.py
from llm import call_llm

WINDOW = 4   # send only the last K messages. Small, so it slides fast in testing.

messages = []            # the FULL record — always append, never trim
cumulative_input = 0

while True:
    user_input = input("you: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    # --- THE ONE CHANGE: send only the tail, not the whole history ---
    windowed = messages[-WINDOW:]
    out = call_llm(windowed)

    in_toks  = out["usage"]["input_tokens"]
    out_toks = out["usage"]["output_tokens"]
    cumulative_input += in_toks
    
    print(f"  [meter] in={in_toks}  out={out_toks}  cumulative={cumulative_input}  "
        f"(sent {len(windowed)} of {len(messages)} msgs)")
    print("claude:", out["text"])
    messages.append({"role": "assistant", "content": out["text"]})