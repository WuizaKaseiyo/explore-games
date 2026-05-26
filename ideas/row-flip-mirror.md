# Row-Flip-Mirror

## Summary

The grid is a fixed-size mosaic of single-cell **coloured tiles**.
Along each edge of the grid sits a row of small **flip-button
sprites** — one button per row (on the left and right edges) and
one per column (on the top and bottom edges). Clicking a button
**reflects the entire row (or column) across its centre**, swapping
the leftmost and rightmost cells, the second-leftmost and
second-rightmost, etc. Tiles in fixed-position **anchor** cells
along the row (locked at level start) refuse to participate — they
stay in place, and the reflection wraps AROUND them as if they
weren't there (their cell is excluded from the reflection set).

Each level shows a static **target arrangement** of tile colours
in a side-panel. The level wins when the live tile arrangement
equals the target. The only failure mode is exhausting the
per-level step counter.

## Visual elements

- 8×8 inner grid of tiles, each 1×1 in saturated palette colour.
- 8 flip-buttons along each of 4 edges = 32 buttons total. Each
  button is a 1×1 cell with a small dark-grey perpendicular
  notch indicating the axis it acts on.
- A **target side-panel** in the bottom-right shows the required
  tile arrangement at scale.
- An **anchor tile** carries a 1-pixel **white dot** in its
  centre (visual fixity marker).
- A **disabled button** (level 3+) renders dimmed (mid-grey).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click a flip-button. The associated row or column reflects across its centre, EXCLUDING anchor cells (they remain in place; non-anchor tiles fold around them). Clicks on tiles or empty cells are no-ops. | always; clicks on disabled buttons are no-ops with no step consumed. |

`available_actions = [6]`.

## Mechanics enumeration

- **M1 — flip-row-or-column:** ACTION6 click on a flip-button
  reflects the cells of the associated row (or column) across
  its centre. Specifically, for a row of length L: cell at
  column c swaps with cell at column (L-1-c) for every c <
  L/2. Anchor cells are skipped — both their position AND
  their content stay in place; the reflection is performed on
  the **subsequence of non-anchor cells** in their original
  positions, then they fold pairwise from outside in.
- **M2 — match-target-arrangement:** the win predicate compares
  the live tile colour grid to the level's target grid.
- **M3 — anchor-tile (level 2+):** specific tiles are tagged
  `anchor` and immovable; flips skip them.
- **M4 — disabled-button (level 3+):** specific flip-buttons are
  tagged `disabled` and refuse to execute (clicks are no-op).
  This forces the player to use the *other* (non-disabled)
  buttons, which often requires combining row and column flips
  in a specific order to achieve the target.

## Per-level progression

### Level 1 — base system (M1 + M2)
- 6×6 active region. Target arrangement requires at least 4 specific row and column flips to reach. 
- **Witness:** 15 actions. The player must find the correct sequence of row and column flips, since flips commute only if they don't intersect in a way that matters. Wait, row and col flips always intersect. Order matters completely.
- **Mechanics required:** M1, M2.

### Level 2 — + M3 (anchor tile)
- 8×8 grid; 6 anchor tiles. The target requires several flips that "fold around" the anchors.
- **Witness:** 35 actions. The anchor tiles act as fixed points that break the symmetry of the flips. The player must use specific sequences of flips to move tiles past the anchors without displacing the tiles that are already in the correct positions relative to the anchors.
- **Mechanics required:** M1, M2, M3.

### Level 3 — + M4 (disabled button) + composition
- 10×10 grid; multiple anchor tiles AND disabled buttons (e.g. the entire left edge of row-flip buttons).
- **Witness:** 60+ actions. The player must achieve a target arrangement using only the non-disabled buttons. If they want to flip row 3, but the button is disabled, they must shift the entire board so that row 3's contents are in row 4, flip row 4, and shift it back. This requires extreme forward planning.
- **Mechanics required:** M1, M2, M3, M4.

## Win condition
After every ACTION6 that resolves to a flip, compare the live tile colour grid to the target grid. If equal, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. Misclicks consume no step.

## Internal state
- `self.tiles: np.ndarray[int]` — colour grid.
- `self.anchors: set[(int, int)]` — anchor cell positions.
- `self.disabled_buttons: set[(int, str)]` — disabled buttons.
- `self.target: np.ndarray[int]`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `lp85 — row-col-shift-grid`**: Row-flip-mirror REFLECTS the row across its centre — a different permutation group, with anchor cells introducing local rule deviations.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random button clicks reflect rows and columns at random; the chance of randomly producing the exact target arrangement is small. Anchor cells and disabled buttons restrict the state space to a very specific puzzle topology.

## Planning depth
- **L1:** moderate — must foresee how a row flip interacts with a col flip.
- **L2:** deep — anchor cells force the player to plan flips that don't scramble the anchored components.
- **L3:** very deep — disabled buttons force a specific sequence of row + column flips to emulate the disabled flips. Extremely order-dependent.
