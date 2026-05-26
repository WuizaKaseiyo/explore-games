# Archiving the workspace at run-end

After `finalize` writes `final-report.md` and appends the index
row, copy the per-run workspace deliverables into the game's
prior-games archive so the run history is co-located with the
generated game.

In what follows, `<WORKSPACE>` is your per-run workspace
(`runs/<run_id>/workspace/`) as set up
by the run-harness skill. The next harness run gets a fresh
`runs/<new_run_id>/workspace/` directory, so there is nothing to
"clean up" here — only an archival copy.

Procedure (run from the repo root):

1. Create archive directory:
   ```bash
   mkdir -p prior-games/<game_id>/run-archive/
   mkdir -p prior-games/<game_id>/run-archive/logs/
   ```

2. Copy all workspace deliverables into the archive. Both `.md`
   and `.py` deliverables (the smoke-test custom checks live in
   `*.py`) need to be copied:
   ```bash
   cp <WORKSPACE>/*.md \
      <WORKSPACE>/*.py \
      prior-games/<game_id>/run-archive/ \
      2>/dev/null || true
   ```

3. Copy the per-state IO logs and the state-log:
   ```bash
   cp <WORKSPACE>/logs/*.md \
      prior-games/<game_id>/run-archive/logs/
   ```

4. Verify the archive populated:
   ```bash
   ls prior-games/<game_id>/run-archive/
   ls prior-games/<game_id>/run-archive/logs/
   ```
   Expected: `mechanic-pick.md`, `mechanic-spec.md`, `critique-pass.md`,
   `implement-summary.md`, `smoke-test-pass.md`, `final-report.md`,
   any `*.py` smoke-test custom checks, and (under `logs/`)
   `state_log.md` plus one IO log per state visit.

The per-run `<WORKSPACE>` itself stays in place under
`runs/<run_id>/` — it is the canonical run record and the TUI's
state-log tail target. The archive copy is the convenience
co-location for users browsing prior-games.

The archive layout becomes:

```
prior-games/<game_id>/
├── <game_id>.py
├── metadata.json
├── mechanism-detail.md
└── run-archive/
    ├── mechanic-pick.md
    ├── mechanic-spec.md
    ├── critique-pass.md
    ├── critique-revisions.md   (only if a revision occurred)
    ├── implement-summary.md
    ├── smoke-test-pass.md
    ├── final-report.md
    └── logs/
        ├── state_log.md
        └── <step>_<state>_io.md  (one per state visit)
```

All co-located under `prior-games/<game_id>/`: the artefact (.py +
metadata), the catalogue entry (mechanism-detail.md), and the run
history (run-archive/) live together.
