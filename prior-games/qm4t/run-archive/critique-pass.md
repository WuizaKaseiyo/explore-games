# critique-pass.md — final verdict for `mechanic-spec.md` v3

Spec v3 is `mechanic-spec.md` with the v2 changes (4 fixes) plus
the v3 patch (3rd maroon at L3 to close the M3-bypass).

## Per-checklist-item verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | Sprites use palette 0..15 (and -1) | ✅ PASS |
| 2 | Universal scaffold structure | ✅ PASS (will be enforced in `implement`) |
| 3 | `available_actions` ⊆ `[1..7]` | ✅ PASS — `[5, 6]` |
| 4 | EXACTLY 3 levels | ✅ PASS |
| 5 | 4-char ID (qm4t) not in reserved or priors | ✅ PASS |
| 6 | Mechanics from core-knowledge-priors only | ✅ PASS — geometry+objectness+agentness |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS — `vertex_post` is a 3-cell vertical bar (explicitly allowed); `critter_*` is a rounded blob; `patroller_purple` is a tapered diamond with a single eye; `tally_dot_*` is a 3×3 hollow square; `strike_marker` is a 3×3 filled red square; `pen_overlay` is a computed convex outline |
| 8 | ≥ 2 distinct mechanics | ✅ PASS — L1 has M1+M2, L2 +M3, L3 +M4 |
| 9 | L1 = base system, no on-screen text | ✅ PASS |
| 10 | L2 / L3 compose by adding mechanics, not scale | ✅ PASS |
| 11 | Mechanic inheritance, +1-or-+2 per level | ✅ PASS — L1=2, L2=3 (+1), L3=4 (+1) |
| 12 | Strict counterfactual necessity (no trivial fallback) | ✅ PASS — see per-mechanic table below |
| 13 | Mechanic family absent from taxonomy | ✅ PASS |
| 14 | Mechanic family absent from prior-games index | ✅ PASS |
| 15 | Concrete distinguishing rule for each near-miss | ✅ PASS — gv47, xn5p, ng52, kn58, pz4t, su15, ar25, r11l each have a concrete rule |
| 16 | Win condition stated | ✅ PASS — tally empty |
| 17 | Lose condition stated | ✅ PASS — 3 strikes OR step counter ≤ 0 |
| 18 | Difficulty floor and ceiling, all 4 bullets per level | ✅ PASS — random-resistance / human time / planning depth / step budget all present for L1, L2, L3 |
| 19 | No hidden state | ✅ PASS — every state mutation has a visible cue (post sprite, pen overlay, tally dot, strike marker, step counter) |
| 20 | Don't generate a low-resolution game | ✅ PASS — full 64×64, sprites at display-pixel level |
| 21 | UI to teach (sprite-role, identical-visual, visual-carries-mechanic) | ✅ PASS — three rules of thumb articulated and satisfied |

## Per-mechanic counterfactual table (item 12)

| Level | Mechanic | Solvable without triggering? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (place) | no | Engine creates posts only via the ACTION6 placement branch; without M1 there are zero posts ⇒ `_compute_hull` returns ∅ ⇒ ACTION5's inside-test finds no critters ⇒ tally never depletes. |
| L1 | M2 (commit) | no | The only function calling `level.remove_sprite` on a `critter` is `_commit_pen` (the ACTION5 handler). No walk-into, no decay, no merge-on-contact. |
| L2 | M1 | no | Same argument as L1 (zero posts ⇒ no hull). |
| L2 | M2 | no | Same argument as L1 (commit is sole removal pathway). |
| L2 | M3 (selective shape) | no | Layout has 4 maroons at the playfield corners. Trivial big pen (e.g. `(0,0)-(63,0)-(32,63)`) captures all 4 → 4 strikes → `lose()`. Witness must place posts in the band between the green cluster and the corner maroons. |
| L3 | M1 | no | Same argument. |
| L3 | M2 | no | Same argument. |
| L3 | M3 | no | Layout has 3 maroons at `(8,32)`, `(58,32)`, `(32,4)`. Trivial big pen captures all 3 → 3 strikes → `lose()`. Even pens that admit just one maroon, combined with mistimed M4, push strikes ≥ 3. |
| L3 | M4 (timing) | no | 3 patrollers synced; phases 0..3 are inside any reasonable witness pen. Committing on phase 0..3 captures 3 patrollers → 3 strikes → `lose()`. The witness MUST count posts to land ACTION5 on phase ≥ 4. |

Every cell answers **no**, with a concrete blocker. PASS.

## Novelty verdict

**Taxonomy similarity-check (against all 25 reference rows):**
- Family-level: no match. None of the taxonomy rows uses any of
  {pen, convex, hull, polygon, vertex, trap, enclose}.
- Description-level near-misses (su15, ar25, r11l) each have a
  concrete distinguishing rule articulated in §9 of the spec.
- **NOVEL.**

**Prior-games similarity-check (against all 34 priors):**
- Family-level: no match.
- Description-level near-misses (gv47, xn5p, ng52, kn58, pz4t)
  each have a concrete distinguishing rule articulated in §9.
- **NOVEL.**

**Negative-similarity check (per `negative-similarity-check.md`):**
- gv47: 2 dimensions shared (click+ACTION5 verb skeleton; step
  counter lose).
- su15: 2 dimensions shared.
- ng52: ≤ 2 dimensions shared.
- All other priors: 0–1 dimensions shared.
- All below the 3-dimension reject threshold.
- **PASS.**

## Verdict
**ALL CHECKLIST ITEMS PASS. NOVELTY: NOVEL on both axes.**
Transition to `implement`.
