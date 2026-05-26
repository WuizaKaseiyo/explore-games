# Museum-Heist-Net

## Core Concept

A museum maze security game. Thieves move through dark, winding gallery
corridors toward the escape door. Existing cameras reveal only nearby corridors,
thieves, and traps; the player spends coins on extra cameras to uncover the rest
of the museum, triggers pre-installed traps at the right moment, and hires
guards that run backward from the exit into the thieves.

## Controls

- `ACTION6` on a marked camera mount places a camera for 10 coins.
- `ACTION6` on a visible armed trap triggers it for 2 coins.
- `ACTION6` on the guard palette buys one guard for 5 coins.
- `ACTION5` waits for one security tick.
- Every action advances thieves, guards, trap cooldowns, and spawning by one
  tick.

## Security Tools

- Cameras: fixed mount positions are always visible in the same yellow as the
  camera sprite. Cameras reveal nearby maze path, thieves, and traps; they do
  not deal damage.
- Traps: authored on the path. Level 1 shows them immediately, while later
  levels hide them until lit by a camera. Triggering an armed trap deals 4
  damage to every thief within three path steps and starts a cooldown.
- Guards: spawn at the exit with 5 health, walk backward through the maze, and
  deal 1 damage per contact while losing 1 health per hit.

The tool mix is deliberately different from tower defense: cameras are
visibility infrastructure, traps are manually timed, and guards are moving
interceptors instead of stationary damage towers.

## Moving Agents

- Pickpocket: 2 health.
- Burglar: 4 health.
- Safecracker: 8 health.
- Master thief boss: 11 health, larger red/purple cloak sprite with crown or
  mask pixels.

If a thief reaches the escape door, the level fails. Capturing a thief awards
1 coin.

## Level Progression

- Level 1: short maze, visible traps, and one active camera. The player learns
  trap timing without hidden information.
- Level 2: longer maze with hidden traps. The opening budget supports two extra
  cameras, then the player mixes revealed trap triggers with guards.
- Level 3: long 64x64 maze with several camera mounts and trap rooms. The
  player must reveal enough of the route early, then spend remaining coins on
  repeated trap timing before the master thief reaches the exit.

## Visual Design

Use the full 64x64 frame: dark museum floor tiles, camera-lit corridor patches,
visible yellow camera mounts, glass artifact cases, paintings on walls, a
vault-like exit, small security guards, mechanical floor traps, and subtle
hit/trap effects. Thief sprites should have readable masked faces and larger
silhouettes for tougher classes.

## Implementation Feasibility

The mechanic is implementable with the same compact primitives already used in
the project: authored Bresenham paths, fixed click targets, deterministic
cooldowns, health counters, moving interceptors, camera radius checks, and
simple 64x64 pixel sprites. No pathfinding or hidden randomness is needed.

## Conflict Check

This does not duplicate `gg25` because the player is not holding/diverting
moving spacecraft. It does not duplicate beam or wire games because cameras
reveal fixed museum space rather than reflecting rays. It also avoids becoming
another `gg02`: the player cannot build freeform towers around a visible path;
instead, they manage visibility, manually timed traps, and guards moving
backward through a hidden maze.
