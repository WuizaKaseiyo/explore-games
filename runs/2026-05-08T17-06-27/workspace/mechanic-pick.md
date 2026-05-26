# mechanic-pick — Run #3

## ID

**`tw94`** — verified not in 25-ref reserved list, not in `prior-games/index.md` (28 entries incl. ej4t + vy3m), not a recognisable English word.

**Pascal class name**: **`Tw94`** — first letter capitalised, "94" preserved (no letter-case ambiguity since trailing `4` is a digit).

## Mechanic family tag

**`toroidal-wrap-playfield`**

## One-paragraph description

The grid is a torus: walking off one edge re-enters from the opposite edge. Pushing a crate off an edge wraps it similarly. Walls in the playfield can block direct paths, forcing the player to deliver crates via the wrap-edge route. **Mechanic 1 (L1)** is *horizontal wrap* — only east-west wraps; vertical boundaries are hard walls. **Mechanic 2 (L2)** adds *vertical wrap* — north-south boundaries also wrap, making the playfield a full 2D torus. **Mechanic 3 (L3)** adds *row-parity wrap* — only EVEN-numbered rows wrap horizontally and only EVEN-numbered columns wrap vertically; odd rows and odd cols have hard boundaries. Player must reason about which row/col to use for wrap-based delivery.

## Distinguishing rules

- **No prior game** in the 28-game corpus uses toroidal/wrap topology. Closest distant taxonomy entry: `vc33` (row-slide-pull-tab) — slides rows but does NOT wrap; this candidate's wrap is a topological property of the grid, not a row-slide action.
- §3.4 commercial ceiling: `wrappingrecipe` is a PuzzleScript demo. Snake-clone games and some Atari titles use toroidal wrap as ambient mechanic, but no major commercial puzzle game makes wrap-discipline the core puzzle dimension. Distinguishing rule: this candidate makes wrap *required* for delivery (counterfactually) and adds row-parity selectivity at L3, neither of which appears in standard toroidal-wrap commercial puzzles.

## Negative-similarity check (7-dim)

vs `vc33` (closest): shared on dim 4 (step budget — universal). 1 dim shared, well under 3-dim threshold.

vs all other 28 priors: ≤ 2 shared dims each (mostly just dim 4 universal).

**Verdict: NOVEL.**

## Inspiration source

PuzzleScript demo `wrappingrecipe.txt` (increpare/PuzzleScript). The demo's single-rule core (player wraps around playfield edges) is composed here into a 3-level progression by adding vertical wrap at L2 and row-parity selectivity at L3.

## Action mapping (preview)

`available_actions = [1, 2, 3, 4]` — pure cardinal motion. Walking into a crate triggers push; push wraps if boundary crossed AND wrap is enabled for that axis at that row/col (L1: H wrap always; L2: H + V wrap always; L3: H wrap only on even rows, V wrap only on even cols).

## Per-level grid sizes (preview)

- L1: 8×8
- L2: 12×12
- L3: 14×14

## Considered alternatives (rejected)

- **companion-reflex-pair** (byyourside): too close to m0r0 (mirror-orb-merge) on visual signature.
- **chained-segment-arm** (robotarm): kinematic implementation complexity.
- **atom-bond** (sokobond): too close to cn04 (nub-pair-glyph) on win-condition family.
