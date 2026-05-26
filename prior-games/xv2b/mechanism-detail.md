# xv2b — vessel-valve-equalize

## Summary
The player faces three vertical water-vessels standing side by side
on a 64×64 playfield, each with a coloured target-line marked on its
right wall. Two verbs are available: ACTION6 toggles the valve, drain,
or pump glyph at the clicked cell, and ACTION5 advances the
hydrostatic simulation by one tick. On each tick, every OPEN valve
between two vessels transfers one cell of water from the higher-level
side to the lower (provided the valve's slit is submerged), every
active pump transfers one cell from its source vessel to its
destination vessel regardless of relative levels, and every drain
consumes one cell from its vessel. The player wins when every
vessel's water-level matches its target. Difficulty scales by adding
mechanics: L1 is just valves, L2 adds an always-on drain that
destroys mass, L3 adds an uphill pump that lifts water past gravity-
capped slits.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Tick the hydrostatic simulation by one global step (snapshot levels → apply queued valve+pump transfers → apply drains) | Always valid |
| ACTION6 | Click at (x, y); toggles the clicked valve OPEN ↔ CLOSED, or the clicked pump ON ↔ OFF; clicks on drains, vessel walls, water, target ticks, and background are no-ops | Always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 — open valves transfer water to equalise adjacent vessels (slit-submerged direction; closed valves transfer nothing) | Discover that ACTION6 toggles valve sprite swap and ACTION5 redistributes water. Witness `[ACTION6@V_AB, ACTION6@V_BC, ACTION5×16]` (18 actions). Starting (24,0,0), target (8,8,8). |
| 2 | M1 carried + M2 — drain destroys one cell per tick from its vessel while level > 0 | Mass-imbalance forces drain reliance: starting mass 36, target mass 28. Witness `[ACTION6@V_BC, ACTION5×8]` (9 actions). Starting (12,24,0) with drain on B, target (12,8,8); the drain consumes B 1/tick while V_BC drains B→C, landing all three on target simultaneously by mass conservation. |
| 3 | M1+M2 carried + M3 — pump transfers source→destination on every tick when ON, regardless of relative levels (uphill-capable) | Three-phase witness: open V_AB to drain A through V_AB and the drain on A; once water settles at (0,8,0), open the pump and tick three times to lift the final 3 cells from B (locked at slit-8) into C. Witness `[ACTION6@V_AB, ACTION5×22, ACTION6@P_BC, ACTION5×3]` (27 actions). Starting (30,0,0), target (0,5,3). |

## Win condition

After every ACTION5 tick, if every vessel's current water-level
exactly equals its target water-level, fire `self.next_level()`.

## Lose condition

`self.lose()` fires when (a) the action counter reaches the per-level
`step_budget` (60 / 70 / 100 for L1/L2/L3 respectively), OR (b)
after a tick, the total water mass across all vessels falls below
the total target mass (no-win-waiting-room guard — the drain has
destroyed too much to ever satisfy targets).

## Internal state

- `water_level: dict[str, int]` — current water column heights for
  vessels A, B, C in 0..30.
- `target_level: dict[str, int]` — per-level target heights.
- `valves: list[dict]` — one entry per valve carrying its left/right
  vessel names, slit height, current `is_open`, and references to
  the swap-pair sprites (`closed_sprite` and `open_sprite`).
- `pumps: list[dict]` — same shape as valves but with `source` /
  `destination` and `is_on`.
- `drains: list[str]` — vessel names with always-on drains.
- `step_budget: int` — per-level action allowance.
- `_step_hud: StepCounterHud` — the bottom-row depleting bar.
- `water_sprites: dict[str, Sprite]` — runtime references to each
  vessel's water-fill sprite (regenerated each tick).

## Notable code patterns

- **Two-sprite swap idiom for stateful togglables.** Both `valve_closed`
  and `valve_open` (and similarly `pump_off` / `pump_on`) are
  pre-placed at the same position; one is set
  `interaction=REMOVED, visible=False` while the other is TANGIBLE.
  Toggling swaps the two via `set_interaction` + `set_visible`. This
  preserves clean click hit-testing (the REMOVED sprite is excluded
  from `get_sprite_at`) and avoids `set_position(-100, -100)` hacks.
- **Snapshot semantics for deterministic per-tick simulation.** Each
  ACTION5 tick reads water levels into a `snap` dict, computes all
  valve and pump transfers as deltas relative to the snapshot,
  applies the deltas, then runs drains. This makes the order of
  multiple simultaneous transfers deterministic and replayable —
  recording playback works.
- **Water-fill sprite re-pixeled each tick.** Instead of multiple
  per-row sprites, each vessel has one `water_fill` sprite whose
  `pixels` array is overwritten in place to reflect the current
  fill height; the topmost filled row is rendered in palette 10
  (light blue) as a meniscus cue, the rest in palette 9 (blue).
- **Step-counter HUD with low-budget warning.** A
  `RenderableUserDisplay` subclass draws a 32-pixel horizontal bar
  on row 63; the fill colour switches from yellow (palette 11) to
  red (palette 8) when `current/max < 0.25`.
- **Early-lose guard against no-win-waiting-room.** After every
  tick, the game checks if total water mass is now below total
  target mass; if so, fires `self.lose()` immediately rather than
  letting the player tick out the budget in an unwinnable state
  (per `difficulty-rules.md` § 1).
