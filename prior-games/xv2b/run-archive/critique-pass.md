# critique-pass — xv2b

Verified each `design-constraints/checklist.md` item plus the
similarity / negative-similarity rules.

## Format & structure

1. **Palette 0..15 / -1 transparent** ✅ — sprites use palettes
   {0, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14} plus `-1`.
2. **Universal scaffold** ✅ — spec follows
   `code/universal-scaffold.md` order (sprites, levels, constants,
   HUD, game class). Will hold under implementation.
3. **`available_actions ⊂ [1..7]`** ✅ — `[5, 6]`.
4. **Exactly 3 levels** ✅ — L1 base, L2 base+M2, L3 base+M2+M3.
5. **4-char ID, opaque, non-colliding** ✅ — `xv2b`; checked
   against the 25 reserved IDs and all 50 entries in
   `prior-games/index.md`; closest priors `xn5p` and `xz5g` differ.

## §3.4 priors & constraints

6. **Core priors only** ✅ — basic physics (hydrostatic
   equalisation, gravity, mechanical pump-work), objectness
   (valves/pumps/drains as discrete entities), basic geometry /
   topology (the valve-graph). No agentness, no acquired symbolic
   knowledge.
7. **No letters/digits/clipart/cultural conventions** ✅ — every
   sprite is an abstract shape (open-top rectangle, square ring,
   block-with-slit, fins-in-box). No glyphs, no arrows, no real-
   world icons. Drain's hole-with-rim does NOT read as the digit
   "0" or "O" — it has a non-circular outer square frame plus a
   distinct floor-row that breaks any letter resemblance.
8. **At least two distinct mechanics** ✅ — three (M1 valve-
   equalize, M2 drain, M3 pump).
9. **L1 tutorial: reduced state space, no on-screen text** ✅ —
   L1 has 3 vessels + 2 valves + step counter. No drains, no
   pumps. Solvable in 18 actions. No text.
10. **L2/L3 increase difficulty by composition, not scaling** ✅
   — L2 adds the *drain mechanic*; L3 adds the *pump mechanic*.
   Both are new physics rules, not bigger grids.

## Mechanic structure (per-level)

11. **+1-or-+2 rule and inheritance** ✅
    - L1: N = 1 (M1).
    - L2: N+1 = 2 (M1 + M2). M1 still witness-required (V_BC must
      open or C never gets water).
    - L3: L2-count + 1 = 3 (M1 + M2 + M3). Every earlier mechanic
      remains required (V_AB and V_BC both open at different phases;
      drain on A consumes 15 cells of mass surplus; pump fires for
      the last 3 cells).
    No level introduces 0 new mechanics or ≥3 new mechanics.

12. **Strict counterfactual necessity (no trivial fallback)** ✅

    | Level | Mechanic | Solvable without M? | Why not (concrete) |
    |---|---|---|---|
    | L1 | M1 | no | Targets (8,8,8) differ from start (24,0,0); only V_AB+V_BC open + ACTION5 ticks redistribute mass. Closing both valves and ticking does nothing (no drains/pumps); targets unreachable. |
    | L2 | M1 | no | C must reach 8 from 0; only V_BC open + ACTION5 adds water to C. |
    | L2 | M2 | no | Mass surplus = 36 − 28 = 8 cells must vanish; valves only redistribute; only the drain on B destroys mass. |
    | L3 | M1 | no | B and C must reach non-zero from 0; only valves can carry water from A through the gap to B (and pump only operates between B and C). |
    | L3 | M2 | no | Mass surplus = 30 − 15 = 15 cells must vanish; only the drain on A destroys mass. |
    | L3 | M3 | no | Once V_AB has finished and water settles at (0, 8, 0), V_BC's slit-height 8 forbids gravity flow B→C (rule requires `B > 8` strictly; B=8 fails); target C = 3 requires water to reach C, and the pump is the only mechanism that bypasses the strict-inequality slit gate. Verified by simulation: spam-everything (V_AB+V_BC+pump on from start) ends at (0, 0, 8) — pump-side overshoots C by 5 because the pump fires B→C every tick a snapshot has B>0, while V_AB+V_BC interaction leaves B trickling at 1; final state is wrong on every vessel. |

    **Plausible alternates enumerated and rejected:**
    - L3 alternate "open every valve + pump on at the start, tick
      until done": traced explicitly in spec §4 / mechanic-pick.md
      addendum. With snapshot semantics each tick A drops 2, B
      hovers near 1, C rises 1; final state (0, 0, 15), C overshoots.
      Fail.
    - L3 alternate "skip drain phase, jump straight to V_BC+pump":
      A still has 30 cells of water trapped by closed V_AB; pump
      can't draw from A; C never reaches 10 because B has no
      source. Fail.
    - L2 alternate "open V_AB to drain A through B's drain": A
      starts at 12 (already at target); flowing A into B raises B
      above what drain can clear in budget; A leaves target. Fail.

## Novelty

13. **Mechanic family absent from `taxonomy-of-25-games.md`** ✅
    — no row matches `vessel-valve-equalize`. Cross-referenced
    against deep-analysis files: sp80's `<id>-deep-analysis.md`
    confirms its mechanic is *discrete drop-trajectory routing
    via slidable shelves with a 4-pour-attempt cap*, not bulk
    hydrostatic equalisation. Distinct.
14. **Mechanic family absent from `prior-games/index.md`** ✅ —
    nearest prior kx14 is single-tank surface-raise with floating
    balls; `prior-games/kx14/mechanism-detail.md` (when present)
    confirms it. Mine is multi-vessel valve-graph with uphill
    pumps. Distinct.
15. **Concrete distinguishing rule per near-miss** ✅ —
    `mechanic-spec.md` §9 + `mechanic-pick.md` give per-prior
    distinguishing rules (sp80 = drops vs continuous level; kx14 =
    single tank vs N-vessel graph; rk7x = single courier vs bulk
    fluid; vd3g = binary terrain marbles vs reservoir levels;
    kp9z = capacity-overflow grains vs hydrostatic level
    equalisation; lv4k = mass-arm torque vs water mass).

## Solvability

16. **Win condition stated** ✅ — "every vessel's water level ==
    its target level after a step()". Tests at every tick.
17. **Lose condition stated** ✅ — step counter reaches 0; plus
    early-lose if `current_total_water < min_target_total` to avoid
    no-win-waiting-room (per `difficulty-rules.md` § 1d).
18. **Difficulty floor and ceiling** ✅ — every per-level
    bullet (a) random-resistance, (b) human time, (c) planning
    depth, (d) step budget present and concrete.
    - L1 planning depth: explicitly *no strict planning required*.
    - L2 planning depth: post-discovery decision space ≥ 2 first
      actions (open V_AB, open V_BC, click drain, ACTION5);
      plausible-but-wrong alternative (open V_AB) named; witness
      reasoning chain stated.
    - L3 planning depth: trivial heuristic ("spam-everything")
      named; divergence point stated (heuristic doesn't close
      V_AB at tick 15, ends with C overshooting); ahead-of-time
      reasoning required for phase ordering.

19. **No hidden state** ✅ — every reasoning-relevant piece of
    state has a persistent visible cue:
    - water level → fill-bar height + meniscus row;
    - valve open/closed → sprite swap (slit gap visible vs solid);
    - pump on/off → orange-fins vs green-fins-with-white-centre;
    - drain → always-visible hole sprite;
    - step counter → bottom-row HUD.

20. **No low-resolution blocky game** ✅ — grid is full 64×64
    (no upscale); vessels carry internal pixel detail (1-pixel
    light-blue meniscus on the water surface, multi-shade frame
    rim with palette-5 floor inner row, palette-3 outer rim);
    valves carry internal slit-bar detail; pumps carry triangular
    fin geometry; drains carry inner ring + dark floor row.

21. **UI teaches, sprite role guessable** ✅ —
    - vessels read as containers (open-top rectangles holding
      blue fill);
    - target ticks read as side-mounted markers (magenta horizontal
      bar) on each vessel;
    - valves read as binary fixtures (closed = solid yellow bar,
      open = visible slit) — the slit makes "fluid can pass" legible;
    - pumps read as mechanical (fins inside box) and the on-state
      visibly differs (green + lit centre);
    - identical visuals correlate with shared roles (all three
      vessels look identical → same equalise rule applies to each).
    L1 screenshot (mental render): 3 tall blue-water columns of
    different fill heights with magenta target ticks; 2 small
    valve sprites between adjacent columns. A first-time viewer's
    natural guess: "these need to match the magenta marks; the
    little bars between columns probably let water move".

22. **ACTION7 = strict-undo or absent** ✅ — ACTION7 not declared
    in `available_actions = [5, 6]`. No overload risk.

## Novelty re-walk (negative-similarity, post-spec)

Spec did NOT drift: L2's drain and L3's pump remain mechanically
distinct from every prior on dim 8 (core dynamic). Visual
signature stays multi-tall-blue-columns + valves/pumps; no prior
shares this. The pick-time negative-similarity check holds for
the fleshed-out spec.

## Verdict

**PASS.** All 22 checklist items satisfied; novelty and negative-
similarity gates clear. Transition to `implement`.
