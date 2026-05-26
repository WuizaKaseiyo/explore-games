# Step #08: smoke_test (visit 1)

## Inputs Consumed
- `prior-games/qm4t/qm4t.py` (the implementation).
- `prior-games/qm4t/metadata.json`.
- `mechanic-spec.md` v3 (for witness extraction and visual-sanity reference).
- `skills/code/smoke-test-checks.md`.

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 4 custom checks (post-place,
  zero-post-noop, enclosed-capture, strike-on-maroon).
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames.
- `workspace/smoke-test-pass.md`: aggregate verdict — every check PASS.

## Notes
- One iteration of the strike-on-maroon custom check used coords with y=3,
  which falls in the HUD band — the click was rejected by `_is_in_playfield`.
  Fixed by moving vertices to y >= 4. After the fix all 4 custom checks pass.
- The visual-sanity pass confirms the spec's described layouts on all 3
  levels. The patroller in particular renders distinctly from critters
  thanks to its single-eye tapered-diamond shape — no risk of confusion.
