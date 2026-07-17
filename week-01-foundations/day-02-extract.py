import json
from pydantic import BaseModel
from llm import call_llm

"""
# Person definition initially
class Person(BaseModel):
    name: str
    age: int
    email: str

"""
class Person(BaseModel):
    name: str
    age: int
    email: str | None = None

# this is a system prompt or just a prompt you send to your
#call_llm funciton call , tweak this prompt by removing
# this statement "No code fences. No markdown . "
# and then check your trace messages

SYSTEM = """ You extract structured data from text .
Respond with ONLY a JSON object matching this schema:
{"name": string , "age": integer, "email": string} 
No other text. No code fences. No markdown . 
If a field is not present in the input, use null for it. 
Never invent values."""

# text = "Rajesh kumar is 40 years old, reach him at rajesh.k@example.com"
text = "Rajesh kumar is 40 years old, reach him at "

def strip_fences(text: str) -> str:
    """Remove markdown code fences if present. Deterministic repair — runs every time."""
    text = text.strip()
    if text.startswith("```"):
        # drop the first line entirely (``` or ```json)
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1:]
        # drop the trailing fence
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    return text.strip()


MAX_ATTEMPTS = 3

messages = [{"role": "user", "content": text}]
person = None

for attempt in range(1, MAX_ATTEMPTS + 1):
    out = call_llm(messages, system=SYSTEM)
    raw = out["text"]
    print(f"--- attempt {attempt} RAW:", repr(raw))

    try:
        data = json.loads(strip_fences(raw))   # cheap repair: EVERY attempt
        #data = json.loads(raw)   # call without strip fences
        person = Person(**data)
        break                                   # success — exit the loop
    except (json.JSONDecodeError, Exception) as e:
        # feed the failure back: the model sees its own output AND the error
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user","content": f"Your response failed with this error:\n{e}\n"
                                    f"Return ONLY corrected JSON matching the schema."})

if person:
    print("PARSED:", person)
else:
    print("FAILED after", MAX_ATTEMPTS, "attempts")
