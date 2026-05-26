# Critique pass — `zd7m` mechanic-spec

## Checklist verdict (all 20 items)

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette 0..15 (-1 transparent) | ✅ | Sprites use {1, 3, 4, 7, 10, 11, 15}; -1 only as transparent. |
| 2 | Universal scaffold | ✅ | Spec describes sprites/levels/constants/HUD/game-class structure per `code/universal-scaffold.md`. |
| 3 | available_actions ⊆ [1..7] | ✅ | `[1, 2, 3, 4]`. |
| 4 | Exactly 3 Level entries | ✅ | L1, L2, L3 enumerated in §4. |
| 5 | 4-char ID, not in reserved/priors | ✅ | `zd7m`; verified absent from 25 reserved IDs and 19 prior-games entries. |
| 6 | Mechanics from core-knowledge-priors only | ✅ | Objectness + topology. No agentness/physics needed. |
| 7 | No letters/digits/clipart/conventions | ✅ | Sprites are abstract: ring + centre dot (pawn), hollow ring (target), checker (anchor), double ring (portal). None resemble letters, digits, or real-world objects. |
| 8 | ≥2 distinct mechanics | ✅ | Cohort-step + colour-matching + anchor + portal = 4 across levels. |
| 9 | L1 tutorial (base dynamic system, reduced state space, no on-screen text) | ✅ | 3 pawns + 3 targets, no anchors, no portals; discoverable in 1-2 presses; no text. |
| 10 | L2/L3 compose all available mechanics | ✅ | L2 witness exercises cohort-step + colour-matching + anchor; L3 witness exercises all four. |
| 11 | Mechanic inheritance and +1-or-+2 per level | ✅ | L1 N=2; L2 N+1=3; L3 L2-count+1=4. Each promotion adds exactly 1; every earlier-level mechanic remains required at later levels. |
| 12 | Strict counterfactual necessity (per-mechanic table) | ✅ (with the note below) | See per-(mechanic, level) table below. |
| 13 | Mechanic family absent from taxonomy | ✅ | `cohort-step-route` not in any of the 25 taxonomy rows; nearest are ka59/m0r0/vc33/lp85 with concrete distinguishing rules. |
| 14 | Mechanic family absent from prior-games | ✅ | Not in `prior-games/index.md`; nearest are kn58/wt39/m0r0-style coupled with concrete distinguishing rules. |
| 15 | Distinguishing rule for near-misses | ✅ | Stated in spec §9 for ka59, m0r0, vc33, lp85, wa30, dc22 (taxonomy) and kn58, wt39, m0r0/kf42/qb84-coupled (priors). |
| 16 | Win condition stated as testable predicate | ✅ | `_check_win` code snippet in §7 — iterates pawns and checks per-pawn colour-matched target. |
| 17 | Lose condition stated | ✅ | `_action_count >= step_budget` → `self.lose()` in §8. |
| 18 | Difficulty floor and ceiling per `difficulty-rules.md` § Critique check | ✅ | All four bullets (random-resistance, human-tractable, planning depth, step budget) present per L1, L2, L3. L2 planning chain identifies the "interleave" wrong path; L3 planning chain identifies the "DOWN-first greedy" wrong path with concrete reasoning about portal column 4. |
| 19 | No hidden state | ✅ | Pawn positions are visible. Teleport phase is shown via 6-frame portal-pulse + pawn-fade animation. No selection state, no modal flag — the cohort verb is stateless per-press. |
| 20 | Visual detail floor (no-information-loss-at-32×32) | ✅ | 3×3 sprites with internal motifs; pawn (centre-dot) vs target (hollow centre) distinguishable by shape, not just colour, at full resolution; the centre-dot vs hollow-centre detail blurs together at 2×2 average-pool, confirming the original detail is informative. |

## Per-mechanic counterfactual table (item 12 detail)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 cohort-step | no | Only declared actions are ACTION1-4; each is a cohort-step. No alternate motion mechanic. |
| L1 | M2 colour-matching | no | The win predicate's colour-check fires on every win attempt; geometrically, the only cohort-position where all 3 pawns simultaneously occupy any target is the colour-correct one (offsets pink-yellow=(-6,0), pink-blue=(-12,0) match target offsets). The predicate's colour comparison is a structural part of every successful `_check_win` call. |
| L2 | M1 cohort-step | no | As L1. |
| L2 | M2 colour-matching | no | Win predicate iterates pawns; without colour-matching the predicate would be "pawn on any target". L2 has 2 pawns + 2 targets; geometrically the only cohort-anchor sequence reaching simultaneous target-overlap is RIGHT × 10 + DOWN × 4 with pink → (14, 4) and yellow → (4, 14), which is colour-correct. The colour predicate ensures any future spec edit that adds a third pawn cannot accidentally alter this. |
| L2 | M3 anchor | no | Without anchors (7, 10) and (14, 7), every cohort press moves pink and yellow identically, preserving offset (0, -6). Reaching pink-target offset (10, -10) requires changing the cohort offset, which is impossible without selective blocking. The witness encounters anchor (7, 10) on every RIGHT (yellow blocked) and (14, 7) on every DOWN (pink blocked). Plausible alternates I enumerated and rejected: (a) "interleave RIGHT and DOWN" — first DOWN moves pink off (4, 4); pink ends at (14, 6) with no recovery within budget. (b) "DOWN first to row 14, then RIGHT" — pink reaches (4, 14) but yellow is anchor-blocked from RIGHT, so cohort can never move pink alone toward column 14; pink ends stuck at (0..4, 14). |
| L3 | M1 cohort-step | no | As L1/L2. |
| L3 | M2 colour-matching | no | Without the colour check, pink landing on portal_a's destination (17, 17) — same cell as target_yellow — would falsely "win" if pink survived to that step. The colour predicate rejects pink-on-target_yellow (colour 7 ≠ colour 11). |
| L3 | M3 anchor | no | Witness encounters anchor (14, 7) on every DOWN press (pink blocked at target). Without that anchor, the four DOWNs needed for yellow's portal traversal would also walk pink off (14, 4) → (14, 8); pink ends 4 cells below target, no win. Witness also encounters anchor (7, 10) on every RIGHT press (yellow blocked from drifting east of column 4 — necessary so yellow remains aligned with portal column when DOWN phase begins). |
| L3 | M4 portal | no | Target_yellow at (17, 17) sits inside a chamber sealed by anchor (16, 14) [north wall covering rows 14..16 cols 16..18], anchor (14, 16) [west wall covering rows 16..18 cols 14..16], and the south + east grid edges. A 3×3 pawn at any walking-approach cell ((17, 16), (16, 17), (17, 18) — last off-grid) has its proposed cells overlapping a chamber-wall anchor or grid edge. The only entry is portal teleport from portal_a at (4, 14) → portal_b at (17, 17). Plausible alternates I enumerated and rejected: (a) "walk yellow down column 17": requires RIGHT × 13 from start; cohort RIGHT is anchor-blocked for yellow at (7, 10), so yellow stays at column 4 — never reaches column 17. (b) "walk yellow down column 8 then RIGHT": yellow on column 8 was the start config but has now been redirected — actually yellow starts at (4, 10), not (8, 4); already-stated cohort coupling + anchors make column-shift impossible. (c) "approach chamber from north": even if cohort pushed both pawns south, anchor (16, 14) blocks every column 16..18 entry at row 14. |

## Novelty re-check on the fleshed-out spec

**Positive similarity (per `mechanic-novelty/similarity-check.md`):**
walked the full spec (not just the family-name) against every
taxonomy entry and every prior-games row. No row matches all
three of (win-condition, primary-action, primary-constraint).
Concrete distinguishing rules are stated in spec §9 for the
flagged near-misses; no flagged near-miss requires a new
distinguishing rule beyond what §9 already provides.

**Negative similarity (per `negative-similarity-check.md`):**
re-walked the seven dimensions against the L1, L2, L3 spec
layouts. The closest single overlap remains kn58 (sharing 4
of the 7 dimensions: board content, ask, kill, cast). All
heavier dimensions (verb, visual signature, sprite grain,
core dynamic) diverge. No prior shares ≥3 dimensions when the
heavier axes are weighted as the rule requires.

**Verdict:** NOVEL by both novelty tests. Spec-drift check
passed — L2 (anchor) and L3 (portal) do not push the candidate
toward any taxonomy or prior entry.

## Final verdict

**PASS — proceed to `implement`.**

All 20 checklist items pass; novelty verdict is NOVEL on both
axes. No revision required.
