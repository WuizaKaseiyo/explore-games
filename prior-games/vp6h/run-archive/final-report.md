# Game generation final report

## Generated game
- **ID**: `vp6h`
- **Source**: `prior-games/vp6h/vp6h.py`
- **Metadata**: `prior-games/vp6h/metadata.json`
- **Lines of code**: 462

## Mechanic

The player walks a 16×16 grid from a small magenta-and-maroon avatar
sprite, hunting cyan-and-purple crystal sprites scattered across the
playfield. Yellow horizontal lantern bars are mounted on rails at the
top edge (and, at level 3, also the bottom edge); each lantern emits
parallel rays through its 5 columns, and grey vertical pillars cast
shadow strips behind themselves in any column the lantern covers. A
crystal can only be picked up while the avatar's reference cell is in
shadow with respect to *every* active lantern; walking onto a lit
crystal is a forgiving no-op (no pickup, no destruction). The player
slides each lantern by clicking any column on its rail (ACTION6).
Difficulty composes across levels: L1 introduces the shadow-pickup
rule with a fixed lantern; L2 adds the lantern-slide ability and
forces an *ordering* — collect a default-shaded crystal before
sliding the lantern leftward, since the slide makes that crystal lit;
L3 adds a second lantern at the bottom rail and the *intersection*
rule — only cells shaded by both lanterns are safe.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Avatar moves up one cell. |
| ACTION2 | Avatar moves down one cell. |
| ACTION3 | Avatar moves left one cell. |
| ACTION4 | Avatar moves right one cell. |
| ACTION6 | Click. If the click maps to row 0, slide the top-lantern so its 5-column extent is centred on the clicked column (clamped to fit the grid). If the click maps to row 15 and the level has a bot-lantern, slide the bot-lantern similarly. Other clicks are no-ops. |

ACTION5 and ACTION7 are unused (not in `available_actions`).

## Levels

- **L1** — Base dynamic system: M1 (shadow-pickup-rule). Single fixed lantern, single pillar, single crystal in the pillar's shadow; step budget 40; witness 6 actions.
- **L2** — +1 mechanic: M2 (lantern-slide). Three crystals across distinct columns; the lantern must be slid leftward to expose one of them, and a crystal in another column must be collected first because the leftward slide would otherwise light it. Step budget 70; witness 25 actions.
- **L3** — +1 mechanic: M3 (dual-shadow-overlap). A second lantern at the bottom rail makes safety the intersection of two shadow regions; the witness pre-positions both lanterns to a config that covers all three crystals' shadows simultaneously. Step budget 120; witness 25 actions.

## Novelty note

- **Closest taxonomy entry**: none with shared core dynamic. Surface
  echoes of "lantern" and "shadow" appear in lq5x (prior, not in the
  25 reference games) but the geometry is inverted there (carried
  cone of light = safe zone) vs. here (rail-mounted lantern; shadow
  *behind* obstacles = safe zone). Distinguishing rules are
  documented in `mechanic-spec.md` § 9.
- **Closest prior-game entry**: lq5x (`lantern-cone-illuminate`).
  Distinguishing rules: (a) geometry inversion — light-as-hostile vs
  light-as-safe; (b) lantern locus — stationary on a 1D rail vs
  carried by the avatar; (c) light field topology — parallel-ray field
  from a 5-cell bar vs 3-wide directional cone; (d) win condition —
  collect-all by occlusion vs match-by-tint; (e) L3 mechanic — dual
  rail-lanterns with shadow intersection vs single-cone modifications
  (wax / filter).

## Index update

One row appended to `prior-games/index.md`:

```
| vp6h | shadow-cast-collect | Shadow-Cast Crystal Collection — collect crystal sprites by walking onto them while standing in cells shaded by every active rail-mounted lantern. | 2026-05-06T15:27:17Z | (autonomous) |
```
