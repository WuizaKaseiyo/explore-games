# Game generation final report

## Generated game
- **ID**: fw8c
- **Source**: `prior-games/fw8c/fw8c.py`
- **Metadata**: `prior-games/fw8c/metadata.json`
- **Lines of code**: 495

## Mechanic
The carrier is a hollow pawn the player walks across a chamber via
cardinal arrow keys. Stepping onto a pigment pad combines that pad's
pigment id (one of orange / pink / light-blue) into the carrier's
stored 3-bit subset, retinting the carrier to a derived colour per a
fixed deterministic mixing table (e.g. orange + pink → green;
all-three → black). Stepping onto a slot whose demanded pigment
subset matches the carrier's current set consumes the slot AND clears
the carrier back to empty. Level 1 introduces the basic
pickup-and-deliver verb; level 2 adds derived-colour slots that
require visiting two pads between consume events; level 3 adds a
state-conditional door that is passable only when the carrier's
pigment subset equals the door's demand, partitioning the chamber
into upper (pickup) and lower (delivery) halves. The level wins when
every slot is consumed; loses when the per-level step counter drains.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move carrier one cell up |
| ACTION2 | Move carrier one cell down |
| ACTION3 | Move carrier one cell left |
| ACTION4 | Move carrier one cell right |

## Levels
- **L1** — base dynamic system: single pad (orange), single slot
  (orange). Tutorial in 9 actions.
- **L2** — adds multi-pigment mixture: two pads + two slots, one
  primary (slot_pink) and one derived (slot_green = {orange, pink}).
  20-action witness.
- **L3** — adds pigment-gated door: chamber partitioned by a wall
  row at y=4 with a single `door_green` (demands {orange, pink})
  bridging upper / lower halves; downstairs has 4 slots and 2 pads.
  26-action witness composes M1 + M2 + M3.

## Novelty note
- **Closest taxonomy entry**: `ls20` (cycler-attribute-match).
  Distinguishing rule: ls20 cycles three independent enum dimensions
  (shape / colour / rotation) through fixed alphabets via per-cycler
  ±1 increments; fw8c's state is a 3-bit subset closed under union
  with no order-dependency, and L3's pigment-gated door introduces
  topology gating absent from ls20 entirely.
- **Closest prior-game entry**: `pk4m` (duotone-flip-walk).
  Distinguishing rule: pk4m's gate is a 1-bit polarity; fw8c's gate
  is exact-equality on a 3-bit subset (passable only when carrier's
  set EQUALS the door's demand — not subset-of, not superset-of, not
  partial overlap). The state space the player navigates is 2 vs 8.

## Index update
One row appended to `prior-games/index.md`:
```
| fw8c | pigment-mix-walk | Pigment-Mix Carrier — carrier walks chamber accumulating 3-bit pigment subset; deliver to slot whose demand matches; pigment-gated door at L3. | 2026-05-10T07:03:04Z | (autonomous) |
```
