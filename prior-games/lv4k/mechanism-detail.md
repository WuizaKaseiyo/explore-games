# lv4k — lever-balance-torque

## Summary

A horizontal beam pivots on a fixed fulcrum at the centre of the playfield. The player picks coloured weights from a tray below the beam — small ring-weights (mass 1) and wider double-width frames (mass 2) — and places them onto evenly-spaced slots along the beam by clicking. The beam visually tilts in proportion to the integer torque sum `Σ (mass × arm)` over all placed weights. The level wins when the tray is empty AND the torque is exactly zero. Step counter HUD bar drains 1 per non-RESET action; running out loses. From level 3 onward, a passenger sprite sits on the beam and shifts one slot toward the dipping side whenever the absolute tilt reaches its extreme; pushing the passenger past the beam end (or onto the fulcrum slot) loses the level.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click at display coords `(x, y)`. The intent is decided by what the click hits: tray weight → select / deselect; placed beam slot → lift the placed weight back to its tray origin; empty beam slot (with a tray weight selected) → place the selected weight there. | always |

(`available_actions=[6]`. Pure click. No movement keys, no commit/modal action.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | **M1: place-balance** — every tray weight must be placed and `Σ mass × arm == 0`. | 4 placement slots at arms `{-2, -1, +1, +2}`, fulcrum at arm 0. 2 mass-1 tray weights. The fulcrum slot is non-placeable (no slot at arm 0), so any solution requires one weight on each side. Witness `[ACTION6@(8,47), ACTION6@(16,26), ACTION6@(20,47), ACTION6@(48,26)]` (4 actions: select m1 #1, place at arm -2, select m1 #2, place at arm +2). Step budget 12. |
| 2 | **M2: mass-arm-asymmetry** — torque is `mass × arm`, so a mass-2 weight contributes twice per slot. | 6 placement slots at arms `{-3, -2, -1, +1, +2, +3}`, fulcrum centred. 1 mass-2 + 2 mass-1 in the tray. Solutions force the mass-2 to arms ±2; mass-1s fill {±1, ±3} or {±2, ∓3, ∓1}-permutations to balance. Witness `[ACTION6@(8,47), ACTION6@(16,26), ACTION6@(20,47), ACTION6@(40,26), ACTION6@(36,47), ACTION6@(56,26)]` (6 actions: m2@-2, m1@+1, m1@+3). Step budget 24. |
| 3 | **M3: passenger-as-mobile-mass** — a green passenger of mass 1 sits on the beam at arm +2 from level start, contributing `1 × passenger_arm` to total torque. When `\|tilt_level\| ≥ 2` after a placement, the passenger slides one slot toward the dipping side (animated over 4 frames). Drift is clamped to `±3`, skips the fulcrum slot (arm 0), and is blocked by occupied slots. The passenger's slot is non-placeable while it's there. | Same beam layout as L2 with 3 mass-2 + 1 mass-1 in the tray and a passenger initially at arm +2 (initial torque +2). Verified by exhaustive enumeration that no torque-zero solution exists with the passenger fixed at +2 — the player MUST drift the passenger to a winnable arm. Witness `[ACTION6@(12,47), ACTION6@(8,26), ACTION6@(24,47), ACTION6@(48,26), ACTION6@(36,47), ACTION6@(24,26), ACTION6@(4,47), ACTION6@(56,26)]` (8 actions: m2@-3 drifts passenger +2→+1, m2@+2 fills the now-vacated slot, m2@-1, m1@+3 → torque 0 with passenger at +1). Step budget 36. |

## Win condition

After every step, evaluate: every tray weight is in `placement.values()` AND `Σ (mass × arm) == 0`. If true, call `next_level()`.

## Lose condition

- **Step exhaustion only**: `_action_count >= step_budget` → `lose()`. The passenger never falls off the beam (clamped at ±3, skips fulcrum, blocked by occupied slots), so L3 has no irrecoverable failure state — the player can always lift weights and re-place to recover from a bad position.

## Internal state

- `selected_weight: Sprite | None` — currently-selected tray weight (visually highlighted via `color_remap` to palette 11).
- `placement: dict[int, Sprite]` — arm-index → placed weight sprite.
- `tray_origin: dict[Sprite, tuple[int, int]]` — per weight, its tray return position.
- `passenger_arm: int | None` — current arm of the L3 passenger; `None` for L1/L2.
- `passenger_sprite: Sprite | None` — the passenger sprite reference.
- `beam_segments: dict[int, Sprite]` — arm → beam_segment sprite, for per-tilt repositioning.
- `tray_weights: list[Sprite]` — every weight sprite in the level (placed or in tray).
- `exposed_arms: list[int]` — per-level placeable arm indices.
- `step_budget: int`, `step_hud.remaining: int` — drained by `_action_count` per step.

## Notable code patterns

- **Per-tilt visual update via integer y_offset table**: `_y_offset_for_arm(arm, tilt_level)` uses truncation-toward-zero division `arm * tilt_level // 2` (with sign-preserving truncation) to compute the per-slot vertical offset. Each beam segment's y is recomputed every step from this; placed weights and the passenger sit one weight-height above their slot's beam segment. Reusable as "discrete tilt rendering for any pivot mechanic".
- **Y-tolerant beam-slot click hit-test (`_beam_lane_contains`)**: strict in x (prevents adjacent-slot ambiguity at small offsets), tolerant ±3 cells in y so clicks register even when the beam has tilted up to its extreme. Lets the player click in a "lane" without tracking the moment-by-moment y of the slot. Reusable for any mechanic with vertically-shifting click targets.
- **Mass-encoded sprite tags**: `weight_mass1` and `weight_mass2` tags carry the integer mass; `_compute_torque` reads tags to multiply by mass. Avoids per-instance attribute storage. Reusable for any mechanic where sprite kinds carry numeric properties.
- **Selection cue via reversible `color_remap`**: the selected weight's frame colour is remapped from its base colour to palette 11 (yellow); on deselect/place the remap is inverted. Cleaner than overlay-sprite halos and survives tilt-driven repositioning.
- **State init before super().__init__()**: `NovaBaseGame.__init__` calls `set_level(0)` which calls `on_set_level` which populates per-level state attributes. If those attributes are initialised AFTER `super().__init__()`, the post-super initialisation overwrites the just-populated state with empty defaults. Universal lesson for any subclass whose `on_set_level` builds derived state.
- **Strict counterfactual M3 design**: tray composition `[m2, m2, m2, m1]` was chosen so every torque-zero solution forces at least one m2@±3 placement, contributing ±6 to tilt_raw, guaranteeing M3 fires in every winning sequence. The M3 mechanic cannot be "skipped" by a player who avoids extreme arms. Pattern: when a mechanic depends on the absolute magnitude of a derived quantity (tilt, torque, energy), constrain the puzzle so all winning paths exceed the trigger threshold.
