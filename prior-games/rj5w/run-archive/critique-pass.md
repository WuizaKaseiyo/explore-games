# Critique pass — round 2

`mechanic-spec.md` (revision 1) reviewed against
`design-constraints/checklist.md` items 1–21 plus the novelty
gates. All pass.

| # | Check | Verdict |
|---|---|---|
| 1 | Sprite palette values within 0..15 (and -1 transparent) | ✅ uses {0, 1, 3, 5, 6, 11, 12, 14, 15, -1} only |
| 2 | File structure follows `code/universal-scaffold.md` | ✅ planned per scaffold (imports → sprites → levels → constants → HUD → game class) |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[1, 2, 3, 4, 5, 6]` |
| 4 | EXACTLY 3 `Level(...)` entries | ✅ L1, L2, L3 |
| 5 | 4-char ID, lowercase, not in references, not in `prior-games/index.md`, not English | ✅ `rj5w` |
| 6 | Mechanics drawn only from `core-knowledge-priors.md` four categories | ✅ geometry/topology + objectness |
| 7 | No letters, digits-as-glyphs, real-world clipart, cultural conventions | ✅ pawn pattern is abstract 4-fold-symmetric green-with-black-diamond + white-cross-notches; target ring is hollow square; fold-line is striped column |
| 8 | At least TWO distinct mechanics | ✅ 4 mechanics by L3 |
| 9 | L1 = tutorial with reduced state space, no on-screen text | ✅ 1 pawn + 1 target + 1 fold-line, no text |
| 10 | L2 / L3 add difficulty by composition, not scaling | ✅ L2 adds H-fold + axis-toggle (composition); L3 adds lock-on-target (composes with V/H folds via the double-V-fold trick) |
| 11 | Mechanic inheritance + +1-or-+2 per level promotion | ✅ L1=1; L2=3 (+2); L3=4 (+1); all earlier mechanics carried forward and witness-required |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ per-mechanic per-level necessity arguments include the M4 (lock) exhaustive enumeration showing no fold sequence wins L3 without it |
| 13 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ `axis-fold-mirror` not in taxonomy; closest is `ar25` (shape-mirror-cover) — distinguishing rule articulated |
| 14 | Mechanic family absent from `prior-games/index.md` | ✅ none of the 36 indexed priors (or fb7t) is a fold/axis-reflect game |
| 15 | If similar to taxonomy/prior, distinguishing rule is concrete | ✅ concrete rules in §9 (vs ar25, m0r0, cn04, lp85, sk48; vs bx84, tg6w, pz4t) |
| 16 | Win condition stated for all levels | ✅ "every pawn coincident with its colour-matched target" |
| 17 | Lose condition stated (or "no lose" with reasoning) | ✅ "step counter exhaustion" |
| 18 | Difficulty floor and ceiling — (a) random-resistance, (b) human time, (c) planning depth, (d) step budget — for each of L1, L2, L3 | ✅ all four bullets present per level; L2's wrong-alternative (V-only translation) is post-discovery; L3's heuristic (single-fold-each-axis) and divergence point (step 6, the second V-fold) are concrete |
| 19 | No hidden state (visual cue for every mutated piece of player-reasoned state) | ✅ active_axis cue (orange/grey color); locked_pawns cue (dim color-remap); F_v/F_h cue (cursor position) |
| 20 | Don't generate low-resolution game (pack visible detail at display-pixel level) | ✅ grid is native 64×64; 5×5 patterned pawns and targets; no upscaling |
| 21 | UI to teach (sprite UI ≈ role, identical visuals share roles, change representation if visual can't carry mechanic) | ✅ matching colors mean matching roles (pawn ↔ target by colour); fold-line cursors are crease-like; locked pawns are visibly dimmed |

## Novelty
- **Positive similarity-check** (`mechanic-novelty/similarity-check.md`): runs against every taxonomy entry and every prior-games row. The closest entries (`ar25`, `m0r0`, `cn04`, `lp85`, `sk48`, `bx84`, `tg6w`, `pz4t`) all have concrete distinguishing rules in spec §9. Verdict: **NOVEL**.
- **Negative similarity-check** (`mechanic-novelty/negative-similarity-check.md`): walked the eight dimensions against every prior; the maximum shared-dimensions count for any single prior is 2 (vs. `ar25` on dim 8, vs. `wa30` on dim 5 + partial dim 7), well under the 3-dimension reject threshold. Verdict: **NOVEL**.

## Verdict
**PASS — transition to `implement`.** No revision needed.
