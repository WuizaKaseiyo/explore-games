# Critique PASS — hd7r (critique_spec visit 1)

Adversarial review of `mechanic-spec.md` against checklist.md (1-26),
similarity-check.md, and negative-similarity-check.md. All pass.

## Checklist items 1-26
1. Palette 0..15 (+ -1 transparent) only — ✅ (teal 10, orange 12, magenta 6, grey 3, slate 2, black 5, purple 15, amber 11; all in range).
2. Matches universal-scaffold structure (sprite bank → levels → constants → HUD → class) — ✅ (planned).
3. `available_actions=[1,2,3,4,6]` ⊂ [1..7] — ✅.
4. EXACTLY 3 Level entries, L1 base / L2 +1 / L3 +1 — ✅.
5. ID `hd7r` 4 lowercase alnum, not reserved, not in index, not an existing dir, not a word — ✅.
6. All mechanics from the 4 priors (agentness flee, objectness, geometry/topology) — ✅.
7. No letters/digits/clipart/cultural conventions; abstract round creatures + hollow pens + beveled walls — ✅.
8. ≥2 mechanics (M1 flee, M2 gate, M3 perp temperament) — ✅.
9. L1 tutorial: 1 creature, 1 pen, no gates/interior walls, no text, all-required — ✅.
10. L2/L3 compose (not scale): L2 adds gate-toggle rule, L3 adds perp-flee rule; each composes with carried-forward mechanics — ✅.
11. Inheritance +1/+1: N=1 (L1) → 2 (L2) → 3 (L3); every earlier mechanic carried & witness-required — ✅.
12. Counterfactual necessity — per-mechanic table below; every row "no", concrete blocker named — ✅.
13. Min-action witness: L1 K=11/D=2; L2 K=11/D=4; L3 K=16/D=5; all ≥3 & ≥2; no 1-2-action or single-repeat win (verified) — ✅.
14. Family `repulsion-herd-funnel` absent from taxonomy — ✅.
15. Family absent from prior-games (scanned all dirs) — ✅.
16. Sounds-similar priors (zk9p/mw8p/gg26/ka59) each given a concrete distinguishing rule in §9 — ✅.
17. Environment win condition stated (every creature on matching-colour pen) — ✅.
18. Lose condition stated (step-budget exhaustion; no other lose; no soft-lock) — ✅.
19. Difficulty floor/ceiling: all four bullets per level; L2 moderate planning (decision space ≥4, named wrong path, witness chain), L3 challenging (decision space ≥5, named failing greedy heuristic + divergence) — ✅.
20. No hidden mutable state lacking a cue: gate open/closed = visible sprite swap; positions/HUD all on-screen; scare-radius is a constant rule discoverable by observation, not mutable hidden state — ✅.
21. 16×16 logical at 4px/cell = native 64×64; 4×4 sprites with internal pixel detail — not chunky upscale — ✅.
22. UI teaches: shepherd reads as agent (brow), creatures as soft fleeing bodies (round + eyes), pens hue-matched to their creature, gate reads as a doorway; magenta vs orange + shape tick distinguishes the two temperaments — ✅.
23. ACTION7 omitted (no undo) — ✅.
24. Animation: flee = single-cell local; gate = in-place swap; no non-local effect → N/A correctly — ✅.
25. Lives: no hard-death path (step-budget only, exempt) → N/A correctly — ✅.
26. New rule not new map: M2 is a new verb (toggle a passage); M3 is a new world-response law (perpendicular flee) — both genuinely new rules, not relayouts — ✅.

## Counterfactual necessity table (item 12)
| Level | Mechanic | Solvable without triggering it? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 flee | no | No push/carry verb exists at L1; creature at (10,8) changes cell only by fleeing; pen (14,3) requires ≥9 flee steps. |
| L2 | M1 flee | no | Both creatures move only by fleeing; each must change cell to reach its pen. |
| L2 | M2 gate | no | Wall fills y=8 ∀x∈{0..15} except gate (8,8) (closed at start); A's pen (8,13) is bottom-region — unreachable until clicked open. BFS-without-toggle = no solution. |
| L3 | M1 flee | no | Straight creature (4,8) moves only by fleeing toward pen (12,8). |
| L3 | M2 gate | no | Wall fills x=8 ∀y∈{0..15} except gate (8,8) (closed); straight creature must cross from west (4,8) to east pen (12,8). BFS-without-toggle = no solution. |
| L3 | M3 perp | no | Magenta creature (5,11) moves only by perpendicular flee to pen (1,11); the all-straight world yields a different solution, so the perp law materially governs routing. |

Independent alternate-strategy enumeration (item 12 "verify by enumeration"):
- "push everything straight at its pen" (L3): treating the magenta creature as straight veers it off-axis (perp law) → fails.
- "open gate first, herd later" (L2/L3): the shepherd's later approach to the second creature re-enters the first creature's scare radius and dislodges it from its pen → fails; witness parks the wall-backstopped creature first.
- "single repeated arrow" (all levels): pure-one-direction leaves each creature on the wrong row/column (L1 verified; L2/L3 have creatures needing orthogonal pushes + a click).
- geometric blocking re-derived: in L2 the wall is the FULL row y=8 (x=0..15) bar the gate, and in L3 the FULL column x=8 (y=0..15) bar the gate — checked the edges and adjacent rows/cols; the border walls close the ends, so the gate is the unique crossing. Not a partial "two-wall" block.

## Novelty verdict
NOVEL against every taxonomy row and every prior-games row. Closest:
ka59 (push vs repel; chase vs flee), zk9p (toward vs away; merge vs
pen), mw8p (chase-web vs flee-field), gg26 (static-sheep+fence-region
vs moving-creatures+pen-occupancy). Negative-similarity seven-dimension
walk: no single prior ≥3 shared dimensions; divergence on core dynamic
(repel-to-steer-a-flee-vector), visual signature, and pixel grain.
Re-walked on the full spec including L2/L3 — no drift toward gg26
(single pre-placed toggle gate, not arbitrary fence placement; discrete
pen win, not flood-fill area).

## Verdict: PASS → implement
critique_spec visits used: 1/10.
