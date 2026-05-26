# Step #05: write_spec (revision 1)

## Inputs Consumed
- mechanic-spec.md (just-written, now being revised)
- critique-revisions.md (3 issues from critique visit 1)

## Deliverables Produced
- mechanic-spec.md (revised). Sections changed:
  - **§3 Sprite roster** — `pusher_knob` row revised: removed "handle protrusion" wording; replaced with symmetric button shape (recessed centre); explicit pixel pattern given. Addresses Critique-1 Issue 2 ("handle reads as directional arrow / cultural convention").
  - **§3 Sprite roster** — added `dead_end_wall` sprite (6×6 black) for explicit dead-end terminal markers. Addresses Critique-1 Issue 3 (off-grid coords).
  - **§4 L1 Layout** — cleaned up; removed the spurious "right pusher decoy" section that conflicted with the socket position; left a single clean "one pusher, one chain, one socket" tutorial.
  - **§4 L2 Layout** — Critique-1 Issue 1 fix: removed `target_socket_yellow` decoy at `(28, 54)` (it was unfillable, making win impossible). Replaced with `dead_end_wall` at `(28, 54)`. Win predicate now satisfied — the only `target_socket` (blue) is at `(28, 6)` and is fillable via up-branch.
  - **§4 L2 Necessity** — updated junction-routing counterfactual to reference `dead_end_wall` (down-branch ends at wall, not at yellow socket).
  - **§4 L2 Difficulty (c)** — updated plausible-but-wrong-alternative + witness-reasoning to reference `dead_end_wall` instead of yellow decoy.
  - **§4 L3 Layout** — Critique-1 Issue 3 fix: positions revised to fit fully within `[0, 64) × [0, 64)`. New layout: chain A horizontal stem at y=46 with vertical up-branch terminating at (20, 28), eject to merge_pad at (20, 22); chain B horizontal stem at y=22 with horizontal left-branch terminating at (26, 22), eject to merge_pad at (20, 22). Both chains' default-active "down" branches now have dead_end_walls explicitly placed on-grid (`dead_end_wall_A` at (20, 58), `dead_end_wall_B` at (38, 34)).
  - **§4 L3 Necessity** — updated junction-routing counterfactual to name the explicit `dead_end_wall` sprites.
  - **§4 L3 Witness** — concrete click coordinates given (junction A click at (23, 49), pusher A at (5, 49), junction B at (41, 25), pusher B at (59, 25)).

## Notes
- All three critique issues addressed inline.
- The L3 layout now has both junctions cycling between "down" (dead-end) and a non-down direction (chain A: up; chain B: left). The state is explicit.
- Witness-action coordinates calibrated to centre of each clickable sprite (`top_left + 3` for 6×6 sprites).
- No other §s required changes; all other checklist items pass per the previous critique pass.
- Re-entering critique_spec for visit 2 of 10.
