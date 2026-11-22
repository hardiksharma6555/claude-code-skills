---
name: long-run-harness
description: Set up and run a multi-session harness so a long task (an app, a paper's experiment suite, a big refactor, a dataset build) finishes instead of stalling or being declared "done" early. Based on Anthropic's "Effective harnesses for long-running agents" (initializer agent + coding agent, feature_list.json, claude-progress.txt, git, init.sh) and the 6-layer harness view (guides, sensors, loop, memory, permissions, tracking). Use whenever a task will span more than one session or context window, when work keeps getting half-finished, when Claude claims done before it is, when a fresh session doesn't know where to resume, or when the user asks to "set up a harness" for a long job.
---

# Long-run harness

Same model, different harness, different results. The agent is the model plus the harness. The harness covers the rules, checks, memory and limits around the model.

Sources:
- Anthropic, "Effective harnesses for long-running agents" (Justin Young, Nov 26 2025), https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Code: https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
- The 6-layer framing (guides, sensors, loop, memory, permissions, tracking) came from a post on X. Paraphrased throughout.

## Why long tasks fail (observed by Anthropic)
1. **One-shotting:** the agent does too much at once and runs out of context mid-feature. The next session has to guess what happened.
2. **Early victory:** a later session sees existing progress and declares the job done.
3. **Untested "done":** features are marked complete on unit tests or curl alone, without an end-to-end check.
4. **Startup waste:** each session spends time working out how to run the project.

## The design
Two prompts, with the same tools and system prompt.

**Initializer (first session only):**
1. Expand the goal into `feature_list.json`. Every item starts as `"passes": false`.
2. Write `init.sh`, which starts or checks the environment.
3. Create `claude-progress.txt`.
4. Make the first git commit.

**Worker session (every later session), in this order:**
1. Run `pwd`. Edit files only under that directory.
2. Read `claude-progress.txt` and `git log`.
3. Read `feature_list.json` and pick the highest-priority item that isn't passing.
4. Run `init.sh` and a basic end-to-end check, to catch bugs the last session left.
5. Build **exactly one** item.
6. Verify it end to end, the way a user would: browser automation for UIs, the real command for CLIs, the frozen evaluator for experiments.
7. Flip `passes` to true only after that check.
8. Commit with a descriptive message, then append to `claude-progress.txt`.
9. Leave the code clean enough to merge.

**`feature_list.json` rules:**
- Each item has `category`, `description`, `steps` (end-to-end check steps) and `passes`.
- Use JSON, not Markdown, because models overwrite JSON less often.
- Workers may change only the `passes` field. Removing or rewording items is forbidden.

```json
[{"category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": ["Click New Chat", "Verify it appears in sidebar"],
  "passes": false}]
```

## The 6 layers and where each lives in Claude Code
| Layer | What it does | Claude Code slot |
|---|---|---|
| 1. Guides | Rules; every new failure becomes a rule | CLAUDE.md, skills, memory |
| 2. Sensors | Objective checks after edits | PostToolUse hooks running linter/tests; frozen evaluators |
| 3. Loop | Plan, build one item, independent check, fix, commit | `brief-and-verify` skill + `stranger-verifier` agent |
| 4. Memory | A fresh session knows where to resume | `claude-progress.txt`, `feature_list.json`, git |
| 5. Permissions | Nothing gets pushed, deleted or deployed without the human | allow/ask/deny lists, `guard_bash.py` hook (ask mode) |
| 6. Tracking | Every tool call and every dollar logged | PreToolUse logging hook, `/cost`, run logs |

Prompt engineering shapes what the model is told. Context engineering shapes what it sees. Harness engineering shapes what it can do.

## Adapting to research work
- For experiments and GPU runs, use `research-harness`, which supplies the frozen protocol, contract and gate. Map the pieces as follows:
  - `feature_list.json` becomes the experiment list. Each item names a run, its acceptance check (a frozen-eval metric or pass bar) and `passes`.
  - `init.sh` becomes the env check: conda env, data paths, GPU free-memory scan via `remote-server-ssh`.
  - `claude-progress.txt` becomes a run log with what launched, where its log sits, and its DONE marker.
- For papers, each section or table is one item. Its check is that it compiles, the numbers match the result files, and the page budget holds.
- For dataset builds, each generator or source is one item. Its check is the count, a checksum, and a sample visual check.

## Setup checklist (do this before starting the long task)
1. Write `feature_list.json` from the spec, with all items false. Get the user's OK on the list.
2. Write `init.sh` and `claude-progress.txt`, then commit.
3. Confirm the sensors exist: a test command, an evaluator, or browser automation.
4. Confirm permissions: risky actions are set to ask.
5. Each session follows the worker routine above. One item per session or per delegated worker.

Open question from the source: one general agent or specialised testing and QA agents? Default to one builder plus `stranger-verifier`, and add more only if a measurement says it helps (see `agent-patterns`).
