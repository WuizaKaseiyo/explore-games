# Sheep-Pasture-Fence

## Core Concept

A pasture planning puzzle. The board contains a sheep, grass, stones, and water.
The player has a limited fence budget and clicks squares to add or remove fence
segments. The goal is to enclose the sheep in the largest useful grass area,
meeting a minimum square target without leaving an escape path to the board
edge.

## Controls

- `ACTION6` on grass places a fence if budget remains.
- `ACTION6` on an existing fence picks it up again.
- Every valid click spends retry energy, so experimentation is allowed but not
  unlimited.

## Mechanics

The sheep uses four-direction reachability. Water, stones, and fences block
movement; diagonal contact never blocks or connects. After each click, the game
flood-fills from the sheep. If the reachable region touches the board edge, the
sheep can escape. If the region is enclosed and contains at least the displayed
minimum number of squares, the enclosed pasture highlights before the level
advances.

## Level Progression

Level 1 closes a compact jagged brook paddock with three required fences and a
target just below the witness pasture size. Level 2 has four openings around a
larger zigzag stream boundary with internal obstacles, requiring players to
evaluate the shape rather than fence a tiny box. Level 3 expands to an
edge-hugging grand hollow where the high area target forces the larger natural
boundary. Each level leaves one spare fence and enough retry energy for several
add/remove experiments.

## Visual Design

Use the full 64x64 frame as grassland: varied grass pixels, water, stones,
wooden fences, and a friendly sheep sprite. The HUD shows fence budget, retry
energy, current reachable area, and the target area. When the solution is valid,
the enclosed pasture changes colour for a few frames before advancing.

## Conflict Check

This replaces the rejected action-containment direction with a static spatial
optimization puzzle. It is distinct from maze, tower defense, conveyor, and
space-traffic games because the primary operation is budgeted enclosure and
area maximization under flood-fill connectivity.
