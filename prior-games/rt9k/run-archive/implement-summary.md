# Implement summary — `rt9k`

## Files written
- `prior-games/rt9k/rt9k.py` — 454 lines, AST-parses, instantiates without raising, 3 levels declared, `available_actions = [1, 2, 3, 4]`, starting tone is magenta.
- `prior-games/rt9k/metadata.json` — schema-conformant (game_id, title, default_fps=30, tags=["claude-generated"], baseline_actions=[1,2,3,4], local_dir, date_generated).

## Implemented rule (plain English)

The avatar walks four-cardinal arrow steps across a small playfield
that is topologically a torus — walking off any one edge brings the
avatar back in from the opposite edge. The avatar carries a single
visible tone-state from a three-element cycle, and every wrap-cross
nudges the tone one step along the cycle (positive-direction wraps
forward, negative-direction wraps backward). Some walls only let
the avatar pass when its tone matches the wall, and the third level
adds a goal cell that only finishes the level when the avatar
arrives in a specific tone — so reaching the goal becomes a problem
of composing wrap-crosses to land in the right cell with the right
tone at the right moment.
