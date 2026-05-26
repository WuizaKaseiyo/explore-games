# critique-revisions.md — visit 1

Spec failed two hard checks. Required revisions below.

## Issue 1 — checklist item 7 (forbidden-elements): forbidden sprite's X-pattern is a cultural symbol

**Section:** §3 Sprite roster, `forbidden`.

**Quote:**
```
- **forbidden** — 4×4, palette {8 red, 4 black}, tag `forbidden`. Internal pattern: red X across the cell — visually reads as a hazard/warning.
  [ 8, -1, -1,  8]
  [-1,  8,  8, -1]
  [-1,  8,  8, -1]
  [ 8, -1, -1,  8]
```

**Violation:** The X-shape is exactly the "X mark" example called out in `forbidden-elements.md`'s "directional arrows / X marks / ? marks" cluster — culturally read as "wrong / forbidden / dead" across players. §3.4 forbids cultural conventions in sprites.

**Fix:** Replace with a non-symbolic shape that reads as "blocked / danger zone" without invoking the X glyph. Recommended:
```
[ 8,  8,  8,  8]
[ 8,  4,  4,  8]
[ 8,  4,  4,  8]
[ 8,  8,  8,  8]
```
Solid red border with black interior block. Reads as "filled hazard cell" via colour density (red border = warning), not via symbolism.

## Issue 2 — checklist item 12 (strict counterfactual necessity): L2 has a trivial fallback

**Section:** §4 Level 2.

**Quote (problem):**
> forbidden_a at `(8, 6)`, forbidden_b at `(8, 9)` — two forbiddens between the two target pairs (a "no-go" middle column).
> ...
> A single big rectangular loop around all 4 targets would also enclose both forbiddens → 2 strikes, level loses on the 2nd big loop.

**Violation:** Strike threshold for lose is 3 (per §8 Lose condition). With only 2 forbiddens enclosed by a single big rectangle, strikes = 2 < 3 → level continues. The single big rectangle captures all 4 targets, making the win predicate fire → **L2 is solvable with ONE closure that triggers M3 (strikes) but doesn't actually require M4 (multi-closure) for the win**. M3 fires but doesn't BLOCK winning, so M4 isn't strictly necessary for L2's win.

This means item 12's per-mechanic check fails for M4 at L2 — there exists a 1-loop solution that wins, so the witness's 2-loop solution isn't the only way.

**Fix:** Add a third forbidden so any single big rectangle around all 4 targets encloses ≥3 forbiddens → 3 strikes → lose. Recommended layout:
- forbidden_a at `(8, 5)`, forbidden_b at `(8, 7)`, forbidden_c at `(8, 9)` — three forbiddens in a vertical column at x=8.

Re-verify witness (left loop x∈{3..5}, right loop x∈{11..13}): both loops still avoid x=8 entirely; both target captures still work. Add a sentence to L2's M3 necessity row clarifying "3 forbiddens in column x=8 → big loop = 3 strikes → lose".

## Issue 3 — checklist item 12 propagation: L3 inherits L2's trivial fallback

**Section:** §4 Level 3.

**Quote (problem):**
> forbidden_a at `(8, 6)`, forbidden_b at `(8, 9)` (same as L2).

**Violation:** Same trivial-fallback issue as L2 propagates. With 2 forbiddens, a big-rectangle alternate at L3 could win in 1 closure (ignoring the M5 pursuer if the closure is fast enough).

**Fix:** L3 inherits the revised 3-forbidden layout from L2's fix (forbiddens at (8,5),(8,7),(8,9)). The L3 witness (3 closures: left pair → right pair → pursuer) is unaffected since each loop already excluded x=8.

## Issue 4 — checklist item 21 polish (sprite UI ≈ sprite role): avatar's eye-dot reads as "creature face"

**Section:** §3 Sprite roster, `avatar`.

**Quote:**
```
- **avatar** — 4×4, palette {4 black, 9 blue, 11 yellow}, tag `player`. Internal pattern: rounded blue square with a yellow eye-dot in the upper-left so facing/identity is unambiguous.
  [-1, 9, 9, -1]
  [ 9, 11, 4,  9]
  [ 9, 4,  4,  9]
  [-1, 9, 9, -1]
```

**Violation:** Asymmetric yellow pixel inside a blue cell reads as a "single eye" — figurative imagery (a creature with an eye), borderline cultural-convention violation. Avatar facing isn't actually mechanic-relevant (movement is action-driven, not facing-driven), so encoding facing in the sprite is unnecessary.

**Fix:** Make avatar symmetric, no eye:
```
[-1,  9,  9, -1]
[ 9,  4,  4,  9]
[ 9,  4,  4,  9]
[-1,  9,  9, -1]
```
Blue ring with black centre. Same shape as `trail_cell` but different colour — this is INTENDED (item 21 rule 2 — "identical visuals imply shared correlated roles" applies here because trail IS where the avatar HAS BEEN; the shared shape encodes that correlation correctly).

## Issue 5 — checklist item 21 polish: pursuer's red eye-dots also read as "creature face"

**Section:** §3 Sprite roster, `pursuer`.

**Quote:**
```
- **pursuer** — 4×4, palette {13 maroon, 8 red, 4 black}, tag `pursuer`. Internal pattern: maroon-bordered cell with red eyes — visually reads as "active threat".
  [13, 13, 13, 13]
  [13,  8,  8, 13]
  [13,  4,  4, 13]
  [13, 13, 13, 13]
```

**Violation:** "Two red eyes above a black mouth" is figurative (creature with face), borderline cultural-convention.

**Fix:** Replace with abstract checker pattern that signals "different from other sprites" without facial features:
```
[13,  8, 13,  8]
[ 8, 13,  8, 13]
[13,  8, 13,  8]
[ 8, 13,  8, 13]
```
Maroon-red checker. Reads as "active / dynamic" without being figurative. Distinct from forbidden (solid red border) and target (solid yellow).

## Issue 6 — checklist item 21 polish (UI teaches the mechanic): closure feedback is too subtle

**Section:** §6 HUD and per-game state; §7 Win condition.

**Observation (not a hard violation, but improves item 21 rule 3 compliance):** The closure→capture rule is the load-bearing mechanic the player must discover. Currently the spec says "target sprite gets InteractionMode.REMOVED" with no animation. A 1-frame jump from "trail + target" to "no trail, no target" is a HARD READ — the player must connect cause and effect across one frame.

**Fix (recommended):** Add a brief post-closure flash phase to the spec. New internal state `_post_closure_flash: int` (initially -1; set to 0 on closure; ramps to 4 over 4 frames before consuming captures and clearing trail). During flash:
- Captured target sprites colour-cycle yellow→white→yellow→white before being set to REMOVED.
- Closed-loop trail cells colour-cycle pink→white→pink→white before being cleared (or converted to walls in L3).
- During flash, all player actions are no-ops (handled in `_get_valid_actions` by returning empty list).

This adds an OBSERVABLE per-frame change that teaches "your loop just captured these specific cells".

Add to §6 HUD/state and to §4's witness traces ("step 18 fires closure; flash ramps over 4 frames; level advances").

---

## Re-verification checklist (after applying fixes)

- [ ] §3 forbidden no longer has X-pattern.
- [ ] §3 avatar is symmetric (no eye).
- [ ] §3 pursuer is checker (no eyes/mouth).
- [ ] §4 L2 has 3 forbiddens at (8,5)(8,7)(8,9).
- [ ] §4 L2 M4 necessity row updated to cite 3-forbidden lose-on-3-strikes.
- [ ] §4 L3 has the same 3-forbidden layout.
- [ ] §6 HUD/state mentions `_post_closure_flash`.
- [ ] §4 witness traces note the flash phase between closure and level-advance.

Transition: back to `write_spec` for revision (visit count after this revision: visit 2 of critique_spec).
