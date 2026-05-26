# Game generation final report — Run #5

## Generated game

- **ID**: dx8m
- **Class**: `Dx8m`
- **Source**: `prior-games/dx8m/dx8m.py`
- **Metadata**: `prior-games/dx8m/metadata.json`
- **Lines of code**: ~290

## Mechanic

A grid of toggleable cells overlaid with region badges that visibly encode count invariants (e.g., "exactly 2 cells of this region must be on"). Player clicks cells (ACTION6) to toggle them on/off. Cells may belong to overlapping regions, so one click can affect multiple regions at once. Win = all region invariants simultaneously satisfied. L1 has disjoint regions (basic count). L2 overlaps two regions (forcing the player to find a shared-cell assignment satisfying both). L3 introduces a reference region whose required count is computed dynamically from the on-counts of two other regions, requiring cross-region planning.

## Skeleton-diversity verdict

| label | value |
|---|---|
| primary_skeleton | spatial-constraint |
| secondary_skeleton | classification-sorting |
| interaction_type | click |
| state_model | constraint-counters |
| objective_shape | satisfy-constraints |

**Gate result**: PASS. Recent-5 skeletons (cy3k=symbolic-rewrite, tw94=topology-transform, vy3m=multi-actor, ej4t=object-placement, tg6w=global-field-update) are all distinct from `spatial-constraint`. spatial-constraint count in corpus = 2 (qz73, lv4k); not high-frequency.

## Smoke test results

```
13 PASS, 0 FAIL, 1 SKIPPED

✅ CHECK_CAMERA_VIEWPORT
✅ CHECK_SPRITE_CONTENT
✅ CHECK_ACTION_BRANCHES
✅ CHECK_ACTION_RUNTIME
✅ CHECK_PALETTE_RANGE
✅ CHECK_WIN_PATH_EXISTS
✅ CHECK_WITNESS_WINS  (L1 3 clicks; L2 4 clicks; L3 8 clicks → WIN)
✅ CHECK_TRIVIAL_FAILS  ([ACTION4 × N] never toggles cells; never wins)
✅ CHECK_LOSE_PATH_EXISTS
✅ CHECK_CAMERA_DEFAULT
✅ CHECK_CLASS_NAME_LOADER
✅ custom_click_toggles_cell
✅ custom_l3_reference_invariant  (verifies dynamic count: A=0+B=0 → C requires 0; A=1+B=0 → C requires 1)
⏭️ CHECK_VISUAL_SANITY (manual)
```

## Lessons applied from cy3k post-mortem

- **Visual richness (item 20)**: cells are 4×4 sprites with internal pattern (palette 4 fill + 1 hollow when off; palette 14 fill + 0 highlight when on) rather than 1×1 chunks scaling to crude blocks. Region badges 5×5 with dot-pattern indicators.
- **Strict counterfactual (item 12)**: each level's witness EXERCISES the new mechanic — L2 witness uses overlap cells to satisfy both regions in fewer clicks; L3 witness's count for region C is dynamically computed from A+B's on-counts.
- **Discoverability (item 21)**: cell toggling is immediate; satisfaction_indicator sprites appear/disappear visually for each region per click. Player learns the mechanic from 1-2 exploratory clicks.
- **§3.4 ceiling**: count-constraint puzzles exist in commerce (Nonogram), but dx8m's specific overlap + reference invariant structure is not a clone of any single commercial title.

## Index update

```
| dx8m | local-invariant-balance | spatial-constraint | classification-sorting | click | constraint-counters | satisfy-constraints | Local Invariant Balance — ... | <ts> | (autonomous) |
```

## Run notes

- Inspiration: PS-004 from the user's curated `extra-mechanic-seeds.md`.
- Skeleton-diversity gate continues to enforce diversification — 2 consecutive non-walk-push games (cy3k symbolic-rewrite + dx8m spatial-constraint).
- Total run time: ~40 minutes.
