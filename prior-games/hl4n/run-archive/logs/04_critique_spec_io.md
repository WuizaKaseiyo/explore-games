# Step #04: critique_spec

## Inputs Consumed
- task-overview.md, states/critique_spec.md.
- mechanic-spec.md (under review).
- mechanic-pick.md (cross-reference for novelty restatement).
- skills/design-constraints/checklist.md (22 items walked).
- skills/design-constraints/{difficulty-rules, composition-and-tutorial, core-knowledge-priors, forbidden-elements}.md.
- skills/mechanic-novelty/{similarity-check, negative-similarity-check, taxonomy-of-25-games, prior-games-index-format}.md.
- skills/global/{action-enum, color-legend}.md.
- prior-games/index.md (re-confirmed 60 entries, none collide on the row-col-tint-cross dynamic).
- All 25 mechanism-details summaries (re-applied for novelty review without re-reading; relied on memory from study).

## Deliverables Produced
- `critique-pass.md`: 22-item checklist verdict + novelty + negative-similarity verdict, all PASS. Per-mechanic counterfactual table (item 12) covers all 6 mechanic-level rows (L1×1, L2×2, L3×3), with concrete blocking arguments and an independent enumeration of plausible alternate strategies (row-only, column-only, ignore-M3, spam-clicks) for each level.

## Notes
- The L3 design *required* explicit verification that M3 (brighter-wins) is necessary — the spec's first L3 lock-placement attempt was column-only-solvable, and only the 7th lock (Lock G at `(2,3)` requiring 14, sharing column 2 with Lock C at `(2,6)` requiring 8) forces the row-dominates-column path. The critique re-derived this and confirmed Lock G's necessity by walking the column-only attempt and showing where it breaks.
- Two design tensions noted but neither is a violation:
  1. *Cells are flat 6×6 fills* — necessary because their job is to display a tint cleanly, but flagged in item 20. ft09's 16×16 grid of 4×4 cells is the precedent — flat cells are acceptable when their role is "display a single color value". The surrounding markers and lock-target rings carry the rich pixel detail.
  2. *L3 brighter-wins rule discoverability* — the cell-color rule changes from L2 to L3 (override → brighter-wins), which the player learns only by playing L3. The cue is observable (clicking a column in L3 may not change the cell's color when the row is brighter), and the rule is inferable in 2-3 clicks. Acceptable per item 21's "guessable after a small number of exploratory actions".
- ID: `hl4n`. Action subset: `[6]`. Three levels with 30 / 60 / 80 step budgets and 6 / 10 / 15 witness clicks.
- Verdict: PASS. Transition to `implement`.
