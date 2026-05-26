# Critique revisions — round 1

Two issues found. Both are addressed in a single revision of
`mechanic-spec.md`.

## Issue 1 — L1 mechanic M2 (colour-pairing) is decoratively listed

**Checklist item violated**: 12 (strict counterfactual necessity / no
trivial fallback). The "decorative mechanic" anti-pattern in checklist
12's examples ("a 'redundant decorative' mechanic whose effect lands
on the same destination the base mechanic would have produced anyway")
applies to M2 at L1.

**Offending section** — spec §4 / Level 1 / "Mechanics required by the
witness":

> 2. **M2 — colour-pairing**. The win predicate compares each
>    block.colour against the target.colour at the block's resting
>    cell. Even though L1 has only one colour, the witness's release
>    must land block_red on target_red — exercising the colour
>    match.

The counterfactual the spec writes for M2 at L1 acknowledges the
problem ("with only one block in L1 the colour test is trivially
passed only because the lone delivery happens to match — no
'non-matching' trivial fallback exists in L1's geometry"). With only
one colour at L1, no plausible alternate strategy can fail the
colour comparison; the comparison is fired but its distinguishing
behaviour (a *failed* match) cannot be triggered by any L1 input
sequence. M2 is therefore decorative at L1.

**Fix**: Drop M2 from L1's mechanic list. Recount mechanics:

- L1 N = 1: just M1 (overhead-manipulator, the base dynamic system).
- L2 N+2 = 3: M1 (carried) + M2 (newly introduced — multi-colour now
  carries real weight) + M3 (rope-clearance-above-wall, newly
  introduced). +2 is allowed under checklist 11.
- L3 L2-count + 1 = 4: M1 + M2 + M3 (carried) + M4
  (gravity-stacking-disassembly).

Update §4 / Level 1 to list only M1, and rewrite the necessity
argument to focus exclusively on M1's three sub-verbs (trolley H,
hook V, grab/release). Remove the M2 row from L1's per-mechanic
counterfactual table. The L1 witness solution itself does NOT
change — it still places block_red at target_red — only the
mechanic-counting framing changes.

In §4 / Level 2's "Mechanics required by the witness" header, change
"N+1 = 3" to "N+2 = 3" and explicitly call out that BOTH M2 and M3
are newly introduced at L2.

In §4 / Level 3's "Mechanics required by the witness" header, change
"L2-count + 1 = 4" — already correct; keep as-is.

## Issue 2 — L2 witness action count miscounted

**Checklist item touched**: 18 (difficulty floor and ceiling — step
budget must be generous over the witness, not shrinking).

**Offending section** — spec §4 / Level 2 / "Witness solution":

> Total: 4+41+1+38+40+1 + 8+38+1+6+1 = 171 actions, shortest.

**Trace-recount**: 4 + 41 + 1 + 38 + 40 + 1 + 8 + 38 + 1 + 6 + 1 =
**179**, not 171. Off by 8.

**Fix**: Update the L2 witness header from "171 actions, shortest" to
"179 actions, shortest". Step budget 250 is still generous over
179 (1.4× rather than 1.5×), so the difficulty justification (d) does
not need to change. Update difficulty justification (a)'s exponent:
P(random win) ≤ 5⁻¹⁷⁹, not 5⁻¹⁷¹.

## Summary of edits required

1. §4 / Level 1: drop M2 from mechanic list; remove M2 row from
   counterfactual; update header `N = 2` → `N = 1`. The witness
   solution is unchanged.
2. §4 / Level 2: update header `N+1 = 3` → `N+2 = 3` and call out
   that both M2 and M3 are newly introduced; update witness count
   `171` → `179` (and `5⁻¹⁷¹` → `5⁻¹⁷⁹` in difficulty justification).
3. §4 / Level 3: no edits needed (already L2-count + 1 = 4).

Functionally the gameplay, sprite roster, action mapping, win/lose
conditions, and witness sequences are unchanged.
