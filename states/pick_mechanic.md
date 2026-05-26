# pick_mechanic

## Description
Read the optional one-line seed (provided by the user as a run
input, possibly empty), the static taxonomy of the 25 NovaPlay
reference games (with the deeper per-game evidence layer at
`deep-analysis-3lvls/<id>/<id>-deep-analysis.md`,
and the legacy summaries under `mechanism-details/`), and the
cumulative `prior-games/index.md`. Choose a mechanic family that:

- Draws ONLY from `design-constraints/core-knowledge-priors.md`'s
  four allowed prior categories.
- Does NOT match (per `mechanic-novelty/similarity-check.md`) any
  entry in the taxonomy or in `prior-games/index.md`. For any
  near-miss in the taxonomy, ALSO read the corresponding
  `mechanism-details/<id>.md` to make a more informed
  distinguishing-rule judgement.
- ALSO passes the negative test in
  `mechanic-novelty/negative-similarity-check.md`. The positive
  similarity-check is necessary but not sufficient — a candidate
  with a defensible distinguishing-rule paragraph can still share
  too many surface features with a prior. Walk the seven
  dimensions in `negative-similarity-check.md` and reject the
  candidate if it resembles any single prior on three or more of
  them. This step has caught at least one prior failure (kf42 →
  vh68); the cautionary tale and worked example are in that file.
- Honours the seed (if provided) — the seed sets the family's
  flavour, but novelty constraints still apply.

Produce a one-paragraph description of the chosen mechanic family
with explicit cross-references to the closest taxonomy / prior-game
entries, naming the concrete rule that distinguishes the candidate
from each.

Also generate the candidate's 4-character ID per
`code/id-generation.md` and verify it does not collide.

## Skills
- skills/global
- skills/design-constraints
- skills/mechanic-novelty
- skills/mechanism-details *(quick-reference summaries; for any
  near-miss, the authoritative evidence is at
  `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`)*
- skills/code

## Next States

### write_spec
**Condition:** A novel mechanic family has been chosen, the
similarity check passes against both the taxonomy and the prior-
games index, and a non-colliding 4-character ID has been generated.
**Deliverables:**
- mechanic-pick.md: 4-character ID, mechanic-family tag,
  one-paragraph description, and (per `similarity-check.md`)
  for each near-miss in the taxonomy or prior-games index, the
  concrete distinguishing rule. If `prior-games/index.md` is
  empty, say so.
