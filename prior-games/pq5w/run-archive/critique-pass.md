# Critique pass — pq5w (visit 2)

| # | Item | Verdict |
|---|---|---|
| 1 | Palette 0..15 (and -1 for transparent) | ✅ |
| 2 | Universal-scaffold structure | ✅ (planned, will be implemented in implement state) |
| 3 | available_actions ⊆ [1..7] | ✅ ([1, 2, 3, 4, 6]) |
| 4 | EXACTLY 3 Level entries | ✅ |
| 5 | 4-char ID, lowercase, alphanumeric, not in 25 reserved, not in prior-games index | ✅ (`pq5w`) |
| 6 | Mechanics drawn from core-knowledge-priors only | ✅ (objectness + topology) |
| 7 | No letters/digits/clipart/cultural-conventions | ✅ |
| 8 | ≥ 2 distinct mechanics | ✅ (4 across L1-L3) |
| 9 | L1 establishes base dynamic system, all required by witness, reduced state space, no on-screen text | ✅ |
| 10 | L2 and L3 each compose every available mechanic | ✅ |
| 11 | Mechanic inheritance + +1-or-+2 rule (L1=2, L2=3 (+1), L3=4 (+1)) | ✅ |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ — L1 wall extended to full column per visit-1 critique. Per-mechanic table: |

| Level | Mechanic | Solvable without M? | Why not (concrete) |
|---|---|---|---|
| L1 | walk | no | avatar must move to reach a portal cell or the goal cell from start (1, 7); no other movement method |
| L1 | portal-traverse | no | wall column at x=8, y=0..14 (15 sprites) forms a full vertical barrier; no walking path crosses x=8, so the goal at (14, 7) is reachable only via a portal jump from A (3, 7) to B (12, 7) |
| L2 | walk | no | avatar must walk to step on portal cells and traverse the room interior |
| L2 | portal-traverse | no | room walls form a closed rectangle at x=4..11, y=2..6 (22 wall sprites); the goal at (10, 4) is INSIDE the room and unreachable by walking |
| L2 | portal-relocate | no | both portals A (6, 4) and B (10, 3) start INSIDE the closed room; without the click-relocate, neither portal is reachable from the avatar's start at (1, 9) outside |
| L3 | walk | no | same as L2 — avatar must walk to step on portal cells and traverse interior |
| L3 | portal-traverse | no | same closed-room walls as L2; only entry into the room is via the portal pair |
| L3 | portal-relocate | no | both portals start INSIDE the room (as L2), so first relocate is required to enter; AND the forbidden column at x=8, y=3..5 separates sub-area-1 (with A) from sub-area-2 (with goal), so a SECOND relocate is required to bring B into sub-area-2 |
| L3 | forbidden-cell-avoid | no | the forbidden column at x=8, y=3..5 makes every walking path from sub-area-1 (where A is) to sub-area-2 (where the goal is) cross at least one forbidden cell, which fires `self.lose()`; the player must route around them via the second portal jump |

| 13 | Mechanic family absent from taxonomy | ✅ (no portal-pair entry in `taxonomy-of-25-games.md`) |
| 14 | Mechanic family absent from prior-games index | ✅ (no portal-pair-relocate; closest is jd4q echo-trail-teleport, distinguished concretely) |
| 15 | Concrete distinguishing rules for any near-miss | ✅ (per spec §9; jd4q, ek73, bx84, vy3k, kn58 each addressed) |
| 16 | Win condition stated as testable predicate | ✅ (`avatar.x == goal.x and avatar.y == goal.y`) |
| 17 | Lose condition stated | ✅ (step-budget exhaustion + forbidden-cell-touch) |
| 18 | Difficulty floor and ceiling — all four bullets per L1, L2, L3 | ✅ |
| 19 | No hidden state | ✅ (avatar position, both portal positions, step counter all visible; teleport-pending visualized as avatar-on-source-portal frame) |
| 20 | Not low-resolution | ✅ (64×60 grid with 4×4 sprites carrying internal pattern; no chunky upscale) |
| 21 | Sprite UI ≈ sprite role | ✅ (avatar yellow body with eyes; anchor portal heavy dark ring; float portal light pink ring with matching magenta core; wall solid block; goal green frame; forbidden red corners) |
| 22 | ACTION7 strict-undo or absent | ✅ (absent; not in available_actions) |

## Novelty verdict
- Family-level: NOVEL — no portal-pair entry in 25-game taxonomy or 67-game prior corpus.
- Description-level: NOVEL with concrete distinguishing rules vs jd4q (consumed-trail vs persistent-pair), ek73 (auxiliary warp pads vs primary verb), bx84 (beam vs walking avatar), vy3k (region swap vs point teleport), kn58 (slide-attract vs point-teleport).
- Negative similarity: walked 7 dimensions vs jd4q (closest); load-bearing axes (visual signature, pixel grain, core dynamic) all diverge. PASS.

## Verdict
All 22 checklist items PASS. Novelty NOVEL. Transition to `implement`.
