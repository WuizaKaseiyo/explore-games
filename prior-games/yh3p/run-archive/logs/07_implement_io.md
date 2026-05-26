# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (v2): the 9-section spec to implement.
- workspace/critique-pass.md: confirmation spec is ready.
- skills/code/universal-scaffold.md: file structure + camera viewport rule + style rules.
- skills/code/novaengine-api.md: API signatures.
- skills/global/* (paths, action-enum, color-legend).
- Reference source files (cn04, sp80, wa30, tu93, vc33) read in #01.

## Deliverables Produced
- prior-games/yh3p/yh3p.py: 411-line implementation.
- prior-games/yh3p/metadata.json: schema-compliant metadata.
- workspace/implement-summary.md: paths, line count, plain-English mechanic summary, verification log.

## Notes
- Spec compliance: 8 sprites, 3 levels, action subset [1,2,3,4,5,6], grid_size=64×64, cell-stride=4. Step budgets 24/50/100. Bud rotations 180/270/0 for buds P/Q/R.
- One mid-implementation bug found and fixed: post-`super().__init__()` attribute assignments in `__init__` were overwriting state set by on_set_level (which fires during super-init). Moved attribute defaults BEFORE super().__init__(); on_set_level now correctly populates the live state.
- Smoke test executed all three witness routes via `perform_action` calls. L1 witness=12 actions, L2 witness=29, L3 witness=40. All three levels advance correctly.
- L3 final state: tip ends at (48, 48) (bud R cell) with facing=None (post-bloom dormancy), 60/100 budget remaining, level_index=2. The engine's last-level handling on _check_win→next_level is its concern.
- __pycache__ cleaned up.
