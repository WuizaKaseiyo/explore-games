# Implement summary — `nb6t`

- **Source**: `prior-games/nb6t/nb6t.py` (579 lines)
- **Metadata**: `prior-games/nb6t/metadata.json`

The game implements a chain of three rectangular rod-segments anchored at a fixed cell. Each segment has an independent absolute heading (E/N/W/S) and integer length (1..14); the player rotates the active segment, extends/retracts it, and (at L3) carries a moveable item on the chain's tip. The active hinge is highlighted by a yellow halo, and the chain's tip is a red dot. ACTION5 cycles the active hinge; ACTION3/4 rotate; ACTION1/2 extend/retract; ACTION6 clicks (sets active when on a hinge, drops carried item when on the tip). Step-counter HUD at row 63 fires lose when exhausted.
