# Step #06: smoke_test

## Inputs Consumed
- prior-games/mr5q/mr5q.py (from #05)
- prior-games/mr5q/metadata.json (from #05)
- mechanic-spec.md (for the visual-sanity comparison and custom-check authoring guidance)
- skills/code/smoke-test-checks.md (the 9 universal checks + custom-check template)

## Deliverables Produced
- workspace/smoke-test-custom.py (4 custom checks, all PASS):
  1. check_click_flips_polarity — ACTION6 toggles polarity bit
  2. check_tick_moves_attracted_pair — ACTION5 moves opposite-state pawns toward each other
  3. check_discharge_at_adjacency — flip + ticks discharges opposite-state pair within Cheb-distance ≤ PAWN_SIZE
  4. check_action_counter_increments — engine action counter advances on each step()
- workspace/smoke-test-universal.py (programmatic universal checks 1-8, all PASS)
- workspace/render-frames.py (renders the 3 level-1-frames to PNG)
- workspace/smoke-frames/level_{1,2,3}.png (rendered initial frames for visual sanity check)
- workspace/smoke-test-pass.md (final report — all 9 universal + 4 custom checks PASS)

## Notes
- Discovered and fixed two implementation issues during the smoke pass:
  1. L1 originally oscillated due to BFS goal-cell tie-break; fixed by orienting BFS expansion order toward the dominant axis from source-to-target so the chosen first step prefers the dominant axis when multiple shortest paths exist.
  2. L3 wall gaps were originally 1 cell wide (impassable for 4-cell pawns); fixed by widening the y=10 wall gap to 4 cells and centring the flip-pad on the unique pawn-position that fits in the gap (3, 10).
- Removed the third (purple) colour group from L3 to avoid pawn-vs-pawn deadlocks that occurred when 6 pawns of 3 colour groups crowded the 16×16 grid; L3 retains 2 colour groups (green + orange), keeping the colour-key mechanic load-bearing.
- Discharge predicate uses Chebyshev distance ≤ PAWN_SIZE (covers both edge-touching and corner-touching), which is more forgiving than strict axis-aligned distance and makes the mechanic robust to BFS path choices.
- All universal checks 1-8 produced PASS-equivalent values. Visual sanity for all 3 levels also PASS.
- Visit count: 1/3.
