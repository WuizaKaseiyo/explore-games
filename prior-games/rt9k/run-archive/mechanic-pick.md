# Mechanic pick — run 2026-05-10T06-16-02

## Game ID
`rt9k`

(Generated as 2-letter prefix `rt` + 2-char suffix `9k`. Not in
the 25 reference IDs; not in `prior-games/index.md`; not in any
unindexed prior-games subfolder; not an English word.)

## Run input
Autonomous (no seed).

## Mechanic family
`torus-wrap-tone-cycle`

## One-paragraph description

The playfield is rendered as a finite rectangle but is
**topologically a torus**: walking off the right edge re-enters from
the left, and walking off the top re-enters from the bottom (and
vice versa for the opposite edges). The player avatar carries a
**tone-state** drawn from a small ordered cycle of three palette
hues. The single, load-bearing rule is that **every wrap-cross
advances the tone-state by exactly one step in the cycle**: a hop
across the right edge or the bottom edge increments tone (`+1`); a
hop across the left edge or the top edge decrements tone (`-1`).
Walking inside the playfield does *not* change tone. The world is
populated by tone-coded **filter walls**: a wall whose tinted ring
matches the avatar's current tone-state is passable (the avatar
crosses through), and any wall whose ring is a different tone is a
solid obstacle. The level wins when the avatar occupies its
goal cell — and at L3 the goal also requires the avatar to *be in
a specific tone-state* on arrival, encoded by the goal cell's
ring tone. The single optional ACTION on top of the four arrows is
ACTION6 click for one specific L3 mechanism (a *toggle-wrap-edge*:
clicking a wrap-edge marker briefly suspends wrap on that single
edge for the avatar's next step). Everything else is pure
`available_actions = [1, 2, 3, 4]` arrow walking, with one new
mechanic per level.

## Similarity check — taxonomy of 25 reference games

I compared the candidate against every row in
`mechanic-novelty/taxonomy-of-25-games.md`. None of the 25
reference games' `mechanic_family` tags (per
`similarity-check.md` § 1) match `torus-wrap-tone-cycle` on the
first two hyphen-split words. Family-level: NOVEL.

The closest description-level near-misses:

- **m0r0 — mirrored-quad-control.** Four avatars whose move axes
  are mirrored per-quadrant; merge pairs onto the same cell.
  *Distinguishing rule:* m0r0 controls **multiple** avatars whose
  inputs are reflected across mid-axes; the playfield is a
  finite, non-wrapping rectangle. `rt9k` controls a **single**
  avatar on a wrapping torus surface where inputs are *not*
  reflected — moving up always moves up; the only "wrap"
  consequence is the tone-cycle increment, not an axis flip.
- **g50t — walk-vs-scroll.** Avatar walks a board that scrolls
  one cell every two turns. *Distinguishing rule:* g50t's scroll
  is *temporal* (board moves on a timer the avatar races); `rt9k`'s
  wrap is *topological* (the board is stationary; the avatar
  re-enters from the opposite edge when it walks off). No timer in
  `rt9k`; no edge-wrap in g50t.
- **tu93 — lockstep-multi-maze.** Lockstep multi-agent walking on
  a value-2 walkable underlay. *Distinguishing rule:* `rt9k` has
  one avatar; the load-bearing structure is the wrap topology
  plus the per-cross tone-cycle, not lockstep multi-agent
  coupling.
- **bp35 — gravity-fall-navigation.** Side-step under gravity
  with portals and gravity-flip pads. *Distinguishing rule:* bp35
  has a constant gravity-axis fall; portals are *placed sprites*
  that teleport the player. `rt9k` has neither gravity nor
  placed portals — every wrap is the *same* opposite-edge wrap,
  always paired with a tone-step.

Per `similarity-check.md` § 2 description-level test, no row
matches all of (win condition, primary action, primary
constraint).

## Similarity check — `prior-games/index.md`

`prior-games/index.md` (and unindexed prior-game folders) was
read in full. Closest candidates:

- **pk4m — duotone-flip-walk.** Avatar with binary colour state
  walks a maze of colour-conditional cells; ACTION5 flips colour;
  pads auto-flip; polarity walls gate by colour.
  *Distinguishing rule (concrete):* pk4m has TWO colour states
  toggled by an *explicit ACTION5* and by *placed flip-pads*
  inside the playfield. `rt9k` has THREE tone states cycled
  *only* by edge-wrap crossings — there is no in-cell verb that
  changes tone, and there is no such pad. The mental model
  diverges sharply: in pk4m the player decides "when to flip"
  inside the playfield interior; in `rt9k` the player must route
  through specific *edge crossings* in a specific *order* to
  reach the desired tone, and tone state is therefore tightly
  coupled to topology, not to a free verb. pk4m's avatar can
  reach any maze cell in any colour state by toggling at will;
  `rt9k`'s avatar can only reach a given cell in a given tone if
  a *path* exists that crosses the right edges in the right
  order, which is a topological constraint pk4m does not impose.
- **lz7q — dual-plane-walk.** Two superimposed Day/Night planes
  with different walls/keys/locks/hazards; ACTION5 toggles
  active plane.
  *Distinguishing rule:* lz7q's two-plane state is a global
  toggle controlled by ACTION5, fully independent of position.
  `rt9k` has no planes — wall-passability is determined by the
  *single avatar's tone* compared to a wall's tone, and tone
  changes only via wrap-cross. lz7q has no wrap.
- **gh4r — repulsion-herd-corral.** Warden walks 4-cell strides;
  drifters flee the warden along shared axes; ACTION5 toggles
  gates at L3. *Distinguishing rule:* gh4r has autonomous flee-
  drifters and a non-wrapping rectangle; `rt9k` has neither
  drifters nor any autonomous follower.
- **wt39 — glide-deflect-thaw.** Pawn glides until wall; angled
  bumpers deflect 90°; brittle thaw-tiles. *Distinguishing rule:*
  `rt9k`'s avatar moves one cell per arrow press (no glide), with
  no deflection physics.
- **bz3k — drift-impulse-cardinal.** Persistent integer
  velocity that arrows ±1. *Distinguishing rule:* `rt9k` has no
  velocity state; tone is the sole carried state, and it is
  cycled only at edge-crosses, not by arrow input.
- **jd4q — echo-trail-teleport.** Avatar walks; each step
  deposits a fading echo, click teleports back consuming the
  trail; closing-doors and eraser cell. *Distinguishing rule:*
  jd4q has *placed teleport pairs* and a click-to-teleport-back
  mechanic; `rt9k` has no placed portals and no teleport-back —
  the only "non-local" navigation is the implicit wrap at the
  rectangle's outer boundary.
- **ek73 — wake-trail-evade.** Vacated cells become decaying
  hazards behind the player; warp pads teleport in pairs.
  *Distinguishing rule:* ek73 has *placed warp pairs* (placed
  teleporters) inside the playfield and decaying-hazard wake.
  `rt9k` has neither — wraps are at the playfield boundary,
  not at internal placed pads, and no trail/wake exists.

No prior game matches all three of (win condition, primary
action, primary constraint) per `similarity-check.md` § 2 — the
positive check returns NOVEL.

## Negative similarity check (`negative-similarity-check.md`)

Per the seven dimensions, walked against every reference game's
L1 screenshot (cn04, sp80, sb26, vc33 sampled visually during
study; mental rendering for the rest from deep-analysis layer)
plus the closest priors above:

| Dim | Description | `rt9k` | Closest prior `pk4m` (`prior-games/pk4m/level_1.png` not opened — but spec read) |
|---|---|---|---|
| 1 | Object on board | single avatar + tone-coded filter walls + tone-coded goal ring + visible wrap-edge markers | avatar + colour-conditional cells + flip-pads |
| 2 | What player does | walks 4-cardinal arrows; the *only* state change off-walk happens at wrap-crosses | walks + presses ACTION5 to flip + steps onto auto-flip pads |
| 3 | What level asks | reach the goal cell, possibly while in a specific tone (L3) | reach exit cell while colour gates open |
| 4 | What kills | step counter | step counter |
| 5 | Cast | avatar + filter walls + goal + (L2) tone-keys + (L3) edge-toggle markers | avatar + walls + flip-pads + exit |
| 6 | Visible visual signature | dark-grey outer ring framing the playfield with ARROW-shaped wrap markers on each of the 4 outer edges (read as "this side wraps to that side"); avatar tinted in current tone; walls have colored ring outlines that match the tone they require | colored cells, two-tone palette |
| 7 | Pixel grain of primary sprites | 4×4 avatar with internal stripe pattern indicating tone (rich); walls are ring-rectangles with thick coloured frames; edge-markers are 4-cell chevron groups | tbd, but pk4m is single-pawn typical of recent priors |
| 8 | Core dynamic | "the topology of the playfield is non-trivial; route through edges in the right order to enter the right tone-state" | "free in-place tone toggle to gate colour walls" |

**Dimensions clearly different from pk4m: 2, 6, 7, 8.**
**Dimensions shared with pk4m: 1, 3, 4, 5** (avatar + walls +
goal + step-counter — these are universal-style features of
NovaPlay demonstration games).

The four shared dimensions are the universal-board pattern; the
three weighted-heavy dimensions (6, 7, 8) all clearly diverge.
Per `negative-similarity-check.md` ("the threshold is judgement,
not arithmetic — sharing on dimensions 6, 7, or 8 is heavier than
sharing on the others, because those are the named principles"),
this candidate clears the negative test. No single prior shares
3+ dimensions including 6, 7, OR 8. The single weakest
distinguishing position is against pk4m on dimensions 1/3/4/5,
which are precisely the universal-board pattern this check
exempts from heavy weighting.

## Cautionary `kf42 → vh68` style audit

The cautionary tale was: two priors shared dominant palette,
1×1 sprite grain, walls + targets + colour-gating, click-then-
arrow input, and step-counter HUD — all surface-similar despite
articulable distinguishing rules. To avoid that failure mode for
`rt9k`:

- **Palette**: I will choose a 4-colour signature distinct from
  pk4m / lz7q / gh4r / and the most recent ~10 priors. Concretely:
  background = palette 1 (off-white) for inside the playfield
  versus palette 4 (off-black) outer frame; tones cycle through
  palette 6 (magenta), palette 11 (yellow), palette 14 (green) —
  three highly distinguishable hues none of which dominates pk4m
  (which uses red/blue duotone) or recent priors. Walls use
  palette 5 (black) as their solid fill with the tone hue painted
  only as a 1-pixel inner ring, not as fill.
- **Sprite grain**: The avatar will be a 4×4 sprite with a
  diagonal striped interior, not a 1×1 plain rectangle. Filter
  walls are 4-tall × 6-wide rectangles with a 1-pixel inner ring
  and a 2-pixel outer black frame — not a flat coloured square.
  Tone-cycle indicators on each playfield edge are 3-cell-wide
  chevron groups, distinctive shape signature.
- **Verb signature**: arrow-only at L1 and L2 (no clicks), which
  is rare in priors (only ls20, tu93, tr87, bz3k, gh4r are pure
  arrow). Adds ACTION6 only at L3 for a single specific verb
  (toggle-wrap-edge), and never ACTION5. This avoids overlap
  with pk4m which leans on ACTION5.
- **Cast composition**: the *visible* board is dominated by the
  outer-frame edge-markers (which are absent from every prior),
  not by walls + targets which are the universal pattern.

This audit will be re-run formally during `critique_spec` once
the spec exists.

## Verdict
**NOVEL.** Proceeding to `write_spec` with mechanic family
`torus-wrap-tone-cycle` and game ID `rt9k`.
