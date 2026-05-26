# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03): the 9-section spec
- skills/code/universal-scaffold.md: file structure, naming convention, camera-viewport rule, two-sprite-swap idiom
- skills/code/novaengine-api.md: Sprite, Level, Camera, NovaBaseGame signatures
- skills/code/spec-template.md: cross-reference to confirm sprite/levels coverage
- skills/global/action-enum.md: ACTION7 strict-undo confirmed omitted
- skills/global/color-legend.md: palette assignments (1, 3, 5, 6, 11, 14)
- 5 reference source files in full from study (cn04, sp80, wa30, sk48, cd82): used for house style — sprite dict at top, levels list as flat constant, RenderableUserDisplay subclass for HUD, tag-based dispatch via get_sprites_by_tag, NovaBaseGame subclass body order

## Deliverables Produced
- prior-games/rt9k/rt9k.py: 454-line implementation. AST-parses; instantiates; 3 levels declared with grid_size=(64, 60) each; step budgets {30, 50, 70}.
- prior-games/rt9k/metadata.json: per spec.
- workspace/implement-summary.md.

## Notes
- Used semantic names throughout (avatar, wall_solid, filter_<tone>, goal_plain, goal_yellow, StepCounterHud, _attempt_move, _check_win, etc.) — no obfuscation, per `universal-scaffold.md` § Style rules.
- The wrap-and-filter precedence is implemented as: detect intended off-grid move → wrap target cell + tentative tone update → check destination for solid wall (always blocks) → check destination for filter (blocks unless avatar's *post-wrap* tone matches the filter's tone) → commit move (and tone change if wrapped). See `_attempt_move`. This matches spec § 5 "Wrap-and-filter precedence".
- Camera viewport set in `on_set_level` to `(64, 60)` (matching level grid_size), with `letter_box=PADDING_COLOR=1`, so the bottom 4 pixel rows are letter-box that the StepCounterHud overwrites. Verified that the playfield occupies pixel rows 0..59 and the HUD bar at rows 60..63 does not intersect any sprite.
- Step budget drains by 1 per action regardless of whether the move succeeded, was blocked by a wall, or hit a filter — matches spec § 8 lose semantics and consistent with reference games (cn04 drains on every action).
- `_set_tone` uses `Sprite.color_remap(old_color, new_color)` to recolour the avatar's body cells when tone changes; the avatar's pixels begin with palette 6 (magenta), and we track `self._tone` to know which palette colour is currently in use.
- Smoke instantiation: instantiated `Rt9k()`, confirmed `len(g._levels) == 3` and `g._available_actions == [1, 2, 3, 4]` and starting tone = 0. (The state's example uses `g.levels` but the engine attribute is `_levels`; harness output adjusted accordingly.)
- Cleaned up `__pycache__` produced during the smoke test.
