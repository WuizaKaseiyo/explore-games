# Orchard-Night-Watch

## Core Concept

A selective-defense orchard game. Pests crawl toward fruit trees while helpful
bees move toward flowers. The player places owl perches and smoke pots to stop
pests without over-disrupting the beneficial bee traffic.

## Controls

- `ACTION6` on the palette selects owl perch or smoke pot.
- `ACTION6` on a valid off-path tile builds the selected tool for 10 coins.
- `ACTION5` waits for one night tick.
- Every action advances pests, bees, and tool cooldowns.

## Buildables

- Owl perch: cost 10, range 4, attacks only pests for 1 damage every tick.
- Smoke pot: cost 10, range 1, pulses every second tick. It slows all agents in
  range for one tick rather than damaging them.

The smoke pot is a tempo tool: it can hold back a dangerous pest, but careless
placement also delays bees.

## Moving Agents

Pests:
- Aphid: 2 health.
- Beetle: 4 health.
- Horned grub: 8 health.
- Boar boss: 11-14 health, larger tusked sprite.

Beneficial agents:
- Bees must reach flowers. If too many bees are delayed until the level timer
  expires, the level fails even if pests are stopped.

## Level Progression

- Level 1: pests only, one path, one owl perch teaches basic defense.
- Level 2: bee path appears separately and crosses near the pest path; smoke can
  help, but bad smoke placement delays bees.
- Level 3: mixed pests, bee traffic, and a boar boss. The player starts with one
  tool, then uses protected-fruit or arrived-bee rewards to build live.

## Visual Design

Use the full 64x64 frame: orchard rows, fruit trees, flower beds, moonlit grass,
small bee swarms, pests with readable faces, owl perches, smoke pot puffs, and a
large boar boss. Ranges and smoke pulses should be subtle so the bees and pests
remain readable.

## Implementation Feasibility

This is feasible but slightly more complex than the other two ideas because it
has two agent classes with different win/loss rules. It is still deterministic:
authored paths, no AI pathfinding, no hidden randomness, and simple tick-based
cooldowns.

## Conflict Check

It does not duplicate `gg24` plant growth because the core is selective moving
agent management, not routing nutrients. It differs from `gg02` because not all
agents are enemies; the main challenge is placement tradeoff and timing.
