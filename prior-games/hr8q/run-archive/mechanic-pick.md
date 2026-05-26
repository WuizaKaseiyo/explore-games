# mechanic-pick

## Game ID
`hr8q`

- 4 lowercase chars, alphanumeric (`h`, `r`, `8`, `q`).
- Not in the 25 reference IDs.
- Not in `prior-games/index.md` (current rows: kf42, qz73, kx14, qb84, lq5x, gv47).
- Not a recognisable English word.

## Mechanic family tag
`pair-blend-recipe`

## One-paragraph description

A right-side **palette panel** holds a small set of distinctly-coloured
square ingredient blocks; a left-side **formula panel** holds two
empty input slots side-by-side and a result slot below them.
Above the formula sits a single target-preview block whose colour is
the puzzle's current goal. The player has no avatar. Each ACTION6
click on an ingredient marks it "selected" (outlined with a contrast
ring) and copies its colour into the next empty input slot; once
both input slots are full the result slot is auto-filled by looking
up the unordered colour-pair in the level's `mix_table`. ACTION5 is
the **commit** verb: if the result colour equals the current target,
the target is consumed (advance to the next target or win the
level); if not, the formula clears (no penalty in L1). At L2 a queue
of multiple targets must be produced in some order; at L3 each
ingredient block has a small **use-counter pip** beneath it that
decrements on commit, and a wrong commit-order can permanently
exhaust an ingredient required by a later target — making the order
of commits load-bearing. The player draws on **objectness** (each
ingredient is a coherent, persistent click-target) and **basic
geometry/topology** (the input/result slot triple is a discoverable
spatial syntax: position-1 + position-2 → result). Mechanics are
fully discoverable from the visual layout — no on-screen text.

## Action set (preview)
`available_actions = [5, 6]`.

- ACTION6: click. Hits an ingredient block → fills next empty input
  slot AND visually marks the ingredient as "selected". A second
  click on a different ingredient (or the same one — repeats are
  legal) fills the second slot. A click on a slot itself clears
  that slot. A click anywhere else is a no-op (still costs a step).
- ACTION5: commit. If both slots are full, look up the result; if
  it matches the current target, target is consumed. Otherwise the
  two slots clear and ingredients un-mark; depletion (L3 only) is
  applied **only on a successful commit**.

## Novelty check (positive)

### Closest taxonomy near-misses

- **sb26 — tile-place-commit** (Mastermind-style guess+feedback).
  Surface overlap: a row of palette tiles on one side, slots on the
  other, ACTION5 commit verb, ACTION6 click-to-place. **Concrete
  distinguishing rule**: sb26 is a *guess-with-per-slot-feedback*
  game where the player iterates by reading "right colour right
  position / right colour wrong position / wrong" feedback over
  multiple commits to converge on a hidden sequence. hr8q has NO
  hidden sequence and NO per-slot feedback — the formula evaluates
  deterministically and visibly under a level-printed mix table; the
  difficulty is *which pair-and-order to use given limited
  ingredient uses*, not "what is the hidden code". Win is "produced
  this rendered colour" (visible match), not "guessed this hidden
  string".

- **su15 — recipe-fruit-collect**. Surface overlap: word "recipe", a
  target the player must satisfy by combining coloured tokens.
  **Concrete distinguishing rule**: su15 is a spatial radial-blast
  game where clicks vacuum nearby fruits at the click point on a
  16×14 cell arena, with patrolling enemies that fail the blast on
  contact. hr8q has no spatial arena, no avatar, no movement, no
  enemies — every click hits an ingredient block in a static
  palette. su15's "recipe" is *quantity per colour* (collect N
  flavour-X); hr8q's recipe is *unordered pair → output*.

- **tn36 — program-pawn-trace**. Surface overlap: click button
  sequence to compose a thing, then commit. **Concrete distinguishing
  rule**: tn36 composes a sequence of *move-and-rotate instructions*
  for a programmable pawn, then runs the programme and traces a
  path on the canvas. hr8q has no pawn, no path, no canvas; the
  composed object is a single output colour, not a path.

- **cd82 — orbit-fire-paint**, **dc22 — colour-cycle-walk**, **gv47
  (prior) — seed-grow-surround-dissolve**. All three involve
  colour-transformation but each is **spatial canvas painting**
  with cells that change colour by rule. hr8q has zero painted
  cells — colour transformation is purely an inventory→output
  operation in a fixed three-slot formula. (Detailed gv47
  comparison in next section.)

### Closest prior-games near-miss: **gv47**

`prior-games/index.md` row: `gv47 | seed-grow-surround-dissolve |
... ACTION5 globally mixes contacting region pairs into a derived
colour.`

This is the load-bearing novelty hazard; gv47's deeper view in
`prior-games/gv47/mechanism-detail.md` confirms ACTION5 mixes
*colour-pair → output colour* using a level-defined `mix_table` —
exactly the same combinatorial primitive hr8q uses.

**Concrete distinguishing rule (specific & testable):**

- **What is on the board.** gv47 has a 12×12 *spatial paint canvas*
  with seed sprites that grow connected coloured regions; pip
  targets must be *surrounded* (Chebyshev-1 ring fully painted) to
  be dissolved. hr8q has NO grid-as-canvas: ingredients are static
  blocks in a palette panel, and the playfield is a fixed 3-slot
  formula widget. There is no concept of "growth", "region",
  "surround", or "Chebyshev neighbourhood" anywhere in hr8q.
- **What the input verb does.** gv47's ACTION6 grows the clicked
  seed's region by one cardinal ring of cells; gv47's ACTION5 fires
  a global mix scanning *all currently-contacting region pairs* and
  fusing those whose pair is in `mix_table`. hr8q's ACTION6 puts
  one ingredient colour into one input slot of the formula; hr8q's
  ACTION5 commits the formula's *single* output against the
  *single* current target.
- **What the level asks for.** gv47 wins when every black-ringed pip
  is dissolved by surrounding paint of the matching colour. hr8q
  wins when every queued target colour has been produced via the
  formula and committed. There is no "surround", no "ring", no
  "region adjacency" predicate in hr8q.
- **Sequencing constraint.** gv47's ordering constraint is
  *spatial*: dissolve a single-colour pip BEFORE that colour's
  region participates in a mix or you lose access to that pip's
  colour. hr8q's ordering constraint (introduced at L3) is
  *budgetary*: each ingredient has a finite use-count, and using
  ingredient X for target T1 may exhaust X for target T2 — the
  binding constraint is integer arithmetic on use counts, not
  region adjacency.

In short: gv47 is *paint-the-cells-around-the-pip-with-the-right-
mixed-colour-on-a-grid*. hr8q is *pick-the-right-pair-to-blend-then-
commit-against-each-target-without-running-out-of-ingredients*. The
shared atom is "two colours blend into one"; the games surrounding
that atom are completely different.

## Negative similarity check (visual / dynamic clone test)

Walking the eight dimensions in `negative-similarity-check.md`
against gv47 (the most-overlapping prior):

1. **What is on the board.** gv47: paint canvas + seeds + pips +
   walls. hr8q: split-screen — a palette panel + a 3-slot formula
   widget + a target-preview chip. **DIVERGENT.**
2. **What the player physically does.** gv47: click a seed to grow
   a region; ACTION5 to mix-by-contact. hr8q: click ingredients to
   fill formula slots; ACTION5 to commit a single recipe.
   **DIVERGENT** (selection+commit vs. region-grow+global-mix).
3. **What the level asks for.** gv47: dissolve every pip by
   surround-paint. hr8q: produce every target colour via blends.
   **DIVERGENT**.
4. **What kills the player.** Both: step counter. **SHARED** (this
   alone is universal across the corpus and per the cautionary tale
   does not count toward overlap).
5. **Cast of supporting elements.** gv47: walls, seeds, pips, paint
   sprites, target rings. hr8q: ingredient blocks, slot frames,
   target preview chip, use-counter pips (L3). **DIVERGENT**.
6. **Visible visual signature.** gv47 fills large connected paint
   regions across a 12×12 canvas; the dominant frame is "blobs of
   yellow/blue/red on grey". hr8q's frame is geometric: a vertical
   divider splits the screen, the right side is a 2×3 (or 2×4)
   grid of small same-size ingredient squares, the left side is a
   `[slot]+[slot]=[result]` widget with a labelled target chip
   above. Almost no surface overlap with gv47's painted-canvas
   look. **DIVERGENT.**
7. **Pixel grain of primary sprites.** gv47's primary sprites are
   ~3×3 seed icons sitting on top of large paint regions; hr8q's
   primary sprites are 6×6 (or 7×7) outlined ingredient blocks
   with a 1-pixel selection ring and a 1-cell use-counter dot.
   **DIVERGENT** — different cell density.
8. **Core dynamic.** gv47: spatial coverage planning under a
   contact-graph mix rule. hr8q: combinatorial recipe scheduling
   under finite ingredient supply. **DIVERGENT** (puzzle category
   is fundamentally different — the player thinks in graphs and
   adjacencies in gv47; in tabular arithmetic over a recipe lookup
   in hr8q).

Shared dimension count vs gv47: 1/8 (only #4, the universal step
counter). Threshold for rejection is 3+. **PASS.**

Walks against the next-closest priors:

- **sb26**: shares (2) click-to-select-then-commit, (3) "match a
  visible spec on a slot widget", (4) step-counter — but loses on
  (1) (sb26 has multiple-row guess board with feedback paint), (5)
  (no use-counters; sb26 has hint-feedback animations), (6)/(7)
  (sb26's per-slot hint stripes give a totally different look),
  (8) (sb26's core dynamic is search-with-feedback; hr8q has no
  hidden information). 2/8. **PASS.**
- **kf42 / kx14 / qb84 / lq5x / qz73 (other priors)**: none are
  formula games; surface overlap is just the ubiquitous step-counter.
  **PASS.**

Verdict: hr8q is **NOVEL** under both the positive similarity check
and the negative similarity check.

## Prior categories used

Per `core-knowledge-priors.md`:

- **Objectness** (#1): each ingredient is a persistent click-target
  with a "selected" state; the formula's two input slots and the
  result slot persist as discrete object-bearing positions; the
  target preview is a coherent object that disappears on a
  successful commit.
- **Basic geometry / topology** (#2): the input slots are
  positioned to read as "inputs" with the result block as their
  combination; the spatial relationship between *the two filled
  slots* and *the result slot* is the discoverable syntax of the
  formula widget. The "(slot, slot) → result" topology IS the
  mechanic's visible representation.

No physics or agentness used; that's intentional — the puzzle is
purely combinatorial under a small ruleset.

## Why this fits NovaPlay §3.4

- **Multi-mechanic** (≥2): pair-blend (L1) + multi-target queue (L2)
  + ingredient depletion / order-matters (L3). Three distinct
  mechanics; each level adds exactly one and previous-level
  mechanics carry forward.
- **Composition over scale**: L3 is NOT a bigger palette of L2; L3
  introduces *finite ingredient inventory*, which makes the
  *ordering of L2's commits* matter for the first time. Swapping
  two L3 commits can break the level. Strict deeper sequencing.
- **No on-screen text, no symbols, no clipart, no cultural
  conventions**. The formula widget's `[a]+[b]=[c]` reading is
  purely topological — three same-size slots with the upper two
  visually adjacent and the lower one offset; no "+", "=", or
  arrow glyphs.
- **Goal discoverable** from the layout: a target-coloured chip is
  visibly displayed; clicking ingredients fills slots; a result
  appears. The player learns the verb in two clicks and the goal
  in one frame.
- **Determinism**: the mix table is fixed per level; commits are
  pure functions of the current formula and target.
- **Action efficiency**: L1 witness ≈ 3 actions; L2 ≈ 8; L3 ≈ 12.
  All comfortably within `5×` human-baseline budgets.
