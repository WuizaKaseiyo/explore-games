# Implement Summary

- `prior-games/ym4k/ym4k.py` — 493 lines.
- `prior-games/ym4k/metadata.json`.
- Implemented a 3-level avatar puzzle with ladders, scaffold cells, two vertically coupled platforms, a latch that freezes the left platform high, and a bridge trigger on level 3.
- `ACTION1/2` handle ladder motion, `ACTION3/4` handle horizontal stepping, and `ACTION5` actuates the platform under the avatar.
- The lose path is a visible step-budget bar; the win path is reaching the goal pad.

