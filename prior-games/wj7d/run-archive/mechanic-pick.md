# Mechanic pick — wj7d

## Game ID
`wj7d` (4-char, lowercase alphanumeric, opaque, not in 25-ref, not in
`prior-games/index.md`, not in `prior-games/` directory; not a
recognisable English word).

## Mechanic family
`fold-crease-overlay`

## One-paragraph description
The playfield is a wide rectangle split into two halves by a single
white **crease line** running either horizontally or vertically. One
half is the **active half**, where a small inventory of coloured
**stamps** (each a small pixel-sprite with a distinctive internal
pattern) sits — the player can move the selected stamp around with
arrow keys. The other half is the **target half**, where a faint
**shadow pattern** is printed onto a darker background — the shadow
shows the target colour for each cell that must be covered. Pressing
ACTION5 (FOLD) reflects the currently-selected stamp across the
crease line: every coloured pixel of the stamp is mirror-projected
onto the target half and permanently laid down (the stamp itself is
consumed and disappears from the active half). Click (ACTION6)
selects which stamp is active. Once a movable crease is introduced,
the crease can be dragged along its perpendicular axis with
arrows-while-no-stamp-selected, AND the crease can be re-oriented
(H↔V) by clicking on the crease line itself; the active half always
stays on the same side relative to the crease. The level wins when
every shadow-target cell on the target half is covered by a
same-colour folded pixel and no stamp remains. The lose trigger is
the universal step-counter exhaustion.

## Mechanics layered across the 3 levels (preview for write_spec)

The base dynamic system at L1 already has TWO interlocking mechanics
(MOVE-stamp + FOLD-commit), so the +1-or-+2 inheritance rule is met
with new mechanics only at L2 and L3:

- **L1 — base system.** ONE stamp on the active half, fixed crease.
  Mechanics required by witness: (M1) **move stamp** with arrows on
  the active half + (M2) **FOLD-commit** with ACTION5. Tutorial:
  positioning matters because the fold reflects across the crease,
  so the stamp must sit at the mirror-image position of the target
  shadow before fold.
- **L2 — adds (M3) SELECT-among-stamps.** Multiple stamps live on
  the active half; ACTION6 click selects which is active. The
  witness must position-and-fold each stamp (each one consumed),
  and order matters because once a target cell is wrong-coloured
  by a fold the level is unrecoverable. M1 and M2 still required
  — the player must still move each selected stamp to its
  pre-fold position before pressing ACTION5.
- **L3 — adds (M4) MOVE-CREASE and (M5) RE-ORIENT-CREASE-H-or-V.**
  Multiple stamps; the crease itself can be slid (with arrows
  while no stamp is selected — empty-selection click toggles
  to crease-grab mode) and re-oriented (click directly on crease
  line). The witness must, for at least one stamp, move the
  crease and/or re-orient it BEFORE folding so the fold lands the
  stamp's mirror image where the shadow demands. M1, M2, M3 still
  required.

This satisfies the +1-or-+2 mechanic-inheritance rule
(`composition-and-tutorial.md` § No hidden mechanics): L1 has 2
required mechanics, L2 has 3 (= L1 + 1), L3 has 5 (= L2 + 2). Every
earlier-level mechanic remains required.

## Similarity-check vs the 25-game taxonomy

Walked the taxonomy. Family-level matches required a description-
level look at: `ar25` (shape-mirror-cover), `cn04` (nub-pair-glyph,
because of rotation/reflection visual flavour), `cd82` (orbit-fire-
paint, because of "fire commit a region of paint" verb shape),
`re86` (frame-paint-canvas, because of overlay-on-target),
`sb26` (tile-place-commit, because of place-then-commit pattern),
`pz4t`-adjacent jigsaws (placement + transform),
`lp85`/`vc33`/`qx7p` (slide-to-align), `ft09` (stamp).

Distinguishing rules per flagged near-miss:

- **ar25 (shape-mirror-cover).** ar25 has a stationary mirror line
  and a continuous, ever-present ghost-mirror of a single shape
  that slides as the player slides; the player wins by passing
  the ghost over every scattered dot before steps run out. The
  mirror is a *passive viewing aid* and the continuous ghost
  always exists. Fold-crease-overlay is the *opposite* in
  cardinality and cardinal verb: the mirror reflection is a
  one-shot DESTRUCTIVE COMMIT (ACTION5) that consumes the stamp
  and lays a permanent mirror image; there is no continuous
  ghost. The crease is also itself movable and re-orientable in
  L3 (ar25's mirror only translates with the shape, never
  re-orients). The player's mental model is "pre-position before
  commit, then the stamp is gone" rather than "slide the ghost
  over every dot".
- **cn04 (nub-pair-glyph).** cn04 has click-to-select then
  arrow-slide then ACTION5-rotates the selected piece; the
  rotation is in-place and 90°. wj7d's ACTION5 is mirror-
  reflection across a global crease that consumes the stamp; no
  in-place rotation. Win is shadow-coverage, not nub-kissing
  pairs.
- **cd82 (orbit-fire-paint).** cd82's ACTION5 fires paint from
  an orbital tank into an axial half or diagonal wedge of a
  fixed central canvas; multiple fires per level, paint colour
  picked from swatches. wj7d's ACTION5 reflects a *specific
  selected stamp* (with its own internal pixel pattern) across
  a crease and consumes it. The stamp's pattern is faithfully
  preserved through the reflection — there is no "fill a wedge
  in one colour" verb. The crease in wj7d is movable (L3); the
  cd82 canvas centre is fixed.
- **re86 (frame-paint-canvas).** re86 has hollow frame-shapes
  sliding to dye themselves on coloured zones, and ACTION5
  cycles which frame is active. wj7d uses ACTION6 click for
  selection, not ACTION5 cycling, and the verb is fold-once
  consume-stamp not slide-over-zone-to-dye.
- **sb26 (tile-place-commit).** sb26 places coloured tiles into
  slots and ACTION5 sends a marker walking left-to-right
  ticking off matches. wj7d does not place tiles into a tray;
  stamps already exist on the active half and are consumed by
  reflection. There is no marker-walk; the win is checked by
  a snapshot of target-half coverage after each fold.
- **lp85 / vc33 / qx7p (row/column shifts).** These slide whole
  rows/columns to align tokens to a target. wj7d does not
  translate the playfield contents; it reflects (mirror-flips)
  individual stamps across a crease. The crease moves in L3,
  but it does not shift coloured contents — it only re-defines
  the axis of reflection. The active half's stamps stay where
  they are until folded.
- **pz4t (anchor-pivot jigsaw).** pz4t tiles a connected dark
  region with multiple polyomino pieces; per-piece anchors are
  set by clicked-pixel; arrows reflect, ACTION5 rotates. wj7d
  does not tile a connected region (the target is a shadow
  pattern with possibly-disconnected target cells); reflection
  in wj7d is a global commit across one fixed crease line, not
  a per-piece reflection axis chosen by the player. wj7d
  consumes stamps via the FOLD verb, not by placement.
- **ft09 (stamp-3x3-paint).** ft09 taps an empty cell to stamp
  a 3×3 colour-pattern around it. wj7d does not stamp at an
  arbitrary cell — the stamp's destination is *determined* by
  the active stamp's current position reflected across the
  crease. The player chooses position-via-arrows, not
  position-via-click.

## Similarity-check vs `prior-games/index.md`

Walked all 36 prior-games rows + the in-flight `fb7t` (Phase-
Transition Matter, not yet indexed but in `prior-games/`). Family-
level keywords like "fold", "crease", "reflect", "mirror" appear
ZERO times across the priors corpus. The rough surface-feature
adjacents to consider:

- **bx84 (beam-mirror-reflect).** bx84 reflects an emitter's
  beam off click-placed mirror cells; the beam IS the action's
  effect every step. wj7d does not have a moving beam; the
  reflection axis is the crease (a static line per turn) and
  the reflected entity is the stamp itself, projected once per
  ACTION5. No emitter, no per-step beam propagation.
- **ar25 (taxonomy near-miss above)** — same distinguishing
  rule.
- **qz73 (radial-cycle-lock).** Rotation-flavoured but rotates
  a central rotor of tips; wj7d does not rotate, it reflects.
  Different verb.
- **pj7k (rolling-cube-face-paint).** A rolling cube whose
  faces deposit colour onto cells; transformation is per-roll.
  wj7d's transformation is mirror-flip not roll. The
  destination of pj7k is the cell beneath the cube; wj7d's
  destination is the mirror image of the source cell.
- **gv47 (seed-bloom).** Click coloured seeds to grow regions;
  surround a pip to dissolve. No reflection axis or fold. Not
  similar.
- **fb7t (Phase-Transition Matter, in-flight).** Read briefly:
  porous walls, solid/liquid/gas matter, avatar walks. No
  mirror or fold mechanic. Not similar.
- **lq5x (lantern-cone-illuminate).** Cone projection. Not a
  reflection or fold. Different.
- **ng52 (multiset-signature-classify).** Bin-classification.
  Different.
- **mr5q (polarity-attract-discharge).** Polarity flip + walk
  toward opposite. Not a reflection axis verb.
- **vd3g, ek73, jd4q, fz5j, kn58, wt39, zk9p, rk7x, gx7m,
  vp6h, kp9z, zd7m, lv4k, xn5p, qm4t, qn7w, zw91, pf3w, tg6w,
  tm5x, qx7p, kj82, nb6t, hr8q, kx14, qb84, kf42** — none
  involve mirror reflection across a movable axis as a
  discrete commit verb. Distinguishing rule for each: wj7d's
  core verb is ACTION5-FOLD = consume-stamp-by-mirror-across-
  crease, with the crease itself being a movable, re-orientable
  reflection axis. None of these priors share that combination.

No flagged similarity passes the (description-match + concrete-
distinguishing-rule) gate as REJECT. wj7d is novel by the positive
test.

## Negative-similarity-check (the seven-dimension overlap test)

Walked the seven dimensions of `negative-similarity-check.md` against
the closest visual-signature priors. Compared against:

- **ar25 (taxonomy)** — initial-frame: a single shape + a long
  mirror line + scattered dots on a mostly-empty grid. wj7d's
  initial-frame: multiple internally-patterned stamps on one
  half, a crease line, a shadow target pattern on the other
  half. Dimensions overlapping with ar25:
    1. What's on the board: ar25 = shape + mirror line + dots;
       wj7d = stamps + crease + shadow targets. Both have
       "an axis line + things to be reflected over it +
       targets". *Overlap: yes (1).*
    2. Player input: ar25 = arrows nudge shape-or-mirror; wj7d
       = arrows nudge stamp + ACTION5 commit-fold + ACTION6
       select. *Overlap: partial.* The verbs are different
       (continuous shape-slide vs. discrete commit-fold), but
       both ultimately use arrows on a moveable thing.
    3. What the level asks for: ar25 = cover scattered dots
       (with continuous ghost passes); wj7d = match shadow
       pattern (with discrete folds). *Overlap: yes (2).*
    4. Kills: step counter. *Overlap: yes (3).* (Universal —
       see cross-cut-frequencies.)
    5. Cast: ar25 = 1 shape + 1 mirror line + N dots; wj7d =
       N stamps + 1 crease + N shadow targets. Conceptually
       similar at coarse level (1 axis line + things-on-side-A
       + targets-on-side-B). *Overlap: borderline yes.*
    6. Visible visual signature (Principle 2): wj7d's palette
       will be DELIBERATELY DISTINCT from ar25's. ar25 uses
       neutrals + a few accent hues with a long mirror line.
       wj7d uses one neutral background per half (e.g., very-
       dark for active half, light-grey for target half),
       white crease, and rich pattern stamps with at least 4
       distinct hues. *Overlap: no.*
    7. Pixel grain (Principle 1): wj7d will use 8×8 stamps
       with internal pixel pattern (filled inner shape +
       border accent), not 1×1/2×2 tokens. ar25's pieces are
       small with limited internal detail. *Overlap: no.*
    8. Core dynamic (Principle 3): ar25's player thinks
       "slide-shape-or-mirror so the ghost ends up covering
       every dot" — a coverage-with-continuous-shadow problem.
       wj7d's player thinks "pre-arrange each stamp's
       position before its single irreversible fold, plan the
       crease changes between folds (L3)" — a discrete-commit-
       sequencing problem with consumed pieces. The mental
       model is fundamentally different: continuous tracing
       vs. permutation-with-commit. *Overlap: no.*

Counted: 3 same-dimensions (1, 3, 4) plus partial overlap on 2
and borderline on 5. Crucially the dimensions that the file
flags as the heaviest — 6, 7, 8 — all diverge. Per the rule of
thumb in `negative-similarity-check.md`, sharing on 1/3/4 alone
is acceptable when 6/7/8 diverge. **Pass.**

- **bx84 (prior — beam-mirror-reflect).** Initial-frame: an
  emitter pip + reflective tiles + path cells + a target. wj7d's
  initial-frame: 2-half playfield + crease + stamps with internal
  patterns + shadow target pattern. Visual signatures, palette,
  and core dynamic all diverge sharply (no emitter, no per-step
  beam, the active *thing* is a sprite-stamp with shape, not a
  ray of pixel-pulse). *No 3+ overlap.*
- **qz73 (prior — radial-cycle-lock).** A central rotor with
  tips + sockets. Visually a centred wheel. wj7d is a flat
  half-plane fold geometry. Core dynamic: rotation vs.
  reflection-and-consume. *No 3+ overlap.*

No prior reaches the 3-shared-dimensions reject threshold.

## Decision
**NOVEL.** Pick `wj7d` / fold-crease-overlay.
