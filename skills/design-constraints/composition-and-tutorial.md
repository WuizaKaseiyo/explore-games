# Composition, levels, and the tutorial

The 25 NovaPlay reference games each have ≥6 levels per §3.4 of the
report. Our generation pipeline OVERRIDES this rule: every generated
game has EXACTLY 3 levels. The other §3.4 structural rules still
apply.

## Multiple mechanics

Each environment must contain MORE than one mechanic. A single
mechanic that scales in size or grid count across levels is the
canonical anti-pattern.

Examples of multi-mechanic compositions:
- "Push blocks AND collect keys to unlock doors" (movement +
  inventory).
- "Move a player AND avoid an enemy that pursues" (agentness +
  movement).
- "Place pieces AND rotate them" (placement + transform).

## Exactly 3 levels (override of §3.4 ≥6)

Every generated environment has EXACTLY 3 `Level(...)` entries:

- **Level 1 — base dynamic system.** L1 establishes the *base
  dynamic system* — one or more interacting mechanics (a single
  verb is fine; a small system is also fine). Every mechanic L1
  declares must be exercised by the witness solution. Reduced
  state space (smaller grid, fewer obstacles). Communicates the
  core interaction pattern by being playable — never with
  on-screen text.
- **Level 2 — base system + one or two new mechanics.** Every
  mechanic from L1 is still active and still required by the
  witness; L2 adds **one or two** new mechanics on top. The L2
  witness must exercise every new mechanic AND every L1
  mechanic — there is no "basic-form" introduction; new
  mechanics carry real weight in the puzzle.
- **Level 3 — system + one or two more new mechanics.** Every
  mechanic from L2 (which itself already includes every L1
  mechanic) is still active and still required by the witness;
  L3 adds **one or two** further new mechanics on top. The L3
  witness must exercise **all** mechanics — every L1 mechanic,
  every L2-introduced mechanic, AND every L3-introduced
  mechanic. L3 is NOT a re-composition of just L1 and L2; it is
  the base system plus L2's additions plus L3's additions, all
  fired in concert.

For each level's **difficulty floor and ceiling** —
random-resistance, human-tractable time, planning depth, and
step budget — see `difficulty-rules.md`. That file is the
canonical home for the per-level *Difficulty justification* the
spec must contain.

Reusing the same `grid_size` and sprite set across the 3 levels is
fine, but each level's configuration (sprite positions, level data,
constraints) must vary.

## No hidden mechanics; one or two new mechanics per level

The level structure above is a **contract**, not a hint. Two hard rules:

1. **No hidden mechanics.** Every mechanic active in a level must be
   *required* to solve that level. A mechanic that exists in the
   engine but is never needed by the witness solution counts as
   hidden and is forbidden. The player must not be able to skip a
   mechanic the level claims to teach.
2. **One or two new mechanics per level promotion, and previous
   mechanics carry forward.** Per the L1/L2/L3 structure above:
   the per-level count of witness-required mechanics rises by
   1 or 2 across the three levels (no level promotion is
   allowed to introduce zero new mechanics, and no level
   promotion is allowed to introduce three or more), and every
   earlier-level mechanic remains active *and* required in
   every later level.

The spec must state, per level, which mechanics the witness
solution actually exercises. *How* a level enforces "no hidden
mechanics" is up to the agent — by puzzle configuration, by
gating, or by any other means.

## Difficulty through composition

L2 and L3 each increase difficulty by **composing every mechanic
introduced so far** — including the new one that level adds. Just
adding a new mechanic without making the prior ones interact with
it does not count as composition.

The composition rule is binary: a level is genuinely harder than
its predecessor if and only if its witness solution requires *every*
mechanic available at that level (the carried-forward ones plus the
newly-introduced one or two) interacting together; otherwise the
spec needs revision.

Composition handles the **planning** stage of difficulty (see
`difficulty-rules.md` § 1): more interacting mechanics means more
plausible-looking moves at each step, which means the player has
to think harder to pick the path that wins. Exploration difficulty
stays roughly constant across levels — see `difficulty-rules.md`
§ 1 for the two-stage model.

## Step budget

Step-budget rules — generous over the witness, never tight, never
shrinking across levels — live in `difficulty-rules.md` § d.
