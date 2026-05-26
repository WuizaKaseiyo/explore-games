# vp6h — shadow-cast-collect

## Summary

The player walks a 16×16 grid as a small avatar sprite, collecting
scattered crystal sprites. Yellow lantern bars sit on rails at the
playfield's top edge and (at level 3) the bottom edge; each lantern
illuminates 5 columns of the grid, but grey vertical pillars cast
parallel-ray shadows behind themselves into the lit columns. A
crystal is pickable only while the avatar's reference cell is in
shadow with respect to *every* active lantern (intersection rule);
walking onto a lit crystal is a forgiving no-op. The player slides
each lantern by clicking any column on its rail; sliding redefines
the lit columns and therefore the safe-pickup zones. Win when every
crystal in the level is collected; lose if the per-level step budget
is exhausted.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Avatar moves up one cell | always (movement guard checks walkability) |
| ACTION2 | Avatar moves down one cell | always (movement guard checks walkability) |
| ACTION3 | Avatar moves left one cell | always (movement guard checks walkability) |
| ACTION4 | Avatar moves right one cell | always (movement guard checks walkability) |
| ACTION6 | Click; maps to grid coords. If `gy == 0`, slide top-lantern to be centred on `gx`. If `gy == 15` and the level has a bot-lantern, slide bot-lantern likewise. Otherwise no-op. | always |

`available_actions = [1, 2, 3, 4, 6]`.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 = shadow-pickup-rule (fixed lantern; single crystal in the only pillar's shadow). | Single pillar at col 7 rows 3..7 shades the crystal at (7, 11..12). Step budget 40. Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION1]` (6 actions): walk avatar from (2, 13) to (7, 12); pickup fires because col 7 row 12 is below the pillar → top-shaded. |
| 2 | M1 + M2 = lantern-slide. Three crystals in default columns 2 / 6 / 14; the col-6 crystal is currently lit; the lantern must be slid leftward to shade it. | Crystal A at col 2 (default-shaded by being outside cols 5..9); crystal B at col 6 (currently lit; no pillar above); crystal C at col 14 (default-shaded; pillar at col 14 rows 5..7 protects it under any lantern position). Sliding the lantern leftward to cols 0..4 exposes col 2 (no pillar → A would become lit) so the witness must collect A first. Step budget 70. Witness 25 actions: walk to A → walk to C → click top rail at col 2 → walk left to B. |
| 3 | M1 + M2 + M3 = dual-shadow-overlap. A second lantern on the bot rail makes safety the intersection of two shadow regions. | Top-pillars at col 2 rows 5..7 and col 10 rows 5..7; bot-pillar at col 13 rows 8..10. Three crystals: A at (col=2, row=11..12), B at (col=13, row=4..5), C at (col=7, row=8..9). Default lanterns (top@cols 5..9 + bot@cols 5..9) leave A and B safe but C unsafe (col 7 lit by both). Pre-positioning top@cols 0..4 and bot@cols 10..14 makes all three crystals double-shaded simultaneously. Step budget 120. Witness 25 actions: click top rail at col 2 → click bot rail at col 12 → walk to A → walk to C (re-routing via row 13) → walk to B (re-routing around the col-13 bot-pillar via col 11). |

## Win condition

Per level, when every crystal sprite tagged `crystal` has had its
interaction set to `InteractionMode.REMOVED`, `self.next_level()`
fires. After level 3 completes, the engine's level-list-end behaviour
calls `self.win()`.

## Lose condition

When the per-level step counter (decremented one per action) hits
zero, `self.lose()` fires.

## Internal state

- `_top_lantern_x: int` — leftmost column of the top-lantern's 5-cell
  range.
- `_bot_lantern_x: int | None` — leftmost column of the bot-lantern;
  active only when the level's `has_bot_lantern` data is True (L3).
- `_has_bot_lantern: bool` — set per level in `on_set_level`.
- `_lit_top: set[tuple[int, int]]` — cells lit by the top-lantern,
  recomputed after every lantern move (or per-level setup).
- `_lit_bot: set[tuple[int, int]]` — same for the bot-lantern; empty
  set at L1, L2.
- `_opaque_by_col: dict[int, set[int]]` — index of pillar pixel rows
  per column; refreshed once per level in `on_set_level`.
- `_step_budget: int` and `_steps_taken: int` — per-level countdown.
- `_step_hud: StepCounterHud` — single `RenderableUserDisplay` widget
  that paints frame[63, :] with palette 12 (orange) for steps
  remaining and palette 4 (off-black) for spent steps.

## Notable code patterns

- **Per-cell ground repaint each step.** A 16×16 `ground` sprite at
  layer -2 holds the dynamic lit/shaded state. After every shadow
  recompute, every cell's pixel is set to palette 1 (lit) or palette
  4 (shaded). This is the visual signal the player reads to decide
  where pickup will succeed.
- **Per-column shadow occlusion via opaque-by-column index.** Pillar
  pixels are pre-indexed by column at level start; for each lit
  column, the smallest opaque row caps top-lantern light from above
  (cells above the pillar are lit; cells below are shaded), and the
  largest opaque row caps bot-lantern light from below. O(W·H) per
  recompute; trivial for the 16×16 grid.
- **2×2 avatar with axis-aligned bounding-box pickup.** The avatar's
  `(x, y)..(x+1, y+1)` footprint is checked for AABB overlap against
  each crystal's bounding box; on overlap the avatar's reference cell
  (x, y) is shadow-checked. Lit overlap is a forgiving no-op (no
  destruction). This is the cleanest way to keep multi-cell sprites
  consistent under collision-light interaction.
- **Single-axis lantern rail with click-to-centre.** ACTION6 click
  coords are converted via `camera.display_to_grid`; the click is
  routed to the top or bot rail by `gy`; the lantern's leftmost
  column is set to `clamp(0, 11, gx - 2)`. No selection state, no
  drag state — clicking a column commits a teleport.
- **Forgiving lit-no-op semantics.** Walking onto a lit crystal
  reaches the pickup attempt, fails the shadow check, and falls
  through; the avatar continues. This avoids the harsh "lit = destroy
  the crystal → unrecoverable level" pattern and makes the
  L3-intersection-rule discovery happen via observation rather than
  destruction.
