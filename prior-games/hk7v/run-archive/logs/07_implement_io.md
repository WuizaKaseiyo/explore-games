# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (carried)
- critique-pass.md (carried)
- skills/code/universal-scaffold.md (carried)
- skills/code/novaengine-api.md (carried)

## Deliverables Produced
- prior-games/hk7v/hk7v.py (449 lines)
- prior-games/hk7v/metadata.json
- implement-summary.md (next file)

## Notes
- ast.parse OK; runtime instantiation OK; on_set_level invoked on
  level 0 finds 1 block + 1 target + 0 walls (correct L1 setup).
- L1 witness simulated in-process: 14 right + 41 lower + grab + 30
  right + release → block_red at (44, 53), check_win True.
- L2 witness simulated: 4 right + 41 lower + grab + 38 raise + 40
  right (carries past wall above row 20, hook.y=11, carry.y=15) +
  release + 8 right + 38 lower + grab + 6 right + release →
  block_red at (44, 53), block_blue at (58, 53), check_win True.
- L3 witness simulated: yellow → blue → red in stack-disassembly
  order, all delivered correctly, check_win True at end.
- pycache cleaned.
