# Study notes — what an NovaPlay game *is*

Synthesised from (1) the 25 reference-game evidence layer (deep
analyses + level_1/2/3.png screenshots), (2) three full source
reads — `cn04` (681 LOC, click+arrow+ACTION5 modal),
`tu93` (1251 LOC, pure cardinal arrows), `r11l` (1822 LOC, pure
click) — and (3) the §3.4 design rules under
`skills/conventions/` and `skills/design-constraints/`.

---

## 1. Cross-cut frequency observations (X/25)

| Dimension | Count | Notes |
|---|---|---|
| Step-counter HUD bar present | 25/25 | Universal. Always a depleting bar; hits 0 → `self.lose()`. Position: bottom row dominant; some games top row, single column at edge, or center swatch. |
| Action consumes ≥1 step | 25/25 | Misclicks may or may not consume; `qz73` (prior) and `r11l`-style click-modal games tend not to consume on no-op. |
| ACTION6 (click) listed | ~22/25 | Click-to-select-then-act is the spine of the modal pattern. |
| ACTION5 used as a distinctive verb | ~13/25 | Where a game's identity gets stamped. Pure click / pure-arrow games skip it. |
| ACTION7 (undo) listed | ~4/25 | Rare; `bp35`, `lf52`, `bp35`, `sb26` (sometimes). Generated games should not assume undo. |
| ACTION1–4 cardinal arrows listed | ~18/25 | Most games use them for motion or for cycling. |
| Tag-based sprite querying (`get_sprites_by_tag`) | ~21/25 | Universal idiom; tags are semantic role names like `sys_click`, `goal`, `enemy`, `target`, `player`. |
| Per-instance recolour via `clone().color_remap()` | ~14/25 | One sprite definition per role; per-instance colour variation lives in `set_position` chain. cn04, qz73 (prior) both use this. |
| Per-level data dict (`level.get_data(...)`) | ~17/25 | Used to parameterise step budget, tether length, level-specific goals, target patterns, etc. |
| Level data drives win condition | ~32% | Win predicate often reads a target-pattern array out of level data. |
| Win = cover-all-coloured-targets | ~9/25 | "Place pawn / drop / drag onto matching-colour tile". Most common single shape. |
| Win = match a target image / pattern | ~8/25 | Canvas painting (`ft09`, `cd82`, `re86`, `tn36`). |
| Win = align-to-config (rings / glyphs / nubs) | ~4/25 | `cn04`, `qz73` (prior), `s5i5`, `r11l`. |
| Hazard / chaser / decay | ~3/25 | `g50t` advancing edge, `wa30` drone, `su15` enemies. Most games have step-counter as the only fail mode. |
| Scrolling viewport (camera not whole grid) | ~2/25 | `ft09`, `g50t`. Generated games default to whole-grid 64×64 camera. |
| 1×1 / 2×2 plain rectangle as primary sprite | "many" | The kf42→vh68 cautionary tale flagged this as a near-clone red flag (palette `{4,8,9}` plain blocks). |

## 2. Recurring design moves

- **Step-counter HUD** is a `RenderableUserDisplay` subclass holding `(max_steps, current_steps)` with a `set_current(remaining)` method called at the top of `step()` from `max_steps - self._action_count` (cn04, kf42-prior) — or from a private `steps_used` counter when misclicks should not consume (qz73-prior, sb26).
- **Tag-based sprite role lookup**: `level.get_sprites_by_tag("vhlesexlqd")[0]` (tu93) / `level.get_sprite_at(x, y, tag="cycler")` (kf42-prior). Sprites carry semantic tags at definition time; the game queries by tag, not by name.
- **One sprite definition + per-instance recolour**: `sprites["tip"].clone().color_remap(None, color).set_position(...)` (qz73, cn04). Avoids per-instance sprite duplication.
- **Modal selection via click-then-act**: ACTION6 picks the active object (recorded as `self.active = sprite`); ACTION1–4 / ACTION5 then operate on the active object. Used by cn04, kf42-prior.
- **Two-pass atomic state update**: when N objects must move simultaneously (qz73 rotation, ka59 push), compute proposed positions in pass 1, validate, commit in pass 2. Avoids "A moves into B's old slot while B is also moving" interleaving.
- **Hidden state encodes selection / counter / colour-state**: a small `np.int16` 2×2 or 4×4 matrix captures things like `(active_index, remaining_steps, pawn_colours)` so the engine can graph-hash them.
- **`_get_valid_actions` pre-enumeration**: many games override this to return a small finite set of clicks (qz73 returns ~3–5 ACTION6 candidates; r11l returns 256 ACTION6 candidates on a 4-pixel grid). Makes the click-space tractable for an agent.
- **Level-data-driven configuration**: `Level(... data={"StepCounter": 32, "TargetPattern": [...]})`; per-level mechanic differences live in the data dict, not in level-specific code branches.

## 3. Recurring anti-patterns (to NOT inherit)

- **Sprite library bloat**: defining 40–120+ sprites and using only 3–20 per level. Decide which sprites the game actually needs and stop.
- **Behaviour encoded in name suffixes**: e.g. `"button_3_L"` parsed at runtime as "button for row 3, direction left". Fragile. Prefer level-data dicts or tags.
- **Win predicate that re-renders the entire grid every step**: O(64²) work per action. Maintain incremental state; check only what changed.
- **Plain 1×1/2×2 coloured rectangles on a small empty walled grid**: visually identical to several priors; flagged as the #1 near-clone trap (kf42 → vh68 case in `negative-similarity-check.md`).
- **Hidden mechanics**: a verb that appears in `available_actions` but is never required by the witness solution. §3.4 forbids; checklist item 10a enforces.
- **Unused ACTION5**: listing slot 5 in `available_actions` without a distinctive verb wastes the most expressive slot.

## 4. Open questions for `pick_mechanic`

- **Action-space shape**: what's the smallest subset of `[1,2,3,4,5,6,7]` that supports the chosen verb? Priors `kf42` and `qz73` both rely heavily on click; should this run reach for an arrow-only or ACTION5-as-distinctive-verb shape to diverge on input pattern?
- **Visual signature**: priors use small rectangular pawns on dark walled grids (kf42) and small isolated tip-squares on grey (qz73). What dominant palette + sprite-grain (e.g. larger multi-colour internally-patterned sprites, hatched fields, dense patterns) breaks visual sameness?
- **Core dynamic**: priors are "select-then-move" and "cycle-and-lock". A genuinely different player thinking-pattern would be e.g. *physics simulation* (gravity / falling), *connectivity / topology* (route a path), *agentness* (pursuit / patrol), or *scanline-style commit verb*.
- **HUD orientation**: bottom-row depleting bar is over-represented across the corpus; an edge-column or shrinking-from-both-ends bar would diverge cleanly.

## 5. Per-game one-line essences (25 reference games)

| ID | Essence |
|---|---|
| ar25 | Mirror-line + shape: nudge shape or mirror so ghost-shape covers all dots. |
| bp35 | Token on procedural graph; click teleport, arrows step, undo rewinds. |
| cd82 | Tank orbits canvas, fires dye to splash halves/wedges; match canvas. |
| cn04 | Click glyph to select, arrows slide, ACTION5 rotates 90°; pair the orange nubs. |
| dc22 | Walk pawn onto colour-trigger; cycles all wedges of that colour through alphabet. |
| ft09 | Click cell → 3×3 stamp paints; match large target canvas in viewport. |
| g50t | Walk avatar; world scrolls left every other turn; reach goal before edge. |
| ka59 | Click switches active pawn, arrows slide 3 cells with recursive push; chaser pursues. |
| lf52 | Token on procedural graph + arrows shuffle along track, click teleport, undo. |
| lp85 | Outside-board L/R buttons shift entire row/column of tokens. |
| ls20 | Avatar 5-px hops; cycler-tiles roll shape/hue/rotation; reach matched goal pad. |
| m0r0 | Mirror-image pawn pair: UP moves both up, LEFT pulls them apart; merge in goal. |
| r11l | Click footprint, click destination → drag; ring follows centroid; land in target ring. |
| re86 | Arrow-slide hollow frames, ACTION5 cycles which frame is active; overlay target tints. |
| s5i5 | Click coloured-window button → telescoping rod stretches/retracts; tip-dots on targets. |
| sb26 | Click bottom-tray tile, click frame-slot → drop; ACTION5 commits marker walk. |
| sc25 | 3×3 directional pad + arrows: avatar walks scene to reach hidden-goal sprite. |
| sk48 | Two snake-heads: arrows grow/retract or shimmy past anchors; segments colour-match. |
| sp80 | Click shelf, arrow-slide, ACTION5 pours water from spouts onto cups. |
| su15 | Click fruit tokens to scoop; tick the recipe; enemies drift toward last click. |
| tn36 | Click slot-buttons in sequence to compose a motion programme; pawn traces target. |
| tr87 | LEFT/RIGHT slide bracket cursor; UP/DOWN cycle bracketed glyph through alphabet. |
| tu93 | 3-px arrow hops along maze corridor; coloured arrows join procession behind player. |
| vc33 | Click pull-tab → entire row of floor + units slides; units land on house-colour matches. |
| wa30 | Arrow-walk + ACTION5 lock latches crate to player; drag to goal-frame; drone competes. |

## 6. Three full-source reads — anchored API expectations

- **`game_sources/cn04/65d47d14/cn04.py`** (681 LOC, click+arrow+ACTION5 modal). Click selects a glyph (`self.weqid` is the active sprite); arrows translate; ACTION5 rotates 90°. Uses `_get_valid_actions` to suppress arrow/rotate before any selection. Per-step recompute of "shared nub cells across glyph pairs" via `kwcxemeyuq` dict. `on_set_level` chooses background colour from level data.
- **`game_sources/tu93/2b534c15/tu93.py`** (1251 LOC, pure cardinal arrows `[1,2,3,4]`). Uses giant maze-tile sprites (`vhlesexlqd` tag) as the level background — clever way to encode topology in a sprite's pixel array. `step()` is a 3-phase state machine via `self.iuubfszcoi ∈ {0,1,2}`: phase 0 reads action and sets player rotation, phase 1 advances player + followers, phase 2 advances autonomous followers and runs win/lose checks. Followers append rotation history into a per-sprite list (`self.sdiguidlbg`), creating delayed-tail behaviour.
- **`game_sources/r11l/aa269680/r11l.py`** (1822 LOC, pure click `[6]`). `_get_valid_actions` pre-enumerates a 256-entry grid of ACTION6 candidates (every 4-pixel cell). Multi-frame animation via `self.bmtib` flag and `self.tjffy` counter — `step()` short-circuits to `tpjhojnaoa()` while an animation is in flight. Click-then-click pattern (first click selects a footprint, second click sets a destination); ring-sprite snaps to centroid of footprints each frame. Heavy use of obfuscated names + per-instance-pixel mutation to write target patterns onto otherwise-empty target sprites.
