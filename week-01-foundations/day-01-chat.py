# week-01-foundations/day-01-chat.py

from llm import call_llm
# <-- THE list. Lives OUTSIDE the loop.This placement is the lesson
messages = []

while True:
    user_input = input("you: ")
    if user_input.strip().lower() in ("quit" , "exit"):
        break
    
    messages.append({"role":"user" , "content":user_input})
    out = call_llm(messages)
    print("claude: text",out["text"])
    print("claude: usage",out["usage"])
    messages.append({"role":"assistant" , "content": out["text"]})
    ##print("usage:" , {out["usage"]})