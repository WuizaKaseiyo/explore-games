# Critique pass — round 2

| Check | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Palette 0..15 + `-1` only | ✅ PASS | All sprites use only 3, 4, 8, 10, 11, 12, 14 + `-1`. |
| 2 | Universal scaffold | ✅ PASS | Spec describes the imports → sprite bank → levels → constants → HUD widget → game class structure per `code/universal-scaffold.md`. |
| 3 | `available_actions ⊆ [1..7]` | ✅ PASS | Subset = `[3, 4, 5, 6]`. |
| 4 | Exactly 3 levels | ✅ PASS | L1, L2, L3 specified per `composition-and-tutorial.md`. |
| 5 | 4-char ID, no collision | ✅ PASS | `pn5d`, lowercase, alphanumeric, not in 25 reserved, not in 49 priors. |
| 6 | Mechanics from §3.4 priors | ✅ PASS | basic physics + basic geometry/topology + objectness — three of the four allowed. |
| 7 | No letters / digits / clipart / cultural | ✅ PASS | `valve_closed` is now solid grey (no X glyph); `pour_cursor` is now a hollow square ring (no directional arrow). All other sprites are abstract rectangles, pips, lips, fills. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | 3 mechanics across the environment (M1 pour, M2 toggle, M3 cap). |
| 9 | L1 tutorial (reduced state space) | ✅ PASS | 2 vessels, 1 fixed-open valve, no toggle, no cap; only M1 active. |
| 10 | L2/L3 increase difficulty by composition | ✅ PASS | L2 adds toggle; L3 adds cap, both composing with prior mechanics rather than scaling grid or item count. |
| 11 | +1-or-+2 per level inheritance | ✅ PASS | L1=1, L2=2 (=L1+1), L3=3 (=L2+1). All earlier mechanics carry forward. |
| 12 | Strict counterfactual necessity | ✅ PASS | Per-mechanic table (below). All rows "no", each with a concrete blocking reason. L3 alternates enumerated 1-8; only 1 and 2 bypass M3, and both exceed the 20-action budget. |
| 13 | Mechanic family absent from taxonomy | ✅ PASS | `vessel-equalize-flow` not in any of the 25 reference rows. |
| 14 | Absent from `prior-games/index.md` | ✅ PASS | Not in any of the 49 priors. |
| 15 | Distinguishing rule for near-misses | ✅ PASS | sp80 (droplet-routing vs. volume-distribution), kx14 (one-tank-one-surface vs. multi-vessel-pour-equalize), lv4k, kp9z, kn58, vd3g — concrete rules per row. |
| 16 | Win condition predicate | ✅ PASS | `all(v.level == v.target for v in self._vessels) → next_level()`. |
| 17 | Lose condition predicate | ✅ PASS | `_action_count >= _max_steps and not all_targets_met → lose()`. |
| 18 | Difficulty floor and ceiling | ✅ PASS | Every level has (a) random-resistance, (b) human time, (c) planning depth, (d) step budget. L2 and L3 planning-depth justifications are concrete (named heuristics that fail, named wrong paths, witness reasoning chains). |
| 19 | No hidden state | ✅ PASS | Cursor position visible via `pour_cursor` sprite; valve state visible via `valve_open`/`valve_closed` swap; liquid level visible via `liquid_fill` band; cap visible via `overflow_cap` lip; target visible via `target_mark` pip. |
| 20 | Not low-resolution | ✅ PASS | 64×64 native grid; sprite internal detail (1-pixel walls, 2-3 pixel pips/lips, 4-pixel valves, 12-pixel fill bars). Adequately detailful; not chunky upscaled cells. |
| 21 | UI teaches (sprite UI ≈ role) | ✅ PASS | Open-top rectangles read as containers; bottom-up liquid bands read as liquid; same-shape-different-colour valve pair signals correlated states; inward pip vs. outward lip differentiates target vs. cap visually. |
| 22 | ACTION7 strict undo or absent | ✅ PASS | ACTION7 not in `available_actions=[3,4,5,6]`. |

## Per-mechanic counterfactual table (per checklist item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (pour) | **no** | ACTION5 is the only verb that mutates surfaces; ACTION3, 4, 6 are inert at L1 (only one fixed-open valve, no toggle). Both surfaces stay 0 without M1. |
| L2 | M1 (pour) | **no** | All three vessels start at 0; only ACTION5 raises surfaces. Targets non-zero (3, 2, 5). |
| L2 | M2 (valve toggle) | **no** | Both valves start OPEN ⇒ initial group `{A, B, C}`. With this group, every ACTION5 raises all three surfaces by exactly 1 — the three surfaces cannot reach distinct heights (3, 2, 5) without disconnection. ACTION6 is the only verb that disconnects. |
| L3 | M1 (pour) | **no** | All four vessels start at 0; targets non-zero (9, 9, 2, 9); only ACTION5 raises surfaces. |
| L3 | M2 (valve toggle) | **no** | All three valves start CLOSED; the closed-only strategy costs 32 actions = 9 (A) + 1 cursor + 9 (B) + 1 cursor + 2 (C) + 1 cursor + 9 (D), exceeding the 20-action budget. At least one ACTION6 toggle is required to fit the budget. |
| L3 | M3 (overflow cap) | **no** | Of the 8 plausible alternate strategies enumerated (all-closed; open A-B only; open A-B and B-C; open A-B and C-D; open B-C only; open B-C and C-D; open C-D only; open all), only **all-closed** (32 actions) and **open A-B only** (24 actions) bypass M3. Both exceed the 20-action budget. The remaining six all require M3 to clip C as the connected group rises past row 2 — without M3, those strategies are impossible (C's surface is tied to the group). |

## Novelty

- Taxonomy similarity-check: NOVEL. No reference game uses connected-vessel volume-distribution.
- Prior-games similarity-check: NOVEL. Closest priors (kx14 single-tank, sp80 droplet-routing) have concrete distinguishing rules; no other prior approaches the family.
- Negative similarity check: 8-dimensions walk passes — no prior overlaps on three or more dimensions.

## Verdict

**ALL CHECKS PASS.** Transition to `implement`.
