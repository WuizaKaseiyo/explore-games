# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (round 2)
- workspace/critique-pass.md
- skills/code/{universal-scaffold, novaengine-api, id-generation, smoke-test-checks}
- skills/global/{action-enum, color-legend, paths}
- Prior reference source files studied in #01 (cn04, wa30, sp80, sk48 — for sprite/level/HUD pattern conventions)

## Deliverables Produced
- prior-games/nh4w/nh4w.py (441 lines)
- prior-games/nh4w/metadata.json
- workspace/implement-summary.md

## Notes
- Used helper functions (`_make_floor`, `_make_brick_wall`, `_make_stalactite`, `_make_target`) instead of inlining big pixel arrays — keeps the sprite bank readable.
- Stalactite shape: 9-row tapered tip ending in a maroon (palette 13) drip, with grey trunk filling the upper rows. Shared by `ceiling_c6` and `ceiling_c14` via height parameter.
- Brick wall shape: alternating brick-offset rows with mortar lines every 4th row.
- During implementation, verified that bbox collision on stalactite of height (50 - clearance) gives the clean "alt < clearance" rule. Spec used clearance values 5 and 13; implementation shifted to 6 and 14 to align with bbox semantics — witness still works out to the same 4-action sequence with yellow only from x=8 and blue only from x=12.
- Engine quirk discovered: `g.levels` is private (`g._levels`); list-of-Levels exposed only via `_levels` attribute.
- Animation pattern: in `step()`, when `self.flight_phase >= 0`, advance one frame and return WITHOUT calling `complete_action()`. Only on the final frame (collision OR end-of-path) call `complete_action()` and check win/lose. Matches sk48/sp80 pattern.
- `_get_valid_actions` returns the standard list during animation; engine ticks step() at FPS until complete_action() resolves.
