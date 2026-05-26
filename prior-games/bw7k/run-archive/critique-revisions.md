# Critique revisions (round 1)

Visit count to `critique_spec`: 1 (under cap of 10).

## Issue 1 — Checklist item 11 violation: L3's `Replay-walls` mechanic is dormant in the witness

**Section quoted** (`mechanic-spec.md` § 4 — Level 3 — Witness solution):

> Replay shade_red snapshot=6, replays UP×6 from `(12, 36)` →
> `(12, 12)` = `target_red`. ✓ Then any subsequent ticks have
> pointer >= snapshot_len, so `shade_red` is exhausted at
> `(12, 12)` and stays put. (The wall at `(8, 12)` is dormant
> in the witness; it defends against trivial-fallback paths
> described below.)
> ...
> The wall at `(60, 8)` is dormant in the witness; it defends
> against trivial-fallback paths described below.

**Problem**: Checklist item 11 requires every earlier-level
mechanic to remain *required* at every later level. Replay-walls
(introduced in L2) is one such mechanic. Item 12 sharpens this:
*"For each mechanic M available at level L, no sequence of
actions may win L within the step budget without triggering M's
distinguishing behavior."*

The current L3 witness wins WITHOUT any wall-skip during a
shade's replay (both shades replay cleanly to their targets, and
both walls are admitted to be "dormant in the witness"). That
means there's a sequence (the witness itself) that wins L3
without triggering Replay-walls' distinguishing behavior. So
Replay-walls is NOT necessary in L3 by the strict counterfactual
test. The L2 mechanic has effectively dropped out of L3.

**How to fix**: Redesign L3 so the witness REQUIRES a wall-skip
during at least one shade's replay. Options:

- (Recommended) Introduce a between-anchors detour wall that
  forces the actor's path to include "extra" moves (e.g. DOWN
  + RIGHT + UP) which then end up in `shade_yellow`'s replay
  tape and require a replay-wall to skip a tail of those
  extra moves so `shade_yellow` ends at the chosen target.
- Or place a target that is NOT at the natural endpoint
  `2*A_i - start`, requiring wall-skips to displace.

Concrete suggested layout (verified by trace):

```
actor start (8, 60)
anchor_red (8, 36); target_red (8, 12)        — natural-endpoint
anchor_yellow (40, 36); target_yellow (40, 12)
actor_goal (24, 4)
wall at (24, 36)   — forces actor to detour between anchors
wall at (44, 16)   — load-bearing replay-wall: blocks shade_yellow's
                     RIGHT-from-(40, 16) during replay
plus standard outer-frame walls
step_budget = 60
```

Witness (28 actions) — pre-red: UP×6 → anchor_red (snapshot 6
of [UP×6]); between-anchors detour: DOWN×1 to `(8, 40)`,
RIGHT×8 to `(40, 40)`, UP×1 to `(40, 36)` = anchor_yellow
(snapshot 16 of [UP×6, DOWN×1, RIGHT×8, UP×1]); post-yellow:
UP×8 + RIGHT×4 to `(24, 4)` = actor_goal.

`shade_red` replay from `(8, 36)` with [UP×6]: → `(8, 12)` =
`target_red` ✓.

`shade_yellow` replay from `(40, 36)` with [UP×6, DOWN×1,
RIGHT×8, UP×1]:
- UP×6 → `(40, 12)`.
- DOWN×1 → `(40, 16)`.
- RIGHT×8: at `(40, 16)` try RIGHT to `(44, 16)` — wall →
  blocked → skip. All 8 RIGHTs blocked → all skipped. Stays
  at `(40, 16)`.
- UP×1 → `(40, 12)` = `target_yellow` ✓.

Replay-walls is now load-bearing in the witness: `shade_yellow`
relies on the wall at `(44, 16)` to skip 8 RIGHTs that would
otherwise carry it to the right boundary, then the final UP
brings it to `target_yellow`.

**Additional note**: re-verify the other two carried-forward
mechanics (Anchor-spawn-shade and Shade-replays-tape) remain
required in L3 — they do, because both anchors must be visited
and both shades must replay-then-arrive.

---

## Cross-check on remaining checklist items (no issues found)

- Item 1 (palette): all sprite pixel arrays use values in
  `{-1, 3, 4, 5, 8, 9, 10, 11, 12, 14}`. ✓
- Item 2 (universal scaffold): spec describes the scaffolded
  structure (sprite bank, level list, constants, HUD, game
  class). ✓
- Item 3 (`available_actions`): subset `[1, 2, 3, 4]` of
  `[1..7]`. ✓
- Item 4 (3 levels): EXACTLY 3 `Level(...)` entries. ✓
- Item 5 (game ID): `bw7k` is 4 lowercase alphanumeric, not in
  the 25 reserved, not in `prior-games/index.md`, not in any
  `prior-games/<id>/` folder, not an English word. ✓
- Item 6 (priors): mechanics drawn from objectness +
  geometry/topology + agentness; no other priors invoked. ✓
- Item 7 (forbidden elements): no letter/digit/arrow glyphs, no
  real-world clipart, no green=go / red=danger conventions. The
  red and yellow palettes are used for COLOUR-MATCHED PAIRS
  (anchor↔shade↔target) — that's a within-game labelling
  convention, not a cultural one (the player learns "red anchor
  spawns red shade and red target collects red shade" by playing,
  not by importing real-world meaning). ✓
- Item 8 (≥ 2 distinct mechanics): 5 mechanics across L1-L3. ✓
- Item 9 (L1 tutorial, no on-screen text): single anchor + single
  target + actor-goal; no walls inside the playing area; no on-
  screen text. ✓
- Item 10 (L2/L3 compose): L2 composes Walking/Anchor-spawn/
  Replay with the new Replay-walls mechanic; L3 (post-revision)
  composes all four with multi-shade simultaneity. ✓ pending the
  L3 revision above.
- Item 11 (mechanic inheritance and +1-or-+2 per level):
  L1=3, L2=4 (+1), L3=5 (+1) — flagged above; revision required
  to make L3's Replay-walls load-bearing in the witness. ❌ →
  revise per Issue 1.
- Item 12 (counterfactual necessity): see Issue 1 above for the
  L3 revision; the per-mechanic table will pass after revision.
- Item 13 (mechanic family absent from taxonomy): ✓.
- Item 14 (mechanic family absent from prior-games): ✓.
- Item 15 (distinguishing rules): ✓.
- Item 16 (win condition): stated as `_check_win()` predicate. ✓.
- Item 17 (lose condition): step counter ≤ 0. ✓.
- Item 18 (difficulty floor and ceiling, four bullets per level):
  all levels have (a)(b)(c)(d). ✓.
- Item 19 (no hidden state): the move-tape T is internal but the
  player observes shade's movement live as the visible cue;
  spawn events animate; anchor consumed (set to REMOVED)
  visibly. ✓.
- Item 20 (not low-resolution): 64×64 native grid; 4×4 sprites
  with internal pixel structure (corner+interior+dark-center for
  pawns; hollow-ring for targets; corner-dot for anchors;
  corner-interior for walls); shape carries meaning, not just
  colour. ✓.
- Item 21 (UI teaches): solid-bordered glyph = movable pawn;
  hollow-ring = destination; corner-dot pad = trigger; solid
  filled = wall. Each role has a distinct silhouette family. ✓.
- Item 22 (ACTION7 strict-undo or absent): omitted from
  `available_actions`. ✓.

## Verdict

One revision required (Issue 1 — L3 mechanic carry-over).
Transition back to `write_spec` to address.
