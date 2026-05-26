# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (this run): mechanic family `hinge-chain-reach`, 4-char ID `nb6t`.
- skills/code/spec-template.md: 9-section schema.
- skills/code/universal-scaffold.md: code structure constraints.
- skills/code/novaengine-api.md: engine API.
- skills/code/id-generation.md: ID rules (already used for `nb6t`).
- skills/design-constraints/composition-and-tutorial.md: 3-level structure (L1 base, L2 +1/+2, L3 +1/+2).
- skills/design-constraints/difficulty-rules.md: per-level (a-d) bullets.
- skills/design-constraints/checklist.md: items 1-21.
- skills/design-constraints/core-knowledge-priors.md: priors used (objectness, geometry, kinematic-physics).
- skills/design-constraints/forbidden-elements.md: no glyphs / clipart / cultural conventions.
- skills/global/action-enum.md: action-slot semantics.
- skills/global/color-legend.md: palette values 0..15.
- skills/conventions/reference-game-patterns.md: design patterns + anti-patterns.

## Mechanic model decision
Adopted the **vector-sum polyline** kinematic model over the strict articulated-arm model. Each segment has its own **absolute direction** θ_i ∈ {E, N, W, S} and length L_i ∈ {1..14}; the chain pose is fully described by (θ_0, L_0, …, θ_{N-1}, L_{N-1}). Hinge_(i+1) position = hinge_i + L_i · dir(θ_i). Tip = hinge_N. Each player rotation modifies the active hinge's segment direction independently of the others.

Rationale:
1. **Discoverability**: each rotation is local to one segment, so the player can build a mental model "active hinge controls one segment's heading" by experimenting with two presses.
2. **Counterfactual cleanness**: independence makes "without mechanic M, target unreachable" enumerable.
3. **Visual signature divergence from priors**: the chain is a visible polyline of independently-oriented rectangles connected at hinge circles — distinct from qz73's radial rotor (rigid-body rotation) and gx7m's gear mesh.

## Pose math (worked once)
Base anchor at fixed cell (Bx, By). For chain pose (θ_0, L_0, …, θ_{N-1}, L_{N-1}):
```
hinge_0 = (Bx, By)
for i in 0..N-1:
    hinge_(i+1) = hinge_i + L_i · DIR[θ_i]
tip = hinge_N
```
where `DIR = {E: (1, 0), N: (0, -1), W: (-1, 0), S: (0, 1)}` (screen Y is down).

Segment_i occupies the cell range from hinge_i (exclusive of segment-body, hinge owns its cell) along DIR[θ_i] for L_i cells. Segment-cell collision check (used at L2+ for walls and at all levels for grid bounds) iterates these cells.

## Witness derivation (cross-checked at write time)

### L1 witness
- Initial: base (8, 32), pose (E, E, E), L all 12, active = 0. Tip = (44, 32).
- Target: (20, 8).
- Required pose: (E, N, N) — sum = (12, 0) + (0, -12) + (0, -12) = (12, -24). Tip = (8+12, 32-24) = (20, 8). ✓
- Path: rotate hinge 1 N, rotate hinge 2 N. Active starts at 0 — cycle to 1 first, then to 2.
- Witness: `[ACTION5, ACTION3, ACTION5, ACTION3]`. Length 4.

### L2 witness
- Initial: base (8, 32), pose (E, E, E), L all 12, active = 0. Tip = (44, 32).
- Target: (16, 8).
- Required pose: (E length 8, N length 12, N length 12) — sum = (8, 0) + (0, -12) + (0, -12) = (8, -24). Tip = (8+8, 32-24) = (16, 8). ✓
- Path: retract seg 0 from 12 to 8 (4 retracts), then cycle/rotate as in L1.
- Witness: `[ACTION2, ACTION2, ACTION2, ACTION2, ACTION5, ACTION3, ACTION5, ACTION3]`. Length 8.

### L3 witness
- Initial: base (8, 32), pose (E, E, E), L all 12, active = 0. Tip = (44, 32).
- Object red at (12, 8). Drop-zone red at (32, 20).
- Phase 1 (pickup): need tip at (12, 8). Pose (E length 4, N length 12, N length 12) — sum = (4, 0) + (0, -12) + (0, -12) = (4, -24). Tip = (12, 8). ✓ Path: retract seg 0 from 12 to 4 (8 retracts), cycle to 1 + rotate N, cycle to 2 + rotate N.
- Phase 2 (drop): from current pose (E4, N12, N12), need tip at (32, 20) on drop-zone red, then ACTION6 click on tip-cell to drop.
  - Required pose for tip (32, 20): (E length 12, N length 12, E length 12). Sum = (12, 0) + (0, -12) + (12, 0) = (24, -12). Tip = (8+24, 32-12) = (32, 20). ✓
  - From (E4, N12, N12): cycle to 2 + rotate N→E (CW once), cycle to 0 + extend seg 0 from 4 to 12 (8 extends), then click tip-cell.
- Witness: `[ACTION2 ×8, ACTION5, ACTION3, ACTION5, ACTION3, ACTION5, ACTION4, ACTION5, ACTION1 ×8, ACTION6@(32,20)]`. Length 8 + 4 + 2 + 1 + 8 + 1 = 24.

(Slight reorder by cycle-via-modulo: `active = (active+1) % 3`. After phase 1, active is at hinge 2. Cycle once to 0 — needs 2 cycles via modular arithmetic. Re-checking: active ends phase 1 at hinge 2. Need active = 0 → press ACTION5 once (2 → 0 since (2+1)%3 = 0). One cycle. Need active = 2 → from 0, press ACTION5 twice (0 → 1 → 2). So phase 2 actions: cycle to 2 = ACTION5 ×2, then ACTION4 (rotate seg 2 N→E), then cycle to 0 = ACTION5 ×1 (since (2+1)%3 = 0), then ACTION1 ×8 (extend seg 0 to 12), then ACTION6 at (32,20). Total phase 2: 2 + 1 + 1 + 8 + 1 = 13. Total witness: 12 + 13 = 25.)

Re-derive phase 1 carefully:
- Active = 0 initially. We need θ_0 unchanged (still E), L_0 → 4 (retract by 8). ACTION2 ×8.
- Active still 0. Cycle to 1: ACTION5.
- Rotate hinge 1 to N: ACTION3.
- Cycle to 2: ACTION5.
- Rotate hinge 2 to N: ACTION3.
- Phase 1 total: 8 + 1 + 1 + 1 + 1 = 12 actions. Active ends at 2. Tip = (12, 8). Object red picked up.

Phase 2:
- Active = 2. Rotate hinge 2 N→E: ACTION4. (One step, CW.) Pose now (E4, N12, E12). Tip = base + (4, 0) + (0, -12) + (12, 0) = (24, 20). Object red still carried.
- Cycle to 0: from active 2, ACTION5 once (2 → 0). Pose unchanged.
- Extend seg 0 from 4 to 12: ACTION1 ×8. Pose now (E12, N12, E12). Tip = base + (12, 0) + (0, -12) + (12, 0) = (32, 20). Object on drop-zone-red cell.
- Click tip cell to drop: ACTION6 at (32, 20). Drops red. Win condition checked: red on drop-zone red. `next_level()`.
- Phase 2 total: 1 + 1 + 8 + 1 = 11 actions.

Total L3 witness: 12 + 11 = 23 actions.

### Click pixel coordinates
ACTION6 takes display-pixel coords. Camera viewport set to grid_size (= 64, 64); scale = 64 // 64 = 1; offset = 0. So display_to_grid is identity and grid coordinates pass through directly.

For L3 final click at grid (32, 20): display pixel = (32, 20).

## Step budgets (post-witness)
- L1: witness 4. Budget = 40 (10× witness, very generous; gives room for exploration).
- L2: witness 8. Budget = 100 (12.5× witness).
- L3: witness 23. Budget = 100 (4.3× witness — still meets generous-over-witness rule, and the rule "budget must NOT shrink across levels" is upheld since budget is non-decreasing 40 → 100 → 100; ties allowed).

Per difficulty-rules.md: budget must be generous; for L3 specifically: "the budget must NOT shrink relative to the witness as level number rises". 100 ≥ 100 = OK, and 100 ≥ 23 (witness) ≈ 4.3× — generous.

## Action mapping enumeration
Available actions per level:
- L1: [3, 4, 5, 6] — rotate CCW, rotate CW, cycle, click. Length-adjust not present at L1 (it's a L2 mechanic).
- L2: [1, 2, 3, 4, 5, 6] — adds extend, retract.
- L3: [1, 2, 3, 4, 5, 6] — same as L2.

`available_actions` declared at game `__init__` time is a single list — must include the union of all actions any level uses. So `available_actions=[1, 2, 3, 4, 5, 6]`. At L1, `_get_valid_actions` overrides to gate ACTION1/2 out (the engine never offers them).

## Visual design

Palette (final, 8 distinct values): `{0 white, 4 off-black, 6 magenta, 8 red, 9 blue, 11 yellow, 12 orange, 15 purple}`.

- **Background**: 0 white. Letter-box: 0 white (since grid is 64x64 and viewport is 64x64, no letter-box needed; set to background to be safe).
- **Base anchor**: 5×5, magenta (6) interior with off-black (4) rim.
- **Segment**: 12×3 rectangle, blue (9) interior with off-black (4) rim. Length scales 1..14 along axis; orientation set via `Sprite.set_rotation(0/90/180/270)`.
- **Hinge marker**: 3×3 ring, off-black (4) outer with yellow (11) inner.
- **Active-hinge halo**: 5×5 ring, yellow (11) outer with off-black (4) inner — outer-rim is 1-cell wider than the standard hinge so it visually surrounds.
- **Tip marker**: 3×3 small dot, red (8) interior with off-black (4) rim.
- **Tip-with-carry overlay**: when carrying an object, a 5×5 halo around the tip in the carried object's colour (red 8 or orange 12) — plus the tip itself stays red (player's avatar identity is constant).
- **Target pad** (L1, L2): 5×5 ring, purple (15) outer with white (0) inner (so the tip-marker visibly sits inside).
- **Object red** (L3): 2×2 dot, red (8) interior with off-black (4) rim.
- **Object blue/orange** (L3 — only one object in this design, but future-proofing): 2×2 dot, orange (12).
- **Drop-zone red** (L3): 5×5 ring, purple (15) outer with red (8) inner (colour-matches the object).
- **Step-counter HUD**: bottom row (row 63), bar fills proportional to (current/max). Colour: yellow (11) for filled portion, off-black (4) for empty.

## Hidden-state audit (checklist item 19)
- Active hinge: visible via active-hinge halo (5×5 yellow ring around the active hinge cell). Persistent for as long as the state holds.
- Currently carried object (L3): visible via tip-with-carry overlay (5×5 halo in object's colour). Persistent until ACTION6 drops it.
- Step counter: visible via HUD bar at row 63. Persistent.
- Per-segment length: visible — the segment sprite is L_i cells long.
- Per-segment direction: visible — segment orientation rendered via `set_rotation`.

No hidden state.

## Forbidden-elements audit (checklist item 7)
- No digits as glyphs.
- No letters.
- No real-world clipart (segments are abstract rectangles; hinges are abstract circles; tip is a small dot).
- No cultural conventions: red is the tip-marker (player avatar identity), not "danger". Drop-zone-red interior matches the carry colour, no green/red dichotomy. Walls absent (so no "wall = danger" signal).
- No on-screen text.

## Counterfactual table (checklist item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 cycle-active-hinge | no | Without ACTION5, active stays at 0 forever. Only seg 0's direction is mutable; segs 1, 2 stay at default E. Tip = base + L_0·dir(θ_0) + (12, 0) + (12, 0) = (8 + L_0·dir_x + 24, 32 + L_0·dir_y). For target (20, 8): need L_0·dir_x = -12 and L_0·dir_y = -24. Single segment can't do both. Unreachable. |
| L1 | M2 rotate-active-hinge | no | Without ACTION3/4, all θ stay at E. Sum = (36, 0). Tip y = 32. Target y = 8. Unreachable. |
| L2 | M1 cycle | no | Same logic as L1 — without cycle, segs 1,2 stay E length 12. Tip = (8 + L_0·dir_x + 24, 32 + L_0·dir_y). For target (16, 8): need L_0·dir_x = -16 and L_0·dir_y = -24. Single segment can't do both, even with length adjust (max L = 14 < 16+24 = 40 axial). Unreachable. |
| L2 | M2 rotate | no | Without rotate, all θ = E. Tip y = 32 always. Target y = 8. Unreachable even with length adjust (length affects sum.x, never sum.y). |
| L2 | M3 segment-length-adjustment | no | Without length-adjust, all L = 12. Tip cells reachable form a discrete set: tips of pose (θ_0, θ_1, θ_2) with each θ ∈ {E,N,W,S}. Sum components are multiples of 12. Target (16, 8) = base + (8, -24). 8 is not a multiple of 12. Unreachable. |
| L3 | M1 cycle | no | Without cycle, only seg 0 modifiable. Tip = (8 + L_0·dir_x + 24, 32 + L_0·dir_y). For pickup target (12, 8): need L_0·dir_x = -20 (impossible: |dir_x| ≤ 1, L_0 ≤ 14) AND L_0·dir_y = -24 (impossible). Unreachable. |
| L3 | M2 rotate | no | Without rotate, tip y = 32. Pickup target y = 8. Unreachable. |
| L3 | M3 length-adjust | no | Without length-adjust, all L = 12. Tip x is multiple of 12 from base x = 8: tip x ∈ {8 - 36, 8 - 12, ..., 8 + 36}. Pickup target (12, 8) needs tip x = 12; 12 - 8 = 4, not a multiple of 12. Unreachable. |
| L3 | M4 carry-and-drop (NEW) | no | Without the carry mechanic, the moveable object never moves. The win predicate ("object_red on drop-zone_red") never fires. Level unsolvable. |

All mechanics counterfactually necessary at every level they're claimed. ✓

Verification by enumeration of plausible alternate strategies for each level:
- L1: alternates: "rotate hinge 0 only" → tested above, unreachable; "click random hinges" → ACTION6 only sets active, doesn't move tip; etc.
- L2: alternates: "rotate without retracting seg 0" → tip x ∈ {discrete L=12 multiples}; can't hit 16; "retract seg 1 or 2 instead of seg 0" → ineffective because the witness's pose has them at L=12 in N direction; retracting them shortens y-displacement, target y=8 missed.
- L3: alternates: "leave seg 0 short between pickup and drop" → tip after rotate to (E4, N12, E12) is (24, 20), drop happens at (24, 20), not on drop-zone red at (32, 20); win predicate fails. "drop red back at pickup cell (12, 8) without moving" → drop-zone red is at (32, 20), so the dropped object is at (12, 8) ≠ drop-zone, win predicate fails.

## Decision-space + heuristic checks (difficulty c)
- L1: trivial post-discovery — once cycle/rotate are understood, route to (20, 8) is visually obvious. No strict planning required. ✓
- L2: post-discovery decision count at level start = 6 valid first actions. Plausible-but-wrong: rotate before retract — works, but ordering doesn't change witness length. Trivial wrong: rotate alone without retract — fails (target x=16 unreachable at L=12 multiples).
  - Witness reasoning: "tip x must be 16 = 8 + 8; with seg 0 = 8 east and segs 1,2 N at length 12, sum.x = 8, sum.y = -24, tip = (16, 8). Retract seg 0 by 4 first; then rotate 1 and 2 to N."
- L3: post-discovery decision count = 6. ≥ L2's. ✓
  - Trivial heuristic that fails: "after pickup at (12, 8), use the same chain pose to navigate around (the chain pose is now (E4, N12, N12), tip at (12, 8); rotating one hinge to E gets close to (24, 20))" — this fails because reaching drop-zone (32, 20) requires re-extending seg 0 from 4 back to 12 AND rotating seg 2 from N to E. Two coordinated changes, not one.
  - Witness reasoning chain: "after pickup, tip is at (12, 8); to reach (32, 20), I need to (a) re-extend seg 0 to 12 to recover x-reach lost during pickup; (b) rotate seg 2 from N to E so seg 2 lays horizontally; the order matters only in that both must happen before the click. Without (a), tip stays at x=24. Without (b), tip stays at x=12 with y wrong."

The post-discovery player is forced to plan ahead-of-time because the pickup-pose mid-state is not the drop-pose mid-state — they share NONE of the same θ or L values. Greedy heuristics (rotate-toward-target without re-extending) and monotone-progress (advance tip x toward 32 incrementally) both fail in this geometry.

## Compositional verification
- L1 mechanics: M1 (cycle), M2 (rotate). Count N = 2.
- L2 mechanics: M1, M2 (carried forward) + M3 (length-adjust). Count = N+1 = 3. ✓ 1 new mechanic added; L1 mechanics still required (verified above).
- L3 mechanics: M1, M2, M3 (carried forward) + M4 (carry-and-drop). Count = L2-count + 1 = 4. ✓ 1 new mechanic added; L1+L2 mechanics still required (verified above).

L2/L3 difficulty escalates by composition: L2 layers length-adjust on top of cycle/rotate (the player must coordinate three different actions); L3 layers carry-and-drop on top of all three (the player must coordinate four actions across two pose-trajectories with shared resource — segment 0's length).

## Deliverables Produced
- `mechanic-spec.md` (workspace/mechanic-spec.md) — full 9-section spec.

## Notes
- The `available_actions=[1..6]` includes length-adjust at all levels. L1 gates ACTION1/2 via `_get_valid_actions` so the engine doesn't offer them — the L1 player only sees 4 valid actions {3, 4, 5, 6}. This is allowed per `action-enum.md` and uses the same gating idiom as cn04.
- Initial click on a cell that is neither hinge nor tip is a no-op. Click on hinge → set active. Click on tip when carrying → drop. Click anywhere else → no-op (action consumed, step counter still ticks down).
- Implementation note: each segment is a long rectangular sprite resized via in-place `pixels = np.full(...)` per length change (similar to s5i5's resize pattern, but simpler since we have a single fill colour). Rotation handled via `Sprite.set_rotation(...)`.
- The chain has 3 segments throughout all three levels — the structure is constant; only level data (target, object, drop-zone, step budget, available action gating) changes per level. This is idiomatic per `reference-game-patterns.md` design move 3 ("per-level data dict drives parameters").
