# critique_spec

## Description
Independently review `mechanic-spec.md` against:

1. Every item in `design-constraints/checklist.md` (numbered
   1-26 — verify all of them). Items 11 (mechanic inheritance
   / +1-or-+2 per level), 12 (strict counterfactual necessity
   / no trivial fallback), 13 (minimum-action witness — no
   one-action or repetitive passes), and 26 (mechanic adds a
   new rule, not a new map) are the load-bearing per-level
   mechanic gates; item 19 covers difficulty floor and ceiling;
   item 24 gates animation for non-local effects; item 25 gates
   a lives mechanism when hard-death is possible.
2. The novelty rules in `mechanic-novelty/similarity-check.md`,
   re-running the comparison on the full spec (not just the
   mechanic-family name). For taxonomy near-misses, consult the
   authoritative deep-analysis at
   `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`
   to validate that the distinguishing rule actually holds against
   the deeper view, not just the taxonomy one-liner.
   (`skills/mechanism-details/<id>.md` is a shorter first-pass
   summary; consult if useful, but the deep-analysis governs.)
3. The negative-similarity test in
   `mechanic-novelty/negative-similarity-check.md`. The fleshed-
   out spec is more concrete than the one-paragraph candidate
   that `pick_mechanic` evaluated; sometimes a candidate that
   passed the negative test at pick time has drifted into too-
   much-overlap by L2 or L3 of the spec. Re-walk the seven
   dimensions and reject if the candidate now resembles any
   single prior on three or more.

Treat the critique as adversarial. **Be patient — a low-quality
game that limps through the gates is worse than no game at all.
Use the revision budget generously rather than rubber-stamping a
borderline pass.**

Common failure modes you must look for:

- Spec drifted: level 2 or level 3 introduces a mechanic that is now
  too similar to an existing taxonomy entry, even though level 1
  wasn't.
- Constraint violation: a sprite's pixel pattern accidentally
  reads as a digit or letter (`forbidden-elements.md`).
- Pseudo-multi-mechanic: the spec claims two mechanics but level 3
  uses only one of them.
- Tutorial too hard: level 1 requires composition that wasn't
  introduced.
- Wrong level count: the spec lists more or fewer than 3 levels.

**Maximum revision cap.** This state may be entered at most 10 times
per run. On the 10th entry, if the spec still fails, write a brief
`workspace/error.md` explaining what could not be resolved and halt
the run instead of looping back to `write_spec` again. Track the
visit count by reading `workspace/logs/state_log.md` (count rows
where state == `critique_spec`).

If any issue is found, transition back to `write_spec`. If clean,
transition to `implement`.

## Skills
- skills/global
- skills/design-constraints
- skills/mechanic-novelty
- skills/mechanism-details *(quick-reference; the deeper
  evidence is at
  `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`)*

## Next States

### write_spec
**Condition:** Any item in `design-constraints/checklist.md` is
violated, OR the novelty check flags a too-similar entry without
a concrete distinguishing rule, OR a structural issue (level
count, action mapping, etc.) is found, AND this is at most the
9th visit to `critique_spec` (so a transition back gives
`write_spec` a 10th attempt before the cap fires).
**Deliverables:**
- critique-revisions.md: A numbered list of issues. For each:
  (a) which checklist item or novelty rule is violated,
  (b) the offending spec section + quote,
  (c) a concrete suggestion for how to fix.

### implement
**Condition:** All checklist items (1-26) pass AND the novelty
check returns NOVEL for every taxonomy + prior-game row.
**Deliverables:**
- critique-pass.md: One line per checklist item plus the novelty
  verdict, with explicit "✅" or "PASS" markers. Brief enough to
  read in 30 seconds.
