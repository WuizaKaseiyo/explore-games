# qz73 — radial-cycle-lock

## Summary
A central hub anchors a ring of eight angular slots; some slots
hold small coloured tip-pieces and others hold matching coloured
hollow rings ("sockets"). The player has two verbs: ACTION5
advances every unlocked tip-piece one slot clockwise (skipping
slots held by locked tips); ACTION6 click toggles whether a tip is
locked. The level is solved when every socket-slot contains a tip
of the matching colour. The only failure mode is exhausting the
per-level step counter.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | "advance dial" — every UNLOCKED tip moves to the next slot clockwise that is not held by a locked tip; the rotation is computed atomically (two-pass desire/commit) so simultaneous shifts don't collide. | always valid; a locked tip never moves. |
| ACTION6 | "toggle lock at click" — `camera.display_to_grid` converts the click pixel coords to grid coords; `level.get_sprite_at(gx, gy, "tip")` looks up the clicked tip; if found, its `tip_locked` flag flips and a 4-corner black overlay (`pdmovjcnhi`) toggles between `InteractionMode.REMOVED` and `INTANGIBLE`. Clicks that miss a tip are no-ops (no step consumed). | always offered; ineffective on hub / socket / empty cells. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | rotation only (no locks needed) | 3 tips at slots {0:orange, 2:green, 4:purple}; 3 sockets at {2:orange, 4:green, 6:purple}. Two ACTION5 presses suffice — random play has a non-zero per-run probability of stumbling through within the 16-step budget (~1/16 per turn that a 2-in-a-row ACTION5 occurs). |
| 2 | rotation + lock | 3 tips at {0:O, 3:G, 6:P}; 3 sockets at {1:O, 4:G, 6:P}. The purple tip is already at its socket-6 — but ACTION5 alone moves it away. Solution: lock purple, then ACTION5 once; orange and green each advance to their sockets. 2 actions, budget 18. |
| 3 | composition of rotate + lock | 5 tips at {0:O, 1:G, 2:P, 5:M, 7:Y}; 5 sockets at {0:Y, 2:O, 3:G, 5:M, 6:P}. Magenta is already at slot-5 (matched). No single rotation aligns more than 1 socket without lock support. Witness sequence: lock M, rotate, lock Y, rotate, lock O+G, rotate (7 actions, budget 32). Pure-rotation play never satisfies all 5 sockets simultaneously — the rotation orbit cycles each tip by the same +1 modulus, so colours cannot align with a heterogeneous socket arrangement. |

## Win condition

After every action, walk the list of socket sprites. For each
socket, find the tip currently at that slot (by matching slot
index). If no tip is there, the socket is unsatisfied → predicate
False. If a tip is there but its centre-pixel colour
(`tip.pixels[1, 1]`) does not equal the socket's colour
(`socket.pixels[0, 0]`), unsatisfied → predicate False. If every
socket is satisfied, predicate True → `self.next_level()`.
After level 3 completes, the engine's base class fires
`self.win()` automatically (per `next_level()`'s last-level
branch).

## Winning strategy — Level 1

Initial layout (slots indexed 0=top, 1=top-right, 2=right,
3=bottom-right, 4=bottom, 5=bottom-left, 6=left, 7=top-left):

- Tips: orange at slot 0, green at slot 2, purple at slot 4.
- Sockets: orange ring at slot 2, green ring at slot 4, purple
  ring at slot 6.

After step 0 the green tip already sits *inside* the orange
ring at slot 2 (mismatch); the purple tip sits inside the green
ring at slot 4 (mismatch); slot 6's purple ring is empty.

Each ACTION5 press shifts every (unlocked) tip one slot
clockwise. After **two ACTION5 presses**, every tip has
advanced by 2: orange 0 → 2, green 2 → 4, purple 4 → 6.
Now each socket holds a tip of its own colour — the win
predicate fires and the level ends.

Plain-words instruction for a human: *press the rotate verb
twice; do not click any tip*. Total: 2 actions out of a
16-step budget. Random play has a non-zero chance of stumbling
through the budget because two ACTION5s in a row (at one-in-
four-actions-per-turn) are reachable on average within ~16
turns; the lock-toggles a random agent invokes can make
recovery impossible, so the strategy above is the reliable
deterministic solve.

## Winning strategy — Level 2

Initial layout: orange tip at slot 0, green tip at slot 3,
purple tip at slot 6; orange socket at slot 1, green socket at
slot 4, purple socket at slot 6. The purple tip already sits
on its purple socket — but if ACTION5 is pressed first, it
would move away.

Solution in 2 actions:
1. ACTION6 click the purple tip (at slot 6) — locks it.
2. ACTION5 — orange advances 0 → 1 (matches), green advances
   3 → 4 (matches), purple is locked and stays at 6 (matches).

## Winning strategy — Level 3

Initial layout: orange@0, green@1, purple@2, magenta@5,
yellow@7; sockets yellow@0, orange@2, green@3, magenta@5,
purple@6. Magenta already matches its socket at slot 5.

Witness sequence (7 actions out of a 32-step budget):

1. ACTION6 click magenta at slot 5 — lock it (it is already
   matched and must not move).
2. ACTION5 — unlocked tips advance by 1: orange 0→1, green
   1→2, purple 2→3, yellow 7→0. Yellow now matches socket-0.
3. ACTION6 click yellow at slot 0 — lock it.
4. ACTION5 — unlocked tips advance: orange 1→2, green 2→3,
   purple 3→4. Orange and green now match sockets-2 and -3.
5. ACTION6 click orange at slot 2 — lock it.
6. ACTION6 click green at slot 3 — lock it.
7. ACTION5 — only purple is unlocked, at slot 4. The CW walk
   skips locked slot 5 and lands purple at slot 6, matching
   the purple socket. Win.

## Lose condition

Single condition: per-level step counter exhausted while the win
predicate is False. The internal `steps_used` counter increments
on each successful ACTION5 and on each successful ACTION6
(misclicks do not consume). When `steps_used >= max_steps`,
`self.lose()` fires. No hazards, no chasers, no instant-fail
collision.

## Internal state

- `self.tips: list[Sprite]` — the placed tip sprites for the
  current level (sorted by initial slot ascending in
  `on_set_level`).
- `self.tip_slot: dict[Sprite, int]` — current slot index 0..7
  per tip.
- `self.tip_locked: dict[Sprite, bool]` — per-tip lock flag.
- `self.lock_marks: dict[Sprite, Sprite]` — per-tip black-corner
  overlay sprite, added to the level at level-start, initially
  `InteractionMode.REMOVED`.
- `self.sockets: list[Sprite]` — placed socket sprites.
- `self.socket_slot: dict[Sprite, int]` — slot index per socket
  (static across the level — sockets never move).
- `self.socket_color: dict[Sprite, int]` — palette value per
  socket, derived once from `socket.pixels[0, 0]`.
- `self.step_bar: kfnplrxazq` — `RenderableUserDisplay` instance
  registered with the camera; tracks current/max steps.
- `self.max_steps: int` / `self.steps_used: int` — per-level
  budget and tally.
- Module constant `SLOT_CENTERS: list[tuple[int, int]]` — the 8
  fixed `(x, y)` pixel slot-centre positions on the radial ring.

## Notable code patterns

- **Atomic two-pass rotation.** `_rotate_unlocked()` computes the
  proposed new slot for every unlocked tip in pass 1 (`proposed`
  dict), then commits all of them in pass 2. This avoids the
  "tip A moves into tip B's old slot while B is also moving"
  conflict that a per-tip sequential commit could produce.
  Reusable as "all-things-move-simultaneously without
  interleaving collision".
- **Skip-locked-slot CW walk.** Inside the proposed-position pass,
  the walk does `for offset in range(1, 9): cand = (cur + offset) % 8;
  if cand not in locked_slots: break`. This implements "rotate
  through the unlocked subset" without enumerating the unlocked
  positions explicitly, which keeps the code O(N) per ACTION5.
- **InteractionMode toggle for the lock overlay.** Lock-marks are
  added to the level at level-start and toggled between `REMOVED`
  and `INTANGIBLE` on each lock-flag flip — the cleaner pattern
  per the universal scaffold's "Two-sprite swap" note. Avoids
  adding/removing sprites mid-game.
- **`color_remap(None, palette)` as the per-instance recolouring
  primitive.** One `rkqbnzwlth` tip definition (default colour 8) is
  cloned and recoloured per-tip via
  `clone().color_remap(None, <colour>).set_position(...)`. Same
  for `eyaslwiprn` socket (default colour 14). One sprite definition
  per role; per-instance variation lives in the level data.
- **`_get_valid_actions` pre-enumerates ACTION6 candidates per
  tip.** Returns `[ACTION5, ACTION6@(slot0_centre), ...]` —
  letting an agent treat the click-space as a small finite set
  rather than a 64×64 continuous one. Modelled on r11l's
  pre-enumerated 256-entry valid-action grid but at 3-5 candidates
  per turn.
- **Step-bar HUD with private counter.** The HUD is driven by
  `self.steps_used` rather than the engine's `_action_count`,
  letting misclick-ACTION6s be no-cost without complicating the
  engine's action flow. cn04 uses the engine counter; sb26 uses a
  dedicated `sjcuorclg` energy field; this game follows sb26's
  approach for finer-grained control over what counts as a
  "step".
