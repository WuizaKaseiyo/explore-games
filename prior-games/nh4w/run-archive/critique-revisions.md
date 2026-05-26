# critique-revisions — round 1

The spec passes structural items 1-10, 13-17, 19-22 cleanly but has arithmetic and presentation issues in §4 (L1/L2/L3 mechanic numbers + witnesses + difficulty-justifications) that require rewrite. The mechanic family is sound; the geometry needs to be re-grounded.

## Issues

### 1. (Item 11/12/18) Max horizontal arc range is inconsistent across levels

The spec §5 declares "max horizontal range = 32 px" as a fixed game rule, but §4 arithmetic for L2's witness uses distances up to 32 (target at center 46) and L3's witness silently relies on a different range to make blue from x=8 reach the blue target at center 54 (a distance of 44, exceeding 32).

**Fix:** Choose ONE max-range value and apply consistently. Recommend `48 px` — large enough to reach across most of the 64-wide playfield, small enough that L1 still requires walking when the launcher starts at x=4 and a target sits past x=54. Update §5 and re-derive L1, L2, L3 witnesses against the new range.

### 2. (Item 12/18) L2 wall-clearance arithmetic is borderline under floor() rounding

The spec's L2 §4 narrative includes a mid-spec "REVISION" that lowered wall to height 8 from height 10, but the witness arithmetic from x=12 (origin 14) to target center 46 has arc altitude at wall midpoint x=26.5 of `10*4*0.391*0.609 = 9.52`. Under floor() collision-rounding this is `9`, which is `> wall_height 8` (clears) — but the margin is only one altitude unit. If a future implementer uses round() or ceil() the result changes. The witness should not depend on rounding choice.

**Fix:** Pick a wall height such that the witness's arc-altitude-at-wall has a robust gap (≥ 2 altitude units) under floor()/round()/ceil(). For L2 with launcher at x=4, target_yellow at x=60 center 62, max range 48, wall_h11 at x=24:
- From x=12 (origin 14, distance 48, peak 16) wall mid x=26.5: alt = `16*4*0.260*0.740 = 12.32` → floor 12 > 11 ✓.
- From x=16 (origin 18, distance 44, peak 14) wall mid x=26.5: alt = `14*4*0.193*0.807 = 8.72` → floor 8 not > 11 BLOCKED.
- From x=8 / x=4 distance > 48 → out of range, lands short.

This forces unique launcher x=12 and the wall is the binding constraint. Witness `[ACTION4, ACTION4, ACTION6@(60, 51)]` (3 actions).

### 3. (Item 12/18) L3 multi-target bind needs both wall and ceiling at exact thresholds

The spec's L3 §4 narrative includes "REVISION" notes (lower wall to 9 then "10" mid-section, ceiling clearances 13 vs 14) and the final witness arithmetic doesn't cleanly demonstrate the asymmetric "yellow from x=8, blue from x=12" claim. Under careful floor()-rounding arithmetic with max range 48:

- Yellow target at center 42, blue target at center 54, wall_h8 at x=24, ceiling1 at x=8 clearance 5, ceiling2 at x=32 clearance 13:
  - **From x=4** (origin 6, distance to yellow 36 in range, peak 12): ceiling1 mid x=11.5 alt = `12*4*0.153*0.847 = 6.21` → floor 6, not < 5 BLOCKED. Yellow blocked from x=4 ✓.
  - **From x=8** (origin 10) → yellow (T=42, distance 32, peak 10): ceiling1 alt = `10*4*0.0625*0.9375 = 1.88` → floor 1 < 5 ✓; wall x=26.5 alt = `10*4*0.516*0.484 = 9.99` → floor 9 > 8 ✓; ceiling2 mid x=35.5 alt = `10*4*0.797*0.203 = 6.47` → floor 6 < 13 ✓. Lands ✓.
  - **From x=12** (origin 14) → yellow (T=42, distance 28, peak 9): wall x=26.5 alt = `9*4*0.446*0.554 = 8.90` → floor 8, NOT > 8 BLOCKED. Yellow blocked from x=12 ✓.
  - **From x=16** (origin 18) → yellow (T=42, distance 24, peak 8): wall x=26.5 alt = `8*4*0.354*0.646 = 7.31` → floor 7, NOT > 8 BLOCKED ✓.
  - So yellow ONLY from x=8.
- Blue:
  - **From x=4** → blue (T=54, distance 48 max, peak 16): ceiling1 alt = `16*4*0.115*0.885 = 6.51` → floor 6, NOT < 5 BLOCKED ✓.
  - **From x=8** → blue (distance 44, peak 14): ceiling1 alt = `14*4*0.034*0.966 = 1.83` → floor 1 < 5 ✓; wall x=26.5 alt = `14*4*0.375*0.625 = 13.13` → floor 13 > 8 ✓; ceiling2 x=35.5 alt = `14*4*0.580*0.420 = 13.62` → floor 13, NOT < 13 BLOCKED ✓.
  - **From x=12** → blue (distance 40, peak 13): wall alt = `13*4*0.3125*0.6875 = 11.18` → floor 11 > 8 ✓; ceiling2 alt = `13*4*0.5375*0.4625 = 12.92` → floor 12 < 13 ✓. Lands ✓.
  - **From x=16** → blue (distance 36, peak 12): ceiling2 alt = `12*4*0.486*0.514 = 11.99` → floor 11 < 13 ✓; wall alt = `12*4*0.236*0.764 = 8.66` → floor 8, NOT > 8 BLOCKED ✓.
  - So blue ONLY from x=12.

This forces the 4-action witness `[ACTION4, ACTION6@(40, 51), ACTION4, ACTION6@(52, 51)]` and the named trivial heuristic "fire both shots from the same launcher x" GENUINELY fails (no shared position works for both targets).

**Fix:** Rewrite L3 §4 with these locked numbers (wall_h8, ceiling1 clearance 5, ceiling2 clearance 13, max range 48), drop the inline "REVISION:" notes, and present the level as a clean final design.

### 4. (Item 11/18) L1 needs walking required under max range 48

Original L1 had launcher at x=4 and target at center 42, with max range 32 — walk 1 step required. Under the new max range 48, the original L1 distance from start = 36 < 48, so direct fire works — M1 (walk) becomes not required.

**Fix:** Move L1's target further right so distance from start exceeds 48 px. Place target_yellow at x=56 (center 58). From start x=4 origin 6, distance to target center 58 = 52 > 48 → projectile lands short at x=54 (= origin + 48 = 54), projectile sprite spans x=53-55, target spans x=56-59 → no overlap, miss. Walk +4 to x=8 origin 10, distance 48 = max, projectile lands at x=58 = origin + 48, sprite spans 57-59, target spans 56-59 → overlap at 57-59 → win. Witness `[ACTION4, ACTION6@(56, 51)]` (2 actions). M1 (walk) genuinely required because direct fire from start misses.

### 5. (Presentation, item 11) Inline "REVISION:" notes in §4 obscure the final design

The spec's §4 presents L2 and L3 with mid-narrative revision notes ("REVISION: lower wall height to 8…", "REVISION: tighten ceiling2 clearance to 13…"). A reader cannot tell at a glance which numbers are the FINAL design vs the abandoned drafts. This makes the spec unreadable as a contract for the implementer and makes critique re-checking error-prone.

**Fix:** Rewrite §4 with the FINAL geometry only, no mid-section corrections. If revision history is useful, put it in the IO log or a separate appendix, not in the spec body.

### 6. (Item 18 d) Step budgets need tweak for new witness lengths

Original budgets (15/25/40) are fine in spirit, but with the corrected witnesses (2/3/4 actions), recommend keeping 15/25/35 as generous-over-witness (~7×, ~8×, ~9× the witness length).

## What is OK and need not be touched

- Sprite roster (§3) — all sprites use valid palette values, have meaningful pixel detail, no symbols/letters/digits, sprite shapes communicate role (launcher's upward muzzle, brick walls, tapered stalactites, hollow target frames).
- §5 action mapping — `[3, 4, 6]` is minimal and ACTION7 correctly omitted; gating descriptions are concrete.
- §6 HUD and per-game state — `StepBarHud` + named instance attributes are sound.
- §7/§8 win/lose predicates — testable boolean checks.
- §9 novelty note — distinguishing rules vs hk7v, vt6q, kn58, bx84, wt39, kj82, bp35, cd82, r11l are concrete and pass both positive and negative similarity tests.
- §2 mechanic family — the prior-coverage (objectness + geometry + physics) is correct.

## Verdict
Spec passes structural and novelty checks. Spec FAILS items 11/12/18 due to the geometry inconsistencies above. Transition back to `write_spec` for revision.
