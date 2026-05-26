# Generating a 4-character game ID

The ID must be:
- exactly 4 characters,
- lowercase,
- alphanumeric,
- not a recognisable English word,
- NOT colliding with any of the 25 reference IDs,
- NOT colliding with any entry in `prior-games/index.md`.

## Reserved IDs (the 25 reference games)

These are taken; do not reuse:

```
ar25  bp35  cd82  cn04  dc22  ft09  g50t  ka59  lf52  lp85
ls20  m0r0  r11l  re86  s5i5  sb26  sc25  sk48  sp80  su15
tn36  tr87  tu93  vc33  wa30
```

## Recommended generation procedure

1. Pick a random 2-letter prefix (lowercase ASCII, a-z).
2. Pick a random 2-character suffix (lowercase letter or digit
   0-9).
3. Combine into a 4-character ID.
4. Check it is not in the reserved list above AND not in
   `prior-games/index.md`'s `game_id` column.
5. If a collision, regenerate.

The 4-letter version produces 26·26·36·36 = 876,096 distinct IDs.
Collision probability with 1000 prior games is < 0.2% per attempt.

If a chosen ID happens to spell an English word
(e.g. `food`, `face`), regenerate; the ID must be opaque per §3.4.
