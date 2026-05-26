# Step #11: finalize (terminal)

## Inputs Consumed
- `workspace/mechanic-pick.md`: game ID, mechanic-family tag, seed (autonomous).
- `workspace/mechanic-spec.md`: §1 title + §2 mechanic family + §5 action mapping + §4 per-level layouts (used to compose final-report.md and mechanism-detail.md).
- `prior-games/kx14/{kx14.py, metadata.json}`: the final outputs whose paths are referenced in the report.
- `prior-games/index.md`: read to confirm the header is intact and the two existing rows (kf42, qz73) precede the new append.
- `skills/finalize/{index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md}`: the procedures.

## Deliverables Produced
- **Index row appended** to `prior-games/index.md` via `echo >> ...`. Verified with `tail -3` showing the new row at the bottom: `| kx14 | tide-tilt-buoyant | Tide-Tilt Buoyant — vertical fluid tank where ACTION1/2 raise/lower the water surface, ACTION3/4 tilt floating balls, ACTION6 anchors. | 2026-04-29T01:42:31Z | (autonomous) |`
- `workspace/final-report.md`: per `final-report-template.md` — game ID, paths, lines-of-code, mechanic paragraph, action mapping, level summary, novelty note vs sp80 + qz73, index-update confirmation.
- `prior-games/kx14/mechanism-detail.md`: per `mechanism-detail-template.md` — summary + action mapping + per-level mechanic progression + win/lose predicates + internal state + notable code patterns. This is the deeper view future runs' similarity-check will consult.

## Notes
- Timestamp captured via `date -u +%Y-%m-%dT%H:%M:%SZ` at finalize time = `2026-04-29T01:42:31Z`. (The state-log narrative uses the within-run advancing timeline; the appended-row timestamp is the actual UTC moment of the append.)
- `mechanism-detail.md` was authored BEFORE archiving (per the state spec ordering note: it sources from `workspace/mechanic-spec.md` which gets archived in the next step).
- Run-archive will be the closure step: move `workspace/*.md` and `workspace/logs/*.md` into `prior-games/kx14/run-archive/` and `prior-games/kx14/run-archive/logs/` respectively, then verify the workspace is empty.
- Per the run-harness skill: do NOT append a new state_log row after the terminal state's body (this IO log itself is the terminal log).
