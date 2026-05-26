# finalize

## Description
Terminal state. Append a row to
`prior-games/index.md` per
`finalize/index-row-format.md`. Write `final-report.md` per
`finalize/final-report-template.md`.

Do NOT modify `<game_id>.py` or `metadata.json` in this state — they
are the final outputs.

After the index is appended and `final-report.md` is written, perform
two final closure tasks per their respective skill files:

1. **Author the per-game mechanism-detail catalogue.** Per
   `finalize/mechanism-detail-template.md`, write
   `prior-games/<game_id>/mechanism-detail.md`. This file is the
   deep counterpart to the 25 reference-game files under
   `skills/mechanism-details/`; future runs' similarity-check will
   read it for any near-miss against this newly-generated game.

2. **Archive the workspace.** Per `finalize/run-archive.md`, copy
   every workspace deliverable + per-state IO log into
   `prior-games/<game_id>/run-archive/`. The per-run workspace
   itself stays in place under `runs/<run_id>/workspace/` (the
   canonical run record); the archive copy is the convenience
   co-location for users browsing prior-games. The next harness
   run gets a fresh `runs/<new_run_id>/workspace/` so there is
   nothing to clean up here.

Order matters: write `mechanism-detail.md` (uses workspace files
as source) BEFORE archiving.

## Skills
- skills/global
- skills/finalize

## Deliverables
- final-report.md: Per `finalize/final-report-template.md` — game
  ID, paths, mechanic paragraph, action mapping, level summary,
  novelty note, and confirmation that the index was updated.
- (Side effect, not a workspace deliverable) one new row appended
  to `prior-games/index.md`.
- mechanism-detail.md: Per `finalize/mechanism-detail-template.md`,
  written to `prior-games/<game_id>/mechanism-detail.md`. The
  deep-view catalogue entry for this generated game.
- run-archive/: Per `finalize/run-archive.md`, populated under
  `prior-games/<game_id>/run-archive/` with the moved workspace
  contents.
