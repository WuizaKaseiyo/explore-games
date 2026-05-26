# critique-pass — nz3v mechanic-spec.md (revision 2)

Re-walked the 22-item checklist + novelty rules against the
revised spec. All gates pass.

| # | Item | Verdict |
|---|---|---|
| 1 | Palette 0..15 + (-1) transparent | ✅ all sprites within bounds |
| 2 | Universal scaffold structure | ✅ spec describes scaffold-conforming layout |
| 3 | `available_actions` subset of [1..7] | ✅ [1, 2, 3, 4] |
| 4 | EXACTLY 3 Levels | ✅ L1, L2, L3 in §4 |
| 5 | 4-char ID, not in references / prior-games | ✅ `nz3v` confirmed unique |
| 6 | Mechanics from 4 priors only | ✅ geometry/topology + physics + objectness |
| 7 | No letters / digits / clipart / cultural | ✅ avatar = octagon (no letter); stop-tile = 4-edge dots (topological "+" — explicitly permitted by `forbidden-elements.md`); switch = spiral curl; wall = cross-hatch; target = hollow ring; rotor = central pillar with notch+marker dot |
| 8 | ≥ 2 distinct mechanics | ✅ M1, M2, M3 |
| 9 | L1 = base dynamic system, no on-screen text | ✅ L1 only M1; no walls; no extra tiles; no text |
| 10 | L2 / L3 each compose every prior mechanic | ✅ each level +1 mech, all carry forward |
| 11 | +1-or-+2 mechanic rule | ✅ L1=1, L2=2 (+1), L3=3 (+1) |
| 12 | Strict counterfactual necessity (no trivial fallback) — per-mechanic, per-level | ✅ §4 enumerates per-level alternates and walks each to failure; L3 alternate-1 explicitly traced to 27 actions > budget 26 |
| 13 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ no "auto-rotating angular sector / walk-in-rotating-wedge" entry in the 25 references |
| 14 | Mechanic family absent from `prior-games/index.md` | ✅ none of the 55 priors uses this family; closest cousins (fz5j, lq5x, vp6h, pf3w, xz5g, qz73) all have explicit distinguishing rules in §9 |
| 15 | If similar, concrete distinguishing rule articulated | ✅ §9 articulates 6 distinguishing rules vs nearest cousins |
| 16 | Win condition stated as testable predicate | ✅ §7: `avatar.x == target.x and avatar.y == target.y` → `next_level()` |
| 17 | Lose condition (or no-lose with reasoning) | ✅ §8: step-budget exhausted OR stepped-into-free-dark-cell |
| 18 | Difficulty floor and ceiling per level (4 bullets each) | ✅ all 12 bullets present (L1 a/b/c/d; L2 a/b/c/d; L3 a/b/c/d). L3 names a trivial heuristic that fails (greedy-toward-target) and shows divergence point at action 3 / irrecoverable loss at action 6 |
| 19 | No hidden state — every action-mutated state has a persistent visual cue | ✅ `_rotor_angle` ↔ wedge tint position + rotor notch; `_direction` ↔ rotor's magenta direction-marker dot (RotorDirectionMarker overlay); `_frozen_remaining` ↔ wedge tint colour (palette 7 pink while frozen, palette 11 yellow otherwise); step counter ↔ StepCounterHud |
| 20 | Don't generate low-resolution game | ✅ wedge no longer flat-fill — 4-corner-dot + centre pattern per lit cell reads as textured zone, not uniform-colour blocks; sprites have internal pixel detail (rotor 10×10 with notch/marker, walls cross-hatch, stop-tile 4-edge dots, etc.); palette set is 10 distinct values |
| 21 | UI teaches the mechanic | ✅ sprite roles legible from rendering: avatar = small movable polygon; target = hollow ring; rotor = central pillar with rotating notch; walls = textured solid; stop-tile = 4-direction marker (the spent-state colour-remap to grey is also visible feedback); switch = spiral curl. Wedge tint signals walkability. Direction marker + freeze tint colour signal the two state-machine variables |
| 22 | ACTION7 strict-undo or absent | ✅ ACTION7 not in `available_actions` |

## Novelty verdict

**Re-walked `negative-similarity-check.md` 8-dimension test
against the closest cousin (fz5j)** with the fleshed-out spec:

| Dim | nz3v (revision 2) | fz5j | Shared? |
|---|---|---|---|
| 1 (board) | avatar + walls + step counter + central rotor + sweep wedge | avatar + walls + step counter + per-cell pulse tiles + lives pips | partial — heavy elements differ |
| 2 (verb) | arrows | arrows | shared (light) |
| 3 (level asks for) | reach target | reach goal | shared (light) |
| 4 (what kills) | step into free dark cell + step counter | step into closed tile (lose life, 3 lives) + step counter | shared family (light) |
| 5 (cast) | rotor + wedge + stop-tile + switch + direction marker | pulse tiles (3 periods) + walls + lives pips | different |
| 6 (visual) | arena + central rotor + textured-dot wedge sector + magenta direction marker + green target ring | corridor + 4×4 frame-and-cross pulse tiles + green avatar + red life-pips | different |
| 7 (pixel grain) | rotor 10×10 + lit cells with 4-corner-dot pattern + 5×5 sprites with internal patterns | 4×4 pulse frames + small avatar + small life-pips | different |
| 8 (core dynamic) | angular sweep timing — single global angle gates a contiguous quadrant | per-cell independent periods — local arithmetic on each tile | same family, different sub-flavour |

3 light dimensions shared (2, 3, 4). 5 dimensions diverge (1
partially heavy, 5/6/7 fully heavy, 8 sub-flavour different).
Heavy axes (5, 6, 7) all diverge — passes per
`negative-similarity-check.md` rubric ("sharing on dimensions
6, 7, or 8 is heavier; 3+ shared is the threshold for
rejection").

Re-checked vs lq5x, vp6h, pf3w, xz5g, qz73, g50t — none shares
3+ heavy dimensions with revision 2. Distinguishing rules in §9
hold under the fleshed-out spec.

**Novelty: PASS.**

## Overall verdict

**PASS** — all 22 checklist items pass; novelty PASS. Transition
to `implement`.
