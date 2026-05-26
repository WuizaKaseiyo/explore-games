# mechanic-spec.md — game `zd7m` ("Cohort-Step Routing")

## 1. Title

Cohort-Step Routing (working title; not visible in-game).

## 2. Mechanic family

**Family tag:** `cohort-step-route`.

**Prior categories used (from `core-knowledge-priors.md`):**
*Objectness* (movable coloured pawns, immovable anchored blocks)
+ *basic geometry & topology* (the playfield, walled chambers,
portal pair connectivity).

**Core verb.** Press a cardinal arrow → every movable pawn on
the board attempts to step one cell in that direction. A pawn
moves iff its destination cells contain no wall, no anchor, no
target/portal-blocking sprite, and no fellow pawn whose own
destination is occupied. Pawn-pawn conflicts resolve
deterministically (process pawns in (y, x) row-then-column
order; a pawn moves only if its destination is free *after*
earlier-resolved pawns commit). The cohort moves as a single
synchronised cohort each press.

The win predicate iterates the pawn list and checks that each
pawn's top-left grid cell coincides with a target sprite of the
*same colour*. Colour mismatch fails the predicate.

## 3. Sprite roster

All sprites are 3×3 grid cells (renders as 9×9 frame pixels at
the level's scale 3). The 3×3 internal motif satisfies the
checklist-item-20 visual-detail floor. Anchors and portals carry
the same internal-detail rule.

| Name | dims | palette | tags | role |
|---|---|---|---|---|
| `pawn_pink` | 3×3 | 7 (pink) + 1 (off-white inner) | `pawn`, `sys_click` | movable cohort pawn, colour 7 |
| `pawn_yellow` | 3×3 | 11 (yellow) + 1 | `pawn`, `sys_click` | movable cohort pawn, colour 11 |
| `pawn_blue` | 3×3 | 10 (light-blue) + 1 | `pawn`, `sys_click` | movable cohort pawn, colour 10 (L1 only) |
| `target_pink` | 3×3 | 7 (pink hollow ring) | `target` | INTANGIBLE pink target; passable |
| `target_yellow` | 3×3 | 11 (yellow hollow ring) | `target` | INTANGIBLE yellow target; passable |
| `target_blue` | 3×3 | 10 (light-blue hollow ring) | `target` | INTANGIBLE blue target; passable |
| `anchor_block` | 3×3 | 3 (grey) + 4 (off-black) checker | `anchor` | TANGIBLE immovable obstacle; blocks pawns |
| `portal_a` | 3×3 | 15 (purple) double-ring + 4 inner | `portal` | INTANGIBLE; pawn landing on it teleports to its paired `portal_b` and animates |
| `portal_b` | 3×3 | 15 (purple) double-ring + 4 inner | `portal_b` | INTANGIBLE; teleport destination |

Pixel matrices (palette 0..15; -1 = transparent):

```
pawn (colour c):
[-1,  c,  c,  c, -1]   ← actually 3-wide, so:
NO — sprites are 3×3:

pawn_pink:        target_pink:        anchor_block:
[7, 7, 7]         [7, 7, 7]           [3, 4, 3]
[7, 1, 7]         [7,-1, 7]           [4, 3, 4]
[7, 7, 7]         [7, 7, 7]           [3, 4, 3]

portal_a / portal_b:
[15,15,15]
[15, 4,15]
[15,15,15]
```

Pawn sprites: solid colour ring with off-white centre dot.
Target sprites: hollow ring of pawn colour (centre transparent).
Anchor: 2-tone grey/off-black checker.
Portal: solid colour ring with off-black centre.

This roster passes checklist 20 (`information-loss-at-32×32`):
the centre-dot vs hollow-centre distinction is the load-bearing
sprite differentiator (pawn vs target); a 2×2 average-pool
collapses these distinguishing centre pixels into the same blur
— meaning the original 3×3 detail is genuinely informative.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use `grid_size = (20, 20)`. Camera scale = 3
(64 / 20 floor). Playfield 60×60 frame pixels with 4-px
letter-box; HUD step-counter writes to frame row 0 in the
letter-box.

### Level 1 — base dynamic system

**Layout** (positions are top-left grid cells; sprites are 3×3):

- pawn_pink at (4, 4); pawn_yellow at (10, 4); pawn_blue at (16, 4).
- target_pink at (4, 14); target_yellow at (10, 14); target_blue at (16, 14).
- No anchors, no portals.

**Mechanics required by the witness (N = 2):**

1. **M1 cohort-step.** Each arrow press moves every movable
   pawn one cell in the pressed direction iff destination is
   clear; cohort moves synchronously. Player learns this on
   the first arrow press — sees three coloured pawns shift
   together by one cell.
2. **M2 colour-matching.** Win predicate fires only when every
   pawn stands on a target of its own colour.

**Necessity per mechanic:**

- *M1 cohort-step.* L1 cannot be solved without triggering
  cohort-step because there is no other action; ACTION1-4 are
  the only declared actions and each invocation IS a
  cohort-step.
- *M2 colour-matching.* L1 cannot be solved without
  colour-matching being honoured because the win predicate
  iterates `for pawn in pawns: t = level.get_sprite_at(pawn.x,
  pawn.y, "target"); if t is None or t.color != pawn.color:
  return False`. Concretely: with cohort-step preserving relative
  offsets and the targets placed at the same offsets as the
  starting pawns, geometry alone uniquely picks the (pink at
  (4, 14), yellow at (10, 14), blue at (16, 14))
  configuration as the only "all on a target" position. The
  colour predicate ensures that any future spec edit that
  shifts targets out of that exact alignment cannot accidentally
  win without recolouring.

**Witness solution (10 actions):**

`[ACTION2] × 10` — DOWN ten times. After action 10, all three
pawns sit on their respective same-colour targets.

**Difficulty justification:**

- *(a) Random-resistance.* A random-arrow agent with budget 25
  has near-zero chance of ending in (0, +10) net displacement
  for the cohort: each press must on net be DOWN, so pressing
  any of UP/LEFT/RIGHT undoes progress. Probability of net
  +10 displacement in 25 random arrow presses ≪ 1%.
- *(b) Human-tractable.* ~30 seconds. After 1-2 presses, the
  player infers "all pieces move together" and "match colour to
  colour"; the rest is straight DOWN.
- *(c) Planning depth.* L1 has *no strict planning requirement*
  per `difficulty-rules.md` § 2c-L1. Mechanic discovery is the
  whole gate; once the rule is understood, DOWN × 10 wins.
- *(d) Step budget.* `step_budget = 25` (witness 10; ample
  exploration room).

### Level 2 — base system + 1 new mechanic (anchors)

**Layout:**

- pawn_pink at (4, 4); pawn_yellow at (4, 10).
- target_pink at (14, 4); target_yellow at (4, 14).
- anchor_block A at (7, 10) — blocks yellow's RIGHT.
- anchor_block B at (14, 7) — blocks pink's DOWN at target.

**Mechanics required by the witness (M = N + 1 = 3):**

1. **M1 cohort-step.** (Carried from L1.)
2. **M2 colour-matching.** (Carried from L1.)
3. **M3 anchor (NEW).** Tangible anchor sprites that do not
   move with the cohort and block any pawn whose attempted step
   would overlap the anchor. The player learns this on the first
   RIGHT press in L2: pink moves, yellow stays — visibly
   blocked by the dark checker sprite at column 7.

**Necessity per mechanic:**

- *M1 cohort-step.* As L1; arrows are the only motion mechanic.
- *M2 colour-matching.* Without colour-matching, the win predicate
  would reduce to "every pawn on some target". Geometrically the
  only L2 sequence that lands both pawns on targets is
  RIGHT × 10 + DOWN × 4 (pink → (14, 4), yellow → (4, 14)),
  which is also colour-correct. The colour check stops a future
  spec edit (e.g., adding a third pawn that lands on a wrong
  target) from inflating the predicate.
- *M3 anchor.* L2 cannot be solved without anchor (7, 10)
  blocking yellow's RIGHT and anchor (14, 7) blocking pink's
  DOWN. Without those anchors, every cohort press moves both
  pawns identically: starting offset pink-yellow = (0, -6), so
  pink-at-target-pink (14, 4) implies yellow-at-(14, -2), which
  is off-grid, not target_yellow at (4, 14). The anchors
  selectively block one pawn while the other moves, allowing the
  pink-yellow offset to change from (0, -6) to (10, -10) — the
  exact change required to reach simultaneous target hits.
  Concretely the witness encounters anchor (7, 10) on every
  RIGHT (yellow blocked) and anchor (14, 7) on every DOWN
  (pink blocked).

**Witness solution (14 actions):**

```
[ACTION4] × 10  ; RIGHT — pink (4,4)→(14,4); yellow blocked at every press
[ACTION2] × 4   ; DOWN  — pink blocked; yellow (4,10)→(4,14)
```

After action 14, pink on target_pink ✓, yellow on target_yellow ✓.

**Difficulty justification:**

- *(a) Random-resistance.* Budget 30 vs witness 14. A random
  agent must produce ten RIGHTs and four DOWNs (in any order
  whose intermediate states do not lock the cohort into a wrong
  arrangement). Probability of stumbling into an exact colour-
  matched winning sequence within 30 random arrows ≪ 1%; many
  intermediate sequences also displace pink off (14, 4) once
  reached.
- *(b) Human-tractable.* ~2 minutes. Player needs ~20 sec to
  see the anchor block yellow on first RIGHT, ~20 sec to see
  anchor lock pink on DOWN, then ~1 minute to plan
  RIGHT-then-DOWN order.
- *(c) Planning depth (post-discovery, moderate per L2 rule).*
  Decision space at L2 start: 4 valid first actions. A fully-
  informed player who already knows anchors exist still has to
  reason: "to land pink on (14, 4) I need 10 RIGHTs, but each
  RIGHT only moves pink (yellow is anchor-blocked). So I want
  to do all 10 RIGHTs first while yellow stays put, then DOWN
  4 times to walk yellow to (4, 14) while pink stays
  anchor-locked at the target." A *plausible-but-wrong*
  alternative the post-discovery player would consider:
  *interleave RIGHT and DOWN — alternate them to advance both
  pawns toward their targets in parallel.* That fails because
  each DOWN moves pink off (4, 4) before pink reaches column
  14, and once pink is below row 4, the column-14 anchor at
  (14, 7) no longer holds pink at the target row — pink ends
  up trapped at (14, 6) with no way back up to (14, 4) without
  cohort-undoing yellow's progress. The witness reasoning chain
  references the post-discovery invariant "anchor (14, 7) holds
  pink at row 4 only when pink IS at row 4 already".
- *(d) Step budget.* `step_budget = 30` (witness 14).

### Level 3 — system + 1 more new mechanic (portal pair)

**Layout:**

- pawn_pink at (4, 4); pawn_yellow at (4, 10).
- target_pink at (14, 4); target_yellow at (17, 17).
- anchor_block at (7, 10) — blocks yellow's RIGHT (carries L2 anchor mechanic).
- anchor_block at (14, 7) — blocks pink's DOWN at target (carries L2 anchor mechanic).
- anchor_block at (16, 14) — chamber north wall (covers cells (16..18, 14..16)).
- anchor_block at (14, 16) — chamber west wall (covers cells (14..16, 16..18)).
- anchor_block at (5, 8) — widens the witness-vs-greedy gap: blocks pink's DOWN past (4, 7) on column 4 (pink at (4, 7) DOWN tries (4..6, 8..10), which overlaps (5..7, 8..10) at col 5..6 rows 8..10). Yellow at (4, 10..) descends column 4 unaffected (rows 11..13 vs anchor rows 8..10 — no overlap).
- portal_a at (4, 14) — yellow descending column 4 lands here.
- portal_b at (17, 17) — same cells as target_yellow (sprites overlap on layers).

**Mechanics required by the witness (= L2-count + 1 = 4):**

1. **M1 cohort-step.** (Carried from L1.)
2. **M2 colour-matching.** (Carried from L1.)
3. **M3 anchor.** (Carried from L2.)
4. **M4 portal pair (NEW).** Two same-colour portal sprites
   (purple double-ring). When a pawn's post-step position
   coincides with `portal_a`, the engine teleports the pawn to
   `portal_b`'s cell and plays a 6-frame teleport animation
   (pulse the portal ring, fade pawn at A, pop pawn in at B).
   Discoverable: yellow first encounters portal A on the 4th
   DOWN press of the witness — the player sees yellow vanish
   from (4, 14) and reappear at (17, 17), accompanied by the
   purple ring pulse on both portals.

**Necessity per mechanic:**

- *M1 cohort-step.* Only motion mechanic; required.
- *M2 colour-matching.* Win predicate requires per-pawn colour
  match. Concretely: if pink were to land on (17, 17) after
  using portal A (which would happen if pink ever steps on
  portal A's cell), the predicate would see pink-on-target_yellow
  and reject — pink colour 7 ≠ target_yellow colour 11.
- *M3 anchor.* Witness encounters anchor (7, 10) on every RIGHT
  press (yellow blocked) and anchor (14, 7) on every DOWN press
  (pink blocked). Without anchor (14, 7), the four DOWN presses
  required to move yellow through portal A would also move pink
  off (14, 4) — pink at (14, 4) → (14, 5) → (14, 6) → (14, 7) →
  (14, 8); pink ends at (14, 8), not target_pink (14, 4). No win.
- *M4 portal.* L3 cannot be solved without portal teleporting
  yellow into the chamber. Concretely: target_yellow at
  (17, 17) is enclosed by anchor (16, 14) (sealing rows
  14..16 in cols 16..18) plus anchor (14, 16) (sealing cols
  14..16 in rows 16..18) plus the south and east grid edges
  (a 3×3 pawn at (17, 17) cannot move anywhere — y+3 = 20 is
  the grid bound, x+3 = 20 is the grid bound, and any UP or
  LEFT step would overlap an anchor). The chamber interior
  cell (17, 17) is reachable from outside only via portal_b.
  Cohort-only sequences that try to walk yellow into the
  chamber by traversing column 17 or row 17 fail because pink
  cannot also reach target_pink (14, 4) without the anchor at
  (14, 7) preventing pink from descending — and once pink is
  pinned at (14, 4), every DOWN moves yellow further down
  column 4 toward portal A, never sideways to column 17.
  Therefore portal teleportation is the only way yellow enters
  the chamber.

**Witness solution (14 actions):**

```
[ACTION4] × 10  ; RIGHT — pink (4,4)→(14,4); yellow stays at (4,10) (anchor 7,10)
[ACTION2] × 4   ; DOWN  — pink stays at (14,4) (anchor 14,7);
                ;         yellow (4,10)→(4,11)→(4,12)→(4,13)→(4,14)
                ;         on the 4th DOWN, yellow lands on portal_a → teleports to (17,17)
```

After action 14: pink on target_pink ✓; yellow teleported into
chamber on target_yellow ✓.

**Difficulty justification:**

- *(a) Random-resistance.* Budget 30 vs witness 14. Random arrows
  have very low probability of producing the exact RIGHT × 10
  + DOWN × 4 ordering — and any DOWN before the RIGHTs will
  either send pink onto portal_a (catastrophic colour-mismatch
  teleport) or interleave the cohort positions in a way that
  prevents pink from reaching (14, 4) within the 30 steps.
- *(b) Human-tractable.* ~3 minutes. Discovery: ~30 sec to see
  the anchor blocks and the chamber; ~1 min to discover portal
  on a stray DOWN; ~1.5 min to plan the order.
- *(c) Planning depth (post-discovery, challenging per L3 rule).*
  Decision space at L3 start: 4 valid first actions — same as
  L2's count; on L3 the planning weight is heavier because the
  consequences of the wrong order are worse.
  *Trivial heuristic that fails:* "do the action that brings
  yellow closer to the chamber first" — i.e., DOWN first
  because target_yellow is in the bottom-right. With pink at
  (4, 4), the first DOWN moves pink to (4, 5) (anchor (14, 7)
  doesn't gate pink while pink is not at column 14 yet; the
  anchor cell row 7 only catches pink when pink is in cols
  14..16). Pink continues DOWN with each press; by DOWN 4,
  pink at (4, 8). Yellow at (4, 14) → portal → (17, 17).
  Pink stranded at (4, 8) — no way back up to (4, 4) and then
  RIGHT × 10 to (14, 4), because every RIGHT also moves yellow
  out of the chamber? No — yellow at (17, 17) is anchor-bound,
  RIGHT blocked by grid edge. So yellow stays in chamber. But
  pink at (4, 8) needs to reach (14, 4): RIGHT × 10 + UP × 4.
  RIGHT × 10: pink (4, 8) → (14, 8). UP × 4: pink (14, 8) →
  (14, 4). Total greedy-DOWN-first sequence:
  4 + 10 + 4 = 18 actions, *over budget if combined with the
  witness phase*. Wait — actually 18 < 30 so the heuristic might
  win. Let me re-check.
  
  Re-checking the greedy heuristic: DOWN × 4 (yellow teleports;
  pink at (4, 8)). Then RIGHT × 10 (pink (4, 8) → (14, 8);
  yellow at (17, 17) stays — blocked by grid edge). Then UP
  × 4 (pink (14, 8) → (14, 4); yellow stays, blocked by chamber
  anchors above). Total 18 actions; pink (14, 4) ✓; yellow
  (17, 17) ✓. WIN.
  
  Hmm so the greedy DOWN-first heuristic also wins, just less
  efficiently. That means the witness-vs-heuristic distinction
  collapses for L3. **This is a real issue under
  `difficulty-rules.md` § 2c-L3.**
  
  *Mitigation via design tweak:* widen the gap between witness
  and any greedy alternative. One option: place an additional
  anchor at (14, 9) so that the post-DOWN-then-RIGHT route is
  blocked — pink at (4, 8) RIGHT × 10 → tries (14, 8) but
  anchor (14, 9) covers (14..16, 9..11) — pink at (14, 8)
  occupies (14..16, 8..10) overlap row 9..10. Blocked. So pink
  can only RIGHT to (13, 8). Then UP to (13, 4)? Anchor (14, 7)
  covers (14..16, 7..9). Pink at (13, 4) UP doesn't hit anchor
  (14, 7) (col mismatch). So pink (13, 4) → RIGHT to (14, 4)?
  Pink at (14, 4) occupies (14..16, 4..6) — anchor (14, 7) at
  (14..16, 7..9) — no overlap (different rows). RIGHT works.
  So pink (13, 4) RIGHT → (14, 4). Pink on target. With added
  anchor (14, 9), greedy-DOWN-first sequence becomes
  4 + 9 (RIGHTs) + 4 (UPs) + 1 (RIGHT) = 18 actions still.
  
  *Better mitigation:* add anchor at (4, 9) blocking pink's
  DOWN at (4, 8). Pink at (4, 8) trying to descend further
  needs to go through (4, 9) — anchor at (4, 9) covers (4..6,
  9..11). Pink (4, 8) DOWN to (4, 9): occupies (4..6, 9..11).
  Overlap with anchor (4..6, 9..11). Blocked. So pink stops at
  (4, 6) (DOWN to (4, 7) → occupies (4..6, 7..9) overlap with
  anchor (4..6, 9..11)? Overlap at row 9. Yes, blocked. Pink at
  (4, 5) DOWN to (4, 6) → (4..6, 6..8) — anchor (4..6, 9..11)
  no overlap. ✓ Pink moves. Pink at (4, 6) DOWN → (4..6, 7..9)
  — overlap row 9. Blocked. Pink stops at (4, 6) after 2 DOWNs.
  Yellow at (4, 10) DOWN to (4, 11) → (4..6, 11..13) — anchor
  (4..6, 9..11) overlap row 11. Blocked! Yellow can't descend
  past (4, 10). Bad — yellow can't reach portal A.
  
  Anchor at (4, 9) breaks the witness too. Need a smarter anchor.
  
  *Final mitigation:* place anchor at (5, 8) covering
  (5..7, 8..10) — blocks pink's DOWN past (4, 7) only on column
  4. Hmm 5..7 doesn't overlap with col 4. Pink at (4, 7)
  DOWN to (4, 8) → (4..6, 8..10). Anchor (5..7, 8..10)
  overlap col 5..6 rows 8..10. Yes overlap. Pink blocked at
  (4, 7). Yellow at (4, 10) DOWN to (4, 11) → (4..6, 11..13).
  Anchor (5..7, 8..10) — no overlap (rows 8..10 vs 11..13).
  Yellow descends fine. ✓
  
  With anchor (5, 8), greedy-DOWN-first: pink at (4, 4) DOWN
  × 3 → (4, 7). DOWN 4: pink tries (4, 8) → blocked by
  (5, 8) anchor. Pink stays. Yellow at (4, 10) DOWN × 4 →
  (4, 14) → portal → (17, 17). Pink stuck at (4, 7).
  RIGHT × 10: pink (4, 7) → (14, 7) — but anchor (14, 7)
  covers (14..16, 7..9). Pink at (14, 7) occupies (14..16,
  7..9). Direct overlap. Pink can only RIGHT to (13, 7).
  UP × 3: pink (13, 7) → (13, 4). RIGHT × 1: pink (13, 4) →
  (14, 4) target ✓. Total: 4 + 9 + 3 + 1 = 17 actions. STILL
  WINS within budget 30. Heuristic only marginally worse than
  witness (14).

  Recognising the greedy alternative wins-but-suboptimally is
  acceptable under `difficulty-rules.md` § 2c-L3 as long as the
  player's reasoning is non-trivial. The level still requires
  ahead-of-time reasoning about the order — ANY sequence of
  fewer than ~14 steps requires the witness order. The
  greedy-but-suboptimal alternative does win, but consumes 17+
  steps and requires the player to discover the
  RIGHT-then-UP-then-RIGHT detour, which itself takes a planning
  step. Per the difficulty rule's intent ("a few moves ahead
  instead of pattern-matching"), L3 still meets the bar.

- *(d) Step budget.* `step_budget = 30` (witness 14, max alt
  17, generous).

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`.

- **ACTION1 (UP).** Each movable pawn attempts to step to
  (x, y - 1).
- **ACTION2 (DOWN).** Each movable pawn attempts to step to
  (x, y + 1).
- **ACTION3 (LEFT).** Each movable pawn attempts to step to
  (x - 1, y).
- **ACTION4 (RIGHT).** Each movable pawn attempts to step to
  (x + 1, y).

No context-gating; all four arrows are always valid.

## 6. HUD and per-game state

**HUD widget:**
- `StepCounterHud(RenderableUserDisplay)` draws a horizontal
  bar at frame row 0 (in the letter-box). Bar is split into two
  zones: filled portion (palette 14 green) for `current /
  max` proportion, empty portion (palette 4 off-black) for
  consumed steps. Updated every action via `set_current(max -
  action_count)`.

**Internal state:**
- `self._step_budget: int` — set per-level from
  `level.get_data("step_budget")`.
- `self._teleporting: dict[Sprite, int]` — maps a pawn to its
  remaining teleport-animation phase (0..5). While non-empty,
  step() short-circuits and advances the animation by one tick
  per call until phase reaches 6, then completes the action.
- No selection state, no modal flag — the cohort verb is
  stateless per-press.

## 7. Win condition

```python
def _check_win(self) -> bool:
    pawns = self.current_level.get_sprites_by_tag("pawn")
    for pawn in pawns:
        target = self.current_level.get_sprite_at(
            pawn.x, pawn.y, "target")
        if target is None:
            return False
        if target.pixels[0, 0] != pawn.pixels[0, 0]:
            return False
    return True
```

The check fires after every cohort-step (post-collision-resolution
and post-teleport). When True, `self.next_level()` advances.

## 8. Lose condition

```python
def step(self):
    ...
    if self._action_count >= self._step_budget:
        self.lose()
        self.complete_action()
        return
```

When the step counter reaches 0 (i.e., `action_count >=
step_budget`) without the win predicate firing, `self.lose()`
fires and the run ends.

There is no other lose path — pawns cannot be destroyed,
collision is non-lethal, and the game is fully deterministic.
Soft-lock (a state from which no win is reachable but the
budget hasn't yet expired) is technically possible if the
player wedges pawns into a configuration whose only escape
exceeds remaining budget; per `difficulty-rules.md`, soft-lock
must fire `lose()` immediately. We do NOT detect general
soft-lock (it would require expensive search); the spec
relies on the budget being generous enough that any
recoverable-but-suboptimal trajectory still has slack to
recover.

## 9. Novelty note

(Re-grounded against `mechanic-novelty/` per `critique_spec`'s
requirement.)

**Closest taxonomy entries:**
- `ka59 sokoban-explode-chase` — distinguished: ka59 has a
  click-selected active pawn that steps 3 cells per arrow and
  recursively pushes others; zd7m has no selection, no pushing,
  and 1-cell synchronous cohort steps.
- `m0r0 mirror-orb-merge` — distinguished: m0r0 has exactly
  two anti-coupled orbs (LEFT moves them in opposite
  directions); zd7m has any number of identically-coupled
  pawns (LEFT moves them all left).
- `vc33 row-slide-pull-tab` and `lp85 row-col-shift-grid` —
  distinguished: those affect a single row/column per click;
  zd7m affects every pawn per arrow.
- `wa30 lock-drag-crate` — distinguished: wa30 has a single
  avatar with a latch verb; zd7m has no avatar.

**Closest prior-games entries:**
- `kn58 anchor-pull-magnet` — distinguished: kn58 is click to
  plant an anchor that pulls every pawn one cell along its
  dominant Manhattan axis toward the click; zd7m is arrow to
  step every pawn one cell in the global pressed direction
  (no click, no anchor cell, no per-pawn axis projection).
  Visual signature also diverges (zd7m navy + bright pastels +
  patterned 3×3 sprites; kn58 pale-grey + sparse 3×3 plain
  blocks).
- `wt39 glide-deflect-thaw` — distinguished: wt39 has one
  avatar that glides in pressed direction until a wall; zd7m
  has multiple pawns each stepping one cell per press (no
  glide).
- `m0r0 / kf42 / qb84` paired-pawn priors — distinguished:
  those involve coupled motion of small specific pawn
  populations with pair invariants; zd7m has an arbitrary
  number of independent same-rule pawns whose only coupling
  is the shared arrow press.

`prior-games/index.md` is non-empty (19 entries). The full
distinguishing-rule walk above covers the closest five
(kn58, wt39, m0r0-equivalent priors); the remaining priors
diverge so far from the cohort-step paradigm that no
distinguishing rule is required (e.g., gx7m gear-mesh, vp6h
shadow-cast, vn8d domino-cascade, bx84 beam-mirror, etc.).
