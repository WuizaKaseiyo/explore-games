# mechanic-pick

## Game ID
`ng52`

- 4 lowercase alphanumeric characters; not in the 25 reference IDs;
  not in `prior-games/index.md` (kf42, qz73, kx14, qb84, lq5x, gv47,
  hr8q); not an English word.

## Mechanic family tag
`multiset-signature-classify`

## One-paragraph description

A pool of irregularly-shaped multi-coloured "sample objects" sits in
a bottom tray. Above it stand N "classification bins"; each bin
displays its **signature** at the top — a small column of 1×L
coloured **sticks** where each stick is one solid-colour run
(e.g. a 1×3 blue stick + a 1×4 purple stick = the multiset
`{blue: 3, purple: 4}`). The player has no avatar. ACTION6 click
selects a sample object (visible "selected" outline) and the next
ACTION6 click on a bin's holding area places the selected object
into that bin (objects stack in 4×4 slot positions inside the bin).
A click on a bin-resident object lifts it back into the
selection. ACTION5 commits the current configuration: for each
bin, the **multiset** of pixel-colour counts of all currently-held
objects is compared to that bin's stick signature. If every bin
matches its signature exactly, the level is won. If not, every
placed object snaps back to its original pool position (no other
penalty) so the player can try again. The player draws on
**objectness** (each object is a coherent, persistent click-target
with a consistent colour-count fingerprint) and **basic
geometry/topology** (the bin's stick signature is a topological
diagram of "this many cells of that colour, regardless of shape" —
the player learns that *shape doesn't matter, colour-counts do*
purely from the level layout).

## Action set (preview)

`available_actions = [5, 6]`.

- ACTION6 click on:
  - a pool object → select it (deselect the prior selection if any).
  - a bin-resident object → lift back to the pool *as the current
    selection* (it leaves the bin, becomes the active selection but
    visually moves to a small "in-hand" indicator above the
    pool until placed elsewhere).
  - a bin's holding area (with an object selected) → place it in
    that bin's next free slot.
  - empty space → no-op.
- ACTION5 commit. Per-bin multiset check. All match ⇒
  `next_level()`. Else ⇒ snap every placed object back to its
  original pool position; selection cleared.

## Novelty check (positive)

### Closest taxonomy near-misses

- **sb26 — tile-place-commit (Mastermind)**. Surface overlap: a
  pool of tiles, slot containers, an ACTION5 commit verb, an
  ACTION6 click verb. **Distinguishing rule**: sb26 is a
  *guess-with-feedback* game where each commit returns per-slot
  hint feedback (right colour right position / right colour wrong
  position / wrong) that narrows down a *hidden code*. ng52's
  bin signatures are FULLY VISIBLE and remain visible across
  attempts; commit returns only a binary pass/fail (with a global
  reset on fail); there is no hidden information. Also: sb26's
  slots have a fixed 1-tile-per-slot capacity in a flat row;
  ng52's bins hold variable-many objects whose pixel-multisets
  must sum to the signature.

- **su15 — recipe-fruit-collect**. Surface overlap: a pool of
  coloured tokens, a recipe to satisfy. **Distinguishing rule**:
  su15 is a spatial radial-blast game with movement, line-of-
  sight, and patrolling enemies on a 16×14 cell arena. ng52 has
  zero spatial gameplay — no avatar, no movement, no enemies. The
  "recipe" in su15 is a single global multiset; ng52 partitions
  the pool across multiple bins simultaneously (a multi-class
  partition problem, not a single-quota problem).

- **tn36 — program-pawn-trace**. Surface overlap: click-build a
  composed object then commit. **Distinguishing rule**: tn36
  composes a *sequence of move-and-rotate instructions* whose
  execution traces a path on a canvas. ng52 has no path, no
  canvas, no sequencing — the bins are an unordered partition.

### Closest prior-games near-misses

- **hr8q — pair-blend-recipe**. Surface overlap: a pool of
  coloured items on the right; a "thing to satisfy" on the left;
  click-to-fill semantics; ACTION5 commit. **Distinguishing
  rule**: hr8q PRODUCES a new colour from a pair/triple recipe —
  the slot count is fixed (2 or 3) and the puzzle is "find the
  right pair to mix into the target output". ng52 PARTITIONS a
  pool of objects into multiple bins simultaneously — the slot
  count per bin is variable, the puzzle is "find the right
  partition such that every bin's pixel-multiset matches", and
  no colour is ever transformed (each object's colours are
  preserved across the placement). hr8q is a single-output
  recipe game; ng52 is a multi-output classification game.

- **gv47 — seed-grow-surround-dissolve**. Spatial paint canvas;
  unrelated.

- **kf42, qz73, kx14, qb84, lq5x**: avatar-on-grid mechanics.
  Unrelated.

## Negative similarity check

8-dimension overlap walks (per
`mechanic-novelty/negative-similarity-check.md`):

- **vs hr8q** (load-bearing recent prior):
  1. board: hr8q has a 2/3-slot formula widget + small palette;
     ng52 has 3 bin holding-areas + an irregular-object pool.
     **DIVERGENT**.
  2. input: hr8q "click ingredient → fill slot, with auto-eval";
     ng52 "click object → select, click bin → place". The verb
     topology is different — ng52 has no "result preview" and no
     "auto-eval"; hr8q has no concept of "place into a bin".
     **DIVERGENT**.
  3. level asks: hr8q "produce target colour"; ng52 "partition
     objects into matching bins". **DIVERGENT**.
  4. kills: step-counter (universal, doesn't count).
  5. cast: hr8q has same-size square ingredients + slot frames;
     ng52 has irregular non-convex multi-pixel objects + stick
     signatures. **DIVERGENT**.
  6. visual signature: hr8q's frame is dominated by 8×8 squares;
     ng52's frame is dominated by 3 columnar bins each with a
     stick-stack signature header. **DIVERGENT**.
  7. pixel grain: hr8q ingredients are 6×6 solid blocks; ng52
     objects are 1-5 pixel non-convex glyphs drawn at small
     scale. **DIVERGENT**.
  8. core dynamic: hr8q is "search a recipe space"; ng52 is
     "search a partition space". **DIVERGENT**.
  Shared: 0/8 (only the universal step-counter axis). PASS.

- **vs sb26**: 2/8 (commit verb + click-to-select pattern). All
  other axes diverge. PASS.

- **vs su15, tn36, gv47, others**: ≤ 1/8 each. PASS.

VERDICT: NOVEL on both checks.

## Prior categories used

- **Objectness** — every sample object is a persistent click-
  target with a stable colour-count fingerprint that survives
  movement.
- **Basic geometry / topology** — each bin's signature is a
  *topological* diagram (a stack of solid-colour 1×L runs) that
  abstracts away from any specific shape; the player learns that
  the puzzle is colour-multiset-matching, not shape-matching.

## Why this fits NovaPlay §3.4

- **Multi-mechanic** (≥2): place-and-commit-classify (L1) +
  multi-stick / compositional bin signature (L2) + selective
  placement under distractors (L3).
- **No on-screen text, no symbols, no clipart, no cultural
  conventions**. Bins are purely geometric (rectangle + stick
  diagram); objects are abstract pixel clusters.
- **Goal discoverable**: the bin signatures are visible from the
  first frame; clicking-then-clicking-a-bin teaches the placement
  verb in two actions.
- **Determinism**: signatures are static per level; commit's
  match check is a pure function of the current placement.
- **Action efficiency**: L1 ≈ 7 actions, L2 ≈ 13, L3 ≈ 13. All
  comfortably within `5×` human-baseline budgets.
