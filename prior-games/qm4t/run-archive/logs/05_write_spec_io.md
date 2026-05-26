# Step #05: write_spec (revision pass v2)

## Inputs Consumed
- `critique-revisions.md` (#04)
- `mechanic-spec.md` v1 (to revise)
- All design-constraints + code skill files (re-read where issue-relevant).

## Deliverables Produced
- `mechanic-spec.md` v2: revised spec addressing all 4 issues:
  - Issue 1 (L2 trivial fallback): bumped maroon count to 4 at corner
    positions, recomputed witness, restated necessity.
  - Issue 2 (L3 patroller necessity): bumped to 3 synced patrollers with
    independent cycles all transitioning between centre/corner phases
    together; recomputed witness and necessity.
  - Issue 3 (strike_marker glyph): redesigned as 3×3 filled red square.
  - Issue 4 (vertex_post glyph): simplified to 3-tall vertical magenta bar.
  - Spec-quality: critter and patroller now have visually-distinct shapes
    (rounded blob vs tapered diamond).
  - Inserted explicit ray-casting geometric verification of the L3 witness's
    pen vs all 5 required, 2 maroons, 3 patrollers.

## Notes
- The cycle definition for L3 patrollers needed care to ensure all 3
  are simultaneously inside (phases 0..3) and outside (phases 4..7).
  Solution: 3 separate parallel cycles indexed by a single global phase
  counter.
- The witness pen at L3 is a quadrilateral, not a triangle, because the
  4-post placement is also what advances the action-count to phase 4
  (the safe commit phase). Composes M1+M3+M4 cleanly.
- Step budgets unchanged: L1=30, L2=50, L3=80.
