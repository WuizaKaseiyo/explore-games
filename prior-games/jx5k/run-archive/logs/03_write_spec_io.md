# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): game ID jx5k, family `constellation-edge-link`, near-miss tables, negative-similarity walkthrough.
- skills/code/spec-template.md: 9-section structure.
- skills/design-constraints/composition-and-tutorial.md: 3-level structure, +1-or-+2 mechanic per promotion.
- skills/design-constraints/checklist.md: full 21-item checklist for self-check.
- skills/design-constraints/difficulty-rules.md: 4-bullet per-level difficulty justification.
- skills/design-constraints/core-knowledge-priors.md: confirmed mechanic uses geometry/topology + objectness only.
- skills/global/action-enum.md, color-legend.md: ACTION enum semantics, palette legend.
- skills/code/universal-scaffold.md: implementation patterns (two-sprite-swap idiom for edge toggling, RenderableUserDisplay for HUD).

## Deliverables Produced
- mechanic-spec.md: full 9-section spec with EXACTLY 3 levels, per-level mechanic enumeration (L1=1, L2=2, L3=3 — strictly +1 each promotion), per-level necessity counterfactuals, witnesses written out as ACTION sequences, per-level 4-bullet difficulty justification.

## Notes
- Self-check against checklist while writing:
  - 1 (palette 0-15 only): yes, palette `{1, 3, 4, 8, 9, 11, 12, 13, 14, 15}` — all in range.
  - 2 (universal scaffold): planned in §3 sprite roster + §6 HUD.
  - 3 (action_enum subset): `[5, 6]` ✓.
  - 4 (exactly 3 levels): yes.
  - 5 (4-char ID): jx5k ✓.
  - 6 (priors): geometry/topology + objectness only ✓.
  - 7 (no glyphs): nodes are circles, pips are dots, edges are line ribbons, walls are brick patterns; no letters, digits, real-world clipart, or arrow glyphs.
  - 8 (≥ 2 mechanics): yes, M1 + M2 active by L2, M3 added at L3.
  - 9 (L1 = base dynamic system, all required by witness): yes, L1's M1 is the only mechanic and is required.
  - 10 (composition L2/L3): L2 composes M1+M2 (every edge requires M2 colour-cycling first), L3 composes M1+M2+M3 (walls force routing AND colour rule still applies).
  - 11 (mechanic inheritance + +1-or-+2): N=1 at L1, N+1=2 at L2, +1=3 at L3 — every promotion adds exactly 1 new mechanic ✓. Every L1 mechanic carries forward at L2/L3 and is required.
  - 12 (strict counterfactual): per-mechanic table is implicit in §4's "necessity" bullets — L1: M1 required because zero edges else win false. L2: M1 required (else zero edges); M2 required (else cross-colour edges all rejected, zero legal edges). L3: M1 required; M2 required (same reason at L3); M3 required (in the spec's argument the witness uses peripheral edges that walls force — though see *open concern* below).
  - 13/14 (novelty): yes, addressed in §9.
  - 15 (distinguishing rule for near-miss): yes, articulated in §9 + mechanic-pick.md.
  - 16 (win condition stated): yes, §7.
  - 17 (lose condition stated): yes, §8.
  - 18 (difficulty floor/ceiling): all 4 bullets per level filled in §4.
  - 19 (no hidden state): selected-node has visible halo cue; reject-flash phase has visible flash; step-remaining has HUD bar.
  - 20 (don't generate low-resolution): grid is 32×32 (not 12 or 16), nodes are 5×5 with internal cross-pattern, walls are 4×4 with brick-pattern, edges have 1-pixel underlay + 1-pixel accent — internal pixel structure throughout.
  - 21 (UI teaches): nodes look pressable (filled circles with rim), pip rings convey degree count, halo conveys selection, edges have visible thickness, walls have brick texture.

## Open concerns to revisit in critique
1. **L3 wall-mechanic exercise is borderline**. The witness AVOIDS walls rather than actively triggering them. Per checklist item 12, the strict-counterfactual question is "can L3 be solved without M3's distinguishing behaviour?". Without walls, alternate edge graphs (using diagonals) ALSO satisfy degree=2-each. So walls are technically a constraint that rules out alternatives, not a verb the witness uses. May need to either (a) make a wall the *only* obstacle on a uniquely required edge, or (b) replace M3 with an active verb (edge-redirect, multi-edge, edge-color-cycle).
2. **L3 wall-rasterisation precision**. The spec assumes Bresenham line rasterisation; need to be careful about diagonal-line corner cases (e.g., does the line from (5, 16) to (16, 5) include (10, 10) or skip it?) when implementing edge-legality.
3. **L1 single-mechanic** — the spec marks L1 with N=1 (only M1). This satisfies the "≥1" floor in `composition-and-tutorial.md` but is at the floor; some past runs preferred N=2 with two interacting mechanics at L1. This is acceptable per the rule but worth flagging for critique.
4. **L2 witness contains 20 actions, step budget 50** — generous. L3 witness 12 actions, step budget 40 — also generous. May want to tighten step budgets to make difficulty justification more pointed.