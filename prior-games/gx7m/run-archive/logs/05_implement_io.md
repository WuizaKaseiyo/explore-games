# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03).
- workspace/critique-pass.md (from #04) — including the `_get_valid_actions` 256-cell-enumeration note.
- skills/code/{universal-scaffold.md, novaengine-api.md, id-generation.md}.
- Reference source files read in #01 (cn04, wa30, tu93, sb26, r11l) — used to anchor naming conventions, sprite-bank placement, level-data dict idiom, BFS cascade pattern, valid-action enumeration.

## Deliverables Produced
- `prior-games/gx7m/gx7m.py` (463 lines).
- `prior-games/gx7m/metadata.json`.
- workspace/implement-summary.md.

## Notes
- File is 463 lines including blank lines and helper functions; well below the 1500-line cap.
- Followed semantic-naming convention per `universal-scaffold.md` § Style rules (no obfuscation): `Gx7m`, `disc_pink`, `_cascade`, `_DIR_CYCLE`, `StepCounterHud`, etc. The 4-char ID `gx7m` is opaque, as required.
- All three witness sequences from the spec were validated end-to-end against a live `Gx7m()` instance: L1 → L2 → L3 → WIN. Cascade math, ratchet gating, and clutch partitioning all produce the spec's predicted rotations at every step.
- `_get_valid_actions` enumerates the 256-cell ACTION6 grid (every (x, y) for x, y in 0..63 step 4), per the `r11l` convention and the critique's note.
- Per-level camera viewport is set in `on_set_level` to match `level.grid_size = (64, 64)`; default 64×64 camera is consistent so no scaling is needed.
- Per `forbidden-elements.md`: gear sprites are octagonal toothed-disc abstractions; collar-rings are hollow square frames with edge-indents; tangs are 1×2 vertical bars (explicitly allowed in the rule). No sprite resembles a letter, digit, or culturally-loaded object.
- `__pycache__` cleanup attempted; nothing to remove (the smoke-test instantiations didn't write a __pycache__ in this directory because the module loaded with `sys.path.insert`).
