# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md, workspace/critique-pass.md
- skills/code/{universal-scaffold, novaengine-api, id-generation, smoke-test-checks}.md
- novaengine source: `.venv/lib/python3.12/site-packages/novaengine/sprites.py` (verified Sprite.tags is a property without setter — must mutate via `sprite.tags.append(...)`)
- 5 reference source files read in #01 (cn04, wa30, m0r0, sk48, sb26): pattern templates for Camera, RenderableUserDisplay, two-sprite-state-swap idiom, tag-based sprite querying.

## Deliverables Produced
- prior-games/qy7w/qy7w.py (730 lines): full game implementation.
- prior-games/qy7w/metadata.json: id, title, baseline_actions=[6], date_generated.
- workspace/implement-summary.md: file paths + line count + plain-English mechanic summary.

## Notes
- Sprite.tags has no setter; mutate via `sprite.tags.append(t)` (the property returns the underlying list reference).
- Two-sprite-swap idiom: each crossing has a PASS variant and a TWIST variant pre-placed at the same coords; one is TANGIBLE, the other REMOVED. Toggle swaps modes via `set_interaction()`. Identification uses sprite tags `cid_C1`...`cid_C5`.
- Click bug found and fixed: LONG crossing's bbox centre lands on the (transparent) col-1 strand region — `get_sprite_at` returns None there. Fixed `_get_valid_actions` to return click coordinates known to be inside the visible grey region of the crossing (local x=9, mid-height).
- Strand canvas is one large 49×64 sprite repainted every step. The canvas pixel array is reconstructed from the strand routing computed by `_trace_strands()`, which walks every screen-y row top-to-bottom, applying crossings, shift cells, and blocker checks in order.
- All 3 spec witnesses verified end-to-end in a single Python session: L1 advanced after 2 clicks, L2 advanced after 2 clicks, L3 reached WIN state after 2 clicks.
