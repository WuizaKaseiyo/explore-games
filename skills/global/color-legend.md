# Color legend (palette values 0..15)

The 64×64 grid uses integer values 0..15 to encode pixel colour.

| Value | Colour |
|-------|--------|
| 0 | white |
| 1 | off-white |
| 2 | light-grey |
| 3 | grey |
| 4 | off-black |
| 5 | black |
| 6 | magenta |
| 7 | pink |
| 8 | red |
| 9 | blue |
| 10 | light-blue |
| 11 | yellow |
| 12 | orange |
| 13 | maroon |
| 14 | green |
| 15 | purple |

A pixel value of `-1` inside a `Sprite.pixels` array means
"transparent / wildcard": the cell defers to whatever is underneath.

For a generated game: pick a small, deliberate palette (typically 3-6
distinct values plus optional wildcard). Do NOT mix every value;
that produces visual noise and breaks the §3.4 "no cultural
conventions" principle (e.g. green=go, red=danger).
