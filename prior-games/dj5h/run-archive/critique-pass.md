# Critique pass — dj5h

Independent adversarial review of `mechanic-spec.md` against `skills/design-constraints/checklist.md` (items 1-22) plus the novelty checks.

## Checklist

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette only 0..15 (and -1 transparent) | ✅ PASS | Spec uses palette values 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14 — all in range. `-1` reserved for transparent in `pulley_halo` interior. |
| 2 | File structure matches universal scaffold | ✅ PASS | Spec describes the structure and orders sprites → levels → constants → HUD → game class. Implementation will follow `code/universal-scaffold.md`. |
| 3 | `available_actions` ⊆ [1..7] | ✅ PASS | `[1, 2, 3, 4, 5, 6]` — 6 of 7 slots. ACTION7 omitted per item 22. |
| 4 | EXACTLY 3 Levels with composition structure | ✅ PASS | L1 (base 3-mech), L2 (+1 = 4), L3 (+1 = 5). Per `composition-and-tutorial.md`. |
| 5 | 4-char lowercase ID, not in reserved or prior-games | ✅ PASS | `dj5h`. Verified against 25 references and 60 priors. |
| 6 | Mechanics from core priors only | ✅ PASS | Basic physics (rope conservation), objectness (platforms/pegs/sockets/walls/cables), basic geometry & topology (walkable graph reshapes per state). |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS | All sprites are abstract: spoked wheel (mechanism, not letter), rectangular slab platform (no glyph), humanoid avatar (no recognisable iconography), 2×2/3×3 pegs (round nubs), recessed-pad socket, vertical-bar wall, dot-polyline cable, concentric-ring goal. Yellow rivet pattern on the beam is dot-decoration repeating every 8 cells — not a glyph. |
| 8 | At least 2 distinct mechanics | ✅ PASS | 3 in L1, 4 in L2, 5 in L3. |
| 9 | L1 tutorial = base dynamic system, reduced state, no on-screen text | ✅ PASS | 1 pulley, 2 platforms, 1 wheel, 1 goal. No HUD beyond the universal step counter. No text. |
| 10 | L2/L3 increase difficulty by composition (not scaling) | ✅ PASS | L2 adds peg-and-socket — composes with L1's pulley toggling (peg-on-socket removes a wall AND requires platform-LOW state to be reachable). L3 adds cable-linkage — composes with everything (the cable-toggle is the only way to reach the L3 goal, AND the player must seat the peg before toggling because the toggle moves PA's blue HIGH, hiding the socket). |
| 11 | Mechanic inheritance and +1-or-+2 per promotion | ✅ PASS | L1 = 3 mechanics (M1 walk, M2 select, M3 toggle); L2 = 4 (+1: M4 peg-and-socket); L3 = 5 (+1: M5 cable-linkage). Every earlier mechanic carried forward and witness-required. |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ PASS | Spec includes per-mechanic per-level counterfactual sentences naming concrete cells/sprites/rules that block alternates. **Plus** independent enumerations of plausible alternate strategies (5 for L2, 6 for L3) with concrete walks showing each fails. The L3 design was iterated mid-spec to make M5 genuinely required: opposite-phase cable coupling forces the C→D bridge to depend on a cable-toggle that simultaneously inverts PA — sequencing the peg-drop *before* the cable-toggle is the unique winning ordering. |
| 13 | Mechanic family absent from taxonomy | ✅ PASS | No taxonomy entry shares (a) coupled vertical motion between paired surfaces, (b) walking on those surfaces, (c) click-then-ACTION5 to toggle pair-state. Closest near-misses (m0r0, kj82, pv5q) addressed in §9 with concrete distinguishing rules. |
| 14 | Mechanic family absent from prior-games | ✅ PASS | 60 priors enumerated; closest (pn5d/xv2b vessels, kn58 anchor-pull, mr5q polarity, vt6q grapple, wb6n tether, gx7m gear-mesh) addressed in §9 with distinguishing rules. **gx7m** is borderline (sign-flip propagation across cardinal mesh ↔ opposite-phase cable coupling); distinguished by **scope**: gx7m propagates rotations across a 2D mesh of many gears with ratchet gates; dj5h's cable couples *exactly two* pulleys in a single binary opposite-phase relation. |
| 15 | Distinguishing rule for any near-miss | ✅ PASS | Concrete rules quoted in §9 for every near-miss in both corpora. |
| 16 | Win condition stated | ✅ PASS | `_check_win()` uses avatar foot-pixel inside `goal_marker` footprint → `next_level()`. After L3, engine fires `win()`. |
| 17 | Lose condition stated | ✅ PASS | `_action_count >= step_budget` → `lose()`. Pit cells unwalkable (move-rejection), not fatal. |
| 18 | Difficulty floor and ceiling per level (a-d bullets) | ✅ PASS | All four bullets present per level. L1 (a) 1-in-270k random-policy bound, (b) ~1.5 min, (c) no-strict-planning, (d) budget=30 (5× witness 6). L2 (a) joint sequence under 1/10 000, (b) ~3 min, (c) decision space ≥ 4 with named wrong-alternative ("toggle PA before walking" = lost steps) and reasoning chain, (d) budget=80 (5× witness 16). L3 (a) joint product bound below 1/10 000, (b) ~3 min, (c) decision space ≥ 5 with named heuristic-that-fails ("greedy-toward-goal" diverges at action #1 and ~#22 from witness), (d) budget=150 (5× witness ~30). Budgets non-shrinking (30 → 80 → 150). |
| 19 | No hidden state — visual cue per mutated state | ✅ PASS | Active pulley → orange `pulley_halo`; pulley state → platform row positions in the rendered frame; carrying → `avatar_carry_<colour>` head re-tint; seated pegs → `peg_seated_<colour>` at socket + wall absence; cable pairs → `cable_link` polyline. All persistent and frame-readable. |
| 20 | Don't generate a low-resolution game | ✅ PASS | grid_size=(64, 64) for all levels; no upscaling. Every gameplay-relevant sprite has internal pixel pattern: pulley_wheel (spokes + ring + centre), platforms (3 pips on bottom row, maroon top-edge), avatar (head/body/feet bands + belt), floor_block (body/speckle/shadow), wall_block (edges + maroon stripe), pegs (body + highlights + outline), socket (recessed-pad ring + corners + centre), goal_marker (concentric rings), beam (rivet pattern), pit_void (cross-hatch dots). |
| 21 | UI teaches via visuals (sprite UI ≈ role) | ✅ PASS | Each sprite role is articulated and the visual register matches: pulley_wheel reads as a mechanism, platform reads as a walkable slab, avatar reads as a humanoid character, peg reads as a small carryable, socket reads as a receptacle, wall reads as a barrier, cable_link reads as a connecting line, goal_marker reads as a target. Coloured-paired correlations (red/blue/green platform pairs match colours of pegs and seated pegs) imply role correlations. The cable polyline crossing-over near PB visually telegraphs the opposite-phase coupling. |
| 22 | ACTION7 strict-undo or absent | ✅ PASS | ACTION7 absent. Spec §5 explicitly notes the omission and the rationale (binary toggle is its own inverse — ACTION5 again is the natural undo). |

## Novelty re-check on the fleshed-out spec

Per `mechanic-novelty/similarity-check.md` and `negative-similarity-check.md`, re-walked the eight dimensions of the negative test against the closest priors (m0r0, kj82, pv5q, pn5d, xv2b, kn58, mr5q, vt6q, wb6n, gx7m). Maximum shared dimensions with any single prior: **2 of 8** (universal step-budget kill plus one of board-element / sprite-cast). Required threshold is < 3. **Verdict: NOVEL.**

Specific re-checks for L2 / L3 drift:
- L2's peg-and-socket-removes-wall idiom does NOT appear in any prior. ds5q's "charge colour at pads to chip walls" is the closest but uses a charge-and-walk-against-wall verb (very different from carry-and-deposit-on-socket). No 3+ dimension overlap with ds5q.
- L3's opposite-phase cable coupling is structurally distinct from gx7m's gear-mesh (gx7m: many gears in 2D arrangement, sign-flip propagation across cardinal mesh, ratchet gates; dj5h: exactly 2 pulleys in 1 cabled pair, single-flip propagation, no gates). Distinguishing rule is the *scope* (2-pair binary coupling vs N-gear mesh propagation).

## Final verdict

**PASS** on all 22 checklist items + novelty checks. Proceed to `implement`.

Note for implementation: the spec's witness solutions name approximate column-coordinates and acknowledge that exact pixel-precise alignment is finalised in implementation. The implementation must produce witnesses that pass `CHECK_WITNESS_WINS` in smoke-test (the named witness must actually advance the level). Tightening the geometry (island column boundaries, socket centre cell, wheel display-pixel coords) is on the implement state.
