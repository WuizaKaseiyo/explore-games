# Step #02: pick_mechanic

## Inputs Consumed
- mechanic-novelty/taxonomy-of-25-games.md (from study): scanned for closest cousins to "rotor sweep" idea
- mechanic-novelty/similarity-check.md, negative-similarity-check.md (from study): applied 8-dimension test
- mechanism-details/fz5j-equivalents conceptually: not applicable (no fz5j in mechanism-details, fz5j is a prior-game not reference)
- prior-games/index.md (55 entries) (from study, re-scanned): no rotor-sweep-walk family present
- prior-games/{fz5j,lq5x,vp6h}/mechanism-detail.md (read in this state): authoritative inputs for distinguishing-rule articulation against the closest cousins
- prior-games/{fz5j,lq5x,vp6h}/run-archive/smoke-frames/level_1.png (viewed in this state): visual signature comparison per negative-check principles 1-3
- code/id-generation.md (from state Skills): rules for 4-char ID
- skills/global/action-enum.md (from study): no ACTION7 except for strict-undo

## Deliverables Produced
- mechanic-pick.md: 4-char ID `nz3v`, family tag `rotor-sweep-walk`,
  one-paragraph description, distinguishing rules vs the seven
  closest cousins (fz5j, lq5x, vp6h, g50t, pf3w, xz5g, qz73, cd82),
  8-dimension negative-similarity check vs fz5j with verdict pass,
  per-level mechanic plan preview, verb subset `[1,2,3,4]`.

## Notes
- Autonomous mode (no user seed).
- ID `nz3v` chosen after grep verified no collision in prior-games index or 25-game reference list. Not English.
- Closest cousin is fz5j; defended via "global angular phase vs per-cell independent periods" distinction.
- Heavy axes (5/6/7 of the 8-dimension test) all diverge; dim-8 (core dynamic) is in the same broad family ("time-walk against periodic constraint") but with a fundamentally different reasoning texture (single global angle vs many local periods). This passes the negative-similarity rule because heavy axes diverge cleanly.
- The action subset `[1,2,3,4]` is intentional: the game's distinctive verb is the *environmental* sweep, not a player verb. ACTION5/6/7 are deliberately not included.
- Decision log: brainstormed and rejected ~25 candidate families before settling on rotor-sweep-walk. Rejected XOR-stencil-overlay (close to vp6h L3 intersection mechanic + visual cluttered), Tower-of-Hanoi tubes (cliché video game), tractor-beam crane (close to wa30/vt6q), telescopic probe (= nb6t), and others.
