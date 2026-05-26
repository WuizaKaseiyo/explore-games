# Critique pass — `mechanic-spec.md` (visit #06)

After the visit #05 revision addressed all four
critique-revisions.md items, the spec passes the
`design-constraints/checklist.md` gates and the
`mechanic-novelty/` similarity tests.

## Checklist 1–22

| # | Item | Verdict | Notes |
|---|---|---|---|
| 1 | Palette 0..15 + transparent | ✅ PASS | All sprite pixel matrices use 0..15 plus -1; verified per-sprite. |
| 2 | Universal scaffold | ⏳ implement-time | Will be enforced in `implement` against `code/universal-scaffold.md`. |
| 3 | `available_actions ⊂ [1..7]` | ✅ PASS | `[5, 6]` — minimal subset. |
| 4 | Exactly 3 levels | ✅ PASS | L1 / L2 / L3 declared in § 4. |
| 5 | 4-char ID, lowercase, opaque, non-colliding | ✅ PASS | `xz5g`; verified against 25 reference + 45-row index + 9 untracked dirs. |
| 6 | Mechanics from `core-knowledge-priors.md` | ✅ PASS | Objectness + basic geometry/topology (rotation around point). No physics or agentness needed. |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS | All sprites are abstract (rings, filled bodies with corner-pips, plus-pip squares). The "+" pip in anchor_pin is explicitly OK per `forbidden-elements.md` ("topological symbol, not a letter"). The direction_indicator's corner-pip is asymmetric square + dot, not arrow / glyph. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | L1=2, L2=3, L3=5. |
| 9 | L1 tutorial reduced state space, no on-screen text | ✅ PASS | Just avatar + target + step bar; no companion, no anchor_pin, no widget. |
| 10 | L2/L3 difficulty by composition, not size scaling | ✅ PASS | L2 adds companion-deliver (multi-pawn coordination); L3 adds visit-checkpoint and direction-toggle. Grid size and per-rotation cost are constant; difficulty rises through composition. |
| 11 | Mechanic inheritance & +1-or-+2 per level | ✅ PASS | L1: M1+M2 (N=2). L2: M1+M2+M3 (N+1=3, +1 new). L3: M1+M2+M3+M4+M5 (M+2=5, +2 new). All earlier mechanics carry forward and remain witness-required. |
| 12 | Strict counterfactual necessity | ✅ PASS | Per-mechanic table below — every (mechanic, level) row answers "no" with a concrete cell/sprite/rule reason. M4 (visit-checkpoint) redesign closed the visit #04 hard fail; the witness now directly triggers M4's distinguishing behavior at CCW1. |
| 13 | Family absent from taxonomy | ✅ PASS | `arena-pivot-rotate` not in 25-game taxonomy. Closest: `cn04 nub-pair-glyph` (per-piece self-rotate) — distinguishing rule cited. |
| 14 | Family absent from prior-games index | ✅ PASS | 45 indexed entries scanned; closest is `vy3k region-swap-arrange` (4-quadrant rotate/swap). 9 untracked dirs scanned; closest is `hp9c pinwheel-cell-rotate` (4-cardinal-cell rotate around clicked centre). Distinguishing rules cited per § 9. |
| 15 | Concrete distinguishing rules | ✅ PASS | § 9 articulates concrete rules vs cn04, vy3k, hp9c, pv5q, qj4r/rj5w/wj7d, qz73; each rule names the geometry/state/scope difference. |
| 16 | Win condition | ✅ PASS | § 7 dual-clause predicate (target-match AND visit-checkpoint). Pseudocode included. |
| 17 | Lose condition | ✅ PASS | § 8 step-budget exhaustion via private `_steps_left`. |
| 18 | Difficulty floor and ceiling | ✅ PASS | L1 / L2 / L3 each have (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget bullets. L2/L3 planning depth named decision-space + plausible-wrong + reasoning chain. |
| 19 | No hidden state — visible cues | ✅ PASS | `_pivot` → halo sprite at the clicked cell. `_direction` → widget pip-corner at L3. `_visited_pins` → anchor_pin's centre 2×2 stamped 14 → 11. `_steps_left` → bottom-row HUD bar. |
| 20 | Don't generate low-resolution game | ✅ PASS | grid_size = (64, 64) on every level — no sub-cell scaling; primary sprites 6×6 (avatar, companion, targets, halo) and 4×4 (anchor_pin, direction_indicator) with internal pixel pattern. |
| 21 | Sprite UI ≈ sprite role | ✅ PASS | Avatar / companion: filled body with frame and pips reads as "movable pawn". Targets: hollow ring with transparent centre reads as "slot wanting a pawn". Anchor_pin: dark frame with green centre reads as "checkpoint pad" (palette flips on visit). Direction_indicator: bordered square with corner-pip widget reads as "interactive toggle". Identical-shape avatar vs avatar_target with same palette = correlated-role cue (per checklist 21 rule). |
| 22 | ACTION7 strict-undo or absent | ✅ PASS | ACTION7 omitted from `available_actions`. No undo verb in this game. |

## Strict-counterfactual table (item 12 detail)

| Level | Mechanic | Solvable without triggering M? | Concrete reason |
|---|---|---|---|
| L1 | M1 pivot-set | no | `_pivot` starts as None; ACTION5 with None pivot is no-op. Avatar at (12, 32) cannot reach target (32, 12) without rotation. |
| L1 | M2 commit-rotate | no | ACTION5 is the only motion verb; ACTION6 only sets pivot. |
| L2 | M1 | no | Same as L1. |
| L2 | M2 | no | Same as L1. |
| L2 | M3 companion-deliver | no | Win predicate AND-s avatar-on-target with companion-on-target; rotation transforms ALL rotatable sprites in lock-step (M2 contract), so any avatar-delivering sequence forces companion-delivery as a side-effect; the witness's two CWs around (32, 32) deliver both. |
| L3 | M1 | no | Same. |
| L3 | M2 | no | Same. |
| L3 | M3 | no | Same as L2. |
| L3 | M4 anchor-pin-visit-checkpoint | no | Win predicate adds visit-clause for `anchor_pin (12, 32)`. CW path within budget never visits (12, 32) at the right pawn-state (CW3 visits (12, 32) but pawns are off targets and recovery requires more rotations than budget allows; the CW orbit around (32, 32) is closed, so additional CW rotations cycle through the same 4-cell orbit without ever simultaneously placing both pawns at targets and visiting (12, 32)). The unique short visit is via CCW1 around (32, 32), which the witness uses; CCW1 lands avatar at (12, 32) → triggers M4 directly. |
| L3 | M5 direction-toggle | no | M4 requires visiting (12, 32). The only short rotation that lands a rotatable sprite at (12, 32) from start is CCW1 around (32, 32). CCW is unavailable until the player toggles direction via the `direction_indicator` widget — that click IS the M5 trigger. |

## Novelty re-check

### similarity-check.md (positive test)

For each near-miss in taxonomy + prior-games index, the spec
articulates a concrete distinguishing rule. Re-checked the
fully-fleshed L1/L2/L3 witnesses against vy3k's deep-analysis
(via `prior-games/vy3k/mechanism-detail.md` — the deep
counterpart to taxonomy entries for prior-games per
`finalize/mechanism-detail-template.md`):

- vy3k's verb is a quadrant-bounded rotate-or-swap; xz5g's is
  a whole-arena pivot-rotate. Verb cardinality differs.
- vy3k's pivot is one of 4 fixed quadrant centres; xz5g's
  pivot is a 4096-cell free choice.
- Visual signatures differ (vy3k has a black divider-cross
  partition; xz5g has none — single continuous arena).
- Cast differs — xz5g introduces direction-toggle widget +
  visit-checkpoint anchor_pin not present in vy3k.

vy3k → NOVEL with concrete rules.

### negative-similarity-check.md (negative test, re-run on full spec)

Walking 8 dimensions vs vy3k (closest single prior):

| Dim | Shared? |
|---|---|
| 1. Board | partial (sprites + targets shared; anchor_pin distinct) |
| 2. Input | shared (click + ACTION5) |
| 3. Goal | partial (pawn-on-target shared; visit-checkpoint distinct at L3) |
| 4. Lose | shared (step budget) |
| 5. Cast | distinct (anchor_pin visit-checkpoint + direction widget vs quadrant frames + locks) |
| 6. Visual signature | **distinct** (continuous arena + halo + corner widget vs 4-quadrant + divider + selection frames) |
| 7. Pixel grain | **distinct** (6×6 / 4×4 with internal pattern vs 4×4 hop blocks) |
| 8. Core dynamic | **distinct** (continuous-pivot vs discrete-quadrant — Principle 3 axis) |

Sharing on the Principle-weighted dimensions (6, 7, 8): zero.
Sharing on universal-platform dimensions (2, 4, parts of 1):
expected. Verdict: **NOVEL** under the negative-similarity
test.

## Overall verdict

**PASS** on all 21 spec-time gates and **NOVEL** on both
similarity tests. The spec is ready for `implement`.

Visit count: critique_spec entered #04 then #06 = 2 visits
(below the 10-visit cap).
