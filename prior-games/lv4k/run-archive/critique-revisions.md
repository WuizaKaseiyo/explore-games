# Critique Revisions — `lv4k` first pass

Two issues found. The spec must be revised before transitioning to `implement`.

---

## Issue #1 — L3 M3 (tilt-passenger-slide) counterfactual fails

**Checklist item violated**: 12 (strict counterfactual necessity / no trivial fallback).

**Offending spec section + quote**: § 4 Level 3 — Necessity per mechanic, M3:

> *L3 cannot be solved without triggering M3 because* starting passenger at +2; ANY single mass-2 placement at arm |2| or |3| causes |tilt_raw| ≥ 4 → passenger slides; reaching tilt_raw = 0 with 4 weights requires interim |tilt_raw| ≥ 4 in some sequences …

**Why it fails**: the counterfactual statement claims M3 is necessary, but with tray `[m2, m2, m1, m1]` and arms `{-3, -2, -1, +1, +2, +3}`, there exist winning sequences that *never* trigger `|tilt_level| ≥ 2` (i.e., never displace the passenger). Concrete counter-example:

- Step 1: m1 at +3 → tilt_raw = +3, tilt_level = +1 (using floor div: `3//2 = 1`). No slide.
- Step 2: m2 at -1 → tilt_raw = +1, tilt_level = 0. No slide.
- Step 3: m1 at -3 → tilt_raw = -2, tilt_level = -1. No slide.
- Step 4: m2 at +1 → tilt_raw = 0, tilt_level = 0. WIN. Passenger never moved.

Because the player can win L3 *without* M3 ever firing, M3 is not counterfactually necessary at L3. ANY 'yes' to "solvable without M" rejects per checklist 12.

**Concrete fix**: change L3 tray composition to `[m2, m2, m2, m1]` (3 mass-2 + 1 mass-1).

Verification that the new composition makes M3 necessary:

Solutions of `2a + 2b + 2c + d = 0` with arms distinct in `{-3,-2,-1,+1,+2,+3}`:
- m2 at `{-3, -1, +3}`, m1 at +2. (Verify: −6 − 2 + 6 + 2 = 0.)
- m2 at `{-3, +1, +3}`, m1 at -2. (Verify: −6 + 2 + 6 − 2 = 0.)
- (mirror images of the above).

For *any* such solution, every ordering of the 4 placements forces at least one step where `|tilt_raw| ≥ 4`. Proof sketch: starting tilt = 0; after step 1 the |tilt_raw| is at most 6 (if m2 at ±3) or 2 (if m2 at ±1, or m1 at ±2). To reach the final tilt = 0 from any non-trivial intermediate, one of the m2 placements at ±3 *must* eventually occur, contributing ±6 in a single step. Whether placed first or after stabilising m2 at ∓1 (which gives at most ±2), the m2@±3 placement produces |tilt_raw| ≥ 6 − 2 = 4. M3 fires every solution.

The counterfactual statement should be rewritten as:
> *L3 cannot be solved without triggering M3 because* every torque-zero solution requires at least one mass-2 weight placed at arm ±3, and a single mass-2 at arm ±3 contributes ±6 to tilt_raw. Even if preceded by a stabilising mass-2 at arm ∓1 (contributing ∓2), the resulting |tilt_raw| after the m2@±3 placement is at least 4 → tilt_level = ±2 → passenger displaces. No alternative arm assignment with 3 m2 weights and 1 m1 can avoid using ±3 (verified by exhaustive search of `2a + 2b + 2c + d = 0` with d ∈ {±1, ±2}).

**Companion change**: update the L3 witness to use the new tray.

A valid 8-action witness:
1. ACTION6@(4, 47) — select m1 in tray.
2. ACTION6@(48, 26) — place m1 at +2. tilt = +2, level = +1.
3. ACTION6@(12, 47) — select m2 #1.
4. ACTION6@(24, 26) — place m2 at -1. tilt = 0.
5. ACTION6@(24, 47) — select m2 #2.
6. ACTION6@(8, 26) — place m2 at -3. tilt = -6, level = -2 → **passenger displaces +2 → +1**.
7. ACTION6@(36, 47) — select m2 #3.
8. ACTION6@(56, 26) — place m2 at +3. tilt = 0. Tray empty + tilt = 0 → WIN. Passenger ends at +1, on beam.

Update the difficulty justification (c) for L3 to use this revised tray:

- Decision space at level start: 4 tray weights × 6 beam slots = 24 first placements.
- Trivial heuristic that fails: "place all mass-2 weights on one side first to form a counter-stack" — concrete counter-example: `m2@-3, m2@-1`. After step 1, tilt = -6 → passenger +2 → +1. After step 2, tilt = -8 → tilt_level = -2 → passenger +1 → 0. Slot 0 is the fulcrum (not in `exposed_arms`) → passenger off beam → `lose()`. The heuristic fails at step 2 of the level.
- Witness reasoning chain: post-discovery, the player must choose which m2 placement order keeps `|tilt_raw|` controlled enough that the passenger remains in `{-3..-1, +1..+3}`. Because every valid solution involves placing one m2 at ±3 (a +6 swing), and the passenger is initialised at +2, the player must ensure that swing happens at a moment when the passenger is at +1 or beyond toward the *opposite* tilt direction — implying a careful pairing of stabilising moves before the big swing.

---

## Issue #2 — `weight_blue` pixel design risks reading as the letter "O" or digit "0"

**Checklist item violated**: 7 (no letters / digits-as-glyphs).

**Offending spec section + quote**: § 3 Sprite roster, `weight_blue`:

> Mass-2 weight. Doubled-ring shape (two adjacent 4-cell ring motifs), palette `9` (blue) outer, palette `5` (black) inner.

**Why it fails**: a pair of side-by-side 4×4 rings reads visually as "OO" — the doubled letter O or doubled digit 0. Even abstractly, the eye groups two rings as a recurring motif that resembles symbolic glyphs.

**Concrete fix**: redesign `weight_blue` as a *single elongated frame* whose width (8 cells) communicates "double mass" through size, not through repeated motif. Pixel matrix:

```
[ 9, 9, 9, 9, 9, 9, 9, 9]
[ 9, 5, 5, 5, 5, 5, 5, 9]
[ 9, 5, 5, 5, 5, 5, 5, 9]
[ 9, 9, 9, 9, 9, 9, 9, 9]
```

This is one continuous frame — `mass_1 weight_orange` is a 4×4 frame; `mass_2 weight_blue` is a 4×8 frame. The visual relationship is "wider = heavier", a pure size cue without any glyph resemblance.

---

## No other items violated

I verified items 1–11, 13–20:

- (1) palette: only 0..15 used.
- (2) scaffold: deferred to implement; spec describes scaffold-conformant structure.
- (3) `available_actions = [6]`, subset of 1..7.
- (4) exactly 3 `Level(...)` entries.
- (5) ID `lv4k` non-colliding, lowercase, alphanumeric, not a word.
- (6) only basic-physics + objectness priors used.
- (7) (with Issue #2 fixed) no letters / digits / clipart / cultural conventions.
- (8) at least 2 mechanics: 3 declared (M1, M2, M3).
- (9) L1 = base dynamic system, M1 only, witness exercises M1, no on-screen text.
- (10) L2 + L3 increase by composition, not grid scaling.
- (11) mechanic counts L1 = 1, L2 = 2 (+1), L3 = 3 (+1) — within +1-or-+2 rule.
- (13) family `lever-balance-torque` absent from taxonomy of 25.
- (14) absent from prior-games index (19 priors).
- (15) `kx14` near-miss has concrete distinguishing rule articulated.
- (16) win condition specified (tilt = 0 & tray empty).
- (17) lose conditions specified (step exhaustion, L3 passenger off).
- (18) all 4 difficulty bullets per level present.
- (19) all internal state has visible cues.
- (20) every sprite has multi-pixel internal structure; shape carries semantic role (ring=liftable weight, triangle=fixed support, frame=slot, cross/halo=overlay).

---

## Verdict

Spec REJECTED. Apply both fixes (§1: re-tray L3 + re-witness L3 + re-derive L3 counterfactuals + re-derive L3 difficulty (c); §2: re-pixel `weight_blue`). Re-enter `write_spec`.
