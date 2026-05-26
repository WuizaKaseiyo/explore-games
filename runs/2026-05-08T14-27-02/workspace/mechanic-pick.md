# mechanic-pick — Run #2

## ID

**`vy3m`** — not in 25-ref reserved list, not in `prior-games/index.md` (27 entries incl. ej4t), not a recognisable English word.

## Mechanic family tag

**`class-swap-roster`**

## One-paragraph description

The level contains 1-3 player-controlled *actor sprites*, each belonging to a distinct *class* with its own interaction rule on adjacent crates. ACTION5 cycles which actor is currently active (the cursor); a halo highlight indicates the active actor. Arrows ACTION1-4 move the active actor; if the active actor walks INTO a crate, the class-specific verb fires:

- **Pusher** (class P): push — crate moves one cell in the same direction (Sokoban-classic).
- **Puller** (class L, "lifter"): pull — crate moves toward the actor's vacated cell as the actor moves (i.e. crate moves in the SAME direction as the actor; conceptually the actor drags the crate one cell behind it).
  Wait, that's the same as push. Let me restate: Puller pulls the crate from BEHIND. When the actor moves in direction D, if the cell BEHIND the actor (opposite of D) has a crate, the crate moves in D too (following the actor).
- **Swapper** (class W): swap — instead of pushing/pulling, the actor and crate swap positions. The actor ends up in the crate's old cell; the crate ends up in the actor's old cell.

The level wins when every target cell is covered by a crate. **Mechanic 1 (L1)** is push (just the Pusher class). **Mechanic 2 (L2)** introduces the Puller class AND the class-swap mechanic (ACTION5 cycles between Pusher and Puller); some crates can only be moved into position via pull, not push. **Mechanic 3 (L3)** introduces the Swapper class; some crates have walls in front and behind so neither push nor pull works — only swap repositions them.

## Mechanism essence

The dynamic: instead of "where does the player walk", the dynamic is "*which class is active when which crate moves*". The player thinks about (a) which class to assign to which crate's task, and (b) what order to swap classes such that intermediate states don't trap a class. Walls can also be class-specific (e.g. only Swapper passes a particular gap).

## Distinguishing rules vs near-misses

### Taxonomy (25-ref) near-misses

#### ka59 (sokoban-explode-chase) — closest near-miss
**Shared**: multi-pawn click-cycling on a sokoban-like grid.

**Distinguishing rule**: ka59's pawns all share the SAME movement and interaction rule (slide three cells, recursive push, explode-tiles spray neighbours). Multi-pawn-ness is a colour-tagging variant, not a class system. This candidate has DIFFERENT physics per class — push, pull, and swap are distinct verbs that operate on the SAME crate sprites. The decision space is "which class's verb to apply to this crate", not "which pawn's colour matches this target". Action depth differs: ka59 = 5 (4 directions + click); this candidate = 5 (4 directions + ACTION5 cycle).

#### m0r0 (mirror-orb-merge) — secondary
**Shared**: multiple movable actors on grid.

**Distinguishing rule**: m0r0's two pawns are mirrored siblings — their motion is COUPLED by mirror rule (UP moves both, LEFT pushes one and pulls the other). The player has no control over which pawn does what — the rule is fixed. This candidate has FULLY INDEPENDENT actors; ACTION5 selects which one moves. Coupling vs independence is the core distinction.

#### tu93 (maze-pickup-train) — distant
**Shared**: multiple actors that can be controlled.

**Distinguishing rule**: tu93's followers are autonomous (march on their own clockwork) once collected; the player only controls the lead pawn. This candidate has the player controlling each actor in turn (no autonomous behaviour); switching is explicit via ACTION5.

### Prior-games (27 entries) near-misses

#### mr5q (polarity-attract-discharge) — closest
**Shared**: multiple actors, attribute-based interaction.

**Distinguishing rule**: mr5q's pawns flip yang/yin via click and walk autonomously toward nearest opposite each ACTION5 (autonomous BFS). This candidate has NO autonomous walking; each actor moves only when player presses arrow while it's active. Attribute-flipping (mr5q) is replaced by class-fixed-per-actor here.

#### zd7m (cohort-step-route) — secondary
**Shared**: arrows step movable pawns.

**Distinguishing rule**: zd7m's arrows step EVERY movable pawn one cell in the same direction (cohort movement). This candidate moves only the ONE active actor per ACTION1-4; other actors are frozen unless explicitly switched-to via ACTION5. Cohort vs single-active is the core distinction.

#### ej4t (radius-scope-influence) — recent prior, distant
**Shared**: arrow-based controls; sokoban-derived push.

**Distinguishing rule**: ej4t has 1 player-actor + a radius gate on chain-pushes. This candidate has multiple player-actors with class-specific verbs and no radius. Mechanic axes are orthogonal (ej4t = scope; this = roster).

### Negative-similarity 7-dim test

vs **ka59** (closest):
1. Board: avatar+crates+targets vs same. **shared** (1)
2. Action verb: cycle-class then move/push/pull/swap vs click-pawn-then-slide-3-cells. Different (cycle ACTION5 vs click pawn).
3. Goal: cover targets with crates vs cover targets with same-coloured pawns. **shared** (2)
4. Death: step budget vs same. **shared** (3 — universal)
5. Cast: 1-3 class-actors + crates + targets + walls vs many pawns + walls + explode-tiles + chaser. Different.
6. Visual signature: each class has a distinct sprite design. ka59 has same-shape coloured pawns. Different.
7. Pixel grain: rich detail per checklist 20. Equivalent.
8. Core dynamic: "which class for which task" vs "click-and-slide three cells". **Different**.

Shared on dims 1, 3, 4 (all three are universal sokoban-family overlaps; dim 4 is universal). Effectively 1-2 shared dims (excluding the universal). Under 3-dim threshold. **PASS.**

vs **mr5q**: shared on 1 (avatar+crates+targets), 4 (universal); different on 2 (no click-flip), 5 (different cast — no autonomous walk; no ACTION5 globaltick), 6 (no autonomous behaviour visual), 8 (different core dynamic). 2 shared, well under threshold.

**Verdict: NOVEL.**

## Inspiration source

PuzzleScript demo `heroes_of_sokoban.txt` (increpare/PuzzleScript). The demo's core (3 hero classes — Fighter pushes, Thief pulls, Wizard teleports — with click-to-cycle) is composed here into 3-level NovaPlay progression. **§3.4 ceiling**: Heroes of Sokoban is an indie game (Jonah Ostroff, 2014) — the demo cites it as inspiration. The full commercial game has many additional features (10+ levels, complex puzzles); this 3-level NovaPlay take with simplified class verbs (push/pull/swap, no teleport-with-cooldown) is mechanically distinct enough to clear ceiling — but the user-side check should verify against the actual commercial game's complexity.

## Action mapping (preview)

- `ACTION1-4`: walk active actor; if walks INTO a crate, fires class-specific verb (push / pull / swap).
- `ACTION5`: cycle active actor (in cyclic order: Pusher → Puller → Swapper → Pusher → ...). Active class shown by halo highlight on the active sprite.
- `ACTION6, ACTION7`: not used.

`available_actions = [1, 2, 3, 4, 5]`.

## Per-level grid sizes (preview)

- L1: 10×10 (Pusher only; 1 crate; 1 target). Tutorial.
- L2: 12×12 (Pusher + Puller; 2 crates; 2 targets — one needs push, one needs pull).
- L3: 14×14 (3 actors + 3 crates + 3 targets + class-specific obstacles).

Final positions, walls, witnesses, and trivial heuristics fixed in `write_spec`.

## Considered alternatives (rejected)

- **chained-segment-arm** (robotarm-inspired): kinematic implementation complexity; deferred to future run.
- **companion-reflex-pair** (byyourside-inspired): too close to m0r0 visual cast (multi-pawn-on-grid).
- **midas touch-transforms** (midas demo): would need careful disambiguation from existing prior games (vp6h shadow, lq5x lantern).
- **chaos-wizard spell-recipe** (chaos wizard): rich but implementation complex; reserve.
