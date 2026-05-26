# implement-summary — yh3p

## Files written

- `prior-games/yh3p/yh3p.py` — 411 lines.
- `prior-games/yh3p/metadata.json`.

## Implementation notes

Tag-based dispatch; sprite bank declared at module scope (8
templates: root, stalk, tip_active, tip_dormant, bud_closed,
bud_notched, bloom, wall). Each level pre-places its own sprite
roster including a tip_active/tip_dormant sprite pair at the root
cell; on_set_level locates them by tag and toggles
`InteractionMode.TANGIBLE` / `REMOVED` to expose exactly the right
sprite based on whether the tip currently has a known facing
direction. Stalks are added dynamically via `level.add_sprite` as
the player extends; bloomed cells replace bud sprites in place.
Step budget per level read from `level.get_data("step_budget")`.

## Plain-English mechanic summary (no spec coordinates)

A growing branching plant: arrows extend a glowing tip leaving a
permanent green trail, click any prior trail cell to spawn a new
branch from that point, and on the final level a directional
commit verb finishes off ringed targets that only accept a tip
arriving from a specific side.

## Verification

- `python -c "import ast; ast.parse(...)"` — passes.
- `python -c "from yh3p import Yh3p; g = Yh3p(); ..."` — passes:
  level count = 3, initial tip at (12, 28) on root cell,
  step_budget = 24 for L1.
- L1 witness (12 ACTION4 presses): completed; level advanced to
  L2 with budget reset to 50. ✓
- L2 witness (29 actions): completed; level advanced to L3 with
  budget reset to 100. ✓
- L3 witness (40 actions): completed; all 3 notched buds bloomed;
  level idx 2 reached the win condition with 60 steps remaining. ✓
