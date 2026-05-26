# critique-pass — `tg6w` mechanic-spec.md

## Pre-pass corrections applied

Two adversarial findings were resolved in-place on `mechanic-spec.md` before this pass:

1. **Sticky-pad pixel pattern** (item 7 risk). The original X-pattern `[[6,-1,6],[-1,6,-1],[6,-1,6]]` resembled a letter X, which `forbidden-elements.md` warns against ("ABSTRACT shapes resembling letters/objects are OK only if they are not RECOGNISABLE as the language/object"). Replaced with the plus-pattern `[[-1,6,-1],[6,6,6],[-1,6,-1]]` — a topological symbol explicitly permitted by `forbidden-elements.md`. References updated in §3 sub-cell-detail and sprite-role commentaries.

2. **L3 row-3 layout typo**: the ASCII diagram had 8 cells (extra leading `█`) where the lattice has 7. Fixed to `█ Y █ █ █ O █` matching the parenthetical clarification.

## Checklist (`design-constraints/checklist.md`) results

| # | Item | Pass? | Note |
|---|---|---|---|
| 1 | Palette values 0..15 (and -1)? | ✅ | Sprites use `{0, 1, 3, 4, 6, 11, 12}` and `-1` for transparency. All within range. |
| 2 | File structure matches universal-scaffold? | ✅ | Spec follows the prescribed 9-section template; implement state will produce code in the universal-scaffold ordering (sprites → levels → constants → HUD → game class). |
| 3 | `available_actions ⊆ [1..7]`? | ✅ | `[1, 2, 3, 4]` per §5. |
| 4 | EXACTLY 3 Level entries with composition? | ✅ | L1 (M1), L2 (M1 + M2), L3 (M1 + M2 + M3). Composition rule binary: each later level requires ALL earlier mechanics + the newly-introduced one. |
| 5 | Game ID 4 lowercase chars, opaque, not in reserved/prior? | ✅ | `tg6w`; verified in `mechanic-pick.md` against the 25 reference + 24 prior-games entries. Not a recognisable English word. |
| 6 | Mechanics from 4 priors only? | ✅ | objectness + physics + geometry/topology, all per `core-knowledge-priors.md`. |
| 7 | No letters / digits / clipart / cultural conventions? | ✅ (post-fix) | Sticky-pad pre-fix risked X-letter; replaced with `+` topological symbol. All other sprites are filled squares, rim-and-core squares, or coloured outlines — none form recognisable letters, digits, or real-world objects. |
| 8 | At least TWO distinct mechanics? | ✅ | Three mechanics (M1 slide, M2 colour-permeable rim, M3 one-shot sticky). |
| 9 | L1 tutorial: base dynamic system, all witness-required, reduced state space, no on-screen text? | ✅ | L1 has 2 yellow blocks + border walls only. M1 is the base dynamic. Witness `[ACTION2]` exercises it. Reduced state. No text. |
| 10 | L2 and L3 each compose all available mechanics (not scaling)? | ✅ | L2's witness requires M1 AND M2 at distinct cells (yellow rim at (3,3); orange rim at (5,3)); L3's witness requires M1 AND M2 AND M3 in concert (yellow uses M2 at (1,3), then M3 at (3,5); orange uses M2 at (5,3)). Each level is structurally distinct from grid-size-scaling. |
| 11 | Mechanic inheritance & +1-or-+2 rule? | ✅ | L1 = 1 (M1). L2 = 1+1 = 2 (M1, M2 — every L1 mechanic carried forward, 1 new). L3 = 2+1 = 3 (M1, M2, M3 — every L2 mechanic carried forward, 1 new). No level promotion introduces 0 or ≥3 new mechanics. |
| 12 | Strict counterfactual necessity (no trivial fallback) — per-mechanic enumeration | ✅ | Per-mechanic table below; alternates enumerated. |
| 13 | Mechanic family absent from taxonomy-of-25? | ✅ | `settle-pile-tilt` not in 25-game taxonomy. Closest entries (g50t, tu93, sp80, m0r0) addressed in §9 with concrete distinguishing rules. |
| 14 | Mechanic family absent from prior-games index? | ✅ | Not in the 24 prior entries. Closest entries (zd7m, wt39, kn58, kx14, kp9z) addressed in §9. |
| 15 | Distinguishing rule for every near-miss? | ✅ | All 9 near-misses cited in §9 (4 taxonomy + 5 prior-games) have concrete distinguishing rules: not vague "different colours" but specific verb / dynamic / cast distinctions. |
| 16 | Win condition stated? | ✅ | §7: every block on same-coloured target. Predicate is testable, deterministic. |
| 17 | Lose condition stated? | ✅ | §8: step exhaustion + soft-lock detection (lose() fires immediately when sticky-pad catches a block whose colour does not match a target at that cell, or any other state from which the win predicate cannot be satisfied). |
| 18 | Difficulty floor and ceiling — all 4 bullets per level? | ✅ | L1: (a) 1/4 random per press (tutorial-stumble OK per L1 guidance), (b) ~30s human, (c) no strict planning required, (d) budget 12. L2: (a) 1/16 random + recovery cost > 1/10000, (b) ~2 min, (c) 3 valid first actions / plausible-but-wrong LEFT-first / witness reasoning chain articulated, (d) budget 25. L3: (a) sticky-pad trap drops random p(win) well below 1/10000, (b) ~3 min, (c) decision space 3 ≥ L2's, trivial heuristic = greedy-DOWN-first → traps orange → soft-lock, divergence at action 1, (d) budget 30 (non-shrinking). All present. |
| 19 | No hidden state — visual cues for every mutated state? | ✅ | Block positions = block sprites. Sticky-pad consumed = caught block overlays the pad. Step counter = HUD bar. Gravity direction = ephemeral (slide animation IS the cue). Articulated in §6. |
| 20 | Visual detail floor (no-information-loss-at-32×32)? | ✅ | All sprites are 3×3 with 1-cell-deep internal contrast (filled-with-pip blocks, rim-and-core walls, plus-pattern sticky, outlined-with-transparent-centre targets). 2×2 average-pool would visibly damage the centre pip / core / plus-pattern relative to the outline — sub-cell detail is semantically load-bearing. |
| 21 | Sprite UI ≈ sprite role? Identical visuals imply correlated roles? | ✅ | Walls = solid grey (read as walls). Coloured-rim walls = walls + colour cue (read as "this colour passes"). Blocks = filled with pip (movable). Targets = same colour as block but outline-only (read as "block goes here"). Sticky-pad = unique plus-pattern in unique colour (read as "catch zone"). No two sprite kinds share visuals AND have unrelated roles; correlated kinds (block + matching target) share colour as the correlation cue. |

## Per-mechanic counterfactual table (item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (slide-to-end) | no | The only verb in `available_actions=[1, 2, 3, 4]` is the arrow-press → slide rule; both yellow blocks must traverse Δy = 4 from row 1 to row 5; no other rule produces position changes. |
| L2 | M1 (slide-to-end) | no | Same as L1 — the only verb. |
| L2 | M2 (yellow-rim permeability) | no | Yellow's target (1, 5) is below row 3 in column 1. Row 3 is `wall_solid` at (1, 3), (2, 3), (4, 3) and `wall_rim_orange` at (5, 3) (which blocks yellow). The ONLY yellow-permeable cell in row 3 is (3, 3). Yellow must slide through (3, 3) at some point — exercising M2. |
| L2 | M2 (orange-rim permeability) | no | Orange's target (5, 5) is below row 3 in column 5. Row 3 is `wall_solid` at (1, 3), (2, 3), (4, 3) and `wall_rim_yellow` at (3, 3) (which blocks orange). The ONLY orange-permeable cell in row 3 is (5, 3). Orange must slide through (5, 3) — exercising M2 at a distinct cell from yellow's. |
| L3 | M1 (slide-to-end) | no | Same — only verb. |
| L3 | M2 (yellow-rim permeability) | no | Yellow's target (3, 5) is below row 3. Row 3: `wall_solid` at (2, 3), (3, 3), (4, 3); `wall_rim_orange` at (5, 3) (blocks yellow); `wall_rim_yellow` at (1, 3) (yellow's only crossing). Yellow must slide through (1, 3) — M2 exercised. |
| L3 | M2 (orange-rim permeability) | no | Orange's target (5, 5) is below row 3. Same row-3 walls; orange's only crossing is (5, 3). Orange must slide through (5, 3) — M2 exercised at a distinct cell. |
| L3 | M3 (sticky-catch) | no | Yellow's target is (3, 5) — a mid-row interior cell with no `wall_solid` between it and the col-6 border in row 5 (cells (4, 5), (5, 5) are open or hold orange/orange-target). Without the sticky-pad at (3, 5), a yellow block sliding RIGHT through row 5 from any column < 3 would settle at (5, 5) (or (4, 5) if orange occupies (5, 5)). Without sliding LEFT through (3, 5) from column ≥ 4, yellow would settle at (1, 5) (border). The sole mechanism stopping yellow AT (3, 5) is the sticky-pad — M3 must be triggered by yellow. |

## Enumeration of plausible alternates (item 12 verification)

L1: random play has ~25% per-press chance of winning (DOWN). UP fails (no-op). LEFT/RIGHT shift blocks horizontally without crossing into row 5. Tutorial-stumble acceptable.

L2: post-discovery alternates explored:
- *LEFT first* — yellow at (3, 1) slides to (1, 1) (border); orange at (5, 1) slides to (2, 1) (blocked by yellow). Yellow now in column 1, where row 3 is `wall_solid`. Subsequent DOWN: yellow stops at (1, 2). Yellow can't cross row 3 from column 1. Recovery requires moving yellow back to column 3 with orange out of the way — non-trivial. Witness's DOWN-first preserves alignment.
- *RIGHT first* — yellow tries right; (4, 1) empty → (5, 1) orange → stops at (4, 1). Orange stays. Now yellow at column 4, can't cross row 3 at (4, 3) (`wall_solid`). Same recovery problem.
- *UP first* — both blocks already at row 1 against top border. No movement; step counter still drains. Wasted action; recoverable but wasteful.

L3: post-discovery alternates explored:
- *DOWN first (greedy-toward-target)* — yellow at (3, 1) blocked at (3, 3); stops at (3, 2). Orange at (5, 1) → (5, 5) ✓ on target. Now yellow at column 3 needs to reach yellow-rim at column 1. Subsequent LEFT slides yellow to (1, 2); orange (5, 5) slides LEFT through (4, 5), enters (3, 5) sticky-pad — orange CAUGHT at (3, 5). Soft-lock: orange occupies yellow's target; lose() fires.
- *RIGHT first* — yellow tries right; (4, 1) empty → (5, 1) orange → stops at (4, 1). Orange stays. Yellow now at column 4, far from yellow-rim. Recovery requires sliding yellow back left past orange.
- *UP first* — both at row 1, top border; no move; wasted step.

## Novelty re-check on the full spec (`similarity-check.md` + `negative-similarity-check.md`)

The fleshed-out spec was re-walked against the closest concerns from `mechanic-pick.md`:

- vs **zd7m cohort-step-route** (top concern): the spec's full mechanic — multi-cell slide-to-end with colour-permeable rims and one-shot sticky-pads — does not drift toward zd7m's anchor-portal-route family at any level. L2's stop-wall idiom is a generic full-blocking wall (not a colour-keyed step-blocker like zd7m's anchors). L3's sticky-pad is fundamentally different from zd7m's portal pair: portal teleports are reversible relocators, sticky is a one-shot catch that fixes a block forever. **Distinguishing rule holds at every level.**
- vs **wt39 glide-deflect-thaw**: still a single-pawn glide game; `tg6w`'s multi-block simultaneous slide with pile-up dynamics is a different cognitive task. wt39's bumpers (90° deflectors) and thaw-tiles (per-use brittle) are absent from `tg6w`; `tg6w`'s rim walls and sticky-pads are absent from wt39. No drift.
- vs **kn58 anchor-pull-magnet**: kn58's verb is click-to-place anchor with single-cell pull; `tg6w` has no click and slides multi-cell. Distinct.
- vs **kx14 tide-tilt-buoyant**: kx14 simulates fluid in a vertical tank; `tg6w` is discrete tile slide on a uniform grid. Distinct.
- vs **kp9z grain-accumulate-topple**: kp9z's grains grow via source-clicks and topple at capacity; `tg6w`'s blocks are fixed-count and slide only. Distinct.

Negative-similarity 8-dimension table (vs zd7m, the closest):

| Dimension | Shared with zd7m? |
|---|---|
| 1. Board content | shared (multi-block-on-grid) |
| 2. Player input | not shared (one-step vs slide-to-end) |
| 3. Goal | not shared (route to terminal vs settle on target) |
| 4. Lose | shared (step counter) |
| 5. Cast | not shared (anchors+portals vs walls+rims+sticky) |
| 6. Visual signature | not shared (post-fix palette divergence + plus-pattern sticky distinct) |
| 7. Pixel grain | shared (3×3 with internal pattern) |
| 8. Core dynamic | not shared |

Shared count: 3 (dimensions 1, 4, 7). At threshold; the heaviest dimensions (6 visual, 8 core dynamic) are divergent. **Verdict: NOVEL.** Below the rejection threshold.

## Verdict

All 21 checklist items pass. Novelty check returns NOVEL against every taxonomy + prior-game row. Negative-similarity check confirms no prior shares 4+ dimensions. **Spec accepted; transition to `implement`.**
