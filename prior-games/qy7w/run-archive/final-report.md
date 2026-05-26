# Game generation final report

## Generated game
- **ID**: `qy7w`
- **Source**: `prior-games/qy7w/qy7w.py`
- **Metadata**: `prior-games/qy7w/metadata.json`
- **Lines of code**: 730

## Mechanic
The playfield shows three vertical coloured strands hanging from
filled coloured caps at the top down to hollow coloured slots at the
bottom. Between the strands sit toggleable crossings: clicking one
flips its visual from a "+" pass-through marker to an X-shaped swap
marker. A swap re-routes the strands at and below that crossing
(adjacent-column swap for the binary type, outer-column swap for the
wider long type). The level wins when each bottom slot's frame
colour is met by the strand that ends in its column. Level 1 uses
three binary crossings; Level 2 adds the long crossing plus a
spatial blocker that ends the run if a yellow-coloured strand routes
through it; Level 3 adds a green dye station that re-paints whichever
strand passes through it, and the slot palette includes a new green
target. Each level's witness is a 2-click toggle sequence.

## Action mapping
| Action | Effect |
|---|---|
| ACTION6 | CLICK at `(x, y)` — if the click lands on a TANGIBLE crossing sprite, that crossing toggles between PASS and TWIST. Click coordinates are interpreted via `camera.display_to_grid(x, y)`. Misses are no-ops (still consume one step). |

## Levels
- **L1** — base mechanic (BINARY crossing toggle). Witness: 2 clicks.
- **L2** — adds LONG crossing toggle (outer-column swap in one click) plus a spatial blocker constraint that ends the run if a matching-colour strand routes through it. Witness: 2 clicks (one binary + one long).
- **L3** — adds a passive COLOUR-SHIFT dye station that re-paints whichever strand passes through it; slot 0 demands the new shifted colour. Blocker constraint still active. Witness: 2 clicks (one binary + one long, leveraging the dye station automatically).

## Novelty note
- **Closest taxonomy entry**: `vc33 — row-column-swap-stripe`. vc33 click-marker swaps stones across a marker on a single row/column. qy7w never moves any sprite — toggling a crossing flips a state-bit that re-routes every strand from that y down through the rest of the level. Different visual signature (vertical strands vs horizontal stone-stripes) and different "what permutes" (a single elementary transposition generator vs a single stone-stripe rearrangement).
- **Closest prior-game entry**: `jx5k — constellation-edge-link`. jx5k builds a graph from scratch by pair-clicking nodes. qy7w toggles crossings on a fixed pre-built strand structure — no graph construction, just permutation generators. Different "what is on the board" (4 floating nodes vs vertical parallel strand bundle).

## Index update
One row appended to `prior-games/index.md`:

```
| qy7w | strand-twist-permute | Strand-Twist Permutation — toggle binary/long crossings to permute three vertical strands; L3 dye-station shifts a strand's colour mid-route. | 2026-05-10T07:07:47Z | (autonomous) |
```
