# Critique revisions for `mechanic-spec.md` (visit #04 → write_spec)

Issues found while running `mechanic-spec.md` against
`design-constraints/checklist.md`. Each numbered item is a
revision trigger; address concretely in the next `write_spec`
pass.

## Issue 1 (item 12 — strict counterfactual necessity, L3 M4)

**Where**: `mechanic-spec.md` § 4 *Level 3*, mechanic M4
(*anchor-pin-blocks-rotation*) and per-mechanic counterfactual.

**Quote** (paraphrased): "M4: L3 cannot be solved without
triggering M4 because the naive 2-CW path around (32, 32)
is rejected on CW1, forcing CCW."

**Problem**: Per checklist item 12, the strict-counterfactual
gate asks *"Is there any way to win L within the step budget
without ever triggering M's distinguishing behavior?"* The named
witness `[ACTION6@(4, 4), ACTION6@(32, 32), ACTION5, ACTION5]`
follows the CCW path from start; it never lands a rotatable
sprite on the anchor_pin cell (52, 32) at any intermediate
step, so M4's distinguishing behavior (rotation-rejection on
anchor_pin landing) is **not observably exercised**. The spec
relies on M4's *constraint role* (it shapes which alternate
paths win) rather than its *active role* in the witness — a
weaker reading of checklist 12 than the strict one in the
verbatim text.

**Fix direction**: Redesign M4 from a *negative blocker*
(reject-on-collide) to a *positive checkpoint* (visit-required):

- **M4 redefined**: `anchor_pin` cells are non-rotatable
  fixtures that stay put. The level's win predicate adds a
  clause: every `anchor_pin` cell MUST have been coincident
  with at least one `rotatable` sprite's top-left at some
  action's end-state during the level. The game tracks
  `_visited_pins: set[tuple[int, int]]`; each `step()` end,
  for each rotatable sprite, if its top-left == any
  anchor_pin's top-left, add the pin's cell to `_visited_pins`.
- **L3 layout updated**:
  - avatar at (32, 12), avatar_target at (32, 52).
  - companion at (8, 32), companion_target at (56, 32).
  - anchor_pin at **(12, 32)** (NOT (52, 32) — moved so it
    lies on the CCW1 path of the avatar but NOT on the CW
    path).
  - direction_indicator at (4, 4).
  - step_budget 12 (generous over 4-action witness).
- **Witness**: `[ACTION6@(4, 4), ACTION6@(32, 32), ACTION5,
  ACTION5]` — 4 actions.
  - Trace step-by-step:
    - CCW1: avatar (32, 12) → CCW(32, 32) = (32 − 32 + 12,
      32 + 32 − 32) = (12, 32) **= anchor_pin → visits ✓**;
      `_visited_pins = {(12, 32)}`. companion (8, 32) →
      (32 − 32 + 32, 32 + 32 − 8) = (32, 56).
    - CCW2: avatar (12, 32) → (32 − 32 + 32, 32 + 32 − 12) =
      (32, 52) ✓ avatar_target. companion (32, 56) →
      (32 − 32 + 56, 32 + 32 − 32) = (56, 32) ✓
      companion_target. WIN.
- **CW alternative now fails**: 2 CWs around (32, 32). avatar
  (32, 12) → (52, 32) → (32, 52) ✓; companion (8, 32) →
  (32, 8) → (56, 32) ✓. Both pawns at targets BUT avatar
  never visits (12, 32) — `_visited_pins` is empty. Win
  predicate's M4-clause fails → level does not advance.
  Player must use CCW (M5) to visit (12, 32). Adding more CW
  rotations after step 2 moves pawns OFF targets, requiring
  yet more rotations to recover. Within step budget 12, the
  shortest CW-only resolution requires at least 4 CWs around
  (32, 32) plus one toggle to CCW plus 1 more CCW = 6+ actions
  AND still ends up needing CCW for visit (since CW only
  visits (52, 32), (32, 52), (12, 32) on the 4th CW which is
  past target reset). In effect, M5 is required and M4
  (visit-clause) is now **observably triggered by every
  winning sequence**.
- **Counterfactual table updated**:
  - M4 (L3) — solvable without triggering M4? **No**. Every
    winning sequence must put a rotatable sprite on (12, 32);
    CW paths never touch (12, 32) within budget; CCW1 around
    (32, 32) is the unique short way; the witness's CCW1
    step is the trigger.
  - M5 (L3) — solvable without triggering M5? **No**. CCW is
    only available after toggling direction; the unique
    short visit-(12, 32) path uses CCW.

**Sprite roster update**: anchor_pin's role-line is now
"L3 visit-checkpoint that must be touched by avatar/companion
at some moment during the level". Tags: `["anchor_pin",
"visit_checkpoint"]`. Drop the `["blocker"]` tag — anchor_pin
no longer blocks rotations, just gates win.

**Discoverability cue update**: when a rotatable sprite first
visits an anchor_pin cell, the anchor_pin's centre 2×2 pixel
flips from palette 14 (green) to palette 11 (yellow) and stays
flipped — the player gets a persistent "checkpoint stamped"
visual that contributes to the no-hidden-state rule. (Per
`reference-game-patterns.md` § *Discoverability*: any state
the player must reason about needs a persistent visible cue.)

## Issue 2 (item 18 — random-resistance phrasing for L2)

**Where**: `mechanic-spec.md` § 4 *Level 2* difficulty
justification (a) random-resistance.

**Quote**: "total P(win | random) ≈ 30/32768 ≈ 1/1092 …
random agent has ~0.5% chance of stumbling, well below 'easy'."

**Problem**: 1/1092 is above the report's strict 1/10 000
graph-based gate (`from-tech-report.md` § 7). The harness's
`difficulty-rules.md` § 2.a uses the softer "near-zero"
framing, but the spec's own number (1/1092) is high enough
that an honest reviewer might flag L2 as random-stumble-
solvable.

**Fix direction**: Two options — either raise the bar or own
the framing more carefully.

- **Option A (preferred)**: change L2's avatar/companion
  starting positions so the only winning pivot is *not* the
  arena centre. Specifically: place avatar at (8, 16),
  avatar_target at (48, 8); companion at (32, 8),
  companion_target at (56, 32) (or another asymmetric
  layout). The unique winning pivot becomes a non-obvious
  cell (e.g. (28, 28) — solve via formula). Random's
  4096-cell click + ACTION5 sequencing now drops below
  1/10 000 within the budget. *Trade-off*: requires
  re-deriving every witness arithmetic for L2 from scratch.
- **Option B**: keep the current layout, but tighten the
  random-resistance prose to acknowledge "the harness uses
  a soft 'near-zero' threshold from `difficulty-rules.md` §
  2.a rather than the report's 1/10 000 graph-gate; under
  the soft threshold a 0.5% random-policy success is
  acceptable for L2 because the gameplay still requires
  pivot-coordinate discovery in two-action coordination,
  not spam".

**Recommendation**: Option B — keep the centred-symmetry
layout (the visual symmetry is part of L2's pedagogical
appeal — the player sees "two pawns at orthogonal axes,
two targets at orthogonal axes; the centre pivot is the
visual midpoint") and just sharpen the prose. Option A
would buy a stronger random-bar but at the cost of
making L2's optimal pivot unintuitive (a 28-ish offset
from corner) and breaking L2's role as the "easy
introduction to multi-pawn rotation".

## Issue 3 (item 21 — discoverability of direction_indicator at L3)

**Where**: `mechanic-spec.md` § 3 sprite roster, § 4 L3
difficulty (b) human-tractable.

**Problem**: The spec describes the direction_indicator as
"a 4×4 widget at (4, 4)" with corner-pip variants for CW vs
CCW. There's no explanation of how a first-time player who
sees the L3 frame *learns* the widget toggles direction. A
small, unfamiliar 4×4 sprite at the corner may read as
decoration, not as an interactive control.

**Fix direction**: The L3 difficulty justification (b) should
spell out the player's discovery pathway:

1. Player tries the L2-style 2-CW around centre. Sees both
   pawns end at the wrong targets (companion at avatar's
   target colour, vice versa) — the rotation directions
   are wrong.
2. Player notices the direction_indicator's pip-corner is
   at top-right, and the only object on the playfield they
   haven't interacted with is this 4×4 widget. Click it
   experimentally.
3. The pip-corner flips to top-left, signalling state
   change. Now ACTION5 rotates CCW.
4. Re-attempt the 2-rotation pattern.

This narrative needs to be in the spec's § 4 L3 (b) bullet,
not implicit. Without it the spec assumes the player will
guess the widget's role unprompted.

## Issue 4 (item 21 — sprite UI ≈ sprite role for the avatar/companion vs targets)

**Where**: `mechanic-spec.md` § 3 sprite roster.

**Problem**: avatar and avatar_target are both 6×6 with
*similar* outer-ring shape and *same* dominant palette (9
blue). The colour-match is the role-correlation cue (per
checklist 21 *Identical visuals imply shared or correlated
roles*) — that's good. But: a first-time L1 viewer sees
TWO 6×6 blue shapes; they need to immediately read "this is
the pawn I move; this is the slot that wants the pawn".
The internal-pattern distinction (pawn = filled tri-quadrant;
target = hollow ring) is the disambiguating cue, but the
spec hasn't specified the internal pattern in enough detail
to verify it reads cleanly.

**Fix direction**: § 3 sprite roster should specify exact
6×6 pixel matrices for avatar and avatar_target so the
critique reviewer (and later, `implement`) can verify the
visual difference at a glance. Concrete suggestion:

- avatar 6×6 (filled tri-quadrant, no transparent cells):
  ```
  [4, 9, 9, 9, 9, 4]
  [9, 0, 9, 9, 0, 9]
  [9, 9, 9, 9, 9, 9]
  [9, 9, 9, 9, 9, 9]
  [9, 0, 9, 9, 0, 9]
  [4, 9, 9, 9, 9, 4]
  ```
  (Solid blue body with corner-frame and two interior white
  pips; rotation-aware — rotated 90° gives a visibly distinct
  pattern.)
- avatar_target 6×6 (hollow ring; transparent centre):
  ```
  [4, 9, 9, 9, 9, 4]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [4, 9, 9, 9, 9, 4]
  ```
  (Hollow centre 4×4 transparent so the avatar shows through
  cleanly when overlaid; same outer frame so the colour-match
  is unambiguous.)

Same pattern for companion (palette 12 instead of 9) and
companion_target.

Add these explicit pixel matrices to the spec § 3.

## Summary

Three concrete revisions for the next `write_spec` pass:

1. **L3 mechanic M4 redesign**: anchor-pin = visit-checkpoint
   (positive); update sprite roster, § 4 L3 mechanics +
   counterfactual + witness, § 7 win predicate (add
   visited-clause), § 6 internal state (add `_visited_pins`).
2. **L2 random-resistance prose**: own the soft "near-zero"
   framing more carefully (Option B above); no layout change.
3. **Sprite roster pixel matrices**: spell out exact 6×6
   matrices for avatar / avatar_target / companion /
   companion_target so the critique reviewer can verify the
   "filled vs hollow" distinction and rotation-asymmetry by
   reading the spec.

Issue 1 is the load-bearing one — it's the only checklist
*hard fail*. Issues 2 and 3 (4 included) are quality polish
that strengthens the spec but not strict gates.
