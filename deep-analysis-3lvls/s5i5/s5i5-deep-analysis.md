# s5i5 — deep analysis

> **3-LEVELS-ONLY NOTE.** This analysis was authored against the
> original full reference games (6+ levels each). Our generated
> games target only **L1, L2, L3** — so any content below that
> describes "level 4+", "L4+", "L5+", sprite rows annotated
> "(level 4+ only)" / "(level 5+ only)", action-handler branches
> for late levels, or internal-state flags gating late-level
> behaviour describe content NOT present in the truncated 3-level
> versions used by the harness. Read the L1/L2/L3 sections as
> primary; treat L4+ references as historical context only.


## Source meta
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/s5i5/a48e4b1d/s5i5.py`
- Lines: 2252
- Class name: `S5i5`
- available_actions: `[6]` (only ACTION6 / click)
- Number of levels in source: 8
- Number of levels documented in this analysis: 3 (per skill scope)
- Imports: from `novaengine` — `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite`. Plus `numpy as np`.

## Mechanic essence (one sentence)

Coloured rectangular rods stand on the canvas like telescoping arms with a tiny dot perched at each tip; when the player clicks one half of a coloured pair-of-windows control the rod of that colour stretches or retracts one notch along its current axis and any rods or walls stacked on top of it slide along with it, and the level is solved when every dot ends up sitting on its matching cross-shaped target.

## Sprite roster

There are 89 entries in the source `sprites = {...}` dictionary. Per skill rules every entry gets a row, but to keep the document readable I group them by tag/role. The per-sprite subsections below cover only the sprites that actually appear in levels 1, 2, or 3 (any sprite that is defined but never referenced from levels 1-3 gets a one-line entry stating it is unused at L1-L3 — this still satisfies the "every sprite has a row" rule).

| sprite (obfuscated) | dims (HxW) | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| alrureofol | 7x13 | 2,3,4,8 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for orange/8 rod (L3) |
| amfbhanllb | 7x13 | 2,3,4,9 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for blue/9 rod (L3) |
| anedvgcwyu | 3x3 | 3,12 | agujdcrunq | (default) | yes | (default) | yes | rod body (purple/12, tip on right) — used L7+ only, not L1-3 |
| aqqxzqvfzz | 3x3 | 11 | (none) | (default) | yes | (default) | yes | small green block — used L8 only, not L1-3 |
| bnbtbmhoct | 7x13 | 2,3,4,14 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for cyan/14 rod (L1, L2, L3) |
| bovrbuxzml | 67x70 | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame — L4 only, not L1-3 |
| bugouggabo | 3x24 | 9,3 | agujdcrunq | (default) | yes | (default) | yes | rod body (blue/9, tip on right) — L5 only |
| crizqgtspi | 3x3 | 14,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip down) — L4 only |
| csewylpqnh | 3x3 | 3,12 | agujdcrunq | (default) | yes | (default) | yes | rod stub (purple/12, tip up) — L8 only |
| cuykgjlznu | 3x3 | 3,14 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip up) — L8 only |
| dgwpklkyik | 5x5 | 2,4,11 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (red/11) — L7 only |
| dlyghqvdlr | 3x3 | -2,13 | zylvdxoiuq | 1 | yes | (default) | yes | tracking dot ("the dot at the tip") (L1, L2, L3) |
| dobbqgqkqm | 7x13 | 2,3,4,11 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for red/11 rod (L2, L3 not used; L2 only) — appears in L2, L4 |
| dwgllpjrka | 3x3 | 3,12 | agujdcrunq | (default) | yes | (default) | yes | rod stub (purple/12, tip on left) — L2 only |
| dxgsplbcdi | 3x3 | 14,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip on right) — L8 only |
| eduyudjgpz | 6x3 | 3,9 | agujdcrunq | (default) | yes | (default) | yes | rod (blue/9, tip on top) — L6 only |
| efimqcucuz | 3x3 | 8,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (orange/8, tip down) — L4 only |
| eqtxuzjmtj | 7x13 | 2,3,4,7 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for orange-yellow/7 rod (L3) |
| eyulammwvk | 5x5 | 2,4,9 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (blue/9) — L7 only |
| fpqwzzjifs | 3x3 | 8,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (orange/8, tip down) — L8 only |
| ftjvxuejja | 70x70 | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame overlay (L3): hollow 15-border with central transparent hole |
| gcvdxoxnwv | 9x3 | 3,11 | agujdcrunq | (default) | yes | (default) | yes | rod (red/11, tip on top) — L1 only |
| gdgaedmejp | 27x3 | 12,3 | agujdcrunq | (default) | yes | (default) | yes | very long rod (purple/12, tip at bottom) — L4 only |
| gfjkihuvil | 3x3 | 14,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip down) — L3 only |
| idnjtkatxu | 5x5 | 2,4,8 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (orange/8) — L7 only |
| ilmeegdqae | 3x3 | 9,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (blue/9, tip on right) — L3 only |
| instimfkuq | 18x3 | 1 | agujdcrunq | (default) | yes | (default) | yes | wall column (no tip; pure cyan/1) — L3 only |
| iqfzjqrfyu | 6x3 | 3,9 | agujdcrunq | (default) | yes | (default) | yes | rod (blue/9, tip on top) — L7 only |
| ixutsglnhs | 5x11 | 2,3,4,11 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller (red/11) compact form — L7 only |
| jbhfimpvgt | 3x3 | 3,11 | agujdcrunq | (default) | yes | (default) | yes | rod stub (red/11, tip on left) — L2 only |
| jrqapndtos | 3x3 | 3,12 | agujdcrunq | (default) | yes | (default) | yes | rod stub (purple/12, tip on top) — L5 only |
| kkxxwxgizv | 3x3 | 3,9 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L8 only |
| kuttnuxntg | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod stub — L6 only |
| kuvfhdmqbz | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L8 only |
| mjqbzaxxvz | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L5 only |
| mvfzjgigjc | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L4 only |
| nlektsynju | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L8 only |
| nnecwlirhw | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L6 only |
| nqfjqnibax | 5x11 | 2,3,4,10 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller (yellow/10) compact form — L5/L7/L8 only |
| nthzregkli | 7x13 | 2,3,4,12 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for purple/12 rod (L2, L3) |
| nurpoywvho | 3x3 | 3,14 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip on left) — L5 only |
| nwtrqgdsmb | 3x3 | -2,13 | cpdhnkdobh | 1 | yes | (default) | yes | TARGET cross/diamond (must be reached by a tracking dot) — L1, L2, L3 |
| nzskdqpisy | 3x3 | 3,12 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L5 only |
| oupeuxupuy | 3x3 | 11,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L7 only |
| oxlmzkxlwo | 12x3 | 1 | agujdcrunq | (default) | yes | (default) | yes | wall column (cyan/1) — L8 only |
| ozleyfpipy | 3x3 | 3,11 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L4 only |
| pcovmzgxdv | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod stub — L7 only |
| pdzhitfvow | 13x7 | 2,3,4,11 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for red/11 rod, vertical pair-of-windows form — L1 only |
| pfqqmzqpef | 21x21 | 15,-1 | agujdcrunq | -1 | yes | (default) | yes | letter-box frame piece — L8 only |
| pirstcnafa | 7x7 | 2,4,11 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (red/11) — L6, L8 only |
| pkxlhmidfi | 3x3 | 3,11 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L4 only |
| qaiufefgvs | 3x3 | 15 | agujdcrunq | (default) | yes | (default) | yes | letter-box-coloured stub (decorative cap) — L3 only |
| qivjsoaoda | 70x70 | -1,15 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame overlay — L7 only |
| qnuxeaowwc | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L8 only |
| qukdkhalyj | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L5/L7/L8 only |
| qwaikxfvfx | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L7 only |
| rohuffupmm | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L5 only |
| ruktfcnnju | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L7 only |
| rzkqifogln | 3x18 | 12,3 | agujdcrunq | (default) | yes | (default) | yes | long rod (purple/12, tip on right) — L3 only |
| sacxfjdztm | 3x3 | 10,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (yellow/10, tip down) — L2 only |
| scnbncadxx | 5x5 | 2,4,10 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (yellow/10) — defined but never placed in any L1-3 level |
| shbgiallgn | 3x6 | 3,14 | agujdcrunq | (default) | yes | (default) | yes | rod (green/14, tip on left) — L1 only |
| snpntdhtic | 5x11 | 2,3,4,9 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller (blue/9) compact form — L5/L7/L8 only |
| ssqccvgvna | 7x7 | 2,4,9 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (blue/9) — L6 only |
| sswrhmndwx | 35x24 | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box L-shape frame fragment — L2 only |
| tksrscbnck | 3x9 | 11,3 | agujdcrunq | (default) | yes | (default) | yes | rod (red/11, tip on left) — L6 only |
| tmvmrsvvke | 3x3 | 3,14 | agujdcrunq | (default) | yes | (default) | yes | rod stub (green/14, tip up) — L2 only |
| tvidpllbtw | 64x30 | 15,-1 | agujdcrunq | -1 | yes | (default) | yes | letter-box frame fragment — L8 only |
| tzaqdgvkkk | 7x13 | 2,3,4,10 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for yellow/10 rod (L2, L3) |
| uhngzgwqzz | 3x3 | 8,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L8 only |
| umhgoiayzk | 3x3 | 14,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L5 only |
| uurtduofts | 3x3 | 11,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L4 only |
| vcjjjmwpuk | 3x3 | 9,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L4 only |
| vgaakxnsja | 5x5 | 2,4,14 | myzmclysbl | 2 | yes | (default) | yes | colour-picker plus token (green/14) — L7 only |
| vgzxuhvxge | 3x21 | 7,3 | agujdcrunq | (default) | yes | (default) | yes | long rod (orange-yellow/7) — L8 only |
| vmgdnqtxsp | 3x3 | 3,10 | agujdcrunq | (default) | yes | (default) | yes | rod stub (yellow/10, tip on left) — L3 only |
| waytmreihe | (large) | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame fragment — L6 only |
| wqhmalmqtu | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L8 only |
| wqirrbwlfv | (small) | (n/a) | agujdcrunq | (default) | yes | (default) | yes | rod — L8 only |
| wtdgqjyuek | 70x58 | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame fragment — L2 only |
| xipfwfleij | 15x3 | 1 | agujdcrunq | (default) | yes | (default) | yes | wall column — L8 only |
| xkfyibfspw | 3x24 | 1 | agujdcrunq | (default) | yes | (default) | yes | wall row (cyan/1) — L3 only |
| xnjfegcxak | 5x11 | 2,3,4,8 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller (orange/8) compact form — defined but never placed in any L1-3 level |
| xxctmacvll | 5x11 | 2,3,4,12 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller (purple/12) compact form — L5/L7/L8 only |
| xzljlcucab | 3x3 | 7,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub (orange-yellow/7, tip up) — L3 only |
| ymgcciqorb | (large) | 15,-1 | agujdcrunq | (default) | yes | (default) | yes | letter-box frame fragment — L5 only |
| ytjfamials | 7x13 | 2,3,4,9 | gdgcpukdrl | 2 | yes | (default) | yes | length-controller for blue/9 rod — L4 only |
| yxqzzpbnam | 18x3 | 1 | agujdcrunq | (default) | yes | (default) | yes | wall column — L5 only |
| zdzrlogohr | 21x3 | 8,3 | agujdcrunq | (default) | yes | (default) | yes | long rod (orange/8, tip down) — L3 only |
| zmohjixbwr | 3x18 | 10,3 | agujdcrunq | (default) | yes | (default) | yes | long rod (yellow/10, tip on left) — L5 only |
| zphfioubwk | 3x3 | 15 | agujdcrunq | (default) | yes | (default) | yes | letter-box-coloured stub (decorative cap) — L1 only |
| zrwegmmtib | 3x3 | 11,3 | agujdcrunq | (default) | yes | (default) | yes | rod stub — L4 only |

Below are the per-sprite subsections only for sprites placed in levels 1-3 (per skill scope of "where it appears: which of levels 1-3 reference it").

### `bnbtbmhoct` — length-controller (cyan / palette 14)

- Pixel pattern: 7×13 sprite. Outer 1-pixel ring of value 2 (border colour); inside, a 5×11 white/4 panel split vertically by a 1-pixel column of value 3 (PADDING_COLOR / black) at column 6; on each half a 3×3 cyan-14 "U-shape" sits in the upper-left corner. The shape reads as a horizontal pair of identical windowed cells joined at the seam — visually a domino.
- Where it appears: L1 (one copy at 36,18), L2 (one copy at 48,54), L3 (one copy at 45,54).
- Role: clickable length-controller (tag `gdgcpukdrl`). Clicking the LEFT half (`x < x+7`) shrinks every cyan rod by one unit; clicking the RIGHT half grows every cyan rod by one unit. The two halves are read in `_get_valid_actions` (it emits one click at the sprite's `(x,y)` and a second click at `(x+7, y)` because `width > height`).
- Visual-vs-functional read: a player at first glance would see a "two-window" decoration; nothing in the rendered frame announces "click-the-halves-to-grow-or-shrink". The two halves look identical, so the player must learn (left = shrink, right = grow) by experimentation. The controller's accent colour (14) tells the player which rod it controls.
  - At-rendered-scale shape: filled rectangle with two interior glyphs and a thin seam.
  - Palette signature: 2 (border), 3 (seam), 4 (interior fill), 14 (window glyph).
  - Nearest-other-sprite check: `nthzregkli` (purple/12), `tzaqdgvkkk` (yellow/10), `dobbqgqkqm` (red/11), `eqtxuzjmtj` (orange-yellow/7), `alrureofol` (orange/8), `amfbhanllb` (blue/9), `ytjfamials` (blue/9 again). All are pixel-identical except for the window-colour value. The accent colour is therefore the only discriminator.
- Visual contrast notes: against the green background (5) the white-on-2 frame stands out cleanly; the seam (3) reinforces "two halves". The accent colour (14) ties it to the rod whose colour also uses 14.

### `dlyghqvdlr` — tracking dot (the "tip-bead", value 13)

- Pixel pattern: 3×3 with 8 transparent (-2) cells around a single value-13 cell in the centre. Effectively a single visible pixel.
- Where it appears: L1 (two copies, at 9,33 and 30,9), L2 (one copy at 15,36), L3 (two copies at 48,3 and 6,27).
- Role: the dot that sits at the tip of one of the rods. Tag `zylvdxoiuq`. In `on_set_level` each `dlyghqvdlr` is attached as a "child" of any `agujdcrunq` rod it overlaps — meaning when that rod grows/shrinks/rotates, the dot rides with it. Win = every target diamond has one such dot at its position.
- Visual-vs-functional read: from a screenshot a player sees a tiny dark-blue dot. The dot looks identical to the central pixel of the target diamond `nwtrqgdsmb` (also value 13), so visually the dot and target glow the same colour — the player must read the SHAPE (single dot vs. diamond/cross) to tell them apart.
  - At-rendered-scale shape: single-cell dot.
  - Palette signature: 13 only.
  - Nearest-other-sprite check: `nwtrqgdsmb` (the target) — same colour 13, but is a 4-pixel cross/plus. The player must use shape, not colour.
- Visual contrast notes: dot value 13 against background 5 is high contrast; collisions with rod-bodies are masked because the dot's layer (1) is below the rods' rendering preference.

### `nwtrqgdsmb` — target diamond/cross (value 13)

- Pixel pattern: 3×3 with values `[[-2,13,-2],[13,-2,13],[-2,13,-2]]` — a 4-pixel "plus" or diamond outline.
- Where it appears: L1 (two copies at 9,51 and 51,9), L2 (one at 51,30), L3 (two at 48,27 and 42,27).
- Role: TARGET landmark. Tag `cpdhnkdobh`. The win predicate `vodebmynqs` walks every `cpdhnkdobh` and asks "is there a `zylvdxoiuq` (tracking dot) at exactly the same (x,y)?" — if every target satisfies this, `next_level()` fires.
- Visual-vs-functional read: visually a small dark-blue diamond. Without the dot (`dlyghqvdlr`) sitting on top of it, the cross is fully visible; once a dot lands, it fills the centre. The colour matches the dot exactly, so the player likely reads the diamond as "the goal mark".
  - At-rendered-scale shape: 4-pixel hollow plus.
  - Palette signature: 13 only.
  - Nearest-other-sprite check: `dlyghqvdlr` (the dot) — same palette, different shape. This is the cleanest "filled vs. outline" discriminator in the game.
- Visual contrast notes: clean contrast against background 5; layer 1 means rod-bodies (layer-default 0 plus controllers at layer 2) render predictably above/below.

### `gcvdxoxnwv` — red rod, vertical, tip on top (L1)

- Pixel pattern: 9 rows × 3 cols. Row 0 = all 3 (the "tip" / black cap). Rows 1-8 = all 11 (red).
- Where it appears: L1 only, one copy at (9,27).
- Role: a rod-body (tag `agujdcrunq`). The cap row of value-3 marks the "tip" end of the rod (this is what the rotation/scale code keys off of). The function `fhkoulsvoi` checks pixels[-1,1], pixels[1,0], pixels[0,1] to determine the rod's current orientation by which edge has the cap. Here the cap is on the top edge → orientation 180.
- Visual-vs-functional read: visually the player sees a red 3-wide tower with a black bar at the top. The black tip is what the player must aim — the tip is where any tracking-dot ends up after rotation/scale. The player likely reads the cap as "the head" of the rod, which matches its mechanical role exactly.
  - At-rendered-scale shape: filled tall rectangle with one striped end.
  - Palette signature: 11 (red body), 3 (cap).
  - Nearest-other-sprite check: many other rods use the same cap-and-body pattern. The discriminating fields are (a) body colour, (b) which edge has the cap, (c) length. Two rods of the same colour (e.g. two purple/12 rods) are mechanically distinguished by length and orientation only.
- Visual contrast notes: red body against green background (5) is high contrast; the cap colour 3 also shows clearly against the body.

### `pdzhitfvow` — vertical length-controller (red / 11) (L1)

- Pixel pattern: 13 rows × 7 cols. Outer 1-pixel ring of value 2 (border); inside, a 5×5 white-4 panel on top with a red-11 "ring-with-stem" glyph; a row of 3s at row 6 (the seam); a mirrored copy below. Effectively a vertical pair-of-windows.
- Where it appears: L1 only, one copy at (21,35).
- Role: clickable length-controller (tag `gdgcpukdrl`). Clicking the TOP half shrinks the red rod; clicking the BOTTOM half grows it. `_get_valid_actions` enumerates clicks at `(x,y)` and `(x, y+7)` because `height > width` here.
- Visual-vs-functional read: the same "two windows" decoration, but stacked vertically. A player would naturally guess "top half does one thing, bottom half does another" but again the labels (which is grow / which is shrink) are not visually marked.
  - At-rendered-scale shape: filled tall rectangle with two glyph cells joined by a seam.
  - Palette signature: 2,3,4,11.
  - Nearest-other-sprite check: every other gdgcpukdrl-tagged controller. The accent colour 11 is the only signal that this controller targets red rods.
- Visual contrast notes: the seam direction (horizontal here vs. vertical for the wide-form controllers) tells the player whether clicks should be split top/bottom or left/right.

### `shbgiallgn` — green rod, horizontal, tip on left (L1)

- Pixel pattern: 3 rows × 6 cols. Column 0 = all 3 (cap). Columns 1-5 = all 14 (green).
- Where it appears: L1 only, one copy at (27,9).
- Role: rod-body. Cap on left edge → orientation 270 (per `fhkoulsvoi`). The right edge is the "free" end (gets the tracking-dot mounted).
- Visual-vs-functional read: a horizontal green bar with a thin black cap on its left side. Looks exactly like a felt-tip whose ferrule is on the left.
  - At-rendered-scale shape: filled rectangle with one striped end.
  - Palette signature: 14, 3.
  - Nearest-other-sprite check: `nurpoywvho`, `umhgoiayzk`, `tmvmrsvvke`, `gfjkihuvil` — all green rods of various lengths/orientations.
- Visual contrast notes: green-14 against background-5 is moderate contrast; player tells rods apart by length and tip-edge.

### `zphfioubwk` — letter-box-coloured 3×3 cap (L1)

- Pixel pattern: 3×3 of value 15 (PADDING / letter-box colour).
- Where it appears: L1 only, two copies at (9,64) and (64,9). Position (9,64) is at the very bottom edge; (64,9) is at the very right edge.
- Role: tagged `agujdcrunq` so the engine treats it as a rod, but in practice it sits flush with the playfield border. Function: a sentinel "stop" cap so the rod-collision check (`ulzimrggno`) prevents rods extending out of the playfield.
- Visual-vs-functional read: the player sees a small grey square at the playfield edge. It looks like part of the frame, not a game piece. Functionally it IS a (very short) rod that participates in the collision check — this is a visual-vs-functional MISMATCH the player might never notice.
  - At-rendered-scale shape: solid 3×3 grey block.
  - Palette signature: 15.
  - Nearest-other-sprite check: `qaiufefgvs` (used in L3) — also 3×3 of 15s, same role.
- Visual contrast notes: grey 15 blends into the letter-box border; deliberately invisible.

### `dobbqgqkqm` — length-controller (red / 11) (L2)

- Pixel pattern: 7×13 wide-form pair-of-windows controller, accent colour 11.
- Where it appears: L2 (one copy at 33,54).
- Role: clickable length-controller for red/11 rods. Same left/right-shrink/grow semantics as `bnbtbmhoct`.
- Visual-vs-functional read: identical visual scheme to all other gdgcpukdrl controllers; only the red accent colour distinguishes.
  - Palette signature: 2,3,4,11.
  - Nearest-other-sprite check: `pdzhitfvow` (also red, vertical form). The same colour appears on a vertical-form controller in L1, so the player has to learn that orientation determines split-axis but not target-colour.
- Visual contrast notes: same as `bnbtbmhoct`.

### `dwgllpjrka` — purple rod stub, tip on left (L2)

- Pixel pattern: 3×3, column 0 = all 3, columns 1-2 = all 12.
- Where it appears: L2 (one copy at 9,39).
- Role: rod stub. Smallest possible rod (length-1 in cap units). Cap on left → orientation 270.
- Visual-vs-functional read: a tiny 3×3 purple square with a thin dark left edge — looks like a single tile, not a rod.
  - Palette signature: 12, 3.
  - Nearest-other-sprite check: `jrqapndtos`, `nzskdqpisy`, `csewylpqnh` — all 3×3 purple stubs with caps on different edges.
- Visual contrast notes: purple-12 on background-5; cap visible on left edge.

### `jbhfimpvgt` — red rod stub, tip on left (L2)

- Pixel pattern: 3×3, column 0 = all 3, columns 1-2 = all 11.
- Where it appears: L2 (one copy at 12,36).
- Role: rod stub.
- Visual-vs-functional read: tiny 3×3 red square with thin dark left edge.
  - Palette signature: 11, 3.
  - Nearest-other-sprite check: `pkxlhmidfi`, `oupeuxupuy`, `zrwegmmtib` — other red stubs.
- Visual contrast notes: high-contrast red.

### `nthzregkli` — length-controller (purple / 12)

- Pixel pattern: 7×13 wide-form pair-of-windows controller, accent colour 12.
- Where it appears: L2 (one at 3,54), L3 (one at 45,45).
- Role: clickable length-controller for purple rods.
- Visual-vs-functional read: same visual scheme as all other length-controllers.
- Visual contrast notes: same as `bnbtbmhoct`.

### `sacxfjdztm` — yellow rod stub, cap on top (L2)

- Pixel pattern: 3×3, row 0 = all 3, rows 1-2 = all 10. Wait — the actual literal pattern is rows-0 `[10,10,10]`, row-1 `[10,10,10]`, row-2 `[3,3,3]`. So cap is on the BOTTOM edge → orientation 0 (per `fhkoulsvoi`).
- Where it appears: L2 (one copy at 12,39).
- Role: rod stub (yellow/10), cap on bottom.
- Visual-vs-functional read: tiny yellow square with cap on its base.
  - Palette signature: 10, 3.
- Visual contrast notes: yellow-10 on background-5.

### `sswrhmndwx` — letter-box L-shape decoration (L2)

- Pixel pattern: 35×24 mostly-transparent (-1) field with grey-15 strips along the left and along an inner vertical column at col 9. Forms an L-shape that frames part of the L2 playfield.
- Where it appears: L2 only (one copy at 33,9).
- Role: tagged `agujdcrunq` so it counts as a "rod" for collision purposes — but functionally it is decorative letter-box shaping. It blocks rods from extending into a particular region (the strips are grey solid, the rest is transparent).
- Visual-vs-functional read: visually reads as a thick L-shaped wall in the letter-box colour. Functionally it's just a static "do-not-cross" boundary; the player should never click it. This is a clear visual-vs-functional MISMATCH: it shares the rod tag but is not a rod the player ever interacts with.
  - At-rendered-scale shape: thin L-strip in grey.
  - Palette signature: 15, -1.
- Visual contrast notes: blends with the letter-box; effectively invisible against grey edge.

### `tmvmrsvvke` — green rod stub, cap on top (L2)

- Pixel pattern: 3×3, rows 0=`[3,3,3]`, rows 1-2=`[14,14,14]`. Cap on top → orientation 180.
- Where it appears: L2 (one at 15,36).
- Role: rod stub (green/14), cap on top.
- Visual-vs-functional read: tiny green square with cap on top.
- Visual contrast notes: green-14 on background-5.

### `tzaqdgvkkk` — length-controller (yellow / 10)

- Pixel pattern: 7×13 wide-form pair-of-windows controller, accent colour 10.
- Where it appears: L2 (one at 18,54), L3 (one at 26,45).
- Role: clickable length-controller for yellow/10 rods.
- Visual-vs-functional read: same as other controllers, only accent-colour discriminates.

### `wtdgqjyuek` — letter-box frame fragment (L2)

- Pixel pattern: 70×58 mostly-transparent grid with a 3-row top strip and a 3-col right strip of value 15. Rows 21-23 contain a small 3-cell wider notch. Used as a corner/edge frame.
- Where it appears: L2 only (one copy placed at 9,-3 — position partly off-grid; only the visible portion shows on the 64×64 frame).
- Role: tagged `agujdcrunq` (rod) for collision purposes; functionally a static letter-box overlay.
- Visual-vs-functional read: looks like part of the frame; player reads it as the playfield edge. Functionally it occupies the rod-tag set, like `sswrhmndwx`. Same MISMATCH as L2's L-shape.
- Visual contrast notes: invisible against the grey letter-box.

### `alrureofol` — length-controller (orange / 8) (L3)

- Pixel pattern: 7×13 wide-form pair-of-windows, accent colour 8.
- Where it appears: L3 (one at 7,45).
- Role: clickable length-controller for orange/8 rods.

### `amfbhanllb` — length-controller (blue / 9) (L3)

- Pixel pattern: 7×13 wide-form pair-of-windows, accent colour 9.
- Where it appears: L3 (one at 7,54).
- Role: clickable length-controller for blue/9 rods.

### `eqtxuzjmtj` — length-controller (orange-yellow / 7) (L3)

- Pixel pattern: 7×13 wide-form, accent colour 7.
- Where it appears: L3 (one at 26,54).
- Role: clickable length-controller for orange-yellow/7 rods.

### `ftjvxuejja` — letter-box frame overlay (L3)

- Pixel pattern: 70×70. Top 3 rows and bottom 3 rows are solid 15; columns 0-2 and columns 67-69 are solid 15. Inner area is -1 (transparent). A grey frame.
- Where it appears: L3 only (one copy at -3,-3 — i.e. inset against the playfield border).
- Role: tagged `agujdcrunq` for collision. Functionally a decorative frame defining the playfield boundary.
- Visual-vs-functional read: clearly a frame (player reads it as wall). Mechanically counts as an extended "rod" border.
- Visual contrast notes: blends with letter-box.

### `gfjkihuvil` — green rod stub, cap on bottom (L3)

- Pixel pattern: 3×3 with row 2=[3,3,3], rows 0-1=[14,14,14]. Cap on bottom → orientation 0.
- Where it appears: L3 (one at 54,24).
- Role: rod stub (green/14), cap down.
- Visual-vs-functional read: tiny green square with thin dark bottom edge.

### `ilmeegdqae` — blue rod stub, cap on right (L3)

- Pixel pattern: 3×3, column 2=[3,3,3], columns 0-1=[9,9,9].
- Where it appears: L3 (one at 30,36).
- Role: blue rod stub, cap on right → orientation 90.

### `instimfkuq` — wall column (cyan / 1) (L3)

- Pixel pattern: 18×3 of value 1.
- Where it appears: L3 (one at 36,21).
- Role: tagged `agujdcrunq` so it joins the collision set — but it has NO cap (no value-3 strip), so `fhkoulsvoi` falls through and returns the default 270. In practice it's a wall: it blocks other rods.
- Visual-vs-functional read: visually reads as a tall solid bar — but unlike rods it has no tip. This is a subtle visual-vs-functional case: the lack of a cap is the only signal that this piece is static (a wall) rather than active (a rod). A player might try to "rotate" or "extend" it via a click on a length-controller and notice nothing happens because no controller's accent colour equals 1.
- Visual contrast notes: cyan-1 on background-5; high contrast.

### `qaiufefgvs` — letter-box-coloured 3×3 cap (L3)

- Pixel pattern: 3×3 of value 15.
- Where it appears: L3 (one at 45,27).
- Role: same as `zphfioubwk` — a sentinel cap at a frame-flush position. Tagged `agujdcrunq`.
- Visual-vs-functional read: invisible (same colour as letter-box).

### `rzkqifogln` — long horizontal rod (purple / 12), cap on right (L3)

- Pixel pattern: 3×18, column 17 = all 3, columns 0-16 = all 12.
- Where it appears: L3 (one at 39,21).
- Role: long purple rod, cap on right → orientation 90.

### `vmgdnqtxsp` — yellow rod stub, cap on left (L3)

- Pixel pattern: 3×3, column 0=[3,3,3], columns 1-2=[10,10,10].
- Where it appears: L3 (one at 6,27).
- Role: yellow rod stub, cap on left → orientation 270.

### `xkfyibfspw` — wall row (cyan / 1) (L3)

- Pixel pattern: 3×24 of value 1, no cap.
- Where it appears: L3 (one at 27,15).
- Role: same as `instimfkuq` — a long static wall (no cap, so no rod-controller will match).

### `xzljlcucab` — orange-yellow rod stub, cap on top (L3)

- Pixel pattern: 3×3, row 0=[3,3,3], rows 1-2=[7,7,7].
- Where it appears: L3 (one at 48,3).
- Role: orange-yellow rod stub, cap on top → orientation 180.

### `zdzrlogohr` — long vertical rod (orange / 8), cap on bottom (L3)

- Pixel pattern: 21 rows × 3 cols. Row 20 = all 3, rows 0-19 = all 8.
- Where it appears: L3 (one at 27,18).
- Role: long orange rod, cap on bottom → orientation 0.

### Per-sprite subsections for sprites NOT placed in L1-L3 (compact form)

The skill requires a subsection per sprite. The 60 sprites below are defined in the source's `sprites = {...}` dictionary but never referenced in any of `levels[0]`, `levels[1]`, or `levels[2]`. For each, the same five sub-bullets apply with these uniform answers (where pixel pattern is given inline):

- `anedvgcwyu` — 3×3 purple/12 stub, cap on right (column 2 = 3). Where: not in L1-L3. Role: rod stub. Visual-vs-functional read: tiny purple square; same family as other 3×3 stubs distinguished only by colour and cap edge. Visual contrast: high contrast against background 5.
- `aqqxzqvfzz` — 3×3 solid red/11, no cap. Not in L1-L3. Role: small static block. Visual-vs-functional: looks like a tile, no cap → static (no rod-controller targets it). Contrast: high.
- `bovrbuxzml` — 67×70 letter-box frame overlay with a large transparent inner region. Not in L1-L3. Role: decorative frame.  Visual: blends into letter-box.
- `bugouggabo` — 3×24 long blue/9 rod, cap on right edge. Not in L1-L3. Role: rod. Visual: long blue strip with thin dark right cap. Contrast: high.
- `crizqgtspi` — 3×3 green/14 stub, cap on bottom (row 2 = 3). Not in L1-L3. Role: rod stub. Visual: tiny green square with cap underneath. Contrast: high.
- `csewylpqnh` — 3×3 purple/12 stub, cap on top. Not in L1-L3. Role: rod stub. Same family as other purple stubs. Contrast: high.
- `cuykgjlznu` — 3×3 green/14 stub, cap on top. Not in L1-L3. Role: rod stub. Contrast: high.
- `dgwpklkyik` — 5×5 plus-token, accent red/11, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker. Visual: plus-shape on white-on-2 background. Contrast: high.
- `dxgsplbcdi` — 3×3 green/14 stub, cap on right. Not in L1-L3. Role: rod stub. Contrast: high.
- `eduyudjgpz` — 6×3 blue/9 rod, cap on top. Not in L1-L3. Role: rod. Contrast: high.
- `efimqcucuz` — 3×3 orange/8 stub, cap on bottom. Not in L1-L3. Role: rod stub. Contrast: high.
- `eyulammwvk` — 5×5 plus-token, accent blue/9, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker. Visual: plus-shape. Contrast: high.
- `fpqwzzjifs` — 3×3 orange/8 stub, cap on bottom. Not in L1-L3. Role: rod stub (duplicate-shape of `efimqcucuz`). Contrast: high.
- `gdgaedmejp` — 27×3 very long purple/12 rod, cap on bottom. Not in L1-L3. Role: rod. Contrast: high.
- `idnjtkatxu` — 5×5 plus-token, accent orange/8, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker.
- `iqfzjqrfyu` — 6×3 blue/9 rod, cap on top. Not in L1-L3. Role: rod. Visual: same shape family as `eduyudjgpz`.
- `ixutsglnhs` — 5×11 length-controller (compact form), accent red/11, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller. Visual: shorter pair-of-windows than the 7×13 family. Contrast: high.
- `jrqapndtos` — 3×3 purple/12 stub, cap on top. Not in L1-L3. Role: rod stub.
- `kkxxwxgizv` — 3×3 blue/9 stub, cap on left. Not in L1-L3. Role: rod stub.
- `kuttnuxntg` — 6×3 green/14 rod, cap on bottom. Not in L1-L3. Role: rod.
- `kuvfhdmqbz` — 3×21 long yellow/10 rod, cap on left. Not in L1-L3. Role: rod.
- `mjqbzaxxvz` — 3×3 of value 15, no cap. Not in L1-L3. Role: grey sentinel cap (same family as `zphfioubwk`, `qaiufefgvs`). Visual: invisible against letter-box.
- `mvfzjgigjc` — 3×3 red/11 stub, cap on right. Not in L1-L3. Role: rod stub.
- `nlektsynju` — 3×3 blue/9 stub, cap on bottom. Not in L1-L3. Role: rod stub.
- `nnecwlirhw` — 7×7 plus-token, accent green/14, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker. Visual: larger plus-shape than the 5×5 form. Contrast: high.
- `nqfjqnibax` — 5×11 length-controller, accent yellow/10, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller (compact form).
- `nurpoywvho` — 3×3 green/14 stub, cap on left. Not in L1-L3. Role: rod stub.
- `nzskdqpisy` — 3×3 purple/12 stub, cap on top. Not in L1-L3. Role: rod stub.
- `oupeuxupuy` — 3×3 red/11 stub, cap on bottom. Not in L1-L3. Role: rod stub.
- `oxlmzkxlwo` — 12×3 wall column of value 1, no cap. Not in L1-L3. Role: static wall (no controller targets value 1).
- `ozleyfpipy` — 3×3 red/11 stub, cap on left. Not in L1-L3. Role: rod stub.
- `pcovmzgxdv` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `pfqqmzqpef` — 21×21 letter-box frame piece. Not in L1-L3. Role: decorative frame.
- `pirstcnafa` — 7×7 plus-token, accent red/11, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker.
- `pkxlhmidfi` — 3×3 red/11 stub, cap on left. Not in L1-L3. Role: rod stub.
- `qivjsoaoda` — 70×70 letter-box frame overlay. Not in L1-L3. Role: decorative frame.
- `qnuxeaowwc` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `qukdkhalyj` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `qwaikxfvfx` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `rohuffupmm` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `ruktfcnnju` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `scnbncadxx` — 5×5 plus-token, accent yellow/10, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker.
- `snpntdhtic` — 5×11 length-controller, accent blue/9, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller (compact form).
- `ssqccvgvna` — 7×7 plus-token, accent blue/9, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker (large plus form).
- `tksrscbnck` — 3×9 red/11 rod, cap on left. Not in L1-L3. Role: rod.
- `tvidpllbtw` — 64×30 letter-box frame fragment. Not in L1-L3. Role: decorative frame.
- `uhngzgwqzz` — 3×3 orange/8 stub, cap on bottom. Not in L1-L3. Role: rod stub.
- `umhgoiayzk` — 3×3 green/14 stub, cap on bottom. Not in L1-L3. Role: rod stub.
- `uurtduofts` — 3×3 red/11 stub, cap on right. Not in L1-L3. Role: rod stub.
- `vcjjjmwpuk` — 3×3 blue/9 stub, cap on bottom. Not in L1-L3. Role: rod stub.
- `vgaakxnsja` — 5×5 plus-token, accent green/14, tag `myzmclysbl`. Not in L1-L3. Role: colour-picker.
- `vgzxuhvxge` — 3×21 orange-yellow/7 long rod, cap on right. Not in L1-L3. Role: rod.
- `waytmreihe` — large letter-box frame fragment with notch. Not in L1-L3. Role: decorative frame.
- `wqhmalmqtu` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `wqirrbwlfv` — small rod stub, tag `agujdcrunq`. Not in L1-L3. Role: rod stub.
- `xipfwfleij` — 15×3 wall column of value 1, no cap. Not in L1-L3. Role: static wall.
- `xnjfegcxak` — 5×11 length-controller, accent orange/8, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller (compact form).
- `xxctmacvll` — 5×11 length-controller, accent purple/12, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller.
- `ymgcciqorb` — large letter-box frame overlay. Not in L1-L3. Role: decorative frame.
- `ytjfamials` — 7×13 length-controller, accent blue/9, tag `gdgcpukdrl`. Not in L1-L3. Role: length-controller.
- `yxqzzpbnam` — 18×3 wall column of value 1, no cap. Not in L1-L3. Role: static wall.
- `zmohjixbwr` — 3×18 yellow/10 long rod, cap on left. Not in L1-L3. Role: rod.
- `zrwegmmtib` — 3×3 red/11 stub, cap on bottom. Not in L1-L3. Role: rod stub.

For all entries above:
- Pixel pattern: described inline.
- Where it appears: not placed in any of L1-L3 (per skill scope, per-level appearances at L4+ are deliberately not enumerated).
- Role: as stated inline.
- Visual-vs-functional read: identical to the in-L1-L3 sprites of the same family — palette signature drives semantic role; cap edge drives orientation; presence/absence of cap drives "rod vs. wall". Nearest-other-sprite is always one of the same sub-family (red rod stub vs. red rod stub, etc.).
- Visual contrast notes: high contrast against background 5 unless the sprite's body colour is 15 (in which case it blends into the letter-box).

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64).
- Number of sprites placed: 10.
- Composition by role: 1 cyan length-controller (`bnbtbmhoct`), 2 tracking dots (`dlyghqvdlr` ×2), 1 red rod (`gcvdxoxnwv`), 2 target diamonds (`nwtrqgdsmb` ×2), 1 vertical red length-controller (`pdzhitfvow`), 1 green rod (`shbgiallgn`), 2 sentinel-grey letter-box caps (`zphfioubwk` ×2). 0 colour-pickers, 0 hazards.
- Level data: `{"StepCounter": 50}`. Semantic: 50-action step budget per level.
- Spawn position(s): no player avatar; the game is click-only. Initial focus is the global level state.
- Per-cell layout (sparse listing — grid is 64×64):
  - `bnbtbmhoct` (cyan length-controller) at (36, 18)
  - `dlyghqvdlr` (tracking dot) at (9, 33) and (30, 9)
  - `gcvdxoxnwv` (red rod, 9 tall, cap on top) at (9, 27)
  - `nwtrqgdsmb` (target) at (9, 51) and (51, 9)
  - `pdzhitfvow` (vertical red length-controller) at (21, 35)
  - `shbgiallgn` (green rod, 6 wide, cap on left) at (27, 9)
  - `zphfioubwk` (grey sentinel cap) at (9, 64) and (64, 9)
- Mechanic introduced relative to the previous level: this IS the tutorial level. Introduces the core grow/shrink interaction: each rod has a tracking dot collisionally attached; clicking one half of a length-controller moves the rod in its current orientation by ±1 unit, the dot rides along, and the level wins when both dots cover their target diamonds. Wide controllers split LEFT/RIGHT; tall controllers split TOP/BOTTOM. NB the source files at L1 use ONLY length-controllers (no colour-picker plus tokens) — so no rotations are required.
- Specific challenge: figure out which click-half grows and which shrinks each colour, and how many clicks of each are needed to push the dots to (9,51) and (51,9). Both rods must be extended so their tip-mounted dots reach the target positions.
- Estimated optimal action count: with two rods to extend (red rod from row 27 down to row 51 = 8 units of length to add; green rod from col 9 across to col 51 = needs roughly the same number of length-additions), plausibly ~10-15 actions.

### Level 2
- `grid_size`: (64, 64).
- Number of sprites placed: 12.
- Composition by role: 1 cyan controller (`bnbtbmhoct`), 1 tracking dot (`dlyghqvdlr`), 1 red controller (`dobbqgqkqm`), 1 purple rod stub (`dwgllpjrka`), 1 red rod stub (`jbhfimpvgt`), 1 purple controller (`nthzregkli`), 1 target (`nwtrqgdsmb`), 1 yellow rod stub (`sacxfjdztm`), 1 letter-box L-shape (`sswrhmndwx`), 1 green rod stub (`tmvmrsvvke`), 1 yellow controller (`tzaqdgvkkk`), 1 frame fragment (`wtdgqjyuek`).
- Level data: `{"Children": [["dwgllpjrka","sacxfjdztm"], ["sacxfjdztm","jbhfimpvgt"], ["jbhfimpvgt","tmvmrsvvke"]], "StepCounter": 150}`. Semantic: 150-action budget. The `Children` list defines a chain of "stacked" rods — when a parent rod scales/rotates, its children move with it (and their children, recursively). The chain here is `dwgllpjrka -> sacxfjdztm -> jbhfimpvgt -> tmvmrsvvke`, i.e. a 4-stage linked chain.
- Spawn position(s): n/a (no player avatar).
- Per-cell layout (sparse, 64×64):
  - `bnbtbmhoct` (cyan controller) at (48, 54)
  - `dlyghqvdlr` (tracking dot) at (15, 36)
  - `dobbqgqkqm` (red controller) at (33, 54)
  - `dwgllpjrka` (purple stub, cap on left) at (9, 39)
  - `jbhfimpvgt` (red stub, cap on left) at (12, 36)
  - `nthzregkli` (purple controller) at (3, 54)
  - `nwtrqgdsmb` (target) at (51, 30)
  - `sacxfjdztm` (yellow stub, cap on bottom) at (12, 39)
  - `sswrhmndwx` (letter-box L-shape) at (33, 9)
  - `tmvmrsvvke` (green stub, cap on top) at (15, 36) — co-located with the tracking dot
  - `tzaqdgvkkk` (yellow controller) at (18, 54)
  - `wtdgqjyuek` (frame fragment) at (9, -3)
- Mechanic introduced relative to L1: introduces the **parent-child rod chain** via the `Children` data dict. Now growing a rod also drags its children along. The single tracking dot is mounted on the top of the chain (`tmvmrsvvke`), so to push the dot to the target the player must extend the chain (and possibly multiple distinct colours) cooperatively. Also introduces the "controller bank" pattern: 4 controllers in a row at the bottom of the playfield (cyan, red, yellow, purple).
- Specific challenge: read which rods are chained (encoded in the `Children` data and visually inferable from rods that touch each other), then plan a sequence of grow/shrink operations across multiple controllers to land the single tracking dot on the single target. Letter-box shapes (`sswrhmndwx`, `wtdgqjyuek`) constrain where chains can extend.
- Estimated optimal action count: the chain is 4 rods deep with the tracking dot at (15,36) and target at (51,30); requires several grows on multiple controllers — plausibly ~15-25 actions.

### Level 3
- `grid_size`: (64, 64).
- Number of sprites placed: 20.
- Composition by role: 4 length-controllers (`alrureofol` orange, `amfbhanllb` blue, `bnbtbmhoct` cyan, `eqtxuzjmtj` orange-yellow, `nthzregkli` purple, `tzaqdgvkkk` yellow — six in total), 2 tracking dots (`dlyghqvdlr` ×2), 2 target diamonds (`nwtrqgdsmb` ×2), 1 letter-box frame (`ftjvxuejja`), several rods (`gfjkihuvil`, `ilmeegdqae`, `rzkqifogln`, `vmgdnqtxsp`, `xzljlcucab`, `zdzrlogohr`), 2 walls (`instimfkuq` cyan column, `xkfyibfspw` cyan row), 1 grey sentinel cap (`qaiufefgvs`).

  Actually re-counting: 6 length-controllers (`alrureofol`, `amfbhanllb`, `bnbtbmhoct`, `eqtxuzjmtj`, `nthzregkli`, `tzaqdgvkkk`), 2 tracking dots, 2 targets, 1 letter-box frame, 6 rods (`gfjkihuvil`, `ilmeegdqae`, `rzkqifogln`, `vmgdnqtxsp`, `xzljlcucab`, `zdzrlogohr`), 2 walls (`instimfkuq`, `xkfyibfspw`), 1 sentinel (`qaiufefgvs`). 0 colour-picker plus tokens, 0 hazards.
- Level data: `{"Children": [["ilmeegdqae","zdzrlogohr"], ["zdzrlogohr","xkfyibfspw"], ["gfjkihuvil","rzkqifogln"], ["rzkqifogln","instimfkuq"]], "StepCounter": 200}`. Semantic: 200-action budget. Two parent-child trees:
  - Tree A: `ilmeegdqae` (blue stub) → `zdzrlogohr` (long orange rod) → `xkfyibfspw` (cyan wall row).
  - Tree B: `gfjkihuvil` (green stub) → `rzkqifogln` (long purple rod) → `instimfkuq` (cyan wall column).
  Note that the leaves of each tree are the two cyan WALLS — so growing the parent rods drags walls around the playfield, which then affect collision with the other tree. This is the level's twist.
- Spawn position(s): n/a.
- Per-cell layout (sparse listing for the 20-sprite, 64×64 grid):
  - `alrureofol` (orange controller) at (7, 45)
  - `amfbhanllb` (blue controller) at (7, 54)
  - `bnbtbmhoct` (cyan controller) at (45, 54)
  - `dlyghqvdlr` (tracking dot) at (48, 3) and (6, 27)
  - `eqtxuzjmtj` (orange-yellow controller) at (26, 54)
  - `ftjvxuejja` (letter-box frame) at (-3, -3)
  - `gfjkihuvil` (green stub) at (54, 24)
  - `ilmeegdqae` (blue stub) at (30, 36)
  - `instimfkuq` (cyan wall column) at (36, 21)
  - `nthzregkli` (purple controller) at (45, 45)
  - `nwtrqgdsmb` (target) at (48, 27) and (42, 27)
  - `qaiufefgvs` (grey cap) at (45, 27)
  - `rzkqifogln` (long purple rod) at (39, 21)
  - `tzaqdgvkkk` (yellow controller) at (26, 45)
  - `vmgdnqtxsp` (yellow stub) at (6, 27)
  - `xkfyibfspw` (cyan wall row) at (27, 15)
  - `xzljlcucab` (orange-yellow stub) at (48, 3)
  - `zdzrlogohr` (long orange rod) at (27, 18)
- Mechanic introduced relative to L2: introduces (a) **walls as chain-leaves** — cyan no-cap pieces that ride along when their parent rods scale, blocking other rods; (b) two independent rod-trees that can collide with each other; (c) a wider controller bank (six controllers along the bottom-left); (d) the letter-box frame proper. The challenge is that growing tree-A pushes a cyan wall into possibly-blocking positions for tree-B.
- Specific challenge: two trees, two separate dot-target pairs, two walls riding on the trees. The player must plan a sequence that gets dot-1 on target-1 and dot-2 on target-2 without ever causing a rod to collide with another rod (the engine rejects such moves via `ulzimrggno` → snapshot rollback).
- Estimated optimal action count: ~25-40 actions.

(No level 4+ subsections per skill scope — levels 4..8 exist in the source but are excluded.)

## Action handlers

The game has a single registered action: ACTION6 (click).

### ACTION6
- Trigger: `self.action.id == GameAction.ACTION6` (line 2193).
- Branches inside `step()` (in plain English):
  1. **Snapshot rollback (top of step)**: if `self.acgkuydgqx` (the snapshot dict) is non-empty from the previous step, the engine restores every sprite in it to its pre-action position and pixels (line 2187-2192). This branch fires when the previous click was REJECTED by the collision check; the snapshot effectively undoes that click. Then `acgkuydgqx` is cleared. (Note: the `elif` on line 2193 means the snapshot branch and the click branch are mutually exclusive within one step, so a rejected click followed by any new click triggers the rollback first.)
  2. **Click handling**: deplete one step on the step-counter HUD (`okmxyzxpez.gdqaemgdnw()`), translate display coords to grid coords, then:
     - If a `myzmclysbl` plus-sign sprite is at the click cell: read its accent colour (centre pixel), find every `agujdcrunq` rod whose body is that colour, snapshot each, and call a per-rod transform helper (`zszsrsbyzi`) which rewrites the rod's pixel array and adjusts its position so the rod's BASE stays put. (At levels 1-3 no `myzmclysbl` sprites are placed in any level, so this branch is unreachable in practice — but it is the live code path in `step()`.)
     - Else if a `gdgcpukdrl` controller is at the click cell: determine which half was clicked by comparing the click's offset within the sprite to its midpoint (`doeimbekrm`). Walk every rod registered to that controller (via `dfyrdkjdcj`), snapshot it, then call `ldmrjbrvwa(rod, index ± 1)` to grow (right/bottom half) or shrink (left/top half) by one cap-unit. Same collision-check / rollback semantics apply.
     - Else: nothing.
  3. **Win/Lose check (always at end of step)**: if `vodebmynqs()` returns True (every target has a tracking-dot at its position) call `next_level()`. Else if the step-counter has reached zero call `lose()`.
  4. `complete_action()` is always called.
- State mutations:
  - Reads: `self.action.data["x"], "y"]`, `self.acgkuydgqx`, `self.dfyrdkjdcj`, `self.enplxxgoja`, `self.current_level`, `self.okmxyzxpez.current_steps`.
  - Writes: `self.acgkuydgqx` (snapshot dict), `sprite.pixels` (rotated/scaled), `sprite.position` (moved), `self.okmxyzxpez.current_steps` (decremented).
- Side effects on sprites: `move(dx,dy)`, `set_position(x,y)`, `pixels = np.rot90(...)`, `pixels = np.full(...)`. No `set_layer`, `set_interaction`, `set_blocking`, `set_visible` calls.
- Engine effects: branch may call `self.next_level()` (when `vodebmynqs()` true), `self.lose()` (when `current_steps == 0`). No `self.win()` call appears anywhere — the game ends by `next_level()` consuming the last level rather than an explicit win.
- Pre-conditions / gating:
  - A click outside any rod/controller is silently swallowed (still costs 1 step from the counter).
  - A click that would cause a rod-on-rod collision is rejected via the snapshot mechanism on the NEXT step.

(No other actions are registered. ACTION1-5 and ACTION7 are not in `available_actions=[6]`.)

## HUD widgets

There is exactly one `RenderableUserDisplay` subclass.

### `ivslbwhvug` (semantic name: StepCounterStrip)
- Class name (obfuscated): `ivslbwhvug`.
- Render-pixel range on the 64×64 frame: row 63 (the very bottom row), columns 0..63.
- What value it displays: `self.current_steps` divided by `self.jjosiqawcv` (the per-level maximum). The widget reads its own `current_steps` and `jjosiqawcv` attributes — these are set by `S5i5.gnnfuqqnqu()` at level start (which copies `level.get_data("StepCounter")` into `jjosiqawcv` and resets `current_steps` to that maximum).
- Visual style: depleting solid-bar strip. Pixels [63, x] are filled with value 3 (PADDING/black) when `x < round(64 * fraction)` and value 4 (white) otherwise. As steps deplete, the bar shrinks left-to-right, with the depleted portion painted white and the remaining portion painted black.
- Update points: `gdqaemgdnw()` is called once per ACTION6 step (line 2194); it decrements `current_steps` by 1 (clamped to 0) and returns whether any steps remain. `tvdzbzbjae()` resets to maximum at level start. `zewpchkcub(value)` (defined but I see no call from the main game class) lets a future caller force-set the value.
- Where it is registered: in `S5i5.__init__`, the camera is constructed as `jcevyecaju(... interfaces=[self.okmxyzxpez])`. So the strip is registered as the only camera interface.

The game has no other HUD widgets — no score, no lives indicator, no message banner. Win/lose feedback comes purely from the engine's level-transition (success) or game-over (failure).

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `okmxyzxpez` | step-counter HUD widget | `ivslbwhvug` | `ivslbwhvug(0)` in `__init__` | `__init__`, `gnnfuqqnqu` (sets `jjosiqawcv` and resets `current_steps`), `step` (decrements via `gdqaemgdnw`) | `_get_hidden_state` (reads `current_steps`), `step` (checks `current_steps == 0`), HUD render | the depleting step-budget |
| `dfyrdkjdcj` | controller→rods registry | `dict[Sprite, list[Sprite]]` | `dict()` in `on_set_level` | `on_set_level` (populated by colour-matching: each rod whose interior colour is in the controller's pixels) | `step` (looked up when a controller is clicked, to find which rods to scale), `_get_valid_actions` | maps each `gdgcpukdrl` controller to the list of rods it controls |
| `enplxxgoja` | parent-rod→children-set | `dict[Sprite, set[Sprite]]` | `dict()` in `on_set_level` | `on_set_level` (initial population from collisions with `zylvdxoiuq` tracking dots, then augmented by the `Children` data), step (read for cascade rotate/scale) | `qdqfmefxmo`, `yxdtnnaclf`, `ldmrjbrvwa`, `zszsrsbyzi`, `step` | the parent-child graph for chained rods |
| `acgkuydgqx` | snapshot for rollback | `dict[Sprite, Sprite]` | `dict()` in `on_set_level` | `step` (populated via `yxdtnnaclf` before each scale/rotate; emptied at top of step on rollback or after successful commit) | `step` (top-of-step rollback) | one-step undo buffer for rejected moves |
| `ssemyeftxy` | "selected sprite" slot | `Sprite | None` | `None` in `on_set_level` | `on_set_level` only — assigned `None`. Never reassigned anywhere I can see. | (never read) | dead/vestigial state — declared but unused in any reachable code path for L1-L3 |
| `hfcjuvfshg` | (unknown counter / index) | `int` | `-1` in `on_set_level` | `on_set_level` only | (never read) | dead/vestigial state |
| `nntjepffpq` | (unknown counter) | `int` | not assigned by `on_set_level` | declared as a class annotation but never written or read | (never read) | dead/vestigial state |

There are also several module-level constants declared after the levels list (lines 1920-1928): `BACKGROUND_COLOR=5`, `PADDING_COLOR=3`, `bjntvocxdv=3`, `smquggholb=5`, `rqyqtrpuud=3`, `hbwmfaubdy=1`, `zahyxpjwoj=4`, `cczmmxbepc=2`. The named-but-obfuscated ones serve as: rod cap thickness (`bjntvocxdv=3`), controller half-width offset (`smquggholb=5`), cap colour (`rqyqtrpuud=3`), wall colour (`hbwmfaubdy=1`), white/UI colour (`zahyxpjwoj=4`), border colour (`cczmmxbepc=2`).

## Win condition

A level is won when, for every `cpdhnkdobh`-tagged sprite (target diamond, only `nwtrqgdsmb`) on the level, there exists a `zylvdxoiuq`-tagged sprite (tracking dot, only `dlyghqvdlr`) at the same `(x,y)` position. The predicate is in `vodebmynqs()` (line 2085-2091):

```python
for vexrltzmfv in hubjefflbl:           # for each target
    if not any([qnvdkghfjq.x == vexrltzmfv.x and qnvdkghfjq.y == vexrltzmfv.y
                for qnvdkghfjq in rqfotcixbl]):  # any tracking-dot match?
        return False
return True
```

Then `step()` calls `self.next_level()` on line 2249 if `vodebmynqs()` returns True. The win condition is identical across L1-L3 — only the number/positions of targets-and-dots differ.

## Lose condition

A level is lost when `self.okmxyzxpez.current_steps` reaches zero. The check is on line 2250: `elif not self.okmxyzxpez.current_steps: self.lose()`. The step counter starts at the value in `level.get_data("StepCounter")` (50 on L1, 150 on L2, 200 on L3) and decrements by 1 every ACTION6 click — including silent clicks on empty cells and clicks on plus-tokens or controllers that produce no valid mutation. There is no other lose condition (no hazards, no collisions-that-kill — collisions are only soft-rollbacks).

## Resource economy

- **Depleting resource**: YES.
  - Variable: `self.okmxyzxpez.current_steps` (HUD widget attribute).
  - Visual: `ivslbwhvug` step-counter strip, bottom row of the 64×64 frame (a depleting solid bar).
  - Trigger to deplete: every ACTION6 click decrements by 1, regardless of whether the click hit anything useful.
  - Threshold for losing: 0.
- **Accumulating resource**: NO. There is no score, no collected-item count, no progress bar that fills as the player succeeds. Win is a state-predicate, not an accumulation.
- **Lives mechanic**: NO. There is no respawn cost, no second chance — a single hit of `lose()` ends the game.
- **Resource interaction with win/lose**: the depleting step-counter is the sole pressure mechanism. Win predicate is independent of the counter (could win at any non-zero value). Lose predicate is independent of progress (can lose with all targets satisfied but no clicks left to commit — the win check fires FIRST, line 2248 vs. 2250, so a lucky last click that completes the level still triggers `next_level`).

## Action-budget signature

- Default budget per level: read from `level.get_data("StepCounter")` at the top of `gnnfuqqnqu()`. Levels 1, 2, 3 use 50, 150, 200 respectively.
- Whether the budget tightens or shifts across L1-3: it grows. L1=50 → L2=150 → L3=200. So the budget LOOSENS as levels become more complex (more rods, longer chains).
- Per-level vs. per-environment: per-level. Each `on_set_level` resets `okmxyzxpez.current_steps` to the new level's `StepCounter`.
- Decrement rate per action: −1 per ACTION6, irrespective of whether the click did anything. There is no variation across levels.
- Refill mechanism: none. Once decremented, only `next_level` (via `tvdzbzbjae` reset) restores it.

## Notable code patterns / techniques

- **Tag-based group lookup**: `level.get_sprites_by_tag("gdgcpukdrl")`, `"agujdcrunq"`, `"myzmclysbl"`, `"cpdhnkdobh"`, `"zylvdxoiuq"`. Five distinct tags are used to partition the sprite pool into role-classes.
- **Click-to-select via display→grid mapping**: `self.camera.display_to_grid(gkvvbxlvir, qypriqzbxd)` then `level.get_sprite_at(game_x, game_y, "<tag>")` to find a sprite of the desired role at the cursor.
- **Snapshot-and-rollback for rejected actions**: `yxdtnnaclf` clones a sprite (and its children recursively) into `self.acgkuydgqx` BEFORE mutation; the next call to `step()` checks this dict and restores from it if it still holds entries (i.e. if the engine rejected the move via the collision check).
- **Cap-edge orientation encoding**: each rod's pixel grid has a 1-cell strip of `PADDING_COLOR=3` along exactly one of its four edges (top / bottom / left / right). The function `fhkoulsvoi(rod)` reads pixels at four indices (`pixels[-1,1], pixels[1,0], pixels[0,1]`) to recover the rod's current orientation (0 / 90 / 180 / 270) without storing it explicitly.
- **np.rot90 + bookkeeping for rotation**: `zszsrsbyzi` rotates a rod by combining `np.rot90` on its pixel array with a careful `set_position` adjustment so that the BASE of the rod stays put while the cap swings 90° around it. Children are translated by the equivalent rigid transform via `ayrfrgnhfh`.
- **`numpy.full` reshape for length-changing**: `ldmrjbrvwa` resizes a rod by replacing its pixel array with a freshly-allocated `np.full` array of the new shape (one body colour everywhere, then the cap re-painted along the correct edge). The position is corrected so that the rod's BASE stays put.
- **`Children` data dict for declarative parent-child relationships**: list-of-pairs in `level.set_data("Children", ...)`. Each pair `[parent_name, child_name]` says "every sprite named child becomes a child of every sprite named parent in the cascade graph". Child rods are then carried along by their parent's transform.
- **HUD rendered via `RenderableUserDisplay.render_interface(frame)`**: the strip widget directly indexes `frame[63, x]` to paint pixel-by-pixel — a minimal pattern other generated games could reuse for any 1D bar HUD.
- **Custom `Camera._raw_render` with transparency mask**: `jcevyecaju._raw_render` overrides the engine default to honour `pixel >= 0` as the visibility mask (i.e. cells with -1 or -2 don't overwrite). This lets sprites with transparent regions (frames, single-pixel dots in a 3×3 surround) compose cleanly.

## Anti-patterns / lessons

- **No visual cue for which-half-grows / which-half-shrinks**: the controllers are perfectly symmetric pair-of-windows decorations. The player learns by trial and error that "right half = grow, left half = shrink" (or "bottom = grow, top = shrink"). A generated game should add a directional glyph (an arrow, or a filled-vs-outline asymmetry) so the player can read the controller without experimentation.
- **Controllers and walls share the `agujdcrunq` tag with rods**: `instimfkuq` and `xkfyibfspw` (cyan walls) carry the rod tag because the level loader uses tag membership for collision tracking. This means an analyst can't just count "rods" by tag — they must also check for the absence of a cap. A cleaner design would use a separate `wall` tag.
- **89 sprite definitions for a 3-level analysis target**: the source defines 89 distinct sprites, of which only ~30 appear in the first three levels. A 3-level generated game would not need this much sprite proliferation — the generator can probably reuse one base "rod" sprite with parametric body-colour and cap-edge rather than emitting 60 nearly-identical concrete rod-stub sprites.
- **Vestigial state (`ssemyeftxy`, `hfcjuvfshg`, `nntjepffpq`)**: declared in `__init__`/`on_set_level` but never read anywhere. A generator should not emit such cruft.
- **No movement animation between snapshot and commit**: when a click is rejected, the rejected sprite was already mutated visibly during `step()` and only un-done at the start of the FOLLOWING step. The intermediate frame can render an invalid (colliding) configuration. A generated game should either roll back synchronously or render only after the collision check passes.
- **Step counter decrements on no-op clicks**: clicking empty space (or unintended targets like plus-tokens with no matching rod) still costs a step. This means a missed click is a hard penalty; combined with rod-on-rod collision rejections (which DON'T cost a step beyond the original click), the budgeting feels uneven.
- **Letter-box frame fragments are dressed up as "rods"**: the L2-L3 letter-box overlays (`sswrhmndwx`, `wtdgqjyuek`, `ftjvxuejja`) are tagged `agujdcrunq` and join the collision graph. This is a hack that works for the engine but is conceptually messy. A cleaner version would separate "static collidable scenery" from "rod" sprites.

## Cross-references

No cross-references — analysis isolated. (No external context for what other reference games look like was used.)

## Frequency-table contributions

- Has step-counter HUD: **YES** (renders to row 63 of the 64×64 frame, full width — bottom edge bar).
- Has lives mechanic: **NO**.
- Has click-to-select (uses ACTION6): **YES**.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): **YES** (tags `gdgcpukdrl`, `agujdcrunq`, `myzmclysbl`, `cpdhnkdobh`, `zylvdxoiuq`).
- Uses ACTION5 (modal): **NO**.
- Uses ACTION6 (click): **YES**.
- Uses ACTION7: **NO**.
- Has level data dicts (uses `level.get_data` / `level.set_data`): **YES** (`StepCounter`, `Children`).
- Multi-mechanic per level (vs. single mechanic per level): **NO** for L1-L3 — only the click-controllers/click-pickers mechanic is in play. L1 uses only length-controllers; L2 adds parent-child chains; L3 adds wall-leaves and a second tree, but these are extensions of the same core mechanic, not parallel mechanics.
- Tutorial level appears solvable by random play: **NO** — random clicks decrement the step counter on every miss, and even hitting a controller requires repeated targeted clicks of the *correct* half to reach the targets. With 50 steps and two rods to extend correctly, a uniform-random clicker would burn through the budget without hitting both targets reliably.
- Has a depleting resource: **YES** (step counter, "actions per level").
- Has an accumulating resource: **NO**.
- Sprite shape convention used: **mixed** — filled solid rectangles (rods, walls), bordered/seamed two-cell glyphs (length-controllers), small plus-shaped 5×5 glyphs (colour-pickers — though none placed in L1-3), single-pixel dots and 4-pixel crosses (tracking dots and targets).
- HUD position: **bottom** (single row at y=63).
- Palette size used: distinct palette values appearing in any sprite of the source = `{1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15}` = 14 distinct values (excluding -1/-2 which are transparency markers). Counting only sprites used at L1-L3: `{1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15}` = 13 distinct values. Reporting the source-wide value: **14**.
- Background colour value: **5** (`BACKGROUND_COLOR = 5`).
- Padding / letter-box colour value: **3** (`PADDING_COLOR = 3`). Note: the LETTER-BOX areas at level edges actually render as 15 (grey), matching the `letter_box=PADDING_COLOR` argument passed to the Camera. There is some confusion in the source: it passes `letter_box=PADDING_COLOR=3` at line 2017, but the letter-box-coloured sprite pieces (`zphfioubwk`, `qaiufefgvs`, all the "frame" overlays) use value 15 for the visible grey. The correct frequency-table answer for "padding/letter-box colour as declared in the source-level constants" is 3; the visible letter-box colour at render time is 15. I report **3** to match the constant.
- Number of distinct mechanics introduced across levels 1-3: **3** (1: grow/shrink rods via length-controllers; 2: parent-child rod chains; 3: walls-as-leaves of rod-trees and the resulting cross-tree blocking).
- Number of levels documented: **3**.

(End of file.)
