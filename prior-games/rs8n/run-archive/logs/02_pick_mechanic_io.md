# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (run input: no seed → autonomous mode)
- skills/mechanic-novelty/* (taxonomy, similarity, negative-similarity, prior-games-format)
- skills/design-constraints/* (priors, forbidden, composition+tutorial, difficulty, checklist)
- skills/global/action-enum.md, color-legend.md
- skills/code/id-generation.md
- skills/mechanism-details/* (all 25 reference summaries — already internalised in study)
- prior-games/index.md (45 prior games — full list)
- L1 screenshots opened for negative-similarity: r11l, su15, vt6q (closest "fire-something-linear-from-pawn" priors)

## Deliverables Produced
- mechanic-pick.md: ID `rs8n`, family `line-reverse-sweep`, full positive + negative similarity tables, distinguishing rules for 3 taxonomy near-misses (lp85, r11l, vc33) + 3 prior-games near-misses (qn7w, vt6q, qx7p). Verdict NOVEL.

## Notes
- Considered 90+ candidate mechanics; many were rejected on visual/verb overlap with priors. Final pick is line-segment-reversal (essentially the pancake-sort move) on a 2D arena with a walking avatar that fires sweeps in its facing direction. No prior implements segment-reversal as a primary verb.
- Pivoted from a row-centric framing (rejected against vc33 — too many shared dimensions) to a 2D-arena framing where the sweep line is freely chosen at fire-time by avatar position + facing. This drops shared dimensions vs vc33 from 5 to ~1.
- Action subset [1,2,3,4,5]; distinctive verb on ACTION5 (the freedom slot), per the canonical pattern in `action-enum.md`.
- L1/L2/L3 plan: walk+sweep → +anchor → +shifter. Each level's witness will require all carried-forward + newly-introduced mechanics together.

