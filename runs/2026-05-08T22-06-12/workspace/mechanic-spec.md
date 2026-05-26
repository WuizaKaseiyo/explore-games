# mechanic-spec — `cy3k`

## 1. Title

Cluster Cycle Pattern (working title).

## 2. Mechanic family

`cluster-cycle-rewrite` — `symbolic-rewrite` primary skeleton. The grid is a 2-D field of single-cell coloured squares from a 4-colour alphabet. Player walks a 3×3 cursor avatar over cells (avatar palette distinct from alphabet); ACTION5 cycles the colour of the cursor's cell forward through the alphabet AND propagates the cycle to every cell in the cursor's 4-connected same-colour cluster. Win = match the target pattern. Drawing from `core-knowledge-priors.md` Objectness + Geometry/topology + (implicitly) symbolic state.

## 3. Sprite roster

- **cursor** (3×3 avatar; palette 9 blue + 4 outline + 0 white center). Walks the grid; visually distinguishable from any cell colour.
- **cell_a** (1×1, palette 11 yellow): one of 4 alphabet colours.
- **cell_b** (1×1, palette 14 green).
- **cell_c** (1×1, palette 8 red).
- **cell_d** (1×1, palette 15 purple).
- **fixed_marker** (3×3, palette 3 grey + 4 corners — bigger so visually distinct from alphabet cells): L2+ only. Cells with a fixed_marker on top do not cycle.
- **transparent_marker** (3×3, palette 10 light-blue thin pip): L3 only. Cells with this marker preserve 4-connectivity across them but do not themselves cycle.
- **target_pattern_hud** (`RenderableUserDisplay`): renders the target pattern as a small swatch grid in the top-right corner. Player compares the playfield to this target.
- **step_counter_hud**: bottom-row depleting bar.

## 4. Level progression

Three mechanics introduced one per level:
- **M1** (L1): cluster-cycle — ACTION5 cycles the cursor's cell colour forward, propagating to entire same-colour 4-connected cluster.
- **M2** (L2): fixed cells — `fixed_marker` sprites mark cells that DO NOT cycle (they remain at their initial colour). Cluster computation still treats them as members based on colour — but they don't cycle when others in their cluster do.
- **M3** (L3): transparent cells — `transparent_marker` sprites mark cells that preserve 4-connectivity (clusters span across them) but the cell itself doesn't cycle.

### Level 1 — base (M1)

**Layout** (6×6 grid):
- Cursor at (0, 0).
- Cells colour layout (initial):
  ```
  AABBBB
  AABBBB
  AABBBB
  CCDDDD
  CCDDDD
  CCDDDD
  ```
  (3 clusters: 6 yellow A, 12 green B, 6 red C, 12 purple D).
- Target:
  ```
  BBAAAA
  BBAAAA
  BBAAAA
  DDCCCC
  DDCCCC
  DDCCCC
  ```
  (Clusters identity preserved; each cluster cycled forward by 1: A→B, B→C... wait A→B but target shows BBaaaa so cluster A cycled to B, but cluster B in same position should now be... hmm let me redesign.)

Simpler layout:
```
Initial:               Target:
AABB                   BBCC
AABB                   BBCC
CCDD                   DDAA
CCDD                   DDAA
```
Wait this is 4×4 with 4 clusters of 4 cells each. To turn cluster-A (yellow) into B (green), cycle A once. But cycling A→B means cluster A's cells become green; they now MERGE with the existing B cluster (already green)! So after cycling, the 4 cells that were A are now B, and they're 4-connected to the existing B cells (since A and B were originally adjacent). New cluster size = 8 (the union).

This is the cluster-fusion phenomenon. It's automatic from the rule — not a separate mechanic.

Let me design L1 to NOT trigger fusion (well-separated clusters). 6×6 with clusters in opposite corners.

Actually let me use 4×4 with target where each cluster cycles exactly once. Initial has 4 clusters of 4 cells each in 2×2 quadrants:
```
AABB
AABB
CCDD
CCDD
```
Target after each cluster cycles exactly once (A→B, B→C, C→D, D→A):
```
BBCC
BBCC
DDAA
DDAA
```

But cycling cluster-A to B causes merger with cluster-B (now both green). So after cycling A first, the 4 A-cells become B; they become contiguous with original 4 B-cells. New cluster size = 8.

Hmm. To avoid fusion in L1, layout must have cycled-A's new color NOT match any adjacent cluster. So if A→B, and B is NOT adjacent to original A cells, no fusion.

Place clusters such that:
- Cluster A is yellow at top-left
- Cluster B is RED at top-right (not green)
- Cluster C is purple at bottom-left
- Cluster D is GREEN at bottom-right

Initial:
```
AACC  (A=yellow, C=red)
AACC
BBDD  (B=purple, D=green)
BBDD
```

Cycle A once (yellow→green): A becomes green. Adjacent cells include C (red, not green) — no fusion. New A cluster is green, still 4 cells.

After cycling each cluster once:
```
A→B (green): top-left becomes green
C→D (purple, since C=red→D? Wait my alphabet cycle order matters.)
```

Let me redefine alphabet cycle: yellow → green → red → purple → yellow.
- A=yellow → green. A cells become green.
- B=purple → yellow. B cells become yellow.
- C=red → purple. C cells become purple.
- D=green → red. D cells become red.

Initial:
```
AACC = yellow yellow red red
AACC = yellow yellow red red  
BBDD = purple purple green green
BBDD = purple purple green green
```

After all 4 cycles:
```
Green Green Purple Purple
Green Green Purple Purple
Yellow Yellow Red Red
Yellow Yellow Red Red
```

Target pattern set this. Witness = visit each cluster (4 visits) and ACTION5 once (4 cycles). Plus walks between them.

Walk count from (0,0):
- At (0,0) cluster A. ACTION5. (1)
- Walk to (3,0) cluster C. 3 walks east. ACTION5. (4 actions: 3 walk + 1 cycle)
- Walk to (3,3) cluster D. 3 walks south. ACTION5. (4)
- Walk to (0,3) cluster B. 3 walks west. ACTION5. (4)

Total: 1 + 4 + 4 + 4 = 13 actions.

Witness: 1 ACTION5 + 3 ACTION4 + 1 ACTION5 + 3 ACTION2 + 1 ACTION5 + 3 ACTION3 + 1 ACTION5. 

But wait, after cycling A from yellow to green, cluster A's color becomes green. Now C cluster is at (3,0) onwards. Is C adjacent to A? Original A: (0,0),(1,0),(0,1),(1,1). Original C: (2,0),(3,0),(2,1),(3,1). A and C ARE adjacent (cells (1,0) and (2,0) are 4-connected). So if A=yellow→green and C=red, after cycling A's new color is green. C is red, not green — no fusion. 

But what about cluster D? Original D: (2,2),(3,2),(2,3),(3,3). D=green. After cycling A to green: are A's new cells (now green) adjacent to D? A cells at row 0-1; D at row 2-3. (1,1) adjacent to (1,2)? (1,2) is original cluster B (purple), not D. So no adjacency between new-A and D.

Hmm wait B is at (0,2),(1,2),(0,3),(1,3). After cycling B from purple to yellow: B's new color is yellow. New-A (green) adjacent to new-B (yellow)? Cells (1,1) and (1,2): (1,1) is now green (was A). (1,2) is now yellow (was B). Different colors, no fusion.

OK no fusion happens after cycling everything. 

But in WHICH ORDER do we cycle? The witness can pick any order. Let me trace order (A, C, D, B):

Initial:
```
A A C C
A A C C
B B D D
B B D D
```

After ACTION5 at (0,0) [cluster A]: A's 4 cells cycle yellow→green.
```
G G C C  (G=green, was A)
G G C C
B B D D
B B D D
```
Cluster G=4 cells, C=4, B=4, D=4. No fusion.

After ACTION5 at (3,0) [cluster C, red]: C cycles red→purple.
```
G G P P  (P=purple)
G G P P
B B D D
B B D D
```
P cells (2,0)(3,0)(2,1)(3,1). B cells at (0,2)(1,2)(0,3)(1,3) are also purple? Yes, B=purple originally. After cycling C only, P cells from C = (2,0)(3,0)(2,1)(3,1). B = (0,2)(1,2)(0,3)(1,3). Adjacent? Row 1 to row 2 at cols 0-1: (0,1)(1,1) are green, (0,2)(1,2) are purple. (1,1) green and (1,2) purple are different colors, no fusion. So C's new purple cluster is 4 cells, B's purple cluster is also 4 cells, but they're NOT adjacent (separated by column 1-2 row 1-2 where all 4 corners are green and purple). Wait (1,1) is green, (2,1) is purple (from C). They're adjacent (4-connected). Same color? Green vs purple. No fusion.

But (2,1) from new C-cluster and (2,2) from D? (2,1) is purple now (from C). (2,2) is green (D's original). Different, no fusion.

After ACTION5 at (3,3) [cluster D, green]: D cycles green→red.
```
G G P P
G G P P
B B R R  (R=red)
B B R R
```
D's new red cluster = 4 cells. Adjacent to A (green) at (1,2)? (1,2) is B, purple, not green. (2,1) is P from C. So D's new red has no adjacent cells of same color → no fusion.

After ACTION5 at (0,3) [cluster B, purple]: B cycles purple→yellow.
```
G G P P
G G P P
Y Y R R  (Y=yellow, was B)
Y Y R R
```
Y cluster = 4 cells (from B). Adjacent to others? G (green), P (purple), R (red). No yellow neighbors. No fusion.

Final state matches target:
```
Target:
G G P P
G G P P
Y Y R R
Y Y R R
```

Wait that's not quite my original target. Let me re-read my target:
```
After all 4 cycles:
Green Green Purple Purple    (top-left)
Green Green Purple Purple
Yellow Yellow Red Red         (bottom)
Yellow Yellow Red Red
```

OK my final state from witness IS:
```
G G P P
G G P P
Y Y R R
Y Y R R
```

Same as target. ✓ Witness works.

Witness sequence (player at (0,0) starting):
- ACTION5 (cycle A)
- ACTION4 ×3 (walk to (3,0))? Wait my cursor occupies a cell. Initial cursor at (0,0) where cluster A is. After ACTION5, cluster A cycles. I need to walk to (3,0) for cluster C. (3,0) is the right edge.

Actually wait — I need cursor to be ON the cell whose cluster I want to cycle. Cluster C cells: (2,0),(3,0),(2,1),(3,1). To cycle C, cursor at any of these cells. Cursor walks (0,0)→(1,0)→(2,0). 2 walks east. Then ACTION5. So 2+1 = 3 actions for cluster C.

Let me re-trace:
- Start cursor (0,0).
- ACTION5: cycle A. (1)
- ACTION4 ×2: cursor → (2,0). (2 walks)
- ACTION5: cycle C. (1)
- ACTION2 ×2: cursor → (2,2). (2 walks south)
- ACTION5: cycle D. (1)
- ACTION3 ×2: cursor → (0,2). (2 walks west)
- ACTION5: cycle B. (1)

Total: 1 + 2 + 1 + 2 + 1 + 2 + 1 = 10 actions. **Witness L1**: `[ACTION5, ACTION4, ACTION4, ACTION5, ACTION2, ACTION2, ACTION5, ACTION3, ACTION3, ACTION5]`.

**Mechanics required by witness** (N=1): M1 (cluster-cycle).

**Necessity**: L1 cannot be solved without M1 because each cluster must cycle to a specific colour to match the target; ACTION5 is the only verb that cycles cells; with no movement-pushes-cells mechanic available, cycling is required.

**Difficulty**: (a) random-resistance: P(random win in 50) negligible — 5 actions per level need to be ACTION5 at specific cells. (b) ~30 sec; (c) L1 no planning gate; (d) step_budget=50.

### Level 2 — base + M2 (fixed cells)

**Layout** (6×6 with 2 fixed cells):
- Same starting layout as L1 but cells (0,0) and (3,3) carry `fixed_marker` — they will NOT cycle when their cluster cycles.
- Initial: same 4-cluster yellow/red/purple/green layout.
- Target: requires cluster cycling but the 2 fixed cells stay at original colour.

For this to be solvable: the target pattern must keep cells (0,0) and (3,3) at their original colours while other cells cycle.

Witness: similar to L1 but cycle counts adjusted. Roughly 10-14 actions.

**Mechanics required by witness** (N+1 = 2): M1 + M2.

**Necessity**: M1 still required. M2 required because target leaves fixed cells at original; only the M2 rule (fixed cells don't cycle when their cluster cycles) preserves this — without M2, cycling cluster A would also move (0,0). So spec must specifically demonstrate target where fixed cells MUST stay at original to win.

**Trivial heuristic**: `[ACTION4 × 14]` (always press right). Cursor walks east across grid to boundary; never presses ACTION5; clusters never cycle; target never reached. **Level does NOT advance.** Structurally distinct from witness (witness has ACTION5 calls; trivial has none).

**Difficulty**: (a) negligible random; (b) ~90 sec; (c) post-discovery: 5 valid first actions; player must reason about which clusters to cycle and in what order to avoid disturbing fixed cells; (d) step_budget=80.

### Level 3 — base + M2 + M3 (transparent cells)

**Layout** (8×8 with fixed + transparent cells):
- 8×8 grid, 4-colour alphabet, 4-5 clusters.
- 1-2 cells carry `transparent_marker`: clusters expand THROUGH them but the cells themselves don't cycle.
- This means clusters can be larger (expanded) but partially uncyclable.

**Mechanics required by witness** (M+1 = 3): M1 + M2 + M3.

**Necessity**: M1 + M2 still required as L2. M3 required because transparent cells expand cluster sizes (a cluster of 4 with 1 transparent neighbour effectively spans 5 cells, but transparent itself stays). Target must require this expanded-cluster cycling effect to win.

**Witness**: ~20 actions including walks + ACTION5 calls.

**Trivial heuristic**: `[ACTION4 × 20]`. Same reasoning — pressing right alone never cycles; level not advanced.

**Difficulty**: (a) negligible random; (b) ~3 min; (c) post-discovery planning is challenging because transparent-extended clusters must be reasoned about (cluster boundary spans multiple visible-cell groups via transparent bridges); (d) step_budget=120.

## 5. Action mapping

- ACTION1-4: walk cursor 1 cell in cardinal direction. If walking off-grid or into a wall (no walls in this game), cursor blocks.
- ACTION5: cycle the colour of the cursor's cell forward through the alphabet (yellow→green→red→purple→yellow); cycle propagates to all cells in the cursor's 4-connected same-colour cluster (excluding fixed cells; including connectivity-bridges from transparent cells).

`available_actions = [1, 2, 3, 4, 5]`.

## 6. HUD and per-game state

- `StepCounterHud`: bottom-row depleting bar.
- `TargetPatternHud`: top-right corner small swatch grid showing target pattern.

State:
- `self._cursor_x, self._cursor_y: int` — cursor position
- `self._cell_colors: dict[(x,y) -> int]` — current colour of each cell
- `self._steps_used, self._max_steps`

## 7. Win condition

For every (x, y) in current_level cells: `cell_colors[(x,y)] == target_pattern[(x,y)]`.

## 8. Lose condition

`self._steps_used >= self._max_steps`.

## 9. Novelty note

- Closest taxonomy: tr87 tape-rewrite-rule (1D rewrite); pj7k rolling-cube-face-paint (symbolic-rewrite primary). Distinguishing rules in mechanic-pick.md § "Distinguishing rules".
- Closest prior: ng52 (classification-sorting; my secondary skeleton). Distinguishing rule: ng52 places objects in bins; cy3k cycles in-place colours.
- §3.4: original synthesis from PuzzleScript inspiration + CA cluster propagation; not a known commercial game.
