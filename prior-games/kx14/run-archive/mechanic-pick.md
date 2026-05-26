# mechanic-pick

## Run input
- **Seed:** none (autonomous mode)
- **Prior-games corpus state:** two priors exist —
  - `kf42` *tether-pawn-cycle* (two pawns + tether-drag + colour-set pads)
  - `qz73` *radial-cycle-lock* (8-slot dial + ACTION5 rotate + ACTION6 lock)

## 4-character ID
**`kx14`** — letter+letter+digit+digit; lowercase alphanumeric; not an English word; not in reserved 25 (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30); not in `prior-games/index.md` (kf42, qz73). Opaque per §3.4.

## Mechanic family tag
`tide-tilt-buoyant`

## One-paragraph description
The playfield is a vertical cross-section of a tank: the lower part is filled with light-blue water up to a movable surface line, the upper part is air, and a few opaque "platform" sprites hang at fixed heights inside the tank. One or more **buoyant balls** rest on the water surface (always exactly at the surface row, in whichever cell they last occupied horizontally). The player has FOUR gameplay verbs across action subset `[1, 2, 3, 4, 6]`:

- **ACTION1 / ACTION2** — *raise* / *lower* the water surface by one row. Each press shifts every buoyant ball upward (or downward) along with the surface unless a platform is in the way; balls that would be blocked instead remain pressed against the platform until the surface clears.
- **ACTION3 / ACTION4** — *tilt left* / *tilt right*. A tilt is an instantaneous nudge that slides every floating (un-anchored) ball one cell in the tilt direction; balls bounded by a wall, a platform, or a same-row neighbour stop where they hit. Tilts do NOT change the water level.
- **ACTION6** — *click a ball* to toggle its **anchor**. An anchored ball ignores all subsequent water-level changes (it stays at its current cell while the surface moves around it) and ignores tilts. Anchor visual: the ball gains a black centre pixel.

Each level's win condition: every coloured target-ring on the playfield must contain a same-coloured ball (anchored or floating, the engine doesn't care). The single failure mode is exhausting the per-level step counter.

The level progression follows the §3.4 / `composition-and-tutorial.md` "one new mechanic per level" contract:

- **L1** introduces tide-control + tilt as the joint base system (all balls float; no platforms in the path; witness raises water and tilts to deliver the ball to its ring; both verbs are required by the witness).
- **L2** adds **platforms** as a topology mechanic — the witness must lower the water below a blocking platform, tilt across, and raise the water again. Tide-control + tilt + platforms all required.
- **L3** adds **anchor** — the witness must anchor one ball at a specific tide-level so it stays put while the second ball is delivered (tilting only affects un-anchored balls; lowering water re-exposes the anchored ball at a now-dry cell so it can be unanchored and tilted last). All four verbs required.

## Positive similarity-check (per `mechanic-novelty/similarity-check.md`)

Walking the candidate against every row in `taxonomy-of-25-games.md` and `prior-games/index.md`. Family-level check first; for each row whose family or first-two-words match, escalate to description-level. Near-misses surfaced:

| Row | Family-level match | Description-level | Verdict |
|---|---|---|---|
| `kf42` (prior) | partial — both pair "click toggle" with "directional movement" | win = same-colour pawn-on-target tile in both. Primary verb in kf42 is `click-then-arrow-step a pawn`; primary verb here is `arrow = tide/tilt the environment`. **No directly-controlled actor in kx14** — the player manipulates the water surface, not a sprite. | NOVEL — concrete distinguishing rule below |
| `qz73` (prior) | partial — both have a "lock-the-object-from-global-action" toggle | qz73's lock prevents a tip from being moved by ACTION5 dial-rotation; kx14's anchor prevents a ball from being moved by tide AND tilt. Different topology (radial dial vs vertical cross-section); different "global action" being immunised against. | NOVEL — concrete distinguishing rule below |
| `sp80` (water-pour, 25-set) | partial — both use water | sp80: water cascades downward from spouts in instant-on-pour events budgeted to 4 pours; player arranges shelves to redirect drops. kx14: water level is a controllable persistent surface that the player raises/lowers each turn; objects float on the surface. | NOVEL — concrete distinguishing rule below |
| `g50t` (walk-vs-scroll, 25-set) | partial — both involve a uniformly-changing playfield | g50t: world auto-scrolls left every other turn against the player. kx14: water surface only changes when the player presses ACTION1/2. Direction of agency reversed. | NOVEL — concrete distinguishing rule below |
| `m0r0` (mirror-orb-merge, 25-set) | partial — both have multi-object cardinal-arrow input that affects multiple objects | m0r0: UP moves both pawns up, LEFT pushes one and pulls the other (mirror-image bound). kx14: tilt acts on ALL un-anchored balls in parallel. | NOVEL — concrete distinguishing rule below |
| `dc22` (colour-cycle-walk, 25-set) | none |  | NOVEL |
| `cn04`, `bp35`, `lf52`, `r11l`, `tn36`, `vc33`, `lp85`, `ka59`, `ar25`, `cd82`, `ft09`, `re86`, `s5i5`, `sb26`, `sc25`, `sk48`, `su15`, `tr87`, `tu93`, `wa30`, `ls20` | none after first-pass | | NOVEL (no family overlap) |

### Concrete distinguishing rules

- **vs kf42:** kf42 has a directly-steered actor (clicked pawn → arrows step it within tether constraints). kx14 has NO directly-steered actor — every arrow press changes the *environment* (the water surface) and balls move passively as a consequence. kf42's win requires both pawn-on-tile AND colour-matched-via-pads; kx14's win is purely geometric position-on-target with no recolouring step. The kf42 cautionary tale (visual sameness via small coloured pawns on dark walled grid) is avoided: kx14's playfield is a light-blue water region + light-grey air region with medium-sized internally-patterned ball sprites — very different visual signature.
- **vs qz73:** qz73's lock prevents an individual tip from participating in the global ACTION5 rotation around an 8-slot ring; the lock is the entire "second mechanic". kx14's anchor prevents a ball from participating in **either** tide changes **or** tilts (immunity from BOTH classes of player-environment-action), and additionally re-exposes a *dry* anchored ball when the tide recedes — a positional consequence qz73's lock does not have. Topology differs entirely (radial dial vs vertical tank cross-section); visual signature differs entirely (8 small coloured tips on grey field vs water/air playfield with 1–3 floating balls).
- **vs sp80:** sp80's water is consumed in pour-events from 4 attempts per level, falling top-to-bottom past arranged shelves to land in cups; the player's verb is shelf-arrangement plus pour-trigger. kx14's water is a continuous, bidirectionally-controlled surface; there is no "pour" event — the player raises and lowers the level each turn, and balls float at the surface throughout. sp80's primary action is `arrange the cascade path`, kx14's is `lift the carrier`.
- **vs g50t:** g50t's playfield change is the antagonist (the leftward scroll happens *to* the player and races to overtake them); kx14's playfield change IS the player's verb (the tide moves only when the player asks). Failure mode in g50t is "edge overtakes avatar"; in kx14 it's only step-counter exhaustion.
- **vs m0r0:** m0r0's pawn-pair has *coupled* arrow semantics (UP moves both up; LEFT pushes one while pulling the other). kx14's tilt acts on all un-anchored balls *uniformly* (every ball moves the same direction together), no inversion or pair-coupling. m0r0 features mirror-pawn merging as the win predicate; kx14 features ball-on-target-ring placement.

## Negative similarity-check (per `mechanic-novelty/negative-similarity-check.md`)

Walking the eight dimensions against the two priors and the closest 25-game near-misses. Visual signatures opened: `prior-games/kf42/run-archive/smoke-frames/level_1.png`, `prior-games/qz73/run-archive/smoke-frames/level_1.png`, `deep-analysis/sp80/level_1.png`, `deep-analysis/g50t/level_1.png`, `deep-analysis/m0r0/level_1.png`, `deep-analysis/dc22/level_1.png`. Mental rendering of kx14 L1: ~12×12 cell grid; lower 5 rows light-blue (water, palette 10); upper 7 rows off-white (air, palette 1); one orange-and-maroon 3×3 buoyant ball at top of water column; one green 3×3 hollow target ring near top-right; thin orange step-bar on top edge.

| Dimension | vs `kf42` | vs `qz73` | vs `sp80` | vs `m0r0` |
|---|---|---|---|---|
| 1. What's on the board | walls + pawns vs **water surface + balls + air** — DIFFERENT | radial hub + tips + sockets vs **water + balls** — DIFFERENT | shelves + spouts + cups vs **water + balls + platforms** — DIFFERENT | mirror-pawn maze vs **water-tank cross-section** — DIFFERENT |
| 2. Player verbs | click-then-arrow vs **arrow=tide-or-tilt + click=anchor** — partly shared (clicks; arrows present) | ACTION5+click vs **arrows + click** — different (no ACTION5 here) | click+arrows+ACTION5 vs **arrows + click** — partly shared | arrows+click vs **arrows + click** — same input shape; different referent |
| 3. What the level asks | colour-pawn on colour-pad vs **same-colour ball in same-colour ring** — weakly shared (geometric match-up) | tip-on-socket colour-match vs **ball-in-ring colour-match** — weakly shared | catch-every-drop on cup vs **ball-in-ring** — different goal-shape | merge-mirror-pair-in-goal vs **ball-in-ring** — different |
| 4. What kills | step-counter only — SHARED (universal in corpus) | step-counter only — SHARED (universal) | step-counter + 4-pour-budget — partly shared | step-counter only — SHARED (universal) |
| 5. Cast of supporting elements | walls + pawns + targets + cyclers — different supporting set | hub + tips + sockets — different | shelves + spouts + cups + drains — different | mirror-pawns + spike-tiles + post-stones — different |
| 6. Visible visual signature | dark walled box, palette {4 wall, 8 red, 9 blue} — **HIGHLY DIFFERENT** from kx14's blue/off-white horizontal-band signature | grey field with small coloured tips — **HIGHLY DIFFERENT** | orange playfield with horizontal blue shelves — partial overlap (both have a horizontal blue band), but kx14's blue is bottom-up tide and the rest of the field is off-white air; sp80's is mid-frame solitary shelves on orange. **DIFFERENT** | dark maze + glow-pawns — **DIFFERENT** |
| 7. Pixel grain | tiny 1-cell pawns — **DIFFERENT** (kx14 uses 3×3 internally-patterned balls + thin platforms) | small 1-cell tips — **DIFFERENT** | thin shelf rectangles + tiny spouts/cups — partly shared (medium horizontal sprites) | small mirror-pawns — **DIFFERENT** |
| 8. Core dynamic | "select-pawn, drag-with-tether to colour target" — **DIFFERENT** from "control the carrier (water + tilt) to deliver passive balls" | "rotate dial, lock to decouple, repeat" — **DIFFERENT** | "arrange shelves to redirect a future cascade" — **DIFFERENT** (kx14 has no cascade event) | "co-pilot two coupled pawns through a maze" — **DIFFERENT** (no coupling in kx14; balls are passive cargo) |

Tally of meaningful shares (excluding dim-4 since it's universal across the corpus):
- vs kf42: 2 weak shares (verb-input-shape, level-asks-colour-match). Below threshold.
- vs qz73: 1 weak share (level-asks-colour-match). Below.
- vs sp80: 1 partial visual share (horizontal blue band) + 1 weak verb share. Below.
- vs m0r0: 1 verb-input-shape share (arrows+click) + 1 weak (level-asks). Below.

No prior shares ≥3 dimensions, especially no overlap on dimensions 6, 7, 8 (the named principles in the negative-similarity skill). **Candidate passes the negative test.**

## Verdict
**NOVEL.** Proceed to `write_spec` with id `kx14`, family `tide-tilt-buoyant`, action subset `[1, 2, 3, 4, 6]`.
