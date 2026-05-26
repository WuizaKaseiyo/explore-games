# yh3p — vine-branch-bloom

## Summary

The player nurses a single rooted vine across the playfield. Arrow
keys extend the vine's active glowing tip one cell at a time,
leaving a permanent green stalk segment behind; the vine cannot
grow into walls or onto existing vine. ACTION6 click on any prior
vine cell jumps the active tip there to start a new branch — the
vine grows as a tree, not a single path. On the final level,
terminal flower buds carry a yellow stamen indicating their intake
direction; the player must arrive at the bud moving INTO the
intake side and press ACTION5 to bloom-commit. Win = all buds
bloomed before the step counter drains. Lose = step budget
exhausted.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Grow active tip 1 cell UP. Tip facing → UP. | Tip is active (not dormant after a bloom) and not blocked on a notched-bud cell. Target cell in bounds, not wall, not vine. `bud_closed`: target allowed (auto-blooms on entry). `bud_notched`: target allowed (tip enters; M1 from there blocked until M3 succeeds or M2 re-anchors). |
| ACTION2 | Grow active tip 1 cell DOWN. Tip facing → DOWN. | As ACTION1, downward. |
| ACTION3 | Grow active tip 1 cell LEFT. Tip facing → LEFT. | As ACTION1, leftward. |
| ACTION4 | Grow active tip 1 cell RIGHT. Tip facing → RIGHT. | As ACTION1, rightward. |
| ACTION5 | Bloom-commit at tip cell. | Tip on a `bud_notched` AND tip facing == bud's intake direction (rotation 0→UP, 90→RIGHT, 180→DOWN, 270→LEFT). On success, replaces bud with `bloom`, sets tip dormant, clears facing. On `bud_closed`: no-op (already auto-bloomed). Action consumes a step regardless. |
| ACTION6 | Click at (x, y) display pixels. | If cell maps to a vine sprite (`root` or `stalk`), re-anchor active tip there and clear facing → none. Click on non-vine cell: no-op. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Extend-tip alone. Single closed bud reached by arrow growth. | Witness `[ACTION4×12]` (12 actions). Empty 12-cell corridor, no walls, no branching needed. |
| 2 | Adds ACTION6 click-to-rebranch. Two closed buds in opposite regions of a walled playfield. | Witness `[ACTION1×6, ACTION6@(16,32), ACTION2×7, ACTION4×8, ACTION1×7]` (29 actions). Wall column at x=8 with single bottom-row gap; first branch covers near bud, then re-anchor at root and route through gap to far bud. |
| 3 | Adds ACTION5 directional bloom-commit on notched buds. Three notched buds with stamens facing UP / RIGHT / DOWN respectively, in three quadrants of L-walled playfield. | Witness `[ACTION2×3, ACTION4×9, ACTION1×4, ACTION3×1, ACTION2×1, ACTION5, ACTION6@(28,28), ACTION2×5, ACTION3×3, ACTION5, ACTION6@(48,28), ACTION2×1, ACTION4×1, ACTION2×5, ACTION3×1, ACTION1×1, ACTION5]` (40 actions). Each branch must terminate with a 1-cell move whose direction matches the bud's intake; after each bloom tip is dormant so M2 click is required between buds. |

## Win condition

After every action, `_check_win` returns True iff no `bud_closed`
or `bud_notched` sprites remain in the level (i.e. all buds have
been replaced by `bloom`). Triggers `self.next_level()`.

## Lose condition

`_step_bar.current_steps <= 0` triggers `self.lose()`. No collision-
based instant-fail.

## Internal state

- `_active_tip_cell: tuple[int, int]` — pixel coords of the cell
  the tip currently occupies (always 4-aligned).
- `_tip_facing: str | None` — one of `"UP"`, `"DOWN"`, `"LEFT"`,
  `"RIGHT"`, or `None` (level start, post-click, or post-bloom).
- `_vine_cells: set[tuple[int, int]]` — pixel coords of all cells
  occupied by vine (root + every grown stalk + bloom cells from
  auto-bloomed `bud_closed`s and bloomed `bud_notched`s).
- `_tip_blocked_on_notched: bool` — True when tip is sitting on an
  unbloomed `bud_notched`; M1 rejected until M3 succeeds or M2
  re-anchors.
- `_tip_active_sprite`, `_tip_dormant_sprite` — the two pre-placed
  tip overlay sprites; one is `InteractionMode.TANGIBLE` and the
  other `REMOVED` at any moment based on `_tip_facing` (None →
  show dormant; not None → show active rotated to facing).
- `_step_bar: StepBarHud` — top-row pink-to-grey depleting bar.

## Notable code patterns

- **Two-sprite swap for tip overlay**: pre-place both `tip_active`
  and `tip_dormant` sprites at the root cell; toggle via
  `set_interaction(TANGIBLE)` / `REMOVED` per facing state. Avoids
  dynamic add/remove for the overlay; rotation on the active sprite
  carries facing.
- **Tag-based collision lookups**: `_wall_at(x, y)` and
  `_bud_at(x, y, tag)` iterate `level.get_sprites_by_tag(tag)` and
  match by position. Cleaner than maintaining a per-cell sprite
  index.
- **Vine cells set as authoritative collision source**: `_vine_cells`
  is the single source of truth for "this cell is filled with
  vine". Updated on every M1 success or successful bloom. Decouples
  collision from sprite enumeration.
- **In-place sprite replacement on bloom**: when M3 blooms a
  `bud_notched`, the bud sprite is removed from the level and a
  fresh `bloom` sprite (cloned from the template) is added at the
  same position. Same idiom for `bud_closed` auto-bloom on M1
  entry.
- **Bud rotation as direction encoding**: bud_notched's rotation
  (0/90/180/270) maps directly to the required intake-facing via
  `BUD_ROT_TO_INTAKE_FACING = {0: "UP", 90: "RIGHT", 180: "DOWN",
  270: "LEFT"}`. Rendering rotates the yellow stamen accordingly,
  giving the player a single visual cue for the rule.
