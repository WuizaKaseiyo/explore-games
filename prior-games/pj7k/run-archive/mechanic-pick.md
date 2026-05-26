# mechanic-pick — pj7k

## Game ID
`pj7k` — 4 chars, lowercase alphanumeric, not English, verified not in
the 25 reference reserved set and not in `prior-games/index.md` (which
contains 8 entries: kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52).

## Run input
Autonomous (no seed provided).

## Mechanic family
`rolling-cube-face-paint`

## One-paragraph description
A single solid 5×5 cube-piece sits on a small grid of empty cells. The
cube has four "side" faces, plus a top and a bottom; each face carries
a distinct palette colour and that colour is rendered as the currently-
visible top face on the cube sprite. ACTION1-4 rolls the cube one cell
in that direction — rolling a cube physically swaps which face is on
top: rolling north makes the old front-face become the top, rolling
east makes the old left-face become the top, and so on. Whenever the
cube finishes a roll into a new cell, the colour that ended up on the
**bottom** is stamped onto that cell's underlying tile. The level
contains tinted "target" tiles whose required colour is shown by a
small inset ring of that colour; the level is solved when every target
tile has been painted with its required colour. The puzzle is therefore
"plan a path through the grid such that, at every target cell, the
cube's bottom-face colour coincides with the target's required colour".
Core knowledge priors used: **objectness** (the cube is a single
persistent entity); **basic geometry/topology** (face-rotation under
rolling is a discrete subgroup of SO(3)); **basic physics** (rolling
without slipping). The cube's current top-face colour is always
visible, so the player can read the future bottom-face implicitly by
mentally rolling. Visual signature: one bold faceted cube on a
warm-cream playfield with a small set of target rings — distinct from
every prior's signature (paired pawns, lattices, fluid surfaces, etc.)
and from every reference game's signature.

## Per-level mechanic plan (sketch — full spec in next state)

- **L1 — base "rolling-paint" verb.** ACTION1-4 only. Tutorial: 4-5
  empty cells and 1-2 target tiles in a row. The witness must roll
  the cube along a path that lands the right face on the bottom at
  the right cell. Mechanics required by L1 witness: {rolling-paint}.
  Count = 1.
- **L2 — adds in-place TWIST (ACTION5).** ACTION5 rotates the cube
  90° about its vertical axis, cycling the 4 side-faces (top and
  bottom unchanged) without moving. No paint deposited on twist.
  Witness must use rolling AND twist: layouts where rolling alone
  cannot align the right face under the right target without a
  twist somewhere mid-path. Mechanics required by L2 witness:
  {rolling-paint, twist}. Count = 2.
- **L3 — adds COLOUR-GATES.** Some grid cells are gates of a specific
  colour; the cube can only roll into a gate cell if its current
  **bottom**-face matches the gate's colour. The witness for L3
  needs all three mechanics — rolling-paint to cover targets,
  twist to choose the bottom-face entering each gate, and gate-
  passage as a topological constraint that orders moves
  non-commutatively. Mechanics required by L3 witness:
  {rolling-paint, twist, colour-gate-passage}. Count = 3.

The L1→L2→L3 mechanic count rises by exactly one per level and every
earlier mechanic remains required.

## Similarity check (positive — `mechanic-novelty/similarity-check.md`)

Comparing the candidate's family `rolling-cube-face-paint` against the
25 taxonomy rows by family-level and description-level checks:

- **ls20 (cycler-attribute-match)** — near-miss on
  description-level: both involve an "avatar with cyclable attributes
  (shape/colour/rotation in ls20; face-orientation here) that must
  match per-cell goals". **Distinguishing rule**: ls20's cycle is
  triggered by stepping on dedicated cycler-tile sprites
  (`ttfwljgohq`, `soyhouuebz`, `rhsxkxzdjz`), and the player chooses
  WHICH attribute to cycle by stepping on the corresponding tile.
  In pj7k there are NO cycler tiles — the face-cycle is an
  unconditional consequence of the rolling physics, deterministic
  from the move-direction, and the player cannot decouple
  "movement" from "face-cycle". The mental model differs:
  ls20 = "route via cyclers to reach pellet with right state",
  pj7k = "every move re-orders the cube faces; sequence the moves
  so the right face lands at the right place". Concrete code
  consequence: ls20 stores three independent indices and a
  pellet-match predicate over `(shape, colour, rot)`; pj7k stores
  a 6-tuple of face colours plus an orientation, and the rolling
  function permutes the tuple deterministically.
- **re86 (flood-fill-multi-canvas)** — near-miss: marker walks and
  paints a target canvas. **Distinguishing rule**: re86's marker
  has ONE paint colour determined by sprite identity (constant for
  the whole level for that marker); pj7k's deposited colour is a
  function of the move-history (which face has been rolled to the
  bottom). The "what colour just got painted?" question for re86
  is "look at the active marker's pixels"; for pj7k it is "trace
  the roll sequence from the cube's initial orientation". This
  forces a path-dependent reasoning chain re86 does not impose.
- **cn04 (rotate-translate-jigsaw)** — near-miss: ACTION5 rotates
  a selected piece 90°. **Distinguishing rule**: cn04's rotation is
  a 2D in-plane rotation of a flat sprite that does not change any
  pixel's identity (the sprite is just transposed). pj7k's rolling
  is a 3D-rotation projection and changes which colour is
  currently visible — different geometric primitive, different
  consequence on play. Also cn04 has a click-to-select model with
  multiple movable pieces; pj7k has exactly one cube and no click
  needed for L1 / L2.
- **ka59 (sokoban-explode-chase)**, **wa30 (carry-pickup-drop)** —
  cardinal-motion games that move a single avatar. **Distinguishing
  rule**: neither has any face/orientation state on the moved
  entity; ka59 slides a flat block and detonates triggers; wa30
  carries passengers. pj7k's avatar carries IMPLICIT state (its
  current face arrangement) that no other taxonomy game tracks.
- All other taxonomy entries (ar25, bp35, cd82, dc22, ft09, g50t,
  lf52, lp85, m0r0, r11l, s5i5, sb26, sc25, sk48, sp80, su15,
  tn36, tr87, tu93, vc33) — no family-level overlap.

Comparing the candidate against `prior-games/index.md` (8 entries):

- **kf42 (tether-pawn-cycle)** — no overlap (no pair, no tether,
  no per-pad colour-set).
- **qz73 (radial-cycle-lock)** — no overlap (no rotor, no radial
  layout; qz73 has multiple lockable tips, pj7k has one cube).
- **kx14 (tide-tilt-buoyant)** — no overlap (no fluid surface).
- **qb84 (bead-lift-swap)** — no overlap (no chain navigation, no
  swap verb).
- **lq5x (lantern-cone-illuminate)** — no overlap (no projected
  cone, no lighting model).
- **gv47 (seed-grow-surround-dissolve)** — no overlap (no region-
  growing, no dissolve).
- **hr8q (pair-blend-recipe)** — no overlap (no recipe widget).
- **ng52 (multiset-signature-classify)** — no overlap (no
  classification bins).

No prior is family-level or description-level matched. No
distinguishing-rule paragraph required for any prior.

## Negative similarity check (`mechanic-novelty/negative-similarity-check.md`)

Walking the eight dimensions against each prior's level_1.png (sampled
in `study-notes.md`):

| Dim | What pj7k has | Most-overlapping prior | Shared? |
|---|---|---|---|
| 1. What is on the board | one bold cube + target rings + walls | none — every prior has multi-piece composition | No |
| 2. Player physical input | ACTION1-4 rolls; ACTION5 twist (L2+) | kf42 / qb84 use arrows; lq5x uses arrows. Shared: cardinal motion. | Partial (cardinal motion is generic, not specific) |
| 3. What the level asks for | paint every target's required colour | re86 (paint canvas), gv47 (paint region) — but among PRIORS, only gv47 is paint-ish | No (gv47 paints regions by surrounding pips, not depositing per-cell) |
| 4. What kills the player | step counter (universal across all 25 + 8 priors) | all | Universal — does not count |
| 5. Cast of supporting elements | the cube + target rings + walls + (L3) colour-gates | none of the priors uses colour-gates or per-cell-colour-deposit | No |
| 6. Visible visual signature | warm-cream background, bold faceted cube, small target rings | priors are dominantly grey/dark backgrounds with small geometric pieces | DIVERGENT — chose warm-cream specifically per Principle 2 |
| 7. Pixel grain of primary sprite | a 5×5 multi-coloured faceted cube | priors mostly use 1×1, 2×2, or 3×3 plain rectangles or simple plus/dot shapes | DIVERGENT |
| 8. Core dynamic | "what mental work is the player doing?" — *plan a path through cells such that the deterministic face-permutation under that path produces the right colour at every target cell* | no prior couples movement direction with sprite-attribute permutation; lq5x rotates a directional cone but does not paint | DIVERGENT |

No single prior overlaps on 3 or more dimensions. The candidate
diverges on dimensions 1, 5, 6, 7, 8 against every prior — the
named-principle dimensions (6, 7, 8) all show divergence.

## Verdict
**NOVEL.** Cleared positive similarity-check and negative similarity-
check against the 25 reference games and the 8 prior-games entries.
Proceed to `write_spec`.

## Cousin in pre-existing video games (manual axis 1)
Rolling-cube/dice-rolling puzzles do exist as a recognised puzzle
sub-genre (commercial examples include "Bloxorz" with a 1×1×2 brick
and various "color cube" mobile titles). pj7k narrows to a 1×1×1 cube
with face-as-paint-stamp — the painting mechanic is not, as far as
the agent knows, a dominant pattern in that sub-genre. Flagged for
the human reviewer; the harness cannot enforce axis 1 automatically.
