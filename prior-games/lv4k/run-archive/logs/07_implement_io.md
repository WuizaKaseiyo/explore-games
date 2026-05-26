# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (section 3-9 for sprite roster, layout, witness, win/lose)
- skills/code/{universal-scaffold.md, novaengine-api.md, id-generation.md}
- 5 reference-game source files in full from study state (cn04, sp80, wa30, sk48, tr87)

## Deliverables Produced
- prior-games/lv4k/lv4k.py (491 lines): full game implementation. Universal-scaffold conformant; semantic naming throughout (no obfuscated tokens); 3 levels with the specified sprite layouts; click-driven select/place/lift; tilt rendering; passenger displacement at |tilt_level|≥2; win/lose predicates.
- prior-games/lv4k/metadata.json: per implement.md schema.
- workspace/implement-summary.md: paths, line count, plain-English summary, smoke-test results, implementation notes.

## Notes
- During smoke testing I found and fixed one critical bug: state attributes were being initialised AFTER `super().__init__()`, which calls `set_level(0)` → `on_set_level()`, which populates those attributes. The post-super initialisation was wiping the valid state. Fix: moved attribute initialisation before `super().__init__()`.
- Refined click hit-testing on beam slots to be y-tolerant (±3 cells) so witness coordinates work whether the beam is at neutral tilt or tilted by up to 2 levels. X remains strict to disambiguate adjacent slots.
- All 3 witnesses (L1: 4 actions, L2: 6, L3: 8) successfully complete — engine reports state WIN after L3.
- The L3 "bad heuristic" (counter-stack m2@-3 followed by m2@-1) was verified to lose: passenger displaces from +2 → +1 → 0 (fulcrum, not in exposed_arms), engine sets state GAME_OVER at step 4.
- __pycache__ cleaned post-test.
- Transitioning to smoke_test state.
