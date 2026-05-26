# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): id `nh4w`, family `arc-loft-shot`, novelty argument
- skills/code/spec-template.md: 9-section format
- skills/code/universal-scaffold.md: code-structure & style rules
- skills/global/{action-enum, color-legend, paths}
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}
- skills/conventions/{from-tech-report, reference-game-patterns, cross-cut-frequencies}

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec.
  - L1: 2 mechanics (walk, click-fire) — witness 2 actions (`[ACTION4, ACTION6@(40,51)]`)
  - L2: 3 mechanics (+wall-clearance) — witness 3 actions (`[ACTION4×2, ACTION6@(44,51)]`)
  - L3: 4 mechanics (+ceiling-block) — witness 4 actions (`[ACTION4, ACTION6@(40,51), ACTION4, ACTION6@(52,51)]`)
  - Action subset `[3, 4, 6]` (minimal: walk-left, walk-right, click-fire); ACTION7 omitted (no undo)
  - Per-mechanic counterfactual necessity stated for each level
  - Per-level random-resistance, human-tractable, planning-depth, step-budget all enumerated
  - Concrete arithmetic in §4 verifies the witness clears walls / fits under ceilings; revised heights/clearances mid-spec to ensure both reachability AND post-discovery-non-trivial planning

## Notes
- During L2 design, initial draft had wall height 10 with launcher at x=12 — the arc altitude at wall x=26.5 came out to 9.52, BELOW wall height. Revised wall to height 8 and verified geometry.
- During L3 design, initial draft had wall height 10 + ceiling clearance 14 — but blue from x=8 grazed ceiling2 at altitude 13.62 (just under 14). Tightened ceiling2 clearance to 13 to force a different launcher position for blue, creating the L3 "yellow at x=8, blue at x=12" asymmetric witness with the named trivial heuristic ("fire both from same position") that fails. Revised wall to height 9 to match.
- Aesthetic considerations: brick-pattern walls (palette 12+8), tapered grey stalactites with maroon tip (palette 3+13), yellow-glow projectile, blue launcher with grey rivets and yellow muzzle. No symbol/letter/digit forms; shapes carry meaning.
- Open implementation questions for `implement` state: precise arc-resolution discretization (2 px per frame); behaviour when projectile flies off-screen-top (clamp peak to 50 px = max altitude 50); precise wall-collision check (per-pixel overlap with wall sprite pixels; or simpler: arc altitude vs wall.y at projectile.x); whether to draw a faint trajectory preview when launcher is selected.
