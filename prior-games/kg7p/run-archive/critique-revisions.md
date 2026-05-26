# critique-revisions — kg7p, critique pass #1

## Per-mechanic counterfactual necessity table (per checklist item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 walk-avatar | no | Avatar at logical `(3, 8)` and target_basic at `(12, 8)` — only walks relocate the avatar; no other action moves anything. |
| L1 | M2 beam-couple-haul | no | block_basic at `(8, 8)` is TANGIBLE/PIXEL_PERFECT; walking *into* it from any side is rejected by collision, so there's no "push" fallback. The only verb that mobilises a block is the beam coupling. |
| L2 | M1 walk-avatar | no | block_yellow at `(8, 4)` and block_orange at `(8, 8)` need to reach distinct targets across the grid; toggling beam alone moves nothing. |
| L2 | M2 beam-couple-haul | no | Same as L1: blocks are solid; no push fallback; coupling is the only mover. |
| L2 | M3 beam-release | no | Engine invariant in `step()`: at most one block coupled at a time. After delivering block_orange to target_orange at `(3, 8)`, the coupling persists; any subsequent walk to fetch block_yellow drags block_orange off `(3, 8)` (offset preserved), un-winning the orange pairing. Only ACTION5-toggling-off detaches block_orange in place and lets the avatar couple a second block. |
| L3 | M1 walk-avatar | no | Avatar at `(3, 3)`, blocks at `(5, 5)` and `(3, 5)`, targets at `(5, 1)` and `(8, 5)` — all spatially separated. |
| L3 | M2 beam-couple-haul | no | Both blocks solid; no push; coupling is the only mover. |
| L3 | M3 beam-release | no | Only one block couplable at a time; both blocks have distinct targets; after delivering block_C, block_D still needs to be coupled separately, which requires releasing block_C first. |
| L3 | M4 direction-lock | no | block_D (east-direction-locked) sits at `(3, 5)` with target at `(8, 5)`. Its east-haul path passes through `(5, 5)` where block_C sits. block_C cannot be moved by pushing or walking into it (no push fallback). block_C is north-direction-locked: coupling check fails unless the beam direction is north, which happens only when the avatar approaches from the south facing north. No alternate cardinal coupling angle to block_C works (the direction-lock predicate rejects coupling). So the player must (a) approach block_C from south facing north (which is the M4 verb), (b) haul it north out of column-5 row-5, (c) only then can block_D's east-haul path clear. Both M4 actions are unavoidable. |

Verdict: every (mechanic, level) row answers "no" with a concrete grounding. **Checklist item 12 passes** in the strict counterfactual sense.

## Independent alternate-strategy enumeration (per checklist item 12 "verify by enumeration")

**L3 alternates re-walked:**

1. *Greedy "deliver nearest first" → block_D first.* Manhattan distance from avatar `(3, 3)` to block_D `(3, 5)` is 2; to block_C `(5, 5)` is 4. The greedy player approaches block_D from the west (only valid coupling side for east-arrow). They reach `(2, 5)`, beam on, walk east — couples block_D, then ACTION4 walks east: avatar `(3, 5)`, block_D wants `(4, 5)` empty → OK. ACTION4: avatar `(4, 5)`, block_D wants `(5, 5)` = block_C → collision → walk rejected. Player wasted ~6 steps and must now release, detour around block_D, deliver block_C first, return for block_D. Heuristic fails.

2. *Couple block_C from a non-south direction (e.g. north).* Avatar approaches `(5, 4)` facing south. Beam cell `(5, 5)` = block_C, beam direction = south, block_C chevron = north → mismatch → coupling rejected. Avatar can repeat from west or east — same result. Only `(5, 6)` facing north works. M4 forces this.

3. *Try to walk avatar onto block_C from any side to "push" it.* All sides: block_C is TANGIBLE PIXEL_PERFECT → walk into block_C cell is rejected by collision. No push fallback exists.

4. *Try to walk block_D east via a south detour.* block_D is east-direction-locked; any walk while block_D is coupled in a direction other than east is rejected. So south detour is impossible while block_D is coupled. The player can release block_D, push it via avatar... no, no push fallback. So block_D must travel strictly east, through `(5, 5)`.

5. *Couple block_C then disconnect mid-haul, fetch block_D, re-couple block_C from somewhere else.* If the player releases block_C in column 5 (e.g. at `(5, 4)` or `(5, 3)`), it still sits in block_D's east path. block_D's east path is `(3, 5) → (4, 5) → (5, 5) → (6, 5) → (7, 5) → (8, 5)` — it passes through `(5, 5)` only. If block_C is parked at `(5, 4)` or `(5, 3)`, those cells aren't on block_D's path. Player COULD release block_C at `(5, 4)` (one step north of original), then deliver block_D, then come back for block_C. But block_C must end at `(5, 1)`. Delivering block_C to `(5, 4)` doesn't win — block_C must reach `(5, 1)`. Player must complete block_C's delivery eventually. So full delivery requires M4 (north-haul of block_C) at some point.

   Subcase: player parks block_C at `(5, 4)`, delivers block_D to `(8, 5)`, then comes back for block_C. Re-coupling block_C: avatar at `(5, 5)` facing north (north of block_C? no, `(5, 5)` is south of `(5, 4)`)... let me redo. block_C at `(5, 4)` north-locked. To couple: avatar at `(5, 5)` facing north, beam cell `(5, 4)` = block_C, direction match. Couple. Haul north to `(5, 1)` — 3 more north walks. Works. This is just a more verbose path that still uses M4 in two phases. M4 is still triggered.

All enumerated alternates either fail or still trigger every claimed mechanic. **Counterfactual necessity verified by enumeration.**

**L2 alternates re-walked:**

1. *Deliver block_yellow first along the straight south path.* block_yellow at `(8, 4)`, target_yellow at `(8, 12)`. Couple yellow from north (avatar at `(8, 3)` facing south… wait, the avatar at `(8, 3)` facing south has beam cell `(8, 4)` = yellow. But our coupling-side rule for non-directional blocks: ANY side works. So yellow couples from north.) Walk south: avatar `(8, 3)` → `(8, 4)`, yellow `(8, 4)` → `(8, 5)`. Continue south. At avatar `(8, 7)`, walk south rejected — avatar destination `(8, 8)` = block_orange (TANGIBLE) → collision. Player must either (a) release yellow at `(8, 7)`, detour avatar+yellow around column 8 row 8, re-couple, finish; or (b) abandon yellow-first.

   This is a post-discovery wrong path: a fully-informed player who knows beam-couple, knows release, but didn't reason about haul-path collisions would naturally try the straight south path. The failure point — "block-on-block collision rejects the walk" — is a post-discovery insight, not a discovery-stage misstep.

2. *Deliver block_yellow first via east detour.* Couple yellow at `(8, 4)`, walk east. Avatar `(8, 3)` → `(9, 3)` east, yellow `(8, 4)` → `(9, 4)`. Continue east. The detour eventually wraps back to `(8, 12)`. Witness-length: ~3 east + 8 south + 1 west = 12 walks vs. 8-south-direct = 8 walks. Extra cost ~4 walks. Plus the release + re-couple of orange = another phase. Total > witness Plan A. Suboptimal but wins within budget.

3. *Witness — orange-first then yellow.* See spec L2 witness. 29 actions. Orange clears `(8, 8)` so yellow's south straight path is open.

So L2 has at least 3 plausible post-discovery strategies; the witness is the shortest. The fully-informed player needs to reason about block-on-block collision to pick the optimal order.

## Issues found

### Issue #1 (CRITICAL) — Forbidden cultural-convention symbol on `block_directional`

- **Item violated:** checklist item 7 / `forbidden-elements.md` row: *"Cultural conventions / Acquired association / Green-means-go; red-means-danger; **an arrow shape implying direction**."*
- **Spec section + quote:** §3 sprite roster, `block_directional`: *"yellow body with red chevron pointing right (in default rotation = east); rotations 90/180/270 yield south/west/north chevrons"*. The chevron pattern `[[11,11,11,11], [11,8,11,11], [8,8,8,11], [11,11,11,11]]` reads unambiguously as a rightward-pointing arrow head. An arrow shape implying a cardinal direction is exactly the forbidden cultural convention.
- **Suggested fix:** Replace the chevron with an abstract **edge-marker pip**: a small bar of off-palette colour (suggest palette `6` magenta) along the *edge* corresponding to the block's allowed haul direction, with no arrow geometry. For default rotation (east), pixels become e.g. `[[11,11,11,11], [11, 4, 4, 6], [11, 4, 4, 6], [11,11,11,11]]` — a 2-pixel magenta stripe along the east edge mid-rows. Rotations 90/180/270 carry the stripe with them so south-haul has the stripe along the south edge, etc. The stripe is a topological marker (one edge highlighted), not a directional symbol. Mechanic stays the same: beam direction must match the stripe's edge for coupling, walks while coupled must match the stripe's edge.

### Issue #2 (CRITICAL) — L2 "wrong path" is a discovery-stage misstep

- **Item violated:** `difficulty-rules.md` § c stage-conflation guard for L2 — *"Reject if the named 'heuristic that fails' or wrong-path argument is a discovery-stage misstep — something a player only does because they haven't yet understood the mechanic. The post-discovery player knows what each action does; their failures must come from picking the wrong action despite full knowledge."*
- **Spec section + quote:** §4 L2 Difficulty (c) Planning depth: *"A plausible wrong path is attempting to walk through (without ACTION5) the row containing a block — the block is solid, the walk rejects, and the player loses ~2 steps before re-toggling."* "Walking without ACTION5" is a discovery-stage misstep (the player hasn't yet realised they need the beam on to move blocks). The post-discovery player knows ACTION5 is needed.
- **Suggested fix:** Redesign L2 layout so the post-discovery wrong path is *picking the wrong delivery order* — a real planning failure. Concrete redesign:

  - Avatar at logical `(3, 8)`, facing east, beam OFF.
  - `block_orange` at `(8, 8)`, target_orange at `(3, 8)`.
  - `block_yellow` at `(8, 4)`, target_yellow at `(8, 12)`.
  - No barriers, no extra walls beyond the perimeter.

  Witness — orange-first then yellow (29 actions): couple orange at avatar `(7, 8)` facing east, haul west 5 cells to target_orange at `(3, 8)`. Release. Walk north + east to avatar `(8, 5)` facing north, couple yellow at `(8, 4)`, haul south 8 cells. Yellow's straight south path through `(8, 8)` is now clear because orange is no longer there.

  Wrong-but-plausible (post-discovery): "deliver yellow first along straight south path." A fully-informed player who knows release + couple + haul mechanics might still take this path. The avatar approaches yellow from north, couples, walks south. At avatar `(8, 7)` the south walk rejects — the coupled yellow's destination is `(8, 8)` where orange sits. The player wasted ~6 steps and must release yellow, detour avatar+yellow around column 8, re-couple. The post-discovery insight: "haul paths can pass through other blocks; check the path before committing to an order".

  Replace the spec's L2 layout (`block_yellow at (6, 8)`, `block_orange at (6, 12)`) with the order-forced layout above. Update the witness to the 29-action trace, the difficulty (c) bullet to name the order-pick as the wrong path, and the M3 counterfactual to use the new positions.

### Issue #3 (MINOR) — Camera/grid_size inconsistency

- **Item violated:** `universal-scaffold.md` "Camera viewport must match level grid_size" — if `grid_size = (64, 64)`, the default 64×64 camera is OK. The spec sets `grid_size = (64, 64)` and never resizes the camera; this is internally consistent. No fix needed, but the spec should explicitly state in §6 (HUD and state) that the camera is the default 64×64 viewport and `on_set_level` doesn't need to resize.
- **Suggested fix:** add one line to §6: *"Camera viewport stays at default 64×64 because all levels declare grid_size = (64, 64); on_set_level does NOT need to resize the camera."*

### Issue #4 (MINOR) — Avatar sprite face-likeness

- **Item to confirm:** checklist item 7 / `forbidden-elements.md` "real-world clipart / cultural conventions" — particularly faces, eyes.
- **Spec section:** §3, avatar pixel pattern `[[5,10,10,5], [10,10,10,10], [10,10,10,10], [5,14,14,5]]`. Re-reading: row 0 has two black corner pixels with light-blue between; row 3 has two black corner pixels with green between. This reads as a **rectangular frame with two coloured pixels on the bottom edge**; the corners are not clearly grouped as "eyes" (the top corners are at the extreme edges, not centred). The two green pixels in row 3 act as the visible emitter cue.
- **Verdict:** Not face-like enough to flag, but the resemblance could be reduced. **Suggested fix (optional):** change the avatar pattern so the top row has palette-10 centre and a single black middle pip rather than two corner pips: e.g. `[[10, 5, 5,10], [10,10,10,10], [10,10,10,10], [5,14,14,5]]` — two black pips in the *centre* of the top row (visually a "shoulder line", not eyes). Or `[[10,10,10,10], [10, 5,10,10], [10, 5,10,10], [5,14,14,5]]`. **This is optional**; the original pattern doesn't unambiguously read as a face. Author may choose to leave it.

## Other items — all PASS

- **Item 1** palette 0..15 + -1: only listed values, no out-of-range.
- **Item 2** universal scaffold: spec is consistent with the layout (sprites, levels, constants, HUD, class).
- **Item 3** `available_actions ⊂ [1..7]`: spec sets `[1, 2, 3, 4, 5]`. PASS.
- **Item 4** exactly 3 Level entries: L1, L2, L3 each defined. PASS.
- **Item 5** ID `kg7p`: 4 lowercase chars, not in reserved or index. PASS.
- **Item 6** core knowledge priors only: objectness + physics + geometry. PASS.
- **Item 8** ≥ 2 distinct mechanics: L1 already has 2 (M1, M2). PASS.
- **Item 9** L1 tutorial: 2 mechanics, both witness-required, reduced state (one block, one target, open arena), no on-screen text. PASS.
- **Item 10** L2/L3 composition: each level requires every earlier-level mechanic AND its new one(s). PASS (verified in the per-mechanic table above).
- **Item 11** +1-or-+2 per level: L1→L2 = +1 (release), L2→L3 = +1 (direction-lock). PASS.
- **Item 13** mechanic family absent from taxonomy: `beam-tether-haul` not in 25 reference. PASS.
- **Item 14** mechanic family absent from prior-games: not in 75+ entries. PASS.
- **Item 15** distinguishing rules: stated concretely for wa30, ka59, dc22, m0r0, kn58, vt6q, kj82, wb6n, kf42, hk7v, dj5h, wq3m, bz3k. PASS.
- **Item 16** win condition: per-block-on-tag-matching-target predicate, computed at end of every step(). PASS.
- **Item 17** lose condition: `_action_count >= level_budget`. PASS.
- **Item 18** difficulty floor/ceiling, four bullets per level: L1, L2, L3 each list (a) random-resistance (b) human-tractable (c) planning depth (d) step budget. Issue #2 above corrects the planning-depth wording for L2; otherwise PASS.
- **Item 19** no hidden state: coupling status visible via beam_indicator; facing visible via avatar's green emitter row; direction-lock visible via the edge-pip (per Issue #1's fix). PASS once #1 is applied.
- **Item 20** low-resolution: 4×4 sprites with internal pattern (hollow centres, hatch, checker, edge-stripe); satisfies "shape carries meaning, not colour alone". PASS.
- **Item 21** UI teaches: avatar reads as a movable unit (light-blue, sensor pip), block reads as cargo (hollow square), target reads as a slot (concentric ring), wall reads as solid, barrier reads as permeable (checker), beam reads as active emission (ring). After Issue #1's fix, the direction-lock pip reads as "this edge is the active side". The L1 frame is parseable by a first-time viewer. PASS.
- **Item 22** ACTION7 strict-undo or absent: ACTION7 is not in `available_actions`. PASS.

## Novelty re-check (full spec, not just family name)

Re-running positive similarity-check against taxonomy + prior-games on the fleshed-out spec: same near-misses as the pick-time pass (wa30, ka59, dc22, m0r0, kn58, vt6q, kj82, wb6n, kf42, hk7v, dj5h, wq3m, bz3k). Distinguishing rules in §9 of the spec are concrete and grounded in mechanical-verb differences (directional sticky beam vs. adjacency pickup, persistent vs. one-shot, free-walking emitter vs. gantry). Still **NOVEL**.

Re-walking negative-similarity-check seven dimensions against wa30 (closest near-miss): 8 dimensions, overlap on dimensions 2 (verb structure) + 3 (cargo-deliver goal) + 4 (step-budget lose) — all universal or weak. Differs on 1 (cast), 5 (supporting elements), 6 (palette), 7 (pixel grain — chevron/pip pixels are distinctive), 8 (core dynamic — beam-couple vs. adjacency-pickup). Below the 3-substantive-dimensions rejection threshold. Still **NOVEL**.

## Verdict

**REJECT** spec for `write_spec` revision. Issues #1 and #2 are critical (forbidden-elements violation + stage-conflation in planning justification). Issues #3 and #4 are minor; #3 is a one-line addition, #4 is optional.

`write_spec` must:
- Replace the `block_directional` chevron with a non-arrow edge-pip pattern (Issue #1).
- Redesign L2 to use the order-forced layout (block_orange at `(8, 8)` with target at `(3, 8)`; block_yellow at `(8, 4)` with target at `(8, 12)`); update the L2 witness and the L2 planning-depth justification with the new post-discovery wrong path (Issue #2).
- Add the one-line camera-viewport statement in §6 (Issue #3).
- Optionally adjust the avatar pattern (Issue #4) — author's choice.
