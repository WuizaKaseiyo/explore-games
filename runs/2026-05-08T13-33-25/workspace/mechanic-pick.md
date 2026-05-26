# mechanic-pick

## ID

**`ej4t`** — verified not in reserved 25-ref list, not in `prior-games/index.md` (26 entries), not a recognisable English word.

## Mechanic family tag

**`radius-scope-influence`**

## One-paragraph description

The player is a single avatar surrounded by a visible influence ring of fixed radius (Manhattan distance R). Crates and switches inside the ring respond to the player's pushes and clicks; the same elements OUTSIDE the ring are inert (clicks pass through, pushes fail at the ring boundary). The ring is centred on the player and moves with them, so the player must navigate to bring the right elements into scope before acting on them. **Mechanic 1 (L1)** is *radius-gated push*: only crates whose top-left cell sits within Manhattan distance R of the player can be pushed; pushes outside the ring no-op. **Mechanic 2 (L2)** introduces *scope-extender pickups*: walking onto a coloured pickup tile permanently grows R by 1 (a one-shot consumable; tile vanishes); some L2 puzzles require collecting an extender before reaching elements that are otherwise out-of-scope. **Mechanic 3 (L3)** introduces *colour-keyed sub-radii*: the player's ring splits into two concentric coloured halves (red inner radius R1 < blue outer radius R2), and each colour-coded element only responds when the same-coloured ring covers it — so L3 forces the player to position so multiple colour-rings simultaneously cover their target elements. The win condition every level is "deliver every coloured crate onto its same-coloured target tile", inherited L1 → L3, with L3 requiring all three mechanics interacting (radius-gated push + extender management + colour-keyed sub-radii) at once.

## Mechanism essence

Spatial-scope rule discipline: the player isn't directly the actor; the *ring around the player* is the actor, and the player chooses where to plant it. Action effects are conditional on geometric coverage. The player's planning concern shifts from "what move helps the goal" to "what position lets the right move become available".

## Distinguishing rules vs near-misses

### Taxonomy near-misses (25 reference games)

#### lq5x (lantern-cone-illuminate) — closest near-miss
**Shared surface**: both have a "scope" projected from a primary actor that gates which cells respond to actions; both have collectables (lq5x's wax pickups extend the cone; this candidate's extender pickups grow R) that grow the scope.

**Concrete distinguishing rule**: lq5x's scope is a **directional 3-wide cone projected from a stationary lantern**, and the player rotates the lantern via ACTION5 to redirect the cone — the player walks separately from the lantern. This candidate's scope is an **omnidirectional Manhattan ring centred on the player**, moving with the player every step — the player cannot rotate the ring, only translate it. The interaction surface is fundamentally different: lq5x is "rotate beam to hit target"; this is "walk to bring target into ring". The cone games have no scope-extender that grows the angle; this candidate's extender grows the radius. The visual signatures differ: lq5x renders a triangular cone footprint; this renders a diamond-shaped Manhattan ring.

#### vp6h (shadow-cast-collect) — secondary near-miss
**Shared surface**: both have "vision-like coverage" gating something; both involve walking the avatar.

**Concrete distinguishing rule**: vp6h's coverage is **shadow projected by ALL active rail-mounted lanterns** (multi-source shadow union); the player must stand in the shaded intersection. This candidate's coverage is a **single ring on the player itself** with no shadow concept; there is no light-vs-shadow polarity. vp6h's collectables (crystals) are gated by shadow; this candidate's collectables (extender pickups) are walkable freely and grow the ring. Different cast (rails vs. no rails), different polarity (avoid light vs. operate within ring), different action target (walk-into-shadow vs. push-within-ring).

#### kn58 (anchor-pull-magnet) — tertiary near-miss
**Shared surface**: both have a click/place-based positional rule that gates motion of other objects.

**Concrete distinguishing rule**: kn58 places **a single magnetic anchor via click**; ALL coloured pawns slide one cell along their dominant Manhattan axis toward it (one-shot per click, global effect). This candidate has **no click-place mechanic**; the influence is automatically attached to the player and only gates push permissibility, not autonomous motion. kn58 is "click → things pull toward click point"; this is "push → only crates within ring respond". Action verb (click vs. push) and effect type (pull-toward vs. permission-gate) both differ.

#### bx84 (beam-mirror-reflect) — quaternary near-miss
**Shared surface**: both have "projection from an actor that reaches some cells" (bx84's beam, this's ring).

**Concrete distinguishing rule**: bx84's beam is a 1-cell-wide ray that reflects off mirrors and stops at walls; the player drops mirrors via click. This candidate's ring is a 2D area, not a 1D ray, with no reflection or mirror sprite. The fundamental geometry differs (line vs. area), and bx84's player builds the reflection topology by clicking; this candidate's player has no equivalent topology-shaping verb.

### Prior-games near-misses (26 entries)

#### lq5x — already addressed above (was both ref and prior; same distinguishing rule applies).

#### bx84 — already addressed above.

#### kn58 — already addressed above.

#### vp6h — already addressed above.

#### lv4k (lever-balance-torque) — distant
**Shared surface**: none structurally — both are "place pieces" but lv4k's pieces sit on a beam computing torque.

**Concrete distinguishing rule**: lv4k is a **summation/balance constraint**: pieces on a beam must sum-to-zero torque. This candidate has no summation, no beam, no torque. Different mechanic family entirely.

#### pf3w (wavefront-converge-timing) — distant
**Shared surface**: both have spatial reach (wavefront radius vs. ring).

**Concrete distinguishing rule**: pf3w is **timing-based**: emitters tick wavefronts that expand each ACTION5; win condition is "all wavefronts coincide on receivers same-tick". This candidate has **no timing**; the ring is always-on and centred on a moving player; coincidence is geometric, not temporal.

### Negative-similarity check (7 dimensions, vs every prior + ref)

Walking the 7 dimensions vs the closest prior, **lq5x**:

1. **What's on the board**: lq5x has a single lantern + wax pickups + filters + target rings; this candidate has a player + crates + targets + extender pickups + ring overlay. **Different cast**.
2. **What the player physically does**: lq5x walks (1-4) + rotates (5); this candidate walks + pushes (motion is push-when-in-ring). **Overlapping (walk + arrow-action) but the rotational primitive differs**.
3. **What the level asks for**: lq5x = match cone colour to ring + reach; this = deliver crates to colour-matched targets. **Different goal structure** (cone-on-ring vs. crate-on-target).
4. **What kills**: both step-budget exhaustion. **Same (universal pattern, doesn't count strongly)**.
5. **Cast**: lq5x lantern + wax + filters + rings; this avatar + ring + crates + extenders. **Distinct supporting elements**.
6. **Visual signature**: lq5x dominant palette likely yellow lantern + colour rings; this avatar + diamond ring overlay (likely dark grey + accent) + coloured crates. **Different visual signature**.
7. **Pixel grain**: both use detailed sprites by checklist item 20. Equivalent quality target.
8. **Core dynamic**: lq5x = "rotate the cone to illuminate the right ring"; this = "position the ring to put the right element in scope, then push". **Different core dynamic** (rotate-to-illuminate vs. position-to-permit).

Sharing on **dimensions 2 (walk+arrow) and possibly 4 (step-budget universal)** = 1-2 dimensions, well under the 3-dimension reject threshold.

Walking against **kn58** (anchor-pull-magnet):
1. board: avatar + ring + crates vs. click-place + pawns + targets — different
2. action verb: push vs. click-place — different
3. goal: deliver crates to targets vs. align pawns to targets — same goal family but different verb path
4. kills: step-budget — same
5. cast: avatar + ring + crates + extenders vs. anchor + pawns + targets — different
6. visual: ring overlay vs. discrete pawns — different
7. pixel grain: both detailed
8. core dynamic: position-ring-to-permit vs. click-anchor-to-pull — different

Sharing on dimensions 3 (deliver-pieces-to-targets) + 4 (step-budget universal) = 2 dimensions. Under threshold.

**Verdict: NOVEL** vs all 26 prior-games and 25 reference games.

## Inspiration source

**Step 5 web research input**: PuzzleScript demo `plus_localradius.txt` (from Auroriax/PuzzleScriptPlus). That demo's core idea was "crates push only within radius around player" — this candidate adopts that core idea, then composes it with two NovaPlay-native mechanics (extender pickups; colour-keyed sub-radii) into a 3-level progression suitable for the §3.4 + checklist structure. The PuzzleScript demo itself is a tech-demo with a single level; **§3.4 commercial-novelty ceiling**: not a commercial game, not a famous puzzle title — should pass user-side ceiling check trivially.

## Action mapping (preview — to be detailed in `write_spec`)

- ACTION1-4: walk avatar one cell (cardinal). Pushing happens automatically when avatar walks INTO a crate AND that crate's top-left is within radius R of avatar's NEW position.
- ACTION5: not used at L1 / L2. At L3, ACTION5 toggles which sub-radius (red inner / blue outer) is "active" for the next push (interpretation: a single crate may need to be pushed only by the red sub-ring while standing within the blue sub-ring as well — toggle determines which ring's gate is checked).
- ACTION6: not used.
- ACTION7: not used.

Subset declared: `[1, 2, 3, 4]` for L1+L2; `[1, 2, 3, 4, 5]` for L3 (engine declares both — but L1/L2 levels' guidance simply makes ACTION5 a no-op silently; this is acceptable per the universal-scaffold idiom).

Actually — per `cross-cut-frequencies.md`, `available_actions` is declared once at `__init__` for the whole game, so we declare `[1, 2, 3, 4, 5]` and L1/L2 just don't need ACTION5 (no-op handler).

## Per-level grid sizes (preview)

- L1: 12×12 (small, 1 crate, 1 extender pickup ignored, R=2)
- L2: 14×14 (2 crates, 1 extender pickup, R=2 → R=3)
- L3: 16×16 (2-3 crates with colour keys, 1-2 extenders, R1=2/R2=4)

(Final grid sizes / sprite positions / step budgets fixed in `write_spec`.)

## Considered alternatives (rejected, briefly)

- **shadow-propagation gating** (inspired by `diesinthelight`): rejected — too close to `vp6h` (shadow-cast-collect). Distinguishing rules existed but visual signature would overlap heavily.
- **direction-aware path coverage** (inspired by `zenpuzzlegarden`): rejected — too close to `tn36` (program-pawn-trace) on the path-tracing dimension.
- **Nonogram-like constraint-sat** (inspired by `plus_nonogram`): rejected for §3.4 commercial-novelty (Nonogram/Picross is famous commercial). Could be revived with a strong distinguishing rule, but requires more thought than this run permits.
- **multi-actor synchronization-to-exit** (inspired by `ponies jumping synchronously`): rejected — too close to `zd7m` (cohort-step-route, arrows step every movable pawn).
- **hierarchical chained-segment arm** (inspired by `robotarm`): a viable alternative, novel WRT corpus. Holding for a future run.
