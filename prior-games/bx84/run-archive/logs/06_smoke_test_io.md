# Step #06: smoke_test

## Inputs Consumed
- prior-games/bx84/bx84.py (the just-generated game)
- prior-games/bx84/metadata.json
- workspace/mechanic-spec.md (for visual-sanity comparison)
- workspace/critique-pass.md
- skills/code/smoke-test-checks.md (universal checks template + custom-check constraints + visual-sanity protocol)

## Deliverables Produced
- workspace/smoke-test-custom.py — 4 custom checks (`check_l1_minimal_solve`, `check_click_empty_places_mirror`, `check_filter_recolours_beam`, `check_prism_toggle_changes_branch`).
- workspace/smoke-test-pass.md — full PASS report, all 9 universal + 4 custom = 13 checks pass.
- workspace/smoke-frames/level_{1,2,3}.png — rendered initial frames per level (used for the vision pass).

## Notes
- Visit count: 1/6. First-attempt pass.
- All 9 universal checks pass; the source already implemented the camera-viewport resize in `on_set_level` (even though all levels share grid_size 16×16, the resize line is harmless).
- The visual-sanity pass per level confirmed the rendered initial frames match the spec's described sprite roster, placement, and HUD presence. Minor cosmetic note for L2: the filter sprite (1×1 palette-9) is visually subsumed into the post-filter blue beam on the same row, so the player perceives the filter as "the cell where yellow becomes blue" rather than as a distinct object. This is acceptable per the spec — the recolouring is the discoverable mechanic, not the filter sprite shape per se.
