# Critique pass — qz73 spec

Reviewed `workspace/mechanic-spec.md` against
`design-constraints/checklist.md` (16 items) and re-ran both
similarity-checks against the full spec (not just the mechanic-
family name).

## §3.4 checklist (16 items)

### Format & structure
1. **Palette 0..15 + `-1` only.** ✅ PASS — every sprite uses
   palette base values in `{3, 5, 8, 14}` (overridden at runtime to
   `{6, 11, 12, 14, 15}` for tips and sockets). Lock-mark uses `[5,
   -1, 5]`. No out-of-range values.
2. **File structure matches `universal-scaffold.md`.** ✅ PASS — spec
   §3 (sprites), §4 (3 levels), §6 (HUD widget + game class)
   describes the file order: imports → sprite bank → levels →
   constants → HUD → game class. Class name `Qz73` (Pascal of `qz73`).
3. **`available_actions` is a subset of `[1..7]`.** ✅ PASS — spec
   §5 specifies `[5, 6]`.
4. **Exactly 3 `Level(...)` entries.** ✅ PASS — spec §4 lists L1,
   L2, L3 only. No "level 4+".
5. **4-character ID, not reference, not prior.** ✅ PASS — `qz73`,
   verified in `mechanic-pick.md` against the 25-game reserved list
   AND `prior-games/index.md` (which lists only `kf42`).

### §3.4 priors & constraints
6. **Mechanics draw only from the four allowed prior categories.**
   ✅ PASS — spec §2 declares Objectness + Basic Geometry/Topology
   (cyclic-permutation group action). Physics and Agentness are
   deliberately not used.
7. **NO letters, digits-as-glyphs, real-world clipart, cultural
   conventions.** ✅ PASS with one note. Hub (5×5 grey block),
   tip-pieces (3×3 coloured squares), socket-rings (5×5 hollow
   rings), lock-mark (4 black corner pixels) are all abstract
   geometric primitives. The 8-slot ring layout could superficially
   suggest a clock face, but: (a) no numerals; (b) no hour/minute
   hand structure; (c) tips do not all occupy all 8 positions in any
   level (3, 3, and 5 tips in L1/L2/L3 respectively); (d) tips and
   sockets are visually heterogeneous (different colours, filled vs
   hollow). The structure is closer to a polygonal vertex ring than
   a clock face. Acceptable per `forbidden-elements.md`'s
   "ABSTRACT shapes resembling … letters/objects are OK only if they
   are not RECOGNISABLE as the language/object" rule.
8. **At least TWO distinct mechanics.** ✅ PASS — Mechanic 1:
   ACTION5 = global cyclic shift of unlocked tips. Mechanic 2:
   ACTION6 click = toggle a tip's lock-state. Both required for L3.
9. **Level 1 is a tutorial: one mechanic, reduced state, no
   on-screen text.** ✅ PASS — L1 has 3 tips + 3 sockets, lock
   mechanic available but never required; ACTION5 alone solves it
   in 2 presses. No text. State space is the smallest possible
   (smallest tip count for "non-trivial-but-still-tutorial").
10. **Later levels compose earlier mechanics, not just scale.**
    ✅ PASS — L2 introduces the lock; L3 requires interleaving
    lock + rotate. L3 is NOT "L2 with more pieces" — its
    composition rule is explicit (no all-rotate-no-lock solution
    exists; no all-lock-no-rotate solution exists; only interleave
    works). L3 has 5 tips vs L2's 3 (more pieces) AND requires
    composition (the qualitative new requirement).

### Novelty
11. **Mechanic family absent from
    `taxonomy-of-25-games.md`.** ✅ PASS — `radial-cycle-lock` is
    not in the taxonomy. The 8 closest entries (ar25, cd82, cn04,
    dc22, lp85, s5i5, tr87, vc33) all involve rotation /
    cycling / per-cell mutation but with concretely different verbs
    (per-piece rotation; basket-on-ring; row-shift permutation;
    walk-cycler). Spec §9 articulates the distinguishing rule
    against each. I cross-checked against the deeper
    `deep-analysis/<id>-deep-analysis.md` evidence layer for ar25,
    cn04, cd82, and lp85: the deep-analysis confirms each of these
    has an avatar-or-cursor selecting a single object to act on,
    whereas qz73's ACTION5 is a global verb with no per-piece
    selection.
12. **Mechanic family absent from `prior-games/index.md`.**
    ✅ PASS — the only prior is `kf42` (tether-pawn-cycle). No
    overlap on family tag.
13. **Distinguishing rule articulated for any near-miss.** ✅ PASS
    — spec §9 has 8 concrete distinguishing-rule lines, each
    naming the specific differing axis (per-piece vs global
    rotation; cyclic shift vs hard-coded permutation; cycling
    SYMBOLS vs cycling POSITIONS; etc.).

### Solvability
14. **Win condition for the environment as a whole.** ✅ PASS — spec
    §7 gives a concrete predicate `_win_check()` returning bool;
    the predicate is testable from outside the class. The
    environment auto-wins after L3 completes (per `NovaBaseGame`'s
    auto-win-on-last-level behaviour, modelled on cn04).
15. **Lose condition stated.** ✅ PASS — spec §8: step counter
    exhaustion. No hazards. Single, deterministic, testable.
16. **Plain-words L1 strategy ≤ 1-2 minutes.** ✅ PASS — spec §4 L1
    description states "after exactly 2 ACTION5 presses the tips
    reach `{2, 4, 6}`". Two button presses; clearly under 1 minute
    even for a hesitant human.

## Re-run novelty (full-spec view)

### `similarity-check.md` matrix (positive test)
- Family-level overlap with: ar25, cd82, cn04, dc22, lp85, s5i5,
  tr87, vc33 (all rotation/cycling/permutation games).
- Description-level: each near-miss differs on at least one of
  WIN-CONDITION / PRIMARY-ACTION / PRIMARY-CONSTRAINT axes:
  - ar25 / cn04: PRIMARY-ACTION differs (per-piece rotation vs
    global rotation).
  - lp85: PRIMARY-ACTION differs (multiple buttons each with
    distinct permutation tables vs one repeated cyclic shift).
  - tr87: PRIMARY-ACTION differs (cycle SYMBOL identity vs cycle
    POSITION assignment).
  - vc33: PRIMARY-ACTION differs (local row-pair swap vs global
    cyclic shift).
  - dc22: PRIMARY-ACTION differs (walk-on-trigger vs ACTION5).
  - cd82: PRIMARY-ACTION differs (basket-on-ring NAVIGATION via
    ACTION1-4 vs whole-rotor rotation via ACTION5).
  - s5i5: PRIMARY-ACTION differs (per-colour-class rotation vs
    whole-rotor rotation).
- Distinguishing rule: concrete, names the differing axis.
- Verdict: **NOVEL**.

### `negative-similarity-check.md` 8-dimension test against kf42
Only one prior to compare against. Counted shared dimensions:

| # | Dimension | Shared? |
|---|---|---|
| 1 | What is on the board | NO |
| 2 | What the player physically does | NO |
| 3 | What the level is asking for | marginally — both reduce to "coloured movable on coloured target", but kf42's verb is *navigate two pawns under tether* and qz73's verb is *cyclic-permute tip positions until socket constraints satisfy*. Counts as ~0.5. |
| 4 | What kills the player | YES (step counter — universal; per the negative-check rule, this dimension alone does not contribute to rejection) |
| 5 | Cast of supporting elements | NO (pawns + target pads vs hub + spokes + sockets + lock-marks) |
| 6 | Visual signature | NO (open black arena, sparse {red, blue} pawns vs grey-bg radial structure with {orange, green, purple, magenta, yellow} tips) |
| 7 | Pixel grain | NO (1×1 single cells vs 3×3 tip blocks + 5×5 hollow socket rings + 5×5 hub) |
| 8 | Core dynamic | NO (path-planning under tether vs cyclic-permutation constraint solving) |

Total non-trivially shared dimensions: ~0.5 (only "goal-shape
match coloured-movable-to-coloured-target", marginal). Threshold for
rejection: 3+. **Verdict: NOVEL** by a wide margin. The candidate
diverges on every named Principle (palette, pixel-grain, core
dynamic).

## Final verdict

**PASS** — every checklist item passes; both similarity-checks
return NOVEL. Transition to `implement`.

## Minor notes for the implementer (non-blocking)

- Pick the L3 colour assignment so that the spec's stated
  "no all-rotate-no-lock witness, no all-lock-no-rotate witness, but
  an interleave does work" property holds. The spec describes L3
  parametrically; a concrete colour list satisfying this should be
  verified before smoke-testing.
- For `_get_valid_actions`, ACTION6 candidates' `(x, y)` should be
  computed in DISPLAY space (not grid space) using the camera scale.
  cn04's `display_to_grid` round-trip is a useful pattern.
- The lock-mark overlay's `interaction=InteractionMode.REMOVED` /
  `INTANGIBLE` toggle (rather than `set_visible(False)`) is the
  cleaner pattern per `universal-scaffold.md`'s "Two-sprite swap"
  note — the lock-mark stays inside the level for inspection but
  doesn't render or collide while inactive.
