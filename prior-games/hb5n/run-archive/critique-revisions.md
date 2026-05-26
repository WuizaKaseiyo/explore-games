# Critique revisions — hb5n (pass #1)

Adversarial review against `design-constraints/checklist.md` items
1-22, novelty `similarity-check.md`, and `negative-similarity-check.md`.

## Items that PASS

1. ✅ Palette: all sprites use values 0..15 plus `-1` transparent.
2. ✅ Universal scaffold: spec describes the intended scaffold; implement
   state to follow.
3. ✅ `available_actions=[1,2,3,4,5]` — subset of [1..7].
4. ✅ Exactly 3 `Level` entries.
5. ✅ ID `hb5n` is 4-char lowercase alphanumeric, not a word, not in
   the 25 reference IDs, not in `prior-games/index.md`, not in the
   9 uncommitted prior-game directories.
6. ✅ Mechanics draw from core priors (geometry/topology +
   objectness).
7. ✅ No letters, digits-as-glyphs, real-world clipart, or cultural
   conventions in sprite designs (green/yellow pickup is a colour
   combination, not a symbol; magenta-on-dark lock is a colour
   combination, not an arrow/letter).
8. ✅ At least 2 distinct mechanics (4 total across levels).
9. ✅ L1 is a tutorial: just walk + rotate, reduced state (no walls,
   no pickup, no lock, no pickup-state, no rotation-lock), no
   on-screen text.
10. ✅ L2 and L3 increase difficulty by *composition* (each adds a new
    mechanic that must compose with the prior mechanics).
11. ✅ Mechanic inheritance and +1/+2 rule: L1 N=2, L2 = N+1 = 3,
    L3 = L2-count + 1 = 4. Every earlier-level mechanic remains
    listed and required.
13. ✅ Mechanic family absent from taxonomy (`polyomino-walker-rotate`
    is not in `mechanic-novelty/taxonomy-of-25-games.md`).
14. ✅ Mechanic family absent from prior-games (verified against
    `prior-games/index.md` and uncommitted recent priors).
15. ✅ Concrete distinguishing rules articulated against cn04, ar25,
    tu93, xv4n, zw91, nz3v, pz4t, nb6t, lt7m.
16. ✅ Win condition stated for all levels (set-equality
    `avatar_cells == target_cells`).
17. ✅ Lose condition stated (step budget exhaustion only;
    irreversibility argument given).
18. ✅ Per-level difficulty bullets a/b/c/d all present.
19. ✅ No hidden state without visible cue: anchor cell visually
    distinguished (orange-centre vs maroon-centre for body cells);
    rotation manifests as visible polyomino orientation;
    pickup consumption visible as sprite disappearance + new body
    cell appearing; lock cells visually marked with magenta dot
    pattern.
20. ✅ Not low-resolution: 4×4 px cells with internal frame+centre
    patterns; sprites differentiate by shape + colour, not colour
    alone.
21. ✅ UI teaches: anchor pivot is obviously the orange-centred cell;
    rotation is the visible effect of ACTION5; pickup is consumable
    (visual change on consumption); lock cells have a distinct
    pattern.
22. ✅ ACTION7 absent — slot 7 not in `available_actions`.

## Item that FAILS — Issue #1 (load-bearing)

### 12. Strict counterfactual necessity — M4 (rotation-lock) at L3

**Violation**: M4 as specified is not strictly necessary at L3. The
spec's witness path presses ACTION5 only at cell `(12, 4)`, which is
NOT a lock cell. The lock cells appear in the witness's traversal
(rows 1-3 cols 5-14) but ACTION5 is never attempted on a lock cell
in the witness, so M4's distinguishing behaviour (rejecting
ACTION5-on-lock-cell) is never *triggered* by the witness.

Spec §4 L3 "Necessity per mechanic" argues: *"if every cell were
lock-free, the player could rotate at any cell on the path. The
witness could then be shorter: rotate at the pickup cell (4, 2)
immediately after consuming, then walk east+south."*

But this argument is wrong for two reasons:

1. **The "shorter" alternate witness without M4 still wins L3.** It
   would just take ~20 actions instead of 21 — both fit the 80-step
   budget. M4 doesn't BLOCK the alternate path from winning; it
   only forces the player to take a slightly longer one. Per
   checklist item 12: *"Is there any way to win L within the step
   budget without ever triggering M?"* Answer for M4 as designed:
   YES (the rotate-at-(4,2) path doesn't trigger M4 either,
   because (4, 2) is not a lock cell).

2. **The witness's only rotation attempt is at (12, 4), a non-lock
   cell.** The witness itself does not trigger M4. Per checklist
   item 12, the witness must *exercise* every listed mechanic;
   M4's distinguishing behaviour (rejection-on-lock-cell) is not
   exercised by the witness.

The spec's M4 mechanic as designed is *redundant-decorative* per
the worked examples in checklist item 12 ("a 'redundant
decorative' mechanic whose effect lands on the same destination
the base mechanic would have produced anyway").

### Suggested fix

Replace M4 with a strictly-necessary mechanic. The cleanest choice
is **PIVOT-RESET CELL**:

- A special cell (sprite `pivot_reset`, magenta-on-dark-frame) on
  the playfield.
- When the avatar's anchor enters a pivot-reset cell, the *anchor
  designation transfers to a specific adjacent body cell* (the
  cell at relative offset `(-1, 0)` from the current anchor in
  rotation 0 frame — i.e. B). The avatar's relative-cells list is
  re-baselined so that B becomes the new (0, 0) anchor and the
  prior anchor A becomes the cell at relative (1, 0).
- Visually: the orange-centre marker moves to the new anchor cell;
  the prior anchor becomes maroon-centred (body).
- Subsequent ACTION5 rotations pivot around the new anchor (B).
- Pivot-reset cells are one-shot (set to `InteractionMode.REMOVED`
  after consumption).

**Why this is strictly necessary**: design L3's target slot as a
**T-shape silhouette** (cells `{(12, 12), (12, 11), (12, 13),
(13, 12)}` for an anchor-at-(12, 12) T at rotation 0, OR
`{(12, 12), (12, 13), (11, 12), (13, 12)}` for rotation 90, etc.).
The A-pivot 4-cell J's 4 rotations produce 4 distinct J-shape
silhouettes — none of them is a T. The B-pivot J's 4 rotations
produce 4 different silhouettes — one of which IS the T.

Therefore the avatar can *only* match the T-target slot by first
acquiring the 4th cell via M3, then switching pivot via M4, then
possibly rotating via M2 to align the B-pivot's correct rotation.

Strict counterfactual:
- *Without M4*: the avatar remains A-pivot. A-pivot J at rotations
  0/90/180/270 produces shapes `D/BA/C-`, `CBD/.A.`, `.C/AB/.D`,
  `.A./DBC` — none of which is a T. The target T-silhouette is
  geometrically unreachable. L3 unsolvable.
- *With M4*: pivot-reset consumes the M4 cell, switching to
  B-pivot. B-pivot's rotation 90 produces the T-silhouette. L3
  becomes solvable in 20 actions.

This passes strict counterfactual necessity.

**Why pivot-reset is novel** against the corpus:

- **pv5q (pivot-rod-swing)** — closest analogue. pv5q has a pawn
  at the END of a rigid radial rod attached to a fixed-position
  STAKE sprite; ACTION5 swaps the rod's stake. **hb5n
  distinguishing rule**: the avatar is a 2D polyomino (not a 1D
  rod attached to a separate stake); the pivot is one of the
  avatar's own cells (not a separate stake sprite); the pivot
  changes by walking the anchor onto a pivot-reset cell (not by
  ACTION5).
- **nz3v (rotor-pivot-walk)** — 2×2 SQUARE avatar; ACTION5
  rotates a separate WEDGE sprite (the world's lit sector), not
  the avatar. **hb5n distinguishing rule**: irregular polyomino,
  pivot is internal to the avatar, M4 changes which cell of the
  avatar serves as pivot (no wedge, no world rotation).
- **nb6t (hinge-chain-reach)** — 3 rod-segments at independent
  hinges. **hb5n distinguishing rule**: single rigid polyomino,
  no hinges, no per-segment selection; pivot is a designation
  swap, not a hinge actuation.

No prior or reference has "the rotation pivot transfers to a
different cell of the same rigid avatar by walking onto a special
cell". This is novel.

### Required spec changes

In `mechanic-spec.md`:

1. **§3 sprite roster**: add `pivot_reset` sprite (1×1 logical, 4×4
   px, with a distinct internal pattern — e.g. magenta-on-dark with
   a centre cross pattern to distinguish from `rotation_lock`):
   ```
   4 6 6 4
   6 6 6 6
   6 6 6 6
   4 6 6 4
   ```
   Tag `["pivot_reset"]`, `collidable=False`, `layer=0`. After
   consumption, `InteractionMode.REMOVED`.

2. **§3 sprite roster**: REMOVE the `rotation_lock` sprite (or repurpose
   for a different effect; here we just remove it to keep the spec
   clean).

3. **§3 sprite roster**: update the target slot for L3 to
   `target_slot_t_b_pivot_rot90` — a 4-cell T silhouette at the
   B-pivot's rotation 90, drawn as a dim palette-3 outline.

4. **§4 L3 redesign**:
   - Layout: outer wall ring; a few internal walls to constrain
     the path; pickup at `(5, 3)`; pivot-reset cell at `(10, 10)`;
     target slot at `(12, 12)` (T-shape at B-pivot rotation 90).
   - Replace all "rotation-lock" language with "pivot-reset"
     language.
   - Mechanic M4 is **PIVOT-RESET**: anchor entering a pivot-reset
     cell transfers anchor designation to the cell at current
     rotation-0 relative offset (-1, 0) (i.e. the B cell).
   - Witness solution (20 actions): `[ACTION4]×2 (pickup)`,
     `[ACTION4]×5 (anchor 5,3 → 10,3)`, `[ACTION2]×7 (anchor 10,3
     → 10,10; pivot-reset triggers on entry to (10,10))`,
     `[ACTION5]×1 (B-pivot rotation 0 → 90)`, `[ACTION4]×3 (anchor
     9,10 → 12,10)`, `[ACTION2]×2 (anchor 12,10 → 12,12)`.
   - Necessity argument: see above (target unreachable without M4).
   - Difficulty justification:
     - **(a)** random-resistance: `(1/6)^20 ≈ 2.7e-16`.
     - **(b)** human-tractable: ~2-3 minutes — the player learns
       pivot-reset by stepping on it and observing the orange-centre
       move to a different cell.
     - **(c)** planning depth: post-discovery, the player must
       realise that pre-pivot-reset rotations operate on the A-pivot
       (and target a different silhouette family) while
       post-pivot-reset rotations operate on the B-pivot. The
       trivial heuristic *"rotate to target orientation immediately
       after pickup, then walk"* fails because A-pivot rotations
       never produce the T-silhouette. The witness's reasoning
       chain: consume pickup at A-pivot rotation 0, then walk to
       pivot-reset to switch to B-pivot, then rotate to 90 at the
       B-pivot orientation that yields the T, then walk to target.
       Decision space at level start ≥ L2's (5 valid first actions:
       ACTION2/4/5 plus rejected ACTION1/3).
     - **(d)** step budget: **80** (unchanged from previous L3
       budget; generous over the 20-action witness).

5. **§5 Action mapping**: unchanged. Still `[1, 2, 3, 4, 5]`.

6. **§6 HUD and per-game state**: add `self.avatar_anchor_cell_index:
   int` — index into `self.avatar_relative_cells` indicating which
   cell is the current anchor (0 = A, 1 = B by default). Used to
   re-baseline relative-cells on pivot-reset.

7. **§9 Novelty note**: add the pivot-reset distinguishing-rule
   paragraphs vs pv5q and nz3v (above).

## Items that PASS but warrant noting

- L3's witness length (20 actions after revision) is still
  comfortably under the 80-step budget — good margin for
  exploratory rotation attempts and wrong-pivot attempts.
- The pivot-reset mechanic preserves the "no hidden state" property
  (item 19) because the orange-centre marker visibly migrates to
  the new anchor cell on consumption.

## Verdict

Transition back to `write_spec` for one revision. The single
load-bearing fix is replacing M4 (rotation-lock) with M4
(pivot-reset) as detailed above. All other checklist items pass.
