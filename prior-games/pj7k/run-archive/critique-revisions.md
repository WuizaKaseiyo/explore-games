# critique-revisions — pj7k spec, pass 1

The spec violates several `design-constraints/checklist.md` items
and contains drafting iterations that must be cleaned up. Bounce
back to `write_spec` for a revision.

## Issues

### Issue 1 — Item 10a (strict necessity) FAILS for L3 walls.

- **Checklist item violated:** §3 item 10a "**Strict necessity.**
  Every mechanic introduced up to and including level L must be
  REQUIRED to solve L — i.e. removing it makes L unsolvable."
- **Offending spec section:** §4 Level 3, "Necessity per mechanic
  → *Walls strict necessity (revisited).* I admit defeat on
  proving strict necessity for walls in this layout in one
  closed-form argument."
- **Why this is a violation:** The spec itself concedes that the
  wall mechanic in L3 is not strictly necessary. Removing the
  walls at (0, 1) and (1, 1), the witness `[ACTION5, ACTION4,
  ACTION4, ACTION4, ACTION5, ACTION2]` still solves the level —
  the cube never visits (0, 1) or (1, 1) in this witness. Walls
  in this layout serve no role in the witness; they only restrict
  *alternative* solutions. Per item 10a, "Exercised by the witness
  is not enough" — the mechanic must be REQUIRED, and walls are
  not required to solve, only to disambiguate from other
  solutions.
- **Concrete fix:** Replace the L3 mechanic with one that is
  **constructively** necessary — i.e. the level is unsolvable
  without it, not just under-constrained without it. Two viable
  options:
  1. **Coloured locks** — sprites that act as walls *until* the
     cube rolls into them with bottom-face matching the lock's
     colour, at which point the lock opens and the cube enters
     (depositing paint as usual). This is constructive: the
     locked cell is impassable without the lock-mechanic, so
     removing locks makes the target behind the lock unreachable.
  2. **Multi-cube selection (ACTION6)** — L3 introduces a second
     cube and ACTION6 click toggles which cube is active. The
     witness must control both cubes to paint targets in
     opposite-corner positions. Removing ACTION6 leaves only one
     cube reachable; the other cube can never be moved →
     unsolvable.

  Recommendation: pick option (1). Locks are a clean topological
  mechanism that keeps the action space at `[1..5]` (no new
  ACTION6 to wire), aligns with the "gate" sprite design already
  drafted, and the necessity argument is one-step: "the target at
  cell C is blocked by a lock requiring colour X, the cube must
  arrive with bottom = X to enter, removing locks makes C
  reachable but reachable in fewer ways → reverse: with locks,
  the path constraints are constructive". Even simpler form: a
  lock that is a *wall except when bottom matches* is a
  constructive constraint — the cell is unreachable any other
  way.

  Re-spec L3 around locks. Suggested layout:
  - 4×4 board, cube at (0, 0).
  - Targets: (1, 0)=14, (2, 0)=11, (3, 0)=8 (a row; the same
    east-row layout as before).
  - **Lock** at (3, 0) requiring colour 8 — i.e. (3, 0) is
    impassable until the cube approaches with bo=8. Without the
    lock, (3, 0) is reachable by `[E, E, E]` painting bo=15
    there → mismatches target (3, 0)=8. With the lock, the cube
    cannot enter (3, 0) until bo=8. The only way to get bo=8 at
    a 3-east-roll position is to first take a longer route that
    cycles the faces; the fact that the *east-only* deposit at
    the third cell is 15 (not 8) means the cube must detour
    south-and-back-north, AND must twist somewhere to land 8 on
    R before the final east-roll.
  - Witness becomes longer (≥ 6 actions); rolling, twist, and
    lock-passage are all strictly necessary.

  Provide a complete trace in the revised spec showing every
  face state at every step, plus the strict-necessity argument
  for each of the three mechanics ("remove rolling → no paint;
  remove twist → can't put 8 on R; remove lock → shorter east-
  only solution exists that doesn't require twist").

### Issue 2 — §4 contains drafting iterations that must be removed.

- **Checklist item violated:** §3 item 4 ("EXACTLY 3 `Level(...)`
  entries") is technically satisfied, but the spec contains
  multiple "Wait — the witness as written above does not solve. Let
  me rewrite..." / "Resolution. I am going to pin..." / "Revised
  L3 layout (final)." / "Final-final L3 layout (third try)" / "Final
  L3 layout (fourth try)" / "Final-final-final" passages. The
  intended L3 is only the LAST of these, and downstream stages
  (`implement`) cannot be expected to find the right block.
- **Offending spec section:** §4 Level 3, several passages.
- **Concrete fix:** Strip every superseded layout and keep ONLY
  the chosen (revised, post-Issue-1) L3 layout, with one clean
  witness trace, one clean necessity argument per mechanic, and
  one clean difficulty justification block.

### Issue 3 — L2 (a) random-resistance numeric claim is too generous.

- **Checklist item violated:** Item 16 (a) random-resistance.
- **Offending spec section:** §4 Level 2 (a): "6-action witness
  over a 5-action space → `5⁶ ≈ 15,625` random sequences."
- **Why this is dubious:** Random play does not stop at the
  witness length; with a step budget of 80, a random agent has
  `5⁸⁰ ≈ 10⁵⁵` sequences, only some of which lose. The relevant
  claim is "P(win | random policy of 80 steps) ≤ 1/10,000",
  which is far harder than the spec's `5⁶` calculation suggests.
- **Concrete fix:** Reframe (a) for L2 as "the 6-action witness
  has cube-orientation × cell-position × paint-state coupling
  that random play within 80 steps fails to satisfy because (i)
  the cube must end at (3, 1) with target-cells (1, 0), (3, 0),
  (3, 1) having the right paint, AND (ii) the deposited colours
  are determined by face-state-at-cell-entry, which is a specific
  point in the 24-orientation × 16-cell state graph that random
  walks visit with probability « 1/10,000". Drop the `5⁶`
  arithmetic.

### Issue 4 — §3 sprite roster: paint sprites layer order needs explicit
specification.

- **Checklist item violated:** Item 2 (universal scaffold
  conformance) — the spec says "paint sprites layer below cube"
  but doesn't pin the exact `layer=` value, and the engine's
  default layer is 0; the cube also defaults to 0.
- **Offending spec section:** §3, "paint_<colour> ... NOT_BLOCKED.
  Layer below cube."
- **Concrete fix:** Specify explicitly: paint sprites have
  `layer=-1` (below default); target sprites have `layer=1`
  (above paint, so the target ring overlay reads through the
  paint colour); cube has `layer=2` (above target rings, so the
  cube body always reads on top); gate/lock sprites have
  `layer=1` (same as targets, mutually exclusive cells anyway).

### Issue 5 — Gate (now lock) sprite plus-pattern.

- **Checklist item violated:** Item 7 (no letters / digits / etc.).
  Borderline but defensible.
- **Offending spec section:** §3 `gate_<colour>` sprite uses a
  cross / plus pattern.
- **Why this might be a violation:** `forbidden-elements.md`
  carves out an explicit allowance: "a vertical bar with two
  horizontal cross-strokes forming a "+" is fine (it's a
  topological symbol, not a letter)." So the plus pattern is
  permitted. **Defer**: the plus pattern is allowed by the
  forbidden-elements doc verbatim. No revision needed on this
  axis. (Listed here so the next reviewer can confirm.)

### Issue 6 — L3 trivial-heuristic argument is a single example.

- **Checklist item violated:** Item 16 (c) L3 — "trivial
  heuristic that fails AND a witness-pair commute test".
- **Offending spec section:** §4 Level 3 (c). The named heuristic
  "always twist before every roll" is plausible; the trace
  showing it deposits 9 at (3, 0) (target wants 8) is correct.
  But the spec only checks ONE heuristic. The
  `difficulty-rules.md` § 2c L3 wording asks for "*which specific
  trivial heuristic L3 defeats*" — singular — so this is fine.
- **Concrete fix:** None — but in the revision, re-derive the
  trivial-heuristic and commute traces against the new (locks-
  based) L3 layout, since the current traces are against the
  walled L3 that's being scrapped.

## Summary

- 4 substantive issues (1, 2, 3, 4); 2 deferred or non-blocking
  (5, 6).
- Issue 1 (strict necessity of L3 mechanic) is the load-bearing
  failure — the L3 mechanic must change from "walls" to
  "coloured locks" (or another constructive mechanism).
- Issue 2 (drafting iterations) is a pure cleanup pass.
- Issues 3 and 4 are small numerics + specification gaps.

Re-enter `write_spec` and rewrite §4 Level 3 around the locks
mechanic. Reuse §1–§3 (with the layer fix from Issue 4) and L1/L2
(with Issue 3's wording cleanup) verbatim; only L3 § + §6/7/8/9
need the new mechanic worked through.
