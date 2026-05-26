# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness): autonomous-mode policy (no seed)
- states/pick_mechanic.md (from harness): description + transition
- skills/global, skills/design-constraints, skills/mechanic-novelty (from harness): inherited from #01 study
- skills/code/id-generation.md (from harness): ID procedure & reserved 25
- prior-games/index.md (read in #01): 75+ entries plus header
- Listed reserved 25 reference IDs (in id-generation.md)
- Mechanism-detail summaries (read in #01) for the 25 reference games; used for similarity-check
- Sampled L1 screenshots (cn04, tu93, sp80) from study; used to ground "visual signature" dimension of negative-similarity-check

## Deliverables Produced
- mechanic-pick.md: chosen 4-char ID `kg7p`, mechanic family `beam-tether-haul`, one-paragraph description with L1/L2/L3 mechanic layering, taxonomy + prior-games similarity check, negative-similarity walk against `wa30` (the strongest near-miss).

## Notes
- Initially considered "plank-bridge-walk", but `kj82 plank-pivot-walk` in priors creates risk of "plank" sprite-grain overlap.
- Settled on `beam-tether-haul`: directional sticky beam from avatar's facing direction; couples haulable blocks 1-for-1 with avatar walks; ACTION5 toggles beam.
- L1=walk+beam-couple-haul (2 mechanics); L2 adds barriers passable to avatar but not blocks (3 mechanics); L3 adds direction-locked blocks (4 mechanics). Composition rule honoured (+1 per level).
- ACTION subset `[1,2,3,4,5]` — no click, no undo. ACTION5 = beam-toggle (the distinctive verb).
- Closest priors: wa30 (carry-pickup-drop), kn58 (anchor-pull-magnet), vt6q (grapple-anchor-yank), hk7v (overhead-trolley-hook). Distinguishing rules articulated per row.
- Negative similarity vs wa30: ~2 substantive shared dimensions (verb structure, cargo-deliver framing). Below 3+ rejection threshold; core-dynamic divergence is concrete.
