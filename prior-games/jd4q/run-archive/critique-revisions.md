# Critique revisions for jd4q

## Issues found

### Issue 1 — L2 fails checklist 18(d) post-discovery decision space ≥ 2

**Checklist item violated:** 18(d) (planning depth via `difficulty-rules.md` § 2 (d)). Specifically:
> *"L2: spec must (1) **enumerate the post-discovery decision space at level start** — count of valid first actions a fully-informed player faces. If < 2, the level is a 1-action-lookup-table by definition → reject."*

**Offending section:** §4 Level 2 layout — the spec puts S at `(2, 2)` with the only floor cell adjacent being `(2, 3)` (south); cells `(1, 2)`, `(3, 2)`, `(2, 1)` are all walls. From the fully-informed player's perspective at level start, the only meaningful first action is ACTION2 (south); ACTION1, ACTION3, ACTION4 are no-ops blocked by walls. Decision space count = 1.

**Concrete fix:** Add a 2×2 floor "vestibule" at S. Make cells `(2, 2)`, `(3, 2)`, `(2, 3)`, `(3, 3)` all floor; the corridor to J branches *both* east (via `(3, 2)..(8, 2)` then `(8, 3)..(8, 7)` south) and south (via `(2, 3)..(2, 8)` then `(3, 8)..(7, 8)` east). Both paths converge at J=`(8, 8)` and are equal-length (12 walks). From S=`(2, 2)` two valid first actions exist: ACTION2 (south to `(2, 3)` floor) and ACTION4 (east to `(3, 2)` floor). Decision space count = 2.

Re-derive the witness with the new layout and re-state §4 L2 mechanics necessity / step counts accordingly.

### Issue 2 — L3 fails checklist 18(d) post-discovery decision space ≥ L2's

**Checklist item violated:** 18(d) (planning depth via `difficulty-rules.md` § 2 (d)). Specifically:
> *"L3: spec must (1) **enumerate the post-discovery decision space**; count ≥ L2's, never smaller."*

**Offending section:** §4 Level 3 layout — the spec puts S at `(2, 2)` with the only floor adjacent being `(2, 3)` (south leg of S→J path). Decision space count = 1.

**Concrete fix:** Apply the same 2×2 floor vestibule at S as in Issue 1. From S, ACTION2 (south) and ACTION4 (east) both reach floor and both feed the S→J path. Decision space count = 2 ≥ L2's 2. Adjust L3 layout so branches A, B, C don't conflict with whichever S→J path the player chooses (specifically: branch A goes north from J only if the east-then-south S→J path doesn't share those cells; otherwise reposition K_A or branch direction so cells are disjoint).

Re-derive the L3 witness step count; budget 100 still applies.

### Issue 3 — L2 (d) wrong-alternative is a discovery-stage misstep, not post-discovery

**Checklist item violated:** 18(d) (per `difficulty-rules.md` § 2 (d) — Stage-conflation guard). Specifically:
> *"Stage-conflation guard. Reject if the named 'heuristic that fails' or wrong-path argument is a discovery-stage misstep — something a player only does because they haven't yet understood the mechanic. The post-discovery player knows what each action does..."*

**Offending section:** §4 Level 2 Difficulty justification (c) — the spec quotes:
> *"Plausible wrong alternative the post-discovery player would consider and reject: trying to walk back through the sealed corridor (ACTION3 from K_A) — the cell `(7, 8)` is sealed, the move is blocked."*

A post-discovery player who already understands the mechanics knows that closing-doors seal on egress; they would not "consider and reject" walking back through a sealed corridor — they already know it's blocked. This is a discovery-stage misstep.

**Concrete fix:** Replace with a genuinely post-discovery wrong alternative — *"skip pickup_a and walk straight from S to goal."* The fully-informed player (knowing all mechanics) might consider this as the shortest path: walk south from `(2, 3)` to `(2, 8) = J`, continue south to `(2, 14) = goal`, win. They reject this because the win predicate requires `pickup_a` collected and the avatar arriving at goal without `pickup_a` does not fire `next_level()`. This is a true post-discovery alternative the player considers (it minimises step count) and rejects (because of the win predicate, which the post-discovery player knows). Plus state the witness's reasoning chain referencing post-discovery state (the win predicate, the fact that closing-doors seal a one-way passage to K_A).

## Minor guidance (not blocking; address while revising)

### Note A — clarify eraser pattern
The spec describes the eraser sprite as a "magenta cross-pattern interior". Make it clear in §3 that the cross is a "+" (topological cross — vertical bar plus horizontal bar) and NOT an "X" (diagonal bars), to stay aligned with `forbidden-elements.md`'s example principle (a "+" is a topological symbol; an "X" reads more letter-like).

### Note B — clarify goal sprite shape
The spec describes the goal sprite as "purple ring with white centre". Make it clear in §3 that this is a square frame (4×4 with the outer pixels purple and the inner 2×2 white) rather than a round-ring shape that could read as a "0" digit. A square frame is geometric/abstract and unambiguously not a digit glyph.

### Note C — restate L2 alternates explicitly
While revising §4 L2 (c), also list other plausible-but-wrong alternatives the post-discovery player might consider (clicking the deepest echo at `(2, 2)` or any other corridor echo — these all win but with longer step counts; the witness's choice of the J-echo is optimal). The spec should make it clear that the L2 decision question is "which echo to click" and that there are multiple winning options; the witness picks the one minimising total steps.
