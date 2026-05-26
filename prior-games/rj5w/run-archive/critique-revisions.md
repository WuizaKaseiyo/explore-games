# Critique revisions — round 1

`mechanic-spec.md` for `rj5w` has issues that block transition to
`implement`. Fix and rewrite.

## Issue 1 (BLOCKER) — checklist item 12 violation at L3
M4 (wall-anchored reflection) is **not counterfactually required**
in the L3 witness as currently specified.

**Where**: § Level 3 — *Necessity per mechanic* — bullet for M4.

**Quote**: *"Without the walls at (36, 28) and (28, 36), the V-fold
at F_v=32 would move yellow to (36, 28) and the H-fold at F_h=32
would move yellow to (28, 36) — both off-target. The win condition
'every pawn on its target' would then fail at the end of any fold
sequence that fires both V and H."*

**Why it's wrong**: the witness fires V-fold **twice** at F_v=32
(once to land green on its target, once to undo purple's
V-displacement). Trace WITHOUT the walls:

- V-fold-1 at F_v=32: yellow (28,28) → (36,28). Not target. No lock.
- V-fold-2 at F_v=32: yellow (36,28) → **(28,28) = target. LOCK.**
- click H, H-fold at F_h=32: yellow LOCKED, stays.

The double-V-fold structure naturally bounces yellow back to its
starting cell on the second V-fold — and that cell is yellow's
target. M5 (lock) then keeps yellow there through the H-fold. So
the witness wins WITHOUT the walls. M4 is redundant with M5 in
this layout.

This is exactly the "redundant decorative mechanic" anti-pattern
flagged in checklist item 12 ("a 'redundant decorative' mechanic
whose effect lands on the same destination the base mechanic would
have produced anyway").

**How to fix**: two options.

- **Option A (preferred — simpler)**: drop walls from L3 and reduce
  L3 to **+1 new mechanic (lock-on-target only)**. The L1/L2/L3
  count rule (`composition-and-tutorial.md` § Exactly 3 levels)
  allows L3 to introduce 1 OR 2 new mechanics; +1 is fine. Re-tune
  yellow's setup so the lock mechanic is plainly exercised — for
  example move yellow's target to (36, 28) so the V-fold AT F_v=32
  lands yellow exactly on its target, locking it on the spot, and
  the lock mechanic is now visibly active across all three pawns
  (green, purple, yellow each lock on a fold).

- **Option B (more complex)**: redesign L3 so walls are strictly
  necessary by adding a fold sequence in the witness that does NOT
  bounce yellow back via the lock-mechanic / double-V-fold
  cancellation. Concretely, this would require an ODD number of
  V-folds (or H-folds) in the witness for one pawn while yellow
  must stay in place — which would cascade into a much more
  complex L3. Not recommended given Option A is simpler and still
  satisfies item 11 (+1 is allowed).

Pick Option A unless there's a strong reason to keep walls.

## Issue 2 — L2 planning-depth wrong-alternative is shaky

**Where**: § Level 2 — *Difficulty justification* — bullet (c)
plausible-but-wrong alternative.

**Quote**: *"'commit V at F_v=30 immediately' — a fully-informed
player might trust the initial axis position. This fails because
green at (8,8) reflects to (52, 8), not (56, 8), and a subsequent
H-fold cannot recover the missing 4-column drift."*

**Why it's weak**: per `difficulty-rules.md` § 3 — "Stage-conflation
guard" — a fully-informed L2 player KNOWS that V-fold reflects
across F_v and KNOWS that F_v=30 reflects x=8 to x=52, not x=56.
They would not commit at F_v=30 thinking it worked. The proposed
"plausible-but-wrong" is really a discovery-stage misstep, not a
post-discovery planning failure.

**How to fix**: name a wrong path that a FULLY informed player
would plausibly consider and reject. Candidates:

- "Try to use only V-folds, e.g. V at F_v=A and V at F_v=B for a
  net translation 2(B−A). This translates pawns horizontally but
  cannot change their rows; rows can only be changed via H-fold;
  ergo H-fold + axis-toggle is required." This is an
  arithmetically-grounded wrong path the player might consider.

- "Pick F_v=32 to align green, but commit H-fold first while V is
  still active — the click ACTION6 at the wrong cell does nothing
  (no-op), so the player learns ACTION6 must hit a fold-line
  cursor, then realises they cannot toggle until they aim
  precisely at a cursor cell." This is a real discoverable
  failure but borders on discovery-stage; use only if the spec
  argues it's a post-discovery planning issue (the player knows
  the toggle exists but mis-aims).

Either of those is sharper than "commit at F_v=30 immediately."

Sharpen the planning-depth justification accordingly.

## Other observations (not blockers, but consider)
- L3's witness uses a "double V-fold" — a non-trivial post-
  discovery planning step. The spec articulates this well; keep
  the wording when revising.
- All other checklist items (1-11, 13-17, 19-21) appear to pass.
- Novelty (positive + negative) appears to pass; no taxonomy or
  prior-game row dominates 3+ shared dimensions.

## Action
Address Issue 1 (BLOCKER) and Issue 2 (sharpen). Re-write
`mechanic-spec.md`. Mark the changed sections and quote the
issue numbers above.
