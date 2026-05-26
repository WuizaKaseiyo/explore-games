# critique-revisions — round 1

Adversarial review of `mechanic-spec.md` against
`design-constraints/checklist.md` items 1-21 and the novelty +
negative-similarity checks. Four fixable issues found; novelty
clean.

## Issue 1 — checklist item 3: `available_actions` declared per-level, but the engine sets it once at `__init__`

**Section:** §5 (Action mapping), bullet for ACTION5.
**Quote:** *"Always valid in L3; not declared in `available_actions`
for L1/L2 (L1/L2 use `[1, 2, 6]`)."*
**Why it fails:** `NovaBaseGame.__init__` accepts a single
`available_actions=[...]` and applies it to every level — there is no
per-level `available_actions` override. The 25 reference games and
all priors take this as a global game-class property. The spec
implies a per-level switch that the engine doesn't provide.
**Concrete fix:** Declare globally `available_actions = [1, 2, 5, 6]`
in `__init__`. Use `_get_valid_actions()` to omit ACTION5 from the
agent's per-tick options when `_current_level_index < 2` (i.e., for
L1 and L2). Cite the same pattern used by `cn04`'s `_get_valid_actions`
and `sp80`'s `_get_valid_actions` — runtime gating, not static.
Restate in §5: "available_actions = [1, 2, 5, 6]; ACTION5 is
filtered out of `_get_valid_actions()` for L1 and L2 so the agent
cannot fire it before the L3 mechanic is introduced."

## Issue 2 — checklist item 7: scan-line caret marks read as arrows (forbidden cultural convention)

**Section:** §3 sprite roster, `scan_line_caret_left` /
`scan_line_caret_right` row + scan-line description.
**Quote:** *"Carets at columns 0..2 and 61..63 read as inward-
pointing arrows that pick out the row."* and *"the white scan-line
row + its yellow caret marks at the frame edges visibly translate."*
**Why it fails:** `forbidden-elements.md` lists "an arrow shape
implying direction" as a banned cultural convention. An "inward-
pointing arrow" is precisely an arrow glyph implying direction.
Even if the caret is small (3 × 5), if the player reads it as
"this points to the row", the cultural-convention test fails.
**Concrete fix:** Replace caret/arrow shapes with non-directional
markers. Two viable options:
1. **Square bookend caps** — a 3 × 3 solid yellow square at each
   frame edge level with the scan-line row, with no chevron or
   triangle shaping. Reads as "row marker", not arrow.
2. **Colon-style dots** — two stacked 1 × 1 yellow dots
   immediately above and below the scan-line row at each frame
   edge, total 5 cells per side, with no horizontal asymmetry.
Choose option 1 for stronger pixel grain (3 × 3 patches are easier
to see than 1 × 1 dots) and rewrite §3's `scan_line_caret_*` rows
accordingly. Drop the word "carets" (replace with "scan-line
markers" or "row markers") throughout the spec.

## Issue 3 — witness solutions are not shortest (spec template requires shortest action sequence per level)

**Section:** §4 witnesses for L1, L2, L3.
**Quote (representative):** L1 — *"`ACTION1 ×7` # shift column_b
up 7 segments"*. L3 — *"`ACTION1 ×7` # shift column_a +7"* and
*"`ACTION1 ×9` # shift column_e +9"*.
**Why it fails:** The spec template says *"the SHORTEST action
sequence that wins"*. Because `column.position` is cyclic mod 12,
shifting `+7` and `−5` reach the same target position, but `−5`
costs 5 actions vs 7 — strictly shorter. Same for `+9` vs `−3`.
Three of the spec's six shift counts are non-minimal:
- L1 `column_b` `ACTION1 ×7` → use `ACTION2 ×5` instead (saves 2).
- L3 `column_a` `ACTION1 ×7` → use `ACTION2 ×5` instead (saves 2;
  bound-pair partner shifts +5 to position 5 ≡ same target).
- L3 `column_e` `ACTION1 ×9` → use `ACTION2 ×3` instead (saves 6).

Witness totals after fix:
- L1: 17 → **15** actions. Step budget 40 still ≥2.6× witness.
- L2: 15 → **15** actions (no change — already minimal).
- L3: 23 → **15** actions. Step budget 100 ≥6.6× witness.

**Concrete fix:** Rewrite each level's witness to use whichever of
ACTION1 / ACTION2 produces fewer actions per column (= `min(k,
12 − k)` for a target shift of `+k`). Recompute the witness totals
in the difficulty justification (a) random-resistance argument and
(d) step-budget justification — both still pass with cleaner ratios.

## Issue 4 — checklist item 20: target patches differ only by fill colour (no internal distinguishing pattern)

**Section:** §3 sprite roster, `target_patch_a..e` row.
**Quote:** *"`target_patch_a..target_patch_e` | 6 × 3 | flat colour
from palette {8, 9, 11, 12, 14, 15} | `[\"target\"]` | Target strip —
one patch per column, painted in the colour the player must surface
on that column at the scan line."*
**Why it fails (mostly):** Checklist item 20: *"Two sprite kinds
that differ only by their fill colour (red blob vs. blue blob) are
not enough — give them distinguishing internal pattern."* The five
target patches differ from each other only in fill colour; no
distinguishing internal shape. They are HUD-ish in role but the
checklist makes no exception for HUD sprites. Risk: critique reads
the rendered frame and judges the targets as flat coloured blocks
that don't pull their own visual weight.
**Concrete fix:** Give each target patch a 1-pixel border in palette
3 (grey), turning it from `6 × 3` solid colour into an `8 × 5`
bordered swatch. The interior 6 × 3 keeps the target colour; the
border identifies the patch as a *label* (a framed swatch is a
recognisable representation of "this is a colour sample" without
relying on cultural convention or text). Update §3's row
accordingly. Aside: this also better visually couples each patch to
its column below (the framed swatch reads as a "this is the goal"
label rather than a stray coloured block).

## Items NOT flagged

- Checklist 1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
  19, 21 all pass on a careful read of the spec.
- Novelty: the §9 distinguishing rules and the re-run negative
  similarity check stand. No drift detected at L2 or L3 toward an
  existing taxonomy / prior. Specifically I re-checked qx7p's L3
  ("scan-line shift" + bound-pair) against `mr5q` (polarity-attract,
  ACTION5 = global tick) and `m0r0` (mirrored-quad, ACTION6 lever
  toggles single-control mode) — both have global ACTION5 / control-
  toggle verbs, but qx7p's ACTION5 changes WHICH ROW the win condition
  reads from, not which entity moves on which axis. Different
  semantics; no drift.
- Stage-conflation guard on L3 planning depth (difficulty-rules § 3
  (d) operational test): the L3 trivial heuristic ("shift both
  bound pairs at the start scan line") is a *post-discovery*
  failure (the player knows ACTION5 exists and what it does, but
  hasn't computed the modular-arithmetic constraint that pair 1's
  target sum is incompatible with offset 3). Clean.

## Action

Transition back to `write_spec` to revise. Issues 1-4 are all
concrete and resolvable in a single revision pass.
