# implement-summary

## Files written
- `prior-games/ek73/ek73.py` — 594 lines (parses; instantiation tested OK; 3 levels declared at module scope).
- `prior-games/ek73/metadata.json` — schema-conforming.

## Implemented rule (3-5 line plain-English summary, no cell coords)
A single avatar walks one cell per arrow-press around a walled grid to collect every target on the level. The cell the avatar just vacated stays as a glowing trail mark for a few turns then fades — stepping onto an active trail mark loses the level. From the second level on, scattered floor pads erase every active trail mark when stepped on, and the third level adds paired warp pads that teleport the avatar between matched-pair pads.
