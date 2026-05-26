# Study notes — what an NovaPlay game *is*

Distilled across the 25 reference games' deep-analysis frequency tables,
three full source reads (sp80, tu93, r11l), the 14 rendered level_1 frames
opened during this state, the design-constraints suite, and the prior-games
corpus (kf42, qz73, kx14, qb84, lq5x).

## Cross-cut frequency observations (n=25 reference games)

Counts derived from the per-game `## Frequency-table contributions`
sections in deep-analysis. UNKNOWN/implicit answers counted as YES when
they describe a present-but-uninteresting widget.

- **Step-counter HUD: 25/25 YES.** Universal. Implementation is always a
  `RenderableUserDisplay` rendering a depleting bar at row 0 or row 63 (or,
  rarely, a column). Fed by `level.get_data("StepCounter")` or an
  equivalent dict key.
- **Lives mechanic: 2/25 YES** (ls20, sp80 — sp80's "lives" is its 4 pour
  attempts). Players do not respawn in the other 23.
- **Click-to-select (ACTION6 in `available_actions`): 17/25 YES.** Roughly
  two-thirds use mouse selection.
- **Tag-based grouping (`level.get_sprites_by_tag`): ~22/25 YES** (r11l
  uses `get_sprites_by_name` with prefix-stripping, equivalent intent).
  Convention is to group sprites by an opaque 10-char tag and query by
  tag in `step` / `on_set_level`.
- **Uses ACTION5 (modal verb): 9/25 YES** — ar25, cd82, cn04, lf52, m0r0,
  re86, sb26, sk48 (no — undo on 7), sp80, wa30. ACTION5 is where each
  game's distinctive verb sits.
- **Uses ACTION6 (click): 17/25 YES.**
- **Uses ACTION7 (undo): 6/25 YES** — ar25, bp35, lf52, sb26, sk48, su15.
  Default for new games should be NO.
- **Has level data dicts: 22/25 YES.** Used heavily for per-level params
  (StepCounter, GoalColor, rotation, seed). A first-class pattern.
- **Multi-mechanic per level (each level introduces a new mechanic that
  composes with the prior ones): 4/25 YES** — ls20 (rotation cycler →
  +refills → +colour cycler + plates), m0r0 (orbs → +hazards → +post-stones),
  cd82 (axial fire → +diagonal → +arrow-tank), tu93 (maze-step →
  +followers → +chasers), wa30 (lock-drag → +drone → +walls), ka59 (push →
  +more pawns → +enemies). 6/25 YES on a generous count. The other 19
  scale a *single* mechanic across levels, which §3.4 calls out as an
  anti-pattern for new games. **The harness's composition-and-tutorial
  rule REQUIRES the new game to land in the multi-mechanic camp** — one
  new mechanic per level, all carry forward.
- **Tutorial level random-solvable: 3/25 YES** (loose, several UNKNOWN).
  Random-resistance is the norm even at L1, despite the report saying
  "random agents can occasionally stumble".
- **Has depleting resource (≡ step counter): 25/25 YES.**
- **Has accumulating resource (target-hit count, etc.): ~17/25 YES.**
- **HUD position breakdown:**
  - bottom row: ~14/25 (cd82, ka59, lp85, re86, sb26, sc25, su15, tn36,
    tr87, tu93, vc33, wa30, sk48 (row 53), s5i5).
  - top row: ~6/25 (cn04, ft09 has bottom in viewport, sp80 top, su15
    top).
  - column / edge: 2/25 (ar25 right column, r11l left column).
  - dual / split: 1/25 (m0r0 top + bottom).
- **Background colour distribution:** 3 (4 games), 5 (8), 4 (5), 1 (2),
  10 (1), 2 (2), 12 (1), 0 (1). Black-grey backgrounds dominate.
- **Padding colour distribution:** 3 (~14), 4 (3), 5 (1), 0 (2), 2 (1),
  1 (1). Padding is almost always grey-3.
- **Palette size used per game:** mostly 8–12 distinct values; outliers
  s5i5 (14), lf52 (16). Big takeaway: most games stay in a small palette.
- **Sprite-shape convention:** "mixed" 25/25 — every game uses a
  combination of solid blocks, hollow rings, glyph-pieces, and HUD bars.
  No game is mono-shape.
- **Camera scrolling beyond 64×64:** 4/25 (ft09 32×32 canvas, lp85
  scrolling viewport, g50t scrolling runway, ka59 small viewport over
  larger arena). Sticking to 64×64 single-frame is the norm and what we
  should do.

## Recurring design moves (keep these)

1. **Step-counter HUD as the lose trigger.** Always wire one. A single-
   row depleting bar driven by a `RenderableUserDisplay` reading
   `level.get_data("StepCounter")` is the canonical shape. tu93 and sp80
   both use this pattern verbatim.
2. **Tag-based sprite querying.** Define each sprite with an opaque
   10-char tag (`"ksmzdcblcz"` in sp80, `"vhlesexlqd"` for the maze in
   tu93) and look it up via `level.get_sprites_by_tag(...)` in step.
   Removes the need for hard-coded references and lets new sprites be
   added per-level without code changes. Universal across the 22-of-25
   that use it.
3. **Per-level data dict drives parameters.** `Level(..., data={"steps":
   30, "rotation": 0})` then `level.get_data("steps")` in
   `on_set_level`. Prefer this over hard-coding per-level constants in
   the class. sp80, tu93, ls20, lp85, ka59 all do this.
4. **Distinctive verb on ACTION5 when the game has more than four
   actions.** sp80's pour, cn04's rotate, sb26's commit, m0r0's lock,
   ar25's selection cycle. ACTION5 is an unusually expressive slot —
   reserve it for the verb that defines the game.
5. **Goal communication by visual coupling, not by symbol.** ka59's
   small filled green target inside a hollow target ring; cn04's red
   nubs that obviously want to pair to red nubs; sp80's three U-cups
   that obviously want filling. Same colour → same role is the
   universal trick.
6. **Multi-phase `step()` for animations.** sp80 keeps a `mlgebkvsmt`
   string in {"change", "spill"} and runs `spill` over many engine ticks
   until cups settle, only then `complete_action()`. tu93 uses an int
   phase 0/1/2 with the same shape. r11l tweens with `tjffy` over many
   ticks. The pattern is: while the animation is active, return without
   `complete_action`, and only finalise the action when the visible
   state has settled.
7. **Letter-box / padding decoration.** Most games render a thin frame
   border (Camera `letter_box=PADDING_COLOR`) around the playfield.
   Padding-3 / background-5 is the most common combination.
8. **Reduced state space at L1.** Fewer pieces, fewer obstacles, smaller
   reachable region. cn04 L1 has 2 pieces; sp80 L1 has 1 shelf, 1 spout,
   2 cups; tu93 L1 has just the maze and the avatar (no followers, no
   chasers).

## Recurring anti-patterns (don't inherit these)

1. **Single-mechanic difficulty escalation.** 19/25 reference games
   scale a single mechanic across levels (cn04, ar25, lp85, vc33, etc.).
   The §3.4 ban + the harness's composition rule rule this out for
   generated games — the new game must add **one mechanic per level**.
2. **Per-level sprite explosion.** Some games define dozens of one-off
   sprites for L4-L6 that never reappear (lp85, lf52). Stay disciplined
   — sprites should be reusable per *role*, not per *level instance*.
3. **Tight step budgets that punish exploration.** lp85 L1 has a 13-step
   cap that random play cannot survive. `difficulty-rules.md §d` is
   explicit: be generous over the witness, especially in L2/L3 where
   discovery time matters.
4. **Behavioural state encoded in pixel-mutation.** r11l flips
   centroid-arm pixels to mark "drag in progress"; tu93 mutates
   `pixels[0,1]` to track activation. This is fragile — use class
   attributes or `level.set_data` instead. The harness universal scaffold
   warns against pixel-mutation as state; we should keep state on `self`.
5. **Implicit goal that requires reading the source.** Some reference
   games' L3 ("decoy snake" in sk48; arrow-tank in cd82 L3) only become
   legible after a few minutes of trial. NovaPlay spec says human-2-of-
   10 must crack it within 20 minutes; if a sighted human can't infer
   the new mechanic in ~2 minutes of play, the spec has failed.

## Open questions for `pick_mechanic`

The mechanic family chosen next must answer all four:

1. **What is the distinctive verb, and on which action slot does it
   live?** ACTION5 modal, ACTION6 click-target, or arrow-as-verb?
2. **What are the THREE compositional mechanics (one per level, each
   carries forward)?** Concretely: M1 introduced by L1, M2 added at L2,
   M3 added at L3; the L3 witness must exercise all three.
3. **How does the game diverge — by ≥3 of the 8 negative-similarity
   dimensions — from each of the 5 priors (kf42 tether-pawn-cycle, qz73
   radial tip-lock, kx14 tide-tilt-buoyant, qb84 bead-lift-swap, lq5x
   lantern-cone-illuminate) AND from any near-miss reference game?**
   The visual signature of the prior-games corpus is already covered by:
   - kf42: dark frame, two coloured pawn-blocks, sparse field.
   - qb84: graph of coloured plus-marks with edges; mid-grey field.
   - kx14: split-tone tank (sky over water), small ring sprites.
   - qz73: mid-grey field with scattered hollow rings + small swatches.
   - lq5x: dark field + yellow ring targets + small avatar/glow.
   So the candidate should reach for a different palette and a different
   "what is on the board" answer (not pawns-on-an-empty-grid; not
   coloured-rings-as-targets-on-grey).
4. **What is the lose condition and what does its difficulty floor look
   like at L1, L2, L3?** Step counter is the universal default; only
   diverge if the mechanic genuinely needs a different lose channel.
