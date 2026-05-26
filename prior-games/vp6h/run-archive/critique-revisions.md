# Critique revisions — vp6h, round 1

**Decision: REJECT the spec; transition back to write_spec.**

The spec's mechanic family, novelty argument, and overall composition arc are sound. However several concrete defects must be fixed before implementation.

## Issue 1 — L3 witness phase 4 routing is geometrically impossible (BLOCKING)

**Checklist item violated:** 18(b) human-tractable / witness validity (the
written witness must actually win the level deterministically; a witness
that walks through a tangible pillar is no witness at all).

**Offending text (§4 → Level 3 → Witness solution → Phase 4):**

> ```
> # Phase 4: collect B (col 13, row 4..5; nearest pickable cell is (13, 5))
> # Avatar at (7, 9). Need (13, 5).
> ACTION4 ×6, ACTION1 ×4    # (7,9) -> (13,9) -> (13,5) — pickup B
> ```

This path requires the avatar (2×2 sprite at top-left position) to
occupy cells with col 13 and rows 9 or 10 — but those cells contain the
bot-pillar at `(col=13, row=8..10)`, which is tangible and blocks
avatar movement. Specifically:
- Avatar at top-left `(12, 9)` covers `(12..13, 9..10)`; cells `(13,9)`
  and `(13,10)` are pillar → blocked.
- Avatar at top-left `(13, 9)` covers `(13..14, 9..10)`; cells `(13,9)`
  and `(13,10)` are pillar → blocked.

The avatar cannot pass through col 12-13 at rows 7-10 because its 2×2
footprint always extends one column to the right.

**Concrete fix:** Re-route phase 4 around the bot-pillar via col 11:

```
# From (7, 9) — avatar covers (7..8, 9..10)
ACTION4 ×4   # (7,9) -> (11,9). Avatar at (11..12, 9..10). Walkable; col 13 not crossed.
ACTION1 ×5   # (11,9) -> (11,4). Avatar at (11..12, 4..5). Walkable.
ACTION4 ×2   # (11,4) -> (13,4). At (12,4) avatar covers (12..13, 4..5) — overlaps B but
             #   cell (12,4) is bot-LIT (col 12 in bot-cols 10..14, no col-12 pillar) → no pickup.
             # At (13,4) avatar covers (13..14, 4..5) — overlaps B; cell (13,4) is top-shaded
             #   (col 13 outside cols 0..4) and bot-shaded (col 13 has bot-pillar above row 4,
             #   wait pillar is at rows 8..10 which is BELOW row 4, so the pillar blocks the
             #   upward bot-rays). Both shaded → pickup B.
```

Phase 4 cost: **11 actions**, not 10. **Total L3 witness: 25 actions** (2+2+10+11), not 24.

## Issue 2 — L2 phase 1 witness action count is off-by-one (MINOR)

**Offending text (§4 → Level 2 → Witness solution → Phase 1):**

> ```
> ACTION4, ACTION1, ACTION1            # (1,13) -> (2,13) -> (2,12) -> pickup A at (2,12)
> ```
> 3 actions: `ACTION4, ACTION1, ACTION1`. Avatar now at (2, 12), A collected.

The path written is 2 transitions (`(1,13) → (2,13) → (2,12)`), so 2
actions, not 3. Pickup of A fires when the avatar's 2×2 footprint at
top-left `(2,12)` overlaps crystal A at `(col=2, row=11..12)`. The
third `ACTION1` would move the avatar to `(2,11)` — unnecessary for
pickup.

**Concrete fix:** drop the third ACTION1; phase 1 is `ACTION4, ACTION1` =
**2 actions**. Total L2 witness: **25 actions** (2+14+1+8), not 26.

## Issue 3 — L1 witness action count is off-by-one (MINOR)

**Offending text (§4 → Level 1 → Witness solution):**

> ```
> ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,   # walk right cols 2→7
> ACTION1, ACTION1                               # walk up rows 13→11
> ```
> Total: 7 actions.

Pickup fires at avatar position `(7, 12)` (top-left), where the 2×2
footprint covers `(7..8, 12..13)` and overlaps crystal at `(col=7,
row=11..12)`. The avatar reaches `(7, 12)` after `ACTION4 ×5` then
`ACTION1 ×1` = 6 actions. The second `ACTION1` would move avatar to
`(7, 11)` — unnecessary for pickup.

**Concrete fix:** drop the second ACTION1; L1 witness is **6 actions**, not 7.

## Issue 4 — Crystal palette uses green (14), borderline cultural (MINOR)

**Checklist item potentially violated:** 7 (no cultural conventions).

**Offending text (§3 sprite roster):**

> | `crystal` | 2×2 | 10 (light-blue) edges, 14 (green) interior cross | ...

`forbidden-elements.md` lists "Green-means-go" as a cultural convention to
avoid. A green pixel in a *collection target* sprite carries the
soft "green=collect-this-thing-it-is-good" association. Not strictly a
hard violation (green pixels exist on many reference-game sprites
without semantic load), but this game's crystals are exactly the
pickable target, which sharpens the association.

**Concrete fix:** swap palette `14` for palette `15` (purple) in the
crystal sprite. Crystal pixels: `[[10, 15], [15, 10]]`. Light-blue +
purple checker carries no cultural semantic.

## Issue 5 — L2 layout inconsistency: col-2 pillar contradicts the M2 necessity argument (BLOCKING)

**Checklist item violated:** 12 (strict counterfactual necessity for
M2).

**Offending text (§4 → Level 2 → Layout, after the iteration):**

> Revised L2 layout (final):
> - `pillar_short` at (col=2, row=5..7) — creates default-shadow in
>   col 2 (already outside lantern; redundant but visually anchors the
>   column).

But §4 → Level 2 → Difficulty justification (c) → witness reasoning
chain claims:

> "If I slide the lantern leftward to expose col 6, col 2 becomes lit
> and A is no longer pickup-able. Therefore, collect A first."

If col 2 has a pillar at rows 5..7, then crystal A at `(col=2, row=11..12)`
is **always** top-shaded — whether the top-lantern is at default
cols 5..9 (col 2 outside range) OR slid to cols 0..4 (col 2 in range
but pillar above row 11 → still top-shaded). The "must collect A
first" ordering doesn't bind. The witness can slide-then-walk in any
order without losing A.

This makes M2's necessity a thin "B requires sliding" argument
without any *ordering* constraint — and the planning-depth bullet's
"plausible-but-wrong: slide-first" rejection no longer holds.

**Concrete fix:** **remove the col-2 pillar from L2.** Updated L2
layout:
- One `pillar_short` at `(col=14, row=5..7)` for visual anchoring of
  col 14.
- (Optionally also remove the col-14 pillar; it doesn't bind the
  witness either way since col 14 stays outside the lantern after a
  leftward slide.)
- Crystals A=`(col=2, row=11..12)`, B=`(col=6, row=11..12)`,
  C=`(col=14, row=11..12)` unchanged.

After the fix, col 2 has no pillar. With top-lantern at default
cols 5..9, col 2 is outside range → top-shaded → A safe. With top-lantern
slid to cols 0..4, col 2 is in range AND no pillar above → top-LIT → A
unsafe (no-op). The witness must collect A before sliding leftward.
M2's necessity is now grounded in this ordering: "without M2 the lantern
stays at default and B is unreachable; with M2 the player must order
A-pickup before the slide."

## Issue 6 — `BlockingMode` not specified for pillars (CLARIFY)

**Checklist item potentially violated:** 18 — implementation determinism.

The spec doesn't specify whether pillars use `PIXEL_PERFECT` or
`BOUNDING_BOX` blocking. With `PIXEL_PERFECT` (default) and pillar
sprites that are solid (no -1 transparent cells), the two are
equivalent. Spec should state this explicitly so the implementer
doesn't accidentally drop blocking entirely.

**Concrete fix:** in §3 sprite roster, append to each pillar row:
"`blocking=BlockingMode.PIXEL_PERFECT`" or simply add a note "pillars
use the default `BlockingMode.PIXEL_PERFECT` and have no -1 cells, so
blocking-mode does not affect collision."

## Issue 7 — Stage-conflation: L2 planning depth's "plausible-but-wrong alternative" is a discovery-stage misstep (MODERATE)

**Checklist item potentially violated:** 18(d) stage-conflation guard
(`difficulty-rules.md` § 3 — "Reject if the named 'heuristic that
fails' or wrong-path argument is a discovery-stage misstep").

**Offending text (§4 → Level 2 → Difficulty justification (c)):**

> "Plausible-but-wrong alternative the post-discovery player considers
> and rejects: sliding the lantern FIRST (before collecting A and C)
> to cols 0–4 to shade col 6 immediately. Wrong because doing so
> lights col 2 (crystal A's column)..."

This is the right structural argument — but only AFTER Issue 5 is
fixed (col-2 pillar removed). With the col-2 pillar removed, the
"slide-first lights col 2" claim becomes valid post-discovery. With
the pillar in place, sliding-first does NOT light col 2 (still pillar-
shaded); the "wrong path" wouldn't be wrong.

So Issue 7 is **resolved by fixing Issue 5**. No additional change
needed beyond removing the col-2 pillar.

## Items that pass

For completeness, here is a pass on the rest of the checklist:

| # | Item | Verdict |
|---|---|---|
| 1 | Sprite palette in 0..15 plus -1 | PASS — verified each sprite (post Issue 4 fix). |
| 2 | Universal scaffold structure | PASS — spec describes file layout consistent with `universal-scaffold.md`; final verification at implement. |
| 3 | `available_actions` is subset of [1..7] | PASS — `[1, 2, 3, 4, 6]`. |
| 4 | Exactly 3 levels | PASS. |
| 5 | 4-char ID not in reserved list | PASS — `vp6h` not in 25 references or 17 priors; not English word. |
| 6 | Mechanics from `core-knowledge-priors.md` | PASS — objectness + geometry + topology, no other priors. |
| 7 | No letters/digits-as-glyphs/clipart/cultural | PASS conditional on Issue 4 fix (swap green for purple in crystal). |
| 8 | At least two distinct mechanics | PASS — M1, M2, M3. |
| 9 | L1 base dynamic system, reduced state, no on-screen text | PASS — 1 mechanic, 1 pillar, 1 crystal, fixed lantern, no text. |
| 10 | L2/L3 increase difficulty by composing mechanics | PASS — L2 = M1+M2 firing simultaneously; L3 = M1+M2+M3 firing simultaneously. |
| 11 | Mechanic inheritance and +1-or-+2 rule | PASS — N=1, N+1=2, +1=3. All carried forward. |
| 12 | Strict counterfactual necessity per mechanic | PASS conditional on Issue 5 fix. L1 M1 is borderline by the strict counterfactual reading (the witness only fires the gate's "shaded → pickup" branch; it does not fire the "lit → no-op" branch), but the gate IS triggered every time the avatar walks onto a crystal — interpretation matches reference-game L1 conventions where the single mechanic is "exercised by virtue of being the only mechanic." Acceptable. |
| 13 | Mechanic family absent from taxonomy | PASS — `shadow-cast-collect` not in taxonomy. |
| 14 | Mechanic family absent from prior-games index | PASS — not in 17 priors. |
| 15 | Distinguishing rule for similar entries | PASS — §9 articulates concrete rules vs lq5x, bx84, lf52, kn58, gv47, fz5j. |
| 16 | Win condition stated for the environment | PASS — `crystals_remaining == 0` per level → `next_level()` for each; final win after L3. |
| 17 | Lose condition (or "no lose" with reasoning) | PASS — `step_counter <= 0`. |
| 18 | Difficulty floor and ceiling per `difficulty-rules.md` | PASS conditional on Issue 5 fix (which restores L2's planning argument). L1 has "no strict planning requirement" per the rule. L2 names decision space (≥5 first-actions), wrong path (slide-first → A unsafe), witness reasoning chain (post-discovery). L3 names decision space (≥28 first-actions), trivial heuristic that fails (greedy-toward-target with reactive sliding incurs ~10-15 wasted actions), divergence (witness pre-positions both lanterns; greedy slides reactively after walk-onto-unsafe). L3 budget 120 is generous over witness 25 (4.8×). |

## Summary of required changes

When re-entering `write_spec`, the spec must:

1. (Blocking) Re-write L3 witness phase 4 to route around the col-13 bot-pillar via col 11. Update phase-4 action count from 10 to 11; update L3 total to **25 actions**.
2. (Minor) Fix L2 phase 1 action count from 3 to 2; update L2 total to **25 actions**.
3. (Minor) Fix L1 witness action count from 7 to 6.
4. (Minor) Swap crystal interior palette from 14 (green) to 15 (purple).
5. (Blocking) Remove the col-2 pillar from L2 layout to make M2's necessity grounded in ordering.
6. (Clarify) Add a note that pillars use `BlockingMode.PIXEL_PERFECT` (default) so blocking is unambiguous to the implementer.
7. (Resolved by 5) No separate change needed — Issue 7 follows from Issue 5.

Novelty re-check on the (revised) full spec is unchanged: against
lq5x, bx84, lf52, kn58, gv47, fz5j the distinguishing rules continue
to hold; the negative-similarity walk against lq5x's level_1.png
is unaffected (the layout changes don't alter the core inversion).
