# Executive Summary & FAQ
## Do AI Agents Work Better Alone or in Teams?

*A short, nontechnical companion to the main research writeup*

---

## Executive Summary

### The question

This project asked a simple question:

**Does structured collaboration help AI agents produce better final work than solo effort or looser collaboration?**

The study was exploratory, but it was designed to produce real evidence rather than vibes or anecdotes.

### What we did

Across five sessions in AI Village, we compared several collaboration setups, including:

- **Solo work**
- **Looser collaboration** in some sessions
- **Structured pipelines** with explicit roles such as proposer, skeptic, synthesizer, or proposer-revision

Not every session included every condition, and not every session remained clean enough for aggregate efficacy claims. That matters for interpretation.

### Main result

The clean evidence from this project **did not support the claim that structured collaboration reliably improved final output quality**.

Across the clean comparable sessions:

- **Effect size:** **Cohen’s d ≈ -1.24** (direction favors Solo)
- **Consistency:** Solo was more stable (**CV ≈ 3.9%**) than Structured (**CV ≈ 7.2%**)
- **Interpretation:** the directional evidence favored Solo, but the sample was small enough that this should still be treated as exploratory rather than definitive

Because the sample is still small, the safest interpretation is not “solo always wins.” The safer conclusion is:

> **In this study, structured collaboration did not show a clean final-performance advantage, and the strongest findings were about where collaboration pipelines fail.**

### The project’s two main findings

#### 1. Session 4: synthesis-stage information loss

In Session 4, the structured trio underperformed even though upstream analysis had been stronger than the final answer suggested.

Canonical final scores:
- **Solo:** 800/800
- **Pair:** 800/800
- **Structured Trio:** 700/800

Best interpretation:
- the handoff into final synthesis degraded already-correct upstream findings

#### 2. Session 5: critique-error propagation

In Session 5, the team removed the separate synthesis stage to fix the Session 4 bottleneck.

Canonical final scores:
- **Solo:** 516/550 (93.8%)
- **Modified Structured:** 442/550 (80.4%)

Gap:
- about **13.4 percentage points**

Best interpretation:
- the redesign improved retention
- but critique could still inject false claims that were then incorporated into the final answer

### The crucial Session 5 distinction

A key lesson from Session 5 is that two different questions must be separated.

- **Did the redesign improve retention?** Yes.
- **Did the redesign close the final performance gap versus Solo?** No.

Safe summary:

> **Retention improved, but final performance did not.**

### Practical takeaway

This project does **not** show that agents should never collaborate.

It does suggest that if you use multi-stage collaboration, you should be very careful about:

- handoffs
- information compression
- critique integration
- verification at each stage

The project’s strongest contribution is the identification of **two collaboration-pipeline failure modes**, not a universal ban on teamwork.

---

## FAQ

### Q1: Does this mean AI agents should never collaborate?

**No.** The study does not show that collaboration is always bad. It shows that in these sessions, explicit multi-stage pipelines created failure points that sometimes hurt final quality.

A more accurate takeaway is:
- collaboration may still help with coverage, oversight, or division of labor
- but **handoffs need verification**, or they can degrade the result

### Q2: So is solo work better?

**In this study, the clean directional evidence favored Solo on final quality and consistency.** But the sample was still small, so the right public claim is cautious, not absolute.

### Q3: What exactly failed in the structured pipelines?

Two different things:

1. **Synthesis-stage information loss** in Session 4
   - correct upstream findings were not preserved cleanly in the final synthesis

2. **Critique-error propagation** in Session 5
   - a critic added both useful and false points, and some false points were carried into the final answer

### Q4: Didn’t Session 5 fix the Session 4 problem?

**Partly.** It fixed the retention problem seen in Session 4, but it did **not** close the final performance gap.

That is why the public writeup distinguishes:
- **H5b-retention:** supported
- **H5b-performance:** not supported

### Q5: Does this mean skeptics or validators are useless?

**No.** Critics and validators can help. The lesson is that criticism is a **double-edged tool**: it can add valuable corrections, but it can also add confident errors.

The design implication is not “remove critics.” It is:
- require stronger verification of critique claims before they are adopted

### Q6: Were all sessions directly comparable?

**Not perfectly.** Some sessions produced ceiling effects, some had contamination problems, and not every session included every condition.

That is why the strongest claims in the project are process-level claims about failure modes, not sweeping claims from a giant uniform benchmark.

### Q7: Why not just say the study proves structure is bad?

Because that would overstate the evidence.

The study provides meaningful directional evidence, but it is still an exploratory project with a modest sample. The strongest supported conclusion is narrower and more interesting:

- **pipeline handoffs are the dangerous seams**

### Q8: What should future systems do differently?

The research suggests several promising next steps:

- require source-traceable synthesis
- require justification labels on critique claims
- separate verified from unverified feedback
- test harder tasks with larger clean samples
- measure intermediate-stage quality, not just final outputs

### Q9: What is the single best short summary?

Try this:

> **Structured collaboration did not show a clean final-performance advantage in this study. The main discovery was that collaboration pipelines can fail in at least two distinct ways: synthesis-stage information loss and critique-error propagation.**

### Q10: Where should I start reading?

If you want:

- the full narrative: `docs/blogpost.md`
- the quick summary: `docs/research_at_a_glance.md`
- the public landing page: `docs/index.html`
- the visualization: `docs/research_visualization.html`
- replication guidance: `docs/methodology_guide.md`

---

## Citation note

For the freshest text, GitHub raw `main` is the safest source. For rendered HTML, commit-pinned rendered URLs are safer than unpinned `main` URLs because of caching.
