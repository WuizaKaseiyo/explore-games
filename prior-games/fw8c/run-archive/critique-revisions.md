# Critique — revision 1

The spec **fails** on multiple checklist items. Adversarial review per
`critique_spec.md`. Issues numbered for revision tracking.

## Issue 1 — Checklist item 12 violated for L2 mechanic M3 (post-consume reset)

**Section quoted from spec §4 L2**:
> *"M3. L2 cannot be solved without triggering M3 because once `slot_pink`
> is consumed (carrier was state `{pink}` to match), the carrier needs to
> be in state `{orange, pink}` to consume `slot_magenta`. Without the
> post-consume reset, the carrier would already hold `{pink}` after
> `slot_pink` consume; walking to `pad_orange` adds orange → state
> `{orange, pink}` — same end state. So the reset's necessity is
> subtle here. ... M3 is WEAKLY-REQUIRED: it doesn't change the witness's
> success, but its absence would change other legal solution paths'
> validity."*

**Failure**: Per `checklist.md` item 12, "no sequence of actions may win
L within the step budget without triggering M's distinguishing behavior".
The spec EXPLICITLY ADMITS that the witness solves L2 with the same
end-state with-or-without M3. That means there exists a winning sequence
that does not require M3's distinguishing behavior — i.e., there is no
strict counterfactual necessity. **Item 12 fails for L2 M3.**

The spec also acknowledges the failure ("WEAKLY-REQUIRED"). Item 12
demands strict, not weak, necessity.

**Concrete fix**:
- **Option A (recommended)**: Drop M3 from L2's mechanic enumeration.
  L2 then has 2 mechanics: M1 (single-pigment delivery) + M2 (multi-pigment
  mixture-and-deliver). L1 had 1 → L2 has 2 → +1, which is within the
  +1-or-+2 rule (`composition-and-tutorial.md`). L3 then needs to introduce
  one or two new mechanics on top of the L2 set of 2.
- **Option B**: Engineer the L2 layout so the post-consume reset is
  STRICTLY counterfactually necessary — e.g., have `slot_magenta` be the
  FIRST slot the witness consumes, leaving the carrier holding `{O,P}`;
  then engineer a path to `slot_pink` that crosses pad_orange a SECOND
  time (still state `{O,P}` due to OR idempotence) but reaches slot_pink
  with state `{O,P}`. Without M3 reset, slot_pink demand `{P}` can
  never match. With M3 reset, the carrier becomes `{}` after slot_magenta
  consume, then can be re-filled to `{P}`. This makes M3 strictly
  necessary — but it also requires a layout where the magenta-first path
  is ALSO the only winning path (otherwise the alternative pink-first
  path again sidesteps M3). Hard to engineer; not recommended.

**Recommendation**: Take Option A. L2's mechanics: M1 + M2 only.

## Issue 2 — Checklist item 18 (d, L3) violated: greedy heuristic does not fail at L3

**Section quoted from spec §4 L3, difficulty justification (c)**:
> *"Heuristic action count: 7 (slot_orange) + 12 (slot_black after detour
> through 3 pads) + 8 (slot_purple) = 27. Witness is 29. Heuristic and
> witness both win, but with different cost orderings. The greedy
> heuristic actually wins slightly faster in this layout!"*

> *"CONCLUSION on L3 planning depth (c): Either the witness as written
> is suboptimal (the greedy heuristic finds a shorter path), OR L3's
> planning depth is shallow because greedy succeeds. ... the post-
> discovery planning depth at L3 is 'moderate' rather than 'challenging-
> even-for-attentive-human'. This fails `difficulty-rules.md` § 2c L3's
> strict reading and will likely be flagged in critique_spec. Revision
> will tighten this."*

**Failure**: Per `difficulty-rules.md` § 2c L3 "Greedy / monotone-
progress / follow-the-obvious-gradient strategies should not reliably
win." The spec's own analysis shows the greedy heuristic wins in 27
actions (faster than the witness 29). The L3 planning-depth gate is
not met. **Item 18 fails for L3 (c).**

The spec self-acknowledges the failure ("will likely be flagged").

**Concrete fix**: The root cause is that the pigment OR-accumulation
mechanic has NO subtractive operation, so adding more pigments is
strictly monotonic and cannot break the greedy-heuristic. To make
L3's planning genuinely require non-greedy reasoning, EITHER:

- **Option A**: Introduce a SUBTRACTIVE mechanic at L3. E.g., a "purge
  pad" that removes one specific pigment from the carrier. This adds
  state-space topology (the player can now reach any of the 8 carrier
  states from any other state, not just expand the set monotonically).
  Greedy nearest-slot then becomes non-trivial because picking up
  unwanted pigments in transit would mismatch the next desired slot
  unless purged.
- **Option B**: Introduce a PIGMENT-GATED DOOR at L3 (M3 = the door
  passability is gated by carrier's pigment-set match). The door
  forces the carrier to be in a specific state to cross. Then route
  topology forces the carrier to plan the mid-traverse state, not just
  the final delivery state. Concretely: place all desirable slots on
  the FAR side of a door demanding `{orange, pink}`. Carrier MUST be
  state `{O, P}` to cross, but on the other side may need state `{O}`
  for a slot — requires a clever pickup ORDER (cross with magenta,
  consume slot_magenta which clears carrier, then pickup pad_orange
  on the far side and consume slot_orange). Greedy heuristic that
  doesn't reason about door state will fail to cross.
- **Option C**: Introduce time-limited slots OR moveable obstacles
  that change reachability per turn. More complex; not recommended.

**Recommendation**: Take Option B (pigment-gated door). It composes
naturally with the existing M1 + M2 (carrier-state arithmetic) and
adds a topology gate that forces post-discovery planning beyond
greedy. Concretely:
- Replace L3's M4 (triple-pigment combination) with M3 = pigment-gated
  door. (Or keep M4 AND add M3 — but that's +2 over L2's 2 mechanics,
  which equals 4 = within the +1-or-+2 rule per `checklist.md` item 11.)

## Issue 3 — Checklist item 10 partially violated: L3 composition is weak

**Section quoted from spec §4 L3**:
> *"M4 — Triple-pigment combination (NEW). ... M4 is materially different
> from M2 because it requires a longer pad-pickup chain (3 distinct pad
> visits) AND it produces a mixture colour outside the 2-pad derived-
> colour outputs (palette 5 vs. {6, 14, 15})."*

**Failure**: Per `composition-and-tutorial.md` § "Difficulty through
composition", a level is genuinely harder than its predecessor only if
"its witness solution requires every mechanic available at that level
(the carried-forward ones plus the newly-introduced one or two)
INTERACTING TOGETHER". M4 (triple-pigment) is just M2 (multi-pigment
mixture) at higher cardinality. The "interacting" between M2 and M4 is
not meaningful — M4 IS M2 with a 3-element subset.

`reference-game-patterns.md` § Recurring anti-patterns explicitly flags
this as the canonical anti-pattern: "Single-mechanic difficulty
escalation. ... §3.4 names this as the canonical anti-pattern and the
harness's composition rule (`composition-and-tutorial.md`) forbids it.
Generated games MUST add one *new* mechanic per level and require
composition in L3."

**Item 10 fails** because L1 → L2 → L3 progression scales from 1-pad to
2-pad to 3-pad pickup chains — that's "scaling a single mechanic", the
banned pattern. L2's M2 is genuinely new (the *act* of mixing produces
a colour not reachable from any single pad), but L3's M4 is just M2 at
N=3 instead of N=2.

**Concrete fix**: This dovetails with Issue 2's fix. Option B (pigment-
gated door) replaces M4 with a genuinely-different mechanic (door-
gating-by-state, not pigment-cardinality). The L3 witness then exercises:
- M1 (single-pigment delivery for some slot demanding 1 pigment).
- M2 (multi-pigment mixture for some slot demanding 2 pigments).
- M3 (door passability gated by carrier-state match).

These three INTERACT: the witness must arrange pigment pickups so that
the carrier's mid-route state matches BOTH the door's demand (M3) AND
the eventual slot's demand (M1 or M2). That's genuine composition.

## Issue 4 — Checklist item 7 borderline (cultural-color-mixing alignment)

**Section quoted from spec §3 mixing table**:
> *"orange+pink → magenta, orange+lightblue → green, pink+lightblue →
> purple, all three → black."*

**Failure (mild)**: Per `forbidden-elements.md`, "Cultural conventions"
are forbidden. The mapping in the table partially aligns with real-world
subtractive colour mixing intuition (e.g., pink + lightblue → purple
matches the mental model "warm + cool = purple-ish"). The spec
self-claims "deliberately NOT colour-theory-aligned" but the actual
mappings ARE recognisable to a player with grade-school colour-mixing
familiarity.

This is borderline. The spec text disclaims cultural alignment, but the
table mappings tell a different story. A player who has never seen the
table will likely guess pink+lightblue → purple correctly because of
real-world colour mixing intuition.

**Concrete fix (optional but recommended)**: Re-randomise the mixing
table outputs to reduce cultural alignment. E.g.,
- orange + pink → green (palette 14) instead of magenta
- orange + lightblue → purple (palette 15) instead of green
- pink + lightblue → magenta (palette 6) instead of purple
- all three → off-black (palette 4) — which is acceptable but the
  intuition "primary mix → black/dark" is cultural too

The mappings are arbitrary per the mechanic; deliberately scrambling
them reduces cultural shortcut. Mark this as a soft-fix, not a hard
rejection — `forbidden-elements.md`'s "Cultural conventions" is itself
a soft-edged rule and the spec's disclaimer is reasonable.

**Recommendation**: Apply this fix as part of revision; it's cheap
and removes ambiguity.

## Issue 5 — Witness step counts in §4 L1 mismatch (off-by-one accounting)

**Section quoted from spec §4 L1**:
> *"`[ACTION2, ACTION2, ACTION4, ACTION4, # (1,1) → (1,3) → (3,3) [pickup
> orange, state {O}] ACTION2, ACTION2, ACTION4, ACTION4, # (3,3) → (3,5)
> → (5,5) ACTION4] # (5,5) → (6,5) [deliver, slot consumed; level wins]
> Wait — recount: from (1,1) to (3,3) is right-2, down-2 = 4 steps; from
> (3,3) to (6,5) is right-3, down-2 = 5 steps. Total 9 steps."*

**Failure (minor)**: The spec contains an inline self-correction that
includes draft-text leftover ("Wait — recount") in the published spec.
This is a quality issue, not a hard checklist item failure. The corrected
witness IS coherent, but the un-deleted thinking-out-loud reads sloppily.

Same kind of leftover in §4 L2 ("OOPS — (2,3) is pad_orange. Need to
route around. Re-plan:") and L3 ("Honest concession: ...").

**Concrete fix**: In the revision, clean up these inline self-edits.
Provide ONE clean witness per level without the meta-narrative.

## Issue 6 — Spec §4 L3 witness route ambiguity

**Section quoted from spec §4 L3 Phase 3**:
> *"A18: ACTION3 → (5,5) (from (6,5) west) ... Layout walls amendment
> (clarifying for the witness): No interior walls in L3."*

**Failure (minor)**: The spec contradicts itself on whether L3 has
interior walls. Earlier in §4 L3 the spec proposed adding walls at
(4,5) and (4,6); later the witness assumes no interior walls. The
final witness uses no walls; the layout text should be cleaned up to
match.

**Concrete fix**: In the revision, commit to ONE final L3 layout
(probably no interior walls if the witness path doesn't need them, OR
add specific interior walls to enforce the door-gating in Issue 2's
fix).

## Items that PASS

For reference, these pass cleanly:

- Item 1 (palette 0..15): all sprites use values 0-15 + -1 transparency. ✅
- Item 3 (`available_actions ⊆ [1..7]`): `[1, 2, 3, 4]` is a subset. ✅
- Item 4 (exactly 3 levels): L1, L2, L3 enumerated. ✅
- Item 5 (4-char ID, novel): `fw8c` verified against 25 reference + 66
  prior. ✅
- Item 6 (mechanics from core-knowledge priors): objectness + topology
  per §2. ✅
- Item 7 sprite-glyphs: no letters / digits / clipart in any sprite
  pixel pattern (the carrier hollow body, pad concentric ring, slot
  thick rim, wall solid block are all abstract shapes). ✅ (the
  cultural-mixing concern is Issue 4 above, separately filed)
- Item 8 (≥ 2 distinct mechanics): M1 + M2 minimum, with M3 in L3
  after revision. ✅
- Item 9 (L1 tutorial): 1 mechanic (M1), small state space, no on-
  screen text. ✅
- Item 11 (mechanic inheritance, +1-or-+2): after revision per Issues
  1 + 3, L1=1, L2=2 (+1), L3=3 (+1). All within bounds. ✅
- Item 13 (mechanic family absent from taxonomy): pigment-mix-walk is
  not in the taxonomy. ✅
- Item 14 (mechanic family absent from prior-games): pigment-mix-walk
  is not in the prior-games index. ✅
- Item 15 (distinguishing rule for near-misses): articulated for ls20,
  hr8q, tm5x, pk4m, etc. in §9. ✅
- Item 16 (win condition): "every slot has been consumed". ✅
- Item 17 (lose condition): step counter at 0. ✅
- Item 18 (a) random-resistance: justified per-level. ✅
- Item 18 (b) human time: ~30 sec / 1.5 min / 3 min per L1/L2/L3.
  Roughly aligns with the ~2-min/level target. ✅
- Item 18 (d) step budget: 30 / 45 / 65, generous, non-shrinking. ✅
- Item 19 (no hidden state): carrier re-tints to current pigment
  mixture; slot replacement on consume; both visible. ✅
- Item 20 (don't generate low-resolution): grid 64×64, sprites 6×6
  with internal pattern (concentric rings, thick rims, hollow bodies),
  step size 8 → ~8 logical cells with rich rendered detail. ✅
- Item 21 (UI teaches): pad shape ≠ slot shape ≠ carrier shape;
  demanded colour visible on slot rim; pad pigment visible at pad
  centre; carrier state visible as carrier centre fill. ✅
- Item 22 (ACTION7 strict-undo or absent): absent. ✅

## Summary

**6 issues; 2 hard failures (items 12, 18(c)); 1 strong concern (item
10); 2 minor (items 7-borderline, 5/6 spec quality).**

Verdict: **REVISE.**

Transition: → `write_spec` (revision 2).
