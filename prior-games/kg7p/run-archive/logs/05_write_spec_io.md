# Step #05: write_spec (revision pass, addressing critique-revisions.md from #04)

## Inputs Consumed
- critique-revisions.md (from #04): four issues to address (two CRITICAL, two MINOR).
- mechanic-spec.md (from #03): the prior-pass spec, edited in place.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md (from harness): unchanged guidance.
- skills/design-constraints/forbidden-elements.md (from harness): Issue #1 driver.
- skills/design-constraints/difficulty-rules.md (from harness): Issue #2 stage-conflation rule.

## Deliverables Produced
- mechanic-spec.md (revised): four changes
  1. **§3 sprite roster:** `block_directional` pixel pattern replaced — chevron arrow replaced with 2-pixel magenta edge-stripe on the haul-side edge. Palette legend updated.
  2. **§4 Level 2:** layout redesigned for forced delivery order (block_orange at (8,8) blocking block_yellow's south path); witness rewritten as 29-action orange-first trace; planning-depth (c) rewritten to name a post-discovery wrong-path ("yellow-first along straight south"); step budget reduced from 70 to 60 (still 2× witness, non-shrinking vs L1).
  3. **§6 HUD/state:** added explicit camera-viewport statement (no resize needed, grid_size = (64, 64) matches default).
  4. **§3 avatar:** left unchanged after re-checking the pixel pattern — the 4 corner black pips + green bottom-emitter does not unambiguously read as a face (Issue #4 was optional).

## Notes
- Mechanic family, action subset, level count, win/lose condition, L1, L3 — all unchanged from #03 pass.
- L2 witness now 29 actions (was 35); L2 wrong-path now post-discovery (was discovery-stage); L2 step budget 60 (was 70).
- Direction-lock visual: stripe on haul-side edge. Rotation 0 = east edge, 90 = south, 180 = west, 270 = north.
- Inner accent of `block_basic` revised to colour 4 (off-black) so block_orange and block_yellow share the same shape and differ only via their target's colour pairing. Per checklist item 21 "identical visuals imply correlated roles" — both basic blocks ARE correlated (both deliverable via the same mechanic); their pairing with specific targets is encoded by the target's distinctive inner colour, not by the block sprite. Spec §3 explicitly describes the shared visual cue between block and target.

## Visit count tracking
- write_spec entries in state_log.md so far: #03 (initial), #05 (this revision). Total = 2.
- critique_spec entries so far: #04. Total = 1. Well under cap of 10.
