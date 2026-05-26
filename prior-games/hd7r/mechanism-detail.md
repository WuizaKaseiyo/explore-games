# hd7r — repulsion-herd-funnel

## Summary
The player walks a single teal **shepherd** one logical cell per arrow
press on a 16×16 board (each cell is 4 display pixels, so the playfield
fills the native 64×64 frame). Scattered on the field are autonomous
**timid creatures**; after every shepherd MOVE, each creature within a
fixed Manhattan scare-radius (4 cells) takes exactly one deterministic
step **away** from the shepherd — orange creatures back straight away
along their dominant Manhattan axis, magenta creatures veer one cell
perpendicular (the away-vector rotated 90° clockwise). Creatures
outside the radius hold still, and a creature whose flee-target is a
wall, a shut gate, the grid edge, or another creature does not move
that tick. The player never carries or pushes a creature — control is
purely positional, by choosing the side from which to approach. The
win condition is spatial: every creature must end on a **pen** of its
own colour. A click toggles a gate post in a dividing wall between shut
(blocking) and open (passable). The only failure is the depleting
top-row energy bar.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move shepherd UP one cell; then every in-radius creature flees | always; blocked by wall/closed-gate/edge/creature |
| ACTION2 | Move shepherd DOWN one cell; then creatures flee | always |
| ACTION3 | Move shepherd LEFT one cell; then creatures flee | always |
| ACTION4 | Move shepherd RIGHT one cell; then creatures flee | always |
| ACTION6 | CLICK; if the clicked cell holds a gate post, toggle it OPEN↔SHUT (no flee step occurs); else no-op | always offered |

ACTION5 and ACTION7 are not declared — there is no modal verb beyond the
click-toggle and no undo (slot 7 reserved strictly for undo, omitted).

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 flee-step (straight) — the base dynamic | Tutorial: one orange creature, one corner pen, no gates/interior walls. Push the creature east to the wall, then north to the corner pen (walls are the backstops). Witness `[1,4,4,4,4,4,4,1,1,1,1]` (K=11, D=2). |
| 2 | + M2 gate-toggle (click) | A horizontal wall splits the board with one shut gate. One creature's pen is below the wall (gate must be clicked open to herd it through); a second creature's pen is a wall backstop on the same side. Park the backstopped creature first so later gate-side moves don't dislodge it. Witness `[2,2,3,3,6@gate,4,2,2,2,4,2]` (K=11, D=4). |
| 3 | + M3 skittish temperament (perpendicular flee) | A vertical wall with one shut gate. A magenta creature flees perpendicular and must be sidestep-herded to a west wall pen; an orange creature must cross through the opened gate to an east pen. Compose all three: park the perpendicular creature first, open the gate, then drive the straight creature across. Witness `[2,2,4,2,4,1,2,3,1,1,6@gate,1,4,4,4,4]` (K=16, D=5). |

(`6@gate` = ACTION6 click on the gate post; its cell centre is display
pixel (34, 34).)

## Win condition
After each action, the level is won iff every `creature`-tagged sprite
occupies a `pen` cell whose pen-tag matches the creature's temperament
(orange `straight` creature on a `pen_straight` cell, magenta `perp`
creature on a `pen_perp` cell). On win, `self.next_level()` (which the
engine maps to `win()` on the final level).

## Lose condition
`self.lose()` fires when the private `_steps_used` counter reaches the
level's `max_steps` budget (44 / 80 / 90) before the win predicate is
satisfied. No hard-death path — creatures cannot harm the shepherd, and
the generous budget plus always-reversible herding prevent soft-locks.

## Internal state
- `_steps_used` — private per-level action counter (only incremented in
  handled action branches, never the engine `_action_count`, to avoid
  the RESET-counts-as-a-step first-frame bug).
- `max_steps` — per-level budget read from `level.get_data("max_steps")`.
- Gate open/closed is NOT a hidden flag — it is encoded by which of the
  two co-located gate-variant sprites (`gate_closed` / `gate_open`) is
  TANGIBLE vs REMOVED (two-sprite-swap), so the state is always visible.
- Creature temperament and pen colour are read from sprite tags at
  runtime (`straight`/`perp`, `pen_straight`/`pen_perp`).

## Notable code patterns
- **Repulsion (flee) resolution as a two-pass cell update**: compute
  each in-radius creature's away-target (straight = dominant-axis sign;
  perp = that vector rotated 90° CW), reject targets that hit a blocked
  cell or a still-occupied creature cell, then commit — guarding against
  two creatures colliding into one cell in a single tick.
- **`_blocked_cells()` recomputed per step** from wall sprites plus
  currently-TANGIBLE closed gates, so collision/flee-blocking is a pure
  set lookup independent of pixel-perfect collision.
- **Two-sprite-swap gate** via `set_interaction(REMOVED/TANGIBLE)` keeps
  the open/closed state legible and gates collision in one move.
- **Logical-cell ↔ display-pixel mapping** at a fixed 4-px stride
  (`_px`, `cell // CELL`) lets the game use a clean 16×16 logical grid
  while rendering rich 4×4 sprites at native 64×64.
- **Step-counter HUD** as a single depleting top-row bar
  (`RenderableUserDisplay`), the only HUD.
