# Critique pass — mw8p

Adversarial review against every item of
`design-constraints/checklist.md`, plus the
`mechanic-novelty/{similarity,negative-similarity}-check.md` rules,
re-run on the FULL spec.

## Format & structure (items 1–5)

| # | Item | Verdict |
|---|---|---|
| 1 | Every sprite uses palette 0..15 + `-1` transparent | ✅ PASS — spec § 3 lists palette values 0, 4, 7, 8, 10, 11, 12, 13, 14, 15 (all in [0..15]); `-1` reserved for transparent in 6×6 sprite design. |
| 2 | File structure matches `code/universal-scaffold.md` | ✅ PASS — spec § 3 & § 6 plan: imports → sprites dict → levels list → constants → StepCounterHud → `class Mw8p(NovaBaseGame)`. (Verifiable at implement time.) |
| 3 | `available_actions` subset of [1..7] | ✅ PASS — spec § 5: `available_actions = [1, 2, 3, 4]`. |
| 4 | EXACTLY 3 `Level(...)` entries | ✅ PASS — spec § 4 has exactly L1/L2/L3 sub-sections. |
| 5 | Game ID = 4 lowercase alnum, not in reserved, not in prior-games | ✅ PASS — `mw8p` verified non-colliding in `mechanic-pick.md` and re-checked against both `prior-games/index.md` (80 rows) and the prior-games subdirectory listing. |

## §3.4 priors & constraints (items 6–10)

| # | Item | Verdict |
|---|---|---|
| 6 | Mechanics draw only from `core-knowledge-priors.md` | ✅ PASS — spec § 2: objectness (persistent creatures/walls) + agentness (B/C pursuit). No physics, no geometry/topology. |
| 7 | No letters, digits-as-glyphs, clipart, cultural conventions | ✅ PASS — sprite roster (§ 3): creatures are abstract shapes with eyes/spikes/leaves (no letter-shapes, no digit-shapes); wall is masonry texture; exit is ring with white cross-inset (topological symbol, not a glyph). HUD step bar is a colour fill (no digits). |
| 8 | At least TWO distinct mechanics | ✅ PASS — three mechanics: M1 (B-chases-A), M2 (C-chases-B-and-kills), M3 (A-eats-C). |
| 9 | L1 is a tutorial: base dynamic system, reduced state space, no on-screen text | ✅ PASS — L1 has one mechanic (M1), three-zone walled layout with B confined to middle chamber, no on-screen text. The witness is solvable in 14 actions with a 25-step budget. |
| 10 | L2 & L3 compose every mechanic available at that level | ✅ PASS — L2's witness exercises BOTH M1 (B's pursuit fires every turn) AND M2 (C kills B on turn 1, without which A loses by turn 8). L3's witness exercises M1 (B's pursuit on turn 1 positions B for M2), M2 (C₂ kills B on turn 1), AND M3 (A eats C₁ on turn 1 — the only legal first move). |

## Mechanic structure: items 11 + 12

### Item 11 (mechanic inheritance + 1-or-+2 per level)

| Level | Witness-required mechanics | Count | Delta vs previous |
|---|---|---|---|
| L1 | M1 | N = 1 | — |
| L2 | M1 + M2 | N+1 = 2 | +1 (M2 introduced) |
| L3 | M1 + M2 + M3 | (L2-count)+1 = 3 | +1 (M3 introduced) |

✅ PASS — every earlier mechanic remains present and required at
every later level (M1 fires every turn at L2 and L3 as well; M2
fires at L3 the same way it does at L2). No mechanic drops out.
Each promotion adds exactly 1 new mechanic (≤ 2 allowed).

### Item 12 (strict counterfactual necessity — per-mechanic table)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 | **no** | B's pursuit step rule runs unconditionally on every action; the 14-action witness triggers M1 14 times. M1's lose-on-same-cell branch is an active constraint on every turn (A cannot enter B's then-current cell). |
| L2 | M1 | **no** | Pursuit rule fires every turn (same as L1). Additionally, M1's pursuit is what positions B at (4, 4) on turn 1 — the cell C catches B at via M2; without M1's pursuit (a static B at (4, 5)), C would still catch B (at (4, 4) on turn 2), but the level's threat (B catching A) only exists because of M1's pursuit half. |
| L2 | M2 | **no** | Without M2's removal-of-B-on-C-entry: B continues chasing A. Counterfactual trace: turn 1 A→(1, 0), B→(4, 4), C steps to (4, 4) but cannot remove B (M2 disabled) — C ends at (4, 3) blocked. Turn 2: B→(5, 3). Turn 3: B→(5, 2). Turn 4: B→(5, 1). Turn 5: B chase A (5, 0). dx=0, dy=-1, B→(5, 0)=A → lose. So M2 must fire on turn 1 (C at (4, 3) → (4, 4) = B's post-pursuit cell). |
| L3 | M1 | **no** | Pursuit fires every turn (same as L1/L2). M1's pursuit also moves B from (5, 7) to (4, 7) on turn 1, which is the cell C₂ catches B at via M2; M2 cannot fire without M1's pursuit half. |
| L3 | M2 | **no** | Without M2: B at (4, 7) is not removed on turn 1. Counterfactual: turn 1 A → (1, 7) (M3 fires, C₁ eaten); B → (4, 7); C₂ tries (4, 7), blocked by B, stays at (3, 7). Turn 2: A → (2, 7); B chase (2, 7), dx=-2 horizontal → (3, 7) blocked by C₂, dy=0 no fallback, B stays at (4, 7); C₂ chase B horizontal → (4, 7) blocked, stays. Turn 3: A's options from (2, 7): (3, 7)=C₂ (M3 fires consuming C₂; A→(3, 7)), (1, 7) backward, (2, 6) wall, (2, 8) OOB. After eating C₂: A at (3, 7); B chase A (3, 7), dx=-1, B → (3, 7) = A → lose. So M2 must fire on turn 1. |
| L3 | M3 | **no** | A's four cardinal neighbours from (0, 7): (1, 7) = C₁ (only enterable via M3); (-1, 7) OOB; (0, 6) wall; (0, 8) OOB. Without M3, A has zero legal moves and the action sequence either consists of all blocked moves (which still consume step budget, eventually firing the lose-on-budget rule) or trips a runtime exception on step(). M3 must fire on turn 1. |

### Verification by enumeration (per item 12 "verify by enumeration, not abstraction")

**L1 alternate strategies enumerated:**
- "Walk straight up col 0": (0, 7) → (0, 6) blocked by wall (row 6 col 0 is in the row-6 wall span 0..6). Fails immediately.
- "Walk LEFT from (0, 7)": OOB. Fails.
- "Walk DOWN from (0, 7)": OOB. Fails.
- "Walk RIGHT then UP via col 5 or earlier": (5, 7) → (5, 6) blocked by wall (row 6 cols 0..6). Forces continuing RIGHT.
- The 7-RIGHT-then-7-UP witness is the unique 14-action shortest sequence.

**L2 alternate strategies enumerated:**
- "DOWN-first": A → (0, 1). B's pursuit dx=-4, dy=-4, tie→x → (3, 5). C's pursuit to B(3, 5): dx=-1, dy=2, vertical → (4, 4). C did not land on B; M2 does not fire. By turn 5, A → (0, 5)=B → lose. **Loses without firing M2.**
- "LEFT-first": OOB. Blocked.
- "UP-first": OOB. Blocked.
- "RIGHT-then-diagonal-zigzag": A → (1, 0) (M2 fires turn 1, B killed). Then any path of 13 more moves reaching (7, 7) wins; the shortest is 7-RIGHT-then-7-DOWN (or any permutation of 6-RIGHT-7-DOWN since one RIGHT is already used). The committed witness is one such shortest sequence.
- "Walk through C's cell at (4, 4) to eat it": adds at least 4 detour moves (must descend to row 4 then return). Not shortest. Witness doesn't pass through (4, 4).

**L3 alternate strategies enumerated:**
- Any non-RIGHT first action: blocked (wall, OOB, or backwards-no-progress). A stays at (0, 7) consuming budget; with 35-step budget A can issue 35 blocked actions before losing. M3 never fires; A loses on budget.
- "RIGHT-first then UP at col 1": (1, 7) → (1, 6) wall. Forced RIGHT.
- "RIGHT to (3, 7), then UP": (3, 7) → (3, 6) wall. Forced RIGHT (which means eat C₂ via M3).
- "RIGHT to (7, 7), then DOWN": OOB. Forced UP.
- The 7-RIGHT-then-7-UP witness is the unique 14-action shortest sequence.

✅ PASS items 11 + 12.

## Novelty (items 13–15)

| # | Item | Verdict |
|---|---|---|
| 13 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ PASS — `predator-prey-triangle` is not listed; closest entries (tu93 maze-pickup-train, m0r0 mirrored-quad-control, ka59 sokoban-explode-chase) all distinguished via concrete distinguishing rules in `mechanic-pick.md` and re-grounded in spec § 9. |
| 14 | Mechanic family absent from `prior-games/index.md` | ✅ PASS — 80 prior entries; closest (zk9p pursuer-merge-walk, nf3z flock-flee-corral, ek73 wake-trail-evade, bw7k actor-replay-shade) all distinguished. |
| 15 | If sounds similar, concrete distinguishing rule articulated | ✅ PASS — spec § 9 cites tu93 with concrete rule (independent tick functions vs single shared pursuit rule), zk9p with concrete rule (single-species self-collision vs tri-species cyclic predation + reach-exit goal). |

### Negative-similarity re-walk on the full spec

Per `negative-similarity-check.md`'s 8-dimension grid, re-run on
the fleshed-out spec (not just the family name):

| Dim | mw8p (full spec) | zk9p (closest prior) | Shared? |
|---|---|---|---|
| 1 What's on the board | A avatar + 1 B + 1 C in L2 / 1 B + 2 C in L3 + walls + exit, on an 8-cell × 8-cell logical grid | avatar + pursuers + walls | yes (coarse) |
| 2 Player physical input | cardinal arrows only ([1,2,3,4]) | cardinal arrows only | yes |
| 3 Level goal | A reaches an exit cell | clear every pursuer | **NO** |
| 4 Lose | B steps onto A's cell | pursuer reaches player | yes (dynamic) |
| 5 Supporting cast | walls + multi-NPC + exit | walls + pursuers | yes (similar) |
| 6 Visible visual signature | maroon walls + light-blue A + orange-red B + green-pink C + purple exit + light-grey background | yellow-dominant signature | **NO** |
| 7 Pixel grain of primary sprites | 6×6 sprites with internal eye-pixels (A), spike-rim + maw (B), leaf-serration + pink core (C), masonry-cross (wall), ring + cross-inset (exit) | simpler solid shapes | **NO** |
| 8 Core dynamic | tri-species cyclic predation (A→C, B→A, C→B) modulated by walls + A-eats-C resource | single-species pursuer self-collision merging | **NO** |

Shared count: 4 (D1, D2, D4, D5) — all on LOW-weight dimensions.
**All three principle dimensions (D6, D7, D8) diverge.** Level goal
(D3) also diverges.

Verdict: per `negative-similarity-check.md` § decision rule (the
threshold is judgement, not arithmetic, and the principle
dimensions are heavier than the coarse-shape dimensions), the
candidate is NOVEL.

## Solvability (items 16–22)

| # | Item | Verdict |
|---|---|---|
| 16 | Win condition stated as a testable predicate | ✅ PASS — spec § 7: "if A's logical cell equals the level's exit cell, call `self.next_level()`". |
| 17 | Lose condition stated (or "no lose" with reasoning) | ✅ PASS — spec § 8 lists three lose paths: A walks onto B, B's pursuit lands on A's cell, step budget exhausted. |
| 18 | Difficulty floor + ceiling per `difficulty-rules.md` § Critique check (a/b/c/d per level) | ✅ PASS — spec § 4 has all four bullets for each level. L1: discovery-only / ~1 min / no strict planning / 25-step budget. L2: moderate post-discovery planning with the wrong-action-path (DOWN-first) named / ~2 min / 30-step budget. L3: trivial heuristic (greedy-distance-to-exit) named with concrete divergence point at turn 4 / ~2-3 min / 35-step budget. |
| 19 | No hidden state — every state mutation has a persistent visible cue | ✅ PASS — step counter HUD shows budget; creature positions are visible; B's pursuit direction is computed (no internal mode flag); no selection mechanic; no charge meter; A-eats-C and C-kills-B are visible removals (sprite disappears). |
| 20 | Not low-resolution — packed visible detail at the display-pixel level | ✅ PASS — uses `grid_size = (64, 64)` (camera default, no chunky upscale per `universal-scaffold.md`); each 6×6 sprite has internal pixel structure (eyes on A, spike rim + maw on B, leaf serration + pink core on C, masonry-cross on wall, ring + cross-inset on exit). Shape carries meaning beyond colour. |
| 21 | UI teaches — sprite UI ≈ sprite role, identical visuals imply correlated roles | ✅ PASS — A's eye-pixels mark it as the player (the only sprite with eye-pixels facing the camera); B's spike-rim + red marks it as dangerous (visually distinct from A); C's leaf + pink core marks it as organic-different from B; walls have masonry-cross pattern (clearly inert texture); exit has white cross-inset (marker). All B's share visuals (one species); all C's share visuals; one wall family. No cross-species visual confusion. |
| 22 | ACTION7 strict-undo or ABSENT | ✅ PASS — ACTION7 is ABSENT (`available_actions = [1, 2, 3, 4]`). No undo verb is overloaded on slot 7. |

## Overall verdict

All 22 checklist items PASS. Item 12's per-mechanic table is
explicit with concrete blocking-cell/blocking-rule justification for
every (mechanic, level) pair. Item 18's difficulty justification
has all four bullets per level. Novelty re-confirmed against
taxonomy + prior-games (positive similarity) and against the
8-dimension negative-similarity test on the full spec.

**Transition: `implement`.**
