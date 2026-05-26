# Mechanic Pick — `nb6t` (hinge-chain-reach)

## Game ID
`nb6t`

## Mechanic family
`hinge-chain-reach`

## One-paragraph description
An articulated chain of N rectangular rod-segments is anchored at a fixed base cell of the playfield. The segments are connected end-to-end by visible circular hinges; together they form a single kinematic chain whose orientation is fully described by a list of per-hinge angles in 90° increments. The player has a tiny tip-marker glued to the chain's free end (the *end-effector*); their job is to position this tip on a target cell.

Three actions drive the mechanic. **ACTION5** cycles which hinge in the chain is currently *active*; the active hinge is highlighted with a brighter halo so the player can see at a glance which joint will react. **ACTION3 / ACTION4** rotate the active hinge by 90° counter-clockwise / clockwise; rotating a hinge swings the **entire descendant sub-chain** (the active hinge's segment and all segments past it) around the hinge's pivot, while the parent sub-chain stays fixed. **ACTION6** is a click on the chain — clicking a hinge picks it as active (a faster path to a specific joint than cycling).

L1 establishes the system with a 2-segment chain on an empty playfield: the player learns *cycle-active-hinge* and *rotate-active-hinge* by feel and reaches a single target cell. L2 introduces **wall obstacles** — cells the chain cannot pass through; any rotation that would put a segment-cell on a wall is rejected. L3 introduces **carry-and-drop** — landing the tip on a moveable object snaps the object to the tip; ACTION6 on the tip releases the object onto the current tip-cell.

## Closest taxonomy entries (`mechanic-novelty/taxonomy-of-25-games.md`)
- **`s5i5` rod-stretch-retract** — superficially in the rod-shape family. Distinguishing rule: s5i5 has multiple **independent** rods, each anchored on its own axis, that **stretch axially** (no rotation around joints). The candidate has **one connected** chain whose segments **rotate** about hinges (no axial stretch). Cast count differs (multi-rod vs single chain) and the player's mental model differs ("which colour swatch to click to extend?" vs "which hinge to rotate?").
- **`cn04` nub-pair-glyph** — superficially in the rotation family. Distinguishing rule: cn04 rotates a **single selected piece** around its own centre as a rigid body, with a connector-snap win condition. The candidate rotates **one joint of a multi-joint chain** so the entire descendant sub-chain swings rigidly around that hinge. cn04 has multiple separate pieces; the candidate has one chain of fixed structure.

No other reference enters the mechanic family-level near-miss test.

## Closest prior-games entries (`prior-games/index.md`)
- **`qz73` radial-cycle-lock** — superficially in the rotation family. Distinguishing rule: qz73 is a **single rigid rotor** with multiple radial tips; rotating the rotor moves all tips together as a rigid body, and individual tips can be **locked** to freeze them while others continue to rotate. The candidate is a chain of **independent** hinges; rotating one hinge swings only the descendant sub-chain. There is no "lock"; every hinge stays controllable.
- **`gx7m` gear-mesh-cascade** — superficially in the rotation-propagation family. Distinguishing rule: gx7m gears propagate **rotation** to meshed neighbours with a sign-flip; the change is orientation-only. Candidate hinges propagate **translation** to descendant segments via the parent's rotation; there is no inter-segment "mesh" — the chain is a tree, not a graph. gx7m has clutches and ratchets; the candidate has neither.
- **`pj7k` rolling-cube-face-paint** — distinct (rolling translates the cube while permuting its faces; chain segments rotate around their parent's tip without translating their pivot).
- **`pz4t` anchor-pivot-place** — distinct (placement + rotate vs no-placement).

All other prior entries are distinct families.

## Negative-similarity check (`mechanic-novelty/negative-similarity-check.md`)

Walked the eight dimensions against the closest priors and references; full table is in `logs/02_pick_mechanic_io.md` § Negative-similarity-check. Summary:

| Comparison | Shared dimensions | Verdict |
|---|---|---|
| vs s5i5 (closest reference) | 3 (light: 3, 4, 7) | PASS — heavy axes 6 & 8 diverge |
| vs gx7m (closest prior, rotation cascade) | 2 (light: 2, 4) | PASS |
| vs qz73 (radial rotor) | 4 (light + 1 heavy partial: 1, 2, 4, 7) | PASS borderline — heavy axes 6 & 8 diverge cleanly |
| vs cn04 (single-piece rotation) | 3 (2, 4, 7) | PASS — heavy axes 6 & 8 diverge |
| vs pj7k (rolling cube) | 1 (4) | PASS |

The qz73 borderline is acceptable because the principal heavy axes (6 visual signature, 8 core dynamic) diverge — qz73's visual reads as a *radial star around a pivot* whereas the candidate reads as an *extended articulated rod-chain*; qz73's dynamic is rigid-body rotation whereas the candidate's is articulated-chain forward kinematics.

## Core-knowledge priors (`design-constraints/core-knowledge-priors.md`)
- **Objectness** — hinges, segments, the tip-marker, and L3 moveable objects are persistent entities.
- **Basic geometry** — 90° rotations around hinge pivots; chain pose is fully determined by per-hinge angles.
- **Basic physics (kinematic constraint)** — rotating one joint rigidly translates the descendant sub-chain.

No agentness; no autonomous NPCs; no language or symbol use.
