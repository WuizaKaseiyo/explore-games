# Mechanic taxonomy of the 25 NovaPlay reference games

Compiled by reading each game's source under `game_sources_3_lvls/<id>/`
and condensing the per-game evidence-layer in
`deep-analysis-3lvls/<id>/<id>-deep-analysis.md`.
Each row gives the game ID, mechanic family (2-3 word tag), and a
one-sentence description that captures actual gameplay (not visual
surface). Used as the static novelty floor by `pick_mechanic` and
`critique_spec`.

| game_id | mechanic_family | description |
|---|---|---|
| ar25 | shape-mirror-cover | A small coloured shape and a long straight mirror-line both float on the playfield; arrows nudge either the shape or the mirror, and the same-shape ghost sliding on the other side must cover every scattered dot before steps run out. |
| bp35 | procedural-graph-walk | A token sits on an 8×8 procedurally-built graph of coloured nodes; LEFT/RIGHT step along the current track, click teleports to a highlighted neighbour, undo rewinds; reach a procedurally-defined target configuration whose layout depends on the level seed. |
| cd82 | orbit-fire-paint | A paint-tank rides an 8-slot ring around a central canvas; arrows step it slot-by-slot, clicking a colour swatch loads a dye, FIRE charges the tank inward to splash a half (axial slot) or triangular wedge (diagonal slot) of the canvas in the loaded colour, until the canvas matches the target. |
| cn04 | nub-pair-glyph | Coloured glyphs with palette-8 nubs poking off their edges; click one to select, arrows slide it and ACTION5 rotates it 90° in place; arrange so every glyph's nubs each kiss exactly one nub of a neighbour. |
| dc22 | colour-cycle-walk | Pawn walks an arena scattered with coloured wedge-blocks and colour-wheel triggers; stepping on a trigger cycles every wedge of that colour to its next state in a fixed sequence; match the target ring. |
| ft09 | stamp-3x3-paint | A 32×32 empty canvas extends past the 16×16 camera viewport; tapping a cell stamps a 3×3 colour-pattern around it until the canvas matches the target pattern printed in the corner. |
| g50t | walk-vs-scroll | An avatar walks a scrolling board where the world slides one cell left every two turns; arrows step the avatar one cell, ACTION5 fires a context-special ability; reach the goal flag before the relentlessly-advancing left edge overtakes the avatar. |
| ka59 | sokoban-explode-chase | Click switches the active pawn among coloured pawns scattered in a walled arena; arrows slide the active pawn three cells and recursively push other pawns; explode-tiles spray neighbouring pawns outward; a chaser shuffles toward the active pawn each turn; cover every coloured target square. |
| lf52 | procedural-graph-walk-undo | Token sits on an 8×8 procedurally-built graph of coloured nodes; arrows shuffle along the current track, click teleports to a neighbour, undo rewinds the latest move; reach a target configuration whose layout depends on the level seed. |
| lp85 | row-col-shift-grid | Grid of coloured tokens inside a Rubik's-cube-like board with a pair of L/R arrow-buttons stuck to every row and every column on the outside; clicking a button shifts the entire matching row or column one cell in that direction until each token sits on its matching target tile. |
| ls20 | cycler-attribute-match | Magenta-yellow avatar wanders a wall-bound maze in five-pixel hops; stepping onto a coloured cycler-tile rolls its shape, hue, or rotation one notch through a fixed alphabet; reach the goal pad with the avatar's shape-colour-rotation triplet matching the imprinted target. |
| m0r0 | mirror-orb-merge | Two glowing pawns roam a winding maze as mirror-image siblings — UP moves both up but LEFT pushes one left while pulling the other right; merge each mirrored pair into one cell, while spike-tiles snap them back and clickable post-stones can be detached and slid aside. |
| r11l | centroid-puppet-leg | A pink-eyed coloured ring hovers at the average of two-or-three matching coloured footprints; clicking a footprint and then a destination drags it across a winding corridor and slides the ring with it; every ring must end up inside its same-coloured target ring without straying into a cyan no-go zone. |
| re86 | frame-paint-canvas | Hollow coloured-frame shapes float over a large hidden canvas with a target picture printed on it; arrows slide one frame and ACTION5 cycles which is active; each frame must visit the right colour-zone to dye itself and then settle over the canvas region whose target tint matches. |
| s5i5 | rod-stretch-retract | Coloured rectangular rods stand on the canvas like telescoping arms with a tiny dot at each tip; clicking one half of a coloured pair-of-windows control stretches or retracts the rod of that colour one notch along its axis (rods stacked on top slide along), until every dot ends up on its matching cross-shaped target. |
| sb26 | tile-place-commit | A row of coloured square tiles sits in a bottom tray and a row of target colour-boxes hangs at the top with one or more numbered frame-slots between; click-place tiles into slots, then ACTION5 sends a marker walking left-to-right across the top boxes ticking off colour matches. |
| sc25 | scene-find-target | A small explorer-avatar wanders an illustrated scene with a 3×3 directional touch-pad in the bottom-right corner and four arrow keys also active; tap-or-press to nudge the avatar one step, find and reach the specific scenery item named in the level's hidden goal-string. |
| sk48 | paired-snake-trail | Two coloured snake-heads lie at opposite ends of a tiled floor with bodies of segments stretched out across coloured tiles; arrows grow or retract the active snake one segment (perpendicular keys shimmy the whole body sideways past an anchor stone), until every segment of one snake covers a tile whose colour matches the corresponding segment-tile of the other snake. |
| sp80 | pour-shelf-route | A row of horizontal coloured shelves hangs above a row of empty U-cups; click a shelf to grab and slide it left/right with arrows; pour-key sends water plummeting from each marked spout (splits on a shelf, falls straight off), and the level wins when every cup catches a drop while drains spend one of four pour attempts. |
| su15 | recipe-fruit-collect | Coloured fruit-tokens scatter across an open arena; click them one at a time to scoop them up — picking the right number-and-flavour combination ticks off the recipe printed at the top, while patrolling enemy-tokens drift toward the player's last click. |
| tn36 | program-pawn-trace | A programmable pawn sits at one end of a coloured runway with a row of slot-buttons across the bottom; click buttons in sequence to choose move-and-rotate instructions, then run the programme; the pawn's traced path must light up exactly the cells of the target pattern. |
| tr87 | tape-rewrite-rule | A bookshelf of input→output rewrite rules sits above two horizontal tapes of coloured glyph-cards; LEFT/RIGHT slide a bracket-cursor along the lower tape and UP/DOWN cycle the bracketed card through its colour's seven-glyph alphabet, until the lower tape spells the exact rewrite of the upper tape under the rule set. |
| tu93 | maze-pickup-train | A 3-cell-tall pawn hops three pixels at a time along value-2 corridors carved into a maze-shaped tile; coloured arrows it walks past either fall in step behind it like ducklings, march one corridor-cell every turn on their own purple-clockwork, or wait dormant until brushed red; lead the whole train onto the goal-marker tile. |
| vc33 | row-slide-pull-tab | A long row of coloured floor-tiles carries a handful of small units perched on top, with a clickable pull-tab dangling from each end of the row; clicking a tab drags the entire row one step in that direction (every unit slides along), and the level is solved when each unit rests over the house painted in its own colour. |
| wa30 | lock-drag-crate | A green-tipped lavender player walks four-pixel hops, and pressing the lock key when standing beside a grey crate latches it to the player so the next walk drags the crate alongside; deliver every crate into a hollow blue-bordered goal-frame, while a purple drone in later levels competes for the same crates. |

## Notes on revising this taxonomy

Each row's `description` should answer: *if a player rendered this game and nothing else were known, what is the moving picture and what is the player doing?* If it reads like a feature list ("the game has X, Y, Z") or jargon ("uses ACTION6, tag-based grouping"), rewrite it.

The `mechanic_family` tag is 2-3 words. It should:
- name the active object and the active verb (e.g. `rod-stretch-retract`, `mirror-orb-merge`)
- avoid implementation detail (no "tag-based", "ACTION-driven", etc.)
- avoid generic placeholders ("puzzle", "game", "match")

For full evidence on any row, open the corresponding file under
`deep-analysis-3lvls/<id>/<id>-deep-analysis.md`.
