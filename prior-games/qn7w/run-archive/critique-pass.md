# Critique pass — visit 2 (revised spec)

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette 0..15 (with -1 transparent) | ✅ PASS | All sprites use {0,1,4,5,6,9,10,11,12,14,15} + `-1`. New `dead_end_wall` uses {5}. |
| 2 | Universal scaffold (file structure) | ✅ PASS | Will be enforced at `implement` per `code/universal-scaffold.md`. |
| 3 | `available_actions` ⊆ [1..7] | ✅ PASS | `[6]` only. |
| 4 | Exactly 3 levels with composition | ✅ PASS | L1, L2, L3; +1 mechanic per level. |
| 5 | 4-char ID, no collision | ✅ PASS | `qn7w` — verified absent from references and prior-games. |
| 6 | Mechanics from core priors only | ✅ PASS | Objectness, basic physics, basic geometry/topology. |
| 7 | No letters/digits/clipart/cultural conventions | ✅ PASS | Pusher_knob redesigned as symmetric button (Critique-1 Issue 2 fix). All sprites are abstract shapes (round balls, rings, hexagons, rectangles). Green-tab on junction_node is a position-based active-branch indicator (the tab's *position* — top vs bottom — encodes state, not the colour); the colour itself is a fixed visibility hue, not a cultural-convention green-means-go signifier (the player does not toggle between green/red; there is no traffic-light coding). |
| 8 | At least 2 distinct mechanics | ✅ PASS | 3: pulse-eject, junction-routing, merge-on-coincidence. |
| 9 | L1 tutorial (base dynamic system, no on-screen text) | ✅ PASS | Single chain, single socket, single pusher; no text anywhere. |
| 10 | L2/L3 increase difficulty by composition (not size) | ✅ PASS | L2 adds junction-routing on top of pulse-eject; L3 adds merge-on-coincidence on top of L2 with both chains needing to fire to fill one pad. Not just bigger grids. |
| 11 | Mechanic inheritance + (+1 or +2) per level | ✅ PASS | L1=1; L2=2 (=N+1); L3=3 (=M+1). All L1 mechanics still required at L2 and L3; all L2 mechanics still required at L3. |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ PASS | Per-mechanic table: |
|   |   |   | • L1 / pulse-eject — no avatar, no arrow keys, no other movable sprites; the only event that fills a target_socket is an ejected ball, which only a pusher click produces. |
|   |   |   | • L2 / pulse-eject — same: only mechanism for moving balls. |
|   |   |   | • L2 / junction-routing — default-active "down" branch ends at `dead_end_wall` at (28, 54); every push without flipping fires balls into the wall (consumed); the only `target_socket_blue` is at (28, 6) on the up-branch, reachable only by flipping the junction. |
|   |   |   | • L3 / pulse-eject — only mechanism for moving balls; `merge_pad` accepts only ejected-ball deposits. |
|   |   |   | • L3 / junction-routing — both junctions default to "down"; chain A's down-branch ends at `dead_end_wall_A` at (20, 58); chain B's down-branch ends at `dead_end_wall_B` at (38, 34); both walls consume any ball ejected through the default-active branch. The only target on the level is the merge_pad at (20, 22), reachable only when junction A = "up" (chain A's up-branch ejects upward to (20, 22)) AND junction B = "left" (chain B's left-branch ejects leftward to (20, 22)). Both junctions must be flipped from default. |
|   |   |   | • L3 / merge-on-coincidence — the only target on the level is a `merge_pad` requiring 2 deposits to register filled. There is no single-ball `target_socket` on L3. A single eject cannot fill the level's only win condition. |
|   |   |   | Independent enumeration of plausible alternates: (i) "spam pusher without flipping" — fails (every eject hits a wall and is consumed). (ii) "flip junctions only, never push" — fails (no balls move; budget runs out). (iii) "fire chain A but not chain B" — fails on L3 (only one deposit; merge_pad needs two). (iv) "fire wrong order" (push before flip) — wastes balls but recoverable in budget; this is a planning mistake, not a fallback that wins. No alternate strategy bypasses the listed mechanics within the step budget. |
| 13 | Mechanic absent from taxonomy | ✅ PASS | `pulse-chain-eject` not in any of the 25 taxonomy rows. |
| 14 | Mechanic absent from prior-games index | ✅ PASS | Not in any of the 33 prior-games entries. |
| 15 | Distinguishing rules for near-misses | ✅ PASS | §9 of spec articulates concrete distinguishing rules vs ka59, r11l, vc33, lp85 (taxonomy) and vs vn8d, kp9z, bx84, kn58, gx7m, xn5p, rk7x (priors). All rules cite mechanical/visual differences, not vague "it's different" statements. |
| 16 | Win condition stated, achievable in all levels | ✅ PASS | `_check_win()`: every `target_socket` filled AND every `merge_pad` has 2 deposits. After Critique-1 Issue 1 fix, L2 has only one target_socket (blue, fillable); L3 has only the merge_pad. Both levels are reachable. |
| 17 | Lose condition stated | ✅ PASS | Budget exhaustion + proactive `_check_winnable()` to detect dead-states (avoids the soft-lock waiting-room anti-pattern). |
| 18 | Difficulty floor and ceiling per level | ✅ PASS | All four bullets per level: |
|   |   |   | • L1: (a) random-tractable as tutorial — by-design per §5 of tech-report; (b) ~30-60 sec; (c) no strict planning; (d) budget=6, generous. |
|   |   |   | • L2: (a) random-resistant — sequence dependency + colour-class non-trivial; (b) ~60-120 sec; (c) post-discovery decision space=2, plausible-wrong=push-without-flip, witness reasoning chain stated; (d) budget=16. |
|   |   |   | • L3: (a) random-resistance ~10⁻⁴ for blind sequences; (b) ~120-180 sec; (c) decision space=4 (≥L2); trivial heuristic="greedy push without flipping" fails (both ejects hit walls); witness diverges at action 1 (flip vs push); (d) budget=30, generous and not shrinking from L2. Stage-conflation guard satisfied — heuristic failure is *post-discovery* (player knows mechanics, makes a planning error). |
| 19 | No hidden state | ✅ PASS | All state mutations have persistent visual cues: junction tab position (active branch); chain ball count (sprites); socket fill (centre filled); merge_pad deposits (centre fill colour); pulse propagation (transient flash). |
| 20 | No low-resolution rendering | ✅ PASS | Native 64×64 grid; 6×6 sprites with internal pixel patterns (highlights, rims, recesses, hollow centres). Sprite kinds differentiated by *shape*, not just colour. |
| 21 | UI teaches | ✅ PASS | Sprite-role mapping explicit and defensible: chain_ball = round physical body; pusher_knob = recessed symmetric button (= pressable); target_socket = hollow ring (= awaits arrival); junction_node = hexagonal switch with position-based tab indicator (= togglable selector); merge_pad = hollow frame with centre pip (= 2-deposit receiver, distinct from single-ball socket); dead_end_wall = solid black block (= impassable barrier). After Critique-1 Issue 2 fix, no sprite encodes direction via shape protrusion. |

## Novelty verdict

**`pulse-chain-eject` (qn7w) — NOVEL** vs the 25-game taxonomy and the 33-entry prior-games corpus.

- Positive similarity check: distinguishing rules concrete and binary (vs vn8d "every cell falls" vs qn7w "only terminal moves"; vs kp9z "per-cell counter state" vs qn7w "stateless balls"; vs bx84 "LOS beam" vs qn7w "physical chain of touching balls").
- Negative similarity check: closest prior is vn8d; shared on dimensions 2 (click) and 4 (budget) strongly, plus 3 (hit targets) and 5 (specialty cells) weakly; diverges on heavy axes 6 (visual signature), 7 (pixel grain), 8 (core dynamic). Below the 3+ rejection threshold and well below when weighted toward heavy axes.

## Verdict

✅ All 21 checklist items pass. Novelty NOVEL. Transition to `implement`.
