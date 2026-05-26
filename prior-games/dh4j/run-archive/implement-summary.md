# implement-summary.md

## Files written
- `prior-games/dh4j/dh4j.py` — 673 lines.
- `prior-games/dh4j/metadata.json` — standard schema.

## Plain-English summary of the implemented rule

The player controls a single avatar on a small grid where every walkable cell visibly carries one to three pip dots. Pressing a cardinal arrow translates the avatar by that pip count in the chosen direction; the avatar leaps over any cells (including walls) in between, and only the destination needs to be a non-wall in-bounds cell — otherwise the press is a no-op. A filter cell flips the global pip→stride legend, recoloring every floor tile and swapping which pip counts correspond to which strides. A pivot cell, when landed on, grants a one-shot stride bonus for the next press, then becomes a regular floor tile. Reach the goal cell to advance levels; run out of presses to lose.

## Implementation notes
- Multi-cell strides animate cell-by-cell via `_slide_remaining` / `_slide_dx` / `_slide_dy` state advanced one cell per engine frame inside `step()` until the slide completes — keeps long-distance leaps legible (per `reference-game-patterns.md`'s "long-distance transitions" guidance).
- Pivot consumption swaps the composite pivot sprite's pixels to the matching plain `floor_pip_2_*` variant and removes the "pivot" tag in place — preserves the position but removes the bonus affordance.
- Filter swap is implemented by recoloring every floor sprite's pip accent in-place (yellow `11` ↔ light-blue `10`) using a single numpy mask.
- The HUD's `LegendChipHud` renders both chips every frame; the active chip gets a 1-pixel black outline so the player can read off which legend is in effect.
- Smoke-test executed during implement: all three witnesses replay successfully and the game reaches `WIN` after L3.
