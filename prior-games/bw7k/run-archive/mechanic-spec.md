# bw7k spec

## 1. Title
Ghost-Playback (working title; not visible in-game)

## 2. Mechanic family
`actor-replay-shade` — drawn from **objectness** (the actor and
shade pawns are persistent entities that move and collide),
**basic geometry / topology** (the shade's replay path is a
geometric translation of the actor's pre-anchor path; walls can
be inside or outside the replay region with topological effect),
and **agentness** (shades behave with apparent intent — they walk
autonomously per a tape recorded by the player's recent
trajectory).

## 3. Sprite roster

The grid is 64×64 with a 4-pixel stride: every game-relevant
sprite is 4×4 pixels. The logical board is 16 cells × 16 cells.

- **`actor`** — 4×4. pixels:
  ```
  [[10, 9, 9, 10],
   [9, 5, 5, 9],
   [9, 5, 5, 9],
   [10, 9, 9, 10]]
  ```
  palette: `{5, 9, 10}`. tags: `["actor"]`. role: the
  player-controlled pawn. Solid-bordered look reads as movable.

- **`actor_goal`** — 4×4. pixels:
  ```
  [[9, 9, 9, 9],
   [9, -1, -1, 9],
   [9, -1, -1, 9],
   [9, 9, 9, 9]]
  ```
  palette: `{9}` + transparent. tags: `["actor_goal"]`. role:
  the cell where the actor must end. Hollow-ring silhouette
  reads as "destination frame" (distinguishable from the solid-
  bordered actor by the transparent middle).

- **`shade_red`** — 4×4. pixels:
  ```
  [[12, 8, 8, 12],
   [8, 5, 5, 8],
   [8, 5, 5, 8],
   [12, 8, 8, 12]]
  ```
  palette: `{5, 8, 12}`. tags: `["shade", "shade_red"]`. role:
  the autonomous companion spawned at `anchor_red`; replays the
  actor's recorded move-tape one entry per game tick.

- **`shade_yellow`** — 4×4 (level 3). pixels:
  ```
  [[14, 11, 11, 14],
   [11, 5, 5, 11],
   [11, 5, 5, 11],
   [14, 11, 11, 14]]
  ```
  palette: `{5, 11, 14}`. tags: `["shade", "shade_yellow"]`.
  role: same as `shade_red` but for the yellow anchor.

- **`target_red`** — 4×4. pixels:
  ```
  [[8, 8, 8, 8],
   [8, -1, -1, 8],
   [8, -1, -1, 8],
   [8, 8, 8, 8]]
  ```
  palette: `{8}` + transparent. tags: `["target", "target_red"]`.
  role: cell where `shade_red` must end. Hollow-ring silhouette
  parallels `actor_goal`; same shape, distinct palette
  (red vs cyan-blue) signals same role in different colour.

- **`target_yellow`** — 4×4 (level 3). pixels:
  ```
  [[11, 11, 11, 11],
   [11, -1, -1, 11],
   [11, -1, -1, 11],
   [11, 11, 11, 11]]
  ```
  palette: `{11}` + transparent. tags: `["target", "target_yellow"]`.
  role: cell where `shade_yellow` must end.

- **`anchor_red`** — 4×4. pixels:
  ```
  [[8, -1, -1, 8],
   [-1, 12, 12, -1],
   [-1, 12, 12, -1],
   [8, -1, -1, 8]]
  ```
  palette: `{8, 12}` + transparent. tags: `["anchor", "anchor_red"]`.
  role: walking-actor onto this cell triggers a one-time spawn of
  `shade_red`; corner-dot silhouette is distinct from the solid-
  border actor and the hollow-ring target — reads as a
  "stamp pad" or "rune".

- **`anchor_yellow`** — 4×4 (level 3). pixels:
  ```
  [[11, -1, -1, 11],
   [-1, 14, 14, -1],
   [-1, 14, 14, -1],
   [11, -1, -1, 11]]
  ```
  palette: `{11, 14}` + transparent. tags:
  `["anchor", "anchor_yellow"]`. role: same as `anchor_red` for
  the yellow shade.

- **`wall`** — 4×4. pixels:
  ```
  [[3, 3, 3, 3],
   [3, 4, 4, 3],
   [3, 4, 4, 3],
   [3, 3, 3, 3]]
  ```
  palette: `{3, 4}`. tags: `["wall"]`. role: blocks both the
  actor's walk and a shade's replay step at this cell. Solid
  filled grey reads as masonry.

The palette across the roster (excluding the HUD) uses `{3, 4,
5, 8, 9, 10, 11, 12, 14}` — 9 distinct values, none from a
narrow `{4-wall, 8-red, 9-blue}` palette family that would echo
the `kf42 → vh68` cautionary example. The actor's blue-cyan
family (9, 10) is differentiated from the shades' warm families
(red 8 + orange 12; yellow 11 + green 14). The actor and shades
share a 5×5-style construction for visual sibling-recognition
("solid-bordered glyph = movable pawn") while the targets share
the hollow-ring silhouette ("hollow-ring = destination") and the
anchors share the corner-dot silhouette ("dotted pad = trigger").
This is a deliberate visual grouping that lets the player infer
role from silhouette and colour from palette — checklist item 21
("sprite UI ≈ sprite role" and "identical visuals imply
correlated roles") is honoured by giving each role its own
silhouette family.


## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 3):
  1. **Walking.** Arrow keys ACTION1/2/3/4 move the actor 4
     pixels in the corresponding cardinal direction, blocked
     only by wall sprites and grid bounds.
  2. **Anchor-spawn-shade.** The first time the actor's post-
     move position lands on an `anchor`-tagged cell, a same-
     colour shade pawn is spawned at that anchor's grid cell,
     and the anchor sprite is consumed (set to
     `InteractionMode.REMOVED`). Subsequent walks over the
     anchor-cell do NOT spawn additional shades.
  3. **Shade-replays-tape.** Immediately on spawn (within the
     same `step()` call that triggered the anchor), the shade
     walks its frozen move-tape snapshot `T[0..snapshot_len-1]`
     in order, one tape entry at a time. Each entry tries to
     translate the shade by `T[i]`. A blocked move (wall or
     grid-bound) is **skipped** — the shade stays in place for
     that entry, the iteration moves to `T[i+1]`. After all
     entries are processed the shade's final cell is its
     resting position for the rest of the level; subsequent
     actor moves do not move this shade.

- **Necessity per mechanic** (counterfactual):
  - *Walking*: the actor's start cell `(12, 56)` differs from
    its goal `(12, 4)`; without ACTION1-4 there is no other
    way to displace the actor, and `_get_valid_actions` only
    returns ACTION1-4. **Necessary.**
  - *Anchor-spawn-shade*: if the actor never lands on
    `anchor_red` at `(12, 36)`, no shade spawns; the win
    predicate requires every shade-target to have a same-
    coloured shade on it, and `target_red` at `(12, 16)` has
    no shade until `anchor_red` is triggered, so the level is
    unwinnable without the trigger. **Necessary.**
  - *Shade-replays-tape*: even after the shade spawns at the
    anchor cell `(12, 36)`, it must reach `target_red` at
    `(12, 16)` — a 5-step UP displacement away. Only the
    replay mechanic can move the shade; there is no other
    means in L1 (no ACTION6 click, no manual shade control).
    **Necessary.**

- **Witness solution**:
  `[ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION1]`
  (13 × ACTION1 — the actor walks UP×13 from `(12, 56)` to
  `(12, 4)`. At action 5 the actor lands at `(12, 36)` =
  `anchor_red`; `shade_red` is spawned at that cell and
  immediately walks its 5-entry tape `[UP×5]` in the same
  step, ending at `(12, 16)` = `target_red`. Actions 6-13
  continue the actor up to `(12, 4)` = `actor_goal` while
  `shade_red` stays frozen on `target_red`. Win predicate
  satisfied at action 13.)

- **Difficulty justification**:
  - *(a) Random-resistance*: a vision-blind random agent has
    `(1/4)^13 ≈ 1.5e-8` of producing `[UP×13]` in 13 actions,
    and even within a 30-step budget the cumulative
    probability of any all-UP prefix passing through
    `(12, 36)` and ending at `(12, 4)` remains below `1e-5`.
    Rejected.
  - *(b) Human-tractable*: <1 minute. An attentive player
    sees a single column of cells from start to anchor to
    actor-goal; the visual layout is a vertical line. After
    one or two exploratory presses they will press UP
    repeatedly. The shade's spawn and replay are observed
    live as the actor walks past the anchor.
  - *(c) Planning depth*: **no strict planning requirement**.
    Once the player has seen the actor walk and the shade
    spawn, the goal is geometrically obvious — keep walking
    UP until everyone is on a target. Mechanic-discovery
    is the entire difficulty.
  - *(d) Step budget*: 30 actions per level data
    `{"step_budget": 30}`. Generous over the 13-action
    witness; allows ~17 actions of exploration / wrong-key
    recovery. Not shrinking across levels.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (N+1 = 4):
  1. **Walking** (carried from L1).
  2. **Anchor-spawn-shade** (carried from L1).
  3. **Shade-replays-tape** (carried from L1).
  4. **Replay-walls** (NEW). Walls placed inside the shade's
     replay region cause shade-steps that would land on a wall
     to be **skipped** (per the L1 skip-rule, but now wall-
     placement makes the skip *load-bearing for solving*).
     Path-shape from start-to-anchor matters because the shade
     replays that exact sequence; a wall anywhere in that
     replayed sequence aborts the corresponding step.

  Single new mechanic, +1 promotion. (Not zero, not two-or-more.)

- **Layout summary** (placed sprites; `step_budget = 50`):
  - `actor` start `(16, 56)`. `actor_goal` `(16, 4)`.
  - `anchor_red` `(16, 32)`. `target_red` `(40, 8)`.
  - **Replay-wall block** at `(36, 8)` — a single `wall`
    sprite. (One `wall` sprite is enough — the next-RIGHT cell
    from `target_red` is occupied by the wall, so any LEFT
    step from `(40, 8)` is blocked.)
  - Two **outer-frame** `wall` rows along the top (`y=0`) and
    bottom (`y=60`) edges, plus stub walls at `(0, *)` and
    `(60, *)` columns to enforce the boundary. Specifically:
    `wall` at every `(x, 0)` for `x in {0, 4, 8, ..., 60}`,
    same at `y=60`, same at `x=0` for `y in {0..60}`, same at
    `x=60`. (16 walls per side × 4 sides − 4 corner double-
    counts = 60 wall sprites for the frame.)

- **Required pre-anchor net displacement**: `anchor - start =
  (16-16, 32-56) = (0, -24)`. Pre-anchor witness path must
  total (0, -24) in net displacement.
- **Required shade replay endpoint**: `target_red - anchor_red
  = (40-16, 8-32) = (+24, -24)`. So the replay sequence must
  end at the target — the replay-net is `(+24, -24)`, a 6-cell
  delta versus the pre-anchor net of `(0, -24)`. The (+24, 0)
  difference must come from skipped LEFT steps in the replay,
  caused by the wall at `(36, 8)` blocking LEFT-from-`(40, 8)`.

- **Necessity per mechanic** (counterfactual, per item 12):
  - *Walking*: actor must displace `(0, -24)` then `(0, -28)`
    over the level (start to actor_goal). Without ACTION1-4
    no displacement happens. **Necessary.**
  - *Anchor-spawn-shade*: `target_red` is empty until the
    actor lands on `anchor_red` at `(16, 32)`. No shade →
    win predicate fails. **Necessary.**
  - *Shade-replays-tape*: even after spawning,
    `shade_red` must move from `(16, 32)` to `(40, 8)` — a
    `(+24, -24)` displacement. Only the tape-replay produces
    shade motion. **Necessary.**
  - *Replay-walls*: the shade's tape must end its replay at
    `(40, 8)`. Without the wall at `(36, 8)`, the shade's
    replay of `T[0..N-1]` would carry it past `(40, 8)` and
    leave it at the natural endpoint `2*anchor - start =
    (16, 8)` (because the pre-anchor net is `(0, -24)` and
    the replay applies the same vectors from anchor). The
    only way to make the shade end at `(40, 8)` is to walk a
    pre-anchor path that reaches `(40, ?)` mid-replay AND
    have a wall block any subsequent LEFT step from there;
    the wall at `(36, 8)` is the load-bearing piece. Without
    `replay-walls`, no path satisfies the `target_red`
    constraint. **Necessary.**

- **Witness solution** (action sequence, 25 actions):
  `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
    ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION3, ACTION3, ACTION3, ACTION3, ACTION3, ACTION3,
    ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION1]`
  (RIGHT×6 then UP×6 then LEFT×6 then UP×7 — the actor walks
  RIGHT×6 to `(40, 56)`, UP×6 to `(40, 32)`, LEFT×6 back to
  `(16, 32)` = `anchor_red`. On action 18 `shade_red` is
  spawned with `snapshot_len = 18` and tape
  `[RIGHT×6, UP×6, LEFT×6]`; in the same step it walks the
  tape: RIGHT×6 → `(40, 32)`, UP×6 → `(40, 8)` =
  `target_red`, then LEFT×6 → all six blocked by the wall at
  `(36, 8)`, so the shade rests at `(40, 8)`. Actions 19-25
  walk the actor UP×7 to `(16, 4)` = `actor_goal`. Win
  predicate satisfied at action 25.)

- **Difficulty justification**:
  - *(a) Random-resistance*: a 50-step random run with 4
    actions has probability `~0` of producing the specific
    25-step sequence above; even any path-shape that
    delivers `shade_red` to `(40, 8)` requires going through
    `(40, 8)` mid-replay AND ending the pre-anchor walk at
    `(16, 32)`. A random-policy / vision-blind / small-LLM
    agent cannot solve L2 within 50 steps.
  - *(b) Human-tractable*: ~2 minutes. After the L1
    discovery the player understands the replay rule. In L2
    they observe `target_red` at `(40, 8)` is to the right
    and away from the actor's straight-up path, and the
    wall at `(36, 8)` is visible. They reason: "to get the
    shade to land at `(40, 8)` I need the shade to go RIGHT
    first when replayed from `(16, 32)`; therefore my pre-
    anchor walk should start with a RIGHT excursion." A
    couple of trials plus the wall's visible-as-block
    affordance gets the player there.
  - *(c) Planning depth (post-discovery)*: **moderate
    planning required**. The post-discovery decision space
    at `(16, 56)` is the four arrow keys; 3 of those (UP,
    DOWN, LEFT) are wrong first moves (UP gives the trivial
    path `target_red = (16, 8)`, DOWN walks into the bottom
    wall, LEFT walks toward `(12, 56)` and nowhere useful);
    only RIGHT first moves on a path that, when
    replayed, can plausibly reach `(40, 8)` via skip-LEFTs.
    A plausible-but-wrong alternative the post-discovery
    player would consider: "walk UP first, then RIGHT after
    spawn." But after spawn the actor's RIGHTs DO NOT get
    appended to the shade's snapshot (snapshot is frozen at
    spawn), so the shade only replays UPs and ends at
    `(16, 8)`. The player must reason: shade moves come
    from PRE-spawn moves only. Witness reasoning chain: the
    `(+24, 0)` x-displacement the shade needs must come
    from RIGHT moves recorded BEFORE the anchor; therefore
    those RIGHTs must be in the pre-anchor path. The only
    way to pre-anchor net (0, -24) while including 6 RIGHTs
    is to also include 6 LEFTs (or another net-0 x-walk);
    the LEFTs at the END of the path are the ones that get
    skipped during replay (because the wall at `(36, 8)`
    blocks LEFT-from-`(40, 8)` after the shade has already
    UP-displaced to `(40, 8)`).
  - *(d) Step budget*: 50 actions per level data
    `{"step_budget": 50}`. Generous over the 25-action
    witness; ~25 actions of exploration / wrong-key
    recovery. Larger than L1's 30 (the budget does not
    shrink across levels).

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (= L2-count + 1 = 5):
  1. **Walking** (carried).
  2. **Anchor-spawn-shade** (carried; now polymorphic over
     two anchor colours, but the spawn rule itself is the
     same one from L1).
  3. **Shade-replays-tape** (carried; each spawned shade
     replays the actor's tape-up-to-its-spawn-tick).
  4. **Replay-walls** (carried from L2 — walls inside the
     replay region cause skips for the affected shade).
     Load-bearing in the L3 witness via `shade_yellow`'s
     replay (8 RIGHT-skips against an interior wall).
  5. **Multi-shade simultaneity** (NEW). Two anchor-target
     colour pairs are present (red, yellow). Each anchor
     spawns its own shade with its own tape snapshot at its
     own spawn tick, and each shade carries its own snapshot
     length. *Both* shade-targets must be simultaneously
     occupied at the same tick the actor stands on
     `actor_goal`. The two shades' replay-tapes share a
     common prefix (whichever shade was spawned first has a
     strict prefix of the shade spawned second), so the
     player's path-shape is doubly constrained — a shape
     that lands `shade_red` at `target_red` must ALSO not
     derail `shade_yellow`'s replay. This is qualitatively
     different from "more red anchors" (which would be a
     single-mechanic content scaling rejected by §3.4): the
     player reasons over a two-target replay-trajectory
     simultaneity from a single shared tape, not a single
     larger one.

  Single new mechanic, +1 promotion.

- **Layout summary** (placed sprites; `step_budget = 60`):
  - `actor` start `(8, 60)`.
  - `anchor_red` `(8, 36)`. `target_red` `(8, 12)` —
    `2*anchor_red - actor_start = (8, 12)`, the natural
    endpoint of `shade_red`'s replay.
  - `anchor_yellow` `(40, 36)`. `target_yellow` `(40, 12)`
    — NOT the natural endpoint of `shade_yellow`'s replay;
    requires interior-wall skips to land here.
  - `actor_goal` `(24, 4)`.
  - **Detour wall** at `(24, 36)` — interior wall on row
    y=36 between the two anchors. Forces the actor's
    between-anchors path to detour around it (via row y=40
    or row y=32), inserting non-RIGHT moves into the tape
    snapshot for `shade_yellow`.
  - **Replay-wall** at `(44, 16)` — interior wall on row
    y=16 just east of the column x=40. Blocks
    RIGHT-from-`(40, 16)` for `shade_yellow` during replay.
  - Outer-frame walls along the four edges (same as L2).

- **Required pre-red-anchor net displacement**: `anchor_red
  - actor_start = (0, -24)`. 6 UPs.
- **Required between-red-and-yellow net displacement**:
  `anchor_yellow - anchor_red = (+32, 0)` (8 RIGHTs net),
  but with the detour wall at `(24, 36)` blocking the
  straight RIGHT path along y=36, the actor must go around
  via DOWN×1, RIGHT×8, UP×1 (or via UP×1, RIGHT×8, DOWN×1).
  Either detour adds 2 extra moves (one DOWN-or-UP + one
  return UP-or-DOWN) for a total of 10 moves between
  anchors.
- **`shade_red` snapshot at red-spawn**: 6 entries (UP×6).
  Replay from `(8, 36)`: UP×6 → `(8, 12)` = `target_red`. ✓
  No walls in `(8, 32)..(8, 12)` corridor.
- **`shade_yellow` snapshot at yellow-spawn**: 6 + 10 = 16
  entries (UP×6, DOWN×1, RIGHT×8, UP×1). Replay from
  `(40, 36)`:
  - UP×6: `(40, 36) → (40, 32) → (40, 28) → (40, 24) →
    (40, 20) → (40, 16) → (40, 12)`. Pointer = 6.
  - DOWN×1: `(40, 12) → (40, 16)`. Pointer = 7.
  - RIGHT×8: at `(40, 16)` try RIGHT to `(44, 16)` — wall →
    blocked → skip. All 8 RIGHTs blocked → all skipped.
    Stays at `(40, 16)`. Pointer = 15.
  - UP×1: `(40, 16) → (40, 12)` = `target_yellow`. ✓
    Pointer = 16 = snapshot_len. Exhausted.

- **Necessity per mechanic** (counterfactual, one line per
  mechanic, citing concrete blockers):
  - *Walking*: actor displacement from `(8, 60)` to
    `actor_goal` `(24, 4)` is `(+16, -56)`; without
    ACTION1-4 no displacement happens, and
    `_get_valid_actions` returns nothing else.
    **Necessary.**
  - *Anchor-spawn-shade*: `target_red` and `target_yellow`
    are empty until the actor lands on each anchor; the win
    predicate requires both to be filled by same-coloured
    shades, so both anchors must be triggered.
    **Necessary** (verified by alternate enumeration below
    — the trivial fallback "skip both anchors and walk to
    actor_goal" fails the win predicate).
  - *Shade-replays-tape*: each spawned shade must displace
    from its anchor cell to its target cell (`(8, 36) →
    (8, 12)` = `(0, -24)` for red; `(40, 36) → (40, 12)` =
    `(0, -24)` for yellow). Only tape-replay produces shade
    motion; there is no manual shade control.
    **Necessary** for both shades.
  - *Replay-walls*: `shade_yellow`'s natural endpoint
    (without any wall-skip during replay) is `2 *
    anchor_yellow - actor_start = (72, 12)` — but the grid
    is 64 cells wide, so without the interior wall at
    `(44, 16)` the shade would walk through the column
    x=40..60 along y=12 region with no skip and end up at
    the right boundary at `(60, ?)`. To re-direct
    `shade_yellow` to `(40, 12)`, the witness's tape MUST
    include `[..., DOWN×1, RIGHT×8, UP×1]` at the tail; the
    wall at `(44, 16)` MUST then skip the 8 RIGHTs (which
    would otherwise carry the shade to `(60, 16)`, leaving
    the trailing UP to land it at `(60, 12)` ≠
    `target_yellow`). Without the wall at `(44, 16)`, no
    path-shape (within the step budget) can land
    `shade_yellow` at `(40, 12)`. **Necessary** for the L3
    witness.
  - *Multi-shade simultaneity*: the win predicate requires
    BOTH `target_red` AND `target_yellow` to be occupied at
    the same tick the actor is on `actor_goal`. Without the
    multi-shade rule (i.e. with only one anchor-target
    pair), L3 reduces to L2-style geometry — but L3 has TWO
    anchor-target pairs and the witness path must satisfy
    both replay-trajectories simultaneously from a single
    shared tape with two different snapshot lengths.
    **Necessary** by win-predicate construction.

- **Per-mechanic enumeration of plausible alternates** (per
  checklist 12 — verify by enumeration, not abstraction):
  Alternates a fully-informed player might try, and why each
  fails:
  1. *"Walk straight UP from `(8, 60)` along x=8 to actor_goal,
      ignoring both anchors."* — actor reaches `(8, 4)`, not
      `(24, 4)` = `actor_goal`. Even if the actor then walks
      RIGHT×4 to `(24, 4)`, no anchors triggered → both
      shade-targets empty → win predicate fails.
  2. *"Walk through anchor_red only, then to actor_goal,
      ignoring anchor_yellow."* — `target_yellow` stays
      empty → win predicate fails.
  3. *"Walk through both anchors with a STRAIGHT between-
      anchors path along y=36."* — the detour wall at
      `(24, 36)` blocks the actor's RIGHT-step at
      `(20, 36)`. Actor's straight RIGHT path is blocked
      mid-way; player must detour. (If the player ignores
      this and submits a sequence with a blocked RIGHT, the
      attempted move is recorded in the tape but the actor
      doesn't move; the player wastes a step but the path
      eventually still must detour.)
  4. *"Walk yellow-first via RIGHT×8 (ignoring detour wall)
      then UP×6."* — The detour wall at `(24, 36)` is on
      row y=36, but the actor starts at row y=60. Walking
      RIGHT×8 from `(8, 60)` lands at `(40, 60)` (row y=60,
      no detour wall hit). Then UP×6 to `(40, 36)` =
      anchor_yellow. Snapshot_yellow = 14 entries
      `[RIGHT×8, UP×6]`. Replay from `(40, 36)`: RIGHT×8 →
      tries `(44, 36)`, `(48, 36)`, `(52, 36)`, `(56, 36)`,
      `(60, 36)` — but `(60, 36)` is the right outer-frame
      wall. So RIGHT×4 successful to `(56, 36)`, then 4
      blocked. Actually wait the outer frame is at x=60+,
      so `(60, 36)` may be wall. Let me say `(60, *)` is
      the right boundary wall. So 4 RIGHTs successful to
      `(56, 36)`, then 4 blocked. Then UP×6: from `(56, 36)`
      to `(56, 32)`, `(56, 28)`, `(56, 24)`, `(56, 20)`,
      `(56, 16)`, `(56, 12)`. Shade_yellow ends at `(56, 12)`
      ≠ `(40, 12)` = `target_yellow`. Fails.
  5. *"Walk through anchor_yellow first, then back to
      anchor_red, then to actor_goal."* — possible alternate
      witness. From `(8, 60)`: RIGHT×8 to `(40, 60)`, UP×6
      to `(40, 36)` = anchor_yellow. snapshot_yellow = 14.
      Replay from `(40, 36)`: per alternate 4 above, ends
      at `(56, 12)` ≠ target. Fails.
  6. *"Walk through both anchors with the detour-around-
      wall layout, but pick the UP detour (UP, RIGHT×8,
      DOWN) instead of the DOWN detour."* — actor at
      `(8, 36)` goes UP×1 to `(8, 32)`, RIGHT×8 to
      `(40, 32)`, DOWN×1 to `(40, 36)` = anchor_yellow.
      snapshot_yellow = 6 + 10 = 16 entries `[UP×6, UP×1,
      RIGHT×8, DOWN×1]`. Replay from `(40, 36)`: UP×6 →
      `(40, 12)`. UP×1 → `(40, 8)`. RIGHT×8: at `(40, 8)`
      try RIGHT to `(44, 8)`. Is there a wall at `(44, 8)`?
      Per the layout above, NO — the only wall on row y=8
      is at the outer frame `(60, 8)`. So RIGHT×8: 5
      successful to `(60, 8)`, 3 blocked at boundary.
      Pointer 14. Then DOWN×1: `(60, 8) → (60, 12)`. Pointer
      = 15. Wait snapshot_len = 16 so one more move: but
      the snapshot tape was 16 entries `[UP×6, UP×1, RIGHT
      ×8, DOWN×1]`. That's 6+1+8+1 = 16. So pointer goes
      0..15, 16 ticks. Shade_yellow ends at `(60, 12)`. NOT
      `(40, 12)`. Fails. (The UP-detour path-shape doesn't
      get the wall at `(44, 16)` to skip RIGHTs because the
      shade hasn't been brought down to row y=16; the wall
      doesn't help the UP-detour shape.)

  So among plausible alternates, only the witness (DOWN-
  detour) reliably places `shade_yellow` at `target_yellow`.
  Other path-shapes either (a) miss anchors (fail
  Anchor-spawn), or (b) miss `target_yellow` due to
  geometric mismatch.

- **Witness solution** (DOWN-detour, 28 actions):
  `[ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION2, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
    ACTION4, ACTION4, ACTION4, ACTION1, ACTION1, ACTION1,
    ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
    ACTION4, ACTION4, ACTION4, ACTION4]`

  Recount: actor start `(8, 60)`. UP×6 → `(8, 36)` =
  `anchor_red`, spawn `shade_red` with snapshot=6. DOWN×1
  → `(8, 40)`. RIGHT×8 → `(40, 40)`. UP×1 → `(40, 36)` =
  `anchor_yellow`, spawn `shade_yellow` with snapshot=16.
  UP×8 → `(40, 4)`. (Wait `(40, 4)` is one row above
  actor_goal at `(24, 4)`.) Need RIGHT×4 to displace from
  `(40, 4)` to … wait that's RIGHT not LEFT. From `(40, 4)`
  to `(24, 4)` is LEFT×4.

  Re-deriving witness: from `(40, 36)` to `(24, 4)` net
  displacement `(-16, -32)`. So 4 LEFTs + 8 UPs = 12 moves.
  `[ACTION1×8, ACTION3×4]` from `(40, 36)`: UP×8 → `(40, 4)`.
  Then LEFT×4 → `(24, 4)`. ✓

  Full witness (28 actions):
  `[ACTION1×6, ACTION2×1, ACTION4×8, ACTION1×1, ACTION1×8,
    ACTION3×4]` = 6 + 1 + 8 + 1 + 8 + 4 = 28 actions.

  Replay (instantaneous-on-spawn): when the actor first lands
  on `anchor_red` at `(8, 36)` (action 6), `shade_red` is
  spawned and immediately walks `[UP×6]` from `(8, 36)` to
  `(8, 12)` = `target_red`. When the actor first lands on
  `anchor_yellow` at `(40, 36)` (action 16), `shade_yellow`
  is spawned and immediately walks the 16-entry tape
  `[UP×6, DOWN×1, RIGHT×8, UP×1]` from `(40, 36)`:
  UP×6 → `(40, 12)`; DOWN×1 → `(40, 16)`; RIGHT×8 → all
  blocked by the wall at `(44, 16)` so the shade stays at
  `(40, 16)`; UP×1 → `(40, 12)` = `target_yellow`. Actions
  17-28 walk the actor UP×8 + LEFT×4 to `(24, 4)` =
  `actor_goal`. Win predicate satisfied at action 28.

- **Difficulty justification**:
  - *(a) Random-resistance*: random-policy / vision-blind
    has near-zero chance of producing the specific 28-step
    sequence above; even any path-shape that delivers BOTH
    shades to BOTH targets requires (1) visiting both
    anchors AND (2) detouring around the wall at `(24, 36)`
    AND (3) ending at `actor_goal`. Within step_budget=60
    a random run has effectively 0 probability of solving.
  - *(b) Human-tractable*: ~2-3 minutes after L2 mastery.
    The two anchor-target pairs visually parallel L2's
    single pair (same silhouettes, different palette), so
    the player extends their L2 understanding. They observe
    that BOTH targets must be filled, that the detour wall
    at `(24, 36)` blocks the straight between-anchors path,
    and that `target_yellow` is at `(40, 12)` (not at the
    natural endpoint `(72, 12)` which is off-grid). They
    reason: "the wall at `(44, 16)` will skip RIGHTs during
    replay, so I should detour DOWN through y=40 then UP to
    yellow-anchor — that puts a DOWN-then-RIGHT-then-UP
    sequence in the tape that, replayed, threads
    `shade_yellow` to `(40, 16)` then UP to `(40, 12)` once
    the RIGHTs are skipped."
  - *(c) Planning depth (post-discovery)*: **moderately
    challenging even for an attentive human**. Post-
    discovery decision space at start: 4 cardinal first
    moves; only UP makes immediate progress (DOWN walks into
    the bottom outer wall, LEFT walks into the left outer
    wall, RIGHT moves away from anchor_red column). A
    plausible-but-wrong alternative the post-discovery
    player would consider: "Walk yellow-first via
    RIGHT×8-then-UP×6" — fails (alternate 4 above;
    `shade_yellow` ends at `(56, 12)` ≠ target). Trivial
    heuristic that fails: "Walk straight to actor_goal
    avoiding anchors" — fails the win predicate (alternate
    1). Witness reasoning chain: visit anchor_red first
    (puts `[UP×6]` in shade_red's snapshot, landing
    `shade_red` at natural-endpoint `(8, 12)` =
    `target_red`); then DOWN-detour around `(24, 36)` to
    insert `[DOWN×1, RIGHT×8, UP×1]` in the tape between
    spawning red and spawning yellow; the RIGHT×8 will
    skip during replay because of the wall at `(44, 16)`,
    leaving `shade_yellow` correctly at `target_yellow` at
    `(40, 12)` after the trailing UP×1.
  - *(d) Step budget*: 60 actions per level data
    `{"step_budget": 60}`. Generous over the 28-action
    witness; ~32 actions of exploration / wrong-key
    recovery. Larger than L2 (50) — the budget does not
    shrink across levels.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. ACTION5, ACTION6, ACTION7
are NOT registered (per `skills/global/action-enum.md`: only
declare slots actually used; ACTION7 is strict-undo and is
omitted because the game has no meaningful undo).

- **ACTION1** — MOVE actor UP by 4 pixels (i.e. `dy = -4`).
  Records `(0, -4)` to the global tape `T` regardless of
  whether the actor's move was blocked by a wall (records the
  ATTEMPTED vector). After the actor's move resolves, every
  active shade with `pointer < snapshot_len` advances by
  applying `T[pointer]` to itself (skip on block); pointer
  increments. Step counter decrements 1.
- **ACTION2** — MOVE actor DOWN by 4 pixels (`dy = +4`). Same
  side-effects as ACTION1 with the opposite vector.
- **ACTION3** — MOVE actor LEFT by 4 pixels (`dx = -4`). Same
  side-effects.
- **ACTION4** — MOVE actor RIGHT by 4 pixels (`dx = +4`). Same
  side-effects.

**Gating**: no context-dependent gating beyond the standard
"during a multi-tick animation, ignore subsequent input"
guard. There are no animations in this game (each tick
resolves immediately); `_get_valid_actions` returns the four
direction-actions on every turn.

## 6. HUD and per-game state

**HUD**: a single `RenderableUserDisplay` subclass
`StepCounterHud` paints the bottom row (`y = 63`, all 64
columns) as a depleting bar. The leading `ceil(64 *
remaining/total)` cells are painted palette-2 (light-grey);
the trailing cells are painted palette-3 (grey). The bar
shrinks from the right edge as steps deplete. Updates every
render frame from `self.steps_remaining` (pulled from the
game's per-level state).

No second HUD widget. The shades' move-tape is NOT visualised
on screen (per the `forbidden-elements.md` rule against
arrow-glyph cultural conventions and against per-cell colour
coding for direction). The shade's animation IS the visual
cue for "the shade is replaying my recent moves" — the player
sees the shade walk autonomously after spawn.

**Per-game state**:

- `self.move_history: list[tuple[int, int]]` — the actor's
  full per-level move tape `T`. Cleared in `on_set_level`.
- `self.shades: list[ShadeRecord]` where `ShadeRecord` is a
  dataclass-style tuple `(sprite, snapshot_len, pointer,
  color)` storing the runtime state of each spawned shade.
  Cleared in `on_set_level`.
- `self.steps_remaining: int` — per-level step counter, set
  from `level.get_data("step_budget")` in `on_set_level`.
- `self.spawned_anchors: set[Sprite]` — anchors that have
  already been triggered and consumed (set to
  `InteractionMode.REMOVED`); avoids double-spawn on revisit.
- `self.actor: Sprite` — cache of the actor sprite; set in
  `on_set_level`.

No animation tick variables. Each tick resolves in one
`step()` call.

## 7. Win condition

**Plain English**: the actor is on its `actor_goal` cell AND
every spawned shade is on its same-coloured target cell.

**Literal predicate** (called at the end of every `step()`
after actor and shade updates):

```python
def _check_win(self) -> bool:
    actor_goal = self.current_level.get_sprites_by_tag("actor_goal")[0]
    if (self.actor.x, self.actor.y) != (actor_goal.x, actor_goal.y):
        return False
    for sr in self.shades:
        target = self.current_level.get_sprites_by_tag(
            f"target_{sr.color}"
        )[0]
        if (sr.sprite.x, sr.sprite.y) != (target.x, target.y):
            return False
    # Also require all anchors triggered (per L1/L2/L3 design
    # the win predicate would already fail if a shade is
    # missing for a target, but defend against degenerate
    # configurations).
    expected_targets = {
        s.tags[1].split("_")[1]
        for s in self.current_level.get_sprites_by_tag("target")
    }
    spawned_colors = {sr.color for sr in self.shades}
    if expected_targets - spawned_colors:
        return False
    return True
```

If `_check_win()` returns True, `self.next_level()`. Same
predicate for L1, L2, L3.

## 8. Lose condition

**Plain English**: the step counter `self.steps_remaining`
reaches 0 before the win predicate is satisfied.

**Literal predicate**:

```python
if self.steps_remaining <= 0 and not self._check_win():
    self.lose()
```

Checked at the end of every `step()` after the win check.

There is no other lose path (no hazards in this game).

## 9. Novelty note

(See `mechanic-pick.md` for the detailed similarity argument.
Summary here.)

**Closest taxonomy entries** (`mechanic-novelty/taxonomy-of-25-games.md`):
- **tn36** (`program-pawn-trace`): both involve a sprite
  executing a recorded list of moves, but tn36 builds the
  programme via explicit click-buttons in a slot-tray UI;
  bw7k records moves implicitly as the actor walks and uses
  arrows for input. Distinguishing rule: tn36's pawn waits
  passively while the player programmes; bw7k's actor is
  walked live and the shade is a SEPARATE COMPANION whose
  motion is derived from a frozen snapshot of the actor's
  walking history.
- **m0r0** (`mirror-orb-merge`): two pawns moved
  simultaneously by mirrored arrow input. Distinguishing
  rule: m0r0's second pawn moves on tick T as an algebraic
  transform (mirror) of the player's tick-T input; bw7k's
  shade moves on tick T as the player's tick-(T-K) input
  (delayed playback) where K is "ticks since the shade was
  spawned". Different mathematical relationship (mirror vs
  delayed playback).
- **lf52 / bp35** (`procedural-graph-walk(-undo)`):
  procedural-graph traversal with undo. No move-tape, no
  shades. Different game shape entirely.

**Closest `prior-games/index.md` entries**:
- **jd4q** (`echo-trail-teleport`): "echo" is a fading
  visual record of visited cells used for teleport-back;
  bw7k's shade is a SPAWNED MOVING entity that replays a
  recorded direction-tape. Distinguishing rule: jd4q's
  trail is a CELL-trail consumed by the actor; bw7k's tape
  is a MOVE-tape consumed by the shade.
- **vp6h** (`shadow-cast-collect`): "shadow" is the
  illuminated-region floor cue; bw7k's shade is an
  autonomous companion. No shared mechanic verb beyond the
  lexical "shadow/shade".
- **zk9p** (`pursuer-merge-walk`): autonomous AI pursuers
  that path toward the avatar each turn; bw7k's shades are
  autonomous but their motion is LITERAL REPLAY of the
  actor's recent path, not pursuit. Different motion source
  (rule-following vs play-back).
- **ek73** (`wake-trail-evade`): vacated cells become
  decaying hazards; bw7k's tape is not a hazard cell-trail
  but a direction-tape consumed by a separate moving
  entity. Sign-inverted dynamic (hazard vs companion).

**Negative similarity check** (per
`negative-similarity-check.md`): walked the eight dimensions
against each named near-miss (tn36, m0r0, zk9p, jd4q, vp6h,
ek73); no single prior shares 3+ dimensions. PASS.

The mechanic family `actor-replay-shade` does not appear in
the taxonomy of the 25 reference games or in the 60-entry
`prior-games/index.md`. Verdict: **NOVEL**.

---

**Spec status**: 9 sections complete; ready for `critique_spec`.
