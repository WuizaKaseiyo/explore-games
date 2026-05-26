# implement-summary — kg7p

- **Source file:** `prior-games/kg7p/kg7p.py` (509 lines).
- **Metadata file:** `prior-games/kg7p/metadata.json`.

## Rule summary (no cell-level coords)

A single avatar walks a 64×64 arena. The avatar faces its last walked direction and projects a one-cell tether beam. While the beam is on, the cell directly in front of the avatar may *couple* a haulable block; once coupled, the block walks in lockstep with the avatar across every subsequent walk. ACTION5 toggles the beam — turning it on attempts an immediate couple at the cell in front; turning it off releases any coupled block in place. Direction-locked blocks carry a magenta edge-stripe along one cardinal edge: those blocks can only be coupled and hauled in the direction the stripe marks. Each block must end on the target whose colour accent matches it; running out of step budget loses.

## Validation

- `ast.parse` on the .py file: PASS.
- Runtime instantiation: `Kg7p()` constructed; 3 levels loaded; `available_actions = [1, 2, 3, 4, 5]`; level 1 `grid_size = (64, 64)`.
