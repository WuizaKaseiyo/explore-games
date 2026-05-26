# What an NovaPlay game *is* — distilled from the technical report

This file distils the **soft design philosophy** of NovaPlay from the
[Nova Prize Foundation Technical Report (April 2026)](https://novaprize.org/media/ARC_AGI_3_Technical_Report.pdf).
The hard rules (palette, action enum, file scaffold, §3.4 priors) live
under `skills/design-constraints/`; this file captures everything those
rules are *for* and the implicit conventions a generated game must
satisfy to *feel* like an NovaPlay environment.

Use this file as the answer to the question: *"is the game I'm about
to specify culturally consistent with NovaPlay?"*

---

## 1. The mission of an NovaPlay environment

Per §2.1, every NovaPlay environment evaluates four pillars of
agentic intelligence:

| Pillar | What the agent must do | Implication for a generated game |
|---|---|---|
| **Exploration** | Actively obtain information by interacting with the environment. | The win condition / mechanics CANNOT be derivable from a single static frame. The agent must take some action to learn. |
| **Modeling** | Turn raw observations into a predictive world model. | Action effects must be deterministic and learnable. Hidden state should be inferable from frame transitions over a few actions. |
| **Goal-Setting** | Identify desirable future states without instructions. | NO on-screen text or hint glyph telling the player the goal. Goal must be implicit from the level layout (e.g., "this looks like a target — get the block onto it"). |
| **Planning & Execution** | Strategically map an action path to the goal; course-correct on feedback. | Levels must reward planning (action efficiency matters) over brute force. Random play should not stumble through. |

A game that fails to exercise ANY one of these pillars is not an
NovaPlay game in spirit, no matter how cleanly it conforms to the
mechanical rules.

## 2. Format invariants (§2.3)

These are **non-negotiable platform contracts**:

- **64×64 integer grid**, each cell 0..15 (16 palette colours).
- **A "frame" is a single grid state.** A frame sequence (animation
  between turns) is permissible — engine renders them sequentially
  before accepting the next action.
- **Action space = subset of:** 5 key actions + an Undo + a "select
  cell" action (= ACTION6 in `novaengine`). Note: undo is unusual in
  the 25 reference games; most don't expose it. Generated games
  should not assume undo is available.
- **Turn-based.** State changes ONLY in response to actions; no
  asynchronous time-step.
- **Hidden state** is a separate signal from the frame. The engine
  hashes `(frame, hidden_state)` for graph identity (§3.5.2). Two
  states that render to the same frame but have different hidden
  state are distinct nodes — the agent can in principle distinguish
  them. Generated games may use hidden state for things like a flip
  counter, an internal selection handle, or a cycle index.

## 3. Action efficiency — the scoring function shapes design (§4.1, 4.2)

NovaPlay's score (RHAE — Relative Human Action Efficiency) is the
**load-bearing reason** the design constraints look the way they
do. Designs that fight the scoring function produce games that
either reward brute force or reward already-knowing-the-answer.

### The formula in plain English

For each level `l` in environment `e`:

```
S_l,e = min(1.15, (h_l,e / a_l,e)^2)
```

where `a_l,e` is the agent's action count and `h_l,e` is the
upper-median best human's action count.

### Implications for game design

- **The exponent is 2.** Doubling the action count quarters the
  score. Tripling it ⇒ ~11%. So the level's optimal solution must
  be reachable from a coherent strategy — if it requires 100
  actions, the agent must be able to plan 100 actions, not flail.
- **Level scores are linearly weighted by level index.** In a
  5-level game, weights are `(1, 2, 3, 4, 5) / 15` → late levels
  contribute disproportionately. **In our 3-level generation cap**,
  weights are `(1, 2, 3) / 6` → **L1 is 17%, L2 is 33%, L3 is 50%**
  of the score. Generated games must put the meaty composition in
  L3 — that's where half the score lives.
- **Per-level cap = 1.15× human baseline.** An agent that finds an
  exploit completing a level in 2 actions when humans took 20
  doesn't get 10× score; it caps at 1.15. Don't design levels with
  trivial exploits.
- **Per-environment cap = weighted fraction of levels completed.**
  For 3 levels, completing 2 of 3 caps the environment at
  `(1+2)/6 = 50%`. Completing only the tutorial caps at `1/6 ≈
  17%`. Levels are sequential — completing L_k means completing
  L_1..L_k.

### The action-budget constraint

Per §4.3, the official leaderboard terminates an agent after **5×
the human-baseline median action count per level** to bound API
spend. So each level should be solvable in a budget where 5×
human-baseline is still tractable.

## 4. The "no instructions" principle (§2.1, §3.4)

The single most important design rule. Quoting the report:

> *"The agent is never told the objective nor provided instructions.
> It must autonomously infer the mechanics of each new environment,
> including the win conditions."*

This means:

- **No on-screen text.** No glyphs depicting letters, words, or
  written hints. Forbidden via `forbidden-elements.md` already, but
  worth re-stating: this includes "→" arrows, "X" marks, "?"
  marks, anything that reads as a symbol.
- **No tutorial pop-ups, no narrators, no banners.** The first
  level itself does the teaching by being playable.
- **The win condition must be discoverable.** A level where the
  player can't tell what they're trying to do, even after several
  exploratory actions, has failed. The CHEAT for the game designer
  is: place a target sprite that visually couples to a movable
  sprite (same colour, complementary shape), so the agent sees
  "this slot looks like it wants this block".

The corollary: every visual element must communicate its role
through shape, colour, and behaviour — not through symbol.

## 5. Difficulty through composition (§3.4)

> *"Difficulty is not intended to arise from obscurity or
> increasing complexity. Rather it is intended to arise from the
> composition of reasoning demands acquired over the course of
> play."*

Concrete patterns the report endorses (and the 25 reference games
implement):

- **L1 introduces ONE primary mechanic.** Reduced state space (small
  grid, few obstacles).
- **Each subsequent level adds ONE thing or composes earlier
  things.** L2 introduces a new interaction; L3 requires combining
  L1's mechanic with L2's.
- **Late levels integrate by composing mechanics.** Difficulty
  rises because the planning gets harder (see
  `design-constraints/difficulty-rules.md` § 1, two-stage model:
  exploration + planning).

### Anti-patterns flagged in §3.4 verbatim

- *"Environments centered on a single mechanic that scaled in size
  or difficulty are treated as an anti-pattern."*
- Difficulty from obscurity (e.g., visually similar sprites that
  the player must discriminate by trial-and-error) — implicit
  anti-pattern; the report frames this as "unclear mechanics" that
  drop human completion rates in §5.

### Implication for our 3-level cap

With only 3 levels, the composition arc is:

- **L1**: primary mechanic, alone, small grid, easy. *"Random
  agents can occasionally stumble into success at this stage,
  which is acceptable by design."*
- **L2**: introduces a SECOND mechanic. Level should be solvable
  using primary OR secondary in a basic form (not yet requiring
  composition).
- **L3**: requires BOTH mechanics together in a non-trivial
  composition. This is where the game's identity lives.

If your spec's L3 is "L2 with a bigger grid", you've failed the
composition rule.

## 6. Tutorial level mechanics (§3.4 + §4.2)

The tutorial serves two roles:

1. **Pedagogical**: communicate the core interaction pattern by
   being playable. The player learns the controls, the goal, and
   the affordances within a few exploratory moves.
2. **Scoring-low-impact**: in a 3-level game, L1 is 17% of the
   environment score. Even if a random agent stumbles through, the
   environment cap (and the L2/L3 weights) prevents this from
   inflating the overall result.

Design constraints on the tutorial:

- One primary mechanic active.
- No hazard, or a hazard whose only role is "you bump into a wall
  and nothing bad happens" (no "lose" possible from L1).
- No HUD elements that the player must learn — those introduce
  themselves in L2 or L3.
- Solvable in a small number of actions (the report doesn't pin a
  number; the reference games tend to allow random-policy
  solubility, which empirically means ≤10 actions for many
  tutorials).

## 7. Validation thresholds (§3.5)

Generated games would, in principle, pass these gates if we wired
them in. Currently we do NOT (the user judges manually), but the
spec design should make these gates achievable in case we add them
later:

| Check | Threshold | Implication |
|---|---|---|
| Random play, 50,000 steps | No level beatable by accident (except possibly tutorial). | L2 + L3 should require deliberate sequencing — not "any sequence of moves eventually wins". |
| Random play, 1,000,000 steps | Non-tutorial levels still unbeaten. | Even with massive exploration budget, L2/L3 should require model-formation. |
| Graph-based win-probability | `P(win | random policy) ≤ 1 / 10,000` per level. | Each non-tutorial level should have a small enough "lucky path" that 1 in 10k random sequences would solve it. |
| Recording playback | Known-good action sequences replay deterministically. | Game must be fully deterministic given `(initial_state, action_sequence)`. No hidden randomness. |

Determinism is implicit but worth stating: **no randomness in the
game's transition function**. If a generated game's `step()`
introduces stochasticity (e.g., enemy moves randomly), it fails
the recording-replay check.

## 8. Human calibration — the "easy for humans" floor (§5)

Every NovaPlay environment must pass:

- Tested by 10 people, **at least 2 must independently fully solve
  it** without instructions or prior briefing.
- Soft cutoff: **20 minutes** per environment.
- Hard cutoff: 30 minutes.
- Median session: 7-8 minutes. Successful runs: 8.1 min median.
  Unsuccessful: 5.9 min median (people give up earlier than they
  succeed).

Implications for spec design:

- Aim for "two reasonably-attentive humans solve it in under 20
  minutes". Not "a puzzle expert can crack it given infinite
  time".
- Per-level completion rates are studied for "drop-off points" —
  where humans get stuck. A spec that has L3 unsolvable for 8 of
  10 humans is rejected. Generated games should NOT have a "trick"
  that you only see if you read the source.

## 9. Novelty has TWO axes (§3.4 + §1.3.3)

The report defines novelty along two orthogonal axes:

1. **Vs. preexisting video games.** "Avoid similarities with
   existing games." This is the axis our harness CANNOT
   automatically check — there's no enumeration of every game ever
   made. The user is the final arbiter.
2. **Vs. other NovaPlay environments.** "Each environment is
   required to be novel … with respect to the previously created
   set of environments." Concretely: *"a single program could
   solve two different environments while being at least 50%
   shorter than the concatenation of two independent solution
   programs"* → those environments are insufficiently distinct.

The harness's `mechanic-novelty/similarity-check.md` mechanically
implements axis 2 (against the 25 reference games + prior-games
corpus). Axis 1 must be enforced manually.

§1.3.3 also adds a **third implicit axis**: novelty against the
publicly-available *demonstration* set. The report worries that
training-time exposure to public games can leak into AI
performance. NovaPlay's response: keep the public set
*deliberately unrepresentative* of the private set. The generated
games we produce here are NEW games, not lookalikes of the public
25 — so we're already aligned with the report's intent.

## 10. Public vs private set conventions (§3.6)

This shapes what the 25 reference games "look like" — they are the
**public demonstration set**, deliberately curated for clarity and
fun:

- "Stronger emphasis on clarity and fun."
- "Intentionally easier for both humans and AI."
- "Does not comprehensively represent the mechanics found in the
  private set."

So when we use the 25 games as a style reference, we're inheriting
the **demonstrational** flavour: clear sprite roles, friendly
HUDs, recoverable failure modes. Private-set games are
**out-of-distribution** from this — broader mechanics, deeper
composition. Our generated games should target a similar "clarity
+ fun" flavour because that's what the 25 reference games
implement and the user will be reviewing.

## 11. Implementation discipline (§3.3, §3.5)

Drawn from the studio's own working practices:

- **The engine is Python with a 1,000 fps target.** Generated games
  should be fast: avoid O(n²) per-step computations over the full
  64×64 grid. Iterate over relevant sprite cells, not every cell.
- **Reproducibility is a first-class concern.** Recordings must
  replay. No `random.random()` in `step()`. No wall-clock dependence.
- **The 4-character ID is opaque** to avoid leaking semantic hints
  about goal or mechanics. (Already enforced via
  `code/id-generation.md`.)

## 12. Production process — what the studio actually does (§3.2)

Useful for understanding the cultural context, even if our
single-pass generation pipeline collapses these stages:

| Studio stage | What happens | What our harness collapses to |
|---|---|---|
| **Specification** | Concept review before implementation. | `pick_mechanic` → `write_spec` → `critique_spec`. |
| **Internal** | Prototype + team playtest. | We have no internal playtest; the user takes this role. |
| **External** | External humans test. Calibrates "easy for humans". | Not present in our pipeline. The user does it ad-hoc. |
| **Done** | Final placement in public/private sets. | `finalize` writes to `prior-games/`. |

The report observes throughput is highest with **3-4 environments
in different stages simultaneously**. Our pipeline is single-game-
per-run, single-stage-at-a-time — fine for offline tooling, but
note this is not how the studio actually works.

## 13. Synthesis: a 12-question gate any spec should pass

Use this as the convention-level analogue of
`design-constraints/checklist.md`:

| # | Question | Source |
|---|---|---|
| 1 | Does the game **require exploration** to learn the mechanic? (Not a single-frame puzzle.) | §2.1 |
| 2 | Does the game **reward modelling** — i.e., once mechanics are known, the agent's action count drops sharply? | §2.1, §4.1 |
| 3 | Is the **goal discoverable from the visual layout** without on-screen instructions? | §2.1, §3.4 |
| 4 | Does the game **reward planning** over brute force? (Random play should not solve L2/L3 within ~50k steps.) | §3.5 |
| 5 | Is the **action space minimal** — only the slots actually needed? (Not every game needs all 7 actions.) | §2.3, §3.4 |
| 6 | Are the **mechanics composed** (L3 requires L1 + L2 together, not "L2 with bigger grid")? | §3.4 |
| 7 | Is the **tutorial level intentionally easy** (random agent can sometimes stumble)? | §3.4 |
| 8 | Is the game **deterministic** (no `random.random()` in `step()`)? | §3.5.1 |
| 9 | Is the **per-level optimal action count** small enough that 5× the human baseline is a reasonable budget? | §4.3 |
| 10 | Does the game **avoid all symbols, letters, digits, real-world clipart, and cultural conventions**? | §3.4 |
| 11 | Is the **mechanic novel** vs. existing video games (manual check) AND vs. the 25-game taxonomy + prior-games corpus (automated)? | §3.4, §1.3.3 |
| 12 | Would **2 of 10 untrained humans** plausibly solve it in under 20 minutes? | §5 |

Each "no" is a revision trigger.

## 14. What this file does NOT cover (intentionally)

- **Cell-level visual conventions** (sprite contrast, target-block
  colour pairing, wall density). These derive from analysing the
  25 reference games' rendered frames, not from the report.
  Documented in `conventions/visual-design-rules.md` (when the
  game-analysis workflow produces it).
- **Baseline mechanical features** (energy bar / step counter,
  click-to-select, tag-based grouping). These come from cross-game
  frequency analysis, not from the report. Documented in
  `conventions/baseline-features.md` (same source).
- **Per-level pacing for the 3-level cap.** Derived from analysing
  how 6+ level reference games introduce mechanics across levels,
  then compressing that into our 3-level structure. Documented in
  `conventions/level-pacing-3-of-6.md` (same source).

This file establishes the **soft philosophy**. The other
`conventions/*.md` files (yet to be authored) translate that
philosophy into mechanical patterns derived from the corpus.

---

**Source**: Nova Prize Foundation, *NovaPlay: A New Challenge for
Frontier Agentic Intelligence*, April 22, 2026.
[Original PDF.](https://novaprize.org/media/ARC_AGI_3_Technical_Report.pdf)
