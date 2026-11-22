---
name: agent-teams
description: Run a Claude Code agent team (experimental) — a lead that coordinates teammates who share a task list and message each other directly — with a cost-aware model split (Opus lead, Sonnet builders, Haiku scout). Use when the user asks for agent teams, teammates, /peers, teammateMode, parallel builders on separate parts of a codebase, or a "lead + builders + scout" setup; also when deciding between subagents, agent teams and a workflow. Holds the doc-verified settings, agent frontmatter, limits and costs, and corrects common myths from social-media posts.
---

# Agent teams

All facts below were checked against the Claude Code docs on 2026-11-22:
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/costs

The setup idea came from an X post. Several of its claims were wrong; see "Myths" below. Re-check the docs if the Claude Code version changes a lot.

## When to use a team (vs. alternatives)
- **Subagents (Agent tool):** the default. Use them for independent jobs that report back to you. They are cheaper and support resume.
- **Agent team:** use it only when the builders must coordinate with each other while working, e.g. the frontend and backend agreeing on an API contract. Each teammate owns a separate set of files.
- **Workflow tool:** use it for deterministic fan-out over many items. It needs the user's explicit opt-in.
- Ask the question from `agent-patterns` first: what is the lowest rung that solves this? Teams use far more tokens. The docs say roughly 7x a standard session when teammates run in plan mode.

## Enable (user settings, ~/.claude/settings.json)
```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "teammateMode": "auto",
  "effortLevel": "high"
}
```
- `teammateMode` takes `auto`, `tmux` or `iterm2`. The flag `--teammate-mode auto` also works, but it is experimental and not shown in `--help`.
- `effortLevel` takes `low`, `medium`, `high` or `xhigh`. `max` is only valid in agent frontmatter.
- Teams don't work in `-p` (non-interactive) mode or in Agent SDK sessions.
- Always show the settings diff and back up first. Never enable this without the user's OK.

## Teammate definitions (~/.claude/agents/*.md frontmatter)
Fields are `model` (sonnet | opus | haiku | fable | full ID | inherit), `effort` (low…max), `tools`, and `isolation: worktree`.

```yaml
---
name: teammate-back
description: Backend builder. Owns server/ and api/ only.
model: sonnet
effort: medium
---
```
```yaml
---
name: teammate-scout
description: Read-only scout. Checks contracts, schemas and edge cases; never edits.
model: haiku
tools: Read, Grep, Glob, Bash
---
```
- **Important:** a teammate spawned from a definition that sets `isolation` still runs in the lead's working directory, so isolation does not apply to teammates. Prevent clashes by giving each teammate its own files, or have the lead create a separate git worktree and tell the teammate to `cd` into it.
- The docs' cost advice: use Sonnet for teammates. An Opus lead, Sonnet builders and a Haiku read-only scout is a sensible split.

## How it runs
- Teammates message each other directly with `SendMessage`. Inboxes live at `~/.claude/teams/{team}/inboxes/`. `/list-agents` (or `/peers`) shows who can be messaged.
- The shared task list is at `~/.claude/tasks/{team}/`.
  - Claiming a task uses file locking, so two teammates can't take the same one.
  - Tasks can depend on other tasks and show as blocked until those complete.
  - Ctrl+T shows the list.
  - There are no locks on source files.
- Manage the team from the agent panel under the prompt: arrow keys, Enter, Escape, and `x` to stop a teammate.

## Scout checkpoints (good practice, not a feature)
Have the Haiku scout check three moments:
1. Before a contract locks: does the frontend payload match the backend schema?
2. When a test fails twice: is the fix addressing the cause, or hiding the symptom?
3. Before "done": which edge cases, races or attack surfaces were missed?

The lead reviews the merged diffs and runs the test suite before merging. This is the `brief-and-verify` / `stranger-verifier` loop applied to a team.

## Limits (from the docs)
- `/resume` and `/rewind` don't restore in-process teammates.
- Task status can lag, and shutdown is slow.
- One team per session, no nested teams, and the lead is fixed.
- There are no per-teammate permission modes at spawn.
- Split panes need tmux or iTerm2.
- In-process teammates can't start background subagents.

## Myths from the source post (all wrong or unverified)
- **"`/teams` command":** it doesn't exist. Use the agent panel and `/list-agents` / `/peers`.
- **"`tasks.json` with file-level mutex locks":** the task list lives in `~/.claude/tasks/{team}/`. Locks apply only to claiming tasks, never to source files.
- **"`isolation: worktree` gives each teammate its own worktree":** it does not apply to teammates.
- **"Haiku at 340 tok/s":** not in any official source. The docs only call Haiku 5.5 the "fastest".
- **"Official Anthropic tip" and "Jev engineering 16 ms":** marketing, with no doc source.

## For research work
Teams fit software builds with separate parts, such as a demo app with a frontend and an API. They are a poor fit for GPU experiment campaigns, where `research-harness` plus subagent workers (`opus-worker`) are cheaper and resumable. Never let teammates ssh to shared servers in parallel without the `remote-server-ssh` rules.
