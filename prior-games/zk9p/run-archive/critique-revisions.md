# Critique revisions — round 1

## Issues found

### Issue 1 (checklist item 12, L2 §4 — wall-block necessity)
**Where**: §4 Level 2, "Necessity per mechanic" / wall-block.
**Quote**: *"The wall column at x=8 from y=4 to y=8 splits the upper arena; without walls, all three pursuers descend straight along y from row 2..."*
**Problem**: Names the wall but does not name the specific cell where the
wall blocks a specific pursuer's specific step. Item 12 requires "naming
a specific cell, sprite, or rule that blocks every alternate path".
**Fix**: Name the concrete blocking event: "the wall at (8, 4) blocks
cyan's tick-2 step from (8, 3) to (8, 4); cyan stalls at (8, 3) and
cannot advance until the avatar shifts off column 8". Without this stall,
cyan reaches the avatar's row before the reds can be baited into a
shared cell.

### Issue 2 (checklist item 12, L2 §4 — orthogonal-major necessity)
**Where**: §4 Level 2, "Necessity per mechanic" / orthogonal-axis-preferring.
**Quote**: *"the witness specifically routes the cyan pursuer through the
wall gap by exploiting its minor-axis-first rule"*
**Problem**: States what the WITNESS does, not what blocks every
alternate path. The actual counterfactual is stronger: if cyan used the
Manhattan rule, cyan would be permanently stuck in the wall lane
(Manhattan rule on |dx|=0 falls back to y, which is wall-blocked;
Manhattan rule on tied |dx|=|dy| picks x, but the wall geometry rarely
produces this); the orth rule's minor-axis preference is what lets the
avatar release cyan from the wall lane by shifting horizontally.
**Fix**: Replace with "If cyan used Manhattan-major, cyan with avatar
on column x=8 stays stuck at (8, 3) forever (dx=0 fallback → y →
wall-blocked); the only way to release cyan is the orth rule's
minor-axis-first preference, which fires when the avatar shifts to
column x≠8 producing a non-zero dx that orth steps on first. Cyan
remaining alive forever means L2 is unwinnable; orth is therefore
strictly necessary."

### Issue 3 (checklist item 12, L3 §4 — tick-skip necessity)
**Where**: §4 Level 3, "Necessity per mechanic" / Tick-skip.
**Quote**: *"the witness exploits ACTION5 to advance pursuers by 1 free
tick at a key moment so that cyan's parity aligns with the
red-yellow-bait setup; without the tick-skip, the avatar must burn an
extra walking step to fix parity, which costs more step-budget than the
2-unit tick-skip and exceeds the budget by 1 unit"*
**Problem**: The "exceeds budget by 1" claim is unverified arithmetic; a
critique cannot validate it without a tick-perfect trace. Item 12 wants
a *structural* reason the alternate path is blocked, not an arithmetic
budget claim.
**Fix**: Replace with a structural counterfactual: "On tick T_bait the
avatar must occupy bait-cell B for the red-yellow merge to land at cell
C_RY on tick T_bait+1 (red and yellow's chase computes step
destinations from the avatar's current cell, so any avatar move on tick
T_bait shifts those destinations off C_RY). Simultaneously, the
cyan-green merge requires cyan to arrive at corridor cell C_CG on tick
T_bait+2, which forces cyan to be one step away (cell adjacent to
C_CG) on tick T_bait+1. Cyan's step on T_bait+1 is computed from the
avatar's position on T_bait+1, which (per the red-yellow geometry)
must still be B. The avatar cannot move on T_bait+1 without breaking
the red-yellow merge; the avatar cannot stay still without ACTION5;
therefore ACTION5 is the only way to advance pursuers on T_bait+1 while
preserving B."

### Issue 4 (checklist item 12, L3 §4 — phase pursuer necessity)
**Where**: §4 Level 3, "Necessity per mechanic" / Phase pursuer.
**Quote**: *"the green pursuer in L3 occupies a cell that is on the
avatar's required path"*
**Problem**: Asserts "required path" without naming the cells that make
it required. Item 12 wants the path-blocking sprite/cell named.
**Fix**: Sharpen to: "Green spawns at corridor cell (9, 9), which is
the only walkable cell between the bait region (rows y=4 through y=7)
and the corridor merge region (row y=10) — the wall structure (horizontal
wall at y=8 spanning x=2..7 and x=9..15, leaving only (8,8) and (9,8)
as openings) plus the vertical wall at x=4 from y=10..14 forces the
avatar to traverse (9, 9) to set up the cyan-green merge in the
corridor. Walking onto (9, 9) when green is tangible (any even tick) =
caught. Therefore the avatar must enter (9, 9) on an odd tick, when
green is intangible, and the phase mechanic is the only way (9, 9) is
reachable without capture."

### Issue 5 (checklist item 18d, L3 step budget)
**Where**: §4 Level 3, "Difficulty justification" / Step budget.
**Quote**: *"100 (only ~4× the witness — tighter than L1/L2 because
L3's mechanic stack is more dense, but still generous over the
witness)"*
**Problem**: `difficulty-rules.md` § d says "the budget must NOT shrink
relative to the witness as level number rises". L3 budget = 100, witness
= ~24. Ratio ~4×. L2 budget = 80, witness = 15. Ratio ~5×. L1: 60/5 =
12×. The RATIO shrinks across levels, not the absolute budget. The rule
"must not shrink relative to the witness" is about the ratio being
insufficient, not strictly non-decreasing — so 4× over witness at L3 is
fine if it's still generous, but the spec should justify why 4× is
generous *given the L3 discovery cost*.
**Fix**: Add: "L3's discovery cost is high (phase parity + ACTION5
purpose) — but the ratio is justified because L3's witness is itself
longer (~24 actions vs L2's ~15), and the absolute slack (100 - 24 = 76
extra actions) exceeds L2's slack (80 - 15 = 65). Slack increases
absolutely, even though the ratio compresses."

## Verdict

5 issues, all fixable in §4. Transition: write_spec for revision.
