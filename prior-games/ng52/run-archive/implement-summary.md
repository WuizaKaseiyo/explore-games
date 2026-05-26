# implement-summary

## Files
- `prior-games/ng52/ng52.py`
- `prior-games/ng52/metadata.json`

## Summary
Three coloured-stick "bin signatures" stand in a top row; a tray of
non-convex sample objects sits below. The player clicks a sample to
select it, clicks a bin to drop it into that bin, and ACTION5
commits the partition. A bin matches when the multiset of pixel-
colours of all its placed objects equals its signature; if every
bin matches the level advances; if any bin mismatches every placed
object snaps back to its pool position. L1 has 3 single-stick
single-colour bins; L2 introduces multi-stick multi-colour
signatures requiring multi-object compositions; L3 adds a
distractor object that must deliberately remain in the pool.

## Smoke evidence
Instantiation succeeds; the L1 (7 actions), L2 (13 actions), and L3
(13 actions, leaving the distractor in the pool) witnesses all
drive the engine to `GameState.WIN`.
