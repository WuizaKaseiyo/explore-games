# mechanic-pick

## game_id
`tm5x`

Generated per `code/id-generation.md`. Verified non-colliding:
- Not in 25 reference IDs (ar25, bp35, cd82, cn04, dc22, ft09, g50t,
  ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48,
  sp80, su15, tn36, tr87, tu93, vc33, wa30).
- Not in 29 entries of `prior-games/index.md` (kf42, qz73, kx14,
  qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84,
  wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w,
  tg6w, vd3g, jd4q, ek73).
- Not an English word (`tm5x` is opaque per §3.4).

## mechanic_family
`thermal-diffusion-blend`

## seed
(autonomous) — no user-provided seed.

## one-paragraph description

A small playfield where every cell carries an integer **temperature**
in {-2, -1, 0, +1, +2} rendered as a five-step palette gradient
(`{4 off-black, 10 light-blue, 0 white, 7 pink, 8 red}`). A single
pawn — a small avatar with a polarity-marker pip on its chest —
walks the field with arrow keys and toggles its own polarity
(hot ↔ cold) with ACTION5. After each pawn step, the cell the pawn
occupies is **stamped** with the pawn's polarity (+2 if hot, -2 if
cold) and then ALL cells perform one tick of integer-rounded
**diffusion** (each cell's new value = round of the mean of itself
and its 4-neighbours, clamped to {-2..+2}). Designated **target
ring** sprites sit on selected cells; each target requires a
specific temperature value (matching its visible ring colour). The
level wins on the tick when every target ring's underlying cell
matches the target value SIMULTANEOUSLY. The puzzle is to plan a
walk + polarity-toggle sequence whose deposits + diffusion settle
the field into the right pattern at the right moment, before the
step-counter HUD runs out.

The verb is genuinely **continuous gradient-shaping** — the player
deposits heat or cold at points and lets the diffusion smear the
field smoothly. There is no discrete topple, no projectile, no
frontier wave; the field's whole integer state evolves toward
equilibrium each tick, and the pawn's deposits perturb that
equilibrium.

## per-level composition outline

- **L1 (base dynamic system, +1 mechanic — pawn walk-and-stamp).**
  One hot-target ring on an open field. Pawn starts cold-side-up
  but the level lays it as already-hot so the polarity toggle is
  not yet necessary. Walking near or onto the target heats the
  cell; diffusion smooths the heat outward. Witness: walk to target
  cell, hold a few steps to stamp heat enough that the cell reads
  +2 and the diffusion-equilibrium does not pull it back down.
- **L2 (+1 new mechanic — ACTION5 polarity toggle).** Two target
  rings: one hot (+2), one cold (-2), placed several cells apart.
  Pawn starts hot. Witness: walk to and stamp the hot target,
  ACTION5 to flip cold, walk across to stamp the cold target,
  arriving at the moment when both rings simultaneously read their
  required values. The L1 walk-and-stamp mechanic is still
  required — every step still deposits — and the new mechanic
  (polarity toggle) is also required because no single-polarity
  walk satisfies both rings.
- **L3 (+1 new mechanic — insulating walls partition the
  diffusion).** Adds wall sprites tagged as **insulators** that
  render as dark rounded blocks; cells on opposite sides of an
  insulator do NOT exchange heat during diffusion. Three target
  rings now require three different temperatures (hot, neutral=0,
  cold), and the insulators partition the field so the player must
  reason about which sub-region each polarity-walk feeds. Witness
  uses all three mechanics: walk-and-stamp + polarity toggle +
  insulator-aware routing.

## similarity check

### Against the 25 reference taxonomy

The candidate's mechanic family is `thermal-diffusion-blend`. The
nearest taxonomy-family stems by primary verb are:

- **dc22 colour-cycle-walk** — pawn walks a maze; stepping on a
  colour-trigger cycles every same-coloured wedge to its next state
  in a fixed sequence; goal is to match the target ring.
- **re86 frame-paint-canvas** — marker walks a hidden canvas,
  depositing colour and flooding by 3 cells per step. ACTION5
  cycles which marker is active.
- **ft09 stamp-3x3-paint** — pure click; clicking stamps a 3×3
  pattern.

**Family-level check.** None match `thermal-diffusion-blend` either
exactly or after hyphen-splitting (no shared first two words). All
three go to **NOVEL — no escalation needed**, but the description
check below is run anyway because re86 and dc22 share the
walk-and-affect-cells dynamic.

**Description-level check.**

- *vs dc22.* dc22 cycles **discrete** wedge-states in a **fixed
  enumerated cycle**; the trigger fires only on the cell stepped
  on; no **diffusion** of state across the field. tm5x runs
  **field-wide diffusion every tick** and uses a **continuous
  integer gradient**, not a fixed cycle. **No description match.**
- *vs re86.* re86 is **flood paint** — the marker physically
  expands a 3-cell shell of paint per move and shrinks the
  opposite side. The painted region is a **boolean-per-channel**
  set of pixels, not a continuous temperature. There is no
  diffusion: paint stays where it landed. tm5x doesn't paint or
  flood — it stamps a single-cell value and lets all cells
  arithmetically average toward equilibrium. **No description
  match.**
- *vs ft09.* ft09 is pure-click stamping a fixed 3×3 colour
  pattern; cells go through a small palette cycle on click. No
  diffusion, no walk. tm5x is walk-driven and integer-arithmetic
  diffusion. **No description match.**

Verdict: **NOVEL** vs the taxonomy.

### Against `prior-games/index.md`

Scanned all 29 entries; the nearest neighbours are:

- **pf3w wavefront-converge-timing** — click pre-placed slots to
  activate emitters; ACTION5 globally ticks each emitter's
  BFS-radius wavefront outward; level wins on the single tick when
  every same-coloured target receiver coincides with a frontier
  cell. **NEAR-MISS** because pf3w also has a tick-globally-
  propagating field, and it also has ACTION5 + targets-must-
  coincide-on-a-tick.
- **kp9z grain-accumulate-topple** — click sources to drop grains;
  cells overflow at capacity 4 to 4 cardinals; sinks absorb;
  click-rotatable redirectors forward grains. **NEAR-MISS** because
  kp9z also has a per-tick cell-state cellular-automaton governing
  the field.
- **gv47 seed-grow-surround-dissolve** — click coloured seeds to
  grow regions; surrounding a same-coloured pip dissolves it.
  **NEAR-MISS** because gv47 also evolves a region structure each
  tick.
- **vd3g valley-dig-roll** — click cells to toggle binary terrain;
  marbles flow downhill. **WEAK NEAR-MISS** — also a global
  flow-field but the dynamic is purely gravity, not diffusion.
- **mr5q polarity-attract-discharge** — pawns flip yang/yin via
  click; per ACTION5 each walks toward nearest same-colour
  opposite; same-colour adjacency discharges. **WEAK NEAR-MISS** —
  shares the polarity-toggle verb (yang/yin), but the dynamic is
  pawn-locomotion, not field-diffusion.

**Distinguishing rules (concrete, per `similarity-check.md`):**

- **vs pf3w.** pf3w propagates a **boolean BFS frontier** outward
  from each emitter; cells are either "in the active frontier this
  tick" or "not". The win check is *coincidence at one tick of
  frontier with receiver*. tm5x maintains an **integer temperature
  field** that smooths via arithmetic averaging; cells carry a
  scalar from -2 to +2 every tick, not a binary-active/inactive
  flag. tm5x has no frontiers — every cell smoothly equilibrates
  every tick. The win check is *every target's underlying cell
  scalar matches a per-target target-value*, not coincidence with
  a frontier. Furthermore, pf3w's verb on the player is
  **click-to-arm + ACTION5-to-tick** (no walking; emitters are
  pre-placed); tm5x's verb is **walk-to-deposit + ACTION5-to-flip
  polarity** (no static emitters). The action shape is different,
  the field representation is different, the win check is
  different — three concrete distinguishing rules.
- **vs kp9z.** kp9z's per-cell rule is **discrete topple at
  capacity 4** — cells either hold ≤3 grains or instantaneously
  cascade out one grain per cardinal neighbour. Topple is a
  threshold non-linearity. tm5x's per-cell rule is **smooth
  averaging with rounding** — every cell, every tick, regardless
  of value. There is no threshold and no avalanche. Furthermore,
  kp9z's player verb is **click-source-to-add + click-to-rotate-
  redirector** (pure-click); tm5x's verb is **walk-to-stamp +
  ACTION5-to-flip-polarity** (pure-arrow + freedom slot). Three
  concrete differences: cell rule (averaging vs threshold-topple),
  player verb (walk vs click), value range (signed scalar vs
  unsigned grain count).
- **vs gv47.** gv47's per-cell rule is **boolean region growth on
  click** — clicking a seed expands its region; surrounding a pip
  dissolves the pip. The field state is a partition into coloured
  regions, not a scalar. tm5x's field is a signed scalar, evolves
  every tick (not per-click), and there is no region-membership
  notion. Player verb in gv47 is **click-to-grow** (pure-click);
  in tm5x it is **walk-to-deposit + polarity-flip**.
- **vs vd3g.** vd3g's flow rule is **gravity along binary
  high/low terrain** — marbles cascade downhill until obstructed;
  the field is `(elevation, marble-position)`. tm5x has neither
  gravity nor marbles; the diffusion is symmetric in all four
  cardinal directions, not biased downward. Furthermore, the
  player verb in vd3g is **click-to-toggle-terrain** (pure-click)
  and in tm5x it is **walk-and-flip-polarity**.
- **vs mr5q.** mr5q's polarity is on **pawns** (yang/yin avatars
  that walk on attraction); tm5x's polarity is on the **single
  pawn's deposit-stamp**. mr5q has no field-of-cell-state — the
  field is just walls + targets; the dynamic is pawn locomotion
  + adjacent-discharge. tm5x has a full integer scalar field that
  every cell carries.

### Negative similarity check (`negative-similarity-check.md`)

Walked the 8 dimensions against the strongest neighbours
(pf3w, kp9z, gv47, vd3g) and the L1 screenshots actually opened
above:

| Dimension | tm5x candidate | pf3w | kp9z | gv47 | vd3g |
|---|---|---|---|---|---|
| 1. What is on the board | Pawn + small target rings on a smooth-gradient temperature field | Pre-placed emitter slots + receiver squares on flat ground | Grid of cells with grain dots accumulating in cells | Yellow seed regions with dark pips | Dotted high/low terrain + marbles + small anchors |
| 2. Player physical input | Walk pawn with arrows + ACTION5 polarity-toggle | Click to activate slots + ACTION5 to tick world | Click to drop grains + click-rotate redirectors | Click seeds to grow + ACTION5 region-mix | Click cells to toggle high/low |
| 3. Level asks for | Each target ring's cell value matches a target value at the same tick | Frontier coincidence with receivers on a single tick | Sinks absorb required count of grains | Surround pips of matching colour | Marbles flow into goal cells |
| 4. What kills | Step counter | Step counter | Step counter | Step counter | Step counter |
| 5. Cast of supporting | Ring-targets, optional walls (L3) | Slots + receivers + ACTION5 | Sources + sinks + redirectors | Seeds + pips + walls | Anchors + marbles + walls |
| 6. Visual signature | Smooth gradient colour-fill across whole field (palette {4,10,0,7,8}) | Discrete frontier squares appear on flat grey ground | Discrete grain dots in dark-bordered cells | Solid yellow regions on grey | Black/grey dotted texture |
| 7. Pixel grain | Pawn with internal pip; rings 4-cell wide; cells ≥4×4 with internal gradient values | Slots and receivers are 3×3 framed boxes; ground is flat grey | 4×4 cells with single-pixel grain dots | Larger blocky regions, dark pips | Heavy dot-texture on every cell |
| 8. Core dynamic | "Deposit heat/cold and let it diffuse smoothly across the field; targets must hit values at the right tick" | "Activate emitters and tick wavefronts to converge on receivers" | "Drop grains and let them topple at capacity" | "Grow seed regions to surround pips" | "Mould terrain so marbles roll to goals" |

**No prior shares 3+ dimensions** with the candidate. The
strongest near-miss is pf3w (shares dimensions 4 (kill: step
counter — too universal to count strongly) and a faint nod on
dimension 8 (both involve "field changes globally per tick"). Even
that overlap is only ~1.5 dimensions — visually pf3w renders
discrete frontier squares, the candidate renders a smooth
temperature gradient. Cell rule (BFS-frontier vs averaging) and
player verb (click-only vs walk+polarity-toggle) diverge.

**No rejection.** The candidate is genuinely visually and
dynamically distinct from every prior. Verdict: **NOVEL**.

### Core-knowledge prior categories (`design-constraints/core-knowledge-priors.md`)

The mechanic draws from:

- **Objectness** — the pawn is a coherent avatar; target rings are
  persistent objects.
- **Basic physics** — diffusion is a recognisable physical analogue
  (heat smoothing, ink spreading); intuitive for humans.
- **Basic geometry & topology** — at L3, insulator walls partition
  the field; the player reasons about connected sub-regions of the
  diffusion graph.

Three of the four §3.4 categories. Agentness is intentionally NOT
part of the core mechanic — there are no chasing NPCs. Three out
of four is in the strong sweet spot named in
`core-knowledge-priors.md`.

## action palette
`available_actions = [1, 2, 3, 4, 5]`

- ACTION1-4: walk pawn one cell (cardinal).
- ACTION5: toggle pawn polarity hot ↔ cold (the distinctive verb,
  per `global/action-enum.md`'s ACTION5 freedom-slot guidance).
- No ACTION6 (click) — the playfield is fully arrow-driven, which
  is intentionally a different action shape from pf3w / kp9z /
  gv47 / vd3g (all click-only or click-heavy).
- No ACTION7 (undo) — only ~6/25 reference games use undo, and
  thermal diffusion's planning rewards forward-look not rewinding.

## visual / palette plan

Dominant palette: `{4 off-black, 10 light-blue, 0 white, 7 pink,
8 red}` — the temperature gradient. Plus `{14 green}` for
target-ring outlines and `{6 magenta}` for the pawn's polarity-
indicator pip (magenta-when-hot, palette-9 blue when cold). HUD
step-counter on row 0 in `{5 black, 0 white}` minimal.

Different palette signature from `kf42 → vh68`'s cautionary
`{4 wall, 8 red, 9 blue}`. Different from kp9z (greys + maroon).
Different from gv47 (yellow + grey). Different from pf3w (greys
+ light blue). Distinct.

## summary

`tm5x` — Thermal-Diffusion Blend. The first tm5x run is by hand
in this harness (autonomous, no seed). All similarity checks
pass; mechanic is novel against both the 25-game taxonomy and
all 29 prior generated games; both positive and negative
similarity tests are clean. Action palette `[1,2,3,4,5]`. Three
core-knowledge categories engaged (objectness + physics +
geometry/topology). Composition: L1 = walk-and-stamp; L2 = + 
polarity-toggle; L3 = + insulating walls.
