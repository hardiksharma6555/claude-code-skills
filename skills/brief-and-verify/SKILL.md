---
name: brief-and-verify
description: Brief -> receipt -> stranger-verify loop for any delegated job. Use whenever the main session hands work to a subagent or worker (opus-worker, general-purpose, haiku-scout, a fork), whenever a task touches several files or a paper/experiment result, or when the user says delegated work drifted, overreached, or was reported done when it was not. Every delegated job gets a written brief with an acceptance check; the builder returns a receipt; a separate stranger-verifier agent checks the receipt against the brief before anything is reported as done.
---

# Brief and verify

Delegated work fails in three ways: the builder edits more than it was asked to, it declares done on a check nobody re-ran, or the conductor accepts its summary because the conductor wrote the hypothesis. This skill closes all three with a fixed brief, a receipt, and a verifier that never sees the builder's reasoning.

## 1. Brief (conductor writes, before delegating)

Every delegated job gets all five fields. If you cannot fill one, the task is not ready to hand off.

```
GOAL: <one or two sentences: what is true when this is done>
MAY EDIT: <exact paths or globs; nothing else may change>
ACCEPTANCE CHECK: <commands or observations that prove the goal, with expected result>
NON-GOALS: <what not to do, even if it looks helpful>
ATTEMPTS: max 4. After 4 failed attempts at the acceptance check, stop and escalate with the error text.
```

Add context the builder cannot find alone (paths, memory notes, server rules; point to the `remote-server-ssh` skill for any ssh work, `research-harness` for experiments). For project workers use the existing `opus-worker` agent; for bulk reading use `haiku-scout`.

## 2. Receipt (builder returns)

The builder ends with a receipt, not a story:

```
FILES CHANGED: <absolute paths, each with one line on what changed>
COMMANDS RUN: <the commands that matter, in order, with exit codes>
EVIDENCE: <acceptance-check output, quoted; numbers with the file they came from>
ATTEMPTS USED: <n of 4>
NOT DONE: <anything skipped or failed, with the error text>
```

## 3. Stranger verification (separate agent)

Spawn the `stranger-verifier` agent with ONLY:
- the brief, verbatim, and
- the receipt, verbatim.

Do not pass the builder's reasoning, the chat history, or your own opinion of the result. The verifier re-runs the acceptance check, compares changed files to MAY EDIT, checks NON-GOALS, and traces every number.

## 4. Decide

- **PASS**: report done, citing the verifier's evidence.
- **FAIL**: send the failing items back to the builder (same brief, attempt count carries over). At 4 attempts, stop and escalate to the user with both reports.
- **CANNOT VERIFY**: say so plainly to the user with what would settle it. Never report it as done.

## When to skip

Skip the verifier for pure lookups (a haiku-scout digest, a single file read) and for one-line edits you can check yourself with one command. Never skip it for paper text, result tables, config changes, or anything that will be pushed or shared.
