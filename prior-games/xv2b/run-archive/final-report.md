# Game generation final report

## Generated game
- **ID**: xv2b
- **Source**: `prior-games/xv2b/xv2b.py`
- **Metadata**: `prior-games/xv2b/metadata.json`
- **Lines of code**: 575

## Mechanic
Three vertical water-vessels stand side by side on the playfield,
each carrying a coloured target-line marker at a specific height.
The player has two verbs: clicking (ACTION6) toggles a valve open
or closed (or, at L3, switches a pump on or off), and pressing
ACTION5 advances the hydrostatic simulation by one global tick.
On every tick, each open valve between two vessels transfers one
cell of water from the higher-level side to the lower (provided
the slit is submerged), each active pump transfers one cell from
its source to its destination regardless of gravity, and each
drain consumes one cell of water from its vessel. The game wins
when every vessel's current water-level matches its target line.
Difficulty composes by adding mechanics: L1 gives only valves,
L2 introduces an always-on drain that destroys mass, and L3 adds
an uphill pump that lifts water past gravity-capped slits — all
three mechanics interacting in the L3 witness.

## Action mapping
| Action | Effect |
|---|---|
| ACTION5 | Advance the hydrostatic simulation by one tick: snapshot levels, queue transfers from open valves and active pumps, apply, then drain consumption. |
| ACTION6 | Click at (x, y); toggles a valve OPEN ↔ CLOSED or a pump ON ↔ OFF when the click lands on one of those sprites; clicks elsewhere are no-ops. |

## Levels
- **L1 — base dynamic system** (1 mechanic): valve-equalize. Witness 18 actions. Targets (8, 8, 8) from start (24, 0, 0); both V_AB and V_BC slit-4 must be opened, then 16 ticks distribute mass.
- **L2 — base + 1** (2 mechanics): valve-equalize + drain. Witness 9 actions. Drain on B forces mass-removal; opening V_BC then ticking 8 times lands all three vessels exactly on target by simultaneous flow + drain consumption.
- **L3 — base + 2** (3 mechanics): valve-equalize + drain + uphill-pump. Witness 27 actions. V_AB slit-15 carries 8 cells from A to B before slit-blocks; drain on A consumes the remaining 22 cells over 22 ticks; pump P_BC lifts the final 3 cells from B (locked at slit-8) into C.

## Novelty note
- **Closest taxonomy entry**: `sp80` (pour-shelf-route). Distinguishing rule: sp80 is *discrete falling drops* triggered by a pour-key with movable shelves redirecting drops into cups; xv2b is *continuous fill-level equalisation* across a graph of vessels connected by togglable valves with no drops.
- **Closest prior-game entry**: `kx14` (tide-tilt-buoyant). Distinguishing rule: kx14 is a *single tank* whose surface is raised/lowered by ACTION1/2 directly while floating balls tilt; xv2b is *N ≥ 2 separate vessels* connected by clickable valves where the player only toggles flow paths and lets gravity equalise — no surface raise, no floating balls, no anchors. Visual signature also differs: kx14 has one big horizontal water expanse; xv2b has 3 thin tall blue columns side-by-side with target-line ticks.

## Index update
One row appended to `prior-games/index.md`:

```
| xv2b | vessel-valve-equalize | Vessel Equalise — three water vessels with togglable valves equalize hydrostatically; L2 adds drains, L3 adds uphill pumps. | 2026-05-08T22:09:34Z | (autonomous) |
```
