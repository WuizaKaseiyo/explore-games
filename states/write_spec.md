# write_spec

## Description
Expand the `mechanic-pick.md` paragraph into a full game spec
following `code/spec-template.md`'s 9 subsections. Cover sprite
roster, level progression (EXACTLY 3 levels per
`design-constraints/composition-and-tutorial.md`), action
mapping, HUD/state, win/lose conditions, and a novelty note that
re-grounds against `mechanic-novelty/`.

If you are RE-ENTERING this state because `critique_spec` flagged
issues, read the latest `critique-revisions.md` first, address each
issue concretely, and rewrite the spec.

Aesthetics are a soft goal but a real one: aim for sprites,
palette, and layout that feel considered and pleasing rather than
placeholder — this is not checked in `critique_spec`'s revision
loop, but the resulting game is meant to be looked at.

**Animation for non-local effects.** If your mechanic produces
non-local effects in a single tick — long-distance transitions
(teleport, slide-until-wall, projectile), chain reactions, or
multi-entity propagation — the spec must include an animation
plan (frame-by-frame breakdown, or "X cells per tick over N
ticks"). A single-frame snap from source to destination hides
the cause-effect link and leaves the player guessing. This is
checklist item 24 and is checked at critique time; not optional
when the mechanic fits the shape. See
`skills/conventions/reference-game-patterns.md` § *Discoverability
through observable change* for the pattern and examples (cd82,
sp80, m0r0, tu93, sb26, r11l).

## Skills
- skills/global
- skills/design-constraints
- skills/code
- skills/mechanic-novelty
- skills/mechanism-details *(quick-reference; the deeper
  evidence is at
  `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`)*

## Next States

### critique_spec
**Condition:** All 9 subsections of `code/spec-template.md` are
present; §4 enumerates per-level mechanics (L1 = N ≥ 1, L2 =
N+1 or N+2, L3 = L2-count + 1 or + 2, all witness-required)
AND a written-out shortest witness solution per level AND a
difficulty justification per level (random-resistance, human
time, planning depth); the action mapping is concrete; the
win/lose conditions are testable predicates.
**Deliverables:**
- mechanic-spec.md: The full 9-section spec. If revising after a
  critique, mark which sections changed and quote the
  `critique-revisions.md` issue each change addresses.
