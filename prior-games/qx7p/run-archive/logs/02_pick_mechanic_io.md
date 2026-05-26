# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no seed string).
- skills/mechanic-novelty/taxonomy-of-25-games.md.
- skills/mechanic-novelty/similarity-check.md and negative-similarity-check.md.
- skills/mechanic-novelty/prior-games-index-format.md.
- skills/code/id-generation.md (4-char ID rules).
- prior-games/index.md (29 priors).
- 25 mechanism-details summaries.
- Visual screenshots: ek73/level_1.png, jd4q/level_1.png, vd3g/level_1.png, lv4k/level_1.png, pf3w/level_1.png, gx7m/level_1.png, bx84/level_1.png, qz73/level_1.png, kp9z/level_1.png, zd7m/level_1.png, xn5p/level_1.png.

## Negative similarity walk (8 dims, vs each prior I considered)

Candidate: column-shift-row-align — vertical bands of coloured segments
that the player slides up or down so that the segments aligned with a
horizontal indicator row match a target colour pattern.

Most-likely overlaps walked in §6 of the deliverable.

## Decision rationale

Visually distinct space (vertical-band rendering, no avatar, no
walking, no projectile, no fluid). Verb is "shift active column
up/down by one segment" — not used by any prior. Composition adds
bound-pair shifting (L2), blocker segments (L2), and movable indicator
row (L3). Closest priors in *gestalt* are lp85 (button-permutation,
row+column shifts in Rubik style) and vc33 (pull-tab row-slide); both
are flat-grid horizontal/row-swap puzzles, while ours is a vertical
band-stack with a horizontal scan-line — different visual signature
and different verb (segment-by-segment shift vs. whole-row tab-pull).

## Deliverables Produced
- mechanic-pick.md: 4-char ID `qx7p`, family tag `column-shift-row-align`, one-paragraph description, distinguishing rules vs each near-miss in taxonomy + priors, 8-dimension negative-similarity check.

## Notes
- Considered several mechanics (carpet-roll-bridge, fold-axis-overlay, fountain-arc, drum-ring-align, etc.) and rejected each on visual or core-dynamic overlap with priors.
- Final pick visually orthogonal: tall vertical bars + horizontal scan line + target strip; verb = click-column + arrow-shift; novel both vs the 25 references and the 29 prior games.
- Game ID `qx7p` not in reserved or priors.

