## Day 0
- Done: venv (resolved conda PATH shadowing), editable install, .env/config.py, sanity check passed
- Surprised: Anaconda was silently shadowing python3.12 in PATH — had to use absolute path
- Next: Day 1 — llm.py wrapper + statelessness demo

## Day 1
- Done: llm.py wrapper (normalized dict), chat loop, statelessness experiment
- Surprised: "memory" was never in the model — moving messages=[] one line killed it
- Next: Day 2 — structured outputs, Pydantic validation, retry-with-feedback loop

## Day 2
- Done: JSON extraction -> Pydantic, strip_fences repair, retry-with-feedback loop
- Surprised: retry loop pressured an honest null into a fabricated "" — green gate, false data; schema str|None legalized honesty
- Next: Day 3 — tool calling, one round trip (get_current_time, calculator)

## Day 3
- Done: tool schemas, one round trip, clock (unfakeable) + calculator (structured args)
- Important to note : model never executes anything — it requests and waits; my code is the hands

## Day 4
- Done: if -> while (bounded), multi-tool turns, parallel + sequential experiments
- Important to Note: tool_use_id is a correlation key — obvious the moment two results travel in one message; iteration 2 built "345 * 2" from a value born at runtime
- Next: Day 5 — robustness: retries, timeouts, feeding tool errors back

