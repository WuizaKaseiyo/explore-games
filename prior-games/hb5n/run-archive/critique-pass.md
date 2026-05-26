# Critique pass — hb5n (final, after revision #1)

Adversarial re-review of revised `mechanic-spec.md` after the
PIVOT-RESET substitution.

## Checklist items (1-22)

1. ✅ Palette 0..15 with `-1` transparent.
2. ✅ Universal scaffold structure described.
3. ✅ `available_actions=[1,2,3,4,5]` ⊂ [1..7].
4. ✅ Exactly 3 `Level` entries.
5. ✅ ID `hb5n` is 4-char lowercase alphanumeric, opaque, not in
   25 references nor in 81-entry index + 9 untracked recent priors.
6. ✅ Mechanics draw from geometry/topology + objectness priors.
7. ✅ No letters/digits/clipart/cultural conventions in sprites.
   Colours are abstract; magenta-cross pivot-reset pattern does
   not read as a glyph.
8. ✅ ≥ 2 distinct mechanics (4 total across L1/L2/L3).
9. ✅ L1 = base dynamic system (M1 walk + M2 rotate), reduced
   state, no on-screen text.
10. ✅ L2 and L3 each compose mechanics — each adds a new mechanic
    that interacts with prior ones in the witness.
11. ✅ +1 per level: L1=2, L2=3, L3=4. All prior mechanics carried
    forward and required by each level's witness.
12. ✅ **STRICT COUNTERFACTUAL NECESSITY** (the previously-failed
    item, now fixed):
    - L1 M1: required for translation; ACTION5 cannot translate.
    - L1 M2: required because target silhouette is at rotation
      270, distinct from starting rotation 0.
    - L2 M1, M2, M3: each strictly necessary (M3 because target
      has 4 cells, avatar starts with 3; M3-pickup at (4,2) is
      the unique 4th-cell source).
    - L3 M1, M2, M3: strictly necessary as in L2.
    - L3 M4 (pivot-reset): **STRICTLY NECESSARY by geometric
      argument**. The A-pivot 4-cell J's 4 rotations produce 4
      asymmetric J/L silhouettes — none of which is a T. The
      L3 target slot is a T-silhouette. Therefore the avatar
      cannot ever match the target at any A-pivot configuration.
      The only way to produce a T is to transfer the anchor to
      a different cell (via M4), giving access to B-pivot's
      rotation space — which DOES include a T (the rotation 90).
      The pivot-reset cell at (10, 10) is the unique trigger;
      no other in-level mechanic transfers the anchor. Therefore
      every winning sequence must consume the pivot-reset cell.
    - Per-mechanic table (one row per (mechanic, level)):

      | Level | Mechanic | Solvable without M? | Why not (concrete) |
      |---|---|---|---|
      | L1 | M1 walk | no | anchor must translate from (2,2) to (12,12); only ACTION1..4 translate |
      | L1 | M2 rotate | no | target silhouette at rotation 270; avatar starts at 0; only ACTION5 rotates |
      | L2 | M1 walk | no | anchor must translate from (2,2) to (12,12) |
      | L2 | M2 rotate | no | target at rotation 180; avatar starts at 0 |
      | L2 | M3 pickup | no | target has 4 cells; avatar has 3; pickup at (4,2) is the unique 4th-cell source |
      | L3 | M1 walk | no | anchor must translate from (3,3) to (12,12) (Manhattan 18) |
      | L3 | M2 rotate | no | B-pivot rotations 0, 180, 270 produce different T-orientations; only rot 90 in the B-pivot frame matches target cells {(12,12),(12,13),(11,12),(13,12)}; ACTION5 is the only rotation verb |
      | L3 | M3 pickup | no | target has 4 cells; avatar has 3 at start; pickup at (5,3) is unique |
      | L3 | M4 pivot-reset | no | A-pivot J's 4 silhouettes are all J/L-shaped (asymmetric, one "hook"); none is a T (a 3-in-line + perpendicular cell). Target is a T. Pivot-reset is the only mechanic that grants access to B-pivot's rotation space, which alone contains a T. |

    **Enumeration of plausible alternate strategies** (per
    checklist item 12's "verify by enumeration"):

    - *"Walk to target, then rotate to match"*: at any A-pivot
      rotation, avatar's silhouette is J/L. Target is T. Set
      mismatch. **Fails.** Independent verification: A-pivot
      cells span a 2×3 bounding box at rot 0/180 (cells in a
      2×3 region with one corner missing) and 3×2 at rot 90/270.
      Target is a 3×2 T (cells in 3 cols × 2 rows with one
      corner cell at (anchor.col, anchor.row+1) missing in the
      perpendicular direction). The cell-sets are not
      congruent.
    - *"Skip the pickup, rotate the 3-cell L to match"*: avatar
      remains 3-cell. Target has 4 cells. Set cardinality
      mismatch. **Fails.**
    - *"Consume pickup, skip pivot-reset, rotate to match"*:
      4-cell A-pivot J's 4 rotations don't include a T (per
      above). **Fails.**
    - *"Consume pivot-reset before pickup"*: at the moment of
      pivot-reset, the avatar is 3-cell L (no pickup yet). The
      cell "at relative offset (-1, 0)" in rotation 0 is B —
      which exists. The pivot transfers to B. But the avatar is
      still 3-cell. Pickup at (5, 3) is still required for the
      4th cell. After eventually consuming the pickup, the
      avatar is a B-pivot 4-cell shape. Cells (B-pivot rot 0):
      B(0,0), A(1,0), C(0,1) (the 3-cell L's C cell at rel
      (-1, 1) from old A is at rel (0, 1) from B in B-pivot),
      then D added at rel (-1, -1) from CURRENT anchor (B) at
      consumption — i.e. at rel (-1, -1) in B-pivot frame.
      Final B-pivot cells: B(0,0), A(1,0), C(0,1), D(-1,-1).
      That's an asymmetric L-shape, NOT a T! So
      pivot-reset-before-pickup ALSO doesn't yield a T. **Fails.**
    - *"Consume pickup AT the pivot-reset cell"*: pickup is at
      (5, 3); pivot-reset is at (10, 10). Different cells. Not
      possible to consume both with one step.

    All plausible alternates fail to produce the T-silhouette.
    The witness's specific order (consume pickup → walk to
    pivot-reset → consume pivot-reset → rotate to 90 in B-pivot
    frame → walk to target) is the unique winning shape modulo
    movement-order trivialities.

13. ✅ Mechanic family absent from taxonomy.
14. ✅ Mechanic family absent from prior-games index.
15. ✅ Concrete distinguishing rules vs cn04, ar25, tu93, xv4n,
    zw91, nz3v, pv5q, pz4t, nb6t, lt7m.
16. ✅ Win condition stated: set-equality `avatar_cells ==
    target_cells`.
17. ✅ Lose condition stated: step budget exhaustion. No
    unwinnable states (irreversibility argument holds — M3 and
    M4 consumption are required, never useless).
18. ✅ Per-level (a) random-resistance, (b) human-tractable, (c)
    planning depth, (d) step budget — all four bullets for L1,
    L2, L3 with concrete reasoning. L3's planning depth names a
    specific trivial heuristic ("rotate to match shape") and
    shows where it diverges from the witness (at pivot-reset
    discovery).
19. ✅ No hidden state without visible cue. Anchor cell visually
    distinguished (orange-centre vs maroon body-centre).
    Rotation manifests in the polyomino's orientation.
    Pickup-consumption visible (sprite disappears, new body
    cell appears). Pivot-reset visible (orange-centre marker
    migrates to the new anchor cell; pivot-reset sprite
    disappears).
20. ✅ Not low-resolution. 4×4 px cells with internal frame +
    centre patterns. Sprites differentiate by shape AND colour.
21. ✅ UI teaches. Anchor pivot is the orange-centred cell.
    Pickup is visually consumable (green-yellow distinctive
    pattern). Pivot-reset has a distinct magenta-cross pattern
    different from any wall, pickup, or target outline.
22. ✅ ACTION7 absent — slot 7 not in `available_actions`.

## Novelty (similarity-check.md re-run on the full spec)

### Against the 25 reference games

Closest near-misses (re-evaluated against the spec, not just the
mechanic name):

- **cn04**: jigsaw rotation via click-select; multi-piece flat
  board; connector-snap win. *Distinguishing rule on full spec*:
  hb5n has no click-select, single-piece avatar, maze walking,
  silhouette-match win. ✓
- **ar25**: reflection + click-select + arrows + rotate;
  reflector lines. *Distinguishing rule*: hb5n has no reflectors,
  no click-select, no mirror copies. ✓
- **tu93**: lockstep multi-agent maze; multi-cell pawns with
  fixed orientation; secondary species. *Distinguishing rule*:
  hb5n has single avatar, no lockstep, rotation-of-self verb. ✓
- No reference game has a rotation-pivot-transfer mechanic. ✓

### Against `prior-games/index.md` (81 entries) + 9 untracked recent priors

Closest near-misses:

- **xv4n** (cavity-nest-fit): click-lift + click-drop + ACTION5
  rotate-held. *Distinguishing rule*: no clicks, avatar IS the
  player, walks maze. ✓
- **zw91** (inflate-fit-burst): single avatar cycles 3 square
  sizes. *Distinguishing rule*: irregular polyomino (not
  square); ACTION5 rotates not resizes; growth from pickups not
  size-cycle. ✓
- **nz3v** (rotor-pivot-walk): 2×2 square avatar + separate
  rotating wedge. *Distinguishing rule*: irregular polyomino,
  rotation of avatar (not wedge), no wedge sprite. ✓
- **pv5q** (pivot-rod-swing): 1D rod attached to a stake;
  ACTION5 swaps stake. *Distinguishing rule*: 2D polyomino, no
  rod-and-stake metaphor, pivot transfer is a passive walked-on
  trigger (not an ACTION5 verb), pivot is internal to the
  avatar's own cells. ✓
- **pz4t** (anchor-pivot-place): click-set-anchor + arrow-reflect
  + rotate to tile a region. *Distinguishing rule*: no clicks,
  no tiling goal, avatar walks. ✓
- **nb6t** (hinge-chain-reach): hinged segment chain.
  *Distinguishing rule*: single rigid polyomino, no hinges. ✓
- **lt7m** (L-jump-tour-block): L-shaped knight jumps.
  *Distinguishing rule*: the L-shape is the body, not the move
  shape. ✓

Verdict: NOVEL against every taxonomy + prior entry.

## Negative-similarity-check.md (8 dimensions)

Walked against the 3 closest priors (xv4n, zw91, nz3v) and 2
closest references (cn04, ar25). No single entry overlaps on 3+
dimensions. Core dynamic ("thread a rigid polyomino through a
maze by walking + rotating + pivot-transferring") is fresh.

## Verdict

**PASS**. All 22 checklist items pass. Novelty NOVEL on both
positive and negative similarity checks.

Transition to `implement`.
