# mechanic-pick

## 4-character ID
`nh4w`

Verified: not in the 25 reserved IDs (`ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30`) and not in `prior-games/index.md` (no row contains `nh4w`). Not an English word.

## Mechanic family tag
`arc-loft-shot`

## One-paragraph description
Arc-Loft Lobber — the player walks a launcher-pawn along the floor with cardinal arrows; clicking any cell within range fires a projectile that travels in a discrete parabolic arc from the launcher's foot-cell to the clicked cell. The arc's peak height equals half the horizontal distance, so short shots fly LOW and long shots fly HIGH. Walls of varying physical heights stand between the launcher and targets; the projectile clears a wall iff its arc height at that wall's column is strictly greater than the wall's height. Hanging ceiling stalactites limit the arc from above: the arc is blocked iff its peak height exceeds the ceiling clearance over its flight column. The win for each level is for the projectile to land on every coloured target square (one shot or several, depending on level). The base dynamic system in L1 is walk + arc-fire; L2 adds floor-walls of varying heights that gate which launcher-positions can clear them; L3 adds hanging ceilings that gate which launcher-positions stay under them, forcing the player to thread the arc between low walls and low ceilings.

## Core-knowledge prior coverage
- **Objectness** ✓ — launcher pawn, projectile, walls, ceilings, targets are all coherent persistent entities.
- **Basic geometry** ✓ — parabolic arc, line-of-flight clearance, peak-vs-height comparison.
- **Basic physics** ✓ — projectile motion under gravity is the canonical physics-prior example (per `core-knowledge-priors.md`).
- **Agentness** ✗ — no autonomous NPCs in this design.

Three of four priors covered; physics + geometry + objectness is the named "common sweet spot" in `core-knowledge-priors.md`.

## Similarity check vs the 25-game taxonomy

Walking the rows in `taxonomy-of-25-games.md`:

- **bp35 — gravity-fall-navigation**: pawn auto-falls one row per step under gravity; arrows side-step; gravity-flippers change axis. **Distinguishing rule:** bp35's pawn falls under gravity AS THE PRIMARY DYNAMIC and the player only controls lateral correction; nh4w's launcher is a static-on-floor walker with full cardinal control, and the parabolic-arc behaviour applies to a SEPARATE projectile sprite that exists only during a fired shot. There is no auto-fall on the avatar.
- **cd82 — orbit-fire-paint**: basket rides an 8-slot ring around a central canvas; ACTION5 fires inward to splash a slot. **Distinguishing rule:** cd82 fires from a fixed ring INWARD at the canvas in straight axial/diagonal slabs; nh4w fires from a freely-walking floor pawn OUTWARD in a parabolic Nova whose trajectory varies continuously with click distance.
- **r11l — centroid-puppet-leg**: click a tray leg, click a target — leg animates toward target with attached heads following. **Distinguishing rule:** r11l's animation is a STRAIGHT-LINE drag (centroid follows leg group), not a parabolic-height arc; r11l has no concept of vertical clearance over walls; the win condition (head-into-lock) and the rigid-body chain are absent.
- **vt6q — grapple-anchor-yank** (also a prior, see below): fires a CARDINAL grapple line that yanks an avatar/anchor along a STRAIGHT cardinal line. nh4w fires a freely-aimed parabolic arc, has no yanking, and has nothing equivalent to a cardinal-only direction.

No taxonomy row passes the family-level + description-level + condition-level overlap test. The closest taxonomy near-miss is bp35 (also gravity-projectile) and cd82 (also fire-and-deposit), neither sharing the parabolic-arc-over-wall dynamic.

## Similarity check vs `prior-games/index.md`

Reading the prior corpus (70 entries):

- **hk7v — overhead-trolley-hook**: gantry trolley + variable-rope hook delivers coloured blocks to coloured floor markers; rope clears walls. **Distinguishing rule:** hk7v's "rope clears walls" mechanic is implemented as a Cartesian-gantry routine — RAISE hook above wall (each press = +1 cell), TRAVERSE horizontally (each press = +1 cell), LOWER. It takes ~80 sequential precise actions per delivery. nh4w's wall-clearance is a SINGLE click-fire whose discrete parabolic arc clears all walls along the column whose height is below `peak_height = horizontal_distance / 2`. The player learns that LONGER shots fly HIGHER (a continuous physics relationship), not that they must press raise/lower keys to manually choreograph altitude. Visual signature: hk7v has an overhead beam with hanging hook (top-down crane); nh4w has a floor-walking pawn with airborne arc (bottom-up lob). Player input: hk7v = raise/lower/slide/grab; nh4w = walk + click-target.
- **vt6q — grapple-anchor-yank**: fire a directed cardinal grapple line. **Distinguishing rule:** vt6q's grapple is a STRAIGHT cardinal line that snaps to the first anchor it hits and either pulls the avatar to it or pulls the anchor to a socket. nh4w's projectile follows a 2D parabolic Nova over a vertical "air" dimension; it has no anchor-yanking dynamic; it lands on a CLICKED cell, not on whatever it first hits.
- **kn58 — anchor-pull-magnet**: click any cell to place a magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it. **Distinguishing rule:** kn58 is a 1-cell sympathetic motion per click of EVERY pawn toward a placed anchor. nh4w is a single-projectile arc whose flight is a multi-frame animation from launcher to click target, with vertical air-clearance dynamics. No "everything slides toward me" behaviour.
- **bx84 — beam-mirror-reflect**: emitter shoots a colored beam; click empty cells to drop mirrors. **Distinguishing rule:** bx84's beam is a STRAIGHT line that reflects at right angles via mirror sprites; geometrically planar, no vertical/peak axis. nh4w's arc has a continuous-altitude vertical axis (even though discrete in pixels) — wall clearance and ceiling block depend on this height, which beams do not have.
- **wt39 — glide-deflect-thaw**: pawn glides in pressed direction until wall; bumpers deflect 90°. **Distinguishing rule:** wt39 is a ground-plane glide of a single pawn (no separate projectile, no air-altitude); the mechanic is glide-until-collision with bumper redirection. nh4w has a separately-fired projectile that flies through air (vertical clearance gate), not a sliding ground pawn.
- **qn7w — pulse-chain-eject**: click pushers to fire momentum pulses through stationary ball-chains; only the terminal ball ejects per pulse. **Distinguishing rule:** qn7w transmits momentum through a PRE-ARRANGED chain of stationary balls; only the chain's last ball ejects. nh4w has no chain, no momentum-transfer; the projectile flies an air arc from launcher to click target.
- **vn8d — domino-cascade-topple**: single click triggers chain reaction through pillars; pads splay 4 ways. **Distinguishing rule:** vn8d's mechanic is chain-reaction cascade through pre-placed pillar topology; no projectile, no arc.
- **kj82 — plank-pivot-walk**: pawn walks long pinned planks; click selects, ACTION5 pivots; springs LAUNCH the pawn along the plank's axis. **Distinguishing rule:** kj82's spring "launch" is a 1D scoot of the pawn along a plank's axis to the plank's far end; it is not a projectile, has no parabolic arc, no air-clearance dynamic. Closest "launch" word in the corpus, but mechanically very different.
- **dj5h — pulley-pair-platform**: overhead pulleys couple paired hanging platforms. **Distinguishing rule:** vertical-coupled platform pairing; no projectile, no arc.

No prior in the corpus passes both the description-level overlap and the core-dynamic overlap. The semantically-closest is hk7v (also "deliver over walls"), and the per-row distinguishing rule above gives the concrete mechanical difference.

## Negative-similarity check (per `negative-similarity-check.md`)

Walking the 8 dimensions against the closest prior, **hk7v**:

1. **What is on the board.** hk7v: overhead gantry beam at top of frame, hanging trolley + rope + hook descending into open arena, walls dividing the floor, coloured supply blocks on the floor, coloured floor-stripe targets. nh4w: floor-walking launcher pawn (small avatar shape with a stubby muzzle), wall-stacks of various heights rising from the floor, coloured floor-target squares, hanging ceiling stalactites of various clearances. **Different cast.**
2. **What the player physically does on input.** hk7v: ACTION1/2 raise/lower hook (vertical micro-positioning), ACTION3/4 slide trolley (horizontal micro-positioning), ACTION5 grab/release. nh4w: ACTION1/2/3/4 walk launcher, ACTION6 click cell to fire arc. **Completely different input pattern** (Cartesian gantry vs walk-and-aim).
3. **What the level is asking for.** hk7v: each coloured supply block delivered to its same-coloured floor target. nh4w: each coloured target hit by an arc-landed projectile. Both are "deliver to colored target" but the delivery medium is different (block in a hook vs projectile in flight). Partially shared.
4. **What kills.** hk7v: step counter exhausted. nh4w: step counter exhausted. **Same.**
5. **The cast of supporting elements.** hk7v: walls, supply column with stacked blocks, colored floor markers. nh4w: walls of varied HEIGHT, ceilings of varied CLEARANCE, projectile-flight markers. Distinct supporting cast (wall-height-as-data + ceiling-as-mirrored-wall-from-top is unique to nh4w).
6. **Visible visual signature.** hk7v: a horizontal beam at the top of the frame with a hanging vertical rope; very distinctive overhead-crane silhouette. nh4w: ground-level launcher pawn with no overhead structure; airborne projectile rendered as small bright sprite at varying heights during animation. **Visually unrelated.**
7. **Pixel grain of primary sprites.** hk7v's primary sprites (trolley + hook + blocks) are roughly small rectangles with hook-claw detail. nh4w's launcher would be a multi-row pawn with a directional muzzle (visible nozzle pointing upward + sideways ridges); walls would have layered hatch fill that visibly stacks N rows for a height-N wall; ceiling stalactites would be jagged inverted shapes hanging from the top. **Differently-pitched pixel grain by design.**
8. **The core dynamic.** hk7v: micro-positioning a Cartesian gantry to choreograph a multi-step delivery. nh4w: aiming a parabolic arc whose physics depends on click distance, with a SINGLE shot per delivery. **Fundamentally different gameplay intent.** In hk7v the player is operating heavy machinery; in nh4w the player is judging a parabola.

Shared dimensions count: 3 partial (item 3 — "deliver to colored target", item 4 — step counter, item 5 — both have walls). Distinct on dimensions 1, 2, 6, 7, 8. The principle-3 axis (core dynamic) clearly diverges. **Verdict: passes negative-similarity.** Reaching for further divergence would mean swapping the entire deliver-to-target conceit, which is a very common NovaPlay win-form (15+ priors and most reference games use it) and is not itself a similarity flag — too many priors share it for it to count alone.

Walking the dimensions against other near-misses (vt6q grapple, kn58 anchor-pull, bp35 fall-nav, qn7w pulse-chain) — each shares at most 2 dimensions with nh4w (target-deliver win + step-budget kill); core dynamic differs strongly in all cases.

## Decision
NOVEL. Proceed to `write_spec` with mechanic family `arc-loft-shot` and ID `nh4w`.
