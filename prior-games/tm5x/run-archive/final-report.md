# Game generation final report

## Generated game

- **ID**: tm5x
- **Source**: `prior-games/tm5x/tm5x.py`
- **Metadata**: `prior-games/tm5x/metadata.json`
- **Lines of code**: 516

## Mechanic

The player controls a single pawn that walks a 16×16 thermal grid
with the four arrow keys, toggling its own polarity (hot ↔ cold)
with ACTION5. After every step, the pawn's current cell is imprinted
with the polarity-driven value (+2 hot, −2 cold) and the four
cardinal-neighbour cells take ±1; all other cells reset to 0. Goal
markers placed on the grid latch permanently the moment their
underlying cell shows the marker's required temperature value, and
the level wins when every marker is latched. Levels compose by
adding new mechanics on top: L1 establishes walk-and-imprint with a
single hot target; L2 adds polarity toggle for matched hot+cold
targets; L3 adds an insulator wall column whose gap forces a
specific routing decision before the player can reach the
opposite-side cold target.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move pawn one thermal cell up |
| ACTION2 | Move pawn one thermal cell down |
| ACTION3 | Move pawn one thermal cell left |
| ACTION4 | Move pawn one thermal cell right |
| ACTION5 | Toggle pawn polarity (hot ↔ cold), swapping the visible pawn variant |

## Levels

- **L1** (step budget 30): walk + aura-imprint. Single hot target, no walls. Witness 5 actions.
- **L2** (step budget 60): + polarity-toggle. Hot target left, cold target right. Witness 16 actions.
- **L3** (step budget 100): + insulator walls. 12-cell vertical wall splits the lower playfield with a top-row gap; hot target on one side, cold target on the other. Witness 43 actions.

## Novelty note

- **Closest taxonomy entry**: dc22 (`colour-cycle-walk`) — pawn
  walks an arena with cycle-triggers; ls20 (`cycler-attribute-
  match`) — pawn carries cycling attributes. Distinguishing rule:
  tm5x's field is a continuous-integer scalar (in {-2..+2})
  recomputed positionally each tick from pawn + polarity, not a
  fixed-cycle discrete state machine on per-cell wedge enumerations.
  No cycler tiles; no per-pawn attribute domain.
- **Closest prior-game entry**: pf3w (`wavefront-converge-timing`)
  shares "ACTION5 ticks the world" and "targets coincide on a
  single tick" surface; lq5x (`lantern-cone-illuminate`) shares
  "pawn-walks + ACTION5 modal verb + colour-targets" surface.
  Distinguishing rules:
  - vs pf3w: tm5x's field is a SIGNED INTEGER scalar (5 distinct
    values per cell), not a BOOLEAN BFS frontier; tm5x's verb is
    walk+ACTION5-polarity-flip, not click-to-arm; tm5x's win is
    cumulative latches, not single-tick coincidence.
  - vs lq5x: tm5x's aura is OMNIDIRECTIONAL 4-cardinal at fixed
    range, not a DIRECTIONAL 3-wide cone with extendable range;
    ACTION5 toggles polarity SIGN, not cone direction; tm5x's
    field carries SIGNED integer values, not boolean light-on.

## Index update

One row appended to
`prior-games/index.md`:

```
| tm5x | thermal-aura-imprint | Aura-Imprint Polarity Stamp — single pawn imprints temperature on its current cell + 4 neighbours; ACTION5 toggles polarity hot/cold; targets latch when their cell reads required value. | 2026-05-07T22:02:56Z | (autonomous) |
```

Also produced under `prior-games/tm5x/`:

- `tm5x.py` — the generated game source (516 lines).
- `metadata.json` — per-game metadata.
- `mechanism-detail.md` — the catalogue entry future runs'
  similarity checks will consult for any near-miss.

The full per-run workspace (state IO logs, mechanic-pick,
mechanic-spec, critique-revisions, critique-pass, implement-summary,
smoke-test custom checks, smoke frames, smoke-test-pass) lives at
`runs/2026-05-07T21-16-26/workspace/`
and is also archived in
`prior-games/tm5x/run-archive/`.
