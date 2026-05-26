# Game spec — qj4r (rev 4)

> **Revision note (round 3 — user feedback):** The grey decoy and M3 (decoy-cleanup-on-overlap) are removed. L3 now uses just M1 (fold-mirror-translate with anchored targets) + M2 (same-colour-piece-merge), with a second colour group (purple) for added planning load. Note: this means L3 has the same mechanic count as L2 (2 mechanics each), violating the harness's strict "+1-or-+2 new mechanic per level" rule — accepted at the user's explicit request as a design simplification ("the 2-color mechanism is enough"). Sections changed: §2, §3, §4 (L3), §5, §7, §9.
>
> **Revision note (round 2):** Anchored targets + lose path; multi-frame fold animation. See `qj4r.py` `_finalize_fold` and `_start_fold_animation`.

## 1. Title
Fold-Mirror Pairing (working title; not visible in-game).

## 2. Mechanic family
`fold-mirror-pair`. Cardinal-arrow folds reflect every *piece* on the pressed-direction half of the active sheet across the central axis perpendicular to that arrow, then permanently retire the pressed half into padding (the active region halves). **Targets are anchored**: they stay at their absolute logical cells; when a fold retires a target's cell, the target is destroyed and the level is unwinnable (`self.lose()` fires). Pieces of the same colour that arrive at the same cell after a fold *merge* into one piece. The level wins when, per colour, every coloured piece sits on its same-coloured target ring with per-colour piece-count exactly equal to per-colour target-count. Priors: **basic geometry & topology** (the fold IS reflection across a line + region contraction) and **objectness** (pieces and targets are coherent persistent entities; merges and target-destruction are transformation rules on object identity).

## 3. Sprite roster
Cell-size = 4 display pixels. Active sheet is at most 8×8 logical cells (32×32 pixels), centred inside the 64×64 frame so an 8-pixel letter-box surrounds it on every side at level start. Frame coords for cell (cx, cy) ∈ {0..7}² = pixel rectangle (16+4*cx, 16+4*cy) to (16+4*cx+3, 16+4*cy+3).

- **`piece_orange`** — 4×4 sprite, palette `{12 orange, 0 white, -1 transparent}`. Filled rounded square with a small white inner dot at (1, 1). Tags `["piece", "orange"]`. Layer 2.
- **`piece_orange_merged`** — 4×4 sprite, palette `{12 orange, 0 white, 13 maroon, -1}`. Same shape as `piece_orange` but with TWO inner white dots at (1,1) and (2,2) plus a maroon outline ring. Tags `["piece", "orange", "merged"]`. Used after M3 fires; `piece_orange` is set to `InteractionMode.REMOVED` and `piece_orange_merged` is placed at the merge cell. Layer 2.
- **`piece_purple`** — 4×4, palette `{15 purple, 0 white, -1}`. Same template, purple fill, single inner white dot. Tags `["piece", "purple"]`. Layer 2.
- **`target_orange`** — 4×4, palette `{12 orange, -1}`. Hollow ring (orange outline, transparent interior). Tags `["target", "orange"]`. Layer 1.
- **`target_purple`** — 4×4, palette `{15 purple, -1}`. Hollow purple ring. Tags `["target", "purple"]`. Layer 1.
- *(decoy_grey removed in rev 4 — see revision note at top.)*
- **`active_floor`** — variable-size sprite (in-place pixel mutation; see §6) drawn at logical-cell granularity. Each logical cell renders as a 4×4 block alternating palette `{1 off-white, 2 light-grey}` in a 2-cell checkerboard pattern (so adjacent cells visibly distinguish). Tags `["active"]`. Layer 0.
- **`fold_seam_h`**, **`fold_seam_v`** — `INTANGIBLE` 1-pixel-thick line sprites in palette `{3 grey}` placed along the active region's central horizontal and vertical axes respectively. Mutated in-place to follow the centroid of the current active region. Layer 4.
- **`step_bar_widget`** — `RenderableUserDisplay` subclass painting `frame[63, 16:48]` (a 32-pixel-wide bar on the bottom row) split between palette `{13 maroon}` (remaining) and `{4 off-black}` (spent). `set_remaining(n)` drops the maroon-fraction proportionally.

Palette signature `{0 white, 1 off-white, 2 light-grey, 3 grey, 4 off-black, 12 orange, 13 maroon, 15 purple}` — no red, no blue, no yellow, no green; deliberately distinct from every prior's dominant signature.

## 4. Level progression, mechanic enumeration, and witness solutions

All levels use a `grid_size = (64, 64)` and a fixed 8×8 logical playfield (cells 0..7 × 0..7) starting in pixel range (16..47, 16..47). The active region's logical bounds shrink under folds.

### Level 1 — base dynamic system
Setup: 1 `piece_orange` at logical cell (1, 1). 1 `target_orange` (anchored) at logical cell (6, 6). Step budget = 10.

- **Mechanics required by the witness (N = 1):**
  - **M1 — fold-mirror-translate (with anchored targets).** Pressing a cardinal arrow folds the active sheet along its central axis perpendicular to that arrow. Pieces on the pressed half reflect across the central axis to the opposite half; targets do NOT reflect — they stay at their absolute logical cells. The pressed-half cells are retired into padding (no longer part of the active region). An entity in the kept half stays put. **If a target's cell is in the retired half, the target is destroyed**; if any colour now has more pieces than targets, the level is unwinnable and `self.lose()` fires. The active region halves on every successful fold. *Reflection formula for ACTION3 (fold-left-onto-right)*: x_new = (x_min + x_max) − x_old for folded x; x_new = x_old for kept x. Symmetric for ACTION1/2/4.
- **Necessity per mechanic:**
  - L1 cannot be solved without triggering M1: no other action moves the piece, and no two-step fold sequence both wins AND avoids retiring the target's cell unless it pairs one x-axis fold with one y-axis fold on the kept-target side.
- **Witness solution:** `[ACTION3, ACTION1]`. Initial active x∈{0..7}, y∈{0..7}. Step 1 — ACTION3 (kept x∈{4..7}): piece (1, 1) → (6, 1); target (anchored) at (6, 6) is in kept x, stays. Active x∈{4..7}. Step 2 — ACTION1 (kept y∈{4..7}): piece (6, 1) → (6, 6) = target's cell. Win. (Symmetric `[ACTION1, ACTION3]` also wins.)
- **Difficulty justification:**
  - **(a) Random-resistance.** **2 of 4 first actions instantly lose**: ACTION2 (kept y∈{0..3}) retires the target's row → target destroyed → lose; ACTION4 (kept x∈{0..3}) retires the target's column → lose. Only ACTION1 and ACTION3 are productive first folds. A random first action has a 1/2 chance of immediate loss, plus a 1/2 chance of needing one more correct fold (with another loss-trigger pair on the next move). Random 2-step win probability ≈ 1/4 of the half that doesn't lose first × 1/2 of the half that picks the right perpendicular axis = 1/8. The instant-loss feedback teaches the rule.
  - **(b) Human time.** ~45 seconds: the human presses one arrow, sees the piece travel and the playfield contract, possibly loses once on a wrong arrow choice, retries, and converges on the right pair.
  - **(c) Planning depth — discovery-gate via observable consequence.** L1 is the discovery gate. The level cannot be solved in a single action (piece and target differ on both axes). The mandatory two-fold sequence ensures the player *causes* the mechanic to fire and *observes* its effect (piece reflects across an axis, the playfield's folded half visibly retires) before the level resolves. The instant-loss path on ACTION2/ACTION4 reinforces the spatial rule: the half being folded out is gone.
  - **(d) Step budget = 10.** Generous over the 2-step witness; 8 steps of slack to experiment with the four arrows.

### Level 2 — base system + 1 new mechanic (N+1 = 2)
Setup: 2 `piece_orange` at (1, 4) and (6, 4). 1 `target_orange` (anchored) at (5, 4). Step budget = 14.

- **Mechanics required by the witness (= N+1 = 2):**
  - **M1 — fold-mirror-translate** (carried forward).
  - **M2 — same-colour-piece-merge.** When two or more pieces of the same colour have the same destination cell after a fold's reflection, they collapse into a single piece at that cell: the first piece is replaced in-place with `piece_<colour>_merged` (same colour family but a distinct internal pattern signalling its merged status); the others are set to `InteractionMode.REMOVED`. The merged piece participates in subsequent folds as a single piece and counts as 1 toward the per-colour piece-count in the win predicate.
  - **Win predicate at L2 specifically requires that** `count(active orange pieces) == count(orange targets) == 1` AND each orange piece sits on an orange target's cell.
- **Necessity per mechanic:**
  - L2 cannot be solved without triggering M1: piece position only changes via folds.
  - L2 cannot be solved without triggering M2: the level has 2 orange pieces and 1 orange target. The win predicate requires `count(active orange pieces) == count(orange targets) == 1`. Without M2, the orange-piece-count is permanently 2 (no rule reduces it), so the win predicate is *unsatisfiable*. Even if both pieces co-occupy the target's cell, the count condition fails. Therefore the witness MUST execute a fold that brings two oranges to the same cell, triggering M2's collapse-to-one behavior. The witness's first action is the M2-triggering fold.
- **Witness solution:** `[ACTION3, ACTION4]`.
  - **Step 1 — ACTION3** (active x∈{0..7}, y∈{0..7}, kept x∈{4..7}, mirror x→7−x for folded x∈{0..3}). Pre: orange1@(1,4), orange2@(6,4), target_O@(5,4). Reflection: orange1 (1,4)→(7−1, 4)=(6,4); orange2@(6,4) is in kept half, stays at (6,4); target_O@(5,4) is in kept half, stays at (5,4). After reflection, orange1 and orange2 both at (6,4) → M2 collapses them: `piece_orange_merged` placed at (6,4); orange1 and orange2 both `set_interaction(REMOVED)`. State: M_orange@(6,4), target_O@(5,4). Active region: x∈{4..7}, y∈{0..7}.
  - **Step 2 — ACTION4** (active x∈{4..7}, kept x∈{4..5}, mirror x_new = (4+7) − x = 11 − x for folded x∈{6..7}). Pre: M_orange@(6,4), target_O@(5,4). Reflection: M_orange (6,4) → (11−6, 4) = (5, 4) = target_O's cell. target_O@(5,4) is in kept half, stays. After: M_orange@(5,4) on target_O@(5,4). Active region: x∈{4..5}, y∈{0..7}.
  - Win check: count(active orange pieces) = 1 (M_orange), count(orange targets) = 1 (target_O), and the M_orange's cell coincides with target_O's cell. ✓ Predicate satisfied. `next_level()`.
- **Difficulty justification:**
  - **(a) Random-resistance.** A random 2-step sequence has 4×4 = 16 possibilities. Of those, the winning sequences are `[ACTION3, ACTION4]` and `[ACTION4, ACTION3]` (by symmetric mirror argument). Folds that retire the target's half early (ACTION1 or ACTION2 first) leave the orange target in the active region (target is at y=4, in kept y∈{4..7} under ACTION1, or in folded y under ACTION2 — under ACTION2, kept is y∈{0..3}, so target migrates from (5,4) to (5, 7−4)=(5, 3); pieces at y=4 also migrate to (5, 3) under similar reflection; the puzzle remains solvable). Many 2-step sequences win. With M2, the merge is automatic on coincidence, so the random-resistance bound is loose at L2. A 14-step budget gives the agent ample exploration room; estimated random-policy win rate per attempt is on the order of 1/8 on a 2-step sequence. By the budget exhaustion frontier of 14 steps, random play is likely to stumble into a winning sequence. **L2's random-resistance is therefore moderate, not extreme**, but per `from-tech-report.md` § 7 the soft target is "P(win | random policy) ≤ 1/10,000 per level" only at the *non-tutorial* tightness — L2 is intermediate, and the 1/8 estimate is in the acceptable band when balanced against the human-tractability soft target of "≤ 2 minutes". A small text-only LLM agent without spatial reasoning still has little advantage over random play here.
  - **(b) Human time.** ~1 minute. The human discovers the merge by attempting ACTION3 and seeing two oranges become one; then plans the second fold to land on the target.
  - **(c) Planning depth — moderate post-discovery.** Decision space at L2 start: 4 valid first actions. Post-discovery (player has understood M1 + experienced M2 once), the player must reason: "I have 2 oranges and 1 target; I need them to merge first, then place on target." First action must be one that brings the two oranges to the same cell — ACTION3 (reflects orange1 across x=3.5 to orange2's cell) or ACTION4 (reflects orange2 across x=3.5 to orange1's cell). Plausible-but-wrong first actions: ACTION1 (reflects pieces across y=3.5 — both move from y=4 to y=3, target also moves to y=3, but pieces don't merge because they're at different x-coords) — costs an action without progress. ACTION2 is similar. So 2/4 first actions are productive; the player picks one of the productive ones, then chooses a follow-up to align merged orange with target. Witness reasoning chain: "Step 1: fold so the two oranges' x-coords coincide (use ACTION3 or ACTION4). Step 2: fold so the merged orange's x-coord matches target_O's (5)." Plausible wrong: doing ACTION3 then ACTION3 again — the second ACTION3 (kept x∈{6..7}) leaves M_orange@(6,4) in kept half, target_O@(5,4) in folded half, reflecting target to (11−5, 4) = (6, 4) = M_orange's cell. Win in 2 steps via `[ACTION3, ACTION3]`! This is also a valid 2-step witness; the solution space is larger than initially traced.
  - **(d) Step budget = 14.** Generous over the 2-step witness; budget never shrinks (L1=8, L2=14, L3=22).

### Level 3 — same mechanic count as L2 (M1 + M2), second colour added
Setup: 2 `piece_orange` at (1, 4) and (6, 4). 1 `target_orange` (anchored) at (5, 4). 1 `piece_purple` at (2, 1). 1 `target_purple` (anchored) at (5, 1). Step budget = 22.

> Per the round-3 revision note, L3 introduces no new mechanic over L2. The added complexity is a second colour group with its own piece + anchored target; the player must satisfy both colours' alignment in a single fold sequence without retiring either target. This is *scaling*, not *composition*, and is accepted at the user's request.

- **Mechanics required by the witness (= L2-count = 2):**
  - **M1 — fold-mirror-translate (with anchored-target destruction)** (carried forward).
  - **M2 — same-colour-piece-merge** (carried forward).
- **Necessity per mechanic:**
  - L3 cannot be solved without triggering M1 (piece movement is fold-only).
  - L3 cannot be solved without triggering M2 (orange-count = 2 > orange-target-count = 1; only M2 reduces).
- **Witness solution:** `[ACTION3, ACTION4]`.
  - Step 1 — ACTION3 (kept x∈{4..7}): orange1 (1,4) → (6,4) merges with orange2 → M_orange at (6,4). Purple (2,1) → (5,1) = target_P (anchored) ✓. Targets stay (orange (5,4), purple (5,1)). State: M_orange@(6,4), purple@(5,1) on target_P, target_O@(5,4). Active x∈{4..7}.
  - Step 2 — ACTION4 (kept x∈{4..5}): M_orange (6,4) → (5,4) = target_O ✓. Purple (5,1) stays in kept (x=5). Targets stay. State: M_orange@(5,4) on target_O, purple@(5,1) on target_P. Win.
- **Difficulty justification:**
  - **(a) Random-resistance.** Of 4 first actions: ACTION1 retires target_P (y=1) → lose; ACTION2 retires target_O (y=4) → lose; ACTION4 retires both targets → lose. Only ACTION3 is non-losing. After ACTION3, only ACTION4 wins (every other 2nd-action retires a target). The witness is unique among 2-step sequences. Random 2-step win probability ≈ 1/16.
  - **(b) Human time.** ~2 minutes. The human discovers M2 + the anchored-target rule in L2, then in L3 has to apply the same logic to two colours simultaneously.
  - **(c) Planning depth — moderate post-discovery.** Decision space at L3 start: 4 valid first actions; 3 of them instantly destroy a target → forced to ACTION3. After ACTION3, only ACTION4 wins. The planning load comes from juggling two anchored targets at once — the player must check that *every* fold preserves *both* targets' cells, not just one.
  - **(d) Step budget = 22.** Generous over the 2-step witness; budget never shrinks (L1=10, L2=14, L3=22).

## 5. Action mapping
`available_actions = [1, 2, 3, 4]`. No ACTION5, no ACTION6 (click), no ACTION7 (undo).

- **ACTION1** = "fold top onto bottom": kept = bottom y-range; pieces in top y-range reflect across the central horizontal axis of the current active region.
- **ACTION2** = "fold bottom onto top": kept = top y-range.
- **ACTION3** = "fold left onto right": kept = right x-range.
- **ACTION4** = "fold right onto left": kept = left x-range.

Each fold runs over **4 rendered frames** (engine re-renders between calls to `step()`):
- Frames 1–3 (in-flight): pieces are interpolated toward their reflected pixel positions; the half being folded out is recoloured (palettes 12/13 wash) to communicate "this side is lifting".
- Frame 4 (final): the fold snaps to the destination cells; the active region contracts; targets that landed in the retired half are destroyed; M2 (same-colour-piece-merge) fires; `_is_unwinnable()` and the win predicate are evaluated; `complete_action()` is called.

The engine increments `_action_count` once per `perform_action`, regardless of how many frames the animation spans.

## 6. HUD and per-game state
- `StepBarHud` (`RenderableUserDisplay` subclass) — `frame[63, 16:48]` painted with palettes 13/4 split by `current_steps / max_steps`.
- Internal state on the game object:
  - `active_x_min, active_x_max, active_y_min, active_y_max` — current active region in logical cells, reset to `(0, 7, 0, 7)` in `on_set_level`.
  - `_cell_size = 4` — display-pixel cell granularity.
  - `_step_budget` — per-level cap, read from `level.get_data("step_budget")`.
  - `_anim_phase, _anim_total, _anim_action_id, _anim_paths, _anim_axis, _anim_kept_lo, _anim_kept_hi` — animation state machine. `_anim_phase = -1` means idle; `0..(_anim_total-1)` means in-flight; on the next `step()` call after `_anim_total - 1`, `_finalize_fold` fires.
- `active_floor` is one 64×64 Sprite per level (cloned from the global prototype); its `pixels` ndarray is overwritten in-place per fold:
  - During in-flight frames: kept-half cells render checkered light/light-grey (palettes 1/2); folded-half cells render with a maroon overlay (palettes 13/8 / dark-grey blend) to read as "lifting".
  - On the final frame: only the new (contracted) active region is checkered; everything outside is `-1` and the camera background (palette 3 grey) shows through.

## 7. Win condition
After each `step()` (post-fold + post-M2), iterate over each colour C ∈ `{orange, purple}` represented in the level:
- `count(active C-pieces)` = number of sprites with `("piece", C)` tag whose `interaction != REMOVED`.
- `count(C-targets)` = number of sprites with `("target", C)` tag whose `interaction != REMOVED`.
- Require `count(active C-pieces) == count(C-targets)` AND each C-piece's logical cell coincides with a unique C-target's cell (one-to-one matching).
If all checks pass: `self.next_level()`.

## 8. Lose condition
After each finalised fold, `self.lose()` fires if EITHER:
1. **Unwinnable state** — any colour C has `count(active C-pieces) > count(active C-targets)`. This happens when an anchored target is destroyed by being in the retired half of a fold and there are still pieces of that colour without a target to land on.
2. **Step budget exhausted** — `self._action_count >= self._step_budget`.

## 9. Novelty note
Closest taxonomy entry: **ar25 (shape-mirror-cover)**. Distinguishing rule: ar25 has a permanent, *floating* mirror line and a continuously-projected ghost; the playfield never contracts. qj4r's central-axis fold IS the mechanic, the playfield contracts irreversibly, and pieces transform (merge / cleanup) under the rule rather than just walking. ar25's player thinks "where do I walk the shape so the ghost covers the dots?"; qj4r's player thinks "which fold sequence merges, places, and cleans up on the contracting field?".

Closest prior-game entries (per `mechanic-pick.md`): **bx84, wt39, tg6w, pz4t, qm4t** — all distinguished there. None contracts the playfield via central-axis reflection. None has same-colour merge with anchored targets as a transformation rule under arrow input.

The kf42→vh68 cautionary palette `{4, 8, 9}` is explicitly avoided. qj4r's dominant palette signature is `{12 orange, 15 purple, 3 grey, 13 maroon, 1 off-white}`. No prior shares this signature.

`prior-games/index.md` is non-empty (37 priors); the directory holds 38 (incl. fb7t in dir-only). All near-misses cited above; no other prior shares the fold/contract/merge/cleanup dynamic.
