# Mechanic pick — jd4q

## ID
`jd4q` — 4 lowercase characters, alphanumeric, opaque (no English word).
Verified not in the 25 reference IDs and not in `prior-games/index.md`'s
`game_id` column (27 prior entries scanned: kf42, qz73, kx14, qb84, lq5x,
gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x,
gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w).

## Mechanic family
`echo-trail-teleport`

## One-paragraph description
The player walks an avatar across a maze grid using arrow keys; every cell
the avatar enters becomes a glowing **echo-stone** for the next K subsequent
steps, then fades back to floor. Echo-stones are clickable: clicking a
visible echo teleports the avatar back to that cell instantly, but the
teleport **consumes the echo and every echo placed after it** (so jumping
back rewinds the trail to that point in time). The puzzle dynamic is
managing where you have been as a set of bookmark-able escape hatches,
because the world has **closing-doors** — special tiles that seal once the
avatar has walked off them, sealing forward routes that you must rewind
through to traverse usefully. L1 is a basic walk to a single target.
L2 introduces echo-teleport (no closing-doors yet, but echo-teleport is
already required because L2's geometry has dead-ends that force a
detour-then-rewind). L3 layers closing-doors on top of L2's mechanics:
one-way doors close behind the avatar each step, so visiting multiple
collect-cells in a single forward pass becomes impossible and
echo-teleport must be used to re-enter previously-traversed corridors.

## Action plan
- ACTION1..4: walk avatar one cell up/down/left/right.
- ACTION6: click an on-screen echo-stone to teleport the avatar to that
  cell (consumes echo + all echoes placed after it).
- No ACTION5, no ACTION7. Subset `[1, 2, 3, 4, 6]` — same shape as
  ka59/dc22/m0r0/wa30. Distinct from those by the click semantic.

## Distinguishing-rule novelty notes

### vs taxonomy near-misses (similarity-check.md procedure)

- **g50t (walk-vs-scroll / ghost-replay-multitarget)** — both have an
  avatar walking with visible past-position artefacts. **Distinguishing
  rule:** g50t's ACTION5 commits the path so far as a ghost that
  replays in lockstep with the avatar on subsequent moves; ghosts
  *accumulate* and *animate* every step. jd4q's echoes are *static*
  fading dots that mark where the avatar has been and are *consumed*
  by clicking. g50t adds ghosts to the world; jd4q removes echoes
  from the trail. Action verb differs (commit vs click-on-trail);
  outcome differs (accumulate ghosts that replay vs erase forward
  trail and teleport).
- **lf52 (fog-of-war-sokoban)** — both have undo-flavoured backtracking.
  **Distinguishing rule:** lf52 is Sokoban with single-block push and
  ACTION7-undo of the most recent commit. jd4q has no block-pushing,
  no fog-of-war, and no single-step undo — instead it has multi-step
  rewind via clicking any visible echo. Cast (avatar+block+fog+target
  vs avatar+echoes+closing-doors+targets) differs.
- **bp35 (procedural-graph-walk)** — both involve a click that
  teleports. **Distinguishing rule:** bp35 walks a procedurally-built
  graph of nodes; click teleports to a *highlighted neighbour node*
  (the graph defines who can teleport to whom). jd4q walks a 64×64
  grid in continuous Manhattan steps; clicks teleport only to
  *prior-self positions* the avatar previously visited. Topology
  differs (graph vs grid) and teleport target differs (graph
  neighbour vs prior trail point).
- **sk48 (paired-snake-trail-match)** — both have visible trails. 
  **Distinguishing rule:** sk48's trail is a list of body-segments
  that grow and shrink as a snake walks, with paired snakes whose
  trail colours must match cell-by-cell. jd4q's "trail" is a sparse
  set of fading echoes (not a connected segmented body), and the
  goal has nothing to do with cell-colour matching across pairs —
  it's grid-navigation under closing-doors.
- **tu93 (lockstep-multi-maze)** — both have grid maze + walk. 
  **Distinguishing rule:** tu93 walks every primary agent in
  lockstep on a directional press; jd4q has a single avatar with
  echo-teleport. No lockstep mechanic.
- **wa30 (lock-drag-crate)** — both have ACTION1..4 walking with
  ACTION-extension. **Distinguishing rule:** wa30 uses ACTION5 to
  pick-up/drop crates against tagged adjacency; jd4q uses ACTION6
  to click an echo to teleport. Crate-delivery (wa30) vs
  trail-jump (jd4q) are different verbs and different goals.

### vs prior-games entries

- **kf42 (tether-pawn-cycle)** — kf42 has paired pawns sharing a
  max-distance tether with click-to-select. jd4q has a single avatar
  with self-deposited echoes. No tether, no second pawn.
- **fz5j (phase-step-tile)** — fz5j has tiles that pulse open/closed
  on per-cell periods 2/3/4 with avatar-respawn-on-closed. jd4q has
  no autonomous tile-pulsing — closing-doors close *only* after the
  avatar has walked off them, deterministically driven by the
  avatar's actions, not time.
- **kn58 (anchor-pull-magnet)** — kn58 click places a magnet anchor
  that slides every coloured pawn one cell on its dominant axis. 
  jd4q's click teleports the avatar to a self-deposited echo; no
  pawn-on-grid radial attraction; no global per-click slide.
- **bx84 (beam-mirror-reflect)** — bx84 emits a continuous beam,
  click drops/cycles mirrors. jd4q has no beam, no mirrors. Different
  cast.
- **wt39 (glide-deflect-thaw)** — wt39 has gliding pawns that deflect
  off bumpers and crack thaw-tiles. jd4q has cell-by-cell walking
  (not glide), and closing-doors close behind the avatar, not
  underfoot. The action is per-step navigation, not slide-until-stop.
- **zk9p (pursuer-merge-walk)** — zk9p has autonomous pursuer AI.
  jd4q has no AI agents, only the player avatar.
- **rk7x (live-switch-routing)** — rk7x has an autonomous courier
  walking one cell per click; player toggles junction blades. jd4q
  has no autonomous walker; the player walks the avatar directly.
- **gx7m (gear-mesh-cascade)** — different family (rotation
  propagation through meshed gears). No overlap with trail-jump.
- **kp9z (grain-accumulate-topple)** — different family (grain
  accumulation+topple cascade). No trail-jump.
- **zd7m (cohort-step-route)** — zd7m has portals that teleport to a
  sealed chamber; multiple movable pawns step in cohort. jd4q has a
  single avatar; "teleport" is jumping to a *self-trail* echo
  (player-deposited and player-consumed), not a fixed portal pair.
- **xn5p (chamber-stamp-partition)** — xn5p stamps walls to subdivide
  regions. jd4q has no wall-stamping; closing-doors close
  automatically after the avatar moves off, not by player action.
- **vn8d (domino-cascade-topple)** — different (chain-reaction click).
- **mr5q (polarity-attract-discharge)** — different (polarity flip +
  global walk-toward).
- **pf3w (wavefront-converge-timing)** — different (timing-based
  wavefront BFS coincidence).
- **tg6w (settle-pile-tilt)** — different (gravity tilt with sliding
  blocks).
- **lv4k (lever-balance-torque)** — different (static torque sum).
- **gv47 (seed-grow-surround-dissolve)** — different (region growth
  by paint).
- **hr8q (pair-blend-recipe)** — different (ingredient blend recipe).
- **ng52 (multiset-signature-classify)** — different (classify into
  bins).
- **pj7k (rolling-cube-face-paint)** — different (cube rolling).
- **pz4t (anchor-pivot-place)** — different (jigsaw with anchor
  pivot).
- **lq5x (lantern-cone-illuminate)** — different (cone projection).
- **vp6h (shadow-cast-collect)** — different (collect under shaded
  cells).
- **qz73 (radial-cycle-lock)** — different (rotor with lockable tips).
- **qb84 (bead-lift-swap)** — different (lift+swap chain navigation).
- **kx14 (tide-tilt-buoyant)** — different (vertical fluid tank).

## Negative-similarity check (negative-similarity-check.md procedure)

Walking the 8 dimensions against the closest priors, mentally
rendering jd4q's L1:

**vs g50t** (closest taxonomy near-miss):
1. *Board:* avatar + maze + fading echo dots + collect targets vs
   avatar + maze + scrolling timer sprite + ghosts + targets. 
   **Different.** Echoes are stationary fading dots; ghosts are
   continuous-replay lines.
2. *Player input:* arrows + click-on-echo vs arrows + ACTION5-commit. 
   **Different.**
3. *Level asks:* reach a target / collect cells under closing-doors
   vs cover all targets via ghost-paths union. **Different.**
4. *Lose:* step budget vs scrolling timer falls off. **Different.**
5. *Cast:* avatar + echoes + walls + closing-doors + target vs
   avatar + ghosts + targets + scroll-timer. **Different.**
6. *Visual signature:* magenta+pink+yellow+green palette with
   detailed avatar swirl, echo star-burst, closing-door petal pattern
   vs g50t's softer palette with timer-strip. Plan **different
   palette signature**.
7. *Pixel grain:* design pawn at 4×4 (or larger) with internal
   structure. Avoid 1×1.
8. *Core dynamic:* "manage temporal trail as escape hatches" vs
   "every past commit is also playing now". **Different question
   the player asks themselves.**
   
*Shared dimensions:* effectively 0 of the 8 once palette and grain
are designed against the cautionary tale. **Pass.**

**vs kf42 (cautionary tale)**:
1-8: avatar count differs (1 vs 2), no tether, different verb,
no colour-tinting pad. **Effectively 0 dimensions shared** beyond
"step counter HUD" (dim 4) which is universal. **Pass.**

**vs fz5j**:
1. board: avatar + maze + closing-doors + echoes vs avatar +
   maze + period-pulsing tiles. **Different.**
2. action: arrows + click-on-echo vs arrows only. **Different.**
3. level asks: reach targets via rewind vs reach goal between
   pulses. **Different.**
4. lose: budget vs lives (3). **Different.**
5. cast: avatar + echoes + doors vs avatar + period-tiles +
   walls. **Different.**
6. visual: explicit echo-dots and door-state visuals vs pulsing
   tile flicker. **Different.**
7. grain: design rich. 8: rewind-via-trail vs synchronise-with-pulse.
   **Different.**

*Shared:* 0-1 dimension. **Pass.**

**vs zd7m**:
1-8: cohort vs single-avatar; portals (fixed pair) vs echoes
(player-deposited); different goals. **Mostly different.**

*Shared:* 0-1 dimension. **Pass.**

## Sanity check on §3.4 priors and forbidden elements
- Core-knowledge prior: **objectness** (avatar, echoes, doors as
  persistent entities) + **basic geometry/topology** (maze
  connectivity, closing-doors changing topology). No basic-physics
  prior, no agentness. Two priors mixed — within the recommended
  2-3 sweet spot.
- Forbidden elements: no letters, no digits-as-glyphs, no real-world
  clipart. Echoes will be abstract circular fade-rings; closing-doors
  will be abstract framed cells; avatar will be an abstract swirl.
  No directional arrow glyphs.
- Step counter: yes, universal HUD bar.
- 64×64 grid: yes (full grid; logical size = display size; no chunky
  upscale).
- 3 levels: yes, with strict +1 / +1 mechanic-introduction per
  promotion (L1 base walking system, L2 adds echo-teleport, L3 adds
  closing-doors).
- Tag-based sprite querying: planned.
- Reduced state space at L1: small maze, ~8 cells path, no doors,
  no echoes-required.

## Verdict
**NOVEL** against all 25 reference taxonomy entries and all 27
prior-games entries. Family `echo-trail-teleport` distinguished by
concrete distinguishing-rule paragraphs from each near-miss.
Negative-similarity check passes against all priors mentally
rendered.
