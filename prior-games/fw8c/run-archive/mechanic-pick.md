# Mechanic pick

## Game ID
**`fw8c`**

Verified against:
- Reserved 25 reference IDs (`code/id-generation.md`): not present.
- `prior-games/index.md` (66 entries reviewed): not present.
- English-word check: "fw8c" is not a recognisable word.
- Lowercase + alphanumeric: yes.

## Mechanic family tag
**`pigment-mix-walk`**

## One-paragraph description
The avatar is a single hollow-bodied "carrier" pawn that walks a chamber of  
pigment-pad tiles via cardinal arrow keys. Each pigment pad is one of three  
distinct accent colours (orange / pink / light-blue). When the carrier steps  
onto a pigment pad, the pad's colour is **OR'ed into the carrier's stored set**  
(the carrier's body re-tints to the resulting mixture per a fixed deterministic  
mixing table, e.g. orange+pink → magenta, orange+light-blue → green,  
all three → black, no pigment held → off-white). Stored pigment sets persist  
across moves until cleared. The carrier delivers its current mixture to  
"slot" sprites that demand a specific colour: stepping onto a slot whose  
demanded colour matches the carrier's current mixture *consumes* the slot  
(it dims to the background) **and clears the carrier's pigment set back to  
empty**. ACTION5 = manually purge the carrier's pigment set without  
consuming a slot (used to recover from a wrong pickup).  

The win condition for a level is "every slot has been consumed". The lose  
condition is the universal step-counter HUD draining to zero. The mechanic  
draws on **objectness** (carrier + pads + slots are persistent objects with  
fixed effects) and **basic geometry/topology** (the spatial layout of pads  
and slots forces the player to plan which pickup-order yields which mixture  
at which slot — a connectivity / routing problem in colour-set space).

## Prior-art comparison

### Taxonomy near-misses (the 25 reference games)

`ls20` — *cycler-attribute-match*. **Family-level overlap:** both involve  
the avatar's state (colour) being mutated by stepping on tiles, with a  
target match required at goal pellets. **Distinguishing rule (concrete):**  
ls20 cycles three INDEPENDENT enum dimensions (shape index, hue index,  
rotation index) through fixed enumerated alphabets, where each cycler-tile  
bumps EXACTLY ONE index by ±1; the target is reached by hitting the right  
sequence of cyclers in the right order, and the per-pellet target is  
*equality on three independent enums*. `fw8c`'s state is a **3-bit subset**  
of {orange, pink, light-blue} closed under union, not a tuple of three  
independent cycled values; the mixing table is non-monotonic (pickups  
*combine* into novel third colours rather than walking a fixed alphabet),  
and the order of pickups is irrelevant since OR is commutative — the  
puzzle is which **pad-set** to visit en route, not which sequence-of-cycles  
to walk through.

`re86` — *frame-paint-canvas*. **Family-level overlap:** "paint" appears  
in both. **Distinguishing rule:** re86's marker DEPOSITS its colour onto  
the canvas at every step (the canvas accumulates a target-image painting);  
the win is image equality. `fw8c` has no canvas — pigment lives ON the  
carrier (not on the floor), and pads are pickup sources whose pixel state  
does not change.

`sc25` — *spell-grid-pattern*. The 3×3 spell-slot lets the player pre-  
combine bits, then auto-cast. **Distinguishing rule:** sc25 selects a single  
DISCRETE spell from a tiny enum (~3 spells per level) by toggling exactly  
the right bits; my pigment set is read DIRECTLY (the union determines  
which colour-slot it can consume), there is no separate "cast" step, and  
the carrier carries the same set across many move-actions.

### Prior-games near-misses (`prior-games/index.md`, 66 entries)

`hr8q` — *pair-blend-recipe*. **Family-level overlap:** "blend" in both  
descriptions. **Distinguishing rule:** hr8q's verb is **pair-click** —  
the player picks two (or three at L3) ingredient sprites and fills a  
formula widget which then consumes a target. `fw8c`'s verb is **walk-into-pad**  
— pigment is collected by *spatial traversal* of an integrated chamber, so  
the puzzle has a routing/topology layer (which pads are reachable in  
which order under wall constraints) on top of the colour-set arithmetic.  
hr8q has no spatial-routing pressure on the ingredient pickup.

`tm5x` — *thermal-aura-imprint*. **Family-level overlap:** the avatar  
imprints state on cells. **Distinguishing rule:** tm5x has an avatar  
that imprints temperature on the *cell + neighbours*, with ACTION5 to  
toggle polarity; targets latch when their cell reads the required value.  
`fw8c` does not modify pads or slots from the avatar's side — pads stay  
put as pickup sources, the carrier accumulates into ITSELF, and slot  
consumption is at-step-of-arrival not via stamping. Different state  
flow direction (board → carrier vs. carrier → board).

`pk4m` — *duotone-flip-walk*. The avatar has a binary colour state and  
walks colour-conditional cells. **Distinguishing rule:** pk4m's avatar  
has only **2 states** (a single bit toggled by pads / ACTION5) and the  
mechanic is gating-of-cells (polarity walls block by colour). `fw8c`'s  
state space is **8 states** (the powerset of 3 pigments), pads are  
pickup-only (no toggle/flip), and slots are *destination filters* not  
mid-path gates.

`pf3w` — *wavefront-converge-timing*, `gv47` — *seed-grow-surround-dissolve*,  
`bx84` — *beam-mirror-reflect*: all involve coloured propagation but  
through *world-state* (cells / wavefronts / beams), not through the  
carrier's pocket-state. None matches the walking-aggregator + slot-consume  
verb pair.

### Negative similarity (`negative-similarity-check.md`) — 7-dimension scan

Worst overlap is with **ls20** (same family of "avatar walks pickup-tiles  
to alter own state, must visit goal-pads matching current state"):

| Dimension | ls20 | fw8c | Shared? |
|---|---|---|---|
| 1. What's on the board | walls + cycler tiles + pellets + enemies | walls + pigment pads + colour slots | partial — both have walls + pickup tiles + targets, but ls20 has enemies+bullets, fw8c has neither |
| 2. Player physical input | walks 5-pixel hops with arrows | walks cell-stride hops with arrows | yes — pure-arrow walking |
| 3. What the level asks | claim each pellet in goal-order with matching avatar state | consume each slot with matching pigment set | yes — visit each goal-tile with right state |
| 4. What kills the player | bullets (3 lives) + step counter | step counter only | no — fw8c has no enemies/projectiles |
| 5. Cast of supporting elements | shape-cyclers, colour-cyclers, rotation-cyclers, enemies | pigment pads × 3 colours, slots × up to 7 colours | no — different supporting sprite kinds |
| 6. Visible visual signature | magenta-yellow avatar on grid maze with cycler tiles | hollow-bodied carrier on chamber with three accent-colour pads + colour-slots in the slot-rim signature; palette {orange-12, pink-7, light-blue-10, magenta-6, green-14, purple-15, off-white-1, light-grey-2} | no — fw8c specifically AVOIDS the {red-8, blue-9, white-0} signature; reaches for a non-RGB primary palette |
| 7. Pixel grain of primary sprites | small (avatar 5px, cycler tiles ~5px) | larger (carrier with internal hollow-body pattern; pad with concentric ring around centre dot; slot with thick colour-rim and dim interior) | no — fw8c invests in internal pixel structure per checklist 20 |
| 8. Core dynamic | "tweak three independent enum dimensions through ordered cycler visits" | "accumulate into 3-bit colour SET via subset-union, deliver to slot, clear, repeat" | no — discrete enum cycling vs. powerset-union accumulation; the *thing the player thinks about* differs (which-cycle-sequence vs. which-pickup-subset) |

Shared dimensions: 2, 3 (and 1 partial). That's 2 hard hits; well below the  
3-dimension threshold the negative test sets. Reject-reason **does not fire**.

Cross-checking against any other prior reaches at most 2 shared dimensions  
(input style + step-counter HUD), which are universal across the 25  
reference games and most of the prior-games corpus — they're soft  
norms, not novelty signals.

## Why this passes §3.4 priors

- **Objectness**: the carrier, pads, and slots are persistent first-class  
  sprites; pickup-OR is a clear mutation.
- **Basic geometry/topology**: a chamber's wall structure constrains  
  which pad-subsets are reachable in which order; routing through the  
  pigment graph is the planning load.
- **Basic physics**: not strictly used (no gravity, momentum, friction).  
  This is fine — "most strong NovaPlay mechanics combine 2-3 categories"  
  per `core-knowledge-priors.md`; using objectness + topology cleanly is  
  acceptable.
- **Agentness**: not used in L1/L2; if a chaser is added at L3 it would  
  add this prior. (Decision deferred to `write_spec`.)

## Why this passes forbidden-elements

- No letters, digits as glyphs, or alphanumeric symbols anywhere.
- No real-world clipart — pads are concentric-ring pickups, slots are  
  thick-rim hollow-frames, carrier is a hollow body with a colour-fill  
  centre. None resembles a known real-world object beyond abstraction.
- No cultural conventions:
  - The pigment palette intentionally avoids the {red-8, blue-9, green-14}  
    "primary" triple that carries cultural mixing intuition; uses  
    {orange-12, pink-7, light-blue-10} as inputs and  
    {magenta-6, green-14, purple-15, black-5} as the mixed-state outputs.  
    Mixing rules are *deterministic* but not aligned to subtractive- or  
    additive-RGB norms — the player learns by playing, not by recalling  
    grade-school colour theory.
  - No arrow glyphs anywhere. No text or tutorial banner.
- No instructions on screen. The first level itself does the teaching.
