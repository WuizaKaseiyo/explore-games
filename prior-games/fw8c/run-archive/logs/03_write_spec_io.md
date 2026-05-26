# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): ID fw8c, family pigment-mix-walk, novelty rationale, palette signature, 8-state mixing table.
- skills/code/spec-template.md (from study): 9-section spec template.
- skills/code/universal-scaffold.md (from study): file structure, sprite naming, camera viewport rule.
- skills/code/novaengine-api.md (from study): API cheatsheet (Sprite, Level, Camera, NovaBaseGame).
- skills/code/id-generation.md (from study): 4-char ID rules.
- skills/global/action-enum.md (from study): action slot semantics, ACTION7 strict-undo.
- skills/global/color-legend.md (from study): palette 0..15 mapping.
- skills/design-constraints/composition-and-tutorial.md (from study): exactly-3-levels rule, +1-or-+2 mechanics per level promotion.
- skills/design-constraints/difficulty-rules.md (from study): per-level (a)/(b)/(c)/(d) sub-bullets.
- skills/design-constraints/checklist.md (from study): items 1..22.
- skills/design-constraints/forbidden-elements.md (from study).
- skills/mechanic-novelty/* (from study): similarity + negative-similarity procedures.
- skills/mechanism-details/ls20.md, hr8q.md, tm5x.md, pk4m.md (re-read for novelty articulation): closest priors.
- prior-games/index.md (66 entries): full corpus reviewed for novelty.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for fw8c covering title, mechanic family, sprite roster (carrier, 3 pads, 7 slots, slot_consumed, wall_block, step_counter_hud), 3-level progression with witness solutions per level, action mapping ([1,2,3,4] only), HUD/state, win/lose conditions, novelty note. Mechanic counts: L1=1, L2=3 (M1+M2+M3 reset), L3=4 (M1+M2+M3+M4 triple-mix). Pure-arrow game; ACTION5/6/7 deliberately not exposed to avoid hidden-mechanic violation.

## Notes
- Self-flagged TWO concerns I expect critique_spec to catch:
    1. L3 §c (planning depth) — I could not construct a watertight "named greedy heuristic that fails" within the layout I committed; the greedy nearest-slot heuristic completes in ~27 actions vs. witness 29. This violates difficulty-rules.md § 2c L3's strict reading. Will need re-design in revision.
    2. L2 M3 (post-consume reset) is "weakly required" — the witness depends on it for path planning but the same end-state could be reached via idempotent OR. critique_spec checklist item 12 may flag this as not strictly counterfactually necessary.
- L2 had to revise the witness during write to avoid having pad_orange on the column-1 path between (1,1) and slot_pink at (1,5); resolved by routing column-1-down for the slot_pink delivery, picking up pink via column-4.
- L3 originally proposed 5 mechanics including ACTION5 manual purge as M5; the strict-counterfactual-necessity test (checklist item 12) failed for M5 in the chosen geometry, AND exposing ACTION5 in available_actions without witness-use would fire checklist item 11's hidden-mechanic flag. Resolved by NOT exposing ACTION5 — the pure-arrow action set is [1,2,3,4]. L3 mechanic count drops to 4 (= L2's 3 + 1), within the +1-or-+2 rule.
- ACTION7 NOT exposed (no undo) per action-enum.md strict rule.
