# gx7m — gear-mesh-cascade

## Summary
The player operates a cluster of toothed-disc gears positioned on a
fixed cardinal mesh-graph. Each disc carries a single coloured rim-
mark; the player clicks a disc's hub to rotate it 90° clockwise, and
the rotation propagates instantly through every mesh-connected
neighbour with the sign flipped, recursing through the connected
component. The puzzle is to drive every disc's mark onto its same-
coloured target indent printed on the static collar-ring framing it.
A ratchet disc (introduced at L2) is a one-way mechanism with two
states: a **yellow bolt sprite** floats above its collar with the
rod sliding between two positions — rod-down (engaged into the
gear, ratchet `LOCKED`) and rod-up (retracted, ratchet `CW` =
free to rotate, but only on a CW arrival). Clicking the bolt
toggles between the two positions. A clutch disc (L3) carries an
identical-shape bolt in purple; rod-down = engaged, rod-up =
disengaged. A disengaged clutch removes its mesh-edges entirely
and partitions the graph.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click. Dispatches by tag at click coords: `disc` → rotate +90° CW + cascade; `ratchet_bolt` → toggle owning ratchet's state (`LOCKED ↔ CW`) and redraw the bolt (yellow rod slides between bottom and top of its 5-cell sprite); `clutch_bolt` → toggle owning clutch's `engaged` boolean and redraw the bolt (purple rod slides). | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Mesh cascade rule (M1). | 3 plain discs in a row; targets all 180°. Witness `[ACTION6@(20,31), ACTION6@(20,31)]` (2 clicks of the same disc-hub double the rotation everywhere via parity-uniform cascade). |
| 2 | + Ratchet one-way gate (M2). | 3 discs (pink + ratchet-magenta + lblue) in a row; ratchet starts LOCKED (its yellow bolt rod sits at the bottom of the bolt sprite, visually engaged into the gear). Targets `(180°, 90°, 270°)` are not in the pure-cascade span; the bolt must be clicked once to retract the rod up (state CW = free-to-rotate-CW) so an R-hub click fires the asymmetric `(−1, +1, −1)` cascade, after which pink-hub clicks (with the ratchet still blocking CCW arrivals back from pink) finish pink. Witness `[ratchet-bolt(30,24), R-hub(30,31), pink(20,31), pink(20,31), pink(20,31)]` — 5 actions. |
| 3 | + Clutch engagement gate (M3). | 5 discs (pink, ratchet, lblue, clutch, orange) in a row; targets `(180°, 90°, 90°, 90°, 180°)`. Parity-0 deltas `(+2, +1, +2)` are non-uniform across pink/lblue/orange — solvable only by partitioning the mesh via clutch-disengage. The clutch's purple bolt sits at the bottom when engaged and slides up when disengaged; the ratchet's yellow bolt sits at the bottom when LOCKED and slides up when CW. Witness `[clutch-bolt(40,24), green-hub(40,31), orange-hub(50,31)×2, ratchet-bolt(20,24), R-hub(20,31), pink-hub(10,31)×3, lblue-hub(30,31)×2]` — 11 actions. |

## Win condition

After every `ACTION6` step, the game iterates over every disc and
compares `disc.rotation` to its level-data target rotation (in
degrees). When all match, `self.next_level()` fires; on the last
level the engine auto-fires `self.win()`.

## Lose condition

When `self._action_count >= step_budget` (read from
`level.get_data("StepBudget")`), `self.lose()` fires. Per-level
budgets: L1=20, L2=30, L3=50. No instant-fail collisions, no hazard
tiles — exhausting the step counter is the only failure mode.

## Internal state

- `disc_list: list[Sprite]` — every gear sprite in the level, sorted
  by `(x, y)` for deterministic ordering.
- `static_mesh: dict[Sprite, list[Sprite]]` — cardinal-adjacency
  mesh-graph computed once per `on_set_level`.
- `ratchet_dirs: dict[Sprite, str]` — per-ratchet state in
  `{"LOCKED", "CW"}`. Default `"LOCKED"`. (CCW state was dropped
  during refinement — it was never required by any witness, and a
  real-world ratchet is by definition a one-way mechanism.)
- `clutch_engaged: dict[Sprite, bool]` — per-clutch boolean. Default
  `True`.
- `bolt_owner: dict[Sprite, Sprite]` — each ratchet/clutch bolt
  sprite resolved to its owning disc by spatial offset
  (`bolt.x == disc.x + 2 and bolt.y == disc.y - 7`). The bolt is a
  1×5 vertical sprite floating above the collar's top frame, against
  the playfield background. It both shows the current state (rod at
  the bottom of the sprite when engaged, rod at the top when
  disengaged) AND serves as the click target for toggling it.
- `disc_targets: dict[Sprite, int]` — per-disc target rotation in
  degrees, read from level-data `"Targets"`.
- `step_budget: int` — read from `level.get_data("StepBudget")`.
- `_step_counter_ui: StepCounterHud` — depleting-bar HUD widget.

## Notable code patterns

- **BFS cascade with parity tracking** — the cascade is a BFS
  starting at the clicked disc; every visited disc carries a parity
  sign (+1 for the source, alternating −1/+1 across hops). Rotation
  delta is `90 if sign == +1 else 270`.
- **Live mesh-graph recomputed per click** — `_live_neighbors(disc)`
  filters the static adjacency by current clutch states: a
  disengaged clutch returns no neighbours, AND any neighbour that is
  itself a disengaged clutch is skipped. This makes
  partition-by-clutch a one-line predicate inside the BFS.
- **Ratchet gating in BFS** — when the BFS visits a ratchet,
  `direction == BLOCKED` or `sign != allowed_sign` short-circuits
  with `continue`, which causes the ratchet to neither rotate nor
  propagate further. Pure data-driven gating; no special-case dispatch
  per ratchet.
- **Bolt-as-click-target-and-state-display** — the ratchet bolt
  and clutch bolt are 1×5 vertical sprites floating one column
  east of the disc's left edge and seven rows above the disc's top
  edge (i.e., above the collar's top frame). Each bolt's coloured
  rod occupies 3 of the 5 cells; the rod's vertical position
  encodes the state, with the remaining 2 cells drawn in dim grey
  as a "track" so the click target stays a stable bounding box.
  Engaged → rod at the bottom 3 cells (visually extending toward
  the disc); disengaged → rod at the top 3 cells (retracted). The
  same sprite both shows the state (via mutable pixels —
  `bolt.pixels[i, 0] = colour`) and accepts the click that toggles
  it, so every state change is reflected in a per-pixel visual
  update on the sprite the player just clicked. Mirrors the
  universal mechanical metaphor of a deadbolt or circuit-breaker.
- **Pre-enumerated 256-cell ACTION6 grid** — `_get_valid_actions`
  returns every `(x, y)` for `x, y ∈ 0..63 step 4`, per the `r11l`
  convention. The agent always sees the same 256 quantised click
  cells; useful clicks are 7 out of 256 per level (yielding strong
  random-resistance for the §3.5 graph check).
