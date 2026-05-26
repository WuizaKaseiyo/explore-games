# `final-report.md` template

Write this file to `<WORKSPACE>/final-report.md` (where
`<WORKSPACE>` is the per-run workspace set up by the run-harness
skill, i.e. `runs/<run_id>/workspace/`)
as the terminal deliverable of `finalize`. Required sections:

```markdown
# Game generation final report

## Generated game
- **ID**: <game_id>
- **Source**: `prior-games/<game_id>/<game_id>.py`
- **Metadata**: `prior-games/<game_id>/metadata.json`
- **Lines of code**: `<wc -l output>`

## Mechanic
One paragraph (~80-150 words) describing the mechanic in plain
English: what the player controls, what they must do, what
constrains them, and how level progression composes earlier
mechanics. This is the sentence the user will read first when
deciding whether to keep the generated game.

## Action mapping
| Action | Effect |
|---|---|
| ACTION_<n> | <description> |
...

## Levels
Brief line per level: which mechanic is introduced or composed.

## Novelty note
- Closest taxonomy entry (and distinguishing rule).
- Closest prior-game entry (and distinguishing rule), or `(none —
  prior-games corpus was empty)`.

## Index update
Confirm one row appended to `prior-games/index.md`; show the row.
```
