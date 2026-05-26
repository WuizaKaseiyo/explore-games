# §3.4 compliance checklist

Use this when authoring a spec (in `write_spec`) and when reviewing
a spec (in `critique_spec`). Each item must be answered explicitly
in the spec; a "no" or "unclear" answer is a revision trigger.

## Format & structure

1. Does every sprite use only palette values 0..15 (and `-1` as
   transparent)?
2. Does the file structure match the universal scaffold in
   `skills/code/universal-scaffold.md`?
3. Does the `Game.__init__` declare `available_actions` as a subset
   of `[1, 2, 3, 4, 5, 6, 7]`?
4. Are there EXACTLY 3 `Level(...)` entries following the
   structure in `composition-and-tutorial.md` § Exactly 3 levels?
5. Is the game ID exactly 4 lowercase characters (letters or
   digits), not in the reference list, not in
   `prior-games/index.md`?

## §3.4 priors & constraints

6. Does every mechanic draw from `core-knowledge-priors.md`'s four
   categories only?
7. Does the game contain NO letters, NO digits-as-glyphs, NO
   real-world clipart, NO cultural conventions (see
   `forbidden-elements.md`)?
8. Are there at least TWO distinct mechanics in the environment?
9. Is level 1 a tutorial that establishes the base dynamic system
   (one or more interacting mechanics, all of them required by
   L1's witness), with reduced state space and no on-screen text?
10. Do L2 and L3 each increase difficulty by COMPOSING every
    mechanic available at that level (the carried-forward ones
    plus the newly-introduced one or two), not by scaling grid
    size or item count?

## Mechanic structure (per-level)

11. **Mechanic inheritance and the +1-or-+2 rule.** Does each
    level's spec state which mechanics its witness solution
    exercises? Let N ≥ 1 be the count of mechanics required by
    L1's witness, and let M be the count required by L2's
    witness. Does L2's witness require either N+1 or N+2 (every
    L1 mechanic carried forward AND one or two new mechanics)?
    Does L3's witness require either M+1 or M+2 (every L2
    mechanic carried forward AND one or two further new
    mechanics)? Every earlier-level mechanic must remain
    present and required at every later level — none may "drop
    out" — and no level promotion may introduce zero new
    mechanics or more than two new mechanics.

12. **Strict counterfactual necessity (no trivial fallback).**
    For each mechanic M available at level L, no sequence of
    actions may win L within the step budget without triggering
    M's distinguishing behavior. Why this matters: it forces
    the player to understand each mechanic fully before
    advancing. The question is not "does the named witness rely
    on M" — it is *"can the level be hacked at all without M"*.

    The critique must produce a **per-mechanic table** with one
    row per (mechanic, level) pair across L1, L2, L3. Each row
    answers: *"Is there any way to win L within the step budget
    without ever triggering M?"* Answer must be **no**, with a
    1-line reason naming a specific cell, sprite, or rule that
    blocks every alternate path. ANY "yes" — or any "no" that
    hand-waves without naming what blocks the alternate path —
    rejects the spec.

    **Verify by enumeration, not by abstraction.** The critique
    must INDEPENDENTLY enumerate the plausible alternate
    strategies a player would naturally try (e.g. "push pawn up
    to row 5 and detour right", "click target B before triggering
    A", "spam ACTION5 from the start position") and concretely
    walk each one, showing why it fails by referring to specific
    cells/sprites/state-checks. How many alternates is enough is a
    judgment call — cover every alternate that has a plausible
    chance of bypassing M; if the geometry / state-space is rich,
    that means more alternates. Quoting the spec's general claim
    ("the walls extend the blockage", "the only path is through
    M") is not sufficient — the critique must re-derive the
    failure case. Geometric/spatial blocking arguments are the
    most common failure mode: a spec saying "walls at (X, A) and
    (X, B) block column X" only blocks rows A and B, not all of
    column X. The critique must check the rows / columns adjacent
    to the named walls and the grid edges.

    | Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
    |---|---|---|---|
    | L1 | M1 | no | ... |
    | L2 | M1, M2, M_new (one row each) | no per row | one row each |
    | L3 | M1, M2, ..., M_newest (one row each) | no per row | one row each |

    Examples of trivial fallbacks the per-mechanic check catches:

    - clicking each interactable individually instead of triggering
      a chain reaction;
    - walking to each target sequentially instead of using a
      teleport / cone / projection mechanic;
    - pressing each button without considering ordering when the
      mechanic is order-dependent;
    - a "redundant decorative" mechanic whose effect lands on
      the same destination the base mechanic would have produced
      anyway (e.g. a push-rule that drops a pawn on a cell the
      pull-rule already routes through).

13. **Minimum-action witness — no one-action or repetitive
    passes.** Every level's witness must satisfy both:

    1. **Length:** ≥ 3 actions.
    2. **Diversity:** ≥ 2 distinct actions. Two ACTION6
       invocations count as distinct iff they target different
       cells. ACTION7 (undo) doesn't count toward either floor.

    A level winnable in ≤ 2 actions, or by repeating the same
    action 3+ times, fails. The check applies to the witness
    *and* the level geometry: the critique must affirm no
    shortcut path exists, naming the concrete cell/sprite/rule
    that blocks both 1-2-action and single-action-repetition
    wins.

    Why: a 1-2 action win is indistinguishable from a lucky
    try; a spam win demonstrates no rule understanding.

    Fixes if too easy: add geometric distance, a precondition
    step (rotate before push, pickup before use), a multi-stage
    consume rule, or a multi-target win condition.

## Novelty

14. Is the chosen mechanic family absent from
    `mechanic-novelty/taxonomy-of-25-games.md`?
15. Is the chosen mechanic family absent from
    `prior-games/index.md`?
16. If the proposed mechanic SOUNDS similar to one in either list,
    has the spec articulated the concrete distinguishing rule?

## Solvability

17. Has the spec stated the win condition for the environment as a
    whole?
18. Has the spec stated a lose condition (or "no lose" with
    reasoning)?
19. **Difficulty floor and ceiling** — does the spec satisfy
    every per-level item in `difficulty-rules.md` § Critique
    check? Specifically, for each of L1, L2, L3 has the spec
    stated (a) random-resistance, (b) human time, (c) planning
    depth, (d) step budget — all four bullets, with the L2/L3
    planning-depth justification concrete (not vague)?

20. **No hidden state.** For every piece of game state the
    player needs to reason about and that is mutated by an
    action (selection, mode, charge-level, lock/unlock,
    target-anchor, active turn-actor, etc.), does the spec
    name the persistent visual cue that surfaces it for as
    long as the state is in effect? Per
    `conventions/reference-game-patterns.md` § Discoverability.
    Reject if a state change is described without a
    corresponding visible cue (e.g., "ACTION6 selects an orb"
    with no description of how the player sees which orb is
    selected).

21. **Don't generate a low-resolution game.**
    The frame is 64×64 pixels — design for that resolution.
    Don't pick a small logical grid (12×12, 14×14, 16×16, etc.)
    that the engine then scales up into chunky uniform-colour
    cell-blocks; a chunky upscaled grid wastes most of the
    available pixel budget and makes the rendering read as
    crude. Some of the 25 reference games do use small logical
    grids — that is not a licence to copy them. Aim for richer
    visuals than the smaller-grid reference games, not parity
    with them.

    Pack visible detail at the display-pixel level: pawns,
    targets, walls, fixtures, and HUD widgets should each have
    real internal pixel structure that a player can read off
    the rendered frame. Shape carries meaning, not just colour.
    Two sprite kinds that differ only by their fill colour
    (red blob vs. blue blob) are not enough — give them
    distinguishing internal pattern (a key looks like a key, a
    button looks like a button, a container has a hollow centre,
    a portal has a ring, a wall has a flat fill, etc.). The
    4-bit palette is a secondary differentiator (red key vs.
    blue key), not the primary one (key vs. door vs. floor).

    The check is qualitative: imagine showing the rendered L1
    frame to someone who has never seen the game. Does the
    rendering look detailed and considered, or does it look
    like coarse coloured blocks pasted onto a grid? If the
    latter, the spec fails — bump the playfield resolution,
    enlarge primary sprites, and add internal pattern until the
    rendering reads as detailful.

22. **Design the UI to teach — the screen is the only
    instruction the player gets.** The agent has no way to teach
    the player through text, narrators, or tutorials. If the
    mechanic is even slightly complex, the visual design has to
    do the teaching — every object the player must reason about
    needs to make its role guessable from the screen, or at
    least guessable after a small number of exploratory actions.

    Three rules of thumb the spec must satisfy:

    1. **Sprite UI ≈ sprite role.** If an object carries a
       semantic meaning the player has to reason about, its
       rendered look — shape, palette, size, position-context —
       should suggest that meaning. Some examples (illustrative;
       the spec picks the actual visual idiom):
       - A button-like activator should read as pressable —
         visibly distinct from inert decoration.
       - A keypad / control panel / interactive surface should
         look like one.
       - A hazard or danger object should use a visual register
         the spec defends as reading-as-dangerous, AND a look
         clearly distinguishable from the player's avatar so the
         two are not confused at a glance.

       The point is not that every object must match a real-world
       referent — abstract is fine — but that the spec must
       articulate *why* the chosen visual reads as the role it
       represents.

    2. **Identical visuals imply shared or correlated roles.**
       If two sprite kinds share the same shape, palette, and
       size, the player will reasonably assume they share common
       features or are correlated in behaviour. If they actually
       behave very differently, the spec has lied to the player.
       Either give them a distinguishing visual feature
       (different shape, different palette, different size, or a
       clearly different position-context) or link them in
       behaviour so the shared visual reflects a real correlation
       (paired endpoints of one mechanic, members of one class,
       etc.). Conversely: when two sprite kinds ARE meaningfully
       correlated in role or behaviour, the spec must give them
       a shared visual cue (matching shape, matching palette
       accent, paired markers, etc.) so the player can read the
       correlation off the screen alone.

    3. **If the visual cannot carry the mechanic, change the
       representation.** When a mechanism is rich enough that no
       static rendering hints at its role to a first-time viewer
       — even after a few exploratory steps — the answer is not
       hidden text, not captions, and not reliance on extensive
       trial-and-error. Try first to switch to a representation
       that *does* carry it; failing that, redesign the mechanic
       itself. The constraint flows: visual budget → mechanic
       complexity, not the other way around.

    The operational test: present an L1 screenshot to someone
    who has never seen the game, no caption. Can they form a
    useful guess about which sprite they control, which sprite
    is the target, and what kind of interaction the level
    invites? If forming any such guess would require source-
    reading or extensive trial play, the spec fails this gate.

23. **ACTION7 is strict-undo or absent.** All 6 of the 6 reference
    games that declare ACTION7 use it for undo of the most recent
    action (ar25, bp35, lf52, sb26, sk48, su15). Generated games
    MUST follow this rule:

    - If the game has a meaningful undo (a single action that
      reverses the most recent action's state change), ACTION7
      may be declared in `available_actions` with that semantic.
    - If the game does NOT have undo, **omit ACTION7 entirely**
      from `available_actions`. Do not overload the slot with any
      other verb (cool, fire, swap, toggle, charge, commit,
      etc.).

    Why: the keyboard binding (`Z` / `⌫`) carries strong undo
    expectations across game culture; a player who tries Z
    expecting undo and gets an unrelated verb has their mental
    model broken catastrophically. The §3.4 "no instructions"
    principle assumes players can rely on cross-game soft-norms
    for the keyboard-bound semantics — slot 7 in particular.

    Verify at critique time: read the spec's §5 (Action mapping).
    If `ACTION7` is declared, verify its semantic is plain-English
    "undo the most recent action". Reject any other semantic.
    See `skills/global/action-enum.md` § Slot 7 is strict-undo
    for the rationale.

24. **Animation for non-local effects.** If the mechanic produces
    non-local effects in a single tick — teleport, slide-until-
    wall, projectile, chain reaction, multi-entity propagation —
    does the spec describe how those effects animate frame-by-
    frame? The critique judges (a) whether the mechanic IS
    non-local in this sense; if yes, (b) the spec must state the
    animation plan (e.g., "N ticks, K cells per tick, leaving a
    fading trail" — concrete enough that `implement` can write
    the multi-frame `step()` loop). Per
    `conventions/reference-game-patterns.md` § *Discoverability
    through observable change*. Reject when the mechanic is
    non-local but the spec has no animation plan.

25. **Lives mechanism for hard-death conditions.** If a level
    has any **hard-death** path — a single action that
    immediately triggers `self.lose()` (hazard, fail-state tile,
    NPC contact, soft-lock) — the spec must include a **lives
    mechanism**: enough attempts per level for a human player
    to learn the hard-death rule by observation. The spec
    author picks the number; the critique sanity-checks that
    the chosen count is plausibly enough to support
    learn-by-trying. Energy depletion under a generous budget
    is NOT hard-death and is exempt.

    On each hard death: decrement the lives counter, reset the
    level to its initial state, respawn the avatar at start. The
    game stays NOT_FINISHED until lives == 0; only then does
    `self.lose()` fire. Lives are **per-level** (fresh count
    each level), not persistent across the run. The counter
    must be a visible HUD cue (per item 19).

    Why: a single-life game punishes the exploration needed to
    discover what kills the player. Lives turn the hard-death
    rule into a discoverable mechanic.

    Spec deliverables in § 4 (per level with hard-death):
    trigger(s), chosen initial lives count + a one-line
    rationale tying it to the death rule's discoverability,
    respawn semantics, visual cue.

26. **Mechanic adds a new rule, not a new map.** A declared
    "mechanic" must add a new rule to the player's rule book —
    a genuinely new behavior that didn't exist at any earlier
    level. New rules can take many forms: a new verb, a new
    cell/sprite behavior, a new state machine, an autonomous
    actor, a new physical regime, and so on — these are
    illustrative, not exhaustive. Anything that genuinely
    expands what the player can do, or what the world does in
    response, counts.

    A new *arrangement* of existing cells/sprites on the grid
    is **level layout, not a mechanic.** Test: can L_n be fully
    described as "L_{n-1}'s rules applied on a different map"?
    If yes, the declared M_new is layout in disguise and fails.

    Spec deliverable: in § 4's *Mechanics required by the
    witness* bullet, for each declared M_new state in 1 line
    the new rule the player learns — in player-facing language.
    If the rule can't be expressed beyond "holes arranged
    differently / goal farther / corridor narrower," it's
    layout.
