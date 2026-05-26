# Critique Pass — yf3h

Visit count: 1/10.

Spec reviewed: `workspace/mechanic-spec.md` (game `yf3h`, mechanic family `pulse-arm-burst-resonate`).

## Checklist (`design-constraints/checklist.md` items 1-20)

### Format & structure
1. **Sprites use only palette `0..15` and `-1` transparent**: ✅ — every pixel matrix in §3 uses `{−1, 0, 4, 6, 8, 9, 11, 14}`.
2. **File structure matches universal scaffold**: ✅ — spec calls for sprite bank, levels, constants, HUD widget, game class. (Final compliance verified at `implement`.)
3. **`available_actions ⊂ [1..7]`**: ✅ — `[5, 6]`.
4. **Exactly 3 `Level(...)` entries**: ✅ — L1 (12×12, 1 emitter + 1 resonator), L2 (12×12, 2 emitters + 2 resonators), L3 (12×12, 3 emitters + multi-resonator + green-resonator + 1 phase-delay tile).
5. **Game ID 4 lowercase chars, not in reference list, not in prior-games**: ✅ — `yf3h`. Verified absent from both reserved lists.

### §3.4 priors & constraints
6. **Mechanics from `core-knowledge-priors.md` only**: ✅ — physics (wave propagation), objectness (emitters/resonators/tiles as persistent objects), basic geometry (Manhattan rings).
7. **No letters / digits-as-glyphs / real-world clipart / cultural conventions**: ✅ — emitters are 5×5 filled squares, resonators are 5×5 hollow frames, phase-delay tiles are 3×3 corner-dot or solid-fill patterns, pips are 2×2 flat blocks. None resemble alphabet letters, digit-glyphs, or real-world objects. The hollow rectangular frame is a topological "container" shape (basic geometry), not a letter "O". The colour assignments (red/blue/green emitters) carry no in-game cultural meaning — colour is the colour-keying mechanic, not danger/go signalling.
8. **At least 2 distinct mechanics**: ✅ — M1 (`arm-fire-ring-strike-resonator`), M2 (`colour-keyed resonator`), M3 (`phase-delay tile`).
9. **L1 = tutorial: base dynamic system, all-required-by-witness, reduced state space, no on-screen text**: ✅ — 12×12 grid, 1 emitter + 1 resonator, single mechanic (M1), no walls/no hazards, witness 2 actions, no text.
10. **L2/L3 increase difficulty by COMPOSING mechanics, not by scaling**: ✅ — L2 keeps the 12×12 grid (no scaling) but adds M2; the witness composes M1 (fire) and M2 (colour-key matching). L3 keeps the same 12×12 grid (no scaling) and adds M3; the witness composes M1 + M2 + M3 — every action of the witness invokes at least one mechanic, and the multi-resonator activation provably cannot occur unless all three fire together.

### Mechanic structure (per-level)
11. **Mechanic inheritance and the +1-or-+2 rule**:
    - L1: N=1 (M1).
    - L2: M = N+1 = 2 (M1 carried + M2 new). ✅ Within {1, 2} new.
    - L3: M = L2-count + 1 = 3 (M1, M2 carried + M3 new). ✅ Within {1, 2} new.
    - Earlier-level mechanics remain present and required: M1 active at L1, L2, L3 (every fire uses it); M2 active at L2, L3 (single-colour resonator at L2; multi-colour resonator + green-resonator at L3). No drop-out. ✅

12. **Strict counterfactual necessity (per-mechanic table)**:

    | Level | Mechanic | Solvable without M? | Why not (concrete) |
    |---|---|---|---|
    | L1 | M1 | no | Only one resonator (`resonator_red` at (8, 6)). The level has no other affordance — the only way to set its centre-fill to white is to have a red ring strike it on its arrival tick. The only way to make a red ring exist is to arm `emitter_red` at (3, 6) and fire. Witness `[arm, fire]` activates M1 directly. |
    | L2 | M1 | no | Two resonators (red and blue) must be activated. Only path: arm and fire emitters. Without firing, no rings exist; resonators stay at hollow-frame-with-grey-centre. |
    | L2 | M2 | no | Without M2 (any-colour ring activates any resonator), arming JUST emitter_red and firing once would activate BOTH the red AND blue resonators. The witness would be 2 actions: `[arm emitter_red, fire]`, but this would NOT exercise M2's colour-key. With M2, the blue resonator at (9, 8) is unaffected by a red ring sweeping over it on tick 12 — only a blue ring activates it. The player MUST arm and fire the blue emitter to activate the blue resonator. |
    | L3 | M1 | no | Same as L2 — without firing, no resonator activates. |
    | L3 | M2 | no | The multi-resonator at (5, 5) requires `{red, blue}` multiset. Without M2 (no colour-keying), a single ring of any colour passing over it would activate it — the green ring (Manhattan 4 from emitter_green at (8, 5)) would do so on tick 4, trivially solving. With M2, only the red+blue combo activates it. The green-resonator at (5, 9) similarly — without M2, a red or blue ring (cross-colour, no path) wouldn't even reach it; with M2, only the green ring activates it. |
    | L3 | M3 | no | The multi-resonator's required `{red, blue}` simultaneity demands red and blue rings arrive on the SAME tick. Without M3, distances are 6 (red) and 7 (blue) — different ticks. The phase-delay tile at (1, 1) is the level's ONLY affordance for adjusting timing. Without engaging it, no number of fires aligns the rings. |

    **Independent enumeration of plausible alternates** (per checklist 12 emphasis):

    - **L3 alt-A "spam ACTION5 with no arms"**: ACTION5 with empty `_armed_emitters` produces no rings; resonators stay inactive. Repeated firing wastes budget. Cannot solve.
    - **L3 alt-B "fire each emitter individually"**: e.g., `[arm red, fire, arm blue, fire, arm green, fire]` — 6 actions. Each fire produces ONE ring; the multi-resonator at (5, 5) needs RED AND BLUE on the same tick, which separate fires cannot achieve. Each individual fire produces only one colour at the multi-resonator → multiset never matches. Multi-resonator stays inactive forever; level fails.
    - **L3 alt-C "click on the multi-resonator directly"**: resonator has no `armable`/`togglable` tag, click is no-op. Wasted step.
    - **L3 alt-D "arm everything, fire (no delay tile)"**: red ring at (5, 5) tick 6, blue tick 7 — multi-resonator's per-tick hits are `{red}` on 6, `{blue}` on 7, never both same tick. Multi-resonator inactive. Level fails.
    - **L3 alt-E "use only emitter_green to bypass the multi-resonator"**: green-resonator activates, multi-resonator stays inactive. Level fails.
    - **L3 alt-F "engage delay tile, but skip green emitter"**: multi-resonator activates (tick 7 for red+blue), but green-resonator stays inactive. Level fails — both resonators must activate.
    - **L3 alt-G "fire many times to randomly catch alignment"**: rings are deterministic. All fires produce the same arrival ticks. No randomness exploit.

    Every plausible alternate strategy fails. The witness `[toggle delay, arm 3, fire]` (5 actions) is the minimum AND the only family of solutions — variants reordering arm-clicks and the delay-tile click work as long as the delay tile is active when fire occurs.

    Geometric/spatial-blocking check: the delay tile at (1, 1) is on emitter_red's ring path at radius 2 (Manhattan 2), on emitter_blue's path at radius 9 (Manhattan 9 — but the multi-resonator decision is at tick 7, so blue is unaffected at the deciding tick), and on emitter_green's path at radius 11 (also after the decision tick). The geometry confirms: only emitter_red is delayed by the tile *at the moment that matters*.

### Novelty
13. **Mechanic family absent from `taxonomy-of-25-games.md`**: ✅ — `pulse-arm-burst-resonate` does not appear as a row.
14. **Mechanic family absent from `prior-games/index.md`**: ✅ — verified against the 22-row corpus.
15. **For SOUNDS-similar entries, distinguishing rule articulated**: ✅ — §9 of the spec gives concrete distinguishing rules vs every flagged near-miss (bx84, gv47, gx7m, kp9z, vn8d, kn58, fz5j, cd82, ka59).

### Solvability
16. **Win condition for the environment as a whole**: ✅ — implicit via the engine's `next_level()` → `win()` chain on completing L3.
17. **Lose condition**: ✅ — `self.lose()` when `_steps_remaining == 0`. Single failure mode.
18. **Difficulty floor and ceiling per `difficulty-rules.md` § 2 — every per-level (a)(b)(c)(d) bullet present**: ✅
    - L1: (a) random-resistance ✅, (b) ~1 min ✅, (c) NO STRICT planning ✅, (d) budget 12 (witness 2) ✅.
    - L2: (a) ✅, (b) ~2 min ✅, (c) 3 first actions / plausible-but-wrong = "fire each colour separately" / witness reasoning chain post-discovery ✅, (d) budget 16 (witness 3) ✅.
    - L3: (a) ✅, (b) ~3 min ✅, (c) 5 first actions / trivial heuristic = "arm-everything-fire" (which fails on multi-resonator) / where heuristic diverges = at fire-time tick-mismatch ✅, (d) budget 18 (witness 5) ✅.
    Step-budget monotonicity: 12 ≤ 16 ≤ 18 — does not shrink across levels. Slack ratios (6×, 5.3×, 3.6×) shrink, but the rule states "budget must NOT shrink absolutely", which is satisfied.

19. **No hidden state — every mutated state has a persistent visible cue**:
    - Emitter arm-state (player-mutable, multi-action lifetime): centre-dot pixel `4` (disarmed) vs `11` (armed). Persistent until next ACTION6 toggle or ACTION5 burst. ✅
    - Phase-delay tile active-state (player-mutable, multi-action lifetime): 4-corner-dot pattern vs solid-fill-with-white-centre pattern. Persistent. ✅
    - Resonator activated-state (sticky, level-lifetime): hollow-frame-with-grey-centre-dot vs solid-white-fill centre. Persistent. ✅
    - In-flight ring footprint (transient, animation-only): rendered to `ring_overlay` sprite each tick during the burst animation. Visible during animation; intentionally transient (rings are wave-fronts, not steady-state). ✅
    - Per-resonator per-tick hit (transient, ~3-tick flash on pip): visible during animation. Player only needs this state during the animation to reason about *why* a resonator did or didn't activate; not a between-actions reasoning state. ✅

20. **Visual detail floor (no-information-loss-at-32×32 test)**: ✅
    - Emitter: 5×5 filled square with centre-dot indicator. 2×2 average pool to ~3×3: outline + centre dot survive as recognisable "filled square with bright/dim mark".
    - Resonator: 5×5 hollow frame. 2×2 pool: hollow vs filled distinguishable.
    - Phase-delay tile: 3×3 with 4-corner-dot vs filled patterns. 2×2 pool degrades but the binary "sparse vs dense" distinction survives.
    - Pips: 2×2 flat blocks. Per checklist 20: pips are HUD-style multiset indicators, exempt like step-counter HUD bars.
    - Sub-cell detail carries semantics: filled square = emitter (active object), hollow frame = resonator (target awaiting input), corner-dot pattern = phase-delay (modifier). Each sprite type's role is describable from the pixel-matrix alone, without reference to colour. Colour then differentiates which colour each emitter/resonator is keyed to.

## Forbidden-elements re-check (per checklist 7)

- No sprite resembles a digit (no "5", "8", etc.).
- No sprite resembles a letter (the resonator's hollow rectangular frame is a topological shape, not "O" — "O" is rounded, this is rectangular with rounded corner cells).
- No real-world clipart (no flowers/keys/swords/tools/weapons).
- No cultural conventions (red/blue/green don't carry danger/go semantics; activated resonator's white-fill is "empty/clean", abstract).

✅

## Negative-similarity re-walk (`negative-similarity-check.md`)

The full spec is more concrete than the one-paragraph candidate. Re-walking the 7 dimensions for the 3 closest priors:

vs **bx84**: same on {ASK at surface "activate every target", KILLS budget, GRAIN 5×5 sprites}; different on {BOARD shape language, INPUT cardinality (mine has ACTION5+6, bx84 has only 6), CAST roles, VISUAL signature (rings vs lines), CORE DYNAMIC (timed multiset vs static routing)}. Three dimensions of overlap, two of which are weak (every step-budget game shares KILLS; every "activate-every-target" game shares ASK). DIFFERENT on principles {6, 8}.

vs **gv47**: same on {INPUT cardinality, KILLS, GRAIN}; different on {BOARD, ASK, CAST, VISUAL, CORE DYNAMIC}. DIFFERENT on principles {6, 8}.

vs **gx7m**: same on {KILLS, GRAIN}; different on {BOARD, INPUT (mine has ACTION5+6, gx7m only 6), ASK, CAST, VISUAL, CORE DYNAMIC}. DIFFERENT on principles {6, 8}.

No prior overlaps with the candidate on 3+ dimensions where 6, 7, 8 are heavyweight. Verdict: **NOVEL**.

## Verdict

**ALL 20 CHECKLIST ITEMS PASS.** **NOVELTY VERIFIED.** **PROCEED TO `implement`.**
