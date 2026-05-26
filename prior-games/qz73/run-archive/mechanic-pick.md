# Mechanic pick — qz73

## 4-character ID
`qz73`

Verified:
- exactly 4 lowercase alphanumerics ✓
- not an English word ✓
- not in the 25 reserved reference IDs ✓
- not in `prior-games/index.md` (which currently lists only `kf42`) ✓

## Mechanic-family tag
`radial-cycle-lock`

## One-paragraph description

A central rotor sits in the middle of the playfield with a small
fixed number of *spokes* radiating outward (3 in L1, more in later
levels). Each spoke ends in a single coloured tip-cell. Around the
periphery of the rotor sits a static ring of *socket* sprites at
fixed angular positions, each socket carrying its own target
colour. The level is solved when, simultaneously, every socket
holds a tip whose colour matches the socket's own colour. The
player has two verbs: ACTION5 *advances* the rotor by one
angular position (a cyclic permutation that moves spoke `i` to the
position where spoke `i−1` was, in a fixed direction), and ACTION6
*toggles a per-spoke lock* — clicking a spoke flips its lock state.
A locked spoke does **not** move when ACTION5 is pressed; the
unlocked spokes continue to advance around it, so locks effectively
break the rotation symmetry and turn the structure from a single
rigid wheel into a set of independent partial-rotations. Win
predicate: `every socket's match-colour == the spoke-tip currently
overlapping that socket`. Lose: step counter (only). The
distinctive verb (ACTION5) is the rotation; the second mechanic
(locking via ACTION6) is what breaks the trivial "spam ACTION5
until alignment" loop and forces planning. Compositionally, L1
introduces ACTION5 alone (no locks), L2 introduces ACTION6 lock
mechanic, L3 forces both — alignment requires partitioning the
spokes into multiple sub-rings each at their own rotation phase,
achievable only by alternating lock-toggles with rotations.

Prior categories used (per `core-knowledge-priors.md`):
- **Objectness**: spokes and sockets are coherent persistent
  entities with colour and position.
- **Basic geometry & topology**: rotation as a symmetry operation;
  the cyclic permutation structure (Z/n group action).
- (Not used: physics, agentness — deliberately keeping the prior
  load small.)

## Novelty rationale

### Vs. the 25 taxonomy entries

The candidate's surface mechanic is closest to a small cluster
of taxonomy rows that involve rotation, cycling, or click-locked
state. Walking the `similarity-check.md` matrix:

| Taxonomy row | Family tag | Closest? | Distinguishing rule |
|---|---|---|---|
| ar25 | shape-mirror-cover | rotation overlap | ar25 rotates **per selected piece** (player picks a sprite, rotates only that one). qz73 rotates the **entire rotor as a single rigid object** via ACTION5; the player never selects a sprite to rotate, only locks/unlocks spokes. The agent-side action space is therefore 1+N (rotate, plus 1 toggle per spoke), not 1×M (rotate per of M selected pieces). |
| cn04 | nub-pair-glyph | rotation overlap | Same distinction as ar25: cn04's ACTION5 rotates **the selected glyph**; qz73's ACTION5 rotates the global rotor. Cn04's win condition is pairwise-pixel-coincidence between piece boundaries; qz73's win condition is per-socket colour equality. Cn04 has no analogue of the lock mechanic — it has nothing that selectively pins a sub-set of pieces against a global motion. |
| lp85 | row-col-shift-grid | permutation overlap | lp85 is a click-only game where each button applies a hard-coded permutation table (Rubik-face style). qz73 has only ONE permutation (cyclic shift by 1), available repeatedly. lp85's button identity matters; qz73's ACTION5 has no parameters. The two games look nothing alike — lp85 is a 2D grid of cells with marginal buttons, qz73 is a radial structure with a centre and a rim. |
| tr87 | tape-rewrite-rule | cycling overlap | tr87 cycles **symbol identities** at a cursor position via ACTION1/2; qz73 cycles **positions** of fixed-identity tips via ACTION5. tr87's verb is "make this card become a different card"; qz73's verb is "rotate this whole structure one click". Visually unrelated (tr87: two horizontal rows of glyph cards; qz73: radial wheel). |
| dc22 | colour-cycle-walk | cycling overlap | dc22's cycler is triggered by walking onto a tile; qz73 has no avatar to walk. dc22 cycles wedges-of-a-colour; qz73 cycles position assignments. Different visual (dc22: maze with wedge-blocks; qz73: rotor + sockets). |
| vc33 | row-slide-pull-tab | click-triggered geometry shift | vc33 slides a row by one cell on click; qz73 rotates the rotor on ACTION5 (not click). vc33 has only ACTION6 (`available_actions=[6]`); qz73 uses ACTION5 + ACTION6 with very different roles. |
| sb26 | tile-place-commit | click-and-commit overlap | sb26's ACTION5 commits the player's current row of tile placements as a guess (Mastermind feedback). qz73's ACTION5 deterministically rotates a structure — no guess, no feedback animation, no candidate-tray. The two games have nothing in common beyond the slot label. |
| cd82 | orbit-fire-paint | "ring of slots" overlap | cd82's basket sits at one of 8 ring-positions; ACTION1-4 navigate the ring; ACTION5 fires the basket at the canvas. qz73 has no canvas, no basket, no fire — the rotor IS the central object, and rotation acts on the structure itself, not on a movable cursor inside the structure. |
| s5i5 | rod-stretch-retract | "rotate by colour-swatch" overlap | s5i5 has a click-on-swatch verb that rotates all rods of that colour 90°. The player can rotate **per colour-class**. qz73 rotates the WHOLE rotor (no per-class rotation); the lock-per-spoke is the only way to selectively exempt parts of the structure, and it is a click-toggle, not a rotation trigger. |
| Every other row | various | not close | The remaining 16 rows (bp35, ft09, g50t, ka59, lf52, ls20, m0r0, r11l, re86, sc25, sk48, sp80, su15, tn36, tu93, wa30) are walking / pushing / shooting / placing / drawing / paired-mirror games whose dynamics share nothing with rotation-and-lock. |

For each near-miss the distinguishing rule is concrete (not "it's
different colours" or "it's harder").

### Vs. `prior-games/index.md` (kf42 only)

kf42 row: `tether-pawn-cycle` — "two pawns share a max-distance
tether; click selects, arrows step, walking onto a coloured pad
sets pawn colour".

**Positive distinguishing rule.** kf42's verbs are
*click-to-select* + *arrow-to-walk* + *implicit-walk-on-pad-to-set-colour*.
qz73's verbs are *ACTION5-rotate-the-whole-rotor* +
*ACTION6-toggle-a-spoke-lock*. The cardinality and meaning of
inputs are completely different; in particular qz73 has no avatar
to navigate, and its ACTION5 is the load-bearing distinctive verb
where kf42 has no ACTION5 at all.

**Negative similarity-check (the 8 dimensions).** Mentally rendering
qz73 L1 — a centre-of-frame rotor (~16-cell-wide hub) with 3
spokes (lines of 3-4 cells each) terminating in coloured tip
blocks, surrounded by a ring of small coloured socket squares —
against kf42 L1's smoke-frame (small open black-walled arena, two
solitary pawn-blocks left of centre, a magenta HUD strip along the
bottom):

| # | Dimension | Shared with kf42? |
|---|---|---|
| 1 | What is on the board | NO — kf42: 2 movable pawn-blocks on an open field. qz73: a single dominant radial structure (rotor) with peripheral sockets. Completely different "what the player is looking at". |
| 2 | What the player physically does on input | NO — kf42: select-then-walk. qz73: rotate-the-world + toggle-a-lock. |
| 3 | What the level is asking for | NO — kf42: get pawn A to pad A and pawn B to pad B. qz73: rotate so every spoke-tip lands on its colour-matching socket. The first is "navigate two pawns to two pads"; the second is "find the rotation+lock-pattern that satisfies a system of equations". |
| 4 | What kills the player | shared — both use a step-counter as the only lose. This is dimension 4 alone; sharing it does NOT trigger rejection (per `negative-similarity-check.md`'s "step counter alone is too universal to count"). |
| 5 | Cast of supporting elements | NO — kf42's cast is {2 pawns, 2 target pads, 0-2 colour-set pads, walls}. qz73's cast is {1 rotor with N spokes, N tips, M sockets, padding}. No element from one cast appears in the other. |
| 6 | Visible visual signature (palette + density) | NO — kf42 palette: black bg + grey wall + red-blue pawns + magenta HUD strip. qz73 will use a different dominant palette: I'll choose a light-grey background (palette 2), a dark-grey hub (palette 3), and tip/socket pairs in {orange, green, purple} (12, 14, 15) — none of {red, blue} dominant. The rotor's radial geometry has high pixel density at the centre and low density at the rim, the inverse of kf42's "two small floating blocks on a mostly-empty arena". |
| 7 | Pixel grain of primary sprites | NO — kf42's pawns are 1×1 single cells. qz73's spokes are multi-cell linear bars (~3-4 cells long) attached to a multi-cell hub block (~3×3); the tips are 1×1 caps. The primary sprite SHAPE language is "linear bar + central blob", not "single cells". |
| 8 | Core dynamic | NO — kf42's player thinks "where do I move next, and which pawn drags which?". qz73's player thinks "how many ACTION5 presses and which spokes locked when, to satisfy each socket constraint?". The first is path-planning under tether constraints; the second is solving a small system of cyclic-permutation equations. |

Shared dimensions: 1 (the universal step-counter). Shared
non-trivially: 0. The
negative-similarity-check threshold is 3+ shared dimensions for
rejection — this candidate sits well below that. The candidate
diverges on every dimension named as a Principle (palette diversity,
pixel grain, core dynamic).

## Verdict

**NOVEL** vs both the taxonomy and the prior-games corpus. Proceed
to `write_spec`.
