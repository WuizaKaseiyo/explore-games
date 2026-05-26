# critique-pass.md (visit 2)

## Checklist (1–18) + items 19–21

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Palette ⊂ [0..15] + -1 | ✅ | Uses 0, 1, 4, 5, 6, 7, 9, 11, 12, 13, 15. |
| 2 | Universal scaffold | ✅ | Spec describes imports → sprites → levels → constants → HUD → game class. |
| 3 | available_actions ⊂ [1..7] | ✅ | [1, 2, 3, 4, 5]. |
| 4 | Exactly 3 levels | ✅ | L1, L2, L3 only. |
| 5 | 4-char ID novel | ✅ | `zw91` not in reserved 25 nor in prior-games index. |
| 6 | Mechanics from §3.4 priors | ✅ | objectness + geometry/topology + basic physics; no agentness. |
| 7 | No letters/digits/clipart/cultural | ✅ | Crosses are topological symbols (allowed); brick / hollow-ring / cracked-star patterns are abstract. |
| 8 | ≥ 2 mechanics | ✅ | L1=2, L2=3, L3=4. |
| 9 | L1 base dynamic system | ✅ | M1 + M2, both witness-required, perimeter-only walls + 1 socket, reduced state space, no on-screen text. |
| 10 | L2/L3 compose, not scale | ✅ | L2 requires M1+M2+M3 in concert; L3 requires M1+M2+M3+M4 in concert. |
| 11 | +1-or-+2 mechanic per level | ✅ | L1 N=2 → L2 M=3 (N+1) → L3 4 (M+1). All carry forward. |
| 12 | Strict counterfactual necessity | ✅ | Revised: alt-path "single burst clears everything without M3" is enumerated and refuted. M3, M4 individually necessary at L3. M3 necessary at L2 (no detour through wall column). |
| 13 | Family absent from taxonomy | ✅ | `inflate-fit-burst` family-tag novel; closest near-misses (s5i5, ka59, ft09) have concrete distinguishing rules in §9. |
| 14 | Family absent from prior-games | ✅ | No prior-games entry for self-resizing avatar. |
| 15 | Concrete distinguishing rules for near-misses | ✅ | §9 articulates per-near-miss rules (not vague). |
| 16 | Win predicate stated | ✅ | "every socket: avatar.top_left==socket.top_left AND avatar.size==socket.size". |
| 17 | Lose predicate stated | ✅ | step counter exhaustion. |
| 18 | Difficulty floor/ceiling per level | ✅ | (a)/(b)/(c)/(d) all stated for L1, L2, L3 per `difficulty-rules.md`. L3-budget > L2-budget. |
| 19 | No hidden state | ✅ | Avatar size: sprite-variant swap visible; overloaded: persistent halo at layer 5; budget: HUD bar. |
| 20 | Pixel-detail richness | ✅ | grid_size=(64,64) at scale 1; every primary sprite has internal pattern (cross, brick, hollow ring with corner accents, cracked star, spoked halo). |
| 21 | UI teaches | ✅ | Sprite shape ≈ role (avatar = filled-with-cross body; socket = hollow ring; shove-block = different-palette cross-block; breakaway = cracked-pattern wall; halo = surrounding spokes). Socket sizes visually correlate with avatar sizes via shared cross-centre motif. |

## Novelty (similarity-check + negative-similarity-check)

| Source | Closest entry | Distinguishing rule | Verdict |
|---|---|---|---|
| Taxonomy | s5i5 (rod-stretch-retract) | Player-embodied vs remote operator; radial vs axial; body-fit vs tip-on-target | NOVEL |
| Taxonomy | ka59 (sokoban-explode-chase) | Player-loaded burst vs environmental explode-tiles; no AI chasers | NOVEL |
| Taxonomy | ft09 (stamp-3x3-paint) | Avatar body vs paint stamp; no canvas | NOVEL |
| Prior-games | nb6t (hinge-chain-reach) | Single avatar radial resize vs multi-segment articulated arm | NOVEL |
| Prior-games | gv47 (seed-grow-surround-dissolve) | Avatar self-resize vs canvas region paint-spread | NOVEL |
| Prior-games | kn58 (anchor-pull-magnet) | Self-footprint push via own growth vs external magnet on multi-pawn | NOVEL |
| Prior-games | kp9z (grain-accumulate-topple) | Single discrete cycle vs sandpile cellular automaton | NOVEL |

Negative similarity (8 dimensions): max overlap with any single prior is 2 dimensions (step-counter universal + mixed arrow+modal action class). No prior shares 3+ dimensions. Strongest divergence on dimensions 5, 6, 7, 8 (cast / signature / pixel-grain / core-dynamic).

## Verdict

**PASS — all 21 checklist items + novelty + negative similarity.** Transition to `implement`.
