# Implement Summary — `lv4k`

## Files written
- `prior-games/lv4k/lv4k.py` (491 lines)
- `prior-games/lv4k/metadata.json`

## Plain-English summary

A horizontal beam pivots on a fixed support post. The player picks coloured weights from a tray below the beam and places them onto evenly-spaced slots along the beam by clicking. Heavier weights swing the beam more strongly than lighter ones. The level ends when the tray is empty and the beam is exactly level. Later levels add a passenger figure that sits on the beam and shifts when the beam tilts too far — pushing it past the beam's end loses the level.

## Smoke test results

- Module parses (`python -c "import ast; ast.parse(...)"`) ✓
- Game class instantiates (`Lv4k()`) ✓
- All 3 levels' witness solutions complete:
  - L1 witness (4 actions): wins; transitions to L2.
  - L2 witness (6 actions): wins; transitions to L3.
  - L3 witness (8 actions): wins; passenger ends safely on beam, state = `WIN`.
- L3 lose-condition verified: a bad heuristic (`m2@-3, m2@-1` consecutively) loses at action 4 with passenger displaced to slot 0 (fulcrum) → `state = GAME_OVER`.

## Implementation notes (one-line each)

- One critical bug found and fixed during smoke test: per-instance state attributes (`self.placement`, `self.tray_weights`, etc.) were initialised AFTER `super().__init__()`, but the parent's `__init__` calls `set_level(0)` which calls `on_set_level` which populates them — so the post-super assignments were wiping out valid state. Moved initialisation before `super().__init__()`.
- Beam slot click hit-testing uses **strict in x, tolerant ±3 in y** (`_beam_lane_contains`). Strict-x prevents adjacent-slot ambiguity (a click at `(48, 26)` should hit slot at arm +2, not arm +1); ±3 in y accounts for the visual tilt offset (the slot's y can shift up to 3 cells from the neutral y=24 when the beam tilts).
- Tray-slot hit-testing uses extended bbox with padding=1 (so a click on the frame surrounding the weight selects it, matching the spec's witness coordinates).
- Tilt rendering: each beam segment's y-position is recomputed every step from `_y_offset_for_arm(arm, tilt_level)` using truncation-toward-zero division so left-right symmetry holds. Placed weights and the passenger sit one weight-height above their slot's beam segment.
- Selection cue: the selected tray weight is repainted by `color_remap` (orange → yellow `11` for mass-1; blue → yellow `11` for mass-2). Reverted on deselect/place.
- Win predicate: `len(unplaced_weights) == 0 and torque == 0`. Lose: step exhaustion OR passenger arm not in `exposed_arms`.
- Class name `Lv4k` matches Pascal-case of game ID, per the universal-scaffold style rule.
