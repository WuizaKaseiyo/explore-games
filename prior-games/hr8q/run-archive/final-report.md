# Game generation final report

## Generated game
- **ID**: hr8q
- **Source**: `prior-games/hr8q/hr8q.py`
- **Metadata**: `prior-games/hr8q/metadata.json`
- **Lines of code**: 729

## Mechanic

The player sees a small target colour chip on the left, two empty
input slots beneath it, and a result slot below those. A column of
distinctly-coloured ingredient blocks sits on the right; a visible
mix-rule strip at the bottom shows each level's recipes
diagrammatically. Clicking an ingredient (ACTION6) fills the next
empty input slot; once both are filled the result is auto-displayed.
ACTION5 commits the formula: a result that matches the target chip
consumes the chip and advances the level; a result that doesn't
match is distilled back into the palette as a new one-shot
intermediate ingredient. L1 introduces the pair-blend-and-commit
verb. L2 adds chained recipes — the target is now reachable only by
distilling an intermediate via a mismatched commit, then using that
intermediate in a second commit. L3 adds a third visible input
slot, enabling triple-arity recipes; the target is reachable only
by combining a distilled intermediate with two primary ingredients
in a 3-slot commit.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Commit the current formula. With 2 slots filled, looks up the unordered pair against the level's pair-mix table; with 3 (L3 only) looks up the unordered triple. Match → consume target. Valid mismatch → distil as new intermediate. Invalid → clear slots. Empty/under-filled → no-op. |
| ACTION6 | Click at (x, y). Hits an ingredient block → fills next empty slot with its colour and toggles its selection ring. Hits a slot frame → clears that slot. Anywhere else → no-op. Each action consumes one step from the budget. |

## Levels

- **L1** — pair-blend-and-commit. Two ingredients (magenta, light-blue), one target (purple). 3-action witness. Step budget 30.
- **L2** — + intermediate-as-ingredient (chained recipe). Three ingredients (magenta, light-blue, pink), one target (maroon) reachable only by first distilling purple via a mismatched commit, then committing (purple, pink). 6-action witness. Step budget 50.
- **L3** — + three-input formula (third visible slot). Four ingredients (magenta, light-blue, pink, yellow), one target (blue) reachable only by distilling purple via a 2-slot commit and then firing a 3-slot commit (purple, pink, yellow). A decoy triple (magenta, light-blue, yellow) → green is also visible in the mix-rule HUD. 7-action witness. Step budget 60.

## Novelty note

- **Closest taxonomy entry**: sb26 (tile-place-commit, Mastermind-style guess board). **Distinguishing rule**: sb26 is a hidden-sequence guessing game where each commit returns per-slot feedback that narrows the search space; hr8q has no hidden information — the mix table is fully visible, the result auto-displays before commit, and the puzzle is constructive (build the right output) rather than searchful (find a hidden code).
- **Closest prior-game entry**: gv47 (seed-grow-surround-dissolve). **Distinguishing rule**: gv47 is spatial coverage planning under a contact-graph mix rule on a 12×12 paint canvas; hr8q has no spatial canvas, no regions, no adjacency. ACTION5 in hr8q operates on a 2- or 3-input formula widget rather than on the playfield, and the win condition references no spatial cells. Negative-similarity 8-dimension overlap = 1/8 (only the universal step-counter axis).

## Index update

Appended one row to `prior-games/index.md`:

```
| hr8q | pair-blend-recipe | Pair-Blend Recipe — click two (and at L3 three) ingredients to fill a formula widget; commit either consumes the matching target or distils the result back as a new intermediate. | 2026-04-30T12:38:41Z | (autonomous) |
```
