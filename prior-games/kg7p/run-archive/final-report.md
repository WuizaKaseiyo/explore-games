# Game generation final report

## Generated game

- **ID**: `kg7p`
- **Source**: `prior-games/kg7p/kg7p.py`
- **Metadata**: `prior-games/kg7p/metadata.json`
- **Lines of code**: 509

## Mechanic

A single light-blue avatar walks a 64×64 arena with arrow keys. The
avatar always faces its last walked direction and projects a one-cell
*tether beam* from its front edge. Pressing ACTION5 toggles the beam:
turning the beam on attempts an immediate couple to any *haulable
block* sitting in the beam cell; turning it off detaches the
currently coupled block in place. A coupled block walks in lockstep
with the avatar across every subsequent walk — both move together
exactly one cell per arrow press, and the walk is rejected if either
the avatar's or the block's destination is a wall or another
uncoupled block. Each block must be delivered to its colour-paired
target. Level 1 has a single block; Level 2 adds a second block and
forces a delivery order (one block's haul path passes through the
other's start cell); Level 3 introduces *direction-locked* blocks
that carry a magenta edge-stripe and can only be coupled and hauled
in the direction that matches the stripe.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk avatar one cell north; rotate to face north; haul coupled block in lockstep. |
| ACTION2 | Walk south; rotate to face south; haul coupled block. |
| ACTION3 | Walk west; rotate to face west; haul coupled block. |
| ACTION4 | Walk east; rotate to face east; haul coupled block. |
| ACTION5 | Toggle beam. ON ⇒ attempt couple at the cell in front. OFF ⇒ detach the coupled block in place. |

(ACTION6 and ACTION7 are not in `available_actions`; the game uses no
click and no undo.)

## Levels

- **Level 1** — Base dynamic system: walk + beam-couple-haul.
  One basic block, one matching target on a row east of the avatar.
  Budget 40 (witness 9).
- **Level 2** — + beam-release (toggle off mid-game). Two blocks
  (yellow at (8, 4), orange at (8, 8)) with two colour-paired targets
  (yellow target at (8, 12), orange target at (3, 8)). Yellow's
  straight-south path passes through orange's start cell, so the
  player must deliver orange first (clearing column 8) or pay an
  extra detour. Budget 60 (witness 29).
- **Level 3** — + direction-locked blocks. Two `block_dir` sprites:
  block_C (haul-north stripe) at (5, 5) and block_D (haul-east
  stripe) at (3, 5). Targets at (5, 1) and (8, 5). block_D's east
  haul path passes through block_C's start cell, forcing the order
  "deliver C first to clear column 5, then deliver D". Budget 80
  (witness 25).

## Novelty note

- **Closest taxonomy entry**: `wa30` — carry-pickup-drop. Both have
  an avatar that walks and transports objects to targets via ACTION5.
  *Distinguishing rule:* `wa30`'s ACTION5 is an **adjacency one-shot
  pickup-or-drop verb**; `kg7p`'s ACTION5 is a **persistent beam
  toggle** whose direction depends on the avatar's facing. The
  coupling persists across many walks and rotations, and direction-
  locked blocks add a per-block cardinal-direction constraint that
  has no analogue in `wa30`.

- **Closest prior-game entry**: `kn58` — anchor-pull-magnet. Both
  have an avatar-controlled "attraction" that mobilises blocks.
  *Distinguishing rule:* `kn58`'s anchor is **clicked globally** and
  pulls *every* coloured pawn one cell along its dominant Manhattan
  axis toward the anchor — a one-shot snap. `kg7p`'s beam is
  **local, directional, and persistent**: only the single block in
  the beam cell couples, and "motion" is the avatar's own walk
  carrying the block in lockstep — no global slide.

## Index update

One row appended to `prior-games/index.md`:

```
| kg7p | beam-tether-haul | Beam-Tether Haul — avatar projects a directional tether beam that couples haulable blocks; ACTION5 toggles beam; L3 adds direction-locked blocks. | 2026-05-11T01:47:59Z | (autonomous) |
```
