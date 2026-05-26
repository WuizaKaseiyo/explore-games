# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (rev 2): full 9-section spec.
- skills/code/universal-scaffold.md: file structure, naming, camera viewport rule.
- skills/code/novaengine-api.md: API cheatsheet.
- skills/code/id-generation.md: ID rules.
- Reference source cn04.py (re-skimmed): structure (sprites dict at top, levels list, BG/PADDING constants, RenderableUserDisplay class, NovaBaseGame subclass with on_set_level/step/_get_hidden_state/_get_valid_actions).

## Deliverables Produced
- prior-games/fw8c/fw8c.py (495 lines): Pascal class `Fw8c(NovaBaseGame)`, sprite bank with carrier + 3 pads + 7 slots + slot_consumed + 3 doors (only door_green used at L3) + wall_block. Levels list with 3 entries. StepCounterHud RenderableUserDisplay. Cell stride STEP_SIZE=8 with 1-pixel SPRITE_INSET. 8-state mixing table (scrambled cultural intuition). All meaningful semantic names; no obfuscation.
- prior-games/fw8c/metadata.json: schema-conformant {game_id, title, default_fps, tags, baseline_actions, local_dir, date_generated}.

## Notes
- `python -c "import ast; ast.parse(...)"` passed.
- Runtime smoke `Fw8c()` instantiated; reports 3 levels, available_actions=[1,2,3,4], L1 grid_size (64,64), 31 sprites in L1.
- Implementation choices not in spec but consistent with it:
    - Sprite layer order: carrier=2 (top), doors=1, slots/pads/walls=0. Ensures carrier renders on top of consumed-slot replacements.
    - Border walls placed via `_border_walls()` helper at all 8 perimeter cells of the 8x8 logical grid; interior walls for L3 added explicitly at row y=4 cells {1,2,3,5,6}.
    - L3 layout includes a SECOND `pad_pink` instance at cell (3,6) downstairs (per spec rev 2's amendment 2c) so the carrier can re-acquire pink without re-crossing the door.
    - Slot consumption is implemented as set_interaction(REMOVED) on the original slot + add a slot_consumed sprite at the same position. The check `_check_win` filters by interaction != REMOVED so consumed slots count as won.
    - Door state toggle: each step's `_update_doors()` walks all `door`-tagged sprites and sets interaction REMOVED if pigment set matches, else TANGIBLE. Called both before move (to evaluate passability) and after pickups (to refresh for next turn).
    - Step counter pattern matches cn04: `_action_count` + `_budget` from level_data; HUD shows remaining count.
- Cleaning __pycache__ done.
EOF
echo "logged"