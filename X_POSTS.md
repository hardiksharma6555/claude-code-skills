# X post drafts

Replace `<REPO_URL>` with the repo link before posting. X counts any link as 23 characters; the counts in the receipt assume that.

## (a) Launch thread

**1/6**
I do deepfake and media forensics research, and most of my day now runs through Claude Code. I've open-sourced the skills, subagents and hooks I built for it.

<REPO_URL>

**2/6**
The setup: the main session plans and checks. Hands-on work goes to worker agents. Each worker gets a written brief with a goal, the files it may touch, an acceptance check and a cap of 4 attempts.

**3/6**
The worker returns a receipt, not a story. Then a separate "stranger" agent checks the receipt against the brief. It never sees the worker's reasoning, so it can't be talked into agreeing. It re-runs the check itself.

**4/6**
Rules I kept repeating became hooks. One asks me before any commit to a paper repo, before model training runs on my laptop instead of the GPU server, and before a LaTeX build with a broken binary. It asks, it doesn't block.

**5/6**
For long jobs there's a harness skill based on Anthropic's long-running agents post: a JSON feature list, a progress file and git, one item per session, marked done only after an end-to-end check. A fresh session knows where to resume.

**6/6**
Also in there: safe SSH rules for agents sharing one GPU server, paper planning, paper breakdowns, and a Socratic tutor for studying. MIT licensed and unofficial. I'm open to research and ML engineering roles.

## (b) Standalone posts

**brief-and-verify**
Delegated agent work fails in three ways: it edits more than asked, it calls done on a check nobody re-ran, or you accept it because it confirms your own idea. My fix: brief, receipt, and a verifier that only sees those two.
<REPO_URL>

**remote-server-ssh**
Several Claude agents shared one SSH socket to a GPU server. A dead socket plus a retry loop turned every retry into a failed login. Now the rule is: hard timeouts, one call at a time, no login fallback, and stop on any error.
<REPO_URL>

**agent-patterns**
Before I add another agent, I ask which rung of Anthropic's "building effective agents" ladder actually solves the task. For research methods the ladder doubles as the ablation table: claim only the lowest rung that wins.
<REPO_URL>

**long-run-harness**
Long agent tasks fail the same ways: too much at once, early "done", features marked complete without a real test. I turned Anthropic's long-running harness post into a skill: feature list, progress log, one item per session.
<REPO_URL>

**tutor + lecture-map**
I was watching lectures and keeping little. Now one skill turns a lecture into a checklist of topics, and a tutor skill teaches each one Socratically: one idea per turn, I explain it back, and spaced reviews get scheduled.
<REPO_URL>

## (c) Pinned post / bio line

**Pinned post**
I research deepfake detection and media forensics. My Claude Code setup (skills, subagents, hooks for running research with agents) is open source here. Open to research and ML engineering roles.
<REPO_URL>

**Bio line**
Deepfake detection and media forensics researcher. I build research workflows with Claude Code. Open to research and ML engineering roles.
