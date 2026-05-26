# Game generation final report — Run #3

## Generated game

- **ID**: tw94
- **Class**: `Tw94` (Pascal-case: first letter caps, digits preserved)
- **Source**: `prior-games/tw94/tw94.py`
- **Metadata**: `prior-games/tw94/metadata.json`
- **Lines of code**: ~290

## Mechanic

The grid is a torus. Walking or pushing a crate off one edge re-enters from the opposite edge — subject to per-level wrap rules. Walls in the playfield block direct paths, forcing the player to deliver crates via the wrap-edge route. L1 has only horizontal (east-west) wrap; L2 adds vertical wrap, making the field a full 2D torus; L3 restricts wrap to EVEN-numbered rows and cols (odd rows/cols become hard boundaries). The player learns wrap rules by trial and by visual pip indicators at wrappable-edge cells. Win = every target covered by a crate.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1-4 | Walk player one cell in cardinal direction; if walking into a crate, push it one cell forward |

`available_actions = [1, 2, 3, 4]`. ACTION5/6/7 unused.

## Levels

- **L1** (8×8): introduces M1 horizontal wrap. Single crate, single target; wall at (2,4) blocks direct west push; delivery requires east-wrap (5 ACTION4).
- **L2** (12×12): introduces M2 vertical wrap. Two crates each requiring different-axis wrap (east-wrap for crate_a, south-wrap for crate_b). Witness ~29 actions.
- **L3** (14×14): introduces M3 row-parity wrap. Same crate setup as L2 but only even rows/cols wrap; all crates placed on even rows/cols (so witness still works); pip indicators only at even-row/col edges to teach the parity rule. Witness ~33 actions.

## Novelty note

- Closest taxonomy: vc33 (row-slide-pull-tab). Distinguishing rule: vc33 *slides* a row of pieces atomically; tw94 has standard sokoban motion with toroidal grid topology. Different mechanism class.
- Closest prior: none — no toroidal/wrap topology in 28-game corpus.

## Index update

Appended row to `prior-games/index.md`:

```
| tw94 | toroidal-wrap-playfield | Toroidal Wrap Playfield — grid is a torus; pushing crates off one edge re-enters from opposite edge; L1 horizontal wrap, L2 +vertical, L3 row-parity (only even rows/cols wrap). | 2026-05-08T17:17:14Z | (autonomous) |
```

## Run notes

- **All 11 universal checks PASS** (CHECK_VISUAL_SANITY skipped — manual). Including the new **CHECK_TRIVIAL_FAILS**: trivial heuristics for L2 (`[ACTION4 × 30]`) and L3 (`[ACTION4 × 35]`) both fail to advance their levels, confirming planning depth.
- **3 custom checks PASS**: horizontal wrap works at L1; L3 odd row 1 doesn't wrap (boundary blocks); L3 even row 0 wraps.
- **Pascal-case fix**: this run's class is `Tw94` (T capitalized; `94` is digits — no case ambiguity). The previous run #2 had a class-naming bug (`Vy3M` vs expected `Vy3m`) that the harness loader caught — this run avoided that pitfall by choosing an ID with all-digit suffix.
- **L3 design tradeoff**: M3 (row-parity wrap) is *visible* (via pip-only-at-even-edges) but not *strictly counterfactual* in the witness — the witness uses crates already on even rows/cols, so it doesn't actually exercise the parity restriction. A stricter L3 design with an additional crate on an odd row was prototyped but the layout didn't converge; deferred. The check that does fire: at L3 walking off boundary on an odd row IS blocked (custom check verifies), so the rule is implemented and visually communicated, just not behaviorally required by L1+L2-carried witnesses alone.
- **Total run time**: ~30 minutes.
