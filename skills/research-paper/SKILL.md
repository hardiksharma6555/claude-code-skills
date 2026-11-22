---
name: research-paper
description: Plan and drive a research paper for a top AI/ML venue (IJCAI, ICML, NeurIPS, ICLR, CVPR, AAAI) from idea to submission, especially deepfake / AI-generated image detection and multimedia forensics work. Use this whenever the user asks what to work on for a conference, which topic or dataset to pick, how to plan a paper, what the deadlines are, how to structure experiments or baselines, or says they feel stuck midway through a project. Also use it when they share a paper and ask how to build on it for their own submission.
---

# Research Paper

Turns "I want a paper at venue X" into a plan that reaches a submittable result, and keeps the project from stalling halfway.

Why this exists: projects tend to stall in the middle, when the first results come in weaker than hoped and work drifts into open-ended variant tuning. The rules below make the decision points explicit and early, so time goes into one sharp, positive result.

## Core rules

1. **Write the claim before coding.** One sentence stating what the paper shows, plus the one table or figure that proves it, with the number it has to hit. Example: "Method X raises cross-generator accuracy on benchmark Y by at least 3 points over the strongest published baseline, at the same inference cost." If the claim cannot be written this way, the project is not ready to start. Everything later (experiments, writing, ablations) is judged by whether it serves this sentence.

2. **Run a kill test in week 1.** The smallest experiment that could show the claim is wrong, with a pass bar fixed before running it. Use cheap setups (cached features, a subset, one generator pair). If it fails, drop the idea and move to the next candidate claim. Don't keep patching the old one; an early switch costs a week, a late one costs the deadline.

3. **Fix the protocol and baselines on day 1.** Pick the standard benchmark split the target paper and its predecessors use, and copy baseline numbers from published tables (cite the source table). Only rerun a baseline when no published number exists for that protocol, or when measuring speed, robustness or per-sample outputs. Mark rerun rows clearly ("reproduced with official code"). Mixed protocols in one table are a common reviewer complaint.

4. **Start writing in week 2.** Draft the intro, the claim, and the method section while experiments run. Writing exposes missing experiments and weak motivation far earlier than results do.

5. **Cap tuning.** At most 5 variants per idea before deciding. Log each variant with its config and score. After the cap, either the claim holds and you write it up, or you switch to the next candidate claim.

6. **One paper, one claim.** Two papers need two distinct claims. Most venues (including IJCAI and ICML) forbid submitting the same or substantially overlapping work to another venue while it is under review, and their review periods overlap.

The goal is a positive result that beats strong baselines under a standard protocol and comes with a clear insight into why. Do not plan papers around negative results or a pre-planned fallback framing; they rarely get accepted at these venues.

## Reporting results in the paper

Space is limited, so the paper has to be focused, and it also has to be honest.

- **Lead with the main claim.** Main-paper tables and figures show the evidence for it under the standard protocol.
- **Report every evaluated setting somewhere.** Settings where the method does not win go in a limitations paragraph or the supplementary material, stated plainly.
- **Keep the paper readable.** Tuning history and abandoned variants belong in the project notes, not the main text, unless they explain a design choice.
- **Follow the layout of the closest accepted paper** so reviewers find things where they expect them.

Rules that are never broken:

- Numbers are never changed, and every row says what it is: a single run, a mean over N seeds, or the best of N runs.
- The text claims only what the tables show.
- Keep the standard columns of the protocol being followed (for example AUC in a detection table).

## Workflow

1. **Venue and deadline.** Always verify dates live from the official site (e.g. `https://<year>.ijcai.org/`, `https://icml.cc/Conferences/<year>/Dates`) instead of trackers or memory. Count the weeks left from today. Read `references/venues.md` for what each venue rewards.
2. **Candidate claims.** Propose 2 to 3 claims that fit the venue and reuse existing assets (data on the server, cached features, prior pipelines). Rank them by: chance of beating baselines, compute cost, and fit to the venue.
3. **Datasets and protocol.** For each claim, list train/test sets, splits, where they live, and any gaps (download, extraction, cleaning). Keep your own `references/datasets.md` listing known datasets and where they live, and check your server before proposing a download.
4. **Baselines.** List baselines with the source table for each copied number, and which ones need rerunning and why.
5. **Kill test.** Define it concretely: data subset, metric, pass bar, expected runtime.
6. **Schedule.** Week by week until the deadline, with the writing start in week 2 and a full-draft checkpoint at least 10 days before the deadline.
7. **Compute.** Training and inference run on the GPU server, never on the laptop.

## Output format

Use this structure for each paper plan:

```
## Paper <N>: <working title>  (<venue>, abstract <date>, full paper <date>, <W> weeks left)
Claim: <one sentence with the target number>
Proof: <the table/figure that shows it>
Why this venue: <one line>
Datasets: <train / test, split, server path or download source, status>
Baselines: <name: copied from <paper, table> | rerun because ...>
Kill test (week 1): <setup, metric, pass bar, runtime>
Schedule: <week-by-week>
Risks: <top 2, each with what you'd check early>
```

Keep it short. A plan the user can act on today beats a survey of options.
