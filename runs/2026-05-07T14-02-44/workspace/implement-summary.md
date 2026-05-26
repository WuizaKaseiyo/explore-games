# Implement summary — yf3h

## Output paths
- Source: `prior-games/yf3h/yf3h.py` (629 lines).
- Metadata: `prior-games/yf3h/metadata.json`.

## Verification
- `python -c "import ast; ast.parse(...)"` → SYNTAX OK.
- `uv run python -c "from yf3h import Yf3h; g = Yf3h()"` → `instantiated OK; level count: 3; available actions: [5, 6]`.

## Implemented mechanic — plain-English summary

The game has stationary "emitter" sprites (red/blue/green, 5×5 filled squares with a small centre indicator) and "resonator" sprites (5×5 hollow frames). The player clicks an emitter to arm it (centre indicator turns yellow); pressing ACTION5 fires every armed emitter at once, each projecting one transient pulse-ring that expands outward 1 cell per animation tick. When a ring's colour is in a resonator's required-multiset and the ring sweeps over the resonator, the resonator records a same-tick "flash" of that colour; if the full required-multiset is concurrently flashing on a single tick, the resonator activates permanently (its centre fills white). From level 3, "phase-delay tile" sprites can be toggled active by ACTION6 click; an active tile delays any ring passing over it by exactly 1 tick (allowing the player to align unequal Manhattan distances when multiple required colours need to converge same-tick on a multi-colour resonator). The level wins when all resonators are activated; loses when the per-level step budget is exhausted.

Animation: the engine's multi-frame-per-action pattern is used — `step()` defers `complete_action()` while a fire-burst animation is in progress, advancing one ring-tick per call until all rings have left the grid (at which point the animation completes and `complete_action()` is called).
