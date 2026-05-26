# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised)
- skills/code/{universal-scaffold,novaengine-api,id-generation,
  spec-template}.md
- skills/global/{action-enum,color-legend,paths}.md
- Reference source patterns from cn04 (full read in #01),
  m0r0 (full read), sb26/tu93/r11l (partial reads)

## Work
- Created `prior-games/wj7d/`.
- Wrote `wj7d.py` (646 lines) following universal-scaffold:
  imports → sprites bank → levels → constants → HUD widgets →
  Wj7d game class.
- Class skeleton: `__init__` registers Camera + interfaces (overlay
  + step counter), `on_set_level` resets per-level state from
  `level.data` (step_budget, crease_movable, crease_orient,
  crease_pos, auto_select_stamp), `step()` dispatches to handlers
  (click / fold / arrow), helpers `_handle_click`,
  `_handle_fold`, `_handle_arrow`, `_try_move_stamp` (collision-
  aware), `_try_move_crease`, `_check_win`, `_check_unwinnable`,
  `_get_hidden_state`.
- Stamps were initially given an asymmetric white inner accent
  which broke fold-coverage win-check (accent reflected to a
  position where the shadow was non-transparent). Fixed by
  switching to a center-2×2 accent that's invariant under both
  H and V reflection; matched shadow patterns made the accent
  positions transparent in the shadow.
- Smoke tested all three witness solutions end-to-end; all pass.
  Tested the named anti-witnesses (fold-without-move at L1,
  greedy red-first at L2, convenient-click re-orient at L3); all
  correctly trigger `lose()` via either the budget exhaustion
  path or the unwinnable-state detection path.

## Deliverables Produced
- prior-games/wj7d/wj7d.py
- prior-games/wj7d/metadata.json
- implement-summary.md (line count + smoke-test recap)

## Notes
- Engine attribute is `_levels` (not `levels`); use module-level
  `levels` constant for reading the levels list.
- `next_level()` on the last level transitions `_state` to
  `GameState.WIN` (not advancing `_current_level_index` past the
  last index).
- Stamps and shadows must have rotationally-symmetric internal
  patterns (under both H and V flips) so reflection alignment
  works for both crease orientations.
