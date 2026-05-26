# Step #04: critique_spec (visit 1/10)

## Inputs Consumed
- mechanic-spec.md (this run): full 9-section spec.
- mechanic-pick.md (this run): mechanic family + ID.
- skills/design-constraints/checklist.md: 21 items.
- skills/design-constraints/composition-and-tutorial.md: level structure rules.
- skills/design-constraints/difficulty-rules.md: per-level difficulty bullets.
- skills/design-constraints/forbidden-elements.md: glyphs / clipart / cultural conventions.
- skills/mechanic-novelty/similarity-check.md: positive novelty rule.
- skills/mechanic-novelty/negative-similarity-check.md: negative novelty rule.

## Walking the checklist (1-21)

| # | Item | Verdict | Notes |
|---|------|---------|-------|
| 1 | Palette 0..15 (and -1 transparent) | PASS | Uses {0, 4, 6, 8, 9, 11, 12, 15}. |
| 2 | File structure matches scaffold | DEFERRED | Verified at implement state. |
| 3 | available_actions ⊆ [1..7] | PASS | [1..6]. |
| 4 | Exactly 3 levels | PASS | L1, L2, L3 listed. |
| 5 | 4-char ID, not in reference, not in priors | PASS | `nb6t` verified. |
| 6 | Mechanics from §3.4 priors | PASS | Objectness + geometry + kinematic-physics. |
| 7 | No glyphs/letters/clipart/cultural conventions | PASS | All sprites abstract; chain reads as articulated rod, not robot. |
| 8 | ≥ 2 mechanics | PASS | 4 mechanics. |
| 9 | L1 establishes base system, all required, no on-screen text | PASS | M1 + M2; both required (counterfactual confirmed); empty playfield. |
| 10 | L2 + L3 difficulty by composition not scaling | PASS | New mechanics layered, not larger grid. |
| 11 | +1-or-+2 mechanic-inheritance | PASS | L1=2, L2=3 (+1), L3=4 (+1). |
| 12 | Strict counterfactual necessity | PASS-WITH-CLARIFICATION | See finding #2 below. |
| 13 | Mechanic family absent from taxonomy | PASS | hinge-chain-reach not present. |
| 14 | Mechanic family absent from prior-games index | PASS | Not in 30 entries. |
| 15 | Distinguishing rule for any near-miss | PASS | Concrete rules vs s5i5, cn04, qz73, gx7m. |
| 16 | Win condition stated for env | PASS | L1/L2 tip-on-target; L3 object-on-drop-zone. |
| 17 | Lose condition stated | PASS | Step counter exhaust → lose. |
| 18 | Difficulty floor and ceiling per level (a)-(d) | **FAIL** | See finding #1 below — L1's (a) random-resistance estimate (~14%) is not "near-zero". |
| 19 | No hidden state | PASS | Active hinge halo, tip-carry halo, step bar all persistent. |
| 20 | Not low-resolution | PASS | 64x64 grid, scale=1, pixel-rich sprites. |
| 21 | UI teaches; sprite role legibility | PASS | Hinge=circle/joint, halo=highlight, tip=dot, target=ring, drop-zone=colour-matched-ring. |

## Novelty re-check on the full spec

Re-walking the negative-similarity test on the spec as fleshed out:

- **vs s5i5** (reference, rod-stretch family): the spec adds length-adjust (M3) at L2, which superficially aligns with s5i5's stretch-retract verb. Re-checking shared dimensions:
  1. board: chain + targets vs rods + targets — partial; chain is 1 connected, rods are N independent. Count NOT shared.
  2. input: ACTION5/ACTION3/ACTION1/ACTION2/ACTION6 vs ACTION6-only. Different. Not shared.
  3. goal: tip-on-target vs rod-tips-on-targets. **shared**.
  4. lose: step budget. shared.
  5. cast: hinges + segments + tip + targets vs sticks + colour swatches + markers + targets. Different. Not shared.
  6. visible visual signature: chain is one connected polyline of rectangles connected at hinge-circles; s5i5 is a collection of separate sticks plus a colour-swatch panel. Different. Not shared.
  7. pixel grain: both use rectangular rod-cells with rim+fill at 3-12 cells length. **shared**.
  8. core dynamic: articulated chain forward-kinematics vs independent stick stretch-and-rotate. Different. Not shared.

  Shared count = 3 (3, 4, 7). Borderline by count, but the heaviest dimensions (6, 7, 8) — only 7 is shared, so heavy axes diverge. PASS.

- **vs qz73** (rotation rotor): unchanged from pick-time analysis (4 shared, but heavy 6, 8 diverge). PASS borderline acceptable.

- **vs cn04** (single-piece rotation): the L3 carry-and-drop puts the candidate into a `pickup-and-place` framing not shared with cn04. cn04 has no carry mechanic. PASS.

- **vs gx7m** (gear cascade): unchanged. PASS.

- **vs other priors**: nothing new at the spec level.

Novelty verdict: **NOVEL** with the borderline qz73 acceptable on the heavy axes.

## Findings

### Finding #1 — L1 random-resistance fails the "near-zero" gate (checklist item 18 / difficulty-rules § 2.a)

**Spec section quoted** (`mechanic-spec.md` § 4 Level 1, Difficulty justification (a)):
> *"a uniform-random policy across the 4 valid actions {3,4,5,6} hits the witness sequence with probability (1/4)^4 ≈ 0.4% per consecutive 4-window. Over a 40-step budget there are ≈37 windows, giving cumulative success ≈ 14%."*

**Issue**: 14% cumulative success is NOT "near-zero" per the strict reading of `difficulty-rules.md` § 2.a. Even granting that `from-tech-report.md` § 6 says random-stumbleability is "acceptable" at L1, 14% is high enough that the spec's own justification flags it. A vision-blind agent has a 1-in-7 chance of accidentally clearing L1.

**Fix**: lengthen the L1 witness to ≥ 6 actions by relocating the base anchor and target so the witness requires at least one extra rotation. Concretely: move the base from `(8, 32)` to `(16, 32)` (so westward rotation is in-bounds), and move the L1 target from `(20, 8)` to `(4, 8)`. The witness becomes `[ACTION3, ACTION3, ACTION5, ACTION3, ACTION5, ACTION3]` (length 6) reaching pose `(W, N, N)` with tip `(4, 8)`.

Re-derived random-resistance: P(uniform-4 hits a length-6 specific sequence) ≈ (1/4)^6 ≈ 0.024%; cumulative over 40 windows ≈ 0.85%. Approximately near-zero. ✓

**Verification of new pose**:
- hinge_0 = (16, 32). seg_0 W12 → hinge_1 = (4, 32). seg_1 N12 → hinge_2 = (4, 20). seg_2 N12 → tip = (4, 8). ✓
- All cells in-bounds (0..63 inclusive on both axes).

**Also bumps**: keep step budget = 40 (still generous: 40 / 6 ≈ 6.7×).

### Finding #2 — M1 wording is over-narrow (checklist item 12 framing concern)

**Spec section quoted** (`mechanic-spec.md` § 4 Level 1):
> *"M1 cycle-active-hinge — ACTION5 advances the active-hinge index modulo N_hinges (here N_hinges = 3, so cycle is 0→1→2→0…). The active-hinge halo follows."*

**Issue**: M1 is described as if it requires ACTION5 specifically, but the spec also defines ACTION6 click-on-hinge to set the active hinge (§ 5 Action mapping). The mechanic's *distinguishing behavior* is "active-hinge index changes"; both ACTION5 and ACTION6 are valid implementations. As-written the spec is technically inconsistent with its own action mapping.

**Fix**: rename M1 to "change-active-hinge" and note in its description that ACTION5 cycles forward and ACTION6 click on a hinge sets active directly. The counterfactual claim ("L1 cannot be solved without M1 because…") still holds — without changing the active hinge from 0 (via either ACTION5 or ACTION6), only seg 0 is mutable.

This is a clarity revision, not a structural one — the spec already passes counterfactual; the wording just needs to match the action mapping section.

### Findings summary

Two revisions required:
1. Move L1 base + target so witness is ≥ 6 actions; recompute random-resistance.
2. Rename M1 to "change-active-hinge" and note both ACTION5 and ACTION6 as implementations.

Both are localised; no L2/L3 revision needed.

## Deliverables Produced
- `critique-revisions.md` (workspace/critique-revisions.md)

## Notes
- This is visit 1/10 to critique_spec.
- Revisions are tractable in one write_spec pass.
- After revision, expect critique to PASS on visit 2.
