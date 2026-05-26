# Game generation final report

## Generated game
- **ID**: ng52
- **Source**: `prior-games/ng52/ng52.py`
- **Metadata**: `prior-games/ng52/metadata.json`
- **Lines of code**: 561

## Mechanic

The screen shows three classification bins side by side; each bin's
top stripe is its **signature** — a stack of 1×L solid-colour
"sticks" describing the target multiset of pixel-colours that bin
will accept. A pool of irregularly-shaped multi-pixel sample
objects sits below the bins. The player has no avatar. Clicking
(ACTION6) a pool object marks it selected (white outline ring); a
follow-up click on a bin's holding area drops it into that bin;
clicking an in-bin object lifts it back. ACTION5 commits: each
bin's currently-held objects are aggregated into a per-colour
pixel multiset and compared with that bin's signature multiset. If
every bin matches, the level advances; if not, every placed object
snaps back to its pool position so the player can try again. L1
introduces classification (single-stick single-colour signatures,
one object per bin). L2 adds multi-stick multi-colour signatures
that require **multiple** objects per bin to sum into the
signature. L3 adds a distractor object that does not fit any
signature and must deliberately be left out of every bin.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Commit. Aggregate each bin's pixel-colour multiset and compare to its signature; on full match, advance the level; on mismatch, snap every placed object back to its original pool position. |
| ACTION6 | Click at (x, y). Hits a pool object → select it (deselect any prior selection). Hits a bin-resident object → lift it back to the player's hand (selection). Hits a bin's holding area with a selection active → place the selected object in that bin's next free 4×4 slot. |

## Levels

- **L1** — 3 single-stick single-colour bins (1×3 / 1×4 / 1×5 blue); 3 single-colour blue objects (3-blue L, 4-blue T, 5-blue plus). 7-action witness. Step budget 40.
- **L2** — bins gain multi-stick multi-colour signatures (1×6 blue; 1×3 blue + 1×3 purple; 1×4 blue + 1×2 purple); 6 objects in the pool, none of which alone matches any bin. Each bin's signature is reachable only by combining 2 objects. 13-action witness. Step budget 60.
- **L3** — same bins as L2 plus a 5-blue plus-shape **distractor** added to the pool. Total pool pixels exceed the bins' total capacity by exactly the distractor; the only feasible partition leaves it in the pool. 13-action witness. Step budget 60.

## Novelty note

- **Closest taxonomy entry**: sb26 (tile-place-commit / Mastermind). **Distinguishing rule**: sb26 is a hidden-code search-with-feedback game; ng52 has no hidden state — the bin signatures are fully visible and commits return only pass/snap-back. sb26 has a fixed 1-tile-per-slot capacity; ng52 bins hold variable-many objects whose multisets sum to the signature.
- **Closest prior-game entry**: hr8q (pair-blend-recipe). **Distinguishing rule**: hr8q produces a single output colour from a 2/3-input recipe; ng52 partitions a pool of objects across multiple bins simultaneously, with no colour transformation. The negative-similarity 8-dimension overlap is 0/8 substantive (only the universal step-counter axis).

## Index update

Appended one row to `prior-games/index.md`:

```
| ng52 | multiset-signature-classify | Multiset Signature Classifier — partition a pool of irregular multi-pixel objects into bins whose stick signatures define a target pixel-colour multiset per bin. | 2026-04-30T15:36:31Z | (autonomous) |
```
