# gv47 — seed-grow-surround-dissolve

## Summary

Seed Bloom is a turn-based colour-territory puzzle on a 12×12 grid.
The player has no avatar; they play by clicking stationary "seed"
sprites of distinct colours to expand each seed's persistent
connected region by one 4-cardinal ring of currently-uncoloured,
non-wall, non-target cells per click. Each level also seats one or
more "target pips" — single coloured cells, each surrounded by a
1-pixel-thick black ring drawn by a HUD overlay tightly hugging the
pip. When all 8 cells around a pip (Chebyshev distance 1) hold
paint of the pip's own colour, the ring auto-dissolves: the target
sprite is removed and the pip cell is absorbed into the surrounding
region (no hollow, and the absorbed cell will be re-coloured by any
subsequent mix that touches the region). Off-grid surround cells
auto-satisfy. ACTION5 fires a global mix: every pair of contacting
different-coloured regions whose colour-pair is in the level's
mix-table fuses into a new region of the mix-output colour; the
parent seed sprites' pixels remap to the new colour and either seed
continues to extend the merged region. The level wins when every
target sprite has dissolved; lose when the step counter runs out.

Note: pips of single-colour targets must be dissolved BEFORE that
colour participates in any mix — once the surround region's colour
changes (e.g. yellow → green via mix), the surround cells no longer
match the pip's colour and the original target is locked out.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Mix — fuse all currently-contacting different-coloured region pairs whose colour-pair is in the level's `mix_table`. Auto-dissolve runs at end of step regardless of action. No-op (still consumes one step) if no qualifying contact exists. | Always valid; effect depends on the contact graph at the moment of firing. |
| ACTION6 | Click — pixel coords are converted via `camera.display_to_grid`; if the grid cell lies inside a seed sprite's bounding box, that seed's region grows by one cardinal ring. Otherwise no-op; still consumes one step. Auto-dissolve runs at end of step. | Always valid; effect depends on whether the click cell hits a seed. |

`available_actions = [5, 6]`. Auto-dissolve is implicit on every
step — players never need to "press a key to dissolve"; surround the
pip and the ring vanishes on the next render.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | click-to-grow + auto-dissolve | yellow seed at (1, 1); yellow pip target at (8, 4); a small wall fragment forces yellow to detour. Witness ≈ 8 yellow grows; budget 30. |
| 2 | + mix-at-contact (ACTION5) | yellow seed (1, 1), blue seed (8, 8); yellow pip at (10, 1) at the top-right corner (E and N surround cells off-grid auto), green pip at (5, 5) — no green seed, only the yellow+blue mix produces green paint. Player must dissolve the yellow target before pressing ACTION5 (otherwise yellow region recolours to green and yellow target becomes unwinnable). Witness ≈ 9 yellow + 1 ACTION5; budget 60. |
| 3 | + ordering across two seed-pairs | yellow (1, 1), red (1, 8), blue (8, 8); yellow pip at (5, 1) and purple pip at (5, 8). Yellow target dissolved by yellow alone; purple target dissolved by red+blue mix. Yellow grows do not contact blue (Chebyshev > 1 between yellow ring 4 and blue seed), so the player can dissolve yellow without disturbing the red+blue setup. Witness ≈ 4 yellow + 4 red/blue alternating + 1 ACTION5; budget 100. |

## Win condition

`self.next_level()` fires when every sprite tagged `target` has been
removed from the level. Per-target check (run in `_dissolve_targets`
at the end of every `step()`):

```
for each target sprite t:
    pip = colour at t.pixels[0, 0]
    for each cell c in the 8 cells at Chebyshev distance 1 from (t.x, t.y):
        if c is off-grid: count as satisfied
        else if cell_colour(c) != pip: target NOT dissolved
    if all 8 satisfied: remove target sprite; absorb the pip cell into a
    surround region whose colour matches the pip
```

## Lose condition

The per-level step counter starts at `level.get_data("step_budget")`
and decrements once per action regardless of effect. When it
reaches 0 before all targets dissolve, `self.lose()` is called.

## Internal state

- `self.regions: dict[str, set[(int, int)]]` — region id → set of
  painted grid cells.
- `self.region_color: dict[str, int]` — region id → palette colour.
- `self.region_seeds: dict[str, list[Sprite]]` — region id → list
  of seed sprites whose region this is (post-mix, the merged region
  inherits both parents' seeds).
- `self.paint_sprites: dict[(int, int), Sprite]` — runtime 1×1
  paint sprite per painted cell; used to update colour in-place
  on mix, and to add a new paint sprite at a dissolved pip's cell.
- `self.steps_remaining: int` — depleting counter.
- `self.mix_table: dict[frozenset[int], int]` — pair-of-colours →
  mix-output colour; populated from `level.get_data("mix_table")`.
- Targets are 1×1 collidable sprites at the pip's grid cell. The
  visible "ring" is drawn purely by the `TargetRingHud` widget.

## Notable code patterns

- **Frame-overlaid ring rendering.** `TargetRingHud` walks every
  `target`-tagged sprite, computes the pip cell's pixel area
  (`tx*scale + ox`...), and writes `WALL_COLOR` into the 1-pixel
  border immediately outside that area. Removing the target
  sprite immediately removes the ring on the next render.
- **Targets block growth.** Pip cells are `collidable=True` so
  region growth flows around the pip rather than through it; this
  is what gives the player a meaningful "surround" task.
- **Auto-dissolve at end of every step.** The dissolve check runs
  unconditionally after each action so surrounding the pip causes
  the ring to disappear on the very next rendered frame.
- **Pip absorption on dissolve.** When dissolving, the code finds
  any 4- or 8-neighbour region of matching colour and adds the
  pip cell to that region (and a paint sprite at the cell). The
  dissolved pip is therefore continuous with surrounding paint
  and recolours along with the region under any later mix.
- **Global region-fusion mix.** `_mix_regions` runs a contact-graph
  loop: while any pair of different-coloured regions in contact
  has its colour-pair in `mix_table`, the two regions fuse into a
  new region of the output colour. All cells of both parents are
  recoloured (paint sprites updated in place); seed sprite
  pixels are remapped via numpy mask `(pixels >= 0) & (pixels !=
  WHITE)` so visual seed colour matches the merged region.
- **Click → seed bbox dispatch.** `step()` converts the click
  pixel through `camera.display_to_grid`, then linearly scans
  `region_seeds` for a sprite whose bounding box contains the
  cell — yielding the region id to grow.
