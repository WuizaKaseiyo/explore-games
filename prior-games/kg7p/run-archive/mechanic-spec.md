# mechanic-spec — kg7p (beam-tether-haul)

## 1. Title
**Beam-Tether Haul** (working title; not visible in-game).

## 2. Mechanic family
A single avatar walks a chambered arena. The avatar always faces its last-walked direction and projects a 1-cell *tether beam* into the cell directly in front of it. While the beam is on, any **haulable block** sitting in the beam cell **couples** to the avatar (binary state, one block at a time). A coupled block keeps a fixed grid-aligned offset from the avatar across every subsequent walk — the block moves in lockstep with the avatar until the beam toggles off, at which point the block detaches in place. The level wins when every haulable block sits on its colour-matched target square.

Prior categories used:
- **Objectness** — blocks and target squares are persistent entities with positions and identities.
- **Basic physics** — rigid coupling of block to avatar (every cell of avatar motion is mirrored by block motion); barriers block blocks but pass the avatar (asymmetric solid-vs-permeable).
- **Basic geometry & topology** — direction-locked blocks have a cardinal-arrow constraint at L3 that restricts which walk direction allows hauling.

(No use of agentness — there are no autonomous NPCs.)

## 3. Sprite roster

Cell stride is **4 display pixels**. The logical grid is **16×16 cells inside a 64×64 frame**. Every gameplay-relevant sprite is a 4×4 pixel sprite with internal pattern; the four corners of each cell carry distinguishing detail so the rendering does not read as uniform-colour blocks (checklist item 20).

Palette: `3` grey (walls), `4` off-black (block-basic inner + block-directional inner + background letter-box), `5` black (avatar outline), `6` magenta (direction-lock edge-stripe), `7` pink (barriers), `9` blue (target outline + directional-target inner-marker), `10` light-blue (avatar body), `11` yellow (block-basic and block-D body), `12` orange (target-basic fill accent), `14` green (beam emission), `15` purple (HUD bar full). `-1` transparent. Note: palette `8` (red) is reserved and only used on `target_directional` inner marker as the visual pairing cue with `block_directional` (revised — the magenta edge-stripe colour 6 makes the *block-directional* distinguishable from the *block_basic*, and target_directional's red inner marker visually couples to the same family).

| Sprite name | Pixels (4×4) | Palette | Tags | Role / interaction |
|---|---|---|---|---|
| `avatar` | `[[5,10,10,5], [10,10,10,10], [10,10,10,10], [5,14,14,5]]` — light-blue body, black corner pips, two-pixel green "emitter" along bottom edge (= front in default rotation) | 5, 10, 14 | `["player"]` | Player; TANGIBLE; collides with walls and uncoupled blocks. Rotates to face last-walked direction; the green emitter row marks the beam side and re-orients with the sprite rotation. |
| `block_basic` | `[[11,11,11,11], [11,4,4,11], [11,4,4,11], [11,11,11,11]]` — yellow hollow square with off-black inner 2×2 | 4, 11 | `["block"]` | Haulable block; TANGIBLE; collides with walls, barriers, other blocks. Used in L1, L2; counts toward win when over a `target_basic`. |
| `block_directional` | `[[11,11,11,11], [11, 4, 4, 6], [11, 4, 4, 6], [11,11,11,11]]` — yellow hollow square with a 2-pixel magenta edge-stripe along the haul-side edge (east edge in default rotation); rotations 90/180/270 carry the stripe to south/west/north edges. **No arrow geometry** — the stripe is a topological edge-marker (one edge highlighted), not a directional symbol. *(Revised to address critique Issue #1 — `forbidden-elements.md` prohibits arrow shapes implying direction. The edge-stripe is abstract and players discover its meaning through play.)* | 4, 6, 11 | `["block", "directional"]` | Direction-locked haulable block; TANGIBLE; same collision rules as `block_basic`. Used in L3. The block's allowed haul direction is the side bearing the magenta stripe: 0°→east edge, 90°→south edge, 180°→west edge, 270°→north edge. |
| `target_basic` | `[[9,9,9,9], [9,12,12,9], [9,12,12,9], [9,9,9,9]]` — blue outline with orange inner 2×2 | 9, 12 | `["target", "target_basic"]` | Target for `block_basic`; INTANGIBLE (does not block walking; rendered under the avatar/block layer). Win check pairs by exact (x, y) match between any `block_basic` and any `target_basic`. |
| `target_directional` | `[[9,9,9,9], [9,8,8,9], [9,8,8,9], [9,9,9,9]]` — blue outline with red inner 2×2 | 8, 9 | `["target", "target_directional"]` | Target for `block_directional`; INTANGIBLE. Win check pairs by exact (x, y) match. (Note: the target is colour-paired with the chevron colour; the rendered tone says "this slot wants the arrow block".) |
| `wall` | `[[3,3,4,3], [3,3,3,3], [3,4,3,3], [3,3,3,4]]` — solid grey with sparse off-black hatch pixels for texture | 3, 4 | `["wall"]` | Static obstacle; TANGIBLE; PIXEL_PERFECT blocking. Avatar and blocks both rejected when targeting a wall cell. |
| `barrier` | `[[7,0,7,0], [0,7,0,7], [7,0,7,0], [0,7,0,7]]` — pink and white checker (a visibly "permeable" texture) | 0, 7 | `["barrier"]` | INTANGIBLE in the engine sense — the engine does not collide it with anything; our `step()` does the asymmetric check (avatars walk through it; coupled blocks treat it as a wall). Used in L2 and L3. |
| `beam_indicator` | `[[14,14,14,14], [14,-1,-1,14], [14,-1,-1,14], [14,14,14,14]]` — green hollow square; rotates to face beam direction | 14 | `["beam"]` | Visual cue; INTANGIBLE. Spawned by `step()` at the cell in front of the avatar whenever `beam_on=True`; removed when beam toggles off. Always renders at layer 5 (above blocks). |

Avatar/block placement uses a **stride-4 logical grid** — every placement is at `(cell_x * 4, cell_y * 4)`. The 16×16 logical grid spans display pixels 0..63 along each axis, with the HUD overlaying row 63 (the bottom row of pixels).

**Style note on the "no hidden state" rule (checklist item 19):** the visible cues are:
- *Coupling status* — the beam_indicator sprite (green ring) appears whenever the beam is on. When a block becomes coupled, the beam_indicator overlays the block, visually marking it as the active tether.
- *Beam direction* — encoded by the avatar's rotation: the green emitter row of the avatar always faces the beam direction, and the beam_indicator sits one cell beyond that row.
- *Direction-lock arrow* — `block_directional` carries a visible red chevron whose pointing direction is exactly the allowed haul direction. The chevron rotates with the sprite.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. `grid_size = (64, 64)` for every level. Cell stride = 4 px throughout. `level_data` holds the step budget per level.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 2):
  - **M1 (walk-avatar):** ACTION1–4 walks the avatar one cell (4 display pixels) in the pressed direction and rotates the avatar to face that direction. A walk is rejected if the destination is a wall or off-grid.
  - **M2 (beam-couple-haul):** ACTION5 toggles the tether beam on (start of level: beam OFF). While the beam is on, the cell in front of the avatar's current facing is checked at the end of every step; a haulable block in that cell becomes COUPLED with a fixed grid-aligned offset to the avatar. Subsequent walks move the avatar and the coupled block in lockstep; the walk is rejected if any destination is invalid for either.

- **Necessity per mechanic** (counterfactual):
  - *L1 cannot be solved without triggering M1* because the avatar starts at logical cell `(3, 8)` and the only `target_basic` is at `(12, 8)` — no sequence of ACTION5 toggles can change positions, so without a single walk the block stays at `(8, 8)` and the target stays empty.
  - *L1 cannot be solved without triggering M2* because `block_basic` is the only sprite whose placement determines the win predicate, and the only way to move a haulable block onto its target cell is for it to be coupled to the avatar; with the beam off, walking simply leaves the block where it is — and walking *into* the block is rejected because uncoupled blocks are solid (PIXEL_PERFECT TANGIBLE).

- **Witness solution** (9 actions):
  ```
  ACTION5,
  ACTION4, ACTION4, ACTION4, ACTION4,
  ACTION4, ACTION4, ACTION4, ACTION4
  ```
  Trace: After `ACTION5`, beam is on (cell in front = `(4, 8)`, empty). Each `ACTION4` walks east. After the third `ACTION4`, avatar is at `(6, 8)` facing east → beam cell `(7, 8)` empty. After the fourth `ACTION4`, avatar at `(7, 8)`, beam cell `(8, 8)` = block_basic → couple (offset `+4, 0` in display px). Steps 6–9: walks east drag the block from `(8, 8)` through `(9, 8), (10, 8), (11, 8)` to `(12, 8)` over target_basic. Win predicate fires at the end of step 9.

- **Difficulty justification:**
  - **(a) Random-resistance:** a vision-blind random-policy agent draws ACTIONS uniformly from `{1, 2, 3, 4, 5}`. P(stumble onto target within 30 steps) is small — the target is 9 specific actions away in the right order; even with the slack, the block has to be in beam cell *while* beam is on AND the avatar continues east. A small-LLM text agent without spatial reasoning fares similarly poorly because there's no in-frame text to read.
  - **(b) Human-tractable:** an attentive human reads the layout (avatar on left, yellow hollow block in middle, blue-orange target on right), tries an arrow, sees the avatar move, tries ACTION5 (the green emitter pulses on), tries another walk and notices the block "stuck" to them after the beam crosses it. ~60 s for first-time players. Target ~2 minutes including initial-look.
  - **(c) Planning depth:** **L1 has no strict planning requirement.** Discovery is the entire difficulty; once "ACTION5 makes the block stick to my walking" is understood, reaching the target is one straight line east.
  - **(d) Step budget:** **40** (witness is 9; budget is 4.4× over witness — generous slack so an exploring player can try ACTION1, ACTION2, ACTION5-twice, etc., and still finish).

### Level 2 — base system + 1 new mechanic *(Revised per critique Issue #2: layout redesigned to force a delivery order; planning-depth wrong-path is now post-discovery.)*

- **Mechanics required by the witness** (= N+1 = 3):
  - **M1 (walk-avatar)** — carried from L1.
  - **M2 (beam-couple-haul)** — carried from L1.
  - **M3 (beam-release):** ACTION5 also toggles the beam *off* — when toggled off, any currently-coupled block detaches at its current cell and stops moving with the avatar. The avatar can then walk freely and re-couple to a *different* block by turning the beam back on (only one block can be coupled at any time, so the release is necessary to switch).

- **L2 layout:**
  - 16×16 logical grid inside a 64×64 frame (cell stride = 4 px).
  - Avatar at logical `(3, 8)`, facing east, beam OFF.
  - `block_orange` (block_basic, palette accent = orange via the target colour pair) at logical `(8, 8)`. `target_orange` at logical `(3, 8)` (the avatar's start cell — target sprites are INTANGIBLE so they don't block the avatar).
  - `block_yellow` (block_basic, palette accent = yellow) at logical `(8, 4)`. `target_yellow` at logical `(8, 12)`.
  - Wall perimeter at row 0, row 15, col 0, col 15. No barriers, no extra walls. The arena interior is open.

  *Visual coupling rule for the target/block pairing (per checklist item 21 "shared visual cue between correlated roles"):* each block and its target share a *colour accent* in the inner pixel — `block_orange`'s inner 2×2 swap is dimmed-orange (palette 12), `target_orange`'s inner 2×2 is the same orange (palette 12). Likewise yellow uses palette 11 on both. The shared accent reads as "this block belongs in that slot" without any text.

- **Necessity per mechanic** (counterfactual, L2 geometry):
  - *L2 cannot be solved without triggering M1* because both `block_orange` at `(8, 8)` and `block_yellow` at `(8, 4)` are spatially separated from their targets at `(3, 8)` and `(8, 12)` respectively — no chain of ACTION5 toggles relocates them; only walks (with beam on) do.
  - *L2 cannot be solved without triggering M2* because both targets are paired by inner-colour accent (yellow ↔ target_yellow, orange ↔ target_orange); the win predicate requires `block_orange` at exact `(3, 8)` and `block_yellow` at exact `(8, 12)`. Walking without coupling leaves both blocks at their starts and the targets unmatched. Walking *into* an uncoupled block is rejected (collision), so no push fallback.
  - *L2 cannot be solved without triggering M3* because at most one block can be coupled at a time (engine invariant of our `step()`). Whichever block is delivered first remains coupled at its target cell; any walk to fetch the second block would drag the first off its target (coupling preserves offset across walks). Only ACTION5-toggling-off detaches the first block at its target cell and allows the avatar to couple the second block. Even if the player attempts to deliver block_yellow first, the same release necessity applies after yellow arrives at `(8, 12)`; M3 is required regardless of order.

- **Witness solution** (29 actions; orange-first then yellow):
  ```
  Phase A — couple orange and haul west (10 actions):
  ACTION5,                                       # beam on; avatar (3,8) facing east, beam cell (4,8) empty
  ACTION4, ACTION4, ACTION4, ACTION4,            # walk east; avatar (3,8) → (7,8); coupling check at end of step 5 — beam cell (8,8) = block_orange → couple, offset (+1, 0)
  ACTION3, ACTION3, ACTION3, ACTION3, ACTION3    # walk west; avatar (7,8) → (2,8), block_orange (8,8) → (3,8) — on target_orange

  Phase B — release and reposition for yellow approach (11 actions):
  ACTION5,                                       # release; block_orange detaches at (3,8); avatar (2,8) facing west
  ACTION1,                                       # avatar (2,8) → (2,7), face north — detour around still-present block_orange at (3,8)
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,   # east; avatar (2,7) → (8,7)
  ACTION1, ACTION1, ACTION1,                     # north; avatar (8,7) → (8,5) → (8,5)→(8,4)? wait — see trace

  Actually the cleaner Phase B trace:
  ACTION5,                                       # release (step 11)
  ACTION1,                                       # avatar (2,8) → (2,7), face north (step 12)
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,   # avatar (2,7) → (8,7) east (steps 13–18)
  ACTION1, ACTION1,                              # avatar (8,7) → (8,6) → (8,5), face north (steps 19–20)

  Phase C — couple yellow and haul south (9 actions):
  ACTION5,                                       # beam on; avatar (8,5) facing north, beam cell (8,4) = block_yellow → couple, offset (0, -1) (step 21)
  ACTION2,                                       # rotate south; avatar (8,5) → (8,6), block_yellow (8,4) → (8,5) (step 22)
  ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2   # haul south; block_yellow (8,5) → (8,6) → (8,7) → (8,8) → (8,9) → (8,10) → (8,11) → (8,12) — on target_yellow (steps 23–29)
  ```
  At the end of step 29, both blocks are on their respective targets. Win predicate fires.

  Note on step 23-onwards: yellow's south path passes through `(8, 8)`. At step 25, avatar would be at `(8, 8)` and yellow at `(8, 7)`. But block_orange is no longer at `(8, 8)` — it's been delivered to `(3, 8)` in Phase A. So column 8 row 8 is empty and the south haul proceeds without collision.

- **Difficulty justification:**
  - **(a) Random-resistance:** a 29-action ordered sequence with the specific ACTION5 toggle at steps 1, 11, and 21 — random-policy probability of stumbling into this within the 70-step budget is negligible. The block-on-block collision invariant adds another gate: random walks that happen to couple yellow first will encounter a hard rejection partway through, and the random policy has no way to reason about the recovery.
  - **(b) Human-tractable:** a player who cleared L1 reads the two-block layout, naturally couples the *closer* or *first-encountered* block (orange, lying directly east of the avatar) and delivers it. After releasing, they walk to approach yellow and finish. Total L1+L2 around 3–4 minutes for an attentive human.
  - **(c) Planning depth (post-discovery, moderate):** the decision space at L2 start has **at least 4 plausible first actions** for a fully-informed player who already understands walk, beam-couple, and release:
    1. *ACTION5 then east* (witness) — turn beam on, walk east toward block_orange at `(8, 8)`.
    2. *ACTION1 then east-north-east traverse* — walk north first to take an avatar-only path above block_yellow, attempt to approach block_yellow's north side and haul south.
    3. *ACTION5 then north* — walk north toward block_yellow's row.
    4. *ACTION1 (south)/(north) first without ACTION5* — re-position the avatar before turning the beam on.

    **Plausible-but-wrong alternative** (a post-discovery failure, not a discovery-stage misstep): *"Deliver block_yellow first along its straight south path."* A fully-informed player who knows beam-couple + release might still pick yellow-first because yellow is the *more upstream* of the two blocks (its target row is the southmost in the layout). The player walks the avatar to `(8, 3)` facing south, ACTION5 on, couples yellow (beam cell `(8, 4)` = yellow), walks south. At avatar `(8, 7)`, walking south rejects — the coupled yellow's destination `(8, 8)` is `block_orange` (still TANGIBLE because not yet delivered). The walk is rejected by the block-on-block collision invariant. The player has wasted ~6 steps approaching yellow, ~3 hauling, and must now release yellow at `(8, 7)`, detour the avatar around column-8 row-8 (block_orange), and choose between two recoveries: (i) finish yellow via an east detour (adds ~4 steps) and then deliver orange (full orange-cycle ~12 steps), or (ii) abandon yellow temporarily, deliver orange (~12 steps), re-couple yellow at `(8, 7)`, finish south. Either recovery costs strictly more than the witness's orange-first ordering. **Post-discovery insight:** when two blocks' haul paths share cells, the order matters even though both blocks are individually deliverable.

    **Reasoning chain the witness assumes the player walks:** "block_orange sits at `(8, 8)` and block_yellow's straight-south haul path is `(8, 4) → (8, 5) → … → (8, 12)`, which passes through `(8, 8)`. If I deliver block_yellow first, block_orange blocks the south haul at step 6. The fix is either to detour block_yellow east of column 8 (extra steps) or to deliver block_orange first, clearing column 8. block_orange's haul path west is `(8, 8) → … → (3, 8)`, which doesn't conflict with block_yellow's start at `(8, 4)`. So orange-first is the lower-cost path."

    The witness's reasoning cites *concrete positions and intermediate haul-path cells* (post-discovery state), not discovery-stage observations.
  - **(d) Step budget:** **60** (witness is 29; budget is ~2.07× over witness — comfortable margin for one wrong-order attempt (~10 wasted steps including release and recovery setup) plus exploration overhead. Non-shrinking relative to L1's 40 — generous because L2 introduces a new mechanic and the geometry pressure of order-pick adds discovery cost.)

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (= L2-count + 1 = 4):
  - **M1 (walk-avatar)** — carried.
  - **M2 (beam-couple-haul)** — carried.
  - **M3 (beam-release)** — carried.
  - **M4 (direction-lock):** Some haulable blocks are `block_directional` — they carry a visible red chevron whose pointing direction is the **only** cardinal direction in which that block may be coupled and hauled. The coupling check inspects the block's tag and rotation: if the beam direction does not match the block's chevron direction, coupling does not occur (the block stays uncoupled even though it sits in the beam cell). Likewise, every walk while a directional block is coupled is rejected if the walk direction differs from the chevron direction.

- **Necessity per mechanic** (counterfactual, L3 geometry):
  - *L3 cannot be solved without triggering M1* because the avatar starts at `(3, 3)` and must reach two delivery cells `(5, 1)` and `(8, 5)` — neither can be reached without walking.
  - *L3 cannot be solved without triggering M2* because the win predicate requires `block_C` at `(5, 1)` and `block_D` at `(8, 5)`; neither block moves except via coupling.
  - *L3 cannot be solved without triggering M3* because `block_C` and `block_D` are independent and only one block can be coupled at a time; after delivering `block_C`, the avatar must release before approaching `block_D` from `block_D`'s west side.
  - *L3 cannot be solved without triggering M4* because `block_C` is a `block_directional` with a north-pointing chevron and `block_D` is a `block_directional` with an east-pointing chevron. *(a)* Coupling to `block_C` only happens when the avatar approaches it from the south facing north — coupling from any other side does not register, and even if the avatar pushed against the block from another side it would not move (no fallback push-mechanic exists). *(b)* `block_D` blocks the natural path from `(3, 3)` to `block_C`'s approach cell `(5, 6)` because the only un-walled route on the west of `block_C` passes column 5 — and `block_D` sits at `(3, 5)` blocking the avatar's row-5 traverse west; the player must therefore detour around `block_D` *or* deliver `block_D` first. Delivering `block_D` first is impossible without M4: `block_D`'s east-arrow constraint forces the avatar to approach it from the west (cell `(2, 5)`) facing east, and the haul path is `(3, 5) → (8, 5)` which passes through `(5, 5)` where `block_C` currently sits — collision rejects every walk along the haul, so `block_D` cannot reach its target until `block_C` has been cleared. M4 thus forces the ordering "deliver `block_C` first to clear column 5, then deliver `block_D`".

- **Witness solution** (25 actions):
  ```
  Phase A — approach block_C from the south (8 actions):
  ACTION4, ACTION4, ACTION4,             # avatar (3,3)→(6,3)
  ACTION2, ACTION2, ACTION2,             # south: (6,3)→(6,6)
  ACTION3,                                # west: (6,6)→(5,6)
  ACTION5,                                # beam on, facing west — beam cell (4,6) empty, no couple

  Phase B — couple+haul block_C north (4 actions):
  ACTION1,                                # rotate north; beam cell (5,5) = block_C; chevron=north matches → couple → walk: avatar (5,5), block_C (5,4)
  ACTION1, ACTION1, ACTION1,              # haul north; block_C (5,3)→(5,2)→(5,1) — on target_C

  Phase C — release, traverse, approach block_D from west (7 actions):
  ACTION5,                                # release
  ACTION3,                                # west: avatar (5,2)→(4,2)
  ACTION3,                                # west: (4,2)→(3,2)
  ACTION3,                                # west: (3,2)→(2,2)
  ACTION2, ACTION2, ACTION2,              # south: (2,2)→(2,3)→(2,4)→(2,5)

  Phase D — couple+haul block_D east (5 actions):
  ACTION5,                                # beam on; facing south, beam cell (2,6) empty
  ACTION4,                                # rotate east; beam cell (3,5) = block_D; chevron=east matches → couple → walk: avatar (3,5), block_D (4,5)
  ACTION4, ACTION4, ACTION4, ACTION4      # haul east; block_D (5,5)→(6,5)→(7,5)→(8,5) — on target_D
  ```
  Win predicate fires at the end of Phase D.

- **Difficulty justification:**
  - **(a) Random-resistance:** a 25-action ordered sequence with a precise mid-level ACTION5 toggle, a precise approach to each block from its arrow-matching side, and a forced ordering — the random-policy probability of stumbling into this within the 80-step budget is well below 1/10,000 (each direction-lock approach has only one valid cardinal entry; getting both right by chance is `≈ 1/4 × 1/4 = 1/16` per visit, multiplied by the ordering constraint).
  - **(b) Human-tractable:** a player who has cleared L2 reads the L3 layout, sees the chevron arrows on the two blocks, tries to couple `block_D` first (close to start), fails because the haul rejects on column 5 (collision with `block_C`), reasons "I need to move `C` first to clear the path", and finishes inside ~2.5 minutes. Total L1+L2+L3 about 5–6 minutes for an attentive human — under §5's 20-minute cutoff.
  - **(c) Planning depth (post-discovery, challenging):** decision space at L3 start, for a fully-informed player who already understands every mechanic, has **at least 5 plausible first moves**:
    1. *ACTION2 toward block_D's row* — closer block first, the natural greedy choice.
    2. *ACTION4 toward block_C's column* — witness path.
    3. *ACTION1* — explore north before committing.
    4. *ACTION5 immediately* — turn beam on early "just in case".
    5. *ACTION3 west* — search for an alternative path.

    **Trivial heuristic that fails — "deliver the nearest block first"**: Manhattan distance from avatar `(3, 3)` to `block_D (3, 5)` is 2; to `block_C (5, 5)` is 4. A greedy player approaches `block_D` first (walks south, beam on, walks east) — coupling succeeds (avatar at `(2, 5)` facing east, chevron east matches), but the haul rejects at the first eastward step that would move `block_D` to `(5, 5)` where `block_C` sits. The player wastes ~5 actions discovering this; then must release, walk away, deliver `block_C` first (the witness order), and only then deliver `block_D`. The heuristic's failure point — the collision with `block_C` at column 5 — is the post-discovery insight: the *arrival cell* of one block coincides with the *current location* of another, so the order of deliveries matters even when both are individually feasible. **A fully-informed player cannot win L3 by greedy approach without ahead-of-time reasoning about the haul path's intermediate cells.**
  - **(d) Step budget:** **80** (witness is 25; budget is 3.2× over witness — generous slack for one wrong-ordering attempt (~5 extra steps) plus exploration).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]`. No ACTION6 (no click). No ACTION7 (no undo).

| Action | Semantic | Gating |
|---|---|---|
| `ACTION1` | Walk avatar one cell north (decrement y by 4 px); avatar rotates to face north. If a coupled block exists, both avatar and block walk together preserving the coupling offset. Walk rejected if the avatar's destination is a wall or off-grid, OR if the coupled block's destination is a wall, barrier, off-grid, or an *uncoupled* haulable block, OR if the coupled block is `block_directional` and its chevron direction ≠ north. | Always selectable. |
| `ACTION2` | Walk south. Same coupling and rejection rules; direction-lock check is "chevron == south". | Always. |
| `ACTION3` | Walk west. Direction-lock check: chevron == west. | Always. |
| `ACTION4` | Walk east. Direction-lock check: chevron == east. | Always. |
| `ACTION5` | Toggle beam. If beam was OFF → set ON and immediately run the end-of-step coupling check (cell in front of current facing). If beam was ON → set OFF, detach any currently-coupled block in place. | Always. |

End-of-step coupling check (after every walk while beam is ON):
1. Compute the cell `c` one step in the avatar's current facing direction.
2. If `level.get_sprite_at(c, "block")` returns a sprite *S*, AND no block is currently coupled, AND (`"directional" not in S.tags` OR S's chevron direction == current facing direction), set `self.coupled_block = S` with offset `(S.x - avatar.x, S.y - avatar.y)`.

## 6. HUD and per-game state

**HUD (`RenderableUserDisplay`)**

`StepCounterHud` — single instance, draws the depleting step-counter bar on the **bottom row** of the frame (row 63):
- Centred segment of 40 pixels (`(64 - 40) // 2 = 12` left margin).
- Empty pixels rendered as palette `4` (off-black); remaining steps rendered as palette `15` (purple).
- Reads `self.steps_remaining` set each `step()` as `level_budget - self._action_count`.

**Camera viewport** *(addresses critique Issue #3)*

The camera stays at its default 64×64 viewport because every level declares `grid_size = (64, 64)`. `on_set_level` does **not** need to call `self.camera.width = ...` or `self.camera.height = ...`. No scaling occurs; cells are 1 display pixel per logical pixel. The 16×16 logical grid is encoded at stride 4 *within* the 64×64 frame by sprite placement (every sprite is positioned at multiples of 4).

**Per-game internal state** (set in `on_set_level`, updated in `step`)

| Field | Type | Purpose |
|---|---|---|
| `self.avatar` | `Sprite` reference | The single avatar sprite for this level. |
| `self.beam_on` | `bool` | Beam state. Initialized `False` each level. |
| `self.coupled_block` | `Sprite | None` | The currently coupled haulable block, or `None`. |
| `self.coupled_offset` | `tuple[int, int]` | Pixel offset `(dx, dy)` of the coupled block relative to the avatar; set when coupling occurs, used to keep the block lockstep. |
| `self._step_counter_ui` | `StepCounterHud` | HUD widget. |
| `self.level_budget` | `int` | Per-level step budget loaded from `level.get_data("step_budget")`. |

Hidden-state cues (per checklist item 19):
- *Beam ON* → a `beam_indicator` sprite is spawned at the cell in front of the avatar each tick when beam is on; removed when beam is off. The green ring is unambiguously visible.
- *Coupled block* → the beam_indicator visually overlays the coupled block (since the block is at the cell the indicator sits on). The block also has its layer raised to 4 while coupled so it renders above any target.
- *Facing direction* → the avatar's pixel pattern places a 2-pixel green "emitter" row along the front edge, which always points at the beam direction. The pip rotates with the avatar's `.rotation` so the player can read facing off the rendered sprite alone.

## 7. Win condition

For every sprite with tag `block`:
- If sprite's tag includes `directional`, look up the matching `target_directional` at the same `(x, y)` (or alternatively, match by additional sub-tag like `block_C` / `target_C` if needed for tie-breaking).
- Otherwise, look up any `target_basic` at the same `(x, y)`.

If every `block` sits on a tag-matching `target` at exactly the same `(x, y)` (in display pixel coords, snapped to multiples of 4), call `self.next_level()`.

Predicate is checked at the end of every `step()` after movement resolution and end-of-step coupling check.

## 8. Lose condition

`self._action_count >= self.level_budget` at the start of `step()` → call `self.lose()` and `self.complete_action()`; return without further processing.

No collision-instant-fail. No hazard.

(Per `difficulty-rules.md` § 1's "soft-locking" guard: the levels are designed so that **no irreversible action** can take place — coupling can always be undone via release, and there is no resource that gets consumed permanently. The player can always recover and try a different path within the step budget. No "no-win waiting room" can be entered.)

## 9. Novelty note

### Taxonomy (25 reference games)

- **`wa30` — carry-pickup-drop.** Closest in *core verb shape* (avatar walks + ACTION5 verb + delivers cargo to targets). Distinguishing rule: `wa30`'s ACTION5 is an *adjacency pickup-or-drop* — the avatar must be one cell away and the verb is a one-shot inventory transfer. `kg7p`'s ACTION5 is a *beam state toggle* — the coupling is a persistent property of the (avatar, block) pair maintained across many walks, and the beam direction is *the avatar's facing*, not raw adjacency. The two yield very different play: in `wa30` the player thinks "stand next to passenger, press"; in `kg7p` the player thinks "face the block, turn beam on, then walk in any direction with the block in tow".
- **`ka59` — sokoban-explode-chase.** Both push/pull blocks onto targets. Distinguishing rule: `ka59`'s primary verb is **directional slide-three-with-recursive-push** plus detonations and enemy chasers; `kg7p` has none of those — no slide-multi, no detonation, no autonomous agents. `kg7p` moves blocks **one cell per avatar walk** rigidly coupled to the avatar's position.
- **`dc22` — remote-arm-pickplace.** Both move objects across distance. Distinguishing rule: `dc22` uses **ACTION6 click on a remote arm that animates a sprite into a target slot**; `kg7p` has no click and no remote arm — every cell of motion is the avatar's own walk.
- **`m0r0` — mirrored-quad-control.** Both move multiple entities with one input. Distinguishing rule: `m0r0` has **four avatars all moving on every input with sign-flipped axes**; `kg7p` has **one avatar and at most one coupled block moving together with the same vector**, not mirrored.

### Prior generated games (`prior-games/index.md`, 75+ entries)

- **`kn58` — anchor-pull-magnet.** Distinguishing rule: `kn58`'s anchor is **clicked anywhere**, every coloured pawn slides one cell along its dominant Manhattan axis toward the anchor — a *global one-shot snap*. `kg7p`'s tether is **local, directional, persistent** — only the single block in beam-cell couples, and "movement" is the avatar's own walk, not a slide-snap.
- **`vt6q` — grapple-anchor-yank.** Distinguishing rule: `vt6q`'s grapple is **one-shot** — fires, yanks once, ends. `kg7p`'s beam is **persistent** across actions until ACTION5 toggles it off.
- **`kj82` — plank-pivot-walk.** Distinguishing rule: in `kj82` the planks are **floor the pawn walks on**, and the verb is *pivot the plank around an anchor*. In `kg7p` the blocks are **cargo the avatar hauls**, and the avatar never walks on a block.
- **`wb6n` — tether-pin-wrap.** Distinguishing rule: `wb6n`'s tether is **a fixed-length leash to a stake**, with reach extended by planting pins. `kg7p`'s coupling is **absolute** — the block moves 1-for-1 with the avatar across arbitrary distance, no slack, no leash.
- **`kf42` — tether-pawn-cycle.** Distinguishing rule: `kf42` couples **two player-controlled pawns**; `kg7p` couples **one avatar + at most one non-player block** (the block is cargo, not a pawn).
- **`hk7v` — overhead-trolley-hook.** Distinguishing rule: `hk7v` uses a **fixed overhead gantry trolley + variable rope** — the hook hangs strictly vertically from a horizontal rail. `kg7p`'s beam can point in any of four cardinals and is **emitted from the avatar's own current position**, not from an overhead rail.
- **`dj5h` — pulley-pair-platform.** Distinguishing rule: `dj5h` couples **two paired platforms via pulleys**; `kg7p` couples an avatar and a block.
- **`wq3m` — current-drift-route.** Distinguishing rule: `wq3m`'s drifters ride **per-cell stamped flow fields** that move them autonomously; `kg7p` has no per-cell flows, and blocks move only when coupled to the avatar's walk.
- **`bz3k` — drift-impulse-cardinal.** Distinguishing rule: `bz3k` has **persistent integer cardinal velocity** for a single avatar — the avatar drifts continuously between inputs. `kg7p` has no velocity state — the avatar moves exactly one cell per input.

### Negative similarity (revisited at spec-time)

Re-walking the seven negative-similarity dimensions against `wa30` (the strongest near-miss) with the fleshed-out spec:

1. **What's on the board.** `wa30`: avatar + passengers + destinations + forbidden cells + secondary mobile sprites. `kg7p`: avatar + ≤2 cargo blocks + targets + walls + (L2/L3) barriers + (L3) direction-lock arrows. **Differs on supporting cast** — no patrolling/secondary mobile NPCs in `kg7p`, and the L3 chevron + barrier introduce visual elements that `wa30` lacks entirely.
2. **What the player physically does.** `wa30`: walk + adjacency-press ACTION5. `kg7p`: walk + beam-toggle ACTION5. **Shared verb-letter, different verb-semantic** — the beam introduces a *facing-direction-dependent* state the player must track, unlike `wa30`'s direction-independent pickup.
3. **Goal.** Both: cargo on target. Universal idiom.
4. **Lose.** Both: step budget. Universal.
5. **Cast.** `wa30`: passengers (animate-looking, with destination affordance painted on); `kg7p`: hollow yellow squares with arrow chevrons in L3 — visually mineral / mechanical, not animate. **Different.**
6. **Visible visual signature.** `wa30` palette: lavender + pale teal + grey-blue. `kg7p` palette: light-blue avatar with magenta-red emitter accents, yellow blocks with red arrow chevrons, blue+orange target rings, grey walls with hatch texture, pink-checker barriers. **Different dominant palette.**
7. **Pixel grain of primary sprites.** Both use mid-size sprites with internal pattern. `kg7p` packs the chevron, the hollow-block centre, the beam-emitter row, and the wall-hatch into each 4×4 sprite — checklist item 20 satisfied. **Comparable richness; not identical.**
8. **Core dynamic.** `wa30`: "stand next to it, press, then move to destination, press". `kg7p`: "**face** it, **turn on the beam**, **walk**: the block rides alongside until **I turn the beam off**". Different moment-to-moment cognition.

**Verdict (re-confirmed): NOVEL.** Overlap on dimensions 2 (verb-letter), 3 (goal), 4 (lose) — all universal or weak. Differs on 1, 5, 6, 7, 8 — including the load-bearing core-dynamic dimension. Well under the 3-substantive-dimensions rejection threshold.
