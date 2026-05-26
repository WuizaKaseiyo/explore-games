# critique-revisions — Run #01, critique pass #1

Reviewed `mechanic-spec.md` against `design-constraints/checklist.md`
(16 items) and `mechanic-novelty/similarity-check.md` (re-run on
the full spec, with deep-analysis verification for the 4 near-miss
taxonomy entries).

Results: **12 of 16 checklist items pass cleanly**; **3 items have
issues**; **1 item passes with a clarification request**. Novelty
verdict still NOVEL after re-checking against the deep-analyses,
but two sprite shapes need adjustment to clear forbidden-elements
ambiguity.

Issues are listed in revision-priority order. Each entry follows
`(a) which check / rule, (b) the offending spec section + quote,
(c) concrete fix`.

---

## Issue 1 — sprite shape for `qmjvbnpkrt` (target pad) silhouettes "0"

(a) `design-constraints/checklist.md` item 7 — "Does the game
contain NO letters, NO digits-as-glyphs, NO real-world clipart, NO
cultural conventions (see `forbidden-elements.md`)?".
`forbidden-elements.md` says "ABSTRACT shapes resembling
letters/objects are OK only if they are not RECOGNISABLE as the
language/object."

(b) `mechanic-spec.md` §3 sprite roster, target pad
`qmjvbnpkrt.pixels`:
```
[8, 8, 8],
[8, -1, 8],
[8, 8, 8],
```
A 3×3 hollow ring with a single transparent centre — exactly the
3×3 silhouette that reads as the digit "0" (or the letter "O").

(c) **Fix.** Replace with a 3×3 *diamond-cross* — four pixels at
the edge midpoints, four transparent corners, transparent centre:
```
[-1,  c, -1],
[ c, -1,  c],
[-1,  c, -1],
```
A clearly topological "4-fold rotation" silhouette that no
character set encodes. The pawn lands on the (1, 1) centre cell;
the four solid edge-midpoint pixels frame the pawn without
overlapping it. Recoloured per instance via `color_remap(None, c)`
where `c ∈ {8 red, 9 blue, 11 yellow}`.

Precedent: sb26's `vgszefyyyp` 6×6 hollow frame passed studio
review, but is too large for our 3-cell-resolution placement; the
diamond-cross at 3×3 is the smallest digit-safe topological frame.

## Issue 2 — sprite shape for `xbjhuofwzg` (cycler pad) reads as "L" / "⌐"

(a) Same as Issue 1 — `forbidden-elements.md` ambiguity.

(b) `mechanic-spec.md` §3, cycler pad
`xbjhuofwzg.pixels`:
```
[c, c, c],
[c, c, -1],
[c, c, c],
```
A 3×3 filled square missing the right-middle cell. Depending on
rotation this silhouettes as a `⌐`, an `L` corner, or a poorly-
drawn arrow. Marginal but flaggable.

(c) **Fix.** Replace with a 3×3 *solid filled square* — no
asymmetry:
```
[c, c, c],
[c, c, c],
[c, c, c],
```
Distinguishable from the diamond-cross target (Issue 1's fix) by
shape (solid vs. spaced) and by the lack of a transparent centre.
The pawn walks onto one of the 9 cells; trigger semantics use
`level.get_sprite_at(x, y, tag="cycler")` to detect any
intersection. Set `BlockingMode.NOT_BLOCKED` so the pawn occupies
the cycler cell visually on top.

## Issue 3 — cycler semantics drift between L2 and L3

(a) `design-constraints/checklist.md` items 8, 10 + general spec-
drift criterion in `critique_spec.md` ("Spec drifted: level 2 or
level 3 introduces a mechanic that is now too similar [to itself
in a different form]").

(b) `mechanic-spec.md` §4, L2 spec says: "the cycler at L2 is a
**direct cycler** that sets the stepping pawn's colour to its own
colour immediately (red→blue in one visit), not a 3-step cycle";
L3 spec says "Two cycler pads, each set to a *different*
destination colour … (yellow → red), … (yellow → blue)" — implying
a 3-colour-alphabet cycler that advances one notch per visit. Two
distinct cycler semantics in the same game is a hidden second
mechanic the player must reverse-engineer; it's also avoidable.

(c) **Fix.** Unify cycler semantics to **direct colour-set across
both levels**: walking the active pawn onto a cycler pad whose
visible colour is `c_pad` sets the active pawn's body colour to
`c_pad` (single visit; idempotent on a second visit). Replace the
L3 description's "yellow → red" / "yellow → blue" cyclic-arrow
language with "red cycler (sets to red)" / "blue cycler (sets to
blue)". The pawn's starting colour at L3 (currently both yellow)
should change accordingly: pawns start red and blue but are
geometrically blocked from reaching their *matching* targets
without first cycling through the OTHER pawn's colour and back.
Adjust the L3 maze layout in §4 to enforce this.

The family-tag `tether-pawn-cycle` remains accurate ("cycle" =
"the moment-of-walk colour change") and the §9 distinguishing
rule against `ls20` (which uses 1-notch advance through a fixed
alphabet) becomes *stronger*: kf42's cycler is a destination-
setter, not an alphabet-walker.

## Issue 4 — `_get_hidden_state` encoding under-specified

(a) `design-constraints/checklist.md` does not directly require
this, but `code/novaengine-api.md` ("`_get_hidden_state() ->
np.ndarray` — debug hook; return any internal state worth
exposing") + the §3.5.2 graph-identity invariant from
`from-tech-report.md` ("Two states that render to the same frame
but have different hidden state are distinct nodes") make it
load-bearing. The spec under-specifies its layout.

(b) `mechanic-spec.md` §6: "Returns a `(2, 2) np.int16` array
encoding `(active_pawn_index, remaining_steps)` plus the two pawn
colours."

(c) **Fix.** Specify the layout explicitly:
```
[[active_pawn_index,   remaining_steps],
 [pawn[0].colour,      pawn[1].colour]]
```
Where `active_pawn_index ∈ {-1, 0, 1}` (-1 before the first
selection). All four entries are int16-safe. This makes the
debug-hook output deterministic and re-greppable.

## Issue 5 — Win-condition edge case (both pawns on the same pad)

(a) `design-constraints/checklist.md` item 14 — "Has the spec
stated the win condition for the environment as a whole?" — passes
in spirit but the per-level predicate has an edge case worth
specifying.

(b) `mechanic-spec.md` §7: "the pawn-to-pad assignment is determined
by position. If both pawns occupy *the same* pad … the predicate
fails because the second pawn has no remaining target."

(c) **Fix.** Strengthen the predicate so it is unambiguous:

```
WIN <=> ∃ a bijection f: pawns → target_pads s.t.
        for each pawn p:
            (p.x, p.y) == f(p).centre AND p.colour == f(p).colour
```

Concretely: a level has exactly two target pads with distinct
centre cells; both pawns must occupy distinct pad centres; both
colour-matches must hold simultaneously. Any state in which the
two pawns occupy the same cell automatically fails the predicate.

---

## Items confirmed PASS (12 + 1 with clarification)

| # | check | result |
|---|---|---|
| 1 | palette 0..15 + -1 | ✅ |
| 2 | universal scaffold | ✅ (verified at §3, §6, §spec-template) |
| 3 | available_actions ⊂ [1..7] | ✅ ([1, 2, 3, 4, 6]) |
| 4 | exactly 3 levels with composition arc | ✅ |
| 5 | 4-char ID, lowercase, alphanumeric, not reserved, not in prior-games | ✅ (kf42) |
| 6 | priors only from 4 categories | ✅ (objectness + geometry/topology + physics) |
| 7 | no letters/digits/clipart | ❌ Issues 1 + 2 |
| 8 | ≥2 distinct mechanics | ✅ (tether + cycler) |
| 9 | L1 tutorial: primary mechanic alone | ✅ |
| 10 | composition not size-scaling | ✅ — but Issue 3 weakens this if not fixed |
| 11 | family absent from taxonomy | ✅ (re-checked deep-analyses for m0r0, r11l, sk48, ls20) |
| 12 | family absent from prior-games | ✅ (empty) |
| 13 | distinguishing rule articulated | ✅ |
| 14 | win condition stated | ✅ — but Issue 5 strengthens it |
| 15 | lose condition stated | ✅ |
| 16 | L1 human-strategy stated | ✅ ("click red, RIGHT × 7, click blue, RIGHT × 3") |

---

## Verdict

**Loop back to `write_spec`.** Issues 1, 2, 3 are the substantive
fixes (forbidden-element ambiguity ×2 + cycler-semantics drift);
Issues 4 and 5 are clarifications. All five fit into a focused
revision pass without re-architecting the mechanic. Visit count to
`critique_spec` after this loop will be 2/5 (well within the cap).
