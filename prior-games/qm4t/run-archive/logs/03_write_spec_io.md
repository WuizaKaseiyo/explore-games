# Step #03: write_spec

## Inputs Consumed
- `mechanic-pick.md` (from #02)
- `skills/code/spec-template.md`
- `skills/code/universal-scaffold.md`
- `skills/code/novaengine-api.md`
- `skills/design-constraints/*` (composition-and-tutorial, difficulty-rules,
  checklist, core-knowledge-priors, forbidden-elements)
- `skills/conventions/reference-game-patterns.md`
- `skills/global/*` (action-enum, color-legend, paths)

## Deliverables Produced
- `mechanic-spec.md`: 9-section spec, with revised L2 mechanic (M3') after
  catching a geometric impossibility in the first L2 draft (a convex hull
  cannot exclude an interior point of a convex set of vertices). The revised
  L2 places maroons OUTSIDE the convex hull of greens, so M3' becomes
  "selective subset choice" — recognising that a small triangle wraps only
  greens and not the maroons that lie outside.

## Notes
- The first L2 draft had a fundamental error: tried to "carve a maroon out of
  a triangle" by adding more vertices, but the convex hull is monotone in its
  vertex set — adding more points only enlarges the hull. The corrected L2
  layout positions maroons outside the convex hull of the greens.
- L3's witness uses a patroller cycle whose phase 4..7 lies outside the pen
  interior; the witness times its 4th post-click so that the immediately-
  following ACTION5 fires on phase 4 (outside).
- Render plan for `pen_overlay` is a 64×64 `INTANGIBLE` sprite recomputed
  every step. Boundary pixels palette 1 (off-white), interior palette 2
  (light-grey), elsewhere -1 transparent.
- Step budgets: L1=30, L2=50, L3=80 — generous over witnesses (≥7×).
