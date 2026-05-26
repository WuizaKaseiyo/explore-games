# Step #03: write_spec

## Inputs Consumed

- mechanic-pick.md (from #02)
- skills/code/spec-template.md — 9-section structure
- skills/design-constraints/composition-and-tutorial.md — exactly 3 levels, +1/+2 mechanics per level, mechanic inheritance
- skills/design-constraints/difficulty-rules.md — 4 sub-bullets per level (random-resistance / human-time / planning / step-budget)
- skills/design-constraints/checklist.md — 21 items (1-21)
- skills/design-constraints/forbidden-elements.md — no digits/letters/clipart
- skills/conventions/cross-cut-frequencies.md — universal patterns (step counter, tag-based queries, etc.)
- skills/conventions/reference-game-patterns.md — design moves to inherit, anti-patterns to avoid
- (carried) skills/code/universal-scaffold.md — applied at section 3 (sprite roster) and section 6 (HUD)

## Deliverables Produced

- mechanic-spec.md — full 9-section spec for `ej4t`
  - 3 mechanics across 3 levels (M1 chain push gated by ring; M2 extender pickup +1 R; M3 shrinker trap −1 R)
  - L1=1 mechanic, L2=2, L3=3 (+1/+1 increments per level)
  - Per-level: counterfactual lines for each mechanic, witness solution, 4 difficulty sub-bullets
  - Win predicate: all targets covered by crates
  - Lose predicate: `_steps_used >= _max_steps`
  - Action mapping: `[1, 2, 3, 4]` directional only
  - Sprite roster: 7 sprites (player, wall, crate, target, extender_pickup, shrinker_trap, ring_overlay)

## Notes

### Decisions made
- Picked R values per level: L1 R_init=2, L2 R_init=1, L3 R_init=2 — varied per level to make extenders necessary at L2/L3.
- Step budgets: L1=25, L2=30, L3=35 — increasing across levels per difficulty-rules.md § 2(d).
- Witness lengths: L1=5, L2=5, L3=7 — per-level budget is 5× witness or more.
- Chose ACTION5 NOT used — game is pure directional. Per `cross-cut-frequencies.md`, this fits the [1, 2, 3, 4] subset (ls20, tu93). Acceptable not to use ACTION5.
- Ring rendering via separate `ring_overlay` sprite re-rendered each tick — solves checklist item 19 (no hidden state for R).
- Visual richness (item 20): every primary sprite has internal pixel pattern (player has eyes/belt; crate has straps; target has yellow center + dark ring; extender looks like sprout; shrinker looks like X-hazard).

### Items potentially flagged for critique
1. L1 has only 1 mechanic — design-constraints requires >1 per ENVIRONMENT (not per level). L1 alone has 1 is fine; total environment has 3. ✓ per checklist item 8.
2. Initial R varies per level — this is a per-level parameter not a mechanic change. Documented via `level.get_data("init_R")`.
3. Counterfactual for M3 is subtle — relies on the trap forcing both extenders when 1 alone would suffice. Need critique to verify this is properly counterfactual.
4. L3 witness is a single straight east-walk (7 ACTION4) — same shape as L1 and L2. Risk that L3 is "L2 with bigger numbers" rather than genuinely new. Counter: M3 (trap) is genuinely a new mechanic; the player's mental model must include trap-shrinks-R. The visual/numerical difficulty bump matters.
