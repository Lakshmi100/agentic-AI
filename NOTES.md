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

## Day 5
- Done: API retry w/ exponential backoff, structured logging, tool errors caught -> fed back as tool_result
- Surprised: divide-by-zero didn't crash the agent — model READ the ZeroDivisionError and explained it; failure became information
- Layering: retry(API) -> try/except(tool) -> model reasoning, each catches what the layer below can't
- Next: Day 6 — consolidate everything into a reusable Agent class (agent.py)

## Day 6 — Week 1 capstone
- Done: Agent class in agent.py — register_tool co-locates schema+fn (anti-drift), run() encapsulates the loop
- Consolidated Days 1-5: statelessness, tool calling, tool_use_id, bounded loop, retry/backoff, errors-as-information
- Capstone verified: one .run() handled parallel tools + a live tool failure + coherent final answer
- Next: Week 2 — memory & context management (the input_tokens growth curve from Day 1 comes due)
## Add-on: get_weather tool 
- Built get_weather (Open-Meteo, no API key): geocode name/zip -> lat/lon, then current conditions 
- Bug: model kept sending "Atlanta, GA" with a comma -> geocoder returned empty -> ERROR string 
- Root cause : the TOOL DESCRIPTION's example had the comma; model imitated it. Fixed the example at the source, kept a defensive split(",") too 
- to make sure ,it just uses Atlanta and not Atlanta,GA . But now ambiquity weighs in as Atlanta ,GA is the popular one and we escape there , 'Springfiled' would be a gamble 
- Lesson: the model treats tool descriptions/examples as instructions — a misleading example is a bug 
- Note: bare "Atlanta" geocodes ambiguously (matched a dam); admin1 filter would pin the city if needed - need to debug on this too  
- Note : couple issues to resolves in the code , 30004 resolves to Murcia,Murcia and not Alpharetta, GA even after tool description/example fixed to say US
- City and state or US zip code - need to come back again to check on this.

## Week 2, Day 1 — token meter
- Done: per-call in/out meter + cumulative_input_billed; TRUNCATED flag on stop_reason==max_tokens
- Growth law measured: typed 5 words on turn 3, billed in=369 (whole history resent). Cumulative 15->81->450->978 = quadratic staircase
- Verified flag both directions (forced low max_tokens -> fired mid-sentence; restore -> clears)
- Aside: verbose replies inflate out= and every later in= — chatty history is expensive to carry
- Next: Day 2 — sliding window: flattens cost, silently destroys memory

## Week 2, Day 2 — sliding window
- Done: window = messages[-K:] sent, full list still appended; meter shows "sent X of Y"
- Experiment: planted fact turn 1, buried it, probed at "sent 4 of 9" — fact was never in the payload
- Model said "you never told me" and WASN'T lying — truthful about the 4 msgs it actually got
- Subtlety: in= still drifted up — window bounds msg COUNT not tokens; one 693-tok reply inflated it. Prod windows on token budget
- Lesson: window fixes cost by destroying memory, indiscriminately (drops the fact and "lol ok" alike)
- Next: Day 3 — compaction: summarize the old instead of dropping it

