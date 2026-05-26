# Negative similarity check — looking for "too much in common"

The companion file `similarity-check.md` describes a *positive* novelty
test: "can you articulate concrete distinguishing rules against any
near-miss?". That test is necessary but not sufficient. A defensive
distinguishing-rule paragraph can be technically correct and the
candidate can still feel like a near-clone of a prior game.

This file describes the **negative** test the agent must also run
before settling on a mechanic. Run it during `pick_mechanic` and
re-run it during `critique_spec`. It uses qualitative judgement, not
numeric scoring — novelty is hard to measure, and any classifier
that bins the 25 reference games into N families will incorrectly
say two genuinely-distinct reference games are "the same kind of
game". Trust the eye and the spec, not a fingerprint table.

## Three principles

1. **Pixel-level detail richness.** Avoid having just a few big blocks moving around on an empty field.
2. **Palette diversity.** Reach for a different dominant palette from every prior; do not let two consecutive games share the same look.
3. **Core dynamic divergence.** Find a fundamentally different "what is the player thinking about while they play?" — not the same dynamic with marginal, incremental novelty on small components.

## The cautionary tale

Two consecutive autonomous runs of this harness produced these
priors in `prior-games/index.md`:

- **kf42** — *tether-pawn-cycle*: two pawns share a max-distance
  tether; click selects, arrows step, walking onto a coloured pad
  re-tints the active pawn.
- **vh68** — *colour-group-shift*: clicking a pawn picks its colour
  as the active colour; arrow keys translate every same-coloured
  pawn one cell in parallel; from L2, walls are passable to
  matching colours only.

`pick_mechanic`'s positive similarity check defended vh68's novelty
in seven paragraphs of distinguishing rules against kf42, vc33,
lp85, cn04, ka59, m0r0, dc22 and ls20. Each rule was factually
correct: vh68's verb cardinality is N-pawns vs kf42's one-pawn,
vh68 has no tether, vh68 has no re-tint pads, etc. By the rules of
`similarity-check.md`, vh68 was novel.

The user's reaction on first sight: *"the game vh68 is super
similar to game kf42"*. And they were right. The positive test had
optimised for "can the agent argue that the candidate is novel?"
rather than for "would a player perceive these as different
games?". The two games shared all of the following:

- Multiple coloured pawn-blocks scattered on a small (12-16
  cell) walled grid.
- Click-to-select then arrow-keys-to-move as the input pattern.
- The same dominant palette (`{4 wall, 8 red, 9 blue}` plus the
  HUD colour). No other palette values in serious use.
- Coloured target tiles where pawns must land.
- Step-counter HUD as the lose trigger.
- Sprites that are mostly 1×1, 2×2, or 3×3 plain rectangles
  with no internal pattern.

That is far too many shared surface features. No verb-cardinality
distinguishing rule can rescue a candidate that visually IS the
prior game in a different costume.

## The test itself

When evaluating a candidate, do NOT ask "what distinguishes this
from each prior?". Instead, open the candidate's mental rendering
of L1 alongside **the rendered initial frames of every relevant
existing game**, and ask the *opposite* question:

> What does the candidate share with this game?

The two image corpora to compare against — both must be opened, not
just read about:

- **Every prior in `prior-games/index.md`**: open
  `prior-games/<id>/run-archive/smoke-frames/level_1.png`
  (and `level_2.png`, `level_3.png` if the comparison needs them).
- **Every taxonomy near-miss flagged by the positive
  `similarity-check.md` pass**, plus any reference game whose
  surface signature could resemble the candidate even when the
  positive check did not flag it: open
  `deep-analysis-3lvls/<id>/level_1.png`
  (and `level_2.png`, `level_3.png` if needed).

Looking at the actual rendered images is mandatory at this step.
The visual signature (palette, sprite grain, density) is one of the
named principles and cannot be judged from text alone.

Walk the dimensions below and count them as shared when the answer
is "essentially the same":

1. **What is on the board.** Object-moving-on-a-grid? A canvas
   being painted? A row of cards being cycled? Tapes? Buttons? A
   scrolling runway?
2. **What the player physically does on input.** Walks an avatar?
   Selects-then-moves? Clicks to stamp? Cycles a card? Slides a
   row? Programmes a sequence?
3. **What the level is asking for.** Cover every target? Match a
   reference image? Spell a sequence? Collect a recipe? Reach a
   goal cell? Pair every glyph?
4. **What kills the player.** Step budget? Hazard contact? Chaser
   catch? Attempt budget? Decoration only?
5. **The cast of supporting elements.** Walls + targets is too
   universal to count alone. *Coloured-pawn-blocks plus same-
   coloured-target-tiles* is specific and counts.
6. **Visible visual signature** (Principle 2 above).
7. **Pixel grain of primary sprites** (Principle 1 above).
8. **The core dynamic** (Principle 3 above).

If the candidate shares **three or more** of these dimensions with
a single prior, stop. That is too much overlap, no matter what the
distinguishing-rule paragraph says. Reject and pick something that
diverges on more axes. The threshold is judgement, not arithmetic
— sharing on dimensions 6, 7, or 8 is heavier than sharing on the
others, because those are the named principles.

## How to apply

1. **At `pick_mechanic`**, after drafting the candidate's one-
   paragraph mechanic description, mentally render L1 and walk the
   eight dimensions above against every prior's
   `level_1.png`. Reject if any single prior overlaps on 3+
   dimensions. When rejecting, reach for divergence on the
   coarsest axis (e.g. swap "multi-pawn-on-a-grid" for "no pawns
   at all — a canvas being painted"), not for an extra cosmetic
   tweak.
2. **At `critique_spec`**, re-walk the test against the now-
   fleshed-out spec. A candidate clean at pick-time can drift
   into too-much-overlap by L2 or L3.
3. **Articulate refusals concretely.** When this check rejects
   a candidate, list the specific shared dimensions in
   `mechanic-pick.md` (or the critique document), naming the
   prior. That makes the next draft start in a substantively
   different place.
