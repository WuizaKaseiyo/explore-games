# implement-summary — wj7d

## Files written
- `prior-games/wj7d/wj7d.py` (646 lines)
- `prior-games/wj7d/metadata.json`

## Implemented rule (3-line plain-English summary)
The player has coloured stamps on one half of a playfield split by a
white axis line; pressing the commit verb mirror-reflects the
selected stamp across that axis and permanently deposits the
reflected pattern on the other half. The level wins when every
pre-painted shadow target on the far half is fully covered by a
matching-coloured fold. Late-level promotions add stamp-selection
among multiples and the ability to translate and re-orient the
crease itself.

## Smoke-test verification
- Instantiation: succeeds; `_levels` populated with 3 entries.
- L1 witness (6 actions): runs cleanly → `_current_level_index`
  advances to 1.
- L2 witness (16 actions, blue-first): runs cleanly → advances to 2.
- L3 witness (9 actions, crease move + re-orient): runs cleanly →
  `_state` becomes `GameState.WIN`, `win_score=3`.
- Anti-witnesses fire `lose()` (GAME_OVER):
  - L1 fold-without-move → GAME_OVER.
  - L2 greedy red-first → red collides with blue at the 4th DOWN
    (move rejected); fold from (24, 16) leaves shadow uncovered;
    unwinnable check fires GAME_OVER.
  - L3 convenient-click at col=32 for re-orient → V crease at
    col=32 (wrong; correct is col=33); fold leaves red shadow
    uncovered; unwinnable check fires GAME_OVER.
