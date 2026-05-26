# lq5x — lantern-cone-illuminate

## Summary

A single small lantern pawn projects a 3-cell-wide directional cone
of "lit" cells out into a darkened arena; the player walks the
lantern with arrow keys (ACTION1-4) and rotates the cone facing 90°
clockwise with ACTION5. A target ring is "lit" when, at any post-
action tick, its centre cell is inside the cone AND the cone's
current colour matches the target's colour. The level wins when
every target is lit and loses when the per-level step counter
exhausts; walking off the grid is a silent no-op that still consumes
a step. From level 2 onward, wax-pickup sprites extend the cone
range R by +2 each on contact (one-shot, removed when consumed);
from level 3 onward, filter cells re-tint the cone's colour to match
the filter's colour for as long as the cone covers any filter and
persistently afterward (until a different-coloured filter is
encountered).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | walk UP — lantern's y decreases by 1 if in-bounds. Cone moves with the lantern. | Always offered. Consumes 1 step regardless of whether the move was in-bounds (off-grid moves are silent no-ops). |
| ACTION2 | walk DOWN — y increases by 1 if in-bounds. | Same. |
| ACTION3 | walk LEFT — x decreases by 1 if in-bounds. | Same. |
| ACTION4 | walk RIGHT — x increases by 1 if in-bounds. | Same. |
| ACTION5 | rotate cone facing 90° clockwise: N→E→S→W→N. Lantern position unchanged. | Always offered. Consumes 1 step. |

ACTION6 and ACTION7 are not in `available_actions`. There is no
action gating — all 5 actions are valid every turn (the engine's
default `_get_valid_actions` is used). After every action the engine
recomputes the cone, scans for any filter cell inside the cone (if
multiple filters tie, the closest-by-Manhattan to the lantern wins;
ties broken by sprite-list order — fully deterministic), updates
`cone_color` to the matched filter's colour, and evaluates the
lit-target predicate.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | walk + cone-rotate (base dynamic system, N=2) | 12×12 open arena. R=4. 2 yellow targets at centres (3, 8) and (8, 6); lantern starts at (3, 3) facing N. Witness `[5, 4, 2, 2, 5]` rotates to E, walks RIGHT once and DOWN twice to bring B into the E-cone, then rotates to S to bring A into the S-cone. Walk-only refutation: with N-facing only, walking to either target's vantage requires 11+ walks > step budget 10. |
| 2 | + wax-pickup-extends-range (N+1=3) | 14×14 arena. R=2 initial. 1 wax pickup at (3, 6) (+2 to R). 2 yellow targets at centres (3, 1) and (3, 12). Lantern starts at (3, 7) facing N. Witness `[1, 1, 2, 2, 2, 2, 5, 5]` (8 actions) walks N onto pickup (R: 2→4), continues N to bring A into cone, walks back S past start, rotates twice to S, lights B. Walk-no-wax refutation: detour around pickup costs 17 actions > budget 12. |
| 3 | + filter-changes-cone-colour (N+2=4) | 14×14 arena. R=2 initial. 1 wax pickup at (3, 2) (+2 to R). 1 red filter at (2, 8). 1 yellow target at centre (8, 2); 1 red target at centre (2, 11). Lantern starts at (2, 2) facing E. Witness `[4, 4, 3, 3, 5, 2, 2, 2, 2, 2]` (10 actions) walks RIGHT onto pickup (R: 2→4), one more RIGHT to bring Y into E-cone (cone yellow, Y lit), walks LEFT back, rotates to S, walks DOWN until S-cone covers filter (cone goes red), continues DOWN until R is in the (now red) S-cone. **Adjacent-action commute that breaks solvability**: swapping witness steps 2 and 3 (walk RIGHT then walk LEFT vs walk LEFT then walk RIGHT) prevents Y from being lit during the only window when the cone is yellow; subsequent step 7 turns the cone red permanently (no yellow filter exists in this level to revert), so Y (yellow) becomes un-lightable and the level is unsolvable. |

## Win condition

Plain English: the level wins when every target sprite has at some
point during the level had its centre cell inside the cone with the
cone's current colour matching the target's colour. Once a target
is lit, it stays lit for the rest of the level.

Predicate: `all(id(t) in self.lit_targets for t in current_level.get_sprites_by_tag("target"))`. Evaluated after every action; if true,
`self.next_level()` is fired (and the engine auto-fires
`self.win()` after the last level transitions).

## Lose condition

Plain English: the level (and run) ends in a loss when the player's
step count reaches the per-level step budget without the win
predicate firing. There is no other lose path — no hazard sprite,
no enemy, no falling off the edge. Walking off the grid is a silent
no-op that still consumes a step.

Predicate: `if self._action_count >= self.step_budget: self.lose()`
at the start of `step()`.

## Internal state

- `lantern: Sprite | None` — the placed lantern sprite for the
  current level. Cached from `level.get_sprites_by_tag("lantern")[0]`
  in `on_set_level`.
- `facing: int` — one of `0, 1, 2, 3` representing N, E, S, W.
  Reset to a per-level start value (read from
  `level.get_data("initial_facing")`).
- `cone_range: int` — current R. Reset to per-level initial in
  `on_set_level`. Incremented by `WAX_BONUS = 2` on pickup.
- `cone_color: int` — palette value of the cone (default 11
  yellow). Reset per-level. Updated when cone covers a filter.
- `step_budget: int` — per-level max actions. Read from
  `level.get_data("step_budget")`.
- `lit_targets: set[int]` — set of `id(target_sprite)` values
  that have been lit so far this level. Reset per-level. Identity-
  keyed (not name-keyed) because target Sprite clones share the
  same `name` field.

Per-level configuration via `level.get_data`: `step_budget`,
`initial_facing`, `initial_range`, `wax_bonus` (defaults to 2 if
absent).

## Notable code patterns

- **`ConeOverlay(RenderableUserDisplay)` HUD widget**: the cone
  is rendered NOT as a sprite but as a HUD overlay that paints
  background-coloured (palette 5) pixels inside the cone region to
  a "lit" palette (palette 1 off-white when cone is yellow; palette
  13 maroon when cone is red). Background-only painting means
  sprites (lantern, targets, pickups, filters) inside the cone
  remain visible — the cone "brightens" empty cells without
  obscuring foreground content. The widget reads game state via a
  `configure(...)` setter called from the game class after every
  action. Pattern: any cosmetic effect that depends on
  game-state-derived geometry (line-of-sight, fog-of-war, heat-
  maps) can use this same approach instead of mutating sprite
  pixels.
- **Identity-keyed lit-set**: `lit_targets` keys on `id(t)` rather
  than `t.name` because Sprite clones from a single template share
  the same `name`. If multiple instances of the same sprite
  template are placed in a level (here: two yellow target rings in
  L1 and L2), keying on name would mark them all lit when only one
  is. Identity is the correct hash key for "this specific clone".
- **Filter pass before target pass in `_scan_filter_and_targets`**:
  the per-action recompute first determines what colour the cone
  is THIS tick (by scanning filter cells in the cone), then
  evaluates whether each target's centre cell is in the cone with
  that colour. Order matters because changing cone colour mid-scan
  would produce inconsistent target lighting.
- **Closest-filter-wins tie-break**: when multiple filter cells
  fall in the cone simultaneously, the Manhattan-closest filter to
  the lantern wins, with ties broken by sprite-list order. This is
  fully deterministic and replayable across runs (no
  iteration-order surprises).
- **Per-level camera resize**: `on_set_level` reads
  `level.grid_size` and assigns `self.camera.width = gw;
  self.camera.height = gh`, so the camera scales the small grids
  (12×12 in L1; 14×14 in L2/L3) up to fill the 64×64 frame
  consistently. Without this, smaller levels would render in a
  small top-left corner of the 64×64 output.

## Anti-patterns / lessons

- **Don't key a state set on `Sprite.name`**: clones from the same
  template share the name. Keep it identity-keyed (`id(s)`) or
  position-keyed if positions are stationary and unique.
- **Cone overlay must run BEFORE the step counter HUD** in the
  Camera's `interfaces` list, so the step bar (which paints the
  bottom row palette 1 / 3) isn't overwritten by the cone's
  background-conditional repaint. In this implementation the order
  is `[cone_overlay, step_hud]` and the step bar paints onto row
  63 which the cone never reaches (cone cells are inside the level
  grid, scaled into the centred 64×64 area, leaving row 63
  letter-box).
