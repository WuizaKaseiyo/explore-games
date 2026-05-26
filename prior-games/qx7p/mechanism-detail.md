# qx7p — column-shift-row-align

## Summary
The player faces a row of three to five tall vertical columns, each
painted as a 12-segment colour-band stack with a 1-pixel side
border. A horizontal scan line cuts across all columns at a per-
level row; whichever segment of each column intersects the scan
line is that column's currently aligned colour. Framed colour-
swatch labels above each column declare the target colour each
column must surface at the scan line. The player clicks a column to
make it active, then ACTION1/ACTION2 shift the active column's
band-stack one segment up or down (cyclic, modulo 12). The win
condition is row-pattern match: every column's scan-line colour
equals its target. Two compositional mechanics layer on top: bound-
pair coupling at L2 (shifting one paired column drives its partner
the opposite way in the same tick) and a movable scan line at L3
(ACTION5 cycles the scan line through three rows, changing which
segment of each column is read).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Shift active column's band-stack +1 segment (mod 12). Drives bound-pair partner −1 in the same tick. | Only when an active column is selected. |
| ACTION2 | Shift active column's band-stack −1 segment (mod 12). Drives bound-pair partner +1. | Only when an active column is selected. |
| ACTION5 | Advance scan-line cycle to next of {row 32, row 35, row 38} (offsets 6, 7, 8). | Filtered out of `_get_valid_actions` for L1/L2; available in L3 only. |
| ACTION6 | Click a cell. If inside a column's bounding box, set as active; else deselect. | Always valid. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1: column-shift (click + arrow) | 3 independent columns, scan line fixed at row 29. Each column's band-stack must be shifted to bring its target colour to the scan line. Witness: `[ACTION6@(16,14), ACTION1×4, ACTION6@(32,14), ACTION2×5, ACTION6@(48,14), ACTION1×3]` — 15 actions. |
| 2 | + M2: bound-pair coupling (ribbon-linked partners shift in opposite directions per arrow) | 4 columns; left two are a bound pair (orange ribbon + dot endcaps at row 10..11). Bound-pair invariant: paired positions sum to a constant (= 0 at start). Targets are antisymmetric so the coupled shift produces them in one motion. Independent columns 3 and 4 shift normally. Witness: `[ACTION6@(12,14), ACTION1×4, ACTION6@(40,14), ACTION1×6, ACTION6@(54,14), ACTION1×2]` — 15 actions. |
| 3 | + M3: scan-line shift (ACTION5 cycles scan-line row through {32, 35, 38}) | 5 columns; two bound pairs (both with k-sum = 4) plus one independent column. Both pairs are unsolvable at start scan-line offset 6 and at offset 7 — only offset 8 satisfies the shared sum constraint. Player must press ACTION5 twice to cycle 0→1→2 (rows 32→35→38) before aligning bound pairs. Witness: `[ACTION5, ACTION5, ACTION6@(6,14), ACTION2×5, ACTION6@(30,14), ACTION2×4, ACTION6@(54,14), ACTION2×3]` — 15 actions. |

## Win condition

After every action, evaluate for each column: visible-segment-index
= `(column.position + scan_line_offset) mod 12`; visible-colour =
`column.base_pixels[visible_segment_index * 3, 2]`. If for every
column this colour equals the matching target patch's interior
colour, fire `self.next_level()`. The third level's
`next_level()` cascades to `self.win()` via the engine default.

## Lose condition

Step counter exhausted: when `self.steps_remaining` reaches 0 after
an action, fire `self.lose()`. There is no instant-fail collision;
all shifts are reversible (via the opposite arrow), so no soft-lock
exists.

## Internal state

- `self.column_positions: dict[str, int]` — per-column shift
  position 0..11.
- `self.column_base_pixels: dict[str, np.ndarray]` — pristine
  per-column pixel matrix; rolled at runtime to render the current
  position.
- `self.bound_partner: dict[str, str]` — symmetric map of bound-pair
  partners.
- `self.scan_line_rows: list[int]` — per-level cycle of scan-line
  rows; length 1 for L1/L2, length 3 for L3.
- `self.scan_line_idx: int` — current index into `scan_line_rows`.
- `self.active_column: Sprite | None` — currently selected column.
- `self.steps_remaining: int` — per-level countdown.
- `self._step_counter_hud: StepCounterHud` — depleting top-row HUD
  bar.

## Notable code patterns

- **`np.roll` for column-stack shifts.** Each shift mutates
  `column.pixels = np.roll(base, -SEGMENT_HEIGHT * pos, axis=0)`
  in O(N) without rebuilding the array — preserves the column's
  static-pattern definition while exposing only one rolling state
  variable per column.
- **Bound-pair coupling via partner map.** `_apply_shift` shifts the
  active column then looks up the partner in `bound_partner` and
  shifts the partner by `−delta`. Single integer state per column;
  no per-pair animation phase needed.
- **Per-level ACTION5 gating via `_get_valid_actions`.**
  `available_actions` is declared globally as `[1, 2, 5, 6]` (engine
  contract; cannot vary per level). Runtime filter
  `_get_valid_actions` removes ACTION5 from the agent's options when
  `len(self.scan_line_rows) <= 1` (i.e. L1/L2). Mirrors the cn04 /
  sp80 idiom.
- **Targets resolved by closest-x-centre.** `_target_colour_for_column`
  picks the target patch whose centre x is closest to the column's
  centre x. Lets target-patch placement vary across levels without
  per-level mapping logic.
- **Persistent active-column highlight.** Two thin
  `active_highlight` strips (1 × 36 white) flank the selected
  column on left and right and stay visible for as long as the
  column is active — surfaces the click-selection state so the
  player can read it from the rendered frame at any moment
  (no-hidden-state rule).
