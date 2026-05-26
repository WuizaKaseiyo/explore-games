# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md (from harness root): the 9-section spec template + revision instruction.
- skills/code/spec-template.md: the 9-section structure with item-11/12/18 cross-references.
- skills/code/universal-scaffold.md: file structure + style rules + camera-viewport-must-match-grid_size warning.
- skills/code/novaengine-api.md: Sprite / Level / Camera / NovaBaseGame signatures.
- workspace/mechanic-pick.md (from #02): ID `ek73`, family `wake-trail-evade`, action palette `[1,2,3,4]`, the open design questions answered, novelty cite list.
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements,difficulty-rules}.md (from #01): structure, +1/+2 rule, four priors, no-symbols, four-bullet difficulty-justification.
- skills/conventions/reference-game-patterns.md (from #01): step-counter HUD pattern, no-hidden-state rule, UI-teaches rule.

## Deliverables Produced
- `workspace/mechanic-spec.md`: the 9-section spec — title (§1), mechanic-family + prior categories (§2), 8 sprite kinds with palette + tag + role (§3), 3 levels (L1, L2, L3) each with mechanics-required + per-mechanic necessity + witness + 4-bullet difficulty justification (§4), action mapping (§5), HUD + per-game state with no-hidden-state cues (§6), win predicate (§7), lose conditions including soft-lock detector (§8), novelty cites against taxonomy + priors (§9).

## Notes
- The spec self-flags two known weaknesses at the end: (a) L2's plausible-wrong-path argument is bad (the alternative also succeeds); (b) L3's sticky-pad necessity is shaky (the corridor only requires single traversal). Both need critique to formally reject and will be addressed in revision.
- Strict counterfactual necessity (item 12) was given a per-mechanic table where each row attempts a 1-line concrete reason naming specific cells/walls/state-checks. The L2 and L3 entries acknowledge gaps explicitly.
- Visual-design rules (item 20, 21): sprite roster gives every sprite an internal pixel pattern distinct from colour-fill; wake's three age states have distinct internal patterns so age is read off the screen alone (no-hidden-state, item 19).
- Action palette `[1,2,3,4]` (pure cardinal) — no ACTION5 (no distinctive verb that isn't already in arrow-press).
- Level-budget chain 60 → 80 → 120 is monotonic-non-decreasing (per difficulty-rules.md § d L3 addendum).
- Soft-lock guard: the lose-condition fires `self.lose()` immediately if the avatar's 4 neighbours are all walls/wake AND the win predicate isn't met — the no-win-waiting-room mirror per difficulty-rules.md § 1.
- Grid choice: `grid_size=(64, 64)` with `CELL_STRIDE=4` (16×16 logical cells, sprites at multiples of 4) — the wa30 pattern. Avoids the "small upscaled chunky-blocks" anti-pattern called out in checklist item 20.
