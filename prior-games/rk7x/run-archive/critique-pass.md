# critique-pass.md — `rk7x` spec critique

Adversarial review of `mechanic-spec.md` against
`design-constraints/checklist.md` items 1-18, plus
`mechanic-novelty/similarity-check.md` (positive) and
`mechanic-novelty/negative-similarity-check.md` (negative). Critique
visit count: 1 (this is the first entry to `critique_spec`).

## Format & structure (items 1-5)

- ✅ **Item 1** — Palette only 0..15 + `-1`. Sprites use 3, 4, 5, 6, 8, 9,
  10, 11, 12, 13, 14, 15 plus `-1`. PASS.
- ✅ **Item 2** — Universal scaffold structure described in §3, §5, §6.
  Camera viewport will be sized to (16, 16) in `on_set_level` per
  `universal-scaffold.md`'s camera-resize requirement (§5 step 1
  references this). PASS.
- ✅ **Item 3** — `available_actions = [6]` ⊂ [1..7]. Pure click. PASS.
- ✅ **Item 4** — EXACTLY 3 levels. §4 explicitly enumerates L1, L2, L3.
  PASS.
- ✅ **Item 5** — ID `rk7x` is 4 chars, lowercase alphanumeric. Verified
  not in the 25-game reserved list and not in `prior-games/index.md`'s
  16 rows. Not an English word. PASS.

## §3.4 priors & constraints (items 6-10)

- ✅ **Item 6** — Mechanics use objectness, geometry/topology, and
  agentness (per §2 of spec). No physics, no symbolic priors. PASS.
- ✅ **Item 7** — Forbidden elements check.
  - No letters: sprites are solid blocks, hollow rings, concentric
    squares, internal cross.
  - No digits as glyphs: no sprite spells a digit.
  - No real-world clipart: courier, switch, stop, terminal sprites
    are all abstract pixel patterns.
  - No cultural conventions: courier "tip" is a single asymmetric
    pixel, not an arrow-glyph; junction central cross is topological,
    not directional. Palette doesn't follow green=go / red=danger
    (red is a stop colour; green is a switch-state colour). PASS.
- ✅ **Item 8** — At least TWO distinct mechanics (L2 has 2; L3 has 4).
  PASS.
- ✅ **Item 9** — L1 is a tutorial: single junction, single courier, no
  on-screen text, single base mechanic (live switch routing). The
  reduced state space and discoverability-by-play criteria are met.
  PASS.
- ✅ **Item 10** — L2 and L3 increase difficulty by COMPOSING every
  available mechanic. L2's witness exercises switch routing AND stop
  visiting (both required: see §4 L2 necessity-per-mechanic). L3's
  witness exercises all 4 mechanics (see §4 L3 necessity-per-mechanic).
  No level scales by grid-size or item-count alone. PASS.

## Mechanic structure (items 11-12)

- ✅ **Item 11** — Mechanic inheritance and +1-or-+2 rule.
  - L1 N = 1.
  - L2 M = 2 = N + 1 (carry: live-switch-routing; new: coloured stops).
  - L3 P = 4 = M + 2 (carry both; new: dual couriers, conflict cells).
  - Both promotions are within {+1, +2}. No mechanic drops out at any
    level. The L2 witness toggles switches AND visits stops (both L1
    and L2 mechanics exercised). The L3 witness exercises all 4. PASS.
- ✅ **Item 12** — Strict counterfactual necessity (per-mechanic table):

  | Level | Mechanic | Solvable without M? | Concrete reason |
  |---|---|---|---|
  | L1 | live-switch-routing | NO | Default blade routes courier into wall at (8, 2); terminal at (8, 14) only reachable after toggle. Spec §4 L1 necessity. |
  | L2 | live-switch-routing | NO | Defaults send courier directly to terminal but bypass both stops; terminal is gated by stops, so without toggling courier walks past inactive terminal into wall at (15, 7). Spec §4 L2 necessity-1. |
  | L2 | coloured-stops | NO | Win predicate is `(on terminal) AND (all stops visited)`. Without the stops constraint, a one-toggle solution exists (just route through one detour); the all-stops requirement is what forces both detours. Spec §4 L2 necessity-2. |
  | L3 | live-switch-routing | NO | All defaults route both couriers east into walls at (15, 1) and (15, 14). Three toggles are required to swap rows. Spec §4 L3 necessity-1. |
  | L3 | coloured-stops | NO | Win requires colour-matched stop visits. Each colour's stops are placed only on that colour's required detour path. Spec §4 L3 necessity-2. |
  | L3 | dual-couriers | NO | Win predicate requires both terminals occupied; with one courier, only one terminal can be reached. The level layout has terminals at opposite corners. Spec §4 L3 necessity-3. |
  | L3 | conflict-cells | NO | The shortest two-courier swap-rows route brings both to the swap junction at the same tick → collision lose. Witness uses a 2-cell holding-loop detour at (7, 4) to desync arrivals. Without the conflict-cell rule, the no-detour path would win in fewer ticks; with the rule, the detour is mandatory. Spec §4 L3 necessity-4. |

  Each row names a specific cell or rule that blocks every alternate
  path. No "yes" answers; no hand-waving. PASS.

## Novelty (items 13-15)

- ✅ **Item 13** — Mechanic family `live-switch-routing` is not in
  `mechanic-novelty/taxonomy-of-25-games.md`. Closest matches (tn36,
  bp35, sp80, vn8d) addressed in spec §9 with concrete distinguishing
  rules. PASS.
- ✅ **Item 14** — Mechanic family is not in `prior-games/index.md`.
  Closest matches (vn8d, bx84, kn58, pj7k, wt39) addressed in spec §9
  with concrete distinguishing rules. PASS.
- ✅ **Item 15** — For every flagged near-miss, the spec articulates the
  concrete distinguishing rule (in §9 of the spec). The closest
  taxonomy match (tn36 — program-pawn-trace) gets a one-paragraph rule
  that names the specific structural difference: "tn36 is
  compose-then-run; rk7x is edit-during-execution; rk7x has no tape
  sprite, no commit verb, no run-button". PASS.

## Solvability (items 16-18)

- ✅ **Item 16** — Win condition stated as a concrete testable predicate
  (§7): courier on terminal AND all required stops visited. PASS.
- ✅ **Item 17** — Lose condition stated as concrete testable predicates
  (§8): wall hit, conflict cell (L3), step budget exhausted. PASS.
- ✅ **Item 18** — Difficulty floor and ceiling per level. All four
  bullets per L1, L2, L3 in §4:
  - **L1**: (a) random ≈ 2.3% with double-toggle correction; (b) ~30s;
    (c) "no strict planning requirement" (matches L1 rule); (d)
    budget 24 over witness 14 (slack 10).
  - **L2**: (a) random < 0.0001%; (b) ~2 minutes; (c) decision space
    of 5+ first actions, named wrong path (forgetting an out-junction
    or losing parity), reasoning chain across 4 ordered toggle
    checkpoints; (d) budget 60 over witness 30 (slack 30).
  - **L3**: (a) random < 1 in 100k; (b) ~3 minutes; (c) decision space
    ≥ 6 first actions ≥ L2's; named heuristic that fails ("greedy-
    toward-target"); divergence from witness at the holding-loop
    detour at (7, 4); reasoning explicitly post-discovery (the
    fully-informed player must reason about timing synchrony, not
    discover the conflict-cell rule); operational test confirms
    heuristic produces a different action sequence than the witness;
    (d) budget 96 over witness 50 (slack 46).

  Slack is strictly non-decreasing across levels (10 → 30 → 46),
  satisfying difficulty-rule §2(d) "budget must NOT shrink relative
  to the witness as level number rises". PASS.

## Novelty re-check on the FULL spec (positive)

Re-walked `similarity-check.md` against the now-detailed spec, not
just the family-name. The L2 mechanics (coloured stops gating win)
and L3 mechanics (dual couriers, conflict cells) introduced new
features that could in principle drift toward priors. Re-checked:

- **L2 + tn36**: tn36's stops-as-target are points the trail must
  light up; rk7x's stops are corridor-cells the courier walks over.
  Different mechanism. PASS.
- **L2 + sk48 (paired-trail-match)**: sk48 has heads on tracks
  drawing trails; mine has a courier visiting stops. sk48's trail
  IS the puzzle state; mine's trail is just the courier's history.
  Different. PASS.
- **L3 + tu93 (lockstep-multi-maze)**: tu93's agents move on player
  arrow input lockstep; rk7x's couriers walk autonomously. Verb is
  fundamentally different (no arrow input in rk7x; no autonomous
  walking in tu93). PASS.
- **L3 + zk9p (pursuer-merge-walk)**: zk9p has pursuers that chase
  the player and self-collide → merge → vanish. rk7x has two
  couriers with NO pursuit relationship; they walk independently
  along corridors. Conflict-cells in rk7x cause LOSS, not merge-
  vanish. PASS.

No drift. PASS.

## Novelty re-check on the FULL spec (negative)

Re-walked `negative-similarity-check.md`'s 7 dimensions against
every prior, focusing on L2 and L3 visual signatures (which add
stops, terminals, and second courier).

Highest-overlap candidate: **tu93** (multi-agent grid maze).
Dimension-by-dimension:

1. *What is on the board.* tu93: maze-shaped underlay + agents +
   exits + species-pickups + walls. rk7x: corridor-network walls
   + 1-2 couriers + switches + stops + terminals. Lists differ —
   tu93 has species-pickups; rk7x has switches. NOT shared.
2. *What player physically does.* tu93: presses arrows for lockstep.
   rk7x: clicks switch cells (no arrows). NOT shared.
3. *What the level asks for.* Both: get every agent to its exit.
   PARTIAL share.
4. *What kills the player.* tu93: step counter + agent destruction
   by enemies. rk7x: step counter + wall hit + courier-courier
   collision. PARTIAL share (step counter only).
5. *Cast of supporting elements.* Walls + agents + targets is
   universal-doesn't-count.
6. *Visual signature.* tu93 uses checker-grey walkable underlay
   filling most of the screen; rk7x uses solid grey corridors
   framed by black walls with green/magenta junction blades. NOT
   shared.
7. *Pixel grain.* tu93's primary agent is a 3-cell-tall pawn with
   minimal internal structure on a high-density walkable underlay;
   rk7x's primary agent is a 4×4 sprite with 2×2 inner block + 1
   directional tip on a low-density corridor (most cells are
   walls). NOT shared.
8. *Core dynamic.* tu93: "press direction → all agents move
   lockstep". rk7x: "click switch → switch toggles AND all couriers
   walk one cell autonomously". NOT shared.

Shared dimensions: 3 (partial), 4 (partial). Total ≈ 1 strong
share. Below threshold of 3. PASS.

Other priors scored at most 2 partial shares (per the table in
`mechanic-pick.md`). PASS.

## Final verdict

**ALL 18 CHECKLIST ITEMS PASS. NOVELTY POSITIVE AND NEGATIVE BOTH PASS.**

Spec is ready for `implement`. Minor implementation notes for the
implement state to keep in mind (these are NOT critique blockers, but
they help the implementation):

- Junction blade semantics need explicit per-junction corridor-topology:
  each junction's two connectible corridor-pairs must be enumerated.
  Document as a `level.set_data("junctions", {(x, y): {"A": ("W", "E"),
  "B": ("W", "S")}, ...})` per-level.
- Click handler order is: (1) toggle if click cell is a switch, (2)
  advance every courier by one cell, (3) check win/lose. This ordering
  matters: a click made on tick K toggles BEFORE the courier on tick K
  walks, so the toggle takes effect during that same tick's courier
  movement IF the courier is approaching the switch but not yet at it.
- Camera resize: `self.camera.width = self.camera.height = 16` in
  `on_set_level`, per `universal-scaffold.md`'s camera-viewport rule.

Transition: `implement`.
