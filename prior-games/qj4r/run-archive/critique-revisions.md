# Critique revisions — round 1

## Issues

### 1. L2 M2-counterfactual fails item 12
**Section**: §4 Level 2 — Necessity per mechanic.
**Quote**: "L2 cannot be solved without triggering M2 because the trivially-tempting two-step sequence `[ACTION3, ACTION1]` (fold-left-onto-right then fold-top-onto-bottom) reflects the piece via `(1, 1) → (6, 1) → (6, 6)` *but the first fold is rejected*..."
**Problem**: Two valid 2-step witnesses exist (`[ACTION3, ACTION1]` post-correction and `[ACTION1, ACTION3]` after the obstacle re-shuffle); the obstacle's role reduces to "prune one fold ordering of two", so a winning sequence exists that never triggers M2's distinguishing rejection behavior. Per checklist 12, M2 is therefore decorative at L2.
**Fix**: Pick a level setup where M2's rejection is unavoidable on every winning sequence — e.g., place the obstacle on the *only* cell every winning permutation must cross, OR redesign so the M2 mechanic IS the witness's trigger (the fold the witness MUST attempt is the M2-validated one, and ANY untouched would-be alternative gets rejected).

### 2. L3 witness math is unverified and the geometry is fragile
**Section**: §4 Level 3 — Witness solution.
**Quote**: "The witness's specific 4-fold sequence below sequences fold directions to keep all pieces' destinations off `(5, 4)`; ... the sequence: ACTION3 reflects orange1 `(1,1)→(6,1)` and purple `(1,6)→(6,6)`; orange2 `(2,1)→(5,1)` (ACTION3 keeps right) ..."
**Problem**: The witness was hand-waved without a complete cell-by-cell trace; on attempted verification, the obstacle's reflected cell coincides with the target's cell, triggering M2-rejection on subsequent folds. The spec admits "finalised in the implementation phase against the actual semantics", which is unacceptable for a critique-passable spec.
**Fix**: Walk the witness step-by-step with concrete pre/post cells for every sprite, verify M2 is not violated at any step, verify M3 (merge) is triggered by an explicit same-cell coincidence, verify the win predicate fires after the final action.

### 3. Obstacle reflection semantics are inconsistent
**Section**: §4 Level 2 — Witness re-derivation; §5 Action mapping.
**Quote**: Two contradictory rules used in the same spec: "obstacles reflect with the rest of the sheet under the same M1 mirror rule" (§3 sprite roster) vs. "obstacles do not reflect" (§4 L2 witness re-derivation).
**Problem**: The witness math depends on which rule is used; unverified.
**Fix**: Pick ONE rule and apply consistently across §§3, 4, 5. Recommend: obstacles DO reflect like every other entity (uniform geometry); M2 rejects iff any *piece's* post-fold cell coincides with any *obstacle's* post-fold cell. This treats every entity uniformly under M1.

### 4. M3 (same-colour-merge) at L3 may be redundant given the natural win predicate
**Section**: §4 Level 3 — Necessity per mechanic.
**Problem**: When a piece and its same-colour target coincide, both reflect together on subsequent folds (they share a cell, so they share a reflected cell). The "merge two oranges then place" puzzle works without M3 if the win predicate accepts "any same-colour piece-count on a target ≥ 1 with all pieces on a target". The current spec's strict "piece-count == target-count per colour" predicate IS what makes M3 necessary, but this predicate is a non-obvious player-facing invariant and isn't visually communicated. Re-derive whether M3 holds counterfactual necessity under a sensible win predicate.
**Fix**: Either (a) commit to the strict count predicate AND make the visual tell match (e.g., orange target visually shows "1 piece needed" via internal pattern), or (b) drop M3 and replace with a different L3 mechanic whose distinguishing behaviour is unambiguously triggered by the witness.

### 5. Visual rendering of "active region contracts" needs concrete sprite plan
**Section**: §3 Sprite roster — `active_floor`.
**Quote**: "variable-size sprite (re-built per level) drawn at logical-cell granularity ... shrinks in `on_set_level` and after every fold."
**Problem**: novaengine `Sprite` pixels are fixed at construction; "re-build per level" suggests the implementation will create new Sprites mid-game. Need a concrete plan: do we maintain a pool of pre-built `active_floor_<W>x<H>` sprites and swap them in, or do we mutate `sprite.pixels` in place? Either is allowed by the API but the spec should specify.
**Fix**: Specify in §6 (HUD/state): the game maintains a single `active_floor` sprite whose `pixels` array is overwritten in-place via `sprite.pixels[:] = new_pattern` at each fold. The fold-seam ticks are similarly mutated.

### 6. Fold-seam tick on the *post-fold* central axis vs. pre-fold
**Section**: §3 — `fold_seam_tick`.
**Problem**: After a fold, the active region's centre shifts; the seam tick must reposition. Spec says it does, but where (which row/column) the tick actually appears is not specified.
**Fix**: Spec §6 should state: "After every fold, two `fold_seam_tick` sprites are repositioned: one horizontal at row = (active_y_min + active_y_max + 1) / 2 across active x-range; one vertical at col = (active_x_min + active_x_max + 1) / 2 across active y-range. They are INTANGIBLE."

## Recommended major restructure

Adopt a SIMPLIFIED level progression:
- **L1**: 1 orange piece, 1 orange target, no obstacles, no merge. M1 (fold) only. Witness 1 fold.
- **L2**: 2 orange pieces, 1 orange target, no obstacles. M1 + M3 (same-colour-merge). Witness 2 folds (`[ACTION3, ACTION4]`). M3 strictly necessary because piece-count-target-count predicate locks.
- **L3**: 2 orange pieces + 1 purple piece, 1 orange target + 1 purple target, ONE obstacle. M1 + M3 + M2 (obstacle-fold-rejection). Witness 3 folds. M2 strictly necessary because the obstacle is positioned so that exactly one of the two natural fold orderings is M2-rejected on the FIRST fold (forcing the witness to pick the alternative ordering that uses M2's distinguishing rejection as a player-observable signal).

The simpler progression aligns with the harness's "+1 mechanic per level" rule and avoids the L2 M2-decorative trap by deferring obstacles to L3 where they can be made unambiguously necessary.
