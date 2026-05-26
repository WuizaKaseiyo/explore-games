# Mechanic Spec — bx84

## 1. Title

Beam-Mirror-Reflect Puzzle (working title; not visible in-game).

## 2. Mechanic family

`beam-mirror-reflect`. A static emitter shoots a 1-pixel coloured beam in a fixed cardinal direction; the player clicks empty grid cells to drop reflective mirrors and clicks existing mirrors to cycle their orientation, with the beam re-traced from emitter to grid-edge after every click and the level winning when the beam visits every coloured target ring at the matching colour. **Core-knowledge priors used**: objectness (mirrors, filter, prism, targets, emitter as persistent objects with positions and behaviours); basic geometry & topology (right-angle reflection, perpendicular splitting at prisms, target-as-cell-set to "visit"); basic physics (light-as-ray straight-line propagation, reflection, splitting). Agentness is NOT used.

## 3. Sprite roster

- **`emitter`** — 1×1 pixels `[[3]]`. Palette: 3 (grey). Tags: `["emitter"]`. Role: the beam source. The firing direction is stored per-level in `level.data["emit_direction"]` as one of `"east"`, `"west"`, `"south"`, `"north"`. The beam is spawned at `(emitter.x + dx, emitter.y + dy)` where `(dx, dy)` is the unit vector of the direction.

- **`mirror_bs`** — 1×1 pixels `[[7]]`. Palette: 7 (pink). Tags: `["mirror"]`. Role: backslash mirror (`\`); reflects the beam by swapping `(dx, dy)` → `(dy, dx)` (i.e. east↔south, west↔north). The player places this by clicking an empty cell.

- **`mirror_sl`** — 1×1 pixels `[[6]]`. Palette: 6 (magenta). Tags: `["mirror"]`. Role: slash mirror (`/`); reflects the beam by `(dx, dy)` → `(-dy, -dx)` (i.e. east↔north, west↔south). The player obtains this by clicking an existing `mirror_bs` (cycles to `/`).

- **`filter`** — 1×1 pixels `[[9]]`. Palette: 9 (blue). Tags: `["filter"]`. Role: when the beam enters this cell, the beam's colour is set to the filter's own palette value (palette-9, blue) for the rest of the trace (including any subsequent reflections). Pre-placed in the level; not interactable by clicking. Distinguishable from `target_blue` by being a 1×1 solid cell vs a 3×3 hollow ring.

- **`target_yellow`** — 3×3 pixels `[[11, 11, 11], [11, -1, 11], [11, 11, 11]]`. Palette: 11 (yellow). Tags: `["target_yellow"]`. Role: a target ring that becomes "lit" when the beam visits any of its 8 perimeter cells while the beam's current colour is palette-11. Once lit, stays lit (sticky).

- **`target_blue`** — 3×3 pixels `[[9, 9, 9], [9, -1, 9], [9, 9, 9]]`. Palette: 9 (blue). Tags: `["target_blue"]`. Role: target ring; lit when beam visits at palette-9. Sticky.

- **`target_green`** — 3×3 pixels `[[14, 14, 14], [14, -1, 14], [14, 14, 14]]`. Palette: 14 (green). Tags: `["target_green"]`. Role: target ring; lit when beam visits at palette-14. Sticky. Used in L3 only.

- **`prism_es`** — 1×1 pixels `[[12]]`. Palette: 12 (orange). Tags: `["prism"]`. Role: an east+south-splitter prism. When the beam enters this cell, the beam continues in its current direction AND a new perpendicular branch is spawned moving south (one cell south, then south indefinitely). Clicking the prism replaces it with `prism_en` (toggle). Used in L3 only.

- **`prism_en`** — 1×1 pixels `[[13]]`. Palette: 13 (maroon). Tags: `["prism"]`. Role: an east+north-splitter prism. Same as `prism_es` but the perpendicular branch moves north instead of south. Clicking replaces it with `prism_es`. Used in L3 only.

- **`beam_overlay`** — 16×16 pixels (initialised to `[[-1]*16]*16`). Tags: `["beam_overlay"]`. Layer 10 (rendered on top of mirrors/filters but only writes non-`-1` cells, so underlying sprites show through). Role: a per-frame overlay that displays the beam's path. After every click, the beam is re-traced and `beam_overlay.pixels[y, x] = colour` is set for every empty cell the beam visits (cells occupied by emitter / mirror / filter / prism / target are NOT painted on the overlay because the underlying sprite is visible there; the player infers continuity).

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use the same `grid_size = (16, 16)`. The camera viewport is set to `(16, 16)` in `on_set_level` so the engine scales 16×16 → 64×64 at scale 4.

### Level 1 — base dynamic system

Layout: emitter at (1, 8) firing east. `target_yellow` at (8, 11) (occupies cells (8, 11) through (10, 13)). No filter, no prism.

- **Mechanics required by the witness** (N = 1):
  - **M1: mirror placement and cycling.** Click an empty cell to drop a `mirror_bs` (`\`); click a `mirror_bs` to cycle it to `mirror_sl` (`/`); click a `mirror_sl` to remove it. The beam re-traces after every click.

- **Necessity per mechanic** (per checklist item 12):
  - **M1: L1 cannot be solved without triggering M1 because** the beam fires east from (1, 8) along row 8 and exits at (15, 8); the target ring at (8, 11)–(10, 13) is below row 8 and is never visited unless a mirror reflects the beam south at column 8.

- **Witness solution** (the SHORTEST):
  - `[ACTION6@(34, 34)]` — one click at pixel (34, 34) which `display_to_grid` maps to grid cell (8, 8) (since scale=4 and there is no x/y offset for a 16×16 viewport in a 64×64 frame: `x_offset = (64 - 64) // 2 = 0`; `grid_x = 34 // 4 = 8`; `grid_y = 34 // 4 = 8`). This drops `mirror_bs` at (8, 8). The beam re-traces: emitter → (2, 8) east → … → (8, 8) hits `\`, deflects to south → (8, 9), (8, 10), (8, 11) which is a perimeter cell of `target_yellow` (lit at colour 11). Win.

- **Difficulty justification** (per `difficulty-rules.md` § 2):
  - **(a) Random-resistance**: a vision-blind / random-policy agent has 256 possible click cells × the chance of correctly cycling on second-hit ≈ 256 effective placement permutations. Only 1 single cell (8, 8) wins in 1 click; chance per click ≈ 1/256. Even 5 random clicks have < 2% cumulative probability of solving.
  - **(b) Human-tractable**: an attentive human who reads the screen sees beam-from-emitter, the gap between beam-row-8 and target-row-11, and the geometric requirement of an east→south reflection at column 8. Estimated: 30 seconds to a minute to find the cell.
  - **(c) Planning depth**: NONE strictly required post-discovery. Once the player understands "click empty cell → drop pink mirror → beam reflects", the remaining task is direct (find the intersection cell). L1 is the tutorial; mechanic discovery IS the difficulty.
  - **(d) Step budget**: 30. Generous over the 1-action witness; the player has 29 spare clicks to experiment with mirror placement and orientation cycling.

### Level 2 — base system + 1 new mechanic (filter)

Layout: emitter at (1, 2) firing east. `filter` (palette-9 blue) at (3, 2). `target_blue` at (10, 11) (occupies cells (10, 11)–(12, 13)). No prism.

- **Mechanics required by the witness** (M = N + 1 = 2):
  - **M1 (carried from L1): mirror placement and cycling.** Same rule.
  - **M2 (new in L2): filter recolouring.** When the beam enters a `filter` cell, the beam's colour is reset to the filter's own palette. The filter at (3, 2) recolours yellow (palette-11) to blue (palette-9) for the rest of the trace.

- **Necessity per mechanic**:
  - **M1: L2 cannot be solved without triggering M1 because** without any mirror, the beam fires east from (1, 2), passes through the filter at (3, 2) (now palette-9 blue), and continues east along row 2 until exiting at (15, 2). The target ring at (10, 11) is below row 2; reaching it requires a `\` mirror at column 10, row 2 (or a chain of mirrors that achieves the same effective east→south redirection at column 10).
  - **M2: L2 cannot be solved without triggering M2 because** `target_blue` accepts only palette-9 (blue) hits. The emitter produces palette-11 (yellow); without the filter recolouring the beam to palette-9, the beam reaches the target at the wrong colour and the target stays unlit. The filter is positioned at (3, 2) such that any east-going beam path from the emitter to columns ≥3 must pass through it; there is no alternate route from emitter to target that bypasses the filter cell.

- **Witness solution**:
  - `[ACTION6@(42, 10)]` — one click at pixel (42, 10), grid cell (10, 2). This drops `mirror_bs` at (10, 2). Beam re-trace: emitter → (2, 2) east (yellow) → (3, 2) filter → (4, 2)…(9, 2) east (blue) → (10, 2) hits `\` → south → (10, 3)…(10, 11) which is the top-left corner of `target_blue` perimeter. Lit at blue. Win.

- **Difficulty justification**:
  - **(a) Random-resistance**: 256 cells × need for correct orientation × the colour-match constraint. The level's witness is 1 click; random clicks find this cell with ≈ 1/256 per attempt. With 50 budget, cumulative random success ≈ 18% — but that's only for the EASY witness; if the player misjudges and places a `\` at a wrong column (e.g. column 8 instead of 10), the beam reflects to (8, 11) which is OUT OF target_blue's bounding box (10..12). Random play has ≪ 18% chance of finding the unique correct column.
  - **(b) Human-tractable**: ~ 1-2 minutes once mechanic learned. The player has to (a) recognise the filter changes beam colour (visible by the beam turning blue after passing it), (b) reason that the target wants blue (matching ring colour), and (c) compute the column-10 mirror placement geometrically.
  - **(c) Planning depth**: MODERATE. Per-step reasoning chain in the witness:
    1. *Read* the emitter's firing direction (east) and current beam path.
    2. *Trace* mentally that the beam already passes through the filter and emerges blue.
    3. *Identify* the target's column (= 10, derived from the target ring's left edge).
    4. *Place* the mirror at column 10 of the beam's row, with `\` orientation (which is the default first-click orientation, so no cycling needed).
  - **(d) Step budget**: 50. Generous over the 1-action witness, allowing the player to experiment with orientations (cycling `\` → `/` for misplaced mirrors) and column choices. L2's budget exceeds L1's because L2 introduces the filter mechanic that requires an extra discovery beat.

### Level 3 — base system + 2 new mechanics (prism, prism toggling)

Layout: emitter at (1, 8) firing east. `prism_es` at (4, 8) — initial state "ES" (splits east-going beam into east + south branches). `filter` at (8, 8). `target_yellow` at (3, 12) (occupies cells (3, 12)–(5, 14)). `target_blue` at (1, 12) (occupies cells (1, 12)–(3, 14)) — wait, this overlaps with `target_yellow`. Let me reposition: `target_blue` at (12, 11) (occupies (12, 11)–(14, 13)). `target_green` at (3, 3) (occupies (3, 3)–(5, 5)).

Final layout (no overlaps):
- emitter at (1, 8) east.
- prism_es at (4, 8).
- filter at (8, 8).
- target_yellow at (3, 12)..(5, 14).
- target_blue at (12, 11)..(14, 13).
- target_green at (3, 3)..(5, 5).

- **Mechanics required by the witness** (M3-count = M2-count + 2 = 4):
  - **M1 (carried from L1): mirror placement and cycling.** Same rule.
  - **M2 (carried from L2): filter recolouring.** Same rule.
  - **M3 (new in L3): prism beam-splitting.** When the beam enters a `prism_es` cell, the beam continues in its current direction (east-continuing, if it entered going east) AND a new perpendicular branch is spawned going south (state "ES") or going north (state "EN"). The prism cell itself is recorded as "visited" but the underlying sprite is not painted by the overlay.
  - **M4 (new in L3): prism toggling.** Clicking on a `prism_es` cell replaces the sprite with `prism_en` at the same position (and vice versa). The next beam re-trace uses the new state. The prism's split-mode is a piece of mutable state controlled by the player via clicks.

- **Necessity per mechanic**:
  - **M1: L3 cannot be solved without triggering M1 because** the east-branch beam, after the prism and filter, continues east through palette-9 (blue) but `target_blue` is at column 12, row 11–13; the beam passes through (9, 8)…(15, 8) along row 8 and exits at (15, 8) — never reaching row 11–13 on column 12 unless a `\` mirror at (12, 8) reflects it south (toward (12, 11) which is the target's top-left corner).
  - **M2: L3 cannot be solved without triggering M2 because** `target_blue` accepts only palette-9 hits; without the filter at (8, 8), the east branch of the beam stays palette-11 (yellow) and target_blue rejects it. The filter is on the unique east-branch path from prism (4, 8) to columns ≥ 8, so any east-branch beam that passes column 7 must traverse the filter cell.
  - **M3: L3 cannot be solved without triggering M3 because** the south branch (palette-11 yellow) hits `target_yellow` at (3, 12)–(5, 14) ONLY if the prism's perpendicular split exists; without the prism, only the east branch exists, and `target_yellow` (south of the emitter row, west of the filter column) is unreachable by east-only beam paths. Likewise `target_green` at (3, 3)–(5, 5) is north of the emitter row and unreachable by east-only paths; only the prism's north-branch (in state EN) reaches it. Without the prism, two of the three targets remain forever unlit.
  - **M4: L3 cannot be solved without triggering M4 because** at any single click, the prism is in EITHER state ES OR state EN — never both. The south branch (which lights target_yellow) requires state ES; the north branch (which lights target_green) requires state EN. To light BOTH target_yellow AND target_green, the player must visit BOTH prism states across the click sequence. Toggling the prism is the only mechanism to switch states.

- **Witness solution**:
  - The level's win condition is "all 3 targets lit". Targets are sticky: once lit, they stay lit. Lighting only happens during click-driven traces (NOT at level-load).
  - Witness (2 clicks):
    1. `ACTION6@(50, 34)` — pixel (50, 34) → grid (12, 8). Drops `mirror_bs` at (12, 8). Beam re-trace with prism state ES:
       - Emitter (1, 8) → (2, 8), (3, 8) east → enters prism (4, 8). Prism splits.
       - East branch continues: (5, 8), (6, 8), (7, 8) → enters filter (8, 8) → palette → (9, 8), (10, 8), (11, 8) → (12, 8) hits `\`, deflects south → (12, 9), (12, 10), (12, 11) which is target_blue's top-left corner. **target_blue lit at blue**.
       - South branch from prism: (4, 9), (4, 10), (4, 11), (4, 12) which is target_yellow's top-left corner. **target_yellow lit at yellow**.
       - target_green NOT lit yet (no north branch in ES state).
    2. `ACTION6@(18, 34)` — pixel (18, 34) → grid (4, 8). Clicks on the prism. Replaces `prism_es` with `prism_en` at (4, 8). Beam re-trace with prism state EN:
       - East branch unchanged (mirror at (12, 8) still reflects east branch to target_blue, **target_blue stays lit** sticky).
       - North branch from prism: (4, 7), (4, 6), (4, 5) which is target_green's bottom-left perimeter cell. **target_green lit at yellow** (palette-11; matches target_green expectation? wait target_green expects palette-14 not 11 — but the beam is yellow palette-11 in north branch since it never passed the filter).
   
   **Bug:** target_green expects palette-14 hit but beam is yellow palette-11. 

   **Revised L3 layout** to fix:
   - Make `target_green` accept palette-11 (yellow). I.e., target_green is just "target" with green ring and accepts yellow hits — but that means the ring colour and the accept-colour differ, which violates visual coupling.
   
   Alternative fix: redesign so the north branch is recoloured by a second filter to green, OR target_green accepts yellow.
   
   Cleanest: change target_green to `target_yellow_2` (a SECOND yellow target, distinguished only by position). Then both south branch and north branch hit yellow targets at their respective ends.
   
   Even cleaner: rename to use "target_yellow_north" and "target_yellow_south" for clarity, both palette-11 rings. The NORTH-branch and SOUTH-branch each light their own yellow target.
   
   The third target keeps `target_blue` for the east branch through filter.
   
   Witness logic still works:
   - Click 1: place mirror, ES state. East→target_blue, South→target_yellow_south. target_yellow_north still unlit.
   - Click 2: toggle prism to EN. East unchanged, North→target_yellow_north. All 3 lit.
   
   Targets all sticky-lit. Win.

   Final L3 layout (final-final):
   - emitter at (1, 8) east.
   - prism_es at (4, 8).
   - filter at (8, 8).
   - **target_yellow_south** at (3, 12)..(5, 14). (Distinguished by position.)
   - **target_blue** at (12, 11)..(14, 13).
   - **target_yellow_north** at (3, 3)..(5, 5).

   Two yellow targets at different positions, plus one blue target. Player sees 3 rings: 2 yellow, 1 blue.

   - target_yellow_south: lit when beam visits at palette-11 ANY of its perimeter cells.
   - target_yellow_north: same expectation, but at the north position.
   - target_blue: lit when beam visits at palette-9.

   Witness (revised, 2 clicks):
   1. `ACTION6@(50, 34)` → grid (12, 8). Drops `mirror_bs`. Beam (state ES): east→target_blue lit, south→target_yellow_south lit.
   2. `ACTION6@(18, 34)` → grid (4, 8). Toggles prism to EN. Beam: east branch unchanged (target_blue stays lit), north→target_yellow_north lit.

   All 3 lit. Win.

- **Difficulty justification**:
  - **(a) Random-resistance**: 256 cells × multiple correct cells (any of (12, 8), (12, 9), (12, 10) for the east-branch reflection cell, etc.) × the prism-toggle requirement. Random clicks have a ≪1% chance of producing the correct sequence within 80 budget.
  - **(b) Human-tractable**: ~2-3 minutes once mechanics learned. The player must (a) discover the prism splits, (b) discover toggling, (c) plan a 2-step click sequence.
  - **(c) Planning depth**: MORE THAN L2.
    - **Trivial heuristic that L3 defeats**: "click cells closest to each target first to redirect the beam toward each ring", which fails because target_yellow_north sits north of emitter row 8 and is unreachable by ANY east-or-south beam path; the player must instead prioritise toggling the prism (which is GEOMETRICALLY REMOTE from any target) to switch to the north-branch state.
    - **Witness-pair commute test**: swapping click 1 (place `mirror_bs` at (12, 8)) and click 2 (toggle prism at (4, 8)) breaks the witness because:
      - Swapped click 1 (= toggle prism): re-trace with state EN, no mirror yet. East branch (no mirror) exits at (15, 8) — target_blue NOT lit. North branch → target_yellow_north LIT. South branch GONE — target_yellow_south NOT lit (and never lit since this is the only chance the south branch existed).
      - Swapped click 2 (= place mirror at (12, 8)): re-trace with state EN. East branch with mirror → target_blue LIT. North still active → target_yellow_north stays lit. target_yellow_south STILL not lit (because state is EN, no south branch).
      - Final after 2 swapped clicks: target_yellow_north + target_blue lit; target_yellow_south UNLIT. NOT WIN. The witness's 2-click solution is broken; recovery requires ≥1 additional click (toggle back to ES, which lights target_yellow_south, costing 3 total). Order-dependence is genuine: the south-branch target must be lit while the prism is in ES state, which requires the FIRST click to leave the prism in ES (i.e. the first click must be a mirror placement, not a toggle).
  - **(d) Step budget**: 80. Generous over the 2-action witness; ≥ L2's 50, satisfying the "budget mustn't shrink as level rises" rule and giving ample exploration for the player to discover toggling.

## 5. Action mapping

`available_actions = [6]`. Pure-click game.

- **`ACTION6` (CLICK at `(x, y)`)**: the player supplies pixel coordinates `x, y ∈ [0, 63]`. The game converts via `self.camera.display_to_grid(int(x), int(y))` → grid coords `(gx, gy)` ∈ `[0, 15] × [0, 15]`. Dispatch by what's at `(gx, gy)`:
  - **Empty cell**: place `mirror_bs` (`\`, palette-7 pink) at `(gx, gy)`.
  - **`mirror_bs` here**: replace with `mirror_sl` (`/`, palette-6 magenta).
  - **`mirror_sl` here**: remove (back to empty).
  - **`prism_es` here** (L3 only): replace with `prism_en`.
  - **`prism_en` here** (L3 only): replace with `prism_es`.
  - **`filter`, `emitter`, or any `target_*` sprite at `(gx, gy)`**: no-op.
  - **`gx, gy` out of grid (0..15) or `display_to_grid` returns None**: no-op.

In all branches, the step counter decrements by 1 and the beam is re-traced (which updates `beam_overlay.pixels` and the per-target lit state). Targets are sticky: once lit, they stay lit until level transition.

No context-dependent gating beyond "click on a cell that's part of an out-of-grid region is a no-op".

## 6. HUD and per-game state

- **`StepCounterHud`** (subclass of `RenderableUserDisplay`): paints row 63 of the rendered 64×64 frame with palette-11 (yellow) for the leading `round(64 × remaining/total)` cells and palette-4 (off-black) for the rest. Updated via `self.step_counter_hud.set_remaining(self.steps_remaining)` after every dispatch in `step()`.

- **Per-game state** (held on the `Bx84` instance):
  - `self.steps_remaining: int` — initialised in `on_set_level` from `level.data["step_budget"]`. Decrements per click.
  - `self.targets_lit: dict[str, bool]` — keys: target sprite-names (e.g. `"target_yellow_south"`); values: True once the beam has visited any of the target's perimeter cells at the matching colour. Reset to all-False in `on_set_level`.
  - The beam itself is NOT held as state — it's recomputed from scratch every click via the trace function. The trace function reads the current emitter, mirrors, filter, prism (whichever sprites are in `self.current_level`) and writes to `self.beam_overlay.pixels`.

## 7. Win condition

`self.next_level()` is called when, after a `ACTION6` dispatch, `all(self.targets_lit[name] for name in self.targets_lit)` is True. The check runs at the end of `step()`'s ACTION6 branch, AFTER the beam re-trace and target-lit-update have run. Since `self.targets_lit` includes only the targets that the level actually placed, every level's win predicate adapts to its sprite roster automatically:

- L1: `targets_lit == {"target_yellow": True}`.
- L2: `targets_lit == {"target_blue": True}`.
- L3: `targets_lit == {"target_yellow_south": True, "target_blue": True, "target_yellow_north": True}`.

## 8. Lose condition

`self.lose()` is called when `self.steps_remaining <= 0` at the START of `step()` (BEFORE the click is dispatched). The step counter decrements per click; if a click would push it to 0 or below, the dispatch happens first (so that final click can still win), but if a SUBSEQUENT click is attempted with `steps_remaining <= 0`, the game loses.

Concrete predicate:
```python
def step(self):
    if self.action.id != GameAction.ACTION6:
        self.complete_action(); return
    if self.steps_remaining <= 0:
        self.lose(); self.complete_action(); return
    self.steps_remaining -= 1
    # ... dispatch click, retrace, mark targets, check win ...
    self.complete_action()
```

## 9. Novelty note

Cited entries from `mechanic-novelty/taxonomy-of-25-games.md` (the closest 4 of the 25):

- **`ar25` (shape-mirror-cover)**: ar25 reflects a 2D shape across a continuous mirror line (axis of symmetry), and the player slides the shape with arrow keys to align the ghost-image over scattered dots. **`bx84` reflects a 1D ray off discrete cell-mirrors at right angles**; there is no axis of symmetry, no shape-ghost, no avatar to slide. ar25's mirror is a continuous line spanning the whole grid; bx84's mirrors are 1×1 cells, and there are several per level.
- **`cd82` (orbit-fire-paint)**: cd82 paints CANVAS CELLS with directional fill from an orbiting tank. **`bx84` traces a beam through cells**, no canvas-painting verb, no orbit. cd82 has discrete fire events (ACTION5) that splash colour onto cells; bx84 has a continuous beam re-traced after every click.
- **`tn36` (program-pawn-trace)**: tn36 builds a programme of move-and-rotate instructions then runs it; the pawn walks a runway tracing a target pattern. **`bx84` is live (no commit step)**; every click immediately re-traces the beam. tn36's pawn is an agent following an instruction list; bx84's beam is a passive ray determined by static reflectors.
- **`re86` (frame-paint-canvas)**: re86's frames slide over a canvas and absorb colour-zone dyes; the player aligns each frame with a target tint. **`bx84` does not paint canvas cells**; the beam either reaches a target ring or doesn't.

Cited entries from `prior-games/index.md`:

- **`lq5x` (lantern-cone-illuminate)** is the closest in thematic space (both involve "light" and "filters"). lq5x has ONE moving lantern (avatar walks with arrows, ACTION5 rotates) projecting a 3-wide directional CONE; **bx84 has a fixed emitter and the player places stationary mirrors**, with a 1-pixel-wide BEAM that REFLECTS off mirrors at right angles. Crucially, lq5x has NO REFLECTION mechanic — the cone always points in the lantern's facing direction. bx84's core mechanic is right-angle reflection, which lq5x does not have at all. The two games' central reasoning tasks differ: lq5x plans walking paths with a moving light source; bx84 plans a static reflector layout.
- **`vn8d` (domino-cascade-topple)**: a single click triggers a chain reaction through pre-placed pillars/burst-pads/rotator-pads. **bx84 BUILDS the network of mirrors via clicks one at a time**; the beam-source is fixed; the player solves by mirror-LAYOUT, not by trigger-CHOICE. vn8d's cascade is a 4-way burst tree from one trigger; bx84's beam is a single ray with at-most-one binary split (at the L3 prism).
- **`kn58` (anchor-pull-magnet)** also pure-click. kn58 places a single anchor that pulls every coloured pawn one cell toward it; **bx84 places mirrors that reflect a beam**, not pawns that move. kn58's "every click moves all pawns" gives intrinsic order-dependence; bx84's order-dependence emerges only at L3 from the toggleable prism.

The negative similarity check in `mechanic-pick.md` was re-walked against the fleshed-out spec; no prior shares 3+ surface dimensions. The pixel grain (small mirror cells, 3×3 hollow ring targets, palette-12/13 prism orange/maroon, palette-9 filter, palette-11 yellow beam) and the dominant palette signature `{3 emitter, 5 background, 7 pink mirror, 6 magenta mirror, 9 blue filter+target, 11 yellow beam+target, 12 orange prism, 13 maroon prism, 14 NOT used (replaced target_green with target_yellow_north)}` differ from every prior game's signature.

The `target_green` ↔ palette-14 shift to `target_yellow_north` ↔ palette-11 was made to ensure the north-branch beam (which never passes the filter) hits a target of its current colour (yellow). No green is used in bx84.
