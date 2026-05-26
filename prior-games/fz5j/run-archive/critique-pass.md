# Critique pass — `fz5j` mechanic-spec.md

## Format & structure

1. **Palette values 0..15 + (-1) only?** ✅ Sprites use {1, 4, 5, 6, 8, 10, 11, 12, 14}; goal/phase-tile open variants use -1 for transparent centres. PASS.
2. **Universal scaffold structure?** ✅ Spec describes the standard layout (sprite bank → levels → constants → HUD → game class). Will be physically realized in `implement`. PASS.
3. **`available_actions` ⊂ [1..7]?** ✅ `[1, 2, 3, 4]`. PASS.
4. **EXACTLY 3 levels?** ✅ Spec §4 has Level 1, Level 2, Level 3 only. PASS.
5. **4-char ID, lowercase, not in reserved or prior-games?** ✅ `fz5j` — verified in `mechanic-pick.md`. PASS.

## §3.4 priors & constraints

6. **Mechanics from 4 allowed priors only?** ✅ Objectness (avatar, walls, tiles, goal as discrete entities), basic geometry/topology (path connectivity), and basic physics framed as **clockwork rhythm / oscillation** — periodicity is in the same family as gravity/friction/momentum: an "intuitive rule" the player observes (cell pulses on a fixed period, like a pendulum or breath). The phase predicate `t % n == offset` is a deterministic temporal-physics rule the player infers by watching pulses. No agentness (no NPCs). PASS — defended on intuitive-rules-of-physics grounds.
7. **No letters/digits/clipart/cultural conventions?** ✅ Sprites:
   - Avatar 4×4: hollow green square frame with off-black inner ring — abstract geometric.
   - Wall 4×4: solid block — abstract.
   - Goal 4×4: hollow yellow square frame, transparent centre — abstract square ring (not round → not "0").
   - Phase-tile open: square frame + 1-px yellow centre dot — abstract.
   - Phase-tile closed: solid black — abstract.
   - Fragile tile: phase-3 pattern + single 1-px palette-8 cell at top-left corner — geometric mark, not a glyph (per amended sprite-roster). NO chevron, NO arrow shape, NO letter/digit silhouette. Tutorial conventions absent (no on-screen text). PASS.
8. **At least TWO distinct mechanics?** ✅ L3 has 5 (walk + period-2 + period-3 + period-4 + fragile-phase-3). PASS.
9. **L1 = tutorial, base dynamic system, no on-screen text?** ✅ L1 has 2 mechanics (walk + period-2). Reduced state space (16×16 grid, 2 phase tiles, no period-3/4/fragile). No instructions; pulsing tiles teach the rule by being pulsing. PASS.
10. **L2/L3 increase difficulty by COMPOSING mechanics, not by scaling?** ✅ L2 keeps the L1 grid size and adds period-3 as a *new rule*. L3 keeps the same logical-grid scale, adds period-4 + fragile-phase-3 as new rules, and the witness composes all 5 mechanics. NOT "L1 with bigger grid." PASS.

## Mechanic structure

11. **Mechanic inheritance + +1-or-+2 rule?** ✅ L1 N=2 → L2 N+1=3 → L3 L2+2=5. Each prior mechanic is required at later levels (every later level's witness exercises every earlier mechanic AND the new ones). No mechanic drops out. The +2 jump on L3 is permitted (period-4 + fragile both new). PASS.
12. **Strict counterfactual necessity / no trivial fallback?** ✅ Per §4 trace, every witness move that is not blocked exercises walk; every phase-tile crossing is on the unique path; the L3 fragile cell makes "retry-in-place" (the L1/L2 trivial fallback) immediately fatal — must compute residue. The L3 commute test (swap actions 12/13) demonstrates a swap leaves avatar in dead-end col-11 → unsolvable, confirming order is load-bearing. PASS.

## Novelty

13. **Mechanic family absent from `taxonomy-of-25-games.md`?** ✅ `phase-step-tile` not in taxonomy. PASS.
14. **Mechanic family absent from `prior-games/index.md`?** ✅ Not in the 11-row index. PASS.
15. **Concrete distinguishing rule for each near-miss?** ✅ Per `mechanic-pick.md` and spec §9, articulated rules vs:
   - **tu93**: stationary phase-cells vs mobile AI agents.
   - **g50t**: per-cell phase vs uniform scrolling.
   - **dc22**: autonomous step-counter mod period vs event-triggered cycles.
   - **ls20**: cell mutation vs avatar-attribute mutation.
   - **wa30**: same action palette but no carry/tether.
   - **tr87**: same pure-arrow palette but no rule-cycle / sprite-name suffix mutation.
   - **bp35** (newly checked — has spike-tile that loses on touch): bp35's spike is *gravity-fall navigation*; fz5j is *step-walk on phase-pulsing field*. Surface dynamic and core thought-shape differ; the "permanent-loss-tile" primitive is shared with bp35's spike and lf52's fog-burn but at the level of a *primitive* not a *mechanic family*. Concrete rule: bp35's spike is unconditional touch-death; fz5j's fragile cell is *conditional* (locks only on residue mismatch — a player who computes residue safely passes). DISTINGUISHING.
   - **kx14, lq5x, vn8d, pj7k, kf42, qz73, qb84, gv47, hr8q, ng52, pz4t** — all addressed in spec §9 / `mechanic-pick.md`.
   PASS.

## Solvability

16. **Win condition stated?** ✅ Spec §7: avatar at goal cell → `next_level()`; engine auto-fires `win()` after L3. PASS.
17. **Lose condition stated?** ✅ Spec §8: step counter ≥ max OR L3 fragile-locked-and-unreachable. PASS.

18. **Difficulty floor and ceiling — all four bullets per level?**
   - **L1**: (a) random-resistance ✅ (random walk on 14-cell-wide interior with budget 22 << expected first-passage); (b) human time ✅ (~1 min); (c) planning depth ✅ (near-zero — L1 allowance, mechanic discovery is the difficulty); (d) step budget 22 ✅ (witness 14, slack 57%, generous). PASS.
   - **L2**: (a) random-resistance ✅; (b) human time ~2 min ✅; (c) planning depth NON-TRIVIAL ✅ — per-step reasoning chain explicitly named (identify next phase-tile by colour, compute period & offset, compute arrival step, decide between direct walk and in-place retry); rejected single-step heuristics named (spam-the-new-verb, follow-the-colour, 1-action lookup); (d) step budget 30 ✅ (witness 16, slack 87%, generous, accommodating period-3 discovery cost). PASS.
   - **L3**: (a) random-resistance ✅ (fragile cell makes random-walk near-immediately fatal); (b) human time ~3 min ✅; (c) planning depth STRICTLY DEEPER than L2 ✅ — named trivial heuristic ("retry-in-place", which won L1/L2) explicitly fails because of fragile cell; concrete witness-pair commute test (actions 12/13) where swap leaves avatar in dead-end col-11; (d) step budget 40 ✅ (witness 26, slack 54%, generous, NOT shrinking relative to witness across L1→L2→L3 [64% / 53% / 65%]). PASS.

## Negative-similarity recheck

Re-walking the 8 dimensions of `negative-similarity-check.md` against fleshed-out spec, closest prior is **tu93**:

| Dim | tu93 | fz5j | shared? |
|---|---|---|---|
| 1. On board | maze + multi-primary + multi-AI-mob + walkable underlay + exits | avatar + walls + 3 distinct phase-tile species + goal + 1 fragile variant | partial (both maze-on-grid; cast specifics differ heavily) |
| 2. Player input | direction-press → ALL primaries lockstep | direction-press → single avatar | NO (multi vs single) |
| 3. Asks for | every primary on its exit | single avatar on goal | partial (universal "reach goal") |
| 4. Kills player | budget OR all primaries destroyed | budget OR fragile-lock-isolation | NO (no enemy destruction in fz5j; fragile is a passive cell hazard) |
| 5. Cast | walls + walkable + 3 enemy AI species + exit | walls + 3 phase-tile colour species + goal + fragile variant | NO (cast roles fundamentally different — passive cells vs autonomous AI) |
| 6. Visual signature | grey/yellow chunky maze | green avatar + magenta/light-blue/orange pulsing tiles + yellow goal + red corner-marks | NO (palette and aesthetic distinct) |
| 7. Pixel grain | mid-detail 5×5 sprites | rich 4×4 frame+dot per phase-tile | partial |
| 8. Core dynamic | "how do I move my primaries together past AI?" | "what step counter do I need at this cell?" | NO |

Heavy dimensions (6, 7, 8) all differ. Shared partials: 1, 3, 4, 7 — none are heavy. Dimension 2 also differs (multi vs single agent, even though both pure-arrow). **Below 3-shared threshold.**

Spot-check vs all priors: kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d — none overlap on 3+ dimensions (per `mechanic-pick.md` analysis, still valid).

**Negative similarity check: PASS.**

## Verdict

**ALL 18 checklist items PASS. NOVEL on positive (similarity-check) and negative (negative-similarity-check) tests.** Spec is approved for `implement`.
