# Glossary & Key Terms

A reference guide to statistical, methodological, and study-specific terms used in the public research writeup.

This glossary is meant to help readers understand the project without introducing stronger claims than the main documents support.

---

## Statistical and measurement terms

### Cohen's d
A standardized effect-size measure describing the difference between two groups in standard-deviation units.

In this project, the public writeup reports **Cohen's d ≈ -1.24** for the clean structured-versus-solo comparison set. The negative sign means the direction favored **Solo** under the convention used there.

Interpretation:
- near 0 = little difference
- larger absolute values = larger separation
- the sign tells you the direction under the chosen group ordering

---

### Coefficient of variation (CV)
A standardized measure of variability: roughly, how large the spread is relative to the mean.

In this project, the public writeup repeatedly cites:
- **Solo CV ≈ 3.9%**
- **Structured CV ≈ 7.2%**

Interpretation:
- lower CV = more consistent performance
- higher CV = more variable performance

---

### Confidence interval (CI)
A range used to express uncertainty around an estimate.

A confidence interval is best treated as a compact summary of uncertainty, not as a guarantee that the true value lies inside the interval.

---

### Effect size
A quantitative description of how large a difference is, rather than just whether it is statistically detectable.

Why it matters here:
- small studies can show large effects without reaching conventional significance thresholds
- effect size can therefore be informative even when a p-value is not decisive

---

### p-value
A quantity used in hypothesis testing to ask how surprising the observed data would be under a specified null model.

In this project, the safest public use of p-values is limited and cautious because the clean comparison set is small.

---

### Standard deviation (SD)
A common measure of spread around a mean.

Lower SD means scores cluster more tightly. Higher SD means they are more dispersed.

---

## Methodological terms

### Blinded scoring
Scoring performed without knowing which condition produced a submission.

Why it matters:
- it reduces bias during evaluation
- it helps keep scoring focused on the artifact rather than the condition label or author identity

---

### Ceiling effect
A situation where a task is too easy, so multiple conditions hit the top of the scale and become hard to distinguish.

This mattered in the early sessions of the project, where tied top-level scores limited what could be learned from final outputs alone.

---

### Condition
One of the comparison setups in an experiment.

Examples from this project include:
- **Solo**
- **Unstructured / pair-like collaboration**
- **Structured collaboration** with explicit pipeline roles

---

### Contamination
Information leakage that undermines a clean comparison between conditions.

Examples:
- a participant sees another condition's solution ideas before completing their own run
- a shared artifact exposes solution details to agents who were supposed to remain fresh
- a scorer learns condition identity when the design intended blind scoring

Why it matters:
- contamination can make a run uninterpretable as clean efficacy evidence

---

### Fresh / exposed
Practical contamination-status labels used during the study.

- **Fresh** = suitable for participant roles on the task in question
- **Exposed** = already saw enough task-related information that clean participation was no longer appropriate

---

### Handoff
A transfer point between stages or roles in a collaboration pipeline.

This project found that handoffs were often the most important failure points.

---

### Hypothesis
A testable claim the researchers try to evaluate.

Important caution for this project:
- some hypotheses evolved in interpretation as new sessions clarified that different mechanisms could produce similar performance gaps

---

### Replication
Repeating a study, either closely or conceptually, to see whether the findings hold up.

Two broad types:
- **direct replication**: stay close to the original design
- **conceptual replication**: test the same idea with different tasks, agents, or environments

---

### Rubric
A structured scoring guide used to evaluate outputs consistently.

A good rubric makes it easier for multiple scorers to judge submissions in comparable ways.

---

### Sample size
The amount of data available for inference.

This project was exploratory and had a modest clean comparison set, so sample-size limits are central to interpretation.

---

## Study-specific terms

### Critique-error propagation
One of the two main failure modes identified in the project.

Meaning:
- a critique stage adds both correct and incorrect claims
- downstream integration carries some of the incorrect claims into the final answer

This was the key Session 5 finding.

---

### H5b-retention
A Session 5 interpretation question:
- did the redesigned pipeline improve retention relative to the Session 4 bottleneck?

Public answer:
- **supported**

---

### H5b-performance
A second Session 5 interpretation question:
- did the redesigned pipeline close the final performance gap versus Solo?

Public answer:
- **not supported**

This distinction is crucial. The redesign improved retention without closing the final-quality gap.

---

### Information retention
How much correct upstream content survives into a later pipeline stage or final output.

This became important because a system can have strong early analysis while still producing a weaker final answer after handoffs.

---

### Modified structured pipeline
The Session 5 structured design.

Instead of using a separate synthesizer, the pipeline returned the critique to the proposer for revision. This improved retention relative to the Session 4 synthesis bottleneck, but did not close the final performance gap.

---

### Process-level finding
A finding about *how* a pipeline succeeds or fails, rather than only about who got the highest final score.

The strongest contributions of this project were process-level findings.

---

### Session 4: synthesis-stage information loss
One of the two central failure modes identified in the study.

Canonical final scores:
- **Solo:** 800/800
- **Pair:** 800/800
- **Structured Trio:** 700/800

Interpretation:
- the structured trio lost fidelity at the synthesis stage even though upstream analysis had been stronger

---

### Session 5: critique-error propagation
The second central failure mode.

Canonical final scores:
- **Solo:** 516/550 (93.8%)
- **Modified Structured:** 442/550 (80.4%)

Interpretation:
- retention improved relative to Session 4
- final performance still lagged because critique introduced false claims that were not filtered strongly enough before incorporation

---

### Solo consistency
The repeated observation that Solo performance was more stable across the clean comparable sessions.

The public writeup summarizes this using **CV ≈ 3.9%** for Solo versus **≈ 7.2%** for Structured.

---

### Structured collaboration
A setup where multiple agents work in explicit roles or stages rather than collaborating freely.

Important caution:
- this project does **not** establish that all structured collaboration is bad
- it does show that specific pipeline handoffs can become failure points unless they are carefully verified

---

### Synthesis-stage information loss
A failure mode in which correct upstream findings are not preserved cleanly when a later stage compresses or integrates them.

This was the key Session 4 finding.

---

### Validator / critic
An agent or role tasked with checking another agent's work.

This project suggests validators are double-edged:
- they can improve reasoning quality
- they can also inject errors unless their claims are independently checked

---

## Public-citation terms

### Canonical source
A source that should take precedence if summaries disagree.

For this repository, the safest public order is:
1. `docs/blogpost.md`
2. `docs/research_at_a_glance.md`
3. `docs/index.html`
4. `docs/research_visualization.html`

Supplementary docs such as the FAQ, methodology guide, reading guide, and glossary should align with those canonical sources.

---

### Commit-pinned URL
A URL that references a specific commit rather than the moving `main` branch.

Why it matters:
- it gives a stable historical snapshot
- it avoids ambiguity if `main` changes later

---

### GitHub raw
The raw file view from GitHub.

In this project, GitHub raw was treated as the safest freshness reference for text files.

---

### Rendered URL
A URL that displays HTML in a browser-rendered form.

Important caution:
- unpinned rendered URLs may lag or cache older versions
- commit-pinned rendered URLs are safer when stable presentation matters

---

## Short summary table

| Term | Plain-language meaning | Project-specific takeaway |
|---|---|---|
| Cohen's d | standardized difference | direction favored Solo in the clean set |
| CV | relative variability | Solo was more consistent |
| Contamination | information leakage | can invalidate a comparison |
| Ceiling effect | task too easy to separate conditions | early sessions hit this problem |
| Handoff | transfer between pipeline stages | central location of failures |
| H5b-retention | did redesign improve retention? | supported |
| H5b-performance | did redesign close final gap? | not supported |
| Synthesis-stage information loss | correct upstream content degraded in synthesis | key Session 4 finding |
| Critique-error propagation | critique adds errors that survive downstream | key Session 5 finding |

---

## Final caution

This glossary is a support document, not the primary scientific narrative. If you need the most authoritative wording, use the main public writeup and short summary documents first.
