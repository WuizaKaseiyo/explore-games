# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): ID, family tag, mechanic description, action subset, novelty notes
- skills/code/spec-template.md: 9-section schema
- skills/code/universal-scaffold.md: file structure for the generated game (informs sprite design)
- skills/code/novaengine-api.md: API signatures (Sprite, Level, Camera, NovaBaseGame)
- skills/code/id-generation.md (re-checked for L3 collision avoidance)
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md
- skills/conventions/reference-game-patterns.md (visual-cue rule, anti-patterns)
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for `rj5w` / `axis-fold-mirror`.
  - L1: V-fold only (1 mechanic). Witness 3 actions. Budget 25.
  - L2: V-fold + H-fold + active-axis-toggle (3 mechanics; +2 from L1). Witness 7 actions. Budget 50.
  - L3: V-fold + H-fold + axis-toggle + wall-anchor + lock-on-target (5 mechanics; +2 from L2). Witness 12 actions. Budget 80.
  - All mechanics are counterfactually required at every level they appear in (per checklist item 12 / difficulty-rules.md).
  - Win condition: every pawn coincident with its colour-matched target.
  - Lose condition: step budget exhausted.

## Notes
- The lock rule was tuned to NOT trigger on no-movement (wall-anchored) folds; this preserves the wall mechanic's distinctness from the lock mechanic. Without that distinction, walls would have been redundant with locks at L3 (an item-12 violation).
- L3's witness includes a "double V-fold" — committing the same V-fold twice — that exploits reflection-as-involution composed with selective locking. This is the named non-trivial post-discovery planning step.
- Both V- and H-line cursor sprites live in the level's sprite list with `interaction=INTANGIBLE` so they do not block pawns; their orange/grey state is a runtime `color_remap`.
- The level's three pawns (green/purple/yellow) use the same 5×5 internal pattern with palette swaps — this satisfies checklist item 20 (richly-patterned primary sprites) while keeping the implementation compact.
- ACTION6 is mapped to "click on a fold-line cursor to make that line active." Click anywhere else is a no-op. This makes the toggle discoverable without polluting the action set with a dedicated key.
