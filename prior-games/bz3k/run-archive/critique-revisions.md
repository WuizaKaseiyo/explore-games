# Critique — round 2

Re-walking `mechanic-spec.md` (revision 1) against the checklist.
Most round-1 issues resolved cleanly. **One residual issue
identified at L3.**

## Resolved (PASS)

- Issue 9 (cap_band sprite size): redefined as 1×1 ✓
- Issue 5 (target green): now palette 11 yellow ✓
- Issue 6 (hazard red): now palette 13 maroon ✓
- Issue 7 (flipper hatched-X): now bowtie pattern, no
  crossing-diagonals-meeting-at-centre ✓
- Issue 4 (L3 step budget shrinking): now 60 ≥ L2's 50 ✓
- Issue 3 (multi-axis velocity): per-axis slide rule explicit ✓
- Issue 8 (L2 wrong-path stage-conflation): rewritten as
  ram-east-wall-vs-symmetric-decel post-discovery decision ✓
- Issue 10 (wake_pixel lifecycle): explicit lifecycle paragraph ✓
- Issue 11 (ek73, jd4q): added with distinguishing rules ✓

## Residual issue (must-fix)

### Issue 12 — checklist 12 (L3 cap counterfactual still has a vy-bypass)

- Section: §4 Level 3 — Layout description and Necessity (M2).
- Quote: *"Internal wall column at x = 32, y ∈ [8, 30] ∪ [34, 56]
  (3-cell gap at y ∈ [31, 33])."* and *"Three cap_band instances
  at (28, 31), (28, 32), (28, 33) — covering the full passage
  height at x = 28."*
- The wall column at `x = 32` blocks west-bound traversal
  *only at x = 32*. Once a pawn passes through the gap at
  `y ∈ [31, 33]` and reaches `x = 31, 30, 29, …`, the chamber
  between the wall column (x=32) and the cap-band (x=28) is
  open with no walls at any y. A pawn can:
  1. Cross wall-gap at e.g. y=31, vx=-2.
  2. At (29, 31), apply ↑-impulse: vy = -1. Per-axis slide
     phase: vertical slide -1 from y=31 to y=30. (29, 30) is
     NOT wall (wall column is only at x=32, y=30 — not at
     x=29). Pawn settles at (29, 30) vy=-1.
  3. Continue drifting west: (28, 30) is NOT a cap cell (cap is
     only at y ∈ [31, 33]). Pawn passes through (28, 30) without
     triggering cap.
  4. Drift to target.
- The only way to close this hole is to make the corridor
  vertically tight enough that vy can't develop. A 1-cell-tall
  corridor with walls above and below makes vy-impulses hit a
  ceiling/floor wall immediately, zeroing vy.
- Concrete fix: redesign L3 as a **1-cell-tall horizontal
  corridor** at y=32 (single row of playable cells at y=32,
  bordered by walls at y=31 and y=33 along the entire corridor).
  Cap at single cell `(28, 32)`. Flipper at single cell
  `(38, 32)`. Hazard cells fill `(44..55, 32)` directly inside
  the corridor east of the flipper, so any eastward drift past
  the flipper enters hazard. Avatar at `(32, 32)` vx=+6.
  Target at `(17, 32)`. Walls fill ALL OTHER interior cells
  (y ≠ 32 in the playable area). With this geometry: vy can
  never persist (any vy impulse hits the ceiling/floor wall
  immediately and zeroes); the only east-west passage is the
  y=32 corridor; cap and flipper are unique chokepoints; the
  flipper-or-hazard dichotomy is unavoidable.

## Other observations (no issues)

- **Checklist 21 (UI teaches)** — borderline assessment of the
  flipper's bowtie reading-as-reverse. The bowtie's pinch-inward
  geometry suggests "things passing through compress / reverse",
  which is the intended cue. The mechanic is discoverable in 1-2
  exploratory passes (the player drives the avatar in, observes
  vx negation, builds the model). Not a hard violation.
- **Witness arithmetic** in §4 L1, L2, L3 was re-derived end-to-
  end and is consistent with the per-axis slide rule and the
  cap/flipper/hazard rules. No errors found.
- **Negative similarity** (§9 table) holds: heaviest dimensions
  (8, 7, and partially 6) differ vs. wt39, ek73, jd4q.

## Action item for `write_spec` revision

Single fix: rewrite §4 Level 3 layout to use a 1-cell-tall
horizontal corridor as described under Issue 12's concrete fix.
The witness arithmetic is unchanged (same 10-action sequence
applies — the corridor restriction merely closes the vy-bypass
without altering any horizontal mechanics). Update the necessity
paragraph for M2 and M3 to reference the corridor wall-ceiling
restriction.
