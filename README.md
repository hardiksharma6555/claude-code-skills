# Claude Code skills for research work

I work on deepfake detection and multimedia forensics, and I use Claude Code as a research harness: it plans experiments, runs jobs on a shared GPU server, reads papers with me and checks its own work before calling anything done. This repo collects the skills, subagents and hooks I wrote for that. Each one started as a failure I kept running into (a worker that edited files it was not asked to touch, a polling loop that flooded a server with failed logins, a task declared finished when it was half done) and became a rule Claude follows every time.

## What is here

### Skills (`skills/`)

| Skill | What it does | When it triggers |
|---|---|---|
| `agent-patterns` | Picks the simplest agentic pattern that works (single call, chain, routing, parallel, orchestrator-workers, evaluator-optimizer, agent) and turns that ladder into an ablation table for papers | Designing or reviewing an agent, a multi-agent setup, or an "LLM + tools" research method |
| `brief-and-verify` | Every delegated job gets a written brief with an acceptance check; the worker returns a receipt; a separate verifier checks the receipt against the brief | Any time the main session hands work to a subagent |
| `long-run-harness` | Multi-session harness: feature list in JSON, progress file, init script, one item per session, verified end to end before it is marked done | Tasks that span more than one context window, or keep getting declared done too early |
| `agent-teams` | Doc-checked setup for Claude Code agent teams (Opus lead, Sonnet builders, Haiku read-only scout): settings, teammate templates, limits, costs, and myths from social posts corrected | Parallel builders that must coordinate, or choosing between subagents, teams and workflows |
| `remote-server-ssh` | Safe rules for many agents sharing one SSH ControlMaster socket, plus an `rsh` wrapper (hard timeouts, one call at a time, no login fallback, stop instead of retry) | Any ssh/scp/rsync work, remote job launches, wait loops |
| `research-paper` | Turns "a paper at venue X" into a plan: one-sentence claim with a target number, week-1 kill test, fixed protocol and baselines, capped tuning, schedule | Choosing a topic, planning experiments, or feeling stuck mid-project |
| `paper-breakdown` | Reads a paper in levels: read/skim/skip verdict, a map, an adversarial "is it true" pass against its own tables, and "can I build on it" | Sharing an arXiv link, PDF or title and asking what it is about |
| `explain-mode` | Explains at a chosen depth (ELI5, ground-up, standard, deep, analogy, jargon-only, compare) and diagnoses where an explanation broke | "Explain like I'm 5", "I didn't get it", "go deeper" |
| `tutor` | Socratic study sessions: calibrate first, one idea per turn, explain-back gate, mastery checks, spaced review dates in a `study/` workspace | "Teach me X", "quiz me", working through coursework |
| `lecture-map` | Breaks a lecture, slides, syllabus or chapter into a dependency-ordered checklist of topics to study with `tutor` | Sharing a lecture video, slides or a course page |

Published separately (not duplicated here):

| Skill | What it does | Repo |
|---|---|---|
| `research-harness` | Experiment harness for ML research on GPU servers: frozen protocol and evaluator, claim contract with a pass bar, gate-decided exits, detached launches, guard hook that blocks edits to frozen files | https://github.com/hardiksharma6555/research-harness-skill |
| `cvpr-paper-review` | Pre-submission review the way CVPR does it: three independent reviewers, an Area Chair meta-review, a ranked fix list, then a fix loop | https://github.com/hardiksharma6555/cvpr_paper_review |

### Subagents (`agents/`)

| Agent | Model | Role |
|---|---|---|
| `opus-worker` | Opus | Does one scoped task from the main session and returns an evidence-backed report. Never widens the task or re-plans the project. |
| `haiku-scout` | Haiku | Cheap read-only reader for long logs, many files and transcripts. Returns a short digest with `path:line` quotes. |
| `stranger-verifier` | Opus | Gets only the brief and the receipt, never the worker's reasoning. Re-runs the acceptance check and returns PASS / FAIL / CANNOT VERIFY per item. |

### Hooks (`hooks/`)

| Hook | What it does |
|---|---|
| `guard_bash.py` | PreToolUse hook for Bash. Returns "ask" (never blocks) before: a git commit or push in a paper repo, model training or inference on the local machine, and a known-broken LaTeX binary. Fails open on any error. |

## Install

```bash
git clone https://github.com/hardiksharma6555/claude-code-skills claude-code-skills-showcase
cd claude-code-skills-showcase

# skills: one folder per skill
mkdir -p ~/.claude/skills ~/.claude/agents ~/.claude/hooks
cp -R skills/* ~/.claude/skills/
chmod +x ~/.claude/skills/remote-server-ssh/scripts/rsh

# subagents
cp agents/*.md ~/.claude/agents/

# hook: copy the script, then merge hooks/settings.snippet.json into ~/.claude/settings.json
cp hooks/guard_bash.py ~/.claude/hooks/
```

You can also copy any of these into a project's `.claude/skills`, `.claude/agents` or `.claude/hooks` folder to use them in that project only. Skills load on their own when a request matches their description; you can also call one by name (for example `/brief-and-verify`).

Before using `guard_bash.py` or `opus-worker`, edit the parts that describe my setup (the LaTeX path, what counts as a paper repo, the server rules) to match yours.

## Architecture

```
                 you
                  |
          main session (orchestrator)
          plans, writes briefs, decides
       /          |              \
 opus-worker   haiku-scout    research-harness / remote-server-ssh
 (one scoped    (bulk reading,   (GPU runs: frozen evaluator,
  task, returns  digest only)     detached jobs, safe ssh)
  a receipt)
       \
   stranger-verifier  -- sees only brief + receipt, re-runs the check
          |
   PASS -> reported done      FAIL -> back to the worker (max 4 attempts)

   guard_bash.py hook: asks the human before risky actions
   long-run-harness:   feature_list.json + progress file + git, so the next session knows where to resume
```

- **The main session is the orchestrator.** It plans and checks; hands-on work goes to workers (`agent-patterns`, rung 5). Before adding any agent, it asks which rung of the ladder is the lowest that solves the task.
- **Workers get briefs, not conversations.** A brief has a goal, the files the worker may edit, an acceptance check, non-goals and an attempt cap (`brief-and-verify`).
- **A stranger checks the work.** `stranger-verifier` never sees the worker's reasoning, so it cannot be talked into agreeing. It traces every number back to a file.
- **Hooks turn rules into checks.** A rule written in prose gets skipped sometimes; a hook runs every time. `guard_bash.py` asks before risky actions, and the `research-harness` hook blocks edits to frozen evaluation files.
- **Memory lives in files.** For long jobs, `long-run-harness` keeps a JSON feature list, a progress log and git history, so a fresh session can pick up where the last one stopped instead of guessing.
- **Experiments are judged by a frozen evaluator.** Metrics come from one hash-locked script, and a gate decides pass, budget exit or stall exit, so tuning cannot drift on forever (`research-harness`).

## Credits

The agent design follows two Anthropic engineering articles. The skills paraphrase them; read the originals:

- Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

## Disclaimer

This is a personal, unofficial collection. It is not affiliated with or endorsed by Anthropic. The skills reflect my own workflow; check and adapt them before relying on them, especially the hook and anything that runs commands on a server.

## License

MIT, see `LICENSE`.
