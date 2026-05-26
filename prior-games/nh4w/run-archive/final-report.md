# Game generation final report

## Generated game
- **ID**: nh4w
- **Source**: `prior-games/nh4w/nh4w.py`
- **Metadata**: `prior-games/nh4w/metadata.json`
- **Lines of code**: 449 (after smoke-test fixes)

## Mechanic
The player walks a small launcher pawn left and right along the floor of a 64×64 playfield. Clicking anywhere fires a yellow projectile that travels in a discrete parabolic arc from the launcher's muzzle to the clicked cell — the arc's peak height grows with horizontal click distance, so short shots fly low and long shots fly high. Brick walls standing on the floor block any arc whose peak is too low to clear them, and hanging grey stalactites (with maroon dripping tips) block any arc whose peak is too high to fit beneath them. Each level wins when the projectile has landed on every coloured target square on the floor. Level 1 introduces walking + arc-firing; Level 2 adds wall-clearance, requiring the player to find a launcher position from which the arc rises above the wall; Level 3 adds ceiling-block plus a second target, forcing two distinct launcher positions because no single x both clears the wall AND fits under both stalactites for both target distances.

## Action mapping

| Action | Effect |
|---|---|
| ACTION3 | Walk launcher 4 px LEFT (blocked by walls and playfield bounds). |
| ACTION4 | Walk launcher 4 px RIGHT (blocked by walls and playfield bounds). |
| ACTION6 | Click cell `(cx, cy)` → fire parabolic-arc projectile from the launcher's muzzle to the clicked cell (clipped to a 48-px range). The arc animates frame-by-frame; if it collides with any wall or ceiling pixel it fizzles, otherwise it lands on the click cell and consumes any target it overlaps. |

## Levels

- **L1.** Empty playfield with one yellow target out of arc range from the start. Player walks one step right to bring the target into range, then clicks it. Witness `[ACTION4, ACTION6@(56, 51)]` (2 actions). Step budget 15.
- **L2.** Adds an 8-px-tall brick wall between the launcher's reachable positions and the target. The player must walk to the unique launcher x where the arc's peak both has enough horizontal distance (so the click lands at the target) AND clears the wall (the arc's altitude at the wall's mid-band exceeds the wall height). Witness `[ACTION4, ACTION4, ACTION6@(62, 51)]` (3 actions). Step budget 25.
- **L3.** Adds two stalactites (one over the launcher's start area at clearance 6 px, one over the wall's right side at clearance 13 px) and a second (blue) target further right. The two targets cannot be hit from a single launcher position: yellow is reachable only from x=8 (where the arc just barely clears the wall but stays under ceiling1) and blue is reachable only from x=12 (where the longer-distance arc is high enough to clear the wall but tucks under ceiling2). The witness fires yellow first, walks one more step right, then fires blue. Witness `[ACTION4, ACTION6@(40, 51), ACTION4, ACTION6@(52, 51)]` (4 actions). Step budget 35.

## Novelty note

- **Closest taxonomy entry:** **bp35 — gravity-fall-navigation** (auto-falling pawn with side-step). Distinguishing rule: bp35's gravity acts continuously on the avatar as the primary dynamic; in nh4w gravity acts only on a SEPARATE projectile sprite during a fired shot, while the launcher walks deterministically with full cardinal control.
- **Closest prior-game entry:** **hk7v — overhead-trolley-hook** ("rope clears walls" via a Cartesian gantry that raises/lowers/slides a hook). Distinguishing rule: hk7v's wall-clearance is a sequential micro-positioning routine (~80 sequential moves per delivery — raise hook +1, traverse +1, lower -1); nh4w's wall-clearance is a SINGLE click-fire whose discrete parabolic arc clears all walls in one shot whose height-at-x is below the arc altitude at that column. The player learns a continuous physics relationship (longer shots fly higher), not a sequential lift-traverse-lower operation. Visual signatures differ (floor-walking pawn with airborne arc vs overhead beam with hanging hook); input patterns differ (walk + click-target vs raise/lower/slide/grab).

## Index update

One row appended to `prior-games/index.md`:

```
| nh4w | arc-loft-shot | Arc-Loft Lobber — pawn launcher walks the floor; click any cell to fire a parabolic-arc projectile that clears low walls and fits under hanging stalactites. | 2026-05-10T14:02:14Z | (autonomous) |
```
