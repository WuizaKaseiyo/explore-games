# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (no run seed; autonomous mode)
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- prior-games/index.md (50 entries — kf42 → vk6m)
- skills/design-constraints/{core-knowledge-priors, forbidden-elements}.md
- skills/global/{action-enum, color-legend}.md
- skills/code/id-generation.md
- skills/mechanism-details/* (recap of 25 reference games for distinguishing rules)

## Deliverables Produced
- mechanic-pick.md: ID `qf8m`, family `rook-cross-toggle`, full
  similarity-check + negative-check audit. Verdict NOVEL.

## Notes
- Decision rule: family-flip novelty came from "global rook-cross
  reach + state-flip" not appearing in any of 75 candidate
  references (25 + 50). Closest near-miss is ft09 (local 3×3
  stamp-cycle with constraint-graph win); the distinguishing
  rule is global vs local reach AND state-flip vs cycle-with-
  constraint-rule.
- ACTION6-only is the chosen action subset, putting the
  distinctive verb on slot 6 (per action-enum.md "distinctive
  verb on ACTION6" pattern). ACTION5 / ACTION7 omitted.
- Visual-signature divergence: deliberately chose magenta +
  light-blue + pink palette accents, away from the over-
  represented `{4, 8, 9}` triple flagged by negative-similarity
  cautionary tale.
