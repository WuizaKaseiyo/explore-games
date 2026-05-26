# Step #03: write_spec

## Inputs Consumed
- `workspace/mechanic-pick.md` (from #02 pick_mechanic): mechanic family `tide-tilt-buoyant`, ID `kx14`, action subset `[1,2,3,4,6]`, distinguishing rules vs kf42/qz73/sp80/g50t/m0r0.
- `workspace/study-notes.md` (from #01 study): cross-cut conventions (step-bar HUD, tag-based grouping, level-data dict, two-sprite swap pattern, `_get_valid_actions` overrides).
- `skills/code/{spec-template.md, universal-scaffold.md, novaengine-api.md, id-generation.md}`: 9-section spec template, file scaffold (camera resize requirement), novaengine surface (`Sprite`, `Level`, `Camera`, `NovaBaseGame`, `RenderableUserDisplay`, `InteractionMode`, `BlockingMode`, `display_to_grid`).
- `skills/design-constraints/{checklist.md, composition-and-tutorial.md, core-knowledge-priors.md, forbidden-elements.md}`: 16-point checklist, one-new-mechanic-per-level rule, four allowed §3.4 priors, banned visual elements.
- `skills/global/{action-enum.md, color-legend.md, paths.md}`: action subset patterns, palette 0–15, repo path table.
- `skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md}`: re-grounded the §9 novelty section against the same near-misses surfaced in pick_mechanic.

## Deliverables Produced
- `workspace/mechanic-spec.md`: full 9-section spec covering (1) title, (2) mechanic family + §3.4 prior categories, (3) sprite roster (5 sprites, all internally patterned to dodge the kf42→vh68 plain-rectangle anti-pattern), (4) per-level layout + mechanics-required-by-witness + concrete witness sequences with action counts (L1=10, L2=15, L3=21) + difficulty justification (random-resistance, human-tractable, planning-depth), (5) action mapping `[1,2,3,4,6]`, (6) HUD widget + per-game state + canonical re-projection algorithm, (7) win predicate (colour-strict ball-on-target-ring), (8) lose predicate (step-counter only), (9) novelty note vs taxonomy and prior-games index.

## Notes
- **Mechanic count per level**: L1 N=2 (water-level control + tilt), L2 N+1=3 (+platform-block), L3 N+2=4 (+anchor toggle). Witness for each level demonstrably exercises every listed mechanic — no hidden mechanics.
- **L3 witness initially had a sequencing bug** — first draft had "tilt left from (3,5)" which would push the orange ball into the wall instead of where intended. Caught and corrected mid-spec: switched to anchoring orange first, raising water (lifts only green), tilting green left to its target, anchoring green there, then unanchoring orange to start the second-half route. The corrected witness is 21 actions and uses both directions of M1, both directions of M2, the platform's block, and the anchor toggle (twice for orange, twice for green = 4 ACTION6 events total, all on actual ball cells so each consumes a step).
- **L3 deliberately defeats the L2 greedy strategy.** L2 was solvable by a directional "raise + tilt right" combo. L3 has TWO balls that must end up on opposite sides — they cannot pass each other via tilt alone (tilt moves both in the same direction). Anchor introduces the asymmetry that makes the swap possible. Order of anchoring matters; anchoring the wrong ball at the wrong tide level produces no feasible solution.
- **Re-projection rule** is specified canonically in §6 with a Python sketch — this is the load-bearing piece for `implement` to translate. Key invariants: (1) anchored balls never move; (2) un-anchored balls always settle to their highest reachable row in their column given current water + platforms; (3) inter-ball collisions during re-projection back the moving ball off by one cell in its movement direction.
- **Camera resize**: the universal-scaffold note flags that non-64×64 grids require `self.camera.width = gw; self.camera.height = gh` in `on_set_level`. Spec specifies grid_size=12×12 and includes the resize step in §6.
- **HUD position** (top letterbox row) deliberately diverges from priors' bottom-row HUDs — small flourish toward visual signature divergence.
- **§3.4 forbidden elements check** (per `forbidden-elements.md`):
  - No digits-as-glyphs ✓
  - No letters ✓
  - No real-world clipart — water rendered as flat blue fill, not "ocean" or "river" iconography; balls are abstract orange/green ring sprites; platforms are abstract grey-with-black-edge bars ✓
  - No cultural conventions — the UP=raise-water mapping is a discoverable physical rule, not a learned association (UP-key acts on the water surface; no cultural priming required to figure it out) ✓
  - No on-screen text ✓
