# Spec — hr8q

## 1. Title
Pair-Blend Recipe (working title; not visible in-game).

## 2. Mechanic family
`pair-blend-recipe` — the player clicks two (and at L3, three)
ingredient blocks in turn to fill the input slots of a formula
widget; the formula auto-displays the resulting colour by looking
up the unordered colour set against the level's mix table; a
separate commit verb either consumes the matching target (when
the result matches) or "distils" the result into a new
intermediate ingredient added to the palette (when it does not).
Difficulty grows by adding the *intermediate-as-ingredient*
mechanic (chained recipes) and then a *three-input formula*
mechanic (triple-arity commits) that strictly requires both
earlier mechanics to chain into.

Prior categories (per `core-knowledge-priors.md`):
- **Objectness** — ingredients, slots, target chip and distilled
  intermediates are persistent, coherent click-targets.
- **Basic geometry / topology** — the spatial relationship
  `[slot1][slot2]→[result]` (and at L3 `[slot1][slot2][slot3]
  →[result]`) IS the discoverable syntax of the formula. The
  mix-table HUD strip uses the same `[A][B][C]` (or `[A][B][C]
  [D]`) topology to communicate each rule. Slot count = recipe
  arity is a topological invariant the player learns by sight.

## 3. Sprite roster

(Coordinates are sample positions; final positions are picked in
the implementation phase. Palette values per `global/color-legend.md`.
The grid is the default 64×64 — no camera resize.)

- **`ingredient_block`** — 6×6 filled square, palette colour
  parameterised at clone time via `color_remap`. Tags:
  `["ingredient", "primary"]` for primaries, or
  `["ingredient", "intermediate"]` for distilled intermediates.
  Role: clickable inventory item. Clicking copies its colour
  into the next empty formula slot. Primaries are uses=∞ (no
  visual indicator beyond the block itself). Intermediates are
  uses=1: after any commit (successful OR failed) consumes their
  slot occupancy, the intermediate sprite (and its pip) is
  removed via `InteractionMode.REMOVED`. Layer 2.

- **`ingredient_selected_ring`** — 8×8 hollow ring (1-pixel-thick,
  white = palette 0). Tags: `["selected_ring"]`. Role: overlay
  drawn around an ingredient currently filling at least one
  slot; toggled via `InteractionMode.INTANGIBLE` (visible) ↔
  `REMOVED` (hidden) per ingredient. Layer 4.

- **`intermediate_pip`** — 1×1 single-cell sprite (white =
  palette 0). Tags: `["pip", "intermediate_pip"]`. Role: drawn
  beneath an intermediate ingredient block to mark it as a
  one-shot palette item (visually distinguishes intermediates
  from primaries without text). One pip per intermediate;
  removed alongside the intermediate. Layer 3.

- **`slot_frame`** — 8×8 hollow square frame (1-pixel rim,
  off-black = palette 4). Tags: `["slot", "slot1"]` or
  `["slot", "slot2"]` or `["slot", "slot3"]` or
  `["slot", "result_slot"]`. Role: the visible empty-state of
  an input or result slot. `slot1` and `slot2` are visible at
  all levels; `slot3` is `set_interaction(REMOVED)` at L1 and
  L2 and `TANGIBLE` at L3 (so the third slot literally appears
  at L3). Layer 1.

- **`slot_fill`** — 6×6 filled square living at the inside of a
  slot frame; same width as `ingredient_block`. Tags: `["slot",
  "slot_fill", "slot1_fill"]` etc. Role: the colour currently
  occupying the slot (or `REMOVED` if slot empty). Cloned from a
  base block and `color_remap`ped to match the assigned colour.
  Layer 2.

- **`target_chip`** — 8×8 filled square framed by a 1-pixel
  off-black rim; the inner 6×6 is a remappable colour cell. Tags:
  `["target"]`. Role: shows the current queue head. Removed when
  consumed; the next queued chip slides into the same position.
  Layer 2.

- **`mix_rule_strip`** — a horizontal strip composed of three
  3×3 colour patches (or four, for triple-arity rules at L3)
  separated by 1-pixel off-black gaps: `[A][gap][B][gap][C]`
  for pair rules and `[A][gap][B][gap][C][gap][D]` for triple
  rules (where the final patch is the result). Each rule is one
  strip. Tags: `["mix_rule"]`. Role: visible mix-table HUD;
  permanent (no REMOVED state). Layer 1. (Built per-level by
  helper.)

- **`step_bar_hud`** — a `RenderableUserDisplay` widget (not a
  Sprite). Draws a 32-cell horizontal bar at row 0 indicating
  `(max_steps - steps_used) / max_steps` filled with palette 0
  on background palette 4. (Pattern from qb84/qz73.)

- **`divider_strip`** — a 1×46 vertical line at x≈31 (off-black =
  palette 4). Tags: `["decor"]`. Role: visual separator between
  formula/target panel and palette panel. Layer 1.

(All sprites use only palette values 0..15 and `-1` for transparent
pixels in hollow rings/frames. No glyphs, no letters, no digits.
The slot-positioning topology, the chip-frame topology, and the
ring-overlay topology are the only "symbols" — none of them
encode language or cultural conventions.)

## 4. Level progression, mechanic enumeration, and witness solutions

Grid size: `(64, 64)` for all three levels (default camera, no
resize). Step budgets are generous over the witness length.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N=1):
  1. **pair-blend-and-commit** — clicking two ingredient blocks
     fills the two formula slots; ACTION5 commits the formula,
     evaluating the unordered pair against the level's mix table;
     if the result matches the current target, the target is
     consumed and the level advances.

- **Necessity per mechanic**: Without pair-blend-and-commit there
  is no way to remove the target. The only legal action sequence
  that reaches `_check_win()` is two ingredient clicks followed by
  ACTION5; removing any of those three steps leaves the target
  un-consumed.

- **Witness solution** (3 actions):
  1. `ACTION6@(54, 16)` — click `ingredient_block(magenta=6)`.
  2. `ACTION6@(54, 28)` — click `ingredient_block(light-blue=10)`.
  3. `ACTION5` — commit; result = `purple=15` matches target;
     next-level fires.

  Inventory at L1: magenta (uses=∞), light-blue (uses=∞). Mix
  table: `{(magenta, light-blue) → purple}`. Target queue:
  `[purple]`. Step budget: 30.

- **Difficulty justification**:
  - **(a) Random-resistance**: a random policy emits any of {click
    one of two cells} ∪ {ACTION5}. The level is winnable in 3 of
    27 random 3-action sequences, but the agent does not know to
    stop at 3 actions; over a 30-action budget, random wins ~10%
    of the time. This is acceptable — L1 is a tutorial whose
    explicit job is to be soluble by random play (per
    `from-tech-report.md` §6).
  - **(b) Human time**: ~30 seconds. The player reads the screen,
    spots the target colour, recognises the only two clickable
    blocks, clicks both, sees the result match, presses ACTION5.
  - **(c) Planning depth**: near zero — the L1 difficulty is
    *mechanic discovery*, not planning. (Allowed per
    `difficulty-rules.md` §c L1.)
  - **(d) Step budget**: 30. Witness is 3; budget is 10× witness.
    Generous, not shrinking — the next levels' budgets are larger
    in step count to reflect their richer witnesses.

### Level 2 — base system + one new mechanic

- **Mechanics required by the witness** (N+1=2):
  1. **pair-blend-and-commit** (carried forward).
  2. **intermediate-as-ingredient** (NEW): a commit whose result
     does NOT match the current target distils the result into a
     new ingredient block appended to the palette (with `uses=1`).
     Subsequent clicks can use that intermediate exactly like a
     primary ingredient.

- **Necessity per mechanic**: The L2 target is `maroon=13`, only
  reachable via the chain `(magenta, light-blue) → purple` (no
  match → distilled), then `(purple, pink) → maroon` (match →
  target consumed). Pair-blend-and-commit alone does not produce
  maroon directly because no `(primary, primary) → maroon` rule
  exists — the player MUST distil the intermediate via the new
  mechanic before chain step 2. Removing intermediate-as-ingredient
  ⇒ unsolvable; removing pair-blend-and-commit ⇒ no commits
  possible at all ⇒ unsolvable. Both required.

- **Witness solution** (6 actions):
  1. `ACTION6@(54, 16)` — click magenta.
  2. `ACTION6@(54, 28)` — click light-blue.
  3. `ACTION5` — commit; result = `purple=15`; mismatch with target
     `maroon=13`; **purple appended to palette as intermediate
     (uses=1)**.
  4. `ACTION6@(54, 40)` — click purple (the new intermediate).
  5. `ACTION6@(54, 52)` — click pink.
  6. `ACTION5` — commit; result = `maroon=13`; matches target;
     win.

  Inventory at L2: magenta (∞), light-blue (∞), pink (∞). Mix
  table: `{(magenta, light-blue) → purple, (purple, pink) →
  maroon}`. Target queue: `[maroon]`. Step budget: 50.

- **Difficulty justification**:
  - **(a) Random-resistance**: with 3 primary ingredients + an
    eventual intermediate, action space ≈ 4-5 click cells + commit
    = 5-6 verbs. Six-action solutions of the form click-click-
    commit-click-click-commit are 1 in ~6^6 ≈ 1/46k random
    sequences; well under the §3.5 1/10k threshold. Spam-commit
    or click-only policies make zero progress because no `(primary,
    primary) → maroon` recipe exists.
  - **(b) Human time**: ~1.5 minutes. The player reads the mix-
    table HUD, sees `(M, LB) → purple` and `(purple, pink) →
    maroon`, plans the chain, executes.
  - **(c) Planning depth — non-trivial multi-step reasoning,
    per-step chain named**:
    *Step 1*: read target = maroon. Scan mix-table HUD; the only
      rule producing maroon is `(purple, pink) → maroon`. Note
      that purple is NOT a primary ingredient — must be made.
    *Step 2*: scan mix-table for rules producing purple. Find
      `(magenta, light-blue) → purple`. Plan the two-commit chain.
    *Step 3*: execute chain step 1 (clk_M, clk_LB, commit). Verify
      purple appears as an intermediate in the palette.
    *Step 4*: execute chain step 2 (clk_purple, clk_pink, commit).
      Verify result = maroon BEFORE committing (the result slot
      auto-displays after the second click).
    Reasoning at each commit decision references both the current
    state (which intermediates exist) AND the future state (will
    this commit produce maroon, or do I need to make a different
    intermediate first?). This is the "state + future state"
    reasoning required per `difficulty-rules.md` §c L2.
    Single-step wins are impossible: there is no recipe taking two
    primary ingredients directly to maroon, so no `[click, click,
    commit]` sequence wins. Spam-the-new-verb fails: ACTION5 with
    empty/single-filled formula is no-op. 1-action lookup tables
    fail: every winning play requires at least two commits.
  - **(d) Step budget**: 50. Witness is 6; budget is 8× witness.
    A first-time player will spend several actions exploring (try
    `(magenta, pink)` and find no recipe — costs 3 actions; try
    `(light-blue, pink)` likewise) before settling on the chain.
    Budget reflects that exploration cost, per L2 addendum in
    `difficulty-rules.md` §d.

### Level 3 — system + one more new mechanic

- **Mechanics required by the witness** (N+2=3):
  1. **pair-blend-and-commit** (carried forward).
  2. **intermediate-as-ingredient** (carried forward).
  3. **three-input formula** (NEW): the formula widget gains a
     visible third input slot at L3 (at L1 and L2 only slots 1
     and 2 are visible; the slot3 sprite is `REMOVED`). When all
     three slots are filled, ACTION5 commit evaluates the
     **unordered triple** of slot colours against the level's
     `triple_mix_table`. (Two-slot commits still fire the L1/L2
     pair recipe when only slots 1 and 2 are filled.) Visually,
     the third slot sits to the right of the second, completing
     a horizontal `[1][2][3]` row above the result slot.

- **Necessity per mechanic**:
  - **pair-blend-and-commit** required: every commit is a
    blend-and-commit. Removing this primitive makes commits
    impossible ⇒ no targets can be consumed ⇒ unsolvable.
  - **intermediate-as-ingredient** required: the L3 target is
    `blue=9` and the only triple recipe producing blue at L3 is
    `(purple, pink, yellow) → blue`. `purple=15` is NOT a
    primary ingredient at L3 — it must be DISTILLED via the
    pair recipe `(magenta, light-blue) → purple` whose result
    does not match the target and is therefore promoted to a
    palette intermediate by the L2 mechanic. Removing
    intermediate-as-ingredient ⇒ no purple available ⇒ triple
    recipe cannot fire ⇒ unsolvable.
  - **three-input formula** (NEW) required: removing the third
    slot leaves only pair commits available; no pair recipe at
    L3 produces blue (the pair-mix-table maps `(M, LB) → purple`
    only). Without the triple commit there is **no** action
    sequence in `[5, 6]` that produces blue. Strict necessity ⇒
    unsolvable without three-input. ✓ (`checklist.md` 10a.)

- **Witness solution** (7 actions):

  Inventory at L3: magenta, light-blue, pink, yellow — all
  primary, uses=∞ (no pip). One distillable intermediate
  (purple) emerges mid-witness with uses=1.

  Mix tables:
  - **pair_mix_table**: `{(magenta, light-blue) → purple}`
    (single pair recipe, carried in spirit from L1's family).
  - **triple_mix_table**:
    - `(purple, pink, yellow) → blue`         — produces target.
    - `(magenta, light-blue, yellow) → green` — DECOY: a triple
      recipe whose result is green, not the target. Discovering
      it costs 4 actions but does not progress the puzzle, and
      consumes the magenta+light-blue+yellow slot occupancy
      (recoverable since primaries are unlimited). Decoy is a
      negative example for the planning chain.

  Target: `blue=9`. Target queue: `[blue]` (single target).
  Step budget: 60.

  Witness:
  1. `ACTION6@(50, 12)` — click magenta. slot1=magenta.
  2. `ACTION6@(50, 22)` — click light-blue. slot2=light-blue.
     Slot3 still empty. Result preview = pair recipe → purple.
  3. `ACTION5` — commit. 2 slots filled ⇒ 2-input recipe fires.
     Result=purple ≠ target=blue → **purple distilled as a
     palette intermediate (uses=1)**. Slots clear.
  4. `ACTION6@(50, 32)` — click purple intermediate. slot1=purple.
  5. `ACTION6@(50, 42)` — click pink. slot2=pink.
  6. `ACTION6@(50, 52)` — click yellow. slot3=yellow.
     Result preview = triple recipe → blue.
  7. `ACTION5` — commit. 3 slots filled ⇒ 3-input recipe fires.
     Result=blue=target → target consumed; queue empty; win.

- **Difficulty justification**:
  - **(a) Random-resistance**: action space at L3 has ≥4 primary
    click cells (magenta, light-blue, pink, yellow) plus the
    transient purple cell + slot-clear cells + ACTION5. A
    7-action specific sequence has prior <1/7^7 ≈ 1/8×10^5; well
    under the §3.5 1/10k threshold. Spam-commit fails: ACTION5
    with 0 or 1 slots filled is a no-op. Spam-click without
    eventual commits cycles slot fills indefinitely without
    consuming a target. Vision-blind LLMs cannot read the
    mix-table HUD and cannot deduce the triple recipe.
  - **(b) Human time**: ~3 minutes. With L1 (~30s) and L2 (~1.5
    min) the environment lands ~5 minutes — within
    `difficulty-rules.md` §b's "around 6 minutes" target.
  - **(c) Planning depth — strictly deeper than L2**:

    *Trivial heuristic that fails*: **"two-slot heuristic"** —
    a player who has internalised L2's `[click, click, commit]`
    pair-blend pattern and never tries the third slot will be
    permanently unable to produce blue. There is no
    `(primary_a, primary_b) → blue` rule and no
    `(intermediate_a, intermediate_b) → blue` rule — the only
    blue recipe is the triple recipe. A player ignoring the
    visibly-present third slot exhausts the budget without
    progress. The witness defeats this heuristic by deliberately
    moving from a 2-slot commit (chain step 1, distilling
    purple) to a 3-slot commit (chain step 2, producing blue) —
    each commit using a DIFFERENT slot count.

    *Decoy recipe*: a "triple-recipe seeker" player who tries
    the wrong triple `(magenta, light-blue, yellow) → green`
    discovers a non-target output. This is a soft trap (no
    permanent damage since primaries are unlimited) but it
    extends the player's time and reinforces that not every
    triple is the answer. A player who decoys once and then
    plans correctly still wins comfortably in budget.

    *Adjacent witness-pair commute test*: swap actions 6 and 7,
    i.e. `[ACTION6 click yellow, ACTION5 commit]` →
    `[ACTION5 commit, ACTION6 click yellow]`. After action 5
    (clk_pink), slots = `[purple, pink, _]` — slot3 is empty.
    Swapped action 6 is now `ACTION5 commit`: 2 slots filled
    ⇒ pair recipe fires for `(purple, pink)`. `(purple, pink)`
    is NOT in the pair_mix_table (which only contains `(M, LB)
    → purple`). The commit is a failed-recipe commit: slots
    clear, AND **the purple intermediate (which had been clicked
    into slot1) is consumed by the commit** (any commit consumes
    the slot occupants — a uniform engine rule the player learns
    in L2 from the success path; the L3 introduction of triples
    does not soften it). Swapped action 7 is `clk_Y` — slot1
    becomes Y, slots = `[Y, _, _]`. The witness's path to blue
    has been broken: purple is gone, the 7-action witness no
    longer wins. Recovery would require redoing the full chain
    from action 1 (re-distil purple, re-fill slots, commit
    triple) — at minimum 7 additional actions for a total of
    13 — and the original "shortest witness" property is
    destroyed. Hence swapping these two adjacent witness actions
    strictly breaks **this** solution; the player must invent a
    longer one. (Whether a longer one fits in the 60-step
    budget is yes, but that is a different solution, not the
    witness.)

    Per-step reasoning chain (L3, condensed): "look at target →
    note no pair recipe produces it → spot the third slot is
    visible (NEW at L3) → look up triple recipes → identify
    `(purple, pink, yellow) → blue` → note purple is not a
    primary → recall L2's distil-via-mismatch behaviour → plan
    chain: pair-commit (M, LB) to distil purple, then triple-
    commit (purple, pink, yellow) → execute". This references
    both current state (which slots and ingredients exist NOW)
    and future state (after the pair-commit, will purple be in
    the palette to pick up?). Going *beyond* L2 by integrating
    a fundamentally new commit-arity mechanic into the L1/L2
    chain plan.

  - **(d) Step budget**: 60. Witness is 7; budget is ~8.5×
    witness. Generous, NOT shrinking from L2's 50 — L3 has more
    discovery cost (a fourth primary ingredient, a third visible
    slot to recognise as interactive, a triple mix-table HUD
    strip section to read, a decoy triple recipe to identify
    and reject). Per `difficulty-rules.md` §d L3.

## 5. Action mapping

`available_actions = [5, 6]`.

- **ACTION5 — Commit**.
  - Determine commit arity by counting filled slots among the
    visible slots (slot1 and slot2 always visible; slot3 visible
    only at L3).
  - **Pair commit (2 slots filled, slot3 empty or hidden)**: look
    up unordered pair in `pair_mix_table`. If found:
    - result == current target → target consumed (queue head
      popped); slots clear; intermediates in slots removed.
    - result ≠ current target → result distilled into a new
      intermediate block (`uses=1`) appended to the palette;
      slots clear; ANY intermediate in the slots is removed
      (consumed by the commit).
    - pair not in mix table → slots clear; intermediates in
      slots removed (failed commit consumes intermediates too —
      a uniform engine rule).
  - **Triple commit (all 3 slots filled, L3 only)**: look up
    unordered triple in `triple_mix_table`. Same three-way
    handling as pair commit (match → consume target;
    mismatch-but-valid → distil; not in table → discard).
  - **Insufficient slots filled** (0 or 1): no-op for state, but
    the action still consumes a step.
  - Primary ingredients are NOT depleted by any commit (uses=∞
    throughout). Intermediates are single-use and disappear after
    being slotted into a commit (see `ingredient_block` sprite
    role in §3).

- **ACTION6 — Click at `(x, y)`** (pixel coords; converted via
  `camera.display_to_grid`).
  - Hit-test (in priority order):
    1. **An ingredient block** (primary OR intermediate): if at
       least one slot is empty, fill the lowest-numbered empty
       slot with this block's colour AND add the matching
       `slot_fill` sprite at the slot; toggle the block's
       `selected_ring` to INTANGIBLE (visible) iff its colour is
       in any slot. If all slots are already full (2 at L1/L2, 3
       at L3), the click is a no-op for state but still costs a
       step.
    2. **A slot frame** (slot1, slot2, or slot3 at L3): clear
       that slot (remove its `slot_fill`). If the slot held an
       intermediate's colour and that intermediate is no longer
       in any slot, the intermediate stays in the palette
       (clearing the slot does NOT consume the intermediate; only
       commits do).
    3. **The result slot frame**: no-op.
    4. **Anywhere else** (including the divider, the mix-table
       HUD, the target chip, the step bar): no-op.

## 6. HUD and per-game state

**HUD widgets** (`RenderableUserDisplay` subclasses):

- `StepBarHud` — horizontal bar at row 0, x=8..56; fill=palette 0
  on background palette 4; tracks `(max_steps - steps_used)`.
  Pattern from qb84/qz73.

- `MixTableHud` — draws the level's `mix_rule_strip` sprites at
  fixed bottom positions (rows 50-58). Each rule is rendered as
  `[A][gap][B][gap][C]` with `A` and `B` the two ingredient
  colours (3×3 patches) and `C` the result colour. The
  permanent visibility of this HUD is what makes the recipe
  rules learnable from the rendered frame alone — satisfying
  the "no instructions" principle (`from-tech-report.md` §4)
  without text.

- `ResultDisplayHud` — draws the auto-evaluated result (if both
  slots are filled and the pair has a recipe) inside the result-
  slot region. Reads `self._current_result_color` from the game
  instance. If only one slot or zero slots are filled, the result
  region is empty (background colour).

**Per-game internal state**:
- `self.ingredients: list[IngredientHandle]` where each
  `IngredientHandle` ties together: the `ingredient_block` sprite,
  its `selected_ring` sprite, its optional `intermediate_pip`
  sprite, its kind (`"primary"` / `"intermediate"`), and its
  `uses_remaining` (∞ for primaries, 1 for intermediates).
- `self.pair_mix_table: dict[frozenset[int], int]` — unordered
  pair → output colour.
- `self.triple_mix_table: dict[frozenset[int], int]` — unordered
  triple → output colour. Empty at L1 and L2; populated at L3.
- `self.target_queue: list[int]` — colour values for each target
  in queue order. (L1, L2, L3 each use a single-element queue in
  this design, but the queue abstraction is shared so future
  variants can use longer queues without engine changes.)
- `self.target_chip: Sprite | None` — display-side chip showing
  the current queue head; removed on consumption and replaced if
  another target is queued.
- `self.slot_colors: list[int | None]` of length 3
  (slot3 always None at L1/L2).
- `self.slot_fills: list[Sprite | None]` of length 3.
- `self.steps_used: int`, `self.max_steps: int`.
- `self.current_result_color: int | None` — recomputed on every
  slot mutation; consumed by `ResultDisplayHud`. Computation:
  count filled slots; if 2 (and L1/L2/L3 all support pair) look
  up `pair_mix_table[frozenset]`; if 3 (L3 only) look up
  `triple_mix_table[frozenset]`; else `None`.

## 7. Win condition

`self.next_level()` fires (and ultimately `self.win()` on the
final level) when `len(self.target_queue) == 0`. Concretely, in
`step()`, after a successful commit pops the queue head, check
`if not self.target_queue: self.next_level(); self.complete_action();
return`.

## 8. Lose condition

`self.lose()` fires when `self.steps_used >= self.max_steps` AND
`len(self.target_queue) > 0`. There is no other lose path — the
player cannot lock themselves out by exhausting inventory because
the engine does not detect "no remaining feasible witness"; they
simply spend their budget without progress. (At L3 the trap
recipe and the asymmetric inventory are designed to FORCE such
budget exhaustion as the failure mode for sub-optimal play.)

## 9. Novelty note

Closest entries in `mechanic-novelty/taxonomy-of-25-games.md`:

- **sb26 — tile-place-commit** (Mastermind-style guess board with
  per-slot hint feedback). Concrete distinguishing rule: sb26 is
  a hidden-sequence guessing game where each commit produces
  feedback that narrows the search space; the player iterates
  many commits until the hidden code is found. hr8q has NO hidden
  information: the mix table is fully visible at all times, the
  result slot auto-evaluates before commit so the player sees the
  outcome BEFORE committing, and the puzzle is constructive
  (build the right output) rather than searchful (find the
  hidden code). The verb on ACTION5 is also semantically
  different — sb26's commit reveals feedback; hr8q's commit
  consumes a target or distils an intermediate.

- **su15 — recipe-fruit-collect** (collect numbered + flavoured
  fruits with patrolling enemies). Concrete distinguishing rule:
  su15 is a spatial radial-blast game on a 16×14 cell arena with
  movement, line-of-sight, and enemy collisions. hr8q has zero
  spatial gameplay — no avatar, no arena, no enemies, no
  line-of-sight. The "recipe" notion in su15 is *count per
  flavour* (collect N of colour X); in hr8q it is *unordered
  pair → output colour* under a fixed lookup table.

- **tn36 — program-pawn-trace** (compose a click-sequence of
  move-and-rotate instructions; run programme; trace must match
  target). Concrete distinguishing rule: tn36's composed object
  is a *spatial path on a canvas*; hr8q's composed object is a
  single output colour with no spatial extent. tn36 has a pawn
  and a runway; hr8q has neither.

Closest entry in `prior-games/index.md`:

- **gv47 — seed-grow-surround-dissolve** (region-grow + global
  contact-mix on a 12×12 spatial canvas). This is the
  load-bearing novelty hazard — gv47 also implements a colour
  mix-table primitive. Concrete distinguishing rule (see
  `mechanic-pick.md` for the full eight-dimension walkthrough):
  gv47 is *spatial coverage planning under a contact-graph mix
  rule* — clicking grows connected regions; ACTION5 fires a
  GLOBAL contact-graph fusion across all currently-touching
  regions; the win condition is "every black-ringed pip cell
  is surrounded by paint of its own colour." hr8q has NO spatial
  canvas, NO regions, NO adjacency / contact graph, NO
  surround-dissolve predicate. ACTION5 in hr8q operates on a
  fixed 2-input formula widget, not on the playfield. The win
  condition is "every queued target colour has been produced via
  a matching commit", which references no spatial cells at all.
  The shared atom is "two colours combine into one"; everything
  surrounding that atom (interface, verb topology, win condition,
  failure mode, planning category) diverges.

The negative similarity check (8-dimension overlap walkthrough)
against gv47 is documented in detail in `mechanic-pick.md`;
overlap = 1/8 (only the universal step-counter axis). Threshold
for rejection is 3+. PASS.

Other prior-games rows (kf42 tether-pawn-cycle, qz73 radial-
cycle-lock, kx14 tide-tilt-buoyant, qb84 bead-lift-swap-sequence,
lq5x lantern-cone-illuminate) share at most 1-2 surface
dimensions with hr8q (typically just the step-counter HUD), well
under the rejection threshold; none implements anything close to
a recipe-driven formula widget.

`prior-games/index.md` is non-empty and was checked row-by-row.
