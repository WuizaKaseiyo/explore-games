# Step #01: study (Run #2)

## Inputs Consumed

### Carried-over context (from same session, run #1):
- 25 ref taxonomy (full table) + cached patterns + design constraints + cross-cut frequencies
- 27 prior games (kf42 ... ej4t, including ej4t finalised in run #1)

### Re-confirmed for this run:
- skills/code/spec-template.md (now requires "Trivial heuristic action sequence" sub-bullet for L2/L3)
- skills/code/smoke-test-checks.md (now 11 universal checks incl. CHECK_TRIVIAL_FAILS)
- states/critique_spec.md (new common failure mode: "Trivial-heuristic missing or weak")
- skills/design-constraints/difficulty-rules.md (§ 2(c) requires action sequence + executable enforcement)

### Step 5 — fresh PuzzleScript demos (re-done):
| Demo | Mechanic family | Notes |
|---|---|---|
| midas | touch-transforms-walls (Crown turns wall→gold) | gravity + jump; partly physics |
| m c eschers armageddon | 4-actor independent directional-locked movement | rotation-tile-flip-actor-direction |
| color chained | match-3 falling blocks | real-time-ish; not NovaPlay fit |
| chaos wizard | spell-recipe combination (gem + prism amplifier + rival-AI) | complex but rich |
| threes | doubling-merge | famous commercial — §3.4 ceiling |
| plus_cloning | sprite copy-inheritance | not a mechanic, just syntax |

Plus prior session vocabulary (modality, sokobond demake, heroes_of_sokoban, atlas shrank, robotarm, wrappingrecipe, constellationz, byyourside, collapse, dropswap, diesinthelight, ponies-jumping-synchronously, zenpuzzlegarden, plus_nonogram, plus_localradius). Total 21 mechanic vocabulary entries available for pick_mechanic.

## Deliverables Produced

None (study is internalize-only).

## Notes

This run's pick_mechanic priorities (different from run #1):
1. **Genuine planning depth** — level layouts must offer multiple valid first actions; not single corridor.
2. **Family novelty** WRT 27 prior games (incl. ej4t = radius-scope-influence).
3. **§3.4 ceiling** — avoid clearly commercial-game clones (skip threes / sokobond direct).

Strong candidates from vocabulary:
- **class-swap-roster** (heroes_of_sokoban-inspired): N actors, each with a different interaction rule (push / pull / swap); ACTION5 cycles active actor; planning depth comes from which-actor-when decisions.
- **chained-segment-arm** (robotarm-inspired): hierarchical kinematics; rotation order matters.
- **companion-reflex-pair** (byyourside-inspired): autonomous companions follow per-reflex rule.

Picking **class-swap-roster** for run #2 — natural planning depth (4 directions × 3 classes = 12 effective actions per turn; trivial heuristic "always control class A, press right" should fail at L2/L3 because some elements only respond to other classes' verbs).
