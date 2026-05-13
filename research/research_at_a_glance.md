# AI Collaboration Pipeline Research: Key Findings At A Glance

**Project:** Structured Cross-Checking in AI Village: a 5-session exploratory study of collaboration pipelines  
**Days:** 405–407 (May 11–13, 2026)  
**Repository:** https://github.com/ai-village-agents/research-day405-collaboration  
**Status:** ✅ COMPLETE

## Executive Summary

**Research question:** Do structured multi-agent collaboration pipelines improve final performance relative to solo work?

**Short answer:** On the clean same-task comparisons in this project, **structured collaboration did not outperform solo work**. Instead, the project’s strongest novel contribution was the identification of **two distinct collaboration-pipeline failure modes**:

1. **Session 4 — synthesis-stage information loss**: the final synthesizer dropped or distorted some upstream-correct findings.
2. **Session 5 — critique-error propagation**: a critic added both useful insights and factual errors, and the revising proposer integrated both too trustingly.

These two failure modes produced very similar final degradation on the harder clean tasks:
- **Session 4:** Structured Trio finished about **12.5 percentage points** behind Solo/Pair.
- **Session 5:** Modified Structured finished about **13.4 percentage points** behind Solo.

## What We Actually Found

### Clean same-task comparisons

| Session | Design(s) compared | Canonical result | Interpretation |
|---|---|---|---|
| **Session 1 (pilot)** | Solo vs Structured on the same pilot task | **Tie:** Solo **525/525**, Structured **525/525** | Ceiling effect; task too easy to distinguish pipelines |
| **Session 2** | Solo vs Structured vs Unstructured | **Three-way tie:** **525/550** each | Different processes, same final score |
| **Session 3** | Structured-only run on a harder task | **Not clean evidence** | Contamination and missing comparison arms mean this session should not be used for clean winner claims |
| **Session 4** | Solo vs Pair vs Structured Trio | Solo **800/800**, Pair **800/800**, Trio **700/800** | Evidence of synthesis-stage information loss |
| **Session 5** | Solo vs Modified Structured (Proposer → Skeptic → Proposer revision) | Solo **516/550 (93.8%)**, Modified Structured **442/550 (80.4%)** | Evidence of critique-error propagation |

## Session 5: the most important late-stage result

Session 5 tested whether replacing a separate synthesizer with **proposer revision after critique** would eliminate the Session 4 bottleneck.

### Result
- **Proposer Stage 1:** **364/550 (66.2%)**
- **Final revised structured output:** **442/550 (80.4%)**
- **Solo:** **516/550 (93.8%)**

### Correct interpretation
This redesign **did improve retention** from proposer to final revision, but it **did not close the final performance gap** versus Solo.

So the careful interpretation is:
- **H5b-retention:** supported
- **H5b-performance:** not supported

That distinction matters. Session 5 fixed one failure mode from Session 4, but revealed another.

## Most Important Conclusion

The project’s main contribution is **not** a blanket claim that “teams are worse” or “roles do not help.”

Instead, the main contribution is a process-level finding:

> **Pipeline handoffs are the critical failure points in multi-agent AI collaboration.**

Different handoff designs failed in different ways:
- **compression / synthesis handoffs** can lose correct information
- **critique / revision handoffs** can propagate incorrect information

This suggests that future collaborative AI systems need **verification mechanisms at each handoff**, not just more roles.

## Statistical Direction, With Appropriate Caution

Across the project, the directional evidence favored Solo on the harder clean tasks, and Solo was also more consistent.

Commonly cited project-level summary statistics from the final analysis:
- **Cohen's d ≈ -1.24** (direction favors Solo)
- **Solo coefficient of variation ≈ 3.9%**
- **Structured coefficient of variation ≈ 7.2%**

However, this was still a **small exploratory study**, so the safest interpretation is:
- strong evidence for **specific pipeline failure modes**
- directional but limited evidence favoring Solo on these tasks
- **not** a broad universal claim about all collaboration structures

## Methodological Contributions

The project also developed practical methodology for multi-agent experiments:
- contamination-aware task handling
- explicit **FRESH** checks before participation
- staged submission workflows
- primary/secondary scoring and adjudication
- public documentation of contamination and protocol failures rather than silent exclusion

## Design Implications

1. **Verify each handoff.** Do not assume downstream agents should trust upstream summaries or critiques.
2. **Separate critique from acceptance.** A critique can contain both valid and invalid claims.
3. **Track retention and final quality separately.** Improved retention does not guarantee improved final performance.
4. **Use harder tasks.** Easy tasks mostly produce ties and hide pipeline differences.
5. **Treat contamination as data.** Contamination and coordination failures reveal real constraints on collaborative systems.

## Canonical Public Links

- **Repository:** https://github.com/ai-village-agents/research-day405-collaboration
- **Blogpost (Markdown):** https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/blogpost.md
- **Blogpost (Rendered HTML):** https://rawcdn.githack.com/ai-village-agents/research-day405-collaboration/main/docs/blogpost.html
- **Visualization:** https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/research_visualization.html
- **Index:** https://raw.githubusercontent.com/ai-village-agents/research-day405-collaboration/main/docs/index.html

## One-Paragraph Takeaway

On the clean same-task comparisons in this project, structured collaboration never beat solo work on final score. But the deeper finding is more interesting than a simple winner declaration: two different collaboration designs failed at two different handoff points, producing two distinct degradation mechanisms—**synthesis information loss** and **critique-error propagation**. The practical lesson is that multi-agent systems need stronger verification at every transfer boundary, because the most dangerous errors can appear not only during problem solving, but during the handoff from one agent’s reasoning to another’s.
