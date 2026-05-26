# Critique Pass — mr5q (visit 1)

## Checklist 1-21

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette only 0..15 (and -1 transparent) | ✅ PASS | Spec uses {1, 3, 6, 10, 11, 12, 14, 15} + -1 transparent only. |
| 2 | File structure matches universal-scaffold | ✅ PASS (pending implement) | Spec describes the pre-paired yang/yin two-sprite swap idiom, the StepCounterHud subclass, and the camera viewport-resize rule. To be re-verified at smoke-test against the implemented file. |
| 3 | available_actions ⊆ [1..7] | ✅ PASS | `[5, 6]`. |
| 4 | EXACTLY 3 levels | ✅ PASS | §4 lists L1, L2, L3 only. |
| 5 | Game ID 4 lowercase chars, opaque, non-colliding | ✅ PASS | `mr5q`: 4 lowercase alphanumeric, mixes letter+digit, not an English word, not in 25 reserved, not in prior-games index (verified by grep). |
| 6 | Mechanics from 4 priors only | ✅ PASS | Maps to 4/4: objectness (persistent pawns), agentness (per-pawn target), basic physics (attract dynamic), basic geometry/topology (yang/yin half-fill encoding + L3 wall-and-pad routing). |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS | Yang/yin half-fill is topological asymmetry (top-half vs bottom-half filled), not + or - operators. Flip-pad checkered 3×3 reads as a patterned fixture, not a glyph. Walls are flat grey blocks. No green-means-go / red-means-danger associations (red palette 8 not used at all; green=14 is just one of three group identities, not load-bearing). |
| 8 | At least 2 distinct mechanics | ✅ PASS | 5 distinct: flip, tick, discharge, colour-key, flip-pad. |
| 9 | L1 tutorial: ≥1 mechanic, all witness-required, reduced state space, no on-screen text | ✅ PASS | L1 = 2 pawns, no walls, 3 mechanics (flip, tick, discharge), all required by 7-action witness. No on-screen text anywhere in the spec. |
| 10 | L2/L3 increase difficulty by COMPOSING mechanics, not by scaling grid/items | ✅ PASS | L2 adds colour-key on top of L1's three mechanics; L2 witness exercises all four (without colour-key the level deadlocks on cross-colour blocks, per the necessity argument). L3 adds flip-pads on top of L2's four; L3 witness exercises all five (the y=9 wall has only pad gaps, forcing pad-traversal). Grid size stays (14, 14) across all three levels — composition, not scaling. |
| 11 | Mechanic inheritance + 1-or-+2 per level | ✅ PASS | L1 N=3; L2 M=4 (= N+1); L3 M'=5 (= M+1). Each promotion +1 (within +1-or-+2 rule). All earlier-level mechanics carry forward and are required by every later level's witness — verified per-mechanic in §4 of the spec. |
| 12 | Strict counterfactual necessity (per-mechanic table) | ✅ PASS | Per-mechanic table walked below — all 12 cells answer "no" with concrete blocker. Independent enumeration of plausible alternate strategies also walked below; all alternates fail by referenced cells/rules. |
| 13 | Mechanic family absent from taxonomy-of-25-games.md | ✅ PASS | No reference game uses "binary-state pawn driving mutual attract dynamics". Closest are ka59, m0r0, tu93 — all distinct verbs (push+detonate; mirrored-direction-key; same-direction-lockstep). |
| 14 | Mechanic family absent from prior-games/index.md | ✅ PASS | Closest priors: kf42 (max-distance tether, direct-arrow movement); kn58 (single-anchor pull, click anywhere); gx7m (gear rotation, mesh propagation); zd7m (cohort-step via arrows, fixed anchors). All distinguished concretely in §9 of the spec. |
| 15 | Distinguishing rule articulated for near-misses | ✅ PASS | Spec §9 articulates concrete rules per near-miss (e.g., "kf42 = arrow-keys-direct-nudge; mr5q = no arrow keys, motion is emergent from polarity field"; "kn58 = click places anchor; mr5q = click flips polarity bit"). |
| 16 | Win condition stated | ✅ PASS | Spec §7: `_check_win()` — active pawn count == 0 → next_level(). |
| 17 | Lose condition stated (or "no lose" with reasoning) | ✅ PASS | Spec §8: step_counter == 0 → lose(). Soft-lock argument: ACTION6 always available as recovery, so no true soft-lock exists; explicit reasoning provided. |
| 18 | Difficulty floor and ceiling — all four bullets per level | ✅ PASS | Each of L1/L2/L3 has (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget. L2 enumerates post-discovery decision space (5 actions), names a plausible-but-wrong alternative (tick first, ignoring uniform polarity), traces witness reasoning. L3 names a trivial heuristic that fails (greedy-without-re-flipping-pad-flipped-pawns) and shows where heuristic diverges from witness. |
| 19 | No hidden state | ✅ PASS | Polarity is always visible via half-fill orientation (top-yellow = yang; bottom-magenta = yin). No selection state; no charge; no lock/unlock. Internal `InteractionMode.TANGIBLE/REMOVED` is engine-side only and is reflected directly in which sprite renders (so the player sees the active polarity at all times). |
| 20 | Visual detail floor (no-information-loss-at-32×32) | ✅ PASS | Pawns are 5×5 with internal half-fill pattern (top vs bottom filled); 2× average-pool would average ring + filled-half + transparent into a muddy intermediate hue, losing the polarity orientation that distinguishes yang from yin. Flip-pads are 3×3 with internal checkered pattern; lossy under pool. The grid is NOT all 1×1 flat-coloured cells. |
| 21 | Sprite UI ≈ role; identical visuals correlated; visual carries mechanic | ✅ PASS | Yang/yin: visually mirror-symmetric across horizontal axis — the same outline with the fill flipped — naturally reads as "two opposite states". Colour groups (green/orange/purple): rings differ in palette only; same-colour pawns are correlated by colour-keyed attract+discharge, so the visual sharing reflects a real behavioural correlation. Flip-pad: distinct shape + palette from any pawn or wall; reads as "active fixture that does something to who steps on it". Walls: flat grey, plain, reads as inert. |

## Per-mechanic counterfactual necessity table (item 12)

| Level | Mechanic | Solvable without M? | Concrete blocker (cell / sprite / rule) |
|---|---|---|---|
| L1 | A flip (ACTION6) | no | level pawn list = [pawn_green_yang, pawn_green_yang]; both yang; same-colour-opposite-polarity target set is empty; `_attract_step` returns no-move; ticks alone produce zero motion. |
| L1 | B tick (ACTION5) | no | flip alone leaves pawns at (3,4)/(10,9), Manhattan 12, not adjacent; discharge predicate False; win predicate False; lose on budget. |
| L1 | C discharge | no | win predicate is `len(active_pawns)==0`; only `_resolve_discharges` decrements; without it pawns at adjacency stay alive and `_check_win` returns False forever. |
| L2 | A flip | no | each colour pair starts uniform polarity (greens both yang at (2,2)/(11,11); oranges both yin at (2,11)/(11,2)); within each colour group, no opposite-polarity partner; attract returns no-target; ticks no-op. |
| L2 | B tick | no | flip alone: pawns at start coords, every same-colour pair Manhattan ≥ 18 (with (7,?) wall detour), not adjacent. |
| L2 | C discharge | no | 4 active pawns at start; win requires count==0; only discharge removes. |
| L2 | D colour-key | no | post-flip cross-colour minimum distance is ≤ 9 cells (same row or same column, no wall between within row 2 / row 11 / col 2 / col 11); same-colour minimum is ≥ 18 with wall detour. Without colour-keying, every pawn's colour-blind nearest opposite-polarity is a cross-colour neighbour; pawns walk to cross-colour adjacency and BLOCK without discharging. Concrete cells: green-yang(2,2) → orange-yin(2,11) via column x=2 (no wall in column 2); orange-yin(2,11) → green-yang(2,2) symmetric. Both pairs deadlock at column 2 (or column 11) within 9 ticks; budget exhausts. |
| L3 | A flip | no | greens both yang; oranges both yin; purples both yang. Attract target set empty in every colour group; no pawn moves; pads cannot bootstrap motion (pads only fire on visiting pawn, no visit possible without motion). |
| L3 | B tick | no | flip alone: pawns at start coords; every same-colour pair Manhattan ≥ 9 (greens row 1) or ≥ 14 (orange/purple cross y=9). Not adjacent; ticks needed. |
| L3 | C discharge | no | 6 pawns at start; win requires count==0; only discharge removes. |
| L3 | D colour-key | no | within row 6 (orange-yin(2,6) and purple-yang(11,6) co-row), colour-blind Manhattan distance = 9, no wall between them. Same-colour pair distances span y=9 wall ≥ 14. Without colour-key, orange-yin walks east toward purple-yang and purple-yang walks west toward orange-yin; they meet at adjacency in row 6 and BLOCK without discharging. Same dynamic between orange-yin(11,12) and purple-yang(2,12) in row 12. Both deadlock pairs use ~9 ticks each before block; budget then must support the rest of the level via no-progress = deadlock. |
| L3 | E flip-pads | no | y=9 wall is solid except at the pad cells (4,9) and (9,9). Orange pair has one pawn at (2,6) (above y=9) and one at (11,12) (below y=9); they MUST cross y=9 to discharge; the only crossings are pad cells. The pad auto-flips polarity on visit, breaking the seeded yang↔yin pairing within ~6 ticks of the initial setup-flip; without the player issuing a re-flip ACTION6 on the post-pad pawn, both orange pawns are now uniform polarity and attract returns no-target → deadlock. Same for purple pair. Concrete cells: (4,9) and (9,9) — the only y=9 gaps. |

### Independent enumeration of plausible alternate strategies (item 12 verification by enumeration)

**For L1**:
- "Press ACTION5 from start": both pawns are pawn_green_yang; same-colour-opposite-polarity target set empty; `_attract_step` → no-move; world stalls; lose on budget. ✗
- "Click both pawns then tick": each click flips one pawn; after 2 clicks both are yin; same problem. ✗
- "Click on empty cell then tick": click on (32, 32) is no-op (no pawn there); ticks then run as in case 1. ✗
- "Click on a pawn 2 times then tick": pawn flips back to yang after 2 clicks; same problem. ✗
- Witness alternates: flipping (3,4) instead of (10,9) is a valid alternate; both work. ✓

No way to win L1 without (A flip ∧ B tick ∧ C discharge).

**For L2**:
- "Press ACTION5 from start": uniform polarity per pair; no attract; no movement; lose on budget. ✗
- "Flip just one pawn": one colour pair gets a yang+yin partner; the other stays uniform; the uniform pair never discharges; win predicate count==0 never reached; lose. ✗
- "Flip same pawn twice": cancels; same as no-flip case. ✗
- "Flip a different colour-blind permutation": e.g., flip green-yang(2,2)→green-yin and orange-yin(2,11)→orange-yang. After flip: green pair = green-yin(2,2)+green-yang(11,11); orange pair = orange-yang(2,11)+orange-yin(11,2). Same number of yangs and yins per colour as the canonical witness — symmetric valid alternate. ✓
- "Spam ACTION6 randomly + tick": polarity state random-walks; even if a valid config is achieved by chance, sustaining for the ~13-15 ticks needed for discharge requires uninterrupted ticks; the random spam interrupts. P(success) per random-resistance analysis ≈ 4×10⁻⁶ << 1/10000. ✗
- "Try to bypass colour-key by flipping cross-colour": the colour-key is a per-pawn property determined by the pawn instance's tag, not by the player's actions; clicking just changes polarity bit, never colour. Cannot exploit. ✗

No way to win L2 without all four mechanics.

**For L3**:
- "Set up flips, tick monotonically without re-flipping at pad": orange-yang traverses (9,9), becomes orange-yin, both orange uniform → stalled; player keeps ticking → budget exhausts → lose. ✗ (this is the named heuristic-that-fails)
- "Set up flips, then click random pawns mid-tick to recover": stochastic re-flip might land at the right moment but not reliably; expected actions ≈ many. May win for budget=200 if luck holds, but not deterministically.
- "Flip the side that's already on the right side of y=9 first": e.g., flip orange-yin(2,6)→orange-yang. Now orange-yang(2,6) walks east-then-south toward orange-yin(11,12). Path crosses y=9 at the closer pad — depends on x-distance. Reaches (4,9) or (9,9) after ~7 ticks → pad-flip → orange-yin → stalled. Same dynamic, same recovery requirement.
- "Choose the wrong pad to cross by tilting initial flip": e.g., flip the pawn that ends up routing through (4,9) instead of (9,9). The x-tie-break makes the route deterministic given start positions. Either pad triggers the same pad-flip; recovery requires re-flip click in either case. ✗ doesn't avoid E.
- "Bypass the wall via diagonal": diagonal moves are not the spec — Manhattan-greedy is the rule. Can't bypass. ✗

No way to win L3 without all five mechanics including E.

## Novelty re-check (full spec, not just family name)

### vs. taxonomy-of-25-games.md

Re-walked against every reference. Closest are ka59, m0r0, tu93, cn04. Concrete distinguishing rules in §9 of spec verified — no taxonomy entry has the binary-state-pawn-with-mutual-attract dynamic. **NOVEL.**

### vs. prior-games/index.md (24 priors)

Re-walked against every prior. Closest are kf42, kn58, gx7m, zd7m. Concrete distinguishing rules:
- **kf42**: max-distance soft tether + direct arrow nudge vs. mr5q's binary-polarity field + click-flip + emergent attract.
- **kn58**: single-anchor pull from clicked cell vs. mr5q's no-anchor mutual attract between same-colour opposites.
- **gx7m**: rotation propagating with sign-flip across mesh vs. mr5q's translation determined by per-pawn polarity targets (no propagation).
- **zd7m**: arrow-cohort-step + fixed anchors vs. mr5q's no-arrow + binary-state-driven motion.
**NOVEL.**

### Negative-similarity-check 8-dimension walk vs full spec

Re-walked against the closest priors. Spec did not drift to higher overlap at L2 or L3:
- vs kf42: 2/8 shared (board content, kill condition); heavy-weighted dimensions (visual signature, pixel grain, core dynamic) all diverge. **PASS** (well below 3+ rejection threshold).
- vs zd7m: 2/8 shared. **PASS.**
- vs kn58: 1/8 shared. **PASS.**
- vs gx7m: 1/8 shared. **PASS.**

## Verdict

**ALL CHECKLIST ITEMS 1-21 PASS. NOVELTY VERIFIED. PROCEED TO `implement`.**
