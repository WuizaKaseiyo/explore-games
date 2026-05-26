# tb4k — critique-spec PASS

Visit count: 1 (cap 10).

## Checklist items 1-25

| # | Item | Verdict | Notes |
|---|---|---|---|
| 1 | Palette 0..15 (+ -1) | ✅ | Palette in use: {1, 2, 3, 4, 5, 9, 10, 12, 13}. All within range. |
| 2 | Universal scaffold | ✅ | Spec describes module-scope `sprites`, `levels`, `BACKGROUND_COLOR`, `PADDING_COLOR`, `RenderableUserDisplay` HUD, `NovaBaseGame` subclass. |
| 3 | `available_actions ⊂ [1..7]` | ✅ | `[1, 2, 3, 4]` — cardinal arrows only. |
| 4 | Exactly 3 levels | ✅ | L1, L2, L3 spec'd. |
| 5 | 4-char ID novel | ✅ | `tb4k` — lowercase, alphanumeric, not in 25 reserved IDs, not in `prior-games/index.md`. Not an English word. |
| 6 | Core-knowledge priors only | ✅ | Objectness, geometry/topology, physics. No agentness (no NPCs). All four §3.4 categories optional, not all required. |
| 7 | No letters/digits/clipart/cultural | ✅ | Brick sprite is an abstract bevel pattern (palette 4/3/5). Hole is a cross-hatched dark pattern. Goal is a blue pad. Life pip is a small maroon-orange dot. No glyph resembles a letter, digit, arrow, or real-world object. |
| 8 | ≥ 2 distinct mechanics | ✅ | 3 mechanics: M1 (tumble), M2 (hole + lives), M3 (narrow bridge). |
| 9 | L1 tutorial — base dynamic system | ✅ | L1 has just M1; reduced state space (no holes, no bridges); no on-screen text. |
| 10 | L2/L3 compose every available mechanic | ✅ | L2 witness requires M1 (the brick moves) and M2 (hole avoidance routing). L3 witness requires M1, M2, AND M3 (bridge-discipline east-only on cx ∈ [6..9]). |
| 11 | Mechanic inheritance + 1-or-2-per-level | ✅ | L1: N=1; L2: N+1=2; L3: L2-count+1=3. Each level adds exactly 1 new mechanic; no L1 mechanic drops out. |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ | See per-mechanic table below. |
| 13 | Min-action witness K≥3, D≥2 | ✅ | L1: K=16, D=2. L2: K=16, D=3. L3: K=14, D=2. All ≥ 3, all D ≥ 2. No repetitive single-action wins (D ≥ 2 enforced). |
| 14 | Mechanic family absent from taxonomy | ✅ | "tumble-block-stand-fall" not present; closest is ka59 (sokoban-explode-chase) but ka59 uses fixed-footprint sliding, no tumble + state-change. |
| 15 | Mechanic family absent from prior-games | ✅ | Closest priors are hb5n (polyomino-walker-rotate), pj7k (rolling-cube-face-paint), zw91 (inflate-fit-burst), nz3v (rotor-pivot-walk). All distinguished concretely in §9. |
| 16 | Concrete distinguishing rules for near-misses | ✅ | §9 of spec articulates concrete rules naming each prior's defining behavior vs tb4k's. |
| 17 | Win condition stated | ✅ | `brick_state == "standing" AND brick_cell == goal_cell`. Same predicate across all levels. |
| 18 | Lose condition stated | ✅ | Two paths: lives exhausted (after hole-falls), or step budget exhausted. |
| 19 | Difficulty floor and ceiling per level | ✅ | All four (a) random-resistance, (b) human time, (c) planning depth, (d) step budget bullets present for L1, L2, L3. L2/L3 planning-depth justification names the post-discovery decision space, a plausible-but-wrong alternative, and the witness reasoning chain. |
| 20 | No hidden state — visual cue for every action-mutated state | ✅ | Brick's standing/lying-h/lying-v state is visible as three distinct sprites. Brick's position visible. Lives count visible via 3 `life_pip` sprites in top-right HUD. Step budget visible via row-0 depleting bar. |
| 21 | Not low-resolution | ✅ | grid_size (32, 32) at scale 2 → each Bloxorz cell renders as 4 actual pixels with sub-cell pattern (2×2 sprite has 4 distinct sub-pixels). Brick / hole / goal / life-pip each carry an internal bevel or cross-hatch pattern (not just fill colour). Floor is camera-background palette 2 (uniform); the spec deliberately keeps floor uniform to let the brick + hazards + goal carry the readable detail. |
| 22 | UI teaches the role | ✅ | Brick (dark bevelled solid) reads as a physical object the player controls. Hole (dark cross-hatched) reads as danger. Goal (bright blue pad) reads as destination. Life pip (small orange-maroon dot) reads as a count. Identical-visual sprites (three brick variants) share the same role correctly. |
| 23 | ACTION7 strict-undo or absent | ✅ | ACTION7 absent from `available_actions`. |
| 24 | Animation for non-local effects | ✅ N/A | Each tumble shifts the brick anchor by at most 2 cells; the post-tumble sprite is rendered in a position adjacent or overlapping the pre-tumble sprite. Single-frame snap is legible because the brick's footprint is continuous across the tumble. Not "teleport / slide-until-wall / projectile / chain reaction / multi-entity propagation". |
| 25 | Lives mechanism for hard-death | ✅ | L1: no hard-death → N/A correctly noted. L2: 3 lives, decrement on hole-fall, level resets and brick respawns at start; lose() fires at lives==0. L3: identical lives logic. Visible HUD: 3 `life_pip` sprites in top-right of frame, removed one-by-one on death. |

## Per-mechanic counterfactual necessity table (checklist 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (tumble) | no | ACTION1..4 all dispatch to tumble; the brick has no other movement verb. Goal at (11,11) is 8 cells from start (3,3) along each axis; the brick must traverse via tumble. |
| L2 | M1 (tumble) | no | Same reason — no other movement verb. |
| L2 | M2 (hole hazard + lives) | no | Direct east from (2,4) hits the hole at (8,4) (lying-h [(8,4),(9,4)] or standing (8,4)). Every path that wins must route around the hole field; removing M2 would let the brick pass through holes and shorten the path to ~10 tumbles. The witness's 16-tumble N-detour is forced specifically by M2's hard-death rule. The S mid-detour at (6,4) → south → east dies at (10,5) hole, ruling it out via M2. The far-N loop (y=2) and far-S loop (y=6) are equally valid alternates that also engage M2 (every viable path avoids holes). |
| L3 | M1 (tumble) | no | Same reason. |
| L3 | M2 (hole hazard + lives) | no | The middle column-band cx ∈ [6..9] is 4 columns × 16 rows = 64 cells, of which 60 are holes and 4 are the bridge cells at y=3. Any tumble that lands the brick footprint on a non-bridge cell in that band dies. The only way to win is to confine bridge crossings to y=3 cells — which engages M2. |
| L3 | M3 (narrow bridge / lying-perpendicular fatal) | no | The bridge is 1 cell wide (y=3, cx ∈ {6,7,8,9}). From standing (8,3): ACTION1 (N) → lying-v [(8,2),(8,3)] where (8,2) is hole → death. ACTION2 (S) → lying-v [(8,3),(8,4)] where (8,4) is hole → death. So while on cx ∈ [6..9], the player must use ACTION3 or ACTION4 only (east-west tumble discipline). Without M3 (e.g., if the bridge were 3 cells wide), the player could freely tumble N or S on bridge cells. |

### Plausible-alternate enumeration for L2 (per checklist 12 "verify by enumeration, not abstraction")

Post-discovery alternates the player would consider from start (2, 4):
1. **Direct east**: dies at lying-h [(8,4),(9,4)] (8,4) is hole. Rejected.
2. **Mid-route N detour at (6, 4)** (witness): K=16, survives. Path: 4E + 2N + 4E + 2S + 4E. ✓
3. **Mid-route S detour at (6, 4)**: dies at lying-v [(10,5),(10,6)] (10,5) is hole. Rejected.
4. **Far-N loop via y=2**: 2N + 12E + 2S = 16. y=2 row is solid for all x. Survives. Engages M2 (avoids the y=3 hole line). ✓
5. **Far-S loop via y=6**: 2S + 12E + 2N = 16. y=6 row is solid for all x. Survives. Engages M2 (avoids the y=5 hole line). ✓
6. **Far-S loop via y=7+**: longer than 16 tumbles, over budget.

Every survivor (#2, #4, #5) engages M2 by avoiding holes. The lethal alternates (#1, #3) demonstrate the necessity of M2 to the player who tries them. Witness chose #2 because the N mid-route is the most natural "go diagonally" intuition.

### Plausible-alternate enumeration for L3 (per checklist 12)

Post-discovery alternates the player would consider from start (2, 5):
1. **Direct E**: dies at lying-h [(6,5),(7,5)]? (7,5) is hole (middle band). Rejected.
   Actually wait — (7, 5) is in the middle band cx∈[6..9], y=5 ≠ 3 → hole. ✓ dies. Rejected.
2. **Greedy N-then-E** (climb to y=1 first, then east): from (2,5) 4N → standing (2,1); 4E → standing (6,1); but (6,1) is in middle band, y=1 ≠ 3 → hole. Death. Rejected.
3. **Witness: N then E across bridge then N**: 2N + 4E (to bridge entry (6,3)) + 4E (across bridge) + 2N + 2E = 14. Survives. ✓
4. **E first, then N**: from (2,5) 4E to (6,5); but (6,5) is hole. Death. Rejected.
5. **N then E at y=2** (try crossing at y=2): from (2,5) 3N → standing (2,2)? Actually 3 N tumbles: standing(2,5)→lying-v[(2,4),(2,5)]→standing(2,3)→lying-v[(2,2),(2,3)]; ends lying-v, not standing. 4N: standing (2,1). Going E: lying-h [(2,1),(3,1)] → standing (4,1) → lying-h [(4,1),(5,1)] → standing (6,1) hole. Death. Same as #2.

Every survivor engages M3 (bridge discipline on cx∈[6..9]). The plausible-but-wrong heuristic "minimize Manhattan distance via greedy N" dies because it reaches the middle band at the wrong y.

Witness reasoning chain (per checklist 19 L3): "The bridge is at y=3 — the only safe row through cx∈[6..9]. I must arrive at y=3 BEFORE entering the middle band, then keep east-only tumbles on the bridge, then resume vertical movement only after exiting at cx≥10." This requires ahead-of-time planning: the post-discovery player who knows the bridge geometry can reason this chain in ~30 seconds, but the greedy-Manhattan heuristic actively misleads.

## Similarity check (full-spec re-pass)

Re-running `similarity-check.md` against the fleshed-out spec, not just the §2 family name:

- **Family-level match** vs all 25 taxonomy entries: no exact family-name match. `cn04` (nub-pair-glyph), `ar25` (shape-mirror-cover) involve sprite rotation but the rotation verb is decoupled from movement; tb4k fuses rotation into each arrow press. No description-level match — no taxonomy game has a "footprint changes shape with each tumble + hole-fall hazard" structure.
- **Family-level match** vs prior-games: closest are hb5n, pj7k, zw91, nz3v, fz5j, dh4j, kj82. Each has a concrete distinguishing rule in §9 of the spec. Description-level match: ALL near-misses fail at least one of (win condition, primary action, primary constraint). tb4k's primary action is "tumble" (fused move+rotate), primary constraint is "hole-fall hazard via brick-footprint geometry", win condition is "brick standing on goal" — no prior shares all three.

Verdict: **NOVEL** for every taxonomy + prior-game row. No concrete near-miss requires a distinguishing-rule paragraph beyond what §9 already documents.

## Negative-similarity full-spec re-pass

Walking the 8 dimensions of `negative-similarity-check.md` against the fleshed-out spec:

vs **hb5n** (polyomino-walker-rotate) — shares dimensions: 2 (arrow input style), maybe 7 (cell-block pixel grain). Differs strongly: 1 (board cast), 3 (level asks), 4 (kills), 5 (supporting cast), 6 (visual signature — tb4k's slate-on-grey palette vs hb5n's red-on-grey), 8 (core dynamic). 2 shared dimensions < 3 threshold. **PASS.**

vs **pj7k** (rolling-cube-face-paint) — shares: 2 (arrow input). Differs: 1, 3, 4, 5, 6 (pj7k is multi-coloured, tb4k is monochromatic dark-on-light), 7, 8. 1 shared dimension. **PASS.**

vs **zw91** (inflate-fit-burst) — shares: nothing strong. tb4k's tumble is movement-coupled; zw91's size cycle is ACTION5-decoupled. Different cast, different kills, different visual, different dynamic. **PASS.**

vs **nz3v** (rotor-pivot-walk) — shares: 4 (kills — both use 3-lives + hard-death). Differs: 1, 2, 3, 5, 6, 7, 8. 1 shared dimension. **PASS.**

vs **kj82** (plank-pivot-walk) — shares: 4 (kills, both step-budget). Differs: 1, 2, 3, 5, 6, 7, 8. 1 shared dimension. **PASS.**

vs **fz5j** (phase-step-tile) — shares: 4 (kills — both use 3-lives + hard-death tile hazard). Differs in everything else: phase-tile has time-varying terrain; tb4k has static terrain + variable brick. **PASS.**

No prior shares 3+ dimensions with the fleshed-out tb4k spec. **Negative similarity: PASS.**

## Verdict

**PASS** — proceed to `implement`.

Notes for implement:
- Reserve Bloxorz row y=0 for HUD (lives pips). Implement tumble bounds as `1 ≤ cy ≤ 15` rather than `0 ≤ cy ≤ 15` to keep the brick out of the HUD row.
- Floor: leave as plain camera-background (palette 2). The brick, holes, goal, and lives pips carry the readable visual detail.
- L1 goal at Bloxorz (11, 11); L2 goal at (14, 4); L3 goal at (12, 1). All same-parity-as-start per Bloxorz tumble physics.
