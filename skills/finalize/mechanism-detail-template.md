# Per-game mechanism-detail file (for `prior-games/<game_id>/`)

After the `metadata.json` is written and the index row is appended,
generate a `prior-games/<game_id>/mechanism-detail.md` mirroring the
format of the 25 reference games' files under
`skills/mechanism-details/<id>.md`. This file becomes the deeper
view that future runs' novelty checks consult.

## Required structure

Use this template, filling each section from `workspace/mechanic-spec.md`
(plus `workspace/final-report.md` where helpful):

```markdown
# <game_id> — <mechanic-family-tag>

## Summary
3-5 sentence prose paragraph drawn from the spec's §1 (Title) + §2
(Mechanic family) + the final-report's Mechanic paragraph. Cover:
what the player controls, primary action(s), win condition in plain
words, key constraint, side-effects.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
(one row per action used; reuse §5 of mechanic-spec)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | ... | ... |
| 2 | ... | ... |
| 3 | ... | ... |
(EXACTLY 3 rows — this generator caps at 3 levels.)

Each row's "Specific challenge / constraint" cell MUST include the
shortest action-sequence witness for that level, copied verbatim
from `mechanic-spec.md` § 4 (e.g. `Witness [ACTION5, ACTION5]` or
`[5, 4, 2, 2, 5]`). This is the player-facing record of "how do
I beat this level"; it must not be omitted.

## Win condition

Plain-English description of the predicate guarding `next_level()`.

## Lose condition

Plain-English description of the predicate guarding `lose()`. If
none, write "no lose state".

## Internal state

Bullet list of key state the Game class tracks. Use semantic names
(this is for human/agent readability; the obfuscation step at
release time is separate).

## Notable code patterns

2-5 bullets on reusable techniques (HUD widget, sprite-swap idiom,
conflict resolution, etc.).
```

This file is the catalogue counterpart to `skills/mechanism-details/`
for GENERATED games. The next run's `pick_mechanic` and
`critique_spec` will consult it for any near-miss against this
prior game.
