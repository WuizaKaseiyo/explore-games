# Game generation final report

## Generated game
- **ID**: `qn7w`
- **Source**: `prior-games/qn7w/qn7w.py`
- **Metadata**: `prior-games/qn7w/metadata.json`
- **Lines of code**: 648

## Mechanic

`qn7w` is a click-only puzzle in which the player triggers single momentum pulses along stationary chains of touching coloured balls. Clicking a pusher knob at one end of a chain fires a pulse that propagates invisibly through the chain — the **intermediate balls do not move**; only the ball at the chain's far end ejects, travelling exactly one ball-width along the chain's terminal axis. The ejected ball lands on the immediately adjacent cell, where it may fill a colour-matched target socket, deposit on a merge pad, or be consumed by a wall. The level ends when every socket is filled (and every merge pad has received its required two deposits). Energy concentrates at the terminal — the inverse of every cascade-style prior. Across three levels the base pulse-eject mechanic is enriched by a T-shaped junction node that gates which branch ejects (cycled by a click), and finally by a two-deposit merge pad that requires balls from two distinct chains to converge.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | Click. If the click lands on a `pusher_knob`, fire a pulse along its chain — eject the terminal ball one ball-width. If the click lands on a `junction_node`, cycle that junction's active branch. Click anywhere else: no-op. |

`available_actions = [6]` — pure click.

## Levels

- **Level 1 (tutorial)** — base dynamic system: `pulse-eject`. Single horizontal chain of 4 balls, one pusher knob, one target socket. Witness: 1 click.
- **Level 2** — adds `junction-routing` (+1 mechanic, total 2). Stem chain branches at a T-junction; the up-branch terminal feeds the only target socket; the down-branch (default-active) ends at a black wall (`dead_end_wall`) that consumes ejects. Witness: flip junction, then push (2 clicks).
- **Level 3** — adds `merge-on-coincidence` (+1 mechanic, total 3). Two chains converge orthogonally on a single merge pad that lights up only after receiving two deposits. Both junctions default to wall-bounded dead-ends; both must be flipped before firing. Witness: flip A, push A, flip B, push B (4 clicks).

## Novelty note

- **Closest taxonomy entry** — `ka59` (sokoban-explode-chase) shares the "click sets in motion a coloured-block dynamic" surface description. **Distinguishing rule**: ka59's player drives an active *moving block* via arrow keys, and explosions DISPLACE every neighbouring block (4-direction propagation). qn7w has no avatar and no arrow input; the chain's intermediates are explicitly stationary; only the chain terminus moves, by exactly one cell. ka59 spreads displacement; qn7w concentrates it.

- **Closest prior-game entry** — `vn8d` (domino-cascade-topple). Both are click-triggered cascades. **Distinguishing rule (binary)**: vn8d's cascade is *distributional* — every pillar in the chain visibly falls (state change for every cell in the path); burst-pads splay outward in 4 directions. qn7w's pulse is *concentrational* — every intermediate ball stays in its position with no state change; only the terminal ball ejects. The visual signatures match the rules: vn8d shows pillars toppling in sequence; qn7w shows a chain that shortens by one at the terminus while the body remains identical. Negative-similarity-check pass: shared dimensions are 2 (single click) and 4 (universal step budget); diverges on the heavy axes 6 (visual signature), 7 (pixel grain), 8 (core dynamic).

(All other prior entries: family-level non-overlap. None share a "chain", "pulse", "Newton's cradle", "momentum-eject", or "terminal-only-moves" descriptor.)

## Index update

One row appended to `prior-games/index.md`:

```
| qn7w | pulse-chain-eject | Pulse-Chain Eject — click pushers to fire momentum pulses through stationary ball-chains; only the terminal ball ejects per pulse. | 2026-05-08T00:11:56Z | (autonomous) |
```
