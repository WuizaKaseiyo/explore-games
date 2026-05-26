# Mechanic pick — Run 4

## Run input
Seed: (autonomous — no seed provided by the user).

## Game ID
**qb84**

ID-generation check:
- 4 lowercase alphanumeric characters: ✓ (q, b, 8, 4 — letter, letter, digit, digit).
- Not in reserved list (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30): ✓.
- Not in `prior-games/index.md` (kf42, qz73, kx14): ✓.
- Not a recognisable English word: ✓ ("qb84" is opaque).

## Mechanic family tag
**bead-lift-swap**

## One-paragraph mechanic description

A serpentine **chain of coloured beads** lies along a fixed snaking
path through a 64×64 playfield. Above and below the chain, scattered
along the path's flank, sit small **peg sprites** of various
colours. The player has a logical **cursor index** picking out one
bead on the chain; ACTION3/4 step the cursor backward/forward along
the chain by one bead. ACTION1 ("lift") temporarily displaces the
cursor's current bead one cell perpendicular to the chain's local
travel direction toward the **above-flank**, swaps that bead's
colour with whichever peg sprite occupies the destination cell (if
any), then drops the bead back to its chain slot. ACTION2 ("drop")
does the same toward the **below-flank**. A lift/drop into a cell
with no peg is a no-op (no step consumed). The level wins when the
chain's bead-colour sequence (cursor-start to cursor-end) matches
the **target sequence sprite** rendered at the playfield corner.
The only failure is exhausting the per-level step counter — there is
no chaser, no hazard, no instant-fail.

## Action-space declaration
`available_actions = [1, 2, 3, 4]` — pure-arrow input. No ACTION5,
no ACTION6 click, no ACTION7 undo. This deliberately diverges from
ALL three prior games' verb-slots: kf42 = click + arrows, qz73 =
ACTION5 + ACTION6, kx14 = arrows + ACTION6.

## Composition arc (3 levels — full check happens in `write_spec`)

- **L1 (base dynamic, N=2 mechanics):** chain + pegs are present;
  cursor exists; ACTION3/4 step cursor; ACTION1 lift-swaps with an
  above-peg; ACTION2 drop-swaps with a below-peg. The L1 witness
  uses BOTH ACTION1 (an above-peg target colour) AND ACTION2 (a
  below-peg target colour) — both verbs are required for the
  shortest path to win.
- **L2 (+1 mechanic, N+1=3):** introduces **sticky pegs** —
  visually-distinguished pegs that, after one swap with a bead,
  permanently lock the bead's colour. The witness must sequence
  lifts so that beads needing further swaps don't pass through
  sticky pegs first. L1's lift+drop verbs are still both required
  by L2's witness; L2 adds the new sticky-peg interaction.
- **L3 (+1 mechanic, N+2=4):** introduces **pair pegs** — pairs of
  pegs joined by an invisible internal link. Lifting/dropping a
  bead onto one pair-peg propagates a same-tick colour swap into
  the bead's neighbour-bead-on-the-chain (positionally on the
  chain, not by colour). The witness must use pair-pegs to reach
  colours otherwise unattainable, while still respecting sticky-
  peg locks AND lift+drop verbs from L1. Order of operations
  matters — the trivial heuristic "for each target slot, find a
  peg of that colour and lift" is defeated because pair-peg
  propagation depends on which neighbour is being swapped.

## §3.4 prior categories
The mechanic draws from:

- **Objectness** (beads and pegs are persistent entities).
- **Basic geometry & topology** (the chain has a fixed serpentine
  path; "above"/"below" the chain are local-frame perpendiculars
  derived from chain travel direction).

No physics is required (no gravity, no momentum). No agentness
(pegs do not pursue; nothing is mobile besides the player-driven
cursor and the bead currently being lifted/dropped). All four
priors are NOT all required — design draws from the two listed.

## Forbidden-elements check

- No letters, no digits-as-glyphs, no real-world clipart (beads and
  pegs are abstract coloured shapes).
- No on-screen instructions or hint text.
- The "above"/"below" framing is a TOPOLOGICAL property of the
  chain's path, not a directional cultural convention (no
  "up = good"). The terminology is internal to the spec; the
  rendered game shows the relationship visually as positional
  offset perpendicular to the chain.

## Positive similarity check (vs taxonomy + priors)

For each row that could be flagged by family-name overlap or
gameplay overlap, the concrete distinguishing rule:

| Row | Family-name overlap? | Description-level near-miss? | Distinguishing rule |
|---|---|---|---|
| **vc33 (row-slide-pull-tab)** | Both involve a chain/row of cells. | vc33 swaps WHOLE ROW positions on a click; mine swaps INDIVIDUAL bead colours via lift/drop. | vc33's verb is "click pull-tab → entire row shifts 1 cell"; my verb is "displace one bead vertically and swap colour with the adjacent peg in the swap destination cell". Different cardinality (whole-row vs single-bead) and different effect (positional shift vs colour swap). |
| **lp85 (row-col-shift-grid)** | Both have a row mechanic. | lp85 PHYSICALLY shifts Rubik-style row/column positions on a click. | lp85 is pure-click + permutation-of-positions; mine is pure-arrow + colour-swap-via-peg-collision. Different verb-slot (`[6]` vs `[1,2,3,4]`) and different effect (position permutation vs colour swap). |
| **tr87 (tape-rewrite-rule)** | Both have a horizontal tape, both pure-arrow. | tr87 cycles a card's symbol identity at the cursor; mine displaces the bead vertically to swap colours with a peg. | tr87 cycles intrinsic symbol identity through a 7-glyph alphabet at a fixed slot; mine PHYSICALLY displaces a bead between the chain and a peg array, transferring the peg's colour into the bead. tr87 has no perpendicular displacement and no colour transfer with a separate sprite. |
| **ls20 (cycler-attribute-match)** | Both involve cycling attributes. | ls20 cycles by walking the avatar onto cycler tiles. | ls20 has a free-walking avatar with WASD; mine has a non-spatial CURSOR that just selects which bead is active. ls20 cycles three independent attributes (shape/colour/rotation); mine swaps colour identity by collision with a peg sprite. |
| **s5i5 (rod-stretch-retract)** | Both have multiple coloured elements that can be operated on. | s5i5 stretches/retracts rod LENGTHS via clicks. | s5i5 changes geometry (rod length); mine changes colour identity (bead colour swap). Different state being mutated. Different verb-slot (`[6]` vs `[1,2,3,4]`). |
| **sb26 (tile-place-commit)** | Both end with "row matching target". | sb26 has a Mastermind-style guess+commit loop; mine has direct in-place colour swap. | sb26 places candidate tiles into slots and commits with ACTION5 to get hint feedback; mine has no commit step, no hint feedback, and no candidate tray — colours come from physically-reachable pegs along the chain's path. |
| **kf42 (tether-pawn-cycle)** prior | Both involve coloured-piece colour change. | kf42 changes a pawn's colour by walking onto a coloured pad. | kf42 is click+arrows with a tether constraint between two pawns; mine is pure-arrow with a fixed chain (no tether, no movable pawns). Different action-space and different constraint topology. |
| **qz73 (radial-cycle-lock)** prior | Both involve elements arranged on a path-like layout. | qz73 has a radial ring of slots; mine has a serpentine chain. | qz73's verb is ACTION5 = "advance EVERY unlocked tip one slot CW"; mine's verb is ACTION1/2 = "displace ONE bead perpendicular to chain". qz73 has a global rotation operator; mine has per-bead local swaps. |
| **kx14 (tide-tilt-buoyant)** prior | None. | None. | kx14 is a vertical-tank water/tilt/anchor game; mine is a chain-traversal swap game. No shared verb, no shared layout. |

No rejection triggered. Every flagged row has a concrete distinguishing rule.

## Negative similarity check (visual + dynamic divergence)

Walking the 8 dimensions of `negative-similarity-check.md` against
the closest priors and taxonomy near-misses:

### vs **kf42** (closest prior by colour-change family)

1. *What is on the board:* kf42 = small walled grid + 2 pawns + maybe colour pads. Mine = serpentine chain of beads with flanking pegs. **DIFFERENT.**
2. *Player input:* kf42 = click-to-select + arrow-to-move. Mine = pure arrow (cursor-step + lift/drop). **DIFFERENT.**
3. *Level asks:* kf42 = each pawn on its target pad. Mine = bead sequence matches target sequence. **DIFFERENT.**
4. *What kills:* both step counter. **SHARED.**
5. *Cast:* kf42 = 2 pawns + target pads + walls + cycler pads. Mine = chain beads + pegs + target reference. **DIFFERENT.**
6. *Visual signature:* kf42 = small walled box, palette-4 walls, 2 vivid pawns. Mine = serpentine chain over neutral background, palette of beads + pegs + target ref panel. **DIFFERENT.**
7. *Pixel grain:* kf42 = 1×1 / 2×2 plain rectangles. Mine = 2×2 or 3×3 patterned beads (rounded), small triangular pegs. **DIFFERENT.**
8. *Core dynamic:* kf42 = "shepherd two tethered pawns to colour-matching pads". Mine = "swap individual bead colours via reachable pegs to compose a target sequence". **DIFFERENT.**

Shared dimensions: **1** (#4 step counter — universal). PASS.

### vs **qz73** (closest prior by structured-array layout)

1. *Board:* qz73 = radial 8-slot ring with hub. Mine = serpentine chain. **DIFFERENT.**
2. *Input:* qz73 = ACTION5 + ACTION6 click. Mine = pure arrow. **DIFFERENT.**
3. *Asks:* qz73 = every socket holds a tip of matching colour. Mine = bead sequence matches target. SOMEWHAT shared (both "match by colour").
4. *Kills:* step counter. **SHARED.**
5. *Cast:* qz73 = tips + sockets + lock-overlays + hub. Mine = beads + pegs + target. **DIFFERENT.**
6. *Visual sig:* qz73 = radial ring on dark background. Mine = serpentine chain. **DIFFERENT.**
7. *Pixel grain:* qz73 = small tip rings. Mine = beads (small ring/square shapes). SOMEWHAT shared.
8. *Core dynamic:* qz73 = "rotate-and-lock to align rotation orbit with sockets". Mine = "displace+swap per bead". **DIFFERENT.**

Shared: ~2 (#3 partial, #4, #7 partial). PASS.

### vs **kx14** (closest prior by vertical-displacement framing)

1. *Board:* kx14 = vertical fluid tank. Mine = serpentine chain. **DIFFERENT.**
2. *Input:* kx14 = arrows + ACTION6 click. Mine = pure arrow. **DIFFERENT.**
3. *Asks:* kx14 = balls in colour-matching ring targets. Mine = bead sequence matches target. **DIFFERENT.**
4. *Kills:* step counter. **SHARED.**
5. *Cast:* kx14 = balls + targets + platforms + water. Mine = beads + pegs + target. SOMEWHAT shared (both have "movable colour-bearing sprites + targets").
6. *Visual sig:* kx14 = light-blue water + off-white air + bright balls. Mine = TBD (avoid water-blue dominance).
7. *Pixel grain:* kx14 = 5×5 cells with platforms as 3-cell-wide bars. Mine = 2-3 cell beads.
8. *Core dynamic:* kx14 = "tide+tilt+anchor planning". Mine = "cursor+lift/drop swap planning". **DIFFERENT.**

Shared: ~2. PASS — but **commit to a non-water palette** to keep the
visual signature divergent from kx14.

### vs **tr87** (closest taxonomy near-miss by pure-arrow row layout)

1. *Board:* tr87 = grid of input/output rule pairs above two horizontal tapes of cards. Mine = serpentine chain with flanking pegs. **DIFFERENT.**
2. *Input:* both pure-arrow (1,2,3,4). **SHARED.**
3. *Asks:* tr87 = bottom tape = rewrite of top tape under rule set. Mine = sequence match. SOMEWHAT shared (both row-vs-target).
4. *Kills:* step counter. **SHARED.**
5. *Cast:* tr87 = symbol cards + rules + cursor brackets. Mine = beads + pegs + target ref. **DIFFERENT.**
6. *Visual sig:* tr87 = cyan + pink cards on grey, distinctive 1-bit glyphs inside cards. Mine = (commit to a divergent palette — see palette section).
7. *Pixel grain:* tr87 has detailed inner-glyph rendering at sub-card scale. Mine = simple bead/peg grain.
8. *Core dynamic:* tr87 = "rewrite under stated grammar rules". Mine = "displacement-swap to compose target". **DIFFERENT.**

Shared: ~3 (#2, #3 partial, #4) borderline. The shared #2 is the
most structurally meaningful — same verb-slot. To diverge harder:
*the spec must commit to a chain layout that is NOT visually
read as a straight horizontal row*. A serpentine S-curve or
zigzag chain is the chosen layout, plus a target reference panel
that's a small icon (not a horizontal tape). PASS conditionally —
write_spec must commit to a serpentine path, not a straight row.

## Palette commitment for visual divergence

To stay visually divergent from all 3 priors AND tr87:

- **Background:** palette 4 (off-black) — distinct from kf42's
  default, qz73 (also dark but with bright radial ring), kx14
  (light-blue water dominant), tr87 (grey).
- **Chain path / channel under beads:** palette 2 (light-grey) —
  thin trail-marker showing the snaking shape.
- **Bead palette:** 4 colours rotating through {6 magenta, 11
  yellow, 14 green, 15 purple} — magenta+yellow+green+purple, a
  distinct quartet not used as the dominant palette in any prior
  (kf42 used red+blue, qz73 used orange+green+purple+magenta+yellow
  in a radial layout, kx14 used orange+green balls in light-blue
  water).
- **Peg distinguishers:** plain pegs = solid coloured triangles in
  the bead palette; sticky pegs = same colours but with a black
  inner pixel; pair pegs = pairs share a small shared dot.
- **Target reference:** a small horizontal mini-strip in the
  bottom-right corner showing the target sequence. Distinct from
  tr87's full-tape display.
- **HUD:** depleting step bar at the very top row (palette 0/4
  white-on-dark), like cn04's bar position — keeps it out of
  central play area.

## Open issues to resolve in `write_spec`

- Concrete chain shape per level: L1 = 6-bead S-curve; L2 = 8-bead
  zigzag; L3 = 10-bead double-S. Must verify each renders cleanly
  on 64×64.
- Per-level step budget tuning (target ~2 minutes per level for an
  attentive human): need to set L1 step budget so witness fits in
  ~6-12 actions, L2 in ~12-20, L3 in ~20-35.
- The "sticky peg" lock: does it permanently fix the bead's
  colour, or only block the same peg from being re-used? Spec
  must commit. (Default: bead's colour locked permanently after
  any swap involving a sticky peg.)
- The "pair peg" propagation rule: does it swap the same colour
  into the neighbour bead, or the inverse colour, or copy the
  pair's other peg colour? Spec must commit. (Default: lifting a
  bead onto pair-peg-A copies pair-peg-B's colour into the bead's
  positional neighbour on the chain.)
- The named trivial heuristic L3 defeats: "find peg of target
  colour, lift bead onto it". L3 defeats this because under
  pair-peg propagation, a 'wrong'-coloured peg may need to be
  visited first to set up a neighbour-bead's colour, after which
  the 'right' peg is reached. Must be made concrete in spec §6
  (witness solution).

## Verdict
**NOVEL.** Family `bead-lift-swap`, ID `qb84`. Proceed to
`write_spec` with the commitments above (especially: serpentine
chain layout, off-black background + magenta/yellow/green/purple
beads, pure-arrow verb-slot).
