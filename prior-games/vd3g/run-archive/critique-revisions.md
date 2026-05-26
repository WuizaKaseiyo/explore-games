# Critique revisions for vd3g spec

The spec largely passes the §3.4 checklist; the issues below are the
concrete revision triggers.

## Issue 1 — L2 wall layout has a row-1 escape

**Checklist item violated:** Item 12 (strict counterfactual necessity).
The L2 wall column was specified as "vertical bar in column 7 from
row 2 to row 14, with one gap at (7, 8)". Row 1 of column 7 is
NOT in that range, so cell (7, 1) is a normal HIGH cell, not a wall.

**Offending spec section + quote:**
> "WALL: outer ring + a vertical bar in column 7 from row 2 to row
> 14, with one gap at (7, 8). 60 + 13 − 1 = 72 wall cells."

**Why this is a problem:** A trivial fallback exists — the player can
route the marble through row 1 (a 1-cell-wide corridor between the
outer-ring wall at row 0 and the col-7 wall starting at row 2) by
digging a path (3,3) → (3,2) → (3,1) → (4,1) → ... → (12,1) → (12,2)
→ ... → (12,4). This path bypasses the (7, 8) gap entirely, so the
walls mechanic at row 8 is never exercised by an alternate witness.
That violates strict counterfactual necessity for M2.

**Concrete fix:** Extend the wall column to cover row 1 of column 7.
Specifically: walls in column 7 from row 1 to row 14, with the
single gap at (7, 8). Cell count: 60 (outer ring) + 14 (col 7 rows
1..14) − 1 (gap) = 73 wall cells.

After the fix, the only column-7 crossing between row 1 and row 14
is (7, 8), and rows 0 and 15 are outer-ring walls. The marble has
no row-1 (or row-15) escape.

## Issue 2 — L2 witness count needs re-derivation; planning depth justification needs to be honest

**Checklist item violated:** Item 18(c)(L2 planning depth) — the
current spec names a wrong-path that is actually a discovery-stage
misstep, not a post-discovery planning challenge.

**Offending spec section + quote:**
> "Plausible-but-wrong: clicking cells north of the marble first,
> intending to escape over the wall, then discovering the wall column
> extends from row 2 to row 14 with the only gap at row 8 — must
> reverse and head south."

**Why this is a problem:** A fully-informed (post-discovery) player
can READ the wall layout off the rendered frame (walls are visually
heavy black sprites). They would already know the gap is at row 8,
not consider going north. Per `difficulty-rules.md`'s stage-conflation
guard: *"Reject if the named 'heuristic that fails' or wrong-path
argument is a discovery-stage misstep — something a player only does
because they haven't yet understood the mechanic."*

**Concrete fix:** With the L2 layout being a single forced detour
(south-to-row-8, east-through-gap, north-to-row-4), L2 has only
modest post-discovery planning. The honest justification is:

- L2 has light planning depth: a fully-informed player's route is
  determined uniquely by the gap position. The "planning" amounts
  to comparing the marble's row (4) to the gap's row (8) and
  computing the L-shaped detour (4 cells south + 9 cells east + 4
  cells north).
- Plausible-but-wrong (post-discovery) alternative: trying to "race
  along the marble's row" by digging east first — even though the
  player KNOWS the wall blocks at (7, 4), they might mistakenly
  attempt to use the LOW-cell-as-passage idea and dig (4, 4),
  (5, 4), (6, 4), thinking the marble can wait at (6, 4) for a
  wall toggle they don't yet realise is impossible. The player
  wastes ~6 clicks before reversing. This IS post-discovery (the
  player understands the dig-and-roll mechanic but mis-applies it
  by assuming walls are toggleable).
- Witness reasoning chain: "wall column at col 7 has unique gap at
  row 8; target is at row 4 east of column 7; therefore detour
  south to row 8, east through gap, north to row 4". The player
  must look-ahead to verify the gap row before committing to a
  direction, and recognise that walls are visually distinct from
  HIGH cells (heavier black with no inner grey, vs HIGH's grey
  corners + lighter inner) — this distinction is the post-
  discovery information that drives the route.

(Also recompute the witness count after the row-1 wall fix: with
walls fully sealing column 7 from row 1 to row 14 except (7, 8),
the path is unchanged from the original spec — 17 transitions =
32 clicks. Step budget 50 still works (1.56× witness).)

## Issue 3 — L3 planning depth justification overstates "irrecoverably"

**Checklist item violated:** Item 18(c)(L3 planning depth) — the
existing language says the wrong heuristic "fails" but the
sequential approach actually still wins, just with 2 extra clicks.

**Offending spec section + quote:**
> "Greedy strategies that route RED first (the closer marble), use
> the anchor, then route BLUE separately, would hit the obvious
> problem: the anchor pair is a JOINT toggle — opening it for BLUE
> later requires another anchor click that ALSO re-flips (8, 6),
> pushing RED off if RED is still on it."

**Why this is a problem:** A trace of the sequential approach (route
RED through anchor first, click anchor twice for re-toggle, route
RED to target, then route BLUE to (9, 9), click anchor twice again,
route BLUE to target) totals 32 clicks vs the parallel witness's
30 clicks. Within the L3 step budget of 80, both approaches succeed.
The wrong heuristic isn't really "failed" — it's just slightly
slower. The current language ("pushing RED off if RED is still on
it") is also incorrect: by the time the player triggers the second
anchor pair to ferry BLUE, RED has already departed (8, 6) onto the
post-anchor row.

**Concrete fix:** Restate L3 planning depth honestly:

- L3 has moderate-but-not-extreme post-discovery planning. The
  challenge is **timing**: the witness saves 2 clicks by
  pre-positioning both marbles at HIGH cells adjacent to their
  respective anchors BEFORE clicking the anchor pair, so a single
  toggle ferries both marbles in one settling pass.
- A trivial post-discovery heuristic ("route the closer marble
  first, then handle the other") DOES still win within the 80-step
  budget — it costs ~32 clicks vs the witness's 30. So the heuristic
  doesn't "fail" categorically; it's sub-optimal by 2 actions.
- The post-discovery decision space is large (256 valid first cells)
  and the player must reason about which marble to pre-position
  first (priority order matters: RED settles before BLUE in the
  per-marble pass), but the planning depth is moderate, not
  challenging.

Acknowledge L3's planning depth is "moderate" rather than
"challenging even for an attentive human"; per
`difficulty-rules.md`'s spirit this is acceptable as long as the
planning IS post-discovery and does discriminate between strategies.

## Issue 4 — minor: §3 sprite roster understates marble role-symmetry

**Checklist item violated:** Item 21(2) — Identical visuals imply
shared or correlated roles.

**Offending spec section + quote:**
> "(L1 uses red only; L2 uses red only; L3 uses red and blue.)"

**Why this is mild:** RED marble at L1 and L2 has the same hue and
shape. Player at L1 learns "red marble goes to red ring". At L2,
red marble again. At L3, red marble plus blue marble. The role-
correlation is consistent: same-coloured marble seeks same-coloured
ring. ✓ (This is a pass, not a fail — but the spec should note the
intentional carry-forward visual identity to make item 21 explicit.)

**Concrete fix (optional):** Add a one-liner to §3 or §6 noting
that marble-hue ↔ target-ring-hue is a load-bearing visual pairing
across all three levels (the player learns it at L1 and applies at
L3 with no re-explanation).

## Summary

Four issues. Issues 1, 2, 3 require concrete spec edits. Issue 4
is a minor optional clarification. Bounce to write_spec for revision.

Pass / fail summary on remaining items 1-21:

- Item 1 (palette 0..15): PASS — every spec'd pixel value is in 0..15 or -1.
- Item 2 (universal scaffold): deferred — checked at implement.
- Item 3 (`available_actions` ⊂ [1..7]): PASS — `[6]`.
- Item 4 (exactly 3 levels): PASS.
- Item 5 (4-char ID, not in lists): PASS — `vd3g`, verified.
- Item 6 (core knowledge priors only): PASS — physics, objectness, topology.
- Item 7 (no forbidden elements): PASS — checked all sprite patterns; no digits/letters/clipart/conventions.
- Item 8 (≥ 2 mechanics): PASS — 3 mechanics across L1-L3.
- Item 9 (L1 tutorial with reduced state space, no on-screen text): PASS — small layout, single marble, no text.
- Item 10 (L2/L3 increase difficulty by composing every available mechanic): PASS — L3 witness exercises M1+M2+M3.
- Item 11 (mechanic inheritance and +1-or-+2): PASS — L1=1, L2=2, L3=3.
- Item 12 (strict counterfactual necessity): FAIL at L2 (Issue 1 above; row-1 escape).
- Item 13 (mechanic family absent from taxonomy): PASS — `valley-dig-roll` is novel.
- Item 14 (mechanic family absent from prior-games): PASS.
- Item 15 (concrete distinguishing rules vs near-misses): PASS — articulated for tg6w, kn58, kp9z, mr5q, ka59, m0r0, tu93.
- Item 16 (win condition stated): PASS — every marble on its target.
- Item 17 (lose condition stated): PASS — step counter to 0.
- Item 18 (difficulty floor/ceiling per level): PARTIAL — L1 PASS; L2 needs honest planning justification (Issue 2); L3 needs honest planning justification (Issue 3).
- Item 19 (no hidden state): PASS — heights, cell types, anchor links, marble positions, step counter all visible.
- Item 20 (no chunky low-res blocks): PASS — every cell type has internal 4×4 multi-palette pattern.
- Item 21 (UI teaches): PASS — every sprite role legible from its visual; cosmetic clarification suggested in Issue 4.

Negative similarity check (re-walked on the full spec): no prior shares
3+ dimensions with any single prior. Pass.

**Verdict:** REVISE. Bounce to write_spec to address Issues 1-3.
