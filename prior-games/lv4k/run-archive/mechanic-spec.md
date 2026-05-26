# Mechanic Spec — `lv4k`

## 1. Title

Lever-Balance Torque

## 2. Mechanic family

A horizontal beam pivots on a fulcrum. The player picks weights from a tray and places them onto fixed slot positions along the beam. The beam's tilt is a deterministic integer function of `Σ (mass × arm)` across all placed weights, and is rendered as the per-slot vertical offset of beam segments. The player wins each level by emptying the tray such that the beam is **level (tilt = 0)** at the moment the last weight is placed. The mechanic combines two §3.4 prior categories: **basic physics** (rigid-body torque, lever-arm equilibrium) and **objectness** (distinguishable weight sprites with persistent identity through pick / place / lift cycles).

## 3. Sprite roster

The frame is 64×64 with grid_size = (64, 64). Palette uses values `{1, 3, 4, 5, 9, 11, 12, 14}` plus transparent `-1`.

| Name | Pixel matrix size | Palette values | Tags | Role |
|---|---|---|---|---|
| `beam_segment` | 8×4 | `1, 3, 4` | `["beam", "slot"]` (per-instance also tagged `slot_<idx>`) | One placement slot of the beam; *clickable*; visual + click-target. Multiple instances per level, one per placement slot. Repositioned in y per turn to render tilt. Internal pixel structure: outer 1-pixel frame in palette `1` (off-white), inner fill in palette `3` (grey), darkened upper edge in palette `4` for sub-cell shadow. |
| `fulcrum_post` | 8×12 | `4, 5` | `["fulcrum"]` | Fixed support post under the beam. Triangular top transitioning to vertical post body. Internal pixel structure: triangle silhouette (palette `4`) with a 1-pixel inner highlight in palette `5`. Non-clickable, non-collidable for placement. |
| `weight_orange` | 4×4 | `5, 12` | `["weight", "weight_mass1"]` | Mass-1 weight. Ring-shape: outer frame palette `12` (orange), inner 2×2 palette `5` (black). Clickable when in tray (selectable) or on beam (lift back to tray). |
| `weight_blue` | 8×4 | `5, 9` | `["weight", "weight_mass2"]` | Mass-2 weight. **Single elongated frame** (8 cells wide × 4 tall) — outer 1-pixel frame in palette `9` (blue), inner fill in palette `5` (black). Wider footprint, not a doubled motif: width = mass cue, no glyph resemblance. (Revision addressing critique-revisions.md Issue #2.) |
| `tray_slot` | 8×6 | `4` | `["tray_slot"]` | A frame outline in the tray showing where weights start. Holds at most one weight. Frame palette `4`; interior transparent so the weight sprite shows through. Click on `tray_slot` clicks the weight inside it. |
| `tray_slot_wide` | 12×6 | `4` | `["tray_slot"]` | Wider variant for housing mass-2 weights in the tray. |
| `passenger` | 4×4 | `5, 14` | `["passenger"]` | (L3 only) A "passenger" piece sitting on a beam slot. Cross-shape with palette `14` (green) and palette `5` (black) interior. Distinct shape (not a ring) signals it is *not* a tray weight and is not user-movable. |
| `selection_halo` | 8×6 (and 12×6 variant) | `11` | `["halo"]` | A bright yellow outline halo that wraps the currently-selected tray weight. Renders one layer above the weight. Multi-pixel internal structure (4-corner brackets, not a solid frame). |
| `step_counter_hud` | n/a (RenderableUserDisplay) | `4, 14` | n/a | A horizontal bar at frame row 0 reflecting `(remaining_steps / step_budget)`. Filled portion palette `14` (green); depleted portion palette `4` (off-black). |

(Each per-level sprite roster also includes the appropriate count of `tray_slot` / `tray_slot_wide` instances pre-positioned in the tray row.)

### Style and palette

- Background colour: palette `3` (grey). Letter-box: palette `4` (off-black).
- Slot positions are **visually identical**, distinguishing only by their position relative to the fulcrum. The fulcrum is the visual anchor — its position tells the player where the pivot is.
- All sprites carry sub-cell internal structure (rings, frames, multi-cell shapes) — passes the no-info-loss-at-32×32 test.

## 4. Level progression, mechanic enumeration, and witness solutions

The 64×64 playfield uses fixed regions:

- **Beam zone**: y rows 24..35 (10 rows wide vertically; the beam visually occupies a 4-row band whose y depends on tilt level).
- **Fulcrum zone**: y rows 28..39, centred under the fulcrum-x of the active level.
- **Tray zone**: y rows 44..49 — row of `tray_slot` frames holding unplaced weights.
- **HUD zone**: y rows 0..0 (1-pixel bar) and frame edges.

Slot **arm values** are integer offsets from the fulcrum along the beam; geometry maps each arm to a fixed x:

| Arm | x-position |
|---|---|
| -4 | 8 |
| -3 | 16 |
| -2 | 24 |
| -1 | 32 |
| 0 (fulcrum, *no placement*) | 40 |
| +1 | 48 |
| +2 | 56 |

(Arm 0 is occupied by the fulcrum-post; the slot is *not* placeable.)

Per-level fulcrum-x and which arms are exposed differ. Tilt level T at any moment is computed as `T = clamp(round(Σ(mass × arm) / 2), -2, +2)`. A `T` value of ±2 means the beam visually rocks by ±3 cells at the slot ends. The win predicate is `len(tray_weights) == 0 and T == 0`.

### Level 1 — base dynamic system (1 mechanic)

Layout: 4 placement slots at arms `{-2, -1, +1, +2}`; fulcrum centred (arm 0). Tray: 2 × `weight_orange` (mass-1).

- **Mechanics required by the witness** (N = 1):
  - **M1: place-balance** — the player must place every tray weight onto a beam slot such that the resulting torque sum is zero. Triggered every time the player clicks a tray weight then a beam slot.
- **Necessity per mechanic (counterfactual)**:
  - *L1 cannot be solved without triggering M1 because* the win predicate requires `len(tray_weights) == 0`; since the tray starts non-empty and weights move only via clicks that place them on slots, no sequence of zero placements satisfies the win predicate. The trivial "place both on the central slot" fallback is blocked by the level geometry: there is no placement slot at arm 0 (the fulcrum-post is rendered there and the click-hit-test misses), so all placements consume a non-zero-arm slot. With two mass-1 weights and only one weight permitted per slot, the only torque-zero placements are pairs `{-2, +2}` or `{-1, +1}` — both require triggering M1.
- **Witness solution** (shortest, 2 actions):
  - `[ACTION6@(48, 26), ACTION6@(8, 26)]`
  - Action 1: click slot at x=48 (arm +1) — wait, but no weight is selected yet. Let me redo.
  - Actually selection happens via clicking a tray weight first. Each placement requires 2 clicks (select-then-place). So the witness has 4 actions:
  - `[ACTION6@(8, 47), ACTION6@(24, 26), ACTION6@(20, 47), ACTION6@(56, 26)]`
    - 1: click tray weight at x=8 → selects first orange weight.
    - 2: click slot at x=24 (arm -2) → places it; tilt = -1.
    - 3: click tray weight at x=20 → selects second orange weight.
    - 4: click slot at x=56 (arm +2) → places it; tilt = -1 + 1 = 0. Tray empty + tilt 0 → win.
- **Difficulty justification**:
  - **(a) Random-resistance**: A vision-blind / random-policy agent has 64×64 click candidates per ACTION6 plus the implicit need to *alternate* select-then-place. Random policy does not preserve "select then place same weight on a slot" pairing; even if 4 random clicks happen to land on tray weights and slots, the probability they land in the correct alternating order with arm-sums zeroing is roughly `(8 / 4096)^4` for clicking inside the right boxes × `2 / 6` for picking opposite arms — well below `1/10000`.
  - **(b) Human-tractable**: An attentive human reads "tray of two weights, beam over fulcrum" and tries the symmetric placement first; ~30 seconds. Comfortably under 2 minutes.
  - **(c) Planning depth**: L1 has *no strict planning requirement*. Once the player understands that clicking a tray weight then a slot places it, the symmetric-placement insight is immediate. The level is a discovery gate — once mechanics are known, the win is one-step planning.
  - **(d) Step budget**: 12 actions. Witness is 4. Generous over witness; allows ~4 wrong placements + lifts before time-out. (Lifts cost 1 action just like placements, computed via `_action_count`.)

### Level 2 — base system + 1 new mechanic (2 mechanics)

Layout: 6 placement slots at arms `{-4, -3, -1, +1, +2, +3}` (asymmetric — the fulcrum is offset to the **right** of geometric centre). The arm-axis is `{-4, -3, -2, -1, 0=fulcrum, +1, +2}` but the level only places clickable slot sprites at arms `-4, -3, -1, +1, +2`; arms `-2` and `+3` exist as positions but are not exposed for L2 (so as not to crowd L2; revealed in L3).

Wait — let me restate cleanly. L2 layout:

- Fulcrum-x at position 32 (so arm 0 is at x=32). Arms exposed: `{-3, -2, -1, +1, +2, +3}` mapped to x-positions `{8, 16, 24, 40, 48, 56}`. 6 placement slots.
- Tray: 1 × `weight_blue` (mass-2) + 2 × `weight_orange` (mass-1).

- **Mechanics required by the witness** (N+1 = 2; introduces 1 new mechanic):
  - **M1: place-balance** (carried forward from L1) — every tray weight must be placed.
  - **M2: mass-arm-asymmetry** (NEW) — the torque contribution of a weight is `mass × arm`, not `arm`. Mass-2 weights swing the beam twice as hard at the same arm, so placing them at non-symmetric arms requires careful counter-placement of mass-1s.
- **Necessity per mechanic (counterfactual)**:
  - *L2 cannot be solved without triggering M1 because* same as L1 — tray must empty for the win predicate. No beam slot at arm 0; all placements consume a non-zero-arm slot. The 3 tray weights cannot all fit on the same arm side without leaving the tray non-empty, so M1 is exercised every solution.
  - *L2 cannot be solved without triggering M2 because* the only torque-zero placements with `[m2, m1, m1]` require treating the mass-2 weight differently from the mass-1s. Concrete: if the player ignored mass and placed by arm-only (treating m2 as m1), the torque would be `arm_m2 + arm_o1 + arm_o2`. To zero that with arms in `{-3, -2, -1, +1, +2, +3}`: sets of 3 distinct arms summing to 0 include `{-3, +1, +2}`, `{-2, -1, +3}`, etc. But with the actual mass formula `2×arm_m2 + arm_o1 + arm_o2`, zero-sum requires `2×arm_m2 = -(arm_o1 + arm_o2)`. Substituting any "arm-only-zero" placement (e.g. m2 at arm -3, m1 at +1, m1 at +2): real torque = `2×(-3) + 1 + 2 = -3 ≠ 0`. The player MUST pick a mass-2 arm position whose doubled contribution is offset by the available mass-1 arm-sum — this *is* the M2 mechanic.
- **Witness solution** (shortest, 6 actions):
  - `[ACTION6@(8, 47), ACTION6@(40, 26), ACTION6@(20, 47), ACTION6@(8, 26), ACTION6@(36, 47), ACTION6@(56, 26)]`
    - 1: click `weight_blue` in tray at x=8 → selects mass-2.
    - 2: click slot at x=40 (arm +1) → places m2; contribution = 2 × +1 = +2. Tilt = +2.
    - 3: click `weight_orange` in tray at x=20 → selects mass-1 (#1).
    - 4: click slot at x=8 (arm -3) → places m1; contribution = -3. Tilt = +2 + -3 = -1.
    - 5: click `weight_orange` in tray at x=36 → selects mass-1 (#2).
    - 6: click slot at x=16 (arm -2)... wait, arm -2 is not exposed in L2.

Let me retry with the correct exposed arms `{-3, -2, -1, +1, +2, +3}`. Hmm I said -2 IS exposed. Let me correct: exposed arms for L2 = `{-3, -2, -1, +1, +2, +3}` — 6 placement slots. Re-check witness:

  - `[ACTION6@(8, 47), ACTION6@(40, 26), ACTION6@(20, 47), ACTION6@(8, 26), ACTION6@(36, 47), ACTION6@(16, 26)]`
    - 1: click tray weight_blue (x=8 in tray) → selects mass-2.
    - 2: click slot at arm +1 (x=40) → places m2; torque = 2×(+1) = +2. Tilt = +2.
    - 3: click tray weight_orange (x=20) → selects mass-1 (#1).
    - 4: click slot at arm -3 (x=8) → places m1; torque = -3. Total = +2 + -3 = -1. Tilt = clamp(round(-1/2), -2, +2) = 0… wait the tilt formula needs reconsidering.

Hmm, I've been sloppy. Let me redefine tilt:

`tilt_raw = Σ (mass × arm)`. Then `tilt_level = clamp(sign(tilt_raw) × ceil(|tilt_raw|/2), -2, +2)`. Wait this allows |tilt| values 0, 1, 2 and saturates. But for the win predicate I want tilt_raw == 0, not tilt_level == 0.

Cleaner: **win predicate is `tilt_raw == 0`** (exact integer torque equilibrium). The displayed `tilt_level` is the *visualisation* and is a separate quantity used only for rendering and (in L3) passenger-displacement. So:

- `tilt_raw = Σ (mass × arm)` — used for win predicate (must be exactly 0).
- `tilt_level = clamp(tilt_raw // 2, -2, +2)` — used for rendering and L3 passenger-slide trigger.

(Integer division with rounding-toward-zero: `tilt_raw=1` → `tilt_level=0`; `tilt_raw=2` → `tilt_level=1`; `tilt_raw=-3` → `tilt_level=-1`; `tilt_raw=-4` → `tilt_level=-2`; `tilt_raw=-5` → `tilt_level=-2` (clamped); etc.)

L2 witness with `tilt_raw==0` requirement, tray = `[m2, m1, m1]`:

Need `2×a_m2 + a_1 + a_2 = 0` with `a_m2, a_1, a_2 ∈ {-3,-2,-1,+1,+2,+3}` distinct.

Options:
- `a_m2 = -1` → `a_1 + a_2 = 2`. Pairs: `(-1, +3)` (-1 used), `(+1, +1)` (repeat), `(-2, +4)` (4 not exposed), `(-3, +5)`. Only `(-1, +3)` would work but -1 is taken. Hmm.
- `a_m2 = +1` → `a_1 + a_2 = -2`. Pairs: `(-3, +1)` (1 taken), `(-1, -1)` (repeat), `(+1, -3)` (1 taken), `(-2, 0)` (0 is fulcrum). Hmm wait, we can use `(-3, +1)` if a_m2 = +1 makes +1 unavailable, but maybe `(-2, 0)`? No 0 is fulcrum. Try `(-3, +1)` → +1 already taken. Try `(+1, -3)` same issue. Hmm.
  - With `a_m2=+1` taken, remaining arms = `{-3,-2,-1,+2,+3}`. Need pair summing to -2: `(-3, +1)` (1 taken), `(-2, 0)` (no 0), actually `(-3, +1)` = -2 but +1 taken... hmm just check: in `{-3,-2,-1,+2,+3}`, pairs summing to -2: `(-3, +1)` not avail, `(-2, 0)` not avail, `(-1, -1)` repeat, `(+1, -3)` not avail. No solution.
- `a_m2 = -2` → `a_1 + a_2 = 4`. Pairs in `{-3,-1,+1,+2,+3}`: `(+1, +3)`. ✓
- `a_m2 = +2` → `a_1 + a_2 = -4`. Pairs in `{-3,-2,-1,+1,+3}`: `(-1, -3)`. ✓
- `a_m2 = -3` → `a_1 + a_2 = 6`. Pairs in `{-2,-1,+1,+2,+3}`: max sum = +5. ✗
- `a_m2 = +3` → `a_1 + a_2 = -6`. Pairs in `{-3,-2,-1,+1,+2}`: max -sum = -5. ✗
- `a_m2 = -1` → `a_1 + a_2 = 2`. Pairs in `{-3,-2,+1,+2,+3}`: `(-1, +3)` not avail (-1 taken), `(-2, +4)` (no), `(+2, 0)` (no), `(+3, -1)` (-1 taken), `(-3, +5)` (no). No solution.
- `a_m2 = +1` (already done) — no solution.

So only two witness families: `m2 at -2 with m1s at +1, +3` OR `m2 at +2 with m1s at -1, -3`. Mirror images.

Witness (12 actions for 6 clicks pairs... wait one click is one action; but each placement is 2 actions: select + place. With 3 weights, 6 actions total).

`[ACTION6@(8, 47), ACTION6@(16, 26), ACTION6@(20, 47), ACTION6@(40, 26), ACTION6@(36, 47), ACTION6@(56, 26)]`
- 1: click tray slot containing m2 at x=8 → m2 selected.
- 2: click beam slot at x=16 (arm -2) → m2 placed; raw torque = 2 × (-2) = -4.
- 3: click tray slot containing m1#1 at x=20 → m1 selected.
- 4: click beam slot at x=40 (arm +1) → m1 placed; raw torque = -4 + 1 = -3.
- 5: click tray slot containing m1#2 at x=36 → m1 selected.
- 6: click beam slot at x=56 (arm +3) → m1 placed; raw torque = -3 + 3 = 0. **Win**.

Wait — beam slot at arm +1 should be at x=40, but I said fulcrum-x = 32 and arm +1 → x=32+8=40. ✓. Beam slot at arm +3 → x=32+24=56 ✓. Beam slot at arm -2 → x=32-16=16 ✓.

Witness valid.

- **Difficulty justification**:
  - **(a) Random-resistance**: 6 actions, each ACTION6 with 4096 click coords. Productive clicks land in `tray_slots` (3 slots × ~6×8 cells each ≈ 144 useful cells) or beam slots (6 × 8×4 = 192). To select-then-place 3 weights correctly takes 6 specific paired clicks; among ~3500^6 random sequences only a handful satisfy. ≪ 1/10000.
  - **(b) Human-tractable**: First-time human spends ~30s realising mass-2 differs from mass-1, then ~60s working out the algebraic constraint → ~90s total. Within 2-min target.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start**: post-discovery (knowing m2 is heavier), the player faces a choice of `2 (which mass-2 placement family) × 3 (where to begin in the order) = 6` distinct first actions. > 2 first actions → not 1-action lookup.
    - **Plausible wrong path**: a post-discovery player might naïvely place mass-2 at arm `+1` (closest to fulcrum, "small swing"); then `2 × 1 = 2`; remaining mass-1s must sum to −2; possible with `(-3, +1)` but +1 is already used, `(-2, 0)` no fulcrum slot, `(-1, -1)` repeats. So no solution exists with m2 at +1 — the heuristic "minimize swing per placement" *fails*. Player must instead place m2 at `±2` which seems "wasteful" but is the only solvable choice.
    - **Witness reasoning chain**: post-discovery, the player computes `2×a_m2 + a_o1 + a_o2 = 0`. Inspecting available `(arm, slot)` pairs and recognising m2 carries 2× weight, the player rules out m2 at ±1, ±3 (no solution there) and discovers m2 must be at ±2.
  - **(d) Step budget**: 24 actions. Witness is 6. Allows `(24-6)/2 = 9` revisions (each lift+replace = 2 actions). Generous.

### Level 3 — system + 1 new mechanic (3 mechanics)

*[Revised per critique-revisions.md Issue #1: tray composition changed from `[m2,m2,m1,m1]` to `[m2,m2,m2,m1]` to make M3 counterfactually necessary; witness, counterfactual statements, and difficulty (c) updated accordingly.]*

Layout: 6 placement slots same as L2 (arms `{-3, -2, -1, +1, +2, +3}`; fulcrum-x = 32). Tray: 3 × `weight_blue` (mass-2) + 1 × `weight_orange` (mass-1) = 4 weights total. Plus a **passenger** sprite starting at slot arm `+2` (x=48).

- **Mechanics required by the witness** (N+1 = 3; introduces 1 new mechanic on top of L2):
  - **M1: place-balance** (carried forward).
  - **M2: mass-arm-asymmetry** (carried forward).
  - **M3: tilt-passenger-slide** (NEW) — when `|tilt_level| ≥ 2` after a placement (i.e. `|tilt_raw| ≥ 4`), the passenger sprite shifts by 1 slot toward the **dipping** end (the side with greater torque). If the shift would move it off the beam (past arm ±3) OR onto arm 0 (which is the fulcrum-only position, not in `exposed_arms`), the level immediately calls `lose()`.
- **Necessity per mechanic (counterfactual)**:
  - *L3 cannot be solved without triggering M1 because* tray non-empty fails the win predicate; weights only move via clicks. (Same argument as L1 / L2 but now with 4 weights.)
  - *L3 cannot be solved without triggering M2 because* tray = `[m2, m2, m2, m1]` has total integer mass-arm products that equal zero only when each m2's contribution is independently doubled. Solutions of `2a + 2b + 2c + d = 0` with distinct arms in `{-3,-2,-1,+1,+2,+3}` reduce to `a + b + c = -d/2`, requiring `d` to be ±2 (the only m1-compatible values producing integer `(a+b+c)`). So m1 must be at ±2; m2s fill three of the remaining arms summing to ∓1. If the player ignored mass differences (treated everything as mass-1) and tried `a + b + c + d = 0` with d∈{-3..-1, +1..+3}, they'd reach configurations like `{-3,-2,+2,+3}` or `{-3,-1,+1,+3}` — but real torque is non-zero for those: e.g. `m2@-3, m2@-1, m2@+1, m1@+3` → `2(-3)+2(-1)+2(+1)+3 = -3`. Player must account for mass-2's 2× contribution.
  - *L3 cannot be solved without triggering M3 because* every torque-zero solution requires at least one m2 placed at arm ±3 (verified by exhaustive enumeration: the four solution families are m2@`{-3,-1,+3}`+m1@+2, m2@`{-3,+1,+3}`+m1@-2, m2@`{-3,+3,-1}`+m1@+2 (= same), m2@`{-3,+3,+1}`+m1@-2 (= same) — every solution includes both an m2@-3 and an m2@+3). A single m2 placement at ±3 contributes ±6 to tilt_raw. Even if preceded by stabilising placements (m2@∓1 = ∓2; m1@±2 = ±2), the maximum stabilisation before placing m2@±3 is `±2 ∓ 2 = 0` (placing one m2@∓1 and one m1@±2 first, both reducing tilt magnitude), which still leaves the m2@±3 placement adding |6| → resulting `|tilt_raw|` after that step is at least 6 → tilt_level = ±2 (clamped). M3 fires. There is no ordering of `{m2, m2, m2, m1}` placements that avoids triggering `|tilt_level| ≥ 2` at some step.
- **Witness solution** (shortest, 8 actions):

  Coordinates: fulcrum-x = 32. Arm-to-slot-x mapping: arm -3 → x=8; arm -2 → x=16; arm -1 → x=24; arm +1 → x=40; arm +2 → x=48; arm +3 → x=56. Tray (row y=47) has 4 cells: m1 tray-slot at x=4 (4 wide); 3 m2 tray-slots at x=12, x=24, x=36 (each 8 wide).
  
  Strategy: place the m1 first (a small +2 swing), then a stabilising m2 at the opposite small arm (m2@-1 = -2; tilt back to 0), then the two extreme m2s (m2@-3 and m2@+3 in either order; one big swing triggers M3, the other returns tilt to 0). The big swing is the M3 trigger; passenger is at +2 at that moment, slides one slot toward the dipping side, and the final placement returns tilt to 0 with passenger still on the beam.

  Witness sequence (8 actions):

  1. `ACTION6@(4, 47)` — click m1 in tray at tray-x=4 → selects m1.
  2. `ACTION6@(48, 26)` — click beam slot at arm +2 (x=48) → places m1 at +2. tilt_raw = 1×(+2) = +2. tilt_level = +1. Passenger at +2 stays.
  3. `ACTION6@(12, 47)` — click m2#1 in tray at tray-x=12 → selects m2#1.
  4. `ACTION6@(24, 26)` — click beam slot at arm -1 (x=24) → places m2#1 at -1. tilt_raw = +2 + 2×(-1) = 0. tilt_level = 0. Passenger stays.
  5. `ACTION6@(24, 47)` — click m2#2 in tray at tray-x=24 → selects m2#2. (Tray and beam clicks distinguished by y: tray-y=47, beam-y=26.)
  6. `ACTION6@(8, 26)` — click beam slot at arm -3 (x=8) → places m2#2 at -3. tilt_raw = 0 + 2×(-3) = -6. tilt_level = -2 (clamped). **M3 triggers**: beam dips left, passenger at +2 slides one slot toward -arm direction (the dipping side) → passenger now at +1.
  7. `ACTION6@(36, 47)` — click m2#3 in tray at tray-x=36 → selects m2#3.
  8. `ACTION6@(56, 26)` — click beam slot at arm +3 (x=56) → places m2#3 at +3. tilt_raw = -6 + 2×(+3) = 0. tilt_level = 0. Tray empty + tilt_raw = 0 → **WIN**. Passenger ends at arm +1, still on beam.

- **Difficulty justification**:
  - **(a) Random-resistance**: 8 actions, each ACTION6 with 4096 click coords. Productive clicks land on tray slots (~ 4 clusters × ~ 32 cells = 128) or beam slots (6 × ~ 32 cells = 192). To match the witness pattern *within* the step budget *and* avoid passenger displacement traps mid-sequence, a random policy would need to produce 8 alternating select/place clicks at specific positions. Number of valid solution orderings (sequences that win without losing the passenger) is roughly 10–20 out of ~320⁸ ≈ 10²⁰ random click-sequences. Probability of random success ≪ 1/10⁴.
  - **(b) Human-tractable**: An attentive human carrying L1/L2 understanding (mass matters, balance matters) needs ~2 minutes on L3. Initial reaction: try the m2-heavy-first heuristic and lose the passenger after a placement or two. Notice "passenger shifted when beam tilted hard". Re-strategy: small placements first, save the big +3/-3 swings for paired moves where they cancel. ~2 min total.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start**: 4 tray weights × 6 beam slots = 24 candidate first placements (post-discovery, knowing M1+M2+M3). All 24 are post-discovery legal (the player understands the rules); a fully-informed player faces ≥ 6 first-placement choices that don't immediately lose (m1 at any arm, m2 at ±1). 24 ≥ L2's 6 — strictly larger.
    - **Trivial post-discovery heuristic that fails**: the "place heavy stuff on the side opposite the passenger first to counter-stabilise" heuristic. Concrete: passenger at +2 (right side), so the heuristic places m2 at -3 first to "lean the beam left and pull the passenger back to centre". Step 1: m2@-3 → tilt_raw = -6 → tilt_level = -2 → passenger +2 → +1. Step 2: heuristic continues with another m2 on the left side to counter-stabilise: m2@-1 → tilt_raw = -8 → tilt_level = -2 (clamped) → passenger +1 → 0. Slot 0 is the fulcrum-only position (not in `exposed_arms`) → **passenger off-beam → `lose()` at step 2**. Heuristic fails after just 2 placements, even though continuing the heuristic would give a numerically valid torque-zero ending.
    - **Heuristic-vs-witness divergence at step 2**: heuristic places m2@-1 (continuing the leftward-counter-stack); witness places m2@-1 also — but only AFTER stabilising with m1@+2 first (witness step 1 was m1@+2, which the heuristic skipped). The divergence is at step 1: the heuristic skips the m1@+2 stabiliser because m1 is "small" and feels like a wasted placement; the witness recognises that m1@+2 is the only piece that locks the tilt at +2 → tilt_level = +1 (safe) and lets subsequent m2 placements happen without crossing tilt_level = ±2 prematurely. The heuristic's step-1 "skip the small piece, lead with heavy" decision irrecoverably leads to losing the passenger.
  - **(d) Step budget**: 36 actions. Witness is 8. Allows `(36 − 8)/2 = 14` lifts/replaces. Generous; budget does not shrink across L1 → L2 → L3 (12, 24, 36) — strictly increasing, more budget for more discovery cost.

## 5. Action mapping

`available_actions = [6]`. Pure click; no movement keys, no commit/modal action.

| Action ID | Semantic | Gating |
|---|---|---|
| ACTION6 | Click at `(x, y)` (in display coords). The intent is decided by what the click hits: `tray_slot` containing a weight → select that weight (or deselect if same weight already selected). `beam_segment` slot containing a weight → lift that weight back to its origin tray slot, deselecting any current selection. `beam_segment` slot empty AND a tray weight is selected → place selected weight there. Click on empty space → no-op. | always |

`_get_valid_actions()` returns the default (`super()._get_valid_actions()`); no per-turn restriction on which slots can be clicked.

## 6. HUD and per-game state

### HUD widgets

- `step_counter_hud` (`RenderableUserDisplay`): a 1-pixel horizontal bar at frame row 0. Filled portion (palette `14`, green) reflects `(remaining_steps / step_budget)`. Updated every step.

### Per-game persistent state

- `self.selected_weight: Sprite | None` — the currently-selected tray weight (or None). Visualised by the `selection_halo` sprite layered above the selected weight; halo is moved to the new position on selection change and hidden when no selection.
- `self.placement: dict[int, Sprite]` — slot-index → weight-sprite mapping, listing which weights are currently on which beam slots.
- `self.tray_origin: dict[Sprite, tuple[int, int]]` — for each weight, the tray (x, y) it returns to when lifted.
- `self.passenger_arm: int | None` — (L3 only) the arm position of the passenger sprite, or None if no passenger.
- `self.fulcrum_x: int` — pixel x of the fulcrum (level-specific).
- `self.exposed_arms: list[int]` — per-level list of clickable arm offsets.
- `self.step_budget: int`, `self.steps_remaining: int` — drained each non-RESET action.
- `self.beam_segments: dict[int, Sprite]` — slot-arm → beam_segment sprite reference, for repositioning on tilt change.

### Internal helpers

- `_compute_torque() -> int`: returns `Σ mass × arm` over `self.placement`.
- `_render_tilt(tilt_level)`: repositions every `beam_segment`, every placed `weight_*`, and (L3) the `passenger` sprite vertically based on the current `tilt_level`.
- `_displace_passenger_if_needed(tilt_level)`: (L3 only) if `|tilt_level| ≥ 2`, slides passenger one slot toward the negative-tilt direction; if it falls off the exposed-arm range, calls `self.lose()`.
- `_check_win()`: returns `len(tray_occupied()) == 0 and _compute_torque() == 0`.

### Hidden-state visibility (checklist item 19)

Every piece of internal state has a persistent visual cue:

| Internal state | Visual cue |
|---|---|
| `selected_weight` | `selection_halo` sprite layered above it; brightens the weight visually. |
| `placement[arm]` | placed weight sprite is rendered on top of the corresponding beam slot. |
| `tilt_level` | the *position* of the beam segments and placed weights is per-tilt; player sees the beam tilt directly. |
| `passenger_arm` | the passenger sprite is rendered at its current arm slot. |
| `steps_remaining` | step_counter_hud bar. |

No state mutation occurs without a corresponding visible change.

## 7. Win condition

After every step, evaluate:

```
all_placed = (every weight in the level's tray-origin set is present in self.placement.values())
torque_zero = (sum(mass * arm for arm, w in self.placement.items()) == 0)
win = all_placed and torque_zero
```

If `win`, call `self.next_level()`. After all 3 levels are advanced, the engine auto-calls `self.win()` per `NovaBaseGame` parent contract.

The win predicate is a pure function of `self.placement` (no time-dependence), so the engine can replay any recording deterministically.

## 8. Lose condition

Two predicates (the second only applies in L3):

1. **Step exhaustion**: `self.steps_remaining <= 0` → `self.lose()`. Drained 1 per non-RESET action.
2. **Passenger fell off beam (L3)**: after `_displace_passenger_if_needed(tilt_level)` shifts the passenger, if its new arm value is not in `self.exposed_arms` (i.e. it slid past arm -3 or +3), call `self.lose()` immediately.

Note: there is no instant-fail on placing a weight anywhere — wrong placements just mis-balance the beam, recoverable by `lift_to_tray`. Only step-exhaustion and (L3) passenger-displacement are loss conditions.

## 9. Novelty note

### Closest taxonomy entries

- **`kx14` (tide-tilt-buoyant)** [from `prior-games/index.md`]. Concrete distinguishing rule: kx14's "tilt" is a *fluid-surface-inclination* mechanic where a water surface inclines and floating balls move via buoyancy; lv4k's "tilt" is *rigid-body torque equilibrium* where a beam pivots about a fulcrum and the player must zero the integer torque sum. kx14 has no fulcrum, no mass-arm asymmetry, no rigid placement slots, and no passenger-slide loss condition. The kx14 win condition (balls reach target cells via buoyancy) is positional; lv4k's is configurational (torque sum equals zero with all weights placed).
- **`pj7k` (rolling-cube-face-paint)**: rolling and cube-face permutation. Different mechanic — lv4k has no rolling, no traversal, no cube faces; only weight placement. No surface-shared with pj7k beyond palette discipline.
- **`pz4t` (anchor-pivot-place)**: jigsaw tiling with click-anchored sprite rotations. The "pivot" in pz4t is a placement-anchor for sprite rotation; in lv4k, the fulcrum is a rigid-body pivot about which torque is computed. Different concept entirely.
- **`vc33` (row-slide-pull-tab)**: row swapping. Different — lv4k has no row swap and no left/right slide of an entire group of pieces; weights are independently placed.

### Closest reference-game entries

- **`sb26` (tile-place-commit)**: tile-on-slot placement + ACTION5 commit. Different — sb26 commits a row of tiles for hint-feedback (Mastermind-style); lv4k has no commit/feedback mechanic, the beam visually responds in real time and there are no hint colours. sb26 also requires inferring a hidden target from feedback; lv4k's target (torque = 0) is mathematical, not learned through hint propagation.
- **`vc33` (row-slide-pull-tab)**: as above.
- **`lp85` (row-col-shift-grid)**: clicking buttons applies fixed permutations to a grid. Different — lv4k has no permutation operator; weights are placed statically and the tilt is a continuous integer function of placements.

### Negative-similarity-check verdict

Per `mechanic-pick.md` § Negative-similarity, no prior shares 3+ surface dimensions with lv4k. Visual signature (single horizontal beam + fulcrum + tray) and core dynamic (rigid-body torque equilibrium) are both genuinely novel against the 25 + 19 prior corpus.
