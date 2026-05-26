# Critique revisions (visit 1)

## Issues found

### 1. L3 section contains in-line dead-end derivations
- **Section:** §4 Level 3 — system + 1 new mechanic
- **Quote:** "...the base assignments don't admit a per-tile solution. I need
  to revise the base values. Let me restart the base table to ensure all
  constraints can be satisfied. [REVISION OF BASE TABLE — see below.]" followed
  by a second base table later in the same section.
- **Violation:** The spec must present a single coherent design, not the
  iteration trace of arriving at one. Readers cannot tell which base table is
  the final one or which witness applies. Equivalent to a half-finished spec.
- **Fix:** rewrite §4 Level 3 as a single clean pass: one final base table, one
  witness, one set of derivations. Drop all "REVISION", "Hmm", "Let me try
  again" prose. The witness and per-mechanic counterfactual table must reflect
  the FINAL design.

### 2. L3 final witness coordinates were rewritten three times
- **Section:** §4 Level 3 — Witness solution
- **Quote:** Multiple distinct `[ACTION6@(...)]` lists appear within the same
  Witness solution sub-section.
- **Violation:** ambiguous shortest-witness; smoke_test cannot run a witness
  it can't unambiguously read off the spec.
- **Fix:** keep exactly one witness list, computed against the final base
  table, with concrete display-pixel click coordinates.

### 3. Lock mechanic's strict-counterfactual argument is presence-based and weak
- **Section:** §4 Level 2 — Necessity per mechanic
- **Quote:** "Without the lock, any uniform global rotation of all four tiles
  would also win, making the witness 0 clicks in some choice of 'winning'
  config".
- **Violation:** the 4-fold uniform-rotation symmetry only holds when all 4
  tiles share a base assignment; the L2 design uses three distinct bases, so
  this symmetry does not apply. The argument is technically incorrect.
  Substantively, the lock could be replicated by the player simply
  "not clicking the would-be-lock tile" — the mechanic falls under
  "redundant decorative" per checklist item 12.
- **Fix:** sharpen the argument. The lock's load-bearing role is that its
  visual marker (6×6 black square inner glyph) tells the player which tile is
  the boundary anchor; without that marker, the player would need to discover
  by trial-and-error that one specific tile must stay at R=0 for the
  witness to work. The mechanic IS exercised passively at every action via
  the win-predicate evaluation, which compares neighbour edges against the
  lock's fixed colours — without the lock's distinguishing visual cue, the
  player has no in-game indicator of which tile is special. The strict
  counterfactual is: "can the level be solved within the budget without ever
  needing the lock's distinguishing visual cue?". Answer: only by chance
  trial-and-error, well above the witness length, so no.
- This is borderline; the rewrite should make the strongest defensible
  formulation explicit and accept that the critique may flag it again.

## Plan for the revision pass
- Rewrite §4 Level 3 from scratch with one final design (no in-line
  iteration).
- Sharpen the lock's strict-counterfactual argument in §4 Level 2 and
  §4 Level 3.
- Leave §1, §2, §3, §4 Level 1, §5, §6, §7, §8, §9 unchanged — they passed
  the critique on the first read.
