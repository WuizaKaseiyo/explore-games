# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (from #05 write_spec, after revision): final 9-section spec with M4 = pivot-reset
- critique-pass.md (from #06 critique_spec): pass verdict
- skills/code/universal-scaffold.md (from earlier states): file structure, naming, style
- skills/code/novaengine-api.md (from this state): API reference
- skills/code/id-generation.md (from earlier): ID rules (already verified hb5n)
- .venv/.../novaengine/base_game.py (read to debug init order issue)

## Deliverables Produced
- prior-games/hb5n/hb5n.py: 471 lines, full game.
- prior-games/hb5n/metadata.json: standard metadata.
- workspace/implement-summary.md: paths, line count, plain-English summary (no cell-level coordinates).

## Notes
- Implementation uses per-cell sprites (anchor + body cells as separate Sprite instances) rather than one composite sprite. Simpler than np.rot90-based composite reconstruction; positions are updated cell-by-cell on translate / rotate / pivot-reset.
- INITIAL BUG: my __init__ assigned default state attributes AFTER super().__init__(). The base class's __init__ immediately calls set_level(0) → on_set_level, which mutated those attributes; my subsequent default assignments then OVERWROTE the on_set_level state, leaving the game in an unusable post-init state. Fixed by moving default assignments to BEFORE super().__init__() so on_set_level's per-level state survives.
- Runtime smoke test executed inline as part of this state: L1 witness (10 east + 10 south + 3 rotate) advanced to L2; L2 witness (10 east + 10 south + 2 rotate, with pickup consumed at action 2 east) advanced to L3; L3 witness (2 east + 5 east + 7 south + 1 rotate + 3 east + 2 south, with pickup consumed at action 2 east and pivot-reset consumed at action 14 south) ended with GameState.WIN, score 3.
- Edge cases verified: wall collision rejects movement (step counter still ticks); step exhaustion via 60 ACTION5 presses fires lose() → GAME_OVER.
- __pycache__ cleaned up post-test.
- Transition to smoke_test for the formal smoke harness.
