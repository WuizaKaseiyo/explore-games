# critique-pass — round 2

Re-review of `mechanic-spec.md` after round-1 revisions. All four
critique issues addressed; checklist + novelty all pass.

## Checklist (`design-constraints/checklist.md`, items 1-21)

1. **Palette values** ✅ — colours used: {0, 3, 4, 8, 9, 11, 12, 14, 15} all in 0..15; `-1` used for transparency in column-bar borders. PASS.
2. **Universal scaffold** ✅ — §3 / §6 / §7 / §8 map cleanly to the scaffold sections. PASS.
3. **`available_actions` ⊆ [1..7]** ✅ — `[1, 2, 5, 6]` declared globally on the game class; per-level ACTION5 gating via `_get_valid_actions()` (cn04 / sp80 idiom). PASS (round-2 fix).
4. **Exactly 3 levels** ✅ — §4 lists L1, L2, L3, no more, no fewer. PASS.
5. **4-char ID** ✅ — `qx7p`, lowercase alphanumeric, not in 25 reserved or 29 priors. PASS.
6. **Mechanics from `core-knowledge-priors.md`** ✅ — objectness (column entities), basic geometry/topology (modular cyclic offsets, scan-line cross-axis), basic physics (bound-pair coupling = rigid linkage). PASS.
7. **No symbols/letters/digits/clipart/cultural conventions** ✅ — column-bar pixel patterns are colour bands with side borders (not glyphs); scan-line markers are 3 × 3 plain squares (no chevron / arrow); target patches are bordered colour swatches (no symbols); bound-pair ribbon is a flat orange line; scan_line is a flat white horizontal line. PASS (round-2 fix replaced chevron carets with non-directional squares).
8. **≥ 2 distinct mechanics** ✅ — L2 has 2 (column-shift + bound-pair); L3 has 3 (+ scan-line shift). PASS.
9. **L1 tutorial** ✅ — single mechanic (column-shift), 3 columns, no bound pair, no movable scan line, no on-screen text. Reduced state space relative to L2 / L3. PASS.
10. **L2 / L3 compose every available mechanic** ✅ — L2 witness exercises both M1 and M2 (any shift on a bound-pair column requires M2). L3 witness exercises M1, M2, and M3 (witness includes 2× ACTION5 + bound-pair shifts + unbound shift). PASS.
11. **+1-or-+2 rule** ✅ — N=1 at L1 → N+1=2 at L2 → 2+1=3 at L3. Every earlier mechanic remains required at later levels (column-shift used at all 3 levels; bound-pair coupling permanently active at L2 and L3). PASS.
12. **Strict counterfactual necessity** ✅ — §4's per-level "Necessity per mechanic" gives a one-line concrete blocker for every (mechanic, level) pair. L3's M3 necessity argument enumerates the bound-pair sum invariant explicitly and shows the start scan-line offset 3 makes both bound pairs unsolvable, forcing ACTION5. PASS.

    Per-mechanic table (sanity check per checklist item 12 format):

    | Level | Mechanic | Solvable without M? | Why not |
    |---|---|---|---|
    | L1 | M1 column-shift | no | start state shows wrong colour at scan line for every column; only M1 mutates `column.position`. |
    | L2 | M1 column-shift | no | start state shows wrong colour at scan line for every column. |
    | L2 | M2 bound-pair | no | bound-pair coupling fires on every M1 application to a paired column; no decoupling action exists; targets are antisymmetric so only the coupled shift produces them. |
    | L3 | M1 column-shift | no | start state shows wrong colour at scan line for every column. |
    | L3 | M2 bound-pair | no | both bound pairs permanently coupled; no decoupling action; antisymmetric targets at the pair-specific scan-line offset. |
    | L3 | M3 scan-line shift | no | bound-pair invariant `pos_a + pos_b ≡ 0 mod 12` is incompatible with the bound-pair target sum (4 mod 12) at start offset 3, AND with the bound-pair-2 target sum (10 mod 12) at start offset 3. Player MUST press ACTION5 at least once to reach a compatible offset; pair 1 needs offset 8 (idx=2), pair 2 needs offset 5 (idx=1), so ≥ 2 ACTION5 are mandatory. |

13. **Mechanic family absent from taxonomy** ✅ — no taxonomy entry has "column-shift" or "row-align" as a family; closest near-misses lp85, vc33, tr87, dc22 distinguished by §9 with concrete rules. PASS.
14. **Mechanic family absent from priors** ✅ — no prior has "column-shift" or "scan-line align"; closest mr5q, m0r0, qz73 distinguished by §9. PASS.
15. **Distinguishing rules for near-misses** ✅ — §9 provides one or more concrete distinguishing sentences per near-miss (lp85, vc33, tr87, dc22, cn04, qz73, mr5q, m0r0, vd3g, kp9z, gv47, vn8d). Re-validated against the deeper deep-analysis-3lvls evidence layer for the four taxonomy entries. PASS.
16. **Win condition stated** ✅ — §7 gives the concrete predicate: for every column, `colours[(column.position + offset(scan_line_idx)) % 12] == target_patch[column].pixels[1, 2]`. PASS.
17. **Lose condition stated** ✅ — §8: step counter = 0 → `self.lose()`. No instant-fail collision; all shifts reversible (via opposite arrow), so no soft-lock. PASS.
18. **Difficulty floor and ceiling** ✅ — every level states (a) random-resistance with concrete numbers, (b) human time, (c) discovery + planning depth (with post-discovery alternative named for L2 / L3 plus stage-conflation guard cleared), (d) step budget (40 / 70 / 100, never shrinking, all generous over the now-15-action witnesses). PASS.

19. **No hidden state** ✅ — every mutated state has a persistent visual cue: active column → flanking white highlight strips; bound-pair → orange ribbon + dot endcaps; scan_line_idx → scan-line sprite y-position visibly different at each idx; column.position → entire column pixels rolled (visible band offsets); step counter → top-row HUD bar. PASS.

20. **Pixel-detail richness** ✅ — `grid_size = (64, 64)` (no upscale). Columns are 6 × 36 with 1-px side borders + 12 × 3-row colour-band stack (rich internal pattern; each column has a distinct band sequence — colour pattern is a per-column fingerprint, not a fill colour). Target patches are 8 × 5 with 1-px grey border around 6 × 3 colour interior (round-2 fix from flat 6 × 3). Bound-pair ribbon + 2 × 2 endcap dots; scan-line + 3 × 3 yellow square bookends; active-highlight 1 × 36 strips; step-counter HUD bar. The rendered L1 frame would read as: a top-bordered target strip → a clear gap → three vertical band-stack columns with thin side rails → a yellow-anchored white scan-line cutting through their middle → a bottom dark margin. Detailful, considered, not coarse blocks. PASS.

21. **UI teaches the mechanic** ✅ — § 3 lays out three rules-of-thumb the spec satisfies:
    1. *Sprite UI ≈ sprite role.* Columns read as "tall sliding bars" (the band-stack visual implies linear cyclic content scrolling past a window). Target patches read as "this colour goes here" (framed colour swatches above each column). Scan line + bookends read as "this is the row that matters" (a continuous bright row + edge anchors). Bound-pair ribbon reads as "these two are tied together".
    2. *Identical visuals imply shared roles.* Two bound-pair columns share the orange-ribbon visual, signalling shared (coupled) behaviour. Two unbound columns share the no-ribbon visual, signalling independent behaviour. The five target patches share the bordered-swatch visual but with different fill colours, signalling "same role (target indicator), different goal colour" — a meaningful colour-only distinction in the *label* layer rather than the *gameplay* layer.
    3. *If the visual cannot carry the mechanic, change the representation.* The bound-pair coupling is the trickiest mechanic to communicate without text. Three layered cues are used: ribbon + dot endcaps (static), and observation that shifting one bound member visibly slides the partner in the same animation tick (dynamic). The first dynamic shift on a bound column is the moment of mechanic discovery; the player sees both columns translate in opposite directions at once and infers the rule. PASS.

## Novelty (`mechanic-novelty/`)

- **Family-level check** vs taxonomy + priors: no match. PASS.
- **Description-level check**: §9 articulates concrete distinguishing rules for every near-miss, validated against the deeper `deep-analysis-3lvls/<id>/<id>-deep-analysis.md` evidence layer for taxonomy entries. PASS.
- **Negative-similarity-check** (8-dim): re-walked on the full revised spec; no single prior shares 3+ dimensions with qx7p. The fleshed-out L2 / L3 mechanics did NOT drift toward an existing taxonomy / prior on second look. PASS.
- **Verdict: NOVEL.**

## Action

Transition to `implement`. Spec is clean.
