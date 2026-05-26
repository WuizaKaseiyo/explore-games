# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): chosen mechanic family.
- skills/code/spec-template.md: 9-section spec format.
- skills/code/universal-scaffold.md: file structure + camera scaling notes.
- skills/code/novaengine-api.md: Sprite/Level/Camera/RenderableUserDisplay API.
- skills/design-constraints/composition-and-tutorial.md, checklist.md, difficulty-rules.md, core-knowledge-priors.md.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for tb4k.
  - L1: 1 mechanic (M1 tumble), K=16, D=2, no hard-death.
  - L2: +1 mechanic (M2 hole + lives), K=16, D=3, 3 lives, asymmetric N/S detour planning gate.
  - L3: +1 mechanic (M3 narrow bridge), K=14, D=2, 3 lives, east-tumble discipline on bridge.

## Notes
- Bloxorz tumble physics: standing↔lying alternates per tumble; each tumble pair shifts standing position by 2 cells along the tumble axis. Reachable standings have the same x-parity and y-parity as the start.
- Grid_size = (32, 32), scale 2 — gives 4 rendered pixels per Bloxorz cell, allowing sub-cell pixel detail in each 2×2 sprite (per checklist 21).
- Brick state machine implemented as three sprites with InteractionMode swapping (idiomatic per universal-scaffold "Two-sprite swap").
- ACTION7 omitted (no undo) per checklist 23.
- Goal-parity caveat noted in L1: goal must be same-parity-as-start (both odd or both even) because tumble pairs shift by 2.
