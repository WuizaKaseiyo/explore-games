# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (rev 1)
- critique-pass.md
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md
- skills/global/{action-enum, color-legend, paths}.md
- Reference styles: cn04 (full read in #01), tu93/sb26 (sampled in #01)
- Sample of zd7m source (recent prior with similar action subset)

## Deliverables Produced
- prior-games/xn5p/xn5p.py (469 lines)
- prior-games/xn5p/metadata.json
- implement-summary.md

## Notes
- One bug caught and fixed: post-super attribute initialisation overwrote on_set_level state. Fixed by reordering. This is documented in lv4k's mechanism-detail; should consider promoting to universal-scaffold.md as a callout (will note in finalize).
- L2 and L3 actual shortest witnesses are 5 actions each (vs 7-10 in spec); M3 is exposed but not strictly counterfactually required.

