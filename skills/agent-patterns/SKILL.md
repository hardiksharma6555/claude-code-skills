---
name: agent-patterns
description: Pick the simplest agentic pattern that works (augmented LLM, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, autonomous agent), based on Anthropic's "Building effective agents" guide. Use whenever designing or reviewing an LLM agent, tool-augmented pipeline, multi-agent workflow or harness — in code, in Claude Code setups, or as the METHOD of a research paper (e.g. an LLM orchestrating domain tools or detectors). Also use when planning ablations for an agentic method, when someone proposes "a real agent" or a multi-agent graph, or when the user asks which pattern/architecture to use. Gives the decision ladder, each pattern's use/avoid/stop rules, tool-design (ACI) rules, and how to turn the ladder into a paper ablation.
---

# Agent patterns: simplest thing that works

Source: Anthropic, "Building effective agents" (Erik S. and Barry Zhang, Dec 19 2024), https://www.anthropic.com/engineering/building-effective-agents. Paraphrased. The page now carries a banner saying tooling has moved on (see Anthropic's Managed Agents docs); the patterns themselves still hold. Cite it in papers as an engineering guide, not a peer-reviewed paper.

## Definitions
- **Workflow:** LLMs and tools follow code paths you wrote in advance.
- **Agent:** the LLM decides its own steps and tool use, in a loop.
- Both are "agentic systems". Agentic systems trade latency and cost for performance. Add a layer only when a measurement improves.

## Decision ladder (go up one rung only when the rung below measurably fails)
0. **No agent:** a single LLM call or a classical model. With retrieval and examples, this often suffices.
1. **Augmented LLM:** one model + tools + retrieval + memory. It writes its own queries, picks tools, and decides what to keep. Most "agents" should stop here.
2. **Prompt chaining:** fixed sequence of steps with programmatic gate checks in between.
   - Use: the task splits cleanly into known steps. You trade latency for accuracy.
   - Avoid: the steps can't be fixed ahead of time.
   - Stop: a gate fails, so halt or escalate.
3. **Routing:** classify the input, then send it to a specialised prompt, tool or model. Cheap model for easy inputs, strong model for hard ones.
   - Use: input categories are distinct and the classifier is reliable.
   - Avoid: classification is noisy, or the route would depend on the answer itself.
4. **Parallelization:**
   - Sectioning: independent subtasks run at once, merged in code. Example: one model screens input as a guardrail while another answers.
   - Voting: the same task runs N times, then aggregate; tune the vote threshold to trade false positives against false negatives.
   - Use: the subtasks are known in advance and independent, or you need confidence.
5. **Orchestrator-workers:** a lead LLM decides the subtasks at runtime, delegates them and merges the results.
   - Use: you can't predict the subtasks in advance.
   - Avoid: the subtasks are fixed. Then parallelization is simpler and the guide prefers it.
6. **Evaluator-optimizer:** generate, critique, revise, in a loop.
   - Use: clear criteria exist, refinement measurably helps, and an LLM can give the feedback a human would.
   - Stop: criteria met, or the attempt or budget cap is hit.
7. **Autonomous agent:** a loop with tools, taking ground truth from the environment each step.
   - Use: open-ended tasks whose steps can't be predicted, in a trusted, sandboxed environment.
   - Required: a max-iteration stop, a human checkpoint, and guardrails. Errors compound.

## Three principles
1. Keep the design simple.
2. Show the plan: make the agent's planning steps visible.
3. Engineer the agent-computer interface (ACI) as carefully as a human interface.

## Tool design (ACI) rules
- Spend as much effort on tool definitions as on the main prompt.
- Write each tool like a docstring for a junior developer:
  - purpose
  - example call
  - edge cases
  - input format
  - how it differs from similar tools
- Choose formats the model sees often in text. Avoid formats with bookkeeping, such as line counts in diffs or code escaped inside JSON.
- **Poka-yoke:** change the arguments so mistakes are impossible. Example from the guide: require absolute paths instead of relative ones.
- Test the tools on many inputs, read the failures, and iterate.
- Frameworks: start with direct API calls, where many patterns fit in a few lines. If you use a framework, read what it does underneath, because hidden prompts hurt debugging.

## Using this as a research-paper method
For any "LLM agent + tools" method (e.g. an LLM orchestrating domain tools), the ladder IS the ablation table. Run every rung with the **same tools, same data, same splits**. Report accuracy and also cost per item (tool calls, tokens, seconds). **Claim only the lowest rung that wins**; reviewers will attack anything above it.

Standard rows:
1. Best single tool
2. All tools with learned stacking (logistic regression or an MLP on the scores). This is the non-LLM baseline the agent must beat.
3. One LLM call that sees all tool outputs (augmented LLM)
4. A fixed chain with gates
5. Routing on observable input properties
6. Parallel run-all with voting
7. Orchestrator choosing tools under a budget
8. Orchestrator plus a stranger verifier that can abstain

Pitfalls to pre-empt:
- **Routing:** never route on anything derived from the label. Route on observables only: properties of the input you can measure before seeing the answer.
- **Parallelization vs orchestrator:** if the tool set is fixed, run-all-and-aggregate is the guide's default. The orchestrator must earn its place by:
  - matching accuracy with fewer tool calls, or
  - gaining on open-set inputs or robustness, where fixed aggregation breaks.
- **Evaluator-optimizer at test time:** there is no ground truth. The evaluator can only check that the evidence is consistent. Map it to abstain or "unknown", with a tool or attempt budget as the stop. Never "loop until it passes".
- **Tool outputs:** use a fixed schema with calibrated scores and short structured evidence fields, never free text. This is poka-yoke for the LLM.
- **Novelty** cannot be "we applied these patterns". It has to be a measured gain plus the reason for it.

## Using it in Claude Code
- Main session = orchestrator.
- Workers get briefs (`brief-and-verify` skill).
- Bulk reading goes to `haiku-scout`.
- Checks go to `stranger-verifier`.
- GPU runs go through `research-harness` and `remote-server-ssh`.
- Before building any multi-agent setup, ask which rung is the lowest that solves the task.
