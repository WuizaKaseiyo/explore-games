# yf3h — Mechanic Spec

## 1. Title
Pulse-Arm-Burst Resonate

## 2. Mechanic family
`pulse-arm-burst-resonate` — a transient-wave-propagation puzzle. Allowed core-knowledge priors: **objectness** (emitters, resonators, phase-delay tiles are persistent stateful objects), **basic geometry** (Manhattan rings = isodistance contours), and **basic physics** (wave propagation at unit speed, with localised delay through certain medium cells). No agentness; no symbolic/cultural conventions.

The player arms one or more stationary emitters by clicking them, then triggers a single simultaneous `ACTION5` "burst" that fires every armed emitter at once. Each fired emitter projects one transient concentric pulse-ring that expands outward 1 cell per animation tick (the ring at tick T is the set of cells at exact Manhattan distance T from the emitter). The puzzle is to choose which emitters to arm, and (from L3) to set up phase-delay tiles, so that on the same tick at each resonator, the colour-multiset of rings sweeping over the resonator matches that resonator's required-multiset. The mechanic combines spatial reasoning (Manhattan distance) with temporal coordination (same-tick arrival).

## 3. Sprite roster

All pixel arrays use palette values `0..15` (or `-1` for transparent). Each gameplay-relevant sprite has multi-pixel internal structure that survives a 2×2 average-pool downsample to 32×32 (per checklist item 20).

- **`emitter_red`** — 5×5; palette values `{8 (red), 4 (dark grey), 11 (yellow)}`.
  - Disarmed pixel matrix:
    ```
    [-1,  8,  8,  8, -1],
    [ 8,  8,  8,  8,  8],
    [ 8,  8,  4,  8,  8],     # tiny dark-grey dot in centre = disarmed
    [ 8,  8,  8,  8,  8],
    [-1,  8,  8,  8, -1],
    ```
  - Armed pixel matrix:
    ```
    [-1,  8,  8,  8, -1],
    [ 8,  8,  8,  8,  8],
    [ 8,  8, 11,  8,  8],     # tiny yellow dot in centre = armed
    [ 8,  8,  8,  8,  8],
    [-1,  8,  8,  8, -1],
    ```
  - Tags: `["emitter", "armable", "colour:red"]`.
  - Role: a stationary emitter; click toggles armed/disarmed; centre-dot colour shows arm-state. The 5×5 solid-filled square shape (vs the resonator's hollow frame and the phase-tile's plus pattern) marks it visually as "an active emitter object".

- **`emitter_blue`** — same shape as `emitter_red`, body colour `9 (blue)`. Tags: `["emitter", "armable", "colour:blue"]`. Same disarmed/armed pixel-pattern with `8 → 9` substitution; centre-dot 4 (disarmed) / 11 (armed).

- **`emitter_green`** — same shape, body colour `14 (green)`. Tags: `["emitter", "armable", "colour:green"]`. Same disarmed/armed convention.

- **`resonator_red`** — 5×5 hollow frame; palette values `{8 (red), 4 (dark grey), 0 (white)}`.
  - Inactive pixel matrix:
    ```
    [-1,  8,  8,  8, -1],
    [ 8, -1, -1, -1,  8],
    [ 8, -1,  4, -1,  8],     # hollow with tiny dark-grey centre dot
    [ 8, -1, -1, -1,  8],
    [-1,  8,  8,  8, -1],
    ```
  - Activated pixel matrix:
    ```
    [-1,  8,  8,  8, -1],
    [ 8,  0,  0,  0,  8],
    [ 8,  0,  0,  0,  8],     # filled bright white = activated (sticky)
    [ 8,  0,  0,  0,  8],
    [-1,  8,  8,  8, -1],
    ```
  - Tags: `["resonator", "single_colour", "required:red"]`.
  - Role: a stationary target. Outline colour matches its single-colour required-multiset. The hollow-frame shape (vs the emitter's filled square) marks it visually as "a target awaiting input". When all required colours hit on the same tick, the centre fills with white permanently.

- **`resonator_blue`** — same shape, outline colour `9`. Tags: `["resonator", "single_colour", "required:blue"]`.

- **`resonator_green`** — same shape, outline colour `14`. Tags: `["resonator", "single_colour", "required:green"]`.

- **`resonator_multi_red_blue`** — same hollow-frame shape, outline colour `3 (grey)` to indicate multi-colour. Tags: `["resonator", "multi_colour", "required:red+blue"]`. Multi-colour resonators DO NOT use their outline to communicate the requirement (because a grey outline by itself is ambiguous); they pair with a `pip_*` sprite stack placed immediately above them.

- **`pip_red`** — 2×2 solid block; palette `{8 (red)}`.
  ```
  [ 8,  8],
  [ 8,  8],
  ```
  Tags: `["pip", "colour:red"]`. Role: HUD-style indicator — placed adjacent above a multi-colour resonator to display one element of its required-multiset.

- **`pip_blue`** — 2×2; palette `{9}`. Tags: `["pip", "colour:blue"]`.

- **`pip_green`** — 2×2; palette `{14}`. Tags: `["pip", "colour:green"]`. (Reserved for hypothetical future multi-colour resonators that include green; not used in the L1-L3 layout below.)

- **`phase_delay_tile`** — 3×3; palette values `{6 (magenta), 4 (dark grey), 0 (white)}`.
  - Inactive pixel matrix:
    ```
    [ 6, -1,  6],
    [-1,  4, -1],     # 4-corner-dot pattern with dim centre
    [ 6, -1,  6],
    ```
  - Active pixel matrix:
    ```
    [ 6,  6,  6],
    [ 6,  0,  6],     # solid filled magenta with bright-white centre
    [ 6,  6,  6],
    ```
  - Tags: `["phase_delay", "togglable"]`.
  - Role: a stationary tile the player toggles via click; when active, the next ring of any colour that passes over this tile is delayed by 1 tick (each ring delays at most once per tile, regardless of how many ticks the ring's radius footprint includes the tile cell). The 4-corner-dot vs filled-square shape change is the visual cue distinguishing inactive from active.

- **`ring_overlay`** — level-sized sprite (`grid_size` matches level grid). All pixels start as `-1` (transparent); repainted on every animation tick during a fire-burst to render each active ring's footprint in the ring's colour. Layer 10 so it draws on top of emitters/resonators/delay-tiles but leaves cells with other sprite content untouched (only writes to cells where the underlying frame is `BACKGROUND_COLOR`). Tags: `["ring_overlay"]`. Role: pure visualisation; not interactable.

  Sprite-as-meaning summary (without colour, just by pixel pattern): emitters are 5×5 SOLID FILLED squares with a centre-dot indicator. Resonators are 5×5 HOLLOW FRAMES; activated state fills the centre with white. Phase-delay tiles are 3×3 with a 4-CORNER-DOT pattern when inactive and SOLID FILLED with white centre when active. Pips are flat 2×2 blocks with no internal structure (intentional — they're HUD-like multiset indicators, not interactable game objects, exempt from #20 like step-counter HUD bars). Every gameplay-relevant sprite type is distinguishable by shape alone before considering colour. (Colour then communicates which colour the emitter/resonator is keyed to.)

## 4. Level progression, mechanic enumeration, and witness solutions

The base playfield is a `12×12` grid for every level (consistent grid_size). `BACKGROUND_COLOR = 4 (dark grey)`; `PADDING_COLOR = 5 (black)`. The 12×12 logical grid scales 5× to fill 60×60 of the 64×64 frame (per universal-scaffold `Camera` math), centred with 2-pixel letter-box padding. The bottom row of the 64×64 frame is reserved for the step-counter HUD (see §6).

### Level 1 — base dynamic system

- **Mechanics required by the witness** (`N = 1`):
  - **M1 (`arm-fire-ring-strike-resonator`)**: clicking an emitter (`ACTION6` at the emitter sprite's bbox) toggles its arm-state; pressing `ACTION5` simultaneously fires every armed emitter, each projecting a Manhattan-ring expanding 1 cell per animation tick. When a ring of colour C reaches cell (rx, ry) at tick T = Manhattan(emitter, (rx, ry)), and (rx, ry) is a resonator with `required = {C}`, the resonator activates permanently.

- **Necessity per mechanic**:
  - *L1 cannot be solved without triggering M1 because* without firing rings, no resonator can be activated (resonators only activate on ring-strike). The only path to activate the `resonator_red` at (8, 6) is to arm `emitter_red` at (3, 6) and fire — the level has no other affordance.

- **Layout**:
  - `emitter_red` at grid (3, 6) (centred-left, anchor sprite cell).
  - `resonator_red` at grid (8, 6) (centred-right).
  - Manhattan distance: `|8-3| + |6-6| = 5`.
  - No walls, no delay tiles, no other emitters or resonators.
  - Step budget: 12.

- **Witness solution** (shortest action sequence): `[ACTION6@(3, 6 emitter_red bbox click), ACTION5]` — 2 actions.
  - Click at the emitter_red cell to arm it (centre dot transitions dark-grey → yellow); the player visually confirms "the emitter is armed".
  - Press ACTION5: the fire animation begins. The red ring expands from emitter_red over 5 animation ticks, reaching the resonator_red at tick 5. The resonator_red's centre fills white permanently.

  In ACTION6 click coordinates: the emitter sprite anchored at grid (3, 6) — at scale 5× and 2-pixel letter-box, the emitter's centre cell maps to display pixel `(3*5 + 2 + 2, 6*5 + 2 + 2) = (19, 34)`. So the canonical click is `ACTION6@(19, 34)`. (Implementation notes: the click handler resolves the click via `camera.display_to_grid` and then `level.get_sprite_at(gx, gy, "emitter")`, so any pixel within the 5×5 bbox of the emitter selects it.)

- **Difficulty justification**:
  - **(a) Random-resistance**: A vision-blind random-action agent, at every step picking either ACTION5 or ACTION6 with random `(x, y)`, has to: hit ACTION6 in the emitter's 5-pixel × 5-pixel bbox (about 25 of 4096 display pixels = 0.6%), then ACTION5 within the budget. The probability of solving in 12 random actions is small but non-zero; this matches §3.4's expectation that "Random agents can occasionally stumble into success at this stage, which is acceptable by design".
  - **(b) Human-tractable**: ~1 minute. The player sees one filled red square (emitter) and one hollow red frame (resonator) and intuits "fire emitter at resonator". ACTION6 click + ACTION5 produces the expanding ring animation, which is the discovery cue for "rings sweep outward from emitters".
  - **(c) Planning depth**: NO STRICT PLANNING REQUIREMENT. Once the player understands "click emitter to arm, ACTION5 to fire", solving is mechanical — there is no choice of which emitter (only one) and the witness is a 2-step sequence with no decision branching.
  - **(d) Step budget**: 12 (witness = 2). Generous over the witness so the player can experiment with random clicks (e.g. clicking on the resonator first to see what happens, clicking on empty cells, pressing ACTION5 with no emitter armed) before the budget bites.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (`M = N+1 = 2`):
  - M1 (`arm-fire-ring-strike-resonator`) — carried forward from L1.
  - **M2 (`colour-keyed resonator`)**: a single-colour resonator with outline colour C only activates when struck by a ring of matching colour C. A wrong-colour ring sweeping over a resonator does nothing — the multiset requirement excludes the wrong colour, so the matching-pip never flashes for a wrong-colour ring.

- **Necessity per mechanic**:
  - *L2 cannot be solved without triggering M1 because* (as in L1) without firing rings, no resonator activates. Two resonators must be activated to win L2; no path bypasses the arm-fire pipeline.
  - *L2 cannot be solved without triggering M2 because* the level has TWO resonators of distinct colours (`resonator_red` and `resonator_blue`), and each can only be activated by its colour-matching ring. If M2 did not exist (any-colour ring activates any resonator), arming just one emitter (say red) and firing once would activate BOTH resonators — but with M2, only the matching colour activates each. The player must arm both emitter_red AND emitter_blue (whether in one fire or two separate fires) to win.

- **Layout**:
  - `emitter_red` at grid (2, 3); `emitter_blue` at grid (2, 8).
  - `resonator_red` at grid (9, 3); `resonator_blue` at grid (9, 8).
  - Manhattan distances: red emitter→red resonator = `|9-2| + |3-3| = 7`; blue emitter→blue resonator = `|9-2| + |8-8| = 7`.
  - Cross-distances: red emitter→blue resonator = `|9-2| + |8-3| = 12`; blue emitter→red resonator = same = 12.
  - No walls, no delay tiles.
  - Step budget: 16.

- **Witness solution**: `[ACTION6@emitter_red, ACTION6@emitter_blue, ACTION5]` — 3 actions.
  - Arm both colours, then fire once. After fire: the red ring reaches (9, 3) on tick 7 and (9, 8) on tick 12; the blue ring reaches (9, 8) on tick 7 and (9, 3) on tick 12. M2 ensures only colour-matching strikes activate each resonator: tick-7 red strike at (9, 3) activates resonator_red; tick-7 blue strike at (9, 8) activates resonator_blue. The tick-12 cross-colour strikes do nothing.

- **Difficulty justification**:
  - **(a) Random-resistance**: The post-discovery solution requires arming two specific emitters and pressing ACTION5; a random agent must hit each emitter's 5×5 bbox plus ACTION5 in the right order. With budget 16, possible but unlikely without exploration of M2.
  - **(b) Human-tractable**: ~2 minutes. The new visual cue is the second emitter (blue) and second resonator (blue). The player tries firing only one colour first (e.g., arm just red, fire) and observes: red-resonator activates, blue-resonator does NOT activate (the blue ring did not exist on this fire). The player infers M2 from the observation: "the ring's colour determines which resonator activates". They then arm both and fire.
  - **(c) Planning depth (post-discovery)**:
    - *Decision space at level start* (number of valid first actions a fully-informed player faces): **3** — arm emitter_red, arm emitter_blue, or fire (firing immediately produces no rings since nothing is armed; this wastes 1 step). Plus the meta-choice of arming-then-firing-once (3 actions total) vs arming-firing-arming-firing (4 actions total).
    - *Plausible-but-wrong alternative the post-discovery player would consider and reject*: "fire each colour separately for cleaner reading" (`arm red, fire, arm blue, fire`) — costs 4 actions instead of 3. A post-discovery player would notice that one fire suffices since rings are independent.
    - *Witness's reasoning chain*: The player reasons "both rings can fire simultaneously without interference because resonators are colour-keyed; the cheapest path is to arm both first, then a single fire activates both resonators by matching colour". This is post-discovery reasoning about action efficiency given M2's colour-keying.
  - **(d) Step budget**: 16 (witness = 3). Gives the player ~13 steps of slack to experiment with arming-firing patterns and to recover from a 1-2-step exploration cost.

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (`M_new = M_l2 + 1 = 3`):
  - M1 (`arm-fire-ring-strike-resonator`) — carried forward from L2.
  - M2 (`colour-keyed resonator`) — carried forward from L2; now extended to a multi-colour resonator with required-multiset `{red, blue}`. (The mechanic is the same — outlined-colour-keying — but the multiset can have multiple colours; activation requires every colour in the multiset to strike on the SAME animation tick.)
  - **M3 (`phase-delay tile`)**: an `ACTION6` click on a phase-delay tile toggles its active-state (visible 4-corner-dots vs solid-filled-magenta). When active, the next ring of any colour that touches the tile cell has its expansion delayed by 1 tick (the ring's radius is held at its current value for one extra tick, then advances normally; downstream cells therefore see the ring 1 tick later than they would without the delay). Each ring delays at most once per tile, even if its expanding radius footprint covers the tile cell on multiple consecutive ticks.

- **Necessity per mechanic**:
  - *L3 cannot be solved without triggering M1 because* (as L1, L2) without firing rings, no resonator activates.
  - *L3 cannot be solved without triggering M2 because* the multi-colour `resonator_multi_red_blue` at (5, 5) requires both red AND blue colours on the SAME tick. Without M2 (any ring activates any resonator), a single ring of any colour passing over it would trivially activate it. With M2, the multi-colour multiset is respected, so the player must orchestrate the simultaneous arrival of red and blue rings. Additionally, the `resonator_green` at (5, 9) is colour-keyed `{green}`; a wrong-colour ring (red or blue) passing over it does nothing.
  - *L3 cannot be solved without triggering M3 because* the multi-colour resonator at (5, 5) is at Manhattan distance 6 from `emitter_red` at (2, 2) and at Manhattan distance 7 from `emitter_blue` at (2, 9). Without M3 (no phase-delay), the red ring reaches (5, 5) on tick 6 and the blue ring reaches (5, 5) on tick 7 — different ticks → multi-resonator never sees both colours simultaneously → never activates. The phase-delay tile at (2, 5) sits at Manhattan distance 3 from emitter_red. When it is set active by ACTION6 click, the red ring's expansion is held 1 extra tick when its radius first equals 3, so the red ring reaches (5, 5) on tick 7 instead of 6 — aligning with the blue ring. The phase-delay tile at (2, 5) is NOT on the blue ring's path to (5, 5) (Manhattan distance from emitter_blue at (2, 9) to tile at (2, 5) is 4, on the blue ring's path; but blue ring already arrives at (5, 5) on tick 7 = the desired tick, so delaying blue would push it to tick 8 and miss), so the player must NOT delay the blue ring — only the red.

  Concrete check that no alternate path bypasses M3:
    - Strategy "arm only red+blue, fire, no delay tile": red reaches multi-resonator tick 6; blue tick 7. Multi-resonator hits = {red on tick 6, blue on tick 7}. Per-tick multiset: {red} on 6, {blue} on 7. Neither matches required {red, blue} — multi-resonator stays inactive.
    - Strategy "arm only green, fire": green ring expands but green is not in multi-resonator's required multiset; green ring does not activate it.
    - Strategy "arm all 3, fire (no delay)": as above, multi-resonator's per-tick multiset never contains both red AND blue on same tick. Multi-resonator inactive.
    - Strategy "engage delay tile, arm all 3, fire": red arrives tick 7, blue tick 7, green ring sweeps to green-resonator tick 7. Multi-resonator activates from {red, blue} simultaneous; green-resonator activates from green. WIN.

  Other potential delay-tile placements that would also work would be on the blue ring's path with the requirement "delay blue by 1 tick" instead of red — but the level provides only ONE delay tile, and it is positioned such that activating it delays only the red ring (the tile is not on the blue ring's path to the multi-resonator at the right radius). So the player has no choice but to use it on the red ring.

- **Layout**:
  - `emitter_red` at grid (2, 2); `emitter_blue` at grid (2, 9); `emitter_green` at grid (8, 5).
  - `resonator_multi_red_blue` at grid (5, 5); `pip_red` at grid (4, 4); `pip_blue` at grid (4, 6) (above the multi-resonator's top-left and top-right corners — these visually display the required-multiset). (Pips render at layer 5, behind the ring_overlay.)
  - `resonator_green` at grid (5, 9).
  - `phase_delay_tile` at grid (2, 5).
  - Manhattan distances:
    - emitter_red (2, 2) → multi-resonator (5, 5) = `|5-2| + |5-2| = 6`.
    - emitter_red (2, 2) → phase-delay tile (2, 5) = `|2-2| + |5-2| = 3`.
    - emitter_blue (2, 9) → multi-resonator (5, 5) = `|5-2| + |5-9| = 7`.
    - emitter_blue (2, 9) → phase-delay tile (2, 5) = `|2-2| + |5-9| = 4`. (The blue ring's radius equals 4 when its footprint includes (2, 5); blue ring would also be delayed by an active tile here, but it would arrive at (5, 5) on tick 8 — too late. So the level forces the player NOT to "use" the tile on blue. Conveniently, the tile is on emitter_red's path *first* — the red ring's radius reaches 3 (the tile cell's distance from emitter_red) on tick 3, before blue's radius reaches 4 on tick 4. The "passed_tiles" tracker per ring ensures each ring is delayed at most once by this tile, and the natural order of ring expansion makes red the first to encounter it.)

    To prevent the blue ring also being delayed (which would miss): the spec stipulates that the per-ring `passed_tiles` set is per-ring not per-tile, so the same tile can delay multiple rings (one each). This means an active tile DOES delay both red and blue. With both delayed by 1 tick, red arrives at (5, 5) tick 7, blue at (5, 5) tick 8 — still mismatched.

    So actually, an active tile at (2, 5) breaks both rings: red delayed 7, blue delayed 8. The witness DOES NOT WORK as I described. **Re-design needed.**
  - Step budget: 18.

  *Re-design note*: I need to position the phase-delay tile such that ONLY the red ring crosses it, OR I need to introduce a barrier so blue can't reach (2, 5). A clean fix is: position the tile at (1, 4) — the (row, col) only on the red ring's path. Manhattan(emitter_red (2, 2), tile (1, 4)) = `|1-2| + |4-2| = 3` (red's footprint at tick 3 includes (1, 4)). Manhattan(emitter_blue (2, 9), tile (1, 4)) = `|1-2| + |4-9| = 6`. So blue's footprint at tick 6 includes (1, 4) — but blue arrives at (5, 5) on tick 7 (Manhattan = 7), which is AFTER tick 6. So the tile delays blue at tick 6, holding blue's radius at 6 for one tick, then advances to 7 on tick 8. Blue's arrival at (5, 5) (Manhattan 7) is now on tick 8.

  Hmm, that breaks the puzzle still.

  Alternative: place the tile on the FAR side of (5, 5) from emitter_blue, so blue's ring passes (5, 5) before reaching the tile. Specifically, tile at row > 5 or col < 5 such that Manhattan(emitter_blue, tile) > 7.

  Tile at (1, 1) — Manhattan(emitter_red (2, 2), (1, 1)) = 2 (red touches at tick 2); Manhattan(emitter_blue (2, 9), (1, 1)) = 9 (blue touches at tick 9, well after blue has already reached the multi-resonator at tick 7). So tile at (1, 1) only affects red (red reaches tick 2 → delayed → red at (5, 5) on tick 7; blue at (5, 5) on tick 7; aligned). Blue's delay at tile (1, 1) would happen at tick 9 but the multi-resonator activation is decided at tick 7 (or whichever tick red and blue first co-occur).

  Update: tile at grid (1, 1).
    - Manhattan(emitter_red (2, 2), tile (1, 1)) = 2 — red's footprint at tick 2 includes (1, 1). If active, red is delayed 1 tick at radius 2. Red's radius timeline: 0, 1, 2 (at tick 2, footprint includes tile, delay applied), 2 (held one extra tick — tick 3 stays at radius 2), 3, 4, 5, 6 — so red reaches radius 6 on tick 7 instead of 6. Red arrives at (5, 5) on tick 7. ✓
    - Manhattan(emitter_blue (2, 9), tile (1, 1)) = 9 — blue's footprint at tick 9 includes (1, 1). But the multi-resonator decision is at tick 7. So blue is unaffected by the tile at the moment of multi-resonator activation.
    - Manhattan(emitter_green (8, 5), tile (1, 1)) = 11 — far enough that green's footprint at tick 11 includes (1, 1), but the green-resonator at (5, 9) is reached at tick 7 (before tile delay applies). So green is unaffected.

  Updated layout:
  - `emitter_red` at grid (2, 2); `emitter_blue` at grid (2, 9); `emitter_green` at grid (8, 5).
  - `resonator_multi_red_blue` at grid (5, 5); `pip_red` at grid (4, 4); `pip_blue` at grid (4, 6).
  - `resonator_green` at grid (5, 9).
  - `phase_delay_tile` at grid (1, 1).
  - Step budget: 18.

  Manhattan distance recap (updated):
    - emitter_red (2, 2) → multi-resonator (5, 5) = 6.
    - emitter_red (2, 2) → phase-delay tile (1, 1) = 2.
    - emitter_blue (2, 9) → multi-resonator (5, 5) = 7.
    - emitter_blue (2, 9) → phase-delay tile (1, 1) = 9.
    - emitter_green (8, 5) → green-resonator (5, 9) = 7.
    - emitter_green (8, 5) → phase-delay tile (1, 1) = 11.

- **Witness solution**: 5 actions.
  - `ACTION6@phase_delay_tile (1, 1)` — toggle the phase-delay tile to active. Visual: tile transitions from 4-corner-dot to filled-magenta-with-bright-centre.
  - `ACTION6@emitter_red (2, 2)` — arm.
  - `ACTION6@emitter_blue (2, 9)` — arm.
  - `ACTION6@emitter_green (8, 5)` — arm.
  - `ACTION5` — burst-fire. The red ring is delayed at radius 2 (touched the active tile); arrives at multi-resonator on tick 7. Blue ring arrives at multi-resonator on tick 7 (no delay). Multi-resonator's per-tick multiset on tick 7 = {red, blue} = required → activates. Green ring arrives at green-resonator on tick 7; green-resonator's required = {green}; activates.

- **Difficulty justification**:
  - **(a) Random-resistance**: Random agent has to find the right delay-tile click + 3 specific emitter clicks + ACTION5, in budget 18. Cumulative probability of stumbling into solve: very low (less than 1 in 100,000 random sequences). The mechanic also requires *understanding* simultaneity, which a random agent has no way to discover. Per NovaPlay §3.5, L3 should require model-formation; this level meets that bar.
  - **(b) Human-tractable**: ~3 minutes. The player observes 3 emitters of distinct colours, 1 multi-colour resonator with `red+blue` pips above it, 1 green-resonator, and 1 phase-delay tile. They first try the strategy that worked at L2: "arm everything, fire". They observe: green-resonator activates (green ring arrives at correct distance/tick), but multi-resonator stays inactive — yet during the animation, they SEE the red ring sweep over (5, 5) on tick 6 and the blue ring on tick 7. This is the discovery cue for "simultaneity matters". They look at the unused phase-delay tile, click it, see it light up, and infer "this must delay something". They arm everything again and fire — multi-resonator activates this time. Total ~3 minutes.
  - **(c) Planning depth (post-discovery)**:
    - *Decision space at level start*: at least **5** valid first actions — toggle phase-delay-tile, arm emitter_red, arm emitter_blue, arm emitter_green, fire (immediately, with no emitters armed). With 18-step budget, the player has many subset-of-arm orderings to consider plus the question of when to engage the delay tile.
    - *Trivial heuristic that fails*: "arm every emitter, fire immediately" — this fails the multi-colour resonator due to the `red, blue` ticks 6-and-7 mismatch (the heuristic is the most natural extension of the L2 strategy; it succeeds on the green-resonator but not the multi-resonator). The post-discovery player who has fully grasped M3 still has to *plan* — they must set up the delay tile BEFORE arming, because once the burst is fired, rings can't be retroactively delayed.
    - *Where the heuristic diverges from the witness*: after arming all 3 and firing (the heuristic), the multi-resonator's per-tick multiset history has `{red}` on tick 6 and `{blue}` on tick 7 — never both at once. The witness corrects this by interposing one extra action (toggle delay tile) BEFORE the fire. The heuristic gets the budget down by 1 step but fails the win condition; even if the player corrects on a second fire (toggle tile then re-arm-fire = 5 more actions, not just 1 + fire because fire disarms emitters), they have spent 6 + 4 = 10 actions where the witness needed 5. The penalty teaches the post-discovery player that *planning the order of actions* matters — toggle the tile FIRST, then arm + fire.
  - **(d) Step budget**: 18 (witness = 5). Generous slack of 13 steps to recover from a single failed strategy attempt (e.g., the "fire without delay" heuristic costs 4 + 1 = 5 actions; a recovery requires re-toggle + re-arm × 3 + re-fire = 5 more, total 10; budget 18 leaves room).

## 5. Action mapping

`available_actions = [5, 6]`. Click + modal verb = "mixed input" family (~12/25 of reference games per `cross-cut-frequencies.md`).

- **`ACTION5`** ("BURST"): simultaneously fire every armed emitter. Emitters become disarmed after firing (one-shot per fire). Initiates the multi-tick fire animation:
  - Each tick, every active ring's radius advances by 1 (or holds if a phase-delay tile in its current footprint hasn't yet delayed it).
  - At the moment a ring's radius first equals Manhattan(emitter, resonator), the resonator records a "hit" with the ring's colour for that tick.
  - At the end of each tick, each resonator checks if its per-tick hit-set equals its required-multiset; if so, the resonator activates permanently.
  - Animation ends when all rings have left the grid (radius > `2 * grid_size + 2 = 26` for safety), at which point `complete_action()` is called.

- **`ACTION6`** ("CLICK"): pixel coords `(x, y)` flow through `camera.display_to_grid` into a grid coordinate `(gx, gy)`. The game checks `level.get_sprite_at(gx, gy, ...)`:
  - If the clicked sprite has tag `armable` → toggle the emitter's arm-state (visible centre-dot transition).
  - Else if the clicked sprite has tag `togglable` → toggle the phase-delay tile's active-state (visible 4-corner-dot vs solid-filled transition).
  - Else (clicked empty cell, padding, resonator, pip, or out-of-bounds) → no-op. Still consumes 1 step from the budget.

No context-dependent gating: `_get_valid_actions` returns the inherited default. Both ACTIONS are always valid.

## 6. HUD and per-game state

### HUD
- **`StepCounterHud(RenderableUserDisplay)`**: a depleting bar at the bottom row (frame row 63, full 64 columns). Per `cross-cut-frequencies.md`, this is the universal pattern (25/25 reference games). Bar background is `4 (dark grey)`; the active "remaining" portion is `11 (yellow)`. Each step decrements the counter; when 0 reached, `self.lose()` fires. Initialized from `level.get_data("step_budget")`.

### Per-game internal state
- `self._armed_emitters: set[Sprite]` — set of currently-armed emitter sprites. Mutated on each ACTION6 click on an armable sprite. Reset to empty at level start and after every burst (on ACTION5).
- `self._delay_tiles_active: set[(int, int)]` — set of (gx, gy) cells whose phase-delay tile is currently active. Mutated on each ACTION6 click on a togglable sprite. Reset to empty at level start.
- `self._anim_active: bool` — true while a fire-burst animation is in progress.
- `self._active_rings: list[Ring]` — list of currently-active rings. Each Ring holds `(emitter_sprite, emitter_colour, current_radius, passed_tiles: set, animation_tick)`. The list is populated at the start of each ACTION5 burst (one Ring per armed emitter) and rings are removed as they leave the grid.
- `self._resonator_per_tick_hits: dict[Sprite, dict[int, set[int]]]` — for each resonator sprite, a map from animation_tick → set of colours that struck it on that tick. Reset to empty at every burst start.
- `self._activated_resonators: set[Sprite]` — sticky set of activated resonators (persist across animation ticks but RESET at level start).
- `self._steps_remaining: int` — depleting counter; initialised from `level.get_data("step_budget")`, decremented on every action (counted before action is processed for the burst-reset semantics).

### Frame visualisation (animation)
- `self._ring_overlay: Sprite` — the level-sized overlay sprite. Cleared (all -1) at every animation tick start; repainted to mark each active ring's footprint cells (cells at exact distance `current_radius` from each ring's emitter), one cell at a time, with the ring's colour. Cells already occupied by a non-overlay sprite (emitter, resonator, pip, phase-delay tile) are skipped (overlay leaves -1 for those cells).
- The visible expansion of rings tick-by-tick is the player's primary observation channel for the mechanic. This is exactly the "Multi-phase step() with phase-tick sentinels for animations" pattern from `reference-game-patterns.md` § Recurring design moves.

### Visible-state cues (per checklist item 19, "no hidden state")
- **Emitter arm-state** (mutated by ACTION6 on the emitter): persistent visible cue is the centre-dot pixel — `4 (dark grey)` when disarmed, `11 (yellow)` when armed. Stays in effect until the next ACTION6 toggle or the next ACTION5 burst.
- **Phase-delay tile active-state** (mutated by ACTION6 on the tile): persistent visible cue is the 4-corner-dot vs solid-filled-with-white-centre pixel pattern.
- **Resonator activated-state** (latched by simultaneous ring strike): persistent visible cue is the centre filled with `0 (white)` (vs the dark-grey dot when inactive).
- **In-flight ring footprint** (during animation only): rendered each tick to the `ring_overlay` sprite. Rings are inherently transient — they exist only during the burst animation — so the visible cue is the animation itself (per `reference-game-patterns.md` "Animation mandatory for long-distance / multi-step transitions").
- **Per-resonator per-tick hit indicator** (during animation only): when a ring of colour C touches a resonator on tick T, the corresponding pip in the resonator's multiset display flashes briefly (held for ~3 animation ticks) — colour goes from inactive grey to colour C. This is the cue that lets the player see WHICH colours arrived on which tick and infer the simultaneity rule. Implementation: per-pip mutable centre pixel.

## 7. Win condition

`self.next_level()` fires when every resonator sprite tagged `resonator` in the current level has been activated (i.e., is in `self._activated_resonators`). This check runs after every animation tick during a burst (once a resonator activates, it adds to the set; the check fires `next_level` if the set covers every resonator).

For the last level (L3), the engine's `next_level()` auto-fires `self.win()`.

## 8. Lose condition

`self.lose()` fires when `self._steps_remaining == 0` at the start of `step()` (i.e., every action call enters with budget > 0; if it would enter with budget 0, the game has already lost). This is the only failure mode — there is no instant-fail collision or hazard.

## 9. Novelty note

### Closest taxonomy near-misses (read at deep-analysis depth or via taxonomy summary)

- **bx84 (`beam-mirror-reflect`)** — both have an emitter-target topology with optional path-modifying tiles. Concrete distinguishing rule: bx84 fires a SINGLE LINEAR beam routed through static reflectors / filters / prisms; mine fires CONCENTRIC RINGS that expand omnidirectionally and uses MULTISET-SAME-TICK simultaneity for activation (a temporal-coordination puzzle). bx84 has no concept of "target needs N inputs at the same instant"; that is mine's central puzzle.
- **gv47 (`seed-grow-surround-dissolve`)** — both have outward expansion from clicked sources. Concrete distinguishing rule: gv47's expansion produces PERSISTENT REGIONS (cells stay coloured); mine's rings are TRANSIENT (each ring exists only at radius R on tick R, then moves on). gv47 player thinks "what cells get covered"; mine player thinks "what tick each cell is touched simultaneously by which colours".
- **gx7m (`gear-mesh-cascade`)** — both have cascade-like dynamics from a click point. Concrete distinguishing rule: gx7m's cascade propagates rotation through a STATIC mesh-graph of gears (BFS, parity-flip per hop); mine's propagation is GEOMETRIC (Manhattan rings through OPEN SPACE) and TIMED (one cell per animation tick). gx7m has no concept of "ring", "colour multiset", or "phase delay".
- **kp9z (`grain-accumulate-topple`)** — both have player-controlled accumulation toward targets. Concrete distinguishing rule: kp9z accumulates persistent grain counts at cells with overflow rules; mine has no per-cell counts — only resonators care about strike-multisets, and they care via simultaneous-multiset-matching, not numeric accumulation.
- **vn8d (`domino-cascade-topple`, per index summary)** — both have "single click triggers cascade". Concrete distinguishing rule: vn8d's cascade is INSTANT chain-reaction through pre-placed PILLARS (the level layout determines the path); mine's expansion is OMNIDIRECTIONAL across open space (geometry determines path) and TIMED (multi-tick).
- **kn58 (`anchor-pull-magnet`)** — shares "click triggers global one-step effect". Concrete distinguishing rule: kn58 moves all coloured pawns one cell toward the click; mine has no pawns and no movement, only ring-pulse propagation. Different cast, different rules.
- **fz5j (`phase-step-tile`)** — shares "tile-period" surface (cells with timing properties). Concrete distinguishing rule: fz5j is an avatar walking on tiles that pulse open/closed on per-cell periods (avatar-vs-timing puzzle); mine has no avatar, and "delay" is a fixed +1 tick offset on passing rings, not a periodic open/closed schedule. Different cast (avatar vs none) and different role of timing (hazard vs alignment-tool).
- **cd82 (`orbit-fire-paint`)** — shares "fire" verb. Concrete distinguishing rule: cd82's fire is DIRECTIONAL (axial slot → half-canvas paint; diagonal → wedge); mine's is OMNIDIRECTIONAL (concentric ring expanding in all directions). cd82 wins by canvas-pattern matching; mine wins by per-resonator multiset activation. cd82 has no timing alignment.
- **ka59 (`sokoban-explode-chase`)** — shares "outward burst" surface (explode-tiles spray neighbours). Concrete distinguishing rule: ka59's explosion is a 1-tick instantaneous push of adjacent pawns (objects move); mine's ring is a multi-tick travelling wave-front across open space, no objects move. ka59 has multiple controllable pawns and a chaser; mine has no agentness.

### Negative-similarity check verdict

Per the 7-dimension table in `mechanic-pick.md`, the candidate is novel — distinct on the principles axes (visual signature, core dynamic) from every prior. Three dimensions of overlap with bx84 are the most concerning, but two of those are "every step-budget game shares the same kill" and "every "hit-all-targets" game shares the same ask" — weak overlaps. The principles-axis differences (rings vs lines, simultaneity vs routing) are concrete and structural.

### `prior-games/index.md` status

Not empty — contains 22 entries. Compared above against the closest 8 (bx84, gv47, gx7m, kp9z, vn8d, kn58, fz5j, plus the cautionary tale kf42 which is firmly different by visual signature and dynamic). All distinguishing rules are concrete; this candidate qualifies as NOVEL.
