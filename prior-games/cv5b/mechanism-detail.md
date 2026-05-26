# cv5b — arc-launch-target

## Summary
A movable launcher walks the playfield carrying a 3-state charge
level cycled through the freedom slot; clicking a landing cell fires
a marble along a parabolic arc from launcher to click, with the
selected charge choosing arc apex AND reachable horizontal range.
The marble lands at the clicked cell and consumes a target ring if
it matches; targets are coloured pink hollow rings sat on the
ground row. Vertical "shield" bars block both walking and arcs that
pass through them, forcing either a walk-around or a steeper arc.
A stippled vertical wind column deflects any arc that passes
through it, shifting the landing cell by +1 — the player must
compensate at aim-time.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move active launcher up 1 cell | not into shield, not out of bounds |
| ACTION2 | Move active launcher down 1 cell | as above |
| ACTION3 | Move active launcher left 1 cell | as above |
| ACTION4 | Move active launcher right 1 cell | as above |
| ACTION5 | Cycle charge level 1→2→3→1 | always |
| ACTION6 | Fire parabolic arc to clicked grid cell | always; out-of-range clicks no-op |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | arc-fire | Tutorial — single ground target reachable at default charge from start. Witness `[ACTION6@(16, 50)]`. |
| 2 | + walk-launcher, + charge-cycle | Two ground targets; far target requires walking closer AND cycling to max charge. Witness `[ACTION5, ACTION6@(28, 50), ACTION4×10, ACTION5, ACTION6@(50, 50)]` (14 actions). |
| 3 | + shield-blocks-arc, + wind-deflects-arc | Single far target; shield blocks ground corridor (forces up-and-over walk path); wind column between launcher and target shifts landing +1, requiring aim-correction. Witness `[ACTION4×9, ACTION1×9, ACTION4×7, ACTION2×9, ACTION5, ACTION5, ACTION6@(49, 50)]` (36 actions). |

## Win condition
A target ring is consumed when an arc's landing cell exactly equals
its centre (target.x + 1, target.y + 1). When every target in the
level is consumed, `self.next_level()` fires on the next step. After
L3, the engine auto-fires `self.win()` past the last level index.

## Lose condition
Each action decrements a per-level step counter; when it reaches 0,
`self.lose()` fires on the next step. No instant-fail collisions —
mis-aimed or shield-absorbed arcs simply waste the action.

## Internal state
- `power: int` — current charge level 1, 2, or 3.
- `targets_remaining: list[Sprite]` — populated in `on_set_level`
  from `level.get_sprites_by_tag("target")`.
- `target_centres: list[tuple[int,int]]` — read from `level.data`.
- `shields: list[Sprite]` — from `get_sprites_by_tag("shield")`.
- `wind_markers: list[Sprite]` — from `get_sprites_by_tag("wind")`.
- `arc_dot_sprites: list[Sprite]` — runtime arc-trail sprites,
  cleared at the top of every `step()` and respawned by `_fire`.
- Step counter HUD as a `RenderableUserDisplay` drawing a depleting
  bar at row 0.

## Notable code patterns
- **Three-launcher swap idiom for charge state.** Three launcher
  variants (1/3, 2/3, 3/3 segments filled in purple — the same hue
  as the arc-preview dots) are placed at the same cell at level
  start; only the active variant is `InteractionMode.TANGIBLE`, the
  other two are `REMOVED`. ACTION5 cycles which is active, swapping
  modes. The shared purple-vs-grey-segment visual links charge state
  directly to the arc the player will see when firing, satisfying
  the "no hidden state" rule with a meaningful colour-coded cue.

- **Fall-short trajectory on out-of-range clicks.** When the player
  clicks a cell beyond the current charge's range, `_fire` does NOT
  silently no-op. Instead it computes the arc to the max-reach cell
  in the click's direction (with the same apex) and renders those
  arc dots — the player sees the marble's trajectory reaching its
  limit and stopping short of the target, instead of a confusing
  blank no-op. No target is registered for fall-short shots.
- **Parametric arc cell trace with dedup.** `_compute_arc` walks a
  fine-grained `s ∈ [0, 1]` parameter and rounds to integer cells,
  deduping consecutive identical cells. Reusable for any cell-by-cell
  trajectory along a continuous curve.
- **Bounding-box overlap for shield collision.** Both walk-blocking
  and arc-blocking use the same axis-aligned bounding-box overlap
  test against the shield sprite's `(x, y, width, height)`. Same
  rectangle test for two different mechanics keeps the behaviour
  coherent.
- **Wind drift applied to last cell only.** If any arc cell is
  inside a wind sprite's bounding box, the arc's terminal cell is
  shifted by +1 along x. Per-arc binary effect, not per-cell — keeps
  the visual prediction simple.
- **Run-time arc dots as level sprites.** Arc trail rendering is
  done by spawning `arc_dot` (1×1, intangible) sprites along the
  arc cells and adding them to the level. They are cleared at the
  top of every `step()` so each action starts with a clean slate.
