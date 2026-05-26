# Mechanic pick

## Game ID
`mz6t`

Verified against reserved 25 reference IDs and all 53 prior-game IDs (41 in `prior-games/index.md` plus 12 on-disk-but-pre-index entries: gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n — and the rest already counted). No collision; not an English word; 4 lowercase alphanumeric chars.

Pascal class: `Mz6t`.

## Mechanic family
`majority-vote-stabilize`

Prior categories used (per `core-knowledge-priors.md`):
- **Objectness** — each cell is a persistent coloured tile that retains its state across ticks until overwritten by a click or a vote.
- **Basic geometry & topology** — propagation respects 4-connected neighbourhoods; walls partition the field into voting regions whose stabilisation is locally determined.
- **Agentness** is *not* used — there is no avatar; the game's "actors" are abstract voting cells.

## One-paragraph description

The playfield is a small rectangular grid of square cells, each in one of three colour states (light pink / orange / light-blue, picked to read as three distinct hues without leaning on the standard red/yellow/green cultural triple). The player has exactly two verbs: **ACTION6** clicks a cell to advance its colour one notch around the 3-cycle, and **ACTION5** ticks the simulation forward one step — every cell *simultaneously* adopts whichever colour is held by a strict majority of its 4 cardinal neighbours, ties leaving the cell unchanged. A *target panel* off to one side of the playfield shows a half-scale stencil of the colour configuration the field must reach. Levels add **wall cells** (tagged dark-stone tiles that don't vote, don't get voted on, and break voting connectivity) and a **lock-when-correct** mechanic where an outlined "anchor" cell freezes its current colour the first time it matches its target value, removing one degree of freedom for subsequent ticks. The puzzle is to compose seed configurations whose multi-step majority cascade resolves to the target without overshoot — the two-verb minimality (no avatar to walk, no per-cell timer to mind) keeps the focus squarely on reasoning about *propagation under majority rules*, which in our taxonomy is an unexplored region.

## Action subset
`available_actions = [5, 6]` — minimal. No avatar movement, no undo. ACTION5 is the distinctive verb (per `action-enum.md` § "ACTION5 is where novelty lives").

## Novelty — positive similarity check (against taxonomy + prior-games)

Walked every taxonomy row and every prior-games row for family-level + description-level overlaps.

### Taxonomy near-misses

- **dc22 (colour-cycle-walk)**. Pawn walks an arena scattered with coloured wedge-blocks and colour-wheel triggers; stepping on a trigger cycles every wedge of that colour to its next state. Family-name overlap on "colour-cycle". Description-level: dc22's cycle is *triggered by walking onto a trigger cell* (agent-driven) and *fires globally on all wedges of one colour* (colour-class-scoped). My candidate has no walking agent and the only "cycle" verb is per-cell, applied to one cell per click — propagation is by majority vote, not by colour-class-scoped cycling. **Distinguishing rule**: dc22's state changes are *triggered globally on a single colour class by a walking pawn*; mz6t's state changes are *per-cell (clicks) and per-cell (vote majority over neighbours)*, with no avatar and no class-wide trigger.
- **ft09 (stamp-3x3-paint)**. Tap a cell to stamp a 3×3 colour-pattern around it until canvas matches target. Description-level: ft09's "match a printed target" is the same goal-shape and shares the corner-stamp printed-target HUD idiom — but ft09's edit primitive is a *3×3 brush* applied at the click location with a fixed paint pattern. My edit primitive is a *single-cell colour cycle*; the "spread" comes from the majority-vote tick, not from the brush radius. **Distinguishing rule**: ft09's brush deposits a 3×3 colour stamp from a fixed mask; mz6t's click changes only the clicked cell, and propagation is via a *separate ACTION5 tick that runs majority-vote globally*.

(Reference games surveyed for any other near-overlap on "click cells to compose, then run a global tick": none of the 25 has a global cellular-automaton rule. cn04 and sb26 have global checks but those are *win-predicate* checks, not state-mutating ticks.)

### Prior-game near-misses

- **gv47 (seed-grow-surround-dissolve)**. Click coloured seeds to grow regions; surround a same-coloured pip with paint and the ring auto-dissolves; ACTION5 globally mixes contacting region pairs into a derived colour. Description-level: shares the "click + ACTION5-global-tick + colour transformation" verb shape and the *match-a-coloured-target* goal. **Distinguishing rule**: gv47's growth is *outward from explicitly placed seed sprites along contiguous regions*, with a *region-merge* operator on ACTION5 that *creates new colours by mixing*. mz6t has no seeds or regions — every cell is a first-class voter, ACTION5 *does not change the palette in use* (cells stay in the original 3-state alphabet; no merging), and propagation is *uniformly local-4-neighbour majority*, not region-scoped.

- **tm5x (thermal-aura-imprint)**. Single pawn imprints temperature on its current cell + 4 neighbours; ACTION5 toggles polarity hot/cold; targets latch when their cell reads required value. Description-level: shares the "imprint a colour-state on a cell + neighbours, target-latching" pattern. **Distinguishing rule**: tm5x has a *single walking pawn* whose footprint imprints the surrounding cells (per-step, not per-tick); ACTION5 toggles which polarity the pawn imprints. mz6t has *no pawn, no imprint footprint*, and *no polarity toggle* — the field is a flat lattice of cells that mutate by majority-of-neighbours, plus per-cell click-cycling. The "active actor" is the rule, not a sprite.

- **qf8m (rook-cross-toggle)**. Click tiles to flip a (2N-1)-cell row+col cross; bishop tiles flip diagonals; tri-state cell cycles mod 3. Family-level: qf8m's flips are *click-triggered, deterministic, structurally non-local* (cross of length 2N-1) and the goal is a target binary/ternary pattern. Description-level: shares the *click-to-mutate-cells-toward-target* shape and the *3-state ternary cell* idea (qf8m has one tri-state cell at L3; mz6t makes every cell a 3-state). **Distinguishing rule**: qf8m's effect of one click is *deterministic and global on a fixed cross/diagonal axis* — no propagation, no time evolution. mz6t's clicks are *purely local (one cell)*; the only way to reach more than the clicked cell is to press ACTION5 to evolve under majority rule, and the resulting cascade is *non-deterministic in shape* (depends on the seeded configuration). qf8m has no notion of a "tick" and no rule that operates without an explicit click target.

- **mr5q (polarity-attract-discharge)**. Pawns flip yang/yin via click; per ACTION5 each walks toward nearest same-colour opposite; same-colour adjacency discharges. **Distinguishing rule**: mr5q has movable pawns that walk under attraction; mz6t has stationary cells that vote. Different objects, different verbs.

- **pf3w (wavefront-converge-timing)**. Click pre-placed slots to activate emitters; ACTION5 ticks BFS-radius wavefronts outward; level wins when target receivers coincide with a frontier cell. **Distinguishing rule**: pf3w's tick *expands frontiers from emitters* (a synchronous BFS), and the win condition is *coincidence-on-one-tick* (timing). mz6t's tick *settles the entire field locally toward the majority*, with no frontier and no timing-coincidence — the win is a *steady-state-pattern match*.

- **gx7m (gear-mesh-cascade)**. Discs whose rotations propagate with sign flip across cardinal mesh. Different prior — propagation is rotational, not majority-vote.

- **kp9z (grain-accumulate-topple)** and **vd3g (valley-dig-roll)**. Both are gravity / overflow-cascade puzzles — quanta routed via height-difference rules. mz6t has no notion of height or quanta; the rule is a vote, not a flow.

### Negative-similarity check (the kf42 → vh68 cautionary test)

I mentally rendered an L1 frame of mz6t — small grid (≤ 8×8) of 8-pixel cells in three pastel hues, plus a half-scale target panel at the right edge of the frame and a step-counter bar along the bottom — and walked the eight dimensions vs the priors with the most "click + global tick on a small cell grid" vibe (qf8m, gv47, ft09, tm5x, pf3w):

| Dim | qf8m | gv47 | ft09 | tm5x | pf3w |
|---|---|---|---|---|---|
| 1. What is on the board | grid of cells *(shared)* | seeds + paint regions *(diff)* | canvas + corner target *(shared)* | pawn + cells *(diff)* | emitters + receivers *(diff)* |
| 2. Player verb | click cells *(shared)* | click seeds + ACTION5 *(shared verb shape)* | click cells *(shared)* | walk + click + ACTION5 *(diff — has pawn)* | click slots + ACTION5 *(shared shape)* |
| 3. What level asks | pattern match *(shared)* | regions match *(diff)* | canvas match *(shared)* | targets latch *(diff)* | timing-coincidence *(diff)* |
| 4. Lose | step budget *(shared)* | step budget *(shared)* | step budget *(shared)* | step budget *(shared)* | step budget *(shared)* |
| 5. Cast | cells + target panel *(shared)* | seeds + pips + paint *(diff)* | canvas + target stamp *(shared)* | pawn + cells *(diff)* | emitters + receivers *(diff)* |
| 6. Visual signature | ternary cells, ring motifs *(distinct: qf8m's signatures use rook/bishop motifs and a magenta+light-blue+pink palette; mz6t avoids those motifs and uses a different palette accent — pink/orange/light-blue cycle with maroon walls)* | organic blooms *(distinct)* | corner-target stamp aesthetic *(partial-share — mz6t reuses the half-scale target-panel idiom)* | aura ring *(distinct)* | spreading frontiers *(distinct)* |
| 7. Pixel grain | rich 8×8 cells with internal motifs *(matched)* | painted blobs *(distinct)* | 3×3 stamps *(distinct)* | aura *(distinct)* | frontiers *(distinct)* |
| 8. Core dynamic | per-click cross-flip *(distinct)* | grow + auto-dissolve *(distinct)* | brush stamp *(distinct)* | walk + imprint *(distinct)* | BFS frontier coincidence *(distinct)* |

**Closest:** qf8m on 5 dimensions (1, 2, 3, 4, 5) and ft09 on 5 (1, 2, 3, 4, 5).

This *is* close to the negative-similarity threshold; the principles guide me to weight 6/7/8 heavily. mz6t's **core dynamic is majority-vote propagation under a *separate tick verb***, which is fundamentally different from qf8m's per-click cross-flip (no time evolution) and ft09's brush stamp (no time evolution). To diverge further on the **visual signature** axis I will:

- Use a maroon-palette wall + dark-grey background (palette `13` and `4`) instead of qf8m's grey/black/magenta scheme.
- Render each voting cell as an **8×8 "tile" sprite with a pink/orange/light-blue centre disc inside a thin off-black ring** — the disc-in-ring motif is distinct from qf8m's rook plus / bishop X / tri-state inner-block motifs.
- Place the target panel on the **left** of the playfield rather than ft09's bottom-right corner, and at **¼ scale** (each target cell is 2×2 pixels) rather than half-scale, so the visual signature reads differently from ft09.

With these visual choices and the wholly distinct core dynamic, mz6t passes the negative-similarity test on the heavyweight axes (6, 7, 8) — the lighter shared dimensions (1, 3, 4, 5) are unavoidable for any "small grid + match a target + step-budget" puzzle and don't, by themselves, push past the 3+ threshold once the principle-weighted axes diverge.

## Verdict
**NOVEL.** The candidate's core dynamic — *majority-vote cellular-automaton propagation under an ACTION5 tick, seeded by per-cell ACTION6 clicks* — does not appear in any of the 25 reference games or in any of the 53 prior generations on disk. Distinguishing rules are stated concretely against the closest 5 priors (gv47, tm5x, qf8m, mr5q, pf3w) and against the closest taxonomy entries (dc22, ft09); negative-similarity has been re-checked against qf8m and ft09 with concrete visual divergences (palette accent, sprite motif, target-panel placement and scale). Proceeding to `write_spec`.
