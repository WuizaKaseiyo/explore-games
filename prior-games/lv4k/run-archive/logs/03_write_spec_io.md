# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md (from harness root)
- skills/code/spec-template.md (the 9-section template)
- skills/code/universal-scaffold.md (scaffold + camera-resize + style rules)
- skills/code/novaengine-api.md (Sprite/Level/Camera/RenderableUserDisplay signatures)
- skills/design-constraints/{checklist.md, composition-and-tutorial.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md}
- workspace/mechanic-pick.md (from #02)

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec for `lv4k` (lever-balance-torque), 3 levels, 3 mechanics introduced 1 per level, witness solutions per level, per-level necessity justification per mechanic, difficulty-justification with all 4 sub-bullets per level (random-resistance, human-tractable, planning-depth, step-budget), action mapping, HUD/state, win/lose conditions, novelty cross-references.

## Notes
- Sketched torque math carefully: with arms {-3..-1, +1..+3}, fulcrum at center for L1 / L2 / L3. L1 uses 4 placement slots (arms ±1, ±2), L2/L3 use 6 (arms ±1, ±2, ±3).
- Win predicate uses RAW integer torque == 0; tilt_level (clamped int from tilt_raw // 2) is for rendering and L3 passenger-slide trigger.
- L3 passenger starts at arm +2; passenger slides one arm toward the negative-tilt direction when |tilt_level| ≥ 2 (i.e., |tilt_raw| ≥ 4). If passenger leaves the exposed-arm range, level loses.
- Verified L3 has multiple distinct witness orderings (planning depth) but trivial heuristic ("place all m2s first") deterministically slides passenger off → loses. Captured in difficulty justification (c).
- Per-level step budget: 12, 24, 36 (strictly increasing per difficulty-rules.md § d).
- Action palette = `[6]` (pure click). All state mutations have visible cues (selection halo, beam tilt position, passenger position).
