# Mechanic pick — dj5h

## Game ID
**`dj5h`** — 4 lowercase chars (2 letters + digit + letter), not an English word, not in the 25 reference IDs, not in `prior-games/index.md`.

## Mechanic family
`pulley-pair-platform`

## One-paragraph description

**Pulley-Pair Platform Walk.** A horizontal beam runs along the top of the playfield with one or more pulley wheels mounted on it. From each pulley wheel two ropes hang down — one on the left side of the wheel, one on the right — each terminating in a coloured rectangular platform. The two platforms attached to the same pulley have a fixed *length-conservation* coupling: when one rises, the other falls. Each pulley has a binary state (`LEFT_HIGH` ↔ `LEFT_LOW`); ACTION5 toggles the currently-selected pulley, instantly inverting the heights of *both* of its platforms. The player walks (arrows) a small avatar along the solid floor and onto platforms; an adjacent platform is only walkable from the floor (or another platform) when its top surface is at floor-level (`LOW`). To reach a goal cell the player must select pulleys (click), toggle them (ACTION5), and walk along the alternating walkable-platform configuration. The mechanic draws on **basic physics** (length conservation across a pulley) and **objectness** (platforms as coherent walkable surfaces).

## Prior categories used
- **Basic physics** — pulley length-conservation (coupled motion).
- **Objectness** — platforms as walkable surfaces; weight-tokens (L2) as carryable objects; ratchet pins (L3) as toggleable fixtures.
- **Basic geometry & topology** — connectedness of the avatar's walkable region depends on platform heights; planning is a graph-reachability question.

## Closest taxonomy entries (25 reference games) and distinguishing rules

The positive similarity-check (`mechanic-novelty/similarity-check.md`) flags the following near-misses:

- **`m0r0` mirror-orb-merge.** *Coupled motion via mirrored arrows: UP moves both up, LEFT pushes one left while pulling the other right.* The coupling is *direction-mirroring* — both pawns move on the same arrow but with sign flips. **dj5h's coupling is vertical only and 1:1 length-conservation between two platforms on opposite sides of one wheel** — there is no mirroring of the avatar's motion (the avatar is a single walker). The active object pairs are platforms (immobile pieces of scenery whose heights toggle), not pawns the player drives.
- **`pv5q` pivot-rod-swing.** *A pawn fixed at the end of a rigid radial rod attached to a pivot stake; arrows swing/extend the rod.* The avatar IS the moving end of the rod. **dj5h's avatar walks freely on the floor; pulleys are scenery the avatar manipulates** by clicking and toggling, not by being attached to.
- **`kj82` plank-pivot-walk.** *A pawn walks long pinned planks; click selects a plank, ACTION5 pivots it 90° around its anchor end.* Planks rotate (rotational mechanic). **dj5h's platforms translate vertically, not rotate** — and rotations of one plank are independent of other planks, whereas dj5h's two platforms are *coupled* (toggling one inverts both).

No taxonomy entry shares all three of: (a) coupled vertical motion between paired surfaces, (b) walking on those surfaces, (c) click-then-ACTION5 to toggle pair-state. So while individual ingredients overlap, the composition is novel.

## Closest prior-games entries (60 entries in `prior-games/index.md`) and distinguishing rules

- **`pn5d` connected-vessel-filling.** *Pour into one vessel raises every connected vessel; toggleable valves split groups.* The coupling is hydrostatic — water levels equalise across all valve-connected vessels. **dj5h's coupling is rope-physical and binary-discrete: exactly one platform on each pulley pair is "down/walkable"; toggling instantly flips both. The visual is hanging platforms vs. filled containers.** No water, no pour, no equalisation across more than 2 platforms (each pair is independent).
- **`xv2b` vessel-valve-equalize.** Same family as pn5d — same distinguishing rule applies.
- **`kn58` anchor-pull-magnet.** *Click any cell to place a single magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it.* A click moves *all* same-influenced pawns. **dj5h's click selects a single pulley; ACTION5 toggles only that pulley's pair**, not all pulleys at once. And dj5h has no avatar-attraction — the click affects scenery, not pawns.
- **`mr5q` polarity-attract-discharge.** *Pawns flip yang/yin via click; per ACTION5 each walks toward nearest same-colour opposite.* Coupling is between paired *pawns* (not scenery), and the dynamic is attraction-along-Manhattan-axis (not vertical pulley toggle).
- **`m0r0` mirror-orb-merge** *(also in taxonomy near-misses above).* Same distinguishing rule applies.
- **`kj82` plank-pivot-walk** *(also in taxonomy near-misses above).* Same distinguishing rule applies.
- **`vt6q` grapple-anchor-yank.** *Fire a directed cardinal grapple line; heavy anchor yanks avatar.* Player yanks self toward an anchor — it is a verb-on-self, not a verb-on-paired-scenery.
- **`wb6n` tether-pin-wrap.** *Pawn on a fixed-length leash to a stake; ACTION5 plants pins that re-anchor the rope.* Tether is a constraint on a single pawn's reach. **dj5h has no tether on the avatar** — the avatar walks freely; the rope-coupling is between two scenery platforms, not between the avatar and a pin.

## Negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

I rendered the candidate's L1 mentally (a horizontal beam at top, one pulley wheel with two coloured platforms hanging on left and right, a small avatar on a floor row, a coloured target cell in the wall) and walked the eight dimensions against the closest priors:

| Dim | dj5h L1 | m0r0 L1 (img) | pv5q L1 (img) | kj82 L1 (img) | mr5q | pn5d | kn58 | wb6n |
|---|---|---|---|---|---|---|---|---|
| 1. What is on the board | beam + pulley + 2 hanging platforms + avatar + goal | bisymmetric maze + 2 orbs | rod + pawn + pivot stake + target | long plank + pivot + pawn + target | grid of pawns | row of vessels with water | grid of pawns + click anchor | pawn + leash anchor + goal |
| 2. What player physically does | walk + click pulley + ACTION5 toggle | walk both orbs in mirror | swing rod, slide pawn | walk plank, pivot plank | flip yin/yang via click + ACTION5 step | pour, toggle valve | click anchor, pawns auto-slide | walk pawn within tether, ACTION5 plant pins |
| 3. What level asks for | avatar reaches a goal cell on the far side | merge mirror orbs | place pawn on target | walk pawn across to target | discharge same-colour pairs | match target water levels | move pawns onto coloured targets | pawn reaches coloured-match goal |
| 4. What kills the player | step budget | step budget | step budget | step budget | step budget | step budget | step budget | step budget |
| 5. Cast | beam, pulley wheel(s), platforms, avatar, weight tokens (L2), ratchet pins (L3) | maze walls, mirror orbs | rod, pivot stake, pawn, target | plank, pivot, pawn, target | colour-pawns, walls | vessels, valves, drains, pumps | pawns, anchors, walls | pawn, stake, pins, goal |
| 6. Visual signature | beige floor + dark beam at top + bright distinct-colour platforms hanging from rope-lines + small avatar | yellow/orange split + black walls + cyan dots | grey background + green block + yellow rod + pink halo | salmon background + plank + pivot + pawn | flat playfield + pawns | tall vertical vessels filled with water | flat grid + coloured pawns + anchor sprite | pawn + visible leash line + stake + pins |
| 7. Pixel grain | platforms are 5×2 with internal coloured shading; pulley is 4×4 spoked wheel; rope is 1-px vertical line; avatar is 3×4 humanoid with internal pattern | rich orb shading and bisymmetric maze detail | rod + halo + spoked block | plank with checker pattern | pawns mostly 3×3 | tall vessels with water gradient | pawns and anchor block | pawn + clear rope rendering |
| 8. Core dynamic | binary toggle of paired-platform heights via overhead pulley → walkable-region graph changes | mirror-symmetric movement of two orbs | swing-extend a radial rod | rotate planks 90° | flip-then-step pawns | hydrostatic equalisation through valves | global slide on one click | tether-distance constraint with re-anchor |

Maximum overlap with any single prior is **2 dimensions** (typically Dim 4 step-budget kill is universal across the corpus, and one of {Dim 1, Dim 2, Dim 5}). No prior shares **3 or more** dimensions with dj5h. The novel core dynamic (binary coupled vertical toggle on shared-pulley pairs) is the load-bearing distinguishing feature; the visual signature (hanging platforms from a horizontal beam) does not appear anywhere in the corpus.

**Verdict: NOVEL.** Proceed to `write_spec`.
