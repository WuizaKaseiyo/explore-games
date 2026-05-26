# mechanic-spec.md — kn58

## 1. Title
Anchor-Pull Magnet (working title; not visible in-game).

## 2. Mechanic family
`anchor-pull-magnet` — a pure-click mechanic in which the player places a single magnetic anchor sprite anywhere on a small walled grid; after every action, every coloured pawn slides exactly one cell along its dominant Manhattan axis toward the anchor. Priors used: **objectness** (persistent pawns/anchor/targets), **basic geometry & topology** (Manhattan-gradient field + axis-aligned slides + walls + connected paths), **basic physics** (magnetic-attraction analogy: a single deterministic force-vector per pawn per tick).

**Revision note (visit #2):** ACTION5 BURST mechanic dropped from this game (was Issue 1 in `critique-revisions.md` visit #1 — L3 witness did not exercise it and the alternative geometry that would force BURST proved too brittle to verify by hand). `available_actions` is now `[6]` only — pure click. L3 adds only M7 (anti-anchor) for a +1 bump.

## 3. Sprite roster

Coordinate convention: the playfield is 16×16 logical cells; each logical cell = 4×4 frame pixels. All sprite pixel matrices are at frame-pixel scale. A 4×4 sprite occupies one logical cell. The 64×64 frame leaves room for: (a) a 1-cell letter-box on rows 60–63 reserved for the HUD bar, and (b) the 16×16 logical playfield occupying rows 0–59 (= cells 0–14 in logical-y plus the HUD row). To simplify: logical playfield = cells (0..15, 0..14), with cells (0..15, 15) hosting the HUD.

- **wall_block** — 4×4, palette {5} (black). Tag `wall`. Static, collidable, blocks pawn slides. Multiple instances tile to form arena perimeter and interior walls.
- **anchor** — 4×4, palette {4 off-black, 10 light-blue, 0 white}: a 4-pointed diamond-spike with a light-blue cross-arm and a single white centre pixel.
  ```
  [-1,  4, -1,  -1]
  [ 4, 10, 10,  4]
  [ 4, 10,  0, 10]
  [-1,  4, 10,  4]
  ```
  Tag `anchor`. Marks the magnetic source; the player places exactly one at a time. Set `interaction=INTANGIBLE` (pawns can occupy the anchor cell).
- **anti_anchor** — 4×4, palette {4 off-black, 8 red}: a four-corner-dot frame with a dark 2×2 inner block. Pattern (revised per critique Issue 2):
  ```
  [ 8, -1, -1,  8]
  [-1,  4,  4, -1]
  [-1,  4,  4, -1]
  [ 8, -1, -1,  8]
  ```
  The pixel arrangement is 4 corner dots + an inner 2×2 block. There are no diagonal strokes connecting the corners, so the sprite reads as "frame with inset" not as a letter. Tag `anti_anchor`. Static, INTANGIBLE. Used L3 only.
- **pawn_orange** — 4×4, palette {12 orange, 4 off-black}:
  ```
  [12, 12, 12, 12]
  [12,  4, 12, 12]
  [12, 12,  4, 12]
  [12, 12, 12, 12]
  ```
  Tags `pawn`, `orange`. Movable, collidable.
- **pawn_purple** — 4×4, palette {15 purple, 4 off-black}: identical pattern with palette 15 instead of 12. Tags `pawn`, `purple`.
_(pawn_green / target_green removed per critique Issue 1: no level uses them; per `composition-and-tutorial.md` no-hidden-mechanics, sprites that no level uses should not appear in the bank.)_
- **target_orange** — 4×4, palette {12 orange, 0 white}: a hollow ring.
  ```
  [12, 12, 12, 12]
  [12,  0,  0, 12]
  [12,  0,  0, 12]
  [12, 12, 12, 12]
  ```
  Tags `target`, `orange`. INTANGIBLE (pawns can land on it).
- **target_purple** — same pattern, palette 15 outline. Tags `target`, `purple`. INTANGIBLE.

## 4. Level progression, mechanic enumeration, and witness solutions

The mechanic ladder used below (revised; M6 removed):
- **M1: anchor-place-by-click.** ACTION6 click on any cell relocates the single magnetic anchor to that cell's logical-cell origin. Clicking the cell already holding the anchor removes it (no anchor active that tick).
- **M2: pawn-magnet-pull.** Phase 1 of every action: each pawn computes Δ = anchor_pos − pawn_pos. If |Δx| ≥ |Δy| (tiebreak horizontal), pawn attempts to move 1 cell along sign(Δx) on x; else 1 cell along sign(Δy) on y. If primary-axis move is blocked (by wall or another pawn), pawn attempts the secondary axis with that step's remaining sign. If both blocked, pawn stays. Resolution is *simultaneous* across all pawns: collect each pawn's desired destination, drop any whose destination is currently occupied by a non-moving pawn or a duplicate destination, commit the rest. (Two-pass rule per `universal-scaffold.md` § Simultaneous-conflict.) When no anchor is currently placed, Phase 1 is a no-op.
- **M3: colour-match-target-win.** A pawn is "matched" when it occupies a target sprite of the same colour-tag. Win = every `pawn`-tagged sprite is matched. Check fires after every action.
- **M4: pawn-pawn-collision.** Two pawns may not occupy the same cell at the end of an action. During simultaneous resolution, a pawn whose destination cell is occupied by another pawn that is *not* leaving that cell stays put. Two pawns whose destinations coincide both stay put (deterministic standoff).
- **M5: matched-pawn-stick.** Once a pawn is matched (M3 condition true for that pawn), it is removed from the slide-update list — no further M2/M7 effect. Implementation: a per-pawn `stuck=True` flag; subsequent ticks skip stuck pawns in both Phase 1 and Phase 2. The pawn's sprite stays TANGIBLE so it still blocks other pawns via M4. (M3 win-check still runs against all pawns.)
- **M7: anti-anchor-repulsion.** Phase 2 of every action (only when an `anti_anchor` sprite is in the level): each non-stuck pawn checks Manhattan distance to the anti-anchor. If distance ≤ `anti_anchor_range` (a level-data integer), the pawn slides 1 cell along the *away* direction (sign(pawn − anti), dominant axis, same secondary-axis-fallback rule as M2). Resolution is simultaneous and uses the same two-pass conflict rule. M3 match-check runs once more after Phase 2 (a pawn may snap onto target by repulsion).

Phases per action:
1. ACTION6 → Phase 1 (pull). Phase-1.5 M3 match-check; mark stuck. Phase 2 (anti-anchor push, only non-stuck pawns; only if anti-anchor present). Phase-2.5 M3 match-check; mark stuck.
2. ACTION6 click on the current anchor cell → toggle anchor off. Phase 1 has no source so it's a no-op; Phase 2 still runs.

(There is no longer an ACTION5 — it was BURST in the prior draft, removed per critique-revisions.md visit #1 Issue 1.)

### Level 1 — base dynamic system

**Layout.** 16×16 logical grid (`grid_size=(64,64)` with logical 4×4 cells). Walls form the perimeter (logical (0, 0..14), (15, 0..14), (0..15, 0), (0..15, 14)). HUD bar on logical row 15. No interior walls.
- `pawn_orange` at logical (4, 7).
- `target_orange` at logical (11, 7).
- Initial anchor: not placed.
- `level.data`: `step_budget=30`.

**Mechanics required by the witness** (N = 3): M1 (anchor-place-by-click), M2 (pawn-magnet-pull), M3 (colour-match-target-win).

**Necessity per mechanic.**
- M1: without placing an anchor, M2 has no source and the pawn never moves; the level is unsolvable.
- M2: the pawn does not move except via anchor pull (no arrow keys are wired in this game's `available_actions`).
- M3: without a colour-match-target-win predicate, there is no win state.

**Witness solution.**
```
ACTION6 @ (44, 28)   # click logical (11, 7) — anchor placed at target cell
ACTION6 @ (44, 28)   # pawn slides east; (4,7) → (5,7)
ACTION6 @ (44, 28)   # (5,7) → (6,7)
ACTION6 @ (44, 28)   # (6,7) → (7,7)
ACTION6 @ (44, 28)   # (7,7) → (8,7)
ACTION6 @ (44, 28)   # (8,7) → (9,7)
ACTION6 @ (44, 28)   # (9,7) → (10,7)
ACTION6 @ (44, 28)   # (10,7) → (11,7) = target. M3 match → win.
```
8 actions. Step 1 places the anchor and ALSO triggers a Phase-1 pull (consistent with the rule: every ACTION6 runs phases). Pawn at (4,7); Δ to anchor (11,7) = (7,0); horizontal east; → (5,7). Steps 2–8 just keep the anchor in the same place; pawn slides east 1 cell per click. At step 8 pawn lands on (11,7) = target_orange → M3 fires → `next_level()`.

Pixel coordinates: logical (cx, cy) maps to display pixel (cx*4 + 2, cy*4 + 2) (centre of the 4×4 cell). For (11,7) → (46, 30). Either coordinate inside the cell snaps to logical (11,7) via `display_to_grid` + 4-cell snapping.

**Difficulty justification.**
- (a) Random-resistance: vision-blind random-policy clicks anywhere in the 64×64 frame. The pawn slides 1 cell toward whatever cell was clicked. The chance the pawn ends up on (11,7) within 30 actions from random clicks is non-negligible (the gradient field happens to drag the pawn somewhere, and (11,7) is one of 256 cells). This level is intentionally tutorial-level easy: random play *can* sometimes stumble through, which `composition-and-tutorial.md` § L1 explicitly permits. A small-LLM agent without vision still has a low success rate because it must click coherently east of the pawn.
- (b) Human-tractable: ~30 seconds for an attentive human (2–3 clicks to discover that clicks pull the pawn, then 8 deliberate clicks).
- (c) Planning depth: near-zero — mechanic discovery is the difficulty.
- (d) Step budget: 30 (3.75× witness length).

### Level 2 — base system + 2 new mechanics (M4 + M5)

**Layout.** 16×16 logical grid; walls outer frame plus interior walls forming a 1-cell-tall horizontal corridor at logical row 7 (cols 1..14) joined by a single 2-cell side-pocket at logical (7, 8) and (7, 9). Concretely:
- Walls: cells (1..14, 0..6) and (1..14, 10..13) are filled with `wall_block`, EXCEPT (7, 8) and (7, 9) which are open. (Effectively: corridor row 7; pocket at column 7 row 8 and row 9.)
- `pawn_orange` at logical (1, 7).
- `pawn_purple` at logical (14, 7).
- `target_purple` at logical (1, 7) (same cell as orange's start — orange must vacate, then purple lands there).
- `target_orange` at logical (14, 7) (same cell as purple's start — symmetric).
- `level.data`: `step_budget=80`.

**Mechanics required by the witness** (M = N + 2 = 5): M1, M2, M3 (carried forward from L1) + **M4 (pawn-pawn-collision)** and **M5 (matched-pawn-stick)** new this level.

**Necessity per mechanic.**
- M1, M2, M3: same as L1 — anchor placement is the only verb; pulls are the only motion; matches are the only win.
- M4: pawn_orange and pawn_purple must swap ends of the corridor; their direct paths intersect on row 7, so the player MUST detour one pawn into the (7, 8)/(7, 9) pocket while the other passes. Without M4, two pawns could occupy the same cell mid-slide and the swap would resolve in 7 ticks; M4 forces the detour (~14 extra ticks). The witness provably cannot solve L2 in fewer ticks without using the pocket.
- M5: once one pawn lands on its colour-target, subsequent anchor placements would otherwise drag it back off. M5 holds it in place so the player can route the second pawn afterward. Without M5, both pawns would never simultaneously rest on their targets — one would always be in motion under the active anchor.

**Witness solution.** (Coordinates given in logical cells; pixel coords = `cell*4 + 2`.)

Click at logical (7, 8) [the upper pocket cell]:
```
1.  ACTION6 @ logical (7, 8)   # orange (1,7)→(2,7); purple (14,7)→(13,7)
2.  ACTION6 @ logical (7, 8)   # → (3,7); → (12,7)
3.  ACTION6 @ logical (7, 8)   # → (4,7); → (11,7)
4.  ACTION6 @ logical (7, 8)   # → (5,7); → (10,7)
5.  ACTION6 @ logical (7, 8)   # → (6,7); → (9,7)
6.  ACTION6 @ logical (7, 8)   # orange Δ=(1,1) tie horiz east → (7,7); purple Δ=(-2,1) horiz west → (8,7)
7.  ACTION6 @ logical (7, 8)   # orange (7,7) Δ=(0,1) vert south → (7,8) = anchor cell; purple (8,7) Δ=(-1,1) tie horiz west → (7,7)
                                #   simultaneous resolution: orange leaves (7,7), purple enters (7,7) — both succeed.
8.  ACTION6 @ logical (1, 7)   # move anchor to target_purple. orange (7,8) Δ=(-6,-1) horiz west → (6,8)=wall; secondary vert north → (7,7) but purple is there. Stays at (7,8).
                                #   purple (7,7) Δ=(-6,0) horiz west → (6,7)
9.  ACTION6 @ logical (1, 7)   # orange stuck at (7,8). purple (6,7) → (5,7)
10. ACTION6 @ logical (1, 7)   # purple → (4,7)
11. ACTION6 @ logical (1, 7)   # purple → (3,7)
12. ACTION6 @ logical (1, 7)   # purple → (2,7)
13. ACTION6 @ logical (1, 7)   # purple → (1,7) = target_purple. M3 fires on purple, M5 marks purple stuck.
14. ACTION6 @ logical (7, 7)   # move anchor north to (7,7). orange (7,8) Δ=(0,-1) vert north → (7,7).
15. ACTION6 @ logical (14, 7)  # move anchor to target_orange. orange (7,7) Δ=(7,0) horiz east → (8,7)
16. ACTION6 @ logical (14, 7)  # → (9,7)
17. ACTION6 @ logical (14, 7)  # → (10,7)
18. ACTION6 @ logical (14, 7)  # → (11,7)
19. ACTION6 @ logical (14, 7)  # → (12,7)
20. ACTION6 @ logical (14, 7)  # → (13,7)
21. ACTION6 @ logical (14, 7)  # → (14,7) = target_orange. M3 fires; M5 marks orange stuck. Win.
```

21 actions.

**Difficulty justification.**
- (a) Random-resistance: the pawn-collision rule (M4) means most random click sequences deadlock the pawns somewhere in the corridor; among the 256 cells × 21 clicks the chance of a pocket-detour-then-resume sequence at random is ≈ (1 / 256)^N for the precise pocket-pocket-target pattern; effectively zero. A small-LLM agent without spatial reasoning cannot compose the detour.
- (b) Human-tractable: ~2 minutes — discover the pocket route by trial after one or two collisions, then execute the 21-step solution.
- (c) Planning depth: NON-TRIVIAL multi-step planning. Step-by-step reasoning the player must do at each tick: "Where is each pawn going to slide if I click here? Will they collide on the corridor or will one detour into the pocket?" Specifically: the player must reason that clicking at (7, 8) pulls *both* pawns toward the pocket and that the natural Manhattan tiebreak (horizontal-first) plus the pocket geometry will route purple into the pocket *exactly when* orange arrives at (7,7), avoiding head-on collision. A single-step / spam-the-anchor-at-target heuristic *fails*: clicking at target_orange first deadlocks both pawns at (7,7) and (8,7) where they collide head-on with no escape route. Greedy "click the closest target" also fails for the same reason.
- (d) Step budget: 80 (≈ 3.8× witness length).

### Level 3 — system + 1 new mechanic (M7)

**Layout.** 16×16 logical grid; walls outer frame only. No interior walls.
- `pawn_orange` at logical (3, 8).
- `pawn_purple` at logical (8, 8).
- `target_purple` at logical (8, 8) (purple **starts on its target** — pre-stuck via M5 carryover; serves as a stationary blocker via M4).
- `target_orange` at logical (12, 8).
- `anti_anchor` at logical (10, 8). `level.data: anti_anchor_range = 1`.
- `level.data: step_budget = 60`.

Note on pre-stuck: at level start `on_set_level` evaluates M3 once: pawn_purple at (8, 8), target_purple at (8, 8) — colour match — M5 sticks purple. Thereafter purple is INTANGIBLE-to-anchor-pull but TANGIBLE-as-collider (still blocks orange's slides per M4). The "stuck" implementation flag controls only Phase 1 / Phase 2 skipping; the sprite remains a collidable obstacle.

**Mechanics required by the witness** (= L2-count + 1 = 6): M1, M2, M3, M4, M5 (carried forward) + **M7 (anti-anchor-repulsion)** new this level.

**Necessity per mechanic.**
- M1, M2, M3: as L1/L2.
- M4 (collision): pawn_orange's straight-east path on row 8 is blocked by pawn_purple at (8, 8). Without M4, orange would walk through purple straight to (12, 8); with M4, orange must detour south through row 9 around purple. The detour is a 5-action loop that is the bulk of the witness.
- M5 (stick): purple is matched at level start (M5 fires once during `on_set_level`'s post-init match-check) and remains in place as a stationary blocker. Without M5, every anchor pull would tug purple along with orange and their joint motion would be impossible to direct independently — purple would never stay seated on its target.
- M7 (anti-anchor): the anti-anchor at (10, 8) range 1 alters orange's path on row 9: at (10, 9) orange is in range and gets pushed south to (10, 10), forcing the player to navigate via rows 10-11 instead of returning straight to row 8 immediately east of (10, 8). Without M7, orange would simply travel back north at (10, 9) and reach (10, 8) → (11, 8) → (12, 8) in 3 ticks; with M7, that approach is bent off-axis and the witness routes through (11, 10) → (11, 9) → (12, 9) → (12, 8). The anti-anchor's effect at the final approach is also load-bearing: at step 12 (orange at (12, 9), anchor at (12, 8)), anchor pulls orange to (12, 8) directly without entering anti-anchor's range — clean landing.

**Witness solution.** (Cell coords; phases applied per definition. ACTION6-only; no ACTION5.)

```
1.  ACTION6 @ logical (12, 12)  # detour anchor south of orange. orange (3,8) Δ=(9,4) horiz east → (4,8); purple stuck.
2.  ACTION6 @ logical (12, 12)  # orange (4,8) → (5,8)
3.  ACTION6 @ logical (12, 12)  # → (6,8)
4.  ACTION6 @ logical (12, 12)  # → (7,8)
5.  ACTION6 @ logical (12, 12)  # orange (7,8) Δ=(5,4) horiz east → (8,8) blocked by purple (M4); secondary vert south → (7,9). End (7,9). (Phase 2: distance from (7,9) to anti (10,8) = 3+1=4 > 1, no push.)
6.  ACTION6 @ logical (12, 12)  # orange (7,9) Δ=(5,3) horiz east → (8,9). Distance to anti = 2+1=3 > 1. No push.
7.  ACTION6 @ logical (12, 12)  # orange (8,9) Δ=(4,3) horiz east → (9,9). Distance = 1+1=2 > 1. No push.
8.  ACTION6 @ logical (12, 8)   # anchor moves to target_orange. orange (9,9) Δ=(3,-1) horiz east → (10,9). Distance to anti = 0+1=1. In range. Phase 2 push: pawn-anti = (0, 1); axis vert; dy = +1; → (10, 10). End (10, 10).
9.  ACTION6 @ logical (12, 8)   # orange (10,10) Δ=(2,-2) tie horiz east → (11,10). Distance = 1+2=3 > 1. No push.
10. ACTION6 @ logical (12, 8)   # orange (11,10) Δ=(1,-2) vert north → (11,9). Distance = 1+1=2 > 1. No push.
11. ACTION6 @ logical (12, 8)   # orange (11,9) Δ=(1,-1) tie horiz east → (12,9). Distance = 2+1=3 > 1. No push.
12. ACTION6 @ logical (12, 8)   # orange (12,9) Δ=(0,-1) vert north → (12,8) = target_orange. M3 match. M5 stick. Win.
```

12 actions. **As noted above, M6 (BURST) is not exercised by this witness.** The spec needs revision in `critique_spec` to either (a) place the target inside the anti-anchor zone in a way that requires BURST to enter, or (b) add a wall structure that makes BURST mandatory for transit.

**Difficulty justification.**
- (a) Random-resistance: chains of 12 specific anchor placements selected from 256 cells; random success ≈ (1/256)^12 ≈ 10⁻²⁹.
- (b) Human-tractable: ~2.5 minutes — recognise blocking pawn, plan detour south, recognise anti-anchor effect on row 8, route through rows 9–10.
- (c) Planning depth: STRICTLY DEEPER than L2. (i) named trivial heuristic that fails: **"click target_orange every tick"** — orange runs east on row 8 toward (12, 8); at (5, 8) the next pull east is to (6, 8), still fine; at (7, 8) the pull east → (8, 8) is blocked by stuck purple (M4); secondary-axis Δy=0 — no fallback — orange stays at (7, 8) forever. (ii) witness-pair commute test: swapping action 6 (`ACTION6 @ logical (12, 12)`) and action 7 (`ACTION6 @ logical (12, 12)`) is a no-op (identical clicks), so use the natural near-pair: swap action 7 (`ACTION6 @ logical (12, 12)`) and action 8 (`ACTION6 @ logical (12, 8)`). After commuting: at step 7 anchor is (12, 8); orange at (7, 9) Δ = (5, -1) horiz east → (8, 9). Then step 8 (now (12, 12)) pulls orange south-east; orange at (8, 9) Δ=(4, 3) horiz east → (9, 9). At step 9 with anchor (12, 8), Δ=(3, -1) horiz east → (10, 9); Phase 2 push to (10, 10); but the original sequence had orange at (9, 9) at step 9 entering the anti-anchor-zone with a different vertical position. The commuted sequence ends step 9 at (10, 10) with anchor (12, 8) — same as original step 8 — but the rest of the original witness assumes orange was at (10, 9) → pushed to (10, 10) at step 8, not step 9. The shift means the player needs an *extra* tick of anchor-(12, 8) before action 9, breaking the 12-action witness. So order matters concretely: swapping these two adjacent actions extends the witness or causes M3 to fail.
- (d) Step budget: 60 (5× witness length, generous over the 12-action witness; allows the player ≥ 4× discovery cost for understanding anti-anchor and the south-detour around purple). Not shrinking relative to L2 (L2 was 80 over a 21-action witness ≈ 3.8×; L3 is 60 over 12 actions ≈ 5.0×, so the *ratio* grows even though the absolute budget shrinks — the witness is shorter because L3 has fewer pawns to route).

## 5. Action mapping

`available_actions = [6]`. Pure click. (Consistent with `cross-cut-frequencies.md`'s 19/25 click-based subset; matches ft09, lp85, sc25, vc33, sb26, su15, r11l et al. in the click-only family.)

- **ACTION6** at pixel (x, y) — CLICK: `display_to_grid(x, y)` snaps to logical cell. Anchor relocates to that cell (or toggles off if click is on the current anchor cell). Phase 1 (pull), Phase-1.5 match-check, Phase 2 (anti-anchor push, only if anti-anchor present), Phase-2.5 match-check.

No context-dependent gating.

## 6. HUD and per-game state

**HUD.** A single `RenderableUserDisplay` subclass `StepCounterHud` draws on logical row 15 (frame-pixel rows 60–63) a horizontal bar shrinking from full-width to 0 as `current_steps / step_budget` decreases. Bar colour: light-blue (10) over off-black (4) background. Displays nothing else — a simple step depletion bar consistent with `cross-cut-frequencies.md`'s 25/25 universal pattern.

**Per-game state** (held on `self`):
- `self.anchor` — `Sprite | None`. The single magnetic anchor sprite; `None` when not placed. Lives in the level via `level.add_sprite()` / `level.remove_sprite()` and is INTANGIBLE.
- `self.stuck_pawns` — `set[Sprite]`. Pawns that have matched their target and been removed from slide updates.
- `self.anti_anchor` — `Sprite | None`. Set in `on_set_level` from the level's sprite list (look up by tag); `None` when anti-anchor is absent.
- `self.anti_anchor_range` — `int`. Read from `level.get_data('anti_anchor_range')`; defaults to 0 (no effect).
- `self._step_counter_ui` — `StepCounterHud` instance.

Hidden state (via `_get_hidden_state`):
- `step_counter`, `len(stuck_pawns)`, `anchor` x/y if placed (or `-1, -1`).

## 7. Win condition

After every ACTION6, evaluate Phase-1.5 then Phase-2.5 match-check:

```
def _check_win(self):
    pawns = self.current_level.get_sprites_by_tag('pawn')
    for p in pawns:
        match_target = next(
            (t for t in self.current_level.get_sprites_by_tag('target')
             if t.x == p.x and t.y == p.y
             and self._color_tag(t) == self._color_tag(p)),
            None,
        )
        if not match_target:
            return False
    return True
```

When `_check_win()` returns `True` AND every pawn is in `self.stuck_pawns`, `self.next_level()`.

## 8. Lose condition

`step_counter` reaches 0 → `self.lose()`. No collision-based lose (the harness's `difficulty-rules.md` warns against tight budgets; difficulty comes from puzzle depth, not step pressure). Note: the design has only one resource (steps) — consistent with `cross-cut-frequencies.md` and `core-knowledge-priors.md` § "Energy bar (must-have, 100% of games)".

## 8b. L3 step-budget calibration (post-revision)

After dropping M6, L3's witness simplifies to 12 actions; the budget of 60 is generous (5× witness). The L1 → L2 → L3 budget arc is 30 → 80 → 60 (witness lengths 8 → 21 → 12). The non-monotonic budget (L3 < L2) is justified by witness length and per-`difficulty-rules.md` § 2.d-L3 the budget must NOT shrink relative to the witness — and L3's witness is shorter than L2's, so a smaller absolute budget that still gives 5× the witness length is consistent with the rule's intent (which targets *witness-relative* tightness, not absolute step count).

## 9. Novelty note

Closest taxonomy entries (per `mechanic-novelty/similarity-check.md` family + description checks; full rule walks are in `mechanic-pick.md`):

- **ka59 (sokoban-explode-chase)** — both have multi-pawn movement on a walled grid covering coloured target cells. **Distinguishing rule:** ka59's verb is "click a pawn to make it active, arrows slide that one pawn one cell, pawns push each other"; kn58's verb is "click any cell to (re)place a single magnetic anchor; every pawn slides simultaneously toward the anchor, pawns block each other but never push".
- **m0r0 (mirror-orb-merge)** — both have multi-pawn simultaneous motion. **Distinguishing rule:** m0r0 mirrors per-quadrant axes off the player's directional input; kn58 computes an independent radial gradient per pawn from a shared anchor — direction varies per pawn per tick.
- **wa30 (lock-drag-crate)** — both involve pawns and target rings. **Distinguishing rule:** wa30 has a single carrier walking with arrows + ACTION5 lock; kn58's player never walks any sprite.
- **r11l (centroid-puppet-leg)** — both: click → indirect motion. **Distinguishing rule:** r11l's geometry is centroid-follow (head sits at average of legs); kn58's geometry is gradient-pull from a single point source. The gradient model and centroid model are mathematically distinct fields.

Closest prior-games entries (`prior-games/index.md`; full rules in `mechanic-pick.md`):

- **kf42 (tether-pawn-cycle)** — both have multi-coloured pawns + target tiles. **Distinguishing rule:** kf42 is click-select + arrow-step-active + tether-drag; kn58 has no tether, no select-active, no direct pawn movement. Verb structures are disjoint.
- **pz4t (anchor-pivot-place)** — *the word "anchor" overlaps* but the mechanic does not. **Distinguishing rule:** pz4t's "anchor" is a *pivot offset* used during piece placement (the clicked pixel of a polyomino becomes its placement origin); the verb is click-pixel + arrow-translate + ACTION5-rotate; the goal is to tile a target dark-grey region with all coloured components. kn58's "anchor" is a *standalone magnetic source* on the playfield; the verb is click-empty-cell-to-place-anchor; pawns are pre-existing and slide autonomously toward the anchor; the goal is each pawn on its same-colour target ring. Disjoint verbs, disjoint goals.
- **vn8d (domino-cascade-topple)**, **fz5j (phase-step-tile)**, **gv47 (seed-grow-surround-dissolve)**, etc.: full distinguishing-rule list in `mechanic-pick.md`. None share 3+ heavy dimensions per the negative-similarity walk.
