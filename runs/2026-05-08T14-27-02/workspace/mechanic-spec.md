# mechanic-spec — `vy3m`

## 1. Title

Class-Roster Push-Pull-Chain (working title)

## 2. Mechanic family

**Class-swap roster**: 1-3 player-controlled actor sprites of distinct classes, each with its own crate-interaction verb. ACTION5 cycles the active actor; only the active actor responds to ACTION1-4. Classes are PUSHER (single push), PULLER (drag-when-walking-away), STOMPER (push + chain-push-of-2). Drawing from `core-knowledge-priors.md` Objectness + Agentness. Inspired by step 5's `heroes_of_sokoban.txt`.

## 3. Sprite roster

- **pusher** (5×5; palette 9 blue + 4 black + 0 white): walking INTO crate pushes it forward (cell beyond must be empty).
- **puller** (5×5; palette 14 green + 4 black + 0 white): walking AWAY FROM crate (crate adjacent in opposite-of-motion direction) drags it to puller's old cell. Walking INTO crate is BLOCKED no-op.
- **stomper** (5×5; palette 12 orange + 4 black + 0 white): walking INTO crate triggers single-push OR chain-push-of-2 (if cell beyond crate has another crate AND cell beyond THAT is empty, push both).
- **crate** (4×4; palette 12 orange + 13 maroon).
- **target** (3×3; palette 11 yellow + 4 dark ring).
- **wall** (4×4; palette 3 grey + 4 corners).
- **active_class_hud** (RenderableUserDisplay): top-left 4×4 badge tinted by active-class colour.
- **step_counter_hud**: bottom-row depleting bar.

## 4. Level progression

Three mechanics, one introduced per level:

- **M1** (L1): push verb (Pusher only).
- **M2** (L2): class-swap (ACTION5 cycles) + Puller's drag-when-walking-away verb.
- **M3** (L3): extended class-swap to 3 classes + Stomper's chain-push-of-2 verb.

### Level 1 — base (M1)

**Layout** (10×10):
- Pusher at (2, 4)
- crate at (5, 4)
- target at (8, 4)
- walls rows 3, 5 (cols 2-8) seal the corridor.

**Mechanics** (N=1): M1.

**Witness**: `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (6 actions: 2 walks + 4 pushes).

**Difficulty**: (a) random P(win) ≈ 0.025% per attempt, budget 30. (b) ~30 sec. (c) L1 = no planning gate. (d) step_budget=30.

### Level 2 — base + M2

**Layout** (12×12):
- **Push lane** (row 2): Pusher at (1, 2); crate_a at (4, 2); target_a at (8, 2). Walls rows 1, 3 (cols 1-10).
- **Pull lane** (row 7): Puller at (4, 7); crate_b at (5, 7); target_b at (3, 7). Walls rows 6, 8 (cols 1-10).
- Lanes vertically isolated (no col connecting rows 2-7).

**Mechanics** (N+1 = 2): M1 (push) + M2 (class-swap + pull).

**Necessity:**
- L2 cannot be solved without M1 because crate_a at (4, 2) must reach target_a at (8, 2); only Pusher's push verb moves it east in the push lane.
- L2 cannot be solved without M2 because crate_b at (5, 7) must reach target_b at (3, 7) (west); pushing crate_b west requires pusher at (6, 7) walking west; pull lane is sealed from push lane (no vertical connection); only Puller starting at (4, 7) can move crate_b. ACTION5 to cycle from Pusher to Puller is required.

**Witness** (12 actions):
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,    # Pusher: 3 walks + 4 pushes
 ACTION5,                                                            # cycle to Puller
 ACTION3, ACTION3,                                                   # Puller: 2 pulls west
 ACTION5, ACTION5]                                                   # filler / no-op (cycle)
```
Specifically: Pusher (1, 2) walks to (4, 2) crate, pushes 4 cells east → target. Cycle. Puller (4, 7) ACTION3 walks west to (3, 7) [target cell, intangible]; crate at (5, 7) is east of Puller, opposite of west; pull fires; crate → (4, 7). Puller at (3, 7); ACTION3 walks west to (2, 7); crate at (4, 7) east; pull; crate → (3, 7) = target_b. WIN.

(Witness is 11 actions: 7 Pusher + 1 cycle + 2 Pulls + 1 cycle. Removed unnecessary trailing cycles.)

Final witness: `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION5, ACTION3, ACTION3]` (10 actions).

**Trivial heuristic action sequence**: `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (12 ACTION4 — "always control Pusher, press right"). Delivers crate_a to target_a (5 ACTION4 used); subsequent pushes drive Pusher east into walls/boundary. Pull lane is sealed; Puller never activated; crate_b never moves. **Level does NOT advance**. Structurally distinct from witness (no ACTION5 cycle, no ACTION3 west-pulls).

**Difficulty:**
- (a) random: P(random win in 50) negligible.
- (b) ~90 sec. Player observes Pusher can't reach pull lane; discovers ACTION5 cycle.
- (c) post-discovery: 5 valid first actions. Plausible-but-wrong: cycling to Puller before delivering crate_a (works but wastes steps). Reasoning: "Pusher delivers a; cycle; Puller delivers b."
- (d) step_budget=50.

### Level 3 — base + M2 + M3

**Layout** (14×14):
- **Push lane** (row 2): Pusher at (1, 2); crate_a at (4, 2); target_a at (8, 2). Walls rows 1, 3.
- **Pull lane** (row 7): Puller at (4, 7); crate_b at (5, 7); target_b at (3, 7). Walls rows 6, 8.
- **Chain lane** (row 12): Stomper at (1, 12); crate_c1 at (3, 12); crate_c2 at (4, 12); target_c at (7, 12). Walls rows 11, 13.
- All three lanes vertically isolated.

**Mechanics** (M+1 = 3): M1 + M2 + M3.

**Necessity:**
- L3 cannot be solved without M1 because crate_a still requires push.
- L3 cannot be solved without M2 because crate_b still requires pull.
- L3 cannot be solved without M3 because crate_c2 must reach target_c at (7, 12); the path requires moving crate_c1 AND crate_c2 east; Pusher's single-push fails on chain-of-2 (push dest of crate_c1 has crate_c2; non-Stomper classes reject chain). Stomper's chain-push-of-2 is the only verb that propagates the chain.

**Witness** (15 actions):
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,  # Pusher: 3 walks + 4 pushes
 ACTION5,                                                          # cycle Pusher → Puller
 ACTION3, ACTION3,                                                 # Puller: 2 pulls west
 ACTION5,                                                          # cycle Puller → Stomper
 ACTION4, ACTION4, ACTION4, ACTION4]                              # Stomper: 1 walk + 3 chain pushes
```

**Trivial heuristic action sequence**: `[ACTION4×15]` (15 ACTION4 — "always control Pusher, press right"). Delivers crate_a (5 actions); subsequent ACTION4s drive Pusher east into walls. Pull and chain lanes sealed; Puller and Stomper never activated; crate_b and crate_c never moved. **Level does NOT advance**.

**Difficulty:**
- (a) random: negligible.
- (b) ~3 min. Player must discover all 3 classes, distinguish Pusher's failure on chain-of-2 from Stomper's success.
- (c) post-discovery: 5 valid first actions. Plausible-but-wrong: trying to push chain crates with Pusher (single push fails when 2nd crate behind 1st). Reasoning: "Each lane requires its specific class; cycle through all 3."
- (d) step_budget=80.

## 5. Action mapping

- ACTION1-4: walk active class one cell. Verb fires per active class on walking-into-crate (Pusher: push; Puller: blocked; Stomper: push or chain-push-of-2).
- ACTION5: cycle active class. Pusher → Puller → Stomper → Pusher (depending on which classes are active in current level).
- ACTION6, ACTION7: not used.

`available_actions = [1, 2, 3, 4, 5]`.

## 6. HUD and per-game state

- `StepCounterHud`: bottom-row depleting bar.
- `ActiveClassHud`: top-left 4×4 badge coloured by active class.

State:
- `self._active_class: str` ∈ `{"pusher", "puller", "stomper"}`.
- `self._steps_used: int`, `self._max_steps: int`.

## 7. Win condition

`{(t.x, t.y) for t in targets}.issubset({(c.x, c.y) for c in crates})`.

## 8. Lose condition

`self._steps_used >= self._max_steps`.

## 9. Novelty note

- Closest taxonomy: **ka59** (sokoban-explode-chase) — multi-pawn click-cycle; distinguishing rule: ka59's pawns all use the SAME slide-3-cells movement; this candidate has THREE DIFFERENT verbs across Pusher/Puller/Stomper.
- Closest prior: **mr5q** (polarity-attract-discharge) — autonomous walking; distinguishing rule: this candidate has NO autonomous behaviour; only the active actor moves; class is fixed-per-actor (no flip).
- §3.4: Heroes of Sokoban (commercial indie). Distinction: simplified to push/pull/chain (no teleport / level-completion-cooldown); fundamentally different replayability; user verifies ceiling.
