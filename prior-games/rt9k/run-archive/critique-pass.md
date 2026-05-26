# Critique pass — `rt9k`

Reviewed `mechanic-spec.md` against `design-constraints/checklist.md`
items 1-22 + similarity-check + negative-similarity-check.

## Checklist

- ✅ **1. Palette 0..15.** Sprites use {1, 3, 5, 6, 11, 14} plus −1 transparent. All within range.
- ✅ **2. Universal scaffold.** Spec's §3, §5, §6 describe sprite bank + Camera + StepCounterHud + Game class — matches `code/universal-scaffold.md`. (Final structural verification at `implement`.)
- ✅ **3. `available_actions ⊂ [1..7]`.** Spec §5 declares `[1, 2, 3, 4]`.
- ✅ **4. Exactly 3 levels.** Spec §4 lists L1, L2, L3 explicitly; no other level entries.
- ✅ **5. ID is 4-char lowercase, opaque, non-colliding.** `rt9k` (4 chars, lowercase, alphanumeric, not in 25 reference IDs, not in indexed prior-games, not in unindexed prior-games — verified at `pick_mechanic`).
- ✅ **6. Mechanics from §3.4 prior categories only.** Spec §2 names *geometry/topology* (torus surface) + *objectness* (avatar/wall/filter/goal). No physics, no agentness. All within §3.4.
- ✅ **7. No letters/digits/clipart/cultural conventions.** Sprite roster: avatar (4×4 ring with black core), wall_solid (4×4 textured square), filter_<tone> (4×4 black frame + tone inner), goal_plain (4×4 grey-frame + black core), goal_yellow (4×4 yellow-frame + black core). None resemble letters, digits, real-world objects, or cultural symbols (no green=go, no red=danger; tones are arbitrary palette values used consistently as identifying tags).
- ✅ **8. ≥ 2 mechanics.** L2 has 3 mechanics (M1 wrap, M2 tone-cycle, M3 filter); L3 has 4 (+ M4 goal-tone).
- ✅ **9. L1 is tutorial.** L1 establishes M1 (torus wrap) alone, with reduced state (single solid wall, single goal, no filters, no tone-mechanic). No on-screen text.
- ✅ **10. L2/L3 difficulty via composition, not scaling.** L2 keeps L1's mid-wall + adds tone-cycle + filter; L3 keeps L2's layout + adds yellow filter band + goal-tone gate. Grid size constant across levels (16×15 logical); no scaling-up of single mechanic.

- ✅ **11. Mechanic inheritance and +1-or-+2 rule.** Spec §4 explicitly enumerates per-level required mechanics:
  - L1 N=1 (M1).
  - L2 N+2 = 3 (M1 carried + M2, M3 added).
  - L3 = L2-count + 1 = 4 (M1, M2, M3 carried + M4 added).
  Every earlier-level mechanic remains required at every later level (re-stated in each level's necessity block, not inherited by reference). Both deltas (+2 then +1) are within the +1-or-+2 envelope.

- ✅ **12. Strict counterfactual necessity.** Per-mechanic table:

  | Level | Mechanic | Solvable without M? | Why not (concrete) |
  |---|---|---|---|
  | L1 | M1 wrap | no | `wall_solid` column at logical col 8 spans every row 0..14 (15 cells, no gap). Avatar at col 4 cannot reach col 11 by any interior path; the only route is to walk LEFT off col 0, re-enter at col 15, and walk left to col 11. |
  | L2 | M1 wrap | no | Same wall_solid full-height column at col 8 — only path from left half (cols 0..7) to right half (cols 9..15) is via wrap. |
  | L2 | M2 tone-cycle | no | `filter_green` at col 14 spans rows 0..14; passing requires green tone. Avatar starts magenta and tone changes only at wrap-cross. Therefore reaching col 13 requires both a wrap and the tone-cycle that wrap entails. |
  | L2 | M3 filter walls | no | Col 14 is `filter_green` for every row 0..14 contiguously. Every path from col 15 (post-wrap landing) to col 13 (the goal column) passes through col 14 — there is no row in which col 14 is open terrain. |
  | L3 | M1 wrap | no | Mid-wall at col 8 spans rows 0..14 (same as L1/L2) — wrap is the only route to the right half. |
  | L3 | M2 tone-cycle | no | The filter_green at col 14 demands tone=green to pass (one tone change), AND the goal-tone gate at (13,7) demands tone=yellow to win (a second tone change). Two distinct tone values in the same run requires ≥ 2 tone changes; tone changes only occur at wrap-crosses. |
  | L3 | M3 filter (green) | no | Col 14 spans rows 0..14 contiguously; reaching col 13 from col 15 requires entering and exiting (14, r) with tone=green for some r. No interior bypass exists. |
  | L3 | M3 filter (yellow) | no | The yellow-tone goal at (13,7) requires tone=yellow at arrival. The only way to end at (13,7) tone=yellow is to wrap UP from (13,0) to (13,14), which lands inside `filter_yellow`. Any alternative — e.g., wrapping into (col, 14) for col in 9..14 — also lands in a filter_yellow cell. Routing via col 15 is infeasible because re-crossing col 14 from the col-15 side requires green tone, which then has to be re-cycled to yellow — a cycle that necessarily passes through one of the filter_yellow cells in cols 9..14 row 14. Filter_yellow is therefore on every winning path. |
  | L3 | M4 goal-tone | no | Without M4, the 4-step LEFT-wrap path lands the avatar on (13,7) with tone=green, and a tone-blind goal would auto-win there. The spec's witness explicitly demonstrates that goal-tone refuses this arrival and forces the player to wrap-cycle further. |

  Plausible alternates checked: (i) DOWN-first wrap (L2): tone goes magenta→yellow, fails to pass green filter, player re-wraps — exercises M3 anyway. (ii) UP-first wrap (L2): tone goes magenta→green at (col, 14), but col 8 still blocks horizontal traversal, requiring an additional wrap. (iii) L3 "wrap-LEFT-and-walk" greedy heuristic: stops on goal cell with tone=green; the goal-tone gate refuses; the player must wrap further. Each alternate's failure is concretely traceable to a specific cell or rule named above.

- ✅ **13. Mechanic family absent from taxonomy.** `torus-wrap-tone-cycle` does not match (family-level or first-two-words-of-hyphen-split) any of the 25 reference families.
- ✅ **14. Mechanic family absent from prior-games.** Re-checked against indexed (64 entries) and unindexed (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n) prior-games. No torus or wrap-edge mechanic exists.
- ✅ **15. Concrete distinguishing rule for sound-similar near-misses.** §9 of spec articulates rules vs m0r0, g50t, bp35 (taxonomy) and pk4m, lz7q, gh4r, wt39, bz3k, jd4q, ek73 (prior-games). pk4m is the closest; the spec's distinguishing rule cites three concrete differences (no in-cell tone toggle, three-tone vs two-tone modular arithmetic, pure-arrows action set vs ACTION5 toggle). Verified against pk4m's mechanism-detail.

- ✅ **16. Win condition stated.** Spec §7 gives a testable predicate: avatar position equals a goal sprite's position AND (for L3) avatar tone equals goal tone. After L3 wins, base class auto-fires `self.win()`.
- ✅ **17. Lose condition stated.** Spec §8: `_steps_remaining == 0` after a step → `self.lose()`. No soft-lock per `difficulty-rules.md` § 1: tone is recoverable from any state in 1 wrap, no irreversible mutations.

- ✅ **18. Difficulty floor and ceiling.** Per `difficulty-rules.md` § 3 critique check, all four bullets present per level:
  - L1: (a) random-resistance ~1/10^5 over 9-step budget; (b) ~30–60s human; (c) **no strict planning** (correct for L1); (d) `step_budget=30`.
  - L2: (a) ≪ 1/10000 random; (b) ~2 min human; (c) **moderate planning** with explicit decision-space (count = 2; ≥ 2 ✓), one named plausible-but-wrong (DOWN-first → wrong tone), and witness reasoning chain referenced post-discovery; (d) `step_budget=50`. Stage-conflation guard: the named wrong path is post-discovery (the player understands the filter rule but picks the wrong wrap *despite* knowing).
  - L3: (a) ≪ 1/10^9 random; (b) ~2.5 min human; (c) **challenging planning** with decision-space ≥ 2 (≥ L2's ✓), trivial heuristic that fails ("walk shortest geometric path through wrap" — stops on goal cell with wrong tone), and the heuristic's divergence from witness named at step 4; (d) `step_budget=70`, strictly ≥ L2's 50 ✓ (per the L3 must-not-shrink rule). Stage-conflation guard: the failing heuristic is post-discovery (the player has read the goal's tone ring; their failure is in the planning, not in the discovery).

- ✅ **19. No hidden state.** Avatar's tone is rendered on the avatar via `color_remap` after every tone change — visible cue persists for as long as the state is in effect. Steps remaining are visible via `StepCounterHud`. No internal-only state (selection, mode, lock) is mutated by an action without a visible cue.

- ✅ **20. Don't generate low-resolution game.** Spec uses 64×60 playfield (logical 16×15 with stride 4). Sprites are 4×4 with internal patterns:
  - avatar: 4-cell ring with transparent corners + black centre — has internal structure beyond flat colour.
  - wall_solid: black outer + grey inner — distinct from filter walls.
  - filter_<tone>: black frame + 2-pixel tone-coloured inner — readable as "wall but with inset colour".
  - goal_plain / goal_yellow: tone-coloured outer ring + black core — inverted-ring signature distinguishes goal from filter.
  Three distinct sprite *shapes* (corner-cut ring, full-square, ringed-outer-tone, ringed-outer-black) plus three tone hues — palette + shape both carry meaning. The L1 frame reads as a deliberate composition (avatar, single tall wall, distinct goal sprite) rather than coarse blocks.

- ✅ **21. UI teaches.** Operational test: an L1 screenshot shows a magenta avatar on the left, a tall vertical black-and-grey wall, and a grey-ringed bullseye on the right.
  1. *Sprite UI ≈ sprite role.* Avatar is the only ring-shaped object → reads as the controllable thing. Wall is a contiguous tall block → reads as obstacle. Goal is a bullseye → reads as target.
  2. *Identical visuals → correlated roles.* Filter walls share colour-coding with the goal-ring (both use the tone palette {6, 11, 14}); a player who learns "yellow ring on a filter means yellow tone passes" can read off "yellow ring on the goal means yellow tone is required". Solid walls have no tone-colour (only black + grey) so they read as a distinct family.
  3. *Visual carries the mechanic.* Wrap is the one mechanic that has no static cue — it is discoverable only by walking off the edge. Per `from-tech-report.md` § 4 the "no instructions" principle accepts discoverability through a small number of exploratory actions; the wrap is reproducibly discovered after at most 2-3 LEFT presses against the playfield's left edge. No source-reading required.

- ✅ **22. ACTION7 strict-undo or absent.** Spec §5 declares `available_actions = [1, 2, 3, 4]`. ACTION7 is not listed; the slot is unused (no overload).

## Novelty re-check on full spec

Re-ran `similarity-check.md` § 2 description-level test against
every taxonomy entry and every prior-games entry, this time on the
fleshed-out spec (not just family name). For each entry:
win condition, primary action, primary constraint were compared.

- No row matches all three of (win = "reach goal cell with required tone via cumulative-wrap-arithmetic", action = "4-cardinal walk only", constraint = "edge-wrap is the sole tone-changing event").
- Closest taxonomy match: m0r0 (multi-avatar mirrored axes) — different in cast (4 avatars vs 1) AND in axis-effect (mirrored input vs topological wrap).
- Closest prior-games match: pk4m (duotone-flip-walk) — different in tone arity (3 vs 2), tone-change verb (edge-wrap-only vs ACTION5-toggle-or-pad), and action set (`[1..4]` vs `[1..5]`).

Verdict: NOVEL.

## Negative similarity re-check on full spec

Re-walked the seven dimensions in
`negative-similarity-check.md` against pk4m (closest), kn58
(magnet pull), nf3z (flock corral), m0r0, lz7q. For each,
`rt9k`'s shared-with-prior count remained ≤ 4, with the divergent
dimensions including 6 (visual signature), 7 (pixel grain), and 8
(core dynamic) — the weighted-heavy axes per the rule. The
fleshed-out spec did not drift toward any prior on these heavy
axes.

Verdict: PASS the negative test.

## Overall

All 22 checklist items + similarity + negative-similarity:
**PASS.**

Transitioning to `implement`.
