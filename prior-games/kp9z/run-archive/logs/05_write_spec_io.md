# Step #05: write_spec (revision)

## Inputs Consumed
- workspace/critique-revisions.md (from #04): item 20 shape-as-meaning fix
- workspace/mechanic-spec.md (existing draft): preserved sections 1, 2, 5, 7, 8, 9 + the per-mechanic counterfactual tables in §4

## Deliverables Produced
- workspace/mechanic-spec.md (revised): §3 rewritten with 10×10 sprite
  layout, shape-distinct cell types via frame-edge notches (top notch =
  source, left notch = sink, bottom notch = redirector_south, corner
  pips = target). §4 anchor and click coords recomputed for the new
  10-stride / `grid_size=(64, 64)` layout (was `(32, 32)` with stride 6
  + 1-px gap). Witness click sequences updated.

## Notes
- Preserved per-mechanic counterfactual necessity tables — those were
  the strongest part of the original spec and §4 critique was clean on
  them.
- Preserved strict win predicate ("every cell at exact target_count").
- Reduced redirector type set from 4 directional variants to 1
  (redirector_south) since L3 is the only level using a redirector and
  only south is needed. If a future level wants other directions, the
  pattern is documented in §3 (notch on the matching frame edge).
- Verified the 10×10 sprite layout passes 2×2-pool sub-cell test:
  every shape feature (frame, pip, type-center, edge-notch) is at
  least 2 onscreen pixels in extent and survives pooling intact.
