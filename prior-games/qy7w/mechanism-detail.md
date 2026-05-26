# qy7w — strand-twist-permute

## Summary
Three coloured strands hang from filled coloured caps at the top of
the playfield down to hollow coloured slots at the bottom. Between
the strands sit toggleable CROSSINGS — adjacent-column "binary"
crossings and (from L2) a wider "long" crossing that swaps the two
outer columns. Clicking a crossing flips it between PASS (strands
go straight through) and TWIST (the two columns it spans swap below
this row). The level wins when each bottom slot's colour matches the
strand that ends in its column. From L2, a spatial BLOCKER cell
ends the run if a matching-colour strand routes through it; from L3,
a COLOUR-SHIFT dye station re-paints whichever strand passes through
it, and the slot palette adds a new colour only the dye station can
produce. The action subset is `[6]` (click only).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click `(x, y)` — toggle the crossing whose bbox covers the clicked cell, if any. The TANGIBLE-vs-REMOVED interaction modes of the two pre-cloned variants (PASS / TWIST) are swapped on toggle. | Always; misses are no-ops. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | BINARY-CROSSING TOGGLE — 3 binary crossings (cols 0-1, cols 1-2, cols 0-1). Click a crossing to swap the strand columns at and below its y. Slots demand a swap permutation that the player infers by trial. | Witness `[ACTION6@(41, 28), ACTION6@(25, 40)]` — toggle the cols 1-2 crossing, then the lower cols 0-1 crossing. |
| 2 | LONG-CROSSING TOGGLE (new) — a 35-px wider crossing across cols 0 and 2 swaps the outer strands in one click. Plus the L2 blocker_yellow cell at (col 1, y=36): a yellow-coloured strand routed through it triggers `lose()`. The blocker eliminates the binary-only winning path, forcing the witness to use the long crossing. | Witness `[ACTION6@(25, 14), ACTION6@(25, 22)]` — toggle the top cols 0-1 binary, then the long crossing. |
| 3 | COLOUR-SHIFT DYE STATION (new) — a passive cell at (col 0, y=38) that re-paints any strand routed through it to palette 14 (green); slot 0 now demands green. Blocker still present at (col 1, y=42). The L1 + L2 mechanics are still required — every winning configuration toggles both binary and long crossings to route the right strand through the dye station while keeping yellow out of (col 1, y=42). | Witness `[ACTION6@(25, 14), ACTION6@(25, 22)]` — toggle the top binary, then the long crossing. (Two further valid 2-click witnesses exist: `(25, 22), (41, 30)` and `(25, 22), (41, 53)`.) |

## Win condition
After every action, the strand routing is re-traced top-to-bottom
applying every TANGIBLE crossing's swap (binary or long), every
COLOUR-SHIFT cell's colour remap, and recording the strand at each
column at every y-row. The win predicate compares the strand at the
canvas's bottom row at each end-slot's column against the slot's
declared colour; if every column matches, `self.next_level()` fires.

## Lose condition
Two predicates:
1. **Step-budget exhaustion**: when `self._action_count >= step_budget`
   (per-level: 30 / 24 / 22), `self.lose()` fires.
2. **Blocker hit**: when the strand routing computes a strand
   carrying the blocker's declared colour at the blocker's (col, y),
   `fail_pending` is raised and `self.lose()` fires at end of `step()`.

## Internal state
- `self._step_counter_ui`: HUD widget tracking remaining steps.
- `self.fail_pending`: bool raised when the strand trace hits a
  matching blocker; consumed at end of `step()`.
- `self._bottom_strands`: list of `(col, colour)` per strand
  identity at the canvas bottom — set every step by `_repaint_strands`,
  consumed by `_check_win`.
- The crossings' state (PASS / TWIST) is implicit in which of the
  two pre-cloned variants per crossing has `InteractionMode.TANGIBLE`.
  Sprite tags `cid_C1`..`cid_C5` identify which crossing each variant
  belongs to.

## Notable code patterns
- **Two-sprite-swap state machine.** Each crossing has both a PASS
  and a TWIST sprite variant placed at the same coords; one is
  TANGIBLE, the other REMOVED. Toggling swaps modes via
  `set_interaction()`. This mirrors the `code/universal-scaffold.md`
  § "Two-sprite swap" idiom.
- **Strand canvas as a one-sprite dynamic painter.** A single 49×64
  `strand_canvas` sprite at layer 0 is fully repainted every step
  by `_repaint_strands()` — its `pixels` ndarray is overwritten with
  3-pixel-wide vertical bars at each strand's current (col, y).
  Crossings, blockers, and shift cells are stable overlays at higher
  layers.
- **Routing trace walks every screen y top-to-bottom.** A single
  loop applies crossings → shift cells → blockers in y-order,
  collecting per-y strand state. Cleaner than per-event branches
  and trivially deterministic.
- **Click clamped to visible region of crossing bbox.** The crossing
  sprites have transparent (-1) pixels at the strand-column regions
  inside their bbox so the canvas shows through; `_get_valid_actions`
  returns click coords offset to the visible grey region (local x=9)
  rather than the bbox centre, which would land on a transparent
  cell and miss the sprite.
