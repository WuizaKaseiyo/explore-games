# implement-summary.md

## Files

- `prior-games/tj4n/tj4n.py` — 599 lines.
- `prior-games/tj4n/metadata.json`.

## Implemented rule (plain English, no spec coordinates)

A single avatar walks a small arena and leaves a coloured trail behind on each step. When the avatar steps onto its own existing trail the loop closes — every "valuable" sprite whose centre lies inside the closed shape is captured (consumed), while any "danger" sprite caught inside costs a strike. Three strikes lose the level; capturing every valuable sprite without exceeding the step budget wins. Higher levels add a danger column that forces multiple smaller loops, then add a roaming threat the player must also enclose in a closure before it reaches the avatar — and after the higher levels' closures the loop's perimeter cells solidify into permanent walls that further constrain the route.

## Smoke test results (step 5 of implement.md)

```
$ python -c "
import sys
sys.path.insert(0, 'prior-games/tj4n')
from tj4n import Tj4n
g = Tj4n()
print('instantiated OK; level count:', len(g._levels))
print('available_actions:', g._available_actions)
print('avatar pos:', g._avatar_pos)
print('step budget:', g._step_budget)
"
instantiated OK; level count: 3
available_actions: [1, 2, 3, 4, 7]
avatar pos: (20, 32)
step budget: 50
```

`ast.parse(...)` returned no SyntaxError. `Tj4n()` instantiates without raising. The avatar's pixel position `(20, 32)` corresponds to logical cell `(5, 8)` — matches L1 layout in the spec. Step budget `50` matches L1 spec. Available actions `[1, 2, 3, 4, 7]` matches the spec's action mapping.

`__pycache__` cleanup completed.
