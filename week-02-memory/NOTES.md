
## Week 2, Day 2 — sliding window
- Done: window = messages[-K:] sent, full list still appended; meter shows "sent X of Y"
- Experiment: planted fact turn 1, buried it, probed at "sent 4 of 9" — fact was never in the payload
- Model said "you never told me" and WASN'T lying — truthful about the 4 msgs it actually got
- Subtlety: in= still drifted up — window bounds msg COUNT not tokens; one 693-tok reply inflated it. Prod windows on token budget
- Lesson: window fixes cost by destroying memory, indiscriminately (drops the fact and "lol ok" alike)
- Next: Day 3 — compaction: summarize the old instead of dropping it
