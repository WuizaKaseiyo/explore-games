# qm4t — convex-pen-trap

## Summary
The player places vertex-posts on the 64×64 playfield by clicking empty
cells; the engine renders the convex hull of all currently-placed posts
as a 1-pixel outlined fence with a faint inside-tint. ACTION5 commits
the pen: every critter or patroller sprite whose centre is strictly
inside the hull is consumed in a single tick, matching-colour captures
tick off per-colour tally chips, and non-matching captures cost a
strike. Win = empty tally; lose = 3 strikes or step-budget exhaustion.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Commit the pen — compute convex hull of placed posts, capture inside critters / patrollers, then clear every post. | Always; no-op when fewer than 3 posts placed. |
| ACTION6 | Click — if the cell is empty (and in playfield, and post-count < 8), place a `vertex_post`; if the cell already has a post, remove it; otherwise no-op. | Always. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (place vertex posts) + M2 (commit pen). | 3 same-colour critters in the centre. Witness `[ACTION6@(15,15), ACTION6@(50,15), ACTION6@(30,50), ACTION5]` — triangle hull encloses every green. |
| 2 | M3 (selective-shape colour discrimination): forbidden critters at corners that the pen MUST exclude. | 3 greens centre + 4 maroons at the playfield corners. Big pen captures all 4 maroons → 4 strikes → lose. Witness `[ACTION6@(12,15), ACTION6@(52,15), ACTION6@(32,55), ACTION5]` — tight triangle around the green cluster. |
| 3 | M4 (patroller-timing): 3 synced patrollers cycle in/out of the centre band; commit must land on an outside-phase. | 3 greens + 2 yellows + 3 maroons + 3 patrollers. Witness `[ACTION6@(12,13), ACTION6@(54,13), ACTION6@(54,54), ACTION6@(12,54), ACTION5]` — rectangle-pen, 4 placements advance the action count to patroller phase 4 (corners-outside), then commit. |

## Win condition

After every action, if `current_level.get_sprites_by_tag("tally")` is
empty, the level is solved → `next_level()` (or `win()` from L3).

## Lose condition

- `_strikes >= 3` → `lose()`.
- `step_counter.current_steps <= 0` → `lose()`.

## Internal state

- `_step_counter_ui: StepCounterHud` (a `RenderableUserDisplay`).
- `_max_steps: int` — per-level step budget.
- `_strikes: int` (0..3).
- `_max_posts: int = 8`.
- `_patroller_phase: int` — current phase of the L3 patroller cycle (mod 8).
- `_patroller_cycles: list[list[(int,int)]]` — the per-patroller
  sequences of cell positions, indexed by `_patroller_phase`.
- `_patroller_sprites: list[Sprite]` — the active patroller sprites at
  L3 (empty at L1/L2).

The `vertex_post`s themselves and the `pen_overlay` are normal level
sprites; the pen geometry is recomputed every step from the live post
positions, so there is no separate cached hull.

## Notable code patterns

- **Convex hull via Andrew's monotone chain.** `_convex_hull(points)`
  sorts the input, builds a lower then an upper chain (each maintains
  CCW turns by popping on `cross ≤ 0`), and concatenates. Output order
  is consistent (CW in image-coord y-down convention) and works for
  any winding-agnostic downstream operation.
- **Ray-casting point-in-polygon.** `_point_in_polygon(px, py, poly)`
  iterates polygon edges, tests `(yi > py) != (yj > py)`, computes the
  edge's x at `py` via linear interpolation, and toggles the inside
  flag on each leftward intersection. No winding assumption needed.
- **Pen overlay as a recomputed 64×64 sprite.** A single
  `INTANGIBLE` sprite at `layer=5` whose `pixels` array is rewritten
  each step: hull boundary cells get palette 1, interior cells get
  palette 2, all else get -1 (transparent). Avoids a per-cell sprite
  fleet and stays cheap for the 64² test region.
- **Synced patroller cycle.** Each patroller has its own cell-list
  cycle, indexed by a shared global phase counter that advances every
  step. Choosing the per-patroller cycles to match phases 0..3 (in)
  and 4..7 (out) gives a "binary timing" puzzle the player can
  observe and plan against.
- **Strike HUD as ordinary sprites.** A strike adds a `strike_marker`
  sprite at one of three fixed slots; capping at 3 markers is enforced
  in `_add_strike`. Lose check then reads `_strikes` rather than
  counting marker sprites — defensive against accidental duplicate
  removal.
