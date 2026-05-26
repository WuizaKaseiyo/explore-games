# bx84 — beam-mirror-reflect

## Summary

The player faces a 16×16 playfield containing a static emitter that shoots a thin one-pixel-wide beam in a fixed cardinal direction; clicks place small reflective mirrors at empty cells, cycle existing mirrors between two diagonal orientations (`\` and `/`), or — at higher levels — toggle a togglable prism's split-direction. After every click the beam is re-traced from emitter to grid-edge, bouncing right-angles off mirrors, recolouring at filter cells, and splitting at prisms. The win condition is "every target ring is lit", where a target becomes lit when a click-driven beam visits any of its perimeter cells at the matching colour and once lit it stays lit. The lose condition is "step budget exhausted". Side-effects of each click: a step decrements; the beam-overlay sprite is repainted; sticky target-lit flags update; if all targets lit, the level advances.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK at `(x, y)`. Empty cell → place `mirror_bs`; `mirror_bs` → cycle to `mirror_sl`; `mirror_sl` → remove; `prism_es` ↔ `prism_en` toggle; filter/target/emitter → no-op. | Always valid. Click outside the 16×16 grid is silently a no-op (still costs a step). |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1: mirror placement and cycling. | Single emitter firing east along row 8; one yellow target at (8, 11)–(10, 13); place a `\` mirror at (8, 8) so the beam reflects south into the target. **Witness**: `[ACTION6@(34, 34)]` (pixel (34, 34) → grid (8, 8); first click on empty cell drops `mirror_bs`). |
| 2 | M2 (new): filter recolouring. M1 carried. | Emitter east along row 2; filter at (3, 2) recolours yellow → blue; one blue target at (10, 11)–(12, 13); place a `\` mirror at (10, 2) so the post-filter blue beam reflects south into target. **Witness**: `[ACTION6@(42, 10)]` (pixel (42, 10) → grid (10, 2)). |
| 3 | M3 (new): prism beam-splitting. M4 (new): prism toggling. M1, M2 carried. | Emitter east; prism (initial state ES = east+south split) at (4, 8); filter at (8, 8); three targets at (3, 3)–(5, 5) yellow-north, (12, 11)–(14, 13) blue, (3, 12)–(5, 14) yellow-south. Place a `\` mirror at (12, 8) to route post-filter east branch into target_blue (this also lights target_yellow_south via the south branch in ES state); then click the prism at (4, 8) to toggle to state EN, spawning a north branch that lights target_yellow_north. **Witness**: `[ACTION6@(50, 34), ACTION6@(18, 34)]` (pixel (50, 34) → grid (12, 8) places mirror; pixel (18, 34) → grid (4, 8) toggles prism). |

## Win condition

Every target sprite that the level placed has its lit-flag set to True. A target's lit-flag is set when the beam, during a click-driven re-trace, visits ANY of the target's 8 perimeter cells (or its hollow centre — beam tracing recognises target sprites at bounding-box level) WHILE the beam's current colour equals the target sprite's perimeter palette. Once set, the lit-flag is sticky. The check runs after every click; when all flags are True, `self.next_level()` is called.

## Lose condition

`self.steps_remaining <= 0` at the START of `step()` calls `self.lose()`. The step counter decrements by 1 per ACTION6 dispatch; budgets are 30 / 50 / 80 for L1 / L2 / L3.

## Internal state

- `self.steps_remaining: int` — depletes per click; reset per level from `level.data["step_budget"]`.
- `self.targets_lit: dict[str, bool]` — keyed by target sprite-name; reset to all-False per level from `level.data["win_targets"]`. Set to True (sticky) when a click-driven trace visits a matching target.
- `self.beam_overlay: Sprite` — a level-sized 16×16 sprite added to `self.current_level` in `on_set_level`. Its `pixels` array is repainted on every trace: cells visited by the beam in EMPTY cells (no other sprite at that grid position) get the beam's current colour; otherwise stay -1 (transparent). Layer 10 so it renders on top of mirrors/filters/prisms but only writes non-transparent cells.
- `self.step_counter_hud: StepCounterHud` — the bottom-row HUD widget; subclass of `RenderableUserDisplay`.
- Per-level state is fully reset in `on_set_level` (which is called fresh on every level transition by the engine, after a clone of the clean level template).

## Notable code patterns

- **Bounding-box hit-testing helper** (`_sprite_at`): a custom helper that iterates `current_level.get_sprites()` and returns the first sprite whose bounding box contains `(gx, gy)`, excluding the level-sized `beam_overlay`. Used both by the click handler (so clicks inside a 3×3 target's hollow centre register as "click on target", not "click on empty") and by the beam tracer (so beams crossing a target ring's centre cell still register a target visit).
- **Beam tracer with cycle detection** (`_trace_beam`): a BFS that consumes a queue of `(x, y, dx, dy, colour)` tuples and dispatches per cell-content (empty / mirror_bs / mirror_sl / filter / prism / target). Visited `(x, y, dx, dy)` tuples are tracked so a closed mirror loop terminates after one full pass instead of looping forever. A hard `max_iters` cap of `4 × gw × gh` is a belt-and-braces upper bound.
- **Reflection rules as small algebraic expressions**: `\` reflects `(dx, dy) → (dy, dx)`; `/` reflects `(dx, dy) → (-dy, -dx)`. No table lookup; the compact form covers all 4 incoming directions for each mirror type.
- **Prism as 2-state sprite-swap**: clicking a prism removes the current sprite and adds the opposite (`prism_es` ↔ `prism_en`) at the same position. Avoids per-prism mutable state; the state is encoded in which sprite is currently in the level.
- **Beam-overlay-only-paints-empty**: target rings, filters, prisms, mirrors render their own colours; the beam overlay paints only on cells where no other sprite exists (other than itself). Continuity through obstacle cells is inferred by the player from the beam appearing on either side of the obstacle.
