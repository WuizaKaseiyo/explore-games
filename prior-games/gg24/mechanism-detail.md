# gg24 - museum-heist-net

Museum maze security game. Thieves spawn one after another and move one tile per
action through dark gallery corridors toward the escape door. `ACTION5` waits
for one tick. `ACTION6` clicks buy guards from the left palette, trigger visible
traps, or place cameras on marked camera mounts. Every click also advances the
heist.

Cameras cost 10 coins and do not damage thieves. They illuminate nearby
corridors, thieves, and traps with a short circular cone-like radius; unlit
gallery paths stay hidden. Camera mounts are always visible in the same yellow
used by active cameras, so players can expand visibility without guessing.

Traps are pre-installed on the maze path. Level 1 shows them immediately, while
levels 2 and 3 hide them until a camera reveals their corridor. Triggering a
visible armed trap costs 2 coins, damages every thief within three path steps
for 4, and then puts the trap on cooldown. Guards cost 5 coins from the left
palette, spawn at the exit, run backward through the maze, and deal 1 damage per
contact while spending one of their 5 hit points.

Pickpocket, burglar, safecracker, and master thieves have 2, 4, 8, and 11
health respectively. Capturing a thief awards 1 coin. If any thief reaches the
escape door, the level fails.

Level 1 teaches the visible-trap timing on a short maze. Level 2 requires buying
two cameras to uncover hidden trap positions and then mixing timed trap pulses
with guards. Level 3 has a longer 64x64 maze, a denser wave, and multiple hidden
trap rooms so the player must reveal the museum before committing the remaining
budget.

The board uses the full 64x64 canvas: dark museum floor tiles, artifact cases,
paintings, visible camera mounts, illuminated corridor patches, masked thief
sprites, guard sprites, entry/escape doors, and a bottom coin bar. Trap and hit
effects are intentionally small so the maze remains readable.
