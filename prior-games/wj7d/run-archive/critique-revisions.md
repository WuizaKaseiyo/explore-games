# Critique revisions for `mechanic-spec.md` (visit #1)

## Issue 1 — L2 difficulty depth (checklist item 18, difficulty-rules.md § 3.d, stage-conflation guard)

**Where.** § 4 → "Level 2 — base system + 1 new mechanic" → Difficulty
justification → (c) Planning depth → "Plausible-but-wrong alternative".

**Quote (offending text).** *"The post-discovery player might click
red and immediately ACTION5 to 'save planning effort' — this is an
obvious wrong action because they already know red is at (8, 4) and
the shadow at (24, 50) is not at (8, 58)."*

**Violation.** This is a discovery-stage misstep, not a post-discovery
failure. A fully-informed player who knows reflection across row 31
maps (8, 4) to (8, 58) would never try the immediate-fold action;
they already know the reflection rule. `difficulty-rules.md` § 3
"Stage-conflation guard" rejects this kind of wrong-path argument.

**Fix.** Restructure L2's level layout so that the *order of folds*
matters post-discovery. Specifically, place blue at a cell that
geometrically obstructs red's path-or-destination, so a fully-
informed player who picks "fold red first" runs into a concrete
collision (blue's body blocks red's destination cell), and must
revise the plan to "fold blue first to clear, then fold red". This
also pulls L2's witness reasoning chain closer to a genuine
sequencing decision, not just two independent placements.

Concrete suggestion: shift red's destination from (24, 12) to
(24, 20) and shift blue's level-1 starting position to (24, 24)
(or equivalently shift blue's body so its 6×6 footprint at rows
24..29 overlaps with red's 6×6 footprint at rows 20..25). Update
witness, counterfactuals, and step budget accordingly. Add a
collision-with-other-stamps movement guard to the action mapping
(item 5).

## Issue 2 — L3 difficulty depth (checklist item 18, difficulty-rules.md § 3.d, stage-conflation guard)

**Where.** § 4 → "Level 3 — system + 2 new mechanics" → Difficulty
justification → (c) Planning depth → "Trivial heuristic that fails".

**Quote (offending text).** *"'Greedy: fold each stamp using the
default H crease at row 31.' Fold blue first → reflection misses
... → lose. OR: 'Fold blue with H crease moved to row 27 (correct),
then fold red with that same H crease at row 27' → red reflection
keeps x=12 ≠ shadow x=48 → lose."*

**Violation.** Both alternatives are discovery-stage missteps —
a fully-informed player who knows `H crease preserves X` and knows
red shadow is at x=48 ≠ stamp x=12 already knows this approach
fails before trying it. The stage-conflation guard rejects this.

**Fix.** Replace the heuristic with a genuine post-discovery
planning failure mode: re-orient-by-click-anywhere. Concretely:
the crease re-orient pivots at the click cell; a fully-informed
player who knows the *mechanic* but not the *planning subtlety*
might re-orient by clicking the most convenient crease cell (e.g.,
the leftmost cell of the H crease at row 27, near the player's
mental "click here to flip orientation"). The V crease then ends
up at the wrong column (col=4 instead of col=30), and red's fold
across col=4 lands at x=−4 (off-grid) → fold contributes nothing
to the red shadow → red consumed → lose. The witness requires the
player to *plan* the click cell: V crease must be at col=30 because
(stamp_x + shadow_x) / 2 = (12 + 48) / 2 = 30; the click for
re-orient must be at col=30 specifically, not anywhere convenient.

Update L3's (c) Planning depth → name this as the trivial heuristic
that fails, show where it diverges from the witness (at the
re-orient click step).

## Issue 3 — minor: per-level `data` dict not explicit

**Where.** § 4 lacks an explicit per-level `data` dict listing.

**Violation.** Non-fatal, but the spec uses phrases like
`crease_movable=False` without listing the full per-level
`level.data` keys. `composition-and-tutorial.md` says per-level
configurations may differ; the spec should make those explicit so
the implementation phase can directly translate them.

**Fix.** Append to § 4 a small per-level `data` dict block:
```
L1: data = {"step_budget": 30, "crease_movable": False,
            "crease_orient": "H", "crease_pos": 31,
            "auto_select_stamp": "stamp_red_cross"}
L2: data = {"step_budget": 50, "crease_movable": False,
            "crease_orient": "H", "crease_pos": 31,
            "auto_select_stamp": None}
L3: data = {"step_budget": 50, "crease_movable": True,
            "crease_orient": "H", "crease_pos": 31,
            "auto_select_stamp": None}
```
