# Step #07: write_spec (visit 3, addressing critique-revisions v2)

## Inputs Consumed
- workspace/critique-revisions.md v2 (2 issues)
- workspace/mechanic-spec.md v2

## Deliverables Produced
- mechanic-spec.md v3: targeted edits to §3 (pivot sprite no longer has upward-arrow; uses "+" cross; avatar_pivot_pending simplified to 2×2 corner accent), §4 L3 (M4 description updated; counterfactual table updated; planning-depth re-justified with IRRECOVERABLE failure of greedy heuristic), §6 (added pivot consumption to visual cue list). Pivot is now ONE-SHOT.

## Notes
- The v3 change is small (only 5 targeted edits to v2) — preserves all the rest of the spec.
- The one-shot pivot makes L3's planning-depth real: greedy heuristic loses the entire game (irrecoverable), not just delays.
- The "+" cross in the pivot sprite is allowed per `forbidden-elements.md` (topological symbol, explicitly OK).
