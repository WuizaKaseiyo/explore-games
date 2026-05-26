# `nb6t` — Game Spec (rev. 2)

Changes since rev. 1 (in response to `critique-revisions.md` visit 1):
- **§ 4** — base anchor moved from `(8, 32)` to `(16, 32)` in all three levels (so westward rotation of seg 0 is in-bounds).
- **§ 4 Level 1** — target moved from `(20, 8)` to `(4, 8)`; witness lengthened from 4 to 6 actions; random-resistance recomputed (≈ 0.85%, near-zero). [Addresses `critique-revisions.md` Issue 1.]
- **§ 4 Level 2** — target moved from `(16, 8)` to `(8, 8)`; witness lengthened from 8 to 10 actions; random-resistance recomputed.
- **§ 4 Level 3** — object_red moved to `(8, 8)`, drop_zone_red moved to `(32, 20)`; witness recomputed at length 19; random-resistance recomputed.
- **§ 4 Mechanic naming** — M1 renamed from "cycle-active-hinge" to "**change-active-hinge**"; description and counterfactual claims updated to reflect that both ACTION5 (cycle) and ACTION6 (click-on-hinge) implement M1. [Addresses `critique-revisions.md` Issue 2.]

## 1. Title
Articulated Reach.

## 2. Mechanic family

`hinge-chain-reach`. A chain of three rectangular rod-segments anchored at a fixed cell forms a polyline; each segment has an absolute heading (E, N, W, S) and an integer length (1..14). The player selects an active hinge and rotates its segment, extends/retracts its segment, and (at L3) carries a moveable object on the chain's tip. Goal across all levels: position the tip on a target cell (and, at L3, deliver carried objects to colour-matched drop-zones).

Core-knowledge priors used (from `core-knowledge-priors.md`):
- **Objectness**: hinges, segments, tip-marker, and the L3 moveable object are persistent entities.
- **Basic geometry**: 90° rotations and integer-length 1D extents on a Cartesian grid.
- **Basic physics (kinematic constraint)**: the chain's vector-sum geometry — each segment's start position depends on the previous segment's end.

## 3. Sprite roster

| Name | Pixel matrix dims | Palette values | Tags | Role |
|---|---|---|---|---|
| `base_anchor` | 5×5 | {4, 6} (rim 4, fill 6 magenta) | `["base"]` | fixed anchor; renders the chain origin; not movable |
| `segment` | length-variable, 3 cells wide | {4, 9} (rim 4, fill 9 blue) | `["segment"]` | one chain segment; orientation set via `set_rotation` |
| `hinge` | 3×3 ring | {4, 11} (outer 4, inner 11 yellow) | `["hinge", "sys_click"]` | hinge marker between segments and at base |
| `active_halo` | 5×5 ring | {11, 4} (outer 11, inner 4) | `["active_halo"]` | persistent highlight around the active hinge |
| `tip_marker` | 3×3 dot | {4, 8} (rim 4, fill 8 red) | `["tip", "sys_click"]` | end-effector of the chain |
| `tip_carry_halo` | 5×5 ring | {colour-of-carried-object, 4} | `["tip_carry_halo"]` | only present when carrying; ring colour matches object colour |
| `target_pad` | 5×5 ring | {15, 0} (outer 15 purple, inner 0 white) | `["target"]` | win-condition cell at L1 and L2 |
| `object_red` | 2×2 dot | {8, 4} (fill 8 red, rim 4) | `["object", "object_red"]` | L3 only — moveable item the chain picks up |
| `drop_zone_red` | 5×5 ring | {15, 8} (outer 15 purple, inner 8 red) | `["drop_zone", "drop_zone_red"]` | L3 only — destination for `object_red` |
| `step_counter_hud` (HUD widget, not a sprite) | row-63 horizontal bar | {11 yellow filled, 4 off-black empty} | n/a | depleting bar at row 63; one unit per action |

The chain's three segments are pre-cloned per-level so each level has independent sprite instances. Per-level layout (positions, lengths, orientations, plus per-level data such as target, object, drop-zone, and step budget) lives in each `Level(... data={...})`.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels.

Common platform constants:
- Grid: 64×64 in every level. Camera viewport set to (64, 64).
- Base anchor cell: `(16, 32)` in every level (the chain anchors at the same physical spot — only the chain's pose, target, per-level mechanic-set, and per-level objects vary).
- Chain has 3 segments throughout. Default initial pose at every level start: each segment's heading = E (east, +x), each segment's length = 12. So tip starts at `(16 + 36, 32) = (52, 32)` in every level.
- Default initial active hinge index = 0 (the base hinge).
- Pose math:
  - `hinge_0 = (16, 32)`. `hinge_(i+1) = hinge_i + L_i · DIR[θ_i]` where `DIR = {E:(1,0), N:(0,-1), W:(-1,0), S:(0,1)}`. Tip = `hinge_3`.
- Pose validity: a pose is valid iff every segment's cells are in-bounds (0..63 inclusive on x and y). A rotation/extension that would result in any segment-cell out of bounds is *rejected* (no state change), but the action is still consumed and the step counter still ticks down.

### Level 1 — base dynamic system

Configuration:
- Pose: (E length 12, E length 12, E length 12). Tip at `(52, 32)`. Active hinge = 0.
- `target_pad` placed at `(4, 8)` (centred 5×5 ring).
- Available actions: `_get_valid_actions` returns {3, 4, 5, 6} — rotate CCW, rotate CW, cycle active, click hinge.
- Step budget: 40.

**Mechanics required by the witness** (N = 2):
1. **M1 change-active-hinge** — two implementations: (i) ACTION5 cycles the active-hinge index forward modulo N_hinges (here N = 3, so 0→1→2→0…); (ii) ACTION6 click on a hinge cell sets the active hinge directly to that hinge's index. Both implementations move the active-hinge halo; the mechanic's distinguishing behaviour is "the active hinge index changes".
2. **M2 rotate-active-hinge** — ACTION3 rotates the active segment's heading 90° CCW (E→N→W→S→E); ACTION4 rotates 90° CW (E→S→W→N→E). The mechanic's distinguishing behaviour is "the active segment's θ changes". The chain's pose updates accordingly; if the new pose has any segment-cell out-of-bounds, the rotation is rejected and θ does not change.

**Necessity per mechanic** (counterfactual):
- *L1 cannot be solved without triggering M1 because* without ANY change to the active hinge (neither ACTION5 nor ACTION6 click on a non-zero hinge), the active hinge stays at 0 forever. Only seg 0 is rotatable. With segs 1, 2 fixed at θ = E, L = 12, tip = (16 + L_0·dir_x(θ_0) + 24, 32 + L_0·dir_y(θ_0)) = (40 + L_0·dir_x, 32 + L_0·dir_y). For target `(4, 8)` we need L_0·dir_x = -36 and L_0·dir_y = -24 simultaneously. Impossible: a single 4-direction segment can contribute to at most one axis at a time, AND L_0 is fixed at 12 at L1.
- *L1 cannot be solved without triggering M2 because* without rotation, all θ stay at default E. Sum.y = 0, so tip y = 32. Target y = 8. Tip y can never reach 8 without at least one rotation that introduces an N or S segment.

**Witness solution**: `[ACTION3, ACTION3, ACTION5, ACTION3, ACTION5, ACTION3]` (length 6). Trace:

| step | action | pose after | tip | notes |
|---|---|---|---|---|
| 0 | (initial) | (E12, E12, E12) | (52, 32) | active = 0 |
| 1 | ACTION3 | (N12, E12, E12) | (40, 20) | hinge_1 (16, 20), hinge_2 (28, 20). In-bounds. |
| 2 | ACTION3 | (W12, E12, E12) | (28, 32) | hinge_1 (4, 32), hinge_2 (16, 32). In-bounds. |
| 3 | ACTION5 | (W12, E12, E12) | (28, 32) | active = 1 |
| 4 | ACTION3 | (W12, N12, E12) | (16, 20) | hinge_1 (4, 32), hinge_2 (4, 20). In-bounds. |
| 5 | ACTION5 | (W12, N12, E12) | (16, 20) | active = 2 |
| 6 | ACTION3 | (W12, N12, N12) | (4, 8) | hinge_1 (4, 32), hinge_2 (4, 20). In-bounds. ✓ tip on `target_pad` → `next_level()`. |

**Difficulty justification**:
- (a) Random-resistance: a uniform-random policy across the 4 valid actions {3,4,5,6} hits the witness sequence with probability ≈ (1/4)^6 ≈ 0.024% per consecutive 6-window. Over a 40-step budget there are ≈ 35 windows, giving cumulative success ≈ 0.85% ≈ near-zero. ✓ Plus, ACTION6 random clicks are uniform over 64×64 = 4096 cells; the chance a random click hits a specific hinge cell is < 0.25%, making click-driven witness paths even less likely. A vision-blind agent has effectively no signal about whether the chain is closer to or further from the target.
- (b) Human-tractable: a sighted player presses each key once and sees the chain bend. They infer "ACTION3 rotates the active segment CCW; ACTION5 cycles which hinge is active; the halo highlights the active hinge". Reaching `(4, 8)` from `(52, 32)` then takes 1-2 minutes of straightforward planning.
- (c) Planning depth: L1 is the discovery gate. Once the rules are understood, reaching `(4, 8)` is visually obvious — bend hinge 0 westward (twice), then bend each of hinges 1 and 2 northward. **No strict planning requirement.**
- (d) Step budget: 40 (≈ 6.7× witness).

### Level 2 — base system + 1 new mechanic

Configuration:
- Pose: (E length 12, E length 12, E length 12). Tip at `(52, 32)`. Active hinge = 0.
- `target_pad` at `(8, 8)`.
- Available actions: {1, 2, 3, 4, 5, 6} — adds ACTION1 extend, ACTION2 retract.
- Step budget: 100.

**Mechanics required by the witness** (carried + 1 new = N+1 = 3):
1. **M1 change-active-hinge** (carried from L1).
2. **M2 rotate-active-hinge** (carried from L1).
3. **M3 segment-length-adjustment** (new) — ACTION1 increases the active segment's length by +1 (max 14); ACTION2 decreases it by -1 (min 1). A length change that would make any segment-cell out-of-bounds is rejected (no state change); the action still ticks the step counter.

**Necessity per mechanic**:
- *L2 cannot be solved without triggering M1 because* with the active hinge stuck at 0, only seg 0 is mutable. Tip = (16 + L_0·dir_x + 24, 32 + L_0·dir_y). For target `(8, 8)` we need L_0·dir_x = -32 and L_0·dir_y = -24 simultaneously — impossible (single 4-direction segment can contribute to at most one axis), AND with L_0 ≤ 14 we couldn't reach -32 along one axis even alone.
- *L2 cannot be solved without triggering M2 because* with all θ = E, sum.y = 0; tip y = 32. Target y = 8. Length-adjust never affects sum.y when every segment is east-pointing.
- *L2 cannot be solved without triggering M3 because* with all L = 12 fixed, sum.x is base.x + a sum of ±12 terms (one per segment, signed by θ). Reachable tip x values from base.x = 16 are `{16 + k·12 : k ∈ {-3, -2, -1, 0, 1, 2, 3}}` = `{-20, -8, 4, 16, 28, 40, 52}`. Target x = 8 — not in this set. Unreachable without length-adjust.

**Witness solution**: `[ACTION3, ACTION3, ACTION2, ACTION2, ACTION2, ACTION2, ACTION5, ACTION3, ACTION5, ACTION3]` (length 10). Trace:

| step | action | pose after | tip | notes |
|---|---|---|---|---|
| 0 | (initial) | (E12, E12, E12) | (52, 32) | active = 0 |
| 1 | ACTION3 | (N12, E12, E12) | (40, 20) | hinge_1 (16, 20). In-bounds. |
| 2 | ACTION3 | (W12, E12, E12) | (28, 32) | hinge_1 (4, 32). In-bounds. |
| 3 | ACTION2 | (W11, E12, E12) | (29, 32) | L_0 → 11. In-bounds. |
| 4 | ACTION2 | (W10, E12, E12) | (30, 32) | L_0 → 10. In-bounds. |
| 5 | ACTION2 | (W9, E12, E12) | (31, 32) | L_0 → 9. In-bounds. |
| 6 | ACTION2 | (W8, E12, E12) | (32, 32) | L_0 → 8. hinge_1 (8, 32). |
| 7 | ACTION5 | (W8, E12, E12) | (32, 32) | active = 1 |
| 8 | ACTION3 | (W8, N12, E12) | (20, 20) | hinge_2 (8, 20). In-bounds. |
| 9 | ACTION5 | (W8, N12, E12) | (20, 20) | active = 2 |
| 10 | ACTION3 | (W8, N12, N12) | (8, 8) | ✓ tip on `target_pad` → `next_level()`. |

**Difficulty justification**:
- (a) Random-resistance: P(uniform-6) for length-10 witness ≈ (1/6)^10 ≈ 1.7×10⁻⁸ per 10-window. Over budget 100 → ~91 windows → cumulative ≈ 1.5×10⁻⁶. Near-zero. ✓
- (b) Human-tractable: a sighted player must additionally discover length-adjust by experimenting with ACTION1/2 — they see the active segment grow or shrink. ~2 minutes to plan and execute.
- (c) Planning depth (L2 = moderate): post-discovery decision count at level start = 6 valid first actions {1, 2, 3, 4, 5, 6}. Plausible-but-wrong: after rotating seg 0 to W (2 actions), retract seg 1 instead of seg 0. With (W12, N12 retracted, N12) the segment-1 retraction shortens y-displacement and overshoots target. Witness reasoning: "tip x = 8 = base.x − 8 means seg 0 contributes -8 horizontally; with seg 0 = W and L_0 = 8, sum.x is -8; segs 1, 2 must each contribute 0 to x AND -12 each to y → both must point N at length 12". The wrong path "retract seg 0 to 4 instead of 8" gives sum.x = -4 and tip x = 12 ≠ 8.
- (d) Step budget: 100. (10× witness.)

### Level 3 — system + 1 new mechanic

Configuration:
- Pose: (E length 12, E length 12, E length 12). Tip at `(52, 32)`. Active hinge = 0.
- `object_red` placed at `(8, 8)`.
- `drop_zone_red` placed at `(32, 20)`.
- Available actions: {1, 2, 3, 4, 5, 6}.
- Step budget: 100.

**Mechanics required by the witness** (carried + 1 new = L2-count + 1 = 4):
1. **M1 change-active-hinge** (carried from L2).
2. **M2 rotate-active-hinge** (carried from L2).
3. **M3 segment-length-adjustment** (carried from L2).
4. **M4 carry-and-drop** (new) — when the chain's tip cell coincides with an `object_*` sprite's position and no object is currently carried, the object is picked up: the object sprite's `set_interaction(InteractionMode.REMOVED)` is applied (so it is no longer rendered nor collidable), and a `tip_carry_halo` overlay sprite in the carried-object's colour is placed at the tip. ACTION6 click on the tip's current cell *while carrying* drops the object: the object sprite's interaction is restored to `TANGIBLE` and its position is set to the tip's current cell, the `tip_carry_halo` overlay is removed. Click on a hinge cell *while carrying* still does the active-set behaviour (the click hits the hinge sprite, not the tip sprite). Click anywhere else is a no-op (the action still consumes a step counter unit).

**Necessity per mechanic**:
- *L3 cannot be solved without triggering M1 because* with active stuck at 0, only seg 0 is mutable. To pick up object_red at `(8, 8)`, tip must equal `(8, 8)`. Tip = (16 + L_0·dir_x + 24, 32 + L_0·dir_y). For (8, 8): need L_0·dir_x = -32 and L_0·dir_y = -24 simultaneously — impossible.
- *L3 cannot be solved without triggering M2 because* without rotation, tip y = 32. Pickup target y = 8. Unreachable regardless of length adjustment.
- *L3 cannot be solved without triggering M3 because* with all L = 12, tip x ∈ `{-20, -8, 4, 16, 28, 40, 52}`. Pickup target x = 8 ∉ set. Unreachable. (Note: drop-zone target x = 32 is also ∉ set, so length-adjust is required for *both* phases of the witness.)
- *L3 cannot be solved without triggering M4 because* the win predicate is "object_red at drop_zone_red AND not carried"; without the pickup mechanic, object_red stays at `(8, 8)` permanently, and the predicate never fires. Level unsolvable.

**Witness solution** (length 19):

Phase 1 — pickup at `(8, 8)`. Identical to the L2 witness through step 10 but the level data places `object_red` at `(8, 8)` instead of a `target_pad`. After step 10, tip is at `(8, 8)`, which coincides with `object_red.position` — auto-pickup triggers; tip_carry_halo (red ring) appears.

Phase 2 — drop at `(32, 20)`:

| step | action | pose after | tip | notes |
|---|---|---|---|---|
| 11 | ACTION4 | (W8, N12, E12) | (20, 20) | active = 2; θ_2 N→E. hinge_2 (8, 20). |
| 12 | ACTION5 | (W8, N12, E12) | (20, 20) | active = (2+1) % 3 = 0 |
| 13 | ACTION3 | (S8, N12, E12) | (28, 28) | active = 0; θ_0 W→S. hinge_1 (16, 40). hinge_2 (16, 28). |
| 14 | ACTION3 | (E8, N12, E12) | (36, 20) | θ_0 S→E. hinge_1 (24, 32). hinge_2 (24, 20). |
| 15 | ACTION2 | (E7, N12, E12) | (35, 20) | L_0 → 7. |
| 16 | ACTION2 | (E6, N12, E12) | (34, 20) | L_0 → 6. |
| 17 | ACTION2 | (E5, N12, E12) | (33, 20) | L_0 → 5. |
| 18 | ACTION2 | (E4, N12, E12) | (32, 20) | L_0 → 4. ✓ tip on drop_zone_red. |
| 19 | ACTION6 @ (32, 20) | (E4, N12, E12) | (32, 20) | click hits tip-marker → drop object_red at (32, 20). object_red.interaction → TANGIBLE; tip_carry_halo removed; win predicate fires → `next_level()`. |

Total length: 10 (phase 1) + 9 (phase 2) = 19 actions.

**Difficulty justification**:
- (a) Random-resistance: P(uniform-6) for length-19 witness ≈ (1/6)^19 ≈ 1.7×10⁻¹⁵ per window. Astronomically near-zero. ✓
- (b) Human-tractable: ~3 minutes. The player understands cycle/rotate from L1 and length-adjust from L2; at L3 they discover carry-and-drop by walking the tip onto object_red (auto-pickup; tip-carry halo appears) and clicking the tip to drop.
- (c) Planning depth (L3 = challenging post-discovery):
  - Post-discovery decision count at level start = 6 valid first actions ≥ L2's count. ✓
  - **Trivial heuristic that fails**: greedy-toward-target, applied after pickup as "rotate the chain to bring tip toward `(32, 20)` directly". A fully-informed player using greedy at the pickup-pose `(W8, N12, N12)` rotates seg 2 from N to E (one ACTION4), arriving at tip `(20, 20)`. They expect drop-zone there but it's actually at `(32, 20)`. Greedy doesn't anticipate that the pickup-pose (with seg 0 retracted to 8 *and* pointing west) is geometrically incompatible with the drop-pose (which needs seg 0 length 4 *and* pointing east). The player must reverse seg 0's direction (W→E, two CCW rotations) AND further retract from 8 to 4, between the pickup and the drop.
  - **Where the heuristic diverges from the witness**: at action #11 (after the ACTION4 rotates seg 2 to E), greedy would click immediately. The drop happens at `(20, 20)` instead of `(32, 20)`, and the win predicate fails. The witness's ahead-of-time reasoning anticipates that the pickup-pose seg-0 direction (W) and seg-0 length (8) are *both* wrong for the drop, requiring 2 rotations + 4 retracts on seg 0 between rotating seg 2 and clicking the tip. Six coordinated actions the greedy heuristic skips.
- (d) Step budget: 100. ≥ L2's 100 (not shrinking). 5.3× witness — generous. ✓

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5, 6]` declared at `__init__`. Per-level gating via `_get_valid_actions`:
- L1: gate to {3, 4, 5, 6} — ACTION1/2 not offered (length-adjust is L2+).
- L2, L3: full {1, 2, 3, 4, 5, 6}.
- ACTION7 is unused.

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | EXTEND active segment by +1 (max 14). | L2+, and L_active < 14, and resulting pose must be in-bounds. |
| ACTION2 | RETRACT active segment by -1 (min 1). | L2+, and L_active > 1. |
| ACTION3 | Rotate active segment 90° CCW (E→N→W→S→E). | always. |
| ACTION4 | Rotate active segment 90° CW (E→S→W→N→E). | always. |
| ACTION5 | CYCLE active hinge: `active = (active + 1) mod N`. | always. |
| ACTION6 | CLICK at display-pixel (x, y). Cases: (a) clicked sprite is a hinge → set active to that hinge's index (this is M1's alternate implementation); (b) clicked sprite is the tip-marker AND carrying an object → drop the carried object at the tip's current cell (M4); (c) anything else → no-op. | always. |

Rotations and length-adjusts that would result in any segment-cell being out-of-bounds are *rejected* (no state change), but the action is still consumed.

## 6. HUD and per-game state

**HUD widget**: `step_counter_hud`, a `RenderableUserDisplay` subclass. Renders a horizontal bar at row 63 of the frame: filled cells (palette 11 yellow) on the left, empty cells (palette 4 off-black) on the right; fill ratio = `current_steps / max_steps`. Updated each `step()` call.

**Per-game internal state** (all visible in the rendered frame; no hidden state):
- `pose`: list of 3 `(θ_i, L_i)` tuples. θ_i ∈ {0=E, 90=N, 180=W, 270=S}; L_i ∈ {1..14}.
- `active_hinge`: int ∈ {0, 1, 2}.
- `carried_object`: Sprite reference or None.
- `_step_counter_ui`: HUD instance.

**Visual surfacing of state** (per checklist item 19):
- `active_hinge` → `active_halo` sprite drawn around the active hinge cell.
- `carried_object` (when not None) → `tip_carry_halo` overlay around the tip cell, in the object's colour.
- `pose` → segment sprites placed at hinge positions with `set_rotation` matching θ_i and `pixels` rebuilt to length L_i.
- `_step_counter_ui.current_steps` → bar fill at row 63.

## 7. Win condition

Per level:
- **L1, L2**: tip cell == target_pad center cell. Concretely: `tip == (target_x, target_y)`.
- **L3**: every `object_*` sprite is currently at its colour-matched `drop_zone_*` cell *and* not currently carried. With the current single-object design: `object_red.position == drop_zone_red.center AND carried_object is None`.

Triggers `self.next_level()`. The engine fires `self.win()` when `next_level()` is called past the last level.

The win check runs at the end of `step()` after the action's effects are applied.

## 8. Lose condition

`self._action_count >= step_budget` for the current level → `self.lose()`. Step budget per level lives in `Level(... data={"step_budget": N})`.

No other lose state — no hazard, no soft-lock. The chain pose is always recoverable (every rotation and every length change has an inverse action available within the same valid-actions set).

## 9. Novelty note

Closest entries in `mechanic-novelty/taxonomy-of-25-games.md`:
- **`s5i5` rod-stretch-retract**: family-level near-miss. **Distinguishing rule**: s5i5 has multiple **independent** rods, each anchored on its own axis, that **stretch axially** via clicking colour swatches; no rotation. Candidate has **one connected** chain whose segments **rotate** about hinges (and *also* stretch via length-adjust, but rotation is the primary verb at L1). Cast count differs: s5i5 has multiple separate rods + a colour-swatch panel; candidate has one chain + hinge markers. Visual signature differs.
- **`cn04` nub-pair-glyph**: rotation-family near-miss. **Distinguishing rule**: cn04 rotates a **single rigid jigsaw piece** as a whole; the win condition is connector-pixel snap. Candidate rotates **one segment of a multi-segment chain**; the win condition is tip-on-target, not connector match.

Closest entries in `prior-games/index.md`:
- **`qz73` radial-cycle-lock**: rotation-family near-miss. **Distinguishing rule**: qz73 is a **single rigid rotor** with multiple radial tips that move together as a rigid body. Candidate is **N independent hinges**; rotating one hinge moves only that one segment's heading. qz73 has a "lock individual tips" mode; candidate has none.
- **`gx7m` gear-mesh-cascade**: rotation-propagation near-miss. **Distinguishing rule**: gx7m gears propagate **rotation** to meshed neighbours (orientation-only); candidate propagates **translation** to descendant segments via the parent's vector contribution (position-only; segments' headings are independent).
- **`pj7k` rolling-cube-face-paint**: distinct (a single rolling cube vs a polyline chain).
- **`pz4t` anchor-pivot-place**: distinct (placing-and-rotating components vs no-placement).

`prior-games/index.md` is non-empty (30 entries); the candidate's family `hinge-chain-reach` does not appear in the index.

Negative-similarity check (per `negative-similarity-check.md`): candidate vs the closest neighbours yields shared-dimension counts of 3 (vs s5i5 — light axes only), 4 (vs qz73 — borderline; heavy axes 6 and 8 diverge cleanly), 3 (vs cn04), 2 (vs gx7m), 1 (vs pj7k). The qz73 borderline is acceptable on the heavy axes (visual signature: radial star vs articulated polyline; core dynamic: rigid-body rotation vs articulated translation).
