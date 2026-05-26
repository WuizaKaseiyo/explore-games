# Game generation final report

## Generated game
- **ID**: pz4t
- **Source**: `prior-games/pz4t/pz4t.py`
- **Metadata**: `prior-games/pz4t/metadata.json`
- **Lines of code**: 332

## Mechanic

A jigsaw assembly puzzle. The screen splits into a *board* region
above and a *palette* region below where unplaced coloured
components sit. The player has one primary verb: ACTION6 click,
which is two-phase. While nothing is held, clicking on a non-
transparent pixel of a component picks it up AND records the
clicked-pixel as the *anchor* (its offset relative to the
component's bounding-box top-left). While a component is held,
clicking any cell on the board places the component such that the
anchor cell aligns with the clicked cell — i.e. position = click −
anchor. ACTION5 rotates the held component 90° clockwise (the
anchor rotates with the pixels); ACTION7 flips it horizontally
(the anchor mirrors with the pixels). The level wins when every
component is placed such that its filled cells exactly match the
matching-colour target shadows on the board. As levels rise the
board grows (10×10 → 12×12 → 14×14) and component count rises
(2 → 3 → 4), with L2 introducing rotation and L3 introducing flip
as strictly-required new mechanics.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Rotate held component 90° CW; anchor rotates with the pixels (no-op if nothing held). |
| ACTION6 | Click. Phase 1 (no held): pick up the component at the clicked cell and record anchor offset. Phase 2 (held): place at `(click_x - anchor_col, click_y - anchor_row)` and drop. |
| ACTION7 | Flip held component horizontally; anchor mirrors with the pixels (no-op if nothing held). |

## Levels

- **L1 (10×10, budget 16)** — base mechanic: anchor-pivot place.
  Two components (red 3-bar, yellow 2-vbar) directly orientable.
  Witness 4 actions.
- **L2 (12×12, budget 28)** — adds **rotation**. Three components
  (red 1×3 vertical, yellow L, green 2×1). Red component must
  rotate 90° CW to fit its horizontal target shadow — strictly
  required. Witness 7 actions.
- **L3 (14×14, budget 40)** — adds **flip**. Four components
  (red Z-tetromino, yellow S-tetromino, green T, magenta 2-bar).
  Red Z component must be flipped horizontally to fit the S-shape
  red target — strictly required (no rotation of Z produces S
  because Z has 180° symmetry). Green T must rotate 90° CW.
  Witness 10 actions; commute test on red triplet (pick, flip,
  place) — flipping with nothing held is a no-op so order matters.

## Novelty note

- **Closest taxonomy entry**: `sb26 tile-place-commit` (click a
  tile then click a slot to place it). **Distinguishing rule**:
  sb26 places a tile at a discrete fixed slot index (the slot
  decides where every cell of the tile lands); pz4t places a
  multi-cell sprite at a free 2D translation determined by
  `click − anchor`. sb26 has no rotation, no flip, no anchor
  pixel.
- **Closest prior-game entry**: `ng52 multiset-signature-classify`
  (click objects then click bin then ACTION5 commit).
  **Distinguishing rule**: ng52 partitions a pool into bins by
  multiset signature with no spatial assembly; pz4t is geometric
  shape-fit with anchor-aligned free placement plus rotation and
  flip transformations.

## Index update

One row appended:

```
| pz4t | anchor-pivot-place | Anchor-Pivot Jigsaw — click pixel on a component sets the anchor; click on board places component at click − anchor; ACTION5 rotates and ACTION7 flips. | 2026-04-30T23:36:02Z | seed: jigsaw click-pivot place |
```
