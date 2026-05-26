# Mechanic pick — ds5q

## ID
`ds5q` — 4 lowercase chars; not in the 25-game reserved list; not in `prior-games/index.md`; not an English word.

## Mechanic family
**wall-erode-chain**

## One-paragraph description
The player walks an avatar (arrows) through a maze of coloured-stripe walls inside a walled chamber. ACTION5 swings a coloured "pickaxe" — every wall in the avatar's 4-cardinal neighbourhood whose colour matches the pickaxe loses one hardness layer; walls reaching zero become passable. The pickaxe starts un-coloured (no walls erode-able) and is recoloured by stepping onto a coloured charge-pad on the floor. From L3 onward, walls of the same colour share a single hardness counter, so eroding any wall of colour C globally reduces every wall of colour C — letting the player chip a wall they cannot stand next to (sandwiched between unbreakable obstacles) by hitting a sibling-coloured wall they can. Goal each level: reach the exit cell.

## Mechanic enumeration (per-level, for write_spec)
- L1 — walk + erode-adjacent. Tutorial: avatar, two soft walls, exit. (N = 2 mechanics required by witness.)
- L2 — walk + erode + colour-matched-pickaxe (+1 new). Avatar starts un-charged; must visit a coloured charge-pad before erode does anything; only same-colour walls erode. (N = 3.)
- L3 — walk + erode + colour-matched-pickaxe + colour-chain-hardness (+1 new). Same-colour walls share hardness globally; one wall is unreachable for direct erosion and can only be cleared via its sibling-coloured wall elsewhere. (N = 4.)

## Action subset
`[1, 2, 3, 4, 5]` — arrows + ACTION5. **No click.** Pure-arrow input dodges the "click-to-edit-terrain" surface signature shared by xn5p and vd3g.

## Core knowledge priors used
- **Objectness** — walls, charge-pads, avatar, exit are coherent persistent entities.
- **Basic geometry & topology** — connectedness of passable cells changes as walls erode; the chain-link rule at L3 is a topological identification of wall classes by colour.

## Positive similarity check (per `mechanic-novelty/similarity-check.md`)

### Closest taxonomy entries
- **xn5p (chamber-stamp-partition)** — *Family-level match: walled chamber + walking pawn + wall manipulation.* Distinguishing rule: xn5p **ADDS** walls (stamps) to subdivide one connected region into per-colour subregions; ds5q **REMOVES** wall layers (erodes) to merge or open passages. Verb is opposite-direction. Goal is "match per-colour partition" (xn5p) vs "reach exit cell" (ds5q). xn5p has no hardness layering and no global colour chain.
- **bx84 (beam-mirror-reflect)** — *Family-level near-miss: routing through colour-matched obstacles.* bx84 routes a coloured beam through mirrors/filters. ds5q routes the avatar (not a beam) by removing walls; no beams, no reflection, no projection cells.
- **wt39 (glide-deflect-thaw)** — *Family-level near-miss: walking + breakable/changing tiles.* wt39 has avatar GLIDE (not step) and brittle thaw-tiles that crack passively after one slide. ds5q is single-step walk; tile state changes only via the player's deliberate erode action; cracking is colour-gated and chain-linked.
- **vd3g (valley-dig-roll, prior game)** — *Family-level near-miss: click-edit-terrain + routing.* vd3g click-toggles cell HIGH/LOW for marbles to flow downhill. ds5q has no marbles, no flow, no toggle (erosion is a reduction, not a flip), and uses ACTION5 instead of click. Different topology (cells with height vs walls with hardness levels) and different routed entity (marbles vs avatar).
- **xn5p (prior game, second pass)** — *Most recent prior using walls + walking pawn.* Same distinguishing rule as the taxonomy match above (additive partition vs subtractive traverse).

### Closest prior-games-index entries
- **xn5p — chamber-stamp-partition** — see above.
- **vd3g — valley-dig-roll** — see above.
- **fz5j — phase-step-tile** — *Closest "tiles change state" prior.* fz5j tiles auto-pulse OPEN/CLOSED on per-cell periods (autonomous timing); the player has no control over WHEN a tile changes, only over WHEN they step. ds5q wall state changes only in response to the player's ACTION5; player has full agency over wall state. fz5j has lives + respawn; ds5q has no lives.
- **ek73 — wake-trail-evade** and **jd4q — echo-trail-teleport** — *Walking-and-trail family.* Both involve the avatar's walked cells changing behind it. ds5q is the OPPOSITE — the player changes the cells *ahead* of the avatar (ahead-walls erode). No trail behind in ds5q.
- **tg6w — settle-pile-tilt** — *Closest "field-mutating action" prior.* tg6w arrow-tilts the entire playfield gravity; loose blocks slide globally. ds5q ACTION5 erodes locally adjacent walls; arrows just walk the avatar one cell. tg6w has no avatar-as-locus.
- **kn58 — anchor-pull-magnet** — *Click-place-then-global-effect family.* kn58 click places an anchor, all pawns slide one cell toward it. ds5q has no global-pull; erosion is local to the avatar; no click action.

## Negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)
Walked the 8 dimensions against each closest prior. The heaviest scrutiny is xn5p (closest by family on dimensions 1, 2, 5, 7 = "walled chamber + walking pawn + walls + rich pixel grain"). Divergence is concentrated on dimensions 3, 6, 8 — the named-principle-heavy dimensions:

- **Dim 3 (what the level asks for)**: xn5p partitions; ds5q traverses. Different goal-shape.
- **Dim 6 (visible visual signature)**: xn5p's L1 frame shows a flat-floor chamber with painted-floor colour pads and a thin avatar; ds5q's L1 frame shows a chamber dominated by **layered-stripe wall sprites** (each wall cell has internal hardness banding) plus floor-tinted charge-pad insets at L2+ and a small avatar holding a visible pickaxe. The dominant visual element is the wall, not the floor.
- **Dim 8 (core dynamic)**: xn5p's question is "where to draw walls so coloured cells fall into matching subregions?". ds5q's question is "which wall to weaken in what order, and which colour to pick up first, so my path opens before I run out of step budget?". Different planning content; different temporal pacing (xn5p partition is one-shot per intent, ds5q erosion is multi-erode-per-wall).

Dimensions 4 (kills via step budget — universal across all 25+41 priors) and 5 (cast: walls+avatar+target — universal across walking puzzles) are not informative here.

ds5q does not share three or more named-principle dimensions with any single prior. Negative test passes.

## Visual & palette plan (preview, fleshed out in spec)
Dominant palette: light-grey background (2), wall stripes alternating off-black (4) and grey (3), charge-pads in saturated colours (8 red / 9 blue / 11 yellow / 14 green) with a thin black rim, avatar in maroon (13) with a white-tipped pickaxe (0) that recolours when charged. Exit cell as a hollow black-bordered ring with off-white interior. Step counter as a thin draining bar at the top. This palette signature does not match any prior's dominant signature on the index — it is wall-dominated, not floor-dominated.
