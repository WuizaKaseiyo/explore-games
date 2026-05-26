# Game generation final report

## Generated game
- **ID**: kn58
- **Source**: `prior-games/kn58/kn58.py`
- **Metadata**: `prior-games/kn58/metadata.json`
- **Lines of code**: 546

## Mechanic

A pure-click puzzle on a 16×16 logical playfield. The player has no avatar and never moves any sprite directly. Their only verb is ACTION6 — a click that places (or relocates) a single magnetic anchor sprite at the clicked cell. After every click, every coloured pawn on the board simultaneously slides one cell along its dominant Manhattan axis toward the anchor (horizontal-first tiebreak, with secondary-axis fallback when the primary direction is wall-blocked). When a pawn lands on a same-colour target ring, it sticks — removed from further updates but still a collidable obstacle for moving pawns. The win condition is every pawn matched and stuck; the lose condition is exhausting the per-level step budget. Difficulty climbs through composition: L2 introduces pawn-pawn collision and a corridor-pocket geometry that forces the player to route one pawn into a side bay so the other can pass; L3 introduces an anti-anchor sprite that, after every pull, repels every non-stuck pawn one cell radially outward within Manhattan range 1, twisting the gradient field around obstacles.

## Action mapping
| Action | Effect |
|---|---|
| ACTION6 | CLICK at pixel (x, y) — relocates the single magnetic anchor to the clicked logical cell. Triggers Phase 1 (every pawn slides 1 cell toward anchor along dominant Manhattan axis), Phase-1.5 match-check, Phase 2 (anti-anchor push, if anti-anchor present), Phase-2.5 match-check. |

## Levels
- **L1 — base dynamic system.** 1 orange pawn at (4, 7), 1 orange target ring at (11, 7), no interior walls. Mechanics M1 (anchor-place-by-click), M2 (pawn-magnet-pull), M3 (colour-match-target-win) are all required. Witness: 7 clicks at logical (11, 7).
- **L2 — base + collision + matched-stick (+2).** 2 pawns (orange + purple) start at opposite ends of a horizontal row-7 corridor with a 2-cell southward pocket at column 7, must swap ends. Adds M4 (pawn-pawn-collision) and M5 (matched-pawn-stick). Witness ≈ 25 clicks via pocket-detour.
- **L3 — system + anti-anchor (+1).** Open arena with a fixed anti-anchor at (10, 8) range 1; orange must reach target_orange at (12, 8) past a pre-stuck purple blocker at (8, 8). Adds M7 (anti-anchor-repulsion). Witness: 12 clicks (south detour around purple, north return via row 9 with anti-anchor pushing pawn off (10, 9) to (10, 10), then back to (12, 8)).

## Novelty note
- **Closest taxonomy entry**: ka59 (sokoban-explode-chase). Distinguishing rule: ka59's verb is "click a pawn to make it active, arrows slide *that one pawn* and pawns push each other"; kn58's verb is "click *any cell* to place a magnetic anchor, every pawn slides simultaneously toward it, pawns block but never push". The player never directly moves a pawn in kn58.
- **Closest prior-game entry**: pz4t (anchor-pivot-place). Word "anchor" overlaps but the mechanic does not — pz4t's anchor is the placement *pivot offset* of a polyomino piece (the clicked pixel becomes the placement origin); kn58's anchor is a *standalone magnetic source* on the playfield with pre-existing pawns sliding toward it. Disjoint verbs (place piece vs place magnet) and disjoint goals (tile region vs match coloured rings).

## Index update
Appended one row to `prior-games/index.md`:

```
| kn58 | anchor-pull-magnet | Anchor-Pull Magnet — click any cell to place a single magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it. | 2026-05-05T11:55:37Z | (autonomous) |
```
