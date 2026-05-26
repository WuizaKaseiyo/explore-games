# wj7d — fold-crease-overlay

## Summary
The player has coloured 6×6 stamps on the active half of a 64×64
playfield that is bisected by a single white crease line. Pressing
the FOLD verb (ACTION5) reflects the selected stamp's pixel pattern
across the crease, permanently deposits the reflected colour into
the target-half cells the reflected footprint lands on, and consumes
the stamp itself. The level is won when every non-transparent cell
of every dim-shadow target on the far half has been covered with the
matching stamp colour. ACTION6 selects which stamp is the focus of
the next fold; in level 3 ACTION6 also selects the crease and
re-orients it H↔V at the click cell. The lose condition is step-
budget exhaustion or detected unwinnability (every same-colour stamp
consumed without covering an uncovered shadow).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move selected stamp -4 in y; or selected H crease row -=4 at L3 | a stamp or crease must be selected |
| ACTION2 | Move selected stamp +4 in y; or selected H crease row +=4 at L3 | as above |
| ACTION3 | Move selected stamp -4 in x; or selected V crease col -=4 at L3 | as above |
| ACTION4 | Move selected stamp +4 in x; or selected V crease col +=4 at L3 | as above |
| ACTION5 | FOLD: reflect selected stamp across the crease, deposit reflected pixels into cells_covered, consume the stamp | a stamp must be selected |
| ACTION6 | CLICK at `(x, y)`: select stamp / select crease (L3) / re-orient crease at click cell (L3) | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 MOVE-stamp + M2 FOLD-commit (the base dynamic system) | One auto-selected red cross stamp at (8, 8); single pink cross shadow at (24, 45); fixed H crease at row 31. Player must move the stamp to (24, 12) — RIGHT 4 times + DOWN 1 time — then FOLD. Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION2, ACTION5]` (6 actions). |
| 2 | + M3 SELECT-among-stamps (ACTION6 click) | Two stamps (red cross at (8, 4), blue ring at (24, 24)); two shadows (red cross at (24, 37), blue ring at (16, 41)); fixed H crease at row 31; no auto-select. Blue's body geometrically blocks red's required pre-fold destination, so the witness must fold blue first to clear the way. Witness `[ACTION6@(24,24), ACTION1, ACTION1, ACTION3, ACTION3, ACTION5, ACTION6@(8,4), ACTION4, ACTION4, ACTION4, ACTION4, ACTION2, ACTION2, ACTION2, ACTION2, ACTION5]` (16 actions). |
| 3 | + M4 MOVE-CREASE (slide crease perpendicular to its orientation) and + M5 RE-ORIENT-CREASE (second click on selected crease pivots H↔V at click cell) | Two stamps (red cross at (16, 12), blue ring at (40, 8)); two shadows (red cross at (45, 16), blue ring at (40, 41)); default H crease at row 31; `crease_movable=True`. Blue needs H crease translated to row 27 (1 ACTION1 press); red needs the crease re-oriented to V at col 33 (a non-obvious column — the trivial heuristic of clicking the visual midpoint col 32 fails). Witness `[ACTION6@(32,31), ACTION1, ACTION6@(40,8), ACTION5, ACTION6@(33,27), ACTION6@(33,27), ACTION6@(16,12), ACTION2, ACTION5]` (9 actions). |

## Win condition
For every active `shadow` sprite in the level, every non-transparent
pixel cell at world position `(x, y)` has `cells_covered[(x, y)]`
equal to the matching stamp colour (red shadow palette 7 ⇄ stamp
colour 8; blue shadow palette 10 ⇄ stamp colour 9). When the
predicate holds, `self.next_level()` fires (or `self.win()` after
the last level).

## Lose condition
1. Step-budget exhaustion: `step_remaining` decremented at the
   start of each `step()`; if it falls below 0 and the level is
   not yet won, `self.lose()` fires.
2. Detected unwinnability: after every fold, for each colour
   that has uncovered shadow cells AND zero remaining stamps of
   that colour in the active half, `self.lose()` fires
   immediately to avoid a soft-lock wait-out.

## Internal state
- `self.selected_stamp` — the currently-selected stamp Sprite (or
  None).
- `self.crease_selected` — bool; whether the active crease sprite
  is currently selected (for moving / re-orienting at L3).
- `self.crease_orient` — `"H"` or `"V"`.
- `self.crease_pos` — row index for H crease, col index for V
  crease.
- `self.crease_movable` — bool; loaded from per-level data
  (`True` only at L3).
- `self.cells_covered` — `dict[(int, int), int]` mapping each
  cell that has been folded onto, to the colour deposited there.
  Re-rendered each frame by `CoveredCellsOverlay`.
- `self.hud.current` / `self.hud.max_steps` — step counter.

## Notable code patterns
- **Step-counter HUD as a depleting bar (universal idiom, row 0
  in this game)**: `StepCounterHud(RenderableUserDisplay)` paints
  cols 4..59 of row 0 with palette 14 (filled) and palette 4
  (empty) proportional to `current/max_steps`.
- **CoveredCellsOverlay re-rendering inked cells each frame**:
  a second `RenderableUserDisplay` registered after the HUD that
  iterates `cells_covered.items()` and writes each (x, y) → colour
  onto the rendered frame. Persistent fold ink without needing a
  canvas sprite.
- **Two-orientation crease via TANGIBLE/REMOVED swap**: both
  `crease_h` and `crease_v` Sprite instances are placed in every
  level; `_activate_crease()` toggles which is `TANGIBLE` based on
  `self.crease_orient` and removes the other.
- **Selection-state machine over ACTION6 click**: `_handle_click`
  resolves clicks against (a) stamp bounding boxes, (b) the active
  crease line, with the second-click-on-selected-crease pivoting
  H↔V at the click cell. At most one of {None, stamp, crease} is
  selected at a time.
- **Stamp-on-stamp collision via pixel-perfect overlap test**:
  `_pixels_overlap` compares the proposed-position pixels of the
  moving stamp against the existing pixels of any other tangible
  stamp; the move is rejected as a no-op if any non-transparent
  pixel pair coincides.
- **H/V-flip-invariant stamp internal accent**: the stamp pattern
  is symmetric under both horizontal and vertical reflection, so
  the matching shadow's transparent cells (where the stamp's
  white-accent pixels would land) align correctly under either
  fold orientation.
