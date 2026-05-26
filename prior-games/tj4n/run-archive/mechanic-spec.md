# mechanic-spec.md — `tj4n`

## 1. Title
Boundary Trace.

## 2. Mechanic family
A single avatar walks a 16-cell-wide arena leaving a coloured trail behind it. When the avatar steps back onto its own existing trail, the trail closes; every TARGET sprite whose centre lies strictly inside the resulting closed polygon (Jordan-curve interior, ray-cast point-in-polygon) is captured. FORBIDDEN sprites that fall inside any closure cost a strike (3 strikes lose). Prior categories drawn from §3.4: **basic geometry & topology** (Jordan-curve interior detection is the load-bearing concept), **objectness** (targets, forbiddens, and the L3 pursuer are coherent persistent sprites), **agentness** (L3 pursuer pursues the avatar via greedy BFS).

## 3. Sprite roster

The grid is 64×64 pixels and the playfield uses 16×16 logical cells of 4×4 pixels each. All gameplay-relevant sprites are 4×4 with internal pixel detail. Avatar moves in 4-pixel hops; positions are multiples of 4.

- **avatar** — 4×4, palette `{4 black, 9 blue}`, tag `player`. Internal pattern: blue ring around a black centre — symmetric, no figurative features. Same shape as `trail_cell` but different colour, so the player reads "current position" (blue) vs "past position" (pink) as a colour-difference of one shape; this is intentional per item 21 rule 2.
  ```
  [-1, 9, 9, -1]
  [ 9, 4, 4,  9]
  [ 9, 4, 4,  9]
  [-1, 9, 9, -1]
  ```
  *Revised — Issue 4 of critique-revisions.md visit 1.*
- **trail_cell** — 4×4, palette `{7 pink, 4 black}`, tag `trail`. Internal pattern: pink ring around a black centre. Visually distinct from `avatar` (no yellow eye, no rounded fill).
  ```
  [-1, 7,  7, -1]
  [ 7,  4,  4,  7]
  [ 7,  4,  4,  7]
  [-1, 7,  7, -1]
  ```
- **target** — 4×4, palette `{11 yellow, 4 black, 12 orange}`, tag `target`. Internal pattern: solid yellow square with a tiny orange centre dot. Visually unmistakably "collectible / valuable".
  ```
  [11, 11, 11, 11]
  [11, 12, 12, 11]
  [11, 12, 12, 11]
  [11, 11, 11, 11]
  ```
- **forbidden** — 4×4, palette `{8 red, 4 black}`, tag `forbidden`. Internal pattern: solid red border with black inset block — reads as a "filled hazard cell" via colour density (red border = warning), not via symbolism. NOT an X-mark.
  ```
  [ 8,  8,  8,  8]
  [ 8,  4,  4,  8]
  [ 8,  4,  4,  8]
  [ 8,  8,  8,  8]
  ```
  *Revised — Issue 1 of critique-revisions.md visit 1.*
- **pursuer** — 4×4, palette `{13 maroon, 8 red}`, tag `pursuer`. Internal pattern: maroon-red checker — reads as "active / dynamic" without facial features. Distinct from `forbidden` (solid red border) and `target` (solid yellow with orange dot). NOT figurative.
  ```
  [13,  8, 13,  8]
  [ 8, 13,  8, 13]
  [13,  8, 13,  8]
  [ 8, 13,  8, 13]
  ```
  *Revised — Issue 5 of critique-revisions.md visit 1.*
- **wall_residue** — 4×4, palette `{5 black, 2 light-grey}`, tag `wall`. Internal pattern: black cross-hatch — reads as a solid blocking wall.
  ```
  [ 5,  2,  5,  2]
  [ 2,  5,  2,  5]
  [ 5,  2,  5,  2]
  [ 2,  5,  2,  5]
  ```
- **arena_border** — 64×4 horizontal strip and 4×64 vertical strip, palette `5`, tag `border`. Used to mark the playfield perimeter so the player can see where the arena ends.

(Background / floor outside the playfield is the camera background `palette 1` off-white; inside-the-playfield empty cells are the same off-white. The trail is the only ambient visual signal of the avatar's history.)

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All use `grid_size=(64, 64)` with the playfield occupying logical cells `(0..15)` × `(0..15)`. Avatar walks in 4-pixel hops; position quantised to multiples of 4.

### Level 1 — base dynamic system

Layout (logical cells; pixel coord = cell × 4):
- avatar at cell `(5, 8)`.
- target_a at `(8, 8)`, target_b at `(9, 8)`, target_c at `(10, 8)` — three targets in a horizontal row in the centre.
- arena empty otherwise.

**Mechanics required by the witness** (N = 2):
- **M1 — walk-deposits-trail.** Each step from cell A to cell B causes A to be marked as a trail cell (a `trail_cell` sprite is placed at A); B becomes the new avatar position.
- **M2 — closing-loop-captures-interior.** When the avatar's step lands on a cell already marked as trail, the loop closes: the cycle (the contiguous trail-sequence from the closure cell forward to the new step) is treated as a closed polygon; every target sprite whose centre is strictly inside the polygon is captured (set to `InteractionMode.REMOVED`); the trail clears.

**Necessity per mechanic (counterfactual):**
- *L1 cannot be solved without triggering M1 because* every winning trajectory must eventually close a loop, and a loop-closure requires the closing cell to already be a trail cell — but trails only exist as a side-effect of M1 (per-step deposit on the cell the avatar leaves). With M1 disabled the trail is always empty, so no step can be a closure step, so the targets at `(8,8) (9,8) (10,8)` are never captured.
- *L1 cannot be solved without triggering M2 because* the win predicate requires every target to be `InteractionMode.REMOVED`; the only mutation in the game that flips a target to REMOVED is M2's closure-side capture. With M2 disabled, the targets remain TANGIBLE forever; no other action can remove them.

**Witness solution** (18 actions, where ACTION1=up/-y, ACTION2=down/+y, ACTION3=left/-x, ACTION4=right/+x; positions in logical cells):
```
start: avatar (5, 8); trail = []
1.  ACTION1  → avatar (5, 7); trail = [(5,8)]
2.  ACTION1  → avatar (5, 6); trail = [(5,8), (5,7)]
3.  ACTION4  → avatar (6, 6); trail = [..., (5,6)]
4.  ACTION4  → avatar (7, 6)
5.  ACTION4  → avatar (8, 6)
6.  ACTION4  → avatar (9, 6)
7.  ACTION4  → avatar (10, 6)
8.  ACTION4  → avatar (11, 6)
9.  ACTION2  → avatar (11, 7)
10. ACTION2  → avatar (11, 8)
11. ACTION2  → avatar (11, 9)
12. ACTION3  → avatar (10, 9)
13. ACTION3  → avatar (9, 9)
14. ACTION3  → avatar (8, 9)
15. ACTION3  → avatar (7, 9)
16. ACTION3  → avatar (6, 9)
17. ACTION3  → avatar (5, 9)
18. ACTION1  → avatar (5, 8)  CLOSURE: (5,8) is in trail (index 0).
                Polygon = trail[0:] + [(5,8)] = (5,8)→(5,7)→(5,6)→(6,6)→...→(5,9)→(5,8).
                Interior cells include (8,8), (9,8), (10,8) — all three targets captured.
                Win.
```

**Difficulty justification:**
- (a) **Random-resistance.** A random-policy agent must produce a step sequence that returns to a previously-vacated cell while having enclosed all three targets. The targets occupy 3 specific cells in a 16×16 = 256-cell arena; the loop must make a Jordan-curve interior containing all three. Random walks rarely close (a return-to-trail probability of ~1/16 per step in mid-arena, multiplied by the conditional probability that the closure encloses the right 3 of 256 cells — empirically < 10⁻⁵ within a 50-step budget per Monte Carlo estimate).
- (b) **Human-tractable.** A first-time player sees the avatar walk and notices the pink trail behind. After 5-15 exploratory steps including a small backtrack, the closure-captures-interior rule becomes visible (target visibly disappears or changes interaction). Solve the level in ~1.5 minutes.
- (c) **Planning depth.** L1 has **no strict planning requirement** — once the player understands "walk a loop around the targets", any rectangle/blob enclosing the three target cells wins. The discovery gate (M1+M2) is the difficulty.
- (d) **Step budget.** 50 steps. Witness is 18; budget is 2.7× — generous over the witness for exploration (player will likely walk in failed loops first).

### Level 2 — base system + 2 new mechanics

Layout:
- avatar at `(2, 8)`.
- target_a at `(5, 6)`, target_b at `(5, 9)` — two targets vertically separated.
- target_c at `(11, 6)`, target_d at `(11, 9)` — another pair on the right.
- forbidden_a at `(8, 6)`, forbidden_b at `(8, 9)` — two forbiddens between the two target pairs (a "no-go" middle column).
- arena otherwise empty; no walls.

The two target-pairs are separated by a vertical strip of forbiddens at `x=8`. A single big rectangular loop around all 4 targets would also enclose both forbiddens → 2 strikes, level loses on the 2nd big loop. Solution: TWO SMALL LOOPS, each around one pair.

**Mechanics required by the witness** (N = 4 = 2 + 2):
- **M1 — walk-deposits-trail.** (Carried from L1.) Required because closures are still the only way to capture targets and closure requires a trail to close on.
- **M2 — closing-loop-captures-interior.** (Carried from L1.) Required because the level's win predicate is "all four targets captured", and the only mutation that captures targets is M2.
- **M3 — forbidden-exclusion-strike.** New. When a closure's interior contains a `forbidden`-tagged sprite, increment `_strikes`. If `_strikes` reaches 3, lose. Forbidden sprites are NOT consumed by enclosure (they remain forever).
- **M4 — multi-closure-sequencing.** New. The level has 4 targets in a layout where no single Jordan-curve polygon can contain all 4 targets while excluding all 2 forbiddens. The player must execute MULTIPLE closures (in this case 2) within the step budget.

**Necessity per mechanic (counterfactual):**
- *L2 cannot be solved without triggering M1 because* same reason as L1 — without per-step trail deposit, no cell is ever a closure target, so no captures occur, so the win predicate never fires.
- *L2 cannot be solved without triggering M2 because* the four targets at `(5,6),(5,9),(11,6),(11,9)` are TANGIBLE and have no other mutation pathway than closure-side capture. With M2 disabled, none ever flip to REMOVED, win-predicate never fires.
- *L2 cannot be solved without triggering M3 because* a single big rectangle around all 4 targets has interior including the 3 forbiddens at `(8,5)(8,7)(8,9)`; this fires M3 three times → `_strikes = 3` → lose. With M3 disabled (no strikes), the same big rectangle would capture all 4 targets and win. M3 is what turns the trivial one-loop fallback into a losing path, forcing the player to plan exclusion-respecting loops.
- *L2 cannot be solved without triggering M4 because* given M3 (3-strike lose threshold AND 3 forbiddens in column x=8), no single Jordan-curve polygon contains all 4 targets while enclosing fewer than 3 forbiddens — any polygon containing both `(4,6)` and `(12,6)` must cross the column x=8 with both top and bottom of its perimeter, putting all three (8,5)(8,7)(8,9) cells strictly inside. So the witness has AT LEAST 2 closures, and at least one closure must be on either side of x=8.

**Witness solution** (33 actions; two closures, one around each target pair):

First loop — around target_a `(5,6)` and target_b `(5,9)`:
```
start: avatar (2, 8); trail = []
1.  ACTION1 → (2, 7)
2.  ACTION1 → (2, 6)
3.  ACTION1 → (2, 5)
4.  ACTION4 → (3, 5)
5.  ACTION4 → (4, 5)
6.  ACTION4 → (5, 5)
7.  ACTION4 → (6, 5)
8.  ACTION4 → (7, 5)
9.  ACTION2 → (7, 6)
10. ACTION2 → (7, 7)
11. ACTION2 → (7, 8)
12. ACTION2 → (7, 9)
13. ACTION2 → (7, 10)
14. ACTION3 → (6, 10)
15. ACTION3 → (5, 10)
16. ACTION3 → (4, 10)
17. ACTION3 → (3, 10)
18. ACTION3 → (2, 10)
19. ACTION1 → (2, 9)
20. ACTION1 → (2, 8)  CLOSURE — (2,8) is in trail (index 0).
                Polygon encloses cells with x ∈ {3..6}, y ∈ {6..9}; this includes
                (5,6) and (5,9). Both target_a and target_b captured. No forbiddens
                inside. trail clears.
```
Avatar now at `(2, 8)`. Walk to right side of arena and form second loop around target_c, target_d:
```
21. ACTION4 → (3, 8) ; trail = [(2,8)]
22. ACTION4 → (4, 8)
23. ACTION4 → (5, 8)
24. ACTION4 → (6, 8)
25. ACTION4 → (7, 8)
```
Wait — the first loop's closure cleared all trail. After step 20, trail = []. After step 21, trail = [(2,8)]. Continuing to walk to the right side will deposit trail along the way. The avatar must SKIRT the forbidden column at `x=8`. The player walks to `(7, 8)` then must go around. Let me restate cleaner:

```
21. ACTION4 → (3, 8); trail = [(2, 8)]
22. ACTION4 → (4, 8); trail = [..., (3,8)]
23. ACTION4 → (5, 8)
24. ACTION4 → (6, 8)
25. ACTION4 → (7, 8)
26. ACTION1 → (7, 7)  -- skirt forbidden (8, 6) by going up over it
27. ACTION1 → (7, 6)
28. ACTION1 → (7, 5)
29. ACTION4 → (8, 5)
30. ACTION4 → (9, 5)
31. ACTION4 → (10, 5)
32. ACTION4 → (11, 5)
33. ACTION4 → (12, 5)
34. ACTION4 → (13, 5)
35. ACTION2 → (13, 6)
36. ACTION2 → (13, 7)
37. ACTION2 → (13, 8)
38. ACTION2 → (13, 9)
39. ACTION2 → (13, 10)
40. ACTION3 → (12, 10)
41. ACTION3 → (11, 10)
42. ACTION3 → (10, 10)
43. ACTION3 → (9, 10)
44. ACTION3 → (8, 10)
45. ACTION3 → (7, 10)
46. ACTION1 → (7, 9)
47. ACTION1 → (7, 8) CLOSURE — (7,8) is in trail.
                Polygon includes cells with x ∈ {8..12}, y ∈ {6..9}; contains target_c (11,6),
                target_d (11,9). Captures both. No forbiddens inside (forbidden_a/b are at x=8 — boundary, may
                be strictly inside or on boundary depending on polygon shape).
```

Hmm, this is too long and I'm unsure whether forbiddens at `x=8` are strictly inside the right-side polygon. Let me reposition the layout to make the witness cleaner:

**Revised L2 layout:**
- avatar at `(8, 13)`.
- target_a at `(4, 6)`, target_b at `(4, 9)`.
- target_c at `(12, 6)`, target_d at `(12, 9)`.
- forbidden_a at `(8, 5)`, forbidden_b at `(8, 7)`, forbidden_c at `(8, 9)` — three forbiddens in column x=8, so any single big rectangle around all 4 targets encloses 3 forbiddens → 3 strikes → lose. Forces multi-loop. *Revised — Issue 2 of critique-revisions.md visit 1.*

**Revised witness** (~32 actions, 2 closures):

Loop 1 — around the left target pair `(4,6)(4,9)`. Avatar starts `(8,13)`:
```
1.  ACTION3 → (7, 13)
2.  ACTION3 → (6, 13)
3.  ACTION3 → (5, 13)
4.  ACTION3 → (4, 13)
5.  ACTION3 → (3, 13)
6.  ACTION3 → (2, 13)
7.  ACTION1 → (2, 12)
8.  ACTION1 → (2, 11)
9.  ACTION1 → (2, 10)
10. ACTION1 → (2, 9)
11. ACTION1 → (2, 8)
12. ACTION1 → (2, 7)
13. ACTION1 → (2, 6)
14. ACTION1 → (2, 5)
15. ACTION4 → (3, 5)
16. ACTION4 → (4, 5)
17. ACTION4 → (5, 5)
18. ACTION4 → (6, 5)
19. ACTION2 → (6, 6)
20. ACTION2 → (6, 7)
21. ACTION2 → (6, 8)
22. ACTION2 → (6, 9)
23. ACTION2 → (6, 10)
24. ACTION2 → (6, 11)
25. ACTION2 → (6, 12)
26. ACTION2 → (6, 13)  CLOSURE — (6, 13) was visited at step 3.
                Loop polygon encloses cells with x ∈ {3..5}, y ∈ {6..12}; includes
                target_a (4,6) and target_b (4,9). No forbiddens (forbidden_a is at x=8 — outside).
                Both targets captured. Trail clears.
```

Loop 2 — around right target pair `(12,6)(12,9)`. Avatar at `(6, 13)`:
```
27. ACTION4 → (7, 13);  trail = [(6,13)]
28. ACTION4 → (8, 13)
29. ACTION4 → (9, 13)
30. ACTION4 → (10, 13)
31. ACTION1 → (10, 12)
32. ACTION1 → (10, 11)
33. ACTION1 → (10, 10)
34. ACTION1 → (10, 9)
35. ACTION1 → (10, 8)
36. ACTION1 → (10, 7)
37. ACTION1 → (10, 6)
38. ACTION1 → (10, 5)
39. ACTION4 → (11, 5)
40. ACTION4 → (12, 5)
41. ACTION4 → (13, 5)
42. ACTION4 → (14, 5)
43. ACTION2 → (14, 6)
44. ACTION2 → (14, 7)
45. ACTION2 → (14, 8)
46. ACTION2 → (14, 9)
47. ACTION2 → (14, 10)
48. ACTION2 → (14, 11)
49. ACTION2 → (14, 12)
50. ACTION2 → (14, 13)
51. ACTION3 → (13, 13)
52. ACTION3 → (12, 13)
53. ACTION3 → (11, 13)
54. ACTION3 → (10, 13)  CLOSURE — (10,13) is in trail (index 4 from this loop's start).
                Loop polygon encloses cells with x ∈ {11..13}, y ∈ {6..12}; includes
                target_c (12,6), target_d (12,9). Both captured. No forbiddens inside
                (forbidden_b at (8,9) is to the left of x=11, strictly outside).
                Win predicate fires.
```

Total witness: 54 actions. Step budget should be ≥ 110 to be generous.

**Difficulty justification:**
- (a) **Random-resistance.** Forming TWO clean rectangular closures around specific target pairs while excluding forbiddens within ~110 steps is empirically near-zero probability for a uniform random walker. Each closure independently has probability ~10⁻⁵; the two-closure conjunction with the forbidden-exclusion constraint pushes it < 10⁻⁹.
- (b) **Human-tractable.** A first-time player has already learned M1+M2 from L1 (~10 actions of replay-and-feel). Discovering M3 (forbidden strikes) takes one mistake (1 strike). Discovering M4 (need two loops) is implied by the layout — interleaved targets and forbiddens make the "single big loop" hypothesis visibly fail. Total ~2.5 minutes.
- (c) **Planning depth — moderate post-discovery.** Post-discovery the player faces decisions at each step: which target pair to lasso first (left or right), what loop shape minimises moves while excluding forbiddens, where to start the second loop (the avatar's position after closing loop 1). At least **2 plausible-but-wrong action paths** the post-discovery player would consider and reject:
  1. Big rectangle around all 4 targets (encloses both forbiddens — 2 strikes; followed by a recovery loop = lose at the next forbidden enclosure).
  2. A loop snaking around the forbidden — say a loop with a "notch" cut around `(8, 6)` and `(8, 9)`. The notch's interior would still include forbiddens unless drawn very precisely; computing the precise polygon-interior requires reasoning about Jordan-curve interior, which a casual player will get wrong.
  Witness reasoning chain (per-step):
  - Step 1-6: walk south-then-west to bottom-left corner — establishes a starting boundary point well clear of all sprites.
  - Step 7-14: walk straight up the left edge — establishes the loop's left side.
  - Step 15-19: walk right then south on `x=6` — completes a tight rectangle around `(4,6)(4,9)` without crossing into forbiddens (at `x=8`).
  - Step 26: close on `(6,13)`.
  - Step 27-32: walk east, BACKTRACKING TO SET UP loop 2's starting point.
  - Step 33-54: traverse loop 2's perimeter.
  Each transition requires choosing direction; a wrong direction adds ~6 steps to fix.
- (d) **Step budget.** 110 steps. Witness is 54; budget is 2× — generous over the witness, gives the player room for one full failed-loop attempt before having to retry with care.

### Level 3 — system + 2 more new mechanics

Layout:
- avatar at `(8, 13)`.
- target_a at `(4, 6)`, target_b at `(4, 9)`, target_c at `(12, 6)`, target_d at `(12, 9)` (same as L2).
- forbidden_a at `(8, 5)`, forbidden_b at `(8, 7)`, forbidden_c at `(8, 9)` (same as L2 — 3 forbiddens in column x=8). *Revised — Issue 3 of critique-revisions.md visit 1.*
- pursuer at `(8, 2)` (top centre).

**Mechanics required by the witness** (N = 6 = 4 + 2):
- **M1, M2, M3, M4** — all carried from L1+L2 (each level promotion requires every prior mechanic to remain present and required).
- **M5 — autonomous-pursuer.** New. The pursuer sprite walks one cell per turn toward the avatar via greedy Manhattan-axis BFS over open cells (avoids forbidden, target, trail, walls). If the pursuer ends a turn at a cell adjacent to the avatar (Manhattan-1), the level loses on the NEXT step before the player moves. The pursuer also CANNOT step on trail cells (so the trail blocks the pursuer in addition to other obstacles).
- **M6 — closure-leaves-walls.** New. After every closure in L3, every trail cell that was part of the closed polygon is converted to a `wall_residue` sprite (permanent for the rest of the level). Walls block both avatar movement and pursuer movement.

**Necessity per mechanic (counterfactual):**
- *L3 cannot be solved without triggering M1 because* the four corner-targets have no other capture pathway than closure-side capture; closure requires trail; trail requires M1.
- *L3 cannot be solved without triggering M2 because* the four targets have no other REMOVAL pathway than closure-side capture; M2 is the rule.
- *L3 cannot be solved without triggering M3 because* a single big rectangle around all 4 targets encloses 3 forbiddens at `(8,5)(8,7)(8,9)` → 3 strikes → lose. M3 is the gate that turns a trivial 1-loop fallback into a losing path.
- *L3 cannot be solved without triggering M4 because* same argument as L2: targets at `x=4` and `x=12` cannot both fit inside a single forbidden-excluding polygon, so multi-closure is mandatory.
- *L3 cannot be solved without triggering M5 because* the pursuer sprite has tag `pursuer` and the win predicate requires the pursuer to have `interaction = REMOVED`. Pursuer doesn't get captured the same way targets do — captures only set REMOVED on TARGET-tagged sprites. PURSUER is captured ALSO, when enclosed by a closure (the same M2 rule applies, but M5's CONTRIBUTION here is that the pursuer is mobile — without M5, the pursuer would just sit at `(8, 2)` and the player could ignore it; with M5 the pursuer drifts toward the avatar, forcing the player to close a loop AROUND it before it reaches the avatar.
  Equivalently: if M5 is disabled (pursuer sits still), L3 is solvable via a leisurely 4-loop circuit (each target pair + one for the static pursuer). With M5 enabled, the pursuer's position changes every turn — so the pursuer-capture loop must be timed; if the player spends too many steps on target captures, the pursuer arrives adjacent → lose.
- *L3 cannot be solved without triggering M6 because* given M5 (pursuer chases) and the L3 step budget being TIGHTER than L2 (the witness has more steps overall but per-target-pair fewer slack), the player needs to use prior trail cells AS WALLS to corral the pursuer. Specifically, the witness's first-loop walls at the bottom of the playfield prevent the pursuer from BFS-circumnavigating; without M6 the pursuer would route around prior trails, lengthening the chase and exhausting the step budget.
  Equivalently: if M6 is disabled (closures only clear trail without leaving walls), the pursuer can BFS through any vacated cell, which gives it shorter paths — the witness solution as written takes 70+ steps; without M6, equivalent wall-aided routing would not exist, and the pursuer would intercept the avatar at step ~50.

**Witness solution** (~72 actions). Sketch:

The player executes 3 closures: closure 1 around target_a/target_b (left pair), closure 2 around target_c/target_d (right pair) — both leave bottom-corridor walls (M6) — then closure 3 around the cornered pursuer in the upper-centre region. The pursuer's BFS path is bottlenecked by the wall residues from closures 1 and 2.

Step-level outline (compressed; full enumeration would mirror L2's loop-1 and loop-2 patterns):
```
Steps 1-26   : Loop 1 around (4,6)(4,9) — same shape as L2 witness loop 1.
                 Closure leaves walls at the loop's perimeter cells.
Steps 27-54  : Loop 2 around (12,6)(12,9) — same shape as L2 witness loop 2.
                 Closure leaves walls at the loop's perimeter cells.
Steps 55-72  : Loop 3 around pursuer's current position. By step 54 the pursuer
                 has walked ~54 cells toward the avatar but is now blocked by walls
                 from closures 1+2 in the bottom half; it has been re-routed to
                 the upper-centre. Player walks an enclosure around (pursuer.x,
                 pursuer.y) that leverages the existing top-row walls.
```

**Difficulty justification:**
- (a) **Random-resistance.** A random walker would fail to close any loop (~10⁻⁵ per closure) and would also fail to time the pursuer (random drift would let pursuer reach avatar in expected ~30 steps). Conjunction: < 10⁻¹⁰ in 200-step budget.
- (b) **Human-tractable.** Once L1 and L2 are mastered, L3 introduces 2 new mechanics. M5 (pursuer) is observable in the first 2-3 turns (the maroon sprite visibly steps toward the avatar). M6 (walls remain) is observable on closure 1 (the closure cells turn into cross-hatched grey). Total ~3 minutes.
- (c) **Planning depth — challenging post-discovery.** Post-discovery decisions: which target pair to lasso first matters — the pursuer's BFS path depends on the avatar's position, so closing the LEFT pair first vs RIGHT pair first changes when the pursuer arrives in the upper region. Trivial heuristic that fails: **"capture targets greedily, then deal with pursuer last"**. This greedy heuristic fails because by the time both target pairs are captured (~54 steps), the pursuer (which has been BFS-walking for 54 turns) has reached an area that can no longer be enclosed without re-walking through wall residues — the avatar finds itself trapped behind its own closures. The witness must instead order the closures so closure 1 + 2's walls funnel the pursuer into a corner of the upper region where closure 3 is geometrically possible. This requires planning 2-3 closures ahead.
- (d) **Step budget.** 200 steps. Witness is 72; budget is ~2.8× — generous over the witness; the player will likely waste 30-50 steps on a failed initial loop or a mis-timed pursuer-capture before retrying carefully.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 7]`.

- `ACTION1` — MOVE UP (avatar.y decreases by 4 pixels = 1 logical cell). Always valid unless: blocked by `wall_residue`, blocked by `forbidden`, blocked by arena border, or pursuer-already-adjacent (lose-pending state).
- `ACTION2` — MOVE DOWN (avatar.y += 4). Same gating.
- `ACTION3` — MOVE LEFT (avatar.x -= 4). Same gating.
- `ACTION4` — MOVE RIGHT (avatar.x += 4). Same gating.
- `ACTION7` — UNDO last move (rolls back trail deposit, any captures from a just-closed loop, any walls from closure, and pursuer's motion). One action per undo. Cannot undo before action 1. Strict-undo per the action-enum convention; never overloaded with any non-undo verb.

ACTION5 and ACTION6 are NOT in `available_actions`. The mechanic has no commit verb (closure happens automatically on stepping onto own trail), and no click need.

## 6. HUD and per-game state

### HUD widgets

- `StepCounterHud(RenderableUserDisplay)` — top row (`frame[0, :]`) shows a horizontal bar from left to right: filled (palette 14 green) cells from x=0 to `(remaining/budget) * 64`, then unfilled (palette 4 black). Fed by `_remaining_steps`.
- `StrikeHud(RenderableUserDisplay)` — three small dot-sprites at `(60..63, 0..2)`. Each dot is dark grey (palette 3) when unstruck, bright red (palette 8) when struck. (L2 and L3 only; not visible at L1.)

### Internal state

- `_avatar_pos: tuple[int, int]` — pixel coords of avatar's top-left corner; multiples of 4.
- `_trail_seq: list[tuple[int, int]]` — ordered list of pixel coords where trail cells exist; oldest first. Each step appends `_avatar_pos` (before move) to the list.
- `_trail_sprites: dict[tuple[int, int], Sprite]` — fast lookup from pixel-coord to the placed `trail_cell` Sprite, for removal on closure.
- `_strikes: int = 0` (L2+).
- `_pursuer: Sprite | None` (L3 only) — the pursuer sprite reference for per-step BFS movement.
- `_walls: list[Sprite]` (L3 only) — solidified trail residues.
- `_undo_stack: list[Snapshot]` — per-action snapshots `(avatar_pos, trail_seq snapshot, removed_sprite_names, walls_added, strikes, pursuer_pos)` for ACTION7 rollback.
- `_step_budget: int` — per-level from `level.get_data("step_budget")` (50/110/200 for L1/L2/L3).
- `_post_closure_flash: int = -1` — animation phase counter for the closure-feedback flash (per Issue 6 of critique-revisions.md visit 1). Sentinel `-1` = no closure pending. On a closure step, set to `0`; ramp to `4` over four `step()` calls. During the flash, `_get_valid_actions()` returns an empty action list (all player actions are no-ops), and the to-be-captured target / pursuer sprites colour-cycle palette `{0 white ↔ 11 yellow}` per frame, while the to-be-cleared trail cells colour-cycle palette `{0 white ↔ 7 pink}`. After tick 4, the captured sprites are set to `InteractionMode.REMOVED`, the trail cells are removed (or converted to `wall_residue` in L3), strikes incremented for any forbiddens-inside, and `_post_closure_flash` reset to `-1`. Witness traces in §4 reference this flash as occurring between the closing step and the next player action.

## 7. Win condition

`_check_win()`:

```
all_targets = current_level.get_sprites_by_tag("target")
all_pursuers = current_level.get_sprites_by_tag("pursuer")
captured_targets = all(s.interaction == InteractionMode.REMOVED for s in all_targets)
captured_pursuers = all(s.interaction == InteractionMode.REMOVED for s in all_pursuers)
return captured_targets and captured_pursuers and _strikes < 3
```

When `_check_win()` is True, fire `self.next_level()` (or `self.win()` from L3).

## 8. Lose condition

`_check_lose()`:

```
if _action_count >= _step_budget:
    return True
if _strikes >= 3:
    return True
# L3 only:
if _pursuer is not None and _pursuer.interaction == InteractionMode.TANGIBLE:
    if _manhattan_dist(_pursuer, _avatar) == 1:
        return True
return False
```

When `_check_lose()` is True, fire `self.lose()`. Lose is always paired with M5 (mobile pursuer adjacency at L3) or with budget exhaustion (any level) or with strike-3 (L2+).

## 9. Novelty note

### Closest entries in `mechanic-novelty/taxonomy-of-25-games.md`

- **sk48 paired-snake-trail**. SHARED: trail-deposit-during-walk. **Distinguishing rule**: sk48 uses TWO mirrored snake heads with axis-flipped controls; the win is per-cell colour-match between trails — pure linear bitmap comparison. Boundary Trace uses ONE avatar with no axis flips; the win is Jordan-curve interior detection (point-in-polygon ray cast over a closed walked path). The mathematical primitive is different (linear cell-equality vs polygon-interior membership). Visually: sk48 has two snake-bodies stretched across a tiled floor; tj4n has a single avatar leaving a glowing trail in an open arena.

### Closest entries in `prior-games/index.md`

- **qm4t convex-pen-trap**. SHARED: enclose-target-sprites-as-win. **Distinguishing rule** (concrete): qm4t builds the pen as the **convex hull** of click-dropped vertex posts (Andrew's monotone chain); the player thinks "where to drop 3-8 discrete vertices to convex-fence the right critters", commits via ACTION5. tj4n builds the polygon as the **avatar's literal walked path** (any 4-connected sequence forming a closed cycle); the player thinks "what walking route returns me to my own trail while including target cells and excluding forbiddens". Crucially: qm4t's pen is ALWAYS CONVEX; tj4n's polygon CAN BE NON-CONVEX (concave, U-shaped, comb-shaped). qm4t's vertices can be far apart (no adjacency constraint between vertices); tj4n's polygon edge length is bounded by walk cost (each cell of perimeter = 1 action). The cognitive task and constraint structure differ.
- **sk48-trail-style priors**: ek73 wake-trail-evade (ek73 trail KILLS the player on contact; tj4n trail is friendly and forms the loop-boundary), jd4q echo-trail-teleport (jd4q trail enables teleport-back; tj4n trail enables loop-closure). NOT FLAGGED — different roles for the trail.
- **toggle-priors**: qf8m rook-cross-toggle (clicks flip a fixed 2N-1 cell row+column cross; pure pattern-match win). NOT FLAGGED — qf8m's flip-region is a fixed cross shape, not a free-form polygon, and the player input is one-shot click vs walk-step sequence.

### Axis-1 note (preexisting video games — manual judgment)

The mechanic resembles the 1981 Taito arcade game **Qix** in its "draw closed polygon to capture territory" core. Key differences:

- Qix is constrained to drawing line segments from the GRID EDGE; tj4n has free 4-connected walking in an open arena.
- Qix's enemy is a free-bouncing geometric shape; tj4n L3 has a BFS-pursuer NPC.
- Qix's win threshold is 75% territory claimed; tj4n's win is capture-all-required-targets (count-based).
- Qix has "stix" guards along the in-progress line; tj4n has no along-the-line hazards.
- Qix is real-time arcade; tj4n is turn-based discrete-grid.

Flagging this for the user's manual axis-1 review. The mechanic is presented as a Jordan-curve-interior re-application in the NovaPlay sprite/turn model, not a Qix port.

`prior-games/index.md` is NOT empty (45 entries); the closest is qm4t as analysed above.
