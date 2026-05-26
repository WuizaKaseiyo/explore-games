# Step #08: smoke_test

## Inputs Consumed
- prior-games/jd4q/jd4q.py (from #07 implement)
- workspace/mechanic-spec.md (witnesses to replay)
- skills/code/smoke-test-checks.md (test catalogue + thresholds)

## Deliverables Produced
- `workspace/smoke-test-pass.md`: 10 universal + 4 custom checks all PASS.
- `workspace/smoke-test-custom.py`: 4 custom-check functions.
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames.

## Notes
All 10 universal checks pass:
- Camera viewport 64×64 matches `(64,64)` `grid_size` for every level.
- Each level renders 6/9/12 distinct non-letterbox palette values (≥2 threshold).
- All 5 declared actions (1,2,3,4,6) are referenced in source.
- All 5 actions run without exception; `_action_count` advances 0→1.
- Palette range [0, 15] every level.
- `self.next_level()` and `self.lose()` both present.
- Per-level camera resize present (defensive; all levels share 64×64 so no-op).
- Witness for each level wins: L1 (11) → score 0→1; L2 (25) → 1→2; L3 (32) → WIN.
- Visual sanity inspection confirms rendered initial frames match the spec for each level (sprite count, placement, HUD presence, no rendering bugs).

Custom checks (4):
- ACTION4 moves avatar +4 px east at L1.
- Engine action counter increments by 1.
- One walk in L2 deposits exactly 1 echo.
- One walk in L1 deposits 0 echoes (echoes_active=False).

Transitioning to finalize.
