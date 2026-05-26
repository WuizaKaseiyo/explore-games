# Reference-game patterns

The cached "study notes" — synthesised from every past run's
`workspace/study-notes.md` (kf42, qz73, kx14, qb84, lq5x, gv47,
hr8q, pj7k). Past runs always derived the same observations, so
the harness now serves them directly. Companion to
`cross-cut-frequencies.md` (which holds the numeric counts).

The agent reads this in `study`. **Do not re-derive.**

## Recurring design moves (inherit these)

1. **Step-counter HUD as a single-row depleting bar.** A
   `RenderableUserDisplay` subclass holding `(max, current)`,
   `set_current(remaining)`, and `render_interface(frame)` that
   paints `frame[63, :]` (or `frame[0, :]`) with two colours
   proportional to `current/max`. Universal pattern; `tu93`,
   `cn04`, `sp80`, `m0r0`, `sb26` are minimal templates.
2. **Tag-based sprite querying as the load-bearing API.** Sprites
   declare `tags=[...]`; runtime code calls
   `level.get_sprites_by_tag(...)` and
   `level.get_sprite_at(gx, gy, "tag")`. ~23/25 references use
   this. Lets level configs add/remove instances without per-
   instance code in the game class.
3. **Per-level data dict drives parameters.** Each `Level(...)`
   declares its budget and tunables in
   `data={"step_budget": N, ...}`; `on_set_level` reads them via
   `level.get_data("step_budget")`. Tunes difficulty per-level by
   editing one integer.
4. **Distinctive verb on ACTION5.** When ACTION5 is in
   `available_actions`, it carries the game's identity verb —
   rotate (`cn04`), commit (`sb26`), pour (`sp80`), lock
   (`m0r0`), cycle-active (`ar25`). Don't waste the slot on
   no-op or duplicate-of-arrows behaviour.
5. **Goal communication by visual coupling, not symbol.** Same
   colour → same role is the universal trick (`ka59`'s green
   target dot in a green ring; `cn04`'s red nub matching a red
   nub; `sp80`'s coloured cup wanting matching liquid). No on-
   screen text, no labels.
6. **Multi-phase `step()` with phase-tick sentinels for
   animations.** When one action triggers a multi-frame visual
   (`sp80`'s spill, `tu93`'s phase 0/1/2, `r11l`'s tween,
   `sb26`'s commit-marker walk), hold an integer cursor (or
   string state) and short-circuit `complete_action()` until
   the animation finishes. Pattern: at the top of `step()`,
   `if self._phase >= 0: advance one frame; return` before
   normal action handling.
7. **Sprite reuse via `clone() + set_position() + color_remap()
   + set_rotation()` per level.** One `sprites = {...}` dict
   declared once; level data clones with positional and colour
   variants. Sprite *kind* is generic, per-instance variation
   lives in level data. `sb26`, `cn04`, `m0r0` all do this.
8. **`_get_valid_actions()` shapes the action enum by game
   state.** When actions are context-gated (e.g. arrows only
   valid after a click-selection in `cn04`; only legal drop
   targets enumerable mid-drag in `sb26`), override
   `_get_valid_actions` to hide irrelevant actions from the
   agent. When no gating, inherit the default.
9. **Win predicate as a small pure function called after every
   action.** `cn04`'s `_check_win`, `tu93`'s exit-test,
   `kf42`'s pawn-on-pad bijection. A simple loop over a tagged
   sprite group; if true, call `self.next_level()`.
10. **Reduced state space at L1.** Tutorial level has fewer
    pieces, smaller reachable region, no hazards. `cn04` L1 has
    2 pieces; `sp80` L1 has 1 shelf + 2 cups; `tu93` L1 has
    just the maze and avatar.
11. **Click-to-select + arrows-to-move + ACTION5-to-commit-or-
    rotate** is the most common verb composition (~11/25). When
    using it, hold selection state on `self.selected_sprite`;
    arrows operate on the selection; ACTION5 either rotates or
    commits.
12. **Walkable region encoded as one big tagged sprite with a
    pixel-value flag.** `tu93`'s `vhlesexlqd` array — `pixels[i,
    j] == 2` defines reachable cells. Collision becomes one
    array lookup. Same idiom in `wa30` BFS, `ar25` reflector
    axes, `sp80` wall sprite.
13. **Two-sprite-swap idiom for state toggles.** Both variants
    pre-placed in the level; one `InteractionMode.TANGIBLE`,
    the other `REMOVED`; toggling swaps. Cleaner than
    `set_visible(False)` because collision is also gated.
    Documented in `code/universal-scaffold.md`.
14. **Letter-box padding around the playfield.** `Camera(
    letter_box=PADDING_COLOR)` — typically palette 3 or
    matching the background. The playfield's logical grid
    (12×12, 14×14, 16×16) sits centred inside the 64×64 frame.

## Discoverability through observable change

A good mechanic is hard to read off the static screen but
easy to learn by playing — every action should produce a
visible state change that lets the player update their
model of the rule.

**Multi-frame animation** is one technique. Instead of
resolving an action's effect in a single frame jump, the
game animates the resolution over several rendered frames.
Mechanically: `step()` advances one tick of an animation
phase counter and returns *without* calling
`complete_action()`; only when the animation finishes does
`complete_action()` run. The engine keeps re-rendering in
between, so the player sees motion instead of a teleport.

Examples from the reference set:

- **cd82** — ACTION5 fires the basket; the basket animates
  outward, deposits paint, animates back.
- **sp80** — pour action animates liquid travelling cup-to-cup
  over several ticks.
- **m0r0** — crash-flash plays over a few frames when a stone
  hits a hazard.
- **tu93** — avatar slides over a 3-phase cursor when stepping.
- **sb26** — commit-marker walks left-to-right across placed
  tiles frame by frame.
- **r11l** — dragged piece tweens across cells over several
  frames.

If the implementation pattern is unclear, refer to the source
of one or more of these games at
`game_sources_3_lvls/<id>/<hash>/<id>.py` — grep for `step()` returns
that aren't preceded by `complete_action()` to find the
phase-tick branches.

Animation is one means among many; the underlying rule is
that the game's *change* must be legible. A static instant
jump can also be legible if the change is small and local —
animate when an action's effect is non-local enough that a
single-frame snap would hide what happened.

**Two cases where animation is essentially mandatory, not
optional:**

1. **Long-distance transitions.** When an action moves an
   entity across enough cells in a single tick that a
   single-frame snap from source to destination would hide the
   path the entity took (teleport through a portal pair on
   opposite sides of the grid, slide along an unobstructed
   corridor until hitting a wall, projectile firing from an
   emitter to a target, etc.), the mechanic itself becomes
   invisible — the player sees the source state and then the
   destination state with nothing connecting them. Animate the
   transition over multiple frames so the path is visible. How
   many frames and how many cells per frame is a judgment call
   based on the specific mechanic; the rule is simply "enough
   that the cause-effect link reads on screen". Teleport is the
   canonical case: at minimum, render the entity arriving at
   the source portal and departing from the paired portal as
   distinct frames.

2. **Complex movement dynamics.** When an action triggers a
   multi-step or compound update — chain reactions (one event
   fires another), cascading collisions, multi-entity
   simultaneous moves, physics-style propagation, or any
   mechanic the player needs to *see unfold* to understand —
   render each intermediate step. If the player would need to
   read the source code to figure out what happened in a
   single tick, animation is the cheaper fix. Examples: domino
   topples (vn8d), chain merges, coupled-movement systems
   where pushing A triggers B which triggers C.

The decision rule when picking a mechanic in `pick_mechanic`:
if the mechanic *is* the long-distance / multi-step dynamic,
plan for a phase-machine implementation from the start. Don't
ship a static snap and hope the player infers the dynamic from
before/after state.

**No hidden state.** Any action that mutates a piece of game
state the player needs to reason about (selection, mode,
charge-level, lock/unlock, target-anchor, currently-active
turn-actor, etc.) MUST produce a visible cue in the rendered
frame for as long as that state is in effect — not just a
one-frame flash at the moment of change. The classic violation
is "click to select an object, but the object's appearance
is unchanged" — the player has no way to confirm which item is
active. Use `color_remap` (e.g., brighten the frame), a halo
sprite, an interaction-mode toggle, a HUD indicator, or a
secondary cursor — whichever fits the visual language. The
test: take a screenshot at any moment in the run and ask "can
the player still tell what state the game is in?". If the
answer requires recalling action history, the cue is missing.

**Design the UI to teach — the screen is the only instruction
the player gets.** NovaPlay's "no instructions" principle (see
`from-tech-report.md` § 4) means the visual is the entire
teaching channel: every object the player must reason about has
to make its role guessable from the rendered frame, or at least
guessable after a small number of exploratory actions. Practical
thumb-rules:

- *Sprite UI ≈ sprite role.* If an object has semantic meaning,
  its rendered look (shape, palette, size, position-context)
  should suggest that meaning — a button reads as pressable, a
  hazard reads as dangerous and is clearly distinguishable from
  the player's avatar.
- *Identical visuals imply shared or correlated roles.* Two
  visually-identical sprite kinds that behave very differently
  mislead the player; either give them a distinguishing visual
  or link their behaviour so the shared appearance reflects a
  real correlation. Conversely, two sprite kinds that ARE
  meaningfully correlated should share a visual cue so the
  player can read the correlation off the screen.
- *If the visual cannot carry the mechanic, change the
  representation* (and only if that fails, redesign the
  mechanic). The constraint flows: visual budget → mechanic
  complexity, not the other way around.

Enforced as `checklist.md` item 22.

## Recurring anti-patterns (do NOT inherit these)

1. **Single-mechanic difficulty escalation.** ~19/25 reference
   games scale a single mechanic across levels (more pieces,
   wider grid, more frames). §3.4 names this as the canonical
   anti-pattern and the harness's composition rule
   (`composition-and-tutorial.md`) forbids it. Generated games
   MUST add one or two *new* mechanics per level and require
   composition in L3.
2. **Per-level sprite explosion.** `m0r0` ships
   `jggua-Level1` … `jggua-Level11` — eleven hand-drawn maze
   variants. Works for a 12-level game; wasteful for our 3-level
   cap. Prefer ONE parameterised sprite plus reposition / re-tag.
3. **Tight step budgets that punish exploration.** `lp85` L1 has
   a 13-step cap that forbids any wrong move. `difficulty-rules.md`
   § d explicitly forbids this — be generous over the witness,
   especially in L2/L3 where mechanic-discovery costs steps.
4. **Behavioural state encoded as pixel-mutation.** `tu93`'s
   `pixels[0, 1] = activation_flag`, `r11l`'s drag-progress
   pixel flips. Fragile and indistinguishable from "the artist
   drew a different shape". Use `color_remap`,
   `set_interaction`, tag membership, or `self`-attributes
   instead.
5. **Implicit goal that requires source-reading.** Some L3 levels
   (`sk48`'s decoy snake; `cd82`'s arrow-tank L3) become legible
   only after 5+ min of trial. NovaPlay §5 requires 2-of-10
   humans solve in 20 min; harness's stricter target is ~6 min
   total. If a sighted human can't infer the L_n mechanic
   within ~2 minutes of play, the spec failed.
6. **Stochastic `step()`.** No reference game uses
   `random.random()` mid-step — everything is deterministic
   given (initial-state, action-sequence). Per-level layout
   randomness is OK at level-build time only. Recordings must
   replay (§3.5.1).
7. **Big-blocks-on-empty-field aesthetic.** Sparse 1×1 pawns
   and targets on a mostly-empty arena. Principle 1 of
   `negative-similarity-check.md` — pixel-detail richness
   matters; primary sprites should have internal pixel
   structure.
8. **Repeated dominant palette `{4 wall, 8 red, 9 blue}`.** The
   `kf42 → vh68` cautionary tale. Each generated game must reach
   for a different palette signature.
9. **Symbol or arrow glyphs in sprites.** Vertical bars, plus
   signs, dots are fine; anything resembling a letter, digit, or
   directional arrow glyph is forbidden by
   `forbidden-elements.md`.
10. **L3 is "L2 with a bigger grid".** Composition-rule
    violation. L3 must require the new L3 mechanic AND every
    earlier mechanic interacting (`composition-and-tutorial.md`,
    `checklist.md` item 10).
11. **Hidden mechanics that are present but optional, OR
    mechanics that are technically used in the witness but
    invisible to the player because a trivial fallback solves
    the level too.** A mechanic exposed in `available_actions`
    but not required by the witness is "hidden" in the harness's
    weak sense; forbidden by checklist item 11. A mechanic that
    is exercised by the witness but indistinguishable from a
    trivial-fallback strategy that also solves the level is
    "invisible" in the harness's strict sense; forbidden by
    checklist item 12. Both cases violate the inheritance + no-
    trivial-fallback rules.
12. **Decorative sprites that read as text/glyphs.** Even
    abstract shapes that resemble letters / digits / arrows
    fail the forbidden-elements check.
13. **Low-resolution rendering.** A small logical grid that the
    engine scales up into chunky uniform-colour cell-blocks
    wastes the 64×64 pixel budget and reads as crude. Even
    though some of the 25 reference games do this, generated
    games should aim higher: pack real internal pixel detail
    into every gameplay-relevant sprite (pawns, targets, walls,
    fixtures, HUD widgets) so the rendered frame looks
    detailful rather than coarse-blocky. Shape carries meaning;
    don't lean on colour alone to differentiate sprite kinds.
    Enforced as `checklist.md` item 21.

## Open questions `pick_mechanic` should resolve

These are the per-run choices the next state has to make. The
agent doesn't need to enumerate them again in study notes; just
internalise that each is on the table.

- **Action palette.** Click-only (~6/25), arrow-only (~7/25),
  or mixed (~12/25). Each is a coherent design family — pick
  one, don't mix two unrelated palettes.
- **Camera mode.** Fixed-grid (most), or scrolling viewport
  (`ft09`, a few others), or camera-rescale per level. Default
  is fixed-grid; only deviate if the mechanic genuinely needs
  it.
- **Resources beyond the step counter.** 25/25 use a step
  counter; ~17/25 also surface an accumulating "captured /
  placed / matched" count. For a 3-level game, step-counter
  alone is enough unless the win condition is N-of-M tickoff
  (then a per-match progress dot helps).
- **Core-knowledge prior pairing.** Physics + objectness is
  over-represented; geometry + topology shows up in a few
  (`ar25`, `cn04`); agentness (chasing/patrolling NPCs)
  shows up in ~6 (`g50t`, `ka59`, `m0r0`, `su15`, `tu93`,
  `wa30`). Less-explored corners of the priors-cube are good
  hunting grounds.
