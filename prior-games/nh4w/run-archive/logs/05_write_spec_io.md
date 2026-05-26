# Step #05: write_spec (round 2)

## Inputs Consumed
- workspace/critique-revisions.md (6 issues from round-1 critique)
- workspace/mechanic-spec.md (round-1 spec, to be rewritten)
- skills/code/spec-template.md
- skills/design-constraints/{checklist, difficulty-rules, composition-and-tutorial, core-knowledge-priors, forbidden-elements}

## Deliverables Produced
- workspace/mechanic-spec.md (REPLACED): full 9-section spec, round 2.
  - §4 rewritten cleanly with locked final geometry and explicit floor()-rounding altitude formula.
  - L1: launcher x=4, target_yellow at (56, 51) (centre x=58); witness `[ACTION4, ACTION6@(56, 51)]` (2 actions); step budget 15.
  - L2: launcher x=4, wall_h11 at (24, 40), target_yellow at (60, 51) (centre x=62); witness `[ACTION4, ACTION4, ACTION6@(62, 51)]` (3 actions); step budget 25.
  - L3: launcher x=4, wall_h8 at (24, 43), ceiling_c5 at (8, 0), ceiling_c13 at (32, 0), target_yellow at (40, 51), target_blue at (52, 51); witness `[ACTION4, ACTION6@(40, 51), ACTION4, ACTION6@(52, 51)]` (4 actions); step budget 35.
  - All counterfactual necessity claims for each (mechanic, level) pair re-derived with explicit floor() arithmetic; verified that the witness positions are UNIQUE under the wall+ceiling+range constraints.
  - Max horizontal range fixed at 48 px globally.
  - Sprite roster: floor (decorative), launcher (5×5 with upward muzzle), projectile (3×3 yellow ball), wall_h8/h11/h12 (brick walls), ceiling_c5/c13 (tapered grey stalactites with maroon tip), target_yellow/blue (4×4 hollow squares), StepBarHud.
  - Action mapping: `[3, 4, 6]` minimal subset, ACTION7 omitted.
  - Win/lose predicates testable, no-hidden-state visible.

## Notes
- Round-2 spec includes a "Changes from round 1" header summarising deltas vs round-1 — addresses critique recommendation to mark which sections changed.
- §4's per-level arithmetic explicitly verifies that yellow only fires from x=8 and blue only fires from x=12 in L3, by enumerating each candidate launcher position and showing its blocking constraint (ceiling1 / wall / ceiling2). This concretely satisfies checklist item 12's "verify by enumeration, not by abstraction" requirement.
- §9 novelty section unchanged — round-1 critique found no novelty issues.
- Open implementation questions (for `implement` state):
  - Pre-compute the flight path during the click handler vs frame-by-frame? Pre-compute is simpler and supports the per-frame collision check naturally.
  - Stalactite sprite construction: helper function `make_stalactite(clearance: int) -> Sprite` that builds a tapered shape of height `(50 - clearance + 1)` with the documented top-down pattern.
  - Projectile-fizzles UX: should the projectile disappear instantly on collision, or should it briefly flash at the collision cell? A 1-frame flash gives clearer feedback. Decide at implement time.
  - Whether a faint "trajectory preview" line should be drawn before the player clicks, to help reading the arc shape: NO — that would give away the mechanic without exploration. Player must learn the arc shape by firing.
