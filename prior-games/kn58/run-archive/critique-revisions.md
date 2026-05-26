# Critique-revisions for kn58 — visit #1

Reviewing `mechanic-spec.md` against `design-constraints/checklist.md` (items 1–18) plus `mechanic-novelty/{similarity-check.md, negative-similarity-check.md}`.

## Pass on most items

- **Item 1 (palette 0..15 + −1):** PASS. All sprite pixel matrices use values from {−1, 0, 4, 5, 8, 10, 12, 14, 15}.
- **Item 2 (universal scaffold):** PASS at spec level. Spec describes scaffold-conformant structure (sprite bank → levels → constants → HUD widget → game class). Implementation will verify.
- **Item 3 (`available_actions` ⊂ [1..7]):** PASS. Spec declares `[5, 6]`.
- **Item 4 (exactly 3 levels):** PASS.
- **Item 5 (4-char ID, lowercase, alphanumeric, not reserved, not in priors, not English word):** PASS. `kn58` is 4 lowercase alphanumeric, not in the 25-game reserved list, not in `prior-games/index.md`, not an English word.
- **Item 6 (mechanics from `core-knowledge-priors.md`'s 4 categories):** PASS. Spec uses objectness + basic geometry/topology + basic physics. No agentness needed.
- **Item 8 (≥ 2 distinct mechanics):** PASS. Spec declares 7 (M1–M7).
- **Item 9 (L1 tutorial):** PASS. L1 = single pawn + single target on bare arena, mechanics M1+M2+M3 only.
- **Item 10 (L2/L3 increase difficulty by COMPOSING):** PASS. L2 same grid, adds collision/stick + 2nd pawn forced into pocket detour; L3 same grid, adds anti-anchor that fundamentally changes the gradient field.
- **Item 11 (mechanic inheritance + 1 or +2):** PASS. L1 = 3 mechanics, L2 = 5 (+2), L3 = 7 (+2).
- **Item 13 (family absent from taxonomy):** PASS. No `anchor-pull-magnet` or close family in `taxonomy-of-25-games.md`.
- **Item 14 (family absent from `prior-games/index.md`):** PASS. Closest tag is `anchor-pivot-place` (pz4t) — different verb (place polyomino) and goal (tile region).
- **Item 15 (distinguishing rules for near-misses):** PASS. Spec §9 + `mechanic-pick.md` enumerate rules vs ka59, m0r0, wa30, r11l, kf42, pz4t, plus brief notes on others. Each rule names a concrete mechanical difference.
- **Item 16 (win condition stated):** PASS. Spec §7 gives a testable predicate.
- **Item 17 (lose condition stated):** PASS. Spec §8: step counter zero → `lose()`.
- **Negative similarity walk on the fleshed-out spec:** PASS for kf42, gv47, pz4t, m0r0, wa30, qb84, lq5x, kx14, qz73, hr8q, ng52, pj7k, vn8d, fz5j; PASS borderline for ka59 (4 light dimensions shared but heavy axes 6, 7, 8 — palette, pixel grain, core dynamic — all diverge).

## Issues

### Issue 1 — Item 12 (no trivial fallback / strict counterfactual necessity): L3 witness does not exercise M6 (ACTION5 BURST)

**Quoted from `mechanic-spec.md` § Level 3 — Necessity per mechanic:**

> "M6 (BURST): once orange reaches (9, 8), it is at Manhattan distance 1 from anti-anchor (10, 8); a normal anchor pull east → (10, 8) lands orange ON anti-anchor where Phase 2 push has direction (0, 0) = no-op, so orange rests there. The next pull from (10, 8) to anchor at (12, 8): Phase 1 pulls east → (11, 8), distance to anti-anchor = 1 → Phase 2 pushes east (sign(11-10) = +1) → (12, 8) = target, M3 match, M5 stick. […] So BURST is not strictly required by the witness in this layout. **This is a spec gap that needs critique-driven revision.**"

The 12-action witness explicitly contains no `ACTION5` step. Per checklist item 12 ("for each mechanic available at level L, no strategy that avoids the mechanic's distinguishing behavior may solve L within the step budget"), the spec must guarantee that BURST is *required*. The current layout fails this gate.

**Concrete suggested fix.** The simplest robust fix is to *drop M6 from L3 entirely* and have L3 add only M7 (anti-anchor) as its single new mechanic. Reasons:

1. The harness rule "+1 or +2 new per level promotion" allows +1. L3 with only M7 added (= 6 total mechanics) is fine.
2. M6 (BURST) requires a layout in which the player must traverse a cell *against* the anti-anchor's repulsion direction. Constructing such a layout that *also* meaningfully exercises M4 (collision) and M5 (stick) is geometrically delicate; a hand-traceable witness for that layout has been attempted in three separate drafts and has produced > 25-action witnesses with subtle correctness gaps.
3. L3 still satisfies the "strictly deeper than L2" requirement: anti-anchor introduces a second force vector that combines with the anchor pull, requiring the player to reason about *net* displacement per tick instead of pure pull. The named trivial heuristic ("click the target every tick") still fails because anti-anchor pushes the pawn off-axis at the wrong moments, and the witness-pair commute test (see L3 § Difficulty justification) still holds.
4. Removing M6 also lets `available_actions` shrink to `[6]` (pure-click game) — visually distinct from arrow-using games and consistent with `cross-cut-frequencies.md`'s 19/25 click-only-or-mostly subset.

**Alternative fix (rejected as risky).** Keep M6 and rework L3 to require BURST. This was attempted via a wall layout that confines the pawn to row 8 and places anti-anchor in a position that pushes against orange's east motion. The construction kept producing layouts that were either unsolvable (collision deadlock) or solvable without BURST via an unintended gradient-tiebreak path. Without a verified witness this is unsafe to ship.

**Recommended action for `write_spec` revision.** Drop M6 from L3. Update:
- §4 Level 3 mechanic count: from 7 to 6 (= L2-count + 1).
- §4 Level 3 § Mechanics required by witness: remove M6 line.
- §4 Level 3 § Necessity per mechanic: remove the M6 paragraph; state explicitly "M6 is not introduced in this game; ACTION5 is removed from `available_actions`."
- §5 Action mapping: change to `available_actions = [6]` (pure click); remove ACTION5 entirely. Drop the BURST sub-rule.
- §3 Sprite roster: remove `pawn_green` and `target_green` (reserved-but-unused; per the harness's "no hidden mechanics", they shouldn't even appear in the sprite bank if no level uses them).
- §6 HUD and per-game state: remove `burst_pending` flag.
- Update §2 mechanic family description to drop the BURST sentence.

### Issue 2 — Item 7 (no letters / digits / clipart / cultural conventions): anti-anchor sprite description risks reading as "X"

**Quoted from `mechanic-spec.md` § 3 Sprite roster — anti_anchor:**

> "**anti_anchor** — 4×4, palette {4 off-black, 8 red, 5 black}: a red X with a dark central hole. […] Tag `anti_anchor`."

The pixel matrix as drawn:

```
[ 8, -1, -1,  8]
[-1,  4,  4, -1]
[-1,  4,  4, -1]
[ 8, -1, -1,  8]
```

While the *literal* pixels are 4 corner-dots + 2×2 dark center (no diagonal strokes), the spec's *prose description* names it "a red X". Letter recognition is a textual concern as well as a visual one — calling something an "X" is a hint to the reader that may also influence the implementation's pixel choices.

**Concrete suggested fix.** Rewrite the description and (if useful) the pixels:
- Description: "a red four-corner-dot frame with a dark 2×2 inner block." Drop "X".
- Pixels (alternate, more clearly non-letter):
  ```
  [ 8,  8, -1,  8]
  [ 8,  4,  4, -1]
  [-1,  4,  4,  8]
  [ 8, -1,  8,  8]
  ```
  An asymmetric, non-symmetric corner dapple — clearly not a letter.
- Or keep the original symmetric corner-dot pixels but only change the prose ("corner-dot frame with inner block").

The original symmetric pixels are likely fine under a strict reading of `forbidden-elements.md` ("ABSTRACT shapes resembling letters/objects are OK only if they are not RECOGNISABLE as the language/object" — 4 dots + a square is not unambiguously an X). But the prose hint is a smell.

### Issue 3 — Item 18 (difficulty floor and ceiling): L3 step budget calibration depends on whether M6 is removed

If Issue 1's recommended fix (drop M6) is applied, the L3 witness simplifies to the 12-action sequence already written. Step budget 60 (5× witness) remains generous. PASS once Issue 1 is addressed.

If Issue 1 is fixed by reworking the layout to require M6, the witness will lengthen and the step budget needs recalibration. This is a derivative concern.

### Issue 4 — Minor: spec re-states sprite scale conventions verbosely; can tighten

`mechanic-spec.md` § 3 spends a paragraph on coordinate convention ("playfield is 16×16 logical cells; each logical cell = 4×4 frame pixels"). This is fine but could move into a single line in the constants section of the implementation. Not a critique-blocker.

## Summary

Two real issues (1 + 2). Issue 1 blocks transition to `implement` because checklist item 12 fails. Issue 2 is a low-cost cleanup. Issue 3 is contingent. Issue 4 is cosmetic.

**Verdict:** transition back to `write_spec` with Issues 1 and 2 to fix.
