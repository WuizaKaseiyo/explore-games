# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised in #05).
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md.
- Reference source files read in full during #01 study (cn04, sp80, sk48, m0r0, tr87).
- prior-games/pf3w/ (created at this step).

## Deliverables Produced
- prior-games/pf3w/pf3w.py (534 lines).
- prior-games/pf3w/metadata.json.
- runs/<run_id>/workspace/implement-summary.md.

## Notes
- Implementation strategy: 64×64 pixel grid with 4-pixel logical cells (matching sk48-style scale convention). Sprite pixel matrices designed at pixel granularity with hollow-frame / filled-frame templates per logical cell that visibly damage on 2:1 downsampling (per checklist item 20). One bug caught and fixed during runtime smoke test: instance-attribute initialization order in `__init__` was overwriting state set by `super().__init__()` (which calls `on_set_level` automatically), so the walkable mask was None at first action; fixed by initializing instance attributes BEFORE calling `super().__init__()`.
- Witness solutions all verified end-to-end: L1 witness (10 actions) advances to L2; L2 witness (11 actions) advances to L3; L3 witness (24 actions) triggers `GameState.WIN` with `_win_score = 3`.
- BFS distances confirmed at runtime:
  - L1: slot_blue (3, 8) → target_blue (12, 8) = 9 cells.
  - L2: slot_A (3, 4) → target_A (12, 4) = 9; slot_B (3, 12) → target_B (10, 12) = 7.
  - L3: slot_blue (2, 2) → target_blue (13, 13) = 22 (around wall via gap); slot_magenta (4, 13) → target_magenta (13, 2) = 20 (also around wall via gap).
- Cross-color L3 distances confirmed: slot_blue → target_magenta = 21, slot_magenta → target_blue = 21 (would-be cross-color simultaneous solution). Without the M3b color-keying enforcement, this 21-tick simultaneous solution would be 1 action shorter than the M3b-enforced 24-action solution. M3b is enforced in code via the `_is_cell_in_frontier(lcx, lcy, color)` predicate which only counts same-color emitters.
- Ready to proceed to smoke_test.
