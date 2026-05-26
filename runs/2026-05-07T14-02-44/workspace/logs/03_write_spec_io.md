# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): mechanic family, 4-char ID, distinguishing rules.
- skills/code/spec-template.md: 9-section spec template.
- skills/design-constraints/composition-and-tutorial.md (carried from #01): exactly 3 levels, +1-or-+2 mechanics per level promotion.
- skills/design-constraints/difficulty-rules.md (carried from #01): per-level random-resistance / human-time / planning-depth / step-budget.
- skills/design-constraints/checklist.md (carried from #01): 18 (now 20) checklist items.
- skills/design-constraints/core-knowledge-priors.md (carried from #01): four allowed priors.
- skills/design-constraints/forbidden-elements.md (carried from #01): no letters/digits/clipart/cultural conventions.
- skills/conventions/reference-game-patterns.md (carried from #01): inherit step-counter HUD, tag-based querying, per-level data dict, distinctive ACTION5 verb, "no hidden state" rule, "visual detail floor" rule, "animation mandatory" rule.
- skills/code/universal-scaffold.md (carried from #01): code structure for the implement state (informs spec choices about HUD widgets, level-data, etc.).
- skills/code/novaengine-api.md (carried from #01): API for sprite/level/camera/RenderableUserDisplay.

## Deliverables Produced
- mechanic-spec.md: Full 9-section spec for game `yf3h` (`pulse-arm-burst-resonate`). 12×12 grid, click + ACTION5 mixed input. L1=1 mechanic (M1 arm-fire-ring-strike), L2=2 (+M2 colour-keyed resonator), L3=3 (+M3 phase-delay tile). Witnesses: 2/3/5 actions. Step budgets: 12/16/18.

## Notes
- During L3 design, caught a subtle bug in my first layout: the initially-planned phase-delay tile at (2, 5) would also have been on the blue ring's path, breaking the puzzle. Re-positioned to (1, 1) where Manhattan(emitter_red)=2 and Manhattan(emitter_blue)=9 — the blue ring only "encounters" the tile at tick 9, well after the multi-resonator activation decision at tick 7. This is documented in §4 L3 layout with the per-emitter Manhattan-distance recap.
- Per checklist 19 (no hidden state), every state mutation has a persistent visible cue (centre-dot for armed-emitter, 4-corner-dots vs filled-square for delay tile, white-fill for activated resonator, ring-overlay sprite for in-flight rings, per-pip flash for per-tick resonator hits).
- Per checklist 20 (visual detail floor), every gameplay sprite uses ≥3×3 multi-pixel patterns with internal structure (5×5 emitters/resonators with internal frames; 3×3 phase-delay with corner-dots-vs-filled patterns). Pips and walls (not used in this game) are HUD-class flat blocks, exempt per the same rule.
- Per the L1 → L2 → L3 mechanic-inheritance rule (checklist 11), the +1 each level is satisfied: L1=1, L2=N+1=2, L3=L2-count+1=3. Each level's witness uses every active mechanic (no hidden mechanics per checklist 9-12).
