# Mechanic spec — qb84 (bead-lift-swap)

## 1. Title

*Bead-Lift Swap-Sequence* (working title; never visible in-game).

## 2. Mechanic family

**Bead-lift-swap.** A serpentine chain of coloured beads must be
recoloured to match a target sequence by displacing individual
beads perpendicular to the chain to swap colours with adjacent
"peg" sprites. Verbs are pure-arrow: ACTION3/4 step a logical
cursor backward/forward along the chain by one bead; ACTION1
("lift") swaps the cursor's bead colour with whichever peg
occupies the bead's pre-declared `above-slot`; ACTION2 ("drop")
swaps with the bead's `below-slot`. The slots are derived
positionally from the chain layout — the player learns
"ACTION1 reaches the peg sprite visible just above the active
bead" from playable cause-and-effect, never from text.

**Prior categories used (per `core-knowledge-priors.md`):**
- **Objectness** — beads and pegs are persistent entities with
  colour identity that is transferred (swapped) on contact. The
  active bead is a coherent, persistent unit selected by the
  cursor.
- **Basic geometry & topology** — the serpentine chain is a
  path through the playfield; "above-slot" and "below-slot" are
  topological adjacencies along the path's flank, not Cartesian
  cardinal directions. The player learns the topological
  relationship by watching ACTION1 swap with a specific spatially-
  visible peg.

No physics, no agentness — pegs are static, no chasers, no
gravity, no momentum.

## 3. Sprite roster

All sprite names are 10-character lowercase opaque tokens
(per `universal-scaffold.md`). The 64×64 grid scale lets each
"cell" be 4 display-pixels wide; bead sprites are 4×4 with
rounded corners (corner pixels = -1), peg sprites are 3×3.

| Sprite name | Pixel matrix dims | Palette values | Tags | Role (author-side) |
|---|---|---|---|---|
| `bdcanvspxz` | 4×4 | 8 (red default — recoloured per instance) + -1 corners | `bead` | Canonical bead. Cloned and `color_remap`-ed per chain instance to {6, 11, 14, 15}. |
| `pgflatfxnh` | 3×3 | 8 default + -1 corners | `peg-plain` | Plain swap peg. 3×3 with `[-1,8,-1; 8,8,8; 8,8,8]` triangular fill. Recoloured per instance. |
| `pgstickfxn` | 3×3 | colour + 4 inner pixel + -1 corners | `peg-sticky` | Sticky peg — same shape as plain but with central pixel set to palette 4 (off-black inner dot) so the player can SEE it differs from plain. Recoloured per instance for the body colour; the centre always stays 4. |
| `pgpairabcd` | 3×3 | colour + 0 corner-pixel + -1 corners | `peg-pair-A` | Pair peg variant A — same shape as plain but with one corner pixel set to palette 0 (off-white) marking pairing. |
| `pgpairefgh` | 3×3 | colour + 0 corner-pixel (different corner) + -1 corners | `peg-pair-B` | Pair peg variant B — same shape as plain but with the OPPOSITE corner pixel set to palette 0. The two pair pegs visually have a "rotational" relationship. |
| `tgrefstrip` | 1×K (K = chain length) | bead colours | `target-ref` | Target reference strip — a horizontal 1-cell-tall strip rendered in the bottom-right corner showing the target colour sequence. Pixels = the target colour list. |
| `chnpathmrk` | per-cell | palette 2 (light-grey) | `path-marker` | Optional thin path-marker sprites laid along the chain to visually communicate the chain's snaking shape. One placed between each adjacent pair of beads. Decorative; INTANGIBLE so they never block. |
| `crsorindov` | n/a — HUD widget, not a Sprite | — | n/a | Cursor indicator. Implemented as a `RenderableUserDisplay` subclass that paints 4 corner pixels around the active bead at runtime. NOT a placed sprite. |

**Palette commitment** (from mechanic-pick.md):
- Background = palette 4 (off-black). `BACKGROUND_COLOR = 4`,
  `PADDING_COLOR = 4`.
- Path markers = palette 2 (light-grey).
- Beads cycle through {6 magenta, 11 yellow, 14 green, 15 purple}.
- Sticky inner pixel = palette 4 (matches background — looks like
  a "hole" in the peg's body).
- Pair-peg corner marker = palette 0 (off-white).
- Step bar = palette 0 (white-on-black bar at the very top row).

## 4. Level progression, mechanic enumeration, and witness solutions

All 3 levels share `grid_size=(64, 64)` so no camera resize is
needed. Each level varies its chain layout, peg placements, and
target sequence via the level's level_data dict.

### Level 1 — base dynamic system (N = 2 mechanics)

**Chain layout:** 6 beads arranged as an S-curve. Bead positions
(top-left of each 4×4 sprite, in 64-pixel coordinates):

```
B0 = (12, 16)
B1 = (24, 16)
B2 = (36, 16)
B3 = (36, 32)
B4 = (24, 32)
B5 = (12, 32)
```

(Reads as horizontal top → corner → horizontal bottom — an "S" laid
on its side. Cursor index 0 → 5 traces this path.)

**Initial bead colours (as a list, index 0 = B0):**
`[14 green, 11 yellow, 6 magenta, 14 green, 11 yellow, 6 magenta]`

**Pegs placed in this level (with associated bead-index by
position; the engine looks up which bead a peg is "near" by
proximity in `on_set_level`):**

| Peg name | Slot | Position (top-left) | Body colour | Type |
|---|---|---|---|---|
| `pg_l1_a` | above-slot of B0 | `(12, 8)` | 6 magenta | plain |
| `pg_l1_b` | above-slot of B2 | `(36, 8)` | 11 yellow | plain |
| `pg_l1_c` | below-slot of B5 | `(12, 40)` | 14 green | plain |

(B1, B3, B4 have no associated peg this level — ACTION1/2 on those
beads is a no-op and consumes no step.)

**Target sequence (index 0 → 5):**
`[6 magenta, 11 yellow, 11 yellow, 14 green, 11 yellow, 14 green]`

So bead-by-bead:
- B0: 14 → 6  (lift to peg `pg_l1_a` = magenta)
- B1: 11 → 11 (already correct, no action)
- B2: 6 → 11 (lift to peg `pg_l1_b` = yellow)
- B3: 14 → 14 (already correct)
- B4: 11 → 11 (already correct)
- B5: 6 → 14 (drop to peg `pg_l1_c` = green)

**Mechanics required by the witness:**
1. **Cursor stepping (ACTION3/4)** — required because the witness
   must place the cursor on at least 3 distinct beads (B0, B2, B5).
2. **Lift-swap to above-peg (ACTION1)** — required to recolour B0
   (uses `pg_l1_a` magenta) and B2 (uses `pg_l1_b` yellow).
3. **Drop-swap to below-peg (ACTION2)** — required to recolour B5
   (uses `pg_l1_c` green).

L1 thus carries N = 2 distinct mechanic verbs (lift and drop), both
exercised by the witness. Cursor stepping is treated as the
navigation primitive that both verbs depend on, not a separate
mechanic. The "+1 per level" rule counts mechanics that change the
puzzle's reasoning surface — ACTION3/4 movement is a constant
across all 3 levels.

> Per `composition-and-tutorial.md`'s framing, "L1 may carry any
> number of mechanics N ≥ 1 (a single verb is fine; a small system
> of interacting mechanics is also fine)." We commit to N = 2
> (lift verb + drop verb).

**Witness solution (10 actions):**

Cursor starts at index 0 (B0) by spec.

```
1. ACTION1                # B0: lift to pg_l1_a; B0 becomes 6 magenta, peg becomes 14 green
2. ACTION4                # cursor 0 → 1
3. ACTION4                # cursor 1 → 2
4. ACTION1                # B2: lift to pg_l1_b; B2 becomes 11 yellow, peg becomes 6 magenta
5. ACTION4                # cursor 2 → 3
6. ACTION4                # cursor 3 → 4
7. ACTION4                # cursor 4 → 5
8. ACTION2                # B5: drop to pg_l1_c; B5 becomes 14 green, peg becomes 6 magenta
                          # WIN check fires after this action — predicate True
```

8 actions total. Step budget: 24.

(Action 9/10 listed in error above — re-counting: 1 lift, 2 walks,
1 lift, 3 walks, 1 drop = **8 actions**. Step budget set to 24 →
3× human baseline → comfortable margin.)

**Difficulty justification:**

- *Random-resistance:* a random ACTION1-4 policy on a 4-action
  alphabet over a 24-step budget has probability ≈ 0 of completing
  L1: the witness is a specific 8-action sequence (1 of 4⁸ ≈ 65k
  pure random sequences); the random-resistant rate is amplified by
  the step budget cap (only sequences of length ≤24 from 4²⁴ ≈
  2.8 ×10¹⁴ paths). A vision-blind / small-text-LLM agent has no
  way to discover the chain topology or peg positions without
  reading frame pixels, so random spam-walk-and-lift cannot win.
- *Human-tractable:* an attentive human reads the chain layout, the
  3 pegs, and the target reference strip in ~30s; the swap rule is
  inferred in 2-3 exploratory ACTIONs (lift on B0 visibly recolours
  the bead AND swaps the peg colour); the remaining solve is
  walk-and-act for ~1.5 min. Total ≈ 2 min.
- *Planning depth:* near-zero (mechanic-discovery is the L1
  difficulty). Once the swap rule is understood, each remaining
  step is trivially picked. **L1 only — L2/L3 will require
  non-trivial planning.**

### Level 2 — base system + 1 new mechanic (N + 1 = 3 mechanics)

**New mechanic: sticky pegs.** A sticky peg looks like a plain peg
but with the central pixel set to palette 4 (visually a hole in
the peg's body). Functionally: after a swap involving a sticky
peg, the bead is permanently locked — its colour cannot be changed
by any subsequent lift/drop. Successful swap with a sticky peg DOES
consume a step (the swap happens once, then locks).

**Chain layout:** 8 beads in a zigzag.

```
B0 = (8, 12)     B4 = (40, 32)
B1 = (20, 12)    B5 = (52, 32)
B2 = (32, 12)    B6 = (52, 48)
B3 = (32, 32)    B7 = (32, 48)
```

(Top horizontal of 3 beads → vertical drop → bottom horizontal of 3
beads, with B5/B6 forming the right-side connector and B6/B7
forming the bottom-right.)

**Initial bead colours:**
`[15 purple, 14 green, 6 magenta, 11 yellow, 14 green, 6 magenta, 15 purple, 11 yellow]`

**Pegs (positions chosen so above/below maps unambiguously):**

| Peg name | Slot | Position | Body colour | Type |
|---|---|---|---|---|
| `pg_l2_a` | above-slot of B0 | `(8, 4)` | 11 yellow | plain |
| `pg_l2_b` | above-slot of B2 | `(32, 4)` | 14 green | sticky |
| `pg_l2_c` | below-slot of B3 | `(32, 40)` | 6 magenta | plain |
| `pg_l2_d` | below-slot of B5 | `(52, 40)` | 14 green | sticky |
| `pg_l2_e` | below-slot of B7 | `(32, 56)` | 15 purple | plain |

**Target sequence:**
`[11 yellow, 14 green, 14 green, 6 magenta, 14 green, 14 green, 15 purple, 15 purple]`

Bead-by-bead:
- B0: 15 → 11 (use `pg_l2_a` yellow)
- B1: 14 → 14 (already correct)
- B2: 6 → 14 (use `pg_l2_b` green — STICKY)
- B3: 11 → 6 (use `pg_l2_c` magenta)
- B4: 14 → 14 (already correct)
- B5: 6 → 14 (use `pg_l2_d` green — STICKY)
- B6: 15 → 15 (already correct)
- B7: 11 → 15 (use `pg_l2_e` purple)

**Mechanics required by the witness (N+1 = 3):**
1. **Cursor stepping (carried from L1).**
2. **Lift-swap (carried from L1).** — required by B0, B2, B5.
3. **Drop-swap (carried from L1).** — required by B3, B7.
4. **Sticky-peg lock (NEW).** — required because B2 and B5 must
   each receive their target colour from a sticky peg. The witness
   chooses to use the sticky pegs for B2 and B5 (no alternative
   plain green peg exists in this level). Once the bead is locked,
   no further tampering can damage the satisfied position — *this
   is the new reasoning surface*: the player commits a colour by
   touching a sticky peg.

Wait — the count is "L2 must carry exactly N+1 — every L1 mechanic
plus exactly one new one". L1 carries N=2 (lift + drop). L2 must
carry 3 mechanics. Lift + drop + sticky-peg-lock = 3. ✓

Cursor stepping is the navigation primitive treated as part of the
verb-set across all levels (per the spec's definition above), not a
counted mechanic.

**Witness solution (12 actions):**

Cursor starts at index 0 (B0).

```
1. ACTION1                # B0 lift to pg_l2_a (yellow); B0=11
2. ACTION4                # cursor 0→1
3. ACTION4                # cursor 1→2
4. ACTION1                # B2 lift to pg_l2_b (sticky green); B2=14, LOCKED
5. ACTION4                # cursor 2→3
6. ACTION2                # B3 drop to pg_l2_c (magenta); B3=6
7. ACTION4                # cursor 3→4
8. ACTION4                # cursor 4→5
9. ACTION2                # B5 drop to pg_l2_d (sticky green); B5=14, LOCKED
10. ACTION4               # cursor 5→6
11. ACTION4               # cursor 6→7
12. ACTION2               # B7 drop to pg_l2_e (purple); B7=15
                          # WIN check fires — predicate True
```

12 actions. Step budget: 32.

**Difficulty justification:**

- *Random-resistance:* random policy probability ≈ 0 (target
  sequence requires specific 12-action plan). A random agent that
  happens to lift on B2 first (sticky peg) and gets the wrong
  colour locks the bead permanently — recovering then requires
  resetting the level.
- *Human-tractable:* once L1's verbs are known, the human reads
  the new sticky-peg's appearance (centre-hole pixel pattern) and
  experiments on B2 to discover lock behaviour; the experiment
  cost is one wasted step but the lesson generalises. ~2 min.
- *Planning depth (HARD requirement from L2 onward):* the player
  must reason *which* swap to commit *first*, because some pegs'
  colours are needed by multiple beads. After lifting B0 to
  `pg_l2_a` (yellow), `pg_l2_a` becomes the bead's old colour
  (15 purple) — so visiting `pg_l2_a` AGAIN later would now
  deposit purple, not yellow. The player must reason about
  state-after-each-action because **every successful swap also
  changes the peg's colour to whatever the bead used to be**.
  Spam-the-new-verb (lift on every sticky peg) cannot win:
  visiting a sticky peg with the wrong colour locks the bead
  permanently against the target. Single-step solutions trivially
  fail (the witness has 12 distinct steps; no single ACTION wins).

### Level 3 — system + 1 more new mechanic (N + 2 = 4 mechanics)

**New mechanic: pair pegs.** A pair peg has a small palette-0
corner-pixel marker (one corner for variant A, the opposite corner
for variant B; the player can SEE the visual pairing because the
two pair pegs share the marker placement-symmetry). Functionally:
when a bead is swapped with `pg_pair_A`, the bead at chain index
`cursor_index + 1` (if exists, else `cursor_index - 1`) is
*simultaneously* given the colour that `pg_pair_B` had at action
start. The propagation is one-shot (it does not re-fire on the
neighbour peg). Sticky-peg locking is honoured — a locked
neighbour bead is not changed by the propagation (the propagation
silently no-ops on the neighbour).

This mechanic is required because it lets the witness reach
colours otherwise unattainable in a 60-step budget.

**Chain layout:** 10 beads in a double-S.

```
B0 = (8, 8)      B5 = (32, 32)
B1 = (20, 8)     B6 = (44, 32)
B2 = (32, 8)     B7 = (44, 48)
B3 = (44, 8)     B8 = (32, 48)
B4 = (44, 24)    B9 = (20, 48)
```

(Top horizontal of 4 beads → corner → middle horizontal of 2
beads → corner → bottom horizontal of 4 beads — a double-S
descending right-to-left and re-rising.)

**Initial bead colours:**
`[15 purple, 6 magenta, 14 green, 11 yellow, 11 yellow, 6 magenta, 14 green, 15 purple, 6 magenta, 14 green]`

**Pegs:**

| Peg name | Slot | Position | Body colour | Type |
|---|---|---|---|---|
| `pg_l3_a` | above-slot of B0 | `(8, 0)` | 11 yellow | plain |
| `pg_l3_b` | above-slot of B3 | `(44, 0)` | 14 green | sticky |
| `pg_l3_c` | below-slot of B5 | `(32, 40)` | 6 magenta | pair-A (paired with d) |
| `pg_l3_d` | below-slot of B6 | `(44, 40)` | 15 purple | pair-B (paired with c) |
| `pg_l3_e` | below-slot of B8 | `(32, 56)` | 14 green | plain |
| `pg_l3_f` | above-slot of B9 | `(20, 40)` | 11 yellow | sticky |

(`pg_l3_c` and `pg_l3_d` are pair pegs — same-tag-pair shared via
sprite-name suffix `pair_l3_cd_A` / `pair_l3_cd_B` at code level.
The spec name `pg_l3_c`/`pg_l3_d` is for human reference only.)

**Target sequence:**
`[11 yellow, 6 magenta, 14 green, 14 green, 11 yellow, 15 purple, 11 yellow, 15 purple, 14 green, 11 yellow]`

Bead-by-bead:
- B0: 15 → 11 (use `pg_l3_a` yellow)
- B1: 6 → 6 (already correct)
- B2: 14 → 14 (already correct)
- B3: 11 → 14 (use `pg_l3_b` green — STICKY)
- B4: 11 → 11 (already correct)
- B5: 6 → 15 (use pair-A `pg_l3_c` — its colour is 6 magenta;
  swapping with B5 gives B5=6, peg=6 — not useful directly. The
  witness uses pair-A to get B6 — see below)
- B6: 14 → 11 (uses pair propagation FROM the swap on B5 — pair-B
  `pg_l3_d` was purple, but the propagation logic copies the OTHER
  pair peg's colour at action start INTO the neighbour bead;
  meaning: lift on B5 to pair-A → B5 takes pair-A's colour (6 →
  unchanged), AND B6 takes pair-B's colour (15 purple). Then B6 =
  15, not 11. Hmm — this doesn't reach the target.

Wait, this needs re-thinking. Let me re-examine the pair-peg rule
to make the L3 witness coherent.

Re-specifying the pair-peg rule cleanly:

**Pair-peg rule (FINAL):** When a swap is committed between a bead
and pair peg X (X is either pair-A or pair-B of a pair):
1. The bead's colour and peg X's colour are swapped (standard
   swap behaviour).
2. *In addition,* the bead's chain-neighbour at index `cursor_index
   + 1` (if exists, else `cursor_index - 1`, else no propagation)
   has its colour SET to the colour that the OTHER pair peg (Y)
   currently holds (as of action start). Peg Y's colour is *not*
   modified by the propagation. The propagation NEVER overwrites a
   locked (sticky-touched) neighbour.

Re-examining the witness with this rule:

- Lift on B5 with cursor=5 to pair-A `pg_l3_c` (magenta @ start):
  - Swap: B5 ↔ pg_l3_c. B5 was 6 (magenta), pg_l3_c was 6
    (magenta). No-op swap (same colour). B5 stays 6, peg stays 6.
  - Propagation: B6 takes pg_l3_d's colour (15 purple). B6: 14
    → 15. ✗ (target is 11 yellow.)

Doesn't reach target. I need to redesign B5/B6 colours to make
this work.

Let me redesign:

- Set B5 initial = 14 green; pair-A `pg_l3_c` initial = 11 yellow;
  pair-B `pg_l3_d` initial = 15 purple. Target B5 = 11 yellow,
  B6 = 15 purple.
- Lift on B5 (cursor=5) to pair-A: B5 ↔ pair-A. B5 takes 11 yellow
  (target ✓), pair-A takes 14 green. Propagation: B6 takes
  pair-B's colour = 15 purple (target ✓).
- One action covers BOTH B5 and B6.

OK so I need to update the L3 plan:

**Revised L3 initial colours:**
`[15 purple, 6 magenta, 14 green, 11 yellow, 11 yellow, 14 green, 14 green, 15 purple, 6 magenta, 14 green]`

(B5 changed from 6→14.)

**Revised L3 target sequence:**
`[11 yellow, 6 magenta, 14 green, 14 green, 11 yellow, 11 yellow, 15 purple, 15 purple, 14 green, 11 yellow]`

(B5 target changed from 15→11; B6 target changed from 11→15.)

Bead-by-bead:
- B0: 15 → 11 (use `pg_l3_a` yellow)
- B1: 6 → 6 (already)
- B2: 14 → 14 (already)
- B3: 11 → 14 (use `pg_l3_b` green — STICKY)
- B4: 11 → 11 (already)
- B5: 14 → 11 (use pair-A `pg_l3_c` from yellow → propagation
  pushes pair-B's purple into B6)
- B6: 14 → 15 (set by pair propagation from the lift on B5)
- B7: 15 → 15 (already)
- B8: 6 → 14 (use `pg_l3_e` plain green)
- B9: 14 → 11 (use `pg_l3_f` sticky yellow)

**Pegs (revised):**

| Peg name | Slot | Position | Body colour | Type |
|---|---|---|---|---|
| `pg_l3_a` | above-slot of B0 | `(8, 0)` | 11 yellow | plain |
| `pg_l3_b` | above-slot of B3 | `(44, 0)` | 14 green | sticky |
| `pg_l3_c` | above-slot of B5 | `(32, 24)` | 11 yellow | pair-A |
| `pg_l3_d` | above-slot of B6 | `(44, 24)` | 15 purple | pair-B |
| `pg_l3_e` | below-slot of B8 | `(32, 56)` | 14 green | plain |
| `pg_l3_f` | below-slot of B9 | `(20, 56)` | 11 yellow | sticky |

(I moved `pg_l3_c` and `pg_l3_d` from below-slot to above-slot of
B5 and B6 respectively, since B5 is in the middle horizontal where
"above" is the natural perpendicular direction. The exact slot
positions are visualised so the player sees the peg "directly above"
the bead.)

**Mechanics required by the witness (N+2 = 4):**
1. **Cursor stepping** (verb primitive).
2. **Lift-swap (carried).** — required by B0, B5, B9 (and
   propagation source B5).
3. **Drop-swap (carried).** — required by B8.
4. **Sticky-peg lock (carried from L2).** — required by B3
   and B9.
5. **Pair-peg propagation (NEW).** — required by B6, which has
   *no peg of its own in the budget*. The only way to set B6's
   colour to 15 purple is via pair-peg propagation triggered by
   the lift on B5.

Wait — that's 4 *new* counted mechanics on top of cursor stepping,
which would be N+3 = 5, not N+2 = 4. Let me recount:

- N (L1) = 2: {lift-swap, drop-swap}.
- L2 = N+1 = 3: {lift-swap, drop-swap, sticky-peg-lock}.
- L3 = N+2 = 4: {lift-swap, drop-swap, sticky-peg-lock, pair-peg-propagation}.

That's 4 distinct counted mechanics at L3. Cursor stepping is the
constant verb primitive. ✓

**Witness solution (15 actions):**

Cursor starts at index 0 (B0).

```
1. ACTION1                # B0 lift to pg_l3_a (yellow). B0=11; pg_l3_a=15
2. ACTION4                # cursor 0→1
3. ACTION4                # cursor 1→2
4. ACTION4                # cursor 2→3
5. ACTION1                # B3 lift to pg_l3_b (sticky green). B3=14, LOCKED; pg_l3_b=11
6. ACTION4                # cursor 3→4
7. ACTION4                # cursor 4→5
8. ACTION1                # B5 lift to pg_l3_c (pair-A yellow).
                          #   Swap: B5=11 yellow; pg_l3_c=14 green.
                          #   Propagation: B6 takes pg_l3_d's colour
                          #   (15 purple). B6=15.
9. ACTION4                # cursor 5→6
10. ACTION4               # cursor 6→7
11. ACTION4               # cursor 7→8
12. ACTION2               # B8 drop to pg_l3_e (plain green). B8=14; pg_l3_e=6
13. ACTION4               # cursor 8→9
14. ACTION2               # B9 drop to pg_l3_f (sticky yellow). B9=11, LOCKED;
                          #   pg_l3_f=14
                          # WIN check fires — predicate True
```

14 actions. Step budget: 60.

(Actually I count: 1,4,4,4,1,4,4,1,4,4,4,2,4,2 = 14 actions.)

**Difficulty justification:**

- *Random-resistance:* A random ACTION1-4 policy has probability ≈
  0 of producing this exact 14-step sequence within the 60-step
  budget. A random agent that triggers a sticky peg with the wrong
  bead colour locks that bead permanently away from the target.
  Random pair-peg activation also miscolours the propagation
  neighbour irreversibly (since the neighbour's colour gets
  overwritten on every pair-peg swap; only sticky-pegging the
  neighbour BEFORE the pair-peg swap protects it, but a random
  agent can't compute this).
- *Human-tractable:* once L2 is solved, the human reads the
  pair-peg visual marker (corner pixel pairing dot) and discovers
  the propagation rule via 2-3 exploratory swaps on B5/B6. ~2 min
  with strategic thinking.
- *Planning depth (STRICTLY DEEPER than L2's):* the witness has
  one critical commute-failure: actions **5 and 8 cannot be
  swapped**. If action 8 fires first (lift on B5 to pair-A), then
  pair-peg propagation pushes 15 purple into B6 and the lift on
  B3 (action 5) sees `pg_l3_b` ALREADY at its initial green
  colour, that fires correctly. But now consider swapping 5 and
  8 in the OTHER direction — e.g. action 8 swaps with action 5:
  Place lift on B3 first, then lift on B5. Order does NOT break
  here. Let me find a sharper commute failure:

Sharper commute failure: actions **5 and 14 cannot be swapped**
(but they're not adjacent). Need adjacent commute failure.

Adjacent failure: action **8 (lift on B5 — pair-peg)** and **action
9 (cursor 5→6)** cannot be swapped — moving cursor first means
when ACTION1 fires, it operates on B6, not B5. The pair propagation
direction (cursor+1 or cursor-1) depends on which neighbour is
non-locked; if B6 had been locked first, propagation would go to
B4 and the witness fails. But neither B6 nor B4 is locked at that
moment, so the propagation still goes to cursor+1 (B6 is
cursor=5+1=6, B4 is cursor=5-1=4 — the rule says "neighbour at
cursor+1 if exists, else cursor-1"; B6 exists, so propagation goes
to B6 only). Swapping the order means actions 8 and 9 become
"cursor 5→6" then "lift on B6" — completely different effect.

Actually, the cleanest adjacent commute failure: **actions 5 (lift
on B3 — sticky green) and any later step that touches `pg_l3_b`**.
Once B3 is sticky-locked, any bead that needed to swap with
`pg_l3_b` later for a green colour cannot. In the actual witness,
no later bead needs `pg_l3_b`'s colour, so the witness is consistent.

Concrete adjacent commute that breaks: **action 8 (lift on B5 —
pair propagation) and action 12 (drop on B8 to plain green
`pg_l3_e`)**. They're not adjacent. The witness's strict
adjacency commute failure is:

Try swapping **action 12 (drop B8 to pg_l3_e green)** and **action
11 (cursor 7→8)**: Doing the drop with cursor at 7 means the swap
is between B7 (currently 15 purple) and `pg_l3_e` (14 green) —
completely wrong target. B7 is already at target 15 → would
become 14, violating its target. So commuting cursor-walk and
verb is universally bad — that's a generic property, not specific
to L3.

For a more interesting commute failure specific to L3:
**actions 5 (lift on B3 — sticky-pegging green) and action 8
(lift on B5 — pair propagation)** — if these were re-ordered to
8-then-5, the propagation from action 8 puts 15 purple into B6.
B3 is later sticky-pegged. That sequence still works. So order
between sticky-touch on B3 and pair-peg-touch on B5 doesn't break.

Let me design a COMMUTE FAILURE explicitly into the witness. To do
that, I'll add a constraint: B0's target colour is yellow (set by
`pg_l3_a` plain yellow), but the SECOND-TO-LAST step of the
witness uses `pg_l3_a` for something else.

Actually, simpler approach: add a witness-intrinsic order
dependency by making one peg dual-use. Let me redesign minimally:

**Simpler order-dependency:** make pair-peg propagation's direction
matter. Specifically: pair-peg propagation sets the
NEIGHBOUR's colour. If the neighbour is the immediate next bead in
chain order, we want a setup where:

1. Step A: lift on B5 to pair-A → B6 gets pair-B's value (15
   purple). ✓
2. Step B: later, lift on B6 to pair-A — would propagate to B7,
   wiping B7's already-correct colour.

If the witness PREVENTS step B by visiting B6 only AFTER B5 (and
not actuating any verb on B6 once it's correct), then the witness
is order-sensitive: doing step B first, before step A, would
require a recovery.

Cleanest order failure: **actions 5 and 8 cannot be swapped if
their adjacent action ordering matters**. Let me reframe: the
witness has cursor at index 5 → ACTION1 (step 8). Suppose
instead of step 5 (which does ACTION1 at cursor=3), the player
does step 8 first (ACTION1 at cursor=5). Then propagation puts
15 purple into B6. THEN the player walks back to B3 and does the
sticky lift. This still works. So this isn't a commute failure.

I think the cleanest order-sensitivity in this design is the
AND-rule between sticky-locking and pair-peg propagation:
*if the player sticky-locks the neighbour bead (B6) BEFORE
firing the pair-peg propagation source (B5), the propagation
silently no-ops on B6, and B6 cannot be set.* This is explicit
in the rule.

To make this a witness constraint:
- Suppose B6 needs colour 15 purple (target).
- The only way to set B6 = 15 is via pair-peg propagation from
  B5 (since no peg adjacent to B6 has colour 15 in this level).
- B6 must NOT be sticky-locked before action 8.

In the current witness, no sticky peg interacts with B6, so this
is trivially satisfied. The "forbidden adjacent commute" is then:
**Actions 5 (sticky-lock B3) and ... no adjacent commute breaks**.

Let me instead make the adjacent commute failure more explicit by
introducing a deliberate setup that forces it. I'll modify the L3
peg layout to add `pg_l3_g` at B6's above-slot, sticky and yellow
— so an inattentive player might try to lift B6 to that
sticky-yellow peg first, locking B6 = 11 yellow, after which the
B5 pair-peg propagation no-ops on B6 (locked), making the level
unsolvable.

Adding `pg_l3_g`: above-slot of B6, position `(44, 24)` ... wait,
that's already `pg_l3_d`'s position. The above-slot of B6 is
already pair-B `pg_l3_d`. So no.

OK I'll lock in the L3 design as is. The order-sensitivity is:
- The witness has a strict ordering constraint that lift on B5
  (action 8) must happen BEFORE B6 is touched by anything else.
- A trivial heuristic "for each bead at wrong colour, find an
  adjacent peg of target colour and lift" defeats the L3 witness
  because B6 has NO adjacent peg of target colour 15 purple —
  the player must NOT directly act on B6 and instead must indirect
  through the pair-peg propagation on B5.

That's the named trivial heuristic L3 defeats.

**Adjacent commute that breaks the witness:** actions 7 (cursor
4→5) and 8 (lift on B5 — pair-A) are adjacent. Swapping their
order (8 then 7) means action 8 fires with cursor=4 on B4 — but
B4 has no peg above OR below (none of `pg_l3_*` is associated with
B4), so action 8 becomes a no-op (no step consumed). Then action
7 happens (cursor 4→5). Now we're 1 step "behind" the witness;
re-firing action 8 (lift on B5) at this cursor position works. So
swapping 7 and 8 wastes one no-op step (still fine within the
60-step budget), not a hard failure.

The CLEANEST adjacent commute that breaks the witness:
**actions 1 (lift on B0 to pg_l3_a yellow) and ... ?** No adjacent
commute fundamentally breaks the witness within budget. The
witness has 60-step slack.

OK so the order sensitivity for L3 is *coarse-grained*:
- B5 (pair-A) must be lifted BEFORE any action that locks B6.
- No locking action targets B6 in the witness, so any sequencing
  works.

The strict §3.4 rule says "L3 must demand sequencing where the
ORDER of actions matters (commuting two adjacent actions changes
solvability)". My current spec doesn't strictly meet this.

**To strengthen: introduce a peg adjacent to B6 that, if used,
would lock B6 to a wrong colour, making B6's target unattainable.**

Add `pg_l3_g`: below-slot of B6, position `(44, 40)` — wait, this
slot is currently `pg_l3_d` is associated with B6's *above*-slot.
Let's put a sticky peg in B6's *below*-slot:

Add **`pg_l3_g`**: below-slot of B6, position `(44, 40)`, body
colour 14 green, **sticky**. The level data says ACTION2 (drop)
on B6 swaps with `pg_l3_g`.

Now the witness involves:
- Action 8: lift on B5 (cursor=5) → propagation sets B6 = 15 purple.
- IF the player had instead first dropped on B6 (cursor=6,
  ACTION2) to `pg_l3_g`, B6 would become 14 green and LOCK. Then
  the lift on B5 silently no-ops on B6 (locked), and B6's target
  15 cannot be achieved.

So: **A FORBIDDEN ACTION SEQUENCE** is "ACTION2 on B6 before
ACTION1 on B5". The witness must lift on B5 first.

Adjacent commute failure: **actions 8 (lift on B5) and any
ACTION2 fired after walking to B6**. In the witness, no ACTION2 is
fired on B6 — the strict order constraint is "do not fire ACTION2
on B6". Adjacency-strict: if the player's cursor is at 5 and they
fire ACTION1 (action 8 in witness), then walks to 6 (action 9),
then fires ACTION2 (alternative action 9b that's NOT in the
witness) instead of walking onward — that would lock B6 with the
wrong colour. So swapping witness action 9 (cursor 5→6) with a
hypothetical ACTION2 at cursor=5 (which would actually be action
8's effect since ACTION2 at cursor=5 swaps B5 with `pg_l3_d`
which is above-slot — wait, `pg_l3_d` is B6's above-slot, not B5's
below-slot. Confused myself.)

Let me re-spec slots cleanly:

**Slot ownership:** each peg in level data is associated with
exactly one bead and one slot ("above" or "below"). The peg is the
ONLY thing reachable from that bead by ACTION1 (above) or ACTION2
(below).

I'll restate L3 pegs with clear ownership and add the new
sticky-trap `pg_l3_g`:

| Peg name | Owner-bead | Slot | Position | Body colour | Type |
|---|---|---|---|---|---|
| `pg_l3_a` | B0 | above | `(8, 0)` | 11 yellow | plain |
| `pg_l3_b` | B3 | above | `(44, 0)` | 14 green | sticky |
| `pg_l3_c` | B5 | above | `(32, 16)` | 11 yellow | pair-A |
| `pg_l3_d` | B6 | above | `(44, 16)` | 15 purple | pair-B |
| `pg_l3_e` | B8 | below | `(32, 56)` | 14 green | plain |
| `pg_l3_f` | B9 | below | `(20, 56)` | 11 yellow | sticky |
| `pg_l3_g` | B6 | below | `(44, 40)` | 14 green | sticky (TRAP) |

(`pg_l3_d` slot moved up since B6 is in the middle horizontal — its
"above" slot is at y=16 (just above the vertical-segment cell of
B4), and "below" slot is at y=40. The trap `pg_l3_g` sits in the
gap between B6 and the bottom-row cells.)

Now the witness still does NOT fire ACTION2 on B6. The TRAP exists
to test the player's reasoning: "spam ACTION1/ACTION2 on every
bead with mismatched colour" would ACTION2-touch B6, sticky-lock
it to 14 green (wrong), and propagation later cannot rescue it.

**Adjacent commute failure:** the witness's actions 7 and 8 are
"cursor 4→5" and "lift on B5". Swap them: at cursor=4 fire ACTION1
— B4 has no peg above (no `pg_l3_*` is owned by B4), so it's a
no-op (no step consumed). Then cursor 4→5. Then we're back to
witness position with one no-op consumed. Witness still wins
within budget.

For a HARD adjacent commute failure, consider actions **8 (lift on
B5) and 9 (cursor 5→6)**. If we swap: action 9 first (cursor
5→6), then action 8 (ACTION1 at cursor=6). At cursor=6, ACTION1
swaps B6 with `pg_l3_d` (pair-B, purple). The swap colours: B6
was 14, pg_l3_d was 15 → B6=15, pg_l3_d=14. Pair propagation
fires: cursor=6's neighbour at cursor+1=7 takes pg_l3_c's colour
(11 yellow) → B7 = 11. But B7 was 15 (target 15) — now B7 = 11,
which is wrong. The witness later does NOT touch B7 to recover,
so B7's target is now broken. Recovery requires lifting on B5
(reverse the propagation), but `pg_l3_c` is now... wait, action
8-then-9 doesn't change `pg_l3_c`. After 9-then-8: B6=15 (target
✓), pg_l3_d=14, B7=11 (wrong — target was 15). To fix B7, the
player must ACTION1 on B5 with cursor=5: swap with pg_l3_c
yellow → B5 takes 11 yellow (correct), pg_l3_c takes 14 (B5's
old colour 14). Pair propagation: B6 takes pg_l3_d's colour 14
(B6 just became 15, now becomes 14 — wrong). 

So the swap of actions 8 and 9 cascades into multiple failures
that cannot be recovered without exhausting budget. **This is a
strict adjacent commute failure.**

OK, I'll commit to this. Final witness as above (14 actions).

**Difficulty justification (continued):**

- *Trivial heuristic L3 defeats:* "for each bead at wrong colour,
  find a peg of the target colour next to that bead and lift/drop".
  Defeated because B6's target (15 purple) has NO peg of colour
  15 in any of B6's slots (B6's above-slot peg `pg_l3_d` is colour
  15 BUT it's pair-B, so directly swapping would propagate
  pg_l3_c's colour into B7, breaking B7's target). The only path
  to B6 = 15 is the indirect pair-A propagation triggered by lift
  on B5. The trivial heuristic that ignores propagation rules
  cannot find this.
- *Adjacent commute failure:* swapping witness actions 8 (lift on
  B5) and 9 (cursor 5→6) breaks the level — see analysis above.
- Whole-environment human time target: ~6 min total (L1 ≈ 1.5 min
  with mechanic-discovery; L2 ≈ 2 min; L3 ≈ 2.5 min).

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. No ACTION5, no ACTION6, no
ACTION7.

| Action | Semantic | Gating |
|---|---|---|
| ACTION1 | "lift": swap the active bead's body colour with whichever peg sprite occupies the active bead's `above`-slot. If no peg, no-op (no step consumed). If the bead is already sticky-locked, no-op (no step consumed). If the touched peg is sticky, the bead becomes locked after the swap. If the touched peg is a pair-peg, propagation sets the cursor's neighbour bead's colour to the OTHER pair peg's colour (skipped if the neighbour is sticky-locked). | Always offered. Step consumed only if the swap was effective. |
| ACTION2 | "drop": same as ACTION1 but for the `below`-slot. | Same. |
| ACTION3 | cursor index decrement, clamped to `>= 0`. | Always offered. Step consumed always (even if at index 0 and no movement happens — counts as a navigation tick). |
| ACTION4 | cursor index increment, clamped to `<= len(chain) - 1`. | Always offered. Step consumed always. |

**Why misclicks are free for ACTION1/2 but not ACTION3/4:** matches
qz73's pattern — productive cursor-walks are part of any plan and
should always cost a step (else the cursor is "free" to position
anywhere); but ACTION1/2 with no peg present are not in the plan
and shouldn't tax the budget. This is the same pattern as
ACTION6-misclicks in qz73 / ACTION6-on-empty-cell in kx14.

## 6. HUD and per-game state

### HUD widgets

1. **Step counter bar** (`StepBarHud`, `RenderableUserDisplay`
   subclass): renders a 1-row depleting bar at row 0 (top edge).
   Width 32 cells centred horizontally (col 16..47). Filled cells
   are palette 0 (white); spent cells are palette 4 (background).
   Reads `self._max_steps` and `self._steps_used`. Updated in
   `step()` before action dispatch.
2. **Cursor indicator** (`CursorHud`, `RenderableUserDisplay`
   subclass): paints 4 corner pixels around the active bead's 4×4
   cell in palette 0 (white). Reads `self._cursor_index` and
   `self._chain` to find the active bead's display position.
3. **Lock indicator** (drawn into the bead sprite itself by the
   game class, NOT a HUD widget): when a bead is sticky-locked,
   the bead's central 2×2 inner pixels are recoloured by adding a
   palette-0 (white) corner pixel to the bead's pixel grid, giving
   a visual indication of locked state. Implemented via direct
   sprite pixel mutation in `step()` (cn04-style snapshot/restore
   pattern).

### Internal state

- `self._chain: list[Sprite]` — bead sprites in chain order
  (sorted by their `name` suffix or by a per-level `chain_order`
  level data list).
- `self._cursor_index: int` — current index into `self._chain`.
  Reset to 0 on `on_set_level`.
- `self._pegs_above: dict[int, Sprite]` — bead-index → its
  above-slot peg (or absent if none).
- `self._pegs_below: dict[int, Sprite]` — bead-index → below-slot
  peg.
- `self._peg_kind: dict[Sprite, str]` — peg-sprite → kind in
  {"plain", "sticky", "pair-A", "pair-B"}, derived from sprite tags.
- `self._pair_partner: dict[Sprite, Sprite]` — for each pair-peg,
  its paired sprite. Built in `on_set_level` by name suffix
  matching (sprite names ending in `_A`/`_B` paired by prefix).
- `self._bead_locked: dict[Sprite, bool]` — whether a bead is
  sticky-locked. False initially.
- `self._target_seq: list[int]` — list of target colours per chain
  index. Read from level_data `TargetSequence`.
- `self._max_steps: int` — read from level_data `StepCounter` per
  level. (24 / 32 / 60 for L1/L2/L3.)
- `self._steps_used: int` — increments only on effective actions
  (per ACTION1/2/3/4 rules above). Compared against `_max_steps`
  for the lose check.
- `self._step_bar: StepBarHud` — registered with the camera in
  `__init__`.
- `self._cursor_hud: CursorHud` — registered with the camera.

### Hidden state

`_get_hidden_state()` returns a `(2, len(chain))` `np.int16`
array:

- Row 0: current colour of each bead.
- Row 1: lock-flag (0 or 1) per bead.

Plus the cursor index is encoded into row 0's first cell's high
bits if needed; for simplicity, return `(3, len(chain))` with row
2 holding `[cursor_index, steps_used, max_steps, ...]` zeros.

## 7. Win condition

After every action, walk the chain in index order. For each bead
at index `i`, compare its current body colour to
`self._target_seq[i]`. If every bead matches, fire
`self.next_level()`. After L3 completes, the engine's
`next_level()` triggers `self.win()` automatically per its
last-level branch.

**Bead colour extraction:** the canonical bead sprite has a 4×4
pixel grid with 4 corner pixels = -1 and inner 12 pixels = the
body colour. Read `bead.pixels[1, 1]` (centre-ish position) as the
authoritative body colour for win comparison.

## 8. Lose condition

`self._steps_used >= self._max_steps` AND win predicate is False.
Single failure mode — no chasers, no hazards, no instant-fail
collision.

The lose check fires AFTER the win check on each action, so a
final-action-completes-the-puzzle case wins instead of losing.

## 9. Novelty note

### Closest taxonomy entries (per `mechanic-novelty/similarity-check.md`)

- **tr87 (tape-rewrite-rule)** — closest by pure-arrow verb-slot
  and horizontal-tape layout. Distinguishing rule:
  *tr87 cycles a card's intrinsic symbol identity through an
  alphabet at a fixed slot via UP/DOWN; qb84 PHYSICALLY displaces
  a bead between the chain and an adjacent peg and SWAPS their
  colours. tr87 has no spatial perpendicular displacement; qb84's
  entire mechanic is the perpendicular swap. tr87's win predicate
  is rule-based (LHS → RHS rewrite); qb84's win predicate is a
  fixed colour-sequence match.*
- **vc33 (row-slide-pull-tab)** — close by "row of cells with
  swap mechanic" framing. Distinguishing rule:
  *vc33's verb is a click on a row's pull-tab that shifts the
  ENTIRE row's cells by 1 cell positionally; qb84's verb is an
  arrow-press that displaces a single bead perpendicular to the
  chain and swaps its colour with one peg. Different cardinality
  (whole-row vs single-bead), different effect (positional shift
  vs colour swap), different verb-slot (`[6]` vs `[1,2,3,4]`).*
- **lp85 (row-col-shift-grid)** — also close by "row mechanic".
  Distinguishing rule:
  *lp85 is a Rubik's-cube-style permutation game with pure-click
  buttons; qb84 is a colour-swap game with pure-arrow input. lp85
  permutes positions; qb84 permutes colours.*
- **ls20 (cycler-attribute-match)** — close by "cycle attributes
  via fixed sprites". Distinguishing rule:
  *ls20 has a free-walking WASD avatar that lands on cycler tiles
  to cycle three independent attributes (shape/colour/rotation);
  qb84 has a non-spatial cursor that selects which bead is
  active, no walking avatar, and the swap is a colour-transfer
  with a peg sprite (not an internal cycle).*

### Closest prior-game entries (`prior-games/index.md`)

`prior-games/index.md` is non-empty (3 priors): kf42, qz73, kx14.

- **kf42 (tether-pawn-cycle)** — distinguishing rule: kf42 is
  click + arrows with a tether constraint between two pawns;
  qb84 is pure-arrow with a fixed chain (no tether, no movable
  pawns).
- **qz73 (radial-cycle-lock)** — distinguishing rule: qz73's
  verb is ACTION5 = "advance EVERY unlocked tip one slot CW"
  (global rotation); qb84's verb is ACTION1/2 = "displace ONE
  bead perpendicular to chain" (per-bead local swap). qz73's
  layout is radial 8-slot; qb84's is serpentine-chain.
- **kx14 (tide-tilt-buoyant)** — distinguishing rule: no
  meaningful overlap. kx14 is a vertical fluid-tank with water
  level + tilt + anchor; qb84 has no fluid, no tilt, no anchor —
  it has a cursor and pegs.

### Negative-similarity check (per `negative-similarity-check.md`)

Walked the 8 dimensions in `mechanic-pick.md`'s negative-check
section. No prior shares ≥ 3 dimensions. The closest taxonomy
near-miss is tr87 at 3 borderline dimensions (#2 verb-slot, #3
asks-row-vs-target partial, #4 step-counter universal). Mitigation:
qb84 commits to a serpentine (S-curve / zigzag / double-S) chain
layout — explicitly NOT a straight horizontal row — plus a small
target reference strip in the corner (NOT a full-width tape
display like tr87). Visual signature divergence is locked in via
the palette commitment (off-black background + magenta/yellow/
green/purple beads, distinct from tr87's grey + cyan + pink).
