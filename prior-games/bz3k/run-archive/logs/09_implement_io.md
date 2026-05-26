# Step #09: implement

## Inputs Consumed
- mechanic-spec.md (rev 2, from #07)
- critique-pass.md (from #08)
- skills/code/universal-scaffold.md, novaengine-api.md
- Source idioms from cn04, sk48, sb26, m0r0, sp80 (anchored in #01)

## Deliverables Produced
- prior-games/bz3k/bz3k.py (598 lines)
- prior-games/bz3k/metadata.json
- implement-summary.md

## Notes
- Followed universal scaffold structure: imports → palette/dim
  constants → sprite pixel patterns → sprite bank dict → wall
  factory → level builders → HUD widgets → game class.
- Used semantic names throughout (no obfuscation per
  universal-scaffold style rules).
- Logical-vs-visual: gameplay sprites are 5×5 visually with
  internal pixel patterns; logical position is sprite center
  (top-left + 2). Wall collision uses engine's pixel-perfect
  via Sprite.collides_with; cap/flipper/target trigger via
  center-cell alignment; hazard via bounding-box pixel check.
- Implemented per-axis slide: horizontal phase then vertical
  phase, with collision/cap/flipper/hazard checks per cell-step.
- Wake_pixel lifecycle: cleared at top of step(), rebuilt after
  slide using INTANGIBLE clones placed in the level.
- Smoke validation:
  - syntax parses ✓
  - Bz3k() instantiates with 3 levels ✓
  - L1 witness (10 actions) reaches target, level advances ✓
  - L2 witness (13 actions) hits cap, ram-east-wall to target ✓
  - L3 witness (10 actions) uses flipper, threads cap, target,
    GameState.WIN ✓
- One bugfix during smoke: `_check_trigger_at_center`'s hazard
  bounding-box check used truthy `if s.pixels else 0` which fails
  on numpy arrays; replaced with `np.asarray(s.pixels)` shape.
- Transition condition met. Proceeding to smoke_test.
