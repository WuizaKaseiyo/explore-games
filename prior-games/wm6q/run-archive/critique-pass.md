# Critique pass (visit 2/10)

## Checklist verification

| Item | Description | Verdict |
|---|---|---|
| 1 | Palette 0..15 (and -1 transparent) only | ✅ tiles use {1, 2, 4, 8, 9, 11, 14, 15} content + 5/11 HUD + 4 padding |
| 2 | Universal scaffold structure | ✅ spec declares sprite bank, levels, constants, HUD widget, game class in order |
| 3 | `available_actions ⊆ [1..7]` | ✅ `[6]` (single-action) |
| 4 | EXACTLY 3 Level entries | ✅ §4 Level 1, Level 2, Level 3 |
| 5 | 4-char ID, lowercase, opaque, non-colliding | ✅ `wm6q` |
| 6 | Mechanics from core-knowledge-priors | ✅ objectness + basic geometry |
| 7 | No letters/digits/clipart/cultural conventions | ✅ abstract colored bands; lock = solid 6×6 black square; link = 6×6 ring outline |
| 8 | ≥ 2 distinct mechanics | ✅ rotate-via-click + locked-tile + linked-pair = 3 |
| 9 | L1 tutorial: base system, reduced state space, no on-screen text | ✅ 2 tiles, 1 mechanic, no text |
| 10 | L2/L3 difficulty by composition (not by scaling) | ✅ each level adds a new mechanic that interacts with all prior mechanics |
| 11 | Mechanic inheritance + (+1 or +2) per level | ✅ L1=1, L2=2 (+1), L3=3 (+1) |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ per-mechanic table per level + plausible-alternates enumeration; lock argued via visual-cue + win-predicate evaluation; linked-pair argued via mechanic-fires-on-every-click |
| 13 | Mechanic family absent from taxonomy-of-25-games | ✅ `edge-color-rotate-match` not in taxonomy |
| 14 | Mechanic family absent from prior-games index | ✅ not present in 70-entry index |
| 15 | Distinguishing rules for near-misses | ✅ cn04 (taxonomy) and qf8m (prior) both have concrete distinguishing rules |
| 16 | Win condition stated | ✅ "every shared edge between adjacent tiles carries the same colour on both sides"; `_check_win` predicate concrete in §7 |
| 17 | Lose condition stated | ✅ `_steps_used >= step_budget`; per-level budgets given |
| 18 | Per-level difficulty floor and ceiling (a/b/c/d bullets per level) | ✅ all 4 bullets present for L1, L2, L3 |
| 19 | No hidden state | ✅ rotation reflected in edge colours; lock state in 6×6 glyph; linked-pair state in shared ring glyph; step counter in HUD bar; no selection state |
| 20 | Display-pixel resolution rendering | ✅ 16×16 tiles with 4 edge bands of 3 px + 10×10 inner area + glyph; no upscaling |
| 21 | UI teaches | ✅ glyphs are role-distinguishing (lock = solid square = blocked; link = ring = paired); identical visuals for linked pair members signal correlated role |
| 22 | ACTION7 strict-undo or absent | ✅ ACTION7 absent from `available_actions` |

## Novelty re-verification on full spec

- **Taxonomy similarity-check:** the closest near-miss remains cn04
  (boundary-alignment via rotation). Re-run on the fleshed-out spec: cn04
  has free-form jigsaw pieces with arrow movement + ACTION5 rotation; this
  spec has fixed-position uniform tiles with click-only and click-rotates-
  edge-permutation. Distinguishing rule articulated in §9. **NOVEL.**
- **Prior-games similarity-check:** the closest near-miss remains qf8m
  (rook-cross-toggle). Re-run: qf8m's click flips a non-local cross of cell
  colours; this spec's click rotates ONE tile's 4-edge permutation locally.
  Distinguishing rule articulated in §9. **NOVEL.**
- **Negative-similarity walk on full spec:** the spec didn't introduce any
  new sprite kinds or mechanics that drift toward existing priors. The 6×6
  black-square lock glyph and 6×6 purple-ring link glyph are abstract and
  do not resemble any prior's surface signature. Walked against cn04 and
  qf8m: ≤ 2 dimensions of overlap each, well below the 3-dimension
  rejection threshold.

## Minor edits applied during critique
- Corrected `(2, 2)` linked-pair base from `(red, green, yellow, blue)` to
  `(red, blue, yellow, green)` (the previous base did not admit any rotation
  satisfying both `top = yellow` AND `left = blue` simultaneously). Updated
  the base table, the linked-pair derivation block, and the prose mention
  of the pair members' bases. Boundary-verification table values were
  already correct (they referenced the desired final-state edge colours, not
  the base) so no changes needed there.

## Verdict

ALL 22 CHECKLIST ITEMS PASS. NOVELTY: NOVEL on both axes. Transition to
`implement`.
