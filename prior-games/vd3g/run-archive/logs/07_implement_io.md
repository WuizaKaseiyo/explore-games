# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised, from #05): full 9-section spec.
- skills/code/universal-scaffold.md: file structure rules.
- skills/code/novaengine-api.md: engine API surface.
- skills/code/id-generation.md: ID rules (vd3g already verified).

## Deliverables Produced
- `prior-games/vd3g/vd3g.py` (553 lines): generated game source.
- `prior-games/vd3g/metadata.json`: run metadata.
- `implement-summary.md`: plain-English rule summary + verification log.

## Notes
- One bug surfaced and fixed during witness simulation:
  - Per-level state attributes (`self.heights`, `self.cell_kind`, etc.)
    were being initialised AFTER `super().__init__()`, but
    `NovaBaseGame.__init__` calls `set_level(0)` internally, which
    triggers `on_set_level` — and that handler writes to
    `self.heights` etc. The post-super initialisation overwrote
    those values back to zeros, leaving the game in a state where
    `max_steps == 0` and every action immediately fired
    `self.lose()`. Moved attribute init BEFORE `super().__init__()`.
- All three witnesses (L1=6, L2=32, L3=30 actions) replay successfully
  in-engine. Final state for L3 witness = WIN.
- Implementation choices:
  - Single 64×64 `terrain` canvas Sprite mutated in place to render
    the heightmap; marbles are 4×4 sprites positioned at multiples
    of 4. Avoids the chunky-blocks anti-pattern by giving every
    "logical cell" 4×4 internal multi-palette pattern.
  - State held in `self.heights` (16×16 int8) and `self.cell_kind`
    (16×16 int8) numpy arrays.
  - Anchor pairs encoded as a `dict[(col, row), (col, row)]` with
    symmetric entries.
  - Settling pass iterates marbles in priority order (alphabetical
    name: red < blue), each marble checks its 4-neighbours in
    N→E→S→W priority for the first valid LOW non-occupied non-wall
    cell.
  - Camera viewport set to `(64, 64)` — matches every level's
    `grid_size=(64, 64)` so the engine's CHECK_CAMERA_VIEWPORT is
    automatically satisfied.
