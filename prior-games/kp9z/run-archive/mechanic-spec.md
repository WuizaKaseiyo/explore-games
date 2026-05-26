# mechanic-spec.md — kp9z

## 1. Title
Grain Accumulate Topple Cascade.

## 2. Mechanic family
**Family tag**: `grain-accumulate-topple`.

Each cell on the playfield carries a non-negative integer "grain count" 0..3.
The player's verb is **drop**: a click on a SOURCE cell adds 1 grain to that
cell. When a cell's count would exceed its **capacity** (default 4), the cell
**topples** — its count resets to 0 and 1 grain is delivered to each of its
four cardinal neighbours, which may themselves topple, producing a
deterministic cascade. **Sink** cells (L2+) absorb every grain delivered
without re-emitting. **Redirector** cells (L3) topple at capacity 1 and emit
their single grain to a fixed cardinal direction (the rest of the cascade-
input is absorbed). Win condition is strict: every cell must end at its
declared target count (0 for non-targets), so over-dropping is a real
failure mode.

Prior categories used (per `core-knowledge-priors.md`): **objectness**
(grains as countable persistent entities at each cell), **basic geometry &
topology** (cardinal-neighbour distribution; redirector handles directional
flow; sinks puncture topology), **basic physics** (overflow-as-spillover;
deterministic conservation of grains except at sinks).

## 3. Sprite roster

**Revised in critique pass to satisfy item 20 (shape-as-meaning).** The
playfield is a small N×N grid of "conceptual cells". Each conceptual
cell occupies a **10×10** sprite (was 6×6); cells abut directly (no
inter-cell gap); the grid_size is 64×64 (camera default, scale 1×). The
sprite has a 2-pixel-thick frame plus a 6×6 interior; each pip and the
type center are 2×2 sprite-pixel blocks. 2-pixel-thick features survive
a 2×2 average-pool to 32×32 unchanged.

### Common 10×10 layout

```
Col:    0  1  2  3  4  5  6  7  8  9
Row 0:  F  F  F  F  F  F  F  F  F  F     ← frame top (2 px thick)
Row 1:  F  F  F  F  F  F  F  F  F  F
Row 2:  F  F  T1 T1 Cn Cn T2 T2 F  F     ← T1, Cn, T2 = 2×2 pip slots
Row 3:  F  F  T1 T1 Cn Cn T2 T2 F  F
Row 4:  F  F  Cw Cw Z  Z  Ce Ce F  F     ← Cw, Z (type), Ce = 2×2
Row 5:  F  F  Cw Cw Z  Z  Ce Ce F  F
Row 6:  F  F  T3 T3 Cs Cs T4 T4 F  F     ← T3, Cs, T4 = 2×2 pip slots
Row 7:  F  F  T3 T3 Cs Cs T4 T4 F  F
Row 8:  F  F  F  F  F  F  F  F  F  F     ← frame bottom (2 px thick)
Row 9:  F  F  F  F  F  F  F  F  F  F
```

- F (frame, 2-px thick on all 4 sides): palette 4 (off-black).
- T1, T2, T3, T4 (target pip slots, 2×2 each at the inner-area's 4
  corners): palette 14 (green) iff target_count ≥ slot-index (1..4),
  else palette 2 (matches backdrop). Painted at level start; never
  changes during play.
- Cn (current-grain pip top, 2×2 at rows 2–3, cols 4–5): palette 11
  (yellow) iff current_count ≥ 1, else palette 2.
- Cw (current-grain pip left, rows 4–5, cols 2–3): palette 11 iff
  current_count ≥ 2, else palette 2.
- Ce (current-grain pip right, rows 4–5, cols 6–7): palette 11 iff
  current_count ≥ 3, else palette 2.
- Cs (current-grain pip bottom, rows 6–7, cols 4–5): palette 11 iff
  current_count ≥ 4, else palette 2 (transient during topple).
- Z (type indicator, 2×2 at rows 4–5, cols 4–5): palette varies by
  cell type.

### Cell-type sprite templates — shape-distinct

Each cell type has a distinct **shape feature** beyond just colour, so
that stripping colour still leaves the type identifiable. The features
exploit positional asymmetry on the frame edge (a "notch" replacing
2 of the frame pixels with a non-frame palette value at a known
position) plus the corner-pip presence (already distinguishing for
targets).

| Type | Z (type center) | Frame-edge notch | Corner pips |
|---|---|---|---|
| regular | palette 2 (invisible) | none | none |
| source | palette 6 (magenta) | TOP edge (rows 0–1, cols 4–5) palette 6 | none |
| sink | palette 9 (blue) | LEFT edge (rows 4–5, cols 0–1) palette 9 | none |
| target_n (n=1..4) | palette 13 (maroon) | none | n green pips lit |
| redirector_south | palette 12 (orange) | BOTTOM edge (rows 8–9, cols 4–5) palette 12 | none |

Without colour, the shape inventory:

- regular: blank (frame border + empty interior).
- source: vertical bar pattern (top-edge notch + center 2×2) — looks like
  a "T" rotated, two clusters in a vertical column.
- sink: horizontal bar pattern (left-edge notch + center 2×2) — two
  clusters in a horizontal row to the left.
- target_n: corner-dot pattern (n corner blocks + center 2×2).
- redirector_south: vertical bar pattern in the *lower half* (center
  2×2 + bottom-edge notch) — visually a downward-pointing pair of
  clusters distinct from source's top-edge notch.

The five types are pairwise shape-distinguishable from the pixel
matrix alone (e.g., source vs sink: top-notch vs left-notch on the
frame; source vs redirector_south: top-edge notch vs bottom-edge
notch — opposite sides of the cell).

### Bank declarations

The Python `sprites` dict declares one template per cell type. The
live in-game sprite for each cell is a clone of the appropriate
template, with current-pip pixels mutated in `step()` and target-pip
pixels painted once in `on_set_level()`.

- `cell_template_regular` — 10×10 with frame palette 4, interior all
  palette 2. tags=`["cell", "regular"]`.
- `cell_template_source` — 10×10 with frame palette 4, top-edge notch
  palette 6 (rows 0–1, cols 4–5), Z 2×2 palette 6, all pip slots
  palette 2. tags=`["cell", "source"]`.
- `cell_template_target_<n>` for n in 1..4 — 10×10 with frame palette 4,
  Z palette 13, target pips T1..T_n palette 14 (others palette 2),
  current pips palette 2. tags=`["cell", "target", f"target_{n}"]`.
- `cell_template_sink` — 10×10 with left-edge notch palette 9 (rows 4–5,
  cols 0–1), Z palette 9. tags=`["cell", "sink"]`.
- `cell_template_redir_south` — 10×10 with bottom-edge notch palette 12
  (rows 8–9, cols 4–5), Z palette 12. tags=`["cell", "redirector",
  "redir_south"]`.

(Only redirector_south is needed for the levels in this spec — the four-
direction variants from the previous draft are not used. If a future
revision needs them, swap in `_redir_north` / `_redir_east` /
`_redir_west` with the notch on the matching frame edge.)

Each level instantiates clones of the appropriate templates at
conceptual positions, mutating the clone's `name` to `cell_<r>_<c>`
(row r, col c) for runtime lookup. Layer = 0 (background); the HUD
bar lives on the camera's interface list.

Step-counter HUD (`StepCounterHud`) — `RenderableUserDisplay` subclass.
Reads `self.steps_left` and `self.max_steps` from the game; renders a
horizontal bar at row 63 of the 64×64 frame. Bar is palette 14 (green)
filling left→right by `steps_left/max_steps`, with palette 4 (off-black)
remainder. No text.

Background (camera background): palette 2 (light grey).
Letter-box (camera letter_box): palette 4 (off-black).

## 4. Level progression, mechanic enumeration, and witness solutions

**Revised in critique pass.** Across all 3 levels the game uses
`grid_size=(64, 64)` (camera default; scale 1×). Cell sprite is 10×10
with no inter-cell gap (sprites abut, frame edges adjacent). Cell (r, c)
(row r, col c) is positioned at sprite-coordinate `(anchor_x + 10c,
anchor_y + 10r)` where the anchor is chosen per level to centre the
conceptual board in the 64×64 grid. Click coordinate at the centre of
cell (r, c) is `(anchor_x + 10c + 5, anchor_y + 10r + 5)`.

### Level 1 — base dynamic system

Configuration:
- Conceptual board: 4×4 cells (16 cells total). Total board pixel size
  = `4 × 10 = 40` game-cells. Anchor `(12, 12)` (centred: `(64−40)/2 = 12`).
  Board occupies game-cells `(12, 12)..(51, 51)`; HUD row at `y=63`
  remains free; letterbox at the frame edges.
- Cell (1, 1) = SOURCE. (Row 1, col 1; all 4 cardinals exist within the
  4×4 conceptual grid.)
- Cells (0, 1), (1, 0), (2, 1), (1, 2) = TARGET, target_count=1 each
  (the 4 cardinals of the source: north, west, south, east respectively).
- All other 11 cells = REGULAR (target_count=0).
- `step_budget` = 8.

**Mechanics required by the witness** (N = 2):
1. **Drop** — clicking the source increments source's grain count by 1.
2. **Topple-on-capacity-4** — when source's grain count would exceed 4, it
   resets to 0 and delivers 1 grain to each of its 4 cardinal neighbours.
   Cells receiving a grain that puts them above capacity in turn topple.

**Necessity per mechanic** (counterfactual):
- L1 cannot be solved without **drop** because there is no other way to
  introduce a grain anywhere on the board. With zero grains the 4 targets
  remain at 0 and the win predicate fails on every check.
- L1 cannot be solved without **topple-on-capacity-4** because the source
  is the only clickable cell (clicks on non-source cells are no-ops); the
  only path for a grain to leave the source and reach a target is via
  topple. Without a topple firing, all targets stay at 0.

**Witness solution** (4 actions, all clicks on the source cell at
mid-cell pixel `(27, 27)` — sprite at `(22, 22)`, mid-cell offset
`(5, 5)`):

```
[ACTION6@(27, 27), ACTION6@(27, 27), ACTION6@(27, 27), ACTION6@(27, 27)]
```

Trace:
- Click 1: source (1,1) count 0→1.
- Click 2: source 1→2.
- Click 3: source 2→3.
- Click 4: source 3→4 → topples → source resets to 0, each cardinal
  receives 1: target (0,1)=1✓, target (1,0)=1✓, target (2,1)=1✓, target
  (1,2)=1✓. Win predicate fires.

**Difficulty justification**:
- (a) Random-resistance — A random / vision-blind agent must choose ACTION6
  with valid click coords. Of 64×64 = 4096 click coords, roughly 12×12 = 144
  fall on the source sprite (the 12×12 onscreen footprint of cell (1,1) at
  scale 2×). Random click probability of hitting source ≈ 144/4096 ≈ 3.5%.
  To win in ≤8 actions a random policy must hit source 4 times (with
  possible misses cushioned by the budget) and not over-shoot. Probability of
  4 source-hits within 8 random clicks is binomial(8, 0.035, k≥4) ≈ 0.001%
  — well below the NovaPlay §3.5 random-policy floor.
- (b) Human-tractable — A first-time human reads "click some cell and watch
  what happens" within ~10–15 seconds. Discovery of the topple after 4
  clicks is direct. Total expected human time: ~30–60 seconds for L1.
- (c) Planning depth — L1 is the discovery gate. Once the rule is
  understood (click source 4 times → cascade → win), no further planning.
  Per `difficulty-rules.md` § 2 (c), L1 has *no strict planning
  requirement*.
- (d) Step budget — 8 actions. Witness length 4. Slack of 4 absorbs
  exploratory misses (clicks on regular cells = no-ops, do not consume the
  budget? No — every click consumes 1 step regardless of where it lands —
  this is critical for forcing the player to learn the source-only-clickable
  rule). Generous over witness, comfortable.

### Level 2 — base system + 1 new mechanic (sink)

Configuration:
- Conceptual board: 5×5 cells (25 cells total). Total board pixel size =
  `5 × 10 = 50` game-cells. Anchor `(7, 7)` (centred: `(64−50)/2 = 7`).
  Board occupies game-cells `(7, 7)..(56, 56)`.
- Cells `(1, 2)` and `(3, 2)` = SOURCE.
- Cells `(0, 2)`, `(2, 2)`, `(4, 2)` = SINK.
- Cells `(1, 1)`, `(1, 3)`, `(3, 1)`, `(3, 3)` = TARGET, target_count=1
  each.
- All other cells = REGULAR (target_count=0).
- `step_budget` = 16.

**Mechanics required by the witness** (M = N + 1 = 3, +1 new):
1. **Drop** (carried forward from L1).
2. **Topple-on-capacity-4** (carried forward from L1).
3. **Sink** (NEW in L2) — sink cells absorb any grain delivered to them
   without re-emitting; they never topple themselves and remain at 0.

**Necessity per mechanic** (counterfactual, one line per mechanic):
- L2 cannot be solved without **drop** because the two sources start at 0;
  without a drop, no grain enters the system and all 4 targets stay at 0.
- L2 cannot be solved without **topple-on-capacity-4** because only sources
  are clickable; reaching the targets requires sources to topple and
  distribute grains to cardinal neighbours. With no topple, every target
  stays at 0.
- L2 cannot be solved without **sink** because each source has cardinal
  neighbours `(0,2)/(2,2)/(4,2)` (the middle-column cells) in addition to
  its target cardinals. Without sinks at those middle-column cells, toppling
  source (1,2) would deposit a grain at (0,2) and at (2,2) (each REGULAR,
  target_count=0) — the strict win predicate would fail because two non-
  target cells now hold count 1 (≠ target_count 0). Sinks absorb those
  grains and preserve the win-state. Every alternate path that involves
  source (1,2) toppling is blocked by the strict count predicate unless the
  cells (0,2) and (2,2) are sinks; symmetric argument for source (3,2).

**Witness solution** (8 actions): click source A at conceptual `(row=1,
col=2)` four times, then click source B at `(row=3, col=2)` four times.
(Order can swap; result identical by the abelian property of the
sandpile.)

Game-grid click coords:
- Source A sprite at `(anchor_x + 10*col, anchor_y + 10*row) = (7 + 20,
  7 + 10) = (27, 17)`. Mid-cell click `(32, 22)`.
- Source B sprite at `(7 + 20, 7 + 30) = (27, 37)`. Mid-cell click
  `(32, 42)`.

```
[ACTION6@(32, 22) × 4, ACTION6@(32, 42) × 4]
```

Trace:
- Clicks 1–4: source A 0→4 → topples → A=0, each cardinal +=1: (0,2)=sink
  absorbs, (2,2)=sink absorbs, (1,1)=1✓, (1,3)=1✓.
- Clicks 5–8: source B 0→4 → topples → B=0, each cardinal +=1: (2,2)=sink,
  (4,2)=sink, (3,1)=1✓, (3,3)=1✓.

Win predicate fires at click 8.

**Difficulty justification**:
- (a) Random-resistance — Two source sprites (~144 game-pixels each onscreen
  out of 4096) → P(random click hits any source) ≈ 7%. To win in ≤16
  actions, a random policy must (i) NOT click a non-source cell more than
  ~8 times (which is the slack), and (ii) accumulate exactly 4 clicks on
  EACH source — clicking 8 times on one source alone makes the source topple
  twice, putting cardinals at count 2 (over target_count 1) → strict fail.
  P(random gives exactly-4-each-source within 16 clicks while avoiding non-
  source clicks) is below 0.0001%. Well under §3.5 floor.
- (b) Human-tractable — L1 has taught the topple rule. L2 introduces sink
  via visual cue (blue 2×2 type indicator at sink cells; player sees a click
  on source whose cardinal is a sink → that cardinal stays at 0, while the
  other cardinals reach 1). A human sees this within ~30 sec and infers
  "blue cells absorb". Total L2 time: ~90–120 sec.
- (c) Planning depth (post-discovery) — Decision space at level start:
  **2 valid first actions** (click source A or click source B) → ≥ 2,
  satisfies the 1-action-lookup-table reject. Plausible-but-wrong post-
  discovery action paths a fully informed player would consider:
  (i) "click source A 8 times to fill all 4 targets at once" — fails
  because A topples twice, depositing 2 grains at (1,1) and (1,3) (over
  their target_count=1) → STRICT OVERSHOOT, win predicate fails. The
  witness's reasoning chain is "each source topples once; each topple
  delivers exactly 1 grain to each non-sink cardinal target; therefore
  each source must be clicked exactly 4 times". The player must reject
  the 8-on-A heuristic (which feels like "do the work in one place")
  and accept the 4+4 split because of the non-aliasing of the 4 targets.
- (d) Step budget — 16 actions. Witness length 8. Slack of 8 absorbs
  exploratory misses on the second source (clicks on non-source = wasted
  step but no count change) and also lets the player overshoot once on
  one source and recover (e.g. accidentally click 5 on A, see overshoot
  warning... actually no, overshoot is irreversible — click 5 puts A=1
  with cardinals already at 1; click 5 doesn't topple again; final state
  has A=1 ≠ 0 → fail). Slack accommodates exploration, not overshoot
  recovery; per `difficulty-rules.md` § 2(d), L2 must reflect the new-
  mechanic discovery cost and 16 is comfortable over the 8-action witness.

### Level 3 — system + 1 new mechanic (redirector)

Configuration:
- Conceptual board: 5×5 cells. Anchor `(7, 7)` (same as L2; `grid_size =
  (64, 64)`).
- Cells `(1, 1)` and `(1, 3)` = SOURCE.
- Cells `(0, 1)`, `(0, 3)`, `(1, 0)`, `(1, 2)`, `(1, 4)` = SINK.
- Cell `(2, 1)` = REDIRECTOR_SOUTH (exit direction = south; topples on
  receiving 1 grain and forwards it to `(3, 1)`).
- Cell `(2, 3)` = REDIRECTOR_SOUTH (forwards to `(3, 3)`).
- Cell `(2, 2)` = SINK.
- Cells `(3, 1)` and `(3, 3)` = TARGET, target_count=1 each.
- All other cells = REGULAR (target_count=0).
- `step_budget` = 16.

**Mechanics required by the witness** (= L2-count + 1 = 4, +1 new):
1. **Drop** (from L1).
2. **Topple-on-capacity-4** (from L1).
3. **Sink** (from L2).
4. **Redirector** (NEW in L3) — a cell with capacity 1; on receiving a
   grain it topples and emits the single grain in its declared exit
   direction (cardinal). Net: 1 grain in, 1 grain out. The "rest of the
   cascade-input absorbed" rule does not apply when the redirector
   receives exactly 1 grain (which is the case in this level's witness).

**Necessity per mechanic** (counterfactual, one line per mechanic):
- L3 cannot be solved without **drop** because both sources start at 0;
  without dropping, no grains enter and target counts stay at 0.
- L3 cannot be solved without **topple-on-capacity-4** because targets
  (3,1) and (3,3) are 2 cells away from each source, beyond the source's
  immediate 4-cardinal neighbour set. Without source toppling, the cascade
  never starts and grains never reach the redirectors. Specifically:
  source A at (1,1) is not cardinal-adjacent to (3,1) — the only path is
  source A → (2,1) → (3,1), requiring source A to topple at least once.
- L3 cannot be solved without **sink** because each source has 3 non-
  redirector, non-target cardinals: source A at (1,1) has cardinals (0,1),
  (1,0), (1,2), (2,1). Of these, (0,1)=sink, (1,0)=sink, (1,2)=sink, and
  only (2,1) is the redirector. Without sinks at (0,1), (1,0), (1,2), the
  source A topple would deposit grains at those (REGULAR) cells, each
  ending at count 1 ≠ target_count=0 → STRICT FAIL. Symmetrically for
  source B at (1,3): cardinals (0,3)=sink, (1,2)=sink, (1,4)=sink, (2,3)=
  redirector. (Note that (1,2) is the sole shared cardinal between the two
  sources — it must be a sink to absorb deliveries from BOTH source topples
  in the single-step witness.)
- L3 cannot be solved without **redirector** because target (3,1) is
  2 cells south of source A, and the cell between them — (2,1) — is the
  redirector. Without redirector at (2,1), a grain reaching (2,1) would
  remain there (count 1 in a REGULAR cell, target_count=0) → STRICT FAIL,
  AND the target (3,1) would never receive a grain (target_count=1 unmet).
  The redirector is required in two directions: it absorbs the cascade
  grain into a topple (clearing (2,1) of the unwanted count) AND forwards
  the grain to (3,1) (filling the target). Symmetrically for redirector
  at (2,3) and target (3,3).

**Witness solution** (8 actions):

- Source A sprite at `(7 + 10, 7 + 10) = (17, 17)`. Mid-cell click
  `(22, 22)`.
- Source B sprite at `(7 + 30, 7 + 10) = (37, 17)`. Mid-cell click
  `(42, 22)`.

```
[ACTION6@(22, 22) × 4, ACTION6@(42, 22) × 4]
```

Trace:
- Clicks 1–4: source A 0→4 → topples → A=0, cardinals receive 1 each:
  (0,1)=sink absorbs; (1,0)=sink absorbs; (1,2)=sink absorbs; (2,1)=
  redirector receives 1 → topples (capacity 1) → (2,1)=0, exit_south
  delivers 1 to (3,1) → (3,1)=1✓.
- Clicks 5–8: source B 0→4 → topples → B=0, cardinals receive 1 each:
  (0,3)=sink; (1,2)=sink; (1,4)=sink; (2,3)=redirector → topples →
  (2,3)=0, exit_south → (3,3)=1✓.

Final state: every source=0, every redirector=0, every sink=0, every
target=target_count, every regular=0. Win predicate fires.

**Difficulty justification**:
- (a) Random-resistance — As L2 (two sources, ~7% random-click hit rate)
  but with stricter exact-4-each-source requirement: any deviation produces
  STRICT OVERSHOOT or undershoot (intermediate target counts, regular
  cells with grain, etc.). Random win probability ≪ 0.0001%.
- (b) Human-tractable — L2 has taught sink. L3 introduces redirector via
  visual cue (orange asymmetric 2×2 type indicator; L1/L2's experience
  shows that orange + non-matching-target-corner pip pattern marks
  redirectors). A human, on first toppling source A, sees grains land at
  the cardinal sinks (no change) AND at the redirector (orange cell pip
  flickers to 1, then drops back to 0 as the next-cardinal cell — (3,1)
  — gains 1). Visible chain: redirector → south. Player infers
  "redirector forwards a grain". Total L3 time: ~120–180 sec; total
  environment ~5–6 minutes.
- (c) Planning depth (post-discovery) — Decision space at level start:
  **2 valid first actions** (≥ L2's). Trivial post-discovery heuristic
  that fails: "click each source 8 times to fill the targets faster".
  A fully-informed player who has internalised the L2 cap-4 topple may
  reach for "topple twice = deliver twice = guaranteed fill" — but L3's
  targets each have target_count=1, so a double topple delivers 2 grains
  via the redirector chain and (3,1) ends at count 2 ≠ 1 → STRICT
  OVERSHOOT, fail. The witness diverges from the 8-each heuristic at
  click 5 onward: at click 5 source A has count 1 (post-topple at click 4)
  and the witness moves on to source B; the heuristic continues clicking
  A. After click 8 (heuristic), source A has toppled twice; (3,1) has
  count 2; target is 1; predicate fails. The argument the player must
  reach is: "the redirector chain delivers exactly 1 grain to (3,1) per
  source-A topple; the target wants exactly 1; therefore source A must
  topple exactly once". This requires reasoning about the propagation
  *count*, not just propagation *direction*, and it must be done before
  the click sequence is committed.
- (d) Step budget — 16 actions. Witness length 8. Slack of 8 — equal to
  L2's, never smaller (per `difficulty-rules.md` § 2(d) addendum: budget
  must NOT shrink relative to witness as level number rises).

## 5. Action mapping

`available_actions = [6]`.

- `ACTION6` (click): drop one grain on the cell at the click's grid
  coordinate, **iff** that cell's `cell_type == source`. If the click
  resolves to a non-source cell or to a coordinate outside the
  conceptual board, the action is a no-op (still consumes one step from
  the budget — non-source clicks are valid in the engine but produce no
  game-state change).

No other actions. ACTION1–5 and ACTION7 are not in `available_actions`.

## 6. HUD and per-game state

**HUD** (`StepCounterHud(RenderableUserDisplay)`):
- Renders frame[63, :w] as palette 14 (green) and frame[63, w:] as palette 4
  (off-black), where `w = round(64 * steps_left / max_steps)`.
- Read by the camera's `interfaces=[hud]` list.
- Updated in `step()` after every action.

**Per-game state** (instance attributes on the game class):
- `self.grain_counts: dict[(int, int), int]` — current grain count per
  conceptual cell `(i, j)`. Updated on click + topple cascade.
- `self.cell_types: dict[(int, int), str]` — type per cell: one of
  `"regular" | "source" | "target" | "sink" | "redirector_north" |
  "redirector_south" | "redirector_east" | "redirector_west"`.
- `self.target_counts: dict[(int, int), int]` — required final grain count
  per cell (0 for non-targets; the target's declared count for targets).
- `self.cell_sprites: dict[(int, int), Sprite]` — handle to the placed
  cell sprite for runtime pixel mutation.
- `self.steps_left: int`, `self.max_steps: int` — step budget tracking.
- `self.board_size: int` — N (4 for L1, 5 for L2/L3).
- `self.anchor: tuple[int, int]` — game-grid offset of cell (0,0)'s
  sprite's top-left corner.

No persistent hidden state across the cascade — cascades resolve
deterministically and instantly within `step()` before the visual is
re-rendered. The cascade is computable from `(grain_counts, cell_types)`
alone, so determinism (per §3.5.1) is preserved.

## 7. Win condition

After each action's cascade resolves, evaluate:

```python
def _check_win(self) -> bool:
    for (i, j), grain in self.grain_counts.items():
        if grain != self.target_counts[(i, j)]:
            return False
    return True
```

If `_check_win()` returns True, call `self.next_level()` (or `self.win()`
on the last level). The predicate is testable: every cell's current
grain count must equal its declared target count, where target_counts
defaults to 0 for all non-target cells.

True for every level: per §4 above, each level's target cell list and
sink/redirector/regular structure produce a unique assignment that
satisfies `_check_win` only when every conceptual cell ends at exactly
its target.

## 8. Lose condition

```python
def _check_lose(self) -> bool:
    return self.steps_left <= 0
```

Triggered when the step counter reaches 0 without a win in the same step.
Calls `self.lose()`.

No instant-fail collision; no irreversible failure mode beyond step-
exhaustion. Overshoot causes a wrong final state but is not detected
mid-cascade — the player continues clicking until the budget runs out
(or, rarely, an overshoot cell topples again and accidentally returns
to a winning state, in which case the win predicate fires immediately).

## 9. Novelty note

Re-grounding against `mechanic-novelty/`, with the per-prior detail
already enumerated in `mechanic-pick.md`. Concrete distinguishing rules
restated here for the spec-level critique:

### Closest taxonomy entries (`taxonomy-of-25-games.md`)

- **dc22 (colour-cycle-walk)** — dc22 cycles a global tag-group state on
  step. **kp9z** is per-cell integer accumulation with overflow-driven
  redistribution. Concrete distinguishing rule: dc22's state mutation is
  GROUP-LEVEL (every wedge of colour X cycles together); kp9z's state
  mutation is CELL-LEVEL (only the dropped-on cell increments), with
  cascade emerging from threshold-overflow rather than from a deliberate
  trigger.

- **gv47-style region growth** is in `prior-games`, not in the taxonomy;
  see below.

No taxonomy game has the per-cell integer-counter-with-overflow dynamic.

### Closest prior-games entries (`prior-games/index.md`)

- **vn8d (domino-cascade-topple)** — closest. Five concrete distinguishing
  rules (also in `mechanic-pick.md` §Novelty):
  1. State cardinality: vn8d cells are binary (standing/fallen); kp9z
     cells are integer-valued (0..3) and the count itself is the
     reasoned-about state.
  2. Trigger: vn8d's chain is one-click-then-cascade; kp9z's cascade
     fires automatically when a cell's count crosses capacity, which can
     happen many drops into a sequence of clicks.
  3. Direction: vn8d's domino tips have a directional pose (which way
     they fall); kp9z topples symmetrically to all 4 cardinals (and the
     L3 redirector is a different mechanic that EXPLICITLY breaks
     symmetry — orthogonal to default cell topple).
  4. Verb cardinality: vn8d wants 1 click; kp9z wants many clicks across
     a planned sequence. Player thinking is "where does this 1 grain
     end up after cascading" not "which cascade am I triggering".
  5. Failure mode: kp9z has overshoot (over-dropping → cell count
     above target → strict fail); vn8d has no equivalent — toppling is
     monotone.

- **gx7m (gear-mesh-cascade)** — propagates rotations across mesh.
  kp9z propagates integer grain counts. Different state space, different
  propagation law.

- **gv47 (seed-grow-surround-dissolve)** — region growth + ring dissolve
  + ACTION5 mix. kp9z has no regions, no rings, no mixing. The "cascade
  via topple" is local-cell integer redistribution, not contiguous-area
  expansion.

- **fz5j (phase-step-tile)** — time-driven tile pulses on per-cell
  periods. kp9z cells change state ONLY in response to player drops (or
  cascade triggered by them); nothing is on a clock.

- **bx84 (beam-mirror-reflect)** — directional beam through mirrors.
  kp9z is 4-way symmetric topple emission; the L3 redirector is *not* a
  beam — it forwards exactly 1 grain to 1 cardinal direction and is
  exhausted.

- **kn58 (anchor-pull-magnet)** — single anchor pulls all pawns one
  Manhattan step. kp9z has no movement of any sprite — only count
  changes per cell.

- **vk8m (vortex-ring-stir)** — rotation of stones in an 8-cell ring.
  kp9z has no rotation, no rings, no avatar.

No prior shares 3+ surface dimensions with kp9z (per the negative-
similarity-check in `mechanic-pick.md`).
