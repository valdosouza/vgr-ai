---
name: retain-knowledge
description: The cycle that makes the engine learn. Use at the END of any task that produced new knowledge — a decision, a pattern, a repeatable procedure, documentation, a lesson learned. Mandatory even without an explicit request.
---

# Skill: Retain Knowledge (the cycle that makes the engine learn)

**When to use**: at the END of any task that produced new knowledge — a decision, a
pattern, a repeatable procedure, documentation, a lesson learned. Mandatory, even
without an explicit request. It is what turns every migration into training for the
engine: "humans are good thinkers with terrible memory" — the process compensates for
the memory.
**Scope**: method

---

## 1. What to retain (quick test)

Retain if the answer is YES to any of these:
- Would a future session WITHOUT this conversation need it to avoid a mistake?
- Was it an owner decision that is not in the code? (decisions are never lost)
- Is it a procedure that will repeat? (→ skill)
- Did it change a project's state? (phase completed, structure renamed, new endpoint)

Do NOT retain: what the code/git already records by itself; details that only matter
to this conversation.

## 2. Where each type goes

| Type of knowledge | Destination | Format |
|---|---|---|
| Architecture/business decision | "Recorded decisions" section of the current phase prompt | Continuous numbering (never renumber); code cites the number in comments |
| Permanent pattern (valid forever) | Domain reference doc (e.g., database standards) | Distilled, without history — only the current rule |
| Repeatable procedure | `<project>/skills/<verb-object>.md` — or the generic skills if valid for any project | When to use + numbered workflow + real situations |
| Module/feature documentation | `<project>/NN-NAME.md` (sequential numbering) | Status, files, how to test |
| Draft / prompt being optimized | `prompts/` | Working version; never loose at the root |
| Completed phase prompt | `<project>/prompt_phaseN_<name>.md` | Closed prompt; the source draft goes to HISTORY/ |
| One-off analysis/report | `HISTORY/` | With its INDEX updated |
| **METHOD insight (portable)** | **The engine's product journal** (1 line: date, insight, origin) | What was learned here serves any case — distilled, without case content |

## 3. Mandatory chained updates

When creating/changing any file above, update IN THE SAME task:

1. **Central index** — the project's list, the workflows (if one was born), the
   history table (date + what + version), the quick map if it changed
2. **Did the project's state change?** → the root rules file ("Current state" section)
3. **Is there persistent agent memory?** → update the topic's file + its index
4. **Did an old instruction become obsolete?** → do not delete: mark it SUPERSEDED,
   pointing to the decision that replaced it

## 4. Writing conventions

- File names: kebab-case for skills, UPPERCASE.md for reference docs
- Every doc starts with: **Status/Version, Origin, References** and **Scope**
  (`method | <case> | mixed` — see the `scope-census` skill)
- Decisions cite the why in 1 line (even — and especially — the controversial ones:
  "kept X — owner's decision, risk recorded")
- Skills gain a "real situations" section when they were born from mistakes found

## 5. Exit checklist (copy into the task's final answer)

- [ ] New knowledge identified and classified (table above)
- [ ] File created/updated in the right place, with Scope
- [ ] Central index updated (list + history)
- [ ] Root rules updated if the project's state changed
- [ ] Agent memory updated (if applicable)
- [ ] Method insight (if any) distilled into the product journal
- [ ] Nothing obsolete left without a SUPERSEDED mark
