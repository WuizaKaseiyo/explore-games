# study

## Description

First state of the run. Before picking a mechanic, the agent must
become fluent in *what an NovaPlay game is* by reading four
complementary inputs:

1. **The 25 reference-game evidence layer** — for each of the 25
   reference games, read **both** the deep analysis text AND
   the rendered initial-frame screenshots. The screenshots are
   what a player actually sees; the text alone is not enough.

   The 25 reference game IDs:
   `ar25`, `bp35`, `cd82`, `cn04`, `dc22`, `ft09`, `g50t`, `ka59`,
   `lf52`, `lp85`, `ls20`, `m0r0`, `r11l`, `re86`, `s5i5`, `sb26`,
   `sc25`, `sk48`, `sp80`, `su15`, `tn36`, `tr87`, `tu93`, `vc33`,
   `wa30`.

   For each of the 25 game IDs:

   - Open the three rendered screenshots:
     `deep-analysis-3lvls/<id>/level_1.png`,
     `level_2.png`, `level_3.png`. 
   - Read `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`
   

2. **Five reference-game source files in full** — pick five games
   from the 25 that span different mechanic families per
   `mechanic-novelty/taxonomy-of-25-games.md`, then read the actual
   `game_sources_3_lvls/<id>/<hash>/<id>.py` source end-to-end. The
   evidence layer summarises but does not preserve every code
   pattern; full source reading anchors API expectations and
   idioms (sprite-tag conventions, action-handler structure,
   level-data dict usage, HUD widget patterns, win/lose predicates).
   Pick across families — for example one click-only game, one
   arrow-only game, and one click+arrow+modal game.

   **Hard constraint on context budget**: pick games whose source
   is at most ~2000 lines so the five full reads fit comfortably.
   Line counts below are for the 3-level-truncated sources at
   `game_sources_3_lvls/<id>/<hash>/<id>.py`. The largest reference
   games (`lp85` 21k lines, `lf52` 5.8k, `bp35` 4.5k, `dc22` 2.7k,
   `g50t` 2.6k, `sc25` 2.5k, `ft09` 2.3k, `s5i5` 2.0k, `re86` 2.0k)
   are FORBIDDEN as the in-full picks here. The fresh evidence-
   layer files for those games already cover what's relevant. Good
   candidates: `cn04` (620), `sk48` (643), `cd82` (677), `tr87`
   (696), `m0r0` (712), `sp80` (738), `sb26` (827), `wa30` (839),
   `tu93` (1113), `ls20` (1178), `ar25` (1486), `ka59` (1539),
   `r11l` (1706), `vc33` (1940), `su15` (1943), `tn36` (1962).

3. **The NovaPlay design philosophy** — read in full:
   - `skills/conventions/from-tech-report.md` (distilled philosophy)
   - `skills/conventions/cross-cut-frequencies.md` (pre-computed
     counts of which features appear in how many of the 25
     reference games — read it; do NOT re-derive)
   - `skills/design-constraints/core-knowledge-priors.md`
   - `skills/design-constraints/forbidden-elements.md`
   - `skills/design-constraints/composition-and-tutorial.md`
   - `skills/design-constraints/checklist.md`

4. **Read the cached study notes.** Past runs all converged on
   the same observations, so the harness now serves them once
   instead of re-deriving them every run. Read in full:
   `skills/conventions/reference-game-patterns.md` (recurring
   design moves to inherit, recurring anti-patterns to avoid,
   open questions for `pick_mechanic`). Internalise; do NOT
   re-derive into a new `workspace/study-notes.md`.

## Skills
- skills/global
- skills/conventions
- skills/design-constraints
- skills/mechanic-novelty
- skills/mechanism-details *(quick-reference summaries; the
  authoritative evidence layer lives at
  `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`
  and is read directly by step 1 of this state — the deep-analysis
  governs when the two disagree)*

## Next States

### pick_mechanic
**Condition:** All four reading inputs have been completed —
the 25 deep-analyses + screenshots, five reference-game source
files in full, the design-philosophy skill files, and
`skills/conventions/reference-game-patterns.md`. No
`workspace/study-notes.md` is required; the cached patterns
file replaces the per-run write.
**Deliverables:**
- None.
