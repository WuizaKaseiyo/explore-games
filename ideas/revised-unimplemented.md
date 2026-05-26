# Revised Unimplemented Game Ideas

This pass narrows the remaining idea pool against `prior-games/index.md` and
the recent `gg15`-`gg20` feedback: avoid more small static grids, avoid
rotation/current/fuse/wave duplicates, make level progression introduce new
rules, and use the full 64x64 frame for richer visual signatures.

## Keep And Implement

### Flashlight-Key-Maze

Status: implemented as `gg21`.

Revision: replace the edge-port scan panel with an embodied maze. The player
navigates with arrow keys, sees only a short flashlight cone, discovers door
colours in the maze, then manages a limited backpack of coloured keys to open
those doors and find the hidden exit. This keeps the hidden-information
blindspot while removing guess-click interaction.

### Conveyor-Switch-Sorter

Status: implemented as `gg22`.

Revision: keep parcels belt-driven and put control into visible switches.
`ACTION5` clocks the conveyor and feeds parcels; `ACTION6` toggles junction
and station switches that determine which lane a parcel takes and which mark
station is active. Parcels enter from varied columns on shared connected belt
graphs, so they cannot be solved by isolated direct lanes. Switch-state overlays
remain visible even under a parcel. The three levels use different conveyor
graphs: right-drop branch sorter, mirrored left-drop return lanes, and a
bottom-to-top sorter with a central dispatcher and mode station. Default switch
states intentionally route parcels into wrong targets unless the player times
the switches. This keeps the factory-line concept without direct parcel
steering.

### Loop-Crossover-Flip / Braid-Strand-Weave

Status: implemented as `gg23`.

Revision: replace abstract loop flipping with a textile weave: thick strands,
over/under crossings, colour bleed, and L3 tension/smoothing. This introduces
a topology-plus-resource mechanic with a visual style unlike the prior blocky
arena games.

### Orc-Path-Tower-Defense

Status: implemented as `gg02`.

Revision: replace the printmaking prototype with a simplified tower defense
game. Orcs of three health classes march along winding, non-axis-aligned paths
toward a castle. `ACTION6` selects or builds off-path arrow/mine towers from a
small palette and `ACTION5` waits; every action advances the wave. Arrow ranges,
mine blast cells, arrow beams, and mine bursts are visible. Mines fire every
second combat tick to balance their high area damage. Levels 2 and 3 end with
a larger boss orc with more health and distinct red/horned pixel art. The
levels use the full 64x64 board with grass, ponds, trees, spawn cave, and castle
dressing. Level 3 requires live building from kill coins rather than solving
entirely from starting placements.

### Museum-Heist-Net

Status: implemented as `gg24`.

Revision: replace the rejected `gg24` direction with a museum security
maze. Thieves move through dark gallery corridors toward an escape door.
`ACTION6` places cameras on marked mounts, triggers visible traps, or hires
guards from the exit; `ACTION5` waits, and every action advances the heist.
Cameras reveal corridors and hidden traps instead of dealing damage. Traps are
manual paid bursts, while guards run backward through the maze and trade their
5 health for 1-damage hits. Levels escalate from visible trap timing, to hidden
trap discovery with guards, to a larger maze where camera placement and trap
cooldowns must be planned before the master thief reaches the exit.

### Docking-Orbit-Control

Status: implemented as `gg25`.

Revision: replace the static graph-building idea with a spacecraft traffic
control puzzle. `ACTION5` advances unheld ships plus moving raider/asteroid
patrols around authored 64x64 flight paths, and `ACTION6` either holds a
clicked ship or toggles a transfer beacon. Docks, moving hazards, and path
transfers make the timing spatially meaningful: the player must stop early
arrivals and divert other ships around hazards until all spacecraft reach their
respective docks.

### Sheep-Pasture-Fence

Status: implemented as `gg26`.

Revision: replace the rejected action-containment direction with a pasture
enclosure puzzle. `ACTION6` toggles fences on grass squares; every click spends
retry energy, and the fence count may not exceed the level budget. Stones,
water, and fences block the sheep's four-direction movement. After each click,
the game flood-fills from the sheep and checks whether the region is enclosed
away from the board edge and large enough for the displayed target. Valid
pastures highlight before the level advances. Levels escalate from a small
two-fence closure to larger irregular grasslands where the target area forces
using natural barriers efficiently rather than fencing a tiny box.

## Keep For Future Runs

## Replace Or Retire

### Wire-Rotate-Current

Retire in its current form. It overlaps heavily with `gg15` pulse-wire-relay
and with earlier beam/current routing games. A future replacement should use a
different representation, for example pressure in flexible tubes or musical
resonance through instruments, not rotatable endpoint wires.

### Heat-Diffuse-Equilibrium

Retire. It remains too close to wavefront/fuse/sandpile cellular propagation
and is visually likely to become another binary grid.

### Life-Tick-Evolve

Retire. Matching a cellular automaton pattern after ticks is hard to teach
without text, visually blocky, and mechanically adjacent to other whole-grid
propagation games.

### Raw Mirror/Optics Variants

Retire unless the visual and state model changes substantially. The corpus
already contains lantern cones, mirror beams, pulse wires, and wave rings.
