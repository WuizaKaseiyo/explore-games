# Action enum

The novaengine exposes 8 action slots; an agent's gameplay vocabulary
draws from 7 of them (slot 0 = RESET is engine-managed and is NOT
listed in `available_actions=[...]`). Each game declares which subset
of slots 1..7 it uses.

## The slots

| Slot | Mnemonic | Conventional semantic | Action data |
|---|---|---|---|
| 0 | (engine) | `RESET` — start the env / restart the level. Fired automatically by the wrapper when the env is initialised or a level transitions; the agent does not choose RESET. | `SimpleAction` |
| 1 | ↑ | UP | `SimpleAction` |
| 2 | ↓ | DOWN | `SimpleAction` |
| 3 | ← | LEFT | `SimpleAction` |
| 4 | → | RIGHT | `SimpleAction` |
| 5 | space | **The freedom slot — game-defined modal verb.** | `SimpleAction` |
| 6 | mouse-click | CLICK at `(x, y)`. Agent supplies pixel coords; convert via `self.camera.display_to_grid(int(x), int(y))`. | `ComplexAction` (`x`, `y` ∈ [0, 63]) |
| 7 | ⌫ / Z | **STRICT: UNDO only.** All 6 of the 6 reference games that declare slot 7 use it for undo (ar25, bp35, lf52, sb26, sk48, su15) — no exception, no overload. | `SimpleAction` |

The mapping in the "Conventional semantic" column is a strong soft-norm
across the 25 reference games, not an engine contract. The engine just
provides numbered slots; the convention exists so a player using
arrow-keys + spacebar + mouse + Z always feels at home.

## Slot 7 is strict-undo

While slots 1-4 (cardinal motion), slot 5 (freedom verb), and slot 6
(click) admit some game-by-game variation, **slot 7 is a hard rule**.
Empirical check across the 25 reference games: every game that
declares ACTION7 uses it for undo of the most recent action — no
generated game may overload it for any other verb (cool, fire, swap,
toggle, etc.). The keyboard binding (`Z` / `⌫`) carries strong undo
expectations across game culture; reusing the slot for a non-undo
verb breaks player intuition catastrophically.

If a generated game does not need undo, **omit ACTION7 from
`available_actions`** rather than reusing the slot. The action subset
should simply not list 7. Use slot 5 for the game's distinctive verb,
slot 6 for click verbs, or extend an existing arrow-direction's
semantic if you need more verbs. Never put a non-undo verb on slot 7.

This is enforced by `design-constraints/checklist.md` item 23.

## ACTION5 is where novelty lives

Slots 1-4 are firmly cardinal motion. Slot 6 is firmly "click somewhere".
Slot 7 is firmly undo (when present). **ACTION5 is the only slot whose
verb is genuinely free**, and it's where each reference game stamps its
distinctive identity. Examples observed across the 25 games:

- **cn04**: ACTION5 = rotate the selected piece 90°.
- **sp80**: ACTION5 = pour water from every spout (the commit verb).
- **sb26**: ACTION5 = commit the current row as a guess.
- **cd82**: ACTION5 = fire the basket at the canvas.
- **m0r0**, **wa30**: ACTION5 = lock-or-unlock onto an adjacent piece.
- **re86**: ACTION5 = cycle which shape is the active frame.
- **g50t**: ACTION5 = a context-special ability defined per level.
- **tr87**: doesn't use ACTION5 — already encodes its distinctive verb
  (cycle a card through an alphabet) on slots 1/2.

When designing a new game, the question to answer first is: **what is
the distinctive verb of this game, and where does it live in the action
space?** Common answers:

- *Distinctive verb on ACTION5* — game uses arrows for navigation and
  spacebar for the special move. Subset like `[1, 2, 3, 4, 5]` or
  `[1, 2, 3, 4, 5, 6]`.
- *Distinctive verb on ACTION6* — pure-click game where the verb is
  encoded in *what* the click targets (lp85's row/column shift buttons,
  vc33's pull-tabs, ft09's stamp). Subset like `[6]` or `[6, 7]`.
- *Distinctive verb on ACTION1-4* — game where directional input is
  itself the unusual mechanic (m0r0's mirror-orbs, sp80's tilt rotation,
  tr87's cycle-direction). Subset like `[1, 2, 3, 4]` or `[1, 2, 3, 4, 6]`.

A game that lists ACTION5 but does nothing distinctive with it is
wasting the most expressive slot in the vocabulary.

## Implementation notes

- For ACTION1..5 and ACTION7: `self.action.id` is the only field used.
- For ACTION6: `self.action.data["x"]` and `self.action.data["y"]`
  contain pixel coordinates; convert with
  `self.camera.display_to_grid(int(x), int(y))` to grid coords.
- `step()` is called once per action and must end with
  `self.complete_action()`. Inside `step()` you can call:
  - `self.next_level()` — advance to the next level (success).
  - `self.lose()` — game-over.
  - `self.win()` — full game completion.
- RESET (slot 0) does not need an explicit `if self.action.id ==
  GameAction.RESET` branch; the engine's default `handle_reset()`
  handles it. Override only if the game needs custom reset behaviour.

## Subset patterns observed across the 25 reference games

| Subset | Style | Example games |
|---|---|---|
| `[1, 2, 3, 4]` | Pure cardinal motion | ls20, tu93 |
| `[6]` | Pure click | r11l, vc33, sc25, ft09, lp85 |
| `[6, 7]` | Click + undo | sb26 (sometimes), su15 |
| `[1, 2, 3, 4, 5]` | Cardinal motion + freedom slot | cn04, sp80 |
| `[1, 2, 3, 4, 6]` | Cardinal motion + click | ka59, dc22, m0r0, wa30 |
| `[1, 2, 3, 4, 5, 6]` | Full keyboard + click | cd82 |
| `[1, 2, 3, 4, 6, 7]` | Cardinal + click + undo | bp35, lf52 |
| `[1, 2, 3, 4, 5, 6, 7]` | All slots | rare; sk48 |
