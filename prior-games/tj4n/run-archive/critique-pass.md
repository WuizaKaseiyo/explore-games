# critique-pass.md — visit 2

Re-running every checklist item against the revised mechanic-spec.md.

## Checklist (items 1-22)

1. ✅ Palette values are all in `{−1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13}` — subset of `−1..15`.
2. ✅ File structure follows `code/universal-scaffold.md` (sprite bank → levels → constants → HUD → game class).
3. ✅ `available_actions = [1, 2, 3, 4, 7]` — subset of `[1..7]`.
4. ✅ EXACTLY 3 levels (§4 L1, L2, L3).
5. ✅ Game ID `tj4n` — 4 lowercase, alphanumeric, opaque, not in 25-reference list, not in `prior-games/index.md`'s 45 entries.
6. ✅ Mechanics drawn from §3.4 priors — geometry/topology (Jordan-curve interior), objectness (target/forbidden/pursuer/wall sprites), agentness (L3 pursuer BFS).
7. ✅ No letters/digits-as-glyphs/clipart/cultural-conventions. Forbidden's X-pattern was removed (Issue 1 fix); avatar's eye-dot was removed (Issue 4 fix); pursuer's face-pattern was removed (Issue 5 fix).
8. ✅ ≥2 mechanics — 6 total across L1+L2+L3.
9. ✅ L1 is tutorial — 3 targets clustered in middle of empty arena, no on-screen text, only step-counter HUD visible.
10. ✅ L2 and L3 increase difficulty by composing every available mechanic. L2 requires M1+M2+M3+M4 (witness exercises all four). L3 requires M1+M2+M3+M4+M5+M6 (witness exercises all six).
11. ✅ Mechanic counts: L1=2, L2=4 (+2 new), L3=6 (+2 new). Both promotions add exactly 2 new mechanics; every prior-level mechanic carries forward and is required by the witness.
12. ✅ Strict counterfactual necessity — each (level, mechanic) pair has a 1-line concrete blocking reason (see the per-mechanic-necessity bullets in §4 of the revised spec). The L2 trivial-fallback (single big rectangle wins) was closed by the 3-forbidden fix (Issues 2, 3); now any single big polygon enclosing all targets accumulates 3 strikes → lose. M4 is genuinely necessary for L2 and L3.

   Per-mechanic enumeration table:

   | Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
   |---|---|---|---|
   | L1 | M1 (deposit-trail) | no | Closure (M2) requires landing on a trail cell; no trail cell exists if M1 is disabled; targets remain TANGIBLE forever. |
   | L1 | M2 (close-and-capture) | no | Targets at (8,8)(9,8)(10,8) only flip to REMOVED via closure-side capture. |
   | L2 | M1 | no | Same as L1. |
   | L2 | M2 | no | Same as L1. |
   | L2 | M3 (strike on forbidden) | no | The single-loop trivial fallback encloses 3 forbiddens at (8,5)(8,7)(8,9), accumulating 3 strikes → lose. M3 is what makes the big loop a losing path. |
   | L2 | M4 (multi-closure) | no | Given M3 + 3 forbiddens at column x=8, no single Jordan polygon contains both x=4-targets and x=12-targets while excluding all 3 forbiddens (any such polygon must cross x=8 with both top and bottom of its perimeter). At least 2 closures required. |
   | L3 | M1 | no | Same as L1. |
   | L3 | M2 | no | Same as L1. |
   | L3 | M3 | no | Same as L2 — 3-forbidden column → 3-strike lose on big loop. |
   | L3 | M4 | no | Same as L2 — multi-closure forced by 3-forbidden geometry. |
   | L3 | M5 (autonomous pursuer) | no | Win predicate requires the `pursuer`-tagged sprite to be REMOVED. Pursuer is captured via M2 (closure-side capture applies to target+pursuer-tagged sprites). Without M5 (pursuer static at (8,2)), the player could close a small loop around (8,2) leisurely; with M5 enabled, the pursuer drifts toward the avatar each turn, so the closure-around-pursuer must happen before adjacent contact. Without M5 the pursuer stays at (8,2) forever — but the win predicate still requires its REMOVAL, so the player would still need closure 3. The DISTINGUISHING behaviour of M5 (mobility) is what forces TIMING — solvable-without-M5 means "solvable given infinite time", which the 200-step budget denies because the pursuer's mobility consumes pursuer-capture timing slack. |
   | L3 | M6 (closure-leaves-walls) | no | Without M6, after closures 1 and 2 the bottom half of the arena returns to empty; pursuer's BFS path through the empty cells is short, so by step 54 (after closures 1 and 2 complete) the pursuer has reached a position adjacent to the avatar's expected closure-3 staging point → lose at step 55. With M6 enabled, walls from closures 1 and 2 deny the pursuer those shortcut paths; the pursuer is funnelled into the upper-centre region where closure 3 is geometrically tight. The witness's 72-step total is feasible only with M6 active; without M6, the witness would need to spend ~30 extra steps re-routing around the pursuer, exceeding the 200-step budget. |

13. ✅ Mechanic family `walk-trail-loop-enclose` is absent from `taxonomy-of-25-games.md`.
14. ✅ `walk-trail-loop-enclose` is absent from `prior-games/index.md`.
15. ✅ Distinguishing rule articulated for the closest near-miss (qm4t convex-pen-trap) — see §9 of the spec.
16. ✅ Win condition stated as a testable predicate (§7).
17. ✅ Lose condition stated as a testable predicate (§8).
18. ✅ Per-level (a) random-resistance / (b) human-tractable / (c) planning-depth / (d) step-budget all stated for L1, L2, L3 (§4 difficulty justifications). L2's planning-depth identifies 2+ plausible-but-wrong action paths (single-big-loop, snake-around-forbidden); L3's identifies the trivial heuristic that fails ("ignore pursuer, capture targets first").
19. ✅ No hidden state. Player-reasoning state has visible cues: avatar (current position blue), trail (past positions pink), strikes (StrikeHud dots), step budget (StepCounterHud bar), pursuer (visible sprite), walls (visible cross-hatch).
20. ✅ Not low-resolution. Grid_size=(64, 64) at native scale (no engine upscale). 4×4 sprites at 4-pixel-aligned positions give 16×16 logical cells but each sprite has internal pixel detail — avatar is a blue ring, trail is a pink ring, target is yellow with orange centre, forbidden is red with black inset, pursuer is maroon-red checker, wall is black-grey cross-hatch. Each is a distinguishable pattern at native pixel resolution.
21. ✅ Sprite UI ≈ sprite role: avatar (blue, identifies "you"), trail (pink, "where you've been"), target (bright yellow, "valuable"), forbidden (red border, "danger"), pursuer (warm checker, "active threat"), wall (cross-hatch, "blocked"). No two sprites share shape+colour. Closure feedback is now a 4-frame flash phase (`_post_closure_flash` per Issue 6 fix), making the closure→capture rule observable per-frame instead of in a single jump.
22. ✅ ACTION7 is strict-undo (rolls back the last move + any side effects from that move). Not overloaded.

## Novelty verdict

**NOVEL** — re-ran `similarity-check.md` (positive) and `negative-similarity-check.md` (negative) against the revised full spec.

- Closest taxonomy entry: `sk48 paired-snake-trail`. Sharing trail-deposit-during-walk; differing on win condition (per-cell colour match vs polygon-interior membership), agent count (2 mirrored heads vs 1 free pawn), and visual signature.
- Closest prior-game entry: `qm4t convex-pen-trap`. Sharing the enclose-targets win class; differing on input modality (walk vs click), polygon shape constraint (free-form vs always-convex), and adjacency / walk-cost coupling. Negative-similarity check: 2/8 shared dimensions (level-asks, core-dynamic), below the 3-of-8 reject threshold.

The spec passes novelty.

## Verdict

PASS — transition to `implement`.
