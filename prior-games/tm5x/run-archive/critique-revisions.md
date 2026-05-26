# critique-revisions (1st pass)

Two material issues found. One forbidden-elements concern in the
sprite roster, and one decorative-mechanic problem at L3 that
fails checklist item 12 (strict counterfactual necessity).

---

## Issue 1 — checklist item 7 / `forbidden-elements.md`: temperature_field thermal-cell patterns read as the letter X

**Where**: spec §3, "temperature_field" entry — patterns for `+2`,
`-2` rows.

**Quote from spec**:

> `+2` (hot): `[[8, 7, 7, 8], [7, 8, 8, 7], [7, 8, 8, 7], [8, 7, 7, 8]]` — red flame X.
> `-2` (deep cold): `[[4, 10, 10, 4], [10, 4, 4, 10], [10, 4, 4, 10], [4, 10, 10, 4]]` — frost diamond.

**Violation**: the `+2` 4×4 pattern (with palette 8 corners and a
diagonal palette-7 cross through the centre) reads as a recognisable
letter "X" — the diagonals X out the square. `forbidden-elements.md`
forbids "Letters of any alphabet ... abstract shapes resembling
letters / objects are OK only if they are not RECOGNISABLE as the
language/object". This X-shape is recognisable. The `-2` "frost
diamond" shares the same diagonal arrangement — also reads as X.

**Fix**: replace the X-arrangement patterns with **rounded-square
fills** — solid centre with corner accent, no diagonals across:

- `-2` (deep cold): `[[10, 4, 4, 10], [4, 4, 4, 4], [4, 4, 4, 4], [10, 4, 4, 10]]` — solid off-black with light-blue corners. (Corners only; no diagonal.)
- `-1` (cool): `[[0, 10, 10, 0], [10, 10, 10, 10], [10, 10, 10, 10], [0, 10, 10, 0]]` — solid light-blue with white corners.
- `0` (neutral): `[[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]]` — solid white with off-white corners.
- `+1` (warm): `[[0, 7, 7, 0], [7, 7, 7, 7], [7, 7, 7, 7], [0, 7, 7, 0]]` — solid pink with white corners.
- `+2` (hot): `[[7, 8, 8, 7], [8, 8, 8, 8], [8, 8, 8, 8], [7, 8, 8, 7]]` — solid red with pink corners.

These look like **chamfered tiles** — corner accents, not diagonals.
Not letter-like.

Apply the same fix to pawn sprites for safety:

- `pawn_hot`: `[[5, 8, 8, 5], [8, 7, 7, 8], [8, 7, 7, 8], [5, 8, 8, 5]]` — black-cornered red icon with pink centre. (No diagonal; pure 2×2 inner square pattern.)
- `pawn_cold`: `[[5, 9, 9, 5], [9, 10, 10, 9], [9, 10, 10, 9], [5, 9, 9, 5]]` — black-cornered blue icon with light-blue centre.

The pawn keeps its border-with-internal-fill structure but the inner
2×2 is uniform (pink for hot; light-blue for cold) rather than a
diagonal pip. Distinguishing hot/cold relies on inner-fill colour
(pink vs light-blue), not on a rotated pip pattern.

---

## Issue 2 — checklist item 12: L3's insulator-wall mechanic is decorative

**Where**: spec §4 Level 3 — wall row at row 7 cols 4..12, witness
27 actions.

**Quote from spec**:

> Wall row at thermal-cells (4..12, 7) ... Walk attempts into a
> wall cell are rejected by the engine; the pawn stays in place.
> ... Removing the wall would let the witness be ~12 actions
> shorter and would change the path topology entirely.

**Violation**: the claim "removing the wall would let the witness
be ~12 actions shorter" is wrong on inspection. With the spec's L3
layout (pawn at (8, 1), target_hot at (3, 13), target_cold at
(12, 13), wall row 7 cols 4..12):

- *With wall*: pawn must DOWN×5 to (8,6), LEFT×5 to (3,6), DOWN×7
  to (3,13). 17 moves. Then ACTION5 + RIGHT×9. Total 27.
- *Without wall (wall removed)*: pawn could go DOWN×12 to (8,13),
  LEFT×5 to (3,13), ACTION5, RIGHT×9 to (12,13). 12+5+1+9 = 27.
  **Same step count.** Or DOWN×12 then LEFT×5 then ACTION5 then
  RIGHT×9 — same. The wall does not add steps; it only changes the
  shape of the path. Per checklist item 12, "a redundant decorative
  mechanic whose effect lands on the same destination the base
  mechanic would have produced anyway" is a violation.

**Fix**: redesign L3 so the wall genuinely lengthens the witness.
Place the wall so the **direct route** between pawn-start and one
target is blocked, forcing a strict detour.

**New L3 layout**:

- Pawn at thermal-cell (3, 1) hot.
- `target_hot` at thermal-cell (3, 13). Required +2.
- `target_cold` at thermal-cell (13, 13). Required -2.
- 12 `wall_insulator` cells at thermal-cells (8, 4), (8, 5), (8, 6),
  (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13),
  (8, 14), (8, 15) — full column-8 wall from row 4 down to row 15.
  Gap is rows 0..3 (top of grid).
- step_budget = 100 (replacing the previous 80, to maintain the
  "be generous" rule per `difficulty-rules.md` § d).

**New L3 witness** (43 actions):

```
ACTION2 ×12   # DOWN ×12: (3,1) → (3,13). target_hot latched (hot, +2).
ACTION5       # toggle to cold.
ACTION1 ×10   # UP ×10: (3,13) → (3,3). (Cross-grid above the wall row 4 start.)
ACTION4 ×10   # RIGHT ×10: (3,3) → (13,3). Through the gap (rows 0..3).
ACTION2 ×10   # DOWN ×10: (13,3) → (13,13). target_cold latched (cold, -2).
```

12 + 1 + 10 + 10 + 10 = 43 actions.

**Counterfactual check (now strict)**:

- *With wall*: 43 actions.
- *Without wall*: pawn at (3,1) → DOWN×12 to (3,13) hot, latch.
  ACTION5. RIGHT×10 to (13,13) cold, latch. 12+1+10 = 23 actions.
- Wall adds 20 actions. **Wall is non-decorative.** Removing it
  would shorten the witness by ~46% — the wall genuinely forces
  the routing.

The trivial heuristic-that-fails for the new L3:

- *Trivial heuristic*: "go to target_cold directly because pawn
  hot polarity already matches target_hot, so I'll save it for
  last". Pawn at (3,1) → ACTION5 (cold) → RIGHT×10 to (13,1) →
  DOWN×12 to (13,13). 1+10+12 = 23 actions. target_cold latched.
  But target_hot at (3,13) still needs visiting hot. ACTION5 →
  hot. UP×12 to (13,1) → LEFT×10 to (3,1) → DOWN×12 to (3,13). 1+12+10+12 = 35
  more actions. Total = 58. Worse than witness 43 by 15 actions.
  Significantly delays the win — fails the heuristic check.

**Apply this fix in the spec's L3 section (layout, witness,
counterfactual table, planning-depth justification, step budget).**

---

## Other observations (non-blocking; spec passes these)

- ✅ Item 1: palette only 0..15 used.
- ✅ Item 2: scaffold structure followed.
- ✅ Item 3: `available_actions = [1,2,3,4,5]` is a subset.
- ✅ Item 4: exactly 3 levels.
- ✅ Item 5: ID `tm5x` is 4 lowercase chars, not in references, not
  in prior-games-index. Verified.
- ✅ Item 6: mechanics from objectness, basic physics, basic
  geometry/topology — all in `core-knowledge-priors.md`.
- ✅ Item 7 (after Issue 1 fix): no letters/digits/clipart/cultural
  conventions.
- ✅ Item 8: 2 distinct mechanics (walk + aura-imprint at L1; +
  polarity-toggle at L2; + insulator-walls at L3).
- ✅ Item 9: L1 has reduced state space (no walls, single target),
  no on-screen text, all L1 mechanics required by witness.
- ✅ Item 10: L2/L3 increase difficulty by composing every prior
  mechanic AND the newly-introduced one. Grid size constant 64×64
  — no scaling-by-grid-size.
- ✅ Item 11 (after Issue 2 fix): N=2 at L1, M=N+1=3 at L2,
  P=M+1=4 at L3. Each promotion adds exactly 1 mechanic. None
  drop out.
- ✅ Item 12 (after Issue 2 fix): per-mechanic-per-level
  counterfactual table fills strictly.
- ✅ Item 13: family `thermal-aura-imprint` absent from taxonomy.
- ✅ Item 14: family absent from `prior-games/index.md` (29 entries
  scanned).
- ✅ Item 15: distinguishing rules concrete for every near-miss
  (pf3w, kp9z, gv47, vd3g, mr5q, lq5x, dc22, re86, ls20).
- ✅ Item 16: win condition is testable (every target latched).
- ✅ Item 17: lose condition is concrete (step counter at 0).
- ✅ Item 18: difficulty justification has all four bullets per
  level. After Issue 2 fix, L3's planning-depth points to a
  concrete failing heuristic.
- ✅ Item 19: no hidden state — polarity surfaced via pawn variant
  swap; latch surfaced via gold-frame target swap.
- ✅ Item 20: 4×4 thermal-cell patterns + multi-pixel pawn / target
  / wall sprites — not chunky uniform-colour blocks. After Issue 1
  fix, patterns avoid X-resemblance.
- ✅ Item 21: visual roles articulated — pawn = bordered avatar,
  rings = goals, walls = block-tiles. Pawn polarity cued by
  inner-fill (pink hot vs light-blue cold) after Issue 1 fix.

After applying both fixes, the spec passes. Re-run critique after
the revision.
