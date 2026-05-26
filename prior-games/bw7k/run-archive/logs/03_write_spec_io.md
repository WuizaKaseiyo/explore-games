# Step #03: write_spec

## Inputs Consumed
- task-overview.md (HITL not allowed; autonomous)
- states/write_spec.md
- skills/global/* (action enum, color legend, paths)
- skills/design-constraints/* (core knowledge priors, forbidden elements, composition-and-tutorial, checklist, difficulty rules)
- skills/code/{spec-template,universal-scaffold,novaengine-api}.md
- skills/mechanic-novelty/* (taxonomy, similarity-check, negative-similarity-check, prior-games-index-format)
- workspace/mechanic-pick.md (#02 deliverable: ID `bw7k`, family `actor-replay-shade`, near-miss distinguishing rules)

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec following spec-template.md, 64×64 native grid with 4-pixel stride, sprites for actor + 2 shade colours + 2 anchor colours + 2 targets + actor-goal + walls; level data per level (step_budget 30/50/70 for L1/L2/L3); five mechanics across the three levels (M1 Walking, M2 Anchor-spawn-shade, M3 Shade-replays-tape, M4 Replay-walls, M5 Multi-shade-simultaneity); witness solutions and difficulty justifications per level.

## Notes
- Resolved several design choices during drafting:
  - 4-pixel stride (vs 6-pixel sk48-style) for cleaner 16×16 logical board.
  - No move-tape HUD widget — would have required arrow-glyph or colour-coded direction sprites, both forbidden by `forbidden-elements.md`. Relying on shade animation as the only visual cue for the replay mechanic.
  - Action subset `[1, 2, 3, 4]` (arrow-only); no ACTION5 (no distinctive verb on slot 5 for this mechanic family), no ACTION6 (no clicks needed), no ACTION7 (no meaningful undo).
  - Anchor consumed (set to `InteractionMode.REMOVED`) on first trigger to avoid double-spawn confusion.
  - `level.get_data("step_budget")` used for per-level step counter.
- Initial L3 layout (v3) had walls placed defensively without being exercised by the witness; flagged by self-critique against checklist 11/12 and revised to v4 in critique round 1 (workspace/critique-revisions.md issue 1).
- Cross-checks against the negative-similarity-check.md and the visual-grouping rules in checklist item 21 included in the spec body.
