# Gear-Mesh-Spin

## Summary

The grid hosts several **gear sprites**, each a 3×3 block of one
solid colour with a single 1-pixel **marker tooth** sticking out
of one of its 8 edge cells. A gear has 8 possible orientations
(the marker can occupy each of 8 positions around the gear's
border). Two gears that are **orthogonally touching** (their
3×3 footprints share a 1-pixel-wide edge) are **meshed**.

The base verb: ACTION6 click a gear to advance its marker by **one
notch clockwise** (a "tooth-tick"). The catch — every meshed
neighbour advances by **one notch counter-clockwise** in the same
step (counter-rotation by mesh). The propagation is *transitive*:
a neighbour of a neighbour advances by one notch back in the
clicked direction, etc., walking the mesh-graph by depth and
alternating sign.

Every level features one or more **target sockets** beside specific
gears; the gear's marker must point *into* the socket (in a fixed
required orientation) for that socket to be satisfied. The level
wins when every socket is satisfied simultaneously.

## Visual elements (distinct from prior corpus)

- 12×12 grid; gears are 3×3 same-colour blocks (one colour per
  gear; saturated palette values 8, 9, 11, 13).
- The 1-pixel **marker tooth** sticks out from one of the 8 edge
  cells of the gear's 3×3 body, painted black.
- A **target socket** is a 1×1 hollow ring sitting *adjacent* to a
  specific gear, in the orientation the marker must point. When
  the marker points at the socket, the socket's ring fills with
  the gear's body colour (visual confirmation).
- A **lock-mark** (level 2+) is a tiny 1-pixel cross overlaid on a
  gear, applied via ACTION5 to freeze that gear (and its
  participation in mesh propagation: a locked gear neither rotates
  nor transmits rotation through itself).
- A **cycle indicator** (level 3+) is a faint dotted ring around
  a closed mesh-loop the level's geometry forms, visible by frame
  inspection (rendered as 1-pixel dots).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Toggle the *lock* state of the most-recently-clicked gear. Locked gears refuse rotation and refuse to propagate rotation through themselves. | a gear is the most-recently-clicked target |
| ACTION6 | Click any gear's pixel; if the gear is unlocked, advance its marker by +1 notch CW; recursively advance every meshed neighbour by 1 notch in the alternating direction (CW for even-depth, CCW for odd-depth) — but skip locked gears (they neither rotate nor propagate). | always |

`available_actions = [5, 6]`. No avatar, no arrow keys.

## Mechanics enumeration

- **M1 — click-rotate-driver:** clicking a gear advances its
  marker by 1 notch clockwise (8 notch positions per gear).
- **M2 — counter-mesh-propagate:** every gear meshed (orthogonally
  touching) with the driver advances by 1 notch counter-clockwise
  *in the same step*; their meshed neighbours advance CW; etc.
  The mesh-graph BFS at even depth = CW, odd depth = CCW.
- **M3 — socket-orientation match:** each socket sprite is
  satisfied when its associated gear's marker points at the
  socket's cell.
- **M4 — gear-lock:** ACTION5 toggles a lock on the
  most-recently-clicked gear. Locked gears do not rotate AND
  truncate the propagation chain — a locked gear acts as a
  *cut-vertex* in the mesh graph from the click's perspective.
- **M5 — closed-mesh-loop:** when the mesh graph contains a
  *cycle* (a closed loop of gears each touching its two
  neighbours), the propagation around the loop is consistent only
  if the loop has even length; an odd-length loop creates a
  contradiction (a single click would demand the gear at the
  start of the loop both CW and CCW). The engine resolves this
  by *refusing to propagate around the cycle* — the cycle's
  closing edge does not transmit, so a click on a cycle member
  rotates it and one strand of neighbours but not the rest. The
  player must use M4 (lock) to break the cycle deliberately.

## Per-level progression (mechanic +1 / +2)

### Level 1 — base system (M1 + M2 + M3)
- 4 gears in a linear chain. 4 target sockets. Because they are in a chain, clicking gear 1 rotates 1 CW, 2 CCW, 3 CW, 4 CCW.
- **Witness:** ~15 actions. The player must calculate the relative rotation offsets required to align all 4 simultaneously. Clicking different gears shifts the relative phases.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (lock)
- 6 gears in a highly connected mesh (but no closed cycles yet). 4 target sockets. 
- **Witness:** ~30 actions. The high connectivity means rotating one gear messes up almost everything else. The player must align one sub-component, *lock* it via ACTION5 to sever the mesh propagation, then align the rest of the board.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (closed-mesh-loop) + composite
- 10 gears with multiple closed cycles. 6 target sockets. The closed cycles naturally refuse to rotate due to parity conflicts.
- **Witness:** 60+ actions. The player must deliberately use locks (ACTION5) to break the cycles into spanning trees. By selectively locking and unlocking "bridge" gears, the player can transmit rotations to distant parts of the board without affecting adjacent gears. This requires deep sequencing of (Lock A, Rotate B, Unlock A, Lock C, Rotate D).
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every action, walk every socket sprite. For each socket, compute its associated gear's marker direction (one of 8); compare to the socket's required orientation. If every socket matches, `self.next_level()`. After level 3, the engine auto-fires `self.win()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. No instant-fail collision.

## Internal state
- `self.gears: list[Sprite]` — all gear sprites; each has a `notch: int` field (0..7) representing marker orientation.
- `self.mesh: dict[Sprite, list[Sprite]]` — adjacency map computed once at level start (orthogonal-touch detection).
- `self.locked: set[Sprite]` — gears whose lock toggled on.
- `self.sockets: list[(Sprite, int, int)]` — socket sprite plus its associated gear and required orientation.
- `self.last_clicked: Sprite | None` — for ACTION5 lock toggle.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `qz73 — radial-cycle-lock`**: Gear-mesh-spin propagates rotation through a *graph* with alternating sign (counter-rotation by mesh) — a clicked gear and its neighbour rotate in *opposite* directions.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
A random clicker rotates random gears; with mesh-counter-propagation, random clicks rapidly de-align everything. L3 requires a *specific lock-then-click order* that is impossible to brute-force.

## Planning depth
- **L1:** moderate — player must understand alternating parity and how shifting the "driver" gear changes relative phase offsets.
- **L2:** deep — locking introduces permanent state boundaries. The player must solve the puzzle in isolated chunks.
- **L3:** very deep — dynamic reconfiguration of the mesh graph. The player must use locks as clutches to engage/disengage specific transmission lines.
