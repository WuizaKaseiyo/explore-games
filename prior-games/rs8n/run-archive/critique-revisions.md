# Critique pass 1 — issues found

Visit count to `critique_spec`: this is the **1st** entry per `state_log.md`. (Cap = 10.)

## Issue 1 — L3 setup contradicts witness step 8 (structural)
- **Checklist item violated:** § Format & structure (level setups must be self-consistent with the witness solution; checklist item 16 `win condition` and the spec-template requirement that the witness be the shortest path implicitly require the witness's stated avatar positions to be physically reachable).
- **Offending spec section:** `mechanic-spec.md` § 4 Level 3 *Setup*, which declares
  > "Wall at (5,10) and at (2,10) (so the sweep stops cleanly at the right end of the recolour line; the left end is bounded by the perimeter wall at (0,10) plus a wall at (2,10) that makes the row-10 segment self-contained)."
- And **§ 4 Level 3 *Witness solution* step 8**, which declares
  > "ACTION4 — face east + walk; (2,10)→ would walk east but (3,10) holds `item_pink_ring` (collidable), so rotation flips to 90° and walk is blocked. Avatar stays at (2,10), now facing east."
- **The contradiction:** if (2,10) is a wall, the avatar cannot stand at (2,10). The witness step 8 places the avatar there before firing ACTION5, which is impossible.
- **Concrete fix:** Remove the wall at (2,10) from the L3 setup. The wall at (5,10) alone provides the east bound for the row-10 sweep, and the perimeter wall at (0,10) provides the west bound for what's reachable. From any avatar position on row 10 with `x ≤ 2` facing east, an east-fired sweep enters (3,10)→pickup, (4,10)→pickup+shifter-recolor, (5,10)→wall stop. The witness's positional claim ("avatar at (2,10) facing east") then matches the geometry. Update the setup paragraph to read:
  > "Row y=10 (recolour line): items (3,10)=`item_pink_ring`, (4,10)=`item_pink_ring`. `shifter_green` floor tile at (4,10) under the second pink ring (layer 0, `INTANGIBLE`, non-collidable). Wall at (5,10) bounding the segment on the east; the west bound is provided by the perimeter wall at (0,10). Cells (1,10) and (2,10) are empty floor — the avatar must stand at (2,10) (or further west on row 10) before firing the row-10 sweep."

## Issue 2 — `item_yellow_xcross` reads as letter X (forbidden-elements)
- **Checklist item violated:** Item 7 (no letters / digits-as-glyphs / cultural conventions) per `forbidden-elements.md`'s rule that "abstract shapes resembling letters/objects are OK only if they are not RECOGNISABLE as the language/object."
- **Offending spec section:** `mechanic-spec.md` § 3 Sprite roster row `item_yellow_xcross`, with pixel matrix
  ```
  [[11,-1,-1,11],[-1,11,11,-1],[-1,11,11,-1],[11,-1,-1,11]]
  ```
  Rendered:
  ```
  X . . X
  . X X .
  . X X .
  X . . X
  ```
  This pattern places lit pixels on both 4×4 diagonals — a clearly-recognisable capital-letter X.
- **Concrete fix:** Replace with a **checkerboard** pattern that is regular and abstract but not letter-like:
  ```
  [[11,-1,11,-1],[-1,11,-1,11],[11,-1,11,-1],[-1,11,-1,11]]
  ```
  Rendered:
  ```
  X . X .
  . X . X
  X . X .
  . X . X
  ```
  Rename sprite key + tag from `item_yellow_xcross` / `shape_xcross` → `item_yellow_checker` / `shape_checker`. Update every reference in § 3, § 4 (level setups, witness, targets, counterfactuals), § 5 (none), § 7 (target signature comparison), § 9 (none).

## Issue 3 — `item_orange_diag` reads as a directional arrow (cultural convention)
- **Checklist item violated:** Item 7 (no cultural conventions / directional-arrow glyphs) per `forbidden-elements.md`'s "an arrow shape implying direction" example.
- **Offending spec section:** `mechanic-spec.md` § 3 Sprite roster row `item_orange_diag`, with pixel matrix
  ```
  [[12,12,-1,-1],[12,12,12,-1],[-1,12,12,12],[-1,-1,12,12]]
  ```
  Rendered:
  ```
  X X . .
  X X X .
  . X X X
  . . X X
  ```
  This reads as a diagonal arrow / chevron from top-left to bottom-right. Per `forbidden-elements.md`, an arrow shape implying direction is forbidden as a cultural convention.
- **Concrete fix:** Replace with a **solid rounded square / blob** that is clearly geometric, not directional:
  ```
  [[-1,12,12,-1],[12,12,12,12],[12,12,12,12],[-1,12,12,-1]]
  ```
  Rendered:
  ```
  . X X .
  X X X X
  X X X X
  . X X .
  ```
  Rename sprite key + tag from `item_orange_diag` / `shape_diag` → `item_orange_blob` / `shape_blob`. The new shape is a filled rounded square and the existing `item_pink_ring` is the *hollow* version of the same outline — visually the player can distinguish them by "solid vs hollow" which is a clean perceptual distinction (hollow ring = pink, solid blob = orange). Update every reference in § 3, § 4 (level setups, witness, targets, counterfactuals), § 7 (target signature), § 9.

---

## Items that PASS as-is (no revision needed)

- Item 1 (palette 0..15 only): all sprites use 0/1/3/4/5/7/9/11/12/13/14 + -1. Pass.
- Item 2 (universal scaffold): spec describes the planned imports/sprite-bank/levels/constants/HUD-class/game-class structure. Will be enforced at `implement`. Pass at spec stage.
- Item 3 (subset of [1..7]): `[1,2,3,4,5]`. Pass.
- Item 4 (exactly 3 levels): § 4 has L1, L2, L3. Pass.
- Item 5 (4-char ID, lowercase, not reserved, not in priors, not English): `rs8n` validated in mechanic-pick.md § 1. Pass.
- Item 6 (mechanics from core priors): objectness + geometry/topology declared in § 2. Pass.
- Item 7 (no letters/digits/clipart/cultural conventions): all PASS *after* Issues 2 + 3 are resolved. Other sprite shapes (ring, bar, anchor pillar, shifter dotted tile, walls) are clearly abstract / non-letter / non-arrow. The avatar's white "eye stripe" at row 0 is a 2-pixel marker that does not read as any letter or digit.
- Item 8 (≥ 2 distinct mechanics): L2 = sweep + anchor; L3 = sweep + anchor + shifter. Pass.
- Item 9 (L1 tutorial reduced state space, no on-screen text): single line of items, single mechanic, generous budget, no preview text. Pass.
- Item 10 (L2/L3 compose mechanics, not scale grid): L2 forces sweep+anchor partition; L3 forces sweep+anchor+shifter triple-composition. Pass.
- Item 11 (+1-or-+2 inheritance): L1=1, L2=2, L3=3, all carried forward. Pass.
- Item 12 (strict counterfactual / no trivial fallback): per-mechanic counterfactual lines provided in § 4. Independent enumeration of alternates done below.
  - **L2 alternate enumeration** (independent of the spec's claims):
    α. *Walk further east before sweeping.* Avatar's east walk blocks at (2,8) because (3,8) is a collidable item. Cannot reach a position east of (2,8) before firing.
    β. *Sweep on a different row/column.* Items are only on row 8. Sweeps on row 7, 9, etc. pick up nothing — useless.
    γ. *West-sweep from east of segment B.* Avatar walks south to row 9, east past (8,8), north to row 8, fires west. Sweep enters (8,8)→ring, (7,8)→bar, anchor at (6,8) stops. Reverse-assigns: ring→(7,8), bar→(8,8). Result (7,8)=ring (target wants bar/9), (8,8)=bar (target wants ring/7). **Mismatches segment-B target.**
    δ. *East-then-west composite sweeps on row 8.* East from west reverses segment-A (achieves segment-A target). West from east reverses segment-B (mis-places segment-B). Net: segment-A correct, segment-B mismatched. Two-sweep solution fails.
    ε. *East twice from west.* Second east sweep re-reverses segment-A back to initial. Fails.
    ζ. *Use a non-existent action.* Available_actions = [1,2,3,4,5]; ACTION6/ACTION7 are not declared. Cannot click/undo.
   None of α–ζ wins. Witness is the unique winning strategy modulo positional permutations of the avatar's first-walk steps — and all positional permutations that share the witness's "fire east from a west-of-(3,8) cell facing east" structure produce the same outcome.
  - **L3 alternate enumeration:**
    α. *Skip row-10 sweep.* Targets (3,10)=ring/14 unmet. Fail.
    β. *West-sweep across (4,10).* Avatar must be east of (4,10) on row 10. Cells (5,10) is a wall, (4,10) is an item. Avatar cannot stand east of (4,10) on row 10. **Unreachable; fail.**
    γ. *Skip row-5 sweep.* Targets (3,5), (4,5), (5,5) unmet. Fail.
    δ. *Sweep row 5 west-from-east.* Avatar east of (8,5), facing west. Sweep enters (8,5)→ring, (7,5)→bar, anchor at (6,5) stops. Reverse-assign: ring→(7,5), bar→(8,5). Mis-places segment-B target. Fail.
    ε. *Sweep row 5 east-then-west.* East gets segment-A correct; west scrambles segment-B. Fail (same as L2 δ).
    ζ. *Sweep row 5 east twice.* Re-reverses; back to initial. Fail.
    η. *Sweep row 10 east twice.* First east-sweep recolours one ring to green; second east-sweep again crosses shifter at (4,10), recolours the new tail-of-queue at that pickup (which is the second-pickup, again pink at this point) to green. Result: both rings green. Target wants (3,10)=green, (4,10)=pink. Fails.
   None of α–η wins. Witness (east-from-west on row 5, walk-south, east-from-west on row 10) is the unique winning strategy. Pass.
- Item 13 (mechanic-family absent from taxonomy): no overlap with any of the 25 reference families. Pass.
- Item 14 (mechanic-family absent from prior-games): no overlap with any of the 45 prior-games entries. Pass.
- Item 15 (distinguishing rules for near-misses): articulated for lp85 / r11l / vc33 (taxonomy) and qn7w / vt6q / qx7p (priors). Pass.
- Item 16 (win condition stated): § 7 gives concrete predicate. Pass.
- Item 17 (lose condition stated): § 8 gives concrete predicate. Pass.
- Item 18 (difficulty floor and ceiling per level): per-level § 4 has all 4 sub-bullets (a, b, c, d). L2 names plausible-but-wrong-path γ explicitly; L3 names trivial heuristic that fails ("the recoloured item ends at the shifter cell") and shows where heuristic diverges from witness. Pass.
- Item 19 (no hidden state): rotation visible via avatar's white eye stripe; position visible by avatar; sweep_phase visible during animation as the sweeper sprite. No latent state. Pass.
- Item 20 (don't generate a low-resolution game): grid 64×64, cell stride 4 = 16×16 logical cells, each gameplay sprite 4×4 with internal pixel structure (avatar with eye + body, walls grey-on-black brick, anchors with corner-and-centre pillar, items with distinguishable shapes — after Issues 2+3 fixes — checker / blob / ring / bar). 11-value palette in use. Pass.
- Item 21 (UI teaches): preview row shows desired arrangement; sprite roles legible (avatar = pawn-with-direction, walls = solid grey frames, anchor = bright-centre pillar reading as obstacle, items = saturated coloured shapes, shifter = green dotted tile reading as active surface). Pass.
- Item 22 (ACTION7 strict-undo or absent): omitted. Pass.

## Verdict
**REJECT** with 3 concrete revisions (Issues 1, 2, 3). All other checklist items pass. Transition back to `write_spec` for revision.
