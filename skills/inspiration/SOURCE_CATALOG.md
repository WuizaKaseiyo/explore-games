# External Inspiration Source Catalog

This catalog tells autonomous runs where to look for mechanically
diverse game ideas. These sources are not copied directly into
generated games. The agent extracts abstract mechanic pressure,
exploration shape, and player-learning structure, then converts that
into an NovaPlay-compatible seed.

Use this catalog in `study` and `pick_mechanic` when broadening the
candidate pool. Network access is best-effort; the structured seed
files in this directory are the offline fallback.

## Priority Sources

| source_key | URL | Best for | Sampling rule |
|---|---|---|---|
| `puzzlescript-gallery` | https://www.puzzlescript.net/Gallery/index.html | compact grid rules, small mechanic loops, turn-based puzzle dynamics | sample non-sokoban titles first; extract verb, state mutation, win predicate |
| `clickmazes-ps` | https://clickmazes.com/index-ps.htm | maze variants, path constraints, stateful movement, unusual graph rules | prioritize games whose title hints at state, locks, parity, or topology |
| `pedro-puzzlescript-db` | https://pedros.works/puzzlescript-games-database | broad PuzzleScript corpus discovery | skim titles; skip obvious demakes / sokoban clones / mods unless twist is explicit |
| `awesome-puzzlescript` | https://leetusman.com/awesome-puzzlescript/ | curated authors and notable PuzzleScript works | use as route to high-quality examples, not as a direct mechanic source |
| `ifarchive` | https://ifarchive.org/ | exploration contracts, affordance discovery, inventory/state logic | extract abstract rule-learning structures, not prose themes |
| `ifdb` | https://ifdb.org/ | highly-rated interactive-fiction puzzle structures and reviews | look for games praised for puzzle design, rule discovery, or systems |
| `experimental-gameplay` | https://experimental-gameplay.org/ | unusual interaction prototypes and short experimental loops | extract one strange interaction or player-learning question per game |
| `indiepocalypse` | https://pizzapranks.itch.io/indiepocalypse | short experimental games, zine postmortems, offbeat mechanics | sample issue pages/postmortems for mechanics that fit turn-based abstraction |
| `itch-experimental` | https://itch.io/games/tag-experimental | broad experimental interaction search | use tags and short descriptions; avoid action/reflex/real-time-dependent ideas |
| `gameplay-design-patterns` | https://gameplaydesignpatterns.org/ | abstract design pattern vocabulary | translate patterns into concrete Nova probes and state models |

## Extraction Template

For each sampled source item, extract only these fields:

```markdown
- source_key:
- item_title:
- source_url:
- observed_mechanic:
- exploration_profile:
- primary_skeleton:
- state_model:
- objective_shape:
- discovery_question:
- probe_actions:
- observable_feedback:
- arc_conversion_risk:
```

Do not preserve story, characters, named objects, UI text, cultural
references, real-world trivia, or copyrighted level layouts.

## Sampling Budget

During autonomous `study`, if network is available:

1. Sample 8-12 items total.
2. Use at least 3 different `source_key` values.
3. At least 4 samples must be outside plain PuzzleScript.
4. Prefer sources likely to produce underused skeletons:
   `recipe-composition`, `classification-sorting`, `spatial-constraint`,
   `topology-transform`, and `symbolic-rewrite`.
5. Stop early if the samples already cover 5+ distinct
   `exploration_profile` values.

During `pick_mechanic`, use this catalog to resolve gaps:

- If the local seed pool does not provide enough skeleton diversity,
  sample one more source family.
- If all surviving candidates are low-exploration execution puzzles,
  sample IF / experimental sources before selecting.
- If recent prior-games block common skeletons, sample sources biased
  toward underused skeletons.

## Nova Conversion Filters

Reject or heavily abstract source ideas that require:

- text parsing or natural-language commands;
- cultural knowledge or real-world trivia;
- reflex timing, continuous physics, or dexterity;
- large inventories or long narrative state;
- hidden arbitrary rules that cannot be surfaced visually;
- copyrighted characters, names, layouts, or story premises.

Keep ideas that can be expressed as:

- visible state transformations;
- finite rule induction;
- local or global grid dynamics;
- tool affordances with immediate feedback;
- topology or connectivity changes;
- short resource / quota experiments;
- multi-actor role discovery;
- constraint probing with visible badges or highlights.
