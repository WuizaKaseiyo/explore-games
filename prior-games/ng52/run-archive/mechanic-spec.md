# Spec — ng52

## 1. Title
Multiset Signature Classifier (working title; not visible in-game).

## 2. Mechanic family
`multiset-signature-classify` — the player partitions a pool of
irregularly-shaped multi-pixel sample objects into N bins, each
of which displays a *signature* expressed as a stack of 1×L
solid-colour sticks. A bin matches if and only if the multiset of
pixel-colour counts of all the objects placed in it equals the
multiset implied by its signature. Difficulty grows from
single-stick single-colour signatures with one object per bin (L1)
to multi-stick multi-colour signatures requiring multiple objects
per bin (L2) to a level with distractor objects that must be
deliberately left out of every bin (L3).

Prior categories (per `core-knowledge-priors.md`):
- **Objectness** — sample objects are persistent click-targets
  with stable colour-count fingerprints under movement.
- **Basic geometry / topology** — the stick-stack signature is a
  topological diagram of "this many cells of that colour, regardless
  of shape", and the bin's holding area is a topological container
  whose contents are summed across.

## 3. Sprite roster

(Coordinates in §4 are concrete and used by the implementation.
Palette values per `global/color-legend.md`.)

- **`sample_object`** — 2×3 to 3×3 sprite holding a non-convex
  arrangement of solid-colour pixels and `-1` (transparent). One
  unique sprite per object instance per level. Tags:
  `["object"]`. Cloned per object with the right pixel pattern.
  Layer 3.

- **`object_outline`** — a 1-pixel-thick ring drawn around the
  *currently selected* object. Tags: `["selection_ring"]`.
  Toggled via `InteractionMode.INTANGIBLE` (visible) ↔ `REMOVED`
  (hidden). Layer 5. Resized at runtime to the selected object's
  bbox.

- **`bin_frame`** — a hollow rectangle marking each bin's holding
  area. Tags: `["bin_frame"]`. Always visible. Layer 1.

- **`signature_stick`** — a 1×L horizontal solid-colour run
  stamped above the bin frame. Tags: `["signature_stick"]`.
  Always visible. Layer 1. Multiple sticks stack vertically with
  a 1-pixel gap.

- **`pool_divider`** — a horizontal 1-pixel-tall off-black line
  separating the bin row from the pool tray. Tags: `["decor"]`.
  Layer 1.

- **`bin_divider`** — a vertical 1-pixel-wide off-black line
  separating bins. Tags: `["decor"]`. Layer 1.

- **`step_bar_hud`** — `RenderableUserDisplay`; horizontal step
  bar at row 0 (pattern from qb84 / qz73 / hr8q).

## 4. Level progression, mechanic enumeration, and witness solutions

Grid size: `(64, 64)` for all three levels (default camera).

Coordinate conventions (used identically across L1, L2, L3):

- Bin columns:
  - Bin A: x ∈ [2, 21]; Bin B: x ∈ [22, 41]; Bin C: x ∈ [42, 61].
- Within each bin column, signature display rows ∈ [3, 9],
  holding area rows ∈ [12, 30].
- Pool tray rows ∈ [33, 62] (height 30, full width).
- Bin holding-area placement slots: a 4-column × 4-row 4×4 grid
  (16 slots). Slot (col, row) top-left = bin's leftmost holding
  cell + (col×4, row×4). Objects are placed at the next free
  slot in row-major order.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N=1):
  1. **place-and-commit-classify** — ACTION6 click on a pool
     object selects it (visual ring); next ACTION6 click on a
     bin's holding area places it there; ACTION5 commits and
     compares each bin's pixel-multiset against its signature.
     Match ⇒ next level. Mismatch ⇒ snap-back-to-pool.

- **Necessity per mechanic**: the only path that produces
  `next_level()` is to bring every bin into multiset agreement
  with its signature and fire ACTION5. Removing any sub-step
  (selection, placement, commit) breaks the only path to the
  win.

- **Bins**:
  - Bin A signature: `[1×3 blue]` ⇒ multiset `{blue: 3}`.
  - Bin B signature: `[1×4 blue]` ⇒ multiset `{blue: 4}`.
  - Bin C signature: `[1×5 blue]` ⇒ multiset `{blue: 5}`.

- **Pool objects** (3 objects, all single-colour blue,
  deliberately non-stick shapes):
  - O1: 3-blue L-shape, `[[B, B], [B, -1]]` placed at pool
    centroid (8, 38).
  - O2: 4-blue T-shape, `[[B, B, B], [-1, B, -1]]` at (24, 38).
  - O3: 5-blue plus-shape,
    `[[-1, B, -1], [B, B, B], [-1, B, -1]]` at (44, 38).
  - Each object is the ONLY pool member whose pixel-count
    matches one of the bins' signatures (3, 4, 5 respectively).

- **Witness solution** (7 actions):
  1. `ACTION6@(9, 39)` — click O1 (3-blue L). O1 selected.
  2. `ACTION6@(11, 20)` — click bin A holding area; O1 placed.
  3. `ACTION6@(25, 39)` — click O2 (4-blue T). O2 selected.
  4. `ACTION6@(31, 20)` — click bin B holding area; O2 placed.
  5. `ACTION6@(45, 39)` — click O3 (5-blue plus). O3 selected.
  6. `ACTION6@(51, 20)` — click bin C holding area; O3 placed.
  7. `ACTION5` — commit; every bin's multiset matches; win.

  Step budget: 40.

- **Difficulty justification**:
  - **(a) Random-resistance**: a random policy among ~10 click
    cells + ACTION5 has prior <1/11^7 ≈ 1/2×10^7 of producing
    this exact sequence; well under 1/10k. Random commit at any
    interim configuration is a no-op-with-snap-back, so random
    cannot stumble through.
  - **(b) Human time**: ~30 seconds. The player counts pixels
    per object, matches to the obvious signature, places, commits.
  - **(c) Planning depth**: near-zero, as L1 requires. Mechanic
    discovery is the difficulty.
  - **(d) Step budget**: 40. Witness is 7; budget is ~5.7×
    witness. Generous over the witness, allowing 4-5 wrong
    placements + reset before the budget bites.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (N+1=2):
  1. **place-and-commit-classify** (carried forward).
  2. **multi-stick compositional bin** (NEW): a bin's signature
     is a vertical *stack* of two or more 1×L sticks of distinct
     colours; the bin matches when the multiset summed *across
     all currently-held objects* equals the union of those
     sticks. This means (i) signatures can express multiple
     colours simultaneously, and (ii) bins can — and must, given
     L2's pool — hold MULTIPLE objects whose pixel counts sum to
     the signature.

- **Necessity per mechanic**: the L2 pool is designed so that
  NO single object in the pool has a pixel-multiset equal to any
  bin's signature. Every bin's signature is reachable only by
  combining 2 objects whose multisets sum correctly. Removing
  the "multi-stick compositional" mechanic (i.e., reverting to
  single-stick bins that hold one object each) ⇒ no bin can be
  filled to its signature ⇒ unsolvable. Removing place-and-
  commit-classify ⇒ no commits possible ⇒ unsolvable.

- **Bins**:
  - Bin A signature: `[1×6 blue]` ⇒ `{blue: 6}`.
  - Bin B signature: `[1×3 blue, 1×3 purple]` ⇒
    `{blue: 3, purple: 3}`.
  - Bin C signature: `[1×4 blue, 1×2 purple]` ⇒
    `{blue: 4, purple: 2}`.

- **Pool objects** (6 objects; chosen so the pool's *total*
  pixel multiset is exactly `{blue: 13, purple: 5}` = sum of all
  three signatures, and so that no single object matches any
  signature alone):
  - O1: 3-blue L-shape, `[[B, B], [B, -1]]` at (4, 38).
  - O2: 3-blue Z-shape, `[[B, B, -1], [-1, B, B]]` at (14, 38).
  - O3: 3-blue V-shape, `[[B, -1, B], [-1, B, -1]]` at (24, 38).
  - O4: 4-blue T-shape, `[[B, B, B], [-1, B, -1]]` at (34, 38).
  - O5: 3-purple L-shape, `[[P, P], [P, -1]]` at (44, 38).
  - O6: 2-purple diagonal, `[[P, -1], [-1, P]]` at (54, 38).
  (B = blue = 9; P = purple = 15.)

- **Witness solution** (13 actions):
  1. `ACTION6@(5, 39)` — click O1 (3B). O1 selected.
  2. `ACTION6@(11, 20)` — click bin A; O1 placed.
  3. `ACTION6@(15, 39)` — click O2 (3B). O2 selected.
  4. `ACTION6@(11, 20)` — click bin A; O2 placed. Bin A holds
     two 3B objects ⇒ multiset `{blue: 6}` ✓.
  5. `ACTION6@(25, 39)` — click O3 (3B). O3 selected.
  6. `ACTION6@(31, 20)` — click bin B; O3 placed.
  7. `ACTION6@(45, 39)` — click O5 (3P). O5 selected.
  8. `ACTION6@(31, 20)` — click bin B; O5 placed. Bin B holds
     `{blue: 3, purple: 3}` ✓.
  9. `ACTION6@(35, 39)` — click O4 (4B). O4 selected.
  10. `ACTION6@(51, 20)` — click bin C; O4 placed.
  11. `ACTION6@(55, 39)` — click O6 (2P). O6 selected.
  12. `ACTION6@(51, 20)` — click bin C; O6 placed. Bin C holds
      `{blue: 4, purple: 2}` ✓.
  13. `ACTION5` — commit; all bins match; win.

  Step budget: 60.

- **Difficulty justification**:
  - **(a) Random-resistance**: action space ~13 click cells +
    ACTION5. A 13-action specific sequence has prior <1/14^13 ≈
    1/8×10^14; vastly below 1/10k. Random commits before all bins
    are correct trigger snap-back-to-pool, so random progress
    is undone.
  - **(b) Human time**: ~1.5 minutes. Count pixels per object,
    plan which 2 objects sum to each bin, place, commit.
  - **(c) Planning depth — non-trivial multi-step reasoning**:
    Per-step reasoning chain:
    *Step 1*: read each bin's signature multiset.
    *Step 2*: count each pool object's pixel-colour multiset.
    *Step 3*: for each bin, identify the *pair* of objects whose
      multisets sum to the signature. Bin A (`{blue: 6}`) =
      O_i + O_j where i, j ∈ {3-blue objects}. Bin B
      (`{blue: 3, purple: 3}`) = a 3-blue + a 3-purple. Bin C
      (`{blue: 4, purple: 2}`) = the 4-blue + the 2-purple.
    *Step 4*: notice pair selection for bin A is constrained by
      what's left for bins B and C — there are three 3-blue
      objects and bin A consumes two, leaving exactly one 3-blue
      for bin B. Plan accordingly.
    *Step 5*: execute placements two-at-a-time per bin; verify
      mentally that each bin's multiset is correct before
      committing.
    Single-step solutions are impossible: no individual object
    matches any bin's signature. Spam-the-commit-verb fails:
    ACTION5 with any incomplete configuration triggers
    snap-back-to-pool. 1-action lookup tables fail: the partition
    requires combining at least 2 objects per bin × 3 bins.
  - **(d) Step budget**: 60. Witness is 13; budget is ~4.6×
    witness. Generous, NOT shrinking from L1's 40. A first-time
    player will spend several actions exploring (e.g. trying
    O1 alone in bin A then realising 3 ≠ 6 only on commit, which
    snaps back) before settling on the witness — budget reflects
    that exploration cost.

### Level 3 — system + 1 more new mechanic

- **Mechanics required by the witness** (N+2=3):
  1. **place-and-commit-classify** (carried forward).
  2. **multi-stick compositional bin** (carried forward).
  3. **selective placement with distractors** (NEW): the pool
     contains a *distractor object* whose pixel multiset does
     not fit cleanly into any bin's signature; the player must
     deliberately LEAVE the distractor in the pool. A commit
     fired with the distractor still placed in any bin (or with
     the distractor placed *anywhere*) will mismatch and trigger
     snap-back.

- **Necessity per mechanic**:
  - place-and-commit-classify: as L1.
  - multi-stick compositional bin: as L2 (every bin needs ≥2
    objects; no single object matches any bin's signature).
  - selective placement: at L3, total pool pixel-count
    > total signature capacity. Without the "leave some objects
    in the pool" mechanic (i.e., requiring every object to be
    placed in some bin), the partition cannot satisfy any bin.
    Strict necessity ⇒ unsolvable without selective placement.

- **Bins** (same signatures as L2 — same multi-stick
  composition):
  - Bin A signature: `[1×6 blue]` ⇒ `{blue: 6}`.
  - Bin B signature: `[1×3 blue, 1×3 purple]`.
  - Bin C signature: `[1×4 blue, 1×2 purple]`.

- **Pool objects** (7 objects = L2's six + one distractor):
  - O1..O6: same as L2 (3B-L, 3B-Z, 3B-V, 4B-T, 3P-L, 2P-diag).
  - **O7: 5-blue plus-shape**,
    `[[-1, B, -1], [B, B, B], [-1, B, -1]]` at (4, 53).
    (The distractor — a 5-blue object that does not sum into
    any bin's signature when combined with any subset of the
    other objects without breaking another bin.)
  - Pool total pixels = `{blue: 18, purple: 5}`. Bin signature
    total = `{blue: 13, purple: 5}`. Excess = 5 blue pixels =
    exactly O7. The ONLY feasible partition leaves O7 in the
    pool.

- **Witness solution** (13 actions — same placements as L2,
  with O7 deliberately untouched):
  1-13. Same 13-action sequence as L2's witness. O7 remains in
        the pool throughout. ACTION5 commit fires; bins match
        their signatures; O7 is irrelevant to the check (the
        check looks only at what is *placed*, not at what
        remains in the pool). Win.

  Step budget: 60.

- **Difficulty justification**:
  - **(a) Random-resistance**: action space ~15 click cells +
    ACTION5. The witness ignoring O7 is a specific 13-action
    sequence; <1/16^13 ≈ 1/4×10^15 random prior; far below
    1/10k.
  - **(b) Human time**: ~3 minutes. ~5 minutes total environment
    time (with L1 ~30s, L2 ~1.5 min) — within
    `difficulty-rules.md` §b's "around 6 minutes" target.
  - **(c) Planning depth — strictly deeper than L2**:

    *Trivial heuristic that fails*: **"place every object
    somewhere"** — the *exhaustive-placement* heuristic. A
    player who internalises L2's "use every object" pattern
    will try to fit O7 into some bin: bin A (6B) doesn't fit
    5B alone (needs 6); pairing 5B+1B requires a 1B object
    which doesn't exist; bin B (3B+3P) doesn't fit 5B; bin C
    (4B+2P) doesn't fit 5B. Whatever bin O7 lands in, that bin
    will mismatch on commit and trigger snap-back. Across
    consecutive failed commits the player must REALISE that O7
    is meant to stay in the pool — a qualitatively new insight
    the L1/L2 mechanics did not require.

    *Adjacent witness-pair commute test*: swap actions 4 and 5,
    i.e. swap `[ACTION6@bin A, ACTION6@O3]` ⇒
    `[ACTION6@O3, ACTION6@bin A]`. After action 3 (`ACTION6@O2`)
    the selection is O2. Original action 4 placed O2 into bin A
    (which now holds {O1, O2} → multiset {blue: 6} ✓). Original
    action 5 selected O3 for the next placement. After the swap:
    action 4 is now `ACTION6@O3` — clicking another object while
    O2 is selected switches the selection to O3 (O2 returns to
    its pool position; O2 is no longer selected). Action 5 is
    now `ACTION6@bin A`: O3 is placed into bin A (bin A holds
    {O1, O3} → multiset {blue: 6} ✓ at the *bin* level — but
    bin B's witness path needed O3 specifically). Continuing the
    rest of the witness verbatim: action 6 selects O5 (3P);
    action 7 places O5 into bin B (bin B holds {O5} → {purple: 3}
    — missing the 3-blue half). The witness can no longer
    complete in 13 actions because bin B's 3-blue requirement is
    no longer met (only one 3-blue object remains in the pool —
    O2 — and the witness's plan placed O2 in bin A originally;
    after the swap O2 is in the pool instead, so the player would
    need to re-thread O2 back). The 13-action witness solution
    is broken by the swap: an additional ≥2 actions are required
    to re-thread O2 back into bin B (and the original bin-A
    membership must be re-checked). The level remains technically
    solvable in a longer sequence, but the 13-action witness is
    destroyed.

    Per-step reasoning chain (L3): "read each bin signature →
    count every pool object's pixel multiset → compute the
    pool's total multiset → subtract the bin-total from the
    pool-total to identify the distractor's multiset → identify
    which pool object IS the distractor → plan the L2-style
    partition over the *non-distractor* subset → execute
    placements → commit". The "subtract pool from bin-total to
    find the distractor" step is genuinely new at L3 and has no
    L2 analogue.

  - **(d) Step budget**: 60 (NOT shrinking from L2 even though
    L3's witness is the same length). Per `difficulty-rules.md`
    §d L3 — L3 has *more* discovery cost (a player must learn
    that some objects are distractors and must be left out, an
    insight that can't be acquired in L1 or L2). Generous over
    the witness; allows ≥3 reset cycles before budget exhausts.

## 5. Action mapping

`available_actions = [5, 6]`.

- **ACTION5 — Commit**.
  - For each bin, compute its current multiset = sum of
    pixel-colour counts of every object placed in it (counting
    only solid-colour pixels; `-1` transparent cells are skipped).
  - If every bin's computed multiset == its declared signature
    multiset (and the player has placed at least one object —
    a no-op commit with empty bins is a no-op for the win check
    but still costs a step): `next_level()`.
  - Else: snap every placed object back to its original pool
    position; clear the current selection.

- **ACTION6 — Click at `(x, y)`**.
  - Hit-test priority order:
    1. **A pool object** (object whose current position is in
       the pool tray): becomes the new selection. The previously
       selected object (if any) is deselected and stays where it
       was.
    2. **A bin-resident object** (object whose current position
       is inside a bin holding area): the object is *picked up*
       — it leaves the bin (bin's slot is freed, subsequent
       slots shift up if needed) and becomes the new selection;
       its visual position moves to a small "hand" indicator at
       a fixed y above the bin row until placed elsewhere.
    3. **A bin holding area** (the rectangle below the
       signature): if an object is currently selected, place it
       in that bin's next free slot. The object's visual
       position updates; the selection clears (selection ring
       removed).
    4. **Anywhere else**: no-op.

## 6. HUD and per-game state

**HUD widgets**:
- `StepBarHud` — horizontal step bar at row 0 (32 cells wide).

**Per-game state**:
- `self.objects: list[ObjectHandle]` where each
  `ObjectHandle` carries: the sprite, the per-colour pixel-count
  multiset, the original pool position `(x, y)`, the current
  position, and the current container (`"pool"` | `"bin_A"` |
  `"bin_B"` | `"bin_C"` | `"hand"`).
- `self.selection: ObjectHandle | None` — the currently
  selected object, with its outline ring sprite anchored to it.
- `self.bins: list[BinHandle]` — three bin records, each
  carrying: the bin's frame sprite, the bin's signature
  multiset (`dict[int, int]`), the list of placed
  `ObjectHandle`s in slot-order, and the bin's holding-area
  rectangle.
- `self.steps_used: int`, `self.max_steps: int`.

## 7. Win condition

`self.next_level()` (and ultimately `self.win()` on L3) fires when
ACTION5 is committed AND, for every bin, the bin's multiset of
pixel-colour counts (summed across all currently-placed objects)
equals the bin's declared signature multiset.

Pseudocode:
```
def _check_win() -> bool:
    for bin_h in self.bins:
        observed = aggregate_multiset(bin_h.placed_objects)
        if observed != bin_h.signature_multiset:
            return False
    return True
```

## 8. Lose condition

`self.lose()` fires when `self.steps_used >= self.max_steps` and
the win condition has not been met. (No other lose path; failed
commits cause snap-back-to-pool but do not end the level.)

## 9. Novelty note

(Full novelty analysis lives in `mechanic-pick.md`. Summary:)

- **Closest taxonomy entry**: `sb26 — tile-place-commit`.
  Distinguishing rule: sb26 is a *guess-with-feedback* game over
  a hidden code; ng52 is a *partition-with-visible-signatures*
  game with no hidden information.
- **Closest prior-game entry**: `hr8q — pair-blend-recipe`.
  Distinguishing rule: hr8q produces a single output colour
  from a 2/3-input recipe; ng52 partitions a pool of objects
  across multiple bins simultaneously, with no colour
  transformation. The two share only the universal step-counter
  axis on the negative-similarity walk (0/8 substantive
  overlap).

`prior-games/index.md` is non-empty (7 priors); each was checked
row-by-row and none implements multiset-classification.
