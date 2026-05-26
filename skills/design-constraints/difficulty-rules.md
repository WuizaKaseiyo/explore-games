# Difficulty rules

The harness's level-structure rules (L1 = base dynamic system,
L2 = +1 or +2 new mechanics, L3 = +1 or +2 more) live in
`composition-and-tutorial.md`. This file is the canonical home
for the **difficulty** rules layered on top of that structure:
random-resistance, human-tractability, planning depth, and step
budget.

`composition-and-tutorial.md` (the principle form),
`checklist.md` item 19 (the critique check), and
`spec-template.md` §4 (the spec instruction) all reference this
file rather than restating its content. Edit here; references
stay current.

## 1. Principle

Difficulty has **two stages**, and a good level uses both:

1. **Mechanism exploration** — the player has to interact with the
   level to figure out what each mechanic does. Discovery is its
   own gate before any planning can begin.
2. **Planning** — once every mechanic is understood, reaching the
   goal still requires deliberate thought. The level offers many
   moves that *look* reasonable; the player must reason about
   future state to pick the path that actually wins.

The two stages scale differently across levels:

- **Exploration difficulty stays roughly constant L1 → L2 → L3.**
  Each level introduces 1-2 new mechanics; discovering them takes
  comparable effort each time. Don't try to make exploration
  *harder* at L3 — that path leads to obscurity and hidden-mechanic
  traps.
- **Planning difficulty escalates L1 → L2 → L3.** L1: little or
  no planning. L2: noticeably more — the player must think
  several moves ahead. L3: enough planning that even an attentive
  human finds it challenging.

Forbidden sources of difficulty (these are not "depth," they are
friction):

- a tight step budget that punishes exploration;
- hidden mechanics that punish players who haven't tried every key;
- soft-locking the player into a state from which the win is
  already unreachable (e.g. an irreversible action consumed the
  last copy of a needed resource) without firing `lose()` on the
  turn the unreachability is detected — making the player wait
  for budget exhaustion in a no-win waiting room is the lose-side
  mirror of a punishingly tight budget.

A level that is hard because the optimal solution is hard to
*find among plausible alternatives* is good. A level that is hard
because the player runs out of energy mid-exploration, or because
the rule was never discoverable, is broken.

## 2. What the spec must state (per level)

Each of the three levels' *Difficulty justification* in the spec
must contain these four bullets. The data here is what
`critique_spec` checks against.

### a. Random-resistance

In 1-2 sentences, explain why a vision-blind / random-policy agent
or a small text-only LLM agent has near-zero chance of solving the
level within the step budget. No "spam-one-verb" wins. This rule
prevents trivial agents from accidentally clearing the level.

### b. Human-tractable

State the time an attentive human or a top vision-language model
needs once the screen has been read. Target: **~2 minutes per level**,
with the whole environment landing **around 6 minutes** total.

### c. Planning depth

This addresses the **second stage** of difficulty (see §1):
**after the player has explored enough to fully understand every
mechanic, do they still have to plan how to reach the target?**
Mechanism discovery and puzzle solving are separate gates; this
one covers the second.

The shape of "good planning difficulty" is **many action paths
look reasonable, but only a few actually lead to the goal.** The
player should face plausible alternatives at each decision point
and have to think hard about which one leads to the goal. A level
where the correct move is visually obvious at every step has no
planning difficulty, however many mechanics it stacks.

Per level:

- **L1**: **no strict planning requirement.** Mechanic discovery
  is the entire difficulty; once the rule is understood,
  reaching the target may be near-immediate.
- **L2**: **moderate planning required (post-discovery).** Even
  with every mechanic understood, getting to the win must still
  demand a sequence of considered moves — reasoning about state
  + future state before each action, with multiple plausible-
  looking action paths at each step. Single-step, follow-the-
  colour, and 1-action-lookup-table solutions reject the spec.
  The spec must justify in 1-2 sentences what reasoning the
  player does at each step of the witness, and what the plausible
  *wrong* paths are that the player must reject.
- **L3**: **planning is challenging even for an
  attentive human (post-discovery).** Greedy / monotone-progress
  / follow-the-obvious-gradient strategies should not reliably
  win. The number of reasonable-looking *action paths* (not
  object-movement paths) at each decision point should be large
  enough that the player has to plan a few moves ahead instead
  of pattern-matching. The spec must name in 2-3 sentences the
  trivial heuristic L3 defeats and why ahead-of-time reasoning
  is needed to find a winning path.

### d. Step budget

State the per-level `step_budget`. **Be generous** — give the
player comfortable room over the witness length to explore the
mechanic, try wrong moves, and recover. A budget that is barely
longer than the witness is forbidden; difficulty must come from
the two stages in §1 (exploration + planning), never from
tightness of the step counter.

Per-level addenda:

- **L1**: no level-specific addendum.
- **L2**: a first-time player will spend several actions
  discovering what the new mechanic does *before* they can attempt
  the witness; the budget must reflect that.
- **L3**: the budget must NOT shrink relative to the witness as
  level number rises — later levels add mechanics and therefore
  *more* discovery cost, not less, so they need *more* exploration
  room.

## 3. Critique check (for `critique_spec`)

For each of L1, L2, L3, verify the spec states all four:

- **(a) Random-resistance** — a non-trivial reason a random /
  vision-blind / small-LLM agent fails.
- **(b) Human time** — an estimate near the ~2-min/level and
  ~6-min/total targets.
- **(c) Discovery difficulty** — verify the spec articulates, per
  level, what mechanic(s) the player must learn by interacting
  with the level (no on-screen text, no labels). This gate covers
  stage 1 of § 1; stage 2 (planning) is the separate bullet below.

  Per level:
  - **L1**: spec names the base dynamic system (≥ 1 mechanic) the
    player discovers from a clean slate.
  - **L2**: spec names one or two new mechanics L2 adds on top of
    L1's, and the observable cue that lets the player learn each.
  - **L3**: spec names one or two new mechanics L3 adds on top of
    L2's, and the observable cue for each.

  Reject if a level introduces a mechanic the player cannot learn
  through play (mechanic is hidden / requires source-reading), or
  if a level claims a new mechanic but there exists solutions that
  doesn't actually exercise it.

- **(d) Planning depth (post-discovery)** — assume the player has
  fully understood every mechanic available at the level. With
  full knowledge, do they still have to choose among action strategies
  to reach the win?

  Per level:
  - **L1**: spec explicitly states *no strict planning requirement*.
    L1 is the discovery gate; once the rule is understood, the win
    may be near-immediate or by trivial planning.
  - **L2**: spec must (1) **enumerate the post-discovery decision
    space at level start** — count of valid first actions a fully-
    informed player faces. If < 2, the level is a 1-action-lookup-
    table by definition → reject. (2) **Name at least one
    plausible-but-wrong alternative** the post-discovery player
    would consider and reject. (3) **Trace the witness's reasoning
    chain** referencing post-discovery state (positions, rotations,
    fragile invariants) — not discovery-stage observations like
    "clicked and nothing moved".
  - **L3**: spec must (1) **enumerate the post-discovery decision
    space**; count ≥ L2's, never smaller. (2) **Name a trivial
    post-discovery heuristic that fails** — greedy-toward-target,
    monotone-progress, or follow-the-obvious-gradient — one a
    fully-informed player would naturally try. (3) **Show where
    the heuristic diverges from the witness** in 2-3 sentences:
    at which step the heuristic and the witness disagree, and why
    the heuristic's choice irrecoverably loses or significantly
    delays the win.

  **Stage-conflation guard.** Reject if the named "heuristic that
  fails" or wrong-path argument is a discovery-stage misstep —
  something a player only does because they haven't yet understood
  the mechanic. The post-discovery player knows what each action
  does; their failures must come from picking the wrong action
  *despite* full knowledge, not from missing knowledge. "No visible
  feedback on click 1" cannot be the failure mode at this gate
  because the post-discovery player already knows click 1 is a
  setup tick.

  **Operational test.** Walk the named heuristic from a fully-
  informed starting state. If the heuristic produces the same
  action sequence as the witness, it doesn't fail post-discovery —
  it succeeds, and (d) is unmet for this level.
- **(e) Step budget** — a value, generous over the witness length,
  not shrinking across levels.

If any per-level bullet is missing, or the L2/L3 planning-depth
justification is vague (e.g. just says "requires planning" without
naming the reasoning chain), the spec is rejected.
