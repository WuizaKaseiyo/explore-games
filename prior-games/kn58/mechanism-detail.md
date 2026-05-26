# kn58 — anchor-pull-magnet

## Summary

A pure-click puzzle in which the player has no avatar and never moves a sprite directly. The only verb is ACTION6 — a click that places (or relocates) a single magnetic anchor sprite at the clicked cell. After every click, every coloured pawn slides one cell along its dominant Manhattan axis toward the anchor (horizontal-first tiebreak; secondary-axis fallback when primary is wall-blocked). When a pawn lands on a same-colour target ring it sticks — removed from further slide updates but still a collidable obstacle. The win condition is every pawn matched-and-stuck; the lose condition is the per-level step budget reaching zero. Difficulty arises through composition: pawn-pawn collision (L2), matched-stick (L2), and an "unlocked-target" synchronisation rule (L3) layer onto the base anchor-pull mechanic.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK at pixel (x, y) — relocates the single magnetic anchor to the clicked logical cell; triggers Phase 1 (anchor-pull), Phase-1.5 match-check, Phase 2 (anti-anchor push, if present), Phase-2.5 match-check. | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (anchor-place-by-click) + M2 (pawn-magnet-pull) + M3 (colour-match-target-win) | Single orange pawn at logical (4, 7), single orange target ring at (11, 7), no interior walls. Witness: 7 × `ACTION6 @ logical (11, 7)`. |
| 2 | + M4 (pawn-pawn-collision) + M5 (matched-pawn-stick) | Two pawns (orange at (1, 7), purple at (14, 7)) and matching same-position targets at the OPPOSITE ends; horizontal row-7 corridor with a 2-cell southward pocket at col 7, rows 8-9. Pawns must use the pocket to pass each other. Witness: 7 × `ACTION6 @ logical (7, 8)` (pocket detour) → 7 × `ACTION6 @ logical (1, 7)` (purple to target_purple) → 12 × `ACTION6 @ logical (14, 7)` (orange to target_orange) ≈ 25 actions; budget 80. |
| 3 | + M6 (targets-unlocked / synchronisation) | Four objects on a single vertical column 8: white target at (8, 2), orange pawn at (8, 3), white target at (8, 9), purple pawn at (8, 12). The two targets are colour-agnostic 2×2 white squares with no coloured frame — a pawn landing on a target does NOT stick. Win = both pawns occupy target cells at the END of the same action. Distances are asymmetric (white-orange = 1, white-purple = 3) so a single anchor placement that parks one pawn over-shoots the other. The player must pick an anchor that lands both simultaneously (the natural choice is anchor at orange's target (8, 2): orange parks there immediately because Δ=0 and stays; purple is pulled north 3 cells and arrives at (8, 9) on the third tick). Budget 30. |

## Win condition

Every pawn-tagged sprite is in the `stuck_pawns` set (locked-target levels) OR every pawn-tagged sprite is on some target cell at the end of the action (unlocked-target levels). Triggers `self.next_level()` on the action that produces the win.

## Lose condition

`self.steps_taken >= self.step_budget` triggers `self.lose()`. No collision-based lose; difficulty is meant to come from puzzle depth, not step pressure.

## Internal state

- `step_budget`, `steps_taken` — per-level resource counter; backs the bottom HUD bar.
- `anchor_sprite` — `Sprite | None`; the single magnetic anchor live in the level (INTANGIBLE); created on first ACTION6 click, relocated thereafter.
- `targets_unlocked` — `bool`; per-level flag (read from `level.data`). When true, match-check sticking is skipped and win is the transient "all on targets at this exact tick" predicate.
- `anti_anchor_sprite`, `anti_anchor_range`, `anti_anchor_strength` — plumbed but not used by any current level.
- `stuck_pawns` — `set[int]`: `id()` of each matched pawn (locked-target mode); skipped in both Phase 1 and Phase 2 but still collidable via M4.
- `_step_counter_ui` — `StepCounterHud` widget rendering rows 60–63 of every frame.

## Notable code patterns

- **Two-phase tick** (`_do_pull_phase` → match-check → `_do_repel_phase` → match-check): Phase 1 applies the anchor's gradient pull; Phase 2 applies the anti-anchor's gradient push. Match-check between phases lets a pawn sticking by Phase 1's pull avoid being knocked off by Phase 2.
- **Two-pass simultaneous-conflict resolution** (`_commit_moves`): collect every mover's desired destination, then iterate to fixpoint dropping any move whose destination is occupied by a non-mover or claimed by another mover that is itself staying. Lets vacate-and-enter chains succeed in a single tick (orange leaves (7, 7) for (7, 8) while purple enters (7, 7) — both move).
- **Manhattan-gradient with secondary-axis fallback** (`_step_along`): primary axis = dominant component of Δ (horiz tiebreak); if blocked by wall, try secondary axis with that step's remaining sign. Walls are checked at planning time; pawn-vs-pawn conflicts deferred to `_commit_moves`.
- **Unlocked-target win predicate**: in `_all_matched`, branch on `self.targets_unlocked` — when true, predicate is "every pawn position is in the set of target positions" (transient, must be true at the end of an action); when false, predicate is the cumulative `stuck_pawns` set.
- **Click cell-snap**: `display_to_grid` produces a frame-pixel coord; `(gx // CELL) * CELL` snaps to the logical-cell origin so the anchor always lands on a logical-cell boundary.
