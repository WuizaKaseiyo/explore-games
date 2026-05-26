# Echo-Delay-Follower

## Summary

The grid hosts a **lead pawn** (player-controlled) and a **follower
pawn** linked to it via an *echo channel*. When the player presses
an arrow key, the lead pawn moves immediately; the follower pawn
also moves — but it executes the lead's move from **K turns ago**,
where K is the per-level *echo delay*. So if K = 2, the
follower's first two moves are no-ops (delay buffer warmup), the
3rd press makes the follower move along whatever the lead did on
press 1, and so on.

The level wins when both pawns simultaneously occupy their own
matching-coloured target rings AT THE END of the same turn. The
only failure mode is exhausting the per-level step counter.

## Visual elements (distinct from prior corpus)

- 12×12 grid; pale-grey floor.
- The **lead pawn** is a 2×2 saturated colour block (orange) with a
  thin coloured outline.
- The **follower pawn** is the same 2×2 size, slightly *desaturated*
  (paler orange), so the visual distinction is colour-saturation,
  not shape. On the same cell, it would be obvious which is which.
- **Echo delay buffer** is rendered along the bottom rim as K
  small chevrons, each chevron coloured by the buffered direction
  (pending move). Chevrons enter on the right and exit on the
  left; the leftmost chevron is the move the follower will execute
  *this turn*. Empty buffer slots stay grey.
- **Targets** are 2×2 hollow rings; orange ring for lead, blue
  ring for follower.
- **Walls** are solid black 1-cell sprites; both lead and follower
  are blocked by them.
- **Spike-tiles** (level 2+) are 1×1 dark-purple cells. ONLY the
  follower dies on contact (lead walks over freely). Stepping the
  follower onto a spike triggers a respawn animation: follower
  returns to its level-start cell and the echo buffer empties.
- **Delay-dial** (level 3+) is a small 3-segment widget on the right
  rim with three states (K = 1, 2, 3). The currently-active K
  segment lights up; clicking the dial via ACTION6 cycles K.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Move lead pawn UP one cell. Push the buffer: enqueue "up"; if buffer length > K, dequeue oldest, apply that direction to follower. | always |
| ACTION2 | Lead DOWN; same buffer logic. | always |
| ACTION3 | Lead LEFT; same. | always |
| ACTION4 | Lead RIGHT; same. | always |
| ACTION6 | (Level 3+) Click the delay-dial to cycle K through {1, 2, 3}. The buffer is *truncated or padded with no-ops* to length K so subsequent moves are well-defined. | only if a delay-dial sprite exists in the level |

## Mechanics enumeration

- **M1 — lead-walk:** ACTION1-4 step the lead pawn 1 cell in the
  pressed direction. Walls block (lead stays put; the buffer still
  records the *attempted* direction so the follower will also try
  to move that direction K turns later, blocked by its own walls).
- **M2 — follower-replay-K:** the follower executes the lead's
  move from K turns ago each turn. For the first K turns of a
  level, the follower's pending-move slot is empty so it does
  not move.
- **M3 — colour-target-pair:** the win condition is BOTH pawns on
  their respective same-colour target ring at end-of-turn. Either
  alone is insufficient.
- **M4 — follower-only-spike:** spike cells kill only the
  follower. Lead can step them freely. Follower spike-death
  respawns it and clears the echo buffer.
- **M5 — delay-dial:** the player can change the echo delay K
  mid-level. Increasing K from 2 to 3 padding-injects a no-op
  into the buffer; decreasing K from 3 to 2 *truncates* the
  oldest pending move (it never reaches the follower).

## Per-level progression (mechanic +1 / +2)

### Level 1 — base system (M1 + M2 + M3)
- K = 2 (fixed; no dial). Open arena with a central wall. 
- Lead starts at (3, 5); follower at (3, 7). Targets: orange ring at (10, 5), blue ring at (10, 8). Notice the targets are NOT just a straight translation of the start positions.
- **Witness:** 12 actions. Because K=2, the follower replicates the lead's path with a 2-step lag. The lead must deliberately step back and forth (wasting steps) to allow the follower to catch up or align vertically before the lead enters its target.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (follower-only spike)
- K = 3. Multiple walls and a corridor filled with spike-tiles that only kill the follower. 
- **Witness:** 25 actions. The lead must walk a safe path, but at specific points, the lead must "stall" in a safe zone so that the follower (lagging by 3 steps) doesn't walk into a spike. If the lead walks continuously, the follower will replicate the path but its delayed timing will align it with moving hazards or force it onto spikes. 
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (delay-dial)
- Complex maze with multiple spike fields. Two target pairs. 
- **Witness:** 50+ actions. The player MUST cycle K mid-level via the dial to "phase shift" the follower. For example, K=2 allows the follower to squeeze past the first spike field, but the second spike field requires K=1. The lead must safely navigate to the dial, cycle it, and then continue, while ensuring the buffer truncation/padding doesn't immediately kill the follower.
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every action, check both pawn positions. If `lead.pos == lead_target.pos` AND `follower.pos == follower_target.pos`, `self.next_level()`.

## Lose condition
- `steps_used >= max_steps` → `self.lose()`.
- (Optional) follower spike-deaths beyond a per-level cap; cleaner to allow infinite respawns and lose only on step exhaustion.

## Internal state
- `self.lead: Sprite` / `self.follower: Sprite`.
- `self.buffer: collections.deque[int]` — buffered direction codes; length always exactly K after each step.
- `self.delay_K: int` — current echo delay.
- `self.lead_start: tuple[int, int]` / `self.follower_start: tuple[int, int]`.
- `self.spikes: set[(int, int)]` — spike cells.
- `self.walls: set[(int, int)]`.
- `self.targets: dict[Sprite, Sprite]` — pawn → required-target.
- `self.dial: Sprite | None` — delay-dial sprite (level 3+).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `kf42 — tether-pawn-cycle`**: Echo-delay-follower has *temporal* coupling — the follower repeats the lead's move from K turns earlier, with no spatial constraint between them.

## Step budget
- L1: 30.
- L2: 60.
- L3: 120.

## Random-resistance
Random arrow presses on the lead drive a random walk; the follower replays with K turns delay, so two simultaneously-random walks will not converge on their respective targets on the exact same turn. Spikes make random paths fatal.

## Planning depth
- **L1:** moderate — player must realize they need to use "stalling" moves (e.g., left-right-left-right) to adjust the relative positioning of the follower before stepping on the target.
- **L2:** deep — player must mentally project two paths simultaneously, offset by K=3 steps, to ensure the follower never touches a spike.
- **L3:** very deep — cycling K dynamically alters the buffer length. The player must calculate exactly when to hit the dial to shift the follower's phase without causing it to jump into a spike.
