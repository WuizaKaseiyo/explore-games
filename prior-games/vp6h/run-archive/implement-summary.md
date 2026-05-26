# implement summary — vp6h

## Files

- `prior-games/vp6h/vp6h.py` — 462 lines
- `prior-games/vp6h/metadata.json`

## Verification

- Python syntactic parse: PASS (`ast.parse` no errors).
- Runtime instantiation: PASS (`Vp6h()` initialises successfully; level
  count = 3; current_level grid_size = (16, 16); available_actions =
  [1, 2, 3, 4, 6]; opaque-pillar index correctly identifies col 7;
  shadow geometry: (col 7, row 11) shaded, (col 7, row 0) lit, both
  consistent with the L1 layout).
- L1 witness drove through `perform_action`: 5 ACTION4 then 1 ACTION1
  → crystals_remaining drops to 0 → level transitions to L2.
- L2 witness drove through `perform_action`: 2 (phase 1) + 14 (phase 2) +
  1 (ACTION6 click on top rail at grid col 2) + 7 (phase 4) = 24
  actions to clear all 3 crystals → level transitions to L3.

## Plain-English summary

Avatar walks a 16×16 grid lit by 1-2 yellow horizontal lantern bars
mounted on rails at the top and bottom edges. Grey vertical pillars
cast shadow strips behind themselves in each lit column. The avatar
collects scattered cyan-and-purple crystals; pickup only succeeds when
the avatar's reference cell is shaded by every active lantern. Players
click any column on a lantern's rail to slide that lantern. Difficulty
rises across the three levels by introducing the lantern-slide ability
and (at L3) a second lantern whose shadow zones must intersect to
permit pickup.
