# Appending a row to `prior-games/index.md`

In `finalize`, the agent appends ONE row to
`prior-games/index.md`. Use this exact procedure:

1. Read the current end of the file. Confirm the header rows are
   present (see `mechanic-novelty/prior-games-index-format.md`); if
   the file is missing the header, write the header before
   appending.
2. Construct the row from the workspace artefacts:
   - `game_id`: from `mechanic-pick.md` (or from the path the
     game source landed at).
   - `mechanic_family`: from `mechanic-spec.md` section "## 2.
     Mechanic family", normalised to lowercase-hyphen-separated.
   - `description`: rebuild as `<title> — <one-sentence summary>`
     from the spec, capped at 140 chars.
   - `timestamp`: from `date -u +%Y-%m-%dT%H:%M:%SZ` run NOW.
   - `seed`: the run's seed input, or the literal string
     `(autonomous)` if no seed was passed.
3. Append the row using a single `bash` command (NOT a manual edit
   that risks rewriting the file). Use:

```bash
echo "| <game_id> | <mechanic_family> | <description> | <timestamp> | <seed> |" \
  >> prior-games/index.md
```

4. Verify the row landed by `tail -1` on the file and confirming it
   matches the constructed row.
