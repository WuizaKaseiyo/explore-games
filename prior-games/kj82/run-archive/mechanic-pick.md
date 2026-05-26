# Mechanic pick

## Game ID

**`kj82`**

Verified opaque: not an English word; not in the 25 reserved
reference IDs (`ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85
ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93
vc33 wa30`); not in `prior-games/index.md` (which contains 29 IDs:
`bx84 ek73 fz5j gv47 gx7m hr8q jd4q kf42 kn58 kp9z kx14 lq5x lv4k
mr5q ng52 pf3w pj7k pz4t qb84 qz73 rk7x tg6w vd3g vn8d vp6h wt39
xn5p zd7m zk9p`).

## Mechanic family tag

`plank-pivot-walk`

## One-paragraph description

Each level shows several long rectangular **plank** sprites lying
flat on a floor, plus a tiny **pawn** avatar standing on one of
them and a small **goal tile** in some other cell. Each plank is
permanently pinned at one end by a circular **anchor joint** (a
ball-and-socket fixture rendered as a small ring at the plank's
tip); the plank cannot translate. The pawn (ACTION1-4) walks one
cell per arrow-press but can only step onto cells covered by a
plank, transferring between planks at cells of overlap. ACTION6
clicks a plank to make it the **active** plank (highlighted by
its anchor ring brightening); ACTION5 then **pivots the active
plank 90° clockwise around its anchor end**, sweeping its tip
across a quarter-arc of cells over a short visible animation. The
sweep can fail (no rotation, plank stays put) if any "post"
obstacle blocks the arc. The goal: walk the pawn from its
starting plank onto the goal tile by orchestrating plank
rotations to bridge between planks.

The dynamic asks the player to think two-dimensionally about
arc-sweeps (where will tip-end be after 1 / 2 / 3 rotations) and
about the temporal ordering of "rotate first then walk" vs "walk
first then rotate", because some level configurations make planks
become unrotatable once walked on (introduced as a third mechanic
in L3).

## Core-knowledge priors used

- **Objectness**: plank is a coherent persistent rigid body.
- **Basic geometry & topology**: rotation around a fixed pivot
  point; arc geometry; connectivity of plank cells determines
  which cells are walkable.
- **Basic physics**: pivot mechanics; obstacle-blocking; "stuck"
  state when a plank has been walked on.

(Three of the four §3.4 priors. No agentness — no NPC.)

## Action space

`available_actions = [1, 2, 3, 4, 5, 6]`

| Action | Verb |
|---|---|
| ACTION1-4 | Step pawn one cell up/down/left/right (only onto plank cells). |
| ACTION5 | Pivot the active plank 90° clockwise around its anchor end (animated arc sweep). |
| ACTION6 | Click a plank to set it active (or click the active one to deselect). |

ACTION7 (undo) is **not** used — keep action space minimal and
consistent with most reference games (only 6/25 use undo; this
class of puzzle does not need it because rotations are reversible
by 3 further rotations).

## Similarity-check (per `mechanic-novelty/similarity-check.md`)

### Family-level: closest taxonomy entries

| Ref | Family | Family-match? | Description-match? |
|---|---|---|---|
| `cn04` | nub-pair-glyph (rotate-translate-jigsaw) | yes (rotate verb shared) | NO (see below) |
| `pz4t` (prior, also "anchor-pivot" in name) | anchor-pivot-place | yes (anchor + pivot shared) | NO (see below) |
| `wt39` (prior) | glide-deflect-thaw | no (sliding ≠ rotating; pawn path ≠ plank rotation) | n/a |
| `bx84` (prior) | beam-mirror-reflect | no (no beam) | n/a |
| `pj7k` (prior) | rolling-cube-face-paint | no (no cube; pawn does not roll, walks discrete cells) | n/a |
| `vp6h` (prior) | shadow-cast-collect | no (no shadow projection) | n/a |
| `xn5p` (prior) | chamber-stamp-partition | no (no wall stamping; planks are pre-placed) | n/a |

### Description-level distinguishing rules (per flagged row)

#### vs. `cn04` (rotate-translate-jigsaw)

`cn04`: the player clicks a jigsaw piece, slides it with arrow keys, and presses ACTION5 to **rotate the piece 90° around the piece's geometric centre**. The piece's centre stays put; only the pixel layout rotates. The win condition is "every '8' connector pixel coincides with another piece's '8' connector pixel".

`kj82`: rotation is **around a level-author-fixed anchor at one end of the plank**, NOT around the plank's centre. The plank's tip sweeps across a quarter-arc of distinct cells; no cell that the plank covered before rotation will still be covered after, except the anchor cell itself. Planks have no translation verb at all (arrows control the **pawn avatar**, not the plank). The win condition is "the pawn stands on the goal tile" — about avatar path-finding, not about pixel-pattern coincidence between pieces.

Concrete distinguishing rule: **cn04's ACTION5 is in-place rotation around piece centre and never changes which cells the piece occupies (only orientation); kj82's ACTION5 is end-pinned rotation around a fixed anchor and changes which cells the plank occupies entirely.** Plus cn04 has no avatar-walking verb; kj82's primary verb is walking the avatar across planks.

#### vs. `pz4t` (anchor-pivot-place)

`pz4t`: the player clicks a pixel on a coloured polyomino component to set the **placement anchor**, then uses arrows to **reflect** the component about that anchor and ACTION5 to **rotate** the component. The goal is to **tile a single connected dark-grey region** so every cell of the region is covered by exactly one component.

`kj82`: planks are **pinned in place** (anchor is level-author-chosen, not user-chosen); the user cannot translate them. Arrows do not reflect the plank — arrows step the **pawn avatar**. There is no tiling goal; the goal is path-walking.

Concrete distinguishing rule: **pz4t is a tiling puzzle where the player places, rotates, and reflects movable polyomino pieces to fully cover a target region; kj82 is a path-walking puzzle where pinned planks rotate about fixed anchors and the player has a separate avatar that walks plank cells.** The verb sets are disjoint apart from "rotate".

#### vs. taxonomy & priors not flagged but worth checking

- `wt39` (glide-deflect-thaw): pawn glides until wall and is deflected by bumpers; **the pawn moves continuously by physics**. kj82's pawn moves cell-by-cell on plank surfaces; planks themselves are the rotating mechanic. Different motion model entirely.
- `pj7k` (rolling-cube-face-paint): single coloured-faced cube rolls through cells; each roll permutes its faces. kj82 has **no cube**, no face-permutation; the pawn is a tiny avatar that walks, and the rotating things are the planks (not the avatar).
- `bx84` (beam-mirror-reflect): emitter shoots a coloured beam through mirrors. kj82 has **no beam, no projectile**; the rotation moves a physical walkable platform.
- `xn5p` (chamber-stamp-partition): pawn walks chamber and stamps walls. kj82 does **not stamp, place, or modify walls**; planks are pre-placed and immobile in translation, only rotating.

## Negative-similarity check (per `negative-similarity-check.md`)

Walked the eight dimensions against the closest single prior, `pz4t`:

| Dim | pz4t | kj82 | Shared? |
|---|---|---|---|
| 1. What is on the board | a connected dark-grey region + several coloured polyomino components ready to place | several long plank sprites pinned at one end + a tiny pawn + a goal tile | no |
| 2. What player physically does | clicks pixels on components, reflects (arrows) and rotates (ACTION5) to tile the region | walks an avatar (arrows), clicks a plank (ACTION6), pivots active plank around its anchor (ACTION5) | no — verb sets differ |
| 3. What level is asking for | tile every cell of the region | walk pawn from start to goal cell | no |
| 4. What kills player | step budget | step budget | yes (universal) |
| 5. Cast of supporting elements | dark-grey region, coloured polyomino components, anchor pixel | planks, anchor joints, pawn avatar, goal tile, posts (L2), sticky-cells (L3) | no |
| 6. Visible visual signature | dark-grey region with coloured polyomino tiles | light pastel field with bright wood-toned planks, dark anchor rings, small pawn | no (palette deliberately diverged) |
| 7. Pixel grain of primary sprites | polyomino components (multi-pixel solid shapes) | long thin planks (1×6 to 1×10 strips with end-decoration), 3×3 pawn with internal pattern, 5×5 anchor ring | no |
| 8. Core dynamic | spatial tiling (place + transform pieces to cover region) | path-walking through dynamically-orchestrated platform rotations | no |

Shared dimension count: 1 (universal step budget). Threshold for rejection is "shares 3+ on a single prior, with weight on dims 6/7/8". **Pass.**

Walked also against `cn04` (the other near-miss):

| Dim | cn04 | kj82 | Shared? |
|---|---|---|---|
| 1. board | jigsaw pieces with green-coloured nub connectors | planks + pawn + goal | no |
| 2. action | click + arrows to slide piece + ACTION5 to rotate piece | click + arrows to walk pawn + ACTION5 to rotate plank | partial — same buttons but different referents (player ↔ piece in cn04 vs avatar ↔ avatar+piece in kj82) |
| 3. asking | match all '8' nub pixels between pieces | walk pawn to goal cell | no |
| 4. kills | step budget | step budget | yes (universal) |
| 5. supporting | jigsaw pieces with green nubs | planks, anchors, pawn, goal, posts, sticky-cells | no |
| 6. signature | mid-tone background with multi-coloured pieces having green nub edges | light pastel + warm-tone planks + dark anchor rings | no |
| 7. grain | multi-pixel jigsaw shapes with edge nubs | long 1-cell-wide wood planks with circular anchor rings | no |
| 8. core dynamic | piece-arrangement to align connectors | avatar path-walking on rotating platforms | no |

Shared: 1 universal + ½ partial. **Pass.**

## Visual-signature plan (advance commitment, before write_spec)

To stay distinctive in the corpus:

- **Background**: pale slate-blue (palette 10) — so far unused as a dominant background in the recent priors I screenshotted (jd4q used black, vd3g used grey, ek73 used grey, kp9z used grey, lv4k used grey).
- **Letter-box / margin**: pale off-white (palette 1).
- **Plank sprite**: warm-orange body (palette 12) with a thin maroon edge stripe (palette 13) at the long-axis centre line, so a single plank renders as a 1×N rectangle with a clear central ridge — visually distinct from prior pawn-shaped sprites.
- **Anchor joint**: a 5×5 ring rendered with palette 5 (black) outer ring and palette 11 (yellow) inner pip — looks like a fastened bolt. The active plank's anchor pip becomes palette 14 (green) to communicate "this one is selected".
- **Pawn avatar**: 3×3 with palette 8 (red) outer + palette 0 (white) inner pip — small but legible.
- **Goal tile**: 4×4 hollow square in palette 6 (magenta) with a small palette 0 (white) inner dot.
- **Post (L2 obstacle)**: 3×3 black-ringed grey square (`{4, 3}`) — visually reads as a cylindrical post viewed top-down.
- **Sticky cell (L3)**: 4×4 cell in palette 15 (purple) with a 4-pixel diagonal weave inside — reads as a textured "trap" surface.

This palette signature `{10 background, 12 plank-body, 13 plank-edge, 5 anchor-outer, 11 anchor-pip, 8 pawn, 6 goal, 4 post-ring, 3 post-fill, 15 sticky}` gives 9 active palette values plus background = 10 distinct values. None of the recent priors I sampled used this combination dominantly (most lean grey + 2-3 accents).
