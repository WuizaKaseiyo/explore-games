# Study Notes — NovaPlay Game Generation, Run 4

Source coverage: read `mechanism-details/*.md` for all 25 reference
games (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85,
ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36,
tr87, tu93, vc33, wa30); viewed level_1 PNG visual signatures across
~17 of 25; read 3 full source files end-to-end:
`game_sources/cn04/65d47d14/cn04.py` (681 lines, click+arrows+ACTION5
jigsaw), `game_sources/r11l/aa269680/r11l.py` (1822 lines, pure click,
centroid-puppet-leg), `game_sources/ls20/9607627b/ls20.py` (2042
lines, pure arrows, cycler-attribute-match). Read all 5 design-
constraint / convention docs in full. Read the 3 prior `mechanism-
detail.md` files (kf42, qz73, kx14).

---

## 1. Cross-cut frequency observations (25 reference games + 3 priors)

| Cross-cut feature | Count | Notes |
|---|---|---|
| Step-counter / energy HUD as primary lose trigger | 25/25 (+3/3 priors) | Universal. Either engine `_action_count` (cn04, ka59) or private `_steps_used` / `sjcuorclg` counter (qz73, kx14, sb26, sp80). |
| `available_actions` includes ACTION6 (click) | 23/25 | Exceptions: ls20, tu93, tr87 (pure cardinal motion). |
| `available_actions` includes ACTION1..4 (cardinal motion) | 16/25 | Pure-arrow games: ls20, tu93, tr87, m0r0 (+lever click), re86. |
| `available_actions` includes ACTION5 (freedom slot) | 8/25 | cn04 (rotate), cd82 (fire-sweep), m0r0 (no — uses 6 for lever), re86 (cycle marker), sb26 (commit row), sp80 (commit/spill), wa30 (pickup/drop), g50t (commit path). qz73 prior also uses ACTION5 as "advance dial". |
| `available_actions` includes ACTION7 (undo) | 6/25 | ar25, bp35, lf52, sk48, sb26, su15. Most games omit undo. |
| Pure click `[6]` only | 5/25 | ft09, lp85, vc33, r11l, tn36 (and s5i5). |
| Pure arrows `[1,2,3,4]` only | 3/25 | ls20, tu93, tr87. |
| Click-to-select-then-arrows | 6/25 | cn04, ar25, ka59, sk48, m0r0 (lever variant), kf42 prior. |
| Two-sprite swap (TANGIBLE↔REMOVED) for state | 5+/25 | dc22 (multi-state name suffix), kx14 prior (float/anchored), qz73 prior (lock-overlay). Also ka59's edge-collider strips. |
| Tag-based level introspection (`get_sprites_by_tag`) | 25/25 | Universal in `on_set_level`. |
| Per-instance recolour via `color_remap(None, palette)` | ≥10/25 | qz73, kx14, ls20, vc33, sb26, kf42 — clone one definition, remap per instance. |
| Pre-enumerated ACTION6 candidates in `_get_valid_actions` | 4/25 | r11l (16×16 grid), su15 (16×14), qz73 prior (per-tip slot centres), sk48 (per-head centres). |
| Frame-queue / animation phase machine | 8/25 | bp35, lf52, cd82, sb26, sc25, sp80, su15, ka59. |
| Hidden state used | universal | `_get_hidden_state` returns small `np.int16` array — usually action count or selection index. |
| Reduced camera (16×16 with cell scaling) | 5/25 | ft09, lp85, sb26, ls20, tn36. Most games use the default 64×64. |

### Win-condition family distribution (from taxonomy descriptions)

| Family | Games |
|---|---|
| Cover/match every target with a corresponding object | ka59, r11l, su15, wa30, sp80, sk48, s5i5, ar25, cn04 |
| Repaint canvas to match a target image | cd82, ft09, re86, vc33 |
| Reach a goal cell (with state) | bp35, lf52, tu93, sc25, g50t (multi-target traversal) |
| Match a row/sequence | sb26, tr87, lp85 |
| Multi-pickup ordered claim | ls20 |
| Trace a target pattern | tn36 |
| Sprite-snap (8-pixel connectors) | cn04, ar25 |

### Lose-condition stack

- Step counter zero: 25/25 (always present).
- Multiple "strikes" / lives: 4/25 (lf52, ls20 [3 lives], r11l [5 strikes], su15).
- Hazard contact instant-fail: 2/25 (bp35 spikes, ka59 enemy collision).
- Wasted-attempt budget separate from steps: 2/25 (sp80 [4 spills], r11l [5 obstacle hits]).

## 2. Recurring design moves (load-bearing patterns)

1. **Step-counter HUD is the default lose mechanism.** Build a tiny
   `RenderableUserDisplay` subclass that renders a 1-row depleting bar
   (cn04 `qdcvayjdkm`, kx14 `bekzbtmcoz`, qz73 `kfnplrxazq`, r11l
   `bdxsqgndfy`); read budget from `level.get_data("StepCounter")` per
   level. cn04 reads engine `_action_count`; qz73/kx14/sb26 maintain
   a private `_steps_used` so misclicks can be free.
2. **Tag-based sprite roles, not per-level Python branches.** Every
   well-organised game routes its level-init through
   `level.get_sprites_by_tag(...)` and stores the lists in fields
   (kx14 `_balls`, qz73 `tips`/`sockets`, ls20 `plrpelhym`/
   `srgbthxut`). Per-level *behaviour* is then driven by `level.data`
   keys plus tagged sprite presence — not by `if level_index == 5`
   branches (which dc22 uses sparingly and is an anti-pattern).
3. **One sprite definition per role, cloned + recoloured per
   instance.** qz73 clones one tip and one socket definition,
   colour-remaps per instance. ls20 clones one shape definition and
   recolours via `color_remap(epeqflmtfc, ...)`. kx14 clones one
   float-ball + one anchor variant. This keeps the sprite registry
   small and visual identity comes from level data.
4. **ACTION5 carries the game's distinctive verb when present.** The
   eight ACTION5 games each install a verb impossible to confuse with
   "directional motion" or "click somewhere": commit (sp80, sb26,
   g50t), rotate (cn04), fire (cd82), cycle (re86), pickup/drop
   (wa30), advance-dial (qz73 prior). A new game using arrows + click
   should put its identity on ACTION5 unless the distinctive verb
   genuinely lives in *what* gets clicked or *which* arrow is pressed.
5. **Click-to-select-then-arrows is the canonical "manipulate one of
   N pieces" idiom.** cn04, ar25, ka59, sk48, kf42 prior all use it.
   `_get_valid_actions` returns ACTION6 only before the first
   selection (kf42's gate); after selection ACTION1..4 are added. The
   click selects the locus; arrows do the verb.
6. **Atomic two-pass commit for "everything moves at once".** qz73's
   `_rotate_unlocked` (every unlocked tip advances simultaneously),
   ka59's pending-direction dict (every block resolves before
   collision), m0r0's per-quadrant simultaneous move, tu93's
   "every primary agent moves in lockstep". When multiple things
   change on one action, compute proposals first and commit second.
7. **Visual feedback by sprite-pair swap, not pixel mutation.** kx14
   prior's float/anchored pair (one TANGIBLE, one REMOVED), qz73's
   lock-overlay pair, dc22's multi-state name suffixes. The
   `InteractionMode` swap is cleaner than mutating `pixels` because
   the alternative state is fully inspectable in the level and
   renders as a different sprite.
8. **Pre-enumerate ACTION6 candidates when click-space is small.**
   r11l (16×16 grid of click-targets), su15 (16×14), qz73 (per-tip
   slot centres). Returning a tabular `_get_valid_actions` lets the
   agent treat the world as a finite policy.
9. **Tutorial L1 communicates by being playable.** Forbidden: on-
   screen text, hint pop-ups, arrow glyphs. Allowed: single piece +
   single target, hint sprite revealed only one cycle-shift away
   (ls20 `hoswmpiqkw`), or a colour-coupled target↔piece pair so the
   player infers "this hole wants this block" (ka59, kf42, kx14, all
   priors). Random play should sometimes stumble through L1 — that
   is acceptable per §3.4.

## 3. Recurring anti-patterns to avoid

1. **Per-level `if level_index == k` branches in `step` or
   `on_set_level`.** dc22 has at least one (`level_index == 5` patches
   a tile to add a tag). bp35 has nested per-level budget conditionals.
   These are brittle; prefer level-data flags (`AnchorEnabled`,
   `Children`, `BackgroundColour`) consumed declaratively.
2. **Single-mechanic-with-bigger-grid as L2 / L3.** Explicitly named
   in §3.4 of the tech report. lp85 and ft09 lean on this — their
   late levels are "more buttons" / "more stamps" rather than a new
   mechanic. Our 3-level cap requires *one new mechanic per level
   promotion* and every prior mechanic must remain *required* by the
   witness. The `composition-and-tutorial.md` rule is binding.
3. **Hidden / decorative mechanics.** A mechanic that sits in the
   engine but the witness never exercises is forbidden by
   `composition-and-tutorial.md`. Easy to slip in (e.g. a "hazard"
   that the optimal route skirts but never touches) and easy to fail
   the §3.4 mechanic-count check on.
4. **Pixel-mutation as state encoding.** sb26 stamps hint stripes
   into slot pixels; kx14 rebuilds the water sprite's pixel array
   per tide change. These work but break replay-friendliness if
   you're not careful with copies; prefer sprite-pair swap (idiom 7
   above) where there are discrete visual states.
5. **Visual-signature collision with priors.** The cautionary tale
   in `negative-similarity-check.md` (vh68 vs kf42) showed that even
   correct distinguishing-rule paragraphs cannot rescue a candidate
   that visually IS a prior in a different costume. Concretely
   means: don't pick "multi coloured pawns on a small walled grid
   with a step bar" again — kf42 already did that.

## 4. Open questions for `pick_mechanic`

1. **Verb-slot architecture.** kf42 = click+arrows; qz73 = ACTION5 +
   click; kx14 = arrows + click. We have NOT done a pure-click game
   yet (ft09/lp85/vc33/r11l/sb26/tn36 territory) and we have NOT
   done a pure-arrows game (ls20/tu93/tr87/m0r0/re86 territory). A
   pure-click or pure-arrows game would diverge on the action-space
   axis from all 3 priors immediately.
2. **Visual signature divergence.** The 3 priors use:
   kf42 — small-walled-grid, palette ~{4 wall, 8 red, 9 blue, HUD};
   qz73 — radial dial on dark background, colourful tips/sockets;
   kx14 — vertical tank, light-blue water + off-white air, colored
   balls. We need a fundamentally different **what is on the
   board**: not "coloured pieces on an arena" again. Candidate
   territories: a canvas being painted; a row of cards being
   cycled; tapes; buttons; a scrolling runway; a graph of nodes;
   a stamp/template grid.
3. **Core dynamic divergence.** All 3 priors are some flavour of
   "spatial manipulation of a few pieces under a step budget". A
   genuinely different dynamic would be: pattern-matching (what
   shape am I trying to produce?), rule-application (rewrite a
   tape under stated rules), program-construction (queue ops then
   run), or canvas-painting (turn a blank board into a target
   image). These are categorically different "what is the player
   thinking about" experiences.
4. **Compositional 3-level arc.** Per `composition-and-tutorial.md`
   the bind is one new mechanic per level promotion AND every prior
   mechanic still required by the witness. The picked mechanic must
   admit *exactly* a 3-step composition where L3 strictly exceeds
   L2's planning depth (a named trivial heuristic must fail at L3).
   Mechanics that compose cleanly: place-then-cycle, mark-then-
   chain, paint-then-mask, queue-then-execute. Mechanics that don't
   compose well into 3 levels: "navigate a maze" (L2 is just bigger
   maze), "click each cell" (L2 is just more cells).
