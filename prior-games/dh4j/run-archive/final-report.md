# Game generation final report

## Generated game
- **ID**: dh4j
- **Source**: `prior-games/dh4j/dh4j.py`
- **Metadata**: `prior-games/dh4j/metadata.json`
- **Lines of code**: 444

## Mechanic

The player controls a single magenta avatar on a small grid where every walkable cell visibly carries one to three small yellow pips. Pressing a cardinal arrow translates the avatar by exactly that pip count in the chosen direction, leaping over any intervening cells (including walls) — only the destination needs to be in-bounds and non-wall, otherwise the press is a no-op. Wall barriers across the playfield force the player to use stride-2 and stride-3 leaps to cross them. A visibly-raised **switch button** (orange/maroon ring with a white core, rounded corners — clearly NOT a floor cell) toggles every pip-2 and pip-3 floor cell in place; the pip patterns themselves visibly transform (2-pip cells sprout a third pip and 3-pip cells lose one), so the connection between visual change and stride change is direct. A **pivot** cell visibly carries one extra maroon "bonus pip" alongside its stride pips; landing on it transfers the maroon pip to the avatar (rendered as a maroon corner dot), granting a one-shot +1 stride on the next press; the next press consumes both the avatar's maroon dot and the pivot cell's bonus pip simultaneously, so the player must visit the switch first and the pivot last to combine them for the final leap. Levels compose by stacking wall barriers (1-row → 2-row → 3-row) that require successively richer stride sources: L1 needs only the variable-stride leap; L2 needs the switch to upgrade a 2-pip to stride-3; L3 needs switch AND pivot to reach stride-4.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | UP leap by current cell's stride (pip count + any pending bonus pip) |
| ACTION2 | DOWN leap (same stride logic) |
| ACTION3 | LEFT leap (same stride logic) |
| ACTION4 | RIGHT leap (same stride logic) |

(No ACTION5 / ACTION6 / ACTION7.)

## Levels

| Level | Mechanic introduced | Specific challenge |
|---|---|---|
| 1 | M1 cell-pip-stride-leap; M2 goal-overlap-wins | Avatar at top-left of the bottom half (0, 4); walks RIGHT × 3 to discover the stride-3 cell at (3, 4); UP leaps the y=3 wall row to the goal at (3, 1). Witness `[R, R, R, U]` (4 actions). |
| 2 | + M3 switch-button-swaps-pip-counts | 2-row wall barrier; the leap cell is 2-pip (stride-2 = insufficient). The visibly-raised switch button at (5, 4) toggles all pip-2/pip-3 cells in place. Witness `[R, R, R, R, L, L, U]` (7 actions). |
| 3 | + M4 pivot-bonus-pip-pickup (one-shot) | 3-row wall barrier; stride-4 required. The pivot at (3, 5) carries a bonus pip; the switch at (5, 6) is below the pivot row so the player must detour down-then-right to the switch, then walk back left to the pivot. Greedy "spam UP" from start wastes the pivot bonus on a wall hit and is irrecoverable. Witness `[D, R, R, R, R, R, U, L, L, U]` (10 actions). |

## Novelty note

- **Closest taxonomy entry**: **lt7m (ell-jump-tour-block)** — *click + L-shape* jumps. **Distinguishing rule**: dh4j's verb is *arrow + cardinal cell-encoded stride*; lt7m's is click-to-L-jump. Different input, different jump shape (cardinal vs L), different distance source (cell pip count vs L-shape geometry).
- **Closest prior-game entry**: **bz3k (drift-impulse-cardinal)**. **Distinguishing rule**: bz3k stores velocity as avatar-internal state persistent across turns (±1 impulse model); dh4j reads stride from origin cell each press with no carried velocity state at all. Visual signatures also differ — bz3k features a velocity-arrow accent on the avatar, dh4j features per-cell pip-pattern floor tiles plus a visibly-raised switch button and a pivot cell with an extra maroon bonus pip.
- The negative-similarity 8-dimension check (re-run on the fleshed-out spec) returned ≤ 4 shared dimensions against the strongest near-misses (bz3k, lz7q, vk6m, wt39), with none sharing on the named principles (visual signature, pixel grain, core dynamic).

## Index update

Appended one row to `prior-games/index.md`:

```
| dh4j | tile-coded-stride | Stride Pips — each walkable cell has a 1/2/3-pip stride; arrow press leaps that many cells (intermediates fly-over); switch swaps 2↔3 pip patterns in place; one-shot pivot bonus pip grants +1. | 2026-05-11T02:02:52Z | (autonomous) |
```
