# implement

## Description
Emit the full Python source for the generated game at
`prior-games/<game_id>/<game_id>.py`,
plus a sibling `metadata.json`. Follow `code/universal-scaffold.md`
exactly. The game has EXACTLY 3 `Level(...)` entries per
`design-constraints/composition-and-tutorial.md`. Encode the
mechanics so each level's witness must exercise every mechanic
available at that level (no hidden mechanics). Do NOT use surface
comments that reveal the mechanic intent (per
`code/universal-scaffold.md` style rules).

**Match the styling of the reference games.** Before writing,
re-skim the source of one or two reference games at
`game_sources_3_lvls/<id>/<hash>/<id>.py`
(prefer the five you already read in full during the `study`
state). The reference games encode a consistent house style — use
them as the template for:

- `sprites = {...}` dictionary placement (top of file, alphabetised
  keys, palette-only pixel arrays).
- `levels = [...]` list (flat top-level constant, one `Level(...)`
  per entry with `sprites=`, `grid_size=`, optional `data=`).
- Module-level palette / dimension / tag constants.
- `class <PascalClass>(NovaBaseGame)` body order: `__init__` →
  `on_set_level` → helpers → `step` → `_get_hidden_state` →
  `_get_valid_actions`.
- `RenderableUserDisplay` subclass for the step bar, registered
  via `Camera(interfaces=[...])`.
- Tag-based dispatch via `level.get_sprites_by_tag(...)` for any
  group of sprites that share a behaviour.

**Naming convention** — the reference games use obfuscated
random-token names (e.g. `lzajfunopv`, `qkndvajqsk`) because they
are released to a competitive setting where source-cracking is a
real concern. Our generated games are prototypes and **must use
meaningful semantic names throughout** (sprite dict keys, sprite
`name=` field, helper class names, helper-method names, constants).
The full rule and rationale lives in
`code/universal-scaffold.md` § Style rules. Do NOT copy the
reference games' obfuscation.

Steps in order:

1. Create directory: `mkdir -p
   prior-games/<game_id>/`.
2. Write `<game_id>.py` (single file_create call; the file may
   be 400-1500 lines for a 3-level game).
3. Write `metadata.json` with this exact schema:
   ```json
   {
     "game_id": "<id>",
     "title": "<spec section 1 title>",
     "default_fps": 30,
     "tags": ["claude-generated"],
     "baseline_actions": <list of action ints used>,
     "local_dir": "prior-games/<id>",
     "date_generated": "<ISO-8601 UTC timestamp>"
   }
   ```
4. Verify the .py file syntactically parses:
   `python -c "import ast; ast.parse(open('prior-games/<id>/<id>.py').read())"`
5. **Runtime smoke test (REQUIRED):** instantiate the generated game
   and run a small sequence of actions on level 1 to verify the
   engine accepts it. From the repo root:
   ```bash
   python -c "
   import sys; sys.path.insert(0, 'prior-games/<id>')
   from <id> import <PascalClass>
   g = <PascalClass>()
   print('instantiated OK; level count:', len(g.levels))
   # Optional: simulate a few actions to confirm step() runs.
   "
   ```
   If instantiation raises, FIX the implementation before transitioning. Do NOT proceed to finalize on a broken game.
6. Clean up any `__pycache__` directories the smoke test created
   under `prior-games/<id>/`:
   ```bash
   find prior-games/<id> -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
   ```

## Skills
- skills/global
- skills/code

## Next States

### smoke_test
**Condition:** Both `<game_id>.py` and `metadata.json` exist
under `prior-games/<game_id>/`, AND the .py file parses as valid
Python (no SyntaxError), AND the runtime smoke test (step 5)
instantiated without raising.
**Deliverables:**
- implement-summary.md: paths to the two files, line count of the
  .py file, and a 3-5 line plain-English summary of the implemented
  rule (NOT including any cell-level coordinates from the spec).
