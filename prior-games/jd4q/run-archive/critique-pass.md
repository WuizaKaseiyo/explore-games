# Critique pass for jd4q (revision 1)

## Checklist (`design-constraints/checklist.md`)

| # | Item | Status |
|---|---|---|
| 1 | All sprites use palette 0..15 (with -1 transparent) | ✅ PASS — avatar {6,7,-1}, echo {11,-1}/{12,-1}, walls {5}, doors {3,10}/{3,5}, pickups {14,9,12}, goal {15,0}, eraser {13,6,-1}. All in palette. |
| 2 | File structure follows universal-scaffold.md | ✅ PASS — implementation in `implement` will follow scaffold (imports → sprites → levels → constants → HUD → game class). |
| 3 | `available_actions` is subset of [1..7] | ✅ PASS — `[1, 2, 3, 4, 6]`. |
| 4 | Exactly 3 Level entries | ✅ PASS — L1, L2, L3 specified. |
| 5 | Game ID 4 chars lowercase alphanumeric, no collision | ✅ PASS — `jd4q`; not in 25 reserved nor 27 priors. |
| 6 | Mechanics draw from `core-knowledge-priors.md`'s 4 categories | ✅ PASS — objectness + basic geometry/topology. |
| 7 | No letters / digits-as-glyphs / real-world clipart / cultural conventions | ✅ PASS — eraser clarified as topological "+" (not letter "X"); goal clarified as square frame (not round "0" digit); pickups are diamond outlines; avatar is abstract magenta block; doors are abstract panel-with-rim. |
| 8 | At least 2 distinct mechanics | ✅ PASS — 4 mechanics across the environment (walk, echo-teleport, closing-doors, eraser). |
| 9 | L1 is tutorial with reduced state, base dynamic, no on-screen text | ✅ PASS — L1 is a single corridor walk; one mechanic (walk); ACTION6 disabled; no text/labels. |
| 10 | L2 and L3 compose every available mechanic (not just scale) | ✅ PASS — L2 composes walk+echo-teleport+closing-doors (closing-doors trigger sealing that traps the avatar; teleport-via-trail is the only escape). L3 adds eraser composed with all (eraser wipes trail, ordering branch-visits around it is the L3 puzzle). |
| 11 | Mechanic inheritance and +1-or-+2 rule | ✅ PASS — L1 N=1; L2 introduces +2 → 3 mechanics required; L3 introduces +1 → 4. Every L1 mechanic active and required at L2 and L3; every L2 mechanic active and required at L3. |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ PASS — per-mechanic counterfactuals stated for L1, L2, L3 with concrete cell/sprite blockers (closing-door corridors, eraser-on-only-path, walls flanking branches). Trivial fallbacks enumerated and rejected: skip-pickup at L2 fails win predicate; greedy-nearest-first at L3 traps at K_A after eraser-wipe. |
| 13 | Mechanic family absent from taxonomy-of-25-games.md | ✅ PASS — `echo-trail-teleport` not in 25 reference games. |
| 14 | Mechanic family absent from prior-games/index.md | ✅ PASS — 27 priors scanned, none match. |
| 15 | Distinguishing rule for near-misses articulated | ✅ PASS — §9 has concrete distinguishing rules vs g50t, lf52, bp35, sk48, tu93, kf42, fz5j, kn58, wt39, zk9p, rk7x, zd7m, xn5p, vn8d, mr5q, pf3w, tg6w, lv4k, gv47, hr8q, ng52, pj7k, pz4t, lq5x, vp6h, qz73, qb84, kx14, gx7m, kp9z, bx84, wa30. |
| 16 | Win condition stated for environment | ✅ PASS — `_check_win()` predicate (per-level required_pickups + on-goal). |
| 17 | Lose condition stated | ✅ PASS — `_check_lose()` (step budget exhausted). |
| 18 | Difficulty floor/ceiling per level | ✅ PASS — per L1/L2/L3 spec has all 4 bullets. L1 (a) acceptable random-tutorial, (b) ~30s, (c) no planning, (d) budget 30 ~3× witness. L2 (a) low random success, (b) ~2 min, (c) decision space 2 at start + post-discovery wrong-alt "skip pickup_a" + witness reasoning chain, (d) budget 60 ~2.4× witness 25. L3 (a) very low random, (b) ~3-4 min, (c) decision space 2 at start (≥L2's), trivial heuristic "greedy nearest" fails (visits C first, eraser wipes trail, traps at K_A), witness reasoning chain, (d) budget 100 ~3.1× witness 32, doesn't shrink relative to L2. |
| 19 | No hidden state (every mutated state has persistent visual cue) | ✅ PASS — avatar position visible; echoes visible (yellow→orange fade); pickups removed visually on collect; closing-doors swap to sealed sprite; step-counter HUD bar; no hidden-state mutation that lacks a visual cue. |
| 20 | Don't generate low-resolution game | ✅ PASS — 64×64 grid with 4×4 sprites that have internal pixel structure (avatar swirl with eye, echo plus-shape, doors with grey rim and coloured interior, pickups with diamond outline + white centre, goal as purple frame, eraser with maroon corners + magenta cross). No chunky uniform-colour cell-blocks. |
| 21 | Design the UI to teach | ✅ PASS — Sprite UI ≈ role: avatar (movable, distinct magenta+pink), echoes (yellow trails, clearly clickable), doors (panel-like with rim, two states distinguishable), pickups (visibly collectible items), goal (frame-with-centre, terminal cell), eraser (visually distinct from all others — maroon+magenta cross). Identical visuals share role: three pickups have the same diamond-outline shape (shared role: collectibles); their colours distinguish for tracking. Visual carries mechanic: closing-door state is visible via colour-swap; eraser is visible as the only maroon-pattern cell on the only path to goal; trail-wipe is visible via echoes vanishing. |

## Novelty (`mechanic-novelty/similarity-check.md` + `negative-similarity-check.md`)

- Re-ran similarity-check on the FULL spec (not just the family
  name). For each near-miss in the taxonomy or prior-games, the
  distinguishing rule is concrete (not "it's different") — see §9
  paragraphs.
- Re-ran negative-similarity check on the fleshed-out spec across
  the 8 dimensions. Closest priors (g50t ghost-replay; lf52
  fog-of-war; zd7m cohort-step-route; bp35 procedural-graph-walk;
  fz5j phase-step-tile) each share fewer than 3 dimensions with
  jd4q, especially heavier dimensions 6/7/8 (palette signature,
  pixel grain, core dynamic). The candidate's question to the
  player ("which echo to bookmark, and which branch to save for
  last") is genuinely distinct from the priors' core dynamics.

✅ PASS — verdict: **NOVEL**.

## Verdict

All 21 checklist items pass. Novelty is NOVEL. **Transitioning to
implement.**
