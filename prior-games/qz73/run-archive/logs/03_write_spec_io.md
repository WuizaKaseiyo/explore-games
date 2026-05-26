# Step #03: write_spec

## Inputs Consumed
- `workspace/mechanic-pick.md` (from #02): the chosen mechanic family
  `radial-cycle-lock`, ID `qz73`, prior-categories used, novelty rationale.
- `skills/code/spec-template.md`: 9-section structure.
- `skills/code/universal-scaffold.md`: file structure rules + camera-viewport rule + style guide.
- `skills/code/novaengine-api.md`: Sprite/Level/Camera/NovaBaseGame API for shaping concrete implementation hints.
- `skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements}.md`.
- `skills/global/{action-enum,color-legend,paths}.md`.
- `skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md`.

## Deliverables Produced
- `workspace/mechanic-spec.md` — all 9 sections of the spec template,
  EXACTLY 3 levels (tutorial / introduce-second / compose), concrete
  pixel layout for the 8-slot ring, sprite roster with opaque
  10-character names, action mapping `[5, 6]`, lose-on-step-counter,
  win predicate as a testable function, novelty re-stated against
  every plausible taxonomy near-miss + the kf42 prior.

## Notes
- The hardest design call was how to draw the rotor visually without
  it reading as a clock face (which would violate "real-world clipart"
  forbidden-elements rule). Solved by NOT drawing spokes-as-bars; tips
  are just 3×3 coloured squares orbiting at fixed radii from a 5×5
  hub, and sockets are 5×5 hollow rings. The structure reads as
  "blocks orbiting a hub" — abstract, not clock-like.
- Considered drawing literal spoke-bars between hub and tip; rejected
  because rendering a line at 8 angular positions on a 64×64 grid
  would require either pre-baked per-angle line sprites or complex
  pixel-painting per step — neither aligns with the universal-
  scaffold's "minimal sprite library" guidance.
- Decided to make ACTION6 misclicks NOT consume a step. The kf42
  mechanism-detail showed an explicit `_action_count`-based step bar
  driven by a private counter, which lets the game decide which
  actions count toward the budget. This avoids the agent accidentally
  burning the budget on pointer noise during exploration.
- Level-3 colour assignment (5 tips × 5 sockets) is described
  parametrically; the implementer must pick concrete colours that
  satisfy "no all-rotate-no-lock witness, no all-lock-no-rotate
  witness, but a 5-7 action interleave does work". This is left to
  `implement` rather than nailed down here, because the spec's
  contract is the mechanic, not the puzzle — the puzzle is one of
  many configurations consistent with the mechanic.
