# critique-pass — lq5x · lantern-cone-illuminate

## Format & structure

- ✅ **#1 — palette 0..15 (and -1)**: All sprite pixels in {4, 8, 11, 12} ∪ {-1}; ConeOverlay repaints background cells to {1, 13}; HUD writes {1, 3}. All in palette range.
- ✅ **#2 — file structure matches universal-scaffold**: Spec §3 sprite roster, §4 levels, §6 HUD widgets, plus standard imports / constants. Mirrors `cn04`'s file shape.
- ✅ **#3 — `available_actions` is subset of [1..7]**: `[1, 2, 3, 4, 5]` (the "cardinal motion + freedom slot" subset, novel for the priors).
- ✅ **#4 — exactly 3 Level entries; L1 = base, L2 = +1, L3 = +1**: Three Level entries (12×12, 14×14, 14×14). L1 declares N=2 (walk, cone-rotate); L2 = N+1=3 (adds wax pickup); L3 = N+2=4 (adds filter-cone-colour). Each level's witness exercises every declared mechanic.
- ✅ **#5 — 4-char ID, lowercase, not reserved, not in priors**: `lq5x`. Not in {25 reference IDs} ∪ {kf42, qz73, kx14, qb84}. Not an English word.

## §3.4 priors & constraints

- ✅ **#6 — every mechanic from core-knowledge-priors**: Cone projection = basic geometry (a directional rectangle); inside/outside relation = topology. Lantern, targets, pickups, filters = objectness. All four mechanics draw on these two prior categories.
- ✅ **#7 — no letters, digits, real-world clipart, cultural conventions**: Lantern sprite is a 3×3 yellow square with a central off-black pixel — abstract, doesn't read as a letter or digit. Target rings are 3×3 hollow rings — abstract. Pickups are 1×1 single cells — abstract. Filters are 1×1 single cells — abstract. The HUD is a depleting bar — no digits. The "lantern" label is author-side; the visible sprite is geometry-only. No cultural conventions (e.g. red ≠ "danger"; the colour pairing of red filter ↔ red target is functional, not cultural-symbolic).
- ✅ **#8 — at least TWO distinct mechanics**: 4 mechanics across the environment (walk, cone-rotate, wax pickup, filter cone-colour).
- ✅ **#9 — L1 = tutorial, base dynamic, reduced state space, no on-screen text**: L1 grid 12×12 (smaller than L2/L3 14×14); 2 mechanics (walk + rotate), both required by the 5-action witness; no text, no HUD digits.
- ✅ **#10 — L2 / L3 increase difficulty by COMPOSING every mechanic at that level**: L2 witness uses all of {walk, rotate, wax}; L3 witness uses all of {walk, rotate, wax, filter}. Difficulty doesn't come from "bigger grid alone" — L1 is 12×12, L2 + L3 are 14×14, only +2 cells per side. Step budgets are tight (10/12/13).
- ✅ **#10a — no hidden mechanics, one new per level, all required by witness**:
  - L1 N=2 → witness exercises walk + rotate, AND walk-only refutation shows budget excludes 11-action walk-only path. Both required.
  - L2 N+1=3 → witness exercises walk + rotate + wax. Walk-no-wax refutation: detour around (3,6) costs 6 walks for A; back-and-forth + S-walk + 2 rotates = 17 actions > budget 12. Wax is strictly required.
  - L3 N+2=4 → witness exercises all four. Without wax, walk-no-wax path = 17 actions > budget 13 (computed). Without filter, R1 (red) cannot be lit because cone defaults yellow (no yellow filter exists in level). Without rotate, R1 cannot be lit because no E-cone covers (2, 11). Without walk, lantern is stuck at start.
  - Per-level mechanic count rises by exactly +1 each promotion. ✓

## Novelty

- ✅ **#11 — mechanic family absent from `taxonomy-of-25-games.md`**: `lantern-cone-illuminate` is not a row. Closest taxonomy entries: ls20 (cycler-attribute-match), bp35/lf52 (procedural-graph-walk), tu93 (maze-pickup-train). Distinguishing rules articulated in spec §9 against each.
- ✅ **#12 — mechanic family absent from `prior-games/index.md`**: Not present (the four priors are tether-pawn-cycle, radial-cycle-lock, tide-tilt-buoyant, bead-lift-swap). Distinguishing rules articulated in spec §9 against each prior.
- ✅ **#13 — concrete distinguishing rule for any sounds-similar entry**: Spec §9 articulates one for ls20 (state lives on cone projection vs avatar body; verb cardinality differs; per-target conjunction over run history vs single goal-cell test); for bp35/lf52 (no abstract graph data structure); for tu93 (no follower/chain dynamic); for m0r0 (one pawn vs two mirror-symmetric); for ka59 (no pushing, no chaser); for r11l (no centroid logic); for kf42/qz73/kx14/qb84 (action-set differences and dynamic-level differences).

## Solvability

- ✅ **#14 — environment-level win condition stated**: §7. After every action, check `all(target.name in self.lit_targets for target in current_level.get_sprites_by_tag("target"))`. Triggers `self.next_level()`. Universal across L1/L2/L3 — same predicate.
- ✅ **#15 — lose condition stated**: §8. `if self._action_count >= self.step_budget: self.lose()`. No other lose path. Walking off-grid is a silent no-op that consumes a step.
- ✅ **#16 — difficulty floor and ceiling per level**:
  - L1: random-resistance ((1/5)^5 ≈ 3×10⁻⁴ for 5-action witness in budget 10) ✓; human ~1 min ✓; planning near-zero (mechanic discovery is the difficulty) ✓.
  - L2: random-resistance ((1/5)^10 ≈ 10⁻⁷) ✓; human ~2 min ✓; planning depth — multi-step state+future-state reasoning ✓; no spam-the-new-verb (rotating ACTION5 in place lights nothing) ✓; no follow-the-colour walkthrough (both targets yellow) ✓; no 1-action lookup (sequential).
  - L3: random-resistance + colour-state requirement ((1/5)^10 × colour-correctness ≪ 10⁻⁷) ✓; human ~2-3 min ✓; planning depth STRICTLY DEEPER than L2 — adjacent commute test: swapping witness steps 2 and 3 prevents Y1 from being lit during the only window when the cone is yellow; subsequent step 7 turns the cone red permanently (no yellow filter exists in L3 to revert), so Y1 (yellow) becomes unlightable. Level becomes unsolvable. The defeated trivial heuristic ("rotate to the unilluminated direction first, then walk toward what I see") is named explicitly in §4.L3. Whole-environment human time ≈ 1 + 2 + 3 = 6 min, matching the harness's ~6 min target ✓.

## Adversarial failure-mode sweep

- **Spec-drift to a similar taxonomy entry at L2 or L3**: L2 adds wax pickup (pickups are present in many reference games — sp80 has 4 pour attempts, ls20 has step-refill pickups in L2). The lq5x wax pickup extends cone *range*, not step budget; ls20's pickups refill steps; sp80's pour attempts limit a different verb. Functionally distinct. L3 adds filter cone-colour; no taxonomy entry has "filter cells re-tint a projected cone" as a mechanic. NO drift detected. ✓
- **Sprite shape accidentally reads as digit/letter**: 3×3 yellow square with central off-black pixel = looks like "filled square with a hole". Not "8" (which would have two stacked rings), not "0" (which would be a hollow ring), not "B" or other letter. Hollow 3×3 ring (target sprite) doesn't read as a digit at the rendered resolution; the four sides are 1-cell-wide and the centre is 1-cell-wide — this is geometric, not glyphic. 1×1 single-cell sprites (pickups, filters) are atoms of colour, not glyphs. ✓
- **Pseudo-multi-mechanic**: each level's witness exercises every declared mechanic; refutations show every mechanic strictly required. Not pseudo. ✓
- **Tutorial too hard**: L1 5-action witness; near-zero planning; only 2 mechanics to discover (walk + rotate). Random has 3×10⁻⁴ chance of stumbling — borderline-near-zero, on the random-resistance floor. ✓ (Per the harness: L1 may be "occasionally" stumbled by random, which is acceptable by design.)
- **Wrong level count**: 3 levels. ✓
- **Negative-similarity drift**: spec didn't move the candidate closer to any prior or taxonomy entry. The dark open arena + lit cone + filters is visually further from kf42/qz73/kx14/qb84 than at pick time, not closer. ✓

## Verdict

**PASS** — every checklist item (1-16 + 10a) passes; novelty check returns **NOVEL** for every taxonomy and prior-game row. Transition to `implement`.
