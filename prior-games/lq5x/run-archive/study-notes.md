# study-notes.md — pre-pick orientation

This file consolidates the cross-cut signal from the 25 NovaPlay
reference games (deep analyses + level_1/2/3 PNGs), three full
source reads (`cn04`, `sp80`, `tu93`), and the design-philosophy
skills under `skills/conventions/` and `skills/design-constraints/`.

## 1. Cross-cut frequency observations

Counts are over the 25 reference games' Frequency-table sections.

| Trait | Yes / 25 | Notes |
|---|---|---|
| Step-counter HUD as the lose trigger | **25 / 25** | Universal. Default is single-row depleting bar; rare exceptions (g50t implicit via scroll). |
| Lives mechanic | 1 / 25 (ls20: 3 lives) | sp80's "4 pour attempts" is per-level, not lives. Generated games typically should NOT have a respawn loop. |
| ACTION6 click in `available_actions` | 19 / 25 | Most games include click. Pure-arrow exceptions: `g50t`, `ls20`, `re86`, `tr87`, `tu93`, `wa30`. |
| ACTION5 modal / freedom slot | 9 / 25 | `ar25 cd82 cn04 lf52 m0r0 re86 sb26 sp80 wa30`. Where novelty most visibly lives. |
| ACTION7 undo | 6 / 25 | `ar25 bp35 lf52 sb26 sk48 su15`. Undo is the exception, not the norm. |
| Tag-based grouping (`get_sprites_by_tag`) | ~21 / 25 | Universal pattern — every type of object gets a tag and is queried by tag. |
| Level data dicts (`level.get_data` / `set_data`) | majority | Per-level config (StepCounter, BackgroundColour, palette knobs) is the dominant pattern. |
| Tutorial random-solvable | mostly NO/UNKNOWN | Even L1 typically resists random play; "solvable by random" is rare. |
| Multi-mechanic per environment (across L1-3) | every game has 2+ mechanics introduced | Range 1-4 distinct mechanics across L1-3 (median 2-3). One-mechanic-with-bigger-grid is the called-out anti-pattern. |
| Has accumulating resource | ~14 / 25 | Common pattern for "progress towards win" alongside the depleting step counter. |
| HUD position | bottom (modal), top, middle, right-edge, multiple | Bottom row is the dominant convention; top is also fine. |
| Palette size used | range 7-14, mode ~9-10 | Small, deliberate palettes win. |
| Background colour | various; 5 most common | Then 4, 3, 2. Avoid white-on-white or full-saturation chrome. |

**Structural backdrop the harness adds on top of those 25:**

- **Exactly 3 levels** (override of §3.4 ≥6) — see
  `composition-and-tutorial.md`.
- **One new mechanic per level promotion**: L1=N base mechanics
  (N≥1), L2=N+1, L3=N+2. Every mechanic must be required by the
  level's witness solution (no hidden mechanics).
- **Difficulty floor & ceiling** (`checklist.md` item 16):
  random / vision-blind / small text-LLM agents must have
  near-zero chance per level; whole environment ~6 minutes for an
  attentive human or top vision-LLM (~2 minutes per level); L2
  must demand non-trivial planning (not single-step / follow-the-
  colour); L3 must require strictly deeper sequencing where order
  matters and greedy/monotone strategies fail.

## 2. Recurring design moves

Patterns to **inherit** when authoring a new game:

- **Tag-based sprite querying.** Every distinct role gets a tag
  string at sprite-construction time; runtime code uses
  `level.get_sprites_by_tag(...)` rather than hard-coded names.
  Confirmed in `cn04` (uses `sys_click`), `tu93` (deep tag set:
  `vhlesexlqd`, `albwnmiahg`, `vllvfeggte`, `zzuxulcort`,
  `natiyqayts`, `xboyuzuyxv`), `sp80` (`ksmzdcblcz`, `nkrtlkykwe`,
  `xsrqllccpx`, `uzunfxpwmd`, `hfjpeygkxy`).
- **Step-counter HUD widget as a `RenderableUserDisplay`
  subclass.** Owns a `current_steps` field, has an `update`
  method, paints one row of palette pixels in `render_interface`.
  See `cn04.qdcvayjdkm` (top row, 32-wide centred), `sp80.gxetqmbwgi`
  (full-width top row), `tu93.klmvbszflr` (decrements via
  `zdxmrkxivd` then renders). Engine wires it via
  `Camera(interfaces=[hud])` or `camera.replace_interface([...])`.
- **`on_set_level` resets and rebuilds** all per-level mutable
  state from scratch — caches, selection handles, accumulators.
  This is what keeps levels independent and recordings replayable.
- **Selection-highlight via in-place pixel substitution.**
  cn04's `lceflskdhw` recolours the selected sprite's non-nub /
  non-overlay pixels to palette 0 and reverts on deselect.
  sp80 does the analogous swap to palette 9 ("blue active") with
  layer raise. The pattern: keep an "original pixels" cache
  (`npwwu` / `agupi` in cn04, runtime mutation in sp80) and
  re-derive the highlight every action.
- **Level-data dict for per-level knobs.** `level.get_data("X")`
  reads things like step budget, background colour, rotation
  flag, target sequence. Avoids hard-coding per-level magic.
  Keeps the level array compact.
- **`_get_valid_actions` overrides for action gating.** cn04
  uses `self.fubdf` to alternate "click → move/rotate" cycles;
  sp80 gates click after pour; the convention is to subclass
  `_get_valid_actions` and return a filtered list of
  `ActionInput`. **Note for novelty work**: action-gating is itself
  an interesting design lever, but not by itself a mechanic.
- **Win/lose checked at the top or end of `step()`.** Most games
  call `complete_action()` once at the bottom, with `next_level()`
  / `lose()` invoked in branches. The order is: read action,
  branch, mutate state, recompute predicates, fire `next_level`
  or `lose` if applicable, `complete_action`.

## 3. Recurring anti-patterns

Things to **avoid** inheriting:

- **Sprite-library bloat.** cn04 ships ~23 glyph sprites in
  `sprites = {...}` but only 8 are placed in L1-L3 (the rest are
  for L4+ — out of our scope but still loaded). Generated games
  with our 3-level cap should ship a tight sprite roster (one
  template per role) and reuse via `clone().set_position(...)`.
- **Two un-tagged sprites mixed in with tagged siblings.**
  cn04's `ezhdijgxgn` and `kodeocvgpm` lack `sys_click` while
  their siblings carry it; the game compensates with
  `ignore_collidable=True`, but cross-cut analyses will miscount.
  Be uniform.
- **Per-sprite full-render predicates each step.** cn04's
  `exlcvhdjsf` re-renders every sprite from `npwwu` and scans
  for stray palette-8 cells every step. For 5+ sprites this
  starts costing real ms. Counter-based predicates (e.g.
  "satisfied_targets == n_targets") scale better.
- **Behavioural state encoded in pixel-mutation alone.** sp80
  re-paints `xsrqllccpx` to palette 13 to mark "drain spent".
  Works but couples render and game logic. Cleaner: a parallel
  `set[Sprite]` for the spent set, plus a render pass that
  derives pixel colour from membership.
- **Sprite-library mirror twins.** cn04 ships `kddtjradhp` and
  `kodeocvgpm` — same colour, same outline modulo chirality.
  Risks visual confusion if both ever appear. Pick one and use
  rotation/flip for the other.
- **Single-mechanic-with-bigger-grid as "L3."** Called out in
  §3.4 verbatim ("scaled in size or difficulty are an
  anti-pattern"). The harness's `composition-and-tutorial.md`
  enforces "exactly one new mechanic per level promotion" plus
  "every mechanic available at the level is required by the
  witness".

## 4. Visual signature range across the 25 + 4 priors

A quick pass over level_1.png screenshots covering
nub-pair-glyph (cn04), pour-shelf (sp80), maze-pickup-train (tu93),
shape-mirror-cover (ar25), tile-place-commit (sb26), row-col-shift
(lp85), sokoban-explode (ka59), mirror-orb-merge (m0r0), lock-drag-crate
(wa30), paired-snake-trail (sk48), orbit-fire-paint (cd82),
centroid-puppet-leg (r11l), colour-cycle-walk (dc22),
cycler-attribute-match (ls20), stamp-3x3-paint (ft09),
program-pawn-trace (tn36) — plus all four prior-games
(kf42, qz73, kx14, qb84) — surfaces the following diversity:

- **Background palette**: ranges over light-blue (cn04), saturated
  orange (sp80), black (tu93, kf42, ka59 grey, wa30 light-grey,
  cd82 black), bright cyan (ar25), very dark grey (sb26, qb84,
  ls20), checkerboard (tn36), split halves (m0r0 yellow/orange),
  light-grey (qz73), tank-split (kx14).
- **Sprite grain**: ranges from single-cell pawns (kf42, qz73,
  qb84, ka59), to 3-9-cell glyphs (cn04, ar25, ls20), to large
  16x16+ canvases (ft09, tn36, lp85, m0r0).
- **Density**: ranges from very sparse (cn04: 2 sprites, qz73:
  6 sprites) to dense (ft09: ~37 stamp cells, lp85: ring of
  pawns + buttons, tn36: full 12x12 board).
- **HUD location**: top (cn04, sp80, su15), bottom (tu93, sk48,
  cd82, sb26, vc33, tn36, wa30, lp85, ls20, tr87, ka59), right
  edge (ar25), left edge (r11l), top+bottom (m0r0).
- **Mood / texture**: priors **kf42** and **qz73** are very
  sparse "dots on a flat field" (high risk for the next game to
  visually echo if it also uses pawns-on-grid). **kx14** has a
  distinctive split-tank look. **qb84** has a chained-graph
  look with peg sprites flanking the chain. None of these four
  lean on textured wall mazes (tu93, ls20, m0r0, r11l) or onto
  big stamp/canvas patterns (ft09, lp85, tn36).

## 5. Open questions for `pick_mechanic`

To resolve in the next state. The novelty bar requires that the
candidate diverges from the four priors on **at least three of
the eight dimensions** in `negative-similarity-check.md` (what
is on the board, what the player physically does, what the level
asks for, what kills the player, the cast of supporting elements,
visible visual signature, pixel grain of primary sprites, core
dynamic).

1. **Action-set shape.** Among the four priors:
   - kf42: `[1,2,3,4,6]` (click-select + arrows)
   - qz73: `[5, 6]` (rotate + click)
   - kx14: `[1,2,3,4,6]` (arrows + click; ACTION1/2 raise/lower
     surface, ACTION3/4 tilt, ACTION6 anchor)
   - qb84: `[1,2,3,4]` (pure arrows with directional verbs)
   So no prior has used `[1,2,3,4,5]` (arrows + a freedom verb,
   no click) or `[6,7]` (click + undo) or `[1,2,3,4,5,6,7]`
   (everything). A different shape is a fresh axis.
2. **What is on the board.** The four priors all use small
   discrete coloured sprites against a flat background. Reaching
   for **a structured field** (a drawable canvas; a graph laid
   out as a tape; a stack/heap of layered cells; a ribbon/track
   wrapping the playfield; a continuous line that the player
   bends) would diverge harder than yet another "scattered
   coloured pawns" board.
3. **What kills the player.** All four priors use only the step
   counter. A second failure axis (hazard contact; collapse of a
   structure; pour-attempts-style limited-attempt budget;
   exhaustion of a non-step resource) is available room.
4. **Core dynamic — what is the player thinking about?**
   - kf42: "how do I drag the second pawn around without losing
     the colour I just set?"
   - qz73: "which tips do I lock so the rotation aligns the
     remaining ones?"
   - kx14: "can I route this ball up through this platform-blocked
     column by alternating tilt and rise?"
   - qb84: "which peg do I have to swap-and-restore so this
     bead's colour propagates to its target?"
   The next game should ask a *different question* — for
   example: "what shape can I sculpt out of this material before
   the budget runs out?" or "in what order do I need to rewire
   this network?" or "which side of this surface do I need to
   flip onto?". A genuinely fresh core dynamic, not a fifth
   coloured-pawn-routing puzzle.

These four questions are the input to `pick_mechanic`'s decision.

## Sources read in this state

**Deep-analysis Frequency-table sections (all 25 — collated via
shell into the cross-cut counts in §1):**
ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85,
ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15,
tn36, tr87, tu93, vc33, wa30.

**Three full source files** (covering different action-set
shapes):
- `game_sources/cn04/65d47d14/cn04.py` (681 lines) — click +
  arrows + ACTION5 rotate. Patterns: `_get_valid_actions`
  override for click→move alternation; `npwwu`/`agupi` cache
  pair for selection-highlight; `RenderableUserDisplay`
  subclass for the step bar; per-level `BackgroundColour`
  override.
- `game_sources/sp80/0ee2d095/sp80.py` (874 lines) — click +
  arrows + ACTION5 pour. Patterns: `state` field as an
  enum-like string (`"change"` / `"spill"`) driving multi-frame
  spill animation; `try_move_sprite` returning collisions;
  multi-level `set_rotation` viewport gimmick;
  `level.get_data("rotation")` and `udeubouzyp`/`fewyrfijcb`
  for coordinate remap.
- `game_sources/tu93/2b534c15/tu93.py` (1251 lines) — pure
  arrows. Patterns: phase-machine inside `step()`
  (`self.iuubfszcoi` cycles 0 → 1 → 2 across follow-up frames);
  heavy tag-based queries (`vhlesexlqd`, `albwnmiahg`,
  `vllvfeggte`, `zzuxulcort`, `natiyqayts`, `xboyuzuyxv`);
  `level.get_sprites_by_tag(...)` everywhere; arrow-keys map to
  rotation values 0/90/180/270 first, then movement.

**Skill files internalised**:
`skills/global/{action-enum, color-legend, paths}.md`,
`skills/conventions/from-tech-report.md`,
`skills/design-constraints/{checklist, composition-and-tutorial,
core-knowledge-priors, forbidden-elements}.md`,
`skills/mechanic-novelty/{taxonomy-of-25-games,
similarity-check, negative-similarity-check,
prior-games-index-format}.md`.

**Visual signatures** (level_1.png passes): all 4 priors
(kf42, qz73, kx14, qb84) plus reference samples cn04, sp80,
tu93, ar25, sb26, lp85, ka59, m0r0, wa30, sk48, cd82, r11l,
dc22, ls20, ft09, tn36.
