# Game generation final report

## Generated game

- **ID**: `gx7m`
- **Source**: `prior-games/gx7m/gx7m.py`
- **Metadata**: `prior-games/gx7m/metadata.json`
- **Lines of code**: 463

## Mechanic

The player faces a small cluster of toothed-disc gear sprites
arranged on a fixed grid. Each disc carries a coloured rim-mark at
its top tooth and is framed by a hollow collar with a single coloured
target indent at one of the four compass positions. Clicking any
disc's hub rotates it 90° clockwise; the rotation propagates
instantly through every cardinally-meshed neighbour with the sign
flipped, recursing through the connected mesh-graph until every
reachable disc has rotated. The puzzle is to drive every disc's mark
onto its same-coloured target indent. Level 2 introduces a ratchet
disc whose external direction-tang gates the cascade — clicks on the
tang cycle the ratchet through `BLOCKED → CW → CCW`, allowing the
player to permit one-way passage through specific edges. Level 3
adds a clutch disc whose lever-tang toggles its engagement with the
mesh: a disengaged clutch removes its incident edges, partitioning
the mesh-graph into independent components.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | Click. Dispatches by sprite-tag at the click cell: `disc` → rotate that disc 90° CW and trigger the cascade; `tang_dir` → cycle the owning ratchet's direction state; `tang_lever` → toggle the owning clutch's engagement. |

## Levels

- **Level 1** — base dynamic system: 3 plain discs in a row; cascade
  rule alone. Witness 2 actions.
- **Level 2** — adds the ratchet (1 new mechanic). Pink + ratchet-
  magenta + lblue in a row; ratchet starts BLOCKED so the magenta
  disc cannot rotate without first cycling its direction-tang.
  Witness 5 actions.
- **Level 3** — adds the clutch (1 new mechanic). 5 discs in a row,
  including ratchet and clutch; the witness REQUIRES disengaging the
  clutch to break the parity coupling between lblue and orange.
  Witness 11 actions.

## Novelty note

- **Closest taxonomy entry**: `lp85` (row-col-shift-grid) is also
  pure-click. *Distinguishing rule*: lp85 invokes pre-computed
  positional permutations of cells; gx7m rotates discs in place
  AND cascades sign-flipped rotations through mesh-edges. lp85 has
  no rotational-cascade analogue.
- **Closest prior-game entry**: `qz73` (radial-cycle-lock) — both
  ask for rotated-mark-to-coloured-target alignment.
  *Distinguishing rule*: qz73 has ONE central rotor with embedded
  tips that all rotate together as a rigid body; gx7m has MANY
  independent discs with sign-flipping propagation across mesh-
  edges and a clutch that *partitions* the mesh-graph. The full
  per-prior write-up lives in `workspace/mechanic-pick.md`.

## Index update

Appended one row to `prior-games/index.md`:

```
| gx7m | gear-mesh-cascade | Gear-Mesh Cascade — discs whose rotations propagate with sign flip across cardinal mesh; ratchet gates direction; clutch partitions mesh. | 2026-05-06T14:55:16Z | (autonomous) |
```
