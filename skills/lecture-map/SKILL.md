---
name: lecture-map
description: >-
  Break a lecture, video, course, syllabus, or study document into a dependency-ordered map of studyable topics so the user can learn each piece actively (with the tutor skill) instead of passively watching or reading. Use whenever the user shares a lecture video or YouTube link, lecture slides (PPTX/PDF), a course syllabus, a textbook chapter or notes document — optionally scoped to a page/slide/chapter range ("map pages 30-58", "just chapter 4") — or names a lecture or course ("break down CS231n lecture 8", "what topics does this video cover", "map this course for me", "turn this lecture into a study plan"). Also use whenever they mention tutorial hell, zoning out during lectures, not retaining what they watch or read, or wanting to study material piece by piece. For research papers, prefer the paper-breakdown skill. Produces a checklist map file in the study/ workspace shared with the tutor skill.
---

# Lecture Map — turn passive lectures into an active study menu

## Why this skill exists

The user's "tutorial hell" pattern: watch a lecture end-to-end, feel like it landed, never self-study the pieces, retain little. The fix is to make the lecture's contents *explicit and enumerable* — a menu of concepts they can conquer one at a time with the `tutor` skill, using the video only as one resource among several. A lecture map converts "I should rewatch that" into "I have 4 unchecked topics left."

## Inputs you can work from

In order of preference:

1. **Actual materials**: a transcript file, slides (PDF or PPTX), lecture notes, a DOCX handout, a book chapter, or a course/series page URL — see *Reading real materials* below for extraction, page/slide ranges, and source anchoring (use WebFetch/WebSearch to pull the real schedule or contents — most university courses have public schedule pages; the same applies to any public course, playlist, or textbook).
2. **A YouTube link**: fetch the description/transcript if accessible.
3. **A personal learning roadmap**, if one is recorded in `study/_progress.md` — a roadmap's per-lecture topic lists alone are enough to build a good map.
4. **Model knowledge** of the standard course content.

Be honest about provenance. If you built the map from the roadmap plus general knowledge rather than the actual video, say so in the map's header (`source: roadmap + inferred`) — never imply you watched the video. If real materials contradict your assumptions, the materials win.

## Reading real materials (PDF, PPTX, DOCX)

Everything needed is already installed — don't reinvent extraction:

- **PDF**: the Read tool reads PDFs natively with a `pages` param (e.g. `"30-58"`, max 20 pages per call); for bulk text, `pdftotext -f 30 -l 58 file.pdf -`.
- **PPTX**: `python-pptx` — slide text and speaker notes by slide index.
- **DOCX**: `python-docx`. Fallbacks: `pymupdf`, `textutil`.

Rules that make the materials branch work:

- **Trust the stated scope, pad the edges.** "Pages 30–58" or "chapter 4" means map that range only — but read a couple of pages either side so a topic that begins on page 29 isn't decapitated. Record the range in the map header (`scope:`); content outside it is out of scope, not silently included.
- **Anchor topics to the source.** With real materials, append where each topic lives to its Depth/Est line (`· Slides 22–31`, `· pp. 41–47`). This is the payoff of having the document: the student can jump straight back when a topic gets hard, and the map becomes checkable instead of trusted. The provenance header then names the actual file and range — strictly better than `roadmap + inferred`.
- **One map per coherent unit.** If the range spans several chapters or lectures, ask whether they want one map per chapter or a single overview — never a 60-topic monster that breaks the 5–15 rule.
- **Research papers are not lectures.** For a paper, hand off to the `paper-breakdown` skill rather than compete with it; other non-lecture documents (book chapters, specs, long tutorials) map fine with the three tiers.

## Building the map

1. **Enumerate concepts**, not slide titles. A concept is something you could run a tutoring session on ("scaled dot-product attention"), not a section heading ("Part 2"). Aim for **5–15 topics per lecture** — fewer means you're hiding structure, more means you've atomized into trivia.
2. **Separate three tiers**:
   - **Prerequisites** — assumed by the lecture; check against `study/_progress.md` and mark which the student already has. A prerequisite whose topic file sits in `study/mastered/` is the strongest kind of yes — it cleared a full review cycle, so tick it and move on rather than re-checking it.
   - **Core** — what the lecture actually teaches.
   - **Teased** — mentioned but not explained (lecturers do this constantly: "we'll see diffusion later", "this relates to information theory"). These are exactly what the user asked to surface — list them explicitly so they become deliberate choices ("study now" / "defer to lecture N") instead of nagging half-thoughts.
3. **Order by dependency**, and say why when the order isn't obvious ("positional encoding before the Transformer block, because the block is permutation-invariant without it").
4. **Assign a depth target** per topic — `intuition`, `derivation`, or `implementation` — following the roadmap's per-lecture instructions where they exist (e.g., CS231n L4 backprop says "derive + implement in NumPy, no autograd"; L10 video understanding says "don't go deep yet"). This stops the student from over-studying low-priority topics, which good study plans explicitly warn against.
5. **Estimate effort** roughly (e.g., "30 min", "2 h with implementation") so a session can be picked to fit the time available.

## Output format

Write to `study/maps/<course>-<lecture-slug>.md`; for material with no course (a YouTube series, a book chapter, a conference talk), slug the source instead — e.g. `english-grammar-modals.md`, `karpathy-zero-to-hero-3.md`. The `study/` workspace is the same one the `tutor` skill uses, resolved the same way: an existing `study/` in the working directory or a parent, else `~/study/` (the global default). If it doesn't exist yet, create the full structure (`study/_progress.md` index, `study/topics/`, `study/mastered/`, `study/maps/`) so the two skills stay in sync from the first map onward — and when `_progress.md` was empty or missing, mark the map's prerequisites as *unverified self-checks* rather than silently assuming them. Use exactly this structure:

```markdown
# <Course> — <Lecture title>
source: <syllabus URL | transcript | file + range | roadmap + inferred>
scope: <pages/slides/chapter range, when mapping part of a document>
created: <date>
roadmap depth guidance: <quote the roadmap's instruction for this lecture, if any>

## Prerequisites (verify before starting)
- [ ] <concept> — <one line: what it is> · already studied: <yes/no per _progress.md>

## Core topics (in study order)
- [ ] **<concept>** — <one line: what it is>. Why it matters: <one line>.
      Depth: <intuition|derivation|implementation> · Est: <time> · <source anchor, e.g. Slides 22–31, when mapping real materials>
      Study: tutor session → <topic-slug>

## Teased, not taught
- **<concept>** — mentioned in context of <what>; covered properly in <course/lecture if known>.
      Decision: <study now | defer until <where>>

## Suggested path
<2–3 sentences: what to do first, what can be skipped or merged given what
_progress.md says they already know, and what the mastery bar for this
lecture is (from the roadmap's mastery test / exit criteria if present).>
```

After writing the file, present the core-topic list briefly in the conversation and ask which topic they want to start with — the natural next step is a tutor session, not more mapping.

## Checkbox lifecycle

The `Study: tutor session → <topic-slug>` line is a contract, not decoration: the map picks each topic's slug once, and the tutor skill uses it verbatim for the topic file and for finding the checkbox to tick. A prose title alone fails silently when the tutor slugifies it differently.

Record the slug, never a folder path. A topic file starts in `study/topics/<slug>.md` and moves to `study/mastered/<slug>.md` once it graduates, so a hardcoded path would break exactly when the topic is finished. The slug is stable across the move; the tutor resolves it by looking in `topics/` first, then `mastered/`.

The `tutor` skill ticks a topic's checkbox when it reaches `mastered`. Don't tick boxes at map-creation time except verified prerequisites. When asked to map a lecture that already has a map, update it in place (preserve checked boxes and decisions) rather than creating a duplicate.
