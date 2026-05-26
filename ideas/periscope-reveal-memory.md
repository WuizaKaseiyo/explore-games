# Periscope-Reveal-Memory

*(NEW idea filling the **partial-observability blindspot** — the
existing 17 `gg*` games and the prior alphanumeric corpus all show
the player the full state of the board at all times. Real-world
inspiration: submarine periscopes, fog-of-war in strategy games,
sonar/echolocation. Top-down hidden-grid layout.)*

## Summary

The play board is shrouded in a **fog**: every cell is rendered
dark until the player sweeps a directional **periscope** beam over
it. The periscope sits on the right-hand panel as a small
swivelling sprite. Its current beam direction is one of N/E/S/W;
ACTION5 rotates it 90° clockwise. ACTION6 click triggers a
**scan**: the engine reveals the row/column ahead of the periscope
for the current tick only.

Underneath the fog hide several **coloured pawns** at unknown
positions. The player's task: scan to find pawns, then click each
to **tag** it. A tagged pawn stays revealed (and is logged on the
right-side roll). When every pawn of every required colour is
tagged the level is won.

## Visual elements (distinct from prior corpus)

- 64×64 canvas. The board area is a 13×13 logical grid rendered at
  CELL=4 px. Default lighting is **midnight-grey** (palette 13)
  with 1-pixel star-flecks (random-but-fixed per level seed) for
  texture; this is **not** the flat grey of every other corpus
  game.
- The **periscope** sprite is a 5×5 cog on the right rim with a
  thin yellow chevron showing current direction. The chevron
  rotates one quadrant per ACTION5.
- A **scan event** lights the entire row or column directly in
  front of the periscope for ONE rendered frame as a translucent
  yellow overlay; cells previously occulted now show their
  contents (pawn colour or empty) on that frame only. After the
  next action, those cells return to fog **unless** they hold a
  *tagged* pawn or the cell was tagged itself.
- **Pawns** under fog are not normally visible. After a scan
  reveals one, the player has the rest of that turn (until the
  next action) to tag it.
- **Tagged pawns** render permanently (no fog): a 1-cell coloured
  bob with a small white tag pin at its top-left.
- A **roll panel** on the right rim shows one row per pawn colour:
  the requirement (e.g. "tag 2 reds") and current count
  (silhouettes filling left-to-right).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Rotate the periscope 90° CW. The current scan view (if any) is cleared on the next action. | always |
| ACTION6 | Click cell `(x, y)`. Resolves to one of: (a) cell currently inside a live scan ray and contains an untagged pawn → tag it (permanently revealed); (b) cell currently inside a live scan ray and is empty → trigger a "marker" pin on that cell (permanently visible as ✕); (c) any cell NOT inside the live scan but holding a marker → remove the marker; (d) the periscope itself → trigger a fresh scan in the current direction. Misclick (off-board, off-fog) = no-op, no step. | always |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — periscope-rotate:** ACTION5 rotates the periscope 90° CW.
- **M2 — scan-line reveal:** ACTION6 click on the periscope
  reveals every cell in a straight line in the chevron direction
  for the next rendered frame (until the next action). Walls
  block the scan; the line stops at the first wall (or at the
  board edge).
- **M3 — tag-pawn:** ACTION6 on a revealed pawn permanently tags
  it (no longer hidden by fog). Tagged pawns may still be
  reasoned about for the win predicate.
- **M4 — marker-pin:** ACTION6 on a revealed empty cell pins a
  small ✕ marker that remains visible. Markers are mnemonic
  scaffolding — they do not affect the game state, only the
  player's memory. The player has only `marker_budget` markers
  per level (typically 4).
- **M5 — match-roll (level 2+):** the win predicate requires
  the level's roll panel to be filled. Some pawns are
  *imposters*: revealed-tagged correctly, but if the
  player tags too many pawns of any colour, the level fails.
  (Roll requires exactly 2 reds: tagging a 3rd red is a fail.)
- **M6 — drift-fog (level 3+):** the fog "drifts": tagged pawns
  remain visible, but **markers fade** after 5 ticks unless
  the player re-confirms them by another scan ray crossing the
  marked cell. This forces a scanning cadence — pure long
  exploration plus reasoning isn't enough; the player must
  periodically re-verify.
- **M7 — colour-paint scanner (level 3+):** before triggering a
  scan, the player can ACTION6 click on a colour palette in the
  roll panel to **tint the scanner** (one of the level's pawn
  colours). A tinted scan reveals only pawns of the matching
  colour — pawns of other colours remain hidden, even in the
  scan beam. This lets the player collapse uncertainty without
  accidentally triggering the over-tag fail (M5) on wrong
  colours.

## Per-level progression

### Level 1 — base periscope (M1 + M2 + M3)
- 10×10 board. 3 pawns hidden (one each of red, blue, gold).
  No imposters. No walls. Roll requires 1 of each colour. The
  player rotates and scans until each pawn is found and tagged.
- **Witness:** ~12 actions (rotate + scan + tag, repeat).
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (markers) + M5 (imposters)
- 13×13 board. 6 pawns: 2 red, 2 blue, 1 gold, 1 silver
  imposter. Walls partition the board into 3 alcoves. Roll
  requires exactly 2 red, 2 blue, 1 gold. **Tagging the silver
  imposter is a level-fail.**
- The walls limit scan ranges, so the player must walk the
  periscope through several rotations and use markers to
  remember where pawns were sighted before tagging. Tagging the
  imposter looks tempting because it appears in the scan like
  any other pawn — the player must read its colour before
  tagging.
- **Witness:** ~28 actions including 3 marker pins. Step budget
  40.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (drift-fog) + M7 (colour-paint scanner)
- 13×13 board, 9 pawns mixed across 4 colours, 2 imposters,
  many walls. Roll requires exactly the right multiset per
  colour. Markers fade after 5 ticks.
- The colour-paint scanner is the strategic verb: tinting the
  scan to "red only" reveals just the 2 red pawns when the
  beam crosses them, leaving silver imposters invisible. But
  paint-changes cost steps, so the player can't tint every
  scan.
- **Witness:** ~60 actions, weaving paint changes, scans, marker
  refreshes, and tags.
- **Mechanics required:** M1, M2, M3, M4, M5, M6, M7.

## Win condition

After every ACTION6, evaluate the roll: every required (colour,
count) row must be exactly satisfied — no over-tagging, no
under-tagging. If the roll is exactly satisfied, fire
`self.next_level()`.

## Lose condition

- `steps_used >= max_steps` triggers `self.lose()`.
- L2+: tagging a wrong-colour pawn (over-counting any colour, or
  tagging an imposter) triggers `self.lose()` immediately. The
  imposter is rendered with a 2-frame red flash before the loss.

## Internal state

- `self.fog: np.ndarray[bool]` — True = occluded.
- `self.live_scan_cells: set[(int, int)]` — currently revealed
  this frame (cleared on next action).
- `self.pawns: list[Pawn]` — `pos`, `colour`, `tagged`,
  `is_imposter`.
- `self.markers: list[Marker]` — `pos`, `placed_tick`,
  `last_refreshed_tick`.
- `self.periscope_dir: int` — 0=N, 1=E, 2=S, 3=W.
- `self.scanner_paint: int | None` — tinted-scanner colour (L3+).
- `self.tick: int`.
- `self.roll_target: dict[colour, int]`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `lq5x — lantern-cone-illuminate`**: lq5x walks a lantern
  with a directional cone in a fully-revealed darkened arena;
  the lantern is the player avatar. Periscope-reveal places the
  player *outside* the board — the periscope has no avatar
  movement, only a rotation and scan, and the board is
  hidden-state until a scan flashes it.
- **vs `bp35 / lf52 — procedural-graph-walk`**: those reference
  games are graph-walks with a known state. Periscope is a
  hidden-state inference puzzle with imposters.
- **vs `gg10 — echo-delay-follower`**: gg10 is a delayed-replay
  movement puzzle. Periscope has no movement, only scan +
  remember.

## Step budget

- L1: 18.
- L2: 40.
- L3: 80.

## Random-resistance

Random rotation + click is exponentially unlikely to satisfy the
roll without tagging an imposter. With 2 imposters out of 11
pawns on L3, random tagging produces a `2/11 ≈ 18%` per-tag
fail-chance on the first wrong pick alone, compounding to
~99%+ failure across an entire random play. The colour-paint
scanner is the only reliable strategy — but that itself
requires deduction.

## Planning depth

- **L1:** shallow — rotate + scan + tag systematically.
- **L2:** moderate — walls force memory; the player uses markers
  as off-grid memory.
- **L3:** deep — drift-fog erases markers, so the player must
  set a *cadence* of refresh scans interleaved with tinted
  identification scans. Many strategies; tight budget.
