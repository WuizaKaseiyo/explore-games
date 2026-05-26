# Mechanic pick — pz4t

## 4-character ID

`pz4t`

- 4 chars lowercase alphanumeric ✓; not an English word ✓.
- Not in 25 reserved ✓; not in priors (kf42 qz73 kx14 qb84 lq5x gv47
  hr8q ng52 pj7k vn4j) ✓.

## Mechanic family tag

`anchor-pivot-place`

## One-paragraph mechanic description

The screen is split between a **board** region (rows 0..H_b-1) and a
**palette** region (rows H_b..H-1) below it. Each level seats one or
more **components** (multi-cell coloured sprites of distinctive
shape) in the palette region, plus one or more **target shadows**
(same shape, dimmer-colour cells) on the board showing where each
component must land. The player has a single primary verb:
**ACTION6 click**, which behaves as a two-phase pick-and-place. In
the *unheld* phase, clicking a cell occupied by a component picks
it up and records the *anchor offset* — the (col, row) of the
clicked pixel relative to the component's bounding-box top-left.
In the *held* phase, clicking any cell on the board places the
held component such that the anchor cell aligns with the clicked
cell (i.e. the component's bbox top-left lands at click − anchor).
Once placed on the board, the component can be picked back up by
clicking it again (anchor recomputed from the new click). At L2,
**ACTION5 rotate** rotates the held component 90° clockwise; the
anchor follows the rotation so the click-pixel-on-component still
points to the same physical pixel after rotation. At L3,
**ACTION7 flip** mirrors the held component horizontally; the
anchor mirrors with it. The level wins when every component is at
its target position; the only failure mode is the per-level step
counter exhausting.

## Action subset

`available_actions = [5, 6, 7]`

- ACTION5 = rotate held 90° CW (no-op if nothing held).
- ACTION6 = click pick-up-or-place, two-phase.
- ACTION7 = flip held horizontally (no-op if nothing held).

The distinctive verb lives on **ACTION6** — the pick-with-anchor
+ place-by-anchor pair. ACTION5 / ACTION7 are mechanic extensions
introduced at L2 and L3.

## Visual signature

- **Background**: palette 2 (light-grey).
- **Letterbox**: palette 4 (off-black).
- **Components**: solid coloured shapes — palette 8 (red), 11
  (yellow), 14 (green), 6 (magenta).
- **Target shadows**: dimmer ring-outlines in same hue, palette
  13 (maroon for red), 12 (orange for yellow), 7 (pink for
  magenta), with 10 (light-blue) outlining green. (Actually I'll
  use a single shadow palette to keep it simple — palette 3
  mid-grey-darker outline that visually reads as "slot shape".)
- **Step counter HUD** at row 63.
- **Held-component highlight**: a small off-white 1×1 anchor
  marker rendered at the held component's anchor cell.

## Similarity check (taxonomy + priors)

### Closest taxonomy entries:
- `cn04 nub-pair-glyph`: click-to-select + arrow-slide + ACTION5
  rotate. Rule: cn04 SLIDES the selected piece by 1 cell per
  arrow press; pz4t does not slide — placement is a single-action
  click that translates the piece to anchor-aligned position.
  cn04 has no anchor concept (selection just attaches arrows to
  the piece); pz4t's anchor is the central novelty.
- `lp85 row-col-shift-grid`: click pull-tabs to shift rows /
  columns. Different verb; no piece pickup.
- `sb26 tile-place-commit`: click tile then click slot to drop.
  Closest in spirit. Distinguishing rule: sb26's click sequence
  is FIXED-SLOT placement (each tile lands at a discrete slot
  index, no anchor offset; the slot decides where every cell of
  the tile goes). pz4t's placement is FREE-PIXEL placement (any
  pixel of the bbox can be the anchor; placement is a 2-D
  translation by `click - anchor`). sb26 has no rotation, no
  flip, no anchor concept.

### Closest prior entries:
- `ng52 multiset-signature-classify`: click objects into bins +
  ACTION5 commit. Rule: ng52 partitions a pool into bins by
  multiset signature; pz4t is shape-fit by anchor-aligned
  placement — different core dynamic. ng52 has no rotation, no
  flip, no anchor pixel.
- `hr8q pair-blend-recipe`: click ingredients to fill formula
  slots. Non-spatial; pz4t is spatial. Different.
- All other priors (kf42 tether, qz73 dial, kx14 fluid, qb84
  bead, lq5x cone, gv47 region-grow, pj7k cube, vn4j topple)
  lack anchor-pivot placement.

### Negative-similarity (8 dimensions vs each prior):
None reach 3+ on the named principles (palette diversity,
pixel grain, core dynamic). Component sprites are multi-cell L-
/ Z- / bar shapes against grey background — distinct grain from
priors' 1×1 pawns / bead-dots / canvas-grids.

## Verdict

NOVEL. Proceed to write_spec with ID `pz4t`, family
`anchor-pivot-place`, action subset [5, 6, 7].
