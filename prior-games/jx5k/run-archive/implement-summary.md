# implement-summary.md

## Files written
- **Source**: `prior-games/jx5k/jx5k.py` (644 lines)
- **Metadata**: `prior-games/jx5k/metadata.json`

## Implementation summary
The game `jx5k` is a 3-level graph-construction puzzle where the player connects coloured node sprites with edges by pair-clicking. Each node has a target degree shown as a small ring of pip markers; the win predicate is met when every node's filled-pip count matches its target. L1 (4 nodes, target degree 2 each) introduces the bare edge-link mechanic with no colour rule. L2 (5 nodes, central + 4 outer, targets `[3, 3, 3, 3, 4]`) adds a colour-cycle action (ACTION5) and a same-colour-only edge constraint, requiring the witness to recolour mismatched starting nodes before edges become legal. L3 (4 nodes, targets `[4, 2, 4, 2]`) extends the per-pair edge cycle to allow parallel double-edges and tunes target degrees so a parallel edge is required on exactly one pair (n0–n2). All three witnesses replay deterministically and win the level.

## Verification performed
- AST parse: PASS.
- Runtime instantiation: PASS (3 levels, camera 32×32, available_actions [5, 6]).
- L1 witness replay: 8 actions → score advances to 1 (next_level fired). PASS.
- L2 witness replay (after L1): 20 actions → score advances to 2. PASS.
- L3 witness replay (after L2): 16 actions → state == WIN, score == 3. PASS.
