# Implement Summary — bx84

## Files

- `prior-games/bx84/bx84.py` — 384 lines.
- `prior-games/bx84/metadata.json` — schema-compliant.

## Implementation summary (plain English, no level-specific cell coordinates)

A static emitter shoots a one-pixel-wide coloured beam in a fixed cardinal direction; the player clicks empty grid cells to drop reflective mirrors and clicks existing mirrors to cycle the orientation between two diagonal patterns. After every click, a tracer re-walks the beam from emitter to grid edge, bouncing off mirrors, recolouring at filters, and splitting at prisms (perpendicular branches in either south or north depending on the prism's current state, which the player can also toggle by clicking it). A target ring becomes "lit" the first time the beam visits any of its perimeter cells at the matching colour, and the level wins when every target is lit. A bottom-row HUD shows step budget remaining; running out of steps is a loss.

## Smoke-test verification

Successfully:
- Instantiated `Bx84()` (3 levels).
- Solved L1 in 1 click (witness: pixel `(34, 34)` → grid `(8, 8)`).
- Solved L2 in 1 click (witness: pixel `(42, 10)` → grid `(10, 2)`).
- Solved L3 in 2 clicks (witnesses: pixel `(50, 34)` then `(18, 34)`).
- Verified L3 adjacent-swap breakage: swapping the 2-click witness (toggle prism first, then place mirror) leaves `target_yellow_south` unlit after 2 clicks; recovery requires a 3rd click (toggle back to ES) to light it. The order-dependence claim from the spec holds at runtime.

Game state at end of L3 witness: `GameState.WIN`.

`metadata.json` written with schema:
```json
{
  "game_id": "bx84",
  "title": "Beam-Mirror-Reflect Puzzle",
  "default_fps": 30,
  "tags": ["claude-generated"],
  "baseline_actions": [6],
  "local_dir": "prior-games/bx84",
  "date_generated": "2026-05-05T14:33:34Z"
}
```
