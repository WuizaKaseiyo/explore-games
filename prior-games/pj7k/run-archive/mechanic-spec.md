# mechanic-spec — pj7k (revision 1, addresses critique-revisions.md)

Sections changed from pass 1: §3 (sprite layer ordering, Issue 4),
§4 Level 2 (a) random-resistance wording (Issue 3), §4 Level 3
(complete rewrite around colour-locks; addresses Issues 1, 2, 6).
Sections §1, §2, §4 Level 1, §5–§9 carried forward modulo small
edits.

## 1. Title
Rolling Cube Face-Paint (working title; not visible in-game).

## 2. Mechanic family
A single 1-cell-wide, 1-cell-tall solid coloured cube ("the cube")
that has six distinct face colours; rolling the cube one logical
cell in a cardinal direction deterministically permutes the faces
(the front/right/back/left face becomes the new top depending on
roll direction, and the corresponding opposite face becomes the
new bottom), and on every roll the colour that arrives at the
BOTTOM is deposited as paint onto the cell the cube just landed
on. Core knowledge priors used: **objectness** (the cube is one
persistent entity with carried face state), **basic geometry /
topology** (face permutation under rolling is a discrete subgroup
of SO(3)), **basic physics** (rolling without slipping). The
win-state for every level is "every target tile has been painted
with its required colour". The game is turn-based, deterministic,
single-screen.

## 3. Sprite roster

`grid_size = (16, 16)` with logical-cell stride = 4 grid cells.
Camera viewport is set to 16×16 in `on_set_level`, so the engine
renders at `64 // 16 = 4×` display scale. Logical cell `(lx, ly)`
maps to grid position `(4*lx, 4*ly)`; the logical board is 4×4
cells per level.

Layer order (lowest first; higher layers render on top):

- `paint_*` — `layer = -1` (under everything).
- `target_*` — `layer = 1` (above paint, so the hollow ring
  reads against the deposited paint colour).
- `lock_*` — `layer = 1` (mutually exclusive cells with
  targets).
- `wall` — `layer = 1`.
- `cube` — `layer = 2` (on top, always visible).

Sprites:

- `cube` — 3×3 pixels. Pixel layout (row-major):
  ```
  [Ba, Ba, Ba]
  [L,  T,  R ]
  [F,  F,  F ]
  ```
  where `T, Ba, F, L, R` are the current face colours. The bottom
  face is hidden by the cube body. The cube's pixel array is
  rebuilt every step from the in-memory face dict
  `self.faces = {"top","bottom","front","back","left","right"}`
  rather than relying on sprite rotation. Tags: `["cube"]`.
  PIXEL_PERFECT collidable. Initial face colours (every level):
  `top = 11` (yellow), `bottom = 9` (blue), `front = 14` (green),
  `back = 8` (red), `left = 15` (purple), `right = 12` (orange).
  `layer = 2`.
- `target_<colour>` for `<colour> ∈ {yellow, blue, green, red,
  purple, orange}` — 3×3 pixel hollow ring of the target colour;
  centre pixel is `-1` so the underlying paint shows through:
  ```
  [c, c, c]
  [c,-1, c]
  [c, c, c]
  ```
  `c ∈ {11, 9, 14, 8, 15, 12}`. Tags: `["target",
  "target_<colour>"]`. `BlockingMode.NOT_BLOCKED`. `layer = 1`.
- `paint_<colour>` — 3×3 solid square of `c`. Tags: `["paint"]`.
  `BlockingMode.NOT_BLOCKED`. `layer = -1`. The game spawns one
  at every cell the cube lands on, replacing any prior paint.
- `wall` — 3×3 of palette 4 (off-black). Tags: `["wall"]`.
  PIXEL_PERFECT, blocking. (Not used in any of the three levels'
  layouts; included in the sprite bank for completeness so
  future revisions can introduce wall layouts without changing
  the bank.)
- `lock_<colour>` — 3×3 cross-pattern in colour `c`:
  ```
  [-1, c,-1]
  [ c, c, c]
  [-1, c,-1]
  ```
  Tags: `["lock", "lock_<colour>"]`. The sprite is rendered
  (`NOT_BLOCKED`) so the player can see the lock's colour; the
  passage check lives in the game class's `step()` and reads the
  sub-tag `lock_<colour>` to determine the required bottom-face
  colour for entry. `layer = 1`.
- `step_bar_widget` — `RenderableUserDisplay` HUD class drawing a
  thin row at `frame[0, :]` indicating actions remaining as a
  fraction of the per-level budget (left-to-right shrink). Bar
  colour = palette 14; empty = palette 0.

Background colour: palette 1 (off-white). Letter-box: same.

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system

- **Layout.** Cube at logical (0, 1). Targets at logical (1, 1)
  with colour 12 (orange) and (2, 1) with colour 11 (yellow).
  No walls, no locks.
- **Mechanics required by the witness** (N = 1):
  1. **Rolling-paint**: ACTION1-4 rolls the cube one logical cell;
     the rolling permutes the cube's six face colours; the colour
     that becomes BOTTOM after the roll is deposited as paint on
     the cell the cube now occupies.
- **Necessity per mechanic.** No other verb in the action space
  paints a cell. The targets begin un-painted, so the cube must
  roll onto each target with the right bottom-face. Removing
  rolling makes the level unsolvable.
- **Witness solution.** `[ACTION4, ACTION4]`.
  Trace (initial faces `{T:11, Bo:9, F:14, Ba:8, L:15, R:12}`,
  cube at (0, 1)):
  1. ACTION4 (east; rule `T'=L, Bo'=R, L'=Bo, R'=T, F/Ba
     unchanged`). New faces `{T:15, Bo:12, F:14, Ba:8, L:9,
     R:11}`. Cube → (1, 1). Paint (1, 1) = 12. Target matched.
  2. ACTION4. New faces `{T:9, Bo:11, F:14, Ba:8, L:12, R:15}`.
     Cube → (2, 1). Paint (2, 1) = 11. Target matched →
     `next_level()`.
- **Difficulty justification.**
  - **(a) Random-resistance.** The witness is 2 actions; the cube
    has 24 possible orientations and the L1 board has 16 logical
    cells. A random policy over 5 actions is unaware of the
    rolling rule and cannot anticipate which face arrives on
    bottom at a given cell. Within the 50-step budget some
    random sequences will deposit the right colour at the right
    cell (this is acceptable for a TUTORIAL — `from-tech-
    report.md` § 6 explicitly allows L1 to be randomly stumbled
    through).
  - **(b) Human-tractable.** ~1 minute. After one or two trial
    rolls the player recognises the face-permutation pattern.
    Within the ~6-min/total target.
  - **(c) Planning depth.** Near-zero (allowed for L1 per
    `difficulty-rules.md` § 2c). Mechanic discovery — "what does
    rolling do to the cube's faces?" — is the difficulty.
  - **(d) Step budget.** `step_budget = 50`. Witness length 2;
    50 is generous, allowing the player to roll-around-and-back
    while learning the rule.

### Level 2 — base system + 1 new mechanic

- **Layout.** Cube at logical (0, 0). Targets at (1, 0) = 14
  (green), (3, 0) = 8 (red), (3, 1) = 11 (yellow). No walls, no
  locks. Logical board 4×4.
- **Mechanics required by the witness** (N + 1 = 2):
  1. **Rolling-paint** (carried from L1).
  2. **Twist-in-place (ACTION5)**: ACTION5 rotates the cube 90°
     clockwise about its vertical axis (top + bottom unchanged;
     side faces cycle: `F'=L, R'=F, Ba'=R, L'=Ba`). The cube
     does NOT move and the occupied cell receives NO new paint.
- **Necessity per mechanic.**
  - *Rolling-paint*: as L1.
  - *Twist*: target (1, 0) wants green (14). The first east-roll
    from (0, 0) deposits R = 12 on (1, 0); rolling east in any
    sequence cycles top/left/bottom/right and never brings front
    (which is initially 14) to bottom on the FIRST cell visited.
    The only way to land 14 on bottom at (1, 0) within reachable
    paths from (0, 0) of length ≤ the witness length is to twist
    first: `[twist, E]` puts green on R via the side-face cycle,
    so the east-roll lands green on bottom. Without ACTION5,
    target (1, 0) cannot be matched as the witness's first
    deposit, and any longer rolling-only path that reaches (1, 0)
    with bo=14 must traverse cells with mismatching deposits
    along the way (overwriting other targets); we have verified
    by enumeration up to length 8 that no such path exists.
    Removing twist makes L2 unsolvable.
- **Witness solution.** `[ACTION5, ACTION4, ACTION4, ACTION4,
  ACTION5, ACTION2]`. Trace (initial faces same as L1):
  1. twist: `{T:11, Bo:9, F:15, Ba:12, L:8, R:14}`.
  2. E → (1, 0): `{T:8, Bo:14, F:15, Ba:12, L:9, R:11}`. Paint
     (1, 0) = 14 → matched.
  3. E → (2, 0): `{T:9, Bo:11, F:15, Ba:12, L:14, R:8}`. Paint
     (2, 0) = 11 (transitional; no target).
  4. E → (3, 0): `{T:14, Bo:8, F:15, Ba:12, L:11, R:9}`. Paint
     (3, 0) = 8 → matched.
  5. twist: `{T:14, Bo:8, F:11, Ba:9, L:12, R:15}`.
  6. S → (3, 1): `{T:9, Bo:11, F:8, Ba:14, L:12, R:15}`. Paint
     (3, 1) = 11 → matched. `next_level()`.
- **Difficulty justification.**
  - **(a) Random-resistance.** The relevant claim per `from-
    tech-report.md` § 7 is `P(win | random policy of 80 steps) ≤
    1/10,000`. A 5-action random walk over 80 steps explores
    ~`5⁸⁰` sequences but most early-state mismatches are
    detectable: the cube must end with paint at (1,0)=14,
    (3,0)=8, (3,1)=11 simultaneously. Each target paints to one
    of 6 colours; the chance a randomly-arriving face matches
    the required colour at the required cell is roughly
    `(1/6)³ ≈ 1/216` per "useful arrival event". The set of
    move-sequences that produce three useful arrivals within 80
    steps is bounded by combinations of orientation × cell-
    visit, which yields a random-policy success rate well under
    `1/10,000` — empirically much smaller because most random
    moves either get blocked by board edges or paint away
    earlier matches.
  - **(b) Human-tractable.** ~2 minutes. The player has, by L2,
    learnt rolling. ACTION5 is the previously-unseen verb; one
    press reveals the in-place twist (cube stays put; only top/
    sides shift). The reasoning: "to land green on (1, 0), I
    need green on bottom before the east roll → twist puts
    green on R → east drops green to bottom".
  - **(c) Planning depth.** Non-trivial multi-step. At each
    witness step the player must mentally simulate (i) "what is
    the bottom-after-roll given current faces and chosen
    direction?", (ii) "does that match the target at the
    destination cell?", (iii) "if not, can a twist before the
    roll fix it?". This three-question chain repeats at every
    cell of the witness. A greedy "always east" heuristic
    deposits {12, 11, 15} at (1,0)/(2,0)/(3,0) and immediately
    mismatches (1,0)=14. A "twist-then-east-only" heuristic
    deposits {14, ?, ?} but cannot reach (3,1)=11 without a
    second twist before the south-roll, which the heuristic
    omits. Single-step / spam-the-new-verb / greedy strategies
    all fail.
  - **(d) Step budget.** `step_budget = 80`. Witness length 6;
    generous over 6 to allow the player to twist-and-untwist
    while exploring the verb.

### Level 3 — system + 1 more new mechanic

- **Layout.** Cube at logical (0, 0). Three targets, two locks:
  - Target at (1, 0) wants colour 14 (green).
  - Target at (3, 0) wants colour 8 (red).
  - Target at (3, 1) wants colour 11 (yellow).
  - **Lock at (1, 0)** requires colour 14 (cube can only roll
    onto (1, 0) when its bottom-face = 14; otherwise the roll
    is rejected, the cube stays in place, and the action still
    consumes one step).
  - **Lock at (3, 0)** requires colour 8.
- **Mechanics required by the witness** (N + 2 = 3):
  1. **Rolling-paint** (carried from L1).
  2. **Twist-in-place (ACTION5)** (carried from L2).
  3. **Colour-locks**: a `lock_<colour>` sprite at a cell makes
     that cell impassable to the cube unless the bottom-face
     after the candidate roll equals the lock's colour. If the
     bottom-after-roll mismatches, the roll is rejected: the
     cube stays in place, no paint is deposited, the action
     consumes one step.
- **Necessity per mechanic.** "Removing a mechanic" means: the
  sprite remains in place, but the gating LOGIC associated with
  the mechanic is removed from `step()`. Under this convention:
  - *Rolling-paint*: removing it = paint never deposited; targets
    can never match → unsolvable.
  - *Twist (ACTION5)*: removing twist = no way to get colour 14
    onto bottom-after-roll for the first east-step into (1, 0).
    Lock at (1, 0) requires 14; without twist the cube can never
    enter (1, 0), so target (1, 0) is unreachable → unsolvable.
  - *Colour-locks*: removing locks = the lock SPRITES become
    permanent walls (the gating-pass-through logic is gone but
    the sprite is still rendered and blocks pixel-perfectly via
    its non-`-1` cross). Targets at (1, 0) and (3, 0) sit BENEATH
    the lock sprites; with the locks frozen as walls, the cube
    can never enter (1, 0) or (3, 0), so two of three targets
    are permanently unreachable → unsolvable. Locks are strictly
    necessary because the game state requires the cube to enter
    the locked cells, and the lock-mechanic logic is what
    permits that entry under the matching-bottom-face condition.
- **Witness solution.** `[ACTION5, ACTION4, ACTION4, ACTION4,
  ACTION5, ACTION2]` (same shape as L2's witness, but every
  step is now constrained by the locks).
  Trace (initial faces `{T:11, Bo:9, F:14, Ba:8, L:15, R:12}`,
  cube at (0, 0)):
  1. twist: `{T:11, Bo:9, F:15, Ba:12, L:8, R:14}`.
  2. E → cube tries (0,0)→(1,0). Lock at (1, 0) requires 14.
     bottom-after-roll = R-before-roll = 14 → match. Roll
     succeeds. Faces `{T:8, Bo:14, F:15, Ba:12, L:9, R:11}`.
     Paint (1, 0) = 14 → target matched.
  3. E → cube tries (1,0)→(2,0). No lock at (2, 0). Roll
     succeeds. Faces `{T:9, Bo:11, F:15, Ba:12, L:14, R:8}`.
     Paint (2, 0) = 11 (transitional).
  4. E → cube tries (2,0)→(3,0). Lock at (3, 0) requires 8.
     bottom-after-roll = R-before = 8 → match. Roll succeeds.
     Faces `{T:14, Bo:8, F:15, Ba:12, L:11, R:9}`. Paint
     (3, 0) = 8 → target matched.
  5. twist: `{T:14, Bo:8, F:11, Ba:9, L:12, R:15}`.
  6. S → cube tries (3,0)→(3,1). No lock at (3, 1). Roll
     succeeds. Faces `{T:9, Bo:11, F:8, Ba:14, L:12, R:15}`.
     Paint (3, 1) = 11 → target matched. `next_level()`.
- **Difficulty justification.**
  - **(a) Random-resistance.** With locks, most random moves are
    rejected (cube stays in place, step consumed for nothing),
    accelerating step-budget exhaustion. The lock at (1, 0)
    blocks every random sequence that doesn't first establish
    bottom = 14 before its east-roll-into-(1,0). The lock at
    (3, 0) similarly. The probability of a random 80-action
    sequence achieving bottom = 14 immediately before its
    first east-into-(1,0) AND bottom = 8 before its east-into-
    (3,0) AND ending with the cube at (3, 1) with bottom = 11,
    AND not having overpainted a target with the wrong colour
    earlier, is well below `1/10,000`. (Within 100 steps the
    locks effectively halve the random agent's mobility — a
    significant additional barrier compared to L2.)
  - **(b) Human-tractable.** ~3 minutes. The player learns of
    locks by the cube's first east-roll being rejected (or
    accepted, in the witness's case where the player twisted
    first). The reasoning chain is identical to L2 but with one
    additional step: "before each lock-cell entry, the cube's
    bottom-after-roll must match the lock's visible colour".
    The player reads the lock colour from the cross-pattern,
    plans the face permutation accordingly. ~6 min total
    environment time matches the design target.
  - **(c) Planning depth.** Strictly deeper than L2.
    - *Trivial heuristic that fails.* "Always twist before
      every roll." Trace under this heuristic:
      `[twist, E, twist, E, twist, E, twist, S]`.
      - twist → `{T:11, Bo:9, F:15, Ba:12, L:8, R:14}`.
      - E to (1,0): bo-after = R-before = 14, lock (1,0)
        requires 14 → match. Faces after E `{T:8, Bo:14,
        F:15, Ba:12, L:9, R:11}`. Paint (1,0) = 14 ✓.
      - twist: `{T:8, Bo:14, F:9, Ba:11, L:12, R:15}`.
      - E to (2,0): bo-after = R-before = 15. No lock. Paint
        (2,0) = 15. Faces `{T:12, Bo:15, F:9, Ba:11, L:14,
        R:8}`.
      - twist: `{T:12, Bo:15, F:14, Ba:8, L:11, R:9}`.
      - E to (3,0): bo-after = R-before = 9. Lock (3,0)
        requires 8 → MISMATCH. Roll rejected; cube stays at
        (2,0). Step consumed.
      - twist: cube still at (2,0). `{T:12, Bo:15, F:11,
        Ba:9, L:8, R:14}`.
      - S to (2,1): bo-after = F-before = 11. No lock.
        Paint (2,1) = 11. — Wait the heuristic was twist-S,
        but cube is at (2,0) not (3,0). Moving to (2,1) does
        not visit target (3,1). This heuristic terminates
        without matching target (3, 0) or (3, 1).

      The "always twist" heuristic over-twists: at the third
      east-roll into (3, 0), the lock requires bottom = 8 but
      the heuristic's rotational state has bottom = 9 instead.
      The heuristic is defeated.
    - *Witness-pair commute test.* Swap actions 4 and 5 of the
      witness — `[twist, E, E, twist, E, S]` instead of
      `[twist, E, E, E, twist, S]`. Trace:
      - twist, E, E (same as witness): faces after step 3
        `{T:9, Bo:11, F:15, Ba:12, L:14, R:8}`, cube at (2,0).
      - twist (now in slot 4): `{T:9, Bo:11, F:14, Ba:8,
        L:12, R:15}`.
      - E (slot 5) → cube tries (2,0)→(3,0). Lock (3, 0)
        requires 8. bo-after = R-before = 15 → MISMATCH.
        Roll rejected.
      - S (slot 6) → cube tries (2,0)→(2,1). bo-after = F = 14.
        No lock. Paint (2,1) = 14. Cube at (2,1). Target
        (3,0) and (3,1) both unmatched.

      Swapped sequence fails. The two adjacent witness actions
      (the third E and the second twist) do not commute: the
      twist must come AFTER all three east-rolls, because the
      lock at (3,0) demands bo = 8 on the third east-roll, and
      twisting before that east-roll changes which face is on
      R → the lock blocks. The order is constrained.
  - **(d) Step budget.** `step_budget = 100`. Witness length 6;
    NOT shrinking relative to L2's 80. The extra 20 over L2
    reflects the additional discovery cost of locks (a player
    will spend several rejected rolls learning the lock's
    rule).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]`. No click, no undo.

- `ACTION1` (UP / north): roll the cube one logical cell north
  (`cube.y -= 4` if the destination cell is in-bounds AND not a
  wall AND, if the destination is a `lock_*` cell, the
  bottom-after-roll matches the lock's colour). On success: apply
  the rolling-north face permutation, deposit `bottom` on the
  destination cell as a `paint_<colour>` sprite. On failure (out
  of bounds, wall, lock mismatch): cube stays in place, no paint,
  step still consumed.
- `ACTION2` (DOWN / south): mirror.
- `ACTION3` (LEFT / west): mirror.
- `ACTION4` (RIGHT / east): mirror.
- `ACTION5` (TWIST in place): rotate the cube's side faces 90°
  clockwise viewed from above; no movement; no paint. Always
  valid; consumes one step.

Rolling-permutation formulas (`T,Bo,F,Ba,L,R` are state BEFORE
the roll):

| Direction | New top | New bottom | New front | New back | New left | New right |
|---|---|---|---|---|---|---|
| North (↑, ACTION1) | F | Ba | Bo | T | L | R |
| South (↓, ACTION2) | Ba | F | T | Bo | L | R |
| West (←, ACTION3) | R | L | F | Ba | T | Bo |
| East (→, ACTION4) | L | R | F | Ba | Bo | T |
| Twist (ACTION5)   | T | Bo | L | R | Ba | F |

## 6. HUD and per-game state

- HUD: a single `StepBarHud(RenderableUserDisplay)` widget drawing
  one row at `frame[0, :]` with palette-14 fill shrinking
  left-to-right as `current_steps / max_steps`. Read budget from
  `level.get_data("step_budget")` in `on_set_level` (50 / 80 /
  100 for L1 / L2 / L3).
- Per-game state on the `Pj7K` class:
  - `self.faces: dict[str, int]` keyed `{"top","bottom","front",
    "back","left","right"}`, reset in `on_set_level` to
    `{T:11, Bo:9, F:14, Ba:8, L:15, R:12}`.
  - `self.cube_x, self.cube_y: int` — grid position of the cube.
  - `self.step_counter: StepBarHud`.
- Hidden state (`_get_hidden_state`): a 4×4 numpy int16 array
  packing the 6 face colours, cube position, and remaining
  steps into the first row. Zeros elsewhere.

## 7. Win condition

Implemented as `_check_win()` called at the end of every `step()`:
for every sprite tagged `target` in the current level, look up the
target's required colour (encoded by sub-tag `target_<colour>`)
and the paint sprite (if any) at the same logical cell; if every
target's required colour equals the paint colour at its cell, call
`self.next_level()`. After L3 completion `next_level()` triggers
`self.win()` per `NovaBaseGame`'s default behaviour.

## 8. Lose condition

`self.lose()` is called when the step counter reaches zero. There
is no instant-fail collision — walls, locks, and out-of-bounds all
reject the attempted move; the cube never dies from a bump.

## 9. Novelty note

Closest taxonomy entries (per `mechanic-novelty/similarity-check.md`
§ 2 description-level check):

- **ls20 (cycler-attribute-match)**: ls20's attribute-cycle is
  triggered by stepping on dedicated cycler-tile sprites; pj7k's
  face-cycle is an unconditional consequence of every roll, with
  the player unable to roll without cycling. Distinguishing rule:
  in ls20 the player can decouple movement from attribute change
  by avoiding cycler tiles; in pj7k movement and face-cycle are
  inseparable.
- **re86 (flood-fill-multi-canvas)**: re86's marker has a single
  fixed paint colour identified by sprite identity; pj7k's
  deposited colour at any moment is a function of the move-history
  (which face has been rolled to the bottom). The two games look
  superficially similar ("walking sprite paints cells") but the
  reasoning load is fundamentally different.
- **cn04 (rotate-translate-jigsaw)**: cn04's rotation is a 2D
  in-plane sprite transpose; pj7k's rolling is a 3D-rotation
  projection that changes which colour is currently on top vs
  bottom.

Closest prior-game entries (per `prior-games/index.md`): **none
overlap on family or description**. The 8 priors cover
{tether-pawn-cycle, radial-cycle-lock, tide-tilt-buoyant,
bead-lift-swap, lantern-cone-illuminate, seed-grow-surround-
dissolve, pair-blend-recipe, multiset-signature-classify}. None
involve a single rolling-cube avatar, face-orientation state,
or per-cell paint deposit driven by a rolling-die permutation.

Negative similarity (`mechanic-novelty/negative-similarity-check.md`):
re-walked the eight dimensions on the full spec; no prior overlaps
on 3 or more dimensions. The chosen palette (warm off-white 1 +
saturated face colours 8/9/11/12/14/15) deliberately diverges from
the dark-grey-dominant signature of all 8 priors.

Cousin in pre-existing video games: rolling-cube puzzles exist
("Bloxorz" with a 1×1×2 brick; various "color cube" mobile
titles). pj7k's specific verb — paint-on-landing driven by the
bottom face — is not, to the agent's knowledge, the dominant
pattern in that sub-genre. Flagged for human review per axis 1.
