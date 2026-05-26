# Mechanic spec — `tg6w` (settle-pile-tilt)

## 1. Title
Settle-Pile Tilt — gravity-rotate puzzle with colour-permeable walls and sticky catch-pads.

## 2. Mechanic family
`settle-pile-tilt`. Each arrow press sets the playfield's "down" direction (one of the four cardinals); every loose **block** sprite slides simultaneously and multi-cell in the chosen direction until obstructed by a wall or another block, then settles in place. Coloured-rim walls let blocks of the matching colour slide straight through. Sticky-pads catch the first block to slide across them and fix the block at the pad's cell for the rest of the level.

Core-knowledge priors used (per `core-knowledge-priors.md`): **objectness** (coherent block sprites with persistent colour identity that pile against each other), **basic physics** (gravity vector, slide-until-blocked dynamics, settle-on-impact), and **basic geometry & topology** (colour-keyed permeable walls partition the playfield into per-colour reachable regions; sticky-pads anchor positions inside open lanes).

## 3. Sprite roster

The base grid is 21×21 cells (lattice of 7×7 logical positions on a 3-cell stride; sprite at lattice (i, j) is placed at base coords `(3*i, 3*j)`). Camera scale = 3 (renders to 63×63 inside the 64×64 frame, 1px asymmetric letter-box on right/bottom).

Palette signature: `{3 grey, 4 off-black, 6 magenta, 11 yellow, 12 orange, 1 off-white}` — 6 distinct values. Background = palette 4 (off-black); letter-box = palette 4 (matches bg). This signature is deliberately divergent from every prior (zd7m's pastel-pink/yellow/cyan, mr5q's magenta-yellow polarities, xn5p's red/blue/green, kp9z's grey-on-grey).

| Sprite | Pixel matrix (3×3) | Palette values | Tags | Role |
|---|---|---|---|---|
| `wall_solid` | `[[3,3,3],[3,3,3],[3,3,3]]` | 3 grey | `wall`, `wall_solid` | full-blocking wall; collidable; immovable |
| `wall_rim_yellow` | `[[11,11,11],[11,3,11],[11,11,11]]` | 11 yellow + 3 grey | `wall`, `wall_rim_yellow` | yellow-block-permeable wall; visually a yellow-rim with grey core; collidable for non-yellow blocks |
| `wall_rim_orange` | `[[12,12,12],[12,3,12],[12,12,12]]` | 12 orange + 3 grey | `wall`, `wall_rim_orange` | orange-block-permeable wall; collidable for non-orange blocks |
| `block_yellow` | `[[11,11,11],[11,1,11],[11,11,11]]` | 11 yellow + 1 off-white | `block`, `block_yellow`, `loose` | movable yellow block with off-white centre pip (distinguishes from yellow-rim wall whose core is grey) |
| `block_orange` | `[[12,12,12],[12,1,12],[12,12,12]]` | 12 orange + 1 off-white | `block`, `block_orange`, `loose` | movable orange block; mirror visual of yellow block |
| `target_yellow` | `[[11,11,11],[11,-1,11],[11,11,11]]` | 11 yellow + transparent | `target`, `target_yellow` | yellow target indicator; outline-only (transparent centre shows background through, distinguishing from filled block); non-collidable visual marker |
| `target_orange` | `[[12,12,12],[12,-1,12],[12,12,12]]` | 12 orange + transparent | `target`, `target_orange` | orange target indicator; same idiom |
| `sticky_pad` | `[[-1,6,-1],[6,6,6],[-1,6,-1]]` | 6 magenta + transparent | `sticky_pad` | catches the first block sliding across it; renders as a magenta plus-shape (transparent corners so background shows through). Plus-shape is a topological symbol explicitly permitted by `forbidden-elements.md` ("a vertical bar with two horizontal cross-strokes forming a '+' is fine — it's a topological symbol, not a letter"). |

A `StepCounterHud` `RenderableUserDisplay` widget draws the depleting bar at frame row 0: filled cells use palette 11 (yellow), drained cells use palette 4 (background dark). Outside the `sprites` dict, registered as a `Camera(interfaces=[...])` HUD per universal-scaffold.

**Sub-cell detail commentary** (per checklist item 20). Every gameplay sprite is 3×3 with internal structure. Walls are solid grey; rim-walls have a 1-pixel grey core surrounded by an 8-pixel coloured outline (the rim "thickness"). Blocks are filled colour with a 1-pixel off-white centre pip. Targets are 8-pixel coloured outlines with a transparent centre (background shows through). Sticky-pads are sparse plus-patterns. The 32×32 average-pool test fails the spec only if sub-cell detail is invisible at half-resolution; here every sprite has a 1-cell-deep internal contrast pattern, so a 2×2 average-pool would visibly blur the centre pip / transparent core / plus-pattern relative to the surrounding outline. ✓

**Sprite-role commentary** (per checklist item 21). Walls visually read as walls (solid grey blocks). Coloured-rim walls read as walls with a colour cue around them — the colour announces "this wall is permeable to that colour". Blocks read as movable objects (filled colour, slightly highlighted centre). Targets read as "outline-only ghost of a block" — the same shape and colour as the block but hollow, signalling "the block goes here". Sticky-pads read as a hazard / catch zone — the plus-pattern shape is unlike any other sprite in the game and the magenta colour is reserved for this role only. The shape language: filled = movable, outline = target, plus = catch-zone, ringed = passable-by-its-colour. Each sprite type's role is visually distinct from every other type's.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(21, 21)` with a 7×7 lattice (positions 0..6 on a 3-cell stride starting at base coord 0, so lattice (i, j) is rendered at base cells `[3i..3i+2, 3j..3j+2]`). Camera viewport is set to `(21, 21)` in `on_set_level` (camera scale = 3 → 63×63 frame inside the 64×64 letter-box). Lattice rows 0 and 6 and lattice columns 0 and 6 are the border (always full-blocking `wall_solid`). Interior is lattice (1..5, 1..5).

In each level, the witness's "Witness solution" line uses lattice coordinates inside `ACTION_*` notation only as helpful annotation (the engine receives only the action ID — there is no click in this game).

### Level 1 — base dynamic system

**Layout** (lattice coords; `.` = empty interior, `█` = `wall_solid`, `Y` = `block_yellow`, `y` = `target_yellow`):
```
y-row\x-col  0 1 2 3 4 5 6
       0     █ █ █ █ █ █ █
       1     █ Y . . . Y █
       2     █ . . . . . █
       3     █ . . . . . █
       4     █ . . . . . █
       5     █ y . . . y █
       6     █ █ █ █ █ █ █
```

- **Mechanics required by the witness** (N = 1):
  - **M1: arrow-press = simultaneous slide-to-end of every loose block in the chosen cardinal direction**. Each press moves every block multi-cell in the same direction; each block slides until obstructed by a wall sprite, by another block, or by the playfield border. Both yellow blocks move on every press.
- **Necessity per mechanic**:
  - L1 cannot be solved without triggering M1 because the only way a block sprite changes position is via the arrow-press → slide rule (no click action exists, no other verb is in `available_actions`); both yellow blocks must reach the row-5 yellow targets, which sit at lattice cells (1, 5) and (5, 5), and they start at (1, 1) and (5, 1) — a Δy = 4 displacement that no other rule can produce.
- **Witness solution**: `[ACTION2]` (DOWN). On the press, the yellow block at lattice (1, 1) slides through (1, 2), (1, 3), (1, 4) and settles at (1, 5) (border `wall_solid` at row 6 stops it on the cell just above the border). The yellow block at lattice (5, 1) slides identically and settles at (5, 5). Both blocks land on their same-coloured targets. `_check_win` → `next_level()`. **1 action.**
- **Difficulty justification**:
  - **(a) Random-resistance**: a vision-blind / small-LLM agent that picks uniformly among `[ACTION1, ACTION2, ACTION3, ACTION4]` solves with probability 1/4 per press from the initial state. This is the L1-acceptable "tutorial-may-stumble" regime per `from-tech-report.md` § 5; the level's role is teaching, not gating, and the score weight is only 17% of the environment.
  - **(b) Human-tractable**: ~30 seconds. A first-time player presses an arrow, sees blocks slide, presses DOWN if not the first guess, sees the win. The single mechanic is communicated by the first slide animation.
  - **(c) Planning depth**: **no strict planning requirement** (per `difficulty-rules.md` § 2c — L1 is the discovery gate). Once the slide rule is observed, the player picks DOWN and wins; no alternative paths matter post-discovery.
  - **(d) Step budget**: 12 actions. Witness is 1; the budget gives room for the player to try UP / LEFT / RIGHT a few times before figuring out DOWN, plus a small safety margin. Generous over the witness; not shrinking from L0 (this is the first level).

### Level 2 — base system + 1 new mechanic

**Layout** (`.` = empty, `█` = `wall_solid`, `Y` = yellow rim wall, `O` = orange rim wall, `y/o` = blocks, `▢/▣` = targets yellow/orange):
```
y-row\x-col  0 1 2 3 4 5 6
       0     █ █ █ █ █ █ █
       1     █ . . y . o █
       2     █ . . . . . █
       3     █ █ █ Y █ O █
       4     █ . . . . . █
       5     █ ▢ . . █ ▣ █
       6     █ █ █ █ █ █ █
```

Where `Y` at lattice (3, 3) is `wall_rim_yellow` and `O` at (5, 3) is `wall_rim_orange`. The row-3 divider's other cells (1, 3), (2, 3), (4, 3) are `wall_solid`. A `wall_solid` stop-wall sits at lattice (4, 5). Yellow target at (1, 5); orange target at (5, 5).

- **Mechanics required by the witness** (= N + 1 = 2; introduces 1 new mechanic):
  - **M1 (carried forward): arrow-press = simultaneous slide-to-end of every loose block.** Both blocks (yellow and orange) slide on every press.
  - **M2 (new): coloured-rim walls are passable to blocks of the matching colour, blocking to all others.** A yellow block sliding into a `wall_rim_yellow` cell continues straight through; an orange block hitting the same cell is blocked. Symmetric for `wall_rim_orange`. Discoverable from the first DOWN press: each block enters its colour-matched rim wall and emerges below the divider, while sliding into a non-matching rim wall would have stopped it.
- **Necessity per mechanic** (one line per mechanic, naming the concrete cell that blocks every alternate path):
  - L2 cannot be solved without triggering M1 because the only verb available in `available_actions=[1,2,3,4]` is the arrow-press → slide rule; both blocks must traverse Δy ≥ 4 from row 1 to row 5 and Δx ≥ 4 (yellow from col 3 to col 1, after settling at row 5), and only the slide rule produces those displacements.
  - L2 cannot be solved without triggering M2 because the row-3 divider's cells (1, 3), (2, 3), (4, 3) are `wall_solid` (full-blocking for every colour); yellow's target (1, 5) is below row 3 in column 1 with no path through the row-3 divider OTHER than (3, 3) `wall_rim_yellow` — the only yellow-permeable cell in row 3. Yellow must slide through (3, 3), so M2 is exercised. Orange's target (5, 5) is below row 3 in column 5 with no path through the row-3 divider OTHER than (5, 3) `wall_rim_orange` — the only orange-permeable cell in row 3. Orange must slide through (5, 3), so M2 is exercised on a separate cell as well.
- **Witness solution**: `[ACTION2, ACTION3]` (DOWN, LEFT). **2 actions.**
  - Trace:
    - Initial: yellow at (3, 1), orange at (5, 1).
    - **ACTION2 (DOWN)** — slide every block downward. Yellow at (3, 1) slides through (3, 2), enters (3, 3) `wall_rim_yellow` (passable), continues to (3, 4), (3, 5) and settles at (3, 5) (border at row 6 stops it). Orange at (5, 1) slides through (5, 2), enters (5, 3) `wall_rim_orange` (passable), continues to (5, 4) and settles at (5, 5) (border stops it). Orange is now on its target ✓; yellow is at (3, 5), not yet on its target (1, 5).
    - **ACTION3 (LEFT)** — slide every block leftward. Resolution order is leftmost-first. Yellow at (3, 5) slides through (2, 5), (1, 5) and settles at (1, 5) on its target (border at col 0 stops it). Orange at (5, 5) tries to slide left but the next cell (4, 5) is `wall_solid` (the stop-wall) — orange does not move and stays settled at (5, 5) ✓ on its target.
    - Win predicate true; `next_level()`.
- **Difficulty justification**:
  - **(a) Random-resistance**: a vision-blind random agent has only 1/16 chance of pressing the specific 2-tuple `[DOWN, LEFT]` (`p = (1/4)^2 = 1/16`); but the more sensitive failure mode is sliding LEFT or RIGHT first, which misaligns blocks with their colour-matched rim columns and requires an undo-equivalent to recover. After ACTION3 first, yellow is at (1, 1) (border) and orange is at (4, 1) (blocked by yellow at (1, 1) via interposed slide). The yellow block is now in column 1, not column 3, so DOWN sends yellow into (1, 3) which is `wall_solid` — yellow stops at (1, 2) and never crosses the divider. Recovery requires sliding yellow right back to column 3 with the orange block out of the way. Random play across the 25-step budget has well below 1/10000 cumulative probability of executing the specific recovery plus winning sequence.
  - **(b) Human-tractable**: ~2 minutes. The player observes from the first DOWN press that "yellow block went through yellow-rim wall, orange went through orange-rim wall" — colour-permeability is read from a single observation. Then needs to figure out the LEFT step: notice yellow at (3, 5) needs to reach (1, 5) and that the stop-wall at (4, 5) keeps orange at (5, 5) when the player slides LEFT. About a minute of observation + half a minute of execution.
  - **(c) Planning depth (post-discovery)**: 
    - **Decision space at level start**: 3 valid first actions. ACTION1 (UP) is no-op — both blocks are already at row 1 with the row-0 border immediately above them. ACTION2 (DOWN), ACTION3 (LEFT), ACTION4 (RIGHT) all produce state changes.
    - **Plausible-but-wrong alternative**: ACTION3 (LEFT) first. A post-discovery player who has just learned colour-permeability might think "I need yellow at column 1 — it's already in column 3, so let me slide it LEFT first to align with target column 1, then DOWN." LEFT slides yellow to (1, 1) (border) — but now yellow is in column 1, where the row-3 divider has `wall_solid` at (1, 3); yellow can't cross. The post-discovery error is failing to notice that the yellow rim is at column 3 (where yellow already started), not column 1. The witness instead presses DOWN first (using the lucky-but-not-trivial column alignment) to ferry both blocks across the divider; then LEFT to nudge yellow alone (the stop-wall holds orange in place).
    - **Witness's reasoning chain**: "Yellow rim is at column 3 — yellow happens to start at column 3. Orange rim is at column 5 — orange happens to start at column 5. Pressing DOWN immediately uses both alignments. After DOWN, orange is on its target; yellow needs to slide left from (3, 5) to (1, 5). The stop-wall at (4, 5) is the sole reason orange stays put on its target during the LEFT press — without it, orange would slide off-target into column 1 too. Recognising the stop-wall's role in fixing orange is the post-discovery insight."
  - **(d) Step budget**: 25 actions. Witness is 2; the budget allows the player to try a wrong first move (LEFT or RIGHT), recover (slide back, e.g. RIGHT then DOWN), and still win. Generous; not shrinking from L1's 12 (L2 is a level promotion, mechanic-discovery cost rises).

### Level 3 — base system + 2 carried-forward + 1 new mechanic

**Layout** (`.` = empty, `█` = `wall_solid`, `Y` = yellow rim wall, `O` = orange rim wall, `y/o` = blocks, `▢/▣` = targets, `*` = `sticky_pad` overlapping yellow target):
```
y-row\x-col  0 1 2 3 4 5 6
       0     █ █ █ █ █ █ █
       1     █ . . y . o █
       2     █ . . . . . █
       3     █ Y █ █ █ O █
       4     █ . . . . . █
       5     █ . . * . ▣ █
       6     █ █ █ █ █ █ █
```

(Note: row 3 has 7 cells matching the lattice grid; the `█ Y █ █ █ O █` reading lattice (0..6, 3) is `wall_solid, wall_rim_yellow, wall_solid, wall_solid, wall_solid, wall_rim_orange, wall_solid`. The yellow-rim is at lattice (1, 3) and the orange-rim is at lattice (5, 3); all other row-3 cells are `wall_solid`.) Sticky-pad at lattice (3, 5). Yellow target at (3, 5) (the same cell as the sticky-pad — the sticky catches the yellow block on top of its target). Orange target at (5, 5).

- **Mechanics required by the witness** (= L2-count + 1 = 3; introduces 1 new mechanic):
  - **M1 (carried forward): arrow-press = simultaneous slide-to-end of every loose block.** Both blocks slide on every press.
  - **M2 (carried forward): coloured-rim walls are passable to blocks of the matching colour.** Yellow-rim at (1, 3); orange-rim at (5, 3). Both must be exercised.
  - **M3 (new): sticky-pads catch the first block to slide ACROSS them and fix that block at the pad's cell for the rest of the level.** A block that is already settled on a sticky-pad cell (didn't slide ACROSS it during a press) is also fixed once it does slide across; subsequent presses see the caught block as a wall (full-blocking).
- **Necessity per mechanic** (one line per mechanic at L3):
  - L3 cannot be solved without triggering M1 because the only verb is the slide rule — both blocks must be repositioned by Δx ≥ 2 and Δy ≥ 4 from their start cells, and only the slide produces those displacements.
  - L3 cannot be solved without triggering M2 because row 3's only yellow-permeable cell is (1, 3) and only orange-permeable cell is (5, 3); every other row-3 cell is `wall_solid`. Yellow's target (3, 5) is below row 3 so yellow must slide through (1, 3) at some point. Orange's target (5, 5) is below row 3 so orange must slide through (5, 3) at some point. M2 is exercised on two distinct cells, neither bypassable.
  - L3 cannot be solved without triggering M3 because yellow's target is at lattice (3, 5) — a mid-row interior cell with NO wall sprite at (4, 5) or beyond up to the col-6 border in row 5. Without the sticky-pad at (3, 5), a yellow block sliding RIGHT through row 5 from any column < 3 would continue past (3, 5) and settle at (5, 5) (or wherever the orange block currently sits, otherwise the col-6 border). Without sliding LEFT through (3, 5) from column ≥ 4, the yellow block would settle at (1, 5) (border). The only mechanism that stops a yellow block AT (3, 5) and not at the wall/border beyond is the sticky-pad. So any winning sequence must have yellow slide ACROSS (3, 5), triggering M3.
- **Witness solution**: `[ACTION3, ACTION2, ACTION4, ACTION2]` (LEFT, DOWN, RIGHT, DOWN). **4 actions.**
  - Trace:
    - Initial: yellow at (3, 1), orange at (5, 1).
    - **ACTION3 (LEFT)** — leftmost-first. Yellow at (3, 1) slides through (2, 1), (1, 1) and settles at (1, 1) (border stops). Orange at (5, 1) slides through (4, 1), (3, 1)—now empty—then (2, 1)—empty—then (1, 1) where yellow is settled, so orange settles at (2, 1). State: yellow (1, 1), orange (2, 1).
    - **ACTION2 (DOWN)** — topmost-first; tiebreak leftmost. Yellow at (1, 1) slides through (1, 2), enters (1, 3) `wall_rim_yellow` (passable), continues to (1, 4), (1, 5) and settles at (1, 5) (border). Orange at (2, 1) slides through (2, 2), tries (2, 3) `wall_solid` — blocked, settles at (2, 2). State: yellow (1, 5), orange (2, 2).
    - **ACTION4 (RIGHT)** — rightmost-first. Orange at (2, 2) slides through (3, 2), (4, 2), (5, 2) and settles at (5, 2) (border at col 6 stops). Yellow at (1, 5) slides through (2, 5), enters (3, 5) which is the sticky-pad — yellow is caught at (3, 5) and FIXED for the rest of the level. State: yellow (3, 5) ✓ FIXED on its target, orange (5, 2).
    - **ACTION2 (DOWN)** — topmost-first. Orange at (5, 2) slides through (5, 3) `wall_rim_orange` (passable), (5, 4), and settles at (5, 5) (border) on its target ✓. Yellow is fixed; doesn't move.
    - Win predicate true; `next_level()`.
- **Difficulty justification**:
  - **(a) Random-resistance**: random play has p ≤ (1/4)^4 = 1/256 of hitting the specific 4-tuple, but the constraining factor is the sticky-pad's one-shot trap: any sequence in which the YELLOW block does not slide across (3, 5) on its first crossing of row 5, OR in which any block slides ACROSS (3, 5) before yellow is the one doing so, ends in yellow stuck at the wrong cell or orange caught at (3, 5) instead. Concretely: pressing DOWN first (the most natural greedy first move) puts orange at (5, 5) immediately; subsequent LEFT presses cause orange to slide leftward through (4, 5) and into the sticky-pad at (3, 5) — orange is now CAUGHT at (3, 5), at yellow's target, and the level becomes UNWINNABLE because orange cannot be dislodged and cannot reach its own target (5, 5). The rate of accidentally trapping orange (or otherwise locking out the win) is high enough that random play with the 30-step budget achieves p(win) well below 1/10,000.
  - **(b) Human-tractable**: ~3 minutes for an attentive human. The player observes (i) row 3 is mostly impermeable; (ii) yellow's column-1 rim and orange's column-5 rim; (iii) the magenta X-pattern at (3, 5) acts as a trap (after a misstep that traps a block there, the player learns the rule). The witness requires the player to recognise that yellow must arrive at column 1 BEFORE pressing DOWN, that pressing LEFT first does this without losing the orange block, and that the sticky-pad must be approached from the LEFT (RIGHT-press, with yellow at (1, 5)) so yellow is the block that gets caught — not orange.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start**: 3 valid first actions. UP is no-op (both blocks at row 1, top-border above). DOWN, LEFT, RIGHT all change state. ≥ L2's 3. ✓
    - **Trivial post-discovery heuristic that fails**: **greedy-toward-target / monotone-progress**. A fully-informed player reads "yellow → (3, 5), orange → (5, 5)" and presses DOWN first because DOWN reduces both blocks' Manhattan distance to target the most. After DOWN: yellow stops at (3, 2) (blocked by `wall_solid` at (3, 3)); orange settles at (5, 5) on its target. So far so good — but now yellow is stuck at column 3 with no row-3 path through the divider in column 3. The player must move yellow to column 1 (LEFT) or back to column 3 by some manoeuvre. After LEFT from this state: yellow at (3, 2) slides left to (1, 2); orange at (5, 5) slides left through (4, 5), then enters (3, 5) sticky-pad — ORANGE IS CAUGHT at (3, 5), occupying yellow's target. The level becomes unwinnable: yellow cannot reach (3, 5) (occupied by orange) and orange cannot leave it.
    - **Where the heuristic diverges from the witness**: at action 1. Greedy presses DOWN; witness presses LEFT. Greedy's mistake is assuming "DOWN first" is locally optimal because it advances both blocks toward their target rows; but it leaves orange in a position where the necessary subsequent yellow-positioning press traps orange in the sticky-pad. The witness instead uses LEFT first to set up yellow's cross-divider alignment WITHOUT moving orange below row 1 (orange at (5, 1) is held against the col-6 border by yellow's leftward shift, ending up at (2, 1) blocked by yellow). Now yellow is in column 1 (the only yellow-permeable column on row 3); subsequent DOWN sends yellow to (1, 5); subsequent RIGHT sends yellow into the sticky-pad at (3, 5) BEFORE orange reaches row 5; subsequent DOWN finally sends orange through (5, 3) orange-rim to (5, 5). The order matters because the sticky-pad is a one-shot resource — and the heuristic's sequence consumes it on the wrong block.
  - **(d) Step budget**: 30 actions. Witness is 4; the budget allows multiple wrong attempts and recovery from a sub-optimal first press before the sticky-pad is consumed (note: once orange is caught, the level is unwinnable, but the player can still observe the trap, run out the clock, and learn for the next attempt — this is handled at the level-restart layer outside the spec, since `tg6w` does not implement undo). Not shrinking from L2's 25 (L3 adds discovery cost for M3).

## 5. Action mapping

`available_actions = [1, 2, 3, 4]` (pure cardinal motion; no click, no ACTION5 freedom slot, no undo).

| Action | Semantic |
|---|---|
| `ACTION1` | UP — set the gravity vector to `(0, -1)`; every loose block slides upward until obstructed by a wall, another block, or the row-0 border. |
| `ACTION2` | DOWN — gravity `(0, +1)`; every loose block slides downward. |
| `ACTION3` | LEFT — gravity `(-1, 0)`; every loose block slides leftward. |
| `ACTION4` | RIGHT — gravity `(+1, 0)`; every loose block slides rightward. |

Per the freedom-slot rule in `action-enum.md` § "Distinctive verb on ACTION1-4", `tg6w`'s identity verb (the gravity-direction-set + simultaneous slide) lives directly on the four cardinal slots; ACTION5 is intentionally unused because the four-direction vector covers the entire mechanic and there is no orthogonal "modal verb" that would benefit from a separate slot. This matches the m0r0 / tr87 pattern (cardinal-only; the directional input IS the unusual mechanic).

**No context-gating**: the four arrows are always valid (the engine never returns "no movement" — even if every block is blocked, the action is consumed and the step counter ticks). The agent can press any direction at any time; the consequence is purely geometric.

## 6. HUD and per-game state

**HUD widget**: `StepCounterHud` (subclass of `RenderableUserDisplay`). Renders a horizontal bar across frame row 0 (top) — 21 cells wide for an outer-grid render of 21 grid cells; filled cells use palette 11 (yellow), drained cells use palette 4 (matching background). The bar drains 1 cell per consumed action regardless of whether any block actually moved (so wasted presses still cost). Registered via `Camera(interfaces=[step_counter_ui])`.

**Internal state** (kept on the Game instance; semantic names per universal-scaffold style):

- `self._step_budget: int` — current level's step budget (read from `level.get_data("step_budget")` in `on_set_level`).
- `self._steps_used: int` — counter of actions consumed (reset in `on_set_level`; incremented at the end of each handled action's branch in `step()`, before the lose/win check). NOT `self._action_count` from the engine, which counts the implicit RESET as a step (per `fix_implementation.md` § CHECK_LOSE_PATH_EXISTS canonical pattern, this avoids the "first-frame energy already lost" bug).
- `self._step_counter_ui: StepCounterHud` — the HUD instance; its `remaining` field is rebound from `self._step_budget - self._steps_used` after every action.
- `self._fixed_block_cells: set[tuple[int, int]]` — set of base-grid coords currently occupied by sticky-pad-caught blocks. Treated as walls during slide resolution; a block whose target cell is in this set stops its slide.
- `self._sticky_pad_cells: set[tuple[int, int]]` — set of base-grid coords of sticky-pad sprites in the current level (read from level sprites at `on_set_level` time). Used by the slide resolver: if a block's slide PATH crosses a `sticky_pad_cell` and that cell is not in `_fixed_block_cells`, the block is caught at that cell, the cell is added to `_fixed_block_cells`, and the block becomes immovable for the rest of the level.

**Persistent visual cues for state-mutating events** (per checklist item 19 — no hidden state):

- *Block position*: the block sprites themselves are the cue; their `(x, y)` after every press is the new state, rendered directly into the frame.
- *Sticky-pad consumed*: when a sticky-pad catches a block, the caught block sprite is positioned exactly at the pad's centre cell; the X-pattern of the pad is overdrawn by the block sprite (the block has higher `layer` than the pad). The visual changes from "magenta X-pattern visible" → "block visible at pad cell" — the X is gone, signalling consumption. Subsequent presses do not move the block, so the cue remains for the rest of the level.
- *Step counter*: the bar visibly shrinks each press; the player can see how many actions remain by counting yellow cells.
- *Gravity direction*: ephemeral per-press only; the slide animation (multi-frame) IS the cue, showing every block moving in the chosen direction. After settling there is no persistent gravity indicator (which is correct — gravity only matters during a slide and is fully determined by the action just pressed; the player does not need a "current gravity" indicator because gravity is reset every press).

## 7. Win condition

After every action's slide-and-settle has fully resolved (including any sticky-pad captures), the game evaluates `_check_win()`:

> Every block sprite occupies a cell at which a target sprite of the matching colour is also positioned (the target sprite at the same `(x, y)` and the block sprite share a colour-tag pair: `block_yellow ↔ target_yellow`, `block_orange ↔ target_orange`). Equivalently: for every sprite `b` with tag `block`, there exists a sprite `t` with tag `target` such that `(t.x, t.y) == (b.x, b.y)` AND `b.tags ∩ t.tags ⊇ {colour-tag}`.

If true, call `self.next_level()` (which advances or wins the environment). The win predicate is checked after every `ACTION1..4`; it is testable, deterministic, and the same predicate works for L1, L2, and L3 (the colour set just expands).

## 8. Lose condition

After every action, after the win check, evaluate:

> `self._steps_used >= self._step_budget`

If true, call `self.lose()`. There is no instant-fail hazard, no irreversible-collision lose, and no out-of-bounds. The only lose path is step exhaustion — the universal pattern across the 25 reference games and confirmed in cross-cut-frequencies.md.

(L3's sticky-pad trap can put the level into an unwinnable state mid-run, in which the player's only outcome is to run out the step budget. Per `difficulty-rules.md` § 1, a soft-lock that doesn't fire `lose()` immediately is forbidden; here the unwinnable state IS detectable — the implementation must check after every press whether `_check_win` can still be satisfied given the current `_fixed_block_cells`, and if not, fire `self.lose()` immediately. This avoids the "no-win waiting room" anti-pattern. Implementation note: the soft-lock check is a small graph reachability probe — for each loose block, can it reach SOME target of its colour given current obstacles + fixed-block-cells? If any block has no reachable matching target, lose() fires.)

## 9. Novelty note

### Closest taxonomy entries (per `mechanic-novelty/similarity-check.md`)

**`g50t walk-vs-scroll`** — single-avatar arrow-step on a scrolling board; ACTION5 is a context special. **Distinguishing rule**: g50t has one player-controlled avatar and a single-cell-step verb plus an autonomous world scroll providing time pressure; `tg6w` has multiple loose blocks with no avatar, no autonomous scroll, and a slide-to-end (multi-cell) displacement per press. The cognitive primitive is "arrange a population by tilting the world" (settle dynamics) vs. "guide an avatar against a moving deadline" (chase/race).

**`tu93 maze-pickup-train`** — leader-follower train on a maze; arrows step the lead pawn one cell. **Distinguishing rule**: tu93 has a leader-follower coupling between the player-controlled lead and tagalong agents that walk one cell per press; `tg6w` has independent equally-affected blocks with no coupling and no leader, sliding multi-cell per press. The verb is "lead a chain through a maze" vs "tilt the world and watch a population settle".

**`sp80 pour-shelf-route`** — rows of shelves over U-cups; click-and-slide a shelf, pour-key spills water cup-to-cup. **Distinguishing rule**: sp80's matter is liquid with split-on-shelf-and-fall-off-end behaviour; the verb is shelf positioning + per-level pour-attempts (4). `tg6w` has discrete block sprites that slide as a population on each press, no liquid splitting, no per-level pour budget — only the universal step counter.

**`m0r0 mirror-orb-merge`** — UP moves both pawns up but LEFT pushes one and pulls the other. **Distinguishing rule**: m0r0 has two pawns with axis-mirrored controls (one input → opposite responses on different axes); `tg6w` has uniform response across all blocks (one input → every block goes the same direction). The cognitive task in m0r0 is unifying coupled-mirror-axis kinematics; in `tg6w` it is settle dynamics with per-colour permeable barriers.

### Closest prior-games entries (per `prior-games/index.md`)

**`zd7m cohort-step-route`** — arrows step every movable pawn one cell; anchors selectively block; portals teleport into a sealed chamber. **Distinguishing rule**: zd7m's arrows move every pawn **exactly one cell** (Manhattan-routing planning where anchors are colour-keyed step-blockers and portals teleport). `tg6w`'s arrows slide every block **all the way until obstructed** (Sokoban-style multi-cell settle); the planning is trajectory prediction with pile-up dynamics, and the obstacles are colour-permeable rim walls (not colour-keyed step-blockers) plus one-shot sticky-pads (not portals). The cognitive task is genuinely different: zd7m is "where does each pawn step this turn" (one-cell granularity, Manhattan-routing); `tg6w` is "where does each block come to rest after a global avalanche" (slide-to-end granularity, settle-dynamics). At the visual level the games also diverge: zd7m uses pastel-pink/yellow/cyan blocks on a dark backdrop; `tg6w` uses a dark backdrop with yellow+orange blocks plus magenta sticky-pads.

**`wt39 glide-deflect-thaw`** — single pawn glides in pressed direction until wall; angled bumpers deflect 90°. **Distinguishing rule**: wt39 has a SINGLE pawn that glides; the gameplay is single-entity trajectory routing through bumpers. `tg6w` has MULTIPLE blocks that slide simultaneously and pile against each other; the distinguishing feature is the inter-block collision/settling dynamic, where block A may stop because block B already settled, and on the next press the chain reorganises. The pile-up coordination has no analogue in wt39's single-pawn glide. wt39 has bumpers (deflection) which `tg6w` lacks entirely; `tg6w` has colour-permeable rim walls and sticky-pads which wt39 lacks.

**`kn58 anchor-pull-magnet`** — click any cell to place a single magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it. **Distinguishing rule**: kn58's verb is click-to-place-anchor; the slide direction is per-pawn (whichever axis is dominant from that pawn to the anchor) and one-cell-only. `tg6w`'s verb is arrow-press; the slide direction is **uniform across all blocks** (pure cardinal, set by the arrow), and the slide magnitude is **multi-cell** (slide-to-end). At a visual level kn58 has sparse 2-block layouts; `tg6w` has more blocks and structural walls partitioning the playfield.

**`kx14 tide-tilt-buoyant`** — vertical fluid tank with ACTION1/2 raising/lowering water level, ACTION3/4 tilting floating balls, ACTION6 anchoring. **Distinguishing rule**: kx14 simulates a vertical fluid tank with continuous water-level state and ball-buoyancy; the action vocabulary is two-axis (level + tilt) plus anchor-click. `tg6w` has no fluid, no buoyancy, no continuous level — a pure 4-direction discrete tile-slide on a uniform grid with no axis privileged. kx14's visual is a half-air-half-water scene; `tg6w` is a uniform gridded board with discrete block sprites.

**`kp9z grain-accumulate-topple`** — click sources to drop grains; cells overflow at capacity 4; sinks absorb; click-rotatable redirectors. **Distinguishing rule**: kp9z grows the grain population by clicking sources; per-cell capacity drives a topple cascade. `tg6w` has a fixed-count block population from level start; there is no capacity, no topple, no source-click — only player-driven simultaneous slide.

### Negative-similarity test (full spec re-walk; per `negative-similarity-check.md`)

Re-walking the 8 dimensions on the now-fleshed-out spec against the closest concern (zd7m):

| Dimension | vs zd7m | Shared? |
|---|---|---|
| 1. Board content | zd7m: pawns + anchors + portals on grid. `tg6w`: blocks + walls (incl. coloured rims) + sticky-pads on grid. Both "multi-block-on-grid". | shared (loosely) |
| 2. Player input | zd7m: arrows = each pawn 1-cell-step coordinated. `tg6w`: arrows = each block slide-to-end. | not shared |
| 3. Goal | zd7m: route pawn to terminal. `tg6w`: every block on its same-coloured target. | not shared |
| 4. Lose | both step counter | shared |
| 5. Cast | zd7m: anchors + portals. `tg6w`: solid walls + colour-rim walls + sticky-pads. | not shared |
| 6. Visual signature | zd7m: dark backdrop + pastel pink/yellow/cyan with white-pip cells. `tg6w`: dark backdrop + yellow/orange with off-white-pip cells, plus magenta X-pad and grey-rim coloured walls. | not shared (palette divergence; sticky-pad shape unique) |
| 7. Pixel grain | both 3×3 sprites with internal pattern. | shared |
| 8. Core dynamic | zd7m: "each press, every pawn moves 1 cell coordinated; route through anchors". `tg6w`: "each press, every block avalanches to a new pile against walls and each other; route via colour permeable cells; one-shot sticky catches". | not shared |

Shared: 1, 4, 7 = 3 dimensions. The fundamental dimensions (8 core dynamic, 6 visual signature) are not shared; the pile-up dynamics + colour-permeability + one-shot sticky-pads constitute a distinct cognitive / mechanical task. **NOVEL** below the rejection threshold.

### Prior-games corpus state
24 entries; the closest concerns above (zd7m, wt39, kn58, kx14, kp9z) all have their distinguishing rules articulated. No other prior is at the family-level near-miss threshold; not enumerated.
