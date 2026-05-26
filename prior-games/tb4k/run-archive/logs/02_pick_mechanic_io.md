# Step #02: pick_mechanic

## Inputs Consumed
- prior-games/index.md (from harness root): cumulative novelty source of truth (78 prior games).
- skills/mechanic-novelty/taxonomy-of-25-games.md (already read in #01).
- skills/mechanic-novelty/similarity-check.md (positive test).
- skills/mechanic-novelty/negative-similarity-check.md (negative test).
- skills/code/id-generation.md (4-char ID rules).
- prior-games/hb5n/mechanism-detail.md (closest neighbour: polyomino growth).
- prior-games/hb5n/run-archive/smoke-frames/level_1.png (visual check).
- prior-games/pj7k/run-archive/smoke-frames/level_1.png (visual check).

## Deliverables Produced
- mechanic-pick.md: tb4k, mechanic-family `tumble-block-stand-fall`, distinguishing rules against hb5n, pj7k, zw91, nz3v, kj82, lt7m, ka59.

## Notes
- Autonomous mode (no seed). Chose Bloxorz-style tumbling-brick mechanic because no prior covers state-dependent footprint changes induced by movement direction (rather than by a separate verb / pickup absorption).
- Positive similarity check: passes. Closest reference is ka59 (sliding block in arena) but ka59's block is fixed-footprint translate-only.
- Negative similarity check: passes. Shares "arrow input" surface dim with several priors but the core dynamic (footprint geometry over holes + narrow bridges) is uniquely mine.
- Hard-death path identified (falling in holes) — checklist item 25 mandates a lives mechanism; will surface in spec §4.
