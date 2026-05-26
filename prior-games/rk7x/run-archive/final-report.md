# Game generation final report

## Generated game
- **ID**: rk7x
- **Source**: `prior-games/rk7x/rk7x.py`
- **Metadata**: `prior-games/rk7x/metadata.json`
- **Lines of code**: 834

## Mechanic
A small coloured courier walks the corridor network autonomously,
exactly one cell per player action, with no input that steers it
directly. Every junction in the network has a clickable "blade" that
selects which of two outgoing corridors the courier will take when it
arrives. The player's only verb is to click anywhere in the frame:
clicks on a junction sprite toggle that junction's blade between two
states; clicks on an empty cell are a "wait" verb that just ticks the
courier one cell. Each level requires the courier to reach a coloured
terminal; from level 2 onward, the level also requires the courier to
pass over every coloured stop on the way. Level 3 introduces a second
courier of a different colour that walks its own disjoint corridor in
lockstep — every player click ticks both couriers simultaneously, and
both must reach their matching terminals while collecting their
matching stops. Difficulty rises through composition: more junctions
to track, longer routes, and parallel-courier coordination at L3.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | Click at (x, y). If the click lands on a junction sprite, swap that junction's blade between H and V. After the (possibly no-op) toggle, advance every courier one cell in its current direction. Couriers that arrive at a junction read the junction's blade and update their direction; couriers that arrive at a coloured stop matching their colour mark the stop as visited; couriers that step into a wall lose the level. |

## Levels

- **L1** — Tutorial. One courier, one junction, one terminal. The
  player learns that the junction's default state routes the courier
  into a wall stub and that one click on the junction redirects the
  courier to the terminal.
- **L2** — Adds coloured stops gating the win. Two side-loop detours,
  each containing a stop, must both be traversed. Four junction
  toggles needed to enter and exit each detour. The win is gated by
  the stops' "visited" state in addition to terminal arrival.
- **L3** — Adds a second courier (different colour) walking its own
  disjoint corridor in lockstep. Both couriers must reach their
  matching terminals after collecting their matching stops. Four
  junction toggles required (two per courier). The conflict-cell rule
  (two couriers may not co-occupy a cell) is structurally present but
  dormant on the witness path because the corridors are disjoint.

## Novelty note

- **Closest taxonomy entry: tn36 (program-pawn-trace).** tn36 has the
  player COMPOSE a tape of move/rotate/resize ops via clicks and then
  RUN the tape. rk7x is edit-during-execution: there is no tape
  sprite, no commit verb, no run-button — every player click is
  simultaneously a tape-edit (switch toggle) AND a tape-execute
  (courier tick). This collapses tn36's two-phase loop into a single
  phase, producing a fundamentally different planning demand.
- **Closest prior-game entries:** vn8d (domino-cascade-topple — single
  click triggers passive chain reaction; rk7x intervenes every tick),
  bx84 (beam-mirror-reflect — beam fired from emitter; rk7x has a
  persistent moving agent), kn58 (anchor-pull-magnet — single
  Manhattan-axis pull; rk7x has many fixed switches that change
  routing rather than direct movement), pj7k (rolling-cube-face-paint
  — cube rolls only on player arrow press; rk7x's courier walks every
  click unconditionally), wt39 (glide-deflect-thaw — multi-cell glide
  per action; rk7x is exactly one cell per action and ignores
  directional input). Each near-miss differs on at least one of:
  player verb cardinality, courier autonomy, switch-as-edit-verb, or
  per-tick movement granularity.

## Index update

One row appended to `prior-games/index.md`:

```
| rk7x | live-switch-routing | Live-Switch Routing — autonomous coloured courier walks one cell per click; player toggles junction blades to route it through coloured stops to terminal. | 2026-05-06T00:25:48Z | (autonomous) |
```
