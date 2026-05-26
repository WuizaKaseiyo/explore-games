# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): id `kn58`, family `anchor-pull-magnet`.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md, id-generation.md: structure.
- skills/design-constraints/*: composition rule (3 levels, +1 or +2 mechanics each), checklist, difficulty-rules.
- skills/global/{action-enum,color-legend,paths}.md: API conventions.

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec for kn58 — sprite roster (8 sprites), 7-mechanic ladder (M1..M7), 3 levels with concrete layouts and witness sequences (L1: 8 actions, L2: 21 actions, L3: 12 actions), action mapping `[5, 6]`, HUD (StepCounterHud), win predicate, lose predicate (step budget exhaustion).

## Notes
- L3 witness has a known gap: M6 (ACTION5 BURST) is not strictly exercised by the current 12-action witness. Flagged in the spec under L3 §Necessity per mechanic for `critique_spec` to drive a layout adjustment that forces BURST.
- Manhattan-gradient-pull rule: dominant axis (|Δx|≥|Δy| → horiz tiebreak); secondary-axis-fallback when blocked. Two-pass simultaneous resolution per universal-scaffold guidance.
- Phases per ACTION6: pull (×2 if BURST), match-check, anti-anchor push (only if anti-anchor present), match-check again. ACTION5 only sets a flag, no phases.
- Pre-stuck purple in L3: at level start `on_set_level` evaluates match-check once and marks purple stuck via M5 carryover; serves as a stationary obstacle for M4 collision.
- Palette signature: `{2 light-grey, 5 black, 12 orange, 15 purple, 14 green, 4 off-black, 0 white, 8 red, 10 light-blue}` — diverse, distinct from prior runs' dominant palettes.
- Sprite scale: 4×4 frame pixels per logical cell on 16×16 logical playfield (64×64 frame, no camera scaling). Pawns/targets/anchor are 4×4 with internal pattern (avoids "big-blocks-on-empty-field" anti-pattern per Principle 1 of negative-similarity-check).
