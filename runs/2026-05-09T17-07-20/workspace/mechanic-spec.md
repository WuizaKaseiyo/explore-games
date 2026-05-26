# mechanic-spec — `dx8m`

## 1. Title

Local Invariant Balance.

## 2. Mechanic family

`local-invariant-balance` — `spatial-constraint` primary skeleton. Click toggles cells between off / on; each cell may belong to one or more visible "region badges" with count invariants (exactly N on, displayed as dot pattern in the badge). Win = all region invariants simultaneously satisfied. Drawing from Objectness + Geometry/topology + Numbers (small counts).

## 3. Sprite roster

- **cell_off** (4×4, palette 4 dark fill + 0 inner hollow): cell in OFF state.
- **cell_on** (4×4, palette 14 green fill + 0 inner highlight): cell in ON state.
- **region_badge_a** (5×5, palette 11 yellow with N-dot pattern showing required count): visual marker indicating a region anchor + count required.
- **region_badge_b** (5×5, palette 8 red with N-dot pattern).
- **region_badge_c** (5×5, palette 15 purple with N-dot pattern; L3 only — reference region).
- **region_member_marker** (1×1 INTANGIBLE pip in region's badge colour): indicates a cell belongs to a particular region. Multiple markers stack on overlap cells.
- **satisfaction_indicator** (3×3, INTANGIBLE green ring): appears next to each region badge when satisfied.
- **step_counter_hud**: bottom-row depleting bar.

## 4. Level progression

Three mechanics introduced one per level:
- **M1** (L1): basic count-invariant — each region requires exactly N cells on within the region.
- **M2** (L2): overlapping regions — cells can belong to multiple regions; a single click affects all regions containing the toggled cell.
- **M3** (L3): reference region — one region's count requirement equals the satisfied count of another region; player must reason about cross-region dependencies.

### Level 1 — base (M1)

**Layout** (8×8 grid):
- Region A badge at (0, 0) with required count = 2.
- Region A members: cells at (1, 1), (2, 1), (3, 1).
- Region B badge at (5, 0) with required count = 1.
- Region B members: cells at (5, 5), (6, 5).
- Initial: all 5 cells off.
- Target invariant: A has 2 on (any 2 of 3), B has 1 on (any 1 of 2).

**Mechanics required by witness** (N=1): M1.

**Necessity**: L1 cannot be solved without M1 because the only verb that can toggle any cell is ACTION6 click; the only victory predicate is "all region count invariants satisfied"; without M1's count rule, there's no win condition at all.

**Witness solution**: `[ACTION6@(1,1), ACTION6@(2,1), ACTION6@(5,5)]` — 3 clicks. Toggles cells (1,1) and (2,1) on (region A: 2/2 ✓); toggles (5,5) on (region B: 1/1 ✓). Win.

(In the implementation, ACTION6 takes display-pixel coordinates; the witness will be expressed in cell coordinates and translated.)

**Difficulty**: (a) random-resistance: P(random win) ≈ negligible — random would need to click exactly the right 3 cells out of many. (b) ~30 sec. (c) L1 = no planning gate. (d) step_budget=20.

### Level 2 — base + M2 (overlapping regions)

**Layout** (10×10 grid):
- Region A: cells (1,1), (2,1), (3,1), (4,1), (5,1). Required count = 3.
- Region B: cells (4,1), (5,1), (4,2), (5,2), (6,2). Required count = 3.
- **Overlap**: cells (4,1) and (5,1) belong to BOTH regions.

**Mechanics required by witness** (N+1 = 2): M1 + M2.

**Necessity**:
- M1: still required (count invariants are the win predicate).
- M2: required because the only valid solution sets must respect BOTH regions simultaneously. The overlap forces specific cells: if (4,1) and (5,1) are both on, that contributes 2 to region A's count (need 1 more) and 2 to region B's count (need 1 more). Player must pick where the third on goes for each region. With M2 active, there exist non-greedy solutions; without (independent regions), the puzzle would just be 2 separate L1s.

**Witness**: `[ACTION6@(4,1), ACTION6@(5,1), ACTION6@(1,1), ACTION6@(6,2)]` — 4 clicks. After clicks: (4,1) on, (5,1) on, (1,1) on, (6,2) on. Region A count = 3 (cells 1,1; 4,1; 5,1) ✓. Region B count = 3 (cells 4,1; 5,1; 6,2) ✓.

**Trivial heuristic action sequence**: `[ACTION4@(0,0)] × 15` — pressing ACTION4 (a no-op direction key in this game) repeatedly. No cells ever toggle. No region ever satisfied. **Level does NOT advance.**

**Difficulty**: (a) negligible random; (b) ~90 sec; (c) post-discovery: 5+ valid first clicks. Plausible-but-wrong: greedy-fill region A first to (1,1)(2,1)(3,1) — then region B requires (4,1),(5,1),(6,2) on, but A now has count 3+2=5 (extra two) → A invariant broken. Reasoning chain: "use overlap cells to count once for both regions". (d) step_budget=40.

### Level 3 — base + M2 + M3 (reference region)

**Layout** (12×12 grid):
- Region A: cells (1,1), (2,1), (3,1), (4,1). Required count = 2 (fixed).
- Region B: cells (1,5), (2,5), (3,5), (4,5). Required count = 2 (fixed).
- Region C (reference): cells (1,9), (2,9), (3,9), (4,9), (5,9). Required count = (count_on of A) + (count_on of B) — i.e., currently equals 4 when both A and B are satisfied.

**Mechanics required by witness** (M+1 = 3): M1 + M2 + M3.

**Necessity**:
- M1: required (count invariants).
- M2: not strictly active here since regions are disjoint. **OR**: redesign so M2 is also required — let's add overlap between A and B by sharing cell (4,1) and (4,2). Actually given complexity, M2 is "carried mechanically" (the engine still supports overlap; just no overlap in this layout). Note: this is a softer counterfactual.
- M3: required because region C's required count is dynamic — it depends on A's and B's satisfied counts. Without M3, region C would have a fixed count, and the puzzle would just be 3 independent L1s.

**Witness**: `[ACTION6@(1,1), ACTION6@(2,1), ACTION6@(1,5), ACTION6@(2,5), ACTION6@(1,9), ACTION6@(2,9), ACTION6@(3,9), ACTION6@(4,9)]` — 8 clicks. A: 2 on ✓. B: 2 on ✓. Region C requires 2+2=4 on; clicked 4 cells in C ✓.

**Trivial heuristic**: `[ACTION4@(0,0)] × 20`. No cells toggle. Fails.

**Difficulty**: (a) negligible random; (b) ~3 min. (c) post-discovery: player must reason about C's dynamic count; trivial heuristic "fill all C cells" gives count 5, not equal to 4 (when A=B=2). Trivial fails. (d) step_budget=60.

## 5. Action mapping

- ACTION6: click at (x, y) display pixel coordinates; converted to grid cell; if cell is a region member, toggle it on/off.
- ACTION4: no-op (declared so trivial heuristic `[ACTION4 × N]` is a valid input sequence; serves as a "do nothing" verb to make trivial-fails gate testable).
- ACTION1, 2, 3, 5, 7: not declared.

`available_actions = [4, 6]`.

## 6. HUD and per-game state

- `StepCounterHud`: bottom-row depleting bar.

State:
- `self._steps_used: int`, `self._max_steps: int`
- `self._cell_states: dict[(x,y) -> bool]` — current on/off
- (Regions and target counts are level-data, computed in `_check_win`)

## 7. Win condition

For each region R: `sum(cell_states[c] for c in R.members) == R.required_count` (where required_count for L3's reference region = on-count(A) + on-count(B)).

## 8. Lose condition

`self._steps_used >= self._max_steps`.

## 9. Novelty note

- Closest taxonomy: lv4k (lever-balance-torque, same primary skeleton). Distinguishing rule: lv4k is single-axis torque; dx8m is multi-region overlapping count-invariants. Different constraint geometry.
- Closest prior: ng52 (multiset-signature-classify, same secondary skeleton classification-sorting). Distinguishing rule: ng52 partitions a pool by signature; dx8m toggles stationary cells against region invariants.
- §3.4 ceiling: count-constraint puzzles like Nonogram are commercial. dx8m differs in (1) regions are explicit OVERLAPPING SETS (not row/col strips), (2) M3 reference invariants are not in standard Nonogram. User-side ceiling check should verify against count-puzzle commercial titles.
