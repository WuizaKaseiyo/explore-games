# Mechanic spec — qz73

## 1. Title
"Radial Tip-Lock Alignment" (working title; never visible in-game).

## 2. Mechanic family
A central hub holds a discrete ring of N=8 angular slots. Some slots
hold *tip-pieces* (3×3 coloured square sprites) and some hold static
*socket-rings* (5×5 hollow ring sprites of a target colour). The
distinctive verb (ACTION5) advances every UNLOCKED tip-piece by one
slot clockwise, with locked tip-pieces holding their slot in place.
The second verb (ACTION6 click) toggles the lock-flag on whichever
tip-piece is clicked. The level is solved when every socket whose
slot currently contains a tip has its colour match that tip's
colour, and the win is automatic on the action that first satisfies
the predicate.

Prior categories used (per `core-knowledge-priors.md`):
- **Objectness**: tips and sockets are persistent coloured sprites
  whose positions are tracked.
- **Basic geometry & topology**: the 8-slot cyclic ring and the
  cyclic-permutation operation Z/8 acting on the unlocked subset of
  tips. The lock mechanic partitions the 8-slot cycle into a
  permutation of fixed-points (locked) and a smaller cycle (the
  rotation orbit of the unlocked subset).

## 3. Sprite roster

(All names are 10-character opaque tokens chosen at random per the
universal-scaffold style note; they do not encode meaning. `-1` =
transparent.)

- **`xkqljmrnbe`** — 5×5 hub block.
  - dimensions: 5×5
  - palette: `[3]` (grey) on every cell
  - tags: `["hub"]`
  - role: static centre piece; visual anchor that establishes the
    rotation centre and is not interactable.

- **`fpzqcvuwts`** — 3×3 tip-piece (one definition; per-tip colour
  applied at level-setup via `color_remap(None, <palette>)`).
  - dimensions: 3×3
  - palette base: `[8]` (red) — overridden at runtime to whichever
    palette value is assigned to this tip (drawn from `{6, 11, 12,
    14, 15}` = magenta / yellow / orange / green / purple).
  - tags: `["tip", "sys_click"]`
  - role: a movable that the rotor's ACTION5 may shift around the
    ring; clickable to toggle lock state.

- **`zjmwofhcyl`** — 5×5 socket ring (one definition; per-socket
  colour applied at level-setup via `color_remap`).
  - dimensions: 5×5
  - palette base: `[[X, X, X, X, X], [X, -1, -1, -1, X], [X, -1, -1,
    -1, X], [X, -1, -1, -1, X], [X, X, X, X, X]]` where `X = 14`
    (green) overridden at runtime.
  - tags: `["socket"]`, `collidable=False`
  - role: target marker. The ring's hollow centre lets a 3×3 tip
    visually nestle inside, so the player can SEE that a tip is
    "in" a socket. Colour-match is detectable visually.

- **`hgvqyzbswn`** — 3×3 lock-mark overlay.
  - dimensions: 3×3
  - palette base: `[[5, -1, 5], [-1, -1, -1], [5, -1, 5]]` (four
    black corner pixels, transparent centre).
  - tags: `["lock_mark"]`, `collidable=False`,
    `interaction=InteractionMode.REMOVED` at startup
  - role: drawn over a tip when it is locked; toggled
    `REMOVED` ↔ `INTANGIBLE` on each ACTION6 lock-toggle. Black
    corners on a coloured tip are the visual signature of "this one
    is held".

## 4. Level progression sketch (EXACTLY 3 levels)

The 8 angular slot-positions are fixed across all levels — they are
the ring sites at radius ~20 from the hub centre (32, 32):

```
slot 0  = ( 32,  10)   (top)
slot 1  = ( 46,  17)   (top-right)
slot 2  = ( 53,  32)   (right)
slot 3  = ( 46,  46)   (bottom-right)
slot 4  = ( 32,  53)   (bottom)
slot 5  = ( 17,  46)   (bottom-left)
slot 6  = ( 10,  32)   (left)
slot 7  = ( 17,  17)   (top-left)
```

Tips are placed with `set_position(slot.x - 1, slot.y - 1)` (their
3×3 box centred on the slot). Sockets with `set_position(slot.x - 2,
slot.y - 2)` (5×5 ring centred on the slot).

### Level 1 — tutorial (rotation only, no locks needed)

Three tip-pieces at slots `{0, 2, 4}` with colours `[12, 14, 15]`
(orange, green, purple). Three socket-rings at slots `{2, 4, 6}`
with colours `[12, 14, 15]` (matching). The rotation rule moves
slot-i to slot-(i+1) mod 8, so after exactly 2 ACTION5 presses the
tips reach `{2, 4, 6}` with the same colour-list — every socket is
satisfied and the level wins. The player CAN click tips and toggle
locks but never NEEDS to. Step budget: 16 (set via
`level.get_data("StepCounter")`).

This satisfies §3.4's "tutorial level": single primary mechanic
active (rotation), reduced state space (only 3 tips on the ring),
no lose-by-hazard. A random agent spamming ACTION5 will solve it on
turn 2. Random agents toggling locks may waste steps but the
generous budget tolerates several misclicks.

### Level 2 — second mechanic introduced (the lock)

Three tip-pieces at slots `{0, 3, 6}` with colours `[12, 14, 15]`.
Three socket-rings at slots `{1, 4, 6}` with colours `[12, 14, 15]`.

Resolution: the green tip is already at slot 6 with the green
socket — a "free win" if its lock state is preserved. But because
ALL unlocked tips advance together, pressing ACTION5 once would
move it AWAY from slot 6 even though slots {0→1, 3→4} are exactly
the moves we want for orange and purple. The intended solution is:
1. ACTION6 click the green tip (at slot 6) to lock it.
2. ACTION5 once. Unlocked tips move: orange 0→1 (matches),
   purple 3→4 (matches). Green stays at slot 6. All sockets
   satisfied. Win.

Total: 2 actions. Step budget: 18.

This forces the agent to LEARN that lock = "exempt from rotation".
A pure-ACTION5 agent oscillates and never aligns; a pure-ACTION6
agent accomplishes nothing. The lock + rotate combination is the
new mechanic.

### Level 3 — composition (lock and rotate must interleave)

Five tip-pieces at slots `{0, 1, 2, 5, 7}` with colours `[12, 14,
15, 6, 11]` (orange, green, purple, magenta, yellow). Five socket-
rings at slots `{2, 4, 5, 6, 7}` with colours `[14, 12, 11, 15, 6]`
(green, orange, yellow, purple, magenta). Step budget: 32.

Resolution sketch: no single ACTION5 chord aligns more than one
socket. The agent must:
1. Observe that the magenta tip at slot 5 doesn't match the yellow
   socket also at slot 5; it does match the purple socket at slot 6
   if rotated by 1. But the purple tip at slot 2 also wants to
   reach the green socket at slot 2 (it doesn't match green).
2. The intended solution is a 7-action interleave that uses two
   lock toggles. One canonical witness sequence:
   - ACTION5 → tips at `{1, 2, 3, 6, 0}` with colours
     `[12, 14, 15, 6, 11]`. Magenta tip now at slot 6 — does NOT
     match purple socket. But yellow tip at slot 0 — no socket
     there.
   - ACTION6 click magenta tip at slot 6. Magenta locks at slot 6.
   - ACTION5 → unlocked tips move 1, 2, 3, _, 0 → 2, 3, 4, _, 1.
     Tips: `{2, 3, 4, 6 (locked, magenta), 1}` with colours
     `[12, 14, 15, 6, 11]`.
     Now: orange tip at slot 2, but slot 2's socket wants GREEN —
     mismatch. Reset thinking.
   - The exact witness sequence depends on the chosen colour
     assignment; the SPEC requirement is that the assignment
     guarantees a 5-7-action solution exists with a 32-step budget,
     while no shorter all-rotate-no-lock or all-lock-no-rotate
     sequence works. The level designer (during `implement`) must
     pick assignments that satisfy this — see Win-condition test
     in §7.

This satisfies §3.4's "L3 composition" rule: solving requires BOTH
mechanics (rotate + lock) interleaving, not just "more of L2".

## 5. Action mapping

`available_actions = [5, 6]`. No movement keys, no undo.

| Slot | ID | Semantic | Effect |
|---|---|---|---|
| 5 | ACTION5 | "advance dial" | every TIP whose `locked` flag is `False` has its slot incremented by 1 mod 8; sprite re-positioned to the new slot's pixel coords. Locked tips do not move. After the move, the win-predicate is re-evaluated; if satisfied, `next_level()`. |
| 6 | ACTION6 | "toggle lock at click" | `camera.display_to_grid(int(x), int(y))` → `(gx, gy)`; `current_level.get_sprite_at(gx, gy)` looks up the clicked sprite; if it is tagged `tip`, flip its `locked` flag and toggle its lock-mark overlay between `REMOVED` and `INTANGIBLE`. Clicks on hub / socket / empty cells do nothing (no step is consumed; see §6). |
| 1..4, 7 | n/a | not in `available_actions` | engine never offers them. |

Gating note: ACTION5 is always valid. ACTION6 is always
*offered* (the engine doesn't know which clicks land on a tip), but
`_get_valid_actions` should pre-enumerate ACTION6 for the centre of
each currently-existing tip — i.e. one ACTION6 candidate per tip,
with `(x, y)` set to the tip's display centre. This mirrors r11l's
"pre-enumerated 256-entry valid-action grid" pattern but at smaller
scale (3-5 candidates).

A click on empty space or on a non-tip sprite IS invalid in the
sense that `_get_valid_actions` does not list it; but if the engine
allows the agent to submit an arbitrary ACTION6 anyway, the `step`
handler treats it as a no-op (does not consume a step). This is
modelled on cn04's `if quyphwtvrr: ...` branch which silently
ignores misclicks.

Step counter consumption:
- ACTION5: always consumes 1 step.
- ACTION6 hitting a tip (toggle): consumes 1 step.
- ACTION6 missing (hits empty / hub / socket / lock-mark): consumes
  0 steps (no-op). This avoids burning the budget on pointer-noise.

## 6. HUD and per-game state

### HUD widget — `StepBarHud(RenderableUserDisplay)`

A single-row depleting bar at row 63 of the 64×64 frame. The bar
spans columns 8..55 (48 pixels wide, leaving a 1-pixel inset
either side of a possible letter-box). Background of the bar is
palette 3 (grey); fill is palette 12 (orange). The number of
filled cells equals
`round(48 * current_steps / max_steps)`. When `current_steps == 0`
the bar is fully empty (all 48 cells palette-3).

(Bottom-row depleting bar is the most common HUD pattern in the 25
reference games — 13/25 — and matches the universal-scaffold's
"Step counter HUD" suggestion.)

### Internal state on the game class

- `self.SLOT_POSITIONS: list[tuple[int, int]]` — 8 fixed
  `(x, y)` pixel slot-centre positions, declared once on the class.
- `self.tips: list[Sprite]` — the placed tip sprites for the current
  level, sorted by initial slot index ascending.
- `self.tip_slot: dict[Sprite, int]` — current slot index per tip.
- `self.tip_locked: dict[Sprite, bool]` — per-tip lock flag.
- `self.lock_marks: dict[Sprite, Sprite]` — per-tip overlay sprite,
  added to the level at level-start, initially `REMOVED`.
- `self.sockets: list[Sprite]` — the placed socket sprites.
- `self.socket_slot: dict[Sprite, int]` — current slot index per
  socket (static across the level — sockets do not move).
- `self.socket_color: dict[Sprite, int]` — palette value per socket
  (derived once from `socket.pixels[0, 0]`).
- `self.step_bar: StepBarHud` — registered with the camera.
- `self.max_steps: int` — read from `level.get_data("StepCounter")`
  in `on_set_level`.

`on_set_level(level)`:
1. Re-size camera viewport to `level.grid_size or (64, 64)` (skip
   if exactly 64×64; per universal-scaffold's camera-viewport rule).
2. Read `max_steps = level.get_data("StepCounter")` (with fallback
   to a default like 16 if missing).
3. `step_bar.reset(max_steps)`.
4. Populate `tips`, `sockets`, `tip_slot`, `socket_slot`, etc. by
   walking `level.get_sprites_by_tag("tip")` and
   `level.get_sprites_by_tag("socket")` and using each sprite's
   `(x, y)` to back-derive which slot it occupies (via lookup in
   SLOT_POSITIONS — sprite top-left = slot.x - 1, slot.y - 1 for
   tips; slot.x - 2, slot.y - 2 for sockets).
5. For each tip, instantiate one `lock_mark` overlay sprite at the
   same slot position with `interaction=InteractionMode.REMOVED`,
   add to `level`, register in `self.lock_marks`.
6. Initialise `self.tip_locked[tip] = False` for every tip.

`step()`:
1. Update `step_bar` with `(max_steps - self._action_count)`.
2. If `current_steps == 0`, call `self.lose()`; return.
3. If `self.action.id == GameAction.ACTION5`: advance each unlocked
   tip's slot by `+1 mod 8`; re-position sprite to new slot pixel
   coordinates. Re-evaluate win predicate (see §7). If True,
   `self.next_level()`.
4. Elif `self.action.id == GameAction.ACTION6`: convert click to
   grid coords; look up sprite-at; if it is a tip, flip its
   `tip_locked` flag, toggle its lock-mark overlay between
   `REMOVED` and `INTANGIBLE`. Re-evaluate win predicate (locking
   may newly satisfy a constraint if it changes which tips are
   counted? — no, lock state does not affect the predicate which
   only checks tip-color vs socket-color at the same slot, so
   this branch will not advance the level. Still, evaluate to be
   safe.) If the click missed, do not consume a step (return
   without `complete_action()` — wait, must always call
   `complete_action()`; see implementation note below).
5. Always end with `self.complete_action()`.

(The "no-step-on-miss" requires NOT incrementing `_action_count`
on miss. Since `_action_count` is engine-managed via
`complete_action`, an alternative is: track a private
`_steps_consumed` counter and feed it to the HUD instead of the
engine count. This is the approach kf42 uses per the notes in its
mechanism-detail.)

`_get_valid_actions()`:
- ACTION5 is always offered.
- For each tip currently in `self.tips`: offer ACTION6 with
  `(x, y) = (tip.x + 1, tip.y + 1)` (the tip-centre converted via
  the camera's display scale — the cn04 `display_to_grid` round-
  trip handles this transparently if we feed display-space coords
  via the camera's `grid_to_display` helper; if the camera scale is
  1 then grid-coord == display-coord).

`_get_hidden_state()`:
Returns `np.array(...)` of shape `(2, max_tips)` where row 0 is
each tip's slot index and row 1 is `1` if locked else `0`. Pad
unused columns with `-1`.

## 7. Win condition

Define `slot_at(sprite) := self.tip_slot[sprite]` for tips and
`self.socket_slot[sprite]` for sockets.

Win predicate `_win_check() -> bool`:

```python
for socket in self.sockets:
    sk_slot = self.socket_slot[socket]
    sk_color = self.socket_color[socket]
    matched = False
    for tip in self.tips:
        if self.tip_slot[tip] == sk_slot:
            tip_color = tip.pixels[1, 1]   # the centre cell of the 3x3 tip
            if tip_color == sk_color:
                matched = True
                break
            else:
                # there is a tip at this socket's slot but wrong colour
                return False
    if not matched:
        # no tip is at this socket's slot
        return False
return True
```

Notes:
- Ambiguity: a slot can hold AT MOST one tip (we never co-locate two
  tips), so the inner loop has at most one true hit.
- If a slot has a socket but NO tip has rotated into it yet, the
  socket is unsatisfied → predicate is False.
- The predicate is symmetric: any unsatisfied socket fails the
  whole; ALL sockets must be satisfied to win.
- After the predicate returns True, `step()` calls
  `self.next_level()`. After level 3 completes, the engine's base
  class auto-fires `self.win()` on the next ACTION5 commit — modelled
  on cn04 where the last-level transition triggers the engine's
  auto-win.

This is testable from outside the game class (just instantiate the
predicate state and call), satisfying the
`design-constraints/checklist.md` "concrete, testable predicate"
rule.

## 8. Lose condition

Single condition: `step_bar.current_steps == 0` while the win
predicate is False. No hazards, no chasers, no instant-fail
collision — the only way to lose is to exhaust the step budget. This
matches 12+ reference games whose only lose-mode is the step
counter (cn04, lp85, ar25, sp80 — the four games whose code we cited
all have step-counter-only).

`step()` checks `current_steps == 0` BEFORE evaluating
ACTION5/ACTION6, so a level that begins with the player already at
0 steps loses immediately — defensive against
`level.get_data("StepCounter") == 0` misconfiguration.

## 9. Novelty note

This section restates the novelty case from `mechanic-pick.md` with
the spec-level details now visible.

### Closest taxonomy entries

- **ar25** (`shape-mirror-cover`, ACTION5 = rotate). Distinguishing
  rule: ar25 rotates A SELECTED PIECE (one at a time, chosen by
  click). qz73 rotates THE WHOLE STRUCTURE; the player never selects
  a sprite to rotate. Action-cardinality differs: ar25's ACTION5 is
  parameterised by the selection state; qz73's ACTION5 is global.
- **cn04** (`nub-pair-glyph`, ACTION5 = rotate selected piece). Same
  distinction as ar25 — global rotation vs per-piece rotation.
  qz73's win predicate is per-socket colour equality; cn04's is
  pixel-level connector coincidence between piece BOUNDARIES — not
  a positional/colour match like qz73.
- **lp85** (`row-col-shift-grid`, click triggers permutations). lp85
  has many distinct buttons each applying a different hard-coded
  permutation; qz73 has one ACTION5 verb applying ONE rotation
  repeatedly. Visually unrelated (lp85: 2D grid of cells with
  marginal buttons; qz73: radial structure).
- **tr87** (`tape-rewrite-rule`, ACTION1/2 cycle a glyph). tr87
  cycles SYMBOL IDENTITIES at a cursor; qz73 cycles SLOT POSITIONS
  of fixed-identity tips. Different verb, different visual (two
  tape-rows vs one radial structure).
- **vc33** (`row-slide-pull-tab`, ACTION6 click triggers a row
  swap). vc33 has only ACTION6; qz73 has ACTION5 + ACTION6 with
  ACTION5 as the load-bearing distinctive verb. vc33's swap is a
  local row-pair exchange; qz73's rotation is a global cyclic shift.
- **dc22** (`colour-cycle-walk`, walking-on-trigger cycles wedges).
  dc22 has an avatar that walks; qz73 has no avatar. dc22 cycles
  colour values; qz73 cycles position assignments.
- **cd82** (`orbit-fire-paint`, basket on 8-position ring + fire).
  cd82's ring is the player's basket-position selector
  (ACTION1-4 step around the ring); qz73's ring is the rotor
  itself. cd82 has a target canvas being painted; qz73 has no
  canvas — the rotor IS the target.
- **s5i5** (`rod-stretch-retract`, click colour-swatch rotates rods
  of that colour 90°). s5i5 rotates per-colour-class via click; qz73
  rotates the WHOLE rotor via ACTION5 and locks per-spoke via click.
  Different verb, different cast of supporting elements.

For every other taxonomy row (16 games), the family is
unambiguously different — walking, pushing, drawing, shooting,
matching, etc.

### Vs. `prior-games/index.md`

Only one prior: `kf42` (`tether-pawn-cycle`). Distinguishing rule
articulated in `mechanic-pick.md`'s 8-dimensions table — qz73
shares only the universal step-counter dimension with kf42; it
diverges on what's-on-the-board (rotor vs pawns), what-the-player-
does (rotate-and-lock vs select-and-walk), what-the-level-asks
(socket-colour-match vs pawn-on-pad), supporting-cast
(hub/spokes/sockets vs pawns/pads), visual-signature (radial
structure vs sparse open arena), pixel-grain (multi-cell hub +
3×3/5×5 ring sprites vs 1×1 pawns), and core-dynamic (cyclic
permutation puzzle vs tethered navigation puzzle).
