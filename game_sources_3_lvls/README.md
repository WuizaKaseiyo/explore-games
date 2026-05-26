# Reference game sources (third-party, truncated to 3 levels)

The **25 reference games** the harness studies for novelty and house
style. They are third-party, MIT-licensed sources, truncated to their
first three levels to match the harness's 3-level rule.

## Layout

```
game_sources_3_lvls/
└── <game_id>/
    └── <version_hash>/
        ├── <game_id>.py       — the NovaBaseGame subclass
        └── metadata.json      — game id, fps, tags
```

The 25 games:

```
ar25  bp35  cd82  cn04  dc22  ft09  g50t  ka59  lf52  lp85
ls20  m0r0  r11l  re86  s5i5  sb26  sc25  sk48  sp80  su15
tn36  tr87  tu93  vc33  wa30
```

Each game directory holds one (or more) version-hash subfolder.

## Notes

- The 4-character ids (`ar25`, `cn04`, …) are opaque aliases; sprite
  names inside each game file are random obfuscated tokens (e.g.
  `fywfjzkxlm`) — the meaningful names were stripped upstream.
- License: MIT (inherited from upstream).
- These sources are reference material for analysing game mechanics
  only — the harness reads them; the players (`play.py`, `web/`) can
  also load and run them.
