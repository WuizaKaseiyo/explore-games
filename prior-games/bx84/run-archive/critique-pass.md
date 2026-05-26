# Critique Pass — bx84 mechanic-spec.md

Walked every gate adversarially. All checks pass.

## §3.4 checklist (`design-constraints/checklist.md` items 1-18)

### Format & structure

1. ✅ Palette values 0..15 + `-1`. The spec uses `{3, 4, 5, 6, 7, 9, 11, 12, 13}` plus `-1` — all valid.
2. ✅ Universal scaffold structure (imports → sprite bank → levels → constants → HUD → game class) is described in §3 and §6 of the spec.
3. ✅ `available_actions = [6]` is a subset of `[1, 2, 3, 4, 5, 6, 7]`.
4. ✅ Exactly 3 levels (L1, L2, L3) per `composition-and-tutorial.md` § "Exactly 3 levels".
5. ✅ Game ID `bx84` is 4 lowercase alphanumeric, not in the reserved-25 list, not in `prior-games/index.md` (verified in `mechanic-pick.md`).

### §3.4 priors & constraints

6. ✅ Mechanics draw from `core-knowledge-priors.md`'s four categories only: objectness (mirrors, filter, prism, targets, emitter as persistent entities); basic geometry & topology (right-angle reflection, perpendicular beam-splitting); basic physics (light-as-ray straight-line propagation). Agentness is NOT used (no NPCs, no chasers).
7. ✅ No letters / digits / clipart / cultural conventions:
   - 1×1 single-colour cells (emitter palette-3, mirrors palette-6/7, filter palette-9, prism palette-12/13).
   - 3×3 hollow ring targets (8-cell perimeter, transparent centre) — abstract geometric frame, not a digit. The "0" digit specifically would have a 3×5 or larger oval shape; a 3×3 perimeter square does not unambiguously read as "0".
   - Beam appears as palette-11 cells along the path — abstract trace, not a "→" arrow.
   - No on-screen text or tutorial banners.
8. ✅ At least TWO distinct mechanics in the environment: spec specifies M1 (mirror placement+cycling), M2 (filter recolouring), M3 (prism beam-splitting), M4 (prism toggling).
9. ✅ Level 1 establishes the base dynamic system (M1 alone) with a reduced state space (1 mirror to place, 1 target ring, no filters or prisms), and no on-screen text. The witness is 1 click; mechanic discovery is the entire difficulty.
10. ✅ L2 and L3 increase difficulty by COMPOSING every mechanic available at that level:
    - L2 witness exercises BOTH M1 (mirror) AND M2 (filter recolouring).
    - L3 witness exercises ALL of M1, M2, M3, M4. L3 is NOT just "L2 with a bigger grid"; it adds the prism (geometric beam-splitting) AND toggling (mutable prism state requiring planned click sequencing).

### Mechanic structure (per-level)

11. ✅ Mechanic inheritance and the +1-or-+2 rule:
    - L1 N = 1 (M1).
    - L2 M = 2 = N + 1 (M1 carried + M2 new). 1 new mechanic introduced. ✓
    - L3 = M + 2 = 4 (M1, M2 carried + M3, M4 new). 2 new mechanics introduced. ✓
    - No level promotion drops a mechanic; M1 is required at L1, L2, AND L3 by the spec's per-mechanic counterfactual rows.
12. ✅ Strict counterfactual necessity (the per-mechanic table). Each mechanic at each level has a 1-line concrete reason that names a specific cell, sprite, or rule blocking every alternate path:

    | Level | Mechanic | Solvable without triggering? | Why not (concrete) |
    |---|---|---|---|
    | L1 | M1 (mirror) | no | Beam fires east at row 8, exits at (15, 8); target ring is at rows 11-13, unreachable without an east→south reflection at column 8. |
    | L2 | M1 (mirror) | no | Beam exits east at (15, 2); target_blue at (10, 11) is south of beam row, unreachable without a `\` mirror at (10, 2). |
    | L2 | M2 (filter) | no | target_blue accepts only palette-9; beam stays palette-11 (yellow) without the filter at (3, 2). |
    | L3 | M1 (mirror) | no | East-branch beam exits at (15, 8); target_blue at (12, 11)–(14, 13) is south of beam row 8, unreachable without `\` mirror at (12, 8). |
    | L3 | M2 (filter) | no | target_blue accepts only palette-9; without filter, east-branch stays palette-11. |
    | L3 | M3 (prism splitting) | no | target_yellow_south at (3, 12) and target_yellow_north at (3, 3) are off-axis from the east-going emitter beam; only the prism's perpendicular branches reach them. |
    | L3 | M4 (prism toggling) | no | target_yellow_south requires state ES (south branch); target_yellow_north requires state EN (north branch). Both must be lit; toggling is the only way to enter both states. |

    Every row answers "no" with a concrete reason (specific cell coordinates and a named blocker). No row hand-waves with "as L1/L2".

### Novelty

13. ✅ Mechanic family `beam-mirror-reflect` is absent from `taxonomy-of-25-games.md` (verified by direct table walk in `mechanic-pick.md`).
14. ✅ Absent from `prior-games/index.md` (the 13 prior generated games).
15. ✅ Concrete distinguishing rules for every near-miss are articulated in spec §9 (and originally in `mechanic-pick.md`):
    - vs `ar25` (shape-mirror-cover): 1D ray reflection vs 2D shape symmetry-folding.
    - vs `cd82` (orbit-fire-paint): ray-tracing vs canvas-painting; static emitter vs orbiting tank.
    - vs `tn36` (program-pawn-trace): live re-trace vs deferred-execution programme.
    - vs `re86` (frame-paint-canvas): no canvas-painting verb.
    - vs `lq5x` (lantern-cone-illuminate): static emitter + reflectors vs walking-lantern + cone; right-angle reflection mechanic ABSENT in lq5x.
    - vs `vn8d` (domino-cascade-topple): player BUILDS network vs trigger-pre-placed-network.
    - vs `kn58` (anchor-pull-magnet): place mirrors that route a beam vs place anchor that pulls pawns.

### Solvability

16. ✅ Win condition stated: "all targets lit", adapted per level. Specifically:
    - L1: `target_yellow` lit.
    - L2: `target_blue` lit.
    - L3: `target_yellow_south` AND `target_blue` AND `target_yellow_north` all lit.
17. ✅ Lose condition stated: `self.steps_remaining <= 0` at the START of `step()` triggers `lose()`. Per-level budgets: 30 / 50 / 80.
18. ✅ Difficulty floor and ceiling. Each of L1, L2, L3 has all four bullets:
    - **(a) Random-resistance**: stated for each level with concrete probability reasoning.
    - **(b) Human time**: ~30 sec / 1-2 min / 2-3 min targets named, hitting the ~2-min/level and ~6-min/total goals.
    - **(c) Planning depth**:
      - L1: NO strict planning (mechanic discovery is the entire difficulty). ✓ matches `difficulty-rules.md` § L1.
      - L2: MODERATE planning, with a 4-step per-step reasoning chain explicitly named. ✓ matches L2 requirement.
      - L3: MORE THAN L2 planning, with (i) a NAMED trivial heuristic ("click cells closest to each target first") that fails, and (ii) a NAMED witness-pair commute test (swapping clicks 1 and 2 breaks the witness — the swapped sequence ends without target_yellow_south lit because the south branch never existed during a click while the prism was still in ES state).
    - **(d) Step budget**: 30 / 50 / 80 — generous over witness lengths (1, 1, 2 actions respectively); monotonically non-decreasing across levels.

## Negative similarity check (re-walked on the fleshed-out spec)

Walking the 8 dimensions in `negative-similarity-check.md` against every prior. The closest priors and their overlap with the now-fleshed-out spec:

| Prior | Dimensions overlapped (out of 8) | Verdict |
|---|---|---|
| lq5x (lantern-cone) | 1 (goal-level "match light colour to target") | NOVEL |
| vn8d (domino-cascade) | 1 (click input) | NOVEL |
| kn58 (anchor-pull-magnet) | 2 (click input, "place item to affect grid state") | NOVEL |
| All other priors | ≤ 1 | NOVEL |

No prior shares 3+ dimensions. The spec's pixel grain (1×1 emitter / 1×1 mirrors / 1×1 filter / 1×1 prism / 3×3 hollow ring targets / per-frame beam overlay), palette signature (`{3, 5, 6, 7, 9, 11, 12, 13}` — distinct from any prior's dominant), and core dynamic ("place reflectors to route a 1D ray") are all novel.

## Common failure modes (from `critique_spec.md`)

- ❎ Spec drift: NO — every level's mechanic stays in the beam-reflect family; no L2 or L3 mechanic drifted into territory shared with a taxonomy entry.
- ❎ Constraint violation in sprite pixels: NO — every sprite was inspected for letter/digit/arrow/clipart shape; all are abstract geometric primitives.
- ❎ Pseudo-multi-mechanic: NO — every mechanic at every level is exercised by the witness AND has a concrete counterfactual blocker.
- ❎ Tutorial too hard: NO — L1 has 1 mechanic, 1 witness click, ~30 sec for human.
- ❎ Wrong level count: NO — exactly 3 `Level(...)` entries.

## Verdict

**PASS** on all 18 checklist items, the positive similarity check, the negative similarity check, and all common failure modes. Transition to `implement`.
