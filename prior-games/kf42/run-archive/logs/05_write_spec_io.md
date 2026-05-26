# Step #05: write_spec (revision pass #2)

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): the v1 spec being revised.
- workspace/critique-revisions.md (from #04 critique_spec): 5 issues with concrete fixes.
- workspace/mechanic-pick.md (from #02 pick_mechanic): unchanged ID and family.
- skills/design-constraints/{forbidden-elements,checklist}.md: re-grounding for sprite-shape and predicate fixes.
- skills/code/{universal-scaffold,novaengine-api}.md: BlockingMode / InteractionMode usage references.
- skills/mechanic-novelty/similarity-check.md: confirms `tether-pawn-cycle` family tag remains accurate after Issue 3 fix.

## Deliverables Produced
- workspace/mechanic-spec.md: revised v2 spec. Sections changed (with `[REVISED — addresses Issue N]` markers and quoted issue text):
  - §1 Title (Issue 3 — wording).
  - §2 Mechanic family (Issue 3 — direct colour-set semantics).
  - §3 Sprite roster (Issue 1 — diamond-cross target; Issue 2 — solid-filled cycler).
  - §4 L3 only (Issue 3 — unified set-semantics + reworked maze).
  - §6 Hidden state (Issue 4 — explicit layout).
  - §7 Win condition (Issue 5 — bijection formalisation).
  - §9 Novelty note vs ls20 (sharpened distinguishing rule).
  - §5, §8, §4 (L1, L2 macro-structure) unchanged.

## Notes
- Cycler is now uniformly a "direct colour-set" pad. The family-tag remains `tether-pawn-cycle` ("cycle" reframed as "moment-of-walk colour change"); novelty distinguishing rule against `ls20` becomes stronger.
- L3 maze geometry adjusted so each pawn is forced through the *opposite-colour* cycler first, requiring planning + click-switch mid-route.
- Hidden state is `(2, 2) np.int16`. All four entries are int16-safe.
