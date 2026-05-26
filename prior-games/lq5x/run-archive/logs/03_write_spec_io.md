# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): family `lantern-cone-illuminate`, ID `lq5x`, action set `[1,2,3,4,5]`, level progression sketch.
- workspace/study-notes.md (from #01 study): cross-cut design moves and anti-patterns.
- skills/code/spec-template.md: 9-section structure.
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md: scaffold + API + ID rules.
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements}.md.
- skills/global/{action-enum,color-legend,paths}.md: palette + action-set conventions.
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games}.md.

## Deliverables Produced
- workspace/mechanic-spec.md: The full 9-section spec. Contains §1 title, §2 mechanic family + prior categories, §3 sprite roster (6 sprites + ConeOverlay HUD note), §4 level progression (L1 12×12, L2 14×14, L3 14×14) with explicit witness solutions per level (5/10/10 actions) AND difficulty justifications (random-resistance, human-tractable, planning depth) AND L1 walk-only refutation, L2 walk-no-wax refutation, L3 strict adjacent-action commute that breaks solvability, §5 action mapping (5 actions, no gating), §6 HUD + per-game state (StepCounterHud, ConeOverlay), §7 win predicate, §8 lose predicate, §9 novelty note re-grounded against taxonomy + priors + manual-axis (vs preexisting games).

## Notes
- **Mechanic count contract**: L1 N=2 (walk + cone-rotate), L2 N+1=3 (adds wax pickup), L3 N+2=4 (adds filter-cone-colour). Each new mechanic enters the game at exactly one level promotion; no mechanic drops out. Every mechanic at every level is exercised by that level's witness AND strictly required by the step budget.
- **Strict adjacent-commute for L3** (the load-bearing checklist-16 requirement): swapping witness steps 2 and 3 (walk RIGHT then walk LEFT vs walk LEFT then walk RIGHT) prevents Y1 from being lit during the only window when the cone is yellow; subsequent step 7 turns the cone red permanently (no yellow filter exists in L3 to revert), so Y1 (yellow) becomes unlightable and the level is unsolvable.
- **No walls in any level** — kept the geometry open to bound implementation complexity. The puzzle pressure comes from R limits, cone-direction constraints, filter-state irreversibility, and tight step budgets.
- **Cone shape**: width 3 cells × depth R cells, projected from the lantern in the facing direction; out-of-bound cells are dropped. Filter activation is positional — if any filter cell is in the cone after an action, `cone_color` updates to that filter's colour. Multiple-filter ties broken by Manhattan distance, then sprite-list order, for full determinism.
- **Cone rendering** via a `ConeOverlay(RenderableUserDisplay)` widget that paints background-coloured cells inside the cone to a "lit" palette (off-white when cone yellow; maroon when cone red), so the cone is visible at a glance and other sprites (lantern, targets, filters, pickups) remain visible inside it.
- The transition condition for `critique_spec` (9 sections present, §4 has per-level mechanic enumeration + witness + difficulty justification, action mapping concrete, win/lose testable predicates) is satisfied. Proceeding.
