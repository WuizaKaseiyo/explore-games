# Implement summary — rs8n (revision 4)

## Files written
- `prior-games/rs8n/rs8n.py` (654 lines)
- `prior-games/rs8n/metadata.json`

## Plain-English rule (no cell-level coordinates)
A maroon avatar walks a 16-cell-square arena scattered with coloured shape items. Arrow keys rotate the avatar to face that direction and walk one cell when open. Pressing the freedom-slot action fires a sweeper in the avatar's facing direction; the sweeper picks up every item along that cardinal line until it hits a wall or anchor pillar, then returns and re-deposits the carried items at the cells they came from, in reversed pickup-order. Anchor pillars halt sweeps mid-line; access-blocking walls flank each anchor cell so the anchor cell is unreachable for the avatar, making the anchor's stop-effect strictly necessary for the per-segment-reversed target permutation. Higher levels add a second anchored line in the perpendicular axis. The level wins when every cell with a target imprint holds the matching shape and colour.

## Changes vs. prior implementation
- Dropped the `shifter_green` and `preview_green_ring` sprites and all shifter detection / `SHIFTER_PALETTE` constants.
- Dropped the `_recolor` helper (now unused).
- L2 now places anchor at (5,8) with access-blocking walls at (5,7) and (5,9); the target is **both segments reversed** (4 targets, not 5).
- L3 (revision 4) is now a single 3-row × 5-column grid at rows 4..6, cols 5..9 with 14 items + 1 anchor at the centre cell (7,5). No L3 access-walls: the grid's own packed geometry blocks the avatar from the anchor cell (every cardinal neighbour is an item). The L3 target has **14 entries** (every non-anchor grid cell). Target permutation: full-column reverses on cols 5/6/8/9 + both row-5 segment-reverses. Preview rendered as a matching 3×5 grid three rows below the playable grid.
- Budgets: L1 50 (unchanged), L2 70 → 100, L3 120 → 250.

## Smoke-test result
- Syntax (ast.parse): OK.
- Instantiation: OK; level count = 3; available_actions = [1,2,3,4,5]; grid_size = (64,64) per level.
- Full L1 → L2 → L3 witness sequence (3 + 15 + 31 = 49 actions total): game terminates with `state == GameState.WIN`, `score == 3`. Budget consumed: 3 / 50 (L1); 15 / 100 (L2); 31 / 250 (L3). Cushions: 17×, 6.7×, 8×.
- L3 witness sweep order (6 sweeps): col 5 south → row 5 west → col 6 south → col 8 south → col 9 south → row 5 east. Column 7 intentionally never swept (the anchor splits it into single-cell segments where reversal is a no-op; the target leaves (7,4) and (7,6) at initial values).
