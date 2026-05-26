# critique-pass.md (visit #3 of `critique_spec`)

Spec under review: `workspace/mechanic-spec.md` (game `jx5k`, after visit-#2 revisions).

## Per-checklist verdict (`design-constraints/checklist.md`)

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette 0-15 only | ✅ PASS | Uses `{1, 3, 4, 8, 9, 12, 14, 15}`; no value out of range. |
| 2 | File structure matches universal-scaffold | ✅ PASS | §3 sprite roster + §6 HUD + §5 action enum follow scaffold; concrete implementation due in `implement` state. |
| 3 | `available_actions` ⊂ [1..7] | ✅ PASS | `[5, 6]`. |
| 4 | Exactly 3 `Level(...)` entries | ✅ PASS | §4 enumerates exactly L1, L2, L3. |
| 5 | 4-char ID, lowercase alphanum, not in reserved list, not in prior-games index | ✅ PASS | `jx5k`; verified vs both lists in pick_mechanic. |
| 6 | Priors envelope (objectness / geometry+topology / physics / agentness only) | ✅ PASS | Geometry+topology + objectness. |
| 7 | No letters, digits-as-glyphs, real-world clipart, cultural conventions | ✅ PASS | Nodes are circles with internal cross-pattern; pips are dots; edges are line strands. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | M1, M2, M3 active by L3. |
| 9 | L1 = base dynamic system; all L1 mechanics required by L1 witness; reduced state space; no on-screen text | ✅ PASS | L1: only M1, required (zero edges → win false); 4-node small layout; no text. |
| 10 | L2 / L3 increase difficulty by COMPOSING every available mechanic | ✅ PASS | L2 witness uses M1 (8 edges) AND M2 (2 recolours); L3 witness uses M1 (6 edges) AND M2 (2 recolours) AND M3 (1 doubling). All mechanics interact. |
| 11 | Mechanic inheritance and +1-or-+2 rule | ✅ PASS | N=1 at L1; N+1=2 at L2 (1 new = M2); L2-count+1=3 at L3 (1 new = M3). Every earlier mechanic carried forward and required. |
| 12 | Strict counterfactual / no trivial fallback | ✅ PASS — see per-mechanic table below |
| 13 | Mechanic family absent from taxonomy-of-25 | ✅ PASS | No taxonomy entry shares `constellation-edge-link` or its description-level signature; nearest near-misses (bp35, lf52) are graph-WALKING vs. graph-CONSTRUCTION. |
| 14 | Mechanic family absent from prior-games/index.md | ✅ PASS | None of the 36 prior-games rows share the family. |
| 15 | If sounds similar, distinguishing rule articulated | ✅ PASS | §9 cites bp35, lf52, cn04, sb26, pz4t, qm4t, vn8d, qb84 with concrete distinguishing rules. |
| 16 | Win condition stated as testable predicate | ✅ PASS | §7 — degree-pip match across all nodes. |
| 17 | Lose condition stated | ✅ PASS | §8 — step counter ≤ 0 fires `self.lose()`. |
| 18 | Difficulty floor and ceiling, all 4 bullets per level | ✅ PASS — see difficulty table below |
| 19 | No hidden state | ✅ PASS | All mutated state has a visible cue: selection → halo, reject → flash, step-remaining → HUD bar, node-color → variant TANGIBLE swap, edge-state → strand sprite TANGIBLE / REMOVED. |
| 20 | Don't generate low-resolution game | ✅ PASS | 32×32 logical grid scales 2× → 64-display-pixel frame. 5×5 nodes (10×10 display pixels) with internal cross-pattern; multi-edge double-strand has visible parallel detail; HUD bar 1-row pattern. Internal pixel structure throughout — not chunky uniform-colour blocks. |
| 21 | UI teaches | ✅ PASS | Pip-rings convey required degree (count visible at a glance); halo conveys selection; edge ribbons conveys connections; node colour-variants distinguish kinds; double-strand renders visibly distinct from single. |

## Strict counterfactual per-mechanic table (item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (edge-link) | NO | Win predicate `every node's filled-pip == target` evaluates `0 == 2` at level start (zero edges). Only edge creation increments filled-counts; edge creation IS M1. |
| L2 | M1 | NO | Same as L1 — zero edges → at least one node fails predicate. |
| L2 | M2 (colour-cycle + same-colour-edge) | NO | Starting colours `[red, blue, red, blue, red]` make 6 of 8 target edges (radials n_i–n4 for i ∈ {1, 3} blue↔red, perimeter pairs all blue↔red) cross-colour and rejected. Witness must recolour both blue nodes to red (or alternative); recolouring = M2. |
| L3 | M1 | NO | Zero edges → at least one node degree 0 ≠ target. |
| L3 | M2 | NO | Starting `[red, blue, red, blue]`. The witness target graph requires edges {n0–n1, n0–n3, n1–n2, n2–n3, n0–n2 (doubled)} = 5 distinct pairs, of which 4 are cross-colour (n0–n1, n0–n3, n1–n2, n2–n3). All 4 rejected at start; recolouring required. |
| L3 | M3 (multi-edge / 3-state cycle) | NO | n0 has target degree 4 with 3 distinct other nodes (n1, n2, n3). Maximum single-edge degree = 3 (one edge to each). The 4th degree-unit must come from a parallel edge. With `max_edge_multiplicity = 1` (the L1/L2 setting), this is unsatisfiable. M3 (max=2) provides the parallel edge; the witness uses n0–n2 doubled. |

Per-mechanic alternates considered and ruled out (item 12 *enumerate alternates* directive):
- *L2 alternate "use n0–n2 chord at L2":* line from (4, 16) to (28, 16) passes through (16, 16) where n4 sits → rejected by `_edge_legal`'s "no other-node body on rasterised line" check. Player observes rejection. So the chord is not a fallback.
- *L3 alternate "spam ACTION5 to recolour and rely on n0–n2 + n1–n3 same-colour pairs alone":* even if n0–n2 doubled and n1–n3 doubled (max degrees 2 each), maximum reachable degrees are `[2, 2, 2, 2]` — n0 and n2 fall short of target 4. M2 recolouring required.
- *L3 alternate "double a different pair":* witness's doubled pair is uniquely n0–n2 (the only pair where both endpoints have target degree 4); doubling any other pair overshoots one endpoint. The post-discovery heuristic-fail argument in §4 L3 (c) walks through this concretely.

## Difficulty floor / ceiling table (item 18)

| Level | (a) Random-resistance | (b) Human time | (c) Planning depth | (d) Step budget |
|---|---|---|---|---|
| L1 | ≪ 10⁻⁸ chance random clicker covers a 4-cycle within 30 actions | ~ 1 min | None required (item 12c L1 — discovery is the entire difficulty) | 30 (≈ 3.75× witness) |
| L2 | ≪ 10⁻¹⁶ within 60 actions | ~ 2 min | Moderate post-discovery: 5+ candidate first-actions, plausible-wrong path (n0–n2 chord rejected via n4 obstruction), 3-step reasoning chain | 50 (≈ 2.5× witness) |
| L3 | ≪ 10⁻¹⁶ within 50 actions | ~ 3 min | Challenging: 6+ candidate first-actions, named heuristic-fails ("double every edge" overshoots, irrecoverable correction cost) | 50 (≈ 3.1× witness) |

Step budgets: 30, 50, 50 — non-decreasing across levels per `difficulty-rules.md` § 2d L3.

## Novelty re-run

| Source | Closest entry | Verdict |
|---|---|---|
| Taxonomy of 25 | bp35, lf52 (graph-walk family) | NOVEL — distinguishing rule: graph CONSTRUCTION vs. graph TRAVERSAL. |
| Taxonomy of 25 | cn04 (nub-pair-glyph) | NOVEL — distinguishing rule: abstract logical edges vs. physical pixel-coincidence snapping. |
| Taxonomy of 25 | sb26 (tile-place-commit) | NOVEL — distinguishing rule: no slots, no commit verb, no Mastermind hint feedback. |
| Prior games (36 entries) | qm4t (convex-pen-trap) | NOVEL — distinguishing rule: degree-match win predicate vs. polygon-containment predicate. |
| Prior games | qb84 (bead-lift-swap) | NOVEL — distinguishing rule: ACTION6 click-pairs vs. arrow chain-navigation; no swap/peg semantics. |
| Negative similarity walk | qm4t / bx84 / bp35 | 0 dimensions of overlap (per `mechanic-pick.md`); fleshed-out spec adds M2 + M3 which further differentiate. |

`prior-games/index.md` non-empty (36 rows); none share family. **NOVEL**.

## Verdict

**ALL 21 CHECKLIST ITEMS PASS. NOVELTY: NOVEL on both axes.**

Transition to `implement`.
