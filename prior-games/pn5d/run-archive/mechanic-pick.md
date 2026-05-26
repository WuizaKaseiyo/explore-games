# Mechanic pick — pn5d

## Run input
- Seed: (autonomous; no user-provided seed)

## Game ID
**pn5d** — random 2-letter prefix `pn` + 2-char suffix `5d`. Not a recognisable English word. Not in the 25-reference reserved list. Not in `prior-games/index.md`.

## Mechanic family
`vessel-equalize-flow`

## One-paragraph description
A horizontal row of open-top rectangular vessels sits on the playfield, each filled to a current "water level" (a coloured fill rising from the vessel's floor up to the level row). Vessels are joined at their bases by short horizontal pipe-segments fitted with **valves** (small click-toggles). Liquid in any *connected group* of vessels (those linked through open valves) immediately equilibrates to a common surface level — pour 1 unit into any vessel of the group, and **every** vessel in the group rises by `1 / (sum of group widths)` of a height-unit (i.e. volume conservation: total height-times-width is preserved across the connected group, not per vessel). A small **pour-cursor** sits above the row of vessels; the player slides it left/right (ACTION3/4), and pressing ACTION5 pours one volume-unit into the cursor's vessel; clicking a valve (ACTION6) toggles it open/closed, immediately re-equilibrating the new groupings. Each vessel has an imprinted **target-mark** notch on one of its inside walls, at a specific row; the level wins when every vessel's surface is at its mark. The single failure mode is the per-level step counter exhausting before all marks are matched — overpouring is recoverable in principle (toggle a valve, redirect, etc.) but consumes steps. Action subset `[3, 4, 5, 6]` (no UP/DOWN — the cursor only translates between vessel tops; no UNDO since L1 is recoverable without it and L2/L3's plan is short enough that re-derivation is cheaper than rewinding).

## Similarity check (positive)

Walking the §3.4-priors taxonomy + `prior-games/index.md` for entries that COULD overlap on family or description:

### Closest taxonomy entries

- **sp80** — `pour-shelf-route` (reference). *"Click a shelf to grab and slide it left/right with arrows; pour-key sends water plummeting from each marked spout (splits on a shelf, falls straight off), and the level wins when every cup catches a drop while drains spend one of four pour attempts."* **Distinguishing rule:** sp80 is a **droplet-routing** mechanic (a single droplet falls vertically through a chain of player-positioned shelves into target cups; the puzzle is *aiming droplets*); pn5d is a **volume-distribution** mechanic (many vessels share a continuous liquid volume across an open-valve graph, and the puzzle is *distributing total volume so each vessel hits its mark*). sp80 has no equilibration — its drops are discrete one-shot trajectories; pn5d has no trajectories — its volume *redistributes instantaneously across the connected group*.

- No other reference game involves liquid-as-fill at all.

### Closest prior-games entries

- **kx14** — `tide-tilt-buoyant`. *"Vertical fluid tank where ACTION1/2 raise/lower the water surface, ACTION3/4 tilt floating balls, ACTION6 anchors."* **Distinguishing rule:** kx14 has **one** tank with a player-controlled **global water surface**, and the win condition is BUOYANT BALLS landing on target rings (objects floating IN the liquid). pn5d has **multiple** vessels connected through valves, the player's verb is **POURING** (not raising the surface), and the win condition is the **liquid surfaces themselves** matching target marks (the liquid IS the active object, no buoyant pieces). Different verb, different goal, different cast of supporting elements.

- **lv4k** — `lever-balance-torque`. *"Place tray weights onto a horizontal beam pivoting on a fulcrum so the integer mass-arm torque sum is zero with all weights placed."* **Distinguishing rule:** lv4k is **placement of discrete weights for static balance**; pn5d is **fluid distribution under continuous equilibration**. Both involve a "balance" intuition but operate on different abstractions (discrete masses with lever-arm vs. continuous volumes with shared-surface equilibration).

- **kp9z** — `grain-accumulate-topple`. *"Click sources to drop grains; cells overflow at capacity 4 to 4 cardinals; sinks absorb; click-rotatable redirectors forward one grain in their oriented direction."* **Distinguishing rule:** kp9z is **discrete grains diffusing one cell per click**, with toppling at capacity; pn5d is **continuous liquid equilibrating instantly across connected vessels** with no per-cell capacity and no neighbour-toppling rule.

- **kn58** — `anchor-pull-magnet`. *"Click any cell to place a single magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it."* **Distinguishing rule:** kn58 is **discrete pawns sliding under a placed attractor**; pn5d has no attractor and no movable pawn — only liquid-volume redistribution.

- **vd3g** — `valley-dig-roll`. *"Click cells to toggle binary terrain HIGH/LOW; marbles flow downhill into adjacent low cells; walls and remote-linked anchor pairs add composition."* **Distinguishing rule:** vd3g is **discrete marbles rolling downhill on a binary-elevation grid**; pn5d is **liquid level equilibrating across a small set of explicit vessels** with valve-toggle topology, not gravity flow over arbitrary terrain.

No taxonomy or prior matches on family-tag (none use `vessel-equalize-flow` or any close variant). Two priors (kx14, kp9z) share the SUBSTANCE but not the MECHANIC; the rest don't overlap meaningfully.

## Negative similarity check

For each potentially-overlapping prior, walking the eight dimensions in `negative-similarity-check.md` against my mental render of pn5d L1 (a row of 2 narrow open-top boxes filled with light-blue from the bottom up to roughly the same height; small notch-marks inside each vessel's right wall; tiny dot-cursor above the left vessel; bottom-row HUD bar):

- **vs sp80** (`pour-shelf-route`): shared = "involves liquid-as-fill aesthetic" (dim. 7 partial). Different on **what's on the board** (rectangular vessels vs. shelves+cups), **what the player does** (toggle valves + pour vs. slide shelves + spout-trigger), **what the level asks for** (vessel-surfaces hit target marks vs. droplets fill cups), **kill mode** (step budget vs. pour-attempt counter), **cast** (vessels+valves vs. shelves+spouts+cups), **visual signature** (vertical fills with horizontal valves vs. horizontal shelf routing), **core dynamic** ("distribute total volume across a connectivity graph" vs. "aim falling drops via deflectors"). Sharing on one dimension. **Pass.**

- **vs kx14** (`tide-tilt-buoyant`): shared = "liquid is filled in cells" (dim. 7 partial — both render water as colored fill). Different on **what's on the board** (multi-vessel-row vs. single-tank), **player verb** (pour-and-toggle-valve vs. raise-water-surface-and-tilt-balls), **goal** (vessel-surfaces vs. balls in rings), **cast** (vessels+valves vs. tank+balls+platforms+anchors), **visual signature** (multiple narrow vertical strips with valves at base vs. one big tank), **core dynamic** ("local pour, system equilibrates via Pascal" vs. "global water-surface up/down, balls re-project"). Sharing on one (partial) dimension. **Pass.**

- **vs kp9z, kn58, vd3g, lv4k**: each shares at most one dimension (some "discrete-resource-distribution" affinity in each, but none on the visual signature, the core dynamic, or the cast). All pass.

No prior overlaps on three or more dimensions. **Negative test passes.**

## Notes on the chosen mechanic
- Core-knowledge prior used: **basic physics** (volume conservation, Pascal's principle for connected vessels) + **basic geometry/topology** (open-vs-closed-valve connectivity defines connected components) + **objectness** (each vessel is a distinct persistent entity).
- Distinctive verb: pour (ACTION5) — fits the "ACTION5 carries the game's identity" idiom.
- Action subset `[3, 4, 5, 6]` is uncommon (none of the 25 reference games declares exactly this subset; closest are `[1, 2, 3, 4, 6]` and `[5, 6]`).
- Why this is a good NovaPlay candidate:
  1. **Exploration**: the player must pour at least once to discover that equilibration is instant and global within a connected group — not derivable from a single static frame.
  2. **Modeling**: once Pascal's principle is observed, the agent can predict each pour's effect deterministically — sharp drop in action count after discovery.
  3. **Goal-discoverable from layout**: the imprinted target marks are visually encoded as small inward notches on the vessel walls — same visual language as the existing fill, no symbol or text.
  4. **Planning**: at L2 and L3, multiple valve-configurations route the same volume to different vessels; the player must pre-plan which valves to open before pouring to avoid wasting steps re-routing.
  5. **No randomness**, **no on-screen text**, **no symbol glyphs** — all visual elements are abstract rectangles, fill, notches, and pipe-segments.
