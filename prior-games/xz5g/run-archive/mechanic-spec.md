# Game spec — xz5g

> **Revision history**
> - Visit #03: initial draft.
> - Visit #05: addressed critique-revisions.md issues 1 (M4
>   redefined as visit-checkpoint), 2 (L2 random-resistance
>   prose tightened), 3 (sprite pixel matrices specified
>   explicitly), 4 (L3 direction_indicator discovery path
>   narrated).

## 1. Title

**Pivot-and-Spin** (working title; not visible in-game).

## 2. Mechanic family

**arena-pivot-rotate**. Core knowledge priors used: §3.4 categories
**objectness** (sprites are persistent entities with positions) and
**basic geometry & topology** (rotation around an arbitrary point;
the central transformation `(x, y) → (px + py − y, py + x − px)` for
CW or `(x, y) → (px − py + y, px + py − x)` for CCW). The player has
no direct movement verb — instead, the entire playfield's rotatable
contents are repositioned by 90° rotations around a player-chosen
pivot cell.

## 3. Sprite roster

- **`avatar`** — 6×6 pawn (filled, palette 9 = blue body with
  palette 4 = dark frame and palette 0 = white interior pips).
  Pixel matrix:
  ```
  [4, 9, 9, 9, 9, 4]
  [9, 0, 9, 9, 0, 9]
  [9, 9, 9, 9, 9, 9]
  [9, 9, 9, 9, 9, 9]
  [9, 0, 9, 9, 0, 9]
  [4, 9, 9, 9, 9, 4]
  ```
  Solid blue body framed by 4 dark corner-pips and 4 interior
  white pips at columns 1, 4 of rows 1, 4. The 4-pip pattern
  is rotationally NON-symmetric in the small ways: rotating
  90° CW vs 0° produces visibly different pip positions
  relative to the body's outer frame, so the player reads
  rotation as a visual change of pip-corner alignment.
  Tags: `["rotatable", "avatar"]`. Collidable True, visible.
  Rotation-aware (sprite's pixel matrix rotates with each
  ACTION5). Role: the player's primary identity-pawn.
- **`avatar_target`** — 6×6 hollow ring (matched to avatar
  footprint, transparent centre). Pixel matrix:
  ```
  [4, 9, 9, 9, 9, 4]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [9, -1, -1, -1, -1, 9]
  [4, 9, 9, 9, 9, 4]
  ```
  Same outer 1-px frame palette 9 / corner-pip palette 4 as
  the avatar — the colour-and-frame match is the *role
  correlation* cue (per checklist 21: identical-visuals →
  correlated-roles). The 4×4 transparent centre is the
  *role distinction* — it reads as "slot/cup" vs the avatar's
  filled body. When the avatar overlays its target the white
  pips show through the transparent centre, so the player
  sees the slot is "filled".
  Tags: `["target", "avatar_target"]`. Collidable False,
  visible. Role: the cell the avatar must end on; size-matched
  to avatar so win = exact top-left coincidence.
- **`companion`** — 6×6 pawn (palette 12 = orange body, palette
  4 = dark frame, palette 0 = white interior pips). Pixel matrix:
  ```
  [4, 12, 12, 12, 12, 4]
  [12, 0, 12, 12, 0, 12]
  [12, 12, 12, 12, 12, 12]
  [12, 12, 12, 12, 12, 12]
  [12, 0, 12, 12, 0, 12]
  [4, 12, 12, 12, 12, 4]
  ```
  Identical structure to the avatar — same corner-pips +
  interior-white-pips — only the body palette changes (orange
  vs blue). This is intentional: avatar and companion share a
  visual *pawn family* and differ only by colour, exactly as
  checklist 21 prescribes for two same-role objects (both are
  "the rotatable pawn the player delivers to its same-coloured
  target"). Tags: `["rotatable", "companion"]`. Collidable
  True, visible. Rotation-aware. Role: the L2/L3 second
  rotatable pawn that must reach its own target.
- **`companion_target`** — 6×6 hollow ring (companion-footprint
  match, transparent centre). Pixel matrix:
  ```
  [4, 12, 12, 12, 12, 4]
  [12, -1, -1, -1, -1, 12]
  [12, -1, -1, -1, -1, 12]
  [12, -1, -1, -1, -1, 12]
  [12, -1, -1, -1, -1, 12]
  [4, 12, 12, 12, 12, 4]
  ```
  Symmetric counterpart to avatar_target with the orange
  palette. Tags: `["target", "companion_target"]`.
  Collidable False, visible. Role: where the companion must
  end. Color-matches the companion.
- **`anchor_pin`** — 4×4 fixed-stake sprite (visit-checkpoint).
  Pixel matrix (initial / unvisited state):
  ```
  [4, 4, 4, 4]
  [4, 14, 14, 4]
  [4, 14, 14, 4]
  [4, 4, 4, 4]
  ```
  Dark frame palette 4 + 2×2 green centre palette 14. The
  sprite reads as a stamped checkpoint / pad. Tags:
  `["anchor_pin", "visit_checkpoint"]`. Collidable False
  (rotatable sprites can land on it; that's the trigger),
  NON-rotatable (no `rotatable` tag — anchor_pin stays put
  through every rotation). Role: the L3-introduced
  visit-checkpoint that gates the win predicate. Every
  `anchor_pin` cell must be coincident with at least one
  `rotatable` sprite's top-left at some action's end-state
  during the level — the level does not advance until this
  is satisfied AND the per-target colour-match is satisfied.
  When a rotatable sprite first lands on the anchor_pin's
  top-left, the centre 2×2 flips palette 14 → palette 11
  (green → yellow) and stays flipped for the rest of the
  level (persistent "stamped" visual cue):
  ```
  [4, 4, 4, 4]
  [4, 11, 11, 4]
  [4, 11, 11, 4]
  [4, 4, 4, 4]
  ```
  This satisfies the no-hidden-state rule: the player can
  read off-screen at any moment whether the checkpoint has
  been visited.
- **`pivot_marker`** — 6×6 hollow halo. Pixels: outer ring palette
  7 (pink), 1-px inner ring palette 6 (magenta), centre palette
  -1. Tags: `["pivot_marker"]`. Collidable False, visible.
  Layer 5 (renders above everything). Role: the persistent
  visual cue showing where the pivot is currently set; one
  instance, repositioned each time the player clicks an empty
  cell. Stays present across rotations (does NOT rotate).
- **`direction_indicator`** — 4×4 widget. Pixels: a 4×4 square in
  palette 13 (maroon) with a single corner pip in palette 11
  (yellow); the pip is at top-right for CW and at top-left for
  CCW (asymmetric — no arrow glyph; the pip-corner indicates
  rotation handedness). Tags: `["direction_indicator"]`.
  Collidable False. Layer 5. Role: L3-only widget; clicking it
  toggles the next rotation's direction; the visible pip-corner
  flips so the player reads off current direction.
- **`step_bar`** — implemented as a `RenderableUserDisplay`
  subclass `StepCounterHud`, NOT a Sprite. Renders row 63 with
  a depleting bar (palette 6 = magenta filled, palette 4 = dark
  drained). Universal step-counter pattern.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. Grid size **(64, 64)** for all levels — no
sub-cell scaling. Background palette 1 (off-white); letter-box
palette 2 (light-grey).

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 2):
  - **M1: pivot-set** — clicking via ACTION6 on any empty cell
    places the pivot_marker at that cell.
  - **M2: commit-rotate** — ACTION5 commits a 90° CW rotation of
    every rotatable sprite around the marked pivot, and rotates
    each rotatable sprite's pixel matrix by 90° too.
- **Necessity per mechanic**:
  - **M1**: L1 cannot be solved without triggering M1 because
    until the player clicks somewhere, no `pivot_marker` exists
    and `_pivot is None`; any ACTION5 with `_pivot is None` is a
    no-op (consumes 1 step but no sprite moves). The avatar at
    (12, 32) cannot reach the target at (32, 12) without a
    rotation, so the pivot must be set first.
  - **M2**: L1 cannot be solved without triggering M2 because
    the only verb that moves the avatar is ACTION5; ACTION6 only
    sets the pivot and rotates nothing. With avatar fixed and no
    other verbs available, the only way to alter the avatar's
    position is ACTION5.
- **Witness solution** (2 actions):
  `[ACTION6@(32, 32), ACTION5]`. The click at display pixel (32,
  32) maps via `camera.display_to_grid` to grid (32, 32) (camera
  is 64×64, scale=1). The single CW rotation around (32, 32)
  maps avatar `(12, 32) → (32 + 32 − 32, 32 + 12 − 32) = (32, 12)`
  which is the avatar_target.
- **Layout**: avatar at (12, 32); avatar_target at (32, 12). No
  companion, no anchor_pin, no direction_indicator.
- **Difficulty justification**:
  - **(a) Random-resistance**: With `available_actions = [5, 6]`,
    a random policy chooses each per-turn 50/50; ACTION6 picks a
    uniform pixel in [0, 63]² (4096 cells). The 2-action witness
    has joint probability `(1/2 × 1/4096) × (1/2) = 1/16384` per
    aligned attempt. Within step budget 25, summed over all
    1-pivot-1-rotate sub-windows, total P(win) ≈ 25/16384 ≈
    1/655, qualifying as random-stumble-tolerant for the
    tutorial level (which is allowed per the report's "random
    agents can occasionally stumble into success at this stage,
    which is acceptable by design"). Spam-one-verb fails: ACTION5
    spam without ACTION6 is no-op forever; ACTION6 spam without
    ACTION5 never moves anything.
  - **(b) Human-tractable**: ~60 seconds. The player presses
    ACTION5 first, sees nothing happens, tries ACTION6 at random
    cells, eventually clicks the centre, sees the pivot_marker
    halo land there, presses ACTION5, watches the avatar swing
    onto the target. The aha-moment is "click sets the pivot;
    space rotates everything around it".
  - **(c) Planning depth**: **No strict planning requirement** —
    once the player understands pivot-and-rotate, finding the
    correct centre is one geometric judgement (the midpoint of
    the avatar-to-target arc).
  - **(d) Step budget**: 25.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (M = N + 1 = 3):
  - **M1: pivot-set** (carried; click sets `_pivot`).
  - **M2: commit-rotate** (carried; ACTION5 rotates).
  - **M3: companion-pawn-deliver (NEW)** — every `rotatable`
    sprite (avatar AND companion) transforms together under a
    single rotation; the win predicate now requires every
    `target`-tagged sprite to have its color-matched
    `rotatable`-tagged pawn co-located (avatar-on-avatar_target
    AND companion-on-companion_target).
- **Necessity per mechanic**:
  - **M1**: As L1 — without setting a pivot, no rotation moves
    anything; the win positions are unreachable from start.
  - **M2**: As L1 — ACTION5 is the only motion verb; without it,
    no sprite ever moves and the win positions are unreachable
    from start.
  - **M3**: L2 cannot be solved without triggering M3 because
    the win predicate AND-s `avatar_on_avatar_target` with
    `companion_on_companion_target`; even if the avatar reaches
    its target, the level does not advance until the companion
    also reaches its target; rotating the avatar without
    rotating the companion is impossible (M2 transforms ALL
    rotatable sprites in one step), so any winning sequence
    must deliver the companion as a forced side-effect of
    delivering the avatar — no "ignore the companion" path
    exists.
- **Witness solution** (3 actions):
  `[ACTION6@(32, 32), ACTION5, ACTION5]`. Two CW rotations around
  pivot (32, 32) using formula `CW(x, y) = (px+py−y, py+x−px)`:
  - Step 1: avatar `(8, 32) → (32+32−32, 32+8−32) = (32, 8)`;
    companion `(32, 8) → (32+32−8, 32+32−32) = (56, 32)`.
  - Step 2: avatar `(32, 8) → (56, 32)`; companion `(56, 32) →
    (32, 56)`.
  - End state: avatar at (56, 32) on `avatar_target`, companion
    at (32, 56) on `companion_target`. WIN.
- **Layout**:
  - avatar at (8, 32); avatar_target at (56, 32).
  - companion at (32, 8); companion_target at (32, 56).
  - No anchor_pin, no direction_indicator.
- **Difficulty justification**:
  - **(a) Random-resistance**: The harness's
    `difficulty-rules.md` § 2.a uses the soft "near-zero"
    threshold ("random-policy chance well below easy"),
    NOT the report's strict 1/10 000 graph-gate. This level
    qualifies under the soft threshold. Joint probability of
    the 3-action witness ≈ `(1/2 × 1/4096) × (1/2) × (1/2)
    = 1/32 768`. Including the small handful of equivalent
    longer winning sequences (4-action and 5-action pivot
    variants), summed over the 30-step budget, total P(win |
    random) ≈ `5 × 30 / 32 768 ≈ 1/220` — about a 0.5%
    random-stumble rate. This is "near-zero" in the soft
    framing: a vision-blind agent has < 1% per-budget
    chance, and the gameplay still requires *coordinate
    discovery* (the player must identify a centre pivot, not
    merely hammer one verb), so structural spam is excluded.
    A text-only LLM has no advantage over random because
    the rotation algebra is not derivable without the
    rendered frame. **Spam fails**: ACTION5 alone is no-op
    without pivot; ACTION6 alone never rotates. The
    centre-symmetric layout is intentional — L2's
    pedagogical role is "the most visually-readable
    introduction to multi-pawn rotation"; an asymmetric
    layout would buy a stronger random-bar but at the cost
    of L2's beginner-friendly composition arc.
  - **(b) Human-tractable**: ~2 min. The player has already
    learned pivot-and-rotate from L1, so the discovery here is
    just "now there are two pawns; how do I rotate to put them
    BOTH on their targets?" A few experimental clicks teach
    the symmetry of the layout; the (32, 32) pivot is then
    obvious from the visual symmetry of avatar-target and
    companion-target.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start**: a fully-informed player
      faces a 4096-cell pivot search and (after pivot is set)
      multiple rotation-count choices (0, 1, 2, ... rotations).
      That's at least dozens of plausible-looking first moves.
    - **Plausible-but-wrong path**: pivot at the avatar's own
      cell (8, 32) — rotating around the avatar's own cell
      leaves the avatar fixed but rotates the companion to
      `(8+8−8, 8+32−32) = (8, 32) = avatar's start cell`,
      which fails the no-overlap constraint and rejects the
      rotation. The full-knowledge player must reject this
      pivot.
    - **Witness reasoning chain**: the player reasons "the only
      pivot that maps avatar (8, 32) → companion's target
      (32, 56) is one whose midpoint-line passes through both
      AND is symmetric to the companion-target arrangement; by
      symmetry-of-layout this is the playfield centre (32, 32);
      and exactly two CW rotations around (32, 32) match the
      half-turn needed to swap horizontal-and-vertical symmetric
      pairs." The reasoning is one symmetry-detection step plus
      one rotation-count choice.
  - **(d) Step budget**: 30. Generous — 10× the 3-action
    witness; allows two full pivot-attempts of 4 actions each
    before the budget pressure starts.

### Level 3 — system + 2 more new mechanics

- **Mechanics required by the witness** (= L2-count + 2 = 5):
  - **M1: pivot-set** (carried).
  - **M2: commit-rotate** (carried).
  - **M3: companion-pawn-deliver** (carried).
  - **M4: anchor-pin-visit-checkpoint (NEW)** — sprites tagged
    `anchor_pin` are non-rotatable fixtures that stay put. The
    win predicate adds a clause: **every `anchor_pin` cell
    must have been coincident with at least one `rotatable`
    sprite's top-left at some action's end-state during the
    level**. The game tracks `_visited_pins:
    set[tuple[int, int]]`; each `step()` end, for each
    rotatable sprite, if its `(x, y)` matches any
    `anchor_pin`'s `(x, y)`, add the pin's coord to
    `_visited_pins`. Once visited, the anchor_pin's centre
    2×2 flips palette 14 → 11 and stays (persistent visual
    "stamped" cue).
  - **M5: direction-toggle (NEW)** — clicking on the
    `direction_indicator` widget (the 4×4 sprite at (4, 4))
    toggles the next-rotation direction between CW and CCW;
    the widget's pip-corner flips to surface the change. CCW
    uses the inverse formula `(px − py + y, px + py − x)`.
- **Necessity per mechanic**:
  - **M1**: As L1/L2 — pivot-less rotations are no-op; the
    avatar must move to win.
  - **M2**: As L1/L2 — only ACTION5 moves rotatable sprites.
  - **M3**: As L2 — both the avatar and the companion must reach
    their respective targets for the level to advance.
  - **M4**: L3 cannot be solved without triggering M4 because
    the win predicate AND-s the per-target colour-match clause
    (avatar at avatar_target AND companion at
    companion_target) with the visit-clause (`anchor_pin (12,
    32)` ∈ `_visited_pins`). No CW path from the start state
    visits (12, 32) within step budget 12 — CW1 of avatar
    around (32, 32) lands at (52, 32) (not (12, 32)); CW2 at
    (32, 52); CW3 at (12, 32) but that takes 4 actions and
    moves the pawns past their targets so additional CW
    rotations are needed to recover, exceeding budget.
    Therefore every winning sequence must put a rotatable
    sprite on (12, 32) via some CCW rotation — and the
    witness's CCW1 step DOES land avatar at (12, 32),
    triggering M4 directly.
  - **M5**: L3 cannot be solved without triggering M5 because
    M4 requires visiting `(12, 32)`; the only short rotation
    that lands a rotatable sprite at (12, 32) from the start
    state is CCW1 around (32, 32). CCW is unavailable until
    the player clicks the `direction_indicator` widget. Hence
    every short winning sequence includes the direction-toggle
    click (M5) before the visiting CCW.
- **Witness solution** (4 actions):
  `[ACTION6@(4, 4), ACTION6@(32, 32), ACTION5, ACTION5]`.
  - Step 1: ACTION6@(4, 4) clicks the direction_indicator widget;
    direction toggles CW → CCW; widget pip-corner flips
    top-right → top-left.
  - Step 2: ACTION6@(32, 32) sets pivot at (32, 32);
    pivot_marker halo appears at (32, 32).
  - Step 3: ACTION5 commits CCW1 around (32, 32). Using CCW
    formula `(px − py + y, px + py − x)`:
    - avatar `(32, 12) → (32 − 32 + 12, 32 + 32 − 32) = (12,
      32)`. **Lands on `anchor_pin` at (12, 32) → triggers M4
      visit; `_visited_pins = {(12, 32)}`; anchor_pin's centre
      pixels flip 14 → 11**.
    - companion `(8, 32) → (32 − 32 + 32, 32 + 32 − 8) = (32,
      56)`. (Not on anchor_pin.)
  - Step 4: ACTION5 commits CCW2 (direction stays CCW; pivot
    stays).
    - avatar `(12, 32) → (32 − 32 + 32, 32 + 32 − 12) = (32,
      52)` ✓ avatar_target.
    - companion `(32, 56) → (32 − 32 + 56, 32 + 32 − 32) =
      (56, 32)` ✓ companion_target.
  - End-state: avatar on avatar_target, companion on
    companion_target, `_visited_pins ⊇ {(12, 32)}`. All three
    win-predicate clauses satisfied. WIN.
- **Layout** (revised after critique):
  - avatar at (32, 12); avatar_target at (32, 52).
  - companion at (8, 32); companion_target at (56, 32).
  - **anchor_pin at (12, 32)** — moved from (52, 32). The new
    location lies on the avatar's CCW1 path (the witness
    triggers it directly) and is NOT on any CW path within
    budget; this is what makes M4 strictly required.
  - direction_indicator at (4, 4).
- **Difficulty justification**:
  - **(a) Random-resistance**: 4-action witness joint probability
    `(1/2 × 4/4096) × (1/2 × 1/4096) × (1/2) × (1/2) ≈ 1/67M`
    (the direction_indicator is a 4×4 region so 4 / 4096 of
    pixel-clicks land on it). Within step budget 50, total
    P(win | random) is much smaller than 1/10 000. CCW must be
    enabled before any winning rotation, so spam-CW + ACTION5
    can never win — the random agent must "discover" the
    direction_indicator click. Spam fails: ACTION5 alone never
    moves anything (pivot still unset); ACTION6 alone never
    rotates.
  - **(b) Human-tractable**: ~3 min. The discovery pathway
    is concrete and sequential:
    1. **L2-style attempt**. The player carries forward the
       L2 pattern: click the centre (32, 32), press ACTION5
       twice. Both pawns land on what LOOK like targets at
       first — but the level does NOT advance, because the
       anchor_pin at (12, 32) is still palette-14 (green,
       unstamped). The player reads "the green pad I haven't
       touched is what's keeping me from winning".
    2. **Notice the green pad's role**. The anchor_pin sprite
       is the single object on the playfield the player
       hasn't interacted with by step 2. Visually it reads as
       a "stamp pad" that wants to be visited.
    3. **Notice the corner widget**. The
       direction_indicator at (4, 4) is small but
       distinctive — palette 13 + palette 11 corner-pip
       against the off-white background. The player hovers
       on it and clicks experimentally.
    4. **Pip-corner flips**. The visible state change
       confirms the widget is interactive. The player infers
       "this widget controls something about rotation" and
       re-attempts with CCW now active.
    5. **CCW1 lands avatar on the green pad**. The pad's
       centre flips green → yellow, persistently. Player
       reads "stamped". CCW2 then lands both pawns at their
       targets and the level advances.
    Total ~3 minutes including the CW dead-end + widget
    discovery + CCW resolution.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start**: ~4096 pivot choices ×
      ~1 direction-indicator click × {CW, CCW} × {1, 2, 3+
      rotations}. ~32768 nominal first-three-action sequences.
      Strictly larger than L2's ~8192.
    - **Trivial heuristic that fails**: greedy "rotate toward
      target" — pick the pivot that moves the avatar one step
      closer to (32, 52) per click. Greedy chooses pivot (32,
      32) (centre), CW first (default direction). This *does*
      put avatar at (32, 52) and companion at (56, 32) after
      2 actions — but the level does NOT advance because the
      anchor_pin at (12, 32) is unvisited. Greedy then tries
      additional CWs to "fix" things, but every additional CW
      moves the pawns OFF their targets without ever visiting
      (12, 32). Greedy never thinks to (a) toggle direction or
      (b) move pawns SIDEWAYS to a different cell that a
      progress-heuristic would reject. The fully-informed
      player must realise: the winning move (CCW1 around (32,
      32)) intentionally moves the avatar to (12, 32), which
      a greedy/monotone-progress heuristic mistakenly rejects
      as regression — it appears the avatar is "going wrong
      direction".
    - **Witness reasoning chain (post-discovery)**: "the
      anchor_pin at (12, 32) has to be visited. (12, 32) is
      not on any CW path within the budget. The unique short
      visit is CCW1 around (32, 32), which I can only access
      after toggling direction at the corner widget. After
      visiting, CCW2 around the same pivot lands both pawns
      on targets."
  - **(d) Step budget**: 50. Generous — 12× the 4-action
    witness, larger than L2's 30 in absolute terms (per
    `difficulty-rules.md` § 2.d L3 addendum: the budget must
    NOT shrink as the level number rises since later levels
    add discovery cost). Supports the L2-style CW dead-end
    (~3 actions to discover M4 is unsatisfied), full back-
    track / pawn-recovery via additional CWs (~4 actions to
    return to start), the toggle click (1 action), the CCW1
    visit + CCW2 win (2 actions), plus ~40 actions of slack
    for exploratory pivots, alternative pivots, and probing.
    Note: CW-only paths CANNOT win regardless of budget —
    the avatar's CW cycle around (32, 32) lands at (52, 32),
    (32, 52), (12, 32), (32, 12) and back; while CW3 visits
    (12, 32), in that state the companion is at (32, 56) —
    not its target — and additional CWs cycle pawns through
    a closed orbit that never lands both at their targets
    simultaneously. M5 (direction-toggle) is therefore
    structurally required; the budget is generous on top.

## 5. Action mapping

`available_actions = [5, 6]`. Slot 7 omitted (no undo verb,
per checklist 22). Slots 1-4 omitted (no cardinal motion verb;
the avatar never directly walks).

| Action | Effect |
|---|---|
| ACTION5 | **Commit-rotate.** If `_pivot is None`, no-op (still consumes 1 step). Otherwise: compute each rotatable sprite's destination cell using the current direction (`_direction = "CW"` default; toggled via M5). Validate: no destination out of bounds (each rotatable sprite's footprint must fit in [0, 64]×[0, 64]); no destination collisions between two rotatable sprites except clean simultaneous swap (each targets the other's pre-rotation cell). If validation fails, the entire rotation is rejected (no sprites move; visual cue: rejected sprites flash palette 7 for 1 frame). If valid, every rotatable sprite's `set_position(...)` to its new cell AND `sprite.rotate(90)` (or `sprite.rotate(-90)` / equivalent for CCW) updates its pixel matrix. The `pivot_marker` and `anchor_pin` do not move (no `rotatable` tag). After all moves, run the visit-checkpoint update: for every `anchor_pin` sprite, if any `rotatable` sprite's top-left == anchor_pin's top-left, add the cell to `_visited_pins` and flip the anchor_pin's centre 2×2 from palette 14 to palette 11 (one-shot stamp; idempotent on subsequent revisits). |
| ACTION6 | **Click at display pixel (x, y).** Convert via `camera.display_to_grid(int(x), int(y))` to grid (gx, gy). Three click-target rules, evaluated in order via `level.get_sprite_at(gx, gy, ...)`: (1) if the click hits the `direction_indicator` sprite (L3 only) → toggle `_direction` between "CW" and "CCW", swap the indicator's pip-corner via two pre-built variants. (2) Else if it hits any rotatable / target / anchor_pin sprite → no-op (pivots are only placed on empty cells). (3) Else → set `_pivot = (gx, gy)`; move the `pivot_marker` halo via `set_position(gx, gy)` (the halo's top-left coincides with the pivot point used in the rotation formula; edge clicks are allowed since the halo is a 6×6 sprite and the engine clips rendering at the camera bounds). |

No context-dependent gating beyond "ACTION6 with no widget-or-pivot-target = no-op": both actions are always callable. The
direction_indicator widget itself is REMOVED at L1/L2 and TANGIBLE at L3, so M5 is naturally gated by the widget's visibility per-level.

## 6. HUD and per-game state

**HUD widgets**:
- `StepCounterHud(RenderableUserDisplay)` — single instance owned
  by the camera; renders row 63 with palette-6 filled / palette-4
  drained. Updated each `step()` via `set_current(self._steps_left)`.
  Universal pattern.

**Internal state** (held on the `Xz5g(NovaBaseGame)` instance):
- `self._pivot: tuple[int, int] | None` — the currently-marked
  pivot cell, or None if not set. Persistent across rotations.
- `self._direction: str` — `"CW"` or `"CCW"`. Default `"CW"`;
  toggled by clicking the direction_indicator widget.
- `self._steps_left: int` — per-level step counter, set in
  `on_set_level` from `level.get_data("step_budget")`.
- `self._step_hud: StepCounterHud` — the HUD instance.
- `self._pivot_marker: Sprite` — the halo sprite; created once
  in `__init__` and repositioned per click.
- `self._dir_indicator: Sprite | None` — the direction widget
  (cached at L3 via tag).
- `self._visited_pins: set[tuple[int, int]]` — cells of
  `anchor_pin` sprites that have been coincident with a
  rotatable sprite at some prior action's end-state during the
  current level. Re-initialised to the empty set in
  `on_set_level`. Mutated by `step()` after the movement
  phase (see § 5 ACTION5).

**Visible cues** (per `reference-game-patterns.md` § *Discoverability*):
- Pivot location → persistent `pivot_marker` halo at `_pivot`.
  Clicking elsewhere relocates it, so the player always sees
  where the next rotation will pivot.
- Rotation direction → the `direction_indicator` widget's
  pip-corner (top-right = CW, top-left = CCW). The pip flips
  the moment the player clicks the widget; the player can read
  current direction off the screen at any frame.
- Anchor_pin visit-state → the anchor_pin sprite renders
  in palette 14 (green) when unvisited and palette 11
  (yellow) when visited; the swap is permanent for the rest
  of the level (idempotent on revisits). The player can read
  off the screen at any moment whether the checkpoint has
  been crossed.
- Rejected rotation (out-of-bounds or rotatable-sprite
  collision) → rejected rotatable sprites flash palette 7
  (pink) for 1 frame; nothing moves; ACTION5 still consumes
  1 step. (Anchor_pins do NOT cause rejections in the
  visit-checkpoint design — they are pass-through fixtures.)
- Step budget → standard depleting bar at row 63.

## 7. Win condition

After every action's `step()` completes its movement phase
AND its visit-checkpoint update, `_check_win()` returns True
iff BOTH clauses hold:

- **(a) Target-match clause**: every sprite tagged `target`
  is co-located with at least one sprite tagged `rotatable`
  of matching tag (`avatar_target` ↔ `avatar`;
  `companion_target` ↔ `companion`).
- **(b) Visit-checkpoint clause**: every sprite tagged
  `anchor_pin` has its `(x, y)` cell in `self._visited_pins`.
  At L1/L2 there are no `anchor_pin` sprites, so this clause
  is vacuously true. At L3 the single anchor_pin at (12, 32)
  must appear in `_visited_pins`.

When both clauses hold, `self.next_level()` is called. After
L3's `next_level()` the engine's auto-WIN fires (3-level cap).

Pseudocode:

```python
def _check_win(self) -> bool:
    # (a) target-match
    for target in self.current_level.get_sprites_by_tag("target"):
        match_tag = "avatar" if "avatar_target" in target.tags else "companion"
        matched = any(
            s.x == target.x and s.y == target.y
            for s in self.current_level.get_sprites_by_tag(match_tag)
        )
        if not matched:
            return False
    # (b) visit-checkpoint
    for pin in self.current_level.get_sprites_by_tag("anchor_pin"):
        if (pin.x, pin.y) not in self._visited_pins:
            return False
    return True
```

The win predicate is structurally the same at every level;
the visit-checkpoint clause is vacuous at L1/L2 and binds
at L3.

## 8. Lose condition

`self._steps_left` is initialised in `on_set_level` from
`level.get_data("step_budget")` and decrements at the end of
every handled action's branch (BOTH ACTION5 and ACTION6 cost 1
step regardless of outcome). When `self._steps_left <= 0` after
the action handlers, `self.lose()` fires.

There is no instant-fail hazard; rejected rotations do NOT cost
extra steps (just the standard 1 per ACTION5). Rejection only
happens via out-of-bounds destination cells or two rotatable
sprites colliding on the same destination cell (excluding clean
simultaneous swaps). Anchor_pins do NOT cause rejection — they
are pass-through visit-checkpoints.

The HUD bar at row 63 surfaces remaining budget.

## 9. Novelty note

### Closest taxonomy near-miss + concrete distinguishing rule

- **`cn04` nub-pair-glyph (reference)** — cn04's ACTION5 rotates a
  *single SELECTED sprite* 90° in place (via `sprite.rotate(90)`).
  Other sprites are unaffected. Selection is per-piece and the
  pivot is implicitly each piece's own bounding-box centre.
  **xz5g** transforms EVERY rotatable sprite simultaneously
  around an EXTERNAL pivot the player chose; every sprite's
  position translates AND its pixels rotate. Two different
  rotation contracts: per-piece self-rotate (cn04) vs whole-
  world-rotate-around-shared-pivot (xz5g). Confirmed against
  cn04's deep-analysis in
  `deep-analysis-3lvls/cn04/cn04-deep-analysis.md`
  via the `lceflskdhw` selected-sprite handle and the
  `gjhtwbvrel` matcher (post-action) — both operate on a single
  selected sprite, never on a global rotation.

- **`qz73` radial-cycle-lock (prior-game)** — qz73 spins a fixed
  central rotor of coloured tips and lets the player lock
  individual tips against rotation. **xz5g** has no fixed rotor;
  the "rotor" is the entire arena and the "pivot" is wherever
  the player clicks (4096 candidate pivot cells, not 1 fixed
  axle). qz73's tips are pre-arranged on the rotor; xz5g's
  rotatable sprites are placed freely.

### Closest prior-game near-miss + concrete distinguishing rule

- **`vy3k` region-swap-arrange (prior-game, 2026-05-08)** — vy3k
  has 4 fixed quadrant centres; ACTION6 selects a quadrant and
  ACTION5 with one selection rotates that quadrant's sprites
  90° CW *contained inside that 32×32 region*. **xz5g** has
  no quadrants and no swap; pivot is a player-chosen any-cell
  (4096 candidates), and rotation is whole-arena (every
  rotatable sprite anywhere on the 64×64 playfield transforms
  relative to the pivot). The cognitive task is *continuous
  pivot search* vs vy3k's *discrete 4-quadrant choice* — the
  Principle 3 core-dynamic divergence in
  `negative-similarity-check.md`. Concrete visual distinctions
  the spec commits to: NO divider cross partitioning the
  playfield, NO per-quadrant frames; ONE pivot_marker halo (not
  four selection_frames); 6×6/8×8 sprites with internal pattern
  vs vy3k's 4×4 hop-grid blocks.

- **`hp9c` pinwheel-cell-rotate (prior-game, untracked)** — hp9c
  rotates the four CARDINAL-NEIGHBOUR CELLS of a clicked centre
  one step CW around it (4-cycle on cell *values*; sprite
  positions do not change). **xz5g** rotates SPRITE POSITIONS
  (and pixel orientations) globally, not cell values locally.
  Different objects (cells vs sprites) and different scope (4
  cardinal neighbours vs every rotatable sprite on the
  playfield). hp9c's transformation is a permutation of fixed-
  cell colour states; xz5g's is a continuous geometric rotation
  applied to sprite (x, y) coordinates.

- **`pv5q` pivot-rod-swing (prior-game)** — pv5q's avatar is
  parametrically tied to (anchor, R, θ); arrows swing/extend the
  rod; ACTION5 swaps anchor between stakes. **xz5g** has no rod
  and no parametric (R, θ) state; every rotatable sprite is a
  free sprite at its own (x, y); ACTION5 transforms ALL of
  them together via a single 90° rotation around the player-
  picked pivot. pv5q's "pivot swap" is an L3-only single-rod
  re-attachment; xz5g's pivot is the central state every level.

- **`qj4r` / `rj5w` / `wj7d` (fold/mirror family)** — those are
  REFLECTION operations across an axis (mirror; D2 reflection
  group). xz5g is ROTATION around a point (C4 rotation group).
  Different geometric transformation; different invariants
  (parity flip vs orientation cycling); different cognitive
  task (line placement vs point placement).

### Negative-similarity check (re-run on full spec)

Walking the 8 dimensions of `negative-similarity-check.md`
against vy3k (the closest single prior):

1. **Board**: rotatable sprites + targets on a grid → SHARED.
2. **Player input**: click + ACTION5 commit → SHARED (xz5g
   omits arrow keys entirely; vy3k has them).
3. **Goal**: pawn(s) on coloured target(s) → SHARED.
4. **Lose**: step budget exhaustion → SHARED.
5. **Cast**: avatar + companion + targets + anchor_pin + halo
   + direction_indicator. vy3k: avatar + walls + target +
   selection_frames + locks. **DIFFERENT** — xz5g has multi-
   pawn delivery from L2 and a unique direction_indicator
   widget at L3; vy3k has no second movable pawn and no
   direction widget; xz5g has no walls, lock-toggles, or
   quadrant frames.
6. **Visual signature**: xz5g's playfield is one continuous
   32-pixel-radius arena with a halo + pip-corner widget
   accent; vy3k's playfield is four 32×32 quadrants with a
   black divider cross and four 32×32 selection-frame
   overlays. **DIFFERENT** — distinct first-glance read.
7. **Pixel grain**: xz5g uses 6×6 / 8×8 sprites with internal
   tri-quadrant pattern + concentric ring targets; vy3k uses
   4×4 hop-grid blocks. **DIFFERENT** — denser grain in xz5g.
8. **Core dynamic**: xz5g = "spin the world around the pin you
   placed"; vy3k = "swap or rotate one of four panels". Both
   are arena-transformations, but the *cognitive task is the
   substantive divergence* — continuous-pivot-search (xz5g)
   vs discrete-quadrant-choice (vy3k). Principle 3 axis
   divergence per `negative-similarity-check.md`.

Shared count on the principal dimensions (6, 7, 8 — the named
weighted ones): zero. Shared count on universal dimensions
(1, 3, 4): three (these are NovaPlay platform commonalities).
Verdict: **NOVEL** under the negative-similarity test.

### Index-empty disclosure

`prior-games/index.md` is non-empty (45 entries). The closest
mechanic-family-tag near-misses are listed above. None has the
free-pivot whole-arena-rotation core dynamic.
