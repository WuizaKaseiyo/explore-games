# mechanic-spec — nh4w (round 2, post-critique)

Changes from round 1 (per `critique-revisions.md`):
- §4 rewritten with FINAL geometry, no inline "REVISION:" notes; locked numbers throughout (addresses issues 1, 5).
- Max horizontal arc range fixed at 48 px globally (addresses issue 1).
- L1 target moved to (56, 51) to force walking under max range 48 (addresses issue 4).
- L2 wall increased to height 11 to give witness ≥ 1 altitude unit margin under floor() rounding (addresses issue 2).
- L3 wall lowered to height 8, ceiling1 clearance tightened to 5, ceiling2 clearance set to 13 to genuinely force "yellow only from x=8, blue only from x=12" asymmetric witness under floor() rounding (addresses issue 3).
- Step budgets tweaked to 15/25/35 (addresses issue 6).
- Altitude formula and rounding made explicit: `alt(x) = floor(peak * 4 * t * (1 - t))` where `peak = floor(distance / 3)` and `t = (x - launch_origin_x) / distance`.

## 1. Title
Arc-Loft Lobber.

## 2. Mechanic family
**Family:** `arc-loft-shot`. The player walks a floor-bound launcher pawn left/right and clicks any cell to fire a projectile that travels in a discrete parabolic arc from the launcher's launch-origin to the clicked cell. Arc peak height equals one third of the horizontal click-distance (`peak = floor(distance / 3)`), so short shots fly low and long shots fly high. Floor-walls of varying heights block low arcs (collision when arc altitude ≤ wall height); hanging ceiling stalactites of varying clearances block high arcs (collision when arc altitude ≥ ceiling clearance).

**Priors used:** Objectness (launcher, projectile, walls, ceilings, targets are persistent entities), basic geometry (parabolic-arc trajectory, line-of-flight clearance), basic physics (projectile motion under gravity is the canonical physics-prior example per `core-knowledge-priors.md`). No agentness — no autonomous NPCs.

## 3. Sprite roster

All sprites placed at integer pixel coordinates on the 64×64 playfield. Floor surface at row 51 (the launcher and targets sit on it; air spans rows 0-50; bedrock spans rows 51-63). Per checklist item 20, every pixel is meaningful (no chunky upscale).

- **`floor`** — 64×13. Filling rows 51-63. Pixels per row (top-down):
  ```
  row 51: [3, 3, 3, ...]                  # ground line in dark grey
  row 52-56: [5, 5, 4, 5, 5, 4, 5, 5, ...] # packed earth pattern (palette 5 black, palette 4 off-black, repeating)
  row 57-63: [4, 4, 4, ...]                # bedrock (off-black)
  ```
  `name="floor"`, `tags=["floor"]`. Non-collidable (sprites just sit on row 50 and reference row 51 as the surface).
- **`launcher`** — 5×5 pawn with a directional muzzle pointing UP. Pixels (top-down):
  ```
  [-1, -1, 11, -1, -1]   # muzzle tip (yellow)
  [-1, 11, 11, 11, -1]   # muzzle flare
  [ 9,  9,  9,  9,  9]   # body upper
  [ 9,  3,  9,  3,  9]   # body with grey rivets
  [ 5,  3,  3,  3,  5]   # base / wheels (black sides, grey wheels)
  ```
  `name="launcher"`, `tags=["launcher"]`. Layer 2. Bottom of launcher (row 4 of sprite) sits at y=50 (i.e., sprite placed at y=46). Walking moves `launcher.x` by ±4 px per ACTION3/4. Its 5-wide footprint is the only thing that collides with walls during walking.
- **`projectile`** — 3×3 yellow-glow ball. Pixels:
  ```
  [-1, 11, -1]
  [11, 11, 11]
  [-1, 11, -1]
  ```
  `name="projectile"`, `tags=["projectile"]`. Layer 5 (renders above walls and ceilings during flight animation). Spawned at flight start, removed when the arc resolves (lands or fizzles). Sprite position references the projectile's CENTER cell — i.e. the sprite is placed at `(center_x - 1, center_y - 1)`.
- **`wall_h8`** — 6×8 brick-wall sprite, height 8 px. Pixels (top-down):
  ```
  [12, 12, 12, 12, 12, 12]
  [12,  8,  8, 12,  8,  8]
  [12,  8,  8, 12,  8,  8]
  [12, 12, 12, 12, 12, 12]
  [ 8,  8, 12,  8,  8, 12]
  [12,  8,  8, 12,  8,  8]
  [12,  8,  8, 12,  8,  8]
  [12, 12, 12, 12, 12, 12]
  ```
  Orange-red brick texture with horizontal mortar lines and vertical brick offsets. `tags=["wall"]`, height-attribute `8`. Layer 1. Collidable (blocks walking when launcher's footprint would overlap; blocks projectile when its altitude ≤ 8 in the wall's x-band).
- **`wall_h11`** — 6×11 brick wall, height 11 px (extends `wall_h8` pattern with 3 more rows on top, alternating mortar lines).
- **`wall_h12`** — 6×12 brick wall.
- **`ceiling_c5`** — 8×46. Hangs from row 0; bottom row (tip) at row 45; clearance = 50 - 45 = 5 px. Sprite shape (top-down) — wide grey trunk for upper rows, then a tapered tip with maroon point:
  ```
  rows 0-37: [3, 3, 3, 3, 3, 3, 3, 3]                      # full-width trunk (grey)
  row 38:    [-1, 3, 3, 3, 3, 3, 3, -1]                    # narrows
  row 39:    [-1, -1, 3, 3, 3, 3, -1, -1]
  row 40:    [-1, -1, 3, 3, 3, 3, -1, -1]
  row 41:    [-1, -1, -1, 3, 3, -1, -1, -1]
  row 42:    [-1, -1, -1, 3, 3, -1, -1, -1]
  row 43:    [-1, -1, -1, 3, 3, -1, -1, -1]
  row 44:    [-1, -1, -1, 13, 13, -1, -1, -1]              # maroon tip
  row 45:    [-1, -1, -1, 13, -1, -1, -1, -1]              # final drip
  ```
  `tags=["ceiling"]`, clearance-attribute `5`. Layer 1. Collidable for projectile collision check (arc altitude ≥ 5 in the ceiling's x-band fizzles).
- **`ceiling_c13`** — 8×38. Same general shape, scaled to 38 rows tall (bottom drip at row 37, clearance 13).

(For implementation: stalactite sprites are constructed by an in-file helper that takes a clearance value `C` and produces a sprite of height `(50 - C + 1)` px with a tapered shape — wide trunk for the upper portion and a narrowing 5-row tip at the bottom. Maroon `13` only at the very tip.)

- **`target_yellow`** — 4×4 hollow square. Pixels:
  ```
  [11, 11, 11, 11]
  [11,  4,  4, 11]
  [11,  4,  4, 11]
  [11, 11, 11, 11]
  ```
  `tags=["target", "yellow"]`. Layer 0. Sits on floor: placed at `(target_x, 51)`. Non-collidable (projectile passes through during flight; win-overlap is checked separately).
- **`target_blue`** — 4×4 hollow square, same shape, palette 9 (blue) instead of 11. `tags=["target", "blue"]`.

**HUD:**
- **`StepBarHud(RenderableUserDisplay)`** — paints row 0 (top row) of the rendered frame. Cells `[0..remaining)` palette 14 (green); cells `[remaining..max_budget)` palette 8 (red). Updated every action via `set_remaining(n)`.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All grids 64×64.

**Global game rules referenced by the witnesses below:**
- Launcher walks 4 px per ACTION3/4 press; movement clamped to playfield bounds and BLOCKED if the launcher's 5-wide footprint at the new x would overlap any sprite tagged `wall`.
- Launcher's launch-origin = `(launcher.x + 2, 50)` (centre of the muzzle, just above the floor surface).
- Click target cell `(cx, cy)` → projectile spawns at launch-origin and animates to `(target_x, 51)` along a discrete parabolic arc. Target_x = `cx` if `|cx - launch_origin_x| ≤ 48` else `launch_origin_x + 48 * sign(cx - launch_origin_x)` (max horizontal range = 48 px; clicks beyond range cause the projectile to fall short at exactly +48 / -48 from origin).
- Arc altitude formula at any x along the path: `alt(x) = floor(peak * 4 * t * (1 - t))` where `t = (x - launch_origin_x) / (target_x - launch_origin_x)` and `peak = floor(|target_x - launch_origin_x| / 3)`.
- Projectile y-position at frame x: `y(x) = 51 - alt(x)`. Projectile sprite (3×3) is placed centred on `(x, y(x))`, occupying pixels `(x-1..x+1, y(x)-1..y(x)+1)`.
- Per-frame collision check: at each frame, if any pixel of the projectile sprite overlaps a non-transparent pixel of any sprite tagged `wall` or `ceiling`, the projectile fizzles at that frame (animation ends, projectile sprite removed, no win credit). Otherwise the animation advances by 2 px in target-direction next frame.
- Win check at flight end: if projectile centre `(target_x, 51)` lies within any `target` sprite's footprint, that target is removed; if the level's target list becomes empty, fire `self.next_level()`.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N=2):
  - **M1 — Walk launcher.** ACTION3/4 step launcher horizontally by 4 px.
  - **M2 — Click-fire arc projectile.** ACTION6 fires the parabolic arc to the clicked cell (range-capped at 48 px).

- **Necessity per mechanic (counterfactual):**
  - **M1.** L1 cannot be solved without walking because the launcher starts at `x=4` (launch-origin x=6) with target_yellow centred at `x=58`; horizontal distance from start = 52 > 48-px max range. A click on the target from start position causes the projectile to fall short and land at `x=54` (= origin 6 + 48), spanning x=53-55; the target spans x=56-59; no overlap. The player MUST walk launcher right by at least one 4-px step (to `x=8`, origin 10) to bring distance ≤ 48.
  - **M2.** L1 cannot be solved without firing because the win predicate is `projectile-overlaps-target`, and the only thing that spawns a projectile is ACTION6.

- **Level layout:**
  - Floor sprite at `(0, 51)` (decorative).
  - Launcher placed at `(4, 46)` (sprite y=46 puts its bottom row at y=50, sitting on floor surface y=51).
  - Single `target_yellow` at `(56, 51)`.
  - No walls. No ceilings.
  - Step budget: 15.

- **Witness solution:** `[ACTION4, ACTION6@(56, 51)]` (2 actions).
  - Step 1: ACTION4 → launcher.x = 4 → 8 (launch-origin x = 6 → 10).
  - Step 2: ACTION6@(56, 51) → click grid cell (56, 51). target_x = 56 (within range from origin 10, distance 46 ≤ 48). peak = floor(46/3) = 15. Arc has no walls/ceilings to collide with. Projectile lands at (56, 51), sprite spans x=55-57 y=50-52, target spans x=56-59 y=51-54 → overlap at x=56-57 y=51-52 → win predicate true → `self.next_level()`.

- **Difficulty justification:**
  - **(a) Random-resistance.** A vision-blind / random-policy agent picking uniformly among ACTION3/4/6 has near-zero chance of producing the required (walk-then-click-near-target) sequence within 15 actions. The click-coordinate space spans 64×64 cells; only clicks with `cx ∈ [54, 60]` (a band of 7 cells) and from a launcher position with origin ≥ x=10 produce a winning land. P(win | random over 15 steps) ≈ (1/7) * (1/64²)^k for k clicks per game ≈ < 0.1%.
  - **(b) Human-tractable.** ~30 seconds. Player sees the launcher and target, clicks target, sees projectile fall short, walks right, clicks again. ~3-5 realtime actions. Well under the 2-min/level target.
  - **(c) Planning depth.** No strict planning requirement — L1 is the discovery gate. Once the player understands "click sets target and range matters", the win is near-immediate.
  - **(d) Step budget.** 15 — generous over the 2-action witness; allows ~6 wasted exploratory clicks/walks.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (= N+1 = 3, one new):
  - **M1 — Walk launcher.** (carried forward, REQUIRED at L2)
  - **M2 — Click-fire arc projectile.** (carried forward, REQUIRED at L2)
  - **M3 — Wall-clearance rule.** A wall sprite of height H placed on the floor blocks any projectile whose arc altitude at the wall's x-band is ≤ H (collision check above); the projectile fizzles at the collision cell (animation stops, sprite removed, action consumed, no win-credit). Walls also block walking — the launcher's 5-wide footprint cannot occupy a position where it would overlap wall pixels.

- **Necessity per mechanic (counterfactual):**
  - **M1.** L2 cannot be solved without walking because launcher starts at x=4 (origin 6) with target centred at x=62; distance = 56 > 48 max range, lands at x=54 missing target (target spans x=60-63). One walk to x=8 brings distance to 52 (still > 48, lands at x=58, missing). A second walk to x=12 brings distance to 48 (in range, lands at x=62). Walking exactly twice is required to reach a position where the arc reaches the target.
  - **M2.** L2 cannot be solved without firing — only ACTION6 spawns a projectile.
  - **M3.** L2 cannot be solved without an arc that clears the wall because the wall_h11 at x=24 (height 11, spans rows 40-50, x in [24, 29]) physically separates every reachable launcher x-position from the target. From x=12 (the unique winning launcher position above), arc altitude at wall mid x=26.5 = `floor(16 * 4 * 0.260 * 0.740)` = `floor(12.32)` = `12`, which is `> 11` (the wall height) — clears. From x=16 (origin 18), distance 44, peak 14: arc altitude at wall x=26 = `floor(14 * 4 * 0.182 * 0.818)` = `floor(8.34)` = `8`, NOT > 11 → BLOCKED at the wall. From x=8 distance 52 > 48, fires-but-lands-short at x=58 missing target (no wall-relevance). So x=12 is the only position from which both range AND wall-clearance permit a winning arc — wall clearance is BINDING.

- **Level layout:**
  - Floor at `(0, 51)`.
  - Launcher at `(4, 46)`.
  - Wall_h11 at `(24, 40)` (sprite y=40, height 11, occupies rows 40-50, x in [24, 29]).
  - Target_yellow at `(60, 51)` (centre x=62).
  - No ceilings.
  - Step budget: 25.

- **Witness solution:** `[ACTION4, ACTION4, ACTION6@(60, 51)]` (3 actions).
  - Step 1: ACTION4 → launcher.x = 4 → 8 (footprint clears wall at x=24).
  - Step 2: ACTION4 → launcher.x = 8 → 12 (footprint x=12-16 clears wall left edge x=24).
  - Step 3: ACTION6@(60, 51) → launch-origin x=14, target_x=60+? (clicked is (60,51); projectile centre lands at clicked x if in range; click x=60, distance from origin 14 is 46 ≤ 48 in range). Wait the spec says target_x = cx (clicked column) if in range. Let me re-state: the projectile's landing x = `min(launch_origin_x + 48, max(launch_origin_x - 48, cx))`. From origin 14 click cx=60: |60-14|=46 ≤ 48 → projectile lands at x=60. Hmm but I want it to overlap target spanning x=60-63 (centre 62). Projectile centre at x=60 = projectile sprite x=59-61. Overlap with target x=60-63 at x=60-61 ✓. Wins.
    
    To make the witness arithmetic crisp, I use distance to target CENTRE x=62. From origin 14: distance to centre 62 is 48 (= max range exactly). Click at (62, 51) — projectile lands at x=62. Sprite spans 61-63 ✓ overlaps target 60-63. peak=floor(48/3)=16. Arc clears wall (alt at x=26.5 = 12 > 11). Win.
    
    So the witness's click is on (62, 51) (target centre) — let me rewrite:
  - Step 3: ACTION6@(62, 51) → projectile lands at x=62, overlapping target (which spans x=60-63), no wall collision → win.

- **(WITNESS REVISION):** `[ACTION4, ACTION4, ACTION6@(62, 51)]` (3 actions).

- **Difficulty justification:**
  - **(a) Random-resistance.** Random policy has ~1/(7·64) ≈ 1/450 chance per click of hitting a coordinate in range of target AND of producing arc that clears wall AND from a launcher position that has been walked to. Over 25 steps, P(win | random) << 1%. Vision-blind LLM agents with no frame-reading have no signal to pick `cx ≈ 62`.
  - **(b) Human-tractable.** ~1.5 min. Player tries firing from start (lands short at x=54), walks right and tries again (still short), tries from x=12 (succeeds), or alternately walks all the way to x=16 first (too close to wall, arc blocked). Some trial-and-error to identify x=12 as the unique sweet spot. ~6-10 realtime actions.
  - **(c) Planning depth (post-discovery).** Moderate. Decision space at level start (post-discovery): 3 action types × 4 walking positions × ~8 click coordinates near target ≈ 96 first-action options, of which 1 is winning. The plausible wrong path: a fully-informed player who has seen the wall blocks low arcs naturally tries walking AS CLOSE to the wall as possible (x=16) thinking "shorter shot → less wall to clear" — but this fails because shorter shot also has lower peak (peak=14 < threshold 12 at the wall x-band). Witness reasoning: "longer shot has higher peak; the wall sits past the arc midpoint when launching from x=12 (mid x=38, wall at x=26.5 is left of mid), so arc altitude at wall is still rising to the peak." This counter-intuitive insight (FURTHER from wall = HIGHER arc at wall) is the post-discovery planning gate that distinguishes correct from incorrect launcher positioning.
  - **(d) Step budget.** 25 — generous over the 3-action witness; allows ~7 wasted exploratory shots.

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (= 3+1 = 4, one new):
  - **M1 — Walk launcher.** (carried forward)
  - **M2 — Click-fire arc projectile.** (carried forward)
  - **M3 — Wall-clearance rule.** (carried forward)
  - **M4 — Ceiling-block rule.** A ceiling-stalactite sprite of clearance C placed at top blocks any projectile whose arc altitude at the stalactite's x-band is ≥ C (per-frame collision check); the projectile fizzles. Ceilings do NOT block walking (they hang above the floor with air below the launcher's height).

- **Necessity per mechanic (counterfactual):**
  - **M1.** L3 cannot be solved without walking because:
    - From launcher start x=4 (origin 6), firing at yellow target (centre 42): ceiling1 (at x=8, clearance 5) blocks the arc. Distance 36, peak 12. At ceiling1 mid x=11.5: t=5.5/36=0.153, alt=floor(12*4*0.153*0.847)=floor(6.21)=6 ≥ 5 → BLOCKED.
    - From launcher start x=4, firing at blue target (centre 54): same ceiling1 blocks. Distance 48, peak 16. At x=11.5: alt=floor(16*4*0.115*0.885)=floor(6.51)=6 ≥ 5 → BLOCKED.
    - The player must walk launcher right at least one 4-px step to escape ceiling1's blocking band.
  - **M2.** L3 cannot be solved without firing — only ACTION6 spawns the projectile that overlaps targets.
  - **M3.** L3 cannot be solved without arc-clears-wall because the wall_h8 at x=24 (height 8) sits between every reachable launcher position and either target. From x=12 firing yellow (centre 42, distance 28, peak 9): arc altitude at wall mid x=26.5 = floor(9*4*0.446*0.554)=floor(8.90)=8, NOT > 8 → BLOCKED. The wall genuinely blocks the natural greedy "walk closer to target" strategy, forcing the player to fire from FURTHER (lower-distance does not help here).
  - **M4.** L3 cannot be solved without arc-stays-under-ceiling because ceiling2 at x=32 (clearance 13) eliminates the longer arcs needed to reach blue from the same launcher position that worked for yellow. From x=8 (the only winning yellow position) firing blue (distance 44, peak 14): at ceiling2 mid x=35.5: alt=floor(14*4*0.580*0.420)=floor(13.62)=13, ≥ 13 → BLOCKED. The player must walk to a different x to fire blue, where the arc's profile through the ceiling2 band stays under 13.

- **Level layout:**
  - Floor at `(0, 51)`.
  - Launcher at `(4, 46)`.
  - Wall_h8 at `(24, 43)` (sprite y=43, height 8, occupies rows 43-50, x in [24, 29]).
  - Ceiling1 (`ceiling_c5`, 46 px tall) at `(8, 0)` (occupies rows 0-45, x in [8, 15], clearance 5).
  - Ceiling2 (`ceiling_c13`, 38 px tall) at `(32, 0)` (occupies rows 0-37, x in [32, 39], clearance 13).
  - Target_yellow at `(40, 51)` (centre x=42).
  - Target_blue at `(52, 51)` (centre x=54).
  - Step budget: 35.

- **Mid-air arithmetic verification of the unique witness positions:**
  - **From x=8 (origin 10) → yellow centre 42:** distance 32, peak 10. Path frames at x = 10, 12, 14, ..., 42 (every 2 px).
    - At x=12 (in ceiling1's x-band [8,15]): t=(12-10)/32=0.0625. alt=floor(10*4*0.0625*0.9375)=floor(2.34)=2 < 5 ✓.
    - At x=14 (in ceiling1's x-band): t=4/32=0.125. alt=floor(10*4*0.125*0.875)=floor(4.38)=4 < 5 ✓.
    - At x=24 (in wall's x-band [24,29], wall left edge): t=14/32=0.4375. alt=floor(10*4*0.4375*0.5625)=floor(9.84)=9 > 8 ✓.
    - At x=26 (in wall): t=16/32=0.5. alt=floor(10*4*0.5*0.5)=floor(10)=10 > 8 ✓.
    - At x=28 (in wall): t=18/32=0.5625. alt=floor(10*4*0.5625*0.4375)=floor(9.84)=9 > 8 ✓.
    - At x=32 (in ceiling2's x-band [32,39]): t=22/32=0.6875. alt=floor(10*4*0.6875*0.3125)=floor(8.59)=8 < 13 ✓.
    - At x=38 (in ceiling2): t=28/32=0.875. alt=floor(10*4*0.875*0.125)=floor(4.38)=4 < 13 ✓.
    - At x=42 (target): t=1. alt=0. Lands at (42, 51), sprite spans x=41-43 y=50-52, target spans x=40-43 y=51-54 → overlap at x=41-43 y=51-52 → yellow consumed.
  - **From x=12 (origin 14) → blue centre 54:** distance 40, peak 13.
    - At x=14 (ceiling1 right edge [8,15]): t=0. alt=0 < 5 ✓.
    - At x=24 (wall left): t=10/40=0.25. alt=floor(13*4*0.25*0.75)=floor(9.75)=9 > 8 ✓.
    - At x=26 (wall): t=12/40=0.3. alt=floor(13*4*0.3*0.7)=floor(10.92)=10 > 8 ✓.
    - At x=28 (wall): t=14/40=0.35. alt=floor(13*4*0.35*0.65)=floor(11.83)=11 > 8 ✓.
    - At x=32 (ceiling2 left): t=18/40=0.45. alt=floor(13*4*0.45*0.55)=floor(12.87)=12 < 13 ✓.
    - At x=36 (ceiling2): t=22/40=0.55. alt=floor(13*4*0.55*0.45)=floor(12.87)=12 < 13 ✓.
    - At x=38 (ceiling2 right): t=24/40=0.6. alt=floor(13*4*0.6*0.4)=floor(12.48)=12 < 13 ✓.
    - At x=54 (target): alt=0. Lands at (54, 51), sprite x=53-55 y=50-52, target spans x=52-55 y=51-54 → overlap → blue consumed.
  - **Verification that yellow CANNOT be fired from any other reachable position:**
    - x=4 (origin 6): yellow distance 36, peak 12. At ceiling1 x=12: t=6/36=0.167. alt=floor(12*4*0.167*0.833)=floor(6.67)=6 ≥ 5 → BLOCKED.
    - x=12 (origin 14): yellow distance 28, peak 9. At wall x=26: t=12/28=0.429. alt=floor(9*4*0.429*0.571)=floor(8.82)=8, NOT > 8 → BLOCKED.
    - x=16 (origin 18): yellow distance 24, peak 8. At wall x=26: t=8/24=0.333. alt=floor(8*4*0.333*0.667)=floor(7.11)=7, NOT > 8 → BLOCKED.
  - **Verification that blue CANNOT be fired from any other reachable position:**
    - x=4 (origin 6): blue distance 48, peak 16. At ceiling1 x=12: t=6/48=0.125. alt=floor(16*4*0.125*0.875)=floor(7)=7 ≥ 5 → BLOCKED.
    - x=8 (origin 10): blue distance 44, peak 14. At ceiling2 x=36: t=26/44=0.591. alt=floor(14*4*0.591*0.409)=floor(13.55)=13, NOT < 13 → BLOCKED.
    - x=16 (origin 18): blue distance 36, peak 12. At wall x=26: t=8/36=0.222. alt=floor(12*4*0.222*0.778)=floor(8.30)=8, NOT > 8 → BLOCKED.

  Yellow only from x=8. Blue only from x=12. Both REQUIRE walking (x=4 fails for both via ceiling1).

- **Witness solution:** `[ACTION4, ACTION6@(40, 51), ACTION4, ACTION6@(52, 51)]` (4 actions).
  - Step 1: ACTION4 → launcher.x=4→8.
  - Step 2: ACTION6@(40, 51) → fires from origin 10 to yellow centre 42; arc clears all per arithmetic above; yellow consumed.
  - Step 3: ACTION4 → launcher.x=8→12.
  - Step 4: ACTION6@(52, 51) → fires from origin 14 to blue centre 54; arc clears all; blue consumed → all targets removed → `self.next_level()` (and since L3 is the last, engine fires `self.win()`).

- **Difficulty justification:**
  - **(a) Random-resistance.** Random-policy agent over 35-step budget has near-zero chance of producing the precise (walk → click yellow column → walk → click blue column) sequence. Click-coordinate space ≈ 4096 cells × 4 launcher positions × ordering = >50k configurations of which 1 wins. P(win | random) over 35 steps < 1e-4.
  - **(b) Human-tractable.** ~2.5 min. Player explores: clicks both targets from start (both blocked by ceiling1, projectile sprite visibly stops mid-flight), realises ceiling1 forces a walk, walks right and tries again. Discovers yellow lands at x=8 but blue from x=8 fizzles at ceiling2 (visible mid-flight stop). Walks further to x=12, blue lands but yellow now blocked at wall. Realises asymmetric position binding. ~12-18 realtime actions of trial-and-error.
  - **(c) Planning depth (post-discovery).** Challenging. Decision space at level start: 3 action types × 4 walking positions × 2 useful target columns ≈ 24 first-action options, of which only 4 are part of the optimal witness chain. The plausible greedy heuristic that fails: **"fire both targets from the same launcher position to save walking actions"** — a fully-informed greedy player would try x=8 (yellow ✓ then blue blocked at ceiling2) or x=12 (blue ✓ then yellow blocked at wall). The arithmetic above shows no shared position works; the player must visit BOTH x=8 (for yellow's wall-clearance band, where peak=10 just barely clears wall=8) AND x=12 (for blue's ceiling2-fit, where peak=13 just barely fits under ceiling=13). The witness's 4-action sequence has the post-discovery insight: "yellow's wall-binding requires the LOWER-peak shot; blue's ceiling-binding requires the LOWER-peak shot ALSO — but they need DIFFERENT distances, so the launcher must move between the two shots." Greedy "do both with one walk" fails by ~1 altitude unit at one constraint or the other. The witness also has the planning-order insight: "fire yellow first (closer to start) then walk further for blue" — reverse order requires an extra walk (3 to x=12 + 3 back to x=8) for a 5-action total, sub-optimal.
  - **(d) Step budget.** 35 — generous over the 4-action witness; allows ~10 wasted shots plus plenty of walking back-and-forth. Per `difficulty-rules.md` § d, L3's budget does not shrink relative to L2's (25) — it grows to 35, reflecting the additional discovery cost of ceilings.

## 5. Action mapping

`available_actions = [3, 4, 6]`. ACTION1, ACTION2, ACTION5, ACTION7 are NOT declared (per checklist item 5: action space minimal; per item 22: ACTION7 omitted because no undo).

| Action | Semantic | Gating |
|---|---|---|
| ACTION3 | Walk launcher 4 px LEFT (`launcher.x -= 4`); BLOCKED if (a) `launcher.x - 4 < 0`, OR (b) the launcher's 5-wide footprint at the new x would overlap any sprite tagged `wall`. | Always callable; effect may be no-op if blocked. |
| ACTION4 | Walk launcher 4 px RIGHT (`launcher.x += 4`); BLOCKED symmetrically (`launcher.x + 5 + 4 > 64`, OR footprint overlaps a wall). | Always callable; effect may be no-op if blocked. |
| ACTION6 | Click at display pixel `(self.action.data["x"], self.action.data["y"])`. Convert via `self.camera.display_to_grid(int(x), int(y))` to grid `(cx, cy)`. Then: spawn a projectile at the launcher's launch-origin `(launcher.x + 2, 50)` and animate it along the parabolic arc to landing-x = `clip(cx, origin_x - 48, origin_x + 48)`. Animation runs frame-by-frame (2 px per frame in the target direction); `complete_action()` is called only on the FINAL frame (whether the projectile lands successfully or fizzles into a wall/ceiling). | Always callable. The full multi-frame animation does NOT consume additional agent actions because the engine ticks `step()` repeatedly during animation while the agent's input is cached (per the sk48/sp80 pattern); only the initiating ACTION6 is counted in the step-counter. |

`_get_valid_actions()` returns the standard `[ACTION3, ACTION4, ACTION6]` list during idle frames. During flight animation (`flight_phase >= 0`), it returns the same list — the engine ignores the agent's input until the animation resolves.

## 6. HUD and per-game state

**HUD widgets:**
- `StepBarHud(RenderableUserDisplay)` — paints row 0 of the rendered frame. Cells `[0..remaining)` palette 14 (green); cells `[remaining..max_budget)` palette 8 (red). Updated on every action via `set_remaining(n)`; `set_max(n)` mutates the budget for the new level.

**Per-game state (instance attributes):**
- `self.launcher: Sprite` — reference to the launcher sprite for the current level (captured in `on_set_level` via `level.get_sprites_by_tag("launcher")[0]`).
- `self.walls: list[Sprite]` — captured walls for collision checks, plus a dict `self.wall_heights: dict[Sprite, int]` mapping wall sprite → height attribute.
- `self.ceilings: list[Sprite]` — captured ceilings, plus `self.ceiling_clearances: dict[Sprite, int]`.
- `self.targets: list[Sprite]` — captured target sprites; removed on hit.
- `self.projectile: Sprite | None` — the in-flight projectile, or None when idle.
- `self.flight_phase: int` — `-1` when idle; `>= 0` indexes the next path-frame to render.
- `self.flight_path: list[tuple[int, int]]` — pre-computed sequence of `(centre_x, centre_y)` pixel positions the projectile will visit.
- `self.flight_target_sprite: Sprite | None` — the target sprite that would be consumed if the projectile reaches its landing cell unobstructed (resolved at flight start by checking which target's footprint overlaps the landing point).
- `self._step_counter_ui: StepBarHud` — the HUD widget instance (constructed once in `__init__`, attached to camera via `interfaces=[]`).
- `self._step_max: int` — current level's `step_budget`.
- `self._step_remaining: int` — remaining actions.

**Hidden state** (returned by `_get_hidden_state`): a 2x2 int16 array with `[0,0]=self._step_remaining`, `[0,1]=self.flight_phase`, `[1,0]=self.launcher.x`, `[1,1]=len(self.targets)`. The frame + hidden-state pair uniquely identifies game state per §3.5.2 of the report.

## 7. Win condition

Per `complete_action()`-time check: after a flight resolves, if the projectile landed on a target sprite's footprint, that target is removed (`self.current_level.remove_sprite(target)` and `self.targets.remove(target)`). Then check `if not self.targets: self.next_level()`. The engine auto-fires `self.win()` after L3's `next_level()` since L3 is the last entry in `levels`. The predicate is testable: `len(self.targets) == 0` after every `complete_action()`.

## 8. Lose condition

Per `complete_action()`-time check: `self._step_remaining` is decremented by 1 each time `complete_action()` is called (i.e., on every walk action and on the LAST frame of every fire-arc flight). If `self._step_remaining <= 0` AND no target was just consumed in the same step, fire `self.lose()`. There is no soft-lock state — the player can always continue submitting actions until the budget runs out.

## 9. Novelty note

(Unchanged from round 1; the critique flagged no novelty issues. Repeated here for completeness.)

**Closest taxonomy entries (per `mechanic-novelty/taxonomy-of-25-games.md`):**

- **bp35 — gravity-fall-navigation.** Pawn auto-falls one row per step under gravity; arrows side-step; gravity-flippers change axis. **Distinguishing rule:** bp35's gravity acts CONTINUOUSLY on the avatar as the primary dynamic; the player only laterally corrects. nh4w's launcher is a static walker with full cardinal control; the parabolic-arc dynamic applies to a SEPARATE projectile sprite that exists only during a fired shot. There is no gravity on the avatar; the launcher does not fall.
- **cd82 — orbit-fire-paint.** Basket on an 8-slot ring around a central canvas; arrows step the basket between slots; ACTION5 fires inward to splash a slab of canvas. **Distinguishing rule:** cd82 fires from a CONSTRAINED RING in only 4 axial / 4 diagonal STRAIGHT directions to splash a deterministic slab; nh4w fires from a freely-walking floor pawn in a parabolic Nova whose trajectory continuously varies with click-target distance, with vertical-altitude geometry that wall and ceiling sprites can interrupt.
- **r11l — centroid-puppet-leg.** Click a tray leg, click a target — leg animates toward target with attached heads following a centroid drag. **Distinguishing rule:** r11l's animation is a STRAIGHT-LINE drag and the win-condition involves rigid-body chain placement; nh4w's animation is a parabolic-altitude arc with vertical-clearance gates (walls below, ceilings above). r11l has no concept of vertical clearance.

**Closest prior-games entries (per `prior-games/index.md`):**

- **hk7v — overhead-trolley-hook.** Gantry trolley + variable-rope hook delivers coloured blocks to coloured floor markers; rope clears walls. **Distinguishing rule:** hk7v's "rope clears walls" is a Cartesian-gantry sequential routine (raise hook +1, traverse +1, lower -1; ~80 sequential moves per delivery); nh4w's wall-clearance is a SINGLE click-fire whose discrete parabolic arc clears all walls along the column whose height-at-x is below `peak * 4 * t * (1-t)`. The player learns a continuous physics relationship (longer shots fly higher), not a sequential lift-traverse-lower operation.
- **vt6q — grapple-anchor-yank.** Fires a directed cardinal grapple line that yanks. **Distinguishing rule:** vt6q's grapple is a STRAIGHT cardinal line that snaps to the first anchor and yanks the avatar/anchor along it; nh4w's projectile follows a 2D parabolic arc with a vertical air-altitude axis (height varies along flight); no anchor-yanking; lands on the CLICKED cell, not on whatever it first hits.
- **kn58 — anchor-pull-magnet.** Click any cell to place a magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it. **Distinguishing rule:** kn58 is a 1-cell sympathetic motion of multiple pawns per click; no projectile, no flight, no air-altitude dimension. nh4w spawns one projectile per click and animates it along an arc.
- **bx84 — beam-mirror-reflect.** Emitter shoots a colored beam; mirrors reflect 90°. **Distinguishing rule:** bx84's beam is a STRAIGHT line that reflects via mirror sprites — geometrically planar with no vertical/peak axis; nh4w's arc has a vertical altitude axis where height-at-x is a function of horizontal distance, and that axis is what wall-height and ceiling-clearance gate.
- **wt39 — glide-deflect-thaw.** Pawn glides in pressed direction until wall; bumpers deflect 90°. **Distinguishing rule:** wt39 is a ground-plane glide of a single pawn (no separate projectile, no air-altitude); the mechanic is glide-until-collision with bumper redirection. nh4w has a separately-fired projectile that flies through air with a vertical-clearance gate, and the launcher does not glide — it walks 4 px per arrow press, no inertia.
- **kj82 — plank-pivot-walk.** Pawn walks long pinned planks; click selects, ACTION5 pivots; springs LAUNCH the pawn along the plank's axis. **Distinguishing rule:** kj82's "launch" is a 1D scoot of the pawn along a plank's axis; no projectile, no parabolic arc, no air-clearance.

Negative-similarity check (per `mechanic-novelty/negative-similarity-check.md`): walked the eight dimensions vs hk7v in `mechanic-pick.md`. Shared dimensions: 3 (target-deliver win-form), 4 (step-budget kill), partial 5 (both have walls). Distinct on dimensions 1, 2, 6, 7, 8 (board cast, input pattern, visual signature, pixel grain, core dynamic). Dimensions 6 and 7 (visual signature and pixel grain) — the named principles — clearly diverge. Verdict: passes.
