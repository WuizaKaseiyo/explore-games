# gx7m — mechanic spec

## 1. Title

Gear-Mesh Cascade. (Internal working title; the 4-character ID
`gx7m` is the only identifier the player sees.)

## 2. Mechanic family

`gear-mesh-cascade` — a small cluster of toothed-disc gears arranged
on a fixed grid; clicking any gear's hub rotates it 90° clockwise,
and the rotation propagates instantly through every cardinally-meshed
neighbour with the **sign flipped** (counter-clockwise), recursing
through the connected mesh-graph. Each gear carries a coloured
rim-mark at its top tooth; the puzzle is to drive every mark to its
same-coloured target indent in the surrounding collar-ring.

Core-knowledge priors used (per `core-knowledge-priors.md`):

- **Objectness** — gears are persistent positionally-fixed entities.
- **Geometry & topology** — rotation, mesh-adjacency graph, mark-to-
  target angular alignment, connected-component partitioning when a
  clutch disengages.
- **Physics** — sign-flipping mesh transmission of rotation is an
  intuitive mechanical-engineering rule.

## 3. Sprite roster

All sprites live on a 64×64 grid. Gears are 6×6 cells; collar-rings
are 10×10 hollow squares centred on each gear. Two gears mesh when
their 6×6 sprite boxes are cardinally adjacent (centre-to-centre
distance = 10 cells along an axis).

| Sprite name | Dims | Palette | Tags | Role |
|---|---|---|---|---|
| `gear_pink` | 6×6 | {2 inner, 4 teeth, 7 mark} | `gear` | Plain gear; rim-mark colour pink (palette 7). |
| `gear_lblue` | 6×6 | {2, 4, 10 mark} | `gear` | Plain gear; mark light-blue. |
| `gear_orange` | 6×6 | {2, 4, 12 mark} | `gear` | Plain gear; mark orange. |
| `ratchet_magenta` | 6×6 | {2, 4, 6 mark} | `gear`, `ratchet` | Ratchet gear; mark magenta (palette 6). |
| `clutch_green` | 6×6 | {2, 4, 14 mark} | `gear`, `clutch` | Clutch gear; mark green (palette 14). |
| `ratchet_bolt` | 1×5 | {3 grey track, 11 yellow rod} | `ratchet_bolt` | 1-column × 5-row vertical "bolt" sprite floating above a ratchet disc's collar. The yellow rod (3 cells) slides between two positions inside the 5-cell sprite: rod at bottom = LOCKED (engaged into the gear); rod at top = CW (retracted, gear free to rotate one-way). Doubles as the click target for toggling state. |
| `clutch_bolt` | 1×5 | {3 grey track, 15 purple rod} | `clutch_bolt` | 1-column × 5-row vertical bolt above a clutch disc; same rod-down-vs-rod-up metaphor as the ratchet bolt, in purple. ENGAGED = rod at bottom; DISENGAGED = rod at top. |
| `collar_pink` | 10×10 hollow | {3 frame, 7 indent} | `collar` | Collar-ring around `gear_pink`'s home cell; one cell of palette 7 marks the target angle. |
| `collar_lblue` | 10×10 hollow | {3 frame, 10 indent} | `collar` | Collar-ring; light-blue indent. |
| `collar_orange` | 10×10 hollow | {3 frame, 12 indent} | `collar` | Collar-ring; orange indent. |
| `collar_magenta` | 10×10 hollow | {3 frame, 6 indent} | `collar` | Collar-ring around the ratchet; magenta indent. |
| `collar_green` | 10×10 hollow | {3 frame, 14 indent} | `collar` | Collar-ring around the clutch; green indent. |
| `step_counter_widget` | (HUD) | {0 white, 4 off-black} | n/a | Single-row depleting bar at frame row 0. |

Per-collar, the indent's position around the ring (north / east /
south / west) encodes the per-level target angle for that gear.

Sprite roles use the conventions in `code/universal-scaffold.md`:
sprite dict keys / `name` fields / class names use semantic English
words; only the gear ID `gx7m` and the class `Gx7m` are opaque.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All use `grid_size=(64, 64)`. Camera viewport
matches grid-size (64×64; no scaling needed).

### Level 1 — base dynamic system

**Layout.** 3 plain gears in a horizontal row, centres at
`(18, 32)`, `(28, 32)`, `(38, 32)`. From left to right:
`gear_pink`, `gear_lblue`, `gear_orange`. Mesh-graph is a chain:
`pink — lblue — orange`. Each gear has its same-coloured collar-
ring sprite framing it, with the target indent at the **south**
position (palette index relative to the ring: bottom-centre cell).

Initial gear rotations: all `0°` (mark points north).
Targets: all `180°` (mark points south).

**Mechanics required by the witness** (N = 1):

- `M1` — Mesh cascade rule: ACTION6 click on a gear hub rotates
  that gear by `+90° CW`; every mesh-connected gear rotates `−90°`
  if its parity (chessboard 2-colouring of the mesh-graph) is the
  opposite of the clicked gear, `+90°` if same parity. Continues
  recursively through the connected component.

**Necessity per mechanic.**

- L1 cannot be solved without triggering `M1` because the player's
  only verb is ACTION6, every ACTION6 click on a gear *triggers*
  the cascade by definition (the engine routes click → cascade
  unconditionally for tag `gear`), and the target requires every
  gear's rotation to change from `0°` to `180°`, which only the
  cascade verb produces.

**Witness solution** (shortest, 2 actions):

Click coordinates are pixel-space; converted via
`camera.display_to_grid` to the 64×64 grid. The click target for
each gear is its centre-cell (e.g., the pink gear's centre-cell is
`(20, 34)` in pixel coords).

```
ACTION6 @ (20, 34)   # click pink gear hub → cascade applies (+1,−1,+1) deltas
ACTION6 @ (20, 34)   # click again → cumulative (+2,−2,+2) ≡ (180°, 180°, 180°)
```

Result: pink at 180°, lblue at 180° (since `−180° ≡ +180°` mod 360),
orange at 180°. All three marks point south, at their respective
south-indents on each collar-ring. Win.

(Equivalent witnesses: 2 clicks of the lblue hub, or 2 clicks of
the orange hub — symmetry of the cascade rule.)

**Difficulty justification (per `difficulty-rules.md` § 2):**

- **(a) Random-resistance.** Random-policy / vision-blind agents
  may stumble through L1 occasionally — this is acceptable per
  `composition-and-tutorial.md` for the tutorial level. The valid-
  action set is 6 cells (3 gear hubs × 2 cells each = 6 click
  targets, since `_get_valid_actions` returns the centre of each
  gear and the cell directly south of the centre as alternates;
  see § 6 below). Random play has `~ (1/6)^2 = 1/36` per 2-step
  attempt; in 50,000 steps, ~1400 wins. ABOVE the formal 1/10000
  threshold — but L1 is intentionally tutorial-tier per the
  spec.
- **(b) Human time.** ~30 seconds. After clicking once and seeing
  all three gears rotate (one CW, two CCW from neighbour-couplings),
  the player infers the cascade. A second click of the same gear
  doubles the rotation, landing every mark at its south-indent.
- **(c) Planning depth.** None. L1 is the discovery gate; once the
  rule is understood, the win is immediate. (Consistent with
  `difficulty-rules.md` § 2 (c) L1 guidance.)
- **(d) Step budget.** `step_budget = 20`. Generous: ~10× the
  witness length, allowing exploration.

### Level 2 — base system + 1 new mechanic

**Layout.** 3 gears in a horizontal row, centres at `(18, 32)`,
`(28, 32)`, `(38, 32)`. Left and right are plain (`gear_pink`
and `gear_lblue`); the middle is `ratchet_magenta`. A
`ratchet_bolt` (1×5 vertical sprite) sits centred above the
ratchet's collar at top-left `(30, 22)` — its yellow rod occupies
3 of the 5 cells, with the rod's vertical position encoding state:
rod at the bottom (cells 3-4-5 of the sprite, immediately above
the collar) = LOCKED (engaged into the gear); rod at the top
(cells 1-2-3) = CW (retracted, free to rotate one-way). The indicator is the click
target AND the visible state display: `LOCKED` paints `[3,3,3]`
(flat grey, blends with the collar frame); `CW` paints `[3,3,11]`
(yellow on the right cell); `CCW` paints `[11,3,3]` (yellow on the
left cell). Each gear's matching collar-ring frames it.

Mesh-graph is the chain: `pink — magenta — lblue`. Magenta is the
ratchet.

Initial rotations: all `0°` (marks point north).
Targets:
- pink: `180°` (south indent).
- magenta: `90°` (east indent).
- lblue: `270°` (west indent).

Initial ratchet direction state: `BLOCKED` (cascade through the
ratchet is blocked; the ratchet's hub-click is a no-op).

**Mechanics required by the witness** (= N+1 = 2; introducing
EXACTLY 1 new mechanic):

- `M1` (carried forward) — Mesh cascade rule. Same as L1.
- `M2` (new) — Ratchet one-way gate: a `ratchet` gear has an
  internal state ∈ {`LOCKED`, `CW`}. ACTION6 click on any cell of
  the ratchet's `ratchet_bolt` (1×5 sprite above the collar)
  toggles the state and slides the bolt's yellow rod between the
  bottom 3 cells (LOCKED) and the top 3 cells (CW). The cascade
  rule for the ratchet is gated:
  - When state is `LOCKED`, the ratchet does not rotate and the
    cascade does not propagate past it.
  - When state is `CW`, a `+90°` (CW) arrival rotates the ratchet
    and the cascade propagates onward (with sign flipped); a
    `−90°` (CCW) arrival is blocked at the ratchet.

**Necessity per mechanic.**

- L2 cannot be solved without triggering `M1` because the targets
  require pink at 180°, magenta at 90°, lblue at 270°. The only
  verb available is ACTION6 → cascade; without firing the
  cascade rule at least once, no gear rotates from 0°.
- L2 cannot be solved without triggering `M2` because (i) the
  ratchet starts `BLOCKED`, so without a `tang_dir` click, the
  magenta gear *never rotates* (cascades from neighbours stop at
  it; its own hub-click is a no-op while blocked) — and the
  target magenta = 90° is unreachable; AND (ii) without setting
  the ratchet direction to allow a one-way pass, it is impossible
  to arrange pink = 180° and lblue = 270° simultaneously: with the
  ratchet `BLOCKED`, pink and lblue are decoupled (good — they can
  be rotated independently) but magenta is stuck at 0°; with the
  ratchet `CW`, a single `R-hub` click lands the asymmetric
  `(−1, +1, −1)` triple onto pink/magenta/lblue that the witness
  exploits. The puzzle's specific `(180°, 90°, 270°)` target is
  not in the linear span of pure-cascade clicks alone, so the
  ratchet-direction gating is essential.

**Witness solution** (shortest, 6 actions):

Pixel coordinates: pink-hub `(20, 34)`, magenta-hub `(30, 34)`,
lblue-hub `(40, 34)`, magenta-bolt `(30, 24)` (any cell in the bolt's
column; centre cell shown).

```
ACTION6 @ (30, 24)   # click magenta-bolt → state toggles LOCKED → CW; rod slides up.
ACTION6 @ (30, 34)   # click magenta-hub → magenta rotates +1 (CW allowed);
                     #                     pink receives −1, lblue receives −1.
                     #                     state: pink=−1=270°, magenta=90°, lblue=−1=270°.
ACTION6 @ (20, 34)   # click pink-hub → pink rotates +1; cascade arrives at
                     #                  magenta as −1 = CCW, blocked (ratchet
                     #                  is CW-only). lblue unchanged.
                     #                  state: pink=0°, magenta=90°, lblue=270°.
ACTION6 @ (20, 34)   # click pink-hub → pink rotates +1 = 90°. magenta blocked.
                     #                  state: pink=90°, magenta=90°, lblue=270°.
ACTION6 @ (20, 34)   # click pink-hub → pink rotates +1 = 180°. magenta blocked.
                     #                  state: pink=180°, magenta=90°, lblue=270°. WIN.
```

Length: 5 actions (one tang-click + one ratchet-hub-click + three
pink-hub clicks). Final state matches the targets at all three
collars. Win.

**Difficulty justification (per `difficulty-rules.md` § 2):**

- **(a) Random-resistance.** Valid-action set is ~7 cells (3 gear
  hubs + 1 tang = 4 unique action cells; plus 3 alternate cells per
  hub for click-tolerance = ~7). Witness length 5; specific-sequence
  prob = `(1/7)^5 ≈ 1/16,800`. In 50,000 random plays:
  ~3 expected wins. BELOW the formal `1/10,000` threshold per the
  graph-based check. Pass.
- **(b) Human time.** ~2 minutes. The player must (i) discover that
  the magenta gear *doesn't rotate* on click (mechanic-discovery
  cue: the magenta hub is unresponsive while ratchet is `BLOCKED`),
  (ii) discover the tang sprite by clicking around it, (iii) try
  one tang-click, observe the magenta-hub now responds, (iv) plan
  the 5-action witness.
- **(c) Planning depth.** Moderate post-discovery.
  - **First-action enumeration**: 4 distinct first-action options
    a fully-informed player faces — click pink-hub, lblue-hub,
    magenta-hub, or magenta-tang. (Clicking magenta-hub before any
    tang-click is a no-op while state is `BLOCKED`; a fully-informed
    player knows this and would not pick it.) ≥ 2 valid first
    actions ✓.
  - **Plausible wrong path**: setting ratchet to `CCW` first (one
    extra tang-click). With ratchet `CCW`, pink-hub click cascades
    through (pink +1, magenta −1, lblue +1) — the lblue-side delta
    arrives at the wrong sign for our target lblue=270°, and
    correcting requires significantly more clicks. The player must
    reason: targets are `(+2, +1, −1)`; clicking pink under
    `CCW` ratchet gives `(+1, +3, +1)` per click — the lblue delta
    is wrong sign — so use `CW` instead.
  - **Witness reasoning chain**: (i) magenta = `90°` is parity-1,
    only reachable via cascade through the ratchet → set ratchet to
    `CW` so that an R-hub click fires the cascade with magenta
    rotating `+1`; (ii) the R-hub click also sends `−1` to pink
    and lblue, giving state `(−1, +1, −1)`; (iii) lblue's target is
    `270° = −1`, *already met* by step (ii); (iv) pink needs
    `−1 → +2`, which is `+3` mod 4 = 3 more clicks of pink-hub
    (each pink-hub click sends `−1` to the ratchet, blocked by `CW`,
    so lblue stays at `−1`).
- **(d) Step budget.** `step_budget = 30`. Generous: 6× the witness.

### Level 3 — system + 1 more new mechanic

**Layout.** 5 gears in a horizontal row, centres at `(8, 32)`,
`(18, 32)`, `(28, 32)`, `(38, 32)`, `(48, 32)`. From left to
right: `gear_pink`, `ratchet_magenta`, `gear_lblue`, `clutch_green`,
`gear_orange`. Mesh-graph is the chain
`pink — magenta — lblue — green — orange`. The ratchet's
1×5 yellow `ratchet_bolt` sits centred above magenta's collar with
top-left at `(20, 22)`; the clutch's 1×5 purple `clutch_bolt` sits
centred above green's collar with top-left at `(40, 22)`. Both
float against the playfield background. Each gear has its
matching collar-ring.

Initial rotations: all `0°`.
Targets:
- pink: `180°` (south indent).
- magenta: `90°` (east indent).
- lblue: `90°` (east indent).
- green: `90°` (east indent).
- orange: `180°` (south indent).

Initial ratchet direction: `BLOCKED`. Initial clutch state:
`ENGAGED` (mesh fully connected).

**Mechanics required by the witness** (= L2-count + 1 = 3;
introducing EXACTLY 1 new mechanic):

- `M1` (carried forward) — Mesh cascade rule.
- `M2` (carried forward) — Ratchet direction gate.
- `M3` (new) — Clutch engagement gate: a `clutch` gear has an
  internal `engaged` boolean (default `True`). ACTION6 click on
  any cell of the clutch's `clutch_bolt` (1×5 sprite above the
  collar) toggles `engaged` and slides the bolt's purple rod
  between the bottom 3 cells (engaged) and the top 3 cells
  (disengaged).
  When `engaged == False`, the clutch's mesh-edges (both incoming
  and outgoing) are removed from the mesh-graph: cascades cannot
  pass through the clutch, AND cascades from elsewhere do not
  rotate the clutch. ACTION6 click on the clutch's hub still
  rotates the clutch by `+1` (with the cascade firing only over
  the connected component *the clutch belongs to right now*; if
  disengaged, that component is just `{clutch}` and only the
  clutch rotates).

**Necessity per mechanic.**

- L3 cannot be solved without triggering `M1` because the only
  verb is ACTION6, every gear-hub or tang click invokes the
  cascade engine, and the targets require all 5 gears at non-zero
  rotation — the cascade rule is unconditionally fired by any
  gear-affecting click.
- L3 cannot be solved without triggering `M2` because the ratchet's
  target rotation is `90°` (parity-1) and the ratchet starts
  `BLOCKED`. With the ratchet `BLOCKED`, magenta never rotates from
  0°, and target magenta = 90° is unreachable — *unless* the
  player toggles `tang_dir` to `CW` to permit the magenta gear to
  rotate. Even after enabling, the ratchet's role-as-asymmetric-
  router is required because the L3 target has the parity-0 gears
  pink/lblue/orange at deltas `(+2, +1, +2)` — *not* uniform —
  which is impossible in the bipartite-only span of the full
  cascade chain. The ratchet must block the cascade-back-to-pink
  while pink is being independently driven up to `+2`.
- L3 cannot be solved without triggering `M3` because of the same
  parity argument applied across the clutch boundary: lblue's
  delta is `+1` and orange's delta is `+2`, but lblue and orange
  are both parity-0 gears in the chain
  `pink(0)–magenta(1)–lblue(0)–green(1)–orange(0)` — they are 2
  hops apart, same parity, and mesh-coupled. With every gear in
  one connected component, no sequence of cascades + ratchet-
  blocks can make their parity-0 deltas differ. The ONLY way to
  have lblue = `+1` and orange = `+2` simultaneously is to
  partition the mesh by disengaging the clutch (removing the
  `lblue—green` and `green—orange` edges), so that orange becomes
  an isolated component and can be rotated independently of lblue.

**Witness solution** (shortest, 11 actions):

Pixel coordinates: pink-hub `(10, 34)`, magenta-hub `(20, 34)`,
lblue-hub `(30, 34)`, green-hub `(40, 34)`, orange-hub `(50, 34)`,
magenta-bolt `(20, 24)` (centre cell of the 1×5 bolt above magenta),
green-bolt `(40, 24)`.

```
ACTION6 @ (40, 24)   # green-bolt → clutch DISENGAGES; purple rod slides up.
                     #               mesh-graph splits into 3 components:
                     #               {pink, magenta, lblue}, {green}, {orange}.
                     #               state unchanged: all 0°.
ACTION6 @ (40, 34)   # green-hub → only green rotates (alone in its component).
                     #             green +1 = 90°.  state: (0°,0°,0°,90°,0°).
ACTION6 @ (50, 34)   # orange-hub → only orange rotates.
                     #              orange +1 = 90°.  state: (0°,0°,0°,90°,90°).
ACTION6 @ (50, 34)   # orange-hub → orange +1 = 180°.
                     #              state: (0°,0°,0°,90°,180°).
ACTION6 @ (20, 24)   # magenta-bolt → ratchet LOCKED → CW; yellow rod slides up.
                     #               state unchanged: (0°,0°,0°,90°,180°).
ACTION6 @ (20, 34)   # magenta-hub → magenta +1 = 90° (CW allowed).
                     #              cascade fires over {pink, magenta, lblue}:
                     #              pink receives −1, lblue receives −1.
                     #              (green, orange untouched: clutch disengaged.)
                     #              state: (270°,90°,270°,90°,180°).
ACTION6 @ (10, 34)   # pink-hub → pink +1 = 0°. cascade arrives at magenta as
                     #            −1 = CCW, blocked (CW-only). lblue unchanged.
                     #            state: (0°,90°,270°,90°,180°).
ACTION6 @ (10, 34)   # pink-hub → pink +1 = 90°. magenta blocked.
                     #            state: (90°,90°,270°,90°,180°).
ACTION6 @ (10, 34)   # pink-hub → pink +1 = 180°. magenta blocked.
                     #            state: (180°,90°,270°,90°,180°).
ACTION6 @ (30, 34)   # lblue-hub → lblue +1 = 0°. cascade arrives at magenta
                     #             as −1, blocked. cascade tries lblue→green
                     #             but clutch disengaged: blocked.
                     #             state: (180°,90°,0°,90°,180°).
ACTION6 @ (30, 34)   # lblue-hub → lblue +1 = 90°. magenta blocked. green-side
                     #             blocked by disengaged clutch.
                     #             state: (180°,90°,90°,90°,180°). WIN.
```

Length: 11 actions. Final state matches the targets `(180°, 90°,
90°, 90°, 180°)` at all five collars. Win.

**Difficulty justification (per `difficulty-rules.md` § 2):**

- **(a) Random-resistance.** Valid-action set ≈ 7 unique cells
  (5 hubs + 1 tang + 1 lever). Specific-sequence probability for
  the 11-action witness: `(1/7)^11 ≈ 5.7 × 10^−10`. In 50,000
  random plays: `~ 3 × 10^−5` expected wins; in 1,000,000 plays:
  `~ 6 × 10^−4`. Far below the `1 / 10,000`-per-attempt threshold
  per `from-tech-report.md` § 7. Pass.
- **(b) Human time.** ~3 minutes. The player must (i) re-discover
  the cascade and ratchet from L2, (ii) discover the clutch lever
  by clicking near the new green gear, (iii) recognise that lblue
  and orange need different deltas under the same parity → must
  partition the mesh, (iv) plan an order: handle the disconnected-
  side first (green and orange while clutch is disengaged), then
  the cascade-side, leveraging the ratchet to break parity within
  the {pink, magenta, lblue} sub-component.
- **(c) Planning depth.** Challenging even for an attentive
  human.
  - **First-action enumeration**: 7 distinct first-action options
    a fully-informed player faces — 5 gear hubs + 1 ratchet-tang +
    1 clutch-lever. ≥ L2's 4 ✓.
  - **Trivial post-discovery heuristic that fails**: *"Rotate each
    gear directly to its target by repeatedly clicking its hub
    until the mark aligns."* A fully-informed player would naïvely
    try this. Walking the heuristic:
    - Click pink-hub 2x → pink = 180°, but cascade fires through
      magenta (blocked, OK) — wait, magenta is BLOCKED on entry
      so cascade dies at magenta on the first hop. Pink alone
      reaches 180° in 2 clicks. *State: (180°, 0°, 0°, 0°, 0°).*
    - Click magenta-hub → no-op (blocked).
    - Click lblue-hub → lblue +1; cascade tries lblue→magenta
      (blocked) and lblue→green; green is engaged, so green
      receives `−1` and cascades to orange `+1`. *State: (180°,
      0°, 90°, 270°, 90°).*
    - Click green-hub → green +1 (cascade fires across the {lblue,
      green, orange} component since clutch is engaged); lblue
      receives `−1`, orange receives `−1`. *State: (180°, 0°, 0°,
      0°, 0°).* Two of the prior gains are wiped.
    - The heuristic loops between progress and regression because
      every click on lblue / green / orange disturbs the others.
      The heuristic *cannot* set lblue=90° AND orange=180° AND
      green=90° simultaneously without the clutch toggle.
  - **Where the heuristic diverges from the witness**: at the
    *very first action*. The witness's first action is
    `green-lever` (disengage clutch); the heuristic's first
    action is some gear-hub. The heuristic never disengages the
    clutch; it operates in the fully-coupled mesh, where the
    parity-coupling between lblue and orange is unbreakable.
- **(d) Step budget.** `step_budget = 50`. Generous: ~4.5× the
  witness; never shrinks relative to L2's 30. (L2 budget × 1.67;
  honours `difficulty-rules.md` § 2 (d) L3 rule "step budget must
  NOT shrink relative to the witness as level number rises".)

## 5. Action mapping

`available_actions = [6]`. Pure-click game.

ACTION6 click coordinates pass through `camera.display_to_grid` to
yield grid `(gx, gy)`. The dispatcher checks the sprite at
`(gx, gy)` via `level.get_sprite_at(gx, gy, ...)` and routes by tag:

| Click target tag | Effect |
|---|---|
| `gear` (any gear's hub region) | Rotate that gear by `+90° CW`; trigger the mesh-cascade. If the gear is a ratchet, rotation gated by direction-state. If the gear is a clutch, propagation only over its current component. |
| `tang_dir` (a ratchet's direction-tang) | Cycle that ratchet's direction state (`BLOCKED` → `CW` → `CCW` → `BLOCKED`). No rotation fired. |
| `tang_lever` (a clutch's lever-tang) | Toggle that clutch's `engaged` boolean. No rotation fired. |
| Any other cell | No-op (cascade does not fire). |

Click-area is the gear's full 6×6 box for hub-clicks (so any click
within the gear's bounding box counts as a hub-click). Tang clicks
are detected by sprite tag at the exact tang cell. `_get_valid_actions`
enumerates the centre cell of every hub + every tang + every lever
(total ≤ 7 click cells per level). Per `r11l`'s convention, this is
the action enumeration the agent sees.

## 6. HUD and per-game state

**HUD** (one widget):

- `step_counter_widget` — a `RenderableUserDisplay` subclass
  rendering a single-row depleting bar at frame row 0. Implementation
  follows the `tu93` / `cn04` minimal template. Width: 32 cells,
  centred (offset 16 from each edge). Drained 1 unit per non-RESET
  action. When the widget reaches 0, `self.lose()` fires.

**Per-game state.**

| Field | Type | Purpose |
|---|---|---|
| `gear_rotations` | `dict[Sprite, int]` | Current rotation in 90° units (0..3) for every gear sprite. |
| `mesh_neighbors` | `dict[Sprite, list[Sprite]]` | Static cardinal-mesh adjacency, computed once per `on_set_level`. |
| `ratchet_dirs` | `dict[Sprite, str]` | One of `"BLOCKED"`, `"CW"`, `"CCW"` per ratchet sprite. |
| `clutch_engaged` | `dict[Sprite, bool]` | Per clutch sprite. |
| `gear_targets` | `dict[Sprite, int]` | Target rotation 0..3 per gear (read from level data). |
| `_step_counter_ui` | `step_counter_widget` instance | The HUD. |

## 7. Win condition

After every ACTION6 click, recompute `gear_rotations`. If for every
gear `g`: `gear_rotations[g] == gear_targets[g]`, fire
`self.next_level()`.

Concretely:
```python
def _check_win(self) -> bool:
    return all(
        self.gear_rotations[g] == self.gear_targets[g]
        for g in self.gear_rotations
    )
```

After the L3 win, the engine auto-fires `self.win()` at the end of
the level list (default `NovaBaseGame` behaviour).

## 8. Lose condition

When the step-counter widget reaches 0 — i.e., when
`self._action_count >= step_budget` (read from
`level.get_data("StepBudget")`) — fire `self.lose()`. No instant-
fail collisions, no hazard tiles.

```python
if self._action_count >= self._step_budget:
    self.lose()
```

## 9. Novelty note

Re-grounding the spec against `mechanic-novelty/`. (Detailed
write-up lives in `workspace/mechanic-pick.md`; condensed
restatement here.)

**Closest taxonomy entries** and the concrete distinguishing rule:

- `lp85` (row-col-shift-grid): both are pure-click (`available_actions=[6]`)
  and rotation-related. *Distinguishing rule*: lp85's clicks invoke
  pre-computed positional permutations of the cell grid; gx7m's
  clicks rotate gears in place AND propagate rotation through a
  mesh-graph with per-edge sign flipping. lp85 has no
  rotational-cascade analogue.
- `cn04` (rotate-translate-jigsaw): both involve rotation +
  click-to-select. *Distinguishing rule*: cn04 selects ONE piece
  and then rotates only that piece (ACTION5); each click is
  independent of the others. gx7m cascades rotation through
  EVERY mesh-connected gear with sign flipping; you cannot rotate
  a single gear in isolation without also affecting its mesh
  neighbours.

**Closest prior-games entries** (full distinguishing rules in
`mechanic-pick.md`):

- `qz73` (radial-cycle-lock): both ask for rotated-mark-to-coloured-
  target alignment. *Distinguishing rule*: qz73 has ONE central
  rotor with embedded tips that all rotate together as one rigid
  body; gx7m has MANY independent gears with sign-flipping
  propagation across mesh-edges and a clutch that *partitions* the
  mesh-graph.
- `bx84` (beam-mirror-reflect): both involve propagation through
  cells. *Distinguishing rule*: bx84 propagates a coloured beam
  through cells, reflecting off mirror sprites; gx7m propagates
  rotation through gear-mesh adjacency with sign flipping. Bx84's
  signal is a directional ray; gx7m's signal is a scalar rotation
  delta that branches across mesh-graph parents.
- `vn8d` (domino-cascade-topple): both have "cascade".
  *Distinguishing rule*: vn8d's cascade is one-shot directional
  and irreversible; gx7m's cascade is bidirectional, instant, and
  fully reversible — every click is undone by 3 more clicks of the
  same gear.
- `kn58` (anchor-pull-magnet): both have "single click triggers
  global propagation". *Distinguishing rule*: kn58 propagates
  *translation* (every pawn slides one cell toward the click);
  gx7m propagates *rotation*, with sign flipping; gx7m has no
  pawn-translation at all.
- All 13 other priors: no surface overlap on the heavy principles
  (visual signature, pixel grain, core dynamic).

**Negative similarity check** (per `negative-similarity-check.md`):
walked the 8 dimensions against every prior; the closest are qz73
(2 shared dimensions, both cosmetic — input-verb and step-counter)
and bx84 (1 shared dimension — step-counter). All are below the
3-dimension reject threshold. The visual-signature plan in §3 of
`mechanic-pick.md` uses palette `{2, 3, 4, 13}` structural +
`{6, 7, 10, 12, 14}` mark colours + `{11, 15}` interaction tangs,
deliberately distinct from every prior-game's recorded palette
signature.
