# week-01-foundations/day-06-agent-class.py
import logging
from agent import Agent
from tools import TOOLS, TOOL_FUNCTIONS

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt="%H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)   # quiet the HTTP noise

agent = Agent(system="You are a concise, helpful assistant.")

# register each tool: schema + its function, co-located
for schema in TOOLS:
    agent.register_tool(schema, TOOL_FUNCTIONS[schema["name"]])

#print(agent.run("What is 15 times 23, then multiply that result by 2?"))
print(agent.run("What time is it, and what is 100 divided by 0?"))