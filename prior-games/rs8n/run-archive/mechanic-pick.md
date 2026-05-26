# Mechanic pick — rs8n

## 1. Game ID
`rs8n` — 4 lowercase characters, alphanumeric, not English, not in the 25-game reserved list, not in `prior-games/index.md` (latest entry: `vt6q`).

## 2. Mechanic family
`line-reverse-sweep`

## 3. One-paragraph description
The avatar walks a 2D arena scattered with a small palette of distinct **item sprites** (each a 4×4 sprite with internal pixel pattern — ring, dot-cluster, X-cross, diamond, cup, etc.). Pressing an arrow rotates the avatar to face that direction and (if open) walks one cell. Pressing the freedom-slot ACTION5 fires a **sweep** in the avatar's facing direction. The sweeper is a small triangular sprite that animates outward cell-by-cell from the avatar's cell along the cardinal direction; on each cell it crosses, any present item is **picked up** into an internal queue (preserving pickup order). The sweep stops when it hits a wall, the playfield edge, or an immovable anchor. It then animates **back** along the same path, depositing items in the reverse pickup-order (last picked is dropped at the cell next to the avatar; first picked is dropped at the farthest cell of the swept segment). The net effect: the items along that line are **reversed in position**. Walls of the arena, target outlines printed on the floor showing each cell's required item, and a step-counter HUD complete the visual.

## 4. Per-level mechanic plan (preview; spec will detail)
- **L1** — base dynamic system: walk + sweep (the core line-reverse verb).
- **L2** — adds **one** new mechanic: **anchor-pillar** (a non-item sprite that blocks the sweep mid-path). Now only the items between avatar and anchor reverse — partial reversals require the player to position the anchor exploit deliberately, AND L1's sweep verb is still required.
- **L3** — adds **one** further new mechanic: **shifter-tile** (a coloured cell on the floor that, while an item passes over it during the *outgoing* leg of a sweep, recolours that item once to the shifter's colour). All three mechanics fire together: anchor partitions a sweep, shifter recolours items mid-flight, line-reverse rearranges the recoloured items into target slots.

## 5. Action mapping (preview)
| Action | Semantic | Notes |
|---|---|---|
| ACTION1 | Face up + walk 1 (rotate-only if blocked) | tu93/wa30 idiom |
| ACTION2 | Face down + walk 1 (rotate-only if blocked) | |
| ACTION3 | Face left + walk 1 (rotate-only if blocked) | |
| ACTION4 | Face right + walk 1 (rotate-only if blocked) | |
| ACTION5 | Fire sweep in current facing direction (animated) | distinctive verb on the freedom slot |

`available_actions = [1, 2, 3, 4, 5]`. ACTION6 (click) and ACTION7 (undo) intentionally omitted: the verb space is exhausted by walk + sweep, and a strict-undo on ACTION7 would meaningfully change the puzzle's planning depth (per `action-enum.md` § Slot 7).

## 6. Novelty — taxonomy similarity check (per `mechanic-novelty/similarity-check.md`)

Family-level scan: `line-reverse-sweep` does not exact-match any of the 25 reference families. Description-level scan against every taxonomy row, focusing on the dimensions in `similarity-check.md` (win condition / primary action / primary constraint):

| Reference | win-cond match | primary-action match | constraint match | Verdict |
|---|---|---|---|---|
| ar25 shape-mirror-cover | no | no | budget-shared | NOVEL |
| bp35 procedural-graph-walk | no | no | shared-budget | NOVEL |
| cd82 stencil-paint-sweep | no | no | shared-budget | NOVEL — shared word "sweep" only; cd82 sweeps a *paint stamp* over a canvas, candidate sweeps a *line of items reversing them*. Different verb. |
| cn04 rotate-translate-jigsaw | no | no | shared-budget | NOVEL |
| dc22 remote-arm-pickplace | no | no | shared-budget | NOVEL |
| ft09 stamp-color-cycle | no | no | shared-budget | NOVEL |
| g50t walk-vs-scroll | no | no | shared-budget | NOVEL |
| ka59 sokoban-explode-chase | no | no | shared-budget | NOVEL |
| lf52 fog-of-war-sokoban | no | no | shared-budget | NOVEL |
| lp85 button-permutation-puzzle | items in target positions (yes-shared) | click button vs click line (different) | budget | flagged → distinguish below |
| ls20 patrol-collect-sequence | no | no | shared-budget | NOVEL |
| m0r0 mirrored-quad-control | no | no | shared-budget | NOVEL |
| r11l tethered-throw-placement | head on lock (different from line-reversal target match) | click far cell to send projectile-like effect (shared) | budget+strikes (different) | flagged on dimension 2 → distinguish below |
| re86 flood-fill-multi-canvas | no | no | shared-budget | NOVEL |
| s5i5 rotate-resize-stick | no | no | shared-budget | NOVEL |
| sb26 mastermind-feedback | no | no | shared-budget | NOVEL |
| sc25 spell-grid-pattern | no | no | shared-budget | NOVEL |
| sk48 paired-trail-match | no | no | shared-budget | NOVEL |
| sp80 liquid-flow-routing | no | no | shared-budget | NOVEL |
| su15 radial-blast-capture | collect-vs-arrange | radial-vs-linear | budget | NOVEL — su15 vacuum-pulls fruits to a click point and consumes them; candidate reverses items along a line and rearranges them. Win condition (collect-all vs arrange-to-target) and shape (radial pull vs line reverse) both differ. |
| tn36 program-shape-buttons | no | no | shared-budget | NOVEL |
| tr87 symbol-cycle-rules | no | no | shared-budget | NOVEL |
| tu93 lockstep-multi-maze | no | no | shared-budget | NOVEL |
| vc33 row-column-swap-stripe | each unit over coloured house (shared with "items match target") | click-tab to slide row (close to "click to manipulate row") | budget | flagged on dim 1 + dim 2 → distinguish below |
| wa30 carry-pickup-drop | passenger on destination (shared) | walk + pick/drop (different from sweep) | budget | NOVEL — wa30 is single-item carry-by-walk; candidate is in-place line reversal with no carrying. |

### Distinguishing rules for the three flagged refs

- **vs lp85 (button-permutation-puzzle):** lp85's clicked buttons apply *fixed, hard-coded* permutations stored per (level, button, direction); the player's task is *learning* what each opaque button does. Candidate's sweep applies a *dynamic, geometry-derived* permutation: the avatar's position + facing chooses *which* line is reversed at the time of the action; the permutation rule itself ("reverse the items between the avatar and the first wall along the cardinal") is constant and visible from a single playthrough. lp85 is "memorise N hidden permutations"; candidate is "compose copies of one publicly-known operation by repositioning."
- **vs r11l (tethered-throw-placement):** r11l's click-target action throws a *single piece* across the board toward the click; the head-piece centroid follows. Candidate's sweep does not throw any individual item; instead it reverses an *entire line of items* in place. r11l's piece never returns to its origin; candidate's sweeper always returns. r11l's win condition is per-group head-on-lock; candidate's is per-cell item-on-target. The "click to send something to a far cell" surface similarity is real but the verb (throw vs reverse-array) is fundamentally different.
- **vs vc33 (row-column-swap-stripe):** vc33 is centred on a single *long row of stripes* with pull-tabs at the row's two ends; clicking a tab shifts every unit on the row by exactly one position (cyclic-style). Candidate has a 2D arena where items are scattered (rows AND columns AND L-shaped clusters), and a single sweep reverses items along *the avatar's chosen line*, not on a fixed row. vc33's verb is row-shift-by-1; candidate's verb is line-reverse-of-arbitrary-segment. vc33 has no walking pawn; candidate is an avatar on a 2D maze. The 2D dispersal of items + walking-then-firing-sweeps is what makes the two play-experiences distinct.

## 7. Novelty — prior-games similarity check

`prior-games/index.md` has 45 entries (kf42 … vt6q). Per `similarity-check.md` § 1, scan family tags for exact match or shared first-two-words after hyphen-splitting.

- No prior tag begins with `line-` or `reverse-` or `sweep-`. Family-level scan emits zero exact / first-two-word matches.
- Description-level scan, focusing on click-or-fire-toward-far-cell + manipulating-multiple-items priors:

| Prior | win-cond | action | constraint | Verdict |
|---|---|---|---|---|
| qm4t convex-pen-trap | capture critters inside hull (different) | click vertex posts | strikes+budget | NOVEL — qm4t is convex-hull capture (vertex-based polygon enclosure); candidate is line-reverse on a 1D segment chosen at fire-time. |
| qn7w pulse-chain-eject | terminal ball ejects per pulse | click pushers to fire pulses | budget | flagged on dim 2 (click to fire linear momentum) → distinguish below |
| vt6q grapple-anchor-yank | items into sockets / pawn yanked | fire grapple in cardinal direction | budget | flagged on dim 2 → distinguish below |
| kn58 anchor-pull-magnet | pawns on coloured targets | click cell to drop anchor (one global anchor point) | budget | NOVEL — kn58 pulls every pawn one cell toward a global anchor; candidate operates on the avatar's chosen line only and rearranges by reversal not by pull-toward. |
| su15 (already covered above) | | | | NOVEL |
| pz4t anchor-pivot-place | tile a region with components | click + arrows + ACTION5 to place | budget | NOVEL — pz4t is jigsaw region-tiling with rotation/reflection; candidate is in-place item reversal. |
| rk7x live-switch-routing | autonomous courier reaches terminal | click to toggle blade | budget | NOVEL — rk7x toggles route blades; candidate fires a one-shot reversing sweep. Different verbs. |
| qx7p column-shift-row-align | match a target row by sliding columns | click column or button | budget | flagged → distinguish below |
| jd4q echo-trail-teleport | reach exit via teleport-back-along-trail | click to teleport, walk to leave trail | budget | NOVEL — jd4q teleports the player back, candidate doesn't move the player. |
| ek73 wake-trail-evade | reach goal | walk leaves hazard wake | budget | NOVEL |
| tm5x thermal-aura-imprint | targets latch at required temp | walk + ACTION5 toggle polarity | budget | NOVEL |
| vn8d domino-cascade-topple | clear chain-end | click to topple | budget | NOVEL |
| pf3w wavefront-converge-timing | targets coincide with frontier on one tick | click slots / ACTION5 tick | budget | NOVEL |
| pj7k rolling-cube-face-paint | paint pattern via cube rolling | walk a cube | budget | NOVEL |
| rj5w axis-fold-mirror | pawns reflected onto targets | slide fold-line + commit reflects | budget | NOVEL |
| wj7d fold-crease-overlay | shadow targets covered after mirror-stamps | mirror across a crease | budget | NOVEL |
| qj4r fold-mirror-pair | same-colour pieces merge on fold | cardinal arrows fold sheet | budget | NOVEL |

### Distinguishing rules for the flagged priors

- **vs qn7w (pulse-chain-eject):** qn7w's primary verb is "click a pusher → fire a single momentum pulse through a stationary chain → only the **terminal** ball of the chain ejects (interior balls don't move)." Candidate's sweep instead **moves every item along the line** and reverses their order; no chain-momentum-physics, no terminal-only effect. qn7w's chains are pre-arranged in fixed lines you cannot freely choose; candidate's sweep line is the avatar's free choice at fire-time. The two verbs share only "click triggers something linear" — the resulting state delta is structurally different (one-ball-ejected vs whole-segment-reversed).
- **vs vt6q (grapple-anchor-yank):** vt6q fires a directional grapple line that *yanks* — heavy anchor yanks the avatar to its adjacent cell, light anchor is yanked to a socket near the avatar. The line connects exactly two endpoints (avatar + first anchor); items between are not affected. Candidate's sweep affects **every item along the line**, doesn't move the avatar, and produces a reversal not a translation. vt6q's win is anchor-into-socket (point-to-point); candidate's win is items-into-target-cells (segment-to-segment). Verb (yank vs reverse-array) and effect-shape (translate one piece vs permute many) are distinct.
- **vs qx7p (column-shift-row-align):** qx7p slides whole vertical colour-band columns past a horizontal scan line; the verb is a column-translation, the win is a target row colour pattern. Candidate has no column-strip world; items are individuated 4×4 sprites scattered freely on a 2D arena, and the sweep reverses an arbitrary cardinal segment chosen at fire-time, not a whole column. Both surface "click manipulates a column-of-cells" but qx7p shifts (rotation-style) and candidate reverses (mirror-style). The pattern-match win is shared at a high level but the player's reasoning is different — qx7p tracks where each band ends up after a series of unit shifts; candidate tracks reversing-permutations of item lists.

## 8. Novelty — negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

Per the file's three principles + 8 dimensions, the candidate was *visually* compared against the L1 frames of priors most likely to share signature: `r11l`, `su15`, and `vt6q` (the three that flagged a "click → linear projectile" surface in §6/§7).

Mental-render of candidate L1: a single avatar (white-and-coloured, 4×4 with a black eye dot indicating facing) standing on a black/grey floored arena bordered by patterned walls (palette 4); a row of 4 distinct item sprites (each a 4×4 with a unique internal pixel pattern — concentric ring in palette 7, dot-cross in palette 11, hexagon in palette 14, asterisk in palette 9) on the centre row; an upper "target preview" strip showing the desired final order of those four items; a depleting step-counter bar at row 63 in palettes 7 + 4. Multiple distinct pixel-detailed sprite kinds; mostly black/grey arena with high-saturation accents on the items.

| Dimension | r11l L1 (legs+heads, dotted-tether, dashed lock-frame) | su15 L1 (scattered fruits, blue ringed enemy, recipe header) | vt6q L1 (two-room split with red centre line, anchor sprites with eye-dots) | Candidate L1 |
|---|---|---|---|---|
| 1 What is on the board | scattered legs + heads + locks + obstacles | scattered fruits + ringed enemy + walls | two halves with anchors + sockets | row of distinct items + target preview + walls |
| 2 Player input | click far cell → throw a leg | click cell → radial blast | arrow → fire grapple | arrow → walk + face / ACTION5 → fire sweep |
| 3 Win cond | every group's head on lock | all fruits + keys collected | anchors into sockets | each cell holds the right item |
| 4 What kills | strikes + budget | strikes + budget | budget | budget only |
| 5 Cast | legs/heads/locks/obstacles | fruits/enemies/keys | anchors/sockets/walls | items/walls/anchors(L2)/shifters(L3) |
| 6 Visual signature | dotted lines + dashed outlines on dark background | scattered ringed colour-blobs + dark | symmetric two-room with red centre stripe | row-of-items + upper target row |
| 7 Pixel grain | small distinctive pieces (eye-dot, ring) | small radial sprites | mid-density rooms | mid-density distinctive items |
| 8 Core dynamic | throw piece → centroid follows | radial vacuum-and-consume | linear grapple-yank one anchor | linear segment-reverse of many items |

Shared-dimension counts:
- vs r11l: 2 (click triggers something), 4 (budget) → 2 dimensions. Below threshold.
- vs su15: 2, 4 → 2 dimensions. Below threshold.
- vs vt6q: 2-ish (linear projectile), 4 → 2 dimensions. Below threshold.

No prior overlaps the candidate on three or more dimensions. Principles 1, 2, 3 (pixel-detail richness, palette diversity, core-dynamic divergence) all hold: candidate uses richly-patterned 4×4 item sprites (not big plain blocks), a deliberately distinct palette signature centred on `{4 wall, 7 pink, 9 blue, 11 yellow, 14 green}` (different from kf42/vh68's tale of `{4, 8, 9}`), and a core dynamic — segment-reversal — that no prior implements.

The negative-similarity check passes.

## 9. Verdict
**NOVEL.** Mechanic family `line-reverse-sweep` clears both the positive similarity-check (taxonomy + prior-games) and the negative similarity-check (3-principle visual + 8-dimension surface comparison) against the three closest priors. Game ID `rs8n` does not collide with the reserved 25 nor with the 45 prior-games index entries, is opaque (not English), and is 4 lowercase alphanumeric characters per `code/id-generation.md`.

Proceed to `write_spec`.
