# Step #02: pick_mechanic

## Inputs Consumed

- Run input seed: empty (autonomous mode)
- mechanic-novelty/taxonomy-of-25-games.md: full table of 25 reference games' mechanic families
- prior-games/index.md: 26 entries (kf42 through tg6w)
- skills/code/id-generation.md: 4-char alphanumeric, lowercase, not a word, not in reserved or prior list
- skills/mechanic-novelty/similarity-check.md: 3-step procedure (family → description → distinguishing rule)
- skills/mechanic-novelty/negative-similarity-check.md: 7-dimension test against priors' rendered frames; reject at ≥3 shared dimensions
- skills/design-constraints/core-knowledge-priors.md: 4 prior categories — mechanic must draw only from these
- (carried from #01 study) Step 5 PuzzleScript demos: 7 newly-fetched + 8 prior session = 15 mechanic vocabulary entries

## Deliverables Produced

- mechanic-pick.md
  - ID: `ej4t` (verified collision-free)
  - family_tag: `radius-scope-influence`
  - One-paragraph description establishing 3 mechanics:
    - L1 base: radius-gated push (only crates within Manhattan R of player respond)
    - L2 add: scope-extender pickups (one-shot consumables grow R by 1)
    - L3 add: colour-keyed sub-radii (concentric red inner R1 + blue outer R2; each colour's elements gated by same-coloured ring)
  - Distinguishing rules vs 4 closest taxonomy near-misses: lq5x, vp6h, kn58, bx84
  - Distinguishing rules vs 4 closest prior-games near-misses: lq5x (also ref), bx84 (also ref), kn58 (also ref), vp6h (also ref), lv4k, pf3w
  - Negative-similarity 7-dim check: ≤2 shared dimensions vs lq5x and kn58 (well under 3-dim reject threshold)
  - Inspiration source: Step 5's `plus_localradius.txt` from Auroriax/PuzzleScriptPlus
  - Considered alternatives: shadow-propagation (rejected — close to vp6h), direction-aware coverage (rejected — close to tn36), Nonogram (rejected — §3.4 ceiling), multi-actor sync (rejected — close to zd7m), robotarm (held for future)

## Notes

### Why this candidate
Step 5 web research surfaced `plus_localradius.txt` whose core idea — "rules apply only within a radius around the player" — has no equivalent in the 25-ref or 26-prior corpus. The PuzzleScript demo itself is a 1-level tech-demo; this candidate composes that core into a 3-level NovaPlay progression by adding scope-extender pickups (L2) and colour-keyed sub-radii (L3).

### Visual signature concern (negative-similarity dim 6)
The ring overlay is a novel visual signature element — no prior renders a Manhattan-diamond ring around the avatar. This is intentional and supports dim-6 divergence vs every prior.

### §3.4 commercial-novelty ceiling concern
`plus_localradius.txt` is itself a tech-demo, not a commercial game. The "radius around player" pattern exists in some stealth/light games (Limbo, Closure) but those games' mechanics differ from `radius-gated push + extender + colour-keyed sub-radii`. The user will judge ceiling at review time per README; this run flags no specific overlap with a famous commercial title.

### Open for write_spec
- Final grid sizes per level (currently 12/14/16)
- Final R values (currently L1 R=2; L2 R=2→3; L3 R1=2 R2=4)
- Ring rendering style (border outline only? gradient fill? checkerboard?)
- Crate / target visual design satisfying checklist item 20 (rich pixel detail) and item 21 (UI teaches by sprite role)
- Step budgets per level
