# Critique revisions for cv5b spec (visit 1/10)

## Issue 1 — Item 12 (counterfactual necessity at L1) violated
**Section affected:** §4 Level 1.
**Quote:** "Witness solution: `[ACTION4×6, ACTION6@(24, 50)]` (= 6 walks
right then fire). 7 actions."
**Diagnosis:** Power-cycle is exposed via ACTION5 from L1; the player
can also win L1 in 2 actions by cycling to power-2 (range 24) and
firing from start. So the listed walk-witness is NOT the shortest, and
walk-launcher is not strictly required at L1 — it can be substituted
by power-cycle.
**Fix:** Either (a) lock power=1 at L1 (gate ACTION5), or (b) demote
L1 to a 1-mechanic tutorial (arc-fire only). Going with (b) — set L1
to a single trivial fire to learn ACTION6, drop walk from L1 mechanic
list. Adjust mechanic counts: L1=1, L2=+walk+power-cycle (+2)=3,
L3=+shield+wind (+2)=5.

## Issue 2 — Item 12 (witness numerically wrong at L3)
**Section affected:** §4 Level 3 witness.
**Quote:** Witness fires at (51, 50) from (17, 50) — distance 34
exceeds the declared power-3 range (32).
**Diagnosis:** Spec declares power-3 range 32; witness path requires
range 34. Witness does not actually win.
**Fix:** Increase power-3 range to 36 (apex 15 unchanged) and update
witness path. From (17, 50) firing at (49, 50) is distance 32 in range
36. Adjust target position from (52, 50) to (50, 50) so wind-correction
aim at (49, 50) lands on (50, 50). Re-derive arc-cell-passing-wind
calculations.

## Issue 3 — Inheritance arithmetic vs new design
**Diagnosis:** Per fix 1, mechanic counts change. New: L1=1
(arc-fire), L2=3 (+walk +power-cycle from L1), L3=5 (+shield-blocks-arc
+wind-deflects-arc from L2). Both increments are +2; both within +1 or
+2 rule. State this explicitly in §4 and verify each level's witness
exercises every prior level's mechanics.

## Issue 4 — Target ring centre coords
**Section affected:** §3 Sprite roster (target_ring).
**Diagnosis:** Spec gave target_ring as 4×3, ambiguous about which
cell is "centre" for landing detection. With wind-correction at L3,
the precise centre cell matters.
**Fix:** Redefine target_ring as 3×3 hollow ring; target placed at
(target_pos.x - 1, target_pos.y - 1) so its centre cell equals
target_pos. Arc-landing predicate checks `arc_end == target_pos`
exactly.

## Issue 5 — L1 random-resistance threshold
**Section affected:** §4 L1 difficulty bullet (a).
**Diagnosis:** Per from-tech-report.md §3.4 ("Random agents can
occasionally stumble into success at this stage, which is acceptable
by design"), L1 is allowed to be solvable by random play. The
candidate's L1 with single-target single-fire has random-win
probability ~1/4096 (close to but worse than the 1/10000 random-
resistance threshold for non-tutorial levels). State explicitly that
L1 random-stumble IS acceptable by design (per the tech report) and
that the strict 1/10000 threshold applies to L2 and L3.
