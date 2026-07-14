from anthropic import Anthropic
from config import ANTHROPIC_KEY

# module level init , happens once on import
client = Anthropic(api_key = ANTHROPIC_KEY) 

MODEL = "claude-sonnet-4-6"

def call_llm(messages, system=None, tools=None, max_tokens=1024):
    """The single choke point between this project and the provider API.
    Returns a normalized dict so the rest of the codebase never touches
    a raw Anthropic response object."""
    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system        # NOTE: top-level, NOT a message
    if tools is not None:
        kwargs["tools"] = tools

    response = client.messages.create(**kwargs)

    # response.content is a LIST OF BLOCKS, not a string. Walk it.
    text_parts = []
    tool_calls = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "tool_use":
            tool_calls.append({
                "id": block.id,
                "name": block.name,
                "input": block.input,
            })

    return {
        "text": "".join(text_parts),
        "tool_calls": tool_calls,
        "stop_reason": response.stop_reason,
        "raw_content": response.content,   # keep the raw blocks — Day 3 needs them
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }


if __name__ == "__main__":
    # Demo under the guard so `import llm` elsewhere doesn't fire this.
    out = call_llm([{"role": "user", "content": "Say hi in 5 words."}])
    print(out["text"])
    print("usage:", out["usage"])