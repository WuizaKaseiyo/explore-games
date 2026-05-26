# Core knowledge priors (allowed)

§3.4 of the NovaPlay Technical Report restricts every environment
to four prior categories. **Mechanics MUST draw from these only;
inventing a mechanic that requires a different prior is a
violation.**

## The four categories

### 1. Objectness
Elements are perceived as coherent, persistent entities that can
move, collide, or be occluded. Examples: a sprite that exists at
a position, can be picked up, can disappear when consumed.

### 2. Basic geometry & topology
Symmetries (mirror, rotation), elementary topology (inside vs.
outside, connectedness, holes). Examples: "the player must reach
the inside of a closed shape", "rotating a piece by 90° unlocks a
match".

### 3. Basic physics
Intuitive rules: gravity, momentum, bouncing, friction. Examples:
"objects fall to the lowest empty cell", "a moving block stops when
it hits another".

### 4. Agentness
Recognition that some objects act with intent and pursue goals.
Examples: "an enemy moves toward the player", "a guard alternates
between two waypoints".

Most strong NovaPlay mechanics combine 2-3 of these. A pure-objectness
game (just "move sprite around") is usually too thin; pure-geometry
("rotate this") is usually too abstract. Mixing physics + objectness
+ topology is a common sweet spot.


## Common features

These are recurring elements observed across the 25 reference games. The
percentages are the rough fraction of reference games that include the
element. The "must-have" entry is required; the others are optional and
should only be included if they serve the chosen mechanic.

### 1. Energy bar (must-have, 100% of games)

Every game has an energy bar that depletes one or more units per action;
the player loses if it runs out. Some levels run a tight step budget
(e.g. 10 steps with each step consuming several units of energy) and
others run a generous one (e.g. 200 steps with each step consuming a
single unit, or even a single unit only every few steps). Tune the
budget per level to match the puzzle's optimal solution length.

The position, colour, and direction of the bar are not fixed — design
them to fit the game's visual style. Common positions are the top row,
the bottom row, or a single column at one edge; common directions are
left-to-right, right-to-left, top-to-bottom, or shrinking from both
ends inward.

### 2. Buttons (optional, ~30% of games)

A button is a clickable sprite that performs a specific in-game action
when clicked (e.g. shift a row, fire a paint sweep, commit a programme).
A button must be visually distinguishable as clickable — usually by a
distinct shape, a coloured rim, or an icon embedded in its centre.
Design each button's shape and colour deliberately so its function is
legible from its appearance alone; do not rely on text labels.

### 3. Code-on-pad (optional, ~15% of games)

Some games ask the player to compose a short program on a code-pad by
clicking specific positions inside a pad region; running the program
then affects the game state. The pad's layout must make the available
syntax learnable from the rendered frame alone — the player must be
able to discover, by trial and inspection, what each pad position
contributes to the resulting program.

When designing this feature, decide explicitly:

- **Code representation** — what does each clickable position encode
  (a literal opcode, a parameter, a slot index, a colour)?
- **Syntax discoverability** — how does the player learn the syntax
  without external instructions (visual cues on the pad, a side-by-side
  effect preview, a worked example built into the level)?
- **Execution effect** — what triggers the run (a dedicated commit
  button, an automatic run after each click, a step-budget cost), and
  how does the result map back onto the game world?
