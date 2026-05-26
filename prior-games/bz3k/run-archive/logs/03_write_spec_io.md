# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md
- skills/code/spec-template.md (9-section template)
- skills/code/universal-scaffold.md (file structure + style rules)
- skills/code/novaengine-api.md (engine API cheatsheet)
- mechanic-pick.md (from #02 pick_mechanic)
- All design-constraints already in head from #01.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for `bz3k`
  - L1: drift-impulse + speed-zero target. Witness 10 actions.
  - L2: + velocity-cap-band. Witness 16 actions.
  - L3: + velocity-flipper-plate (+ initial vx=6 + hazard wall).
    Witness 14 actions.
  - HUD: step-counter row 63 + velocity-dot-cross top-right + wake
    trail pixels behind avatar.

## Notes
- Designed at 64×64 pixel-cell resolution (no camera scaling) to
  satisfy checklist 20 (low-res cell-block forbidden).
- Wake pixels surface the persistent velocity hidden state per
  checklist 19 / "no hidden state" rule.
- All sprites have internal pixel detail (avatar asymmetric blob,
  walls bricked, target hollow ring, cap-band striped, flipper
  hatched, hazard spike-patterned).
- Palette deliberately diverges from prior `{4 wall, 8 red,
  9 blue}` dominance — uses orange/maroon/green/purple/yellow.
- L3 witness arithmetic was carefully derived using Σ s_i × (k-i+1)
  formula for cumulative drift; final 14-action sequence is
  ` →←→→←→←←→←→←→→ ` with phase 1 (flip) + phase 2 (return).
- ACTION7 deliberately omitted (no undo verb) per checklist 22.
- Transition condition met. Proceeding to critique_spec.
