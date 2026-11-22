---
name: paper-breakdown
description: >-
  Break down a research paper so the reader actually understands it — what problem it solves, whether its claims hold up, and whether it is worth building on. Use this whenever the user shares a paper in any form (arXiv link or ID, DOI, PDF path, pasted abstract or text, or a paper title) and wants to understand it, or asks things like "what is this paper about", "break this down", "explain this paper", "is this paper any good", "should I read this", "summarise this for me", "help me understand this". Also use it when the user is deciding whether a paper is relevant to their own work, when they need the jargon in a paper explained, or when they want to find a research gap in a paper. Prefer this over writing an ad-hoc summary — a plain summary tells the user what the paper says, this tells them whether to believe it and what to do with it.
---

# Paper Breakdown

Most paper summaries fail the reader in the same way: they faithfully restate what the paper claims, and stop. The reader ends up knowing the paper's own marketing but with no idea whether the result is real, whether the baseline was fair, or what they could actually do next. This skill exists to close that gap.

Three things distinguish a useful breakdown from a summary:

1. **A recommendation.** The reader's scarcest resource is attention. Say whether to read, skim, or skip — and why.
2. **A verification pass.** Check the headline claim against the paper's own tables. Papers overclaim, and prose and tables disagree more often than people expect.
3. **A next step.** The limitations paragraph is a list of open problems the authors handed over for free. Surface it.

## Getting the paper

If given an arXiv ID or link, fetch it. `https://arxiv.org/abs/XXXX` gives metadata; `https://arxiv.org/html/XXXX` or `https://ar5iv.labs.arxiv.org/html/XXXX` usually gives readable full text. For a DOI, resolve it. For a local PDF, read it directly.

If the full text is unavailable — paywall, failed render, PDF too large — **say so explicitly and label the breakdown as abstract-only.** An abstract-only breakdown is still useful, but the reader must know they are getting the authors' own framing without the evidence behind it. Never silently downgrade.

## The four levels

Progressive disclosure exists because reading a paper is a filtering process. Most papers should be abandoned after Level 0. **Deliver Levels 0 and 1 by default.** Go further only when the reader asks, or when Level 1 makes it obvious the paper matters to their current work.

### Level 0 — Should I read this? (~30 seconds)

```
PAPER      <title>
VENUE      <venue + year, or "arXiv preprint — not peer reviewed">
PROBLEM    <one sentence: what is broken in the world>
APPROACH   <one sentence: what they did about it>
RESULT     <the single headline number, with its metric and dataset>
VERDICT    <READ / SKIM / SKIP> — <one sentence of reasoning>
```

The verdict is the point of this level. Make it a genuine judgement, not a hedge. "SKIM — the method is standard, but Table 3 has the only published numbers for X" is useful. "This paper may be relevant depending on your interests" is not.

Venue matters and is routinely glossed over. An unpublished preprint and an ICCV paper carry different evidential weight, and the reader deserves to know which one they are holding.

### Level 1 — The map (~3 minutes)

Four short paragraphs:

- **What problem exists**, stated concretely enough that someone could recognise it in the wild.
- **Why prior work fails at it** — the specific failure, not "existing methods have limitations."
- **The core idea**, in plain language. If you cannot state it without equations, you have not understood it yet.
- **What they showed** — the main result and what it was measured against.

Then close with the three questions. These matter because the answers to the last two are usually where a new project lives:

```
1. What breaks if the main idea is removed?     → <answer from the ablation, or "not tested">
2. What dataset was NOT tested?                 → <the obvious omission>
3. What would this cost to run?                 → <params, GPU, training time — or "not reported">
```

Question 2 deserves real thought. Papers are evaluated on the benchmarks that flatter them. Naming the dataset conspicuously absent is often the single most valuable line in the whole breakdown.

### Level 2 — Is it true?

This level is adversarial, on the reader's behalf.

**The main results table.** What is the baseline? Is it tuned as carefully as the proposed method, or is it a number copied from an older paper? A method compared against an undertuned baseline is a common and hard-to-spot failure.

**The ablation table.** Remove each component; does the number actually drop? Components that contribute under a point are decoration. Say so.

**Reconciliation.** Check the paper's headline claims against its own tables and recompute. Prose and tables disagree surprisingly often — a real example: DINOv2's §8.1 prose describes a "25.7%" regional gap while its Table 12 gives Africa 74.0 and Europe 89.7, a 15.7-point difference that no relative computation recovers either. When numbers do not reconcile, **report both, show the arithmetic, and do not pick a side.** The reader can then cite the table (safe) rather than the prose (indefensible).

**Statistical care.** Single seed? Error bars? A 0.4-point gain with no variance reported is not a result.

Flag overclaiming plainly. Being polite about a weak paper wastes the reader's time.

### Level 3 — Can I build on it?

- **Code and weights** — released, or promised? Does the repo look alive? Would it run in one evening, which is the practical bar for a baseline.
- **Data** — which splits, what preprocessing, anything gated behind an access form.
- **Compute** — what it actually takes to reproduce, versus what the reader has.
- **The limitations paragraph** — read it as a list of open problems. Quote it, then say which ones look tractable. Authors are often unusually candid here because it is expected of them.

## The jargon panel

Attach to every breakdown, at the end:

```
JARGON
  <term> — <one or two plain sentences>
  <term> — already in your glossary
```

Check the project's `GLOSSARY.md` (working directory or repo root) first when it exists. If a term is already defined there, say so rather than redefining it — repetition is noise, and it tells the reader their glossary is doing its job. At the end, suggest any terms worth adding.

Define at the level of someone new to the field. If a definition needs another undefined term, define that one too, or pick a different definition.

## Honesty rules

These matter more than polish, because a confidently wrong breakdown is worse than no breakdown.

- Separate what the paper **claims**, what it **demonstrates**, and what it merely **implies**. These are three different things and papers blur them.
- If a number cannot be verified from the paper itself, mark it unverified rather than repeating it with confidence.
- Never invent a number, a table reference, or a section number. If you did not see it, say you did not see it.
- Say when a paper is weak, overclaims, or compares against a straw baseline.
- Attribute correctly. "The authors report X" and "X is true" are different sentences.

## Drill-down

After the breakdown, the reader may ask for any section explained, any figure explained, any term expanded, or the whole thing restated more simply. For anything that needs a change in explanation style — "explain like I'm new", "from basics", "in simple words" — use the **explain-mode** skill, which handles that properly, rather than improvising.

Also useful to offer once, briefly, at the end: a deeper level if you stopped early, or a comparison against another paper the reader has mentioned.
