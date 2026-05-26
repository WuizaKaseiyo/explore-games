# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): mechanic family,
  ID, novelty argument, level outline (L1 walk-and-stamp; L2 +polarity;
  L3 +insulator-walls)
- skills/code/spec-template.md (9-section spec template)
- skills/code/universal-scaffold.md (style rules, two-sprite swap idiom,
  camera/grid_size relationship)
- skills/code/id-generation.md (already used in pick_mechanic)
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,difficulty-rules,forbidden-elements}.md
  (already digested in study)
- skills/global/{action-enum,color-legend,paths}.md (already digested)
- skills/mechanic-novelty/* (similarity rules — re-applied in §9 of spec)

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec covering title, mechanic
  family, sprite roster (8 sprite kinds + step-counter HUD widget),
  3-level progression with witness solutions (L1: 5 actions; L2: 16
  actions; L3: 27 actions), per-mechanic counterfactual-necessity
  table per checklist item 12, action mapping `[1,2,3,4,5]`, HUD,
  win condition, lose condition, novelty note vs taxonomy and
  prior-games corpus.

## Notes
- Grid size is 64×64 with 4-pixel-stride movement (à la wa30) so
  thermal cells are conceptually 16×16 (4×4 display block per cell)
  while pawn / target / wall sprites are 4×4 internal-pattern sprites
  rendered at full display resolution. This satisfies checklist item
  20's ban on chunky uniform-colour cell-blocks: every thermal cell's
  4×4 block uses an internal 2-tone pattern (frost-diamond, X-flame,
  etc.) rather than a flat fill, and every gameplay sprite has
  internal pip / ring / border pattern.
- Cumulative-latch win semantics chosen over simultaneous-tick win
  semantics to keep planning depth manageable: visiting target T with
  matching polarity LATCHES T permanently; player doesn't have to
  re-arrive at all targets at the same tick. This avoids combinatorial
  explosion for L2/L3 witnesses. The latch is surfaced visually by a
  gold-frame target variant (checklist item 19).
- Mechanic count per level: L1=2, L2=3, L3=4 — each level introduces
  EXACTLY ONE new mechanic on top of all carried-forward ones, per
  the +1-or-+2 rule in checklist item 11.
- Counterfactual necessity argued per-mechanic per-level. Insulator
  wall at L3 is justified as strict because pawn at col 8 cannot
  walk DOWN through wall row at row 7 cols 4..12; without the wall
  the witness would be ~12 actions vs ~27 with wall — major routing
  change.
- Step budgets: L1=24, L2=50, L3=80 (~5×, ~3×, ~3× witness
  respectively). All increase across levels per
  difficulty-rules.md § d.
- Action set [1,2,3,4,5] — pure cardinal + freedom slot (ACTION5 =
  polarity toggle). No click, no undo. Action shape distinct from
  the click-heavy near-misses (pf3w, kp9z, gv47, vd3g).
