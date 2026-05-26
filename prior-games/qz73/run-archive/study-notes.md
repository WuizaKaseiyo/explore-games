# Study Notes — NovaPlay game-generation primer

Distilled from reading the 25 reference games' deep-analysis files + level_1
screenshots, three reference sources in full (cn04, tu93, sb26), and the
NovaPlay §3.4 design constraints. Used to anchor `pick_mechanic`.

The cumulative prior corpus has 1 entry: `kf42` (tether-pawn-cycle —
two pawn-blocks on a walled grid, click-select + arrow-move + walk-on-pad
re-tints). The negative-similarity-check explicitly warns against the
"two coloured pawns on a walled grid" surface signature; a candidate
that visually IS kf42 in different costume is rejected even with a
correct positive distinguishing-rule paragraph.

## Cross-cut frequency observations

Counts derived from the 25 frequency-table sections (tagged YES across the
full 25-game evidence layer). UNKNOWN entries are excluded from the
denominator.

| Feature | YES count | Reading |
|---|---|---|
| Step-counter HUD (depleting bar) | 24/25 | The single most universal pattern. The lone "no" (`g50t`) substitutes a scrolling-timer sprite that plays the same role. **Every generated game should have one.** |
| Has a depleting resource | 25/25 | Always step-counter; sometimes also pour-attempts (sp80), strikes (su15, r11l), or lives (ls20 has 3). |
| Has lives mechanic (separate from step-counter) | ~4/25 | Rare. Most games use only the step counter for lose. |
| ACTION6 used (click) | 19/25 | Click is the default modal verb. The arrow-only games are: g50t, ls20, re86, tr87, tu93, wa30. |
| Click-to-select (then arrow-move) idiom | 11/25 | ar25, cd82, cn04, ka59, m0r0 (with lever), s5i5, sb26, sp80 — when click is paired with arrows, this is the dominant pattern. |
| ACTION5 (modal/distinctive verb) | ~8/25 | When present, this is where each game stamps its identity (rotate, commit, fire, cycle-active, lock-or-unlock). When ACTION5 is in `available_actions` but does nothing distinctive, the slot is wasted. |
| ACTION7 (undo) | 6/25 | Minority. ar25, bp35, lf52, sb26, sk48, su15 use it. Generated games should NOT assume undo is available unless the mechanic specifically rewards it. |
| Tag-based grouping (`level.get_sprites_by_tag`) | ~23/25 | Almost universal. cd82 and r11l use `get_sprites_by_name` instead — equivalent intent. |
| `level.get_data("StepCounter")` for per-level budget | ~20/25 | Standard idiom. The level dict carries the budget and `on_set_level` reads it. |
| Multi-mechanic active within a single level (vs. one new mechanic per level) | 1/25 | Only `ls20` layers two mechanics inside one level. Reference games introduce ONE new mechanic per level — composition happens at L_n by *combining* L_{n-1}'s and L_n's mechanics, not by activating two new ones together. |
| Tutorial L1 solvable by random play | 0/25 confirmed YES | Most are explicit NO; some UNKNOWN. The §3.4 "random can stumble through L1" rule is satisfied only loosely; most reference tutorials still demand at least targeted action. |
| HUD position bottom (single-row depleting bar) | 13/25 | Dominant. Top: 4 (dc22, sp80, su15, sb26-middle row 53). Right edge full-height: 1 (ar25). Multi: 1 (m0r0 top+bottom). |
| Background colour value 5 (black) | 13/25 | Dominant. Variants: 0 (g50t), 1 (ka59, wa30), 2 (sc25, tr87), 3 (ls20), 4 (cn04 module, dc22, ft09, lp85, sb26), 10 (lf52, cn04 L1 override), 12 (sp80, cn04 L2 override). |
| Distinct mechanics across L1-L3 in source | 1-3, mode = 1-2 | Reference games typically have ONE base mechanic with 1-2 wrinkles introduced in L2/L3. Our 3-level cap forces ALL 2 mechanics into L1+L2 with composition mandatory in L3. |
| Palette size used | range 7-14, typical 9-11 | A deliberate small palette (3-6 distinct values + transparent) is what the constraint files prescribe; some reference games drift higher because of late-level features that don't apply at L1-3. |

Cross-cut takeaway: a generated game with a bottom-row step-counter HUD,
tag-based sprites, exactly 3 levels, and ACTION5 carrying its distinctive
verb sits squarely in the centre of the reference distribution. Diverging
on the *mechanic* without diverging on these structural conventions
preserves "NovaPlay family resemblance" while leaving the mechanic
free to be novel.

## Recurring design moves (patterns to inherit)

1. **Tag-based sprite querying as the load-bearing API.** ~23/25 games
   group sprites by `tags=[...]` then query `level.get_sprites_by_tag(...)`
   in `on_set_level` and per-step logic. Lets level configs add/remove
   instances without per-instance code. Concrete example: tu93's
   `get_sprites_by_tag("vhlesexlqd")[0]` for the walkable underlay,
   `get_sprites_by_tag("albwnmiahg")` for primary agents.
2. **`RenderableUserDisplay` step-counter that paints a single row of
   the 64×64 frame.** Universal HUD pattern. cn04's `qdcvayjdkm` and
   tu93's `klmvbszflr` are minimal templates: `current_steps` int +
   `render_interface(frame)` that fills `frame[63, :]` (or `frame[0, :]`)
   with two colours proportional to `current/max`. Constructor takes
   `mimisncrjk` (max steps); a setter updates current; render proportions
   by ratio.
3. **Phase-machine animation via `phase_tick: int = -1` sentinels.**
   sb26 has 8+ such phase ints (xjxrqgaqw, bbiavyren, lmvwmlqtw, ...);
   each starts at -1 (idle). Step() begins with a chain of
   `if self.<phase> >= 0: <advance frame>; return`, then falls
   through to action handling only when no phase is running. Lets
   long animations finish without mixing with input.
4. **`_get_valid_actions()` that shapes the action enum by game state.**
   cn04 returns ACTION1..5 only after a piece has been clicked; before
   first click it returns the default (which is just ACTION6). sb26
   pre-enumerates all valid (x,y) clicks based on what's clickable
   right now. Reusable as "hide irrelevant inputs from the agent".
5. **Click-to-select + arrows-to-move + ACTION5-to-commit-or-rotate.**
   The most common "verb composition" in the reference set
   (ar25, cn04, ka59, m0r0, sb26, s5i5 partial). Selection state is held
   on `self.selected_sprite`; arrows operate on the selection;
   ACTION5 either rotates (cn04) or commits (sb26).
6. **Sprite reuse via `clone() + set_position() + set_rotation() +
   color_remap()` per level.** sb26's level data shows the same
   `sprites["lngftsryyw"]` cloned 7+ times per level with each clone
   re-coloured to a different palette value via
   `color_remap(None, <palette>)`. cn04 sets per-level rotation
   (`set_rotation(90)`) on cloned sprites. Generated games should
   apply this to keep the sprite library minimal.
7. **Win predicate as a small pure function called at the end of every
   action.** cn04's `exlcvhdjsf()`: "no `8`-pixel left unmatched".
   tu93's `vpaafwwtxk` + `rodqliwlhy`: "every primary agent on an
   exit". Each is a trivial loop over sprites; if True, call
   `self.next_level()`. Position-or-pixel equality is the dominant
   primitive — never numeric thresholds.
8. **Per-level budget via `level.get_data("StepCounter")`.** Set in
   each `Level(... data={"StepCounter": N})` block; read in
   `on_set_level`. Lets you tune difficulty per-level by changing
   one integer in the level dict, not the source.

## Recurring anti-patterns (things to avoid)

1. **A single mechanic scaled across all levels.** §3.4 explicitly
   names this as the canonical anti-pattern. The reference set
   nevertheless commits it heavily (cn04, ft09, lp85, sk48, sp80,
   tr87 all "1 mechanic" per their own frequency tables). For our
   3-level cap this is FATAL — we MUST introduce a second mechanic
   in L2 and force composition in L3. Do not copy "more pieces in
   L2, even more pieces in L3".
2. **Encoding game state in pixel cells (`sprite.pixels[0, 1] = X`).**
   tu93's "marked" flag at `pixels[0, 1] == fltjxhzdlv` and kf42's
   hidden-state-as-pixels pattern are fragile. Generated games should
   keep state on `self.<attr>` and use `color_remap` for visual changes.
3. **Heavy sprite library with per-level near-duplicates.** lp85 (21k
   lines!) and tn36 inline near-identical sprites per level. Use
   `clone()` + `color_remap()` + `set_rotation()` instead.
4. **Random / cosmetic rotation of glyph cards** (tr87 line 897:
   `set_rotation(random.choice([0, 90, 180, 270]))`). Adds cognitive
   load without serving the mechanic. Glyphs should be deterministic
   from level data.
5. **Wall-collision tracked manually on top of `collidable=False`
   sprites** (wa30): the engine's collision system is not used; instead
   a `qthdiggudy` set of forbidden cells is recomputed each step.
   Generated games should set `collidable=True` and rely on the engine.
6. **ACTION5 in `available_actions` with no distinctive behaviour.**
   m0r0 lists ACTION5 but its handler is a no-op that just consumes a
   step. If ACTION5 is exposed, give it a real verb.

## Open questions for `pick_mechanic`

1. **Diverge on the visual signature, not just the mechanic.** kf42's
   level_1 is "two single-cell coloured pawns floating on an open
   walled black arena, palette {4, 5, 8, 9} + magenta HUD strip". The
   negative-similarity-check warns this was the exact failure mode of
   the prior vh68 candidate. Our candidate's L1 mental rendering
   should NOT be "small coloured movable on an open walled grid" —
   prefer a non-pawn-on-grid scene (a row of cells being modified, a
   canvas being painted, a structure being arranged, a tape being
   read, etc.). If we keep movable pawns, the sprites must NOT be
   plain rectangles in {red, blue} on a black field.
2. **Click-only, arrow-only, or hybrid?** kf42 is hybrid. Picking
   click-only or arrow-only would diverge on "what the player physically
   does". Click-only games (ft09, lp85, r11l, sb26, vc33) have a
   different feel — there is no avatar to identify with. Arrow-only
   games (g50t, ls20, re86, tr87, tu93) have a different feel too —
   the agent IS the game, not a hand selecting from outside.
3. **What is the second mechanic, and why does L3 need both?** A spec
   that introduces mechanic B at L2 but where L3 could be solved with
   just A (or just B) fails the §3.4 composition rule. The composition
   has to be *forced* — for example "B unlocks a region that A must
   then traverse", or "A creates a state that only B can reverse".
4. **Lose-mode: step-counter alone or step-counter + something?** The
   step-counter is universal; adding a hazard/chaser/obstacle-strike
   mode increases lose surface and complexity. For a 3-level
   generated game, step-counter-only is the cleanest default unless
   the chosen mechanic specifically rewards a hazard.

## Cited reference games (full sources read)

- **cn04** — minimal template for click-select + arrow-move + ACTION5
  rotate. Demonstrates `_get_valid_actions()` shaping based on
  selection state, and rotation-aware win predicate.
- **tu93** — minimal template for pure-arrow lockstep movement with
  walkable underlay (`vhlesexlqd` tag, pixel value 2 = walkable),
  three-phase step machine (input → enemy ticks → win-eval), and
  step-counter HUD.
- **sb26** — minimal template for click-place + ACTION5 commit +
  ACTION7 undo, with extensive use of phase-tick animation
  sentinels and per-level sprite cloning + colour remap.
