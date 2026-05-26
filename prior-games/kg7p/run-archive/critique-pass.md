# critique-pass — kg7p, critique visit #2

Verdict after the write_spec revision pass (#05) which addressed all four issues from critique-revisions.md (#04).

## Re-verification of the four critique-revisions issues

| Issue | Status | Verification |
|---|---|---|
| #1 — chevron arrow on `block_directional` (forbidden-elements violation) | ✅ FIXED in spec | The sprite pixel pattern is now `[[11,11,11,11], [11, 4, 4, 6], [11, 4, 4, 6], [11,11,11,11]]` — a 2-pixel magenta edge-stripe along the east edge in default rotation. Rotations 90/180/270 carry the stripe to south/west/north edges. No arrow geometry; the stripe is a topological edge-marker. |
| #2 — L2 wrong-path was discovery-stage (stage-conflation guard) | ✅ FIXED in spec | L2 layout redesigned to force a delivery order: block_orange at (8,8) sits on block_yellow's straight south path. The post-discovery wrong-path "deliver yellow first along straight south" produces a genuine collision rejection at avatar (8,7) when yellow's destination is (8,8) = block_orange. A fully-informed player who knows beam-couple + release would still try this path; the failure is a planning failure, not a discovery failure. |
| #3 — explicit camera viewport note in §6 | ✅ FIXED in spec | §6 now states the camera stays at default 64×64 because every level's grid_size = (64, 64); on_set_level does not need to resize. |
| #4 — optional avatar revisit | (left unchanged) | Author elected to keep the original avatar pattern; not face-like enough to flag. |

## All 22 checklist items — final pass

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette values 0..15 (and -1 transparent) only | ✅ PASS | Spec uses {3,4,5,6,7,9,10,11,12,14,15,8,-1}. All valid. |
| 2 | File matches universal-scaffold structure | ✅ PASS | Spec organised per scaffold; implement state will produce the file. |
| 3 | `available_actions ⊂ [1..7]` | ✅ PASS | `[1, 2, 3, 4, 5]`. |
| 4 | EXACTLY 3 `Level(...)` entries | ✅ PASS | Spec §4 enumerates three levels with distinct configurations. |
| 5 | ID is 4 lowercase alnum, not reserved, not in `prior-games/index.md`, not English | ✅ PASS | `kg7p` — checked against reserved 25 + 75+ index entries + untracked subdirs. |
| 6 | Mechanics draw from `core-knowledge-priors.md` only | ✅ PASS | Objectness + basic physics + basic geometry. (No agentness; no out-of-prior reach.) |
| 7 | No letters / no digits-as-glyphs / no clipart / no cultural conventions | ✅ PASS | Issue #1's chevron replaced with abstract edge-stripe. No arrows, no faces, no real-world clipart. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | L1 has 2; L2 has 3; L3 has 4. |
| 9 | L1 = tutorial with reduced state space, no on-screen text, base dynamic system | ✅ PASS | L1: avatar + 1 block + 1 target + walls. No HUD text. |
| 10 | L2 and L3 increase difficulty by COMPOSING all available mechanics | ✅ PASS | Witness for each level exercises every available mechanic (per the counterfactual table in critique-revisions.md). |
| 11 | Mechanic inheritance and +1-or-+2 rule | ✅ PASS | L1 N=2; L2 N+1=3; L3 L2+1=4. Each new mechanic is named; all earlier mechanics carry forward. |
| 12 | Strict counterfactual necessity (no trivial fallback), per (mechanic, level) | ✅ PASS | Per-mechanic per-level counterfactual table in critique-revisions.md, every row "no" with concrete reason. L3 M4 verified by alternate-strategy enumeration (greedy "deliver-D-first" fails at column-5 collision; couple-from-wrong-side fails the stripe-direction match). |
| 13 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ PASS | `beam-tether-haul` not in 25 reference. |
| 14 | Mechanic family absent from `prior-games/index.md` | ✅ PASS | Closest priors (kn58, vt6q, kj82, wb6n, kf42, hk7v, dj5h, wq3m, bz3k) — distinguishing rules in §9. |
| 15 | Concrete distinguishing rule for each near-miss | ✅ PASS | Every near-miss has a mechanical distinguishing rule. |
| 16 | Win condition stated for the environment | ✅ PASS | §7: every `block` on its colour-paired `target` (stride-4 (x,y) equality). |
| 17 | Lose condition stated | ✅ PASS | §8: step budget exhaustion. No soft-lock (coupling reversible; no irreversible action). |
| 18 | Per-level difficulty floor and ceiling (a/b/c/d all four bullets) | ✅ PASS | L1, L2, L3 each have (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget. L2 planning-depth now post-discovery after Issue #2 fix. L3 names a trivial heuristic (deliver-nearest) and shows its failure point geometrically. |
| 19 | No hidden state — visible cue for every mutable state | ✅ PASS | Beam-on/off → green `beam_indicator` ring. Coupling → indicator overlays the block. Facing → avatar's green emitter row rotates with avatar. Direction-lock → magenta edge-stripe rotates with sprite. |
| 20 | Don't generate a low-resolution game | ✅ PASS | 4×4 sprites with rich internal pattern: hollow centres on blocks and targets; checker on barriers; sparse-hatch on walls; edge-stripe on directional blocks; ring-with-cutout on the beam indicator; emitter-row + corner-pip on the avatar. Shape carries meaning, palette is secondary. |
| 21 | Design the UI to teach | ✅ PASS | Avatar reads as movable unit; block reads as cargo (hollow square); target reads as paired slot (concentric ring with inner-colour accent matching the block); wall reads as solid; barrier reads as permeable (checker); beam reads as active emission; direction-lock stripe reads as "this edge is the active side". |
| 22 | ACTION7 strict-undo or absent | ✅ PASS | ACTION7 not in `available_actions`. |

## Novelty verdict

**Taxonomy + prior-games** (positive similarity-check on full spec): every flagged near-miss has a concrete mechanical distinguishing rule. Closest is `wa30` (adjacency pickup-drop) — distinguished by "directional sticky-beam persistent coupling" vs. "adjacency one-shot inventory transfer". **NOVEL.**

**Negative similarity-check** (re-walked seven dimensions vs `wa30` on the revised spec): shared on dimensions 2 (verb-letter, weak — universal idiom), 3 (cargo-deliver goal — universal), 4 (step-budget lose — universal); divergent on 1 (cast — no patrolling NPCs in kg7p), 5 (supporting elements — barriers and direction-locks are unique), 6 (palette signature — light-blue + yellow + magenta + blue-orange diverges from wa30's lavender/teal), 7 (pixel grain — edge-stripe is distinctive), 8 (core dynamic — facing-directional persistent beam vs. adjacency pickup). Below the 3-substantive-dimensions rejection threshold. **NOVEL.**

## Verdict

**PASS** — all 22 checklist items pass, all four critique-revisions issues are FIXED in the spec (not deferred), and novelty is verified.

**Transition to `implement`.**
