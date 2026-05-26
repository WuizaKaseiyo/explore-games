# Implement summary — fz5j

## Files written
- `prior-games/fz5j/fz5j.py` (608 lines)
- `prior-games/fz5j/metadata.json`

## Summary
Three levels on a 16×16 logical grid (4-pixel cells on a 64×64 frame) where the player nudges a small green dot through cells that flip between two visible states on a deterministic schedule. Two-sprite-swap idiom (open variant TANGIBLE while closed variant REMOVED, swapped each step) renders the alternation; per-cell period and offset are read from per-level data and resolved in `on_set_level`. A late-level fragile variant locks itself permanently on a first failed entry and, when locked, post-step BFS detects whether the goal is now unreachable and fires `lose()`. Smoke-tested: full witness across all three levels reaches `GameState.WIN`; intentional mis-timed entry on the fragile cell reaches `GameState.GAME_OVER`; budget exhaustion on level 1 reaches `GameState.GAME_OVER` at the configured step cap.
