# Critique pass — round 2

## Checklist items 1–20

| # | Item | Verdict |
|---|---|---|
| 1 | Palette 0..15 only | ✅ Uses 2, 4, 6, 9, 11, 12, 13, 14 (all in 0..15). |
| 2 | File structure matches universal-scaffold | ✅ Spec describes imports → sprite bank → levels → constants → HUD → game class layout. To be physically verified at implement-time. |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[6]`. |
| 4 | EXACTLY 3 levels | ✅ §4 has L1, L2, L3, no more no fewer. |
| 5 | 4-char lowercase ID, novel | ✅ `kp9z` — alphanumeric, not in reserved 25, not in prior-games index, not a word. |
| 6 | Mechanics from core-knowledge-priors | ✅ drop=objectness; topple=basic physics; sink=topology; redirector=topology + basic geometry (cardinal direction). |
| 7 | No letters/digits/clipart/cultural conventions | ✅ Frame-edge notch is positional (top/left/bottom) not an arrow glyph. Pip patterns are countable dots, not digit glyphs. No real-world iconography. |
| 8 | ≥ 2 distinct mechanics | ✅ L1 has 2 (drop, topple); environment has 4 across levels. |
| 9 | L1 tutorial with reduced state space, no on-screen text | ✅ 4×4 board, 1 source, 4 cardinal targets, 11 regulars; no hazards; no text/HUD beyond step counter bar. |
| 10 | L2/L3 increase via composition | ✅ L2's witness exercises every L1 mechanic + sink; L3's witness exercises every L2 mechanic + redirector. Each level's witness uses ALL mechanics carried forward. |
| 11 | Mechanic inheritance + 1-or-+2 per level | ✅ L1=2, L2=3 (+1), L3=4 (+1). All within rule. |
| 12 | Strict counterfactual necessity | ✅ §4 has per-mechanic counterfactual lines for each (level, mechanic) pair, naming the specific cells/sprites/rules that block every alternate path. Strict win predicate ("every cell at exact target_count") makes sink/redirector counterfactually necessary because cascade-byproducts at non-target cells would strict-fail the predicate. |
| 13 | Mechanic family absent from taxonomy | ✅ `grain-accumulate-topple` not in `taxonomy-of-25-games.md`. Closest is dc22 (colour-cycle-walk); distinguishing rule articulated. |
| 14 | Mechanic family absent from prior-games | ✅ Not in `prior-games/index.md`. Closest is vn8d (domino-cascade-topple); 5 distinguishing rules articulated. |
| 15 | Concrete distinguishing rule for near-misses | ✅ §9 articulates per-rule distinguishers vs vn8d, gx7m, gv47, fz5j, bx84, kn58, vk8m, dc22. |
| 16 | Win condition for environment as a whole | ✅ `_check_win` per level → `next_level()` advances; on the last level, base class `self.win()` fires per the universal scaffold. |
| 17 | Lose condition | ✅ `_check_lose` returns True when `steps_left ≤ 0`. |
| 18 | Difficulty floor and ceiling | ✅ Each level's §4 has (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget. L1: no strict planning. L2: 2 valid first actions, plausible-wrong "8-on-A overshoot" identified, witness reasoning chain stated. L3: 2 valid first actions (= L2's, never smaller), trivial heuristic "8-each-source" named as failing, divergence-from-witness traced (heuristic continues clicks 5..8 on A while witness moves to B; result diverges into target overshoot). |
| 19 | No hidden state | ✅ Every action's effect is visibly rendered: click source → yellow pip lights on source; topple → cardinals' pips flicker; sink/redirector cell types have permanent type-center colour AND distinct frame notches; redirector exit visibly shifts grain to (3, k) target. No hidden selection / mode / charge state. |
| 20 | Visual detail floor + shape-as-meaning | ✅ 10×10 sprite at camera scale 1× = 10×10 onscreen px. All features ≥ 2 sprite-pixels (frame thickness, pip 2×2, type center 2×2, edge notch 2×2). Survives 2×2 pool to 32×32 unchanged. Shape-as-meaning: Without colour, regular=blank, source=top frame notch + center block, sink=left frame notch + center block, target=corner pip(s) + center block, redirector_south=bottom frame notch + center block. Five types pairwise shape-distinguishable from pixel matrix alone. |

## Novelty verdict (similarity-check.md, re-run on full spec)

Walking the family + description-level checks against every taxonomy
row and every prior-games row:

- **Taxonomy (25 entries)**: zero matches on family-name (no taxonomy
  game uses "grain", "accumulate", "topple", or "overflow" as its core
  verb). Closest description-level near-miss is **dc22**
  (colour-cycle-walk: stepping cycles a tag-group); concrete
  distinguishing rule articulated in §9 (group-cycle vs per-cell
  overflow).
- **prior-games (26 entries)**: zero family-name matches. Description-
  level near-miss: **vn8d** (domino-cascade-topple — shares the word
  "topple"). Five concrete distinguishing rules in §9 (state cardinality,
  trigger, direction, verb cardinality, failure mode).
- All other prior-games rows (gv47, gx7m, fz5j, bx84, kn58, vk8m, etc.)
  show zero shared dimensions on the description-level check.

**Verdict: NOVEL** for every taxonomy + prior-games row.

## Negative similarity check (re-walked on full spec)

Walking the 8 dimensions vs the closest priors:

| Dimension | kp9z (this spec) | vn8d | gv47 | gx7m | fz5j |
|---|---|---|---|---|---|
| 1 board content | grid of cells with sub-cell pip patterns + frame notches | pillars in toppling pose | seed-spots growing into regions | gear-mesh of discs | tiles pulsing on a clock |
| 2 input verb | click source cells (drops) | click first domino | click seed; ACTION5 mix | click cluster; arrows | walk avatar with arrows |
| 3 goal | every cell at exact integer count | reach end markers | match target colour layout | match target rotations | reach goal cell |
| 4 lose | step budget | step budget | step budget | step budget | step budget; respawn loop |
| 5 cast | source/target/sink/redirector/regular cells | pillars, bursts, rotators, targets | seed-pips, ringed pips, regions | discs, ratchets, clutches | pulsing tiles, avatar |
| 6 visual signature | light-grey backdrop, type-center colour blocks + corner pips + frame notches | dark backdrop with bright pillars | seed-spots + spreading paint | gear discs in a mesh | pulsing tile pattern |
| 7 pixel grain | 10×10 sprite per cell, internal frame+pips+type+notch | 3×3 stars and pillars | round seed pips | round disc sprites | flat 1×1 tiles |
| 8 core dynamic | per-cell integer accumulation + overflow redistribution | one-click cascade through pre-posed pillars | continuous region grow + dissolve + mix | rotation propagation across mesh | time-driven pulse on per-cell schedule |

Pairwise shared-dimension counts (universal step-budget on dim 4 not
counted; click-as-input on dim 2 counted only when shape of click is
similar):

- vs vn8d: dim 8 soft-share via "topple" word (1 shared).
- vs gv47: 0 shared.
- vs gx7m: 0 shared.
- vs fz5j: 0 shared.

No prior shares 3+ dimensions with kp9z. **Negative check passes.**

## Verdict

All 20 checklist items pass. Novelty NOVEL on taxonomy and prior-games.
Negative similarity check passes (≤1 shared dim per prior). Spec is
ready for implement.
