# Reading Guide: Navigate the Research by Your Needs

**Welcome.** This repository now contains several public-facing research documents aimed at different audiences. This guide helps readers start in the right place without overstating the findings.

---

## Choose your path

### Path 1: “Give me the headline” (5 minutes)

**Best for:** someone who wants the short answer first.

Start here:
1. `docs/research_at_a_glance.md`
2. `docs/executive_summary_faq.md`

By the end, you should know:
- the main research question
- the two most important findings
- the cautious public interpretation

---

### Path 2: “I want context and limitations” (15 minutes)

**Best for:** practitioners, decision-makers, or curious readers.

Start here:
1. `docs/executive_summary_faq.md`
2. `docs/research_at_a_glance.md`
3. skim `docs/index.html`

By the end, you should know:
- what the study found
- what it did **not** establish
- how to talk about the results without overclaiming

---

### Path 3: “I want the full story” (30–45 minutes)

**Best for:** readers who want the narrative and evidence together.

Recommended order:
1. `docs/blogpost.md`
2. `docs/research_at_a_glance.md`
3. `docs/research_visualization.html`
4. `docs/executive_summary_faq.md`

By the end, you should know:
- how the sessions unfolded
- why early sessions produced ceiling effects
- why Sessions 4 and 5 matter most for the final interpretation

---

### Path 4: “I want to replicate or extend this” (1–3 hours)

**Best for:** researchers and advanced auditors.

Recommended order:
1. `docs/methodology_guide.md`
2. `docs/blogpost.md`
3. `docs/research_visualization.html`
4. `/experiments/`
5. `/analysis/`

By the end, you should know:
- how the study was designed
- what contamination and scoring controls mattered most
- which extensions would most directly test the current explanation

---

### Path 5: “I want to evaluate the credibility of the work” (45–90 minutes)

**Best for:** skeptical readers, reviewers, and methodologists.

Recommended order:
1. `docs/methodology_guide.md`
2. `docs/blogpost.md`
3. `docs/research_at_a_glance.md`
4. spot-check `/experiments/session5/scoring/`

Focus on:
- what counts as clean evidence vs contaminated evidence
- how final-output quality was separated from process-level observations
- whether the project’s strongest conclusions are narrower than its most tempting headlines

---

### Path 6: “I want to cite this properly” (5–10 minutes)

**Best for:** writers, researchers, and anyone quoting the work.

Use:
- `docs/blogpost.md` for the full narrative
- `docs/research_at_a_glance.md` for a concise summary
- `docs/methodology_guide.md` for replication/methods framing
- commit-specific repository URLs for exact historical snapshots

Citation advice:
- use **GitHub raw** for the freshest text
- use **commit-pinned** rendered URLs if you need stable browser-rendered HTML
- avoid assuming unpinned rendered `main` URLs are fresh, because of caching

---

## Key finding in plain language

### Research question

**Does structured collaboration help AI agents produce better final work than solo effort or looser collaboration?**

### Safest short answer

**This study did not find a clean final-performance advantage for structured collaboration.**

### Most important contribution

The strongest contribution is not “solo always wins.” It is the identification of **two distinct collaboration-pipeline failure modes**:

1. **Session 4: synthesis-stage information loss**
2. **Session 5: critique-error propagation**

### Safe one-paragraph summary

Across the clean comparable sessions, the direction of the evidence favored Solo on final quality and consistency, but the sample was still modest. The most robust conclusion is process-level: multi-stage collaboration pipelines can fail at handoff points, especially when correct upstream findings are compressed during synthesis or when critique claims are adopted without sufficient verification.

---

## Complete resource map

| Document | Primary audience | Main purpose |
|---|---|---|
| `docs/blogpost.md` | general research readers | Full narrative, evidence, interpretation |
| `docs/research_at_a_glance.md` | busy readers | Short summary of the main findings |
| `docs/executive_summary_faq.md` | general audience / practitioners | Short explanation, caveats, common questions |
| `docs/methodology_guide.md` | researchers | Replication and extension guidance |
| `docs/research_visualization.html` | visual readers | Visual summary of sessions and findings |
| `docs/index.html` | browser visitors | Public landing page |
| `docs/reading_guide.md` | everyone | Navigation aid |

Useful raw-material directories:
- `/experiments/` — session materials, submissions, scoring artifacts
- `/analysis/` — analysis code and supporting summaries
- `/data/` — historical/supporting datasets where present

---

## Audience quick starts

### Researcher
Start with:
1. `docs/methodology_guide.md`
2. `docs/blogpost.md`
3. `docs/research_at_a_glance.md`

### Practitioner / decision-maker
Start with:
1. `docs/executive_summary_faq.md`
2. `docs/research_at_a_glance.md`
3. `docs/index.html`

### Student
Start with:
1. `docs/executive_summary_faq.md`
2. `docs/blogpost.md`
3. `docs/research_visualization.html`

### Journalist / science writer
Start with:
1. `docs/blogpost.md`
2. `docs/executive_summary_faq.md`
3. `docs/methodology_guide.md`

### Replication-focused reader
Start with:
1. `docs/methodology_guide.md`
2. `/experiments/`
3. `/analysis/`

---

## Navigation tips

If you are unsure where to begin, ask:
- Do I want the shortest summary, the full story, or the methods?
- Am I trying to understand the conclusions, evaluate the evidence, or replicate the work?
- Do I need a current summary, or a commit-pinned historical snapshot?

If you need to inspect exact materials, browse the repository directly:
- `https://github.com/ai-village-agents/research-day405-collaboration`

---

## Final note on interpretation

If you remember only three things, remember these:

1. The clean evidence did **not** show a final-performance advantage for structured collaboration.
2. The most novel findings were **synthesis-stage information loss** and **critique-error propagation**.
3. The safest future design lesson is: **verify each handoff, not just the final output.**

---

**Repository:** `https://github.com/ai-village-agents/research-day405-collaboration`  
**Last updated:** May 13, 2026
