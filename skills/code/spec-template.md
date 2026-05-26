# Spec template (for `write_spec`)

Every spec MUST contain these 9 subsections in order. The
`critique_spec` state checks each subsection independently.
Section 4 is the load-bearing one for items 11 (mechanic
inheritance / +1-or-+2 per level), 12 (strict counterfactual
necessity / no trivial fallback), 13 (minimum-action witness —
no one-action or repetitive passes), and 19 (difficulty floor
and ceiling).

```markdown
## 1. Title
A neutral working title (NOT visible in-game; for human reference
only). E.g. "Reflection-Symmetry Puzzle".

## 2. Mechanic family
A 1-2 sentence description of the core mechanic (drawing from
`design-constraints/core-knowledge-priors.md`). Specify which prior
categories are used.

## 3. Sprite roster
A bulleted list. For each sprite:
- name (meaningful semantic name, e.g. `lantern`, `target_yellow`,
  `wax_pickup`. The reference games use obfuscated random tokens
  for crack-proofing; our generated games do not — see
  `code/universal-scaffold.md` § Style rules.)
- pixel matrix dimensions
- palette values used
- runtime tags
- one-line role (e.g. "player; movable; collides with walls")

Roles can be semantic — they are author-side labels, not in-game
language.

## 4. Level progression, mechanic enumeration, and witness solutions
EXACTLY 3 levels. For EACH level, fill in three subsections — the
data here is what `critique_spec` checks items 11 (mechanic
inheritance / +1-or-+2 per level), 12 (strict counterfactual
necessity), 13 (minimum-action witness — no one-action or
repetitive passes), 19 (difficulty floor and ceiling), 24
(animation for non-local effects), 25 (lives mechanism for
hard-death), and 26 (mechanic adds a new rule, not a new map)
against.

The level structure (L1 = base system, L2 = +1 or +2 new
mechanics, L3 = +1 or +2 more) is defined in
`design-constraints/composition-and-tutorial.md`. The per-level
*Difficulty justification* sub-bullets are defined in
`design-constraints/difficulty-rules.md` § 2.

### Level 1 — base dynamic system
- **Mechanics required by the witness** (let N ≥ 1): list each
  mechanic (verb + rule) needed to solve L1. A single mechanic is
  fine; a small system of 2-3 interacting mechanics is also fine.
  Every mechanic listed here MUST be exercised by the witness
  solution below — no hidden mechanics.
- **Necessity per mechanic** (counterfactual, per checklist
  item 12): for each listed mechanic M, state in 1 line —
  *"L1 cannot be solved without triggering M because [name the
  specific cell, sprite, or rule that blocks every alternate
  path]."* If you can't finish that sentence concretely, M
  isn't necessary at this level — remove M or change the level.
- **Witness solution**: the SHORTEST action sequence that wins L1,
  written out action by action. For ACTION6, include the click
  coordinate. Example: `[ACTION5, ACTION6@(32, 47), ACTION5]`.
  State K = witness length and D = count of distinct actions
  (per checklist item 13): K ≥ 3 and D ≥ 2 required.
- **Animation plan** (per checklist item 24): if any mechanic in
  this level produces non-local effects in a single tick
  (teleport, slide-until-wall, projectile, chain reaction,
  multi-entity propagation), describe the per-frame animation
  (N ticks, K cells per tick, trail / fade, etc.) concretely
  enough to implement. Write "N/A — no non-local effects" if
  not applicable.
- **Lives mechanism** (per checklist item 25): if this level
  has any hard-death path (single action immediately triggers
  `self.lose()` — hazard, fail-state tile, NPC contact,
  soft-lock), state the hard-death trigger(s), chosen initial
  lives count with a one-line rationale (enough for a human
  player to learn the death rule by observation), respawn
  semantics (level resets to initial state, avatar respawns at
  start), and visual cue for remaining lives. Write
  "N/A — no hard-death" if not applicable (energy depletion
  alone is exempt).
- **Difficulty justification**: fill in the four bullets
  (a) random-resistance, (b) human-tractable, (c) planning depth,
  (d) step budget — per `difficulty-rules.md` § 2 (apply L1's
  per-level guidance under each).

### Level 2 — base system + 1 or 2 new mechanics
- **Mechanics required by the witness** (= N+1 OR N+2): list
  every L1 mechanic (carried forward) PLUS one or two new
  mechanics. Every mechanic listed MUST be exercised by the
  witness — no hidden mechanics, and no L1 mechanic may drop
  out. State explicitly whether L2 introduces 1 or 2 new
  mechanics; both are allowed but not 0 and not ≥ 3. For each
  newly-introduced mechanic, state in 1 line the new rule the
  player learns at L2 — in player-facing language (per
  checklist item 26: a new arrangement of existing
  cells/sprites is layout, not a mechanic).
- **Necessity per mechanic** (counterfactual, per checklist
  item 12): one 1-line counterfactual sentence for *each*
  mechanic listed above (carried-forward + newly-introduced).
  Format: *"L2 cannot be solved without triggering M because
  [concrete cell/sprite/rule that blocks every alternate
  path]."* Every L1 mechanic AND every L2-new mechanic gets
  its own line; no hand-waved "as L1" — restate per mechanic
  because L2's geometry differs and so does what blocks the
  alternate path.
- **Witness solution**: the SHORTEST action sequence that wins L2.
  State K and D per checklist item 13 (K ≥ 3, D ≥ 2).
- **Animation plan** (per checklist item 24): per-frame animation
  for any non-local effect introduced or carried into L2. Write
  "N/A — no non-local effects" if not applicable.
- **Lives mechanism** (per checklist item 25): if this level has
  any hard-death path, state trigger / chosen initial lives count
  with a one-line rationale / respawn semantics / visual cue.
  Write "N/A — no hard-death" if not applicable.
- **Difficulty justification**: fill in the four bullets per
  `difficulty-rules.md` § 2 (apply L2's per-level guidance — note
  in particular that L2 requires moderate post-discovery planning
  with the per-step reasoning chain named and the plausible wrong
  action paths identified).

### Level 3 — system + 1 or 2 more new mechanics
- **Mechanics required by the witness** (= L2-count + 1 OR
  L2-count + 2): every L2 mechanic (which already includes
  every L1 mechanic) PLUS one or two further new mechanics.
  All listed mechanics MUST be exercised by the witness.
  State explicitly whether L3 introduces 1 or 2 new mechanics;
  both are allowed but not 0 and not ≥ 3. For each newly-
  introduced mechanic, state in 1 line the new rule the
  player learns at L3 — in player-facing language (per
  checklist item 26: a new arrangement of existing
  cells/sprites is layout, not a mechanic).
- **Necessity per mechanic** (counterfactual, per checklist
  item 12): one 1-line counterfactual sentence for *each*
  mechanic listed above (every L1 + L2 carried-forward + L3-new).
  Format: *"L3 cannot be solved without triggering M because
  [concrete cell/sprite/rule that blocks every alternate
  path]."* No "as L1/L2" — restate per mechanic at L3 because
  the geometry differs and so does what blocks the alternate
  path.
- **Witness solution**: the SHORTEST action sequence that wins L3.
  State K and D per checklist item 13 (K ≥ 3, D ≥ 2).
- **Animation plan** (per checklist item 24): per-frame animation
  for any non-local effect introduced or carried into L3. Write
  "N/A — no non-local effects" if not applicable.
- **Lives mechanism** (per checklist item 25): if this level has
  any hard-death path, state trigger / chosen initial lives count
  with a one-line rationale / respawn semantics / visual cue.
  Write "N/A — no hard-death" if not applicable.
- **Difficulty justification**: fill in the four bullets per
  `difficulty-rules.md` § 2 (apply L3's per-level guidance — note
  in particular that L3's planning should be a little challenging
  even for an attentive human, with a named trivial heuristic
  that fails and a brief argument for why ahead-of-time reasoning
  is needed).

Reusing the same `grid_size` and sprite set across the 3 levels
is fine, but each level's configuration (sprite positions, level
data, constraints) must vary.

## 5. Action mapping
The subset of `[1..7]` used. For each, specify:
- `ACTION_<n>`: <semantic, e.g. "MOVE UP"; or "CLICK at (x, y)" for
  ACTION6>.
- Any context-dependent gating (e.g. "ACTION5 only valid when a
  sprite is selected").

## 6. HUD and per-game state
What the player sees beyond the playfield (e.g. step counter,
energy bar, target indicator). Specify the
`RenderableUserDisplay` subclass(es) needed.

What internal state the game maintains across actions (e.g.
selected-sprite handle, accumulated rotations, captured tiles).

## 7. Win condition
Concrete, testable predicate that triggers `self.next_level()`.
Must be true-ish for ALL levels, not just level 1.

## 8. Lose condition
Concrete predicate that triggers `self.lose()`. May be "no
explicit lose; player can always reset" if no lose state exists.

## 9. Novelty note
- Cite the entries in `mechanic-novelty/taxonomy-of-25-games.md`
  the proposed mechanic is closest to. Articulate the concrete
  distinguishing rule (NOT just "it's different").
- Cite any entries in `prior-games/index.md` that are close. Do
  the same.
- If `prior-games/index.md` is empty (first run), say so
  explicitly.
```
