---
name: explain-mode
description: >-
  Explain a concept, term, method, error, or piece of code at a chosen depth and style, with jargon defined rather than assumed. Use this whenever the user asks for an explanation and either names a style or signals that the default is not landing — "explain like I'm 5", "ELI5", "from basics", "in simple words", "in layman terms", "I didn't understand", "I don't get it", "explain it again", "what does this term mean", "explain all the jargon", "go deeper", "with the maths", "explain it with an analogy", "how is this different from X". Also use it proactively when a previous explanation was clearly not understood, or when explaining something to someone new to a field where the standard explanation would assume too much. Prefer this over an ad-hoc explanation — it picks a depth deliberately, defines terms at the moment they are first used, and diagnoses which step broke rather than restating the same thing more slowly.
---

# Explain Mode

A failed explanation is almost never too short. It is pitched at the wrong level, or it uses a term the listener does not have yet, or it skips the one step where their understanding actually broke. This skill makes the pitch a deliberate choice rather than an accident.

## Picking a mode

The reader may name a mode. More often they signal one:

| They say | Mode |
|---|---|
| "ELI5", "like I'm five", "layman terms", "simple words" | **eli5** |
| "from basics", "from scratch", "I'm new to this", "assume I know nothing" | **ground-up** |
| *(nothing in particular)* | **standard** |
| "in detail", "with the maths", "I'm implementing this" | **deep** |
| "give me an analogy", "what's this like" | **analogy** |
| "just the jargon", "what do these terms mean" | **jargon-only** |
| "how is this different from X", "I already know Y" | **compare** |
| "I didn't understand", "I'm lost", "explain again" | **diagnose first** — see below |

When the signal is ambiguous, pick the simpler mode. Being told something you already knew costs seconds; being lost costs the whole explanation. Say which mode you are using only when it is not obvious — announcing it every time is noise.

## The modes

**eli5** — Zero jargon. Everyday analogies, short sentences, concrete objects. The test: a smart person with no computing background follows it end to end. If a technical term is genuinely unavoidable, it stops being eli5 — switch to ground-up and say so.

**ground-up** — Build from first principles. Every term is defined at the moment it is first used, never before it is needed and never assumed. No forward references: if step 4 depends on a concept, that concept appears by step 3. This is the right default for someone new to a field who wants real understanding rather than a comforting simplification.

**standard** — Assumes general technical fundamentals but no domain expertise. Names things properly and defines domain-specific terms inline on first use. The default when nothing suggests otherwise.

**deep** — Full technical detail, including the mathematics, edge cases, and the reasons behind design choices. Appropriate when the reader is implementing or debugging something. Depth here means completeness, not density — a wall of notation with no interpretation is not a good deep explanation.

**analogy** — Sustain one concrete analogy the whole way through, then map each part of it back to the real thing explicitly. Two rules keep this honest: the mapping must be stated rather than left implied, and **the analogy's limits must be named**. Every analogy breaks somewhere, and an unflagged break becomes a misconception that is expensive to remove later.

**jargon-only** — Define the terms in a piece of text and nothing else. No summary, no explanation of the whole. Useful when the reader understands the shape of something but keeps tripping over vocabulary.

**compare** — Explain the new thing against something the reader already knows. Structure it as: what carries over, what changes, and what has no counterpart. That third category is where the real learning is, and it is the one usually left out.

## Rules that apply in every mode

**Concrete beats abstract.** Real numbers, named examples, actual file paths. "A ViT-B has 86 million parameters, roughly 344 MB in float32" lands; "the model is quite large" does not.

**Work an example whenever one is possible.** One worked example teaches more than three paragraphs of description, and it exposes gaps in your own understanding before it exposes them in the reader's.

**Define on first use, not in a glossary at the end.** A term the reader has to scroll for is a term that breaks their reading.

**Separate fact from interpretation.** "This is how attention works" and "I think this is why it works" are different claims. Mark the second as yours.

**Close by naming the likely sticking point.** End with the single step most likely to have not landed, and offer to expand exactly that. Something like: *"The part that usually needs a second pass is why the gradient signal is weaker for rare conditions — say the word and I'll take just that apart."* This is more useful than a generic offer to help, because it shows you know where the difficulty is, and it gives the reader permission to admit confusion about a specific thing rather than the whole.

## When the reader says they did not understand

This is the moment the skill earns its place, and the instinct to avoid is restating the same explanation in more words. That almost never works, because the problem was never volume.

Instead:

1. **Find the break.** Which step was the last one that made sense? Either ask directly, or infer it from what they said back to you — the thing they got wrong points at where it went wrong.
2. **Restart one step earlier than the break.** The failure is usually in the step *before* the one that felt confusing, because a step only feels confusing when its input was already shaky.
3. **Change something.** Drop a level, switch to analogy, or work a concrete example. Same words at a slower pace is not a different explanation.
4. **Check the vocabulary.** Very often the whole failure is one undefined term doing quiet damage. Scan back for terms used without definition.

If two attempts have not worked, say so plainly and try a genuinely different angle — a diagram, a worked numerical example, or building up from a simpler adjacent problem. Repeating a third time is worse than admitting the approach is not working.

## Length

Match length to the question. A term definition is two sentences. A method explanation might be a page. Padding an explanation to look thorough makes it harder to read, and the reader can always ask for more — that is what the closing offer is for.
