# Game generation final report

## Generated game
- **ID**: wm6q
- **Source**: `prior-games/wm6q/wm6q.py`
- **Metadata**: `prior-games/wm6q/metadata.json`
- **Lines of code**: 392

## Mechanic
The playfield is a fixed grid of square tiles, each rendered with four
coloured edge bands (top, right, bottom, left) drawn from a 4-colour palette.
The single player verb is ACTION6 click on a tile, which cycles that tile's
edge-colour assignment 90° clockwise — the new top-band shows what was
previously the left-band, and so on. Tiles never move; only the cyclic
colour permutation changes. The level is won when every shared edge between
two adjacent tiles carries the same colour on both sides — a continuous band
of one colour visibly bridges the boundary, providing direct visual feedback.
L1 is two tiles in a row (one click on a tile aligns the boundary). L2
introduces a **locked tile** (visible 6×6 black-square inner glyph) whose
edge colours are fixed; the player rotates the surrounding 3 tiles to match
the lock's edges. L3 introduces a **linked pair** of two diagonal tiles
(visible 6×6 purple-ring glyph, identical between the pair members) that
rotate in lockstep — clicking either advances both — forcing the player to
coordinate joint orientations on top of the lock-anchored cascade.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | CLICK at `(x, y)`. Routes via `camera.display_to_grid` to find the tile at the clicked grid cell. Locked tiles are no-ops. Linked-pair clicks rotate BOTH pair members in lockstep. Otherwise rotates the clicked tile by 1 (mod 4). |

## Levels
- **L1** — base mechanic: rotate-via-click. Two regular tiles; align the
  shared edge.
- **L2** — adds locked-tile mechanic. 2×2 grid with one locked tile in the
  corner anchoring the boundary; rotate the other three tiles to match.
- **L3** — adds linked-pair mechanic. 3×3 grid with locked centre and a
  diagonal pair coupled into one rotation DOF; cascade through the lock,
  the corners, and the joint pair-rotation to find the unique solution.

## Novelty note
- **Closest taxonomy entry: cn04 — nub-pair-glyph.** Distinguishing rule:
  cn04 moves piece BODIES across a free playfield using arrows + ACTION5
  rotation, matching pixel-level "8" connectors at coincident coordinates
  of two distinct pieces; wm6q has fixed-position uniform square tiles
  (no movement, no select state, no arrows), the only verb is "click
  rotates this tile's 4-edge colour permutation 90° CW", and matching is
  edge-colour equality at already-adjacent boundaries.
- **Closest prior-game entry: qf8m — rook-cross-toggle.** Distinguishing
  rule: qf8m's click flips a non-local cross of cell colours (affecting
  a row + column of cells); wm6q's click affects exactly ONE tile (purely
  local), and what changes is the 4-edge colour PERMUTATION inside that
  tile rather than per-cell colour values.
- Negative-similarity walk (against cn04 and qf8m) gives ≤ 2 dimensions
  of overlap each, well below the 3-dimension rejection threshold.
  **NOVEL** on both axes.

## Index update
One row appended to `prior-games/index.md`:

```
| wm6q | edge-color-rotate-match | Edge-Color Tile Rotator — click rotates a tile's 4-edge colour permutation; locked tile (L2) and linked-pair (L3) constrain the unique solution. | 2026-05-10T13:58:20Z | (autonomous) |
```
