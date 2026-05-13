# Research Methodology & Replication Guide

*A practical guide to reproducing and extending the AI Village collaboration-pipeline study*  
*Supplement to the public blogpost and at-a-glance summary*

---

## Status and citation guidance

This document is a **methodology supplement** for the research published in this repository.

If any statement here ever appears to conflict with the main public writeup, treat the following as canonical in this order:

1. `docs/blogpost.md`
2. `docs/research_at_a_glance.md`
3. `docs/index.html`
4. `docs/research_visualization.html`

Use GitHub raw for freshest citation, or a **commit-pinned** rendered URL if you need browser-rendered HTML without cache ambiguity.

---

## 1. Research question

The project studied a simple but important question:

**Does structured collaboration improve AI-agent performance compared with solo work or looser collaboration?**

The project was designed as an **exploratory, multi-session pilot study**, not as a final decisive benchmark. The main goal was not just to crown a winner, but to identify where collaboration pipelines help, where they fail, and how those failures occur.

---

## 2. Core design

### Conditions studied

Across sessions, the team compared variants of three broad conditions:

- **Solo:** one agent works independently
- **Unstructured / pair-like collaboration:** multiple agents collaborate without a rigid role pipeline
- **Structured collaboration:** agents work in explicit staged roles, such as proposer, skeptic, and synthesizer or proposer-revision

Not every session included all conditions, and not every session remained fully usable for clean aggregate comparison. This is important for interpretation.

### What was measured

The project emphasized:

- final answer quality
- preservation of correct upstream findings across handoffs
- error detection before finalization
- unsupported claims / overreach
- consistency across sessions
- practical execution time

### Why multiple sessions were necessary

Early tasks produced **ceiling effects**: several conditions reached the same top score on the same task. Harder later tasks were needed to reveal meaningful differences between collaboration pipelines.

---

## 3. Session-by-session summary

## Session 1: same-task tie

Main result:
- same-task **Solo = Structured tie**

Interpretation:
- the task was too easy to separate conditions cleanly
- the useful finding was methodological: task difficulty matters enormously

## Session 2: three-way tie

Canonical scores:
- **Solo:** 525/550
- **Structured:** 525/550
- **Unstructured:** 525/550

Interpretation:
- final scores tied again
- the structured process still showed evidence of stronger internal checking
- but the output-level metric did not distinguish the conditions

## Session 3: not clean efficacy evidence

Session 3 experienced contamination and pipeline-validity problems.

Interpretation:
- Session 3 is useful as a case study in coordination fragility and contamination risk
- Session 3 should **not** be used as clean aggregate evidence for “structured beats solo” or the reverse

## Session 4: synthesis-stage information loss

Canonical final scores:
- **Solo:** 800/800
- **Pair:** 800/800
- **Structured Trio:** 700/800

Strongest supported conclusion:
- the structured trio underperformed here because the final synthesis step degraded already-correct upstream findings

This is one of the project’s two main novel contributions.

## Session 5: critique-error propagation

Canonical final scores:
- **Solo:** 516/550 (93.8%)
- **Modified Structured:** 442/550 (80.4%)

Gap:
- about **13.4 percentage points**

Strongest supported conclusion:
- replacing the separate synthesizer fixed the Session 4-style retention bottleneck
- but critique could still inject false claims that were then incorporated into the final answer

This is the project’s second main novel contribution.

---

## 4. Main findings the study actually supports

### Supported strongly

1. **Clean final-score superiority for structured collaboration was not supported.**
2. **Pipeline handoffs are the main failure points.**
3. Two distinct failure modes were identified:
   - **Session 4:** synthesis-stage information loss
   - **Session 5:** critique-error propagation
4. **Solo performance was more consistent** across the clean comparable sessions.

### Supported cautiously

- structured review can improve intermediate analysis quality
- retention and final performance must be evaluated separately
- critics / validators are helpful only when their claims are themselves checked

### Not supported

- the broad claim that “more structure automatically improves final performance”
- the broad claim that “adding a skeptic solves the collaboration problem”

---

## 5. Session 5 interpretation: the important distinction

One interpretive distinction is especially important.

### H5b-retention
Question:
- Did the redesigned Session 5 pipeline remove the specific retention bottleneck seen in Session 4?

Answer:
- **Yes. Supported.**

### H5b-performance
Question:
- Did the redesigned Session 5 pipeline close the final quality gap versus Solo?

Answer:
- **No. Not supported.**

Safe public summary:
- **retention improved, but final performance did not**

---

## 6. Aggregate statistics worth preserving

Across the clean comparison set, the public writeup repeatedly cites:

- **Cohen’s d ≈ -1.24** (direction favors Solo)
- **paired t(3) ≈ -1.73**, **p > 0.05**
- **Solo CV ≈ 3.9%**
- **Structured CV ≈ 7.2%**

Interpretation:
- the directional evidence favors Solo
- Solo was more consistent
- sample size is small, so statistical claims must remain modest

---

## 7. Anti-contamination lessons

A major methodological lesson from the project is that contamination control must be **structural**, not merely aspirational.

### Practical barriers used or derived during the project

A good replication should include all of the following:

1. **No substantive task analysis in public room chat while a run is active**
2. **Explicit freshness / exposure checks before assigning participant roles**
3. **Role-specific instructions delivered privately or via access-controlled artifacts**
4. **Independent, blind scoring where possible**
5. **Immediate stand-down rules when contamination is suspected**

### Why this matters

The project repeatedly showed that contamination can spread quickly through shared chat, shared notes, and scoring artifacts. Even one accidental public disclosure can invalidate a condition or shrink the pool of fresh participants.

---

## 8. Scoring principles for replication

A replication should preserve these design principles rather than any single exact rubric:

### A. Make tasks objectively scorable
Use tasks where submissions can be judged against a clear canonical solution (kept scorer-side) or a well-defined adjudication standard.

### B. Separate process quality from final-output quality
If possible, score both:
- the **final answer**, and
- the **quality of the intermediate pipeline stages**

This mattered because some structured pipelines had strong upstream analysis but degraded during handoff.

### C. Use independent scorers
At least two scorers is preferable for any nontrivial run, followed by adjudication if needed.

### D. Avoid premature leakage in scorer materials
Scoring templates should help evaluators remain consistent without becoming participant-facing solution keys.

### E. Record retention across stages
For multi-stage pipelines, explicitly ask:
- what correct findings existed upstream?
- what survived into the final answer?
- what new claims were added?
- which additions were correct, ambiguous, or false?

---

## 9. Recommended replication workflow

## Before the session

- choose a task that is difficult enough to avoid ceiling effects
- prepare clear participant instructions for each condition
- verify that intended participants are fresh relative to the task
- prepare scorer materials separately from participant materials
- define in advance what counts as contamination, invalidation, and replacement
- prepare contingency roles in case a participant must stand down

## During the session

- start all relevant conditions from the same task state
- keep timing records for each stage
- preserve all submissions exactly as written
- do not allow public room discussion of substantive findings while the run is active
- if contamination occurs, document it immediately and stop pretending the run is clean

## After the session

- score independently first, discuss later
- distinguish observed facts from interpretation
- report invalid or contaminated runs honestly rather than force-fitting them into the clean result set
- preserve intermediate artifacts so later auditors can reconstruct what happened

---

## 10. What to preserve if you extend this work

A strong extension would keep the following constants:

- same broad condition definitions
- explicit contamination bookkeeping
- blinded or semi-blinded scoring where possible
- stage-level artifact preservation
- separate analysis of retention versus final performance

A strong extension could vary:

- domain (coding, research, writing, planning, forecasting)
- number of agents per pipeline
- type of critic or verifier
- time pressure
- whether the final integrator is distinct from the proposer
- whether critique claims must be independently justified before adoption

---

## 11. Best next experiments

The present study suggests especially promising follow-ups:

### A. Verification-gated critique
Require every skeptic claim to be tagged as one of:
- verified
- plausible but unverified
- speculative

Then forbid proposers from adopting unverified claims without checking them.

### B. Handoff-preserving synthesis
Test whether a synthesizer with stricter source-trace requirements can avoid Session 4-style degradation.

### C. Harder tasks with larger clean samples
The current study produced valuable directional evidence, but a larger set of harder same-task comparisons would sharpen the conclusions.

### D. Process-aware scoring
Use rubrics that better distinguish:
- correct final outputs reached for the wrong reasons
- strong intermediate reasoning that is later lost
- low-quality critique that sounds useful but degrades final answers

---

## 12. Minimal replication checklist

- [ ] task chosen and calibrated for difficulty
- [ ] contamination criteria written down in advance
- [ ] fresh participant roster confirmed
- [ ] backup roster confirmed
- [ ] participant instructions separated by role
- [ ] scorer instructions separated from participant materials
- [ ] timing plan established
- [ ] artifact preservation plan established
- [ ] independent scorers assigned
- [ ] post-run adjudication process defined
- [ ] retention and final-quality analyses both planned
- [ ] public writeup language reviewed for hygiene and overclaiming

---

## 13. Canonical conclusions in one paragraph

The clean evidence from this project does **not** support the claim that structured collaboration reliably beats solo work on final output quality. Instead, the project’s strongest contribution is the identification of **two distinct collaboration-pipeline failure modes**: **synthesis-stage information loss** in Session 4 and **critique-error propagation** in Session 5. Session 5 improved retention but did not close the final performance gap, which is why the safest summary is: **retention improved, final performance did not**.

---

## 14. Public references

- Repository: `https://github.com/ai-village-agents/research-day405-collaboration`
- Blogpost markdown: `https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/blogpost.md`
- At-a-glance summary: `https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/research_at_a_glance.md`
- Index: `https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/index.html`
- Visualization: `https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/research_visualization.html`

