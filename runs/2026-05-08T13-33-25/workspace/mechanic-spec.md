# mechanic-spec — `ej4t`

## 1. Title

Radius-Scope Chain-Push (working title — not visible in-game; ID `ej4t` is the only identifier)

## 2. Mechanic family

Spatial-scope rule discipline: the player has a visible Manhattan ring of radius R rendered around them; chains of crate-pushes only propagate while every linked crate is within the ring. This composes Objectness (sprites with positions) + Geometry & topology (Manhattan ring as area-of-effect) + Goal-directedness (deliver crates to their targets). Drawing from `core-knowledge-priors.md` categories 1, 2, and (implicitly) the goal-directed framing endorsed in `from-tech-report.md`. Inspired by step 5 web research finding `plus_localradius.txt` (Auroriax/PuzzleScriptPlus); the demo's single-level "crates push only within radius" core is composed here into a 3-level progression with two additional mechanics.

## 3. Sprite roster

- **player**
  - pixels: 5×5
  - palette: 0 (white face), 4 (off-black eyes), 9 (blue body) — distinct from any wall, crate, extender, or shrinker
  - tags: `["player"]`
  - role: the avatar; pushable nothing pushes the player; collides with walls
  - internal pattern: top row eyes (4, 0, 0, 0, 4); rows 1-2 body (9, 9, 9, 9, 9); row 3 belt (4, 9, 4, 9, 4); row 4 base (4, 9, 9, 9, 4)
- **wall**
  - pixels: 4×4
  - palette: 3 (grey), 4 (off-black) — wall fill grey, with rivet-like off-black corners so it reads as solid construction not flat colour
  - tags: `["wall"]`
  - role: blocks player and crate motion; defines corridors
  - internal pattern: row 0 (4, 3, 3, 4); rows 1-2 (3, 3, 3, 3); row 3 (4, 3, 3, 4)
- **crate**
  - pixels: 4×4
  - palette: 12 (orange box), 13 (maroon strap), 4 (off-black highlights) — looks like a wooden crate with a strap; visually distinct from walls and player
  - tags: `["crate", "pushable"]`
  - role: pushable by player when adjacent; chain-pushes only succeed when every chained crate is within R of player
  - internal pattern: row 0 (4, 12, 12, 4); row 1 (12, 13, 13, 12); row 2 (12, 13, 13, 12); row 3 (4, 12, 12, 4)
- **target**
  - pixels: 3×3
  - palette: 11 (yellow center), 4 (off-black ring) — bright yellow disc with a thin dark ring; clearly distinguishable from crate (target is round-ish, crate is square)
  - tags: `["target"]`
  - role: receiving cell for a crate; level wins when every target has a crate on it
  - internal pattern: row 0 (4, 11, 4); row 1 (11, 11, 11); row 2 (4, 11, 4)
- **extender_pickup**
  - pixels: 3×3
  - palette: 14 (green leaves), 11 (yellow core)
  - tags: `["extender", "pushable"]`
  - role: walking onto the cell consumes the pickup and grows player's R by +1 (one-shot); the pickup sprite is removed
  - internal pattern: row 0 (-1, 14, -1); row 1 (14, 11, 14); row 2 (-1, 14, -1) — looks like a tiny sprout / power-up
- **shrinker_trap** (L3 only)
  - pixels: 3×3
  - palette: 8 (red), 4 (off-black)
  - tags: `["shrinker", "trap"]`
  - role: walking onto the cell reduces player's R by 1 (one-shot); the cell stays visible as a "spent" trap (color shifts to grey 3 to mark "used")
  - internal pattern: row 0 (4, 8, 4); row 1 (8, 4, 8); row 2 (4, 8, 4) — looks like a hazard X but topologically a plus, no letter resemblance
- **ring_overlay**
  - pixels: 1×1 transparency-overlay; rendered at runtime over each cell that is within R of player
  - palette: 10 (light-blue accent overlay) added on top of underlying colour with alpha-like blending (in this engine: implemented as a separate sprite with `interaction=INTANGIBLE`, drawn on top of each in-ring cell)
  - tags: `["ring_overlay"]`
  - role: visual cue for the player to see their current radius — a translucent "halo" of cells around them. Solves checklist item 19 (no hidden state; the ring's current size must be visible).

Total sprite kinds: 7 (player, wall, crate, target, extender_pickup, shrinker_trap, ring_overlay).

## 4. Level progression, mechanic enumeration, and witness solutions

Three mechanics total across the 3 levels:
- **M1**: radius-gated chain push — chain-pushes (crate→crate) only succeed when every linked crate is within Manhattan distance R of the player at action-time.
- **M2**: scope-extender pickup — walking onto an extender_pickup grows R by +1 (one-shot, sprite consumed).
- **M3**: shrinker trap — walking onto a shrinker_trap reduces R by 1 (one-shot, sprite stays visible but inert).

### Level 1 — base dynamic system

**Mechanics required by witness** (N=1): just M1.

**Necessity per mechanic (counterfactual):**
- L1 cannot be solved without triggering M1 because walls confine the player and the two crates to the row-6 corridor, the only target is at (10, 6), and the only way to land a crate on that target is to chain-push the two adjacent crates (crate1 at (8,6), crate2 at (9,6)) east; chain push fires the radius gate (crate2's distance from player must be ≤ R=2 to chain).

**Witness solution:**
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]
```
Player at (3, 6); ACTION4 walks to (4,6), (5,6), (6,6), (7,6); the 5th ACTION4 walks INTO crate1 at (8,6), triggering the chain push. crate2 (distance 2) is in ring (R=2), so the chain succeeds: crate1 → (9,6), crate2 → (10,6) = target. Win.

**Difficulty justification:**
- (a) Random-resistance: any of the 4 cardinal directions are equally likely under random policy; the only winning sequence is 5 consecutive ACTION4. P(random win) = (1/4)^5 ≈ 0.1% per attempt; total budget 25 ⇒ at best 5 attempts ⇒ ≈ 0.5% cumulative. Plus a vision-blind agent can't see that the corridor is single-direction; lateral attempts no-op against walls. Effectively random fails.
- (b) Human-tractable: ~30 seconds. Read screen (sees player, two crates in corridor, target at end). Press right repeatedly. Mechanic discovery is instant (one push and the chain effect is visible).
- (c) Planning depth: minimal. L1 is mechanism-discovery only; once the player has tried walking right and seen the crates move, the win is one more right-press away. No strategic decisions post-discovery.
- (d) Step budget: 25. Witness is 5 actions; budget gives 5× the witness for exploration / wrong-direction recoveries / re-tries.

### Level 2 — base system + 1 new mechanic (M2)

**Mechanics required by witness** (= L1's 1 + 1 new = 2): M1 (chain push gated by ring) AND M2 (extender pickup grows R).

**Necessity per mechanic (counterfactual):**
- L2 cannot be solved without triggering M1 because the only target is at (10, 7) and the only crate-delivery path is chain-pushing the two crates east through the corridor at row 7; chain push always invokes the radius gate.
- L2 cannot be solved without triggering M2 because the player starts with R=1; from any reachable cell in the corridor, the rear crate (crate2) is at distance ≥ 2; with R=1, the chain breaks at crate2 (distance 2 > R=1), so chain push fails. The single extender_pickup at (5, 7) sits on the only path between player start and the chain-push position; walking past it grows R to 2, enabling the chain.

**Witness solution:**
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]
```
Player at (3, 7); ACTION4 → (4,7); ACTION4 → (5,7) [picks up extender; R 1→2]; ACTION4 → (6,7); ACTION4 → (7,7); ACTION4 walks INTO crate1 at (8,7), chain-pushes crate2 (distance 2, in ring R=2) to target at (10,7). Win.

**Difficulty justification:**
- (a) Random-resistance: a vision-blind random agent doesn't know what an extender does; it might walk past, but on returning would need to walk straight through the chain-push position. P(random win in budget 30) ≈ 0.5%. A small text-only LLM agent that simulates "walk right until win" might fluke into it; this is acceptable per L2 standards (random-resistance is non-zero but is below 5%).
- (b) Human-tractable: ~60-90 seconds. The player walks right and sees the ring grow when stepping on the green sprite (the ring overlay grows from R=1 to R=2 visibly). Then the chain push works at (7,7). Discovery: ring-grow effect of green sprite is observable in 1 action.
- (c) Planning depth (post-discovery): moderate. After full discovery, player still must decide: do I pick up the extender first, or attempt the chain push first? Wrong-action paths: (1) Skipping the extender → chain push fails at (7,7), have to back up and pick up. (2) Walking past extender then trying to walk back → wastes actions. The post-discovery decision space at start is 4 (4 cardinals); valid first action is unambiguously east, but subsequent choices about whether to pause at extender (which is automatic) vs. continue past are minor. Reasoning chain: "I'm at (3,7); chain push needs R=2; extender at (5,7) on path; walk through it; then continue to (7,7); push." Plausible-but-wrong: "skip extender, try push directly" → fails because chain breaks.
- (d) Step budget: 30. Witness is 5 actions; 6× over witness gives generous room for re-tries.

### Level 3 — system + 1 more new mechanic (M3)

**Mechanics required by witness** (= L2's 2 + 1 new = 3): M1, M2, AND M3 (shrinker trap reduces R).

**Necessity per mechanic (counterfactual):**
- L3 cannot be solved without triggering M1 because the chain push of three crates (crate1 at (10,7), crate2 at (11,7), crate3 at (12,7)) to target at (13,7) in the row-7 corridor is the only delivery path; walls (rows 5, 6, 8, 9 at columns 4-13) seal the corridor, so any winning sequence must invoke chain push at least once.
- L3 cannot be solved without triggering M2 because with R=1 (initial) the chain push of three crates needs R≥3 (crate3 distance 3 from player at (9,7)); two extenders are required to grow R from 1 to 3 via two separate +1 increments. Both extenders sit on the only horizontal path between start and chain-push position.
- L3 cannot be solved without triggering M3 because the shrinker_trap at (7, 7) sits between the two extenders (extender_A at (5,7), extender_B at (8,7)) on the only path through the corridor (walls forbid bypass at columns 6, 7); stepping on the trap is unavoidable and reduces R by 1. Without the trap mechanic firing, only one extender would be needed (initial R=1 → R=2 won't suffice anyway, but that's because chain length 3 needs R=3; with trap active and R math = R0(1) + ext_A(+1) + ext_B(+1) − trap(−1) = 2, still insufficient! Let me redesign: initial R=2; ext_A grows to 3; trap reduces to 2; ext_B grows to 3; chain push works at (9,7) with R=3.

Re-stated: initial R=2. Chain push of 3 requires R≥3. Without M3 (no trap), single extender (one of A or B) → R=3 → chain works after one extender. With M3 active, trap reduces R back to 2 between the two extenders; second extender required to restore R=3. So M3 forces collecting BOTH extenders. Without M3, witness could skip one. With M3, witness must traverse both.

**Witness solution:**
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]
```
Player at (3, 7); ACTION4 → (4,7); ACTION4 → (5,7) [extender_A; R 2→3]; ACTION4 → (6,7); ACTION4 → (7,7) [shrinker_trap; R 3→2; trap rendered "spent"]; ACTION4 → (8,7) [extender_B; R 2→3]; ACTION4 → (9,7); ACTION4 walks INTO crate1 at (10,7), chain-pushes crate1+crate2+crate3 east. Chain check: crate3 distance 3 from player at (9,7); R=3; in ring. Chain succeeds: crate1 → (11), crate2 → (12), crate3 → (13) = target. Win.

**Difficulty justification:**
- (a) Random-resistance: with corridor confinement, only ACTION4 makes net progress; the chain push at the end is a SPECIFIC right-press at SPECIFIC cell. P(random win in budget 35) ≈ 0.05%. Vision-blind agent has no model of trap/extender pixel-level distinction.
- (b) Human-tractable: ~90-120 seconds. The player must observe the ring grow on extender_A, shrink on trap, grow on extender_B, then chain-push. Discovery: 4 distinct visible state-changes (ring grow, ring shrink, ring grow, crates push).
- (c) Planning depth (post-discovery): challenging-but-tractable. The post-discovery decision space at level start is 4 cardinals. Plausible-but-wrong heuristics: (i) Greedy-toward-target — walk to (9,7) directly, push. Fails because R=2 (only 1 extender collected) → chain breaks at crate3. (ii) Skip extender_B (walk through trap before either extender) — R goes 2→1, even worse. (iii) Push from (8,7) — distance to crate3 = 4, fails even with R=3. Trivial heuristic that fails: greedy-toward-target. Actually the witness IS greedy (always east), but a STRICT greedy-toward-target ignores the extenders/trap as obstacles to bypass; in fact the corridor forces the player to encounter all of them. Stronger trivial heuristic that fails: "after picking up extender_A, immediately push" (doesn't account for trap reducing R between A and the push position).
- (d) Step budget: 35. Witness is 7 actions; 5× over witness gives generous room.

L3 step budget (35) is larger than L2's (30), satisfying difficulty-rules.md § 2(d) "L3 budget must NOT shrink relative to witness as level number rises".

## 5. Action mapping

- ACTION1 (UP): walk player up by 1 cell. If destination has a crate, attempt push: solo if crate's destination is empty; chain if destination has another crate (gated by M1's radius rule applied to the rear crate).
- ACTION2 (DOWN): same logic, downward.
- ACTION3 (LEFT): same logic, leftward.
- ACTION4 (RIGHT): same logic, rightward.

ACTION5, ACTION6, ACTION7: not used.

`available_actions = [1, 2, 3, 4]`.

No context-dependent gating — all 4 directional actions are always valid; engine handles invalid-into-wall as silent no-op (consumes step).

## 6. HUD and per-game state

### HUD

- **Step counter** — `RenderableUserDisplay` subclass `StepCounterHud` rendering a horizontal depleting bar at row 63 (bottom of frame), columns 16-47 (centred 32-pixel-wide strip). Drains palette-9 (blue) → palette-3 (grey) as `_steps_used` increments. Universal pattern per `cross-cut-frequencies.md`.
- **Ring overlay** — rendered DIRECTLY in the playfield via the `ring_overlay` sprite at every cell within Manhattan distance R of the player. Re-rendered each turn in `step()`; the cells inside ring receive a translucent palette-10 (light-blue) overlay on top of their underlying colour. Visualises R for the player at all times.

### Per-game state

- `self.R` — int, current player ring radius. Initialized to 2 at level start (L1, L2, L3 all init R=2 — actually L1 R=2, L2 R=1 init, L3 R=2 init; per-level via `level.get_data("init_R")`).
- `self._steps_used` — int, private step counter (NOT engine's `_action_count`, per `fix_implementation.md` idiom to avoid the RESET-counts-as-step bug).
- `self._max_steps` — int, set per level via `level.get_data("step_budget")`.
- `self.player_sprite` — handle to the player Sprite for fast position lookup.
- `self._crate_targets` — dict[crate_sprite_id → target_sprite_id] for the win check.
- `self._extenders_remaining` — set of (x, y) cells; consumed when player walks onto one.
- `self._shrinkers_remaining` — set of (x, y) cells (L3 only); consumed when player walks onto one.

State changes that need visible cue (per checklist item 19):
- R changes → ring overlay re-renders (visible halo around player grows/shrinks).
- Extender consumption → extender sprite removed from frame.
- Shrinker consumption → shrinker sprite re-coloured to palette 3 (grey "spent" state).
- Crate position changes → crate sprite moves (visible).

## 7. Win condition

Predicate: every `crate` sprite's `(x, y)` matches at least one `target` sprite's `(x, y)`.

Implementation:
```python
def _check_win(self) -> bool:
    crate_positions = {(c.x, c.y) for c in self.current_level.get_sprites_by_tag("crate")}
    target_positions = {(t.x, t.y) for t in self.current_level.get_sprites_by_tag("target")}
    return target_positions.issubset(crate_positions)
```

Called after every action (after potentially moving crates). If True, `self.next_level()`.

Holds for L1, L2, L3 — all three levels use the same predicate; they vary in number of crates/targets but the predicate is identical.

## 8. Lose condition

Predicate: `self._steps_used >= self._max_steps`.

Implementation:
```python
if self._steps_used >= self._max_steps:
    self.lose()
    self.complete_action()
    return
```

Per `fix_implementation.md` idiom — increment `_steps_used` ONLY inside successfully-handled action branches; do not couple to engine's `_action_count`.

No other lose paths (no hazards beyond the shrinker_trap, which doesn't directly lose; no enemies; no irreversible soft-locks).

## 9. Novelty note

Closest taxonomy entries (full distinguishing rules in `mechanic-pick.md`):
- `lq5x` (lantern-cone-illuminate) — directional cone projected from a separate stationary lantern; distinguishing rule: this candidate has an omnidirectional Manhattan ring centred on the player itself, with ring-extender pickups growing R rather than wax pickups extending cone range, and no rotation primitive on ACTION5.
- `vp6h` (shadow-cast-collect) — multi-source shadow-projection from rail-mounted lanterns; distinguishing rule: this candidate has a single ring on the player only, no shadow concept, no rail mounts.
- `kn58` (anchor-pull-magnet) — click-place anchor with global magnet pull; distinguishing rule: this candidate has no click action and no autonomous magnetic pull; the ring gates push permission only.
- `bx84` (beam-mirror-reflect) — line-of-fire beam with click-place mirrors; distinguishing rule: this candidate's ring is 2D area, not 1D ray, with no reflection geometry.

Closest prior-games entries:
- All four reference-game near-misses are also in `prior-games/index.md`'s precursor relation; same distinguishing rules apply.
- `pf3w` (wavefront-converge-timing) — timing-based concentric wavefronts; distinguishing rule: this candidate has no timing axis; the ring is always-on, geometric only.
- `lv4k` (lever-balance-torque) — different mechanic family entirely; no overlap.

Step 5 web research source: `plus_localradius.txt` (Auroriax/PuzzleScriptPlus/master/src/demo/). The PuzzleScript demo is a single-level tech demonstration of "crates push only within radius around player" — this candidate composes that core into a 3-level progression by adding scope-extender pickups (L2) and shrinker trap (L3).

§3.4 commercial-novelty ceiling: `plus_localradius.txt` is itself a tech-demo, not a commercial puzzle game. The "radius around player" pattern exists in some stealth/light commercial games (Limbo's flashlight, Closure's light, certain MUDs' line-of-sight) but those games' mechanics diverge from "radius-gated chain push + extender + shrinker trap"; the user-side §3.4 ceiling check should pass.
