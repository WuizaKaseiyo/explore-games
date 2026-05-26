# Post-finalize refinement: ratchet/clutch state-display redesign

This refinement happened in three rounds, each addressing a fresh
issue raised after the initial run finalised cleanly. The final
design is the 2-state vertical bolt described in round 3.

## Round 1 — east-tang → above-disc indicator

### Why

The original release used yellow / purple "tang" sprites placed one
column east of each ratchet/clutch disc. Two issues:

1. **Hidden state**. Clicking the tang cycled the ratchet's
   direction state without changing anything visible on screen,
   making the direction a hidden variable
   (forbids `forbidden-elements.md` / `from-tech-report.md` § 4 /
   `reference-game-patterns.md` # 11 anti-pattern).
2. **Visual occlusion**. The east-tang sat in the gap between the
   ratchet's east tooth and the east target-indent on its collar,
   breaking the mark↔target visual coupling.

### What changed

- Removed `tang_dir` / `tang_lever` sprites.
- Introduced 3×1 horizontal `ratchet_indicator` / `clutch_indicator`
  sprites placed in the 1-cell gap between the disc top and the
  collar's top frame, centred on the disc.
- Indicator pixels mutated on click to encode state:
  - Ratchet 3-state: LOCKED `[3,3,3]`, CW `[3,3,11]`, CCW `[11,3,3]`.
  - Clutch 2-state: ENGAGED `[15,15,15]`, DISENGAGED `[3,3,3]`.

## Round 2 — indicator moved above the collar frame

### Why

User noted the clutch indicator was "hard to see" because the
`[3,3,3]` DISENGAGED state was the same grey as the collar frame
just above it, and the indicator's proximity to the gear's cog-tooth
pattern was visually crowded.

### What changed

- Indicator y-position moved from `disc.y - 1` (inside the collar's
  top gap) to `disc.y - 3` (one row above the collar's top frame),
  against the playfield background where every state colour has full
  contrast.

## Round 3 — 2-state bolt design (current)

### Why

User raised two further issues:

1. **The clicked-indicator-doesn't-rotate-the-gear confusion**. With
   the 3-state indicator the player saw the yellow dot move from the
   centre to the right (LOCKED → CW) but the gear stayed at 0°,
   which read as "the gear is still locked" because there was no
   on-screen reason to expect that the next click on the gear's hub
   would now succeed. The indicator was a *symbol* of state rather
   than a *picture* of state.
2. **CCW state was never used**. Re-tracing the witnesses for L2 and
   L3, the third state was never required by any solution. It was
   carrying cognitive load without paying for it.

### What changed

- Dropped CCW: ratchet state space is now `{LOCKED, CW}`. State
  cycle is a binary toggle: `LOCKED ↔ CW`. Constant `DIR_BLOCKED`
  renamed to `DIR_LOCKED`. Cascade rule simplified: when state is
  `CW`, only `+90°` arrivals rotate the ratchet and propagate past
  it; `−90°` arrivals are blocked.
- Replaced the 3-cell horizontal indicator with a **1×5 vertical
  bolt** sprite (`ratchet_bolt` and `clutch_bolt`):
  - The yellow / purple "rod" occupies 3 of the 5 cells.
  - Engaged state (LOCKED for ratchet, ENGAGED for clutch) →
    rod at the bottom 3 cells, visually extending toward the disc.
  - Disengaged state (CW for ratchet, DISENGAGED for clutch) →
    rod at the top 3 cells, visually retracted.
  - The remaining 2 cells are dim grey "track" so the click target
    stays a stable 1×5 bounding box.
  - This mirrors the universal mechanical metaphor of a deadbolt
    or a circuit-breaker — bolt-down = engaged, bolt-up = free.
- Click target: any cell of the 1×5 sprite. Bolt top-left at
  `(disc.x + 2, disc.y - 7)`. Centre cell click coord `(disc.x + 2,
  disc.y - 5)` works (e.g. L2 ratchet at `(30, 24)`, L3 ratchet at
  `(20, 24)`, L3 clutch at `(40, 24)`).

### Witness coordinate progression

| Action | Round 0 (east tang) | Round 1 (top indicator) | Round 2 (above collar) | Round 3 (bolt, current) |
|---|---|---|---|---|
| L2 ratchet click | `(34, 31)` | `(30, 28)` | `(30, 26)` | `(30, 24)` |
| L3 ratchet click | `(24, 31)` | `(20, 28)` | `(20, 26)` | `(20, 24)` |
| L3 clutch click  | `(44, 31)` | `(40, 28)` | `(40, 26)` | `(40, 24)` |

## Verification

- `ast.parse` passes.
- L1, L2, L3 witnesses (2 / 5 / 11 actions) all still solve to
  `GameState.WIN` end-to-end with the round-3 design.
- All 4 custom mechanic checks pass on the round-3 binary.
- Re-rendered initial-state PNGs at
  `workspace/smoke-frames/level_{1,2,3}.png`; state-variant frames
  at `level_2_ratchet_unlocked.png` and
  `level_3_clutch_disengaged.png` show the bolt's rod sliding from
  bottom (engaged) to top (disengaged).

## Files updated (final)

- `prior-games/gx7m/gx7m.py` — 2-state ratchet logic, `ratchet_bolt`
  / `clutch_bolt` sprites, `_render_ratchet_bolt` /
  `_render_clutch_bolt` helpers.
- `prior-games/gx7m/mechanism-detail.md` — summary, level table,
  internal state, notable patterns.
- `runs/2026-05-06T14-11-46/workspace/mechanic-spec.md` — sprite
  roster, L2/L3 layout, `M2` / `M3` definitions, witness coords.
- `runs/2026-05-06T14-11-46/workspace/smoke-test-custom.py` —
  clutch click coord at `(40, 24)`.
- `prior-games/gx7m/run-archive/` — resynced.

## Files NOT updated

- `prior-games/index.md` — the row stays; mechanic-family tag and
  description are unchanged.
- `metadata.json` — unchanged.
- `runs/.../meta.json` — the run is still `completed`; this
  refinement is a post-finalize patch, not a re-run.
