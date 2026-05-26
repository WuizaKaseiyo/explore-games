# mz6t — Majority-Vote Stabilizer

## 1. Title
Majority-Vote Stabilizer (working title; never shown in-game).

## 2. Mechanic family
`majority-vote-stabilize`. Prior categories used (per `core-knowledge-priors.md`):
- **Objectness** — each grid cell is a persistent coloured tile that retains its state across actions until overwritten by a click or by a vote-induced flip.
- **Basic geometry & topology** — vote propagation respects 4-connected cardinal neighbourhoods; walls partition the field into voting regions whose stabilisation is locally determined; anchor cells lock once they reach a target colour.

Agentness is *not* used: there is no avatar; the game's "actors" are abstract voting cells.

## 3. Sprite roster

All sprites are 8×8 pixel tiles unless noted, on a 64×64 logical grid. Backgrounds are palette `4` (off-black) tile rims. The full rendered field uses palettes `4` (off-black rim/bg), `7` (pink), `10` (light-blue), `12` (orange), `13` (maroon walls), `14` (green anchor-locked accent), `5` (black anchor-unlocked corner accent). No palette value reads as a digit, letter, or recognisable real-world object.

| Name | Dimensions | Palette values | Tags | Role |
|---|---|---|---|---|
| `vote_lb` | 8×8 | 4, 10 | `["voter"]` | Voting cell currently in state 0 (light-blue solid disc inside a pixel-thick black rim). |
| `vote_or` | 8×8 | 4, 12 | `["voter"]` | Voting cell currently in state 1 (orange hollow ring inside a pixel-thick black rim). |
| `vote_pk` | 8×8 | 4, 7 | `["voter"]` | Voting cell currently in state 2 (pink plus-sign inside a pixel-thick black rim). |
| `wall_cell` | 8×8 | 4, 13 | `["wall"]` | Immutable wall cell (maroon woven block with off-black gaps). Doesn't vote, isn't voted on, click is a no-op. |
| `anchor_lb` | 8×8 | 4, 5, 10 | `["voter", "anchor"]` | Voting cell with anchor decoration (black corner pips on the 4 outer corners) currently in state 0. Identical voting behaviour to `vote_lb` until it reaches its target colour. |
| `anchor_or` | 8×8 | 4, 5, 12 | `["voter", "anchor"]` | Anchor cell currently in state 1. |
| `anchor_pk` | 8×8 | 4, 5, 7 | `["voter", "anchor"]` | Anchor cell currently in state 2. |
| `anchor_locked_lb` | 8×8 | 4, 14, 10 | `["voter", "anchor", "locked"]` | Anchor cell that has already matched its target while in state 0 — the 4 corner pips switch from black (`5`) to green (`14`) to signal the lock. Cannot be re-coloured by click or by tick. |
| `anchor_locked_or` | 8×8 | 4, 14, 12 | as above | Locked anchor in state 1. |
| `anchor_locked_pk` | 8×8 | 4, 14, 7 | as above | Locked anchor in state 2. |
| `target_lb` | 3×3 | 4, 10 | `["target_cell"]` | Quarter-scale target tile rendering state 0. The half-scale target panel is a 5×5 mosaic of these. |
| `target_or` | 3×3 | 4, 12 | `["target_cell"]` | Quarter-scale target tile rendering state 1. |
| `target_pk` | 3×3 | 4, 7 | `["target_cell"]` | Quarter-scale target tile rendering state 2. |
| `target_wall` | 3×3 | 4, 13 | `["target_cell"]` | Quarter-scale target tile rendering a wall position. |
| `target_anchor_lb` | 3×3 | 4, 5, 10 | `["target_cell"]` | Quarter-scale target tile for an anchor position whose target is state 0 (corner-pip motif preserved at 3×3 scale). |
| `target_anchor_or` | 3×3 | 4, 5, 12 | `["target_cell"]` | Quarter-scale target tile for anchor target = state 1. |
| `target_anchor_pk` | 3×3 | 4, 5, 7 | `["target_cell"]` | Quarter-scale target tile for anchor target = state 2. |

The 3 voting-cell colour states are visually distinguished by **shape** (solid disc / hollow ring / plus-sign) on top of palette difference — readers can tell them apart in greyscale, satisfying checklist item 20 ("shape carries meaning, not just colour").

Anchor cells are visually distinguished by the **4 corner pips** in palette `5` (or `14` once locked); the centre motif (disc/ring/plus) still indicates current colour state.

Layout of a level (logical grid 64×64):
- **Voting playfield** at pixel (2, 2)..(41, 41): a 5×5 grid of 8×8 cells, occupying 40×40 px.
- **Target panel** at pixel (44, 13)..(58, 27): a 5×5 mosaic of 3×3 mini-cells, occupying 15×15 px, vertically centred opposite the playfield.
- **Step-counter HUD** along row 62, x=2..61: a 60-px horizontal bar that depletes one tick per consumed action.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels per `composition-and-tutorial.md`. Grid size is 5×5 cells throughout (no per-level resize); `level.grid_size = (64, 64)` with the voting playfield laid out as described in §3. Level data carries per-level `initial_state`, `target_state`, `step_budget`, plus tagged sets for walls and anchor positions.

**Initial / target notation in this section.** A 5×5 array `I[r][c]` (or `T[r][c]`) for `r, c ∈ 0..4`. Symbols: `0` = state 0 (light-blue), `1` = state 1 (orange), `2` = state 2 (pink), `W` = wall, `A0/A1/A2` = anchor cell with current/target state appended.

### Level 1 — base dynamic system

**Mechanics required by the witness (N = 2):**

- **M1 — Click cycles a cell's colour state.** ACTION6 click on a voting cell advances its state by `+1 mod 3` (light-blue → orange → pink → light-blue). Click on a wall cell is a no-op.
- **M2 — Tick applies majority-vote propagation.** ACTION5 reads each voting cell's 4 cardinal neighbours, counts colour states among neighbours that are voters (excluding off-grid and excluding walls), and if any single colour state `C` has `count(C) ≥ 3` (strict majority over up to 4 voters), the cell adopts `C`. All cells update simultaneously (read old state → write new state). The win check fires *only on ACTION5* — a level cannot be won with clicks alone, the player must end with a tick.

**Layout.**
- Walls: none.
- Anchors: none.
- `I[0]` = `[0, 0, 0, 0, 0]`
- `I[1]` = `[0, 0, 1, 1, 0]`
- `I[2]` = `[0, 1, 0, 1, 0]`
- `I[3]` = `[0, 1, 1, 1, 0]`
- `I[4]` = `[0, 0, 0, 0, 0]`
- `T[0]` = `[0, 0, 0, 0, 0]`
- `T[1]` = `[0, 1, 1, 1, 0]`
- `T[2]` = `[0, 1, 1, 1, 0]`
- `T[3]` = `[0, 1, 1, 1, 0]`
- `T[4]` = `[0, 0, 0, 0, 0]`

The diff cells (initial vs target) are `(1,1)` and `(2,2)` — both must end in state 1.

**Necessity per mechanic:**

- **L1 cannot be solved without triggering M1** because cell `(1,1)` has 4 cardinal neighbours `{(0,1)=0, (2,1)=1, (1,0)=0, (1,2)=1}` whose colour counts are `2 × state-0` and `2 × state-1`. No single colour reaches `count ≥ 3`, so no tick (or sequence of ticks) ever flips `(1,1)`. The only way to advance `(1,1)` to state 1 is an ACTION6 click on it.
- **L1 cannot be solved without triggering M2** because the win check fires only on ACTION5; the engine never inspects target match after an ACTION6 click. Even if the player composes a state that matches the target via clicks alone, the level only advances on a tick. (Additionally, `(2,2)` flips state 1 *only* under M2 — its 4 neighbours after the diff click are all state 1, so the tick is what places `(2,2)` into the target state without an extra click.)

**Witness solution (shortest):**

```
1. ACTION6 click at display pixel (14, 14)   # cell (col=1, row=1); cycles state 0 → 1 (orange)
2. ACTION5                                     # tick; (2,2) flips to state 1 because its 4 neighbours are all state 1
```

Two actions. Click pixel `(14, 14)` is the centre of cell `(col=1, row=1)`: pixel `(2 + 1·8 + 4, 2 + 1·8 + 4) = (14, 14)`.

**Difficulty justification.**

- **(a) Random-resistance.** A vision-blind / random-policy agent has effectively zero chance of winning L1 in the step budget: the action space is `{ACTION5, ACTION6@(any of 64×64 pixels)}` and the level only wins when (i) the unique missing-orange diff cell `(1,1)` has been clicked exactly once *and* (ii) the agent ends with an ACTION5. A random click lands on any of the playfield's 25 cells uniformly (~4% on `(1,1)`), and even the right click must be followed by an ACTION5 with no intervening clicks elsewhere overwriting `(1,1)` past state 1. With a budget of 25 actions, the joint probability of a winning random sequence is well below the §3.5 graph threshold of 1 / 10,000.
- **(b) Human-tractable.** ~2 minutes for an attentive human reading the screen for the first time. The two verbs are visually obvious from sprite cycling on a click and from the synchronous shape-shift on a tick; the missing diff at `(1,1)` is legible because the target panel shows it in state 1 while the playfield shows it in state 0.
- **(c) Planning depth.** *No strict planning requirement.* L1 is the discovery gate; once the player has understood that ACTION6 cycles a cell and ACTION5 ticks the field, the witness is near-immediate.
- **(d) Step budget.** `step_budget = 25`. Witness length is 2; budget is 12.5× the witness, well over the "generous" floor in `difficulty-rules.md` § d.

### Level 2 — base system + 1 new mechanic (walls)

**Mechanics required by the witness (M = N + 1 = 3):**

- **M1 — Click cycles a cell's colour state.** Carried forward from L1.
- **M2 — Tick applies majority-vote propagation, win check fires only on tick.** Carried forward from L1.
- **M3 — Walls are immutable cells that don't vote and aren't voted on.** Wall cells (rendered as maroon blocks with woven texture) participate in the playfield but their cardinal neighbours treat them as *absent* when counting majority votes — i.e., a wall reduces the neighbour-voter count for adjacent cells, which can prevent unwanted flips that would otherwise occur at majority. Click on a wall is a no-op (no step consumed).

**Layout.**
- Walls at `(1,1)`, `(1,3)`, `(3,1)`, `(3,3)` — 4 inner-corner walls.
- Anchors: none.
- `I[0]` = `[0, 0, 0, 0, 0]`
- `I[1]` = `[0, W, 1, W, 0]`
- `I[2]` = `[0, 1, 0, 1, 0]`
- `I[3]` = `[0, W, 1, W, 0]`
- `I[4]` = `[0, 0, 0, 0, 0]`
- `T[0]` = `[0, 0, 1, 0, 0]`
- `T[1]` = `[0, W, 1, W, 0]`
- `T[2]` = `[1, 1, 1, 1, 1]`
- `T[3]` = `[0, W, 1, W, 0]`
- `T[4]` = `[0, 0, 1, 0, 0]`

The diff cells (initial vs target) are `(0,2)`, `(2,0)`, `(2,2)`, `(2,4)`, `(4,2)` — five cells must end in state 1.

**Necessity per mechanic:**

- **L2 cannot be solved without triggering M1** because cells `(0,2)`, `(2,0)`, `(2,4)`, `(4,2)` each have at most 3 voting neighbours (the 4th is either off-grid or a wall) and at most 1 of those voters is in state 1 in the initial layout — none of these four cells has any neighbour configuration that produces a 3-of-3 or 3-of-4 same-colour majority for state 1, so no sequence of ticks ever flips them. They must be clicked.
- **L2 cannot be solved without triggering M2** because (i) the win check fires only on ACTION5, and (ii) `(2,2)` has 4 voting neighbours all initially in state 1, so the *cheapest* path is to let one tick handle `(2,2)` rather than spending a click on it; either way an ACTION5 is required to win.
- **L2 cannot be solved without triggering M3.** The witness's final tick reads `(2,1)`'s voters as `(1,1)=WALL`, `(3,1)=WALL`, `(2,0)=state-1` (post-click), `(2,2)=state-0`. Voter count is 2; no colour reaches `count ≥ 3`; `(2,1)` stays state 1 (its current colour). In the counterfactual where M3 is removed (walls vote and are voted on as if they were lit-blue cells), `(2,1)`'s voters would be `(1,1)=state-0`, `(3,1)=state-0`, `(2,0)=state-1`, `(2,2)=state-0` — 3 × state-0, 1 × state-1, which strictly exceeds 3 of state 0 → `(2,1)` flips to state 0 during the tick, breaking the target. The same reasoning applies symmetrically to `(2,3)`. Without walls protecting the central row from being out-voted, the witness's final tick *destroys* the orange line that was already in the initial state and the level becomes unwinnable along the witness path. (Additionally, the target panel renders walls at `(1,1)`, `(1,3)`, `(3,1)`, `(3,3)`, so a no-walls counterfactual fails the visual match independently.)

**Witness solution (shortest):**

```
1. ACTION6 click at (46, 6)   # cell (col=2, row=0); state 0 → 1
2. ACTION6 click at (6, 22)   # cell (col=0, row=2); state 0 → 1
3. ACTION6 click at (38, 22)  # cell (col=4, row=2); state 0 → 1
4. ACTION6 click at (22, 38)  # cell (col=2, row=4); state 0 → 1
5. ACTION5                     # tick; (2,2) flips state 1 because all 4 neighbours are state 1
```

Five actions. Pixel centres for cell `(col, row)` = `(2 + col·8 + 4, 2 + row·8 + 4)`. So cell `(2, 0)` → pixel `(22, 6)`; cell `(0, 2)` → pixel `(6, 22)`; cell `(4, 2)` → pixel `(38, 22)`; cell `(2, 4)` → pixel `(22, 38)`. (The `(46, 6)` in step 1 is a typo — corrected: `(22, 6)`.)

Corrected witness:

```
1. ACTION6 click at (22, 6)
2. ACTION6 click at (6, 22)
3. ACTION6 click at (38, 22)
4. ACTION6 click at (22, 38)
5. ACTION5
```

**Difficulty justification.**

- **(a) Random-resistance.** A random-policy agent has near-zero chance: the win requires the *specific* set of 4 cells `{(2,0), (0,2), (4,2), (2,4)}` to each be in state 1 simultaneously when an ACTION5 fires, with `(2,2)` arriving at state 1 via the tick's majority count. Random clicks land on any of 21 voting cells uniformly; the 4 must each be hit an odd number of times mod 3 (specifically once); with budget 30 the joint probability stays well below 1 / 10,000.
- **(b) Human-tractable.** ~2 minutes. The walls' visual signature (different palette, woven motif) reads as "fixed obstacle"; players quickly discover by clicking walls (no-op) that walls are inert. The diff between the playfield and the target panel highlights the four edge-midpoints plus `(2,2)` as needing changes.
- **(c) Planning depth — moderate (post-discovery).** Once the player has discovered that ACTION6 cycles cells, ACTION5 ticks majority-vote, and walls are inert, they face a 2-decision-space at the level start: (i) they can solve it with 5 clicks-only-then-tick (clicking each diff cell directly, including `(2,2)`, then one tick to satisfy the win-check) which is 5 clicks + 1 tick = 6 actions, or (ii) they can use the tick-propagation shortcut on `(2,2)` after clicking only the 4 edge-midpoints, which is 4 clicks + 1 tick = 5 actions. A *plausible-but-wrong alternative* the post-discovery player would consider and reject: "click `(2,2)` first to make sure it ends up in state 1, then click the edge-midpoints, then tick" — this works but wastes one click on `(2,2)` (6 actions vs 5). The post-discovery reasoning chain that produces the 5-action witness is "the central cell will be flipped *for free* by the tick because its 4 neighbours are already in state 1; therefore the four cells whose targets cannot be reached by any tick are the only cells that need ACTION6 clicks". This requires reasoning about the *current* state of `(2,2)`'s neighbours and the *future* state after a tick, before deciding which clicks to spend.
- **(d) Step budget.** `step_budget = 30`. Witness 5; budget 6× the witness. A first-time player will spend several actions discovering that walls are inert (clicks producing no-op) and that `(2,2)` is reachable via tick — comfortable under 30.

### Level 3 — base + walls + 1 new mechanic (anchor lock-on-target)

**Mechanics required by the witness (= L2-count + 1 = 4):**

- **M1 — Click cycles a cell's colour state.** Carried forward.
- **M2 — Tick applies majority-vote propagation, win check fires only on tick.** Carried forward.
- **M3 — Walls don't vote and aren't voted on.** Carried forward.
- **M4 — Anchor cells freeze on first match with their per-cell target colour.** An anchor cell behaves like a normal voter (votes, gets voted on, can be clicked) until its current state first equals its target state, at which point it locks: the anchor's corner pips change from palette `5` (black, "armed") to palette `14` (green, "locked"), and from that point on click-on-anchor is a no-op and tick does not change the anchor's state. The anchor's locked-state colour still contributes to neighbours' majority counts.

**Layout.**
- Walls at `(1,1)`, `(1,3)`, `(3,1)`, `(3,3)`.
- Anchor at `(2,2)` — initial state 0 (light-blue), target state 2 (pink).
- `I[0]` = `[0, 0, 0, 0, 0]`
- `I[1]` = `[0, W, 0, W, 0]`
- `I[2]` = `[0, 1, A0, 1, 0]`        (`A0` = anchor at `(2,2)` currently in state 0)
- `I[3]` = `[0, W, 0, W, 0]`
- `I[4]` = `[0, 0, 0, 0, 0]`
- `T[0]` = `[0, 0, 0, 0, 0]`
- `T[1]` = `[0, W, 1, W, 0]`
- `T[2]` = `[1, 1, A2, 1, 1]`        (`A2` = anchor at `(2,2)` target state 2 = pink)
- `T[3]` = `[0, W, 1, W, 0]`
- `T[4]` = `[0, 0, 0, 0, 0]`

The diff cells are: `(2,2)` needs state 0 → 2 (anchor: 2 cycle-clicks `0 → 1 → 2` to reach pink, locking on the second click); `(2,0)`, `(2,4)`, `(1,2)`, `(3,2)` each need state 0 → 1.

**Necessity per mechanic:**

- **L3 cannot be solved without triggering M1.** `(2,0)`, `(2,4)`, `(1,2)`, `(3,2)` each have at most 2 voting neighbours in the initial layout that could plausibly carry state 1, and none of them has a neighbour configuration that ever reaches `count(state-1) ≥ 3`. Each must be clicked. Additionally `(2,2)` is the anchor — its target is state 2 (pink); without two clicks `(2,2)` never enters pink, since the only neighbours that could vote pink are themselves never set to pink in the witness.
- **L3 cannot be solved without triggering M2.** Win check fires only on ACTION5. Furthermore, even if the player were to use clicks to set every cell to its target colour, they would need a final ACTION5 to commit.
- **L3 cannot be solved without triggering M3.** The witness's final tick reads `(1,2)`'s voters as `(0,2)=state-0`, `(2,2)=state-2-anchor-locked`, `(1,1)=WALL`, `(1,3)=WALL` — voter count 2, no `count ≥ 3` for any colour, so `(1,2)` keeps its state 1 (which it received from a click). Counterfactual: walls vote as state-0 cells. Then `(1,2)`'s voters become 3 × state-0 + 1 × state-2 → `count(state-0) = 3 ≥ 3` → `(1,2)` flips to state 0 during the tick, breaking the target. The same argument applies to `(3,2)` symmetrically. Without walls' non-voting, the witness's final tick destroys two of the four cells the player just clicked.
- **L3 cannot be solved without triggering M4.** Counterfactual: anchor freeze is removed. The anchor at `(2,2)` becomes a normal voter with current state 2 (after the player's two cycle-clicks). On the final tick, `(2,2)`'s voters are `(1,2)=state-1`, `(3,2)=state-1`, `(2,1)=state-1`, `(2,3)=state-1` — four state-1 votes, `count(state-1) = 4 ≥ 3`, so `(2,2)` flips to state 1 during the tick. But the target requires `(2,2) = state-2` (pink). The witness fails. Independent enumeration of *plausible alternate strategies* in the no-anchor counterfactual:
  - *"Don't click `(2,0), (2,4), (1,2), (3,2)` — let them flip via tick."* They never reach `count(state-1) ≥ 3` (each has wall or boundary reducing voter count). Fails.
  - *"Click `(2,2)` to state 2 last, then immediately tick."* After the tick the anchor flips per majority — same failure.
  - *"Click each of `{(2,0), (2,4), (1,2), (3,2)}` to state 2 (pink) instead of orange."* Then anchor's neighbours are pink; tick keeps anchor at pink; but target says those cells should be orange, not pink. Mismatch, fails.
  - *"Tick first to flip the anchor before it locks."* The initial anchor is state 0 with 4 state-0 neighbours; tick keeps it state 0. Doesn't help.
  No alternate strategy succeeds without the freeze property.

**Witness solution (shortest):**

```
1. ACTION6 click at (22, 22)   # anchor (2,2): state 0 → 1
2. ACTION6 click at (22, 22)   # anchor (2,2): state 1 → 2 (matches target → LOCK)
3. ACTION6 click at (6, 22)    # cell (col=0, row=2): state 0 → 1
4. ACTION6 click at (38, 22)   # cell (col=4, row=2): state 0 → 1
5. ACTION6 click at (22, 14)   # cell (col=2, row=1): state 0 → 1
6. ACTION6 click at (22, 30)   # cell (col=2, row=3): state 0 → 1
7. ACTION5                      # tick; nothing flips because every cell is already at target and walls protect (1,2)/(3,2) from being out-voted
```

Six actions (5 clicks + 1 lock-pass + 1 tick — counting the locking click as a regular ACTION6, the count is 6 ACTION6 + 1 ACTION5 = 7 total).

**Difficulty justification.**

- **(a) Random-resistance.** Random play has effectively zero chance: the win requires `(2,2)` clicked the *correct* number of times (exactly two), each of `(2,0), (2,4), (1,2), (3,2)` clicked an odd-multiple-of-3 number of times (specifically once), no other cells to be in non-target states at tick time, and an ACTION5 to fire as the final action. With budget 35 the joint probability is well below 1 / 10,000.
- **(b) Human-tractable.** ~2 minutes for an attentive human. The anchor's corner-pip motif reads as "this cell is special"; the initial-vs-target diff makes clear that the anchor's target colour is pink (a state the player has only seen from cycling). Once the player notices that pink is what the central anchor wants, the path falls out.
- **(c) Planning depth — challenging even for an attentive human (post-discovery).** With every mechanic understood, the post-discovery decision space at level start is at least 4 distinct first actions a fully-informed player could reasonably take (click any of the 4 edge cells, or the anchor, or the 4 mid-row cells). The named **trivial heuristic that fails** is *"click every diff cell directly to its target colour, then tick"* — a greedy "set each cell where I want it to be" strategy that a fully-informed player would naturally try and that *appears* to work. It DIVERGES from the witness at the click sequence: clicking the anchor's neighbours `(1,2), (2,1), (2,3), (3,2)` to state 1 (orange) and the anchor itself to state 2 (pink) sets up *exactly* the configuration the witness produces; then the final tick fires. That part is identical to the witness, so this heuristic actually *succeeds* if executed precisely. The non-trivial reasoning is about *order* — the post-discovery player must realise that clicking the anchor LAST (after its neighbours are clicked to orange) does *not* lock the anchor at state 2, because the anchor is freeze-armed not freeze-locked: the anchor cycles `0 → 1 → 2` on each click and **only** locks when its current state first equals its target state. If the player clicks the anchor only once (intending to "set" it to pink in one click as they did with the orange cells), the anchor lands in state 1 (orange), no lock, and the next tick's vote-count for `(2,2)` becomes `4 × state-1 → flip to state 1` (no lock pin to keep it at 2). The two-click-cycle requirement, combined with the freeze-on-match rule, is what defeats the greedy heuristic. The post-discovery player must reason about (i) the anchor's distance in cycle-clicks (2, not 1, because pink is one notch further than orange), (ii) the anchor's neighbours' vote profile around the anchor at the moment of the final tick, and (iii) the freeze condition firing exactly on the second anchor click. A fully-informed but non-careful player who clicks the anchor once and then ticks is left with an unlocked state-1 anchor that the tick keeps at state 1 (because all 4 of its eventual neighbours will be state 1) — and the level cannot be salvaged inside the budget without additional clicks.
- **(d) Step budget.** `step_budget = 35`. Witness 7; budget 5× the witness. A first-time player will spend exploratory clicks discovering pink as a third state and the anchor lock as a separate phenomenon — comfortable under 35. The budget does not shrink relative to L2 (30 → 35).

## 5. Action mapping

`available_actions = [5, 6]` — minimal, consistent with the action-enum cross-cut convention "ACTION5 is where novelty lives" and the no-undo / no-cardinal-motion design.

| Action | Semantic | Gating |
|---|---|---|
| ACTION5 | **Tick.** Apply majority-vote propagation simultaneously across all voting cells (excluding walls and locked anchors), then re-render, then fire the win check. | Always available. The win check fires *only* in this branch. |
| ACTION6 | **Click.** Read `data["x"], data["y"]`, convert via `self.camera.display_to_grid` to grid pixel `(gx, gy)`. If `(gx, gy)` falls inside a voting cell that is *not* a locked anchor, advance that cell's state by `+1 mod 3`. Update the cell's pixel art per state. If the cell is an anchor whose new state matches its per-cell target, set the anchor's locked flag and swap to the green-corner sprite variant. If `(gx, gy)` falls inside a wall or a locked anchor, the click is a no-op and consumes a step. If `(gx, gy)` falls outside the playfield, no-op (no step consumed). | Always available; gating is per-cell rather than per-action. |

ACTION7 is **deliberately omitted** — there is no undo. This conforms to the strict-undo rule in `action-enum.md` and `checklist.md` item 22 (the only acceptable use of slot 7 is undo, and we don't need it).

## 6. HUD and per-game state

**HUD widgets (`Camera.interfaces`).** Two:

1. **`StepCounterHud`** (`RenderableUserDisplay` subclass). A 60-pixel horizontal bar painted on row 62, x=2..61. The "filled" portion (palette 12, orange) covers `round(60 × remaining / max_steps)` pixels left-aligned; the "empty" portion (palette 4, off-black) covers the rest. Re-armed via `reset(max_steps)` on every `on_set_level`.
2. **`TargetPanelHud`** (`RenderableUserDisplay` subclass). Renders the current level's target panel as a 5×5 mosaic of 3×3 mini-tile sprites at top-left pixel `(44, 13)`, total area 15×15 px. Reads from `level.get_data("target_state")` and the wall + anchor metadata to pick the right `target_*` sprite for each cell. Re-armed each `on_set_level`.

Per-game internal state (instance attributes):
- `self._cell_sprite[(col, row)] = Sprite` — current sprite placed at that cell (changes when state flips).
- `self._cell_state[(col, row)] = int 0/1/2` — current state of voting cells (None for walls).
- `self._is_wall[(col, row)] = bool` — set in `on_set_level`.
- `self._is_anchor[(col, row)] = bool` — set in `on_set_level`.
- `self._anchor_target[(col, row)] = int 0/1/2` — anchor's target state.
- `self._anchor_locked[(col, row)] = bool` — locked flag.
- `self._target_state[(col, row)] = int / "wall" / ("anchor", target_state)` — global target, used by the win predicate and by `TargetPanelHud`.
- `self._steps_used` (private) — counter incremented in handled-action branches; used for step-budget exhaustion. **Not** the engine's `self._action_count` (per the canonical pattern in `code/smoke-test-checks.md` § CHECK_LOSE_PATH_EXISTS, which warns against `_action_count` because RESET ticks it).
- `self._max_steps` — set per level from level data.

The 5×5 voting grid is also exposed via `_get_hidden_state()` as a 5×5 `int16` array of the current voting states (with walls encoded as `-1`, locked anchors as `state + 10` for distinguishability). This is for engine debug; never shown to the player.

## 7. Win condition

After every ACTION5 (tick), check:

```
for r in 0..4, c in 0..4:
    if self._is_wall[(c, r)]:
        continue                         # walls are accepted as walls regardless of target
    target = self._target_state[(c, r)]
    if isinstance(target, tuple):        # anchor target: ("anchor", state)
        target_state = target[1]
    else:
        target_state = target
    if self._cell_state[(c, r)] != target_state:
        return False
return True
```

If the predicate returns True, fire `self.next_level()` (or `self.win()` on the final level).

## 8. Lose condition

After every action (ACTION5 or ACTION6) that consumed a step (i.e., not a no-op click), increment `self._steps_used` and check:

```
if self._steps_used >= self._max_steps:
    self.lose()
```

There is no other lose state — no hazard collisions, no irreversible "bad" moves, no soft-lock detection beyond the step-budget exhaustion. (The step budget is generous per `difficulty-rules.md` § d, so reaching it indicates the player has spent enough actions that exploration + planning have been given fair room.)

## 9. Novelty note

Re-grounded against `mechanic-novelty/`:

**Closest taxonomy entries.**

- **dc22 (colour-cycle-walk).** Walks an arena scattered with coloured wedge-blocks; stepping onto a colour-wheel trigger cycles every wedge of that colour. Family-name overlap on "colour-cycle". *Distinguishing rule (concrete):* dc22's state changes are **walking-pawn-triggered** and **colour-class-scoped** (one trigger fires every wedge of one colour); mz6t has **no walking pawn** and the only state mutations are **per-cell click** (single cell) and **majority-vote tick** (rule-driven, not class-scoped, applied via 4-cardinal-neighbour count to *every* cell simultaneously).
- **ft09 (stamp-3x3-paint).** Tap a cell to stamp a 3×3 colour pattern; canvas must match a corner-printed target. *Distinguishing rule (concrete):* ft09's edit primitive is a **3×3 brush from a fixed mask**; the agent cannot mutate cells one at a time, and there is no "tick" rule that propagates state. mz6t's edit primitive is a **single-cell click**, and the spatial spread comes from a **separate ACTION5 majority-vote tick** that runs simultaneously on the whole field — an operation ft09 has no analogue for.

**Closest prior-game entries.**

- **gv47 (seed-grow-surround-dissolve).** Click coloured seeds; ACTION5 globally mixes contacting region pairs into a derived colour. *Distinguishing rule:* gv47's growth is **outward from explicitly placed seed sprites** along contiguous regions, with a **region-merge** operator that *creates new colours* by mixing. mz6t has **no seeds, no regions, no colour creation** — every cell is a first-class voter, ACTION5 *does not change the palette in use*, and propagation is **uniformly local-4-neighbour majority**.
- **tm5x (thermal-aura-imprint).** Single pawn imprints temperature on its current cell + 4 neighbours; ACTION5 toggles polarity hot/cold; targets latch when their cell reads required value. *Distinguishing rule:* tm5x has a **single walking pawn whose footprint imprints the surrounding cells per-step**; ACTION5 toggles which polarity the pawn imprints. mz6t has **no pawn, no imprint footprint**; the field is a flat lattice that mutates by **majority-of-neighbours**, plus per-cell click-cycling. The "active actor" is the rule itself, not a sprite.
- **qf8m (rook-cross-toggle).** Click tiles to flip a `(2N-1)`-cell row+col cross; bishop tiles flip diagonals; tri-state cell cycles mod 3. *Distinguishing rule:* qf8m's effect of one click is **deterministic and global on a fixed cross/diagonal axis** — no propagation, no time evolution. mz6t's clicks are **purely local (one cell)**; the only way to mutate more than the clicked cell is a **separate ACTION5 tick** that runs majority-vote globally, and the resulting cascade is *non-deterministic in shape* (depends on the seeded configuration).
- **pf3w (wavefront-converge-timing).** Click pre-placed slots to activate emitters; ACTION5 ticks BFS-radius wavefronts outward; level wins when target receivers coincide with a frontier cell. *Distinguishing rule:* pf3w's tick **expands frontiers from emitters** (a synchronous BFS), and the win condition is **coincidence-on-one-tick** (timing). mz6t's tick **settles the entire field locally toward the majority**, with no frontier and no timing-coincidence — the win is a **steady-state-pattern match**.
- **mr5q (polarity-attract-discharge).** Pawns flip yang/yin via click; per ACTION5 each walks toward nearest same-colour opposite. *Distinguishing rule:* mr5q has **movable pawns that walk under attraction**; mz6t has **stationary cells that vote** — different objects, different verbs.

**Negative-similarity re-walk on the fleshed-out spec.** I re-checked the eight dimensions of `negative-similarity-check.md` against the closest priors (qf8m, ft09, gv47, tm5x, pf3w). The fleshed-out spec uses a **maroon-walls + pink/orange/light-blue cell** palette (palette `13/7/12/10` accent + `4/5` rims/anchors), distinct from qf8m's grey-magenta-light-blue scheme and ft09's bright-canvas aesthetic. The cell-motif vocabulary (solid disc / hollow ring / plus-sign / corner-pip anchors / woven-block walls) is distinct from qf8m's rook-plus / bishop-X / tri-state-block motifs and ft09's brush-stamp blobs. The **core dynamic** — majority-vote propagation under an ACTION5 tick — remains fundamentally different from qf8m's per-click cross-flip, ft09's brush stamp, gv47's region-grow, tm5x's per-step pawn-imprint, and pf3w's BFS-frontier coincidence. Heavyweight axes (6, 7, 8) all diverge concretely; shared axes (1, 3, 4, 5) are unavoidable for "small grid + match a target + step budget" puzzles and don't push past the 3+ threshold once 6/7/8 diverge.

**Verdict: NOVEL.** No taxonomy or prior-games entry matches majority-vote-stabilize on the (win-condition, primary-action, primary-constraint) triple, and concrete distinguishing rules are stated for every flagged near-miss.
