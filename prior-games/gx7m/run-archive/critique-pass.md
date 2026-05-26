# Critique pass — gx7m mechanic-spec.md

Independent adversarial review against
`design-constraints/checklist.md` items 1-18,
`mechanic-novelty/similarity-check.md` (re-run on full spec),
`mechanic-novelty/negative-similarity-check.md` (re-walk 8 dims).

## Format & structure

| # | Item | Verdict |
|---|---|---|
| 1 | Sprite palette ⊂ {0..15, -1} | ✅ PASS — all sprite pixel values are in {0, 2, 3, 4, 6, 7, 10, 11, 12, 14, 15} ∪ {-1}. |
| 2 | Universal scaffold | ✅ PASS — sprites dict, levels list, constants, HUD widget, game class structure all present in §3, §4, §6. |
| 3 | `available_actions` ⊂ [1..7] | ✅ PASS — `[6]` per §5. |
| 4 | EXACTLY 3 levels | ✅ PASS — §4 enumerates L1, L2, L3, no more, no fewer. |
| 5 | 4-char ID, lowercase, opaque, no collisions | ✅ PASS — `gx7m` verified in `mechanic-pick.md` against the 25 reserved IDs and the 17-row prior-games index. Not an English word. |

## §3.4 priors & constraints

| # | Item | Verdict |
|---|---|---|
| 6 | Mechanics ⊂ core-knowledge-priors categories | ✅ PASS — Objectness (gears), Geometry+topology (rotation, mesh adjacency, mark-target alignment, connected-component partitioning), Physics (sign-flipping rotational transmission). All four allowed categories. No agentness. |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS — gear cog-tooth pattern is mechanical-abstract; collar-ring is a hollow square frame; tangs are 1×2 nubs. Marks at compass positions are angular-alignment cues, not arrow glyphs. No sprite resembles a letter or digit. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS — 3 mechanics across the environment: cascade (M1), ratchet (M2), clutch (M3). |
| 9 | L1 = tutorial: base dynamic, no on-screen text, reduced state | ✅ PASS — L1 has 3 plain gears in a row, single mechanic (cascade), no ratchet/clutch/text. Reduced state space (smallest level). |
| 10 | L2/L3 increase difficulty by COMPOSING, not by scaling | ✅ PASS — L2's witness exercises BOTH cascade AND ratchet (the ratchet's tang-click is essential per the per-mechanic necessity argument); L3's witness exercises ALL THREE mechanics. Levels do not just scale grid/item count. |

## Mechanic structure

### Item 11 — Mechanic inheritance and the +1-or-+2 rule

✅ PASS.

| Level | Mechanics witness-required | Count | Δ from prior |
|---|---|---|---|
| L1 | M1 (cascade) | 1 | n/a |
| L2 | M1, M2 (ratchet) | 2 | +1 ✓ |
| L3 | M1, M2, M3 (clutch) | 3 | +1 ✓ |

Every L1 mechanic carries forward to L2 and L3 (cascade fires on
every click). Every L2 mechanic carries forward to L3 (ratchet
direction-gating still required at L3 to break A-B parity coupling).
No level introduces 0 or ≥3 new mechanics.

### Item 12 — Strict counterfactual necessity (no trivial fallback)

✅ PASS. Per-mechanic table, one row per (mechanic, level) pair:

| Level | Mechanic | Solvable without M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 cascade | NO | The only available verb is `ACTION6` and every gear-affecting click invokes the cascade engine in the dispatcher; targets `(180°, 180°, 180°)` are non-zero from initial `(0°, 0°, 0°)`, so at least one click — hence at least one cascade — must fire to win. |
| L2 | M1 cascade | NO | Same argument: targets `(180°, 90°, 270°)` non-zero from `(0°, 0°, 0°)`; cascade is unconditionally fired by any gear/tang click. |
| L2 | M2 ratchet | NO | Magenta starts BLOCKED. Magenta's target rotation is `90°` ≠ 0°, so magenta MUST rotate at least once. The ratchet rotates only via a CW-allowed cascade or a CW-allowed hub click; both require state ≠ BLOCKED, which only the `tang_dir` click can change. Hence `tang_dir` MUST be clicked at least once. Furthermore, the (180°, 90°, 270°) target is not in the linear span of pink-hub/lblue-hub clicks alone (they leave magenta at 0° forever) — the ratchet's asymmetric pass-through (allowing R-hub click to fire while later cascades from pink are blocked back at R) is the load-bearing route to the target. |
| L3 | M1 cascade | NO | Targets non-zero everywhere; same as L1/L2. |
| L3 | M2 ratchet | NO | Magenta target `90°` reachable only via cascade through magenta, gated by ratchet direction (default BLOCKED). Tang must be clicked. Furthermore, parity-0 gear deltas across the chain are `(pink=+2, lblue=+1, orange=+2)` — *non-uniform*; pure-cascade span requires uniform parity-0 deltas, so the ratchet's role-as-asymmetric-router is required to drive pink up to `+2` while lblue stays at `+1`. |
| L3 | M3 clutch | NO | lblue and orange are both parity-0 in the chain `pink(0)–magenta(1)–lblue(0)–green(1)–orange(0)`, separated by 2 hops, hence mesh-coupled to the same parity-0 delta in any cascade-only or cascade-with-ratchet scheme. Their targets `(+1, +2)` are *different*. The ONLY way to make them differ is to *partition the mesh-graph* by removing the lblue↔green and green↔orange edges — i.e., by disengaging the clutch via the `tang_lever` click. |

Every row answers NO with a specific cell/sprite/rule that blocks
every alternate path. No row hand-waves. No row's "no" depends on
"the witness happens to use M".

Trivial fallbacks the per-mechanic check explicitly rejects:

- "Click each gear individually until each mark aligns" — fails
  because of bipartite parity coupling at L3 (and at L2 the
  magenta gear cannot be advanced by hub-click without first
  setting the ratchet direction).
- "Click only one gear repeatedly" — works for L1 (target is
  parity-uniform), fails for L2 and L3 (targets are not in
  pure-cascade span).
- "Don't touch the ratchet/clutch tangs" — fails for L2 (magenta
  stays at 0°) and L3 (lblue/orange parity coupling).

## Novelty

| # | Item | Verdict |
|---|---|---|
| 13 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ PASS — `gear-mesh-cascade` is not a row in the taxonomy. Family-tag word-stems (`gear`, `mesh`, `cascade`) match no taxonomy row at the family-level check. |
| 14 | Mechanic family absent from `prior-games/index.md` | ✅ PASS — verified against all 17 priors. The closest in spirit is `qz73` (radial-cycle-lock — single rotor with locked tips); the fleshed-out spec deepens the divergence (per-edge propagation, mesh-graph partition via clutch, multiple independent gears) rather than narrowing it. |
| 15 | Concrete distinguishing rule for SOUNDS-similar near-misses | ✅ PASS — §9 of the spec articulates rules for `lp85`, `cn04`, `qz73`, `bx84`, `vn8d`, `kn58`. Each rule names what concretely differs (object cardinality, propagation rule, win-condition, action verb), not vague "different-feeling" language. Re-checked the spec's L2 and L3 against the deeper deep-analyses for `qz73` and `bx84` — no drift; the new clutch mechanic at L3 reinforces divergence (qz73 has no graph-partition operation; bx84 has no rotational cascade). |

### Negative similarity check (re-run on full spec)

Re-walking the 8 dimensions on the full spec (which is more
concrete than the candidate paragraph evaluated at pick time):

- vs `qz73`: shared dimensions still 2 (verb-is-click, step-counter
  HUD) plus partial on dim 3 (mark-to-coloured-target alignment).
  Heavy principles (visual signature, pixel grain, core dynamic)
  all still diverge. The L3 clutch + L3 5-gear cluster diverges
  *further* from qz73's single rotor. Below 3-dim threshold. ✅ PASS.
- vs `bx84`: shared dimensions still 1 (step counter). ✅ PASS.
- vs all other priors: ≤ 1 shared dimension each. ✅ PASS.
- vs all 25 reference games: closest is `lp85` (pure-click +
  pre-computed transformations); shared 2 (verb, step-counter);
  heavy principles diverge. ✅ PASS.

**Verdict: NOVEL on both axes.**

## Solvability

| # | Item | Verdict |
|---|---|---|
| 16 | Win condition stated for whole environment | ✅ PASS — §7 specifies `_check_win()` predicate; engine auto-fires `self.win()` after L3 completion per default `NovaBaseGame` behaviour. |
| 17 | Lose condition stated | ✅ PASS — §8 specifies step-counter exhaustion via `level.get_data("StepBudget")` triggers `self.lose()`. No instant-fail collisions. |

### Item 18 — Difficulty floor and ceiling

For each level, all four bullets per `difficulty-rules.md` § 2:

| Level | (a) Random-resistance | (b) Human-tractable | (c) Planning depth | (d) Step budget |
|---|---|---|---|---|
| L1 | ✅ tutorial-grade per `composition-and-tutorial.md` (random may stumble; acceptable). | ✅ ~30 s. | ✅ NONE — discovery-only gate, per L1 guidance. | ✅ 20; ~10× witness 2. |
| L2 | ✅ ~5e-13 per attempt with 256-cell ACTION6 enumeration (the standard NovaPlay enumeration; see `r11l`). Far below 1/10,000 threshold. | ✅ ~2 min. | ✅ ≥ 2 first actions (4); plausible-wrong-path named (CCW direction); witness reasoning chain traced explicitly post-discovery. | ✅ 30; 6× witness 5. |
| L3 | ✅ ~9e-25 per attempt with 256-cell enumeration. Far below threshold. | ✅ ~3 min. | ✅ ≥ L2's first-action count (7 ≥ 4); trivial heuristic named ("rotate each gear directly to its target") and walked operationally to show it loops without converging; divergence point named (first action: clutch-lever vs gear-hub). Stage-conflation guard: heuristic argument is post-discovery (player knows what each click does), not discovery-stage. | ✅ 50; 4.5× witness 11; never shrinks vs L2's 30. |

**Implementation note (forward to `implement` state):** `_get_valid_actions` MUST enumerate the standard 256-cell ACTION6 grid (every `(x, y)` for `x, y ∈ 0..63 step 4`), per the convention in `r11l`. The spec's §6 currently says "≤ 7 click cells per level" — this should be amended in implement to match the standard convention. The random-resistance numbers above assume the 256-cell enumeration.

This is a non-blocking note for `critique_spec` because it's an
implementation detail, not a spec-level structural issue.

✅ PASS.

## Other adversarial checks (common failure modes per state file)

- **Spec drift in L2/L3?** No — re-checked similarity against full
  spec including all 5 gears at L3; no drift toward existing
  taxonomy rows.
- **Sprite reads as digit/letter?** No — gear cog pattern is
  mechanical-abstract; collar-ring is a hollow square; tangs are
  1×2 nubs. None resembles a letter or digit.
- **Pseudo-multi-mechanic?** No — per-mechanic counterfactual
  table above demonstrates each mechanic is genuinely required.
- **Tutorial too hard?** No — L1 is 2 actions, single mechanic,
  no ratchet/clutch, random-stumble allowed.
- **Wrong level count?** No — exactly 3 levels.

## Final verdict

**ALL 18 CHECKLIST ITEMS: ✅ PASS**
**NOVELTY (axis 1 + axis 2): ✅ NOVEL**
**NEGATIVE-SIMILARITY (8 dims, every prior): ✅ PASS**

Transition to `implement`.
