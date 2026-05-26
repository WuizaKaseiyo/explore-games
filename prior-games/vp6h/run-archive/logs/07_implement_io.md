# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revision 1)
- workspace/critique-pass.md (verification round 2)
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md
- 4 reference game sources read in study (cn04, sk48, sp80, wa30) for house-style guidance

## Deliverables Produced
- prior-games/vp6h/vp6h.py — 462 lines. Universal-scaffold structure: imports, sprites dict (alphabetised), levels list (3 entries), constants, StepCounterHud class, Vp6h(NovaBaseGame). Semantic naming throughout (no obfuscated tokens). Tag-based sprite dispatch for `pillar`, `crystal`, `avatar`, `lantern_top`, `lantern_bot`, `ground`.
- prior-games/vp6h/metadata.json — schema-compliant.
- workspace/implement-summary.md — paths, line count, plain-English summary.

## Notes
- Python parse: PASS.
- Runtime smoke: PASS. Drove L1 + L2 witnesses via `perform_action`. L1 → L2 transition fires after pickup at avatar (7, 12). L2 → L3 transition fires after pickup of B (avatar at (7, 12), which overlaps crystal B at (col=6, row=11..12) — pickup occurs at action 7 of phase 4 rather than action 8 because the avatar's 2×2 footprint covers col 7 first).
- Cleaned up __pycache__ after smoke test.
- Implementation key choices: ground sprite at layer -2 with per-cell repaint after every shadow recompute; pillars on layer 1 (above ground); lanterns layer 1 (INTANGIBLE); rail markers layer 0; crystals layer 2 (INTANGIBLE); avatar layer 3. Avatar movement zone constrained to cols 0..14 rows 1..13 (2×2 footprint must fit and not overlap rails). Lantern slides clamp to `max(0, min(11, gx - 2))` for the leftmost column.
