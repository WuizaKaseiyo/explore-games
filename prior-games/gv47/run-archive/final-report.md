# Game generation final report

## Generated game
- **ID**: gv47
- **Source**: `prior-games/gv47/gv47.py`
- **Metadata**: `prior-games/gv47/metadata.json`
- **Lines of code**: 564

## Mechanic

The player faces a small wall-bound grid seeded with several
distinctly-coloured "seed" sprites and a sparse set of "target"
cells, each target marked with a tiny coloured pip telling the
player which colour the cell needs to end up. Clicking a seed
expands its persistent connected region by one cardinal-adjacent
ring of currently-uncoloured non-wall cells; pressing ACTION5 fires
a global "mix" event that fuses any pair of contacting different-
coloured regions into a single new region, recolouring both into a
derived colour from a per-level mixing table. Level 1 introduces
click-to-grow alone with one yellow seed and a wall-pinch puzzle.
Level 2 adds the mix verb with a green target reachable only by
fusing yellow and blue. Level 3 keeps both verbs and introduces a
stationary wind-strip sprite that biases each grow ring to extend
one extra cell eastward; three seeds, two mix-targets, and one
single-colour target compose all three mechanics.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Global "mix" — every pair of currently-contacting different-coloured regions whose colour pair is in the level's mixing table is fused into a single new region with the table's output colour. No-op (still consumes a step) when no contact exists. |
| ACTION6 | Click — `data["x"]`/`data["y"]` are pixel coords mapped via `camera.display_to_grid`. If the resulting grid cell falls inside a seed sprite's bounding box, that seed's region grows by one ring (east-biased on L3). Otherwise no-op (still consumes a step). |

## Levels

- **L1 (12×12, budget 30)**: yellow seed + yellow target, vertical wall column with a single gap. Witness exercises `click-to-grow` only.
- **L2 (12×12, budget 50)**: + blue seed and a green mix-target. Witness alternates yellow/blue grows until contact, fires ACTION5 to produce green, then continues growing to claim the yellow target.
- **L3 (12×12, budget 80)**: + red seed, wind-strip on east edge, additional purple and red targets. Witness exercises grow + mix + wind-biased growth.

## Novelty note

- **Closest taxonomy entry — ft09 (stamp-3x3-paint).** Distinguishing rule: ft09 stamps a fixed 3×3 pattern centred on the click coordinate; gv47 grows a connected region from a fixed seed sprite, painting one cardinal ring per click of that seed. Click coordinates select *which seed* (i.e. which existing region to extend), not which cell to paint. ft09 has no equivalent of ACTION5 mix.
- **Closest prior-game entry — lq5x (lantern-cone-illuminate).** Distinguishing rule: lq5x projects a transient directional cone from a moving avatar (illumination is volatile; ACTION5 rotates the cone direction). gv47 has no avatar at all — coverage is persistent ring growth from stationary seeds, and ACTION5 *combines two contacting regions into a derived colour* rather than steering a beam.

## Index update

The following row was appended to
`prior-games/index.md`:

```
| gv47 | seed-grow-mix | Seed Bloom & Mix — click coloured seeds to grow concentric rings; ACTION5 mixes contacting regions; L3 wind biases growth east. | 2026-04-29T15:23:22Z | (autonomous) |
```
