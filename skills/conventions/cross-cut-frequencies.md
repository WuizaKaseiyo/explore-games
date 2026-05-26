# Cross-cut frequencies across the 25 reference games

Pre-computed counts of which features appear in how many of the 25
reference games' `## Frequency-table contributions` sections. This
file is the *cached answer* — past runs all re-derived these
numbers in `study-notes.md`, so the harness now serves them
directly instead of re-counting every run. Trust this table; do
not recount.

| Feature | Frequency | Notes |
|---|---|---|
| Step-counter HUD that drains 1+ per action and fires `lose()` at zero | **25 / 25** | Universal. Implementation is a `RenderableUserDisplay` rendering a depleting bar at row 0 or row 63 (occasionally a column). Fed by `level.get_data("StepCounter")` or equivalent. The single near-exception is `g50t`, where pressure is via scrolling backdrop rather than a counter — but the spirit (one resource that depletes per action) is universal. |
| Tag-based sprite querying (`level.get_sprites_by_tag(...)`) | **25 / 25** | Universal idiom. Sprites are grouped by shared `tags=[...]` and looked up by tag at runtime, not by name or layer. |
| 64×64 base canvas with sub-cell scaling via `Camera` | **25 / 25** | Universal. Several reference games declare smaller logical grids (12×12, 14×14, 16×16) that the engine scales up to fill the 64×64 frame with letter-box padding centred. **Do not copy this for generated games** — the upscale produces chunky uniform-colour cell-blocks that read as crude. Design at the display-pixel level (a 64×64 grid, or a closer-to-64 grid with rich internal sprite detail). See `checklist.md` item 21. |
| `available_actions` is a minimal subset of `[1..7]` | **25 / 25** | Every game declares only the action IDs it actually uses. Never the full 7. |
| ACTION1-4 arrows present | **~22 / 25** | Near-universal. Click-only exceptions: roughly `ft09`, `r11l`, `sb26`, `su15` and a few others. |
| ACTION6 click in `available_actions` | **19 / 25** | Click is the modal default. Pure-arrow exceptions: `g50t`, `ls20`, `re86`, `tr87`, `tu93`, `wa30`. Click hit-detection via `level.get_sprite_at(gx, gy, tag)` is the universal idiom. |
| ACTION5 used as a modal / "freedom slot" verb | **9 / 25** | `ar25`, `cd82`, `cn04`, `lf52`, `m0r0`, `re86`, `sb26`, `sp80`, `wa30`. Where most novelty visibly lives — the per-game distinctive verb. |
| ACTION7 undo | **6 / 25** | `ar25`, `bp35`, `lf52`, `sb26`, `sk48`, `su15`. Undo is the exception, not the norm. |
| Lives mechanic (multiple respawns) | **1 / 25** | Only `ls20` has explicit lives (3). `sp80`'s "4 pour attempts" is a per-level resource, not lives. Generated games should NOT have a respawn loop by default. |
| Camera viewport == level grid_size (per-level resize) | **25 / 25** | Every game with non-64 grids resizes the camera viewport in `on_set_level`. Default 64-by-64 viewport on a 12×12 grid renders the world in a corner. |

## How to use this in `study`

The `study` state used to ask the agent to re-derive these numbers
every run. That re-derivation always produced the same answers,
just with slightly different formatting. The state now skips that
work and the agent is expected to read this file once.

If the underlying reference set changes (a new game added, a
deep-analysis frequency table edited), update this file by
re-counting and bump the table accordingly.
