# critique-pass — `ej4t`

All 21 `design-constraints/checklist.md` items + similarity-check + negative-similarity-check + difficulty-rules § 2 verdicts.

## Format & structure (items 1-5)

| # | Item | Result | Notes |
|---|---|---|---|
| 1 | Palette 0..15 (and -1 transparent) | ✅ PASS | All declared sprites use values 0, 3, 4, 8, 9, 10, 11, 12, 13, 14 — all in range. ring_overlay uses palette 10. |
| 2 | Universal scaffold structure | ✅ PASS | Spec section 6 plans `RenderableUserDisplay` HUD + Camera + 7 sprites + standard `step()` dispatch; full code in implement. |
| 3 | available_actions subset of [1..7] | ✅ PASS | `[1, 2, 3, 4]` declared. |
| 4 | Exactly 3 Level entries | ✅ PASS | L1 (12×12), L2 (14×14), L3 (16×16) per spec § 4. |
| 5 | 4-char ID, not reserved, not in prior-games | ✅ PASS | `ej4t` verified in mechanic-pick.md. |

## §3.4 priors & constraints (items 6-10)

| # | Item | Result | Notes |
|---|---|---|---|
| 6 | Mechanics from 4 priors only | ✅ PASS | Objectness (sprites with positions, push) + Geometry/topology (Manhattan ring as area-of-effect) + Goal-directedness (deliver crates to targets). No agentness or other priors. |
| 7 | No letters/digits/clipart/cultural convention | ✅ PASS with one watch-item | Sprite shapes are abstract: player is humanoid-like (5×5) but uses only dots/lines, not a recognizable "person" figure (no arms/legs); crate is an abstract box-with-strap that doesn't unambiguously read as a real-world crate; target is a yellow disc; extender is a plant-like sprout that's abstract; shrinker is a *plus-shape* (topological symbol, NOT a letter "X"). **Watch-item**: in implement, ensure pixel patterns don't accidentally read as digits or alphabet glyphs. |
| 8 | At least 2 mechanics per environment | ✅ PASS | 3 mechanics total (M1 chain push, M2 extender, M3 shrinker). |
| 9 | L1 is tutorial, base mechanic, reduced state, no on-screen text | ✅ PASS | L1: 12×12, 1 mechanic (M1), 2 crates + 1 target + walls; no HUD-text; no lose hazard. |
| 10 | L2/L3 composition, not size-scaling | ✅ PASS | L2 introduces M2 (extender) and the level forces collecting it (witness MUST walk through pickup). L3 introduces M3 (trap) and the layout forces stepping on the trap, requiring both extenders. |

## Mechanic structure (items 11-12)

| # | Item | Result | Notes |
|---|---|---|---|
| 11 | Mechanic inheritance, +1-or-+2 per level | ✅ PASS | L1=1 mechanic (M1), L2=2 (M1+M2 inherited M1), L3=3 (M1+M2 inherited+M3). Increments are +1, +1. M1 fires in every level's witness (chain push). M2 fires in L2 and L3 (pickup at (5, 7)). |
| 12 | Strict counterfactual necessity | ✅ PASS — verified via the per-mechanic table below |

### Per-mechanic counterfactual table (item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (chain push gated) | NO | Walls at row 5 cols 4-10 and row 7 cols 4-10 confine player and crates to row 6 corridor. Vertical push is impossible (walls). The only target is at (10, 6). The only crate2 → (10, 6) delivery path is east-direction chain push from west of crate1; that chain push triggers M1's radius gate. |
| L2 | M1 (chain push gated) | NO | Same corridor structure as L1. Chain push of crate2 to (10, 7) is the only delivery path; chain push fires M1 gate. |
| L2 | M2 (extender +R) | NO | Initial R=1; from any reachable cell in row-7 corridor, crate2 (at (9, 7)) is at distance ≥ 2 (player max-east approach is (7, 7), crate2 distance 2). Chain push requires R ≥ 2 to cover crate2. With R=1, gate breaks chain. The extender at (5, 7) is on the only path between (3, 7) and chain-push position; walking to (7, 7) requires passing through (5, 7) which auto-consumes the pickup, growing R to 2. |
| L3 | M1 (chain push gated) | NO | Same — row-7 corridor confinement; chain push of crate1+crate2+crate3 to (13, 7) target is the only delivery. |
| L3 | M2 (extender +R) | NO | Initial R=2; chain push of 3 crates needs R ≥ 3 (rear crate distance 3 from player at (9, 7)). With R=2, chain breaks. Two extenders at (5, 7) and (8, 7) on the only path; both required to net R=3 after the trap reduces R by 1. |
| L3 | M3 (shrinker −R) | NO | Trap at (7, 7) sits between the two extenders on the only path. Player MUST step through (7, 7) to reach (9, 7). Stepping fires the trap mechanic. WITHOUT M3 active, only one extender would suffice (R=2 + 1 = 3); WITH M3 active, both required (R=2 + 1 − 1 + 1 = 3). The trap mechanic is exercised in every winning path. |

**Stage-conflation guard** (per `difficulty-rules.md` § 2(d)): All counterfactuals named above are post-discovery — they describe the player's failure to win even with full mechanic knowledge, not just discovery-stage stumbles.

**Trivial-fallback search** (independent enumeration):
- Could the player skip walls by some unintended route? No — boundary walls + corridor walls form a closed system.
- Could crates be moved by means other than push? No — only ACTION1-4 verbs are declared; no click, no rotate.
- Could a crate accidentally land on target via gravity / autonomous movement? No — no autonomous behavior; pure action-driven.

## Novelty (items 13-15)

| # | Item | Result | Notes |
|---|---|---|---|
| 13 | Mechanic family absent from 25-ref taxonomy | ✅ PASS | `radius-scope-influence` not in 25-ref taxonomy. Closest near-misses (lq5x, vp6h, kn58, bx84) addressed in spec § 9 with concrete distinguishing rules. |
| 14 | Mechanic family absent from prior-games index | ✅ PASS | Verified against 26 entries in `prior-games/index.md`. No collision. |
| 15 | Distinguishing rules concrete (not vague) | ✅ PASS | All 6 cited near-misses have specific rules: cone-vs-ring (lq5x), shadow-vs-ring (vp6h), click-anchor-vs-player-attached (kn58), 1D-ray-vs-2D-area (bx84), timing-vs-static (pf3w), unrelated (lv4k). |

### Negative-similarity (7-dim test)

Versus closest near-miss `lq5x`: shared dimensions on (2) walk+arrow input and (4) step-budget lose. = 2 dimensions, well under 3-dim reject threshold.

Versus closest prior-game `kn58`: shared on (3) deliver-pieces-to-targets and (4) step-budget. = 2 dimensions.

Versus all other priors: ≤ 2 shared dimensions each.

**Verdict: NOVEL.**

## Solvability (items 16-18)

| # | Item | Result | Notes |
|---|---|---|---|
| 16 | Win condition stated | ✅ PASS | "every target sprite has a crate at its position" — testable via `_check_win()` after every action. |
| 17 | Lose condition stated | ✅ PASS | `_steps_used >= _max_steps`. Per-level budgets 25/30/35. No other lose paths. |
| 18 | Difficulty floor and ceiling — all 4 sub-bullets per level | ✅ PASS | Per spec § 4: L1, L2, L3 each declare random-resistance + human-time + planning-depth + step-budget. Per-level structure in `difficulty-rules.md` § 2. L3 names trivial heuristic that fails ("greedy-toward-target with only one extender → chain breaks at crate3"). |

## No hidden state, visual quality (items 19-21)

| # | Item | Result | Notes |
|---|---|---|---|
| 19 | No hidden state — every state change has visible cue | ✅ PASS | R changes → ring_overlay re-rendered each tick (visible halo size matches R). Extender consumption → sprite removed from frame. Shrinker consumption → sprite recolored to palette 3 (grey "spent"). Player position → sprite moves visibly. _steps_used → drains step counter HUD. |
| 20 | Visual richness — pixel detail per sprite | ✅ PASS | Player 5×5 with eyes/body/belt; crate 4×4 with strap pattern; target 3×3 with yellow center + dark ring; extender 3×3 sprout shape; shrinker 3×3 plus-pattern; wall 4×4 with corner rivets. No 1×1 plain-colour sprites. |
| 21 | UI teaches — sprite role legible from rendered frame | ✅ PASS | Player has unique humanoid silhouette with clear eyes — reads as "the agent". Crate has strap pattern — reads as "movable thing". Target yellow disc — reads as "place a thing here". Extender green sprout with yellow core — reads as "power-up / pickup". Shrinker red plus on dark — reads as "hazard / don't step here". Ring overlay translucent halo — reads as "area of influence". A first-time viewer of L1 would immediately guess: "I am the blue figure; I should move the orange box to the yellow target". |

## Final verdict

**PASS — transition to `implement`.**

No revisions required. One soft watch-item (Item 7 sprite abstractness) noted for the implement state to verify pixel patterns don't accidentally read as alphabet glyphs.
