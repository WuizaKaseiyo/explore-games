# Implement summary

## Files written
- `prior-games/pn5d/pn5d.py` — 432 lines.
- `prior-games/pn5d/metadata.json`.

## Verification
- AST parse: PASS.
- Runtime instantiation: PASS (`Pn5d()` constructed, 3 levels loaded).
- `__pycache__` cleaned.

## Implementation summary (3-5 lines, no spec coordinates)
The game presents a horizontal row of open-top vessels connected at their bases by toggleable valves. Each pour adds one liquid unit to every vessel in the cursor's currently-connected group; clicking a valve flips its state and re-partitions the connectivity. Vessels can be marked with an outward overflow lip — surface above the lip's row is clipped after each pour, mirroring real-world spillway behaviour. Win triggers when every vessel's surface matches its red inward pip; lose triggers when the bottom step bar runs out.
