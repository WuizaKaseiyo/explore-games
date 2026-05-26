# Critique pass — qy7w spec

Re-read `mechanic-spec.md` against `design-constraints/checklist.md`
items 1-22, the novelty rules, and the negative similarity check.

## Checklist items 1-22

- **1. Palette 0..15.** ✅ Sprites use {3, 4, 5, 7, 8, 9, 11, 14}; strand-canvas uses -1 for transparent.
- **2. Universal scaffold.** ✅ Spec describes structure consistent with `code/universal-scaffold.md` (sprite bank → levels → constants → HUD widget → game class).
- **3. `available_actions` ⊂ [1..7].** ✅ `[6]` only.
- **4. Exactly 3 levels.** ✅ L1, L2, L3.
- **5. ID = 4 lowercase chars, opaque, non-colliding.** ✅ `qy7w` — 4 chars, lowercase, no English meaning, not in 25-game reserved list, not in `prior-games/index.md`, not in untracked `prior-games/<id>/` dirs.
- **6. Mechanics from core-knowledge-priors.** ✅ Geometry & topology (primary), objectness, basic physics (L3 colour-shift).
- **7. No letters/digits-as-glyphs/clipart/cultural conventions.** ✅ TWIST crossing renders strands with visible over-under bridges (continuous over-strand, 1-pixel break on under-strand) — NOT a clean letter "X". Blocker is a generic 4×4 framed-coloured-square (no hazard-stripe). Strand canvas paints colour bars only — no symbols. Slots and caps are abstract framed/filled rectangles.
- **8. ≥ 2 distinct mechanics in environment.** ✅ BINARY toggle, LONG toggle, COLOUR-SHIFT cell.
- **9. L1 tutorial — base dynamic system, all L1 mechanics witness-required, reduced state space, no on-screen text.** ✅ L1 has 1 mechanic (BINARY) with witness toggling 2 of 3 binary crossings; only 3 crossings (vs 4 at L2 and 5 at L3); no text glyphs.
- **10. L2/L3 increase difficulty by composition (not by scaling).** ✅ L2 adds LONG mechanic (qualitatively new — single-click long-distance transposition) + blocker constraint that forces composition with L1's BINARY. L3 adds COLOUR-SHIFT (new mechanic that interacts with both BINARY and LONG via routing-determines-which-strand-gets-shifted). L3 is NOT "L2 with bigger grid" — same grid, same strand count, qualitatively new mechanic.
- **11. Mechanic inheritance and +1-or-+2 rule.**
  - L1: N=1 (BINARY).
  - L2: N+1 = 2 (BINARY + LONG). Both witness-required.
  - L3: M+1 = 3 (BINARY + LONG + COLOUR-SHIFT). All witness-required.
  - ✅ +1 each level, within rule. Every earlier-level mechanic carried forward and required at every later level.
- **12. Strict counterfactual necessity (no trivial fallback).** Per-mechanic enumeration:
  - **L1 / BINARY**: ✅ initial all-PASS bottom is (R, B, Y); slots want (Y, R, B). The only player verb is BINARY toggle. No win without it.
  - **L2 / BINARY**: ✅ enumerated (c1, c2, c3, c4) ∈ {0,1}^4. With c1=c3=c4=0 (no binary toggle), bottoms are (R,B,Y) for c2=0 and (Y,B,R) for c2=1 — neither matches slot (Y,R,B).
  - **L2 / LONG**: ✅ enumerated all c2=0 (binary-only) configs. Only (c1=0, c2=0, c3=1, c4=1) gives bottom (Y, R, B), and at y=36 col 1 = strand_Y (yellow) → blocker_yellow at (col=1, y=36) matches → `lose()`. Every other c2=0 config has wrong bottom permutation. Hence no binary-only path wins; LONG necessary.
  - **L3 / BINARY**: ✅ with c1=c3=c5=0, c2=1, c4=0: trace gives (G, B, R) at bottom — col 1 wrong. At least one binary toggle required.
  - **L3 / LONG**: ✅ enumerated c2=0 paths. For col 0 bottom = G, the strand at col 0 at y=38 must stay there (c4=0). With c2=0 and c1=0, that's strand_R → R passes through SHIFT-G → strand_R becomes G. But constraint (iii) demands strand_R end at col 1 (slot wants R = original strand_R colour). With c1=0 and c2=0, strand_R is at col 0 to bottom — wrong column AND its colour is now G (not R). Slot 1 has wrong strand. With c1=1 and c2=0, strand_B at col 0 → B becomes G. But strand_B must end at col 2 (slot 2). With c1=1, c2=0, strand_B at col 0 to bottom — wrong column. Slot 2 has wrong strand. Hence no binary-only path wins; LONG necessary.
  - **L3 / COLOUR-SHIFT**: ✅ none of {R, B, Y} = G (palette 14). No mechanic except SHIFT-G introduces green. Slot 0 demands G, so SHIFT-G must be triggered.
  - **L3 / blocker_yellow (constraint, not mechanic)**: present and avoided by witness. Plausible alternates ("toggle C3 first to build σ_b", "toggle C3+C4 to build σ_b σ_a", greedy generators) routinely route strand_Y to (col=1, y=42) or strand_B with shifted colour to col 0 → fail.
  - Plausible alternate strategies enumerated (per item 12's "verify by enumeration"):
    1. *L1: "Toggle every crossing to TWIST"* — net = σ_a σ_b σ_a = (Y, B, R), slot wants (Y, R, B). Mismatch.
    2. *L2: "Toggle C3 + C4 (build σ_b σ_a directly)"* — bottom (Y, R, B) MATCH but at y=36 col 1 = Y → blocker → lose.
    3. *L2: "Toggle C1 + C3 (build σ_a σ_b)"* — bottom (B, Y, R), mismatch.
    4. *L3: "Greedy: toggle each binary in turn, ignore the long crossing"* — c1=c3=1, c2=0, c4=c5=0: trace → bottom strand_B(G) at col 0, strand_Y at col 1, strand_R at col 2 → slot mismatch at col 1 (want R, got Y) and col 2 (want B, got R).
    5. *L3: "Long-only"* — c2=1, others 0: bottom strand_Y(G) at col 0, strand_B at col 1, strand_R at col 2. Slot mismatch.
- **13. Mechanic family absent from taxonomy.** ✅ `strand-twist-permute` not in any of 25 reference rows; closest are vc33, lp85 (cite distinguishing rules in mechanic-pick.md and spec §9).
- **14. Mechanic family absent from prior-games index.** ✅ Walked every entry; closest are jx5k, vy3k, rk7x — distinguishing rules cited.
- **15. Distinguishing rules articulated for near-misses.** ✅ See spec §9.
- **16. Win condition stated.** ✅ Spec §7 — `_check_win` predicate.
- **17. Lose condition stated.** ✅ Spec §8 — step budget OR blocker-hit.
- **18. Difficulty floor and ceiling.** Per `difficulty-rules.md` § Critique check:
  - **L1**: ✅ (a) random play has high stumble probability — acceptable per § 1 for tutorial; (b) ~90 sec; (c) no strict planning required (correct per L1 rule); (d) budget 30, generous.
  - **L2**: ✅ (a) random walk on 4-cube + 4 absorbing-loss states (blocker hits) + budget cap = non-trivial barrier; (b) ~2 min; (c) post-discovery planning explicitly enumerates 4 first-clicks, names the wrong heuristic ("just compose adjacent generators"), traces witness reasoning; (d) budget 24, generous over 2-click witness.
  - **L3**: ✅ (a) random walk on 5-cube with multiple loss states + tight blocker pattern; (b) ~3 min; (c) post-discovery planning names trivial heuristic that fails (greedy adjacent-generator composition) AND traces where it diverges from witness (at first toggle, due to blocker constraint); (d) budget 22, generous over 2-click witness, not shrinking from L2 in the relative sense (L3 budget 22 vs L2 24 — close, both >>witness).
- **19. No hidden state — visible cue for every mutated state.** ✅ Crossing PASS/TWIST is visible via the crossing sprite's pixel pattern; strand routing/colour is rendered live in the dynamically-painted strand_canvas; SHIFT-G's effect (strand colour change) is visible from y=38 down on the canvas; blocker is visible as a small sprite at (col, y); step counter is visible in HUD bar. No "selected sprite" hidden state because there is no selection.
- **20. Don't generate a low-resolution game.** ✅ Native 64×64 grid_size, no upscaling. Strand bars are 3 pixels wide. Crossings are 19×7 sprites with internal X/parallel-bar pattern. Top caps and bottom slots have distinct shape (filled vs hollow framed). Blockers are 4×4 framed sprites with internal colour pattern. Each sprite kind has *internal* pixel structure (not just colour fill).
- **21. Design the UI to teach.** ✅
  - *Sprite UI ≈ role*: top caps are FILLED coloured rectangles at the top — read as "starting label / pin at the top of a strand". Bottom slots are HOLLOW coloured frames at the bottom — read as "container / destination". Crossings are X-or-parallel-bar shapes between strand columns — read as "bridge / linkage". Each crossing's PASS state shows two parallel bars (clearly "pass-through"); TWIST state shows X with bridges (clearly "swap"). Blockers are small framed coloured squares at fixed cells — read as "marker / obstruction"; the player learns their role through trial-and-fail (blocker-triggers-lose is harsh but corpus-conforming — sk48, ka59, lf52 also have insta-lose hazards).
  - *Identical visuals imply shared role*: All BINARY crossings share the same shape; all LONG crossings share the same wider shape — distinct from BINARY. Different crossing types are visually distinguishable at a glance. All blockers share the framed-square shape; their colour distinguishes which strand they reject.
  - *Visual carries the mechanic*: The strand canvas's live re-painting after every toggle makes the cause-effect link maximally legible. Player toggles a crossing → sees strand colours rearrange below it.
  - *Operational test*: An L1 screenshot shows three vertical coloured strands with X-marker overlays at three rows, plus coloured pins at top and frames at bottom. A first-time viewer can guess "click the X markers to rearrange the strands; goal is to match top colours to bottom frames".
- **22. ACTION7 strict-undo or absent.** ✅ Action subset is `[6]` only — ACTION7 explicitly omitted (no meaningful undo in this game). Per `action-enum.md`'s § Slot 7 is strict-undo: do not overload the slot; omit when no undo.

## Novelty (re-run on the full spec)

- **Vs taxonomy of 25**: ✅ NOVEL. Closest near-misses (vc33, lp85, cn04, tn36, sk48, r11l) reviewed; distinguishing rules in spec §9 hold against the full spec, not just the family-name. The fleshed-out spec adds COLOUR-SHIFT (L3) which further distances from any taxonomy entry — no reference game has a per-strand colour mutator.
- **Vs prior-games index** (66 tracked + 9 untracked dirs): ✅ NOVEL. Closest (jx5k, vy3k, mz6t, qf8m, gx7m, rk7x) reviewed; distinguishing rules hold.
- **Negative similarity check**: ✅ Re-walked the 8 dimensions on the full spec against vc33, lp85, jx5k, qf8m, mz6t, rk7x. No prior shares ≥ 3 dimensions. The two consistent shared dimensions across all comparisons are D2 (click-based input) and D3 (colour-match win predicate); these are too generic to count as overlap on their own. The named principles (D6 palette, D7 pixel grain, D8 core dynamic) all diverge — qy7w's vertical-strand visual is unique in the corpus.

## Verdict

**PASS.** Transition to `implement`.
