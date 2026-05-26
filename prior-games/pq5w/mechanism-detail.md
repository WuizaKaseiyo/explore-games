# pq5w — portal-pair-relocate

## Summary
Twin-Portal Drag — the playfield contains exactly two paired portal
sprites: an *anchor portal* (A, fixed) and a *float portal* (B,
movable). The avatar walks the grid via arrow keys; stepping onto
either portal queues a teleport that resolves on the next action,
sending the avatar to the paired portal's cell. ACTION6 click on a
valid empty floor cell (not a wall, anchor, goal, forbidden, or the
avatar) relocates B to that cell. The player drags B around the
level by walking through the pair and clicking new placements,
chaining portal jumps to bypass walls and route around forbidden
cells.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk avatar UP one STRIDE-cell | always; blocked by walls and out-of-bounds |
| ACTION2 | Walk avatar DOWN one STRIDE-cell | always; blocked by walls and out-of-bounds |
| ACTION3 | Walk avatar LEFT one STRIDE-cell | always; blocked by walls and out-of-bounds |
| ACTION4 | Walk avatar RIGHT one STRIDE-cell | always; blocked by walls and out-of-bounds |
| ACTION6 | CLICK at pixel (x, y) — select-then-place float portal B | click on B's own cell toggles `_float_selected` (visible cue: B's four corner pixels tint pink→light-blue, rest of the sprite is unchanged); a subsequent click on a valid empty floor cell relocates B there and deselects; click on an invalid cell when selected is a no-op (selection persists); click on any cell when NOT selected is a no-op |

When `_teleport_pending` is set (i.e., the previous action stepped
the avatar onto a portal cell), the *next* action's id is consumed
to advance the teleport phase: the avatar's position is set to the
paired portal's cell and no walk / click occurs that turn. This is
the standard `_phase >= 0` pattern from
`reference-game-patterns.md` and renders the source-portal frame as
a distinct intermediate render.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base dynamic system: walk + portal-traverse | Full-height wall column at logical x=8 (15 wall sprites) splits the playfield; goal at (14, 7) is reachable only by stepping onto anchor A at (3, 7) and teleporting to float B at (12, 7). Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (5 actions: 2 RIGHT walks, 1 RIGHT-as-resolve, 2 RIGHT walks). Step budget 30. |
| 2 | + portal-relocate (select-then-place ACTION6 clicks) | Closed walled room (22 wall sprites at x=4..11, y=2..6) with both portals A (6, 4) and B (10, 3) inside; goal (10, 4) inside. Avatar starts outside at (1, 9). Player must click B to select it, click an outside cell to place B near the avatar, walk onto B → teleport to A inside, then walk to goal. Witness `[ACTION6@(42, 14), ACTION6@(10, 38), ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (8 actions). Step budget 50. |
| 3 | + forbidden-cell-avoid | Same closed room as L2, plus a forbidden column at x=8, y=3..5 that fully separates sub-area-1 (with anchor A) from sub-area-2 (with goal). Stepping on a forbidden cell fires `self.lose()`. Player must teleport in (as L2), walk off A, do a second select-then-place of B into sub-area-2, walk back onto A → teleport to B in sub-area-2, walk to goal. Witness `[ACTION6@(42, 14), ACTION6@(10, 38), ACTION4, ACTION4, ACTION1, ACTION6@(10, 38), ACTION6@(38, 18), ACTION2, ACTION2, ACTION4]` (10 actions). Step budget 80. |

## Win condition

After every action's resolution (walk, teleport-resolve, or click),
`_post_action_resolve()` checks whether the avatar's (x, y) equals
the goal sprite's (x, y); if so, calls `self.next_level()`. After
the third level wins, the engine fires WIN.

## Lose condition

`self.lose()` is fired in two situations:
- the avatar's (x, y) equals the (x, y) of any forbidden sprite
  (avatar stepped on a forbidden cell) — L3 only;
- `_steps_used >= _step_budget` after the action's increments
  (private step counter exhausted).

## Internal state

- `_avatar`, `_anchor_portal`, `_float_portal`, `_goal` are looked up
  by tag (`get_sprites_by_tag`) on demand; positions live on the
  Sprite objects themselves.
- `_step_budget` (int) — per-level constant from
  `level.get_data("step_budget")`.
- `_steps_used` (int) — private step counter incremented inside
  step() (NOT `self._action_count`, to avoid the implicit-RESET
  off-by-one).
- `_teleport_pending` (tuple `(dst_x, dst_y)` or None) — set when
  the avatar walks onto a portal; consumed (and zeroed) by the next
  step() call's resolve branch.
- `_float_selected` (bool) — toggled on click-on-float-cell; gates
  whether a subsequent click on an empty cell relocates the float
  portal. The visible cue is a re-tint of the float portal's four
  corner pixels (pink ↔ light-blue) applied via direct
  `sprite.pixels[y, x]` writes; the rest of the outer ring and the
  magenta core stay unchanged.

## Notable code patterns

- **Phase-tick teleport**: avatar steps onto portal → set
  `_teleport_pending = (paired.x, paired.y)`; next step() resolves
  via `avatar.set_position(*_teleport_pending)` and clears the flag.
  This makes the source-portal frame a distinct render (the engine
  renders BEFORE the next step()).
- **Tag-based dispatch**: every per-sprite lookup
  (`_anchor_portal()`, `_wall_at()`, `_forbidden_at()`,
  `_portal_at()`) goes through `level.get_sprites_by_tag(...)`. The
  portal sprites carry both `"portal"` (for "is this any portal?"
  queries) and one of `"anchor"` / `"float"` (for "which one is it?"
  queries).
- **Click validation**: ACTION6 click rejects targets that aren't
  STRIDE-aligned empty floor cells; this closes the trivial-fallback
  exploit where a player would relocate B onto the goal cell to
  shortcut the win.
- **Select-then-place with persistent visual cue**: clicking the
  float portal toggles `_float_selected` and writes its four corner
  pixels directly (`sprite.pixels[y, x] = colour`), swapping them
  between pink (palette 7, unselected) and light-blue (palette 10,
  selected). The rest of the sprite is left alone, so the cue is
  subtle but persistent across frames. A second click on a valid
  empty cell performs the relocation and reverts the corners.
  Implements checklist item 19's "persistent visual cue for mutated
  state" rule for the new select state.
- **Per-level step budget via `level.get_data("step_budget")`**:
  the budget tunes per-level difficulty by editing one int.
- **Pure step counter via `_steps_used`**: avoiding the
  `self._action_count` off-by-one (RESET counts) per the
  fix_implementation guidance.
