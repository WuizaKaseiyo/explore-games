# mechanic-pick — nz3v

## Game ID
`nz3v` (not in 25-game reference list, not in `prior-games/index.md`,
opaque 2-letter + digit + letter, not an English word).

## Mechanic family
`rotor-sweep-walk`

## One-paragraph description

A central rotor pillar at the centre of the playfield projects a
90° "lit wedge" outward and **auto-rotates one quarter-turn
clockwise per agent action** (no player input required; the wedge
sweeps regardless of which arrow is pressed). The player avatar
walks the playfield with cardinal arrows. Cells inside the
current lit wedge are walkable; cells outside are dark and
stepping into a dark cell ends the level. The base puzzle is to
**time arrow presses so each step's destination cell is in the
lit wedge at that step** — riding the rotating sector around
to reach a target. L1 introduces the rotor + sweep alone. L2 adds
**stop-tiles** that, when stepped on, freeze the rotor for the
next K actions (the wedge stops sweeping while the player walks
through the stalled period — a deliberate "wait verb" that the
player can place into their path). L3 adds a **second
counter-clockwise rotor** at the opposite point of the playfield;
walkable cells are now the **intersection of both lit wedges**.
The rotor mechanism, the stop-tile mechanism, AND the dual-rotor
intersection mechanism are all required by the L3 witness.

Priors used (per `core-knowledge-priors.md`): geometry & topology
(angular sector partitioning the plane), basic physics (uniform
rotation, deterministic per tick), objectness (rotor sprites, stop
tiles, target). No agentness, no symbolic content. Verbs:
arrows-only at L1/L2; arrows-only at L3 (no click, no ACTION5,
no ACTION7).

## Novelty defence

### Closest taxonomy near-misses

**fz5j (phase-step-tile)** — *closest cousin in the prior corpus.*
fz5j has per-cell pulse tiles each on its own period (2/3/4) that
open/close independently. The player computes `t mod period == offset`
per tile and inserts wall-bumps to align arrival residues. **Distinguishing
rule: nz3v has ONE global angular phase (the rotor's heading) that
gates a CONTIGUOUS quadrant of the playfield, not independent
per-cell timers.** The player reasons about *angular position* ("the
beam is pointing NE; in three steps it will be pointing E") rather
than *modular arithmetic per tile* ("col 10 is period-2 offset-0,
so I need t even when I arrive"). The walkable set in nz3v is
always one connected sector; in fz5j it is a constant corridor with
gates that flicker independently. Visually, fz5j renders pulse tiles
as 4×4 frame+cross sprites strewn along a corridor; nz3v renders a
solid lit wedge spanning a full quadrant from a central rotor — the
silhouettes share no primary element.

**lq5x (lantern-cone-illuminate)** — directional cone projected
from a player-carried lantern; ACTION5 rotates the cone, walking
moves the lantern. **Distinguishing rule: nz3v's wedge is
*environment-driven and auto-rotates per action* — the rotor is a
fixed central sprite, not a player avatar.** lq5x's lantern IS the
avatar; in nz3v the avatar is a separate pawn that the player walks
*within* the rotor's wedge. The verbs differ: lq5x has ACTION5 (player
controls cone facing); nz3v has only arrows (rotation is automatic).
The reasoning differs: in lq5x the player decides where to point the
cone; in nz3v the player has zero rotation control and must time
movement against the inevitable sweep.

**vp6h (shadow-cast-collect)** — collect crystals while standing in
shadow cast by static pillars under static (slidable) lanterns.
**Distinguishing rule: vp6h's lit/shaded geometry is fully spatial
and updates only when the player slides a lantern; nz3v's
walkable region rotates *every action* regardless of player input.**
vp6h's safety condition is intersection of static shadows; nz3v's L3
intersection is the intersection of two *time-varying* rotating
wedges. The temporal axis is the entire mechanic in nz3v, absent
in vp6h.

**g50t (walk-vs-scroll)** — board scrolls leftward; reach goal
before edge overtakes. **Distinguishing rule: g50t has a unidirectional
linear timer; nz3v has a *cyclic angular* constraint with
no monotonic "edge" — the wedge always returns to any angle
eventually.** g50t lets the player commit ghost paths via
ACTION5; nz3v has no commit verb.

**pf3w (wavefront-converge-timing)** — concentric BFS-radius
circles expand outward from emitters; level wins when target
cells coincide with frontiers on a single tick.
**Distinguishing rule: pf3w expands radial circles uniformly and
the player triggers emitters; nz3v rotates an angular wedge
auto-advanced by every action and the player walks within it.**
Geometry differs: concentric vs angular. Player verb differs:
click-emitters + ACTION5 commit (pf3w) vs arrows only (nz3v).

**xz5g (arena-pivot-rotate)** — click sets pivot, ACTION5 rotates
every rotatable sprite 90° around it. **Distinguishing rule:
xz5g rotates *sprites* at the player's command; nz3v rotates a
*walkable region* automatically per action.** Different agent (sprites
vs region), different cadence (player-pressed vs auto), different
verb.

**qz73 (radial-cycle-lock)** — rotate a single rotor of coloured
tips; ACTION5 advances rotation, click locks individual tips
to align with sockets. **Distinguishing rule: qz73 rotates the
rotor at the player's discretion (verb-driven) and the puzzle is
target-matching of tips to sockets; nz3v's rotor rotates
involuntarily and the puzzle is a walkability gate.** qz73 is a
shape-alignment puzzle; nz3v is a navigation puzzle.

**cd82 (stencil-paint-sweep)** — basket rides 8-position ring,
ACTION5 commits a sweep. **Distinguishing rule: cd82's ring is the
*action surface* (player navigates around it); nz3v's wedge is
the *terrain constraint* (player navigates within it).** Different
relationship of player to rotation.

### Closest prior-game near-miss screenshot comparison
Screenshots opened: `prior-games/fz5j/run-archive/smoke-frames/level_1.png`,
`prior-games/lq5x/run-archive/smoke-frames/level_1.png`,
`prior-games/vp6h/run-archive/smoke-frames/level_1.png`. **Visually
distinct on principle 2 (palette diversity / signature):** fz5j is
a horizontal grey corridor with red-cross life-pips; lq5x is a
black arena with a single-cell yellow lantern + 3 grey target
rings; vp6h is a vertical lit corridor with grey pillars and an
orange step-counter. nz3v's intended L1 silhouette is an open
arena with a centred dark-grey rotor pillar plus a brightly tinted
quadrant wedge filling 1/4 of the playfield — no priors share
this radar-sweep silhouette. **Principle 1 (pixel-detail richness):**
nz3v's primary sprites (rotor base, rotor cap, avatar, target
ring, stop-tile) will each carry internal pixel pattern (rotor
has a ringed base + tall cap with a pointing notch; stop-tile is
a square with an internal cross marker). **Principle 3 (core
dynamic divergence):** the player's mental model in nz3v is "I
must pick the arrow that puts me in the rotating wedge given the
current angle" — angular reasoning over a single global state.
None of fz5j, lq5x, or vp6h reduce to that.

### Negative-similarity 8-dimension count vs fz5j (closest cousin)
1. What's on the board: avatar + walls + step counter + sweep wedge + central rotor (nz3v) ↔ avatar + walls + step counter + per-cell pulse tiles (fz5j). **Different on the heavy elements (rotor + wedge vs pulse tiles).**
2. Player input: arrows only. **Same.**
3. Level asks for: reach target. **Same.**
4. What kills: stepping into the wrong cell at the wrong time, plus step counter. **Similar (timing-fail family).**
5. Cast: rotor + wedge + stop-tile + (L3) second rotor (nz3v) ↔ pulse tiles + walls + lives pips (fz5j). **Different.**
6. Visual signature: arena + central rotor + glowing wedge sector (nz3v) ↔ corridor + pulsing 4×4 frame-and-cross tiles (fz5j). **Different.**
7. Pixel grain: rotor pillar + filled wedge + accent pawn (nz3v) ↔ small per-cell pulse tiles + corridor walls (fz5j). **Different.**
8. Core dynamic: time-walk against rotating angular sector (nz3v) ↔ time-walk against per-cell independent periods (fz5j). **Same family, different sub-flavour: global angular reasoning vs local modular arithmetic.**

Shared count: 2 (verb), 3 (win), 4 (timing fail family) — 3 *light* axes.
Diverged: 5, 6, 7 are the *heavy* axes per the negative-check rubric, all clearly different. Dim 8 partially shared (timing-walk family) but with a fundamentally different reasoning texture.

Verdict per `negative-similarity-check.md`: passes — heavy axes diverge. The cluster of "timing-walk" priors (fz5j, lq5x, vp6h) does exist, but each member of that cluster occupies a distinct sub-cell, and rotor-sweep-walk fills a previously-empty sub-cell (auto-rotating angular wedge as terrain).

## Per-level mechanic plan (preview, full structure to be written in spec)

| Level | New mechanic(s) | Mechanics witness must use |
|---|---|---|
| L1 | M1 = rotor-sweep walkability | M1 |
| L2 | + M2 = stop-tile freezes rotor for K actions | M1, M2 |
| L3 | + M3 = second counter-clockwise rotor; walkable = intersection of both wedges | M1, M2, M3 |

+1 mechanic per level, every earlier mechanic remains required.

## Verbs / action subset
`available_actions = [1, 2, 3, 4]` — pure cardinal walk. Slot 5
deliberately *omitted* (no distinctive ACTION5 verb is needed; the
distinctive verb is the *passive sweep*, not a player action).
Slot 6 omitted (no click). Slot 7 omitted (no undo, per
`action-enum.md` strict-undo rule — not overloaded).

This unusual "no ACTION5, no ACTION6" subset is itself a divergence
from most timing-walk priors (lq5x has ACTION5; vp6h has ACTION6;
fz5j has arrows-only also). Matches reference subset pattern
`[1,2,3,4]` (ls20, tu93). The "freedom slot" is unused because the
game's distinctive verb is environmental, not a player verb.
