# Step #02: pick_mechanic

## Inputs Consumed
- skills/global, skills/design-constraints, skills/mechanic-novelty, skills/code (read in #01 and reapplied here)
- skills/mechanism-details/<id>.md as needed for near-miss judgement
- prior-games/index.md (36 entries) + prior-games/fb7t/ (in-flight, not yet indexed — Phase-Transition Matter)
- task-overview.md notes (autonomous mode — empty seed)

## Work

Seed: empty (autonomous mode).

Walked the taxonomy + priors corpus. Looked for axes still relatively
underrepresented in the prior-games corpus. Cumulative theme-clusters
already saturated: pawn-grid-walking (~10), click-place-commit (~5),
beam/projectile routing (~5), shift/slide (~4), pour-physics-settle
(~3), gear/cascade (~3), self-transform (~3), reach/articulation (~3),
phase-step (~2). Underrepresented: explicit *geometric reflection /
folding* across a movable axis as a discrete commit-verb. The only
reference-set game touching mirror-reflection is `ar25`
(shape-mirror-cover) and its mirror is a continuous ghost slide, not
a discrete consume-stamp fold. No prior-games entry uses fold/crease.

Picked **fold-crease-overlay**: a paper-folding mechanic where the
player commits one-shot reflections of coloured stamps across a
crease line that splits the playfield into an "active" half and a
"target" half. Each fold consumes the stamp and lays its mirror image
permanently on the target half; win = every shadow target cell ends
up covered by a same-colour folded pixel.

ID: rolled `wj7d` (not in 25 reference, not in prior-games index, not
a recognisable English word, not in prior-games directory listing).

## Deliverables Produced
- mechanic-pick.md: 4-char ID `wj7d`, mechanic family `fold-crease-overlay`,
  full description, similarity-check distinguishing rules vs every flagged
  near-miss, negative-similarity-check seven-dimension walk vs ar25 + bx84
  + qz73. Verdict: NOVEL.

## Notes
- The mechanic visibly couples a movable crease line + reflectible stamps
  + a shadow target pattern. Renders well at 64×64 if I keep stamps ~6–8
  pixels and crease 1px wide.
- Inheritance rule satisfied: L1=2 reqs, L2=3, L3=5 (each promotion adds
  one or two new required mechanics).
- The earliest design risk for write_spec is making sure each mechanic is
  *required* by the witness (no trivial fallback) — especially in L3
  where a clever stamp arrangement might let the player avoid moving the
  crease. write_spec must explicitly engineer cells that force every
  mechanic.
