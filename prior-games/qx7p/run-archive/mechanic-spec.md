# mechanic-spec — qx7p

## 1. Title
Column-Shift Row-Align — vertical colour-band stacks slid past a
horizontal scan line to match a target row colour pattern.

## 2. Mechanic family
**`column-shift-row-align`.** A row of independent vertical "columns"
(tall thin sprite-bars) each holds a stack of differently-coloured
horizontal segments (a vertical bar-code of 12 segments × 3 rows).
A horizontal "scan line" cuts across all columns at one specific
row; the segment of each column intersected by the scan line is
that column's *currently aligned colour*. Player verbs are: click a
column to make it active, ACTION1/ACTION2 shift the active column's
band-stack up/down by one segment (cyclic), and (from L3) ACTION5
shift the scan line itself up/down by one segment-row. The level
wins when, for every column, the currently-aligned colour at the
scan line equals the colour shown for that column on a fixed
target-strip above the playfield.

Core-knowledge priors:
- **Objectness** — each column is a coherent persistent entity with
  a stable identity and a single integer state (its position).
- **Basic geometry & topology** — modular cyclic offset along a 1D
  axis; a horizontal scan-line as a fixed cross-axis intersecting
  every column; bound-pair coupling as a rigid sign-flipped linkage.
- **Basic physics** — bound-pair coupling reads as a mechanical
  link between adjacent columns: pushing one drives the other in
  the opposite direction by the same amount.

## 3. Sprite roster

The 64×64 frame uses no logical sub-grid scaling — `grid_size =
(64, 64)` for every level. Concrete pixel coordinates are given so
the witness solutions, the necessity arguments, and the L2/L3
geometry checks have a single source of truth.

| Name | Pixel size | Palette values | Tags | Role |
|---|---|---|---|---|
| `column_a` | 6 × 36 | column-bar pattern (see §3a) | `["column", "active"]` | First column. Internal pixel pattern is 12 stacked colour-segments × 3 rows × 6 cols, with a 1-px-wide left-and-right border in palette 4 to read as a discrete "bar" rather than a flat colour block. Position state stored on the game object, applied by `np.roll(pixels, -3 * position, axis=0)` in `on_set_level` and after each shift. |
| `column_b`,`column_c`,`column_d`,`column_e` | 6 × 36 | column-bar patterns (see §3a) | `["column"]` (tag `"active"` added/removed at runtime) | Subsequent columns; one variant per L1/L2/L3 column count (3 / 4 / 5). |
| `scan_line` | 64 × 1 | palette 0 (white) | `["scan_line"]` | Horizontal indicator drawn across the full frame at the current scan-line row. |
| `scan_line_marker_left`, `scan_line_marker_right` | 3 × 3 | palette 11 (yellow) flat solid square | `["scan_line_marker"]` | Two 3 × 3 solid yellow square bookend markers placed at the frame edges (rows centred on the scan-line row, columns 0..2 and 61..63). Non-directional — square, not chevron — so they don't read as arrows; they read as "row markers" pointing-out neither left nor right. (Fixes critique issue 2 — original chevron carets violated forbidden-elements "arrow shape implying direction".) |
| `target_patch_a`..`target_patch_e` | 8 × 5 | inner 6 × 3 fill from palette {8, 9, 11, 12, 14, 15}; 1-px outer border in palette 3 (grey) | `["target"]` | Target strip — one patch per column, painted in the colour the player must surface on that column at the scan line. Drawn with a 1-pixel grey border around a coloured interior so it reads as a *framed colour-sample label* rather than a stray flat block — addresses checklist item 20 (no two sprites differ only by fill colour). The interior 6 × 3 sits at the *same x* as its column so the visual coupling is unambiguous. (Fixes critique issue 4.) |
| `bound_pair_ribbon` | 14..30 × 1 | palette 12 (orange) | `["bound_pair", "ribbon"]` | A 1-px-tall horizontal ribbon connecting the tops of two paired columns at row 11; the ribbon colour and shape read as a tie/linkage. |
| `bound_pair_endcap_left`, `bound_pair_endcap_right` | 1 × 3 | palette 12 | `["bound_pair_endcap"]` | Small 1-cell-wide vertical caps at each end of the ribbon, descending into the column tops to make the ribbon read as physically attached. |
| `active_highlight_l`, `active_highlight_r` | 1 × 36 | palette 0 (white) | `["active_highlight"]` | Two thin 1-pixel-wide vertical strips drawn flanking the active column on left and right, set visible only while a column is selected. The active-column visual must persist for as long as the column is active — see §6. |
| `step_counter_hud` | (drawn by `RenderableUserDisplay`, not a Sprite) | palettes 11, 4 | n/a | Top-row step counter HUD: 64 × 1 strip at row 0 showing remaining steps as a yellow-on-off-black depleting bar. |
| `bound_pair_marker_dot_a`, `bound_pair_marker_dot_b` | 2 × 2 | palette 12 (orange) | `["bound_pair_marker"]` | Two small dot patches placed at the very top of each bound-pair column (row 11..12) to give a redundant visual cue beyond the ribbon, so the pairing reads even when columns scroll. |

### 3a. Column pixel-pattern construction

Each column's 36-row stack is constructed segment-by-segment. Each
segment is 3 rows × 6 cols. For each segment, the 6 cols are NOT a
flat coloured block: they are a stylised pixel motif (colour-fill at
columns 1..4, palette 4 (off-black) at columns 0 and 5 for a 1-px
side border) so the column visually reads as a *bar with bands*
rather than a flat coloured strip — addressing checklist item 20 on
visual richness. Segments are separated by no extra gap (3 rows
each, packed); the segment-to-segment transition is visible because
adjacent segments differ in colour.

Each column has 12 segments. Per-column colour orderings (named
indices 0..11 from top to bottom in the segment-stack) are designed
so that:

- Each colour from the level's palette appears at least once.
- Adjacent segments are always different colours (no two-segment
  runs of the same colour).
- The segment colours are pre-computed so the witness positions
  named in §4 produce the target colours at the scan line.

The 12 segment colours per column for L1/L2/L3 are fixed at level
authoring time. They are not regenerated per run.

### 3b. Where the scan line cuts each column

The scan line is at a per-level row `S`. The columns occupy rows
`Y_top` through `Y_top + 35` (36 rows tall). The visible segment at
the scan line for a column at vertical offset `Y_top` is segment
`((column.position + (S - Y_top) // 3) mod 12)`. The constant
`(S - Y_top) // 3` is fixed at level start. The witness positions in
§4 are stated as **column.position values** with the understanding
that the offset constant is rolled into them; the player only ever
sees segment colours, never segment indices.

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system
- **Mechanics required by the witness (N = 1):**
  - **M1: column-shift.** Click a column (ACTION6 inside its
    bounding box) to make it active; ACTION1 shifts the active
    column's segment stack upward by one segment (i.e. its
    `column.position` increments by 1 mod 12, and the segment
    visible at the scan line changes to the next segment in the
    cyclic order); ACTION2 decrements `column.position` mod 12.
    Only the active column responds. The scan line is fixed for
    this level.

- **Necessity per mechanic** (counterfactual, per checklist item
  12):
  - L1 cannot be solved without triggering M1 because at L1's
    initial state every column shows a colour at the scan line
    that *differs* from that column's target patch — concretely,
    `column_a` at position 0 shows red (palette 8) while its
    target patch is green (palette 14); `column_b` at position 0
    shows blue (palette 9) while its target is yellow (palette 11);
    `column_c` at position 0 shows yellow (palette 11) while its
    target is purple (palette 15). The win predicate (§7) fails
    until *every* column's scan-line colour equals its target
    patch, and the only way to change a column's scan-line colour
    is via M1.

- **Layout:**
  - `grid_size = (64, 64)`, scan line `S = 31` (centre-ish — drawn
    inside the segment that spans rows 30..32).
  - 3 columns:
    - `column_a` at x = 16, y = 14, position-target = 4.
    - `column_b` at x = 32, y = 14, position-target = 7.
    - `column_c` at x = 48, y = 14, position-target = 3.
  - 3 target patches drawn at the top of the playfield, each
    aligned in x with its column (rows 8..10, x = 16..21, 32..37,
    48..53).
  - No bound-pair ribbon; no movable scan line; no blockers.

- **Witness solution** (shortest action sequence, **15 actions** —
  uses `min(k, 12-k)` direction per column):
  ```
  ACTION6@(16,14)       # click column_a → active
  ACTION1 ×4            # shift column_a up 4 (4 < 12-4=8)
  ACTION6@(32,14)       # click column_b → active
  ACTION2 ×5            # shift column_b down 5 (5 < 12-5=7) →
                        # column_b.position becomes -5 ≡ 7 mod 12 ✓
  ACTION6@(48,14)       # click column_c → active
  ACTION1 ×3            # shift column_c up 3 (3 < 12-3=9)
  ```
  Total: 3 clicks + 12 shifts = **15 actions**. (Fixes critique
  issue 3 — original used ACTION1 ×7 for column_b, 2 actions
  longer than ACTION2 ×5.)

- **Difficulty justification:**
  - **(a) Random-resistance:** With 3 independent columns × 12
    positions = 12³ = 1,728 states. Within the L1 step budget of
    40 actions, a uniformly-random policy that does not
    distinguish the active column from the inactive ones has
    probability ≪ 1 of stumbling into the target — even
    discounting the click-to-select gating, the mean hit rate is
    on the order of 40 / 1728 ≈ 2.3%, and crucially the random
    policy must also click the right column before each shift to
    have ANY effect, which compounds the rejection rate.
  - **(b) Human time:** ~40-60 seconds for an attentive
    untrained human after first contact (discover that ACTION6
    selects, that ACTION1/2 shift, then count off shifts).
  - **(c) Planning depth:** L1 has *no strict planning
    requirement* — once the player understands shift, each
    column is solved independently. L1 is the discovery gate.
  - **(d) Step budget:** **40**. Generous over the 15-action
    witness (~2.7×) — leaves ample room for the player to over-
    shift and correct via the opposite arrow.

### Level 2 — base system + 1 new mechanic (= 2 mechanics total)
- **Mechanics required by the witness (= N + 1 = 2):**
  - **M1: column-shift.** Carried forward from L1, unchanged.
  - **M2: bound-pair coupling.** Two columns are visually linked
    by an orange ribbon at row 11 plus orange dot markers at
    each linked column's top. While a player is shifting one
    member of a bound pair (ACTION1 or ACTION2 on the active
    column), the partner column shifts by *the opposite amount*
    in the same animation tick. Internally: a `bound_pair[col]`
    map maps each linked column to its partner; whenever
    `column.position` changes by `dp`, partner's `position`
    changes by `-dp` mod 12. Click-to-select still picks one
    column at a time as active; the partner's
    `position`-update happens implicitly. The *visual* signature
    is the ribbon plus dots; the *behavioural* signature is the
    paired counter-shift. L2 introduces exactly **one** new
    mechanic (M2) on top of L1's M1.

- **Necessity per mechanic** (counterfactual, per checklist item
  12):
  - **M1 at L2:** L2 cannot be solved without triggering M1
    because at L2's initial state every column shows a colour at
    the scan line that differs from its target. Concretely:
    `column_a` at position 0 shows blue, target is yellow;
    `column_b` at position 0 shows yellow, target is purple;
    `column_c` at position 0 shows red, target is green;
    `column_d` at position 0 shows green, target is red. Reaching
    every target requires changing every column's `position`
    away from 0, and M1 (click + arrow-shift) is the only verb
    that mutates `column.position`.
  - **M2 at L2:** L2 cannot be solved without triggering M2's
    coupled-shift behaviour because *the bound-pair coupling is
    permanently active* — every shift to either bound-pair
    column ALSO mutates the partner. There is no way to mutate
    one bound-pair column's position without also mutating the
    partner's: the M2 rule fires on every M1 application to a
    bound-pair member. The puzzle is constructed so the
    bound-pair partners (`column_a`, `column_b`) start at
    position 0 / 0, whose targets are 4 / 8 (= -4 mod 12), i.e.
    perfectly antisymmetric — so the witness shifts `column_a`
    by +4 and the coupling drives `column_b` to 8 simultaneously,
    AND the witness has no shorter route. The independent columns
    `column_c`, `column_d` are unbound and shift normally; they
    are present so the level is not solved by bound-pair alone.

- **Layout:**
  - `grid_size = (64, 64)`, scan line `S = 31` (same as L1 — L2
    does not move the scan line).
  - 4 columns:
    - `column_a` at x = 12, y = 14, position-target = 4.
    - `column_b` at x = 26, y = 14, position-target = 8.
      (`column_a` and `column_b` are **bound-pair**; ribbon
      drawn from `(13, 11)` to `(31, 11)`, dots at `(14, 12)` and
      `(28, 12)`.)
    - `column_c` at x = 40, y = 14, position-target = 6.
    - `column_d` at x = 54, y = 14, position-target = 2.
  - Initial positions all 0.

- **Witness solution** (shortest, ~30 actions):
  ```
  ACTION6@(12,14)       # select column_a (the bound pair member)
  ACTION1 ×4            # shift column_a up 4 → column_a.position=4
                        # bound-pair: column_b.position drops from 0
                        # to -4 ≡ 8 mod 12. Both targets met.
  ACTION6@(40,14)       # select column_c
  ACTION1 ×6            # shift column_c up 6
  ACTION6@(54,14)       # select column_d
  ACTION1 ×2            # shift column_d up 2
  ```
  Total: 3 clicks + 12 shifts = **15 actions**.

  Plausible alternate witness routes:
  - Select `column_b` first and shift it +8: that drops
    `column_a` from 0 to -8 ≡ 4 mod 12. **Same** outcome; +8
    shifts on `column_b` is more action-expensive than +4 on
    `column_a` because it's 4 more shifts.
  - Decoupled-style attempts: shift `column_a` +4 (column_b
    becomes 8 — already correct), then shift `column_b`. But
    any shift on `column_b` drives `column_a` away from 4. So
    decoupled-style attempts always drift one of the pair off
    target. The witness above is uniquely shortest; the player
    *must* commit to the coupled effect and use it as the verb.

- **Difficulty justification:**
  - **(a) Random-resistance:** 4 columns × 12 positions, with
    bound-pair coupling reducing the coupled state space, gives
    on the order of 12 × 12² = 1,728 reachable joint
    configurations. Within the L2 step budget of 70, the chance
    of a uniformly-random policy hitting the target is < 1 in
    100 even before factoring in the click-to-select gating that
    forces every shift to be preceded by selecting a column.
  - **(b) Human time:** ~2 minutes — discover the bound-pair
    coupling within the first half-dozen shifts (the ribbon and
    matching orange dots are hard to miss; first attempt to shift
    `column_a` will *visibly* shift `column_b` in the opposite
    direction, which is the cue), then plan: do the bound pair
    first, do the unbound columns afterwards.
  - **(c) Planning depth — *post-discovery*:** Assume the player
    has fully understood that ACTION6 selects, ACTION1/2 shift,
    and shifting a bound column slides its partner the opposite
    way.
    - **Post-discovery decision space at level start:** the
      player faces 4 valid first actions (one ACTION6 click for
      each of the 4 columns), well above the 2-action floor. After
      the first click, the player has 2 valid arrow shifts, and
      among the 4 columns' possible orderings × 12 valid first
      shift counts, the post-discovery decision tree branches
      heavily.
    - **Plausible-but-wrong post-discovery alternative:** "Click
      `column_b`, shift it up +8 — both bound targets met,
      same as shifting `column_a` +4 — because the bound pair
      is symmetric." This *looks* equivalent but costs +8 shifts
      vs +4 shifts on the other partner; under the L2 step
      budget of 70 it still works, but a tighter L3 budget
      requires the cheaper pick. The *core* wrong path is "do
      the unbound columns first, then come back to the bound
      pair". This works in L2 (the unbound columns don't
      interact with the bound pair) but *teaches* an instinct
      that L3 will punish, see (c) below.
    - **Witness reasoning chain (post-discovery):** Step 1:
      identify `column_a` and `column_b` as bound (orange ribbon
      + dots). Step 2: notice their targets are antisymmetric
      around the start position (4 and 8 = -4 mod 12). Step 3:
      shift the cheaper member (`column_a`, 4 shifts vs 8 for
      `column_b`); the partner falls into place automatically.
      Step 4: do `column_c` and `column_d` independently in any
      order. Each step references the current geometric state
      (column positions modulo 12), not discovery-stage
      observations.
  - **(d) Step budget:** **70**. Generous over the 15-action
    witness — covers exploration of the bound-pair behaviour
    plus over-shoot recovery.

### Level 3 — system + 1 new mechanic (= 3 mechanics total)
- **Mechanics required by the witness (= L2-count + 1 = 3):**
  - **M1: column-shift** (carried forward from L1/L2).
  - **M2: bound-pair coupling** (carried forward from L2).
  - **M3: scan-line shift.** ACTION5 shifts the global scan-line
    row up by one segment (3 rows) when applied; the scan line
    cycles through three positions: row 22 (segment-3
    intersection), row 31 (centre, segment-5), and row 40
    (segment-8). Pressing ACTION5 advances one step in this
    cycle. The visual signature: the white scan-line row + its
    yellow caret marks at the frame edges visibly translate.
    Internally, a single integer `scan_line_idx ∈ {0, 1, 2}`
    tracks the current scan-line position; the visible-segment
    formula (§3b) becomes
    `(column.position + offset(scan_line_idx)) mod 12`. L3
    introduces exactly **one** new mechanic (M3) on top of L2.

- **Necessity per mechanic** (counterfactual, per checklist item
  12):
  - **M1 at L3:** L3 cannot be solved without triggering M1.
    Concretely: at the start scan line and start positions, no
    column shows its target colour at the scan line — for
    example, `column_a` shows red at scan line, target is
    purple. Reaching the target requires changing each column's
    `position`, which only M1 does.
  - **M2 at L3:** L3 cannot be solved without triggering M2's
    coupled shifts because the L3 layout has *two* bound pairs
    (`column_a`–`column_b` and `column_c`–`column_d`), each
    permanently coupled. Any M1 applied to any bound member
    *necessarily* triggers M2 on its partner — there is no
    decoupling action. The L3 puzzle further forces M2 to be
    actively useful: the targets per bound pair are antisymmetric
    relative to the *active scan line*, so shifting one bound
    member toward its target ALSO drives the partner toward its
    target. Without M2 the puzzle is overspecified and not
    solvable in budget; with M2 it solves with the witness below.
  - **M3 at L3:** L3 cannot be solved without using ACTION5 to
    shift the scan line because the bound-pair invariant
    constrains `column_a.position + column_b.position = 0 mod
    12`, and at the *start* scan line (row 22, segment-offset 3),
    the target colour pair for `column_a` and `column_b` requires
    `column_a.position + column_b.position = 6 mod 12` — which
    is impossible under the bound-pair invariant. Specifically:
    target colours for the bound pair correspond to segment
    indices `k_a = 3`, `k_b = 9` (so `k_a + k_b = 12 ≡ 0` mod
    12); under the start-row offset `3`, the required sum is
    `(k_a - 3) + (k_b - 3) = 6`, contradicting the
    bound-pair-zero invariant. Pressing ACTION5 once changes the
    offset from 3 to 5 (move scan line down to row 31), and the
    required sum becomes `(k_a - 5) + (k_b - 5) = 2`,
    still not zero. Pressing ACTION5 again advances the offset
    to 8 (scan line at row 40); the required sum becomes
    `(k_a - 8) + (k_b - 8) = -4 ≡ 8 mod 12`, still not zero. So
    a *single* ACTION5 is insufficient — the witness must use
    ACTION5 to find a (k_a, k_b) target where the offset
    cancels, which the L3 layout designs into the second-cycle
    target pair (see Layout: the *second* bound pair —
    `column_c`–`column_d` — has targets that are antisymmetric
    only under offset `5`, while the first pair is antisymmetric
    only under offset `8`; the witness uses the *cycle* of
    ACTION5 to satisfy each pair at its own offset and reads
    out the unbound `column_e` colour at whichever offset is
    last). A single fixed scan-line cannot satisfy both bound
    pairs simultaneously; at least one ACTION5 is mandatory.

- **Layout:**
  - `grid_size = (64, 64)`. Scan line cycle through rows
    {22, 31, 40} via ACTION5. Initial `scan_line_idx = 0`
    (row 22).
  - 5 columns:
    - `column_a` at x = 6, y = 14, target colour C_A.
    - `column_b` at x = 18, y = 14, target colour C_B.
      (Bound-pair 1 — `column_a`–`column_b` linked by ribbon
      at row 11.)
    - `column_c` at x = 30, y = 14, target colour C_C.
    - `column_d` at x = 42, y = 14, target colour C_D.
      (Bound-pair 2 — `column_c`–`column_d` linked by ribbon at
      row 11.)
    - `column_e` at x = 54, y = 14, target colour C_E (unbound,
      independent column).
  - Targets and segment placements designed so:
    - Pair 1 is *only* solvable at `scan_line_idx = 2` (row 40):
      `(k_a + k_b - 2 × offset(2)) mod 12 = 0` with
      `offset(2) = 8`, so `k_a + k_b = 16 ≡ 4 mod 12` — set
      `k_a = 3`, `k_b = 1` for bound-pair-1, with corresponding
      target colour patches.
    - Pair 2 is *only* solvable at `scan_line_idx = 1` (row 31):
      `k_c + k_d = 10` — set `k_c = 7`, `k_d = 3`.
    - Independent column 5 has target colour at any position;
      its target colour exists once in its segment list at
      index `k_e = 5`, requiring shift to `position = 5 -
      offset(scan_line_idx)` mod 12 at whichever scan-line is
      currently active when finalising it.

  Concretely (one valid choice — colours fixed at level
  authoring time so witness positions below resolve to fixed
  integers): bound pair 1 targets are red (8) and orange (12),
  with `column_a.colours[3] = 8` and `column_b.colours[1] = 12`
  (so the segment indices that produce the targets are
  `k_a = 3`, `k_b = 1`); bound pair 2 targets are yellow (11)
  and green (14), with `column_c.colours[7] = 11`,
  `column_d.colours[3] = 14`; independent column 5 target is
  purple (15) at `column_e.colours[5] = 15`.

- **Witness solution** (shortest, **15 actions** — uses
  `min(k, 12-k)` direction per column):
  ```
  ACTION5               # shift scan line to idx=1 (row 31)
  ACTION6@(30,14)       # select column_c (bound pair 2)
  ACTION1 ×2            # shift column_c +2; bound: column_d -2.
                        # column_c.position=2, column_d.position=10.
                        # At offset 5, column_c shows segment
                        # (2+5)=7=k_c=yellow ✓
                        # column_d shows segment (10+5)=15≡3=k_d=
                        # green ✓
  ACTION5               # advance scan line to idx=2 (row 40)
  ACTION6@(6,14)        # select column_a (bound pair 1)
  ACTION2 ×5            # shift column_a -5 (5 < 12-5=7); bound:
                        # column_b +5. column_a.position=7
                        # (-5≡7 mod 12), column_b.position=5.
                        # At offset 8, column_a shows segment
                        # (7+8)=15≡3=k_a=red ✓
                        # column_b shows segment (5+8)=13≡1=k_b=
                        # orange ✓
  ACTION6@(54,14)       # select column_e
  ACTION2 ×3            # shift column_e -3 (3 < 12-3=9);
                        # column_e.position=9 (-3≡9 mod 12).
                        # At offset 8, column_e shows segment
                        # (9+8)=17≡5=k_e=purple ✓
  ```
  Total: 2 ACTION5 + 3 clicks + (2 + 5 + 3) shifts = **15 actions**.
  (Fixes critique issue 3 — original used ACTION1 ×7 for column_a
  and ACTION1 ×9 for column_e, 8 actions longer than the minimal
  ACTION2 directions.)
  Note the ordering matters: pair 2 is finalised at offset 5
  (idx=1) BEFORE moving to offset 8, because moving the scan line
  re-reads pair 2 at the new offset and breaks its alignment
  unless its `position`-sum invariant happens to match the new
  offset's required sum, which it won't.

- **Difficulty justification:**
  - **(a) Random-resistance:** 5 columns × 12 positions × 3
    scan-line states + bound-pair invariants ≈ 12⁵ × 3 ≈
    750k joint configurations, of which only ~1 satisfies the
    target. A uniform random policy within the L3 step budget of
    100 has probability of order 100 / 750k ≈ 1.3 × 10⁻⁴, well
    within the §3.5 random-resistance threshold.
  - **(b) Human time:** ~3 minutes — discover ACTION5 by
    pressing every key after the first 30s of M1+M2 fail to make
    progress on pair 1 (because pair 1's target is impossible at
    the start scan line); see the scan line move; recognise that
    different scan-line positions enable different bound-pair
    targets; plan order pair 2 → ACTION5 → pair 1 → independent.
  - **(c) Planning depth — *post-discovery*:** Assume the player
    has fully understood click-to-select + ACTION1/2 shift +
    bound-pair coupling + ACTION5 scan-line cycle.
    - **Post-discovery decision space at level start:** 5
      ACTION6 candidates (one per column) + 1 ACTION5 = 6 valid
      first actions, *strictly greater than L2's 4*; after each
      first action the post-discovery branching factor is at
      least as large as L2's. The 5-column × 3-scan-line ×
      bound-pair-coupling search space is the largest at any
      level.
    - **Plausible-but-wrong post-discovery heuristic — "shift
      both bound pairs at the start scan line first, then move
      scan line for the unbound column":** A fully-informed
      player who has solved L2 will instinctively try to solve
      both bound pairs *first* at the start scan line before
      using ACTION5. This is "monotone progress on bound pairs"
      and it FAILS post-discovery: at offset 3 (start row), pair
      1's required sum (`k_a + k_b - 6 = -2 ≡ 10`) is not zero,
      so pair 1 is unreachable; pair 2's required sum
      (`k_c + k_d - 6 = 4`) is not zero, so pair 2 is
      unreachable. Even with full knowledge of what each action
      does, this heuristic plays itself into a state where no
      bound pair satisfies its target.
    - **Where the heuristic diverges from the witness, in 2-3
      sentences:** The witness diverges at action 1 — instead of
      attempting pair 1 or pair 2 immediately, the witness presses
      ACTION5 first to move the scan line to offset 5, where pair
      2 *is* solvable. The greedy heuristic loses because it
      ignores that the bound-pair invariant `pos_a + pos_b ≡ 0
      (mod 12)` constrains the *sum* of partner positions, and
      that this sum is comparable to `k_a + k_b - 2 × offset`;
      when this combination doesn't equal zero at the current
      offset, the bound pair is unsolvable at that offset. The
      heuristic only inspects per-column visible colours, not
      this hidden modular arithmetic, and so misses that the
      scan line *must* move at least once.
  - **(d) Step budget:** **100**. Generous over the 15-action
    witness (~6.6×) — covers two scan-line shifts, the ~6 wasted
    shifts a first-time player will spend exploring the bound-pair
    invariant before realising the scan line must move, and full
    recovery from any over-shift via the opposite arrow.

## 5. Action mapping

`available_actions = [1, 2, 5, 6]` — declared once globally on the
game class (engine sets `available_actions` at `__init__`, not per
level). 4 of the 7 slots used. **Per-level gating of ACTION5** is
done at runtime via `_get_valid_actions()` — when
`self._current_level_index < 2` (i.e. for L1 and L2), ACTION5 is
filtered out of the valid actions returned to the agent so the
scan-line shift mechanic is hidden until L3 introduces it. (This
is the cn04 / sp80 `_get_valid_actions` pattern. Fixes critique
issue 1 — original spec implied a per-level `available_actions`
which the engine doesn't support.)

| Action | Verb | Gating |
|---|---|---|
| ACTION1 | Shift active column up by 1 segment (`column.position` += 1 mod 12). If the active column is a bound-pair member, ALSO mutates its partner: partner's `position` -= 1 mod 12 in the same animation tick. | Only valid when a column is currently active (`active_column is not None`). If no column active, the action is filtered from `_get_valid_actions()` and is a no-op if forced. |
| ACTION2 | Shift active column down by 1 segment (`column.position` -= 1 mod 12). Mirror behaviour for bound-pair (partner +=1). | Only valid when a column is currently active. |
| ACTION5 | Advance scan-line cycle: `scan_line_idx = (scan_line_idx + 1) mod 3`. Updates the scan-line sprite's y-position to one of {22, 31, 40}. Re-evaluates the visible-segment formula for every column. | Filtered out of `_get_valid_actions()` for L1 and L2 (`_current_level_index < 2`); always valid in L3. |
| ACTION6 | Click anywhere; if the click cell falls inside a column's bounding box (rows 14..49, x in column's range), set that column as active and move the active-column-highlight strips to flank it. Clicking outside any column de-selects (clears `active_column`). | Always valid. |

ACTION3, ACTION4, ACTION7 are unused — keeping the action subset
minimal per checklist item 5 and tech-report § 9.

## 6. HUD and per-game state

**HUD widget:**
- `StepCounterHud(RenderableUserDisplay)` — draws a yellow-on-black
  depleting bar at row 0 reflecting `step_budget_remaining /
  step_budget`. Updated every action via the standard pattern
  (`tu93`, `cn04`, `sp80`).

**Per-game state (held on the `Qx7p` instance):**
- `self.active_column: Sprite | None` — currently selected column,
  or `None` when no column is active. Active column is visibly
  highlighted by two thin white vertical strips
  (`active_highlight_l`, `active_highlight_r`) flanking it on both
  sides; these strips are repositioned every selection. Persistent
  for as long as the column is active (per checklist item 19 — no
  hidden state).
- `self.bound_pairs: dict[str, str]` — maps each bound-pair column
  name to its partner's name. Initialised in `on_set_level`. Visual
  cue: ribbon sprite + endcap dots persistently rendered above the
  paired columns.
- `self.scan_line_idx: int` — index in {0, 1, 2}, only used in L3.
  Scan-line `y` is a function of this index. Visible cue: the
  scan_line sprite is repositioned each ACTION5; the cyclic
  position is implicit but readable from where the bar is on
  screen.
- `self.step_budget_remaining: int` — decremented per action.
- (No animation phase counter — shifts are instantaneous to the
  player; the rolled column pixels reflect the shift immediately
  in the same `step()` tick.)

## 7. Win condition

After every action, evaluate for each column:
```
visible_segment_idx = (column.position + offset(scan_line_idx)) % 12
visible_colour      = column.colours[visible_segment_idx]
target_colour       = target_patch[column].pixels[1, 2]
```
Where `offset(idx)` is computed once at level start as
`(scan_line_y_for_idx - column.y) // 3`. If for ALL columns
`visible_colour == target_colour`, call `self.next_level()`. The
final level's `next_level()` cascades to `self.win()` via the engine
default.

## 8. Lose condition

Single failure mode: the step counter reaches zero. When
`self.step_budget_remaining <= 0` after an action, call
`self.lose()`. There is no instant-fail collision, no soft-lock —
all shifts are reversible (via the partner action), so the player
can always recover from a wrong shift at the cost of two actions.

## 9. Novelty note

### Closest taxonomy entries

- **`lp85`** (button-permutation-puzzle) — flat 2D grid, click-only
  permutations applied to many cells at once via pre-baked
  permutation tables; goal = pieces over goal cells anywhere in
  grid. **qx7p distinguishing rule:** independent vertical bars
  with linear modular shifts (no permutation tables; no shared 2D
  grid of pieces); win is matched against a single horizontal
  scan-line row, not against arbitrary positional matching.
- **`vc33`** (row-slide-pull-tab) — clicking a tab on the edge of a
  row slides every stone in that row by one cell horizontally;
  goal is each stone over its same-coloured house slot.
  **qx7p distinguishing rule:** vertical (not horizontal) shifts;
  shifts a column's *colour-band stack*, not a row of pieces; win
  is row-pattern match at a scan line, not stone-to-house bijection.
- **`tr87`** (tape-rewrite-rule) — arrow keys cycle a card through
  a 7-glyph alphabet on a horizontal symbol tape against grammar
  rules. **qx7p distinguishing rule:** vertical band-stack with no
  rewrite-grammar overlay, no glyph alphabet, no premise-LHS / RHS
  rule pairing. Both have arrow-cycle verbs but the operands and
  goal are entirely different.
- **`dc22`** (colour-cycle-walk) — walking pawn steps onto trigger
  pads to cycle every wedge-block of that colour through a fixed
  state sequence. **qx7p distinguishing rule:** no avatar, no
  walking, no trigger pads, no global per-colour cycling — every
  shift is local to its column (or its rigid bound partner).
- **`cn04`** (rotate-translate-jigsaw) — click + arrow + ACTION5
  rotate verb on connector-snap pieces. **qx7p distinguishing
  rule:** no jigsaw connectors, no rotation; the verb is linear
  modular shift, not 90° rotation.

### Closest prior-games entries

- **`qz73`** (radial-cycle-lock) — rotate a single rotor of
  coloured tips around a central pivot and lock individual tips.
  **qx7p distinguishing rule:** linear (not radial) bars,
  independent (not single shared rotor), no per-tip locking;
  visually qz73 is radial pawns around a centre, qx7p is straight
  vertical bars.
- **`mr5q`** (polarity-attract-discharge) — click pawns to flip
  yang/yin, ACTION5 globally walks pawns toward nearest opposite.
  **qx7p distinguishing rule:** no pawns, no walking, no global
  attract step; the only "coupling" is per-bound-pair antisymmetric
  shift, which fires on the player's M1, not on a global step
  verb.
- **`m0r0`** (mirrored-quad-control) — four avatars walk in
  lockstep with mirrored axes per quadrant. **qx7p distinguishing
  rule:** no avatars walking on a maze; bound-pair coupling is
  per-pair (not per-quadrant) and applies to a 1D position state
  (not a 2D walking grid).
- **`vd3g`** (mound-marble-routing), **`kp9z`** (grain-accumulate),
  **`gv47`** (seed-grow-surround), **`vn8d`** (domino-cascade) —
  cellular-automaton / cascading propagation puzzles. **qx7p
  distinguishing rule:** zero propagation. Each shift mutates
  *only* the named column (and its rigid bound partner); no
  cascade, no grain flow, no flood fill, no domino chain.

### Negative-similarity-check (re-run on full spec, 8 dimensions)

Walked the 8 dimensions of `negative-similarity-check.md` against
each near-miss (lp85, vc33, tr87, dc22, qz73, mr5q, m0r0, vd3g,
kp9z, gv47, vn8d):

- **What is on the board:** vertical band-stack columns + scan
  line + target patches + bound-pair ribbon. Distinct from every
  prior — no prior renders vertical-band stacks.
- **What the player does:** click + arrow-shift band-stack;
  ACTION5 cycles scan line. Distinct verb.
- **What the level asks:** scan-line row equals target colour
  pattern. Distinct goal.
- **What kills:** step counter (universal — discounted).
- **Cast of supporting elements:** ribbon-linked pairs, movable
  scan line. Neither appears in any prior.
- **Visible visual signature:** tall thin vertical bars + horizontal
  scan-line + above-strip targets. Distinct from every prior
  inspected.
- **Pixel grain:** column bars rendered as 6-wide bands with 1-px
  borders, internal segment patterns of 3 rows each — internally
  detailful per checklist item 20.
- **Core dynamic:** "slide each band stack to bring the right
  segment to a fixed (or movable) window, with bound pairs and
  movable window adding composition". No prior centres this
  dynamic.

No single prior shares 3+ dimensions with qx7p. Negative-similarity
check passes.

`prior-games/index.md` is not empty (29 entries) — the priors-side
checks above are real, not vacuous.
