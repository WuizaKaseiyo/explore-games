# Implement summary

## Files written
- `prior-games/pq5w/pq5w.py` (420 lines)
- `prior-games/pq5w/metadata.json`

## Plain-English rule
A walking avatar shares the level with two paired portal sprites,
one fixed (anchor) and one movable (float). Stepping onto a portal
queues a teleport that resolves on the next action, sending the
avatar to the paired portal's cell. ACTION6 click on a valid empty
floor cell relocates the float portal. Levels compose by walling
the goal off (forcing a portal jump), then by adding a forbidden-
cell column inside the room (forcing a second relocate + jump).

## Verification done
- `python -c "import ast; ast.parse(...)"` — AST parse OK.
- Instantiation smoke: `g = Pq5w()` → instantiated OK; level count
  3; available_actions [1, 2, 3, 4, 6]; camera viewport (64, 60)
  matches L1 grid_size.
