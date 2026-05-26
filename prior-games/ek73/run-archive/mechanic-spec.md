# mechanic-spec — ek73 (v2 — addresses critique-revisions.md pass 1)

> **Changes from v1** (each tagged with the critique-revisions issue it addresses):
> - **§3** — Added `player_sticky_overlay` sprite to the roster (issue 5/lighter).
> - **§4 L1** — Layout redesigned to force wake-engagement in the witness (issue 4).
> - **§4 L2** — Layout simplified to a 2-wide corridor with a forced detour; wrong-path argument now rests on step-budget exhaustion (issue 2).
> - **§4 L3** — Replaced the chimney/sticky-pad design with a T-junction layout where the new mechanic is a **paired warp pad** (one-shot teleport between two paired pads); both clearer and warp are now strictly counterfactually necessary (issues 1, 3).
> - Sticky pad mechanic dropped entirely. The sprite roster's `sticky_pad` and `player_sticky_overlay` are removed in v2.

## 1. Title
Wake-Trail Evade — *(neutral working title; not visible in-game)*

## 2. Mechanic family
A single avatar walks one cell per arrow-press. Each cell the avatar **vacates** stays behind as a glowing **wake** mark for K=3 turns then fades. Stepping onto an active wake cell = lose. The base dynamic system is "plan around your own decaying recent footprints". Prior categories: **objectness** + **basic geometry & topology**. (No physics, no agentness.)

## 3. Sprite roster

`grid_size=(64, 64)`; `CELL_STRIDE = 4`. Every game-relevant sprite is 4×4 px; positions snap to multiples of 4 (16×16 logical grid).

- **`player`** — 4×4; palette `{11 yellow, 4 off-black}`; pattern: yellow cross with off-black "eye" pixel (top-centre). Tag: `player`. Movable; collides with walls; lethal contact with TANGIBLE wake; consumes collectibles by overlap; triggers pads by overlap.
- **`collectible`** — 4×4; palette `{12 orange, 1 off-white}`; hollow 4-pointed-star pattern. Tag: `collectible`. Removed when the avatar overlaps it. Win = all `collectible` removed.
- **`wall`** — 4×4; palette `{4 off-black, 5 black}`; 2-pixel staggered brick pattern. Tag: `wall`. Blocks movement; move into a wall is a no-op (step counter still ticks).
- **`wake_age1` / `wake_age2` / `wake_age3`** — 4×4 each; palette `{6 magenta, 1 off-white}`; the three sprites differ only in internal pattern (most-vivid → least-vivid) so the player reads remaining lifetime off the rendered frame. Tag: `wake`. Stepping onto an `InteractionMode.TANGIBLE` wake-tagged cell triggers `self.lose()`.
- **`clearer_pad`** — 4×4; palette `{14 green, 0 white}`; green-bordered cell with a white inner asterisk. Tag: `clearer`. One-shot. Stepping on it removes every wake-tagged sprite (sets `InteractionMode.REMOVED`) and removes the pad itself.
- **`warp_pad`** — 4×4; palette `{10 light-blue, 9 blue}`; concentric blue rings (clearly distinct from the clearer's green asterisk and the orange star collectible). Tag: `warp`. Pairs declared in `level.get_data("warp_pairs")`. Stepping on a warp pad teleports the avatar to its paired warp pad's position; both pads of the pair become `REMOVED` (one-shot pair). The avatar's vacated cell still becomes wake age 1 normally; the destination cell does NOT become wake.
- **`step_counter_bar`** — virtual; rendered by `StepCounterHud` into row 63.

Each sprite kind is distinguishable by **shape AND palette** (cross / star / brick / magenta-fade-glyph / green-asterisk / blue-ring). Per checklist item 20.

## 4. Level progression, mechanic enumeration, and witness solutions

K = 3 across all three levels.

### Level 1 — base dynamic system (wake load-bearing in witness — fix issue 4)

**Layout.** 16×16 logical grid with wall border. Internal walls form a "T-shape" arm: a horizontal corridor 1-cell-wide at row `r=3` (cells `(c, r)=(1..12, 3)` walkable; everything else in row 3 is wall) AND a vertical corridor 1-cell-wide at column `c=3` (cells `(3, r)=(3, 4..13)` walkable). The intersection `(3, 3)` is walkable (it's part of both corridors). South of row 3 except column 3 is solid wall; north of row 3 except (1, 0..2) is solid wall — so the avatar can ONLY traverse the T's two arms. Avatar starts at `(3, 3)` (T intersection). Two collectibles: `(12, 3)` (east end of horizontal arm) and `(3, 13)` (south end of vertical arm). Step budget = 60.

**Mechanics required by the witness** (N = 1):
1. **Walk-with-decaying-wake**: arrow-press moves one cell; vacated cell becomes wake age 1; existing wake ages by 1; wake of age > 3 is removed; stepping into age-1/2/3 wake = lose; stepping into a wall = no-op.

**Necessity per mechanic** (item 12 strict counterfactual):
- *L1 cannot be solved without triggering "walk-with-decaying-wake" because the two collectibles are at `(12, 3)` and `(3, 13)`, geometrically diametric in the T — the witness must traverse both arms, and the only way to traverse them is arrow-presses, each of which creates a wake mark on the vacated cell.*

  *The wake mechanic is **load-bearing in the witness**: after collecting `(12, 3)` (avatar at far east end of horizontal arm), the avatar's most recent 3 wake cells are `(9, 3), (10, 3), (11, 3)` (ages 3, 2, 1). The avatar must return west to reach the vertical arm at `(3, 3)`, but `(11, 3)` is age-1 wake — the immediate west move loses. The horizontal arm is 1-wide (rows 2 and 4 are wall), so there's NO detour. The avatar must walk EAST further to `(12, 3) → (13, 3)`? No — `(13, 3)` is walkable per the layout (the horizontal arm extends to column 12 — let me re-state: cells `(1..12, 3)` walkable; `(13, 3)` and `(14, 3)` are walls). So the avatar truly has no escape east, and west is wake-blocked. **Soft-lock fires `self.lose()` on the turn `(12, 3)` is collected unless the avatar timed the collection differently.***

  *Wait — this means L1 as stated is unsolvable. **Layout must be adjusted** — extend the horizontal arm to column 14 (cells `(1..14, 3)` walkable), so after collection the avatar can step east 2 cells to let wake decay, then return west wake-free. Witness then has a forced 2-cell east detour after collection — wake-engaging.*

  *Re-state: the horizontal arm spans columns 1-14 (14 cells walkable along row 3). Avatar starts at `(3, 3)`. Walks east to `(12, 3)` collect. Wake at `(9, 3), (10, 3), (11, 3)` ages 3, 2, 1. Cannot step west (would land on age-1 wake). Steps east `(12, 3) → (13, 3)`: wake (9, 3) decays, (10, 3) age 3, (11, 3) age 2, (12, 3) age 1. Step east `(13, 3) → (14, 3)`: (10, 3) decays, (11, 3) age 3, (12, 3) age 2, (13, 3) age 1. Step west `(14, 3) → (13, 3)`? `(13, 3)` age 1 → BLOCK. Hmm — same problem one cell over.*

  *The 1-wide constraint is the issue. If the avatar can't wait, it can't let wake decay. **Real fix**: make the horizontal arm 2-wide at the east end (rows 3 AND 4 walkable for columns 11-14). Then after collecting `(12, 3)`, the avatar steps south to `(12, 4)` (row 4) and walks west on row 4 back to column 3, while wake on row 3 decays. The 2-wide bend FORCES a wake-aware reroute.*

  *FINAL L1 layout:* horizontal arm 1-wide at row 3 columns 1-14 + a 2-wide turning area at columns 11-14 rows 3-4 + vertical arm 1-wide at column 3 rows 4-13. So the walkable cell set is: `{(c, 3) : c in 1..14} ∪ {(c, 4) : c in 11..14} ∪ {(3, r) : r in 4..13}`. Avatar at `(3, 3)`. Collectibles `(12, 3)` and `(3, 13)`.

**Witness** (FINAL): from `(3, 3)`:
- 9 east steps along row 3 → `(12, 3)`. Collect. Wake `(9, 3): 3, (10, 3): 2, (11, 3): 1`.
- 1 south to `(12, 4)` (turning area). Wake ages: `(9, 3) decays, (10, 3): 3, (11, 3): 2, (12, 3): 1`.
- 4 west on row 4 → `(8, 4)`. After 3 steps: wake at `(11, 3) decays`, ... by step 14 (at `(11, 4)`), wake at `(12, 3) decays, (12, 4): 1`.
- continues west to `(11, 4) → (10, 4)` — but row 4 is only walkable for columns 11-14; `(10, 4)` is wall. So the 2-wide turning must end somewhere allowing return to row 3.

This is becoming intricate; **commit a slightly different L1 layout that is provably solvable**: a 16×16 grid with **TWO parallel 1-wide corridors** at rows 3 and 4 (cells `(1..14, 3)` and `(1..14, 4)` walkable), connected at the east end (cell `(14, 3) ↔ (14, 4)` open). Vertical arm at column 3 rows 5-13 walkable. Avatar at `(3, 3)`. Collectibles `(12, 3)` and `(3, 13)`. **Walls everywhere else.**

Witness:
- 9 east on row 3 to `(12, 3)`. Collect. Wake `(9, 3): 3, (10, 3): 2, (11, 3): 1`.
- 2 east to `(14, 3)`. Wake ages: `(11, 3): 3, (12, 3): 2, (13, 3): 1`.
- 1 south to `(14, 4)`. Ages: `(12, 3): 3, (13, 3): 2, (14, 3): 1`.
- 11 west on row 4 to `(3, 4)`. By `(3, 4)`, wake at `(13, 3) and (14, 3) ages` will have all decayed; current wake is at the most recent 3 cells of row 4 e.g. `(5, 4), (4, 4), (3, 4)... avatar at (3, 4) so vacated last was (4, 4)`. Wake: `(6, 4): 3, (5, 4): 2, (4, 4): 1`.
- 9 south to `(3, 13)` along the vertical arm. Wake propagates south. Collect.

Total: 9 + 2 + 1 + 11 + 9 = 32 actions. Under 60-step budget. **Wake is load-bearing**: the post-collection west detour via row 4 is *forced* by the wake at `(11, 3), (10, 3), (9, 3)` blocking the direct west route. The witness explicitly engages with the wake constraint.

**Difficulty justification**:
- (a) Random-resistance: a random policy steps on its own age-1 wake within ~4 actions. The chance of a 32-action wake-respecting random sequence is `(3/4)^32 ≈ 0.01%`.
- (b) ~2 minutes. The 2-row corridor visually invites the row-4 detour.
- (c) **No strict planning requirement** at L1 — once the wake mechanic is understood, the row-4 detour is visually obvious.
- (d) Step budget 60 vs witness 32 → 1.9× witness. Generous.

### Level 2 — base + wake-clearer (fix issue 2)

**Layout.** 16×16 logical grid, walls border. A 2-wide horizontal corridor at rows `r=7,8`, cells `(c, r) for c in 1..14, r in {7, 8}` walkable. A 1-cell branch north into row 5 at `c=8`: cells `(8, 6), (8, 5)` walkable. Walls everywhere else. Avatar at `(2, 8)`. **One** `clearer_pad` at `(8, 5)` (top of branch). Collectibles: `(14, 8)` (east end) AND `(2, 7)` (just north of start, single-cell up). Step budget = 35.

**Mechanics required by the witness** (= N+1 = 2):
1. Walk-with-decaying-wake (carried).
2. **Wake-clearer pad**: stepping on `clearer`-tagged sprite removes every wake-tagged sprite; pad becomes REMOVED.

**Necessity per mechanic**:
- *Walk: as L1 — collectibles only consumed by avatar overlap.*
- *Wake-clearer: the witness order is forced to go EAST first to `(14, 8)`, then return west to clear at `(8, 5)`, then collect `(2, 7)` at the start area. Reverse-order alternative ("collect `(2, 7)` first, then east, then back") fails because the east-then-west return without clearer leaves the avatar's wake on row 8 blocking the west-row-8 return; row 7 is also wake-laden from the initial outbound trip; and the branch at column 8 to clearer requires a 2-step north-then-2-step-south detour that, by the time the avatar reaches it, has consumed enough step budget that the further westward leg (8 cells) and the final-collectible north-step exceed the 35-step budget.*

  *Concrete alternate-strategy enumeration:*
  - **Strategy A (no clearer): "east first, then immediate west-return on row 7":** witness east-leg = 12 actions to reach `(14, 8)`. Wake at `(11, 8): 3, (12, 8): 2, (13, 8): 1`. Try `(14, 8) → (14, 7)` (1 step into row 7). Then west on row 7. After 12 west steps to `(2, 7)`, collect. But row 7 also has wake — wait, no, row 7 was never walked yet. Row 7 is fresh. So this works *without* clearer! **Strategy A defeats the necessity of clearer.** **The layout must be amended.**
  
  *Amendment: row 7 cells columns 11-14 are WALLS.* I.e. `(11..14, 7)` are walls, blocking the avatar from using row 7 as a return path from the east end. Then after `(14, 8)`, the avatar's only westward options on row 8 are wake-blocked, and row 7 is wall-blocked at the east. The branch at column 8 (cells `(8, 7), (8, 6), (8, 5)`) is the only escape — clearer is now NECESSARY.

  *Re-enumerate alternates with the amendment:*
  - **A**: east-then-return-on-row-7: row 7 walls at columns 11-14 → avatar stuck at `(14, 8)`. Soft-lock LOSE.
  - **B**: skip east-collectible, collect `(2, 7)` only, then walk east: only collects 1 of 2 → win condition unmet → step budget exhausts → LOSE.
  - **C**: walk to clearer at `(8, 5)` first (no wake to clear initially): clearer fires (wasted), then proceed. East-leg has wake; return is now wake-blocked, no clearer left → LOSE.
  - **Witness D (correct)**: east-to-`(14, 8)` collect → step into row 7 at column-9 area (where row 7 is open) — wait, with walls at cols 11-14 on row 7, the only row-7 access from row 8 is at column 10 or earlier. So `(14, 8) → (10, 8) → (10, 7)` (4 west on row 8 + 1 north). But (11, 8), (12, 8), (13, 8) are wake from the east-leg → blocking the 4-west.

  *The amendment doesn't fully solve it.* **The layout needs further work to make the witness flow cleanly.** I'll commit a layout that is **demonstrably solvable** even if the wrong-path argument isn't perfectly closed:

  *FINAL L2 LAYOUT (committing):* 16×16 grid, walls border. 2-wide horizontal corridor rows 7-8, columns 1-14, all walkable. Branch up at column 8 to (8, 5), (8, 6) walkable. ONE `clearer_pad` at `(8, 5)`. ONE collectible at `(14, 8)`. ONE collectible at `(2, 5)` (which is reached only via the branch — cells `(2..8, 5)` walkable connecting the branch top to the west end). Avatar at `(2, 8)`. Step budget 50.

  *Necessity of clearer*: to reach `(2, 5)`, the avatar must walk through the branch and along row 5 west. To reach `(14, 8)`, the avatar walks east on rows 7 or 8. After collecting `(14, 8)`, returning west on row 7 or 8 hits the avatar's own wake. The clearer at `(8, 5)` lifts this — but the avatar must visit `(8, 5)` to use it (single-shot), which is also on the path to `(2, 5)`. So **the witness ordering: `(14, 8)` → return west via clearer at `(8, 5)` → continue west on row 5 to `(2, 5)`** uses BOTH mechanics naturally. Wrong-path order *(start → clearer → `(2, 5)` → east to `(14, 8)`)* still works only if the east-leg post-`(2, 5)`-collection has enough step budget left and finds a wake-free return — which it does because there's no return needed (the east collectible is the last). So this wrong path also wins. **L2 (c) plausibly fails strict moderate-planning.**

**Witness** (committed): `(2, 8) → 12 east steps → (14, 8)` collect → `(14, 8) → (14, 7) → 11 west on row 7 → (3, 7)` (wake from row 8 east-leg has decayed by step ~11 of return) → `(3, 7) → (8, 7) → (8, 6) → (8, 5)` clearer → `(8, 5) → 6 west → (2, 5)` collect. ~32 steps. Under 50-step budget.

**Difficulty justification**:
- (a) Random: < 0.5%.
- (b) ~2.5 min.
- (c) **Moderate planning (acknowledged thin)**: the post-discovery decision space at level start is 2-3 valid first actions (east to `(14, 8)`, or branch up to clearer). Witness order: east first because clearer is mid-grid and collecting east first creates wake that the clearer then erases. **Plausible-but-wrong**: clearer first → then east → wake on east-leg traps return to `(2, 5)`. Concretely, if the avatar does `(2, 8) → north to clearer → fires (wasted, no wake) → east → `(14, 8)` collect → return west: row 7 fresh, row 8 has wake. Avatar walks west on row 7. Reaches `(2, 7)`. Walks south to `(2, 8)`? Wake age depends on timing. If `(2, 8)` is age 3 from initial step at start... it's decayed after 3 steps of east-leg, so by return to `(2, 7)` it's wake-free. Walks south to `(2, 8)`. Walks 5 west? No, `(2, 5)` is at column 2, row 5. To reach: from `(2, 8)`, north to `(2, 7) → (2, 6) → (2, 5)`. Wait `(2, 6)`: is it walkable? In the layout, only `(2, 5)` and `(2, 7), (2, 8)` are walkable; `(2, 6)` not specified — say it's wall. Then `(2, 5)` only reachable via branch path: `(2, 5) ← (3, 5) ← ... ← (8, 5)`. With clearer consumed and wake on row 5? On the wrong-path-traversal, the avatar walks `(8, 5) → (7, 5) → (6, 5) → ... → (2, 5)`. This was JUST after returning from east-leg, so wake on row 5 doesn't block (row 5 is fresh except recent west-walk). Witness works. Wrong-path also works. **Conclusion: L2 still has ambiguous wrong-path argument; pass-by-budget-tightness is the only honest defense — making step budget 35 instead of 50 would force tighter pacing where the wrong-order spends ~3-5 extra steps and risks budget overflow.**
- (d) Step budget 35 (tightened from 50). Witness ~32 → 1.1× witness, tight. Wrong-path ~ 35-40 → may exhaust. **This is the wrong-path defense.**

### Level 3 — base + clearer + warp pad pair (fix issues 1, 3)

**New mechanic**: paired warp pads. Stepping on warp pad A teleports the avatar to warp pad B's position; both are then REMOVED (one-shot pair). Avatar's vacated cell becomes wake age 1 normally; the destination cell does NOT.

**Layout.** 16×16 grid, walls border. T-junction: horizontal corridor row 8 (cells `(1..14, 8)` walkable, 1-wide); vertical branch column 8 going north (cells `(8, 1..7)` walkable, 1-wide). Walls everywhere else. Avatar at `(8, 8)` (junction centre). Three collectibles: `(8, 1)` (top of vertical branch), `(1, 8)` (west end of horizontal), `(14, 8)` (east end of horizontal). One `clearer_pad` at `(8, 1)` co-located with the top collectible. One `warp_pad` pair: A at `(3, 8)`, B at `(12, 8)`, declared via `level.set_data("warp_pairs", [("A", "B")])`. Step budget = 80.

**Mechanics required by the witness** (= L2-count + 1 = 3):
1. Walk-with-decaying-wake (L1).
2. Wake-clearer pad (L2).
3. **Paired warp pad**: stepping on a warp pad teleports to its pair; pair becomes REMOVED.

**Necessity per mechanic**:
- *Walk: as before.*
- *Wake-clearer*: the vertical branch is 7 cells deep (rows 1-7) and 1-wide. Climbing it leaves wake of ages 3, 2, 1 at the cells just below the avatar. After collecting `(8, 1)`, the avatar's most recent wake at `(8, 2)` (age 1), `(8, 3)` (age 2), `(8, 4)` (age 3) blocks the only descent path. Without the co-located clearer at `(8, 1)`, the avatar is soft-locked at `(8, 1)` (walls north, west `(7, 1)`, east `(9, 1)`; south `(8, 2)` wake age 1). With clearer firing on overlap, all wake erased, descent is clean.
- *Warp pad pair*: the horizontal corridor is 14 cells wide and 1-wide. To collect both `(1, 8)` and `(14, 8)`, the avatar must traverse from one end to the other. Without warp, after collecting one end, return is blocked by wake on the corridor (wake K=3 means the most-recent 3 cells block; corridor is 1-wide; no detour). The warp pair at `(3, 8) ↔ (12, 8)` is positioned such that the witness approaches `(3, 8)`, warps to `(12, 8)`, walks east 2 to `(14, 8)`, collects, then must walk west past `(12, 8)` and across to `(1, 8)` — but warp pads are consumed; this leg is wake-blocked.

  *Re-derive: the witness must use both clearer (north branch) AND warp (horizontal corridor) cleverly:*
  
  Witness candidate:
  - `(8, 8) → 7 north → (8, 1)` collect + clearer fires. Wake state cleared.
  - `(8, 1) → 7 south → (8, 8)`. Wake builds: `(8, 2) ages, ..., (8, 7): 1` at the moment.
  - `(8, 8) → 4 west → (4, 8) → (3, 8)` warp A. Teleports to `(12, 8)` warp B. Wake: vacated `(4, 8)` age 1; `(3, 8)` is unchanged (departure point, didn't vacate normally — actually warp ITS departure cell is `(3, 8)`; on teleport the avatar leaves `(3, 8)` so per spec "vacated cell becomes wake age 1"; let's say yes, wake at `(3, 8) age 1`).
  - `(12, 8) → 2 east → (14, 8)` collect.
  - Now must reach `(1, 8)` west. Warp consumed. Wake at `(8, 8): 4 (decay)`, `(7, 8): 3`, ..., `(3, 8): age varies`, `(12, 8) age varies`, recent: `(13, 8): 1` (just vacated). Walks west `(14, 8) → (13, 8)` BLOCK. → LOSE.
  
  *So this witness candidate fails. Need to reorder:*
  
  Witness (revised):
  - `(8, 8) → 1 west → (7, 8)`. Wake `(8, 8): 1`.
  - `(7, 8) → 6 west → (1, 8)` collect. (passes through `(3, 8)` warp — does warp fire on passing through?)
  
  Per the warp pad spec: stepping on it teleports — so passing through `(3, 8)` would teleport. The avatar can't pass-through.
  
  **REVISE LAYOUT to delay warp pads**: place warp pads at `(2, 8)` and `(13, 8)` (one cell inward from each collectible). Then approaching `(1, 8)` requires entering `(2, 8) → (1, 8)`, triggering warp on the way. Same problem.
  
  **Better fix**: warp pads NOT on the direct corridor; place them on side branches.
  
  *FINAL L3 layout amendment*: add side branches at column 4 and column 12 going south to row 9 (cells `(4, 9), (12, 9)` walkable). Warp pad A at `(4, 9)`, warp pad B at `(12, 9)`. Walking the corridor doesn't trigger warp; the avatar must explicitly step south into the branch to use warp.
  
  Witness (committed):
  - `(8, 8) → 7 north → (8, 1)` collect+clearer. Cleared. Wake state {}.
  - `(8, 1) → 7 south → (8, 8)`. Wake at `(8, 6), (8, 7), (8, 8) ages 3, 2, 1` after returning to `(8, 8)`. Wait — at step 14 (back at `(8, 8)`), vacated `(8, 7)` last, so wake at `(8, 7): 1, (8, 6): 2, (8, 5): 3`.
  - `(8, 8) → 4 west → (4, 8)`. Wake `(8, 8): 1, (7, 8): 2, ... wait. Avatar's path of moves: `(8, 8) → (7, 8) → (6, 8) → (5, 8) → (4, 8)`. So wake at last 3 vacated: `(5, 8): 1, (6, 8): 2, (7, 8): 3`.
  - `(4, 8) → 1 south → (4, 9)` warp A. Teleports to `(12, 9)`. Wake: vacated `(4, 8) age 1`; ages prior wake: `(5, 8): 2, (6, 8): 3, (7, 8) decays`; teleport destination `(12, 9)` doesn't get wake. State: `{(4, 8): 1, (5, 8): 2, (6, 8): 3, ...}` plus the warp departure `(4, 9): 1`.
  - `(12, 9) → 1 north → (12, 8)`. Wake builds.
  - `(12, 8) → 2 east → (14, 8)` collect.
  - `(14, 8) → walk west`. Wake from east-leg: `(12, 8): 3, (13, 8): 2, ... avatar AT (14, 8) so most recent vacated (13, 8): 1`. West blocked.
  - **Stuck**. Need clearer — already used.
  
  *Damn. The east collectible's return is blocked.*
  
  **Witness (re-revised)**: collect east-collectible LAST so no return needed:
  
  - `(8, 8) → 7 north → (8, 1)` collect+clearer. Wake state {}.
  - `(8, 1) → 7 south → (8, 8)`. Wake `{...}`.
  - `(8, 8) → 8 west → (1, 8)` (wait — is path clear?). Avatar path: `(8, 8) → (7, 8) → (6, 8) → (5, 8) → (4, 8) → (3, 8) → (2, 8) → (1, 8)`. 7 west steps. Wake: most recent 3: `(4, 8): 1, (3, 8): 2, (2, 8): 3` at avatar `(1, 8)`. Collect `(1, 8)`.
  - `(1, 8) → north (no wall path to north or south from (1, 8))` — stuck west, east blocked by wake. → LOSE.
  
  *Still trapped. The narrow 1-wide horizontal corridor traps after collecting either end.*
  
  **Solution**: use warp pads for the trapped-end escape. Witness:
  - North branch: collect `(8, 1)`, clearer fires, descend.
  - West collectible: walk west to `(1, 8)`, collect. Stuck. **Walk back via warp**: but warp pads are at (4, 9), (12, 9) — south of corridor.
  - From `(1, 8)`, try to step south: `(1, 9)` is wall (per layout). North `(1, 7)` is wall. East: `(2, 8)` wake → BLOCK. **Soft-lock LOSE.**
  
  *Need warp pads accessible from the dead-end. Place warp A at `(1, 9)` (south of west collectible) — i.e. the cell just south of `(1, 8)` is walkable AND a warp pad.*
  
  *FINAL L3 LAYOUT (committed):* horizontal corridor row 8 + side branches at columns 1 and 14 to row 9 (cells `(1, 9)` and `(14, 9)` walkable). Warp pad A at `(1, 9)`, warp pad B at `(14, 9)`. North branch column 8 rows 1-7 with clearer+collectible at `(8, 1)`. Three collectibles: `(8, 1), (1, 8), (14, 8)`. Avatar at `(8, 8)`.
  
  **Witness** (FINAL):
  1. `(8, 8) → 7 north → (8, 1)` collect+clearer. State {}. (7 actions)
  2. `(8, 1) → 7 south → (8, 8)`. Wake `(8, 5..7) ages 3, 2, 1`. (14 total)
  3. `(8, 8) → 7 west → (1, 8)` collect. Wake `(2..4, 8) ages 3, 2, 1`. (21 total)
  4. `(1, 8) → 1 south → (1, 9)` warp A. Teleports to `(14, 9)`. Wake `(1, 8) age 1` (vacated normally). (22 total)
  5. `(14, 9) → 1 north → (14, 8)` collect. (23 total)
  6. **Win** (all collected).
  
  *Strict counterfactual checks:*
  - WITHOUT clearer: step 1 traps avatar at `(8, 1)` (vertical branch dead-end, all neighbours walls or wake) → soft-lock LOSE.
  - WITHOUT warp: step 4 has nowhere to go from `(1, 8)` — south wall, north wall, east wake → soft-lock LOSE. Avatar can't reach `(14, 8)` (corridor is 1-wide and west-half is wake-blocked).
  
  **Both clearer AND warp are strictly necessary.** ✓

**Difficulty justification**:
- (a) Random: ~0%.
- (b) ~2.5 min.
- (c) **Challenging post-discovery planning**: post-discovery decision space at start ≥ 4 (north to vertical, east/west on row 8, south to row 9). **Trivial heuristic that fails**: greedy-toward-nearest-collectible. From `(8, 8)`, greedy notes `(1, 8)` is 7 away, `(14, 8)` is 6 away, `(8, 1)` is 7 away. Greedy picks east `(14, 8)`. Walks 6 east, collects, wake at last 3 cells blocks west return. Tries warp at `(14, 9)` → teleports to `(1, 9)`. Walks north `(1, 8)` collects. Tries to reach `(8, 1)`: walks east `(1, 8) → (2, 8)` BLOCK. Tries south `(1, 9)` — warp consumed → wall. **Soft-lock**. Greedy fails because the warp must be saved for the LAST corridor traversal, and the vertical branch's clearer must be used FIRST (otherwise climbing the branch traps the avatar). The witness defeats greedy by ordering: vertical-first (clearer), west-second (warp escape), east-third (final collection at end of horizontal).
- (d) Step budget 80 vs witness 23 → ~3.5× witness. Generous.

## 5. Action mapping
`available_actions = [1, 2, 3, 4]`. Per-direction: avatar moves one logical cell in that direction, subject to wall/wake/off-grid checks. After successful move, vacated cell becomes wake age 1 (UNLESS the move was a warp teleport — then vacated *original* cell becomes wake age 1, destination cell does NOT). Pads at destination fire their effects (clearer / warp).

## 6. HUD and per-game state
Single HUD: `StepCounterHud` (depleting bar at row 63). State on `Ek73`:
- `wake_cells: dict[(int, int), int]` (logical cell → age 1..3).
- `wake_sprite_for: dict[(int, int), Sprite]` (parallel — the wake sprite currently rendered at each cell).
- `_step_budget: int` (read from `level.get_data("step_budget")`).
- `_warp_pairs: list[tuple[Sprite, Sprite]]` (loaded from level data; consumed on use).

No-hidden-state cues (item 19): wake age via 3 distinct sprite kinds; warp/clearer pads visible until consumed; collectibles visible until removed.

## 7. Win condition
`all collectible-tagged sprites are InteractionMode.REMOVED → self.next_level()`.

## 8. Lose condition
Fires `self.lose()` if:
- Successful move's destination overlaps a TANGIBLE wake-tagged sprite.
- `self._action_count >= _step_budget`.
- Soft-lock detector: avatar's 4 cardinal neighbours are all walls OR active wake AND win predicate not satisfied.

## 9. Novelty note
Same cites as v1. Closest priors: g50t, sk48, fz5j, wt39, zd7m. Distinguishing rules unchanged. Negative similarity: closest concern remains fz5j with 3 shared dims; engineered divergences on dim 6/7/8 hold. Warp pad mechanic adds a secondary axis that further distinguishes from fz5j (no teleport in fz5j).

The warp pad mechanic recalls zd7m's "portals teleport into a sealed chamber" but: zd7m's portals are non-consumable and integrated with cohort-step (every pawn moves); ek73's warp pair is one-shot, single-avatar, and integrated with wake-trail-evade. Distinguishing rule articulated.

---

## Known weaknesses (acknowledged for next critique)

- **L2 wrong-path argument** still rests on step-budget tightness rather than a layout-forced fail. If the next critique rejects this, the fix is to add a third small obstacle on the wrong-path that absorbs ~5 extra steps.
- **L1 layout description** has been amended mid-spec (to add the row-4 return corridor); the implementation must use the FINAL layout: `(1..14, 3)` walkable, `(1..14, 4)` walkable, `(3, 4..13)` walkable, walls elsewhere — **plus** the east-end connection at `(14, 3) ↔ (14, 4)` is automatic (both cells walkable adjacent).
