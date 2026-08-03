---
name: decision-rounds
description: Turns a draft of ideas (loose text, notes, pasted DDL, the business owner's master prompt) into an executable phase/project plan through numbered, permanent decisions. Phase 3 of the engine — the business owner DECIDES; nothing is decided for them.
---

# Skill: Decision Rounds (draft → executable prompt)

**When to use**: whenever there is a draft of ideas (loose text, notes, pasted DDL,
the business owner's master prompt) that needs to become an executable phase/project
plan. It is Phase 3 of the engine: the business owner DECIDES; nothing is decided for
them.
**Origin of the method**: case zero — a draft of hundreds of lines became a closed
prompt with dozens of numbered decisions, validated DDL, and code with tests.
**Scope**: method

---

## The method

The draft is not silently corrected. It is **organized as-is** and the problems become
**numbered questions** that the project owner decides. Every decision is recorded
permanently. Repeat until pending items reach zero.

### Round 0 — Organize
1. Restructure the draft into the standard phase-prompt format:
   `Context → Objectives → Workflow → Grouped specifications → Success criteria`
2. Keep the content faithful; mark problems with ⚠️ at the exact spot + a reference to
   the question
3. Create the section **"⚠️ Pending questions (round N)"** — each item:
   **problem → evidence → suggested correction** (objective questions, with options
   when possible)

### Rounds 1..N — Decide and apply
1. The owner answers the questions (in chat or by editing the file directly — always
   **re-read the file before editing**, it changes between rounds)
2. Apply each decision to the document; sweep for residues with textual search (old
   names, removed columns, orphaned references)
3. Move decisions to the permanent section **"Recorded decisions"** (numbering is
   continuous across rounds — it becomes the project's logbook)
4. New problems discovered while applying → a new round of questions
5. Convergence: **"Pending questions: None"** + a list of what was explicitly left for
   future phases

### Closing — Execute
1. Generate the deliverables (scripts, code, docs) **citing the decision numbers in
   comments** (`-- decision 14`) — full traceability
2. Validate programmatically (SQL parser, compiler, tests) before delivering
3. Copy the final prompt to the project's folder in the knowledge base and distill new
   patterns into the reference docs; the source draft goes to HISTORY/

## Rules that make it work

- **Never decide for the owner** on architecture/business items — suggest with
  "(Recommended)" and wait
- **Never lose a decision**: once decided, it enters the permanent section with a
  number — and numbers are NEVER reused/renumbered
- **Always sweep for residues** after every naming change (search for the old names)
- **Distinguish** "correcting" (an objective error) from "deciding" (a choice between
  valid alternatives) — only the second becomes a question
- Deferred items go to "Out of scope / future phases" — they do not disappear, they
  change place
- A decision can be REVISED in a future round: it gains the note "REVISED by decision
  N", it is never deleted

## Section structure of the final prompt

```markdown
# Prompt — Phase N: <name>
## Context
## Objectives (numbered)
## Workflow (step-by-step flows, with decision tables)
## <Specifications grouped by domain>
## Deliverables (table: item → what it does → when)
## Recorded decisions (1..N, permanent)
## Pending questions (zeroed at closing)
## Out of scope for this phase
## Success criteria (numbered, testable)
```

## Why this is the engine's differentiator

Anyone can plug an AI into a legacy repository. What cannot be copied is the
human-in-command process: the AI organizes, evidences, and suggests; the business
owner decides; the decision becomes a permanent record traceable down to the line of
code. In systems with decades of history, this is what keeps the rewrite from
repeating the mistakes the legacy already made — and from losing the right calls it
accumulated.
