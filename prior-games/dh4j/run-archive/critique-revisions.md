# critique-revisions.md — iteration 2

The v2 spec resolved all 8 issues from iteration 1 cleanly. Two remaining issues remain. Continue to `write_spec` v3.

## Issue 1 (v2) — Pivot cell visual reads as a directional arrow

**Checklist item violated**: 7 (forbidden-elements: "an arrow shape implying direction" is a cultural convention violation).

**Offending spec section**: §3 (`pivot_cell` sprite description: "an abstract upward-arrow pattern (a vertical 1-pixel column of white at pixel column 3..4, rows 2..5, plus two horizontal 1-pixel marks at row 2, cols 2 and 5 forming the 'arrowhead')").

**Why this is wrong**: a vertical white stroke with two diagonally-converging marks at the top forms a recognizable upward-pointing arrow. Per `forbidden-elements.md`, arrow shapes implying direction are cultural conventions and are forbidden. The pivot's role is "stride bonus" not "go up", so an upward-arrow visual would also be misleading about the mechanic.

**Fix**: replace the pivot's interior pattern with a non-directional, non-symbolic abstract figure. Use a **"+" cross**: a horizontal 3-pixel white (0) bar at row 4, columns 2..6, plus a vertical 3-pixel white (0) column at column 4, rows 2..6. This produces a centered "+" cross which is explicitly allowed by `forbidden-elements.md` ("a vertical bar with two horizontal cross-strokes forming a '+' is fine; it's a topological symbol, not a letter"). The "+" symbol abstractly suggests "addition / bonus" without arrow-direction connotation.

Also tighten the `avatar_pivot_pending` decoration: remove the L-shape description (which is just three pixels and reads as ambiguous decoration); replace with a single white (0) 2×2 block at pixels (5, 1)..(6, 2) — a small abstract corner accent that visually indicates "bonus pending" without arrow or symbol content.

## Issue 2 (v2) — L3 greedy heuristic does not significantly delay the witness

**Checklist item violated**: 18 (difficulty floor and ceiling — `difficulty-rules.md` § 2c L3, planning-depth post-discovery: "Greedy / monotone-progress / follow-the-obvious-gradient strategies should not reliably win. ... Show where the heuristic diverges from the witness in 2-3 sentences: at which step the heuristic and the witness disagree, and why the heuristic's choice irrecoverably loses or significantly delays the win").

**Offending spec section**: §4 L3's planning-depth justification.

**Why this is wrong**: with the v2 pivot being re-usable, the trivial greedy heuristic ("spam UP toward goal") and the witness both take 9 actions. Greedy step 1 lands on pivot (UP from start), step 2 wastes the bonus on a wall-hit no-op (UP from pivot in yellow → wall), but then steps 3–9 follow a symmetric path to the witness (visit filter via RIGHT-RIGHT, return to pivot via LEFT-LEFT-LEFT, leap UP, walk UP to goal). Both paths total 9. Per `difficulty-rules.md` § 2c L3 operational test ("if the heuristic produces the same action sequence as the witness, it doesn't fail post-discovery — it succeeds, and (d) is unmet for this level"), the heuristic does NOT significantly delay; it ties. L3's planning-depth gate is unmet.

**Fix**: make the **pivot one-shot** — when the avatar lands on a pivot, `_pending_bonus = 1` is set as before, but the **pivot cell itself becomes a regular floor cell** after the bonus is consumed (on the next press, regardless of whether that press succeeds or no-ops). Visually: the pivot's maroon ring and "+" cross are removed; the underlying pip pattern is preserved (so the cell becomes a `floor_pip_2_yellow` or `floor_pip_2_blue` depending on legend). The avatar's `avatar_pivot_pending` rendering reverts to `avatar_normal` simultaneously.

With this rule, the greedy heuristic strictly fails:

1. UP → `(3, 5)` = pivot, `_pending_bonus = 1`, avatar shows pending. (1)
2. UP from `(3, 5)` 2-pip yellow (stride-2) + 1 = stride-3 → destination `(3, 2)` = wall → no-op. Bonus consumed; pivot cell consumed; cell becomes `floor_pip_2_yellow`. (2)
3. RIGHT from `(3, 5)` 2-pip yellow = stride-2 → destination `(5, 5)`. (3)
4. RIGHT from `(5, 5)` stride-1 → `(6, 5)` = filter; legend → Blue. (4)
5. LEFT from `(6, 5)` stride-1 blue → `(5, 5)`. (5)
6. LEFT from `(5, 5)` stride-1 blue → `(4, 5)`. (6)
7. LEFT from `(4, 5)` stride-1 blue → `(3, 5)` (now a regular `floor_pip_2_blue` — pivot consumed). No bonus reset. (7)
8. UP from `(3, 5)` 2-pip blue (stride-3) + 0 (no bonus) = stride-3 → destination `(3, 2)` = wall → no-op. (8)
9. The greedy player is stuck — pivot consumed, cannot regain bonus, cannot leap 3-row wall. Remaining actions waste step budget until lose. **Irrecoverable failure**.

Witness path with one-shot pivot is unchanged (filter first, pivot last) and stays at 9 actions. Greedy diverges from the witness at step 1 (greedy chooses UP, witness chooses RIGHT); the greedy's choice irrecoverably consumes the pivot, leaving no way to achieve stride-4. ✅

Update spec §3 (sprite descriptions for pivot consumption transition), §4 L3 M4 description, §4 L3 counterfactual table (note that the pivot is single-use), §4 L3 planning-depth (re-trace the greedy heuristic to show irrecoverable failure), and §6 internal-state (add the consumption flag if needed; alternatively, just remove the pivot tag from the cell's sprite at consumption time).

## Revision summary

Move back to `write_spec` for v3. The v3 spec should:
- Update §3 `pivot_cell` and `pivot_floor_pip_2_yellow/blue` sprites: replace the upward-arrow interior with a centered "+" cross (allowed topological symbol).
- Update §3 `avatar_pivot_pending`: simplify the corner decoration to a 2×2 white block (abstract corner accent).
- Update §4 L3 M4 description: pivot is **one-shot** (consumed on bonus consumption). Visual: pivot maroon ring is removed; the cell becomes a regular `floor_pip_2_*` matching the current legend's variant.
- Update §4 L3 counterfactual table to reflect one-shot pivot.
- Update §4 L3 planning-depth justification: greedy heuristic IRRECOVERABLY FAILS (not "ties witness"). Trace the failure concretely.
- Update §6 internal-state: optionally track `_pivot_consumed` (set when bonus is consumed); alternatively, the level itself can be updated to swap the pivot sprite to a floor variant at consumption time.

This is critique iteration **2 of 10**. 8 remaining.
