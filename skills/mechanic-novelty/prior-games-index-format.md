# `prior-games/index.md` schema

`prior-games/index.md` is a cumulative table the harness maintains
across runs. It is empty (header-only) on the first run; every
successful run appends one row in `finalize`.

## Schema

| Column | Type | Source | Example |
|---|---|---|---|
| `game_id` | 4-char string | generated in `pick_mechanic` per `id-generation.md` | `qj17` |
| `mechanic_family` | short tag (2-3 words, lowercase, hyphen-separated) | from the spec's "## 2. Mechanic family" subsection | `tile-flip-with-mirror` |
| `description` | <140-char sentence | from the spec's title + mechanic family lines | `Click cells to flip them; player must produce a level-specific mirror-symmetric pattern.` |
| `timestamp` | ISO-8601 with timezone | `date -u +%Y-%m-%dT%H:%M:%SZ` at finalize time | `2026-04-26T13:42:11Z` |
| `seed` | one-line user seed or `(autonomous)` | run input | `(autonomous)` |

## Format

Pipe-separated markdown table. The header row is fixed:

```markdown
| game_id | mechanic_family | description | timestamp | seed |
|---|---|---|---|---|
```

Followed by one data row per generated game, **appended** in
generation order (do NOT re-sort — newest entries are at the
bottom).

## Initial state

When the harness is first set up, `prior-games/index.md` exists
with only the header rows above. The harness MUST tolerate this
empty-corpus state: `pick_mechanic` reads the file, sees only the
header, and proceeds with no prior-game similarity to check.
