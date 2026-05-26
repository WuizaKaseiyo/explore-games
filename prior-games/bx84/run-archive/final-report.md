# Game generation final report

## Generated game

- **ID**: `bx84`
- **Source**: `prior-games/bx84/bx84.py`
- **Metadata**: `prior-games/bx84/metadata.json`
- **Lines of code**: 384

## Mechanic

A small static emitter at the edge of a 16×16 playfield continuously shoots a thin one-pixel-wide coloured beam in a fixed cardinal direction; the player clicks empty grid cells to drop reflective mirrors and clicks existing mirrors to cycle their orientation between two diagonal patterns (`\` then `/` then empty). After every click, the beam is re-traced from the emitter to the grid edge — bouncing off mirrors at right angles, recolouring at filter cells, and splitting at prism cells (perpendicular branch direction depends on the prism's current state, which is itself toggleable by clicking it). A target ring becomes "lit" the first time a click-driven beam visits any of its perimeter cells at the matching colour, and lit-state is sticky. The level wins when every target is lit. Level progression composes mechanics: L1 introduces mirror placement-and-cycling alone; L2 adds the filter (so targets demand specific colours that only the post-filter beam can deliver); L3 adds the prism plus the player-toggleable prism-state (so reaching all three targets requires the player to BOTH place mirrors that route the post-filter east branch AND visit both prism-states across the click sequence — order matters because the south-branch target must be lit while the prism is still in its initial ES state).

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | CLICK at `(x, y)`. Pixel coords convert to grid via `camera.display_to_grid`. Empty cell → place `mirror_bs` (`\`, palette-7 pink). `mirror_bs` cell → cycle to `mirror_sl` (`/`, palette-6 magenta). `mirror_sl` cell → remove. `prism_es` cell → toggle to `prism_en` (and vice versa). Filter / target / emitter cell → no-op. Each click decrements the step counter; the beam re-traces immediately and targets that match colour become lit. |

## Levels

- **L1** (16×16, budget 30): emitter + 1 yellow target. Player learns the mirror-place-and-cycle verb. Witness = 1 click.
- **L2** (16×16, budget 50): emitter + filter + 1 blue target. Adds filter recolouring (M2). Witness = 1 click; filter recolours pre-mirror beam to blue, mirror reflects beam south to target.
- **L3** (16×16, budget 80): emitter + prism (ES initial) + filter + 3 targets (yellow north, blue middle, yellow south). Adds prism beam-splitting (M3) AND prism toggling (M4). Witness = 2 clicks: place mirror to route post-filter east branch through to target_blue (which also lights target_yellow_south via the south branch in ES state); then toggle prism to EN to spawn a north branch lighting target_yellow_north. Swapping the two clicks breaks the witness — toggling first removes the south branch before target_yellow_south can be lit, requiring an extra recovery click.

## Novelty note

- **Closest taxonomy entry**: `lq5x` (lantern-cone-illuminate) is the only reference in the "light" thematic space, but lq5x has a MOVING lantern projecting a 3-wide directional cone; bx84 has a STATIONARY emitter and STATIONARY MIRRORS that route a 1-pixel-wide beam at right angles. lq5x has no reflection mechanic at all. The two games' central reasoning tasks differ: lq5x plans walking paths with a moving light source; bx84 plans a static reflector layout.
- **Closest prior-game entry**: same — `lq5x`, distinguished by the same rule. None of the other 13 prior generated games involve light, beams, mirrors, prisms, or filter-recolouring; bx84 is genuinely novel against the cumulative corpus.

## Index update

One row appended to `prior-games/index.md`:

```
| bx84 | beam-mirror-reflect | Beam-Mirror-Reflect — emitter shoots a coloured beam; click empty cells to drop mirrors that reflect at right angles, click mirrors to cycle orientation; L2 adds a filter that recolours the beam, L3 adds a togglable prism that splits beam east+south or east+north. | 2026-05-05T15:03:57Z | (autonomous) |
```
