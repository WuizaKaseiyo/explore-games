# critique-pass — round 2

Round-2 spec (`mechanic-spec.md`) re-verified against `design-constraints/checklist.md` items 1-22 and novelty rules in `mechanic-novelty/`.

## Checklist items

1. **Palette 0..15 + -1 wildcard.** ✅ PASS. All sprite pixel matrices use `[0..15] ∪ {-1}` only (`-1` for transparent in stalactite tapered tips, launcher muzzle silhouette, projectile glow).
2. **Universal-scaffold structure.** ✅ PASS (deferred to `implement`). Spec is structured to map onto the universal-scaffold cleanly.
3. **`available_actions` subset of [1..7].** ✅ PASS. `[3, 4, 6]`.
4. **EXACTLY 3 levels.** ✅ PASS.
5. **4-char lowercase ID, not in reserved/index.** ✅ PASS. `nh4w`.
6. **Mechanics from `core-knowledge-priors.md`'s 4 categories.** ✅ PASS. Objectness + basic geometry + basic physics (parabolic projectile motion is the canonical physics example).
7. **No letters / digits / clipart / cultural conventions.** ✅ PASS. Brick wall mortar lines are pattern, not letters; stalactite tapered shapes are abstract (not letters/digits); hollow-square targets are abstract framings; launcher pawn has no symbol-resembling features.
8. **≥ 2 distinct mechanics.** ✅ PASS. 4 mechanics by L3.
9. **L1 base dynamic system, all witness-required, no on-screen text.** ✅ PASS. M1+M2 both required by L1's witness; no on-screen text.
10. **L2/L3 compose every available mechanic.** ✅ PASS. L2's witness exercises M1+M2+M3 all together; L3's witness exercises M1+M2+M3+M4.
11. **Mechanic inheritance and +1-or-+2 rule.** ✅ PASS. L1=2, L2=3 (+1), L3=4 (+1). All carried-forward mechanics required at each level.
12. **Strict counterfactual necessity per (mechanic, level).** ✅ PASS. Per-mechanic counterfactual stated for every (M, L) pair; L3 includes explicit enumeration of all 4 reachable launcher positions for both targets, showing each blocking constraint by floor() arithmetic. The "verify by enumeration, not by abstraction" requirement is met.
13. **Mechanic family absent from taxonomy.** ✅ PASS. `arc-loft-shot` not in `taxonomy-of-25-games.md`.
14. **Mechanic family absent from prior-games index.** ✅ PASS.
15. **Distinguishing rule for any near-miss.** ✅ PASS. Concrete distinguishing rules vs hk7v, vt6q, kn58, bx84, wt39, kj82, bp35, cd82, r11l in §9.
16. **Win condition for environment.** ✅ PASS. All targets removed; engine auto-fires `self.win()` after L3's `self.next_level()`.
17. **Lose condition.** ✅ PASS. Step counter exhausted.
18. **Difficulty floor and ceiling per-level (4 bullets).** ✅ PASS. (a)/(b)/(c)/(d) all stated for L1/L2/L3. L2/L3 (c) post-discovery-planning includes decision-space count, named plausible-wrong heuristic, witness reasoning chain. Stage-conflation guard satisfied: the named wrong-path heuristics ("walk closest", "fire both from same position") are FULLY-INFORMED greedy choices, not discovery-stage missteps. Operational test passes: walking each heuristic from a fully-informed starting state produces a different action sequence than the witness, and the heuristic FAILS at a concrete constraint (L2 wall, L3 ceiling2).
19. **No hidden state.** ✅ PASS. Launcher position visible (sprite); projectile visible during flight; targets visible (and disappear when consumed = visible state change); step counter visible (HUD); no off-screen mode/selection state.
20. **Don't generate a low-resolution game.** ✅ PASS. Pixel-level design throughout (every pixel meaningful). Launcher 5×5 with multi-pattern internals. Walls 6-wide brick-pattern with mortar lines and brick-offset details. Stalactites tapered shapes with maroon tip. Projectile 3×3 with diamond-shape glow. Targets 4×4 hollow frames. No chunky upscale.
21. **Design UI to teach.** ✅ PASS. Per the three rules of thumb:
    - *Sprite UI ≈ sprite role.* Launcher's upward-pointing yellow muzzle visibly reads as "lobs upward" — distinct from a horizontal-firing cannon. Walls read as solid brick obstacles. Stalactites hang from the top with maroon tip, visibly reading as "things that drop down". Targets are hollow framed squares clearly distinct from any other sprite kind.
    - *Identical visuals imply correlated roles.* Target_yellow and target_blue share the same shape (4×4 hollow square) — correctly correlating their roles ("both are targets"); the only differentiator is color, which is the role differentiator (which target is which).
    - *Visuals carry the mechanic.* The arc is rendered visibly during animation (projectile sprite at varying altitudes). Wall heights are visible from sprite height. Stalactite clearances are visible from how far each stalactite hangs down. The mechanic is fully readable from rendered frames.
22. **ACTION7 strict-undo or absent.** ✅ PASS. ACTION7 omitted entirely; no slot 7 in `available_actions`.

## Novelty re-check (full spec)

Re-walked similarity dimensions against the FLESHED-OUT spec, not just the family name:

- vs **hk7v** (closest near-miss): The full L2/L3 spec confirms the parabolic-arc dynamic is the binding mechanic — wall heights and ceiling clearances both gate arc altitudes via per-frame collision checks. This is mechanically distinct from hk7v's discrete raise/lower/traverse routine. Visual signature differs (floor-bound launcher pawn vs overhead-beam gantry).
- vs **vt6q, kn58, bx84, wt39, kj82, bp35, cd82, r11l**: each remains distinct on core dynamic per §9.

Negative-similarity (8-dimension) re-walk against hk7v: still passes (3 dimensions partial-shared, 5 distinct, including the named principle dimensions 6, 7, 8 — visual signature, pixel grain, core dynamic).

## Verdict

**ALL 22 checklist items PASS. NOVELTY check returns NOVEL for every taxonomy + prior-game row.**

Transition to `implement`.
