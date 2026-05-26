# mechanic-pick — run 2026-05-11T01-16-19

## Run input
- Seed: (autonomous)
- Date: 2026-05-11

## 4-character ID
`kg7p`

Collision check:
- Not in 25 reference IDs (ar25..wa30).
- Not in `prior-games/index.md`'s `game_id` column (verified by grep).
- Not in untracked prior-games subdirs (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n).
- Not an English word; lowercase alphanumeric, length 4.

## Mechanic family tag
`beam-tether-haul`

## One-paragraph description
A single avatar walks a chambered arena with ACTION1–4. The avatar always faces its last-walked direction and emits a short cardinal **tether beam** (visible as a translucent 1-cell ray) from its front edge. Any **haulable block** that overlaps the beam cell becomes COUPLED to the avatar — coupling is sticky: once coupled, the block keeps the same relative offset to the avatar across subsequent moves, regardless of whether the beam keeps pointing at it. ACTION5 toggles the beam on/off; toggling off **detaches every coupled block in place**, toggling on re-couples whatever currently sits in the beam cell. A coupled block can't move into a wall, into another block, or off-grid — in any of those cases the avatar's walk is rejected and no tile changes. The level wins when every haulable block sits on its colour-matched target square. Per-level mechanics layer:

- **L1** — one haulable block, one target. Walk to face the block, attach via beam, walk it onto the target square. Two mechanics: walk-avatar + beam-couple-haul.
- **L2** — adds **barrier cells** that the avatar can walk through but a coupled block cannot. Forces the player to ACTION5-release before the barrier and re-couple on the far side. Now three mechanics required by the witness: walk + beam-couple-haul + release-and-re-couple via ACTION5.
- **L3** — adds **direction-locked blocks** whose visible cardinal arrow restricts the cardinal directions in which they can be hauled (a north-arrow block can only be hauled while the beam points north — coupling to it from any other side rejects the avatar's walk). Composes with L2's barriers and L1's basic haul: avatar must approach each block from its arrow side, route around barriers, release-and-re-attach at each barrier, and dock the block on its target.

Action subset: `[1, 2, 3, 4, 5]`. No ACTION6 (no click). No ACTION7 (no undo).

## Novelty — similarity check

### Reference taxonomy near-misses (per `mechanic-novelty/similarity-check.md`)

| Ref ID | Family | Why it's a near-miss | Concrete distinguishing rule |
|---|---|---|---|
| `wa30` | carry-pickup-drop | Both have an avatar that walks and transports objects to targets. | wa30 uses **adjacency + ACTION5 = pick-up/drop one passenger at a time** (a discrete inventory verb); kg7p uses **a directional beam that couples in line-of-sight** and the coupling is **sticky across moves** until ACTION5 toggles it off — multiple in-line blocks could be coupled simultaneously, and coupling depends on the avatar's facing direction (not raw adjacency). |
| `ka59` | sokoban-explode-chase | Both push/pull blocks onto targets. | ka59 is **slide-three-cells-with-recursive-push + detonation**; kg7p has no slide-multi, no detonation, and the block follows the avatar's *every-cell-of-its-walk* rather than firing once on key press. |
| `dc22` | remote-arm-pickplace | Both have an avatar that interacts with blocks across distance. | dc22's "remote arm" is **clicked, then animates a sprite into a target slot** — fundamentally a click-place verb; kg7p has no click action and no remote arm — the beam attaches blocks to the avatar locally and the avatar's walks do the relocating. |
| `m0r0` | mirrored-quad-control | One direction-press moves multiple entities. | m0r0 moves **four mirrored avatars per press with sign-flipped axes**; kg7p has **one avatar + a variable number of coupled blocks moving in lockstep with the avatar (same vector)**, not mirrored. |

No reference game uses a **directional beam coupling mechanic with sticky attach until release**. The closest verb-level idiom is wa30's pickup-drop, distinguished above.

### `prior-games/index.md` near-misses

`prior-games/index.md` has 75+ entries; the relevant near-misses (where the candidate could collide on dimensions of the negative-similarity check) are:

| Prior ID | Family | Why it's a near-miss | Concrete distinguishing rule |
|---|---|---|---|
| `kn58` | anchor-pull-magnet | Both have an "attractor" that pulls blocks. | kn58 is **click any cell → every coloured pawn slides one cell along its dominant Manhattan axis toward the anchor** — a global, one-shot, click-driven snap. kg7p is **local, sticky, beam-directional coupling** moving with the avatar's per-step walk. No global pull; coupling is binary (in-beam or not), not a smooth gradient. |
| `vt6q` | grapple-anchor-yank | Both fire a directional cardinal line that affects an object. | vt6q's grapple is **one-shot**: fires, anchor yanks avatar one cell (or yanks the light anchor one cell to a socket), grapple ends. kg7p's beam is **persistent**: it stays on until ACTION5 toggles it off, and the block stays coupled across every subsequent walk-step. Different time horizon and verb cardinality. |
| `kj82` | plank-pivot-walk | Has "pawn walks across rigid bodies". | kj82 has **planks** that are pivoted (rotated) around an anchor; the pawn walks ON them. kg7p has **blocks the avatar hauls** — the blocks are cargo, not floor; the avatar never walks on a block. Different role for the rigid bodies. |
| `wb6n` | tether-pin-wrap | A tether connects an avatar and a thing. | wb6n is **fixed-length leash to a stake + pin-plant verb to extend reach**; kg7p has **no leash distance** — coupling is absolute (the block moves with the avatar 1-for-1, no slack). Different physics. |
| `kf42` | tether-pawn-cycle | A tether connects two pawns. | kf42's tether is a **max-distance constraint between two pawns**, both player-controlled; kg7p has one avatar + an arbitrary number of haulable blocks (not player-controlled). Different cardinality. |
| `hk7v` | overhead-trolley-hook | Both deliver blocks to coloured floor markers via a controllable attached connector. | hk7v uses a **fixed overhead gantry trolley + variable-rope hook**, the rope hangs down and operates **only vertically** from the trolley line. kg7p has a **free-walking avatar** whose beam can point in any cardinal direction; the block couples locally, not via a fixed overhead line. Different topology. |
| `dj5h` | pulley-pair-platform | Coupled pair-of-things across the field. | dj5h pulleys couple **paired hanging platforms** (raise one, lower the other). kg7p has no pulley, no pairing — only the avatar's local beam. |
| `wa30`-style families (carrier-and-deliver) above (already covered). | | | |

For every taxonomy / prior-games near-miss, the distinguishing rule names the **mechanical verb difference** (directional sticky beam vs adjacency pickup, persistent vs one-shot, free-walking emitter vs gantry, etc.) rather than cosmetic colour/shape differences.

## Negative-similarity test (per `negative-similarity-check.md`)

Walking the seven dimensions against the closest prior `wa30` (the highest-risk near-miss):

1. **What's on the board.** wa30: avatar + passengers + destinations + forbidden cells. kg7p: avatar + haulable blocks + targets + barrier cells. **Both have an avatar + cargo + targets.** Overlap (weak — universal idiom).
2. **What the player physically does on input.** wa30: walk + ACTION5 pickup/drop. kg7p: walk + ACTION5 beam-toggle. Overlap on **arrow + ACTION5 verb structure**; differs on what ACTION5 does (one-shot adjacency pickup vs beam-state toggle).
3. **What the level is asking for.** wa30: every passenger delivered. kg7p: every block on its target. Both are "deliver each thing to its target". Overlap.
4. **What kills the player.** Both: step budget. Universal.
5. **Cast of supporting elements.** wa30: passengers / destinations / forbidden-cells / secondaries. kg7p: blocks / targets / barriers / direction-locks. Different supporting elements (no patrolling-NPCs, no two-mobile-sprite tether) but the *core triplet* (avatar + cargo + target) is shared.
6. **Visible visual signature.** TBD by spec — will pick a palette that differs from wa30's lavender/grey/blue (e.g. dark-purple background, light-teal avatar, magenta beam, off-yellow blocks, off-white targets).
7. **Pixel grain.** kg7p plans **5×5 or 6×6 avatar** with internal pattern (small porthole / sensor pip), targets as **4×4 hollow squares with a coloured inner accent**, blocks as **4×4 with a directional chevron in L3**. wa30 uses similar mid-size pixel sprites — moderate overlap on grain.
8. **Core dynamic.** wa30: "pick up, walk, drop"; kg7p: "**face**, **beam-attach**, **walk dragging**, **release at barrier or target**". The presence of a *facing direction* and a *visible beam emanating from the avatar* changes the **moment-to-moment thinking**: in kg7p the player thinks "is my beam pointing at the right block?", "would walking left de-attach because the block can't follow?", "do I need to release before this barrier?". In wa30 the player thinks "am I adjacent to the next passenger?".

Overlap count vs wa30: dimensions 1, 2, 3, 4, 7 share something; 5, 6, 8 differ. Dimension-by-dimension:

- Dimensions 1, 3, 4 are universal (cargo, deliver, step-budget). Don't count strongly.
- Dimension 2 is a genuine shared idiom (arrow + ACTION5 verb structure).
- Dimension 7 will be addressed by enriching pixel grain in the spec; pawns get internal pattern, beam gets a distinctive translucent halo.
- Dimensions 5, 6, 8 differ. The **core dynamic** (8) — beam-directional sticky coupling — is the most load-bearing difference and a real "what is the player thinking?" divergence.

Verdict: **NOVEL.** Overlap on 1-2 substantive dimensions (input-verb structure + cargo-deliver framing), well below the 3+ rejection threshold. The core-dynamic divergence (directional sticky beam vs adjacency pickup-drop) is concrete and load-bearing.

## Decision

PROCEED to `write_spec` with:
- ID: `kg7p`
- Family: `beam-tether-haul`
- Action subset: `[1, 2, 3, 4, 5]`
- Levels: L1 = walk + beam-couple-haul; L2 + barriers; L3 + direction-locked blocks.
