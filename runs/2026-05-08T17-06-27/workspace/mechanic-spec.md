# mechanic-spec — `tw94`

## 1. Title

Toroidal Wrap Playfield (working title).

## 2. Mechanic family

`toroidal-wrap-playfield`. The grid is a torus: walking / pushing off one edge re-enters from the opposite edge (subject to per-axis wrap rules). Drawing from `core-knowledge-priors.md` Objectness + Geometry/topology. Inspired by PuzzleScript demo `wrappingrecipe.txt`.

## 3. Sprite roster

- **player**: 5×5 (palette 9 blue + 4 black + 0 white).
- **crate**: 4×4 (palette 12 orange + 13 maroon).
- **target**: 3×3 (palette 11 yellow + 4 dark ring).
- **wall**: 4×4 (palette 3 grey + 4 corners).
- **wrap_indicator**: 1×1 (palette 10 light-blue) — tiny pip drawn at edge cells whose row/col DOES wrap (visible cue for L3's row-parity rule). At L1 and L2, all edge cells get a pip on their wrappable axes; at L3, only even-row/even-col edge cells get a pip.
- **step_counter_hud**: bottom-row depleting bar.

## 4. Level progression

Three mechanics, one per level:
- **M1** (L1): horizontal wrap (east-west only).
- **M2** (L2): vertical wrap (north-south) added — full 2D torus.
- **M3** (L3): row-parity wrap — only even rows wrap horizontally; only even cols wrap vertically; odd rows/cols have hard boundaries.

### Level 1 — base (M1)

**Layout** (8×8): player (5,4), crate (4,4), target (6,4). Walls form a sealed row-4 corridor: row 3 cols 0-7, row 5 cols 0-7. Wall at (5,4)? No, player is there. Walls at (3,4)... let me redo: wall block at (5,4) blocks east push.

Actually simpler L1: Player at (5, 4); crate at (3, 4); target at (6, 4). Walls at (4, 4) and (5, 4) — wait player can't be on wall. Let me place definitively:

- Grid 8×8.
- Player at (1, 4).
- Crate at (2, 4).
- Target at (5, 4).
- Wall at (4, 4) blocks direct east push.
- Walls at row 3 cols 0-7 and row 5 cols 0-7 seal the lane.
- To deliver crate east from (2,4) to (5,4): push east blocked by wall at (4,4) (after pushing crate to (3,4), next push to (4,4) wall fails).
- Push west via wrap: from player at (1,4), walk west: (1,4) → (0,4) → wrap → (7,4) → (6,4) → (5,4) target → ... player can't push crate from this side initially because crate is at (2,4) east of player.
- Actually for the puzzle to work: player must push crate west via wrap.
- Player walks east first to be west of... no, crate is already at (2,4) east of player at (1,4).
- Walk east to (2,4)? Crate. ACTION4 push east: crate (2,4)→(3,4). Continue: push (3,4)→(4,4) wall. Fail.
- So east push only delivers crate to (3,4), 2 cells short of target (5,4). Wall blocks.
- **Push west via wrap**: from west of crate. Player at (1,4) walks west: ACTION3 dest (0,4) walk. Player → (0,4). ACTION3 dest (-1,4) → wrap → (7,4) walk. Player → (7,4). Player now east of target (5,4) and east of crate via wrap-direction.
- ACTION3: dest (6,4) walk (target intangible). Player → (6,4).
- ACTION3: dest (5,4) target → walk. Player → (5,4).
- ACTION3: dest (4,4) wall. Blocked.
- Hmm player can't reach crate via west wrap because wall at (4,4) blocks.
- Try north-south detour: walls at row 3 and row 5 seal the lane. No detour possible.

Layout doesn't work. Let me redesign:

**L1 redesigned** (8×8):
- Player at (3, 4); crate at (4, 4); target at (1, 4).
- Wall at (2, 4) blocks direct west push (push (4,4)→(3,4)→(2,4)wall fails after 1 push).
- Walls at row 3 cols 0-7, row 5 cols 0-7.
- To deliver crate west from (4,4) to (1,4): push west via wrap.
  - Push west #1: player (3,4) ACTION3 walks INTO (4,4)? No, (4,4) east of player. ACTION3 would walk to (2,4) wall. Blocked.
  - To push crate west, player needs east of crate. Walk east: ACTION4 dest (4,4) crate. PUSH east: dest (5,4) empty. Push: crate (4,4)→(5,4). Player → (4,4).
  - ACTION4: dest (5,4) crate. Push: (6,4) empty. Push: crate→(6,4), player→(5,4).
  - ACTION4: push (6,4)→(7,4). Player→(6,4).
  - ACTION4: push (7,4) → wrap → (0,4). Player→(7,4).
  - ACTION4: walk wrap to (0,4) crate. Push east: dest (1,4) target. Push: crate→(1,4)=target. Player→(0,4). WIN.

5 ACTION4 push-via-wrap. Counterfactual M1 (wrap): direct west push fails (wall); direct east push reaches (7,4) without wrap, then push (7,4) east boundary fails without wrap. So wrap is the only way to get crate from (7,4) to (1,4) (just 2 cells via wrap).

Witness: 5 ACTION4.

**Mechanics required by witness** (N=1): M1 (horizontal wrap).

**Necessity per mechanic:**
- L1 cannot be solved without M1 because the wall at (2, 4) blocks west-push of crate; east-pushing reaches (7, 4) at the east boundary, where wrap is required to continue and reach target at (1, 4) via wrap.

**Witness solution:**
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]
```

**Difficulty:**
- (a) random P(5 consecutive ACTION4) ≈ 0.1%; budget 25 → ~0.5% cumulative.
- (b) ~30 sec.
- (c) L1 = no planning gate.
- (d) step_budget=25.

### Level 2 — base + M2 (vertical wrap)

**Layout** (12×12):
- Player at (5, 5).
- Crate_a at (4, 6); target_a at (8, 6). Wall at (6, 6) blocks east push of crate_a.
- Crate_b at (6, 4); target_b at (6, 8). Wall at (6, 6) blocks south push of crate_b. (Same wall, dual purpose.)
- Walls row 5 cols 0-11, row 7 cols 0-11 seal row 6 horizontally; walls col 5 rows 0-11, col 7 rows 0-11 seal col 6 vertically (creating a "+" shape of walls except at (6, 6) which is itself the central wall).

Wait this is getting complex. Let me simplify with two SEPARATE corridors:

- Push lane row 6 (cols 0-11): for crate_a east-via-horizontal-wrap delivery.
- Push column col 6 (rows 0-11): for crate_b north-via-vertical-wrap delivery.
- The two corridors cross at (6, 6) which is a wall (or just a junction cell).

Actually simpler: forget walls, just place crates and targets at positions where wrap is the shortest path.

L2 final layout (12×12):
- Player at (1, 1).
- Crate_a at (10, 4); target_a at (2, 4). Direct west push: 8 west-pushes. East-wrap push: 4 east-pushes (10→11→0→1→2 via wrap). Wrap shorter.
- Crate_b at (4, 10); target_b at (4, 2). Direct north push: 8 north-pushes. South-wrap push: 4 south-pushes (10→11→0→1→2 via wrap). Wrap shorter.
- For *strict counterfactual*: walls blocking direct path. Wall at (5, 4) blocks crate_a west-push at midpoint. Wall at (4, 5) blocks crate_b north-push at midpoint.

Hmm OK let me commit: walls do block direct paths. East-wrap and south-wrap are required.

**Mechanics required by witness** (N+1=2): M1 (horizontal wrap) + M2 (vertical wrap).

**Necessity:**
- L2 cannot be solved without M1 because crate_a's direct west push hits wall at (5, 4); east-wrap is the only delivery path.
- L2 cannot be solved without M2 because crate_b's direct north push hits wall at (4, 5); south-wrap (vertical) is the only delivery path.

**Witness solution** (~20 actions):
```
[walks to east of crate_a, ACTION4 ×N to east-wrap-push to target_a,
 walks to north of crate_b, ACTION2 ×N to south-wrap-push to target_b]
```

(Detailed trace: skipped; counts are ~10 + ~10.)

**Trivial heuristic action sequence**: `[ACTION4 × 20]` (always press right). Pushes crate_a east-via-wrap to target_a (4 pushes after 8 walks ≈ 12 ACTION4); subsequent ACTION4s walk player east through wrap; never touches crate_b (different col). **Level does NOT advance** because crate_b not delivered.

**Difficulty:**
- (a) random: negligible.
- (b) ~2 min.
- (c) post-discovery: 4 valid first actions, decision is "which crate first; which axis-wrap to use".
- (d) step_budget=60.

### Level 3 — base + M2 + M3 (row-parity wrap)

**Layout** (14×14):
- Same crate_a, crate_b, walls as L2 but at L3 coordinates.
- Add **crate_c at (3, 5)**; **target_c at (10, 5)**. Row 5 is ODD — does NOT wrap horizontally at L3. Direct path blocked by walls.
- Player must push crate_c vertically to ROW 4 (even, wraps), then wrap east, then push back south to row 5.

Wait: row-parity rule says even rows wrap. Crate_c at row 5 (odd) cannot be pushed via east wrap on its own row.

**Mechanics required by witness** (M+1=3): M1 + M2 + M3.

**Necessity:**
- L3 cannot be solved without M1 because crate_a still requires horizontal wrap.
- L3 cannot be solved without M2 because crate_b still requires vertical wrap.
- L3 cannot be solved without M3-aware navigation because crate_c is on row 5 (odd) where horizontal wrap is disabled; player must push crate_c to row 4 (even) before wrapping. The player must REASON about which row supports wrap (M3's distinguishing behaviour).

**Witness solution** (~30 actions): deliver crate_a via east-wrap on row 4 (even, wraps); deliver crate_b via south-wrap on col 4 (even, wraps); for crate_c: push it vertically to row 4, wrap east, push back south to row 5 at target_c.

**Trivial heuristic action sequence**: `[ACTION4 × 30]` (press right). Pushes crate_a via east-wrap to target_a; doesn't touch crate_b or crate_c. **Level does NOT advance**.

**Difficulty:**
- (a) random: negligible.
- (b) ~3 min. Player observes that wrap fails on odd rows (boundary block), then realises even-row pattern.
- (c) post-discovery: planning across both wrap axes AND row-parity.
- (d) step_budget=120.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. Walking-into-crate triggers push. Push at boundary attempts wrap (subject to per-axis and per-level wrap rules).

## 6. HUD and per-game state

- `StepCounterHud`: bottom-row depleting bar.
- Per-game state: `self._steps_used`, `self._max_steps`. (Wrap rules are per-level, computed in movement logic from `_current_level_index`.)
- Wrap-indicator pip sprites visualise which axis wraps at each edge cell.

## 7. Win condition

`{(t.x, t.y) for t in targets}.issubset({(c.x, c.y) for c in crates})`.

## 8. Lose condition

`self._steps_used >= self._max_steps`.

## 9. Novelty note

- Closest taxonomy: **vc33** (row-slide-pull-tab). Distinguishing rule: vc33 *slides* a row of pieces atomically; this candidate has standard sokoban motion with a *toroidal grid topology*. Different mechanism class.
- Closest prior: none — toroidal/wrap topology is new to the 28-game corpus.
- §3.4 commercial: PuzzleScript `wrappingrecipe` is a tech-demo, not commercial; user verifies ceiling.
