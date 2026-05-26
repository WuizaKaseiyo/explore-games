# Mechanic spec — ds5q (wall-erode-chain) — round 2 (post-critique)

**Changes vs round 1** (each addressing an issue from `critique-revisions.md`):
- §3 (avatar sprites) — redesigned avatar to abstract framed-token-with-corner-indicator; removed the word "pickaxe" throughout the spec (Issue 4).
- §4 L1 layout — sealed top/bottom detour by replacing the four scattered stones at (3, 3), (3, 5), (5, 3), (5, 5) with full stone rows at row 3 and row 5 (Issue 1).
- §4 L2 layout — sealed col 7 except at the exit, plus added stones at (5, 1), (6, 3), (6, 5) so the only entry into (6, 4) is via the blue wall (Issue 2).
- §4 L3 layout — applied the same col-7/(5,1)/(6,3)/(6,5) sealing as L2; added a SECOND red wall at (3, 1) hardness 2 with stones flanking it at (3, 0), (3, 2), creating a row-1 alternate route through col 3 (Issues 3 + 5).
- §4 L3 difficulty (c) — replaced the discovery-stage heuristic ("single-erode-per-wall") with a post-discovery one ("monotone-progress along the goal-row"); enumerated the new decision space and traced where the failing heuristic diverges from the witness (Issue 5).

---

## 1. Title
Pickaxe Chamber — an erode-and-traverse puzzle where a coloured charge-indicator on the avatar must be matched at coloured pads before adjacent same-colour walls can be chipped away.

## 2. Mechanic family
**wall-erode-chain.** The avatar walks 8-pixel cardinal hops; ACTION5 strikes and decrements the hardness of every same-coloured wall in the avatar's 4-cardinal neighbourhood by 1; walls reaching hardness 0 are removed. The avatar's *charge state* is set by stepping onto a coloured charge-pad sprite (red or blue), and walls have integer hardness (1 at L1/L2, up to 3 at L3) rendered as visible stripe count in the wall sprite. Priors used: **objectness** (avatar, walls, pads, exit are persistent entities) and **basic geometry / topology** (the connectedness of the floor-reachable region changes as walls erode).

## 3. Sprite roster
- `avatar_uncharged` — 8×8 pixels; outer rim palette 4 (off-black); a 6×6 inner area with palette 2 (light-grey) padding around a 4×4 palette-13 (maroon) filled square; a 2×2 corner indicator at top-right (rows 1-2, cols 5-6) painted palette 0 (white) for the uncharged state. No tool shape, no humanoid features. Tags `["avatar"]`. Role: player; movable; visual cue for charge state.
- `avatar_red` — same pattern; corner indicator palette 8 (red). Tags `["avatar"]`. Role: red-charged variant.
- `avatar_blue` — same pattern; corner indicator palette 9 (blue). Tags `["avatar"]`. Role: blue-charged variant.
- `wall_red_h1` — 8×8; outer rim palette 4; interior 6×6 of palette 8 (red) crossed by ONE horizontal palette-13 (maroon) stripe at the vertical midline. Tags `["wall", "red"]`. Hardness-1 red.
- `wall_red_h2` — interior crossed by TWO horizontal stripes (top third and bottom third). Tags `["wall", "red"]`. Hardness-2 red.
- `wall_red_h3` — interior crossed by THREE horizontal stripes (top, middle, bottom). Tags `["wall", "red"]`. Hardness-3 red.
- `wall_blue_h1` — 8×8; outer rim 4; interior palette 9 (blue) crossed by ONE palette-15 (purple) stripe. Tags `["wall", "blue"]`.
- `wall_blue_h2` — TWO purple stripes.
- `wall_blue_h3` — THREE purple stripes.
- `wall_grey_h1` — 8×8; outer rim 4; interior 6×6 of palette 3 (grey) crossed by ONE palette-4 stripe at the midline. Tags `["wall", "grey"]`. L1's neutral-colour wall (charge_state defaults to `"grey"` so any L1 erode strikes it).
- `stone` — 8×8; outer rim palette 5 (true black); solid palette-4 (off-black) interior with NO stripes. Tags `["stone"]`. Un-erodable barrier; collidable; never destroyed.
- `charge_pad_red` — 8×8; outer 1-pixel padding palette 2; inner ring of palette 8 (red); central 2×2 palette 0 (white) dot. Tags `["pad", "red"]`. Stepping onto it sets `charge_state` to `"red"`; intangible to walking.
- `charge_pad_blue` — 8×8; same pattern but ring palette 9. Tags `["pad", "blue"]`.
- `exit` — 8×8; outer ring palette 14 (green); inner 4×4 palette 0 (white); central 2×2 palette 14. Tags `["exit"]`. Stepping onto it triggers `next_level()`; intangible to walking.

Background: solid palette 2 (light-grey). Letter-box: same colour. Step-counter HUD draws on row 0 (palette 4 over palette 0).

## 4. Level progression, mechanic enumeration, and witness solutions

Common physical layout: `grid_size = (64, 64)`; sprites at 8-pixel-tile alignment so positions form a logical 8×8 board. Camera viewport set to 64×64 in `on_set_level`.

### Level 1 — base dynamic system
- **Mechanics required by the witness** (N = 2):
  - **walk** (ACTION1–4 hop the avatar 8 pixels in the cardinal direction; movement blocked by walls and stones).
  - **erode-adjacent** (ACTION5 reduces by 1 the hardness of every wall in the avatar's 4-cardinal neighbourhood whose colour matches `charge_state`; `charge_state` is initialised to `"grey"` at L1, so all L1 walls — `wall_grey_h1` — are erodable).
- **Necessity per mechanic** (counterfactual, per checklist item 12):
  - **walk**: L1 cannot be solved without walking because the exit at tile (7, 4) is 7 east of the avatar at (0, 4); ACTION5 alone never relocates the avatar.
  - **erode-adjacent**: L1 cannot be solved without eroding because two `wall_grey_h1` instances at tiles (3, 4) and (5, 4) sit on the avatar's only east-bound corridor; row 3 and row 5 are FULL stone walls (8 stones each) sealing every alternate east-bound route, so the avatar cannot detour around either grey wall via rows 0-2 or 6-7 (those rows are unreachable because (0, 3) and (0, 5) are stones, isolating the row-4 corridor from everything north and south of it).
- **Layout** (8×8 logical board; `S` = `stone`, `G` = `wall_grey_h1`, `A` = avatar start, `E` = `exit`, `.` = floor):
  ```
  . . . . . . . .
  . . . . . . . .
  . . . . . . . .
  S S S S S S S S
  A . . G . G . E
  S S S S S S S S
  . . . . . . . .
  . . . . . . . .
  ```
- **Witness solution**:
  1. ACTION4 — (0,4) → (1,4)
  2. ACTION4 — (1,4) → (2,4)
  3. ACTION5 — erode `wall_grey_h1` at (3,4) (hardness 1 → 0; removed)
  4. ACTION4 — (2,4) → (3,4)
  5. ACTION4 — (3,4) → (4,4)
  6. ACTION5 — erode `wall_grey_h1` at (5,4) (hardness 1 → 0; removed)
  7. ACTION4 — (4,4) → (5,4)
  8. ACTION4 — (5,4) → (6,4)
  9. ACTION4 — (6,4) → (7,4) `exit` → `next_level()`
  Total = **9 actions**.
- **Difficulty justification**:
  - *(a) Random-resistance.* 5-action vocabulary (`{1,2,3,4,5}`); a 30-step random rollout that wins must press ACTION5 at exactly steps 3 and 6 (the moments the avatar is at (2, 4) and (4, 4) respectively); the joint probability is below 1 / 30,000 for any reasonable random policy.
  - *(b) Human time.* ~30 seconds; tutorial.
  - *(c) Planning depth.* No strict planning requirement at L1. The level is a discovery gate — once "ACTION5 strips an adjacent wall" is internalised, reaching the exit is trivial.
  - *(d) Step budget.* `step_budget = 30`. Generous (3.3× witness).

### Level 2 — base system + 1 new mechanic
- **Mechanics required by the witness** (N = 3 = L1's 2 + 1):
  - **walk** (carried forward).
  - **erode-adjacent** (carried forward).
  - **colour-pickaxe-match** (new): the avatar begins L2 with `charge_state = None`; ACTION5 has no effect with `None`; stepping onto `charge_pad_red` sets `charge_state = "red"` and visually swaps the avatar to `avatar_red`; stepping onto `charge_pad_blue` swaps to `avatar_blue`. Erode now only affects walls whose `wall_color` equals `charge_state`.
- **Necessity per mechanic**:
  - **walk**: L2 cannot be solved without walking because the avatar must traverse from (0, 4) to the exit at (7, 4); col 3 is sealed except at (3, 4) (a wall, not floor), and col 7 is sealed except at (7, 4), so any solution requires lateral motion across the playfield.
  - **erode-adjacent**: L2 cannot be solved without eroding because the only opening in col 3 is `wall_red_h1` at (3, 4) and the only entry into (6, 4) — itself the only way to reach the exit at (7, 4) — is via `wall_blue_h1` at (5, 4); each must be removed by ACTION5.
  - **colour-pickaxe-match**: L2 cannot be solved without exercising colour-charging because the avatar starts uncharged and ACTION5 is a no-op until a pad is visited. The red wall at (3, 4) requires `charge_state = "red"` (set only at the red pad at (1, 0)); the blue wall at (5, 4) requires `charge_state = "blue"` (set only at the blue pad at (6, 2)). The two pads charge the indicator to two different colours — neither one alone clears both walls.
- **Layout** (`PR` = `charge_pad_red`, `PB` = `charge_pad_blue`, `R` = `wall_red_h1`, `B` = `wall_blue_h1`):
  ```
  . PR S . . . . S
  . . . S . S . S
  . . . S . . PB S
  . . . S . S S S
  A . . R . B . E
  . . . S . S S S
  . . . S . . . S
  . . . S . . . S
  ```
  Stone placements: col 3 at every row except (3, 4); col 7 at every row except (7, 4); plus (5, 1), (5, 3), (5, 5), (6, 3), (6, 5). The combination guarantees (a) col 3 is sealed except at the red wall, (b) col 7 is sealed except at the exit, (c) (6, 4) is reachable only from (5, 4) [the blue wall] or (7, 4) [the destination], and (d) the blue pad at (6, 2) is reachable only from the right side of col 3 via (4, 2) → (5, 2) → (6, 2).
- **Witness solution**:
  1. ACTION1 ×4 — (0,4)→(0,3)→(0,2)→(0,1)→(0,0)
  2. ACTION4 — (0,0)→(1,0) onto `charge_pad_red`; `charge_state = "red"`, avatar → `avatar_red`
  3. ACTION2 ×4 — (1,0)→(1,1)→(1,2)→(1,3)→(1,4)
  4. ACTION4 — (1,4)→(2,4)
  5. ACTION5 — erode `wall_red_h1` at (3,4): 1 → 0, removed
  6. ACTION4 ×2 — (2,4)→(3,4)→(4,4)
  7. ACTION1 ×2 — (4,4)→(4,3)→(4,2)
  8. ACTION4 ×2 — (4,2)→(5,2)→(6,2) onto `charge_pad_blue`; `charge_state = "blue"`
  9. ACTION3 ×2 — (6,2)→(5,2)→(4,2)
  10. ACTION2 ×2 — (4,2)→(4,3)→(4,4)
  11. ACTION5 — erode `wall_blue_h1` at (5,4): 1 → 0, removed
  12. ACTION4 ×3 — (4,4)→(5,4)→(6,4)→(7,4) `exit`
  Total = **25 actions**.
- **Difficulty justification**:
  - *(a) Random-resistance.* 5-vocab, 25-step witness with 4 ACTION5/charge-pad events at exact positions; below 1/10,000.
  - *(b) Human time.* ~2 minutes after reading the screen.
  - *(c) Planning depth (post-discovery).*
    - **Decision space at L2 start (post-discovery):** 3 useful first actions (ACTION1 / ACTION2 / ACTION4; ACTION3 hits the west grid edge; ACTION5 is a no-op while uncharged).
    - **Plausible-but-wrong alternative:** "go down (ACTION2) first to look for a south detour around col 3" — col 3 is sealed at every row, so south leads into the boxed-in left half of the playfield with no crossing.
    - **Witness reasoning chain:** the post-discovery player reasons that (i) col 3 is sealed except at the red wall, so red-charge is mandatory before any east progress; (ii) the blue pad is on the *east* side of col 3 (reachable only after eroding red), so red-first is forced; (iii) the only entry to the exit at (7, 4) is via (6, 4) which in turn is only reachable via the blue wall at (5, 4), so eroding the blue wall is mandatory after charging blue at (6, 2).
  - *(d) Step budget.* `step_budget = 80`. Generous (3.2× witness).

### Level 3 — system + 1 new mechanic
- **Mechanics required by the witness** (N = 4 = L2's 3 + 1):
  - **walk** (carried forward).
  - **erode-adjacent** (carried forward).
  - **colour-pickaxe-match** (carried forward).
  - **layered-hardness** (new): walls now expose hardness as visible stripe count; a wall sprite shows N stripes when its hardness is N (1, 2, or 3 stripes); each ACTION5 strike against a same-colour wall decrements its hardness by 1, and the wall's visible sprite is swapped to the next-lower-hardness variant (`wall_red_h3` → `wall_red_h2` → `wall_red_h1` → REMOVED; same for blue). Implemented by tracking per-wall hardness in `self.wall_hardness` and swapping sprites on each strike.
- **Necessity per mechanic**:
  - **walk**: L3 cannot be solved without walking — the avatar at (0, 4) must reach (7, 4), and ACTION5 alone never relocates the avatar.
  - **erode-adjacent**: L3 cannot be solved without eroding — col 3 is sealed except at (3, 1) (`wall_red_h2`) and (3, 4) (`wall_red_h3`); col 7 is sealed except at (7, 4); (6, 4) is reachable only via (5, 4) (`wall_blue_h1`). Both col-3 openings AND the col-5 blue wall must be eroded.
  - **colour-pickaxe-match**: L3 cannot be solved without colour-charging — the avatar begins L3 with `charge_state = None` and ACTION5 is a no-op until a pad is visited; the red pad at (1, 0) charges red, the blue pad at (6, 2) charges blue, and the col-3 openings (red walls) and col-5 wall (blue) require different colours.
  - **layered-hardness**: L3 cannot be solved without exercising layered-hardness because BOTH col-3 openings hold walls of hardness > 1: (3, 1) is `wall_red_h2` (hardness 2, two strikes required) and (3, 4) is `wall_red_h3` (hardness 3, three strikes required). No alternate path through col 3 exists; either route requires multi-strike erosion. The blue wall at (5, 4) is hardness 1 (one strike) but the layered-hardness mechanic is exercised by the red wall on the witness path regardless.
- **Layout** (`R2` = `wall_red_h2`, `R3` = `wall_red_h3`, `B1` = `wall_blue_h1`, otherwise as L2):
  ```
  . PR . S . . . S
  . . . R2 . S . S
  . . . S . . PB S
  . . . S . S S S
  A . . R3 . B1 . E
  . . . S . S S S
  . . . S . . . S
  . . . S . . . S
  ```
  Col 3 stones at (3, 0), (3, 2), (3, 3), (3, 5), (3, 6), (3, 7) (i.e., every row except (3, 1) which is `wall_red_h2` and (3, 4) which is `wall_red_h3`). Other stones identical to L2's right-side sealing.
- **Witness solution** (the row-1 route, **Path A**, which is the shortest):
  1. ACTION1 ×4 — (0,4)→…→(0,0)
  2. ACTION4 — onto `charge_pad_red`; `charge_state = "red"`
  3. ACTION2 — (1,0)→(1,1)
  4. ACTION4 — (1,1)→(2,1)
  5. ACTION5 — erode `wall_red_h2` at (3,1): 2 → 1 (sprite swap to `wall_red_h1`)
  6. ACTION5 — erode: 1 → 0 (sprite removed)
  7. ACTION4 ×2 — (2,1)→(3,1)→(4,1)
  8. ACTION2 — (4,1)→(4,2)
  9. ACTION4 ×2 — (4,2)→(5,2)→(6,2) onto `charge_pad_blue`; `charge_state = "blue"`
  10. ACTION3 ×2 — (6,2)→(5,2)→(4,2)
  11. ACTION2 ×2 — (4,2)→(4,3)→(4,4)
  12. ACTION5 — erode `wall_blue_h1` at (5,4): 1 → 0
  13. ACTION4 ×3 — (4,4)→(5,4)→(6,4)→(7,4) `exit`
  Total = **22 actions**.
- **Difficulty justification**:
  - *(a) Random-resistance.* 5-vocab, 22-step witness with 5 ACTION5 strikes at three distinct standing positions ((2, 1) twice, (4, 4) once) plus colour-charge events at two pads; well below 1/10,000.
  - *(b) Human time.* ~2.5 minutes after reading the screen, with extra time for inferring (i) that wall stripe count corresponds to required strike count, and (ii) that the row-1 route is shorter than the row-4 route.
  - *(c) Planning depth (post-discovery).*
    - **Decision space at L3 start (post-discovery):** 3 useful first actions (1, 2, 4) — same as L2's 3. The richer post-discovery choice appears AFTER charging red, when the player picks between two cross-col-3 routes: row 1 (via `wall_red_h2`, 2 strikes, 22-action total path) and row 4 (via `wall_red_h3`, 3 strikes, 27-action total path). At this branch point the decision space is 2 plausible routes — strictly larger than the L2 equivalent which had no such branch (L2 forces a single route once col 3's red wall is identified).
    - **Trivial post-discovery heuristic that fails:** *"stay on the row containing the exit (row 4) — monotone-progress along the goal-row"*. A fully-informed player who knows the stripe count on each wall might still default to row 4 because the exit IS on row 4 and the corridor continues monotonically east toward the goal; the row-4 route is the visually obvious choice.
    - **Where the heuristic diverges from the witness (operational walk-through):** at step 3 of the witness (after charging red at (1, 0)), the witness goes south *one step* to (1, 1) and then east to (2, 1) (toward the row-1 wall, AWAY from the exit row). The monotone heuristic instead goes south *four steps* to (1, 4) and then east to (2, 4) (toward the row-4 wall). The two diverge from this point. The heuristic then commits to ACTION5 ×3 at (2, 4) (row-4 wall is hardness 3) versus the witness's ACTION5 ×2 at (2, 1) (row-1 wall is hardness 2) — costing 1 extra strike. Subsequent route to the blue pad and back: the heuristic emerges at (4, 4) which is 4 cells from the blue pad's eventual erode position; the witness emerges at (4, 1) which is 3 cells from (4, 2) (one cell south then directly east to the blue pad). Net delay: the heuristic takes 27 actions vs the witness's 22 — a 5-action / ~23% overhead. The player is not irrecoverably lost (step budget 90 absorbs both), but the witness is meaningfully shorter and finding it requires reasoning *against* the natural monotone-toward-exit pull.
  - *(d) Step budget.* `step_budget = 90`. Generous (4.1× witness); does not shrink relative to L2 per `difficulty-rules.md` § d L3.

## 5. Action mapping
- `ACTION1`: MOVE UP — translate avatar by (0, −8) pixels (one logical tile north). Blocked by walls (any colour, any hardness > 0) and stones.
- `ACTION2`: MOVE DOWN — (0, +8). Blocked similarly.
- `ACTION3`: MOVE LEFT — (−8, 0). Blocked similarly.
- `ACTION4`: MOVE RIGHT — (+8, 0). Blocked similarly.
- `ACTION5`: ERODE — for every wall sprite in the avatar's 4-cardinal neighbourhood whose `wall_color` equals `self.charge_state`, decrement its hardness by 1; if hardness reaches 0, set the wall sprite to `InteractionMode.REMOVED`; otherwise swap the wall sprite to the next-lower-hardness variant. If `self.charge_state is None`, ACTION5 is a no-op.
- `available_actions = [1, 2, 3, 4, 5]`.

Context-dependent gating: none. ACTION5 is always emitted; its effect is conditional on `charge_state` and adjacent walls.

## 6. HUD and per-game state
**HUD widgets** (registered via `Camera(interfaces=[...])`):
- `StepCounterHud(RenderableUserDisplay)` — depleting bar in row 0, palette 4 (off-black) over palette 0 (white). Width = 64 px; full bar at level start, drops one pixel per action; reaches zero on the final action. Reads `(step_budget − action_count)` from the game.

**Charge-state cue**: the avatar sprite itself is the cue — the 2×2 corner indicator shows white when `charge_state is None`, red when `"red"`, blue when `"blue"`. The avatar is swapped between `avatar_uncharged`, `avatar_red`, `avatar_blue` on every pad visit. This is a persistent visual cue per checklist item 19.

**Per-game state** (held on the `Ds5q` instance):
- `self.charge_state: str | None` — current charge colour (`"red"`, `"blue"`, `"grey"` at L1, or `None` at L2/L3 before first pad visit).
- `self.wall_hardness: dict[Sprite, int]` — current hardness per placed wall sprite.
- `self.wall_color: dict[Sprite, str]` — colour per placed wall sprite (`"red"`, `"blue"`, `"grey"`).
- `self.avatar: Sprite` — handle to the currently-active avatar variant; the three avatar variants are placed at the same position with `set_interaction(REMOVED)` on all but one.
- `self.wall_sprite_at: dict[tuple[int,int], Sprite]` — index of (gx, gy) to the currently-tangible wall sprite at that cell, used by the ACTION5 handler to find adjacent walls.

Per-level data (`level.get_data(...)`):
- `step_budget: int` — 30 / 80 / 90 for L1 / L2 / L3.
- `charge_initial: str | None` — `"grey"` at L1, `None` at L2 and L3.

## 7. Win condition
After every action's movement is committed, if `self.avatar.x == exit.x and self.avatar.y == exit.y` (or equivalently `level.get_sprite_at(self.avatar.x, self.avatar.y, "exit") is not None`), call `self.next_level()`. The exit sprite is `InteractionMode.INTANGIBLE` so the avatar can stand on its cell. True for every level.

## 8. Lose condition
At the start of `step()` (before action processing), if `self._action_count >= step_budget`, call `self.lose()`. The step budget is read from `level.get_data("step_budget")` in `on_set_level`. No other lose condition: walls never irrecoverably trap the player (the avatar can always step back to a charge-pad and re-attempt).

## 9. Novelty note
- **Closest taxonomy entries** (`mechanic-novelty/taxonomy-of-25-games.md`):
  - **xn5p** (chamber-stamp-partition): xn5p ADDS walls to subdivide a chamber; ds5q REMOVES wall layers to traverse one. Verb is opposite-direction (additive vs subtractive); goal is opposite-shape (partition vs reach-exit). xn5p has no charge-pad / colour-match mechanic and no hardness layering.
  - **wt39** (glide-deflect-thaw): wt39's avatar GLIDES until colliding and brittle thaw-tiles crack passively after one slide; ds5q's avatar steps in single 8-pixel hops, walls only change in response to deliberate ACTION5 strikes, and erosion is colour-gated by the charge-pad system — none of which is present in wt39.
  - **bx84** (beam-mirror-reflect): bx84 routes a coloured *beam* through mirrors and filters; ds5q routes the *avatar itself* by removing wall layers. No beams, no reflection, no projection.
- **Closest prior-games-index entries**:
  - **xn5p** — same distinguishing rule as the taxonomy match above.
  - **vd3g** (valley-dig-roll): vd3g uses click to toggle binary terrain HIGH/LOW and routes marbles flowing under gravity. ds5q has no marbles, no flow, no toggle (erosion is a multi-step decrement not a binary flip), and uses ACTION5 not click.
  - **fz5j** (phase-step-tile): fz5j tiles auto-pulse open/closed on per-cell schedules independent of the player; ds5q wall state changes only in response to the player's deliberate ACTION5; the player has full agency in ds5q vs none over the timing in fz5j.
  - **kn58** (anchor-pull-magnet): kn58 click places a global anchor, every coloured pawn slides one cell; ds5q has no global pull and no click; erosion is local to the avatar and the avatar itself never slides.
  - **ek73** (wake-trail-evade) and **jd4q** (echo-trail-teleport): both involve the avatar's *trail behind* it. ds5q's player changes the cells *ahead* of the avatar, not behind; there is no trail and no decay.
- **Negative similarity check** (`mechanic-novelty/negative-similarity-check.md`): the closest single prior is xn5p, sharing dimensions 1 (board: walled chamber + walking pawn — universal in walking puzzles), 4 (kills via step budget — universal), 5 (cast: walls + avatar — universal), 7 (rich-pixel walls). Diverging on dimensions 3 (goal is reach-exit, not partition), 6 (visible visual signature is wall-dominated with stripe-banded hardness cues, charge-pad rings, and a corner-indicator avatar — distinct from xn5p's floor-dominated colour-pad insets), and 8 (core dynamic: subtractive wall removal with colour-charge and stripe-counted hardness, not additive wall stamping). The diverging dimensions are the named-principle dimensions (6, 8 are explicit principles), so the test passes — ds5q does not share three or more named-principle dimensions with any single prior.
