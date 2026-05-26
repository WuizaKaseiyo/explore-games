# Marble-Drop-Switchyard

*(Replaces `life-tick-evolve.md`. Real-world inspiration: marble-run
toys, train switchyards, gravity-fed bingo machines. Side view,
falling motion, dynamic.)*

## Summary

A tall vertical board with **diagonal ramps**, **Y-junction switches**,
and a row of **collection cups** at the bottom. The player launches
**coloured marbles** from a tray at the top. Every tick, every
in-flight marble rolls one cell along its current ramp; on hitting a
switch it diverts left or right by the switch's current orientation;
on falling off the bottom of a ramp it drops vertically until it
lands on the next ramp or in a cup.

The player has two verbs: **launch a marble** (ACTION6 click on a
marble in the tray) and **flip a switch** (ACTION6 click on any
switch). Switches can be flipped at any time — including while
marbles are in flight, which is the whole game. ACTION5 advances
the simulation one tick.

The level wins when every marble has come to rest in a cup of its
own colour. Marbles in wrong cups, marbles still rolling, or marbles
that fall off the world all count as failures at end-of-level.

## Visual elements (distinct from prior corpus)

- 64×64 canvas oriented as a **vertical side view**: tray of marbles
  at top (3-cell-tall band), playfield with ramps in the middle, cup
  row at bottom. Visually unlike anything in the corpus.
- **Marbles** are 2×2 sprites in distinct palette colours; while
  in flight they leave a 2-tick fading streak (lighter shade) so
  the player can read direction at a glance.
- **Ramps** are 1-pixel-thick diagonal lines drawn in dark wood-
  brown, oriented either `\` (right-falling) or `/` (left-falling).
  A marble on a ramp visually sits 1 pixel above the line.
- **Y-junction switches** are small 3×3 sprites with a triangular
  arm; the arm's direction (down-left or down-right) is the switch
  state. A faint dot at the centre flashes once per tick to
  communicate "live".
- **Collection cups** are 4-cell-wide U-shaped sprites at the
  bottom, each tinted in the colour they accept (with a 1-pixel
  white rim if currently empty, gold rim if filled correctly,
  red rim if filled with the wrong colour).
- L2 introduces:
  - **Speed pips** on each in-flight marble: a tiny 1-pixel pip on
    its top side. 0 pips = slow (default), 1 pip = fast.
  - **Friction-rugs**: 1-cell red-orange textured cells you can
    place on horizontal ramp segments — they drain a fast marble
    back to slow when the marble passes over.
- L3 introduces:
  - **Mixer cup** (purple-rimmed, neutral colour) — when two
    same-colour marbles enter, they fuse into a single marble of
    a derived colour (recipe per level).
  - **Track-flip levers**: two tall lever sprites flanking a
    column; clicking one flips every ramp in that column from
    `\` to `/` (and vice versa) at the cost of 1 step.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the simulation one tick. Each in-flight marble moves one cell along its current ramp; gravity pulls falling marbles 1 cell down. Switches do not move. | always |
| ACTION6 | Click cell `(x, y)`. Resolves to one of: (a) marble in tray → launch (place at the column directly below, in flight); (b) switch → flip; (c) friction-rug placement (L2+, only on a designated rug-tray); (d) track-flip lever (L3+). Misclick = no-op, no step. | always |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — launch:** ACTION6 click on a tray marble places it at the
  top of the playfield in the column the tray sits in. The marble
  becomes "in flight" with speed=0 and ramp=current cell.
- **M2 — physics tick:** ACTION5 advances every in-flight marble
  one cell. Movement rule:
  - On a `\` ramp: marble moves diagonally down-right one cell.
  - On a `/` ramp: marble moves diagonally down-left one cell.
  - Off-ramp / falling: marble falls down one cell.
  - On a switch: marble enters the switch and exits in the
    switch's current direction (down-left or down-right) on the
    next tick.
  - On a cup: marble settles, scored.
- **M3 — switch-flip:** ACTION6 click on a switch flips its
  arm direction, including mid-tick (the marble currently atop
  the switch will use the new direction on the next tick).
- **M4 — match-cup:** the win predicate requires every marble to
  rest in a cup of its own colour. Wrong-colour cups and
  off-board falls count as fails.
- **M5 — speed-decay (level 2+):** when a marble falls 3 cells
  vertically in a row without hitting a ramp diagonal, its speed
  pips advance to 1. A speed-1 marble that enters a switch
  **ignores the switch's arm and goes straight through** (in the
  direction the switch's last marble exited, i.e. the previous
  arm position). Friction-rugs (cells the player places on
  designated rug-tray slots) drain a speed-1 marble back to 0
  when it passes over. There is a finite supply of rugs per
  level.
- **M6 — mix-cup + track-flip (level 3+):**
  - **Mixer cup**: when two same-colour marbles enter the same
    mixer cup, they fuse into a derived-colour marble that
    immediately re-enters the playfield from the cup's top, with
    speed=0, in the column above the cup.
  - **Track-flip lever**: clicking inverts every ramp in one
    column simultaneously. Cannot be undone. Cost 1 step.

## Per-level progression

### Level 1 — base run (M1 + M2 + M3 + M4)
- 12-cell-wide playfield. 3 marbles in tray (red, blue, gold).
  3 cups at the bottom (red, blue, gold in scrambled order).
  4 switches arranged to route from any column to any cup.
- The player must launch each marble, time switch flips so each
  marble takes the right path. Marbles arrive at switches in
  predictable cadence given launch order.
- **Witness:** sequence of (flip, launch, tick, tick, flip, launch,
  …) totaling ~16 actions. Step budget 22.
- **Mechanics required:** M1, M2, M3, M4.

### Level 2 — + M5 (speed-decay + friction-rugs)
- 14-cell-wide playfield. 4 marbles, 4 cups. Geometry includes
  long vertical drops where marbles accelerate to speed=1. The
  player has 2 friction-rugs in a side tray, placeable on three
  designated rug-slot cells.
- One target cup is reachable only via a switch that the marble
  must NOT skip — i.e. the marble must arrive at speed=0. The
  player must place a friction-rug to bleed off the speed before
  the critical switch.
- **Witness:** ~30 actions including 2 rug placements.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (mixer + track-flip)
- 16-cell-wide playfield. 5 marbles: 2 red, 2 blue, 1 gold. Cups:
  red, blue, **purple** (= red + red), **green** (= blue + blue),
  gold. So the red and blue marbles must be paired through mixers
  to produce purple and green; gold goes solo. 6 switches; 3
  rug-slots; 2 track-flip levers (each affecting a different
  column).
- The track-flip levers are required because the default ramp
  layout sends BOTH reds to the same first switch — they will
  collide unless the layout is reshaped mid-level. The player
  must flip a column of ramps to bifurcate the early path.
- **Witness:** ~55 actions. Step budget 80.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition

After every ACTION5, check the cups. If every marble has settled
in a cup of its own colour AND no marble is still in flight AND
no marble fell off the world, fire `self.next_level()`.

## Lose condition

- `steps_used >= max_steps` triggers `self.lose()`.
- An in-flight marble that falls off the bottom of the world (no
  cup catches it) → `self.lose()`.
- A marble that lands in a wrong-coloured cup → `self.lose()`.

## Internal state

- `self.tray: list[Marble]` — pending marbles each with `colour`.
- `self.in_flight: list[Marble]` — `(pos, colour, speed, last_dir)`.
- `self.cups: list[Cup]` — `pos`, `accepted_colour`, `contents`.
- `self.ramps: dict[(int, int), str]` — `'\\'` or `'/'`.
- `self.switches: dict[(int, int), str]` — `'down-left'` or
  `'down-right'`.
- `self.rugs_available: int`, `self.rug_slots: list[(int, int)]`.
- `self.mixers: dict[(int, int), Mixer]` — `holding_colour`,
  `recipe`.
- `self.track_levers: list[(int, int, int)]` — `(lever_pos, column,
  used: bool)`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `gg17 — fuse-burn-ignite`**: fuse-burn propagates fire
  across a graph of fuse cells. Marble-drop has *physical
  trajectories* — falling balls with momentum and direction
  inheritance, not graph propagation. Marbles can be rerouted by
  flipping switches mid-flight, which fire cannot.
- **vs `vn8d — domino-cascade-topple`**: vn8d is a planar topple
  graph. Marble-drop is a **vertical motion** puzzle with
  trajectory + speed + cup-matching.
- **vs `gg11 — tide-current-drift`**: tide-current is a global
  drift on a top-down board. Marble-drop is a per-marble
  trajectory on a side-view board with switches that affect each
  marble individually.

## Step budget

- L1: 22.
- L2: 38.
- L3: 80.

## Random-resistance

Random launch + random switch flips fail almost always: a marble
needs ~5-7 correct switch states to reach the right cup. With 4+
marbles and switches, the joint probability of random play
reaching every cup correctly is exponentially small. L3 in
particular punishes random play — the mixer recipes only fire on
exactly-paired colours, so a random launch order destroys
recipes.

## Planning depth

- **L1:** moderate — read the board, plan switch flips, launch
  in the right order.
- **L2:** deep — speed propagation and the limited friction-rug
  budget force the player to identify *which* switch needs a
  slow arrival vs. which can take a fast pass-through.
- **L3:** very deep — mixers create dependent pairs (must launch
  same-colour marbles to the same mixer), track-flip is a one-way
  topology change, and the budget is tight.
