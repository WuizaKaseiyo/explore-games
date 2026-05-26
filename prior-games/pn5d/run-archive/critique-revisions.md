# Critique revisions — round 1

Revisions required to `mechanic-spec.md` before transitioning to `implement`.

## Issue 1 — Item 7 (forbidden elements): `valve_closed` X-pattern is a Latin letter glyph

**Spec section**: §3 Sprite roster, `valve_closed` entry.

**Quote**:
> `valve_closed` — 2 wide × 4 tall, `[[3,3],[15,3],[3,15],[3,3]]`. … X-pattern (palette 15 cross on palette 3 grey).

**Problem**: The X-pattern is a recognisable Latin "X" letter glyph. Per `forbidden-elements.md`: *"Letters of any alphabet — Acquired symbolic knowledge."* Even though the spec describes it as "abstract", the 4-pixel two-diagonal pattern reads unambiguously as ×.

**Fix**: Replace the X-pattern with a non-glyph, non-symbolic shape that still visually distinguishes "closed" from "open". Suggested:

```
valve_closed: 2 wide × 4 tall, [[3,3],[3,3],[3,3],[3,3]]  # solid grey
valve_open:   2 wide × 4 tall, [[14,14],[14,14],[14,14],[14,14]]  # solid green (unchanged)
```

The colour-only contrast (green = open, grey = closed) is sufficient: same shape, different palette signals state-correlated identity (per checklist item 21 rule 2). The player learns the meaning from the obvious binary contrast and from the binary effect of clicking it (cursor over a closed valve, click → it becomes green; the connected pour behaviour changes).

## Issue 2 — Item 7 (forbidden elements): `pour_cursor` downward triangle is a directional arrow

**Spec section**: §3 Sprite roster, `pour_cursor` entry.

**Quote**:
> `pour_cursor` — 5 wide × 3 tall, downward triangle `[[-1,-1,11,-1,-1],[-1,11,11,11,-1],[11,11,11,11,11]]`.

**Problem**: A downward-pointing triangle is a directional indicator (▼). Per `forbidden-elements.md`: *"Cultural conventions — … an arrow shape implying direction."* The triangle "points" at the active vessel, leveraging the cultural arrow-as-pointer convention.

**Fix**: Replace with a non-directional shape that still cues "this is the focused vessel" via positional placement (above the vessel) without conveying direction. Suggested:

```
pour_cursor: 3 wide × 3 tall,
  [[11, 11, 11],
   [11, -1, 11],
   [11, 11, 11]]   # hollow yellow square / ring
```

A hollow square reads as a "selection bracket" (no direction), and the player learns "the bracket sits above the active vessel" from observation. Position alone communicates which vessel is selected; the bracket only marks "this column is the target of ACTION5".

## Issue 3 — Item 12 (strict counterfactual necessity): L3's M3 (overflow cap) is bypassed by a budget-fitting alternate strategy

**Spec section**: §4 Level 3 — necessity per mechanic, M3.

**Quote**:
> M3: L3 cannot be solved without M3 *under the budget-fitting strategy*. The budget-fitting strategy opens both valves, merges into group `{A, B, C}`, and pours 9 times … Conversely, the closed-valve strategy that bypasses M3 over-runs the budget (22 > 19) and loses, so M3 is the load-bearing rule that makes the budget-fitting strategy work.

**Problem**: The spec only enumerates *two* alternates (open-all and closed-all). Per `checklist.md` item 12 ("Verify by enumeration, not by abstraction"), the critique must enumerate the plausible alternate strategies a fully-informed player would consider. **One missing alternate**: *"open A-B only, leave C isolated"*.

Walking the alternate concretely:

1. `ACTION6` @ valve A-B → open. Group `{A, B}`, isolated `{C}`.
2. `ACTION5` × 9 (cursor on A, group `{A, B}`): A=9, B=9. **No clipping** because C never sees these pours.
3. `ACTION4`: cursor A → B.
4. `ACTION4`: cursor B → C.
5. `ACTION5` × 2 (cursor on C, group `{C}` alone): C=2.

Total: 1 toggle + 9 pours + 2 cursor moves + 2 pours = **14 actions**. Under L3's 19-action budget. M3 (the overflow cap) **never fires** in this strategy because C is never poured beyond 2.

So M3 is *not* counterfactually necessary at L3 as currently specified. Item 12 fails for the M3 row.

**Fix**: Re-architect L3 so that *every* alternate that bypasses M3 exceeds the step budget. The cleanest rebuild adds a **fourth vessel D** at L3 with a non-zero target, forcing the merge-strategy to be the only budget-fitting path:

- L3 layout: 4 vessels A, B, C, D (e.g., cols 8..15, 18..25, 28..35, 38..45). 3 valves: A-B, B-C, C-D, all starting `valve_closed`.
- C carries the `overflow_cap` at row y=20 (cap height 2). All other vessels uncapped.
- Targets: A=9, B=9, C=2, D=9.
- Step budget: 20 (witness 12, buffer 8 — matches L2's buffer of 8, no shrink).
- Witness: 3 toggles (open A-B, B-C, C-D) + 9 ACTION5 pours into the merged `{A, B, C, D}` group = 12 actions.
- Alternates re-enumerated:
  - **All-closed**: 9 (A) + 1 cursor + 9 (B) + 1 cursor + 2 (C) + 1 cursor + 9 (D) = 32 actions. > 20. Fails.
  - **Open A-B only** (analogous to the failure case above): 1 toggle + 9 (A,B group) + 2 cursors + 2 (C) + 1 cursor + 9 (D) = 24 actions. > 20. Fails.
  - **Open A-B and C-D** (group `{A,B}` and `{C,D}`): {A,B} pour 9 = 9 actions; {C,D} needs C=2, D=9 — **requires M3** to clip C as D rises. Without M3, this strategy is impossible (C and D are tied in the connected group, can't reach different surfaces without clipping). So this alternate IS using M3.
  - **Open A-B and B-C** (group `{A,B,C}` and `{D}`): {A,B,C} needs A=9, B=9, C=2 — **requires M3**.
  - **Open B-C and C-D** (group `{A}` and `{B,C,D}`): {B,C,D} needs B=9, C=2, D=9 — **requires M3**.
  - **Open all three valves** (witness): merged `{A,B,C,D}` needs A=B=D=9, C=2 — **requires M3**.

The only alternates that BYPASS M3 are the all-closed and open-A-B-only strategies, both of which exceed the 20-action budget. Therefore M3 is now strictly necessary at L3. ✓

**Re-derive L3 §4 entries** with the 4-vessel layout, the 12-action witness, the 20-action budget, the per-mechanic counterfactual table (M1, M2, M3 each with its own row per level), and updated difficulty justification (random-resistance, human time, planning depth, step budget).

L2 stays unchanged (3 vessels A, B, C, witness 10, budget 18, buffer 8). L1 stays unchanged (2 vessels, witness 4, budget 12, buffer 8). The buffer is stable (8) across all three levels — no shrink relative to witness.

## All other checklist items pass

For completeness: items 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18 (post-Issue-3-fix), 19, 20, 21 (post-Issue-1-fix; the colour-only valve contrast satisfies the rule-2 same-shape-correlated-roles condition since open/closed are correlated states of one valve), 22 all pass. Negative similarity check (`mechanic-pick.md`'s eight-dimensions walk) passes — the 4-vessel L3 still does not overlap any prior on three or more dimensions.
