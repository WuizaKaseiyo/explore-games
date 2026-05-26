# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): seed policy, no seed provided so autonomous mode
- skills/global/* (registered): action enum, palette, paths
- skills/design-constraints/core-knowledge-priors.md: 4 allowed prior categories
- skills/design-constraints/forbidden-elements.md: no symbols/digits/letters/clipart/cultural conventions
- skills/design-constraints/checklist.md (consulted ahead of write_spec): novelty + per-mechanic gates
- skills/mechanic-novelty/taxonomy-of-25-games.md: similarity check against 25 references
- skills/mechanic-novelty/similarity-check.md: positive distinguishing-rule procedure
- skills/mechanic-novelty/negative-similarity-check.md: 8-dimension test (3-or-more = reject)
- skills/mechanic-novelty/prior-games-index-format.md: schema reference
- skills/mechanism-details/*.md: per-game quick-reference (especially ka59, m0r0, tu93 as nearest-by-family neighbours)
- skills/code/id-generation.md: 4-char ID rules
- prior-games/index.md (24 priors): cumulative novelty floor
- L1 screenshots viewed: kf42 (cautionary palette), kn58 (single-anchor magnet), zk9p (multi-pursuer chase), zd7m (binary-state ringed pawns) — to ground negative similarity check on visual signature.

## Decisions
- **Mechanic family**: `polarity-attract-discharge`. Two-state pawns (yang/yin) auto-attract their nearest opposite per ACTION5 tick; ACTION6 flips a pawn's state; opposite-pair adjacency = discharge; level wins when all discharged.
- **Game ID**: `mr5q` — verified non-collision against 25 reserved + 24 priors; not an English word.
- **Action enum**: `[5, 6]` — pure click + freedom-slot. No arrow keys at all (the load-bearing constraint that kills random-policy attempts past L1).
- **Visual signature**: 14×14 grid scaled 4×; cream background; pawns are 5×5 with green ring + half-fill (yellow=yang top-half, magenta=yin bottom-half). Deliberately diverges from kf42's red+blue plain-rectangle aesthetic and from zd7m's centre-pixel-state ring aesthetic.
- **L1**: 2 same-state pawns; flip one then tick. Both flip and tick are required by the witness.
- **L2**: introduce **colour-keyed discharge** — ring colour determines who discharges with whom; cross-colour adjacencies just block.
- **L3**: introduce **flip-pads** — cells that auto-flip pawn polarity on entry, so the player must route attractions through pads to reach the right polarity at the right time. Walls also added for routing complexity.

## Deliverables Produced
- mechanic-pick.md: 4-char ID `mr5q`, mechanic-family tag `polarity-attract-discharge`, full description + per-near-miss distinguishing rule + 8-dim negative-similarity walks against the closest priors (kf42, zd7m) and a check on every other prior. Also includes a visual sketch of the on-screen pixel design and an action-budget sanity check.

## Notes
- Considered alternatives before settling: rigid-linkage-arm (rejected for implementation complexity and surface kinship to kf42), fold-and-unfold-paper (rejected for animation complexity), pulley-pair (same), mirror-reflect-paint (too close to ar25), slot-shift-sequence (close to vc33). Polarity-attract-discharge wins on (a) genuinely novel core dynamic, (b) clean two-action vocabulary that random-policy can't crack, (c) tractable implementation.
- The negative-similarity check explicitly flagged the kf42 cautionary tale (red+blue+plain-rectangle pawns + step-counter + walled grid). Mitigation: deliberate palette pivot to {1 cream, 3 grey, 14 green, 11 yellow, 6 magenta} avoiding the {4 red 8 blue 9} signature, plus larger 5×5 sprites with internal half-fill carrying the polarity bit.
- zd7m near-miss is on the visual front (binary-state ringed pawns); mitigation is to encode polarity by half-fill SHAPE instead of centre-pixel COLOUR. Different rendering pattern.
- The mechanic exercises 3 of 4 priors: objectness, agentness, basic geometry/topology, basic physics — all but topology in the deepest sense. L3's routing through flip-pads adds a topology/connectivity flavour.
