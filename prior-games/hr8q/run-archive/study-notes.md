# Study notes

## Cross-cut frequency observations

Drawn from `taxonomy-of-25-games.md`, the frequency-table sections of
`mechanism-details/*.md`, and the deep-analysis essence sections.

- **Step-counter HUD**: ~25/25 games. Universal lose trigger.
- **ACTION6 click as primary or selection verb**: ~22/25 (only
  arrow-only games like ls20, tu93 omit). Click hit-detection via
  `level.get_sprite_at(gx, gy, tag)` is universal idiom.
- **Tag-based sprite querying** (`get_sprites_by_tag`): universal.
- **`available_actions` minimal subset of `[1..7]`**: every game
  declares only the slots it actually uses. ACTION5 carries the
  game's distinctive verb when present.
- **Per-level data via `level.get_data(...)`**: ~24/25; standard
  pattern for step budget, witness layouts, mix tables.
- **Camera resize in `on_set_level` to match `grid_size`**: required
  whenever `grid_size != (64, 64)`; common pattern.

## Recurring design moves

- **Sprite bank → level construction → game class** is the universal
  scaffold (`code/universal-scaffold.md`). Every reference game and
  every prior follows it.
- **Color-remap helpers** for parameterising sprite color (`s = base
  .clone().color_remap(8, color)`). Used in qb84, qz73, gv47.
- **HUD step bar as a `RenderableUserDisplay`** drawing a horizontal
  filled bar at row 0 or row 63. Pattern in qb84, qz73, sb26, su15.
- **Hit-test by tag in `step()`**: `target = level.get_sprite_at(gx,
  gy, "ingredient")` returns None or the clicked sprite.
- **Witness-required `_get_valid_actions`**: enumerate the click
  positions (and any non-click verbs) the puzzle actually accepts;
  pre-shrinks the agent's action space.
- **State toggle by `InteractionMode`**: TANGIBLE ↔ REMOVED to
  show/hide variant sprites at the same cell (`code/universal-scaffold.md`
  § Two-sprite swap).

## Recurring anti-patterns to avoid

- **Big-blocks-on-empty-field aesthetic**: dense pixel grain matters.
  `negative-similarity-check.md` flags this as Principle 1.
- **Repeated dominant palette {wall=4, red=8, blue=9}**: kf42 / vh68
  cautionary tale. Candidate must reach for a different palette.
- **Symbol or arrow glyphs**: forbidden by `forbidden-elements.md`.
- **L3 is "L2 with a bigger grid"**: composition rule violation
  (`composition-and-tutorial.md`).
- **Stochastic `step()`**: violates determinism (`from-tech-report.md`
  §7).

## Open questions for `pick_mechanic`

- User seed is a recipe-style color-blend game with a left "formula"
  panel and right ingredient palette plus a target hint. **Closest
  prior**: gv47 (Seed Bloom) — also color-mix, but spatial / region-
  surround. Distinguishing rule: candidate has NO spatial canvas;
  blending is a pure recipe operation, not a region-merge.
- **Closest taxonomy near-misses**: sb26 (place-tiles-and-commit,
  Mastermind-style guess+feedback), tn36 (click button sequence to
  programme path), su15 (recipe-fruit-collect: collect N tokens of
  a flavour combination). All differ on core dynamic.
- **Action set**: `[5, 6]` is right — ACTION6 to click ingredients,
  ACTION5 as a commit/clear verb (or use auto-eval after 2nd pick).
- **Palette divergence from gv47**: gv47 uses big yellow/blue/red
  paint regions. Candidate should pick distinct ingredient hues
  (e.g. magenta, orange, light-blue, light-grey) and put the target
  preview in a contrasting frame so the visual signature reads
  totally differently from gv47.

## Sources read in full

- **qb84.py** (519 lines, prior, arrow-driven chain, sticky pegs):
  full source. Patterns: `_find_sprite_near` helper for layout,
  StepBarHud, two-sprite swap via color_remap, target sequence in
  `level.get_data`.
- **qz73.py** (394 lines, prior, ACTION5+ACTION6, tip-lock):
  full source. Patterns: socket+tip layered sprites, click hit-test
  by tag, lock-mark state via `set_interaction(REMOVED|INTANGIBLE)`,
  `_get_valid_actions` enumerates click coords, camera-viewport
  resize in `on_set_level`. **This is the closest structural template
  for the candidate.**
- **sb26 mechanism-detail (place-and-commit Mastermind)** as a third
  click+commit family example — its commit verb on ACTION5 with
  per-slot hint feedback is a useful negative reference (the
  candidate must NOT become a guess+feedback game).
