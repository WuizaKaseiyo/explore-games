# tb4k — tumble-block-stand-fall

## Seed
(autonomous — no user seed)

## 4-character ID
**tb4k** — confirmed not in the 25 reference IDs and not in
`prior-games/index.md`. Not an English word.

## Mechanic family tag
`tumble-block-stand-fall`

## One-paragraph description

A 1×1×2 brick sits on a tiled floor. Each arrow press **tumbles**
the brick end-over-end one step in that direction; the brick has
exactly three states — **standing** (single-cell footprint),
**lying horizontal** (two cells east-west), and **lying vertical**
(two cells north-south) — and tumbles alternate it between
standing and one of the lying states deterministically with each
move. Solid floor tiles support the brick in any state; **hole
tiles** kill the brick instantly if either of its occupied cells
lies over a hole. The goal cell is a sunken square that only
opens (winning the level) when the brick is **standing** on it
exactly; lying-across does not solve it. L1 is an open floor with
the goal at the other end (player learns the tumble rule). L2
introduces holes (lying-across becomes a hazard). L3 adds
**narrow bridges** — 1-cell-wide corridors where the brick can
only safely cross when standing or lying *along* the corridor, not
*across* it — so the player must plan the brick's state at every
junction.

## Core-knowledge priors used
- **Objectness** — the brick is a coherent, persistent object that
  moves, occupies cells, and can be destroyed (falling into a
  hole).
- **Basic geometry & topology** — the brick's footprint changes
  shape between 1×1 and 1×2 / 2×1 as it tumbles; the player
  reasons about rectangle orientation vs. corridor width.
- **Basic physics** — the brick "falls" into holes; standing vs.
  lying is a centre-of-mass distinction. The tumble itself is an
  end-over-end pivot.

(No agentness — no autonomous NPCs. This is a pure spatial
reasoning game.)

## Similarity check (positive — vs taxonomy + prior-games)

### Nearest TAXONOMY entries

- **None directly comparable.** The 25 reference games include no
  "tumble" or "stand-vs-lie footprint" mechanic. Nearest is
  **ka59 (sokoban-explode-chase)** — a single block slides on
  arrows and may detonate against walls. Distinguishing rule:
  ka59's block has a fixed footprint and translates one cell per
  press; tb4k's brick has 3 footprint states and tumbles
  end-over-end (move + rotate in a single press), with hole-fall
  hard-death.

### Nearest PRIOR-GAMES entries

- **hb5n (polyomino-walker-rotate)** — a rigid L-polyomino avatar
  walks via arrows and rotates 90° via ACTION5; grows by absorbing
  adjacent pickups; target is a goal silhouette to match.
  **Distinguishing rule:** hb5n maintains a fixed-and-growing
  rigid polyomino whose footprint only ever grows monotonically;
  tb4k's brick has 3 fixed footprints (1×1 standing, 1×2 east-west,
  2×1 north-south) that the player cycles through with each tumble.
  No pickups, no growth, no shape-matching target — tb4k's target
  is "stand exactly on this one cell". The mental experience is
  "I am planning rotation+translation of a single 1×1×2 brick over
  hazardous terrain", not "I am sculpting a polyomino by routing
  through pickups".
- **pj7k (rolling-cube-face-paint)** — a single coloured-faced cube
  rolls cell-to-cell; each roll permutes face colours and stamps
  the bottom face onto the cell. **Distinguishing rule:** pj7k's
  cube always occupies exactly one cell; the dynamic is face-
  permutation + paint-deposition. tb4k's brick occupies one or two
  cells (state-dependent), and the dynamic is footprint geometry
  over holes and bridges — no painting, no face permutation, no
  cell-state-change-by-cube.
- **nz3v (rotor-pivot-walk)** — a 2×2 avatar straddles a wedge
  boundary; ACTION5 rotates a player-controlled "lit sector"; 3
  lives per level. **Distinguishing rule:** nz3v's avatar is a
  rotating 2×2 with a sector mechanic centred on the rotor.
  tb4k has no rotor, no wedge sector, and no separate rotate verb
  — every tumble is one arrow press that simultaneously moves and
  changes state.
- **zw91 (inflate-fit-burst)** — a single avatar whose footprint
  cycles 3 sizes (1×1 / 2×2 / 3×3); arrows move, ACTION5 grows-
  pushes-or-bursts; body must fit same-size socket.
  **Distinguishing rule:** zw91's footprint change is **player-
  triggered** via ACTION5 and the avatar stays at one centre cell
  (radial inflation). tb4k's footprint change is **deterministic
  on arrow direction** (no separate verb), and the brick's centre
  shifts during each tumble (end-over-end translation+rotation).
  zw91 socket-fits a size; tb4k stands on a single cell.
- **kj82 (plank-pivot-walk)** — pawn walks long pinned planks;
  ACTION5 pivots a plank 90° around its anchor end. **Different**:
  kj82's pivoted object is the walkable surface (a plank, not the
  pawn); tb4k pivots the player object itself, and pivoting is
  fused with each arrow press.
- **lt7m (ell-jump-tour-block)** — click an L-shape-reachable cell
  to jump. **Different**: lt7m uses click-target jumps over an
  L-shape; tb4k uses arrow-directed end-over-end tumbles of a
  rectangular brick.

## Similarity check (negative — surface signature)

Walking the 8 dimensions of `negative-similarity-check.md` against
the closest priors (hb5n, pj7k, zw91, nz3v):

| Dim | tb4k L1 | hb5n L1 | pj7k L1 | zw91 L1 | Match? |
|---|---|---|---|---|---|
| 1. What is on the board | brick, plain floor, single goal cell | polyomino avatar + target outline | colour cube + colour targets | cycling avatar + size sockets | distinct |
| 2. Player input | arrow tumbles | arrows translate + ACTION5 rotate | arrows roll cube | arrows move + ACTION5 cycle size | partial (arrows) but tb4k *fuses* rotate into the arrow |
| 3. What level asks | stand exactly on goal cell | match target footprint | paint cells per target pattern | fit body into matching socket | distinct |
| 4. What kills | hole-fall (hard-death, 3 lives) + step budget | step budget | step budget | step budget | tb4k uniquely has hard-death |
| 5. Cast | brick, holes, narrow bridges, goal | polyomino, walls, pickups | cube, paint targets | size sockets | distinct |
| 6. Visual signature | mid-grey floor, dark slate brick with bevel-shaded faces, deep-magenta holes, blue goal pad | grey arena + red-orange polyomino + dim outline | grey + brightly coloured square cube + colour rings | similar | distinct palette: tb4k uses (3 grey floor, 5 dark slate brick, 4 bevel, 13 maroon hole, 9 blue goal) — no red/orange family |
| 7. Pixel grain of primary sprites | brick has internal shading (top face vs side face vs shadow); holes have crosshatched dark texture; bridges have rivet pattern | flat L-cells | flat coloured cube faces | flat | tb4k aims for richer internal pattern |
| 8. Core dynamic | "plan footprint-shape over holes and narrow paths" | "grow polyomino by routing through pickups" | "permute cube faces while paint-stamping cells" | "cycle my body size to fit sockets" | distinct |

No prior shares 3+ dimensions. **PASS** negative-similarity test.

## Hard-death note (checklist item 25)

Falling into a hole is hard-death. Per checklist 25, the level
spec MUST include a **lives mechanism (≥ 3 attempts per level,
respawn at start, lives counter visible)**. L1 may not have holes
(tutorial), but L2 and L3 do — lives mechanism activates from L2.
This will be addressed in `mechanic-spec.md` §4 per the template.
