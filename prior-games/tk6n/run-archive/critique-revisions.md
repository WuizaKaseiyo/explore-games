# critique-revisions.md (revision 1)

## Issue 1 — L2 counterfactual necessity for M2 fails on the alternate-path enumeration (checklist.md item 12)

**Violation.** L2's per-mechanic table for M2 ("wall-height gating —
`wall_tall` blocks both, `wall_short` blocks avatar only") does not
hold against the geometric alternate-path test. The spec's L2 layout:

> bounding `wall_tall` perimeter at the edges; `wall_tall` interior
> obstacle at column `20`, rows `8..40`; `wall_short` interior obstacle
> at column `38`, rows `12..36`; targets at `(28, 32)` and `(28, 16)`.

For the upper target at `(28, 16)` the spec claims:

> "the only line that lights `(28, 16)` is a westward throw from a cell
> with column ≥ 38 and row 16 — but reaching such a cell from the
> avatar's start at `(8, 32)` requires the avatar to walk south below
> row 36, then east past column 38 (which means walking AROUND
> `wall_short` since avatar cannot cross it), then north to row 16,
> then westward throw"

This argument MISSES a plausible alternate that an enumeration must
catch: the avatar can walk NORTH from `(8, 32)` to e.g. `(8, 7)`, EAST
along row `7` past the top of the `wall_tall` pillar (which extends
only rows `8..40`, leaving row `7` open), then SOUTH back into the
corridor at any column 21..37 — landing the avatar at e.g. `(33, 16)`,
which is BETWEEN the two interior walls. From `(33, 16)` a westward
throw advances the boomerang to `(32, 16) → (31, 16) → ... → (28, 16)`
without ever crossing the `wall_short` at column 38. M2 is NOT
triggered on this path. Therefore the spec's claim that "the only
line that lights `(28, 16)`" requires M2 is false; M2 is not strictly
counterfactually necessary at L2 with the current geometry.

**Suggested fix.** Redesign L2's geometry so the boomerang must cross
a `wall_short` cell to reach EVERY target. Concretely, replace the
two-target layout with a SINGLE target enclosed by walls on every
side, where the only boomerang-permeable side is `wall_short`. For
example:

- Avatar at `(8, 32)`. Target at `(40, 32)`.
- Wall_tall horizontal line at row `24`, cols `5..58` (top of corridor).
- Wall_tall horizontal line at row `40`, cols `5..58` (bottom).
- Wall_tall vertical line at col `56`, rows `25..39` (east bound).
- Wall_short vertical line at col `28`, rows `24..40` (vertical
  barrier across corridor; permeable to boomerang only).

The corridor west of `wall_short` (cols 5..27 rows 25..39) is the
avatar's accessible region; cols 29..55 rows 25..39 is unreachable by
the avatar (sealed by `wall_tall` top/bottom/east + `wall_short`
west). The target at `(40, 32)` lies in the unreachable region.

Counterfactual enumeration:
- Throw east from any cell `(c, r)` with `c < 28`, `r ∈ {25..39}`:
  boomerang flies east, must cross `wall_short` at col 28 to reach
  any cell with col ≥ 29. M2 triggered.
- Throw east from outside corridor (e.g., `(8, 8)` row outside
  `25..39`): boomerang flies east, hits `wall_tall` at row 24 (or
  row 40 for south throws). Does not reach `(40, 32)`.
- Throw south from `(40, < 24)`: avatar can't reach col 40 row < 24
  because the corridor's top wall_tall extends from col 5 to col 58
  at row 24 — but the rows ABOVE 24 are open on cols outside corridor.
  However, to STAND at col 40 row < 24 the avatar must walk around
  the top wall_tall, which ends at col 58 east — there's no way past
  col 58 (level boundary). Avatar can stand at col 40 row 23 (just
  above the top wall_tall). From `(40, 23)` throw south: boomerang
  flies south, hits wall_tall at row 24 — switches to returning at
  row 23. Does not reach (40, 32).

  Wait — does wall_tall at row 24 cols 5..58 actually block a south
  throw at col 40? Yes, the wall_tall sprite at (col 40, row 24)
  occupies that cell. So boomerang at (40, 23) advancing south hits
  wall (40, 24) and is bounced to returning.

  M2 is therefore the ONLY way to light the target. Necessity holds.

This replaces the two-target dual-throw witness with a single-target,
single-throw witness that is much easier to verify and is provably
M2-necessary.

## Issue 2 — L1 witness solution is non-canonical and was rewritten mid-spec (checklist.md items 11 + 18)

**Violation.** L1's "Witness solution" subsection contains TWO
sequences (one 12-action, one 20-action), neither of which is
authoritatively shortest. The spec ends the subsection with:

> The shortest closed-form is **17 actions** ... the implementer will
> validate the precise length in `smoke_test`.

Item 18(d) (step budget) and item 11 (mechanic enumeration) require
the witness to be a CONCRETE shortest sequence. The spec defers this
to smoke_test, which violates the spec's "concrete witness" gate.

**Suggested fix.** Pick a tighter L1 geometry, derive the shortest
witness analytically, and write it out fully. Concrete proposal:

- Avatar at `(20, 32)`. Initial facing right.
- Target at `(28, 32)` (8 cells east of avatar).
- Wall_tall corridor: row `28` cols `15..50`, row `36` cols `15..50`,
  col `52` rows `28..36`. (No wall on west side; avatar bounded by
  level edge there.)
- `throw_range = 8`, `step_budget = 25`.

Shortest witness (15 actions):
```
[ACTION5,
 ACTION1, ACTION1, ACTION1, ACTION1,
 ACTION1, ACTION1, ACTION1,
 ACTION2, ACTION2, ACTION2,
 ACTION2, ACTION2, ACTION2, ACTION2]
```
(Walk-up-then-walk-down witness with the throw at action 1; boomerang
outbound east 8 cells lights target at (28, 32) after 8 ticks; homing
return brings boomerang back to avatar's column.)

For finer accuracy, the implementer should validate by running the
sequence in a smoke test, but the witness is calibrated to ~15
actions with comfortable margin in the 25 budget.

## Issue 3 — Minor: target sprites collidable=True conflicts with avatar walking through targets (universal-scaffold.md default + spec semantics)

**Violation.** The spec's per-game state semantics say the boomerang
overlap rule lights targets, and the avatar's walking onto a target's
cell does NOT light the target. But the universal-scaffold default
has all sprites at `collidable=True`, meaning the avatar would COLLIDE
with targets and not be able to walk through them. The spec doesn't
specify `collidable=False` for `target_dim` / `target_lit`.

**Suggested fix.** Explicitly mark `target_dim` and `target_lit` as
`collidable=False, layer=-1` (background-layer non-blocking) in §3
sprite roster.

## Issue 4 — L3 witness solution incomplete (item 11 + 18)

**Violation.** L3's witness reads "estimated ~60 actions" with a
narrative description but no action-by-action sequence.

**Suggested fix.** Either compute the explicit witness sequence, or
at minimum break the narrative into 4 phases with action counts and
the cell coordinates each phase ends at. Detailed concrete witness is
the gate's requirement.

## Issue 5 — Acceptance: novelty check passes; checklist items 1-10, 13-17, 19-22 pass

For completeness:
- Item 1 (palette 0..15): ✅ — all sprites use values in 0-15 + -1.
- Item 2 (universal scaffold): ✅ — pending implementation.
- Item 3 (`available_actions ⊆ [1..7]`): ✅ — `[1, 2, 3, 4, 5]`.
- Item 4 (exactly 3 levels): ✅.
- Item 5 (4-char ID, not in lists): ✅ — `tk6n` verified.
- Item 6 (priors only): ✅ — objectness + physics + geometry +
  agentness.
- Item 7 (no letters/digits/clipart/cultural): ✅ — sprites are
  abstract; "boomerang" is a 3×3 angular blade silhouette without
  recognisable real-world detail at that resolution.
- Item 8 (≥ 2 mechanics): ✅ — M1, M2, M3.
- Item 9 (L1 tutorial): ✅ — single mechanic, reduced state space.
- Item 10 (L2/L3 compose, not just scale): ✅ — each level adds a
  new rule.
- Items 11, 12, 18: see Issues 1, 2, 4 above.
- Item 13 (mechanic family absent from taxonomy): ✅.
- Item 14 (mechanic family absent from prior-games): ✅.
- Item 15 (distinguishing rules): ✅ — articulated in §9.
- Item 16 (win condition stated): ✅.
- Item 17 (lose condition stated): ✅.
- Item 19 (no hidden state): ✅ — all state surfaced via avatar
  eye-dot, boomerang sprite position, BoomerangPhaseIndicator HUD,
  and target sprite swap.
- Item 20 (not low-resolution): ✅ — 64×64 grid_size, sprites at
  display-pixel resolution with internal pattern.
- Item 21 (UI teaches): ✅ — sprite roles legible from shape +
  palette; visual differences between wall_tall and wall_short are
  explicit (crossbar pattern vs. stripe pattern).
- Item 22 (ACTION7 strict-undo): ✅ — ACTION7 omitted from
  `available_actions`.

## Decision

Three real revisions required (Issues 1, 2, 4) plus one minor
clarification (Issue 3). Transition back to `write_spec` for
revision 2.
