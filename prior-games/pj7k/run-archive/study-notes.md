# Study notes — run #9 (autonomous)

## Sources consulted

- **Evidence layer (25 reference games)**: read mechanism-details summaries
  for all 25 IDs (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52,
  lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15,
  tn36, tr87, tu93, vc33, wa30) plus the taxonomy-of-25-games table.
  Sampled prior-game level_1.png screenshots for visual signature
  (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52).
- **Three reference-game source files in full**:
  - `cn04` (681 lines, click + arrows + ACTION5 rotate) — anchors
    selection-then-manipulate idiom and pixel-level snap matching.
  - `sp80` (874 lines, arrows + click + ACTION5 commit) — anchors
    multi-phase animation, tilt/permutation tables, fluid spread.
  - `tu93` (1251 lines, pure cardinal motion, multi-agent lockstep)
    — anchors 3-phase step state machine, walkable-underlay tagged
    sprite as collision map, multi-species enemy AI.
- **Design philosophy**: read in full —
  `conventions/from-tech-report.md`,
  `design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md`,
  `mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md`,
  `global/{paths,action-enum,color-legend}.md`.

## Cross-cut frequency observations (from the 25 mechanism-details + taxonomy)

- **Step-counter HUD that drains 1+ per action and triggers `lose()`
  at zero**: 25/25. Universal. (Sp80, cn04, tu93, ar25, ka59, lp85,
  sb26, ls20, m0r0, r11l, re86, s5i5, sc25, sk48, su15, tn36, tr87,
  vc33, wa30, dc22, ft09, g50t, bp35, cd82, lf52). It is also a hard
  must-have per `core-knowledge-priors.md`.
- **Tag-based sprite querying** via
  `level.get_sprites_by_tag("...")`: 25/25.
- **64×64 base canvas with sub-cell scaling** through `Camera`: 25/25.
- **Action subsets**:
  - Pure-click `[6]`: ft09, lp85, r11l, s5i5, tn36, vc33 (≈6/25).
  - Pure-cardinal `[1,2,3,4]`: ls20, tu93, tr87 (≈3/25).
  - Cardinal+ACTION5 (`[1..5]`): cn04 [+6], sp80 [+6], cd82 [+6], wa30,
    re86, m0r0 [+6] — ACTION5 is the genuine novelty slot in ≈10/25.
  - Click+arrow combos `[1,2,3,4,6]`: ka59, dc22, m0r0, wa30 (≈4/25).
  - Includes ACTION7 undo: ar25, bp35, lf52, sb26, sk48, su15 (≈6/25).
- **ACTION6 click is a primary input** (selection or interaction) in
  ≈17/25.
- **Two-flag commit pattern (`win_pending`/`lose_pending` set this
  step, fired next step so animation finishes)**: g50t, tn36, sb26,
  sk48, sp80 (≈5/25, but reused widely as a recipe).
- **Multi-phase animation `step()` (commit → animate → resolve)**: cd82,
  sb26, sk48, su15, sp80, ka59, m0r0, sc25, tn36 (≈9/25).
- **Pre-enumerated quantised click grid** (cell-snapped ACTION6
  candidates returned by `_get_valid_actions`): r11l, su15 (≈2/25 but
  recommended for any pure-click game with a cell grid).
- **Snapshot-and-rollback or ACTION7 undo via state stack**: ar25,
  s5i5, sb26, sk48, su15, lf52 (≈6/25).
- **Selection model: click selects a "live" piece, then arrow keys
  manipulate IT (rather than a single global avatar)**: cn04, ar25,
  ka59, m0r0, sp80, sk48, dc22(arms) — ≈7/25. Gating via a `selected`
  flag flipped by ACTION6.
- **Grid sizes**: 16×16 (cd82, dc22, ft09, lp85, r11l, sp80, sc25,
  vc33, su15) and 20×20 (cn04 levels 1-5, sp80 L4-6) dominate; ls20,
  tu93 use larger maps via underlay sprites at full 64-pixel canvas.

## Recurring design moves to imitate

- **A walkable region encoded as one big tagged sprite** whose
  `pixels[i,j] == 2` defines reachable cells (tu93's `vhlesexlqd`).
  Lets collision be a single O(1) array lookup; same idiom used by
  wa30's BFS, ar25's reflector-axes, sp80's wall sprites.
- **Tag-encoded sprite roles**: every "object kind" gets a tag, and
  win/lose/AI predicates iterate `get_sprites_by_tag(tag)` rather
  than checking `isinstance` or names. cn04, ar25, ka59, sp80 all
  use this. The tag string is opaque (e.g. `"vhlesexlqd"`) so the
  agent cannot read intent off it.
- **A selection idiom**: ACTION6 click sets `self.selected = sprite`,
  the sprite's pixels are temporarily dimmed/highlighted to show
  selection (cn04 turns matching connector pixels from 8 → 0 while
  selected), then ACTION1-4 / ACTION5 act on `self.selected`. On
  re-click of the same sprite or click elsewhere, restore and swap.
- **Win-by-pixel-coincidence**: cn04, ar25, re86, lp85 win when, after
  an action, every "live" connector/marker pixel coincides with a
  matching cell of another sprite (or matches a target sprite's
  pixels). Computed via O(N) rendering then a dict keyed by world
  coords. Reliable, deterministic, easy to visualise.
- **Per-action visual feedback on the game's own sprites** (rather
  than HUD popups): cn04 flips matched 8→3, sb26 stripes hint colours
  into slot pixels, vc33 paints buttons blue/red. Keeps everything
  inside the 64×64 frame; no on-screen text needed for legibility.

## Recurring anti-patterns to avoid

- **Hidden mechanics that are present but optional**: lp85 has
  buttons whose effect is "discovered" only by trial. The
  `composition-and-tutorial.md` rule and checklist 10a explicitly
  forbid this — every mechanic active at level L must be REQUIRED
  by L's witness. Use mechanics in the witness, or remove them.
- **Tightening step budget to make difficulty**: re86, sc25 levels
  with shrinking budgets fight `difficulty-rules.md` — difficulty
  must come from puzzle depth, not budget tightness. Generated
  game's L3 budget must NOT shrink below L2's.
- **Per-level branching budget thresholds** (bp35: `if level==1: 64;
  elif level<6: 64*5; else 64*10`) — opaque to the player, easy to
  get wrong on a 3-level pipeline. Prefer one explicit `steps`
  level-data field per level, generous over the witness.
- **Random `random.random()` in step()** — every reference game
  carefully avoids it. tr87 uses per-level seeded layouts but the
  transition function itself is deterministic. §3.5.1 / checklist.
- **Decorative or tutorial sprites that read as letters / digits /
  arrows**: avoid even when they "feel" abstract. Per
  `forbidden-elements.md` — vertical bars, plus signs, dots are OK
  but anything resembling a glyph is rejected.

## Prior-games visual signatures (sampled level_1 PNGs)

- **kf42**: dark room, red+blue paired-pawn cluster — colour-pair
  pawn-on-grid signature.
- **qz73**: pale grey, scattered coloured single-cell tips around a
  central rotor — radial alignment.
- **kx14**: orange-and-blue tank with horizontal water-line bisecting
  the field — vertical fluid surface.
- **qb84**: dark field, lattice of saturated beads connected by line
  segments — chain navigation.
- **lq5x**: black field, two grey concentric squares + a small yellow
  lantern marker — sparse cone illumination.
- **gv47**: grey field, yellow filled blocks with a white pip and
  small dark-grey pip-rings — seed-bloom.
- **hr8q**: grey field, three empty bordered squares + magenta/cyan/
  purple ingredient + recipe ribbon — pair-blend.
- **ng52**: grey field, three large bordered bins, blue stick
  fragments scattered above — multiset signature.

Across the 8 priors, **dark-grey/grey backgrounds dominate**;
candidate game must reach for a different palette to satisfy
`negative-similarity-check.md`'s Principle 2.

## Open questions for `pick_mechanic`

- **Action axis with novelty.** ACTION5 has been used by ≈10/25
  reference games as the "freedom slot"; among priors only kx14
  (anchor) and lq5x (rotate cone) use it. Re-using ACTION5 with a
  fresh verb is a strong, under-used surface.
- **What "is on the board" diverges from priors?** Priors so far
  cover: pawn pairs (kf42, qb84), rotors/radials (qz73), fluid
  surfaces (kx14), chains (qb84), cones (lq5x), regions/canvas
  (gv47), recipes/widgets (hr8q), bins (ng52). Reference games add
  trains, sokoban blocks, fog rooms, mazes, programmes, tapes,
  buttons, sticks. **Under-explored on this corpus**: vertical
  layered/stacked structures (towers, stacks, columns of pieces)
  where pieces interact by gravity/equilibrium WITHOUT being a
  conventional Tetris-like fall.
- **Single-screen vs scrolling viewport?** All priors are
  single-screen. tu93 / sp80 / ar25 use larger underlay sprites but
  the camera covers the full play. Sticking to single-screen is
  safer and matches priors — no need to change.
- **Two mechanics to combine vs three.** Spec must satisfy 3-level
  composition (L1 base, L2 +1, L3 +2). Need a base verb that
  naturally admits TWO orthogonal additional mechanics, each of
  which actively constrains the witness solution. Candidates: a
  sliding/cycling primitive with an orthogonal "swap" or "carry"
  transformation.
