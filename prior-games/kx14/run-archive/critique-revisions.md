# critique-revisions — round 2

(Round 1 archived below for traceability. Two new issues found in round 2 — both substantive enough to warrant another round trip; the spec is the canonical handoff to `implement` and these must be correct.)

## Issue 2 — L1 witness action count is off by one

**Item violated.** §3.4 checklist item 16(b) (per-level human-tractable time) — depends on accurate action counts so the tractability claim is grounded. Also item §4 of the spec template ("the SHORTEST action sequence that wins L1, written out action by action").

**Offending section.** `mechanic-spec.md` §4 → "Level 1" → witness header reads:
```
- **Witness solution (10 actions).**
```
But the body has 4 ACTION1 + 5 ACTION4 = **9 actions**, not 10.

Trace: water rises 8→7→6→5→4 (4 ACTION1s) puts orange at (3,4). Tilt right 5 times moves orange (3,4)→(4,4)→(5,4)→(6,4)→(7,4)→(8,4) — that's 5 ACTION4s, total 9.

**Concrete fix.** Change "(10 actions)" → "(9 actions)" in the L1 header.

## Issue 3 — §6 re-projection pseudocode has high/low semantics inverted

**Item violated.** Implementation correctness — the §6 algorithm is the spec's canonical guidance for `implement`; if `implement` copies the pseudocode literally, the platform-block mechanic will be implemented incorrectly.

**Offending section.** `mechanic-spec.md` §6 → "Re-projection rule" pseudocode:

```python
if r > self.water_level:
    # Ball was below new surface; rises buoyantly.
    # Highest blocking platform_row P with water_level <= P < r
    P = self._highest_platform_in_col_in_range(c, self.water_level, r - 1)
    if P is not None:
        new_r = P + 1                          # rest just below platform
elif r < self.water_level:
    # Ball was above new surface (in air); falls to surface.
    # Lowest blocking platform_row P with r < P <= water_level
    P = self._lowest_platform_in_col_in_range(c, r + 1, self.water_level)
    if P is not None:
        new_r = P - 1                          # rest just above platform
```

**Bug.** In our coordinate system row 0 = top of grid, row 11 = bottom. So "highest platform" = topmost = smallest row number; "lowest platform" = bottom = largest row number.

For a **rising** ball (`r > water_level`, ball is submerged below surface, wants to rise to surface), the platform that BLOCKS it first is the platform CLOSEST to the ball's current row from below — i.e., the **largest-row** platform in the path range `[water_level, r-1]`. The pseudocode incorrectly asks for "highest" (smallest row), which would give the platform FARTHEST from the ball — wrong.

For a **falling** ball (`r < water_level`, ball is in air above surface, wants to fall to surface), the platform that blocks first is the platform CLOSEST to the ball from above — i.e., the **smallest-row** platform in the path range `[r+1, water_level]`. Pseudocode incorrectly asks for "lowest" (largest row) — wrong.

**Concrete fix.** Swap "highest" ↔ "lowest" in both helper-function names and comments. Specifically:
- Rising case: rename `_highest_platform_in_col_in_range` → `_max_platform_row_in_col_in_range` (returns the largest `platform_row` in the inclusive range) and update comment to "Largest-row blocking platform_row P with water_level ≤ P < r (closest platform from below)".
- Falling case: rename `_lowest_platform_in_col_in_range` → `_min_platform_row_in_col_in_range` (returns the smallest `platform_row` in the inclusive range) and update comment to "Smallest-row blocking platform_row P with r < P ≤ water_level (closest platform from above)".

Verify against L2 witness: orange at (1, 9), water 9→6 over 3 ACTION1s. After the 3rd ACTION1, water=6, orange was at (1, 7). Re-project: r=7, water=6, r > water. Want max-platform-row in col 1 in `[6, 6]` — that range has only one row (6), and platform exists at (1, 6). New_r = 7. Orange stays at (1, 7) ✓ matches the spec's witness comment "blocked at platform row 6".

The L1, L2, and L3 witnesses themselves are correct (each was traced by hand against the *intended* semantics); only the pseudocode that documents the algorithm is wrong.

---

# critique-revisions — round 1 (archived)

Treating the critique adversarially. The spec passes 16/16 + 10a checklist items and the novelty + negative-similarity checks unambiguously. The single substantive issue is presentational: the L3 witness sequence is presented twice — first an aborted draft with a "see correction below" inline comment, then the corrected sequence. A downstream `implement` reader could mis-read the first block as authoritative.

## Issue 1 — L3 witness has an inline aborted-draft block

**Item violated.** No specific checklist item directly, but the spec is the canonical handoff to `implement`; an ambiguous witness undermines spec-template item §4 (level progression with witness solutions). The §4 contract is "the SHORTEST action sequence that wins L3, written out action by action" — not "two sequences, one of them a discarded sketch".

**Offending section.** `mechanic-spec.md` §4 → "Level 3" → witness block 1:
```
ACTION6@(8,9)*,                                # anchor green ball at (8,9)
ACTION1, ACTION1, ACTION1, ACTION1,            # water 9→5; orange (3,9)→(3,5); green pinned at (8,9)
ACTION3, ACTION3, ACTION3, ACTION3, ACTION3,   # tilt left ×5; orange (3,5)→… wait, see correction below
```
followed by the "Correction:" callout and the corrected block 2.

**Concrete fix.** Delete the aborted block 1 and the "Correction:" preface entirely; present only the corrected witness (block 2) as THE witness. Renumber the action steps from 1..21 (without circled-glyphs if the visual ① ② ㉑ are noisy in the spec format — plain integers are fine). Keep the explicit click-pixel translation note at the bottom (`*` → `display = (col*5+2, row*5+2)`).

## Items checked, no issues found

### §3.4 compliance checklist

| # | Item | Verdict |
|---|---|---|
| 1 | Sprite palette in 0..15 (+ -1) | ✅ uses {1, 3, 4, 5, 10, 12, 14, -1} |
| 2 | File structure matches universal-scaffold | ✅ imports → sprite bank → levels → constants → HUD → Game class |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[1, 2, 3, 4, 6]` |
| 4 | EXACTLY 3 levels, structured per composition-and-tutorial | ✅ L1 base (N=2), L2 +platform (N+1=3), L3 +anchor (N+2=4) |
| 5 | 4-char ID, lowercase alnum, not English, no collision | ✅ `kx14` not in 25-set or in priors {kf42, qz73} |
| 6 | Mechanics from core-knowledge-priors.md only | ✅ physics + objectness + geometry/topology |
| 7 | No letters, digits-as-glyphs, clipart, cultural conventions | ✅ all sprites abstract; the "water-rises-on-UP" mapping is a discoverable physical rule, not a learned convention |
| 8 | At least 2 distinct mechanics in environment | ✅ 4 mechanics across the 3 levels (water-control, tilt, platform-block, anchor) |
| 9 | L1 = tutorial with reduced state space, no on-screen text | ✅ 1 ball + 1 target + no platforms + no anchor; both base mechanics required |
| 10 | L2 / L3 increase difficulty by COMPOSITION, not just scaling grid/items | ✅ L2 adds a topology constraint (platform); L3 adds an asymmetry primitive (anchor) — neither is "more of the same" |
| 10a | One new mechanic per level; every listed mechanic exercised by witness | ✅ L1 N=2; L2 N+1=3 (platform forces deflection in witness); L3 N+2=4 (witness anchors twice — the swap is impossible without anchor) |
| 11 | Mechanic family absent from taxonomy | ✅ `tide-tilt-buoyant` not in 25-row taxonomy; nearest neighbours sp80, g50t, m0r0, ar25, ka59 each addressed |
| 12 | Mechanic family absent from prior-games index | ✅ not in {kf42, qz73}; both addressed |
| 13 | Concrete distinguishing rules for any near-miss | ✅ §9 of the spec has concrete rules (verb-cardinality, agency-direction, topology, win-predicate) for every flagged row |
| 14 | Win condition stated | ✅ §7 — colour-strict ball-in-target-ring matching, evaluated after each action |
| 15 | Lose condition stated | ✅ §8 — single fail mode is step-counter exhaustion |
| 16 | Per-level: random-resistance + human-tractable + planning depth | ✅ §4 has all three sub-bullets per level; L1 near-zero planning depth, L2 deliberate multi-step, L3 strictly deeper than L2 (greedy "raise + tilt" defeats; only anchor-induced asymmetry resolves the swap) |

### Novelty re-walk on full spec (per `similarity-check.md`)

Re-running positive similarity-check on the full spec (not just the family name):

- vs `kf42`, `qz73`: distinguishing rules in §9 hold against the deeper view in `prior-games/<id>/mechanism-detail.md`.
- vs `sp80`: deep-analysis review confirms sp80's water is event-driven (instant cascade on ACTION5 fire, 4-pour budget) — kx14's persistent-surface model is qualitatively different. NOVEL.
- vs `g50t`, `m0r0`, `ar25`, `ka59`, `dc22`, `ls20`: each has at most one weak shared dimension after deep-analysis review.

### Negative similarity-check (per `negative-similarity-check.md`)

Re-walked the eight dimensions on the full spec against both priors and the four closest 25-game entries. No prior shares ≥ 3 dimensions; in particular dimensions 6 (visual signature), 7 (pixel grain), 8 (core dynamic) — the heaviest-weighted ones — diverge cleanly. The kf42→vh68 cautionary tale (small coloured pawns on dark walled grid) is explicitly avoided.

### Adversarial sweep — common failure modes

- *Spec drifted at L2/L3?* No — each level adds exactly one mechanic and the witness uses it.
- *Sprite reads as a digit/letter?* The 5×5 hollow target ring could marginally evoke a "0" or "O", but per `forbidden-elements.md` "ABSTRACT shapes resembling letters/objects are OK only if they are not RECOGNISABLE as the language/object" — at 5×5 resolution the ring reads as a topological symbol (a portal/socket shape), not a glyph. Acceptable.
- *Pseudo-multi-mechanic where L3 only uses one?* No — L3 witness exercises all four mechanics including both directions of M1 (raise + lower) and M2 (left + right).
- *Tutorial too hard?* No — L1 has one ball, one target, no obstacles, no anchor. 10-action witness using only the two base verbs.
- *Wrong level count?* No — exactly 3 levels.

## Verdict

One presentational issue (Issue 1). Transition back to `write_spec` for a clean revision; everything else passes on first review.
