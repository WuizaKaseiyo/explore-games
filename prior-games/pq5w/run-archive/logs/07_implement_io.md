# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revised version)
- workspace/critique-pass.md
- code/universal-scaffold.md, novaengine-api.md (style + API)
- prior-games/rt9k/rt9k.py (canonical recent generated-game style)

## Deliverables Produced
- prior-games/pq5w/pq5w.py (420 lines)
- prior-games/pq5w/metadata.json (game_id, title, baseline_actions,
  local_dir, date_generated)
- workspace/implement-summary.md

## Verification done
- AST parse OK.
- Instantiation: g = Pq5w() succeeds; 3 levels; available_actions
  [1, 2, 3, 4, 6]; camera viewport (64, 60) at L1.

## Notes
- Used Pq5w as the Pascal class name (camelcase of `pq5w`).
- Phase-tick teleport implemented: stepping onto a portal sets
  `_teleport_pending`; the next step() consumes any action id and
  resolves to the paired portal's cell, then runs
  _post_action_resolve. The intermediate frame (avatar at source
  portal) is rendered between the two step() calls.
- ACTION6 click handler validates target cell against wall / anchor
  / goal / forbidden / avatar; only relocates float portal if the
  target is "empty floor".
- Forbidden cells use `collidable=False` so the avatar can step on
  them; _post_action_resolve fires self.lose() if avatar lands on
  forbidden.
- HUD uses palette 14 fill / 5 empty at pixel rows 60..63.
