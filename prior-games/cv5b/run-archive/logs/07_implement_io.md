# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revised)
- workspace/critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md
- Reference source cn04 (read in study) for scaffold conventions.

## Deliverables Produced
- prior-games/cv5b/cv5b.py (428 lines).
- prior-games/cv5b/metadata.json.
- workspace/implement-summary.md.

## Notes
- Launcher 5×5 sprite; "fire origin" at sprite top-left + (2, 2). Three
  variants (p1/p2/p3) co-located, only one TANGIBLE at any time.
- Sprite-swap idiom (per universal-scaffold) used for power-cycle.
- Arc cells computed parametrically with up to ~58 sub-steps and
  deduped to integer cells.
- Wind drift applied to final cell only when any arc cell overlaps a
  wind sprite's bounding box.
- Shield blocking: arc truncated at first cell intersecting a shield;
  no target registered.
- Witness verification: L1 1-action, L2 14-action, L3 39-action paths
  all reach WIN end-state cleanly.
