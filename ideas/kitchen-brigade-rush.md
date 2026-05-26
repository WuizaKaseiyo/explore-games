# Kitchen-Brigade-Rush

## Core Concept

A compact production-defense game. Ingredients move along winding kitchen
counters toward a service bell. The player places prep stations beside the
counter to finish dishes before they reach service. Completed dishes award
coins, letting later levels require live station placement during the rush.

## Controls

- `ACTION6` on the palette selects the active station type.
- `ACTION6` on a valid off-counter tile builds the selected station if the
  player has enough coins.
- `ACTION5` waits for one kitchen tick.
- Every action, including selecting and building, advances ingredients one step.

## Buildables

- Knife station: cost 10, range 4, trims 1 prep point from the leading
  ingredient in range every tick.
- Oven station: cost 10, range 1, applies 4 heat/prep points to every cookable
  ingredient in range, but only every second tick.
- Optional later extension: garnish table, cost 10, range 2, only affects
  ingredients already reduced below half prep.

## Moving Agents

- Salad: 2 prep.
- Soup pot: 4 prep.
- Roast: 8 prep.
- Banquet roast boss: 11-14 prep, larger platter sprite and distinct colour.

Agents follow authored, non-axis-aligned counter paths. If any unfinished dish
reaches the bell, the level fails.

## Level Progression

- Level 1: 10 coins, one counter path, salads and soup. One knife station can
  clear the level.
- Level 2: 30 coins, a longer counter with roast agents. The player can afford
  knife + oven + knife, and must understand the oven cooldown.
- Level 3: 10 coins, long mixed rush. Early completed dishes fund a mid-wave
  oven and later knife before the banquet roast reaches service.

## Visual Design

Use the full 64x64 frame: checker kitchen floor, winding counters, steam puffs,
plates, sink tiles, stove glow, and a service bell at the end. Ingredients use
clear silhouettes: green salad bowl, blue soup pot, brown roast, and large
banquet roast. Station ranges are subtle dotted rings, and active prep feedback
is a small sparkle/steam pixel rather than large overlapping effects.

## Implementation Feasibility

This is realistic in the current harness: it needs only authored paths,
click-to-build palette state, deterministic cooldowns, and health-like prep
counters. It avoids text, random hidden state, and complex physics.

## Conflict Check

This does not duplicate `gg22` because ingredients are processed, not sorted by
switches. It does not duplicate `gg02` thematically because the fantasy is
production timing rather than defending a castle, though the proven economy and
cooldown structure can be reused.
