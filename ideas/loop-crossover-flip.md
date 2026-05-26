# Loop-Crossover-Flip — *Braid-Strand-Weave*

## Summary

Three to five thick coloured **rope strands** snake across the
playfield as continuous chains of cell-segments. Where two strands
visit the same cell from perpendicular axes the cell is a **crossing**;
one strand is drawn **over** (full thickness, plus a 1-pixel highlight
along the visible edge to fake depth), the other is drawn **under**
(two stub half-segments with a 1-pixel gap and a darker shade where
the over-strand crosses).

The player has one verb: ACTION6 click on a crossing flips which
strand is over. The level wins when every crossing's over-strand
matches the level's target signature **and** every strand's tension
counter is ≤ its breaking threshold (L3 only).

## Visual elements (distinct from prior corpus)

- 64×64 canvas; the playable board is a 13×13 logical grid rendered
  at CELL=4 px so each strand visibly fills a chunky 3-pixel-thick
  ribbon (not a 1-pixel line). Background is canvas-cream (palette 9
  light, roughened to two-tone for a textile look).
- Each strand carries its own palette colour (e.g. crimson, ochre,
  teal, navy). A 1-pixel **highlight stripe** runs along the
  *northwest* edge of every "over" segment; a 1-pixel **shadow
  stripe** runs along the southeast edge of every "under" segment.
  This gives the illusion of depth — over-strands appear raised;
  under-strands appear recessed.
- Crossings are visibly raised pixels at the *over* strand's centre
  (one pixel brighter than the strand's body colour) and a 1-pixel
  gap on the *under* strand on each side of the crossing cell.
- Where the original spec showed the target as bars in the corner,
  the revised version shows the target as a **miniature woven
  tapestry icon** in a 12×12 inset on the right rim — an actual scaled
  rendering of the desired weave, with the same shading rules. The
  player solves by visual matching, not by reading bar codes.
- L2+ adds a **bleed indicator**: each strand carries a thin colour
  bar along the bottom HUD; if a strand has been "bled", the bar
  shows an alternating-colour stripe (its current carried colour).
- L3+ adds **tension pips** stacked above each strand's HUD bar —
  one filled pip per ACTION6 click on a crossing the strand
  participates in. Filled pips turn red as they approach the snap
  threshold.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click cell `(x, y)`. If the click resolves to a crossing cell, flip its over/under designation. Updates bleed (L2+) and tension (L3+) bookkeeping. | always |

`available_actions = [6]`. No avatar.

## Mechanics enumeration

- **M1 — crossing-flip:** ACTION6 click on a crossing flips the
  over/under at that crossing.
- **M2 — match-target-tapestry:** the win predicate compares each
  crossing's `over_strand_id` to the level's target.
- **M3 — strain-bleed (level 2+):** when a crossing is flipped, the
  strand that newly *passes over* the other one **bleeds 1 unit of
  colour** into the under-strand for the rest of the under-strand
  past the crossing (in visit order). Bleed is cumulative —
  multiple bleeds re-tint a strand. Each strand stores a current
  *colour-load*: a stack of (donor_strand, count) entries. The win
  predicate now requires both the over/under signature AND each
  strand's colour-load to match the level's target colour-load
  spec.
- **M4 — tension-snap (level 3+):** every flip increments tension
  on each strand involved by `+1`. A strand whose tension reaches
  its snap threshold (level data, typically 5–7) **snaps**: the
  strand renders frayed and the level instantly fails. Tension
  decreases by 1 per turn ONLY when the player clicks a non-
  crossing rope cell (a "smooth" click that consumes a step but
  does no flip). This produces a *click-economy*: untangling
  forces the player to interleave smoothing clicks with flips.

## Per-level progression

### Level 1 — base weave (M1 + M2)
- Three strands (crimson, ochre, teal) interlace in a Celtic-knot
  pattern with **8 crossings**. The starting over/under signature
  is exactly inverted from the target (every crossing is wrong).
- The target tapestry icon shows the desired knot in the right
  inset. The player must flip each crossing once.
- **Witness:** click each of the 8 crossings in any order — 8
  steps. Step budget 12.
- **Mechanics required:** M1, M2.

### Level 2 — + M3 (strain bleed) and routed colour-mix
- Four strands (add navy) with **14 crossings** in a basket-weave
  pattern. The target spec includes BOTH a target signature AND a
  required final colour-load on each strand (e.g. crimson must end
  with one ochre bleed; navy must end clean).
- A flip routes colour. Naively flipping every wrong crossing
  produces too many bleeds. The player must find an *order* of flips
  that ends with the correct bleed counts (some flips cancel
  bleeds because the donor strand's identity changes after a prior
  flip).
- **Witness:** specific 18-flip sequence; step budget 25.
- **Mechanics required:** M1, M2, M3.

### Level 3 — + M4 (tension-snap) and forced economy
- Five strands; **22 crossings** in a complex over-and-under cable
  pattern. Every strand has a tension threshold of 6, except the
  central strand (threshold 4) — the player cannot solve this by
  rapidly fixing the centre.
- The player must:
  (a) plan flip order that ends with correct over/under + correct
      bleed-load (composition of L1 + L2)
  (b) interleave **smooth clicks** on non-crossing rope cells to
      decay tension on critical strands before they snap, AND
  (c) front-load flips on robust strands first so the centre's
      tension stays under threshold.
- Step budget 60. Witness sequence has ~30 flips and ~20 smooth
  clicks; the remaining 10 are slack for exploration.
- **Mechanics required:** M1, M2, M3, M4.

## Win condition

After every ACTION6 click that resolves to a flip, walk every
crossing. For each, check `current_over_strand == target_over_strand`.
On L2+, also check each strand's colour-load matches its target. If
all checks pass and (L3+) no strand has snapped, fire
`self.next_level()`.

## Lose condition

- `steps_used >= max_steps` → `self.lose()`.
- L3+: any strand reaching its tension threshold → `self.lose()`
  with a 1-second frayed-rope render before the end-of-level frame.

## Internal state

- `self.strands: list[Strand]` — each strand has `colour: int`,
  `cells: list[(int, int)]` (visit order), `tension: int`,
  `tension_threshold: int`, `colour_load: list[(donor, count)]`,
  `snapped: bool`.
- `self.crossings: list[Crossing]` — each crossing has `pos`,
  `strand_a`, `strand_b`, `index_a`, `index_b`, `over_is_a: bool`.
- `self.target_signature: dict[Crossing, bool]`.
- `self.target_load: dict[Strand, list[(donor, count)]]` (L2+).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `gg09 — gear-mesh-spin`**: gear-mesh propagates rotation
  through a graph; click-flip-with-bleed flips a binary state at
  one cell with downstream colour bleed. Strain-bleed is a *colour
  carrier*, not a rotation graph.
- **vs `gg08 — row-flip-mirror`**: row-flip reflects whole rows of
  fixed-position tiles; braid-strand-weave flips at *one cell* and
  changes a layered topology, not a 1D reflection.
- **vs `gg13 — chromatic-drip-labyrinth`**: drip mixes carried
  colour by passing through pigment wells under player movement.
  Strain-bleed mixes carried colour by *flipping a topological
  crossing*, not by walking.

## Step budget

- L1: 12.
- L2: 25.
- L3: 60.

## Random-resistance

A random clicker has a `~1/N` chance per click to flip the
right crossing in the right direction; for N=22 crossings on L3
with bleed-load and tension constraints, random clicks essentially
never converge. L3 in particular punishes random play — random
flips run out the tension budget on the central strand within a
few turns.

## Planning depth

- **L1:** shallow — visual matching, eight independent flips.
- **L2:** moderate — flip order matters because each flip routes
  colour through downstream segments. Solving requires reasoning
  about *which flip cancels which bleed*.
- **L3:** deep — three coupled constraints (signature + load +
  tension) under a step economy. Every flip costs both budget AND
  tension on at least two strands; the player must interleave
  smoothing clicks to keep the centre alive.
