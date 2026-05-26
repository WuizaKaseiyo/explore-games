# rt9k — torus-wrap-tone-cycle

## Summary

A single avatar walks a small (16×15-cell, stride-4-pixel) playfield
with the four arrow keys. The playfield's outer rectangle is
identified as a torus: walking off any edge re-enters from the
opposite edge. Every wrap-cross advances the avatar's visible
tone-state by one step in a three-hue cycle ({magenta, yellow,
green}, with right/down wraps `+1 mod 3` and left/up wraps `-1 mod
3`). Tone-coded filter walls only let the avatar pass when its tone
matches the wall's tone. The level wins when the avatar reaches a
goal cell with the right tone (any tone for the L1/L2 plain goal,
yellow only for L3's tone-keyed goal). The level is lost when the
step counter reaches zero. The avatar's body recolours in place
each tone change so the tone state is always visible.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar 1 cell up. If that would leave the playfield, wrap to the bottom edge AND tone `-= 1 mod 3`. | Always; the destination cell is rejected silently if it is a solid wall, or a filter wall whose tone ≠ the avatar's post-wrap tone. |
| ACTION2 | Move 1 cell down. Wrap to top + tone `+= 1 mod 3` if leaving. | As ACTION1. |
| ACTION3 | Move 1 cell left. Wrap to right + tone `-= 1 mod 3` if leaving. | As ACTION1. |
| ACTION4 | Move 1 cell right. Wrap to left + tone `+= 1 mod 3` if leaving. | As ACTION1. |

(ACTION5, ACTION6, ACTION7 are not used. Per `skills/global/action-enum.md` § Slot 7 is strict-undo, ACTION7 is omitted entirely rather than overloaded.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 — torus wrap. | Avatar at logical (4, 7) and `goal_plain` at (11, 7) are split by a full-height `wall_solid` column at col 8; the only route is to walk off the left edge and re-enter from the right. Witness `[3, 3, 3, 3, 3, 3, 3, 3, 3]` (9 LEFT presses); step budget 30. |
| 2 | M2 — tone-cycle on wrap-cross; M3 — tone-coded filter walls (green filter column at col 14 spans the full playfield height). | Avatar at (1, 1), goal at (13, 13). Mid-wall at col 8 forces a wrap; LEFT-wrap takes magenta=0 → green=2, which is the tone needed to pass the green filter at col 14 in the same step. Witness `[3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]` (4 LEFT + 12 DOWN); step budget 50. |
| 3 | M4 — goal-tone requirement (the L3 goal advances the level only when avatar tone equals the goal's tone). The yellow filter colour is added to M3 (same rule, new tone), but is not counted as a separate mechanic. | Avatar at (1, 7), `goal_yellow` at (13, 7) demanding tone=yellow on arrival. Mid-wall at col 8 and full-height green filter at col 14 still apply; a yellow filter strip at row 14 cols 9..13 gates the bottom of the right half. The 4-step LEFT-wrap-and-walk path lands the avatar on (13, 7) with tone=green, which the goal-tone gate refuses. The witness adds 7 UPs to (13, 0), an UP-wrap that lands at (13, 14) with tone=yellow (passing the yellow filter cell as it arrives), and 7 more UPs back to the goal. Witness `[3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]` (4 LEFT + 15 UP = 19 actions); step budget 70. |

## Win condition

After every action, if the avatar's `(x, y)` coincides with a goal
sprite's position, the level advances iff:
- the goal carries the `goal_any` tag (L1, L2 — any tone), OR
- the goal carries the `goal_yellow` tag AND the avatar's tone is
  yellow (L3 only).

When this predicate holds, `self.next_level()` fires; after L3, the
base class auto-fires `self.win()`.

## Lose condition

After every action, if `self._steps_remaining == 0`, the game calls
`self.lose()`. Each action — successful, blocked, or unrecognised
— consumes exactly one step from the per-level budget. There is no
soft-lock state because tone is recoverable from any value via a
single wrap, and no game state is irreversibly mutated.

## Internal state

- `self._tone: int` — current tone in {0=magenta, 1=yellow, 2=green}; reset to 0 on `on_set_level`.
- `self._step_budget: int` — pulled from `level.get_data("step_budget")` in `on_set_level`.
- `self._steps_remaining: int` — drains by 1 per action; surfaced via the bottom HUD bar.
- `self._step_counter_hud: StepCounterHud` — `RenderableUserDisplay` subclass rendering a 4-row depleting bar at pixel y=60..63.
- The avatar sprite's body colour is `Sprite.color_remap`'d on every tone change so the tone is always rendered in place.

## Notable code patterns

- **Wrap-then-test atomic step.** `_attempt_move` resolves edge-wrap (target cell + tentative tone) FIRST, then tests the destination for `wall_solid` (always blocks) and `filter_<tone>` (blocks unless avatar's *post-wrap* tone matches). The mechanic is therefore one atomic action: a single arrow press performs wrap, tone-update, and destination-test in one shot.
- **Tag-based dispatch via `level.get_sprites_by_tag(...)`.** All collision queries (`_wall_at`, `_filter_at`, `_goal_at`) iterate small per-tag lists rather than scanning the full sprite roster — the same idiom every reference game uses.
- **Tone change via `Sprite.color_remap`** rather than swapping pre-baked sprite variants. Three palette colours are walked (6 → 14 → 11 → 6 forming the cycle) so the avatar's body cells track the current tone without a sprite swap.
- **Bottom HUD strip in the letter-box.** `Camera(width=64, height=60)` and `letter_box=PADDING_COLOR=1` reserve the bottom 4 pixel rows; `StepCounterHud.render_interface` overwrites those rows with a green/black depleting bar — same pattern as `wa30`'s step counter.
- **No-overlap discipline at intersections.** L3's yellow filter strip stops at col 13 instead of col 14 to avoid placing two `filter`-tagged sprites at the same cell `(56, 56)` where the green filter column sits — the universal "two-sprite swap" idiom from `code/universal-scaffold.md` § Common patterns is for *deliberate* swaps; an accidental overlap would produce a visual/behavioural mismatch (renderer draws the later sprite, but `_filter_at` returns the earlier-inserted one).
