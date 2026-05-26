# Missing Oracle Recordings Summary

This document summarizes the `prior-games` levels that still do not have a
usable in-folder oracle solution recording after the latest recovery pass.

Checked on `2026-05-12` from:

- [prior-game-recordings-summary.json](prior-games/prior-game-recordings-summary.json)
- a direct file-presence scan for:
  - `oracle_solution.recording.jsonl`
  - `oracle_solution.mp4`
  - `oracle_verification.json`

## Totals

- `70` games still missing one or more oracle solution levels
- `168` unresolved level slots in total
- `147` level slots with `no_available_solution_artifact`
- `21` level slots with `mechanism_detail_witness_failed`

## No Available Solution Artifact

These levels still have no recovered oracle recording, and the current pass did
not find a reusable solved artifact or a sufficiently explicit witness for them.

| Game | Missing levels |
|---|---|
| `bz3k` | 2, 3 |
| `dh4j` | 1, 2, 3 |
| `ek73` | 1, 2, 3 |
| `gg01` | 1, 2, 3 |
| `gg02` | 1, 2, 3 |
| `gg03` | 1, 2, 3 |
| `gg04` | 1, 2, 3 |
| `gg05` | 1, 2, 3 |
| `gg06` | 1, 2, 3 |
| `gg07` | 1, 2, 3 |
| `gg08` | 1, 2, 3 |
| `gg09` | 1, 2, 3 |
| `gg10` | 1, 2, 3 |
| `gg11` | 1, 2, 3 |
| `gg12` | 1, 2, 3 |
| `gg13` | 1, 2, 3 |
| `gg14` | 1, 2, 3 |
| `gg15` | 1, 2, 3 |
| `gg16` | 1, 2, 3 |
| `gg17` | 1, 2, 3 |
| `gg18` | 1, 2, 3 |
| `gg19` | 1, 2, 3 |
| `gg20` | 1, 2, 3 |
| `gg21` | 1, 2, 3 |
| `gg22` | 1, 2, 3 |
| `gg23` | 1, 2, 3 |
| `gg24` | 1, 2, 3 |
| `gg25` | 1, 2, 3 |
| `gg26` | 1, 2, 3 |
| `gv47` | 2 |
| `gx7m` | 2, 3 |
| `hb5n` | 2, 3 |
| `hr8q` | 3 |
| `jc9r` | 1, 2, 3 |
| `jd4q` | 1, 2, 3 |
| `jx5k` | 2, 3 |
| `kf42` | 1, 2, 3 |
| `kn58` | 1, 2, 3 |
| `kx14` | 3 |
| `lq5x` | 3 |
| `lv4k` | 1, 2, 3 |
| `mr5q` | 1, 2, 3 |
| `ng52` | 2, 3 |
| `nz3v` | 3 |
| `pj7k` | 3 |
| `pq5w` | 1 |
| `qb84` | 3 |
| `qj4r` | 1, 3 |
| `qy7w` | 3 |
| `qz73` | 3 |
| `rj5w` | 1 |
| `rk7x` | 1, 2, 3 |
| `rs8n` | 3 |
| `tj4n` | 2 |
| `tk6n` | 1 |
| `vd3g` | 2, 3 |
| `vp6h` | 1, 2, 3 |
| `wm6q` | 2, 3 |
| `xn5p` | 1, 2, 3 |
| `xv2b` | 1, 2, 3 |
| `zw91` | 1, 2, 3 |

## Mechanism-Detail Witness Failed

These levels have witness text in `mechanism-detail.md`, but the current
generic replay path still does not reach `WIN` from those witness descriptions.

| Game | Failed levels | Notes |
|---|---|---|
| `bw7k` | 1 | Witness parsed, but replay still misses the game-specific progression semantics. |
| `bx84` | 1, 2, 3 | Click-coordinate witness is parsed, but replay still does not satisfy the in-engine win predicate. |
| `dj5h` | 1 | Later levels replay; L1 still fails under the current generic click/toggle path. |
| `kj82` | 1, 2, 3 | Witness exists, but the current parser/replayer is not yet matching the plank-selection interaction correctly. |
| `kp9z` | 2 | Partial success on other levels; this level's witness still fails under replay. |
| `mw8p` | 1 | Later levels replay; L1 still fails under the current generic path. |
| `rt9k` | 1 | Later levels replay; L1 still fails under the current generic path. |
| `tj4n` | 3 | L1 replays, L2 has no artifact, L3 witness currently fails. |
| `tk6n` | 2, 3 | Witness text present, but replay still fails on later levels. |
| `vd3g` | 1 | Later levels still lack artifacts; the L1 witness itself currently fails. |
| `wm6q` | 1 | Later levels still lack artifacts; the L1 witness itself currently fails. |
| `zd7m` | 1, 2, 3 | Witnesses parse, but replay still fails across all levels. |
| `zk9p` | 2, 3 | L1 recovered from prior artifacts; L2/L3 witness replay still fails. |

## Suggested Next Pass

- Add explicit witness sequences or other solved-oracle artifacts for `gg01` through `gg26`; the current pass found neither reusable recordings nor parseable `mechanism-detail.md` witnesses for any of their levels.
- Add game-specific replay handling for the remaining `mechanism_detail_witness_failed` set.
- Manually encode exact click / selection order for underspecified graph and routing games such as `jx5k`.
- Pull any additional solved artifacts from other branches or runs if they exist outside the current `JM` analysis outputs.
