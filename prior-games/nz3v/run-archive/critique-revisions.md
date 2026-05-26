# Critique revisions for nz3v mechanic-spec.md

After adversarial review against `design-constraints/checklist.md`
and `mechanic-novelty/{similarity,negative-similarity}-check.md`,
the spec fails on several gates. Issues below — each numbered,
each cites the violated rule, the spec section/quote, and a
concrete fix.

## 1. Item 7 (forbidden elements) / Item 21 (UI teaches role) — sprite shapes risk reading as letters

**Rule**: `forbidden-elements.md` forbids "letters of any
alphabet" as visual elements; `checklist.md` item 7 is the
binary check; item 21 says "Sprite UI ≈ sprite role" with the
visual not lying about the role.

**Offending spec section** (§3 Sprite roster):
- *avatar*: "a 5×5 chevron with palette 10 (light-blue) outline"
- *stop_tile*: "an X-cross (palette 12 orange diagonals) on a palette 4 (off-black) background"

**Why it's a violation**: A 5×5 chevron unambiguously reads as
the symbol `>` or `V` (depending on orientation) — both are
recognisable directional / arrow / letter glyphs. An X-cross
unambiguously reads as the Latin letter `X` regardless of
intent. Per `forbidden-elements.md`: "a sprite that unambiguously
reads as a digit '1' is not [allowed]" — same rule applies to
letters.

**Fix**:
- *avatar*: redesign to a non-arrow, non-letter shape. Suggested:
  a 5×5 hollow square with two diagonal corner pixels removed
  (an "octagonal" footprint), palette-10 outer ring around a
  palette-0 inner cell. Reads as "small polygonal figure", not
  any letter.
- *stop_tile*: redesign to a non-letter shape. Suggested: a 5×5
  square frame in palette 12 (orange) with a smaller filled 3×3
  palette 12 square *inside it* offset to one corner — i.e., a
  framed-block. Reads as "a fixture / target / region marker",
  not the letter X. Alternative: 5×5 dot-grid (palette 12 dots
  at the four edge-centre cells: top/bottom/left/right; centre
  empty) — reads as a "+" topological cross which the
  forbidden-elements file explicitly *allows* ("a vertical bar
  with two horizontal cross-strokes forming a '+' is fine — it's
  a topological symbol, not a letter").

The counter_switch's "magenta spiral" reading is fine (not a
letter; reads as a curl/loop topology). Walls' "cross-hatch" is
fine. Target's hollow ring is fine.

## 2. Item 19 (no hidden state) — _direction has no persistent visual cue

**Rule**: `checklist.md` item 19: "For every piece of game state
the player needs to reason about and that is mutated by an
action, does the spec name the persistent visual cue that
surfaces it for as long as the state is in effect?"

**Offending spec sections**:
- §6 lists `_direction: int ∈ {+1, -1}` as internal state.
- §6 mentions `RotorNotchOverlay` and `WedgeOverlay` but neither
  shows direction.
- §4 L3 difficulty justification says "the rotor's notch — which
  had been advancing clockwise — visibly reverses direction on
  the next rotation". This makes direction inferable *over time*
  (by watching which sector the notch goes to next), but the
  current frame at any moment doesn't tell the player the
  current direction; the player has to remember history.

**Why it's a violation**: If the player looks at any single
rendered frame, they cannot tell whether the rotor is currently
in clockwise or counter-clockwise mode — only the history of
notch positions over multiple frames betrays direction. The
state is "hidden" in the per-frame sense.

**Fix**: Add a persistent cue tied to `_direction`. Suggested
implementation: the rotor sprite has a *secondary directional
mark* — a small palette-11 (yellow) dot at the rotor's
clockwise-next-corner position (when direction is +1, the dot
sits in the cell adjacent to the lit notch on the clockwise
side; when direction is -1, the dot moves to the counter-
clockwise side). This dot is drawn by extending the rotor
sprite's pixel pattern, or via a dedicated `DirectionMarker`
overlay. The dot's position on the rotor body unambiguously
reads as "the notch will next move toward this side". Spec must
explicitly name this cue in §6 (HUD widgets) and §3 (rotor
sprite description).

## 3. Item 19 — _frozen_remaining has no persistent visual cue

**Same rule as #2.**

**Offending spec section**:
- §6 lists `_frozen_remaining: int` as internal state.
- §4 L2 says "they observe the wedge does NOT rotate on the
  next action". This is an *event* cue (you notice the wedge
  didn't move), not a persistent cue (does the player know
  RIGHT NOW whether they're frozen and how many frozen actions
  remain?).

**Why it's a violation**: An attentive player who steps on the
stop-tile, then on the next action sees the wedge stayed put,
might guess "freeze active". But two actions later, if they
wonder "is freeze still on?" they have to wait another action
and watch. That's reasoning-about-history, not a per-frame cue.

**Fix**: Add a persistent visual indicator for freeze state.
Two options:
- (a) The wedge tint colour shifts when frozen — palette 11
  (yellow) → palette 7 (pink) for the duration of freeze.
  Discrete, unmissable colour signal. Pulses or holds steady.
  When freeze ends, returns to yellow.
- (b) The rotor sprite's outline gets a "frozen frame" — a
  palette 9 (blue) ring around the rotor while frozen, removed
  when freeze ends.

Either works. (a) is more economical (uses existing wedge
overlay; just remap palette). Spec §6 must name the chosen cue.

## 4. Item 20 (don't generate low-resolution game) — uniform-yellow wedge fills ~35 cells in flat colour

**Rule**: `checklist.md` item 20: "Don't pick a small logical
grid (12×12, 14×14, 16×16, etc.) that the engine then scales
up into chunky uniform-colour cell-blocks; a chunky upscaled
grid wastes most of the available pixel budget and makes the
rendering read as crude."

**Offending spec section**: §4 says
"a `WedgeOverlay(RenderableUserDisplay)` HUD widget repaints
background-coloured pixels (palette 4) inside the current
sector to **palette 11 (yellow)**".

**Why it's a violation**: 12×12 grid; one quadrant ≈ 35
non-rotor cells; each cell renders at 5×5 = 25 px; uniform
palette-11 fill = 35 × 25 = 875 px of flat-yellow blocks. Per
checklist 20: imagine showing the rendered L1 frame to someone
who has never seen the game — does the rendering look detailed
and considered, or like coarse coloured blocks pasted on a
grid? The current spec produces the latter for the wedge area.

**Fix** (spec must adopt one): 
- (a) **Internal pattern in lit cells**: instead of repainting
  every pixel of every lit cell to palette 11, paint a 5×5
  *pattern* that signals "lit" without flat fill. E.g., a 5×5
  cell rendered as palette 4 background + palette 11 dots at
  the 4 corner pixels (a 4-dot accent per cell) — the cell
  visibly reads as "tinted with a four-dot mark", not flat
  yellow. The pattern is visible across the wedge area as a
  textured zone.
- (b) **Gradient by distance**: each lit cell's repaint uses
  palette 11 (closer to rotor) or palette 12 (farther), with
  a discrete band per ring of distance. Two-band gradient
  reads as "wedge has structure". 
- (c) **Border outline only**: paint only the BORDER pixels of
  each lit cell in palette 11, leaving cell centres at
  background palette 4. The wedge reads as a tessellated grid
  pattern.

Option (a) is closest to the lq5x precedent (which uses
"palette 1 off-white" for lit but on a small cell area; the
fill is visually busy because the cone is small). nz3v's wedge
is much larger so option (a)'s textured fill is more important.

Spec §4 must specify which option is used.

## 5. Item 12 (counterfactual necessity) / spec readability — L3 §4 contains intermediate-draft attempts inline

**Rule**: `checklist.md` item 12: "The critique must produce a
**per-mechanic table** with one row per (mechanic, level)
pair... Verify by enumeration, not by abstraction." This
implies the spec itself must present a *single canonical*
witness path that the critique can verify against; an internal
contradiction in the spec invalidates the per-mechanic
counterfactual table.

**Offending spec section**: §4 Level 3 contains *three*
witness traces in sequence — the first ends with a wall-
collision issue, the second labels target as `(3, 10)` but
ends at `(1, 10)`, the third ("L3 layout (final)") is the
intended canonical version. The intermediate drafts are
labelled inline (`*Re-trace*: Avatar at (3, 3) action 4...`,
`*— hmm this routing is failing the path...*`). A reader
cannot tell at a glance which is canonical.

**Why it's a violation**: A reviewer or implementer reading §4
encounters contradictory data and has no way to verify the
counterfactual without back-solving which trace is canonical.

**Fix**: §4 Level 3 must be rewritten to contain only the
final canonical layout and witness — no intermediate drafts,
no inline editorial. The final layout is:
- avatar at (1, 1)
- target at (1, 10)
- walls at (3, 1), (3, 2), (3, 4)
- stop-tile at (2, 3)
- counter-rotation switch at (4, 5)
- step budget 22 (subject to revision per critique #6)
- witness: 15 actions (sequence specified in revision target)

Drop everything else from §4 Level 3.

## 6. Difficulty rules § d (step budget non-decreasing) — L2 budget shrinks from L1

**Rule**: `difficulty-rules.md` § d / `checklist.md` item 18.d:
"Be generous — give the player comfortable room over the witness
length to explore the mechanic"; per-level addendum for L3:
"the budget must NOT shrink relative to the witness as level
number rises — later levels add mechanics and therefore *more*
discovery cost, not less, so they need *more* exploration room."

**Offending spec sections**:
- L1: step budget 28 (witness 18, slack 10).
- L2: step budget 22 (witness 15, slack 7).
- L3: step budget 22 (witness 15, slack 7).

**Why it's a violation**: The intent of the addendum is that
later levels have *more* discovery cost (new mechanic to learn)
and therefore should have *more* exploration room. L2's budget
of 22 is *less* than L1's 28 — directly opposite to the rule's
spirit. L2 has a NEW mechanic (M2 = stop-tile) that the player
must discover by trial; the budget should reflect MORE discovery
room, not less.

**Fix** (and interaction with critique #4 + counterfactuals):

- Increase L2 budget from 22 to **30** (witness 15 + 15 slack)
  — comfortable exploration room for M2 discovery.
- Increase L3 budget. But L3 must keep the budget *below* the
  shortest M3-bypassing path, otherwise M3 isn't strictly
  required (item 12 violation).

  Currently L3's clockwise-only path (with M2 freeze) takes ≥
  ~28 actions per the counterfactual analysis. So budget 30
  (≥ L2's 30) would NOT force M3.

  **Two compatible fixes**:
  - (i) Add walls in NE/SE/SW that force the clockwise-only
    path to ≥ 35 actions (so budget 30 can't accommodate it
    while M3-witness 15 fits with 15 slack).
  - (ii) Lengthen L3 witness by adding a second target / a
    secondary objective that takes more actions, while M3 still
    halves the sweep transitions; budget 30 fits the M3 path
    but not the no-M3 path.

  (i) is simpler. Add walls at:
  - (8, 2), (9, 2), (10, 2) in NE — block direct east traversal
    in NE upper rows.
  - (8, 9), (9, 9), (10, 9) in SE — block direct east at gy=9.
  - (1, 8), (2, 8) in SW — extend SW navigation.
  Total clockwise-only path lengths after these walls:
  approx 35+ actions (rough estimate; spec must verify).

  Then set L3 budget to 30 (≥ L2's 30; ≥ witness 15). M3
  still strictly required because clockwise alternative > 30.

Spec §4 Level 3 must be rewritten to (a) include these
additional walls, (b) update the step budget to 30, (c)
re-derive the counterfactual analysis showing clockwise-only
takes > 30 actions.

## 7. (Minor) §4 L3 trace had wall-collision moments inline — clean up

This is encompassed by critique #5 (rewrite L3). When rewriting,
verify every move's destination is not blocked by a wall or
the rotor; the witness must be valid. Specifically:

- Wall at (3, 4) is in the L3 layout — the witness path must
  not attempt `(3, 3) → (3, 4)`. Current witness (action 5)
  goes `(3, 3) → (4, 3)` which is fine (no wall at (4, 3) per
  the final L3 layout). Verify the rewritten witness similarly.

## 8. (Minor) §4 L1 — `step_budget` justification too narrow

Currently: "step budget = 28 (witness 18 + 10 slack)". Slack 10
on a witness of 18 is generous (~55%). But per the
non-decreasing rule, L1 should not be the largest. After
critique #6, L1 budget 28 ≤ L2 budget 30 ≤ L3 budget 30 — the
ordering is fine. Keep L1 at 28.

---

## Summary

8 issues identified. Fix by:

| # | Section | Fix |
|---|---|---|
| 1 | §3 sprite roster | redesign avatar (octagon) and stop-tile (4-edge dots or framed-block) — non-letter shapes |
| 2 | §3 sprite roster + §6 HUD | add persistent direction-cue (rotor secondary marker dot) |
| 3 | §6 HUD | add persistent freeze cue (wedge tint shift palette 11 → palette 7 while frozen) |
| 4 | §4 wedge rendering | adopt textured/dotted pattern for lit cells, not flat-fill |
| 5 | §4 L3 | rewrite cleanly: only the final layout + witness; drop intermediate drafts |
| 6 | §4 L1/L2/L3 budgets + L3 walls | budgets non-decreasing (28, 30, 30); add walls in NE/SE forcing clockwise-only > 30 |
| 7 | §4 L3 witness | verify every move's destination is unblocked under final layout |
| 8 | (minor, encompassed in #6) | L1 budget OK once #6 ordering is fixed |

Transition back to `write_spec` for revision (visit count 1 of 10).
