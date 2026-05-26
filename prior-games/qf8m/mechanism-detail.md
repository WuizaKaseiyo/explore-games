# qf8m — rook-cross-toggle

## Summary

The player drives a 5×5 grid of state-tiles into a target pattern
shown alongside the playfield via clicks (ACTION6 only). Each tile
has a *kind* signalled by its internal motif: a **rook** tile
(`+`-cross) toggles every tile in its row OR column when clicked;
a **bishop** tile (`X`-cross) toggles every tile on its main and
anti-diagonals when clicked; a **tri-state** tile (pink ring with
coloured centre) is click-inert but cycles its own state mod 3
whenever its row/column/main-diagonal/anti-diagonal is touched by
another tile's click. Win is a cell-by-cell state match against
the level's target pattern; lose is step-budget exhaustion.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click at pixel `(x, y)`. Cell coords derived as `col = (x − 2) // 8`, `row = (y − 2) // 8`. Rule fired depends on clicked tile's kind: rook → toggle row+col mod 2; bishop → toggle main+anti diagonals mod 2; tri-state → no-op (step consumed). | always; out-of-grid clicks no-op with no step consumed |

`available_actions=[6]`. Slot 5 omitted because the distinctive
verb is encoded into ACTION6 by the cell-kind dispatch (per
`action-enum.md`'s "distinctive verb on ACTION6" pattern). Slot 7
omitted: binary clicks are self-inverse on Z₂ so re-clicking is
the in-game undo for those.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base dynamic system: rook-flip — clicking any tile flips state mod 2 of every tile in its row OR col (9 cells per click on a 5×5 grid). | All-rook 5×5 grid; target is the XOR of two rook-cross flips at (1,1) and (3,3) — a 14-lit cells in cross-grid pattern. Witness: `[ACTION6@(10, 10), ACTION6@(26, 26)]` (2 actions). Step budget: 25. |
| 2 | + bishop-flip — clicking a bishop tile toggles every tile on its main `i−j=a−b` AND anti-diagonal `i+j=a+b`. | 23 rook tiles + 2 bishop tiles at (1,1) and (3,3). Target: 5-cell centred plus at (2,2). Rook necessary because bishop diagonals only reach row 2 at (2,0) and (2,4), missing (2,1)/(2,3); bishop necessary because target row-parity vector is mixed → unreachable by rook-only. Witness: `[ACTION6@(18, 18), ACTION6@(10, 10), ACTION6@(26, 26)]` (3 actions). Step budget: 50. |
| 3 | + tri-state cell — a single cell at (2,2) cycles state mod 3 (light-grey centre → magenta → light-blue) instead of mod 2. Other cells continue to flip mod 2. | 22 rook + 2 bishop at (1,1)/(3,3) + 1 tri-state at (2,2). Target binary cells form a square-frame-with-corners pattern; tri-state cell must end in state 2 (light-blue centre). State 2 requires exactly 2 flips touching (2,2), delivered by the witness's two bishop clicks (both bishops' main diagonal `i-j=0` passes through (2,2)). Witness: `[ACTION6@(34, 2), ACTION6@(2, 34), ACTION6@(10, 10), ACTION6@(26, 26)]` (4 actions). Step budget: 60. |

## Win condition

After every action, every cell's `_cell_state[(col, row)]` is
compared against `_target_state[(col, row)]`. If equal at every
cell, `self.next_level()` fires. After L3's `next_level()` the
engine's default behaviour fires `self.win()` (3-level cap).

## Lose condition

`_steps_remaining` reaches 0 with the grid not matching the
target — `self.lose()` fires. No instant-fail hazard; binary
clicks are self-inverse and tri-state cycling is forgiving (any
state can be re-cycled to the target by additional touches).

## Internal state

- `_cell_state: dict[(col, row) → int]` — current state per cell
  (0/1 binary, 0/1/2 tri-state).
- `_target_state: dict[(col, row) → int]` — target state per cell,
  loaded from `level.get_data("target")` in `on_set_level`.
- `_cell_kind: dict[(col, row) → "rook" | "bishop" | "tristate"]`
  — click-rule selector per cell, populated from sprite tags.
- `_cell_sprite: dict[(col, row) → Sprite]` — live tile sprite
  per cell; pixels reassigned on state change.
- `_target_sprites: dict[(col, row) → Sprite]` — mirror-grid
  mini-tile sprites; pixels set once in `on_set_level`.
- `_max_steps`, `_steps_remaining` — budget bookkeeping.

`_get_hidden_state` returns the 5×5 grid of `_cell_state` values
as int16 so the engine's `(frame, hidden_state)` graph hash
distinguishes states that render identically — particularly
important across the tri-state cell's 3-color cycle, which the
8×8 mini-tile rendering compresses into similar palette-7-frame
patches.

## Notable code patterns

- **In-place pixel reassignment for state changes** — each cell
  has a single live sprite whose `.pixels` is set to a fresh copy
  of one of the pre-computed numpy arrays (`_ROOK_DARK_NP` /
  `_ROOK_LIT_NP` / `_BISHOP_*` / `_TRISTATE_NP[s]`) on every state
  change. Cleaner than the two-sprite-swap idiom for 2-3-state
  cells.
- **Tag-based dispatch on cell kind** — cells share a base tag
  `cell` plus a sub-tag per kind (`rook` / `bishop` / `tristate`).
  `level.get_sprites_by_tag("cell")` enumerates them in
  `on_set_level`; `sprite.tags` membership selects the click rule
  via `_cell_kind` cache. Clean dispatch without a giant
  if-elif tree on sprite name.
- **Pre-enumerated 25-cell ACTION6 candidates** —
  `_get_valid_actions` returns 25 ActionInputs at the cell
  centres so an external agent has a tabular click vocabulary.
  Reused from r11l / su15 idiom.
- **Step-counter HUD as single-row depleting bar** — universal
  pattern, painted on row 63 with palette-6 filled / palette-4
  empty. Reset per level via `level.get_data("step_budget")`.
- **Visual identity = motif (not palette)** — each cell-kind's
  internal motif (+, X, ring) is preserved across state-color
  variants. The motif is the player's only cue to "what click
  rule governs this cell"; palette indicates state alone.
