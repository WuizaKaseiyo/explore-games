# Step #05: write_spec (revision 1)

## Inputs Consumed
- workspace/critique-revisions.md (from #04 critique_spec): 3 issues + 3 minor notes
- workspace/mechanic-spec.md (from #03): existing spec to revise

## Deliverables Produced
- Revised `workspace/mechanic-spec.md`. Changes:
  - **§3 eraser sprite** (Note A): clarified pattern is a "+" topological cross (not "X"); inline 4×4 pixel layout shown.
  - **§3 goal sprite** (Note B): clarified shape is a square frame (4×4 outer ring purple, inner 2×2 white); inline pixel layout shown to disambiguate from "0"-digit.
  - **§4 L2 layout** (Issue 1): added 2×2 floor vestibule at S so 2 valid first actions exist; both south-then-east and east-then-south paths converge at J; branch east of J now leads to pickup_a at (14, 8); goal at (8, 14). Witness re-derived to 25 actions.
  - **§4 L2 difficulty (c)** (Issue 3 + Note C): replaced wrong-alternative (no longer "walking back through sealed doors", which was discovery-stage). New post-discovery wrong-alternative is "skip pickup_a and walk straight to goal" — fully-informed player considers it for shortest distance, rejects it because win predicate requires pickup_a. Plus enumerated post-discovery decision space at level start = 2 (south or east from S), and the witness's reasoning chain referencing post-discovery state.
  - **§4 L2 difficulty (a)**: tidied to remove stale "branch B" reference; updated valid-echo-cell count to ~12.
  - **§4 L2 difficulty (d)**: updated witness length to 25.
  - **§4 L3 layout** (Issue 2): same 2×2 vestibule; branches positioned to not conflict with either S→J approach (specifically: walls at (4,2)..(7,2) and (3,4)..(3,7) so the east-then-south first move is a dead-end pocket; branch A at column 8 rows 3-7; branch B at row 8 columns 9-13; branch C south of J via eraser at (8, 9)). post-discovery decision space at level start = 2 (≥ L2's 2).
  - **§4 L3 witness**: re-derived to 32 actions with the cleaner layout (no double round-trip).
  - **§4 L3 difficulty (d)**: updated witness length to 32.

## Notes
All 3 critique-revisions.md issues addressed concretely. Minor notes A, B, C all addressed. The revised spec is self-consistent: layouts, witness step counts, mechanic-necessity arguments, and difficulty justifications all align.
Transitioning back to critique_spec for re-verification.
