from config import ANTHROPIC_KEY
from anthropic import Anthropic

client = Anthropic(api_key=ANTHROPIC_KEY)
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[{"role": "user", "content": "hello"}]
)
print(response.content[0].text)