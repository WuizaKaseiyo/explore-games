# Critique revisions (visit 1)

The spec passes most checklist items but has substantive issues with §4 — particularly L2 witness mid-trace anomalies and L3's M3 mechanic which the spec authored, abandoned, replaced, and partially-replaced again, leaving the L3 witness as a "sketch" rather than a concrete action sequence.

## Issues

### 1. **CHECKLIST 12 (strict counterfactual / no trivial fallback) — L3 witness is not concrete.**

Spec §4 — Level 3 — Witness solution: *"Detailed action sequence omitted from the spec; will be made concrete during `implement` and verified in `smoke_test` via custom check."*

This violates the spec-template requirement that the witness be the *shortest action sequence that wins L3, written out action by action*. Without a concrete witness, item 12's per-mechanic counterfactual table cannot be rigorously evaluated for L3.

**Fix**: rewrite L3 with a simpler M3 mechanic (suggestion: **stamp-toggle** — re-pressing ACTION5 on a cell that already holds a stamp removes it) and a fully-listed action witness.

### 2. **CHECKLIST 12 — L2 witness mid-trace had unresolved dead-ends.**

Spec §4 — Level 2: the spec walks through several attempted witness sequences and lands on an 11-action witness `[ACTION3, ACTION2, ACTION5, ACTION1, ACTION5, ACTION1, ACTION5, ACTION4, ACTION5, ACTION2, ACTION5]`, but the trace narrative shows multiple attempts that failed and was reasoned about in real-time inside the spec. The final witness ought to be verified end-to-end without commentary.

**Fix**: re-state L2 with a clean layout, clean witness trace, and remove the "let me try again" detours from the spec body.

### 3. **CHECKLIST 18(c) — L3 planning depth argument depends on dropped M3 design.**

Spec §4 — Level 3 — Difficulty justification (c) Planning depth references "the magnetic drifts west toward this stamp" — but the M3 mechanic was loosened mid-spec to "dormant-magnetic" (drifts only on ACTION5). The trivial-heuristic argument needs to be re-derived against whichever M3 the spec finally commits to.

**Fix**: with M3 = stamp-toggle, restate the L3 trivial-heuristic argument: e.g., the greedy heuristic "stamp every channel cell on first traversal" is wrong because ordering of stamps gates avatar reachability of subsequent cells, and only by toggling-off a previously-placed stamp can the avatar reopen a path it already sealed.

### 4. **CHECKLIST 17 — Lose-condition section has a soft-lock disclaimer that hand-waves.**

Spec §8 — *"`_check_soft_lock()` is NOT implemented; the spec accepts that the player will see budget run out and re-attempt."*

`difficulty-rules.md` § 1 explicitly forbids "soft-locking the player into a state from which the win is already unreachable … without firing `lose()` on the turn the unreachability is detected — making the player wait for budget exhaustion in a no-win waiting room is the lose-side mirror of a punishingly tight budget."

**Fix**: With M3 = stamp-toggle, soft-lock cannot occur at L3 (every stamp is reversible, so any state is recoverable). For L1/L2 with permanent stamps, design layouts so the avatar always has a reachable path to every needed channel cell from start, AND every stamp the witness places is on a cell the witness does not need to re-traverse. Restate §8 to say "no soft-lock state exists for L3 (all stamps reversible) and L1/L2 layouts are designed such that every reachable witness move is available without backtracking through a stamped cell."

### 5. **MINOR — Sprite roster lists `stamp_decay_*` sprites that are no longer needed once M3 changes.**

Spec §3 includes `stamp_decay_3 / stamp_decay_2 / stamp_decay_1` sprites for the original decaying-stamp M3.

**Fix**: drop the decay sprites from §3 once M3 changes to stamp-toggle.

### 6. **MINOR — L1 witness trace mid-spec shows internal reasoning about "rows 7 and 10".**

Spec §4 — Level 1 — Witness solution: the narrative says *"this needs to also block row 10. Revised: …"* — that's drafting work that should have been resolved before the final spec was written.

**Fix**: clean up L1 witness narration so the final spec reads as a polished design, not a working draft.

## Summary

The mechanic and the L1 design are sound. The spec's clarity collapsed in L2/L3 due to the M3 mechanic being reformulated mid-document. Recommend: re-author the spec with M3 = **stamp-toggle**, re-verify L2 witness end-to-end, and strip mid-document reasoning detours.
