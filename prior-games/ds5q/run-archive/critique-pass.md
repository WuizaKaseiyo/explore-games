# Critique-pass — round 2 (revised spec)

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Palette 0..15 + -1 only | ✅ PASS | All sprites use values 0–15; `-1` only as transparent. |
| 2 | Universal scaffold | ✅ PASS | § 3 roster, § 4 levels, § 5 actions, § 6 HUD, § 7/8 win/lose all present. |
| 3 | available_actions ⊆ [1..7] | ✅ PASS | `[1, 2, 3, 4, 5]`. |
| 4 | Exactly 3 levels | ✅ PASS | L1, L2, L3. |
| 5 | 4-char ID, lowercase, alphanumeric, not English, no collision | ✅ PASS | `ds5q`. |
| 6 | Mechanics from core-knowledge-priors only | ✅ PASS | Objectness + geometry/topology. No physics or agentness invoked. |
| 7 | No letters/digits/clipart/cultural conventions | ✅ PASS | Avatar redesigned as rim+inner-block+corner-indicator; no tool, no humanoid. Walls are abstract striped rectangles. Stones are solid blocks. Pads are concentric rings. Exit is nested squares. None resemble letters/digits or real-world clipart. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | L3 has 4 (walk + erode-adjacent + colour-pickaxe-match + layered-hardness). |
| 9 | L1 tutorial — reduced state space, no on-screen text, witness exercises L1 mechanics | ✅ PASS | L1 corridor is 1 tile wide; no text; witness uses both walk and erode. |
| 10 | L2/L3 difficulty by composition (not grid scaling) | ✅ PASS | Same `grid_size` 64×64 across all levels; mechanic count grows; geometry composes carry-forward + new mechanics. |
| 11 | Mechanic inheritance + (+1 or +2) per level | ✅ PASS | L1 N=2, L2 N=3 (+1 colour-pickaxe-match), L3 N=4 (+1 layered-hardness). All carried forward. |
| 12 | Strict counterfactual necessity (per-mechanic table) | ✅ PASS | See table below. Every mechanic at every level has a "no" answer with concrete cell/sprite/rule blocking alternates. |
| 13 | Mechanic family absent from taxonomy | ✅ PASS | `wall-erode-chain` not in 25-game taxonomy. |
| 14 | Mechanic family absent from prior-games index | ✅ PASS | Not in 41-row corpus. |
| 15 | Concrete distinguishing rules for near-misses | ✅ PASS | xn5p, wt39, bx84, vd3g, fz5j, kn58, ek73, jd4q each have a concrete rule in § 9. |
| 16 | Win condition stated as testable predicate | ✅ PASS | `avatar.x == exit.x and avatar.y == exit.y → next_level()`. |
| 17 | Lose condition stated | ✅ PASS | `_action_count >= step_budget → lose()`. |
| 18 | Difficulty floor and ceiling per level (a-d, plus L2/L3 planning depth concrete) | ✅ PASS | All four bullets per level. L2 (c) names south-detour as plausible-wrong with witness reasoning chain. L3 (c) names "monotone-progress along goal-row" as the failing post-discovery heuristic with concrete divergence trace at step 3 of the witness and a quantified ~23% delay. |
| 19 | No hidden state | ✅ PASS | Charge state visible via avatar's corner indicator pixel; persistent for the duration of the charge. |
| 20 | Not low-resolution | ✅ PASS | 64×64 grid, 8×8 sprites with internal stripe / ring / nested-square / corner-indicator patterns. Each gameplay-relevant sprite has real internal pixel detail. |
| 21 | UI teaches | ✅ PASS | Sprite-shape ≈ sprite-role for walls, stones, pads, exit, avatar. Wall stripe count communicates hardness. Pad ring colour communicates which charge. Avatar corner-indicator communicates current charge. Visual carries every mechanic; no text needed. |

## Per-mechanic counterfactual table (item 12)

| Level | Mechanic | Solvable without M? | Why not (concrete) |
|---|---|---|---|
| L1 | walk | no | Avatar at (0,4) must reach exit at (7,4); ACTION5 alone never relocates the avatar. |
| L1 | erode-adjacent | no | Two `wall_grey_h1` at (3,4), (5,4) on the only east-bound corridor at row 4; row 3 is full stone (S×8) and row 5 is full stone (S×8), sealing every detour around either grey wall. |
| L2 | walk | no | Same as L1 — only walking changes avatar position. |
| L2 | erode-adjacent | no | (3,4) is the only opening in col 3 (other (3,y) are stones); (5,4) is the only opening into the (6,4) → (7,4) exit-approach corridor (col 7 sealed except exit, (6,3) and (6,5) stones). |
| L2 | colour-pickaxe-match | no | Avatar starts uncharged; ACTION5 no-op until pad. Red wall needs red charge (only at (1,0)); blue wall needs blue charge (only at (6,2)); pads charge to two distinct colours, both required. |
| L3 | walk | no | Same as L1/L2. |
| L3 | erode-adjacent | no | Col 3 sealed except at (3,1) red h2 and (3,4) red h3; (6,4) reachable only via (5,4) blue wall; col 7 sealed except (7,4) exit. |
| L3 | colour-pickaxe-match | no | Same as L2 — uncharged avatar, two pads, two colour-walls. |
| L3 | layered-hardness | no | BOTH col-3 openings have hardness > 1 ((3,1) is hardness 2, (3,4) is hardness 3). No alternate path through col 3 exists, so multi-strike erosion is unavoidable on whichever route is chosen. |

## Novelty verdict

- **Positive similarity check:** every taxonomy near-miss (xn5p, wt39, bx84) has a concrete distinguishing rule in § 9 grounded in opposite-direction verb (additive vs subtractive), different routed entity (beam vs avatar), and different player input style (glide vs single-step). Every prior-game near-miss (xn5p, vd3g, fz5j, kn58, ek73, jd4q) has a concrete rule grounded in different routed object, different input action, autonomous-vs-deliberate state change, or trail-direction.
- **Negative similarity check:** closest single prior is xn5p, sharing 4 universal-trivial dimensions (board has chamber + walking pawn, kills via step budget, cast has walls + avatar, rich pixel grain) and diverging on the 4 named-principle dimensions (player input has no click in ds5q, goal is reach-exit not partition, visual signature is wall-dominated stripe-banded vs floor-dominated colour-pad insets, core dynamic is subtractive erosion with colour-charge vs additive wall stamping). Mental render of ds5q L1 (corridor with two striped walls, exit on right) vs xn5p L1 (chamber with avatar stamping walls into a colour-painted floor) shows visually distinct frames. **NOVEL.**

---

All 21 checklist items pass; novelty verdict NOVEL on every taxonomy and prior-game row. Transition to `implement`.
