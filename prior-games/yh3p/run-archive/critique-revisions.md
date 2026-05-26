# critique-revisions — yh3p (round 1)

Walked checklist items 1-22 + similarity-check + negative-similarity-
check against `mechanic-spec.md`. Two blocking issues, two minor
improvements. Send back to `write_spec`.

## Issue 1 — Internally inconsistent L3 wall layout (BLOCKING)

- **Checklist item violated**: item 12 (strict counterfactual
  necessity) — the spec's necessity argument references one wall
  layout while the witness uses a different one, leaving the
  necessity claim untestable against a concrete geometry.
- **Offending spec section**: §4 → "Level 3 — system + 1 new
  mechanic" → "Layout" subsection.
- **Quoted contradiction**:
  - First (in the `**Layout**` bullet list):
    > *"Vertical wall: cells (8, 0), (8, 1), (8, 2), (8, 3), (8,
    > 4), (8, 5), (8, 6), (8, 7). Horizontal wall: cells (1, 8),
    > (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8). The corner
    > cell (8, 8) is OPEN."*
  - Second (mid-witness, under "Re-thinking the L-shape"):
    > *"Vertical wall: (8, 0) through (8, 6) — leaving (8, 7)
    > OPEN. Horizontal wall: (0, 8) through (6, 8) — leaving (7, 8)
    > OPEN. Cell (8, 8) is also open."*
  - The witness route uses the second (it walks through (8, 7) as
    a gap and through (7, 8) as a gap), so the layout subsection
    must be rewritten to match.
- **Concrete fix**: delete the first layout block. Replace with:
  - *Vertical wall*: 7 wall sprites at cells (8, 0), (8, 1), (8, 2),
    (8, 3), (8, 4), (8, 5), (8, 6). Cell (8, 7) is OPEN — this is
    the row-7 gap that lets a branch cross from the top-left
    quadrant into the top-right quadrant.
  - *Horizontal wall*: 7 wall sprites at cells (0, 8), (1, 8), (2,
    8), (3, 8), (4, 8), (5, 8), (6, 8). Cell (7, 8) is OPEN — this
    is the column-7 gap that lets a branch cross from the top-left
    into the bottom-left.
  - *Cell (8, 8) is also OPEN* and provides a diagonal corner the
    branches can use.
  - State the four quadrants explicitly: top-left = `{(x, y) : 0 ≤
    x ≤ 7 and 0 ≤ y ≤ 7}` minus the wall cells, top-right = `{x ≥
    9} ∪ {(8, y) : y ≥ 8}`, bottom-left = `{y ≥ 9} ∪ {(x, 8) : x ≥
    8}`, bottom-right = `{x ≥ 9 and y ≥ 9}`. (Or some clean
    partition that names which cells belong to which quadrant.)
  - Re-verify the witness routes against the cleaned-up layout
    (the witness already implicitly uses this layout, so this
    should be a textual fix, not a route change).
  - Re-verify the M2 necessity argument under this layout (see
    Issue 4 for a cleaner argument that bypasses the wall
    topology entirely).

## Issue 2 — `bud_notched` sprite reads as a letter (BLOCKING)

- **Checklist item violated**: item 7 — *"NO letters, NO
  digits-as-glyphs, NO real-world clipart, NO cultural conventions
  (see `forbidden-elements.md`)."*
- **Offending spec section**: §3 → `bud_notched` sprite definition.
- **Quoted spec**:
  > ```
  > pixels = [
  >     [-1, -1, -1, -1],   # ← notch (open) at top in rotation 0
  >     [12,  6,  6, 12],
  >     [12,  6,  6, 12],
  >     [12, 12, 12, 12],
  > ]
  > ```
- **Why this fails**: a 4×4 closed ring with one side transparent
  is *exactly* the silhouette of the letters **C**, **U**, **n**,
  or **⊃** depending on rotation. Rotation 0 = horseshoe-open-up
  (resembles "U"); rotation 90 = open-right (resembles "C");
  rotation 180 = open-down (resembles "n"); rotation 270 =
  open-left (resembles "⊃"). `forbidden-elements.md` rejects any
  sprite that "unambiguously reads as a digit/letter".
- **Concrete fix**: redesign `bud_notched` as a CLOSED ring with
  a directional asymmetric extension on the intake side, so the
  silhouette is not letter-shaped. Example pattern (rotation 0 =
  intake from the south, i.e., tip must approach moving NORTH /
  facing UP):

  ```
  pixels = [
      [-1, 12, 12, -1],
      [12,  6,  6, 12],
      [12,  6,  6, 12],
      [-1, 11, 11, -1],   # ← intake-side stamen extension
                          #   in palette 11 yellow, on the bottom
  ]
  ```

  - All four cardinal sides have closed orange-ring petals so the
    base shape never resembles C/U/n/⊃.
  - A 2-pixel-wide yellow "stamen" stub on the intake side
    indicates direction. Stamen on the bottom = intake from the
    south = tip facing UP.
  - At rotation 90 (intake from west, tip facing RIGHT) the
    stamen ends up on the LEFT of the rendered sprite; at 180 on
    the TOP; at 270 on the RIGHT.
  - Re-confirm `forbidden-elements.md` clearance: the resulting
    silhouette is a "flower-with-tab" shape, not a letter.
  - Update §3 the bud_notched pixel matrix and add a clarifying
    note that the intake direction is the side where the yellow
    stamen extends out of the ring. Update §4-L3 to refer to bud
    rotations using the stamen-direction convention (e.g., "Bud P
    at (12, 4), rotation 180 (stamen extends UP, i.e., intake
    from north, tip must approach moving DOWN, facing DOWN)").

  Alternative if the stamen tab is visually too small at 4×4 to
  read clearly: bump bud_notched to 6×6 with a 2×2 inner core
  and a 2-cell-long stamen extension. Author chooses; either
  satisfies the constraint.

## Issue 3 — Tip activity after auto-bloom on `bud_closed` is unspecified (MINOR)

- **Checklist item touched**: item 19 (no hidden state) — this is
  a state transition that affects what the player sees and what
  the engine does.
- **Offending spec section**: §4 → action mapping for ACTION1-4
  ("`bud_closed` cells are valid targets — entering auto-blooms
  them.") and §6 → state machine.
- **Quoted spec**:
  > *"On a `bud_closed` (already auto-bloomed by entry) → no-op."*
- **Why this matters**: when the tip enters a `bud_closed` cell,
  the cell's `bud_closed` sprite is replaced with `bloom`. Does
  the tip remain active (so the player can keep growing onward),
  or does it become dormant (forcing an ACTION6 click)? The L2
  witness uses ACTION6 to start the second branch from the root
  AFTER bud A's auto-bloom, but it doesn't say whether ACTION6
  is *required* (because tip went dormant) or merely *chosen*.
  This affects the M2 necessity argument at L2.
- **Concrete fix**: add to §4 / §6 / §5 the explicit rule that:
  *"Auto-blooming a `bud_closed` on M1 entry does NOT change the
  tip's active/dormant status. Tip remains active; the player may
  continue M1 growth from the bloomed cell. ACTION5 is what causes
  dormancy, and it only fires on `bud_notched` direction-match.
  Auto-bloom is a bonus side-effect of M1, not a tip-state change."*
- Recheck L2 M2 necessity under this rule: even if tip stays
  active after bud A's auto-bloom, the topology argument (wall
  column at x = 8 sealed except (8, 15); two buds in opposite
  regions) still forces a second branch via M2 because no single
  contiguous trail can cover both buds without backtracking
  through already-vine cells. So the argument is unchanged. State
  this clearly in the L2 mechanic-necessity row.

## Issue 4 — Simplify L3 M2 necessity using the dormancy-after-bloom rule (MINOR)

- **Checklist item touched**: item 12 (strict counterfactual
  necessity) — the current argument is correct but more involved
  than necessary, and it leans on the contested L3 wall layout
  (see Issue 1).
- **Offending spec section**: §4 → "Level 3" → "Necessity per
  mechanic" → M2 row.
- **Current argument summary**: "regions separated by L-walls; only
  one crossing per region pair; no single contiguous branch can
  cover all 3 buds with correct facing".
- **Concrete fix**: lead with the dormancy argument, append the
  topology argument as supporting weight:
  - *"At L3 every successful bloom-commit (M3) sets the tip
    dormant. The only way to re-activate the tip is M2 (ACTION6
    click on a vine cell). With three `bud_notched` targets, a
    successful run requires at least three bloom-commits, and
    therefore at least two M2 invocations between them. Without
    M2, after the first successful bloom the tip is dormant
    forever and the remaining two buds are unreachable. Even
    setting the dormancy aside, the L-walled topology (see
    Layout) admits no single contiguous branch from the root
    that arrives at all three buds with the correct intake
    direction — see the witness §c and the alternate-strategy
    enumeration §d."*
- This refactoring makes the M2 necessity argument robust to the
  L3 wall layout's detailed cell-by-cell partitioning (Issue 1),
  since the dormancy argument depends on M3's behaviour, not on
  the walls.

## Issue 5 — L1 frame visual sparseness (BORDERLINE; not blocking)

- **Checklist item touched**: item 20 (low-resolution rendering) —
  qualitative test.
- **Spec position**: L1 is one root sprite (8×8) + one bud (4×4) +
  tip overlay on a 64×64 light-grey background. No walls, no
  decorative scenery. Most of the rendered frame is empty
  background.
- **Why this is borderline**: the reference game `wa30` has a
  similarly-sparse L1 (light-grey background + 5-7 small colored
  squares). The 25-game reference set permits this aesthetic. So
  per `negative-similarity-check.md` principle 1 ("avoid having
  just a few big blocks moving around on an empty field"), yh3p's
  4×4 sprites with internal palette pattern are richer than the
  cautionary kf42→vh68 case but still on the sparse end.
- **Concrete suggestion** (not a hard requirement):
  - Add a subtle background pattern at the playfield edges (a
    `soil_border` decorative sprite that frames the grid in a
    different palette) for visual richness — non-collidable,
    non-mechanic, just texture.
  - Alternatively, scatter 3-5 non-collidable decorative pebbles
    or moss-tufts on each level's open ground. Tag them
    `decoration` and skip them in `_check_win` / collision logic.
    Distinct from gameplay sprites by palette (use lighter grey
    or off-white) and shape (tiny 1-2 pixel speckles).
  - Flagging only — `wa30` has shipped with similar sparseness, so
    this is preference, not regulation.

## Other checklist items — all PASS

| # | Item | Verdict |
|---|---|---|
| 1 | Palette values 0..15 (and -1 transparent) | ✅ uses {2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14}; `-1` for transparent |
| 2 | Universal scaffold structure | ✅ imports → sprites → levels → constants → HUD → game class |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[1, 2, 3, 4, 5, 6]` |
| 4 | EXACTLY 3 levels | ✅ L1, L2, L3 |
| 5 | 4-char ID, opaque, not in reserved/index | ✅ `yh3p` |
| 6 | Mechanics from core priors | ✅ objectness + topology + light geometry |
| 7 | No letters/digits/clipart/cultural | ⚠️ Issue 2 above |
| 8 | ≥ 2 mechanics | ✅ M1 + M2 + M3 = 3 |
| 9 | L1 tutorial, base system, no on-screen text | ✅ |
| 10 | L2/L3 increase difficulty by composition | ✅ each adds a verb that interacts with prior verbs |
| 11 | Mechanic inheritance + 1-or-+2 rule | ✅ L1=1, L2=2 (+1), L3=3 (+1); all carried |
| 12 | Strict counterfactual necessity table + enumeration | ⚠️ Issues 1, 4 above |
| 13 | Mechanic family absent from taxonomy | ✅ no name match; descriptions distinguished |
| 14 | Mechanic family absent from prior-games index | ✅ 66 priors checked |
| 15 | Concrete distinguishing rule for similar-sounding | ✅ stated for each near-miss |
| 16 | Win condition stated | ✅ `len(buds) == 0` → `next_level()` |
| 17 | Lose condition stated | ✅ `step_bar.current_steps <= 0` → `lose()` |
| 18 | Difficulty floor + ceiling per `difficulty-rules.md` | ✅ all 4 bullets per level |
| 19 | No hidden state | ✅ visibility-cue table provided |
| 20 | Don't generate low-resolution game | ⚠ Issue 5 (borderline) |
| 21 | UI to teach (sprite ≈ role; identical-visual ≈ shared role) | ✅ subject to Issue 2 fix |
| 22 | ACTION7 strict-undo or absent | ✅ omitted |

## Novelty re-check on the full spec

Re-walked `similarity-check.md` against the fleshed-out L1-L3 (not
just the family-name) — no drift detected. The L3 mechanic
"directional bloom-commit" is genuinely novel; no taxonomy or
prior-games entry uses an "approach-direction-must-match-target-
notch" rule. Re-walked `negative-similarity-check.md` 8 dimensions:
maximum overlap with any single prior remains 2 dimensions
(walk + step-counter, both partial). Below the 3-dimension reject
threshold. ✅ NOVEL.

## Verdict

**REJECT — go back to `write_spec` to address Issues 1, 2, and
note Issues 3, 4 as worthwhile additions.** Issue 5 is a soft
suggestion only. Visit count for `critique_spec` after this entry:
1; 9 entries remain before the cap.
