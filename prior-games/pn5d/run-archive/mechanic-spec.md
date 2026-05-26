# pn5d — full spec (revised round 2)

> Revision marks (this round):
> - **§3 changed** (Issue 1, Issue 2): `valve_closed` is now solid grey, no X-pattern. `pour_cursor` is now a hollow yellow square, no triangle.
> - **§4 Level 3 changed** (Issue 3): rebuilt with 4 vessels A/B/C/D, witness 12 actions, step budget 20, M3 strictly necessary.
> - All other sections unchanged from round 1.

## 1. Title
Connected-Vessel Filling

## 2. Mechanic family
`vessel-equalize-flow`. Core mechanic: a row of open-top rectangular **vessels** is connected at their bases by toggleable **valves**; pouring into any vessel raises every vessel in the cursor's currently-connected group by 1 height-unit at once (open-valve groups rise as a unit). Draws on **basic physics** (volume sharing in connected vessels), **basic geometry / topology** (open-vs-closed-valve connectivity defines the connected component each pour acts on), and **objectness** (each vessel + each valve are persistent entities the player tracks).

## 3. Sprite roster *(changed: §3.4 forbidden-elements compliance — Issues 1 and 2)*

- `vessel_outline` — 8 wide × 14 tall, 1-pixel walls on left, right, bottom; open top. Palette `4` (off-black, walls); interior `-1` (transparent). Tag `vessel`. Cloned once per vessel per level. Role: vessel border; the wall pixels block any extraneous fill rendering and define the vessel's hit-region.
- `liquid_fill` — 6 wide × 12 tall, all `-1` initially, mutated at runtime. Tag `fill`. Sits inside its parent vessel at `(parent.x + 1, parent.y + 1)`. Layer below `vessel_outline`. Role: each instance's bottom `level` rows are mutated to colour `10` (light-blue); rows above remain `-1`.
- `target_mark` — 2 wide × 1 tall, `[[8, 8]]`. Tag `target`. Layer above `vessel_outline`. Role: red (palette 8) inward pip rendered ON the inside of the vessel's right wall at the target row. One per vessel per level.
- `overflow_cap` — 3 wide × 1 tall, `[[12, 12, 12]]`. Tag `overflow`. Layer above `vessel_outline`. Role: orange (palette 12) outward-jutting lip rendered on the OUTSIDE of vessel C's left wall at row R, indicating: surface above row R in this vessel spills out. **L3 only**, applied to vessel C.
- `valve_open` — 2 wide × 4 tall, all-filled `[[14,14],[14,14],[14,14],[14,14]]`. Tag `valve`, `sys_click`. Layer 1. Role: solid green (palette 14) block in the gap between two adjacent vessel bases, indicating valve is OPEN.
- `valve_closed` *(changed)* — 2 wide × 4 tall, `[[3,3],[3,3],[3,3],[3,3]]`. Tag `valve`, `sys_click`. Layer 1. Role: solid grey (palette 3) block, indicating valve is CLOSED. Same shape and size as `valve_open`; differs only in palette. The shared-shape, distinct-colour pair signals "two correlated states of one valve" per `checklist.md` item 21 rule 2 — exactly what the player must read off the frame.
- `pour_cursor` *(changed)* — 3 wide × 3 tall, hollow square `[[11, 11, 11], [11, -1, 11], [11, 11, 11]]`. Tag `cursor`. Layer 2. Role: yellow (palette 11) hollow ring rendered above the row of vessel tops, centered above whichever vessel is currently selected. The ring is non-directional; the player learns "the active vessel is the one with the bracket above it" from the bracket's *position*, not its shape.

(Per `code/universal-scaffold.md` § Style rules: sprite names are plain semantic English. Class name is forced Pascal-case from the game ID, hence `class Pn5d(NovaBaseGame)`.)

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. Grid `64 × 64` for all three (no per-level resize). Vessel internal liquid range = 0..12 height-units. Vessels arranged in a horizontal row, centered on the playfield. Vessel tops at `y=8`, vessel bottoms at `y=22` (internal liquid rows `y=10..21`). Pour-cursor row at `y=4..6`. Valve gaps span `y=23..26`. HUD step bar at row `y=63`.

### Level 1 — base dynamic system

**Layout**: 2 vessels A (cols 23..30) and B (cols 33..40), 1 fixed-open valve A-B at cols 31..32 / rows 23..26. **No `valve_closed` instance is created** — the valve is permanently open (toggle does not yet apply). Targets: A=4 (red `target_mark` pip at row `y=18`), B=4 (pip at row `y=18`). All initial surfaces = 0. **Step budget 12.**

- **Mechanics required by the witness** (N=1):
  - **M1** = *pour-and-equalize*: ACTION5 with the pour-cursor over a vessel adds 1 height-unit to every vessel in the cursor's currently-connected group. Group = `{A, B}` (one fixed-open valve), so each pour raises both A and B by 1.
- **Necessity per mechanic**:
  - **M1**: L1 cannot be solved without triggering M1 because both vessels start at 0 with targets 4 / 4; ACTION5 is the only state-mutating verb.
- **Witness solution** (4 actions):
  1. `ACTION5` (cursor on A by default) → A=1, B=1.
  2. `ACTION5` → A=2, B=2.
  3. `ACTION5` → A=3, B=3.
  4. `ACTION5` → A=4, B=4. **Win check** ⇒ `next_level()`.
- **Difficulty justification**:
  - **(a) Random-resistance**: random play uniformly over `[3, 4, 5, 6]` fires ACTION5 with prob 1/4. Probability of completing 4 ACTION5s within the 12-action budget ≈ 0.16. Acceptable for a tutorial L1.
  - **(b) Human-tractable**: ~30 seconds. Player tries each action once, sees ACTION5 fills both vessels, repeats.
  - **(c) Planning depth**: **no strict planning requirement**. Discovery gate only.
  - **(d) Step budget**: 12 (witness 4, buffer 8).

### Level 2 — base system + 1 new mechanic (M2)

**Layout**: 3 vessels A (cols 16..23), B (cols 26..33), C (cols 36..43); 2 valves A-B (cols 24..25, rows 23..26) and B-C (cols 34..35, rows 23..26). Both valves start OPEN (`valve_open` `TANGIBLE`, sibling `valve_closed` `REMOVED`). Targets: A=3 (pip `y=19`), B=2 (pip `y=20`), C=5 (pip `y=17`). All initial surfaces = 0. **Step budget 18.**

- **Mechanics required by the witness** (N+1 = 2):
  - **M1** = *pour-and-equalize* (carried forward).
  - **M2** = *valve toggle*: ACTION6 click on a `valve_open` or `valve_closed` sprite swaps its `TANGIBLE`/`REMOVED` state with its sibling, splitting or merging the connected component.
- **Necessity per mechanic**:
  - **M1**: L2 cannot be solved without M1 because all three vessels start at 0 and targets are non-zero (3, 2, 5); only ACTION5 raises surfaces.
  - **M2**: L2 cannot be solved without M2 because both valves start OPEN and targets are distinct heights (3, 2, 5); with the entire `{A, B, C}` group connected, every ACTION5 raises all three surfaces simultaneously by exactly 1 — they cannot reach different heights. The only way to leave A, B, C at different heights is to disconnect them, which requires firing ACTION6 on at least one valve.
- **Witness solution** (10 actions):
  1. `ACTION5` (cursor on A; group `{A,B,C}` open) → A=1, B=1, C=1.
  2. `ACTION5` → A=2, B=2, C=2 (B reaches target).
  3. `ACTION6` @ display click `(24, 24)` → toggle valve A-B from open → closed; groups `{A}` and `{B, C}`.
  4. `ACTION6` @ display click `(34, 24)` → toggle valve B-C from open → closed; groups `{A}`, `{B}`, `{C}`.
  5. `ACTION5` (cursor still on A; group `{A}`) → A=3 (target met).
  6. `ACTION4` → cursor A → B.
  7. `ACTION4` → cursor B → C.
  8. `ACTION5` (cursor on C; group `{C}`) → C=3.
  9. `ACTION5` → C=4.
  10. `ACTION5` → C=5 (target met). **Win check** ⇒ `next_level()`.
- **Difficulty justification**:
  - **(a) Random-resistance**: random play would need toggling two specific valves, moving cursor to specific vessels, pouring the right counts; satisfying all three different targets within 18 random actions is far below 10⁻⁴ — overpouring of at least one vessel is near-certain under random play.
  - **(b) Human-tractable**: ~2 minutes. The player must (1) discover the toggle verb (ACTION6 on a valve flips green ↔ grey), (2) connect the change in group structure with the change in pour behaviour, (3) plan the pour sequence.
  - **(c) Planning depth (post-discovery)**: **moderate planning required**. **Decision space at level start (post-discovery)**: 4 toggle combinations possible (00, 01, 10, 11), each leading to a different group structure for the first pour. At least 3 first-action paths a fully-informed player would consider. **Plausible-but-wrong alternative**: "pour into A's group with valves open until A hits 3, then deal with B and C" — but with valves open, A=3 ⇒ B=3, C=3, which overshoots B (target 2) and undershoots C (target 5). The fully-informed player must reject this and reach for the toggle verb. **Witness reasoning chain post-discovery**: "B's target (2) is the lowest. Pour into the merged group up to B's target first, then close valves and pour each remaining vessel to its own height." Each step references current surface heights and group structure — post-discovery state, not discovery-stage observations.
  - **(d) Step budget**: 18 (witness 10, buffer 8).

### Level 3 — base + L2 + 1 new mechanic (M3) *(changed: 4-vessel rebuild for Issue 3)*

**Layout**: 4 vessels A (cols 8..15), B (cols 18..25), C (cols 28..35), D (cols 38..45); 3 valves A-B (cols 16..17, rows 23..26), B-C (cols 26..27, rows 23..26), C-D (cols 36..37, rows 23..26). All three valves start CLOSED (`valve_closed` `TANGIBLE`, `valve_open` siblings `REMOVED`). Vessel C carries an `overflow_cap` instance at row `y=20` (cap height = 2), drawn outward of C's left wall at cols 25..27. Targets: A=9 (pip `y=13`), B=9 (pip `y=13`), C=2 (pip `y=20`), D=9 (pip `y=13`). All initial surfaces = 0. **Step budget 20.**

- **Mechanics required by the witness** (= L2-count + 1 = 3):
  - **M1** = *pour-and-equalize* (carried forward).
  - **M2** = *valve toggle* (carried forward).
  - **M3** = *overflow cap*: vessel marked with `overflow_cap` at row R cannot hold more than R height-units. After every pour, if the marked vessel's surface would exceed R, the surface clips to R (excess lost through the visible side-spillway lip).
- **Necessity per mechanic**:
  - **M1**: L3 cannot be solved without M1 because all surfaces start at 0 and targets are non-zero (9, 9, 2, 9); only ACTION5 raises surfaces.
  - **M2**: L3 cannot be solved without M2 because all three valves start CLOSED. The closed-only strategy costs `9 (pour A) + 1 (cursor A→B) + 9 (pour B) + 1 (cursor B→C) + 2 (pour C) + 1 (cursor C→D) + 9 (pour D) = 32 actions`, well over the 20-action budget. To fit, at least one valve must be opened — i.e., M2 fires.
  - **M3**: L3 cannot be solved without M3 within the 20-action budget. Enumerating every plausible alternate strategy a fully-informed player might try (per checklist item 12, "verify by enumeration, not by abstraction"):
    1. **All valves closed, pour each separately**. Cost = 32 actions. > 20. Fails — also fails M2 necessity above.
    2. **Open A-B only** (groups `{A, B}`, `{C}`, `{D}`). Pour 9 in `{A, B}` (no clipping needed, A=B=9), cursor to C, pour 2, cursor to D, pour 9. Cost = 1 + 9 + 2 + 2 + 1 + 9 = 24 actions. > 20. Fails. M3 not used.
    3. **Open C-D only** (groups `{A}`, `{B}`, `{C, D}`). `{C, D}` needs C=2 and D=9 — REQUIRES M3 to clip C while D rises. Pours alone yield C=D=9 without M3. So this alternate uses M3.
    4. **Open A-B and C-D** (groups `{A, B}`, `{C, D}`). `{C, D}` again needs M3 to differentiate C and D.
    5. **Open A-B and B-C** (groups `{A, B, C}`, `{D}`). `{A, B, C}` needs A=9, B=9, C=2 — REQUIRES M3.
    6. **Open B-C only** (groups `{A}`, `{B, C}`, `{D}`). `{B, C}` needs B=9, C=2 — REQUIRES M3.
    7. **Open B-C and C-D** (groups `{A}`, `{B, C, D}`). `{B, C, D}` needs B=9, C=2, D=9 — REQUIRES M3.
    8. **Open all three** (witness; merged `{A, B, C, D}`). Pour 9 — REQUIRES M3.
    
    Of strategies 1-8, only 1 and 2 bypass M3, and both exceed the 20-action budget. **Therefore M3 is strictly necessary at L3.**
- **Witness solution** (12 actions):
  1. `ACTION6` @ display click `(16, 24)` → toggle valve A-B closed → open. Group `{A, B}`.
  2. `ACTION6` @ display click `(26, 24)` → toggle valve B-C closed → open. Group `{A, B, C}`.
  3. `ACTION6` @ display click `(36, 24)` → toggle valve C-D closed → open. Group `{A, B, C, D}`.
  4. `ACTION5` (cursor on A by default; group `{A,B,C,D}`) → A=1, B=1, C=1, D=1.
  5. `ACTION5` → A=2, B=2, C=2, D=2.
  6. `ACTION5` → A=3, B=3, C clipped to 2 (M3 fires), D=3.
  7. `ACTION5` → A=4, B=4, C clipped at 2, D=4.
  8. `ACTION5` → A=5, B=5, C clipped at 2, D=5.
  9. `ACTION5` → A=6, B=6, C clipped at 2, D=6.
  10. `ACTION5` → A=7, B=7, C clipped at 2, D=7.
  11. `ACTION5` → A=8, B=8, C clipped at 2, D=8.
  12. `ACTION5` → A=9, B=9, C clipped at 2, D=9 (all targets met). **Win check** ⇒ `next_level()`.
- **Difficulty justification**:
  - **(a) Random-resistance**: random play must (i) emit three specific toggles before pouring, (ii) pour exactly 9 times in the merged group. Probability of stitching this within 20 random `[3, 4, 5, 6]` actions is < 10⁻⁴ — random play almost certainly skips toggles or overshoots.
  - **(b) Human-tractable**: ~2-3 minutes. The player must (1) realise valves are CLOSED at L3 start (the grey blocks vs. the green ones at L2) and need opening, (2) recognise C's overflow lip on the left wall as a *cap* rather than a target marker (visual contrast: orange outward-jutting 3-pixel lip vs. red inward 2-pixel pip), (3) plan that opening all valves merges the group such that C's natural cap matches its target — over-pours absorbed.
  - **(c) Planning depth (post-discovery)**: **planning challenging even for an attentive human**. **Decision space at level start, fully informed**: 8 toggle subsets × pour-vessel choice. At least 7 first-action paths to consider (any of the 3 valves to toggle first, or pour first). Only the 3-toggles-then-pour path fits the budget. **Trivial heuristic that fails**: *"target each vessel independently"* — a player who internalised L2's "different targets ⇒ close valves" rule will reach for the closed-valve strategy. With L3 targets 9, 9, 2, 9, this costs 32 actions — well over the 20-action budget. The greedy heuristic loses. **Where heuristic diverges from witness**: the witness opens *all* valves before pouring (steps 1-3 are toggles); the greedy heuristic skips the toggles entirely. Divergence at action 1: witness invests in valve setup that *appears wasteful* (no level rises until action 4) but is the only path that fits the budget — ahead-of-time reasoning is needed because the player must compute "three toggle actions saving (32 − 12 = 20) pour actions" before their first pour, anticipating the merged-group + overflow-cap composition.
  - **(d) Step budget**: 20 (witness 12, buffer 8). Buffer = L2's buffer = L1's buffer = 8 — **no shrink** relative to witness across levels.

## 5. Action mapping

Subset = `[3, 4, 5, 6]`.

| Action | Semantic | Gate |
|---|---|---|
| `ACTION3` | Move pour-cursor LEFT one vessel (decrement `_cursor_index`, clamped at 0). | Always offered. |
| `ACTION4` | Move pour-cursor RIGHT one vessel (increment `_cursor_index`, clamped at `len(_vessels) - 1`). | Always offered. |
| `ACTION5` | Pour 1 height-unit into every vessel of the cursor's currently-connected group; then for every vessel with an `overflow_cap` set at row R, clip its surface to R if it exceeds R. | Always offered. |
| `ACTION6` | Click `(x, y)` (display pixels). Convert via `camera.display_to_grid(int(x), int(y))`. If the resolved grid cell is occupied by a `valve` sprite, swap its `valve_open` / `valve_closed` siblings. Otherwise no-op. Always consumes 1 step (per cn04, sb26 precedent). | Always offered. |

ACTIONs 1, 2, 7 are NOT in `available_actions`. Slot 7 is omitted because the game has no meaningful undo; pour is monotone-up and toggle is freely reversible. Slots 1, 2 are omitted because the cursor moves only horizontally.

## 6. HUD and per-game state

**HUD widget**:
- `StepCounterHud(RenderableUserDisplay)` — draws a 1-row depleting bar at row `y=63`. Two-colour: palette `4` (off-black) for remaining steps, palette `3` (grey) for consumed steps. Bar spans full 64 columns; depletion uses `math.ceil(64 * (steps_left / max_steps))`.

**Per-game state** (instance attributes on `Pn5d(NovaBaseGame)`):
- `_cursor_index: int` — index 0..N-1 of the vessel under the pour-cursor. Initialised to 0 in `on_set_level`.
- `_max_steps: int` — read from `level.get_data("max_steps")`. 12 / 18 / 20 across L1 / L2 / L3.
- `_vessels: list[dict]` — each entry: `{"name", "outline_sprite", "fill_sprite", "level": int, "target": int, "overflow_cap": int | None, "x": int, "y": int}`. Populated in `on_set_level` from `level.get_data("vessels")`.
- `_valves: list[dict]` — each entry: `{"open_sprite", "closed_sprite", "is_open": bool, "left_index": int, "right_index": int}`. Populated similarly.
- `_step_bar: StepCounterHud` — HUD widget instance.

**Visible state cues** (per `checklist.md` item 19):
- The pour-cursor's on-screen position IS the persistent cue for `_cursor_index`.
- Valve open / closed states are rendered as visually distinct `valve_open` (green) vs. `valve_closed` (grey) sprites — the player reads off the connectivity at every frame.
- Liquid surface in each vessel is the bottom-up `liquid_fill` band — directly observable.
- Overflow cap on C is the orange outward lip on C's left wall.
- Target marks are the red inward pips on each vessel's right wall.

No game state is hidden behind one-frame flashes.

## 7. Win condition

After every committed action (at the end of `step()`, before `complete_action()`):

```python
all_targets_met = all(v["level"] == v["target"] for v in self._vessels)
if all_targets_met:
    self.next_level()
    return
```

L3's terminal `next_level()` triggers the engine's automatic `self.win()`.

## 8. Lose condition

Single fail mode (checked AFTER the win check):

```python
if self._action_count >= self._max_steps:
    self.lose()
    return
```

No hazards, no soft-lock states. Pour is monotone-up clamped by overflow caps; toggle is freely reversible.

## 9. Novelty note

### Closest taxonomy entries (25 references)
- **sp80** (`pour-shelf-route`). Distinguishing rule: sp80 is **droplet-routing** — discrete drops fall vertically through player-positioned shelves into target cups, with a 4-attempt counter; the puzzle is *aiming drops*. pn5d is **volume-distribution** — multiple vessels share continuously-filling surfaces across an open-valve graph; the puzzle is *distributing total volume*. No drops, no aiming, no attempt-counter.

No other reference game involves liquid-as-fill at all.

### Closest prior-games entries (`prior-games/index.md`, 49 priors)
- **kx14** (`tide-tilt-buoyant`). Distinguishing rule: ONE tank with player-controlled GLOBAL water surface + buoyant balls; pn5d has MULTIPLE vessels with toggleable valves, the player POURS, and the win is the SURFACES THEMSELVES at marked rows. Different cast, verb, goal axis.
- **lv4k** (`lever-balance-torque`). Discrete-weight static balance vs. fluid distribution under continuous group equalisation.
- **kp9z** (`grain-accumulate-topple`). Discrete grains with toppling-at-capacity-4 vs. liquid surfaces in pre-defined containers.
- **kn58** (`anchor-pull-magnet`). Discrete pawns sliding under attractor vs. no movable pawn.
- **vd3g** (`valley-dig-roll`). Discrete marbles on binary-elevation grid vs. fluid in containers.

### `prior-games/index.md` non-empty
49 priors at run start. None match `vessel-equalize-flow` family.

### Negative similarity check summary
Closest priors (kx14, sp80) overlap on at most 1 of 8 dimensions ("involves liquid-as-fill aesthetic"). All other priors share at most 1 dimension. **Pass.** Adding a 4th vessel at L3 does not introduce new prior overlap (D is just another rectangle; the cast count rises but not the diagnostic dimensions).
