# Mechanic Pick

## Game ID
**hk7v**

Verified non-colliding against:
- the 25 reserved reference IDs
- every row in `prior-games/index.md`
- every existing folder under `prior-games/`
- every folder under `game_sources_3_lvls/`

Opaque (not an English word, no semantic hint about the mechanic).

## Mechanic family
**`overhead-trolley-hook`**

## One-paragraph description
A horizontal beam runs across the top of the playfield carrying a small
movable trolley; a vertical rope of variable length hangs from the
trolley with a hook at its end. The player has no walking avatar — all
input drives the trolley/rope/hook system from above. ACTION3/4 slide
the trolley left/right one cell along the beam, ACTION1/2 raise/lower
the hook one cell along the rope, and ACTION5 toggles the hook's
grab/release state: when the hook is at a block's cell and grab is
toggled on, the block latches to the hook and follows it; when grab is
toggled off, the block detaches and falls under gravity until it hits
the floor or the top of an existing stack. The win condition is that
every coloured block sits on its same-coloured floor target. Two
mechanics layer on top of the base manipulator across L2 and L3:
**rope-collides-with-walls** (the rope is a vertical line of cells from
the trolley down to the hook, and any wall sprite intersecting that
column at any row between trolley and hook blocks the rope, so the
trolley cannot move horizontally while the hook is below the wall — the
player must raise the hook above the wall first), and
**gravity-stacking** (released blocks fall and stack vertically; only
the topmost block in a column can be grabbed, so a stacked supply
column must be disassembled top-down).

## Core-knowledge priors
Draws from §3.4's allowed categories only:
- **Objectness**: trolley, hook, blocks, walls, targets are persistent
  entities that move, collide, and pair (block→target).
- **Basic physics**: gravity-induced falling and stacking; rope as a
  rigid vertical link that cannot intersect solid walls.
- **Basic geometry & topology**: trolley horizontal axis decoupled
  from rope vertical axis; rope-clearance-above-wall is a topology
  constraint.

No agentness (no autonomous NPCs, no chasers, no pursuers). All state
changes are deterministic given the action sequence.

## Action subset
`available_actions = [1, 2, 3, 4, 5]` — cardinal motion repurposed for
the manipulator (UP/DOWN raise/lower hook, LEFT/RIGHT slide trolley) +
ACTION5 as the modal grab/release verb. Slot 6 (click) is absent
because all manipulation is positional via the trolley/hook, not via
direct cell selection. Slot 7 (undo) is absent — the game has no
meaningful undo (releasing a block is destructive in the sense that the
block's new position depends on falling stack state, but there is no
"reverse the last action" semantic this game would honour, and per
checklist item 22 / `global/action-enum.md` ACTION7 must be omitted
rather than overloaded).

## Distinguishing rules vs the closest priors

For each near-miss in the taxonomy and prior-games index, the concrete
distinguishing rule (per `similarity-check.md` + `negative-similarity-check.md`):

### vs `wa30` (lock-drag-crate, taxonomy)

`wa30`: a green-tipped lavender player walks four-pixel hops on the
floor; pressing the lock key when standing beside a grey crate latches
it to the player so the next walk drags the crate alongside. Goal is
to deliver every crate into a hollow blue-bordered goal-frame; later
levels add a competing purple drone.

**Distinguishing rule**: in `wa30` the player IS the actor on the
floor — they walk to a crate, latch beside it, and drag it via their
own footpath. In `hk7v` there is no walking avatar at all; the player
operates an overhead trolley+rope+hook system from above. The rope
is a separately-tracked sprite with its own collision rule
(rope-cannot-intersect-walls), which has no analogue in `wa30`.
Negative-similarity dimension count: shared on dim 3 (delivery goal)
and dim 4 (step-budget lose). Differs on dims 1 (overhead vs floor),
2 (trolley/hook input vs walking input), 5 (no avatar, rope sprite
unique), 6 (top-beam+vertical-rope visual signature unique), 8
(core dynamic = "indirect overhead manipulation under rope-clearance
constraint" vs "walk-latch-walk"). 2-3 shared dims < 3-dim threshold.

### vs `dj5h` (pulley-pair-platform, prior)

`dj5h`: overhead pulleys couple paired hanging platforms; click selects
a platform, ACTION5 toggles state, peg unlocks walls, cable couples
pairs at L3.

**Distinguishing rule**: `dj5h`'s "overhead" element is a pair of
*coupled* platforms whose vertical positions are linked (one rises,
the other falls) and the player rides on one platform. In `hk7v` there
is exactly ONE rope hanging down with one hook at its end and no
coupling — raising the hook does not lower anything else. The game
has no platforms a player rides; the player is not anywhere on the
playfield, only the hook contacts blocks. The composition rules
differ: `dj5h` adds couplings and pegs, `hk7v` adds rope-vs-wall
collision and gravity stacking. Negative-similarity: shared dim 4
(step budget). Differs on every other dim.

### vs `vt6q` (grapple-anchor-yank, prior)

`vt6q`: fire a directed cardinal grapple line; heavy anchor yanks
avatar to adjacent cell, light anchor yanked to socket.

**Distinguishing rule**: `vt6q` fires an *instantaneous* grapple line
each input — the line travels far in a single tick, snaps to a single
cell, and resolves the yank. `hk7v` has no firing — the rope is always
present (a static vertical sprite from trolley to hook) and the hook
crawls one cell per ACTION1/2; manipulation is continuous-position,
not fire-and-snap. Also `vt6q` has a walking avatar that gets yanked;
`hk7v` has no avatar at all. Shared dim: 4. Differs on every other dim.

### vs `nb6t` (hinge-chain-reach, prior)

`nb6t`: three rod-segments at independent hinges; rotate / extend /
cycle active; carry-and-drop at L3 to deliver an item to a drop-zone.

**Distinguishing rule**: `nb6t`'s manipulator is a *hinged articulated
arm* — the player rotates segments around hinges, and reach is
controlled by *angular* motion. `hk7v`'s manipulator is a
*Cartesian* gantry — independent X (trolley) and Y (rope length) axes,
no rotation involved. The reach geometry is a 2D rectangle, not the
arc-of-articulated-arm reach geometry of `nb6t`. Carry-and-drop
existing in `nb6t` L3 is a partial overlap on dim 3; differs on dims
1, 2, 5, 6, 8.

### vs `wb6n` (tether-pin-wrap, prior)

`wb6n`: pawn on a fixed-length leash to a stake; ACTION5 plants pins
that re-anchor the rope, extending reach.

**Distinguishing rule**: `wb6n`'s "rope" is a leash from a stake to a
walking pawn — the pawn is the avatar and the leash constrains the
pawn's reachable cells. `hk7v`'s "rope" hangs from a movable trolley
to a non-walking hook — the rope is straight vertical and length is
explicitly variable per action. No pin-replanting in `hk7v`; no
leash-radius constraint. Shared dim 4. Differs on every other dim.

### vs `pv5q` (pivot-rod-swing, prior)

`pv5q`: pawn fixed at end of rigid radial rod attached to a pivot
stake; arrows swing/extend rod, ACTION5 swaps anchor between stakes.

**Distinguishing rule**: `pv5q` is a *radial* manipulator — the pawn
is on the end of a rigid rod that swings around a pivot, so the
reach is a circle of fixed radius. `hk7v` is a *Cartesian* manipulator
— the hook moves in independent X/Y axes, reach is a rectangle. No
swinging in `hk7v`. Shared dim 4. Differs on every other dim.

## Negative-similarity-check synthesis

The candidate's visual signature (top horizontal beam, single small
trolley moving along it, vertical rope of variable length hanging
straight down to a hook, floor with coloured blocks and outlined
target zones) is unique against every prior in the index — none of
the priors render an overhead-beam-and-rope assembly. The dominant
palette is targeted at greens/yellows/whites for the manipulator and
distinct primary palette colours for blocks/targets, deliberately
diverging from the `{4, 8, 9}` cautionary tale (kf42→vh68) and from
the orange-and-blue-only `wa30`-adjacent palette.

The core dynamic is "operate a Cartesian gantry under a vertical-rope-
clearance constraint, with gravity-driven stacking on release". No
prior shares this dynamic — the closest (`wa30`, `nb6t`, `pv5q`,
`dj5h`, `wb6n`, `vt6q`) each diverge on at least 5 of the 8 negative-
similarity dimensions.

## Composition plan (preview for write_spec)

- L1 mechanics (witness-required): overhead-manipulator (the base
  dynamic system: trolley H + hook V + grab/release), color-pairing
  (block must be released on its same-coloured target). Two
  interacting mechanics — small base system, fully exercised by the
  L1 witness.
- L2 adds **+1**: rope-collides-with-walls. A free-standing wall
  separates the supply side from the target side at a height that
  forces the player to raise the hook above the wall before
  traversing it horizontally. L2 witness exercises all three
  mechanics.
- L3 adds **+1**: gravity-stacking. The supply blocks start as a
  stacked column (3 blocks deep); only the topmost block can be
  grabbed; releasing a block in any column drops it onto the floor
  or the existing stack top. L3 witness exercises all four mechanics.

Per the difficulty-rules.md two-stage model, planning depth grows
L1→L2→L3: L1 has near-immediate planning post-discovery (move trolley,
lower, grab, raise, traverse, lower, release); L2 introduces rope-vs-
wall ordering constraints (must clear before moving); L3 introduces
ordering constraints from the stack (which block to disassemble first
matters because the order of placements is dictated by how high the
stack regrows when you release elsewhere).
