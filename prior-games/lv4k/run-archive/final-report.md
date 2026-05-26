# Game generation final report

## Generated game
- **ID**: `lv4k`
- **Source**: `prior-games/lv4k/lv4k.py`
- **Metadata**: `prior-games/lv4k/metadata.json`
- **Lines of code**: 491

## Mechanic

A horizontal beam pivots on a fulcrum at the centre of the playfield. The player has a tray of coloured weights below the beam: small (mass 1) and wider (mass 2) ring sprites. Clicking a tray weight selects it; clicking an empty beam slot places the selected weight there. Each weight contributes `mass × arm` to a running torque, and the beam visually tilts up to two levels in either direction; the level wins when every tray weight has been placed AND the torque sum is exactly zero. Across the three levels the system grows: L1 introduces placement-balance with two equal weights on a centred fulcrum; L2 adds mass-arm-asymmetry by mixing a heavier weight with two light ones; L3 adds a passenger sprite that sits on the beam and slides toward the dipping side whenever the tilt reaches its extreme — pushing the passenger off the beam ends or onto the fulcrum loses the level, so the player must order placements to keep the beam composed.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | Click at `(x, y)` — selects a tray weight, places the selected weight at an empty beam slot, or lifts a placed weight back to the tray, depending on what the click hits. |

## Levels

- **L1**: 4 placement slots at arms `±1, ±2`; tray = 2 mass-1 weights. Mechanic introduced: **place-balance**. Witness 4 actions (select-place pairs).
- **L2**: 6 placement slots at arms `±1, ±2, ±3`; tray = 1 mass-2 + 2 mass-1. Mechanic added: **mass-arm-asymmetry** (m2 contributes 2× per arm). Witness 6 actions.
- **L3**: same beam as L2; tray = 3 mass-2 + 1 mass-1; **passenger** sprite at arm +2. Mechanic added: **tilt-passenger-slide** (passenger shifts toward dipping side at `|tilt_level| ≥ 2`). Witness 8 actions; passenger ends safely on beam.

## Novelty note

- **Closest taxonomy entry**: `kx14` (`tide-tilt-buoyant`) — token "tilt" overlap. Distinguishing rule: kx14's tilt is fluid-surface inclination with floating balls moving via buoyancy; `lv4k`'s tilt is rigid-body torque equilibrium with no fluid, no buoyancy, and no anchor verb. The win predicate also differs: kx14 = positional (balls reach target cells); `lv4k` = configurational (torque sum equals zero with tray empty).
- **Closest prior-game entry**: `kx14` (same as above — present in both lists). No other prior shares ≥ 3 dimensions with `lv4k` per the negative similarity-check; the visual signature (single horizontal beam + fulcrum + tray) and core dynamic (rigid-body torque equilibrium) are absent from the 25 + 21 prior corpus.

## Index update

Appended one row to `prior-games/index.md`:

```
| lv4k | lever-balance-torque | Lever-Balance Torque — place tray weights onto a horizontal beam pivoting on a fulcrum so the integer mass-arm torque sum is zero with all weights placed. | 2026-05-06T23:41:37Z | (autonomous) |
```
