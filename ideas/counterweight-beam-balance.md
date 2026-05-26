# Counterweight-Beam-Balance

*(Replaces `sandpile-grain-topple.md`. Real-world inspiration: Roman
balance scales, beam-engine pumpjacks, mobile sculptures by
Calder. Side view, torque-driven.)*

## Summary

A **horizontal beam** pivots at the centre of the playfield. From
each end of the beam hangs a **pan** by a thin rope. The player
places **stones** (each of weight 1, 2, or 3) on either pan. The
beam's tilt angle is the discrete sign-and-magnitude of net torque:
`tilt = clamp(left_torque - right_torque, -2, +2)`. The pans
visually rise/fall with the tilt; in deeper levels, *more beams
hang from those pans*, propagating the tilt cascade.

The level wins when the beam-tilt configuration matches the
target (a sequence of tilts, one per beam) at the end of any
turn.

## Visual elements (distinct from prior corpus)

- 64×64 canvas oriented as a **side view** with a deep-sky grey
  background. The room is implied with a 1-pixel ceiling line at
  the top and floor line at the bottom.
- The **central beam** is a 1-pixel-thick wood-brown horizontal bar
  that visibly rotates around its centre pivot. At tilt = 0 it is
  horizontal; at tilt = +2 the right end drops by 2 pixels and the
  left end rises by 2 (mirror at -2).
- **Pans** are 5-cell-wide trapezoidal sprites hanging from each
  end. The rope from the beam to the pan is rendered as a
  vertical 1-pixel grey line; on tilt the rope visibly leans.
- **Stones** are 1-cell square sprites with palette colours
  encoding weight: weight 1 = pale-grey, weight 2 = mid-grey,
  weight 3 = dark-grey. Stones are stacked on the pan with
  pixel-level offsets so the player can see how many.
- The **stone tray** is a horizontal shelf below the beam-and-pan
  region containing all stones not yet placed; it is 1 cell tall
  and 12 cells wide.
- A **target indicator** on the right rim shows the desired tilt
  pattern: one wedge icon per beam. A green check appears next to
  any beam currently matching its target tilt.
- L2 introduces **cascaded beams**: a smaller beam hangs from
  the right pan of the main beam. The right pan of beam-1 is the
  pivot point of beam-2 — and beam-2 has its own two pans. Beam-2
  hangs visibly below the main beam's right pan.
- L3 introduces:
  - **Sliding stones**: rendered with a small green arrow chevron
    on top. On every ACTION5 tick, a sliding stone migrates from
    its current pan to the *lower* pan of the same beam (the
    side that has dropped). If both pans are equal, the stone
    stays.
  - **Lock-pin**: a small silver pin sprite placed on the beam
    pivot. While locked, the beam doesn't tilt regardless of
    torque (visually horizontal). Lock-pins are clicked to toggle.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance one tick. On L3+, sliding stones migrate; tilts recompute from new weights. | always |
| ACTION6 | Click cell `(x, y)`. Resolves to one of: (a) a stone in the tray + a pan → place that stone on that pan; (b) a stone on a pan + the tray → return it to the tray (free no-op for un-stuck stones); (c) a lock-pin → toggle lock; (d) anywhere else → no-op, no step. The first ACTION6 click in a placement pair selects a stone (pip lights up); the second commits. | always |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — stone-place:** ACTION6 selects a tray stone, then ACTION6
  selects a pan; the stone is placed on the pan. Both clicks
  consume 1 step total (placement is a 2-click sequence).
- **M2 — torque-tilt:** at end of any tick or placement, every
  beam's tilt is recomputed: `tilt = clamp(sum(weights on left
  pan) - sum(weights on right pan), -2, +2)`.
- **M3 — match-target:** the win predicate compares each beam's
  current tilt to its target tilt. All must match.
- **M4 — cascaded beams (level 2+):** secondary beams hang from
  pans of primary beams. The pan acts as the secondary beam's
  pivot. The primary beam's tilt **does not** directly affect
  the secondary's torque, but it determines the secondary's
  **physical position** in the visual layout — the player still
  sees the cascade swing as a connected mobile.
  Importantly, a secondary beam's two pans contribute to neither
  the primary beam's torque (the primary beam treats the
  secondary as a fixed-mass pendant) — this prevents nasty
  feedback loops while still letting the player solve a
  hierarchical tilt pattern.
- **M5 — sliding stones (level 3+):** a sliding stone on a pan
  migrates to the *opposite* pan of its beam every tick if the
  opposite pan is currently lower. If the beam is balanced
  (tilt = 0), the stone stays.
- **M6 — lock-pin (level 3+):** while locked, a beam's tilt is
  fixed at 0 regardless of torque. ACTION6 click toggles the
  lock. A locked beam still receives sliding-stone migrations,
  but the migration uses the locked beam's *intended* tilt
  (computed counterfactually) — so unlocking later releases the
  beam into a possibly-different state than the player expects.

## Per-level progression

### Level 1 — base balance (M1 + M2 + M3)
- One beam, two pans. Tray has 6 stones (mixed weights 1, 2, 3).
  Target tilt = +1. The player must select a subset whose right-
  side weight exceeds left-side weight by exactly 1.
- **Witness:** place stone-3 (weight 1) on left pan, stone-5
  (weight 2) on right pan. Tilt = +1. Total ~6 actions.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (cascaded beams)
- Three beams: beam-A (top), beam-B (hanging from A's right pan),
  beam-C (hanging from B's left pan). 9 stones in tray.
- Target: beam-A tilt +1, beam-B tilt -2, beam-C tilt 0. Each
  beam's tilt is independent of the others' tilts but visible as
  a cascading mobile, which makes spatial reasoning harder. The
  player must distribute weights across all three beams' pans
  while keeping each tilt at its target.
- **Witness:** ~14 actions across 3 beam placements. Step budget
  24.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (sliding) + M6 (lock-pin)
- Four beams in a deeper cascade. 12 stones, 2 of which are
  sliding. Two lock-pins, one on beam-A and one on beam-D.
- Target tilts: `(+2, 0, -1, +1)`. Sliding stones on the wrong
  beam will migrate each tick away from where the player wants
  them — UNLESS the beam is locked, in which case migration
  follows the *counterfactual unlock state*. This forces the
  player to reason about both current and counterfactual tilts
  every turn.
- The strategy is to lock the beams whose targets oppose
  natural sliding, place the sliding stones on the locked beam's
  pan that *would* be lower if unlocked (so they stay), and
  unlock at the right moment.
- **Witness:** ~30 actions. Step budget 50.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition

After every ACTION5 or completed placement, walk every beam.
Check `current_tilt == target_tilt`. If all match → `self.next_
level()`.

## Lose condition

`steps_used >= max_steps` → `self.lose()`. There is no instant-
fail; the system is fully reversible (stones can be returned to
tray as a free no-op for un-locked-in stones).

## Internal state

- `self.beams: list[Beam]` — `pivot_pos`, `left_pan_pos`,
  `right_pan_pos`, `tilt: int`, `target_tilt: int`,
  `parent_beam: int | None`, `parent_side: 'left'|'right'|None`,
  `locked: bool`.
- `self.stones: list[Stone]` — `weight`, `location: 'tray' |
  ('pan', beam_idx, side)`, `sliding: bool`.
- `self.lock_pins: list[(beam_idx, pin_pos)]`.
- `self.selected_stone: int | None` — first click of a placement.
- `self.tick: int`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `kx14 — tide-tilt-buoyant`**: kx14 is a vertical fluid
  tank where buoyant balls drift left/right on a tilt verb.
  Counterweight-beam is a *torque-balance* mobile — pans hanging
  from a beam, not balls floating in water — and the cascade of
  hanging beams forms a mobile, which kx14 does not.
- **vs `gg07 — stack-pillar-lift`**: stack-pillar moves blocks
  between fixed-height columns; counterweight-beam moves stones
  between *tilting* pans whose vertical position changes as a
  function of the contents.
- **vs `vn8d — domino-cascade-topple`**: cascade-topple is a
  threshold cascade through a planar graph; counterweight-beam
  is continuous torque on a hierarchical mobile.

## Step budget

- L1: 12.
- L2: 24.
- L3: 50.

## Random-resistance

Random placements are very unlikely to reach exact tilt targets:
on L3 with four beams, four targets, twelve stones, and two
locks, the joint probability of random play matching all targets
simultaneously is exponentially small. Sliding stones in
particular punish sloppy placement — they migrate to whichever
side is lower, ruining tilts that the player had set up.

## Planning depth

- **L1:** moderate — pick a subset that sums to the right delta.
- **L2:** deep — independent beams but limited stone supply;
  must allocate stones across beams to satisfy multiple targets.
- **L3:** very deep — sliding-stone migration depends on the
  *counterfactual* tilt of locked beams, so locking at the wrong
  moment has cascading effects.
