# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): id ds5q, family wall-erode-chain, per-level mechanic enumeration draft.
- skills/code/spec-template.md (9 sections), universal-scaffold.md, novaengine-api.md.
- skills/design-constraints/* (checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements).
- skills/conventions/reference-game-patterns.md (recurring design moves, anti-patterns, Discoverability).
- skills/global/* (action-enum, color-legend, paths).

## Deliverables Produced
- `workspace/mechanic-spec.md` — full 9-section spec covering title, mechanic family, sprite roster (12 sprites), 3-level layouts with witnesses (L1=9, L2=24, L3=27 actions), action mapping, HUD, win/lose, and novelty grounding.

## Notes
- Pivoted L3's second-new-mechanic from `colour-chain-hardness` (initially proposed in mechanic-pick.md) to `layered-hardness`. Rationale: chain-link forcing was structurally hard to satisfy under §3.4-style strict counterfactual necessity (a wall sandwiched between unbreakable obstacles can never be entered by the avatar even after chain-erosion drops it to hardness 0), whereas layered-hardness has an obvious clean forcing — a hardness-3 wall on the unique east-traversal path requires three consecutive ACTION5 strikes from cardinally-adjacent floor.
- Mechanic-pick.md remains the recorded family-tag and §9-novelty target ("wall-erode-chain" — the "chain" wording survives as a flavour cue in the family tag even though L3 implements the depth via stripe-count-hardness, since the underlying mental model is "chained hits on a wall"). Critique should validate this re-naming.
- L1 was initially designed to require zero charge-pads (pickaxe defaults to grey). To preserve this without diluting the L2 colour-pickaxe-match introduction, L1 uses `wall_grey_h1` walls and the pickaxe is initialised to `"grey"` so erode is auto-active.
- The L1 layout adds stones at (3,3), (3,5), (5,3), (5,5) to forbid detour around the row-4 grey walls and force the witness through erode.
- L2 forces red-first by making the blue pad reachable only on the east side of the red wall — col 3 is sealed at every row except (3,4).
- L3 forces layered-hardness by placing the hardness-3 red wall at the unique col-3 opening.
- All 3 levels share the same playfield 64×64 with 8-pixel-tile alignment; sprite roster reused with only sprite positions changing per level.
- Step budgets: L1 30, L2 80, L3 90 — never shrinking, all ≥ 3× witness.
