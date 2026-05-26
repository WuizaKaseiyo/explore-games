# critique-revisions — pass 1 of `mechanic-spec.md`

## Verdict: REJECT — revisions required.

The spec has 3 substantive issues plus 2 lighter ones. The L3 design is broken at the strict-counterfactual gate (item 12) for the sticky-pad mechanic. L2 has a planning-depth claim that's admitted to be false. L1's necessity claim is technically OK but the wake mechanic isn't load-bearing in the L1 witness — the player could ignore the wake constraint at L1 because the witness path is monotone and never has wake within reach of any next move.

Below: numbered list of issues. Each gives (a) the violated rule, (b) the offending spec section + quote, (c) a concrete fix.

---

### 1. **Item 12 (strict counterfactual necessity) — L3 sticky-pad necessity is not demonstrated.**

**(a) Rule violated.** Per `checklist.md` item 12: *"for each mechanic M available at level L, no sequence of actions may win L within the step budget without triggering M's distinguishing behavior."* The critique must enumerate plausible alternates and concretely walk why each fails.

**(b) Offending section.** §4 Level 3 — "Necessity per mechanic" for `wake-sticky pad`:

> "*L3 cannot be solved without triggering 'wake-sticky pad' because: the corridor `(8, 8)` is exactly 1 cell wide and is the only path between the two chambers. To traverse it twice (south→north for the first collectible, then north→south to return), the avatar must pass over `(8, 8)` itself twice.*"

The spec then SELF-FLAGS this:

> "*'Don't traverse the corridor twice': the start and one collectible are in the SOUTH chamber, the other collectible is in the NORTH chamber → the corridor must be traversed at least once, and to return to a final state where both collectibles are consumed, at least once is enough. So actually traversing the corridor once is sufficient. Then sticky may not be required!*"

The current L3 layout requires only one corridor traversal (south→north and stop in NORTH chamber). After collecting the NORTH item, the avatar can wait for corridor wake to decay during chamber walking (~4 moves of distance ⇒ corridor wake decays naturally) and then return south through the corridor wake-free. **Sticky is not needed.**

**(c) Fix.** Redesign L3 so a critical wake-blocked move is unavoidable AND the only way around it is sticky. Concrete proposal: a **chimney** layout in the NORTH chamber. Specifically:

- NORTH chamber has a 1-cell-wide vertical chimney at column `c=8`, rows `r=3..7`, with walls at `(c=7, r=3..6)` and `(c=9, r=3..6)`. The chimney is open only at the top (row 3, the collectible cell) and bottom (row 7, the corridor cell).
- The collectible is at `(8, 3)` (top of chimney).
- The sticky pad is at `(8, 4)` (one cell south of the collectible, INSIDE the chimney).
- Step budget tuned so soft-lock detection fires if the avatar gets stuck in the chimney without sticky.

Witness: avatar climbs chimney `(8, 7) → (8, 6) → (8, 5) → (8, 4)` — at `(8, 4)` STEP ON STICKY (`sticky_pending = True`). Then `(8, 4) → (8, 3)` — vacated `(8, 4)` does NOT leave wake (sticky consumed). Collect. Now to descend: `(8, 3) → (8, 4)` — wake-free at `(8, 4)`, OK; ages on subsequent steps decay the column's earlier wake by the time the avatar reaches each cell. (Note: `(8, 5)` and `(8, 6)` will still have wake during the immediate-next-step, so the descent must actually wait in the open-bottom of the chimney for ages to decay, OR the chimney's geometry needs further tuning.)

Without sticky: at `(8, 3)` the avatar's only neighbour-not-wall is `(8, 4)`, which has age-1 wake from the just-completed step → step would lose. Soft-lock detector fires → LOSE before win predicate is met.

**The clearer mechanic must also be necessary at L3.** Solution for clearer-necessity: place the clearer pad NOT at `(8, 3)` (would short-circuit sticky) but in the SOUTH chamber on the path to the second collectible — say `(3, 9)` — and engineer the SOUTH chamber such that the path from corridor exit `(8, 9)` to the second SOUTH collectible at `(12, 12)` requires crossing wake created during the south-chamber traversal. *That path must be re-derived in the next `write_spec`; if it does not work out, drop sticky-via-chimney back to a single new mechanic and rework.*

---

### 2. **Item 18 (difficulty floor and ceiling) — L2 planning-depth wrong-path argument is broken.**

**(a) Rule violated.** Per `difficulty-rules.md` § 2c (L2 sub-bullet 2) and § 3 (critique-check L2): the spec must "name at least one plausible-but-wrong alternative the post-discovery player would consider and reject" AND demonstrate the wrong path actually fails.

**(b) Offending section.** §4 Level 2 — Difficulty justification (c):

> "*Plausible-but-wrong alternative the post-discovery player must reject: enter the spiral first, then exit and collect (2, 14) second. This wrong path is rejected because: after exiting the spiral, the wake-clearer is consumed; on the way back to (2, 14) the avatar's wake (now tracked from the spiral exit) is small enough to allow safe routing — so this wrong path actually also succeeds. Reformulate*"

The spec admits the alternative does not actually fail. **L2 (c) is unmet.**

**(c) Fix.** Engineer a real wrong path. Concrete proposal: place the OUTER `(2, 14)` collectible behind a tight corner where reaching it after exiting the spiral requires the wake-clearer (because the spiral-exit wake plus the corner-approach wake combine to block the only entrance). Then the wrong path "spiral first, then `(2, 14)`" fails because the clearer was consumed inside the spiral and the corner is impassable without it. The witness reverses the order: `(2, 14)` FIRST (no clearer needed because no spiral-trapping yet), then spiral with the clearer at the centre. The wrong-path argument becomes: "*greedy 'collect the visible spiral first because it dominates the screen' loses access to `(2, 14)` because the only path to `(2, 14)` requires a wake-clearer the player no longer has.*"

Alternative simpler fix: remove the `(2, 14)` collectible entirely; L2 has only the spiral-centre collectible + clearer. Then L2's planning-depth bullet rests on "the post-discovery player must enter the spiral and use the clearer at the right moment". That's a single-decision-point puzzle which is L1-level planning. **Better to keep the second collectible and fix the layout per the proposal above.**

---

### 3. **Item 18 (difficulty) — L3 planning-depth heuristic-vs-witness divergence not precisely traced.**

**(a) Rule violated.** Per `difficulty-rules.md` § 2c L3 sub-bullet 3: *"Show where the heuristic diverges from the witness in 2-3 sentences: at which step the heuristic and the witness disagree, and why the heuristic's choice irrecoverably loses or significantly delays the win."*

**(b) Offending section.** §4 Level 3 — Difficulty justification (c):

> "*The greedy heuristic and the witness diverge at the very first move (witness: ACTION4 east to set up sticky-then-corridor; greedy: ACTION4 east to start the south-collect path) — both look similar, but the witness arrives at sticky first, then corridor; greedy walks past sticky toward south item.*"

This is hand-wavy. Both first moves are ACTION4 east. The "divergence" is several moves later. The argument doesn't trace concretely WHICH MOVE differs and WHY greedy loses.

**(c) Fix.** After fixing issue 1 (chimney layout), re-derive the greedy-trace concretely: from `(3, 12)`, greedy heads east-and-north toward the visible chimney collectible at `(8, 3)` because it's the most "demanding-looking" target. Greedy arrives at the chimney bottom `(8, 7)`, climbs `(8, 6) → (8, 5) → (8, 4) → (8, 3)`, leaving wake at `(8, 6), (8, 5), (8, 4)` (ages 3, 2, 1 at the moment of collection). Greedy then tries to descend `(8, 3) → (8, 4)` — `(8, 4)` is age-1 wake → loses. The witness defeats greedy by stepping on the sticky pad at `(8, 4)` mid-climb so vacated `(8, 4)` doesn't leave wake — concretely, greedy never noticed the sticky pad existed until it was a click-too-late.

---

### 4. **Item 12 — L1 wake mechanic is not load-bearing in the witness.**

**(a) Rule violated.** Item 12's spirit (and `difficulty-rules.md` § 1's "every level must EXERCISE every mechanic"). The L1 witness path goes (3,4) → east → (12,4) → south → (12,12) → west → (3,12). It is monotone and the wake constraint never gates a single decision in this path — the avatar's age-1/2/3 wake is always behind it (in the direction it just came from), and the avatar is moving away from it. The mechanic is *present* (every move creates wake) but not *load-bearing* (the wake mask never shrinks the chosen action set).

**(b) Offending section.** §4 Level 1 — entire witness solution.

**(c) Fix.** Redesign L1 to FORCE at least one wake-aware decision in the witness. Two options:

- **Option A** (simpler): make the L1 layout a corridor where the avatar enters, collects, and must exit, with the corridor's interior 4+ cells deep (so on exit the entrance-wake has decayed but the most-recent 3 cells are wake). The witness must pick a wake-respecting path back. Specifically: a 6-cell-deep dead-end corridor with the collectible at the dead end. The avatar walks 6 cells in, collects, walks 6 cells back. By move 4 of the return trip, the wake from move 1 has decayed; before that, wake blocks. The witness must respect wake during the return.
- **Option B** (richer): two collectibles arranged so that after collecting the first the avatar must reverse direction and go past the start cell — but the start cell still has wake age 1/2/3 — so the avatar must take a 1-cell detour around it. This forces wake-engagement.

Either fix makes wake load-bearing in L1's witness without forcing the player to LOSE during normal play.

---

### 5. **Item 12 — L2 spiral-centre clearer/collectible single-cell duplication is unverified.**

**(a) Rule violated.** Item 12 is satisfied per the spec's argument, but the LAYOUT detail "the clearer pad and collectible are at the same cell `(8, 8)` and trigger together on overlap" is implementation-fragile and the spec doesn't specify what happens IF the avatar enters the cell from a wake-blocked direction (i.e., what if the spiral's wake at `(8, 9)` exit is lethal AND the only neighbours are wake → soft-lock at the entry cell).

**(b) Offending section.** §4 Level 2 layout:

> "*One **`clearer_pad`** at `(8, 8)` (the spiral's centre). One **`collectible`** at `(8, 8)`*"

**(c) Fix.** The same-cell co-location is fine semantically, but the spec must say what happens at the cell — specifically: BOTH effects fire on the entering step (collectible REMOVED, clearer fires erasing all wake, clearer pad REMOVED). And the spec must verify the spiral's geometry actually requires the avatar to reach `(8, 8)` BEFORE the surrounding wake becomes lethal — i.e. the avatar walks the inward corridor and arrives at the centre exactly as their tail wake is about to overlap them, the clearer fires JUST IN TIME. Re-derive in the rewrite.

---

### Lighter issues (to address opportunistically, not blocking on their own)

- **L1 step-budget = 60 vs witness = 27** — fine, ~2.2× witness, generous. No issue.
- **L2 step-budget = 80 vs witness ≈ 57** — 1.4× witness. The spec § 2(d) L2 addendum says "*a first-time player will spend several actions discovering what the new mechanic does before they can attempt the witness*". 23 extra actions is OK for clearer-pad discovery but check the spiral entrance distance allows recovery from a wrong inward turn.
- **No-hidden-state cue for `sticky_pending`** — spec mentions a "1-pixel purple halo" overlay sprite. Make sure the halo sprite is declared in the sprite roster (currently it's mentioned only in §6 narrative). Add to §3.

---

## Visit count
This is critique_spec visit #1 of 10.
