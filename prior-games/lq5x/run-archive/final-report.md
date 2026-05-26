# Game generation final report

## Generated game

- **ID**: `lq5x`
- **Source**: `prior-games/lq5x/lq5x.py`
- **Metadata**: `prior-games/lq5x/metadata.json`
- **Lines of code**: 440

## Mechanic

A small lantern pawn projects a 3-cell-wide directional cone of
"lit" cells into a darkened 12×12 (L1) or 14×14 (L2/L3) arena. The
player walks the lantern with arrow keys (ACTION1-4) and rotates
the cone facing 90° clockwise with ACTION5. A target ring is "lit"
when, at any post-action tick, its centre cell sits inside the cone
AND the cone's current colour matches the target's colour; once
lit, it stays lit. Level 1 introduces walk + rotate as the base
dynamic system. Level 2 adds wax pickups that extend the cone's
range R by +2 each on contact (the cone too short to reach distant
targets without collecting wax, and tight step budget rules out
walking around them). Level 3 adds a red filter cell — when the
cone covers the filter, `cone_color` permanently updates to red
(no yellow filter exists in L3 to revert), so yellow targets must
be lit first while the cone is still yellow before the player walks
toward the filter. Loss is exhausting the per-level step counter.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | walk lantern UP one cell (silent no-op if blocked by grid edge; step still consumed) |
| ACTION2 | walk DOWN |
| ACTION3 | walk LEFT |
| ACTION4 | walk RIGHT |
| ACTION5 | rotate cone facing 90° clockwise (N→E→S→W→N) |

## Levels

- **L1** (12×12, R=4, budget 10): base walk + cone-rotate. Two yellow targets in opposite quadrants; lantern starts facing N. Witness `[5, 4, 2, 2, 5]` → 5 actions.
- **L2** (14×14, R=2 → 4, budget 12): adds **wax pickup** (+2 to R on step-on). Two yellow targets at far N and far S; lantern starts facing N at the centre. Witness `[1, 1, 2, 2, 2, 2, 5, 5]` → 8 actions. Wax strictly required (no-wax path = 17 actions, exceeds budget).
- **L3** (14×14, R=2 → 4, budget 13): adds **filter cell re-tints cone**. One yellow target + one red target; one wax pickup; one red filter. Lantern starts facing E. Witness `[4, 4, 3, 3, 5, 2, 2, 2, 2, 2]` → 10 actions. Adjacent commute (steps 2 and 3) breaks solvability — yellow target must be lit before cone touches the red filter.

## Novelty note

- **Closest taxonomy entry**: `ls20` (cycler-attribute-match). lq5x's puzzle is a *line-of-sight cone-aiming* puzzle whose colour state lives on the projected cone, not on the avatar; verb cardinality differs (`[1,2,3,4,5]` vs ls20's `[1,2,3,4]`); the win predicate is a per-target conjunction over the run history, not a single goal-cell test on the avatar's body state.
- **Closest prior-game entry**: `qz73` (radial-cycle-lock) — both use ACTION5 as a rotation verb. qz73 rotates an 8-slot ring of physical *tip-pieces* and uses ACTION6-click to lock individual tips; lq5x rotates the *facing of a non-physical projected cone* and has no click and no lock verb. The board (radial ring vs walled arena), the cast (tips + sockets vs lantern + cone + targets + pickups + filters), and the core dynamic ("which tips to lock so rotation aligns?" vs "where do I aim the cone, and in what colour state?") all diverge.

## Index update

One row appended to `prior-games/index.md`:

```
| lq5x | lantern-cone-illuminate | Lantern Cone Illuminate — single lantern projects a 3-wide directional cone; arrows walk, ACTION5 rotates; wax pickups extend cone range, filters re-tint cone colour to match coloured target rings. | 2026-04-29T09:53:05Z | (autonomous) |
```
