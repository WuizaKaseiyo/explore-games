# Critique pass — round 2 (after revision)

Visit count to `critique_spec`: 2 of 10. Spec is clean.

## Checklist 1-22

| # | Item | Status | Note |
|---|---|---|---|
| 1 | Palette 0..15 + `-1` transparent | ✅ PASS | All values used: 0, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15. |
| 2 | Universal-scaffold layout | ✅ PASS | Spec §3-7 enumerate sprite bank, levels, constants, HUD, game class as scaffold expects. Verified at implement. |
| 3 | `available_actions` ⊆ [1..7] | ✅ PASS | `[1, 2, 3, 4, 5]`. |
| 4 | Exactly 3 `Level(...)` entries | ✅ PASS | L1, L2, L3. |
| 5 | 4-char ID, no collision | ✅ PASS | `hk7v` verified non-colliding against reserved + 63 priors + untracked-folder slugs. |
| 6 | Mechanics from §3.4 priors only | ✅ PASS | Objectness + physics + topology. No agentness. |
| 7 | No letters/digits/clipart/cultural | ✅ PASS | All sprites abstract; trolley + hook + rope + block + wall shapes carry no symbolic recognisability. |
| 8 | ≥ 2 distinct mechanics in env | ✅ PASS | M1, M2, M3, M4 (4 mechanics across env). |
| 9 | L1 = tutorial base dynamic system | ✅ PASS | L1 = M1 only, single block, single target, no on-screen text, witness 87 actions. |
| 10 | L2/L3 compose, not scale | ✅ PASS | L2 introduces M2 + M3 atop M1; L3 introduces M4 atop {M1,M2,M3}. Each level's witness exercises every mechanic available at that level. |
| 11 | +1-or-+2 inheritance per level | ✅ PASS | L1=1, L2=3 (+2), L3=4 (+1). All in [+1, +2]. None drop out. |
| 12 | Strict counterfactual necessity | ✅ PASS | Per-(mechanic, level) counterfactual table written explicitly with concrete cells/sprites/rules blocking every plausible alternate. M2's L1 row was removed in revision round 1 to avoid the decoratively-trivial trap. |
| 13 | Family absent from taxonomy | ✅ PASS | `overhead-trolley-hook` absent from all 25 reference rows. |
| 14 | Family absent from prior-games | ✅ PASS | Absent from all 63 prior rows. |
| 15 | Distinguishing rules vs near-misses | ✅ PASS | Concrete rules vs wa30, dj5h, vt6q, nb6t, pv5q, wb6n. |
| 16 | Win condition stated | ✅ PASS | `_check_win`: each block at (target.x+1, 53) with matching colour tag. |
| 17 | Lose condition stated | ✅ PASS | `_action_count >= step_budget` → `lose()`. |
| 18 | Difficulty floor and ceiling | ✅ PASS | Per-level (a) random-resistance, (b) human time, (c) planning depth, (d) step budget all stated. L2/L3 planning-depth justifications concrete (decision space + plausible-wrong + witness reasoning chain). |
| 19 | No hidden state | ✅ PASS | Hook position, trolley position, carrying state are all visually rendered. Carrying = block sprite directly below hook bottom. |
| 20 | Don't generate low-resolution | ✅ PASS | Grid is 64×64 directly (no upscaling). Sprites have internal pixel pattern: blocks 5×5 dual-colour grid; trolley 5×4 multi-palette internal; hook 5×4 distinctive U-claw + peg; wall 3×36 with grain; targets 7×1 dashed pattern. |
| 21 | Sprite UI ≈ sprite role | ✅ PASS | Trolley reads as "movable thing on rail"; hook reads as "thing dangling from rope, claws extended"; blocks read as "objects with internal pattern, colour-distinguished by inset"; targets read as "marker stripes on floor with same colour as their target block"; walls read as "solid pillars with grain"; floor reads as "ground". Identical-shape variants (3 blocks, 3 targets) share shape and differ only in palette to communicate same-role-different-colour-pairing. |
| 22 | ACTION7 strict-undo or absent | ✅ PASS | ACTION7 omitted from `available_actions`. |

## Novelty re-check (similarity-check + negative-similarity-check)

Re-walked against the full revised spec, not just the
`pick_mechanic` paragraph.

- **Family-level**: `overhead-trolley-hook` does not match any
  taxonomy or prior family.
- **Description-level**: closest = wa30 (delivery goal), but
  primary action differs (Cartesian gantry vs walking). Closest
  prior = dj5h (overhead element), but coupling vs single-rope.
  All distinguishing rules re-articulated in spec §9.
- **Negative-similarity (8-dim re-walk)** vs every prior the
  positive check flagged + the principle-1/2/3 axes:
  - vs wa30: shared 2 dims (3, 4); diverges on 1, 2, 5, 6, 7, 8.
  - vs dj5h: shared 1 dim (4); diverges on 1, 2, 3, 5, 6, 7, 8.
  - vs vt6q: shared 1 dim (4); diverges on 1, 2, 3, 5, 6, 7, 8.
  - vs nb6t: shared 1 dim (4); diverges on 1, 2, 5, 6, 7, 8;
    partial on 3.
  - vs pv5q: shared 1 dim (4); diverges on 1, 2, 5, 6, 7, 8;
    partial on 3.
  - vs wb6n: shared 1 dim (4); diverges on 1, 2, 3, 5, 6, 7, 8.
  
  No prior shares ≥ 3 dimensions. Below threshold. NOVEL.

## Implementation notes for `implement` state

- §5 ACTION3/4 collision check should be implemented comprehensively:
  reject the move if ANY of (rope cells, hook cells, carried block
  cells) overlap any wall sprite cell at the new position. The spec
  enumerates rope-vs-wall and carried-block-vs-wall explicitly;
  hook-vs-wall is implicit in "hook + rope + carried block move
  with it" + the global no-overlap intent. Implementation must
  cover all three.
- Same for ACTION1/2: lowering or raising the hook should be
  rejected if the hook's new footprint would overlap a wall cell
  (or a non-carried block, or pass below floor row 58).
- Block fall on release should be a snap-fall (instant) with
  rest-position computed by simulated descent stopping when
  block bottom row would equal floor row OR collide with another
  block OR collide with a wall. The reference-game-patterns.md
  preference for animated long transitions is acknowledged as a
  follow-up if smoke test reveals visual confusion; the
  base implementation snaps.

## Verdict

**PASS — proceed to `implement`.**
