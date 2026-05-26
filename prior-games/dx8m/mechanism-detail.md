# dx8m — local-invariant-balance

## Skeleton labels

```yaml
primary_skeleton: spatial-constraint
secondary_skeleton: classification-sorting
interaction_type: click
state_model: constraint-counters
objective_shape: satisfy-constraints
family_class: constraint-satisfaction
```

## Summary

A grid of toggleable cells overlaid with several "region badges" — each badge defines a set of member cells with a visible count invariant (encoded as a dot pattern in the badge: 1 dot = require 1 on, 2 dots = require 2 on, etc.). The player clicks cells via ACTION6 to toggle them on/off. Cells may belong to multiple regions; a single click can affect counts in multiple regions simultaneously. Win condition: every region's count invariant is simultaneously satisfied. L1 introduces independent regions (single-region count puzzle). L2 introduces overlap (cells shared between two regions, requiring an assignment that satisfies both at once). L3 introduces a reference region whose required count is dynamically computed from the on-counts of two other regions.

## Action mapping

| Action | Semantic |
|---|---|
| ACTION6 | Click at display pixel; converted to grid cell; if cell is a region member, toggle on/off |
| ACTION4 | No-op (declared so trivial-heuristic gate's `[ACTION4 × N]` sequence is a valid input that effectively does nothing) |

`available_actions = [4, 6]`. ACTION1, 2, 3, 5, 7 unused.

## Per-level mechanic progression

| Level | Mechanic | Specific challenge / witness |
|---|---|---|
| 1 | M1: count invariant | 8×8 grid; 2 disjoint regions (A: 3 cells require 2 on; B: 2 cells require 1 on). Witness: click 3 cells (2 in A, 1 in B). |
| 2 | M2: overlapping regions | 10×10 grid; 2 regions sharing 2 cells; (A: 5 cells require 3 on; B: 5 cells require 3 on; share (4,1) and (5,1)). Witness: 4 clicks using overlap cells to count for both regions simultaneously. |
| 3 | M3: reference invariant | 12×12 grid; 3 regions (A: 4 cells require 2; B: 4 cells require 2; C: 5 cells require count = on(A) + on(B), i.e. dynamic). Witness: 8 clicks (2 in A, 2 in B, 4 in C since C requires 2+2=4). |

## Win condition

`all(region.on_count == region.required_count for region in regions)`. For reference regions (L3 region C), `required_count` is computed dynamically from referenced regions' on-counts.

## Lose condition

`self._steps_used >= self._max_steps`. Per-level: L1=20, L2=40, L3=60.

## Internal state

- `self._steps_used`, `self._max_steps`
- Cell on/off state stored in each cell Sprite's `pixels` (toggling between CELL_ON_PIXELS and CELL_OFF_PIXELS)
- `LEVEL_REGIONS` constant: per-level list of region dicts with `members` and either `count` (fixed) or `ref` (reference)

## Notable code patterns

- **Cell-state via pixel-array swap**: each cell sprite is 4×4; toggling between off (palette 4 fill + 1 hollow) and on (palette 14 fill + 0 highlight) via `cell.pixels = np.array(NEW_PIXELS, dtype=np.int16)`. Avoids two-sprite swap idiom; uses pixel mutation directly.
- **Region invariant check**: `_is_region_satisfied(region, regions)` computes `_region_on_count(region) == _region_required(region, regions)`. The `regions` list is passed so reference regions can look up their referenced regions.
- **Satisfaction indicator HUD-via-sprite**: each region has an associated `sat_indicator` sprite (3×3 green ring); after every cell toggle, `_refresh_satisfaction()` toggles each indicator's `interaction` mode (TANGIBLE if region satisfied, REMOVED if not). This is the visual feedback that solves item 19 (no hidden state for satisfaction).
- **ACTION4 as testable no-op**: declaring ACTION4 in `available_actions` and handling it as a no-op (just increments step counter) lets the smoke test's CHECK_TRIVIAL_FAILS run a trivial sequence without invalid-action errors. This pattern keeps the trivial-heuristic gate operational even for click-only games.
- **NEW: skeleton-diversity gate forced this design**: at run time, recent-5 skeletons banned `symbolic-rewrite` (cy3k), `topology-transform` (tw94), `multi-actor-coordination` (vy3m), `object-placement` (ej4t), `global-field-update` (tg6w). dx8m's `spatial-constraint` was selected from the available pool. Gate working as designed.
