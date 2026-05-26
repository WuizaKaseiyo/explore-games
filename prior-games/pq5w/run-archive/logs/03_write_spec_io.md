# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md
- code/spec-template.md
- design-constraints/* (composition-and-tutorial, difficulty-rules, checklist, forbidden-elements, core-knowledge-priors)
- conventions/reference-game-patterns.md (esp. discoverability via animation; long-distance transition rule)
- global/action-enum.md, color-legend.md, paths.md
- code/universal-scaffold.md, novaengine-api.md

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec for game pq5w
  (`portal-pair-relocate`). 3 levels, witness solutions written
  out action-by-action with click pixel coords; per-level
  difficulty justification covering all four bullets per
  difficulty-rules.md.

## Notes
- Picked phase-tick teleport pattern (1-action consumed by
  teleport-resolve) per reference-game-patterns.md long-distance
  rule, so the player sees the avatar AT the source portal as a
  distinct frame.
- Made portal A always-fixed and portal B always-movable — visual
  cue in sprite design (dark outer ring vs light pink outer ring) —
  to avoid a hidden "which portal is selected" mode.
- Disallowed relocating B onto goal / anchor / forbidden / wall
  cells — closes a trivial-fallback exploit in L3.
- Forbidden column at x=8 in L3 fully separates sub-area-1 from
  sub-area-2 — required so that direct walk from A to goal MUST
  cross forbidden cells (which fail the level).
- L1 step budget 30 (witness 5), L2 budget 50 (witness 7), L3
  budget 80 (witness 8) — generous, never shrinking.
