# ar25 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/ar25/e3c63847/ar25.py`
- Lines: 1832
- Class name: `Ar25`
- available_actions: [1, 2, 3, 4, 5, 6, 7]
- Number of levels in source: 8 (more than 3 — only 1, 2, 3 are documented per skill scope)
- Number of levels documented in this analysis: 3
- Imports: `math`, `collections.deque`, `typing.Optional`, `typing.TypedDict`, `numpy as np`; from `novaengine`: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite`.

## Mechanic essence (one sentence)

A small coloured shape sits on one side of a long straight mirror line that floats across the playfield, casting a same-shape ghost on the other side; pressing the arrow keys nudges either the shape or the mirror, sliding the ghost in tandem until every dot scattered on the far side is covered by the ghost (or by the shape itself).

## Sprite roster

Total entries in `sprites = {...}`: 51.

Of these, only the following are actually placed in levels 1, 2, or 3: `dlcwjcwyoc`, `qdwjaukgpe`, `vrfjzqaker`, `noaqoztjku`, `zxikvwjsyl`, `ezdsyuixsn`, `jewbedvusb`, `jidgddyrxm`, plus runtime-cloned `sllpppnezc` (selection-flash overlay) and three runtime-cloned `flrtaztmgm` overlay layers. The remaining sprites are either defined but never placed (dead library entries), or placed only in levels 4-8 (excluded from this analysis but listed in the table to remain faithful to the source).

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ayrdgendzn` | 4×3 | 9 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph (paint colour 9, background-coloured); not placed in L1-3 |
| `bdahvvicge` | 5×5 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | game-piece glyph (padding-colour 5); not placed in L1-3 |
| `bvrpiabnip` | 2×5 | 14 | gljpmsnsnx, dmfgetmeus | default | yes | (default) | yes | rotating-on-horizontal-mirror-distance-change game piece; not placed in L1-3 |
| `bygbqopxpx` | 3×3 | 12 | gljpmsnsnx | default | yes | (default) | yes | filled square game-piece glyph; not placed in L1-3 |
| `bzlvolgaii` | 2×3 | 8 | gljpmsnsnx | default | yes | (default) | yes | small game-piece glyph; not placed in L1-3 |
| `cbisykcsod` | 11×15 | 12 | (none) | -11 | yes | (default) | yes | unused decorative library entry; never placed |
| `cqudpppobe` | 2×3 | 9 | gljpmsnsnx | default | yes | (default) | yes | small filled game-piece glyph; not placed in L1-3 |
| `dixkmhikii` | 4×3 | 11 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `dlcwjcwyoc` | 1×41 | 10 | edyhkfhkcf, pwbzvhvyzx, zxikvwjsyl | -5 | yes | (default) | yes | static vertical mirror line (un-selectable); placed in L1 |
| `ezdsyuixsn` | 41×1 | 10 | edyhkfhkcf, sys_click, ezdsyuixsn | -5 | yes | (default) | yes | movable horizontal mirror line; placed in L3 |
| `flrtaztmgm` | 12×12 | -2 | flrtaztmgm | default | yes | (default) | yes | runtime overlay buffer that the renderer paints reflected pixels into (cloned 3× per level for three layer slots) |
| `fsiruetubh` | 3×3 | 9 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `fvjhjlhjuf` | 2×3 | 8 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `gpzuzhlrhg` | 3×3 | 14 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `gvfzzaatcv` | 5×3 | 14 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `hfkrronohx` | 5×4 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `hjulakxurp` | 6×1 | 5 | gljpmsnsnx | default | yes | (default) | yes | thin horizontal bar game-piece; not placed in L1-3 |
| `hylzmztfzg` | 5×2 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | bracket-glyph game-piece; not placed in L1-3 |
| `jewbedvusb` | 4×2 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | T-shape game-piece glyph; placed in L3 |
| `jidgddyrxm` | 4×4 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | L-shape game-piece glyph; placed in L3 |
| `jsfvegkkzt` | 4×2 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | T-stub game-piece glyph; not placed in L1-3 |
| `mcboadguwj` | 1×6 | 5 | gljpmsnsnx | default | yes | (default) | yes | thin vertical bar game-piece; not placed in L1-3 |
| `nkambdndiv` | 5×3 | 11 | gljpmsnsnx | default | yes | (default) | yes | triangle game-piece glyph; not placed in L1-3 |
| `noaqoztjku` | 5×4 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | Z-shape game-piece glyph; placed in L2 |
| `nrgjumocvu` | 3×3 | 5 | gljpmsnsnx | default | yes | (default) | yes | bell game-piece glyph; not placed in L1-3 |
| `ogmsxhaplk` | 2×2 | 11 | (none) | default | yes | (default) | yes | unused decorative library entry; never placed |
| `ozczvjrlvj` | 13×3 | 11 | (none) | default | yes | (default) | yes | unused decorative library entry; never placed |
| `poltvpjvmx` | 3×3 | 12 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `qbnxtboqne` | 4×3 | 15 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `qdwjaukgpe` | 3×4 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | Z-shape game-piece glyph; placed in L1 |
| `qipnjfgkkc` | 5×4 | 9 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `qmeteyzpbi` | 5×3 | 9 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `razhanllyi` | 4×3 | 5 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `rgxjiyepyh` | 3×5 | 11 | gljpmsnsnx | default | yes | (default) | yes | cross-arrow game-piece glyph; not placed in L1-3 |
| `rkowgfsvgp` | 3×3 | 5 | gljpmsnsnx | default | yes | (default) | yes | diagonal game-piece glyph; not placed in L1-3 |
| `sezinyfuyf` | 5×5 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | snake game-piece glyph; not placed in L1-3 |
| `siwmqkomrd` | 3×3 | 15 | gljpmsnsnx | default | yes | (default) | yes | Z-stripe game-piece glyph; not placed in L1-3 |
| `sllpppnezc` | 5×4 | 0 | (none) | 5 | yes | (default) | yes | runtime-cloned cue overlay used as a level-1 hint flash; layered above mirror layer |
| `tsjkpdckto` | 3×5 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `ucyadwewwc` | 1×6 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | thin vertical bar game-piece; not placed in L1-3 |
| `uheevkztwx` | 5×2 | 15 | gljpmsnsnx | default | yes | (default) | yes | game-piece glyph; not placed in L1-3 |
| `ujqxnvjoap` | 5×3 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | hook game-piece glyph; not placed in L1-3 |
| `vrfjzqaker` | 1×1 | 11 | vrfjzqaker | -4 | yes | (default) | yes | single-pixel target dot (must be reflected onto by a piece-ghost) |
| `wexprfkuze` | 11×7 | 15 | (none) | default | yes | (default) | no | invisible decorative library entry; never placed |
| `wfqvujekdi` | 4×4 | 12 | gljpmsnsnx | default | yes | (default) | yes | S-shape game-piece glyph; not placed in L1-3 |
| `wroxfpaeeo` | 3×3 | 8 | gljpmsnsnx, xnpsicjqxc | -2 | yes | (default) | yes | rotates when its distance to vertical mirror changes; not placed in L1-3 |
| `wyxvlfjfoi` | 4×1 | 12 | gljpmsnsnx | default | yes | (default) | yes | thin horizontal bar game-piece; not placed in L1-3 |
| `xjpqgyadus` | 2×2 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | small step-glyph game-piece; not placed in L1-3 |
| `xusbtwzcmm` | 3×7 | 5 | gljpmsnsnx, sys_click | default | yes | (default) | yes | tall S-shape game-piece glyph; not placed in L1-3 |
| `ykqcrphnko` | 4×3 | 12 | gljpmsnsnx, fmxjsieygg | -1 | yes | (default) | yes | game-piece that ONLY reflects across vertical mirror; not placed in L1-3 |
| `zxikvwjsyl` | 1×41 | 10 | edyhkfhkcf, sys_click, zxikvwjsyl | -5 | yes | (default) | yes | movable vertical mirror line; placed in L2 |

### `ayrdgendzn` — colour-9 game piece (background-coloured!)
- Pixel pattern: 4-wide × 3-tall asymmetric blob of palette 9 with transparent (-1) interior — `[[9,9,9],[9,-1,9],[-1,-1,9],[-1,-1,9]]` (note: the literal source matrix is 3 cols × 4 rows; W=3, H=4).
- Where it appears: not placed in levels 1-3.
- Role: candidate game-piece glyph (movable, mirrors-eligible). Shares the player-piece tag `gljpmsnsnx`.
- Visual-vs-functional read: at first glance this is INVISIBLE — palette 9 is the background colour. A player could be confused that there's nothing to grab. Functionally it is a real game piece; the renderer (`gdycxeziaj`) overrides its colour to a different value (the `liirwepfdj` background recolour pipeline).
  - At-rendered-scale shape: thin diagonal-corner glyph.
  - Palette signature: {9}. Shared with the level background colour.
  - Nearest-other-sprite check: similar to `cqudpppobe` (3×2 of 9), `fsiruetubh`, `qmeteyzpbi`, `qipnjfgkkc` — all 9-only game pieces. Tells apart by silhouette.
- Visual contrast notes: hides on background unless renderer recolours; in actual frame the renderer assigns palette 9 to plain pieces and 2 (red) to the currently-selected piece, so contrast comes from selection state.

### `bdahvvicge` — 5-coloured C-bracket game piece (only placed L6+)
- Pixel pattern: 5×5 hollow C of palette 5 with transparent interior.
- Where it appears: not placed in L1-3.
- Role: clickable game piece.
- Visual-vs-functional read: shape reads as a frame/bracket but functions as a movable mirror-target piece.
  - At-rendered-scale shape: hollow ring/glyph.
  - Palette signature: {5}. Shared with the letter-box padding colour.
  - Nearest-other-sprite check: similar in palette to `hfkrronohx`, `jewbedvusb`, all the `gljpmsnsnx + sys_click` glyphs.
- Visual contrast notes: pieces share palette 5 with the letter-box border, so a 5-piece touching the letter-box edge can blend in.

### `bvrpiabnip` — 14-coloured Z piece with rotation-on-distance-change (not placed L1-3)
- Pixel pattern: 2×5 zigzag of palette 14.
- Where it appears: not placed in L1-3.
- Role: game piece that auto-rotates 90° whenever its distance to the horizontal mirror (`hitrtbsoq` / `ezdsyuixsn`) changes.
- Visual-vs-functional read: looks like an ordinary glyph; functionally has hidden distance-tracked rotation behaviour.
  - At-rendered-scale shape: zigzag diagonal glyph.
  - Palette signature: {14}.
  - Nearest-other-sprite check: similar palette to `gpzuzhlrhg`, `gvfzzaatcv`.
- Visual contrast notes: 14 contrasts with the 9 background and with the 10 mirror-line colour.

### `bygbqopxpx` — 3×3 filled palette-12 block (not placed L1-3)
- Pixel pattern: filled 3×3 of value 12.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: solid block; reads as a "block" but is a mover, not a wall.
  - At-rendered-scale shape: solid square.
  - Palette signature: {12}.
  - Nearest-other-sprite check: similar to `poltvpjvmx`, `wfqvujekdi`, `ykqcrphnko` (all 12-coloured).
- Visual contrast notes: solid 12 stands out against 9 background.

### `bzlvolgaii` — small palette-8 plus glyph (not placed L1-3)
- Pixel pattern: 2×3 plus-sign-cap of palette 8.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: small symbol; functions as ordinary piece.
  - At-rendered-scale shape: tiny plus.
  - Palette signature: {8}.
  - Nearest-other-sprite check: shape similar to `fvjhjlhjuf` (also 8-coloured).
- Visual contrast notes: 8 (red-ish) contrasts strongly with the 9 background.

### `cbisykcsod` — large 11×15 ornament (unused library entry)
- Pixel pattern: large lattice of palette 12 (decorative, sym­metric pattern with diagonals and cross-arms).
- Where it appears: never placed in any level.
- Role: dead library entry — defined but unreferenced in the level list. Likely a hint glyph that was cut.
- Visual-vs-functional read: would read as a logo/decoration; doesn't function in-game because never placed.
  - At-rendered-scale shape: lacework/spider.
  - Palette signature: {12}.
  - Nearest-other-sprite check: largest palette-12 shape; would dominate any frame it appeared in.
- Visual contrast notes: 12 vs 9 background, very visually busy. Excluded by being unplaced.

### `cqudpppobe` — small palette-9 filled rectangle (not placed L1-3)
- Pixel pattern: 2×3 filled of palette 9.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: visually invisible at base palette (matches background); renderer reassigns colour. Same caveat as `ayrdgendzn`.
  - At-rendered-scale shape: small block.
  - Palette signature: {9}.
  - Nearest-other-sprite check: family with `ayrdgendzn`, `fsiruetubh`, `qmeteyzpbi`.
- Visual contrast notes: see `ayrdgendzn`.

### `dixkmhikii` — palette-11 zigzag (not placed L1-3)
- Pixel pattern: 4×3 zigzag of palette 11.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary movable glyph.
  - At-rendered-scale shape: lightning bolt.
  - Palette signature: {11}. Shared with `vrfjzqaker` (target dot) — potential confusion.
  - Nearest-other-sprite check: shares palette with `nkambdndiv`, `rgxjiyepyh`, and target dots.
- Visual contrast notes: SHARES palette 11 with the target dots — a player could mistake a moving piece pixel for a target. Distinguishable only by shape (multi-pixel vs single-pixel).

### `dlcwjcwyoc` — STATIC vertical mirror line (Level 1)
- Pixel pattern: 1-wide × 41-tall column of palette 10. Spans the entire 21-row playfield with overhang.
- Where it appears: Level 1, placed at (10, 0) — exactly the centre column of a 21-wide grid. There is one copy.
- Role: fixed (un-selectable) vertical mirror axis. Tagged `pwbzvhvyzx` which marks it un-selectable in the cycling/click logic. The reflection routine treats any sprite tagged `zxikvwjsyl` as a vertical mirror, including this static one.
- Visual-vs-functional read: Same colour and silhouette as the player-controllable `zxikvwjsyl` mirror (also 1×41 of palette 10) — but THIS one cannot be moved or selected. A player would not be able to tell from the rendered frame alone that this mirror is fixed; they discover it by trying to select/move it.
  - At-rendered-scale shape: thin vertical line.
  - Palette signature: {10}. Shared with `zxikvwjsyl` and `ezdsyuixsn`.
  - Nearest-other-sprite check: identical pixel-grid to `zxikvwjsyl` (movable vertical mirror). Distinguishable only by behavioural test, NOT by appearance.
- Visual contrast notes: palette 10 against 9 background is high-contrast; mirror is unmistakable as a mirror but its movability is invisible.

### `ezdsyuixsn` — movable horizontal mirror line (Level 3)
- Pixel pattern: 41-wide × 1-tall row of palette 10.
- Where it appears: Level 3 at (-5, 16) — y=16 row of the playfield (5 cells off the left edge so the line extends past the playfield).
- Role: player-controllable horizontal mirror axis. Reflects across y=16 (i.e. for any input pixel (x, y), produces a ghost at (x, 32 - y)).
- Visual-vs-functional read: looks like a horizontal "wall" but functions as a mirror; pieces appear to pass through it in ghost-form. Player must learn that crossing the line is a reflection, not a collision.
  - At-rendered-scale shape: thin horizontal line.
  - Palette signature: {10}. Same as the vertical mirror.
  - Nearest-other-sprite check: 90°-rotation of `zxikvwjsyl`. Same colour, perpendicular orientation.
- Visual contrast notes: high-contrast against 9 background; orientation alone signals mirror axis direction.

### `flrtaztmgm` — internal pixel-buffer overlay (runtime, all levels)
- Pixel pattern: 12×12 of palette -2 (engine-special "do not draw" sentinel). The actual content is overwritten at runtime with reflected-pixel maps.
- Where it appears: cloned 3 times inside `on_set_level` and added to the level (`vakuvqumo`, `ehoxfqdzf`, `jgzwiwsnn`) at layer 0, -1, -2. Holds three computed reflection maps (one per reflect-rule variant: free / fmxjsieygg / reflect_horizontal_only).
- Role: invisible scratch sprite the renderer uses to compose ghost reflections into a single bitmap layered into the engine's frame.
- Visual-vs-functional read: not a sprite the player sees as a coherent shape — it's a render trick.
  - At-rendered-scale shape: full-grid overlay (rectangle).
  - Palette signature: {-2}. Engine-special.
  - Nearest-other-sprite check: similar concept to `sllpppnezc` (also a runtime overlay), but `sllpppnezc` is a localized cue, not a full-grid pixel buffer.
- Visual contrast notes: invisible by virtue of palette -2 unless replaced by computed pixels.

### `fsiruetubh` — palette-9 L glyph (not placed L1-3)
- Pixel pattern: 3×3 vertical-bar-with-bottom-arm L of palette 9.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: invisible against 9 background until renderer recolours. Same caveat as other 9-pieces.
  - At-rendered-scale shape: L.
  - Palette signature: {9}.
  - Nearest-other-sprite check: family with `ayrdgendzn`, `cqudpppobe`.
- Visual contrast notes: see `ayrdgendzn`.

### `fvjhjlhjuf` — palette-8 plus glyph (not placed L1-3)
- Pixel pattern: 2×3 plus-tip of palette 8.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: small palette-8 mark; ordinary piece.
  - At-rendered-scale shape: plus-tip.
  - Palette signature: {8}.
  - Nearest-other-sprite check: similar to `bzlvolgaii`, `wroxfpaeeo`.
- Visual contrast notes: 8 contrasts with 9 background.

### `gpzuzhlrhg` — palette-14 T glyph (not placed L1-3)
- Pixel pattern: 3×3 T of palette 14.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: T.
  - Palette signature: {14}.
  - Nearest-other-sprite check: family with `bvrpiabnip`, `gvfzzaatcv`.
- Visual contrast notes: 14 contrasts with 9.

### `gvfzzaatcv` — palette-14 V glyph (not placed L1-3)
- Pixel pattern: 5×3 wide-V of palette 14.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: V/funnel; ordinary piece.
  - At-rendered-scale shape: wide V.
  - Palette signature: {14}.
  - Nearest-other-sprite check: similar palette-14 family.
- Visual contrast notes: 14 vs 9.

### `hfkrronohx` — palette-5 squat block-with-feet (not placed L1-3)
- Pixel pattern: 5×4 with two-row solid centre and two pin-feet of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: looks like a creature/totem; functions as ordinary piece.
  - At-rendered-scale shape: figure with feet.
  - Palette signature: {5}. Shared with letter-box.
  - Nearest-other-sprite check: shape distinct from other 5-pieces but palette identical.
- Visual contrast notes: see `bdahvvicge`.

### `hjulakxurp` — palette-5 horizontal bar (not placed L1-3)
- Pixel pattern: 6×1 row of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: looks like a thin wall; functions as a movable piece — potential visual confusion.
  - At-rendered-scale shape: thin horizontal bar.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to `wyxvlfjfoi` (4×1 of 12).
- Visual contrast notes: 5 vs 9 background.

### `hylzmztfzg` — palette-5 angular glyph (not placed L1-3)
- Pixel pattern: 5×2 of palette 5; top row two corners only, bottom row solid.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary piece.
  - At-rendered-scale shape: angular bracket.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to other clickable 5-pieces.
- Visual contrast notes: see other 5-pieces.

### `jewbedvusb` — palette-5 T glyph (Level 3)
- Pixel pattern: 4×2 T-cap of palette 5 — top row full, bottom row middle two.
- Where it appears: Level 3 at (15, 9). One copy.
- Role: clickable game piece — must be moved so its reflection across the horizontal mirror covers a subset of targets.
- Visual-vs-functional read: ordinary game piece.
  - At-rendered-scale shape: T-cap.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to `jsfvegkkzt`, `noaqoztjku`.
- Visual contrast notes: 5 vs 9 background, distinguishable from co-placed `jidgddyrxm` by silhouette.

### `jidgddyrxm` — palette-5 L glyph (Level 3)
- Pixel pattern: 4×4 L (left column + bottom row) of palette 5.
- Where it appears: Level 3 at (4, 7). One copy.
- Role: clickable game piece — second piece in level 3, paired with `jewbedvusb`.
- Visual-vs-functional read: ordinary L piece.
  - At-rendered-scale shape: L.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar palette to `jewbedvusb`; distinguished by L-vs-T silhouette.
- Visual contrast notes: 5 vs 9 background.

### `jsfvegkkzt` — palette-5 small T glyph (not placed L1-3)
- Pixel pattern: 4×2 small T (top row sparse, bottom solid).
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary piece.
  - At-rendered-scale shape: small T.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to `jewbedvusb`.
- Visual contrast notes: see other 5-pieces.

### `mcboadguwj` — palette-5 vertical bar (not placed L1-3)
- Pixel pattern: 1×6 column of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: looks like part of a wall; is a piece.
  - At-rendered-scale shape: thin vertical bar.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to `ucyadwewwc` (also 1×6 of 5, with sys_click).
- Visual contrast notes: see other 5-pieces.

### `nkambdndiv` — palette-11 triangle (not placed L1-3)
- Pixel pattern: 5×3 triangle of palette 11.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph; SHARES palette with target dots.
  - At-rendered-scale shape: triangle.
  - Palette signature: {11}. Shared with `vrfjzqaker`.
  - Nearest-other-sprite check: family with `dixkmhikii`, `rgxjiyepyh`.
- Visual contrast notes: shape vs single pixel distinguishes from targets.

### `noaqoztjku` — palette-5 Z glyph (Level 2)
- Pixel pattern: 5×4 Z made by `[5,5,5,-1,-1] / [-1,-1,5,-1,-1] / [-1,-1,5,-1,-1] / [-1,-1,5,5,5]`.
- Where it appears: Level 2 at (15, 6). One copy — the sole piece in L2.
- Role: clickable game piece in L2.
- Visual-vs-functional read: ordinary Z-shape piece.
  - At-rendered-scale shape: Z.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar Z-family to `qdwjaukgpe`, `xusbtwzcmm`.
- Visual contrast notes: 5 vs 9 background.

### `nrgjumocvu` — palette-5 bell glyph (not placed L1-3)
- Pixel pattern: 3×3 hollow bell of 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: bell/diamond.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `ogmsxhaplk` — palette-11 corner (unused library entry)
- Pixel pattern: 2×2 with three of four cells filled palette 11.
- Where it appears: never placed.
- Role: dead library entry.
- Visual-vs-functional read: a small palette-11 mark would read as a target if placed; cut from levels.
  - At-rendered-scale shape: corner.
  - Palette signature: {11}.
  - Nearest-other-sprite check: similar to `vrfjzqaker` (target dot).
- Visual contrast notes: not relevant — unplaced.

### `ozczvjrlvj` — palette-11 corner-pair-banner (unused library entry)
- Pixel pattern: 13×3 banner with palette-11 pixels at four corners only (rest -1).
- Where it appears: never placed.
- Role: dead library entry; might have been a hint frame.
- Visual-vs-functional read: would read as four target dots in a rectangle.
  - At-rendered-scale shape: 4-corner frame.
  - Palette signature: {11}.
  - Nearest-other-sprite check: visually similar to a cluster of `vrfjzqaker` dots.
- Visual contrast notes: not relevant — unplaced.

### `poltvpjvmx` — palette-12 P glyph (not placed L1-3)
- Pixel pattern: 3×3 P/cross of palette 12.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: P.
  - Palette signature: {12}.
  - Nearest-other-sprite check: family with `bygbqopxpx`, `wfqvujekdi`, `ykqcrphnko`.
- Visual contrast notes: 12 vs 9.

### `qbnxtboqne` — palette-15 hook (not placed L1-3)
- Pixel pattern: 4×3 hook of palette 15.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: hook.
  - Palette signature: {15}.
  - Nearest-other-sprite check: family with `siwmqkomrd`, `uheevkztwx`, `wexprfkuze`.
- Visual contrast notes: 15 vs 9.

### `qdwjaukgpe` — palette-5 Z game piece (Level 1)
- Pixel pattern: 3×4 Z `[[5,5,5],[-1,-1,5],[-1,-1,5],[5,5,5]]`.
- Where it appears: Level 1 at (6, 5). The sole piece in L1.
- Role: clickable game piece — must produce a reflection across the static central mirror that covers all 5 target dots.
- Visual-vs-functional read: ordinary Z piece.
  - At-rendered-scale shape: Z.
  - Palette signature: {5}.
  - Nearest-other-sprite check: similar to `noaqoztjku` (5×4 vs 3×4 Z).
- Visual contrast notes: 5 vs 9 background.

### `qipnjfgkkc` — palette-9 zigzag (not placed L1-3)
- Pixel pattern: 5×4 zigzag of palette 9.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: invisible against background until recoloured.
  - At-rendered-scale shape: zigzag.
  - Palette signature: {9}.
  - Nearest-other-sprite check: family with other 9-pieces.
- Visual contrast notes: see `ayrdgendzn`.

### `qmeteyzpbi` — palette-9 cross-arm (not placed L1-3)
- Pixel pattern: 5×3 of palette 9 with diagonal-cross structure.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: invisible until recoloured.
  - At-rendered-scale shape: scattered cross.
  - Palette signature: {9}.
  - Nearest-other-sprite check: family with other 9-pieces.
- Visual contrast notes: see `ayrdgendzn`.

### `razhanllyi` — palette-5 angular glyph (not placed L1-3)
- Pixel pattern: 4×3 angular shape of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: angular.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `rgxjiyepyh` — palette-11 cross/dagger (not placed L1-3)
- Pixel pattern: 3×5 cross/dagger of palette 11.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: SHARES palette with target dots.
  - At-rendered-scale shape: cross.
  - Palette signature: {11}.
  - Nearest-other-sprite check: family with `dixkmhikii`, `nkambdndiv`, target dots.
- Visual contrast notes: shape distinguishes from single-pixel targets.

### `rkowgfsvgp` — palette-5 diagonal (not placed L1-3)
- Pixel pattern: 3×3 diagonal of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: diagonal.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `sezinyfuyf` — palette-5 snake glyph (not placed L1-3)
- Pixel pattern: 5×5 snake-path of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: snake.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `siwmqkomrd` — palette-15 zigzag (not placed L1-3)
- Pixel pattern: 3×3 zigzag of palette 15.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: zigzag.
  - Palette signature: {15}.
  - Nearest-other-sprite check: 15-piece family.
- Visual contrast notes: 15 vs 9.

### `sllpppnezc` — palette-0 cue overlay (runtime, level 1 only)
- Pixel pattern: 5×4 Z (matches `qdwjaukgpe` shape) but in palette 0.
- Where it appears: cloned at runtime in `on_set_level` and assigned to `self.uehyvizcj`. Toggled visible/invisible (`set_position` to either piece location or off-screen at x=500) during a "blinking" cue at level 1 when steps drop below 50.
- Role: warning blink — when the L1 player has used >14 steps without solving, this cue blinks at the piece position to highlight it.
- Visual-vs-functional read: a flashing Z-shape would read as the piece itself, just in a different colour. This is intentional — it visually says "this is where your piece is."
  - At-rendered-scale shape: Z (mimicking the L1 player piece).
  - Palette signature: {0}.
  - Nearest-other-sprite check: identical silhouette to `qdwjaukgpe` (the L1 piece).
- Visual contrast notes: palette 0 (very dark) vs 9 background; appears as a darker Z layered atop or near the player Z.

### `tsjkpdckto` — palette-5 hook glyph (not placed L1-3)
- Pixel pattern: 3×5 hook of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: hook.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `ucyadwewwc` — palette-5 vertical bar (not placed L1-3)
- Pixel pattern: 1×6 column of palette 5 (sys_click variant of `mcboadguwj`).
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: looks like a wall fragment but is a piece.
  - At-rendered-scale shape: vertical bar.
  - Palette signature: {5}.
  - Nearest-other-sprite check: identical pixels to `mcboadguwj` — only difference is the `sys_click` tag.
- Visual contrast notes: see other 5-pieces.

### `uheevkztwx` — palette-15 zigzag (not placed L1-3)
- Pixel pattern: 5×2 zigzag of palette 15.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: zigzag.
  - Palette signature: {15}.
  - Nearest-other-sprite check: 15-piece family.
- Visual contrast notes: 15 vs 9.

### `ujqxnvjoap` — palette-5 hook (not placed L1-3)
- Pixel pattern: 5×3 hook of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: hook.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `vrfjzqaker` — single-pixel target dot (every level)
- Pixel pattern: 1×1 of palette 11.
- Where it appears: 5 copies in L1 (cluster on the right side); 9 copies in L2 (left side); 26 copies in L3 (scattered around two rectangular target zones plus a central square). Also appears in L4-L8.
- Role: target — every dot must end up covered by either a real piece pixel or a reflected piece-pixel for the level to win (`etzeptsuxx` checks `mqrjslqocj[y, x] >= 0` for every dot).
- Visual-vs-functional read: a single palette-11 pixel reads as a tiny dot. Functionally it is the WIN target.
  - At-rendered-scale shape: single cell.
  - Palette signature: {11}. Shared with several piece glyphs (`dixkmhikii`, `nkambdndiv`, `rgxjiyepyh`, `ogmsxhaplk`, `ozczvjrlvj`) — but those pieces aren't placed in L1-3, so in the documented levels there's no palette confusion.
  - Nearest-other-sprite check: nothing else in L1-3 is a 1×1 cell of palette 11, so unique within scope.
- Visual contrast notes: high contrast against 9 background; clearly stands out as a target marker.

### `wexprfkuze` — invisible 11×7 X (unused library entry)
- Pixel pattern: 11×7 with-X pattern of palette 15. Has `visible=False`.
- Where it appears: never placed.
- Role: dead library entry — possibly a "level complete" splash that was cut.
- Visual-vs-functional read: invisible by definition.
  - At-rendered-scale shape: would be a large X.
  - Palette signature: {15}.
  - Nearest-other-sprite check: only invisible sprite in the roster.
- Visual contrast notes: not relevant — unplaced and invisible.

### `wfqvujekdi` — palette-12 zigzag (not placed L1-3)
- Pixel pattern: 4×4 zigzag of palette 12.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: zigzag.
  - Palette signature: {12}.
  - Nearest-other-sprite check: 12-piece family.
- Visual contrast notes: 12 vs 9.

### `wroxfpaeeo` — palette-8 piece with rotation-on-distance-change (not placed L1-3)
- Pixel pattern: 3×3 zig of palette 8.
- Where it appears: not placed in L1-3.
- Role: game piece tagged `xnpsicjqxc`. When the piece's distance-to-vertical-mirror changes by even one cell, the piece is rotated 90° (`vlnwxwcdzf`). Layer -2.
- Visual-vs-functional read: looks ordinary but has hidden auto-rotate-on-move-near-mirror.
  - At-rendered-scale shape: zig.
  - Palette signature: {8}.
  - Nearest-other-sprite check: 8-piece family.
- Visual contrast notes: 8 vs 9.

### `wyxvlfjfoi` — palette-12 horizontal bar (not placed L1-3)
- Pixel pattern: 4×1 row of palette 12.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph.
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: thin horizontal bar.
  - Palette signature: {12}.
  - Nearest-other-sprite check: 12-piece family.
- Visual contrast notes: 12 vs 9.

### `xjpqgyadus` — palette-5 small step (not placed L1-3)
- Pixel pattern: 2×2 step of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: small step.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `xusbtwzcmm` — palette-5 tall S (not placed L1-3)
- Pixel pattern: 3×7 tall S-curve of palette 5.
- Where it appears: not placed in L1-3.
- Role: game-piece glyph (sys_click).
- Visual-vs-functional read: ordinary glyph.
  - At-rendered-scale shape: tall S.
  - Palette signature: {5}.
  - Nearest-other-sprite check: 5-piece family.
- Visual contrast notes: see other 5-pieces.

### `ykqcrphnko` — palette-12 piece reflectable only across vertical mirror (not placed L1-3)
- Pixel pattern: 4×3 inverted-T-with-cap of palette 12.
- Where it appears: not placed in L1-3.
- Role: game piece with `fmxjsieygg` tag — the reflection routine (`tfvpyidngc` / `irtdqpexfv` / `mbpwomuihy`) skips reflections across non-vertical-mirrors for this sprite. So its ghost only appears across vertical mirrors.
- Visual-vs-functional read: looks ordinary but has hidden mirror-axis restriction.
  - At-rendered-scale shape: inverted-T.
  - Palette signature: {12}.
  - Nearest-other-sprite check: 12-piece family.
- Visual contrast notes: 12 vs 9.

### `zxikvwjsyl` — movable vertical mirror line (Level 2)
- Pixel pattern: 1×41 column of palette 10.
- Where it appears: Level 2 at (12, -3). One copy.
- Role: player-controllable vertical mirror axis. Reflects (x, y) to (2·m.x − x, y).
- Visual-vs-functional read: same colour and shape as the static `dlcwjcwyoc` mirror — a player cannot tell them apart visually.
  - At-rendered-scale shape: thin vertical line.
  - Palette signature: {10}. Shared with `dlcwjcwyoc`, `ezdsyuixsn`.
  - Nearest-other-sprite check: identical pixels to `dlcwjcwyoc`. Distinguished only by selectability.
- Visual contrast notes: high contrast against 9 background.

## Levels 1, 2, and 3 only

**Hard rule note:** the source defines 8 levels. Levels 4-8 are excluded per skill scope.

### Level 1
- `grid_size`: (21, 21)
- Number of sprites placed: 7 (1 static mirror, 1 piece, 5 targets) plus 4 runtime overlay sprites (`uehyvizcj` cue + 3 `flrtaztmgm` reflection buffers) added in `on_set_level`.
- Composition by role: 1 game piece, 1 fixed vertical mirror, 5 single-pixel targets, 0 movable mirrors, 0 hazards, 0 HUD widgets in level data (energy bar drawn from `StepCounter`).
- Level data:
  - `StepCounter`: 64 → maximum step budget read by `tfeokrxpyi` and stored on the energy-bar widget.
  - `edyhkfhkcf`: `["zxikvwjsyl", None]` → metadata (the source code never reads this key; appears unused but stored as level metadata).
- Spawn position(s): the player piece `qdwjaukgpe` starts at (6, 5). The auto-selected sprite (`self.llludejph`) is set to the first non-`pwbzvhvyzx` mirror, falling back to first non-`pwbzvhvyzx` piece — in L1 there is no movable mirror, so the piece itself is the initial selection.
- Per-cell layout (21×21, only non-background cells listed; M = static mirror at column x=10, P = piece footprint, T = target dot):

```
Mirror (M): column x=10, rows y=0..20 (line extends from y=0 down past the playfield)
Piece P (qdwjaukgpe at x=6,y=5): occupies (6,5),(7,5),(8,5),(8,6),(8,7),(6,8),(7,8),(8,8)
Targets T:
  (19,15)
  (17,15) (18,15)
  (17,16)
  (17,17)
```
Coordinate listing of placed non-target sprites: `dlcwjcwyoc` at (10, 0); `qdwjaukgpe` at (6, 5).
- Mechanic introduced relative to the previous level: this is the introductory level — establishes the "reflect-piece-onto-targets" core mechanic with a fixed central vertical mirror (the `pwbzvhvyzx` static-mirror tag). The player only moves the piece.
- Specific challenge: Reflect a Z-shape across the central x=10 mirror so its ghost lands exactly on a five-target arrangement on the right half of the grid. Player only has piece-movement; they must work out the destination by mental reflection.
- Estimated optimal action count: ~10-12 moves (one ACTION6 click on the piece if needed, then ~9 directional steps to position the piece so its reflection covers the targets — the piece at (6,5) needs to move so that its mirrored ghost covers the 5 targets clustered around (17-19, 15-17)).

### Level 2
- `grid_size`: (21, 21)
- Number of sprites placed: 11 (1 piece, 1 movable vertical mirror, 9 targets) plus runtime overlays.
- Composition by role: 1 game piece, 1 movable vertical mirror, 9 targets, 0 fixed mirrors, 0 hazards.
- Level data:
  - `StepCounter`: 64
  - `edyhkfhkcf`: `["zxikvwjsyl", None]` (unused metadata)
- Spawn position(s): piece `noaqoztjku` at (15, 6); movable mirror `zxikvwjsyl` at (12, -3) — the mirror is partly above the visible playfield (it's 41 tall and the y origin is -3, so it extends from y=-3 to y=37, fully covering the 21-row playfield). The auto-selected sprite is the mirror (first non-`pwbzvhvyzx` `edyhkfhkcf`-tagged sprite).
- Per-cell layout:

```
Mirror (M): column x=12 (movable left/right via ACTION3/ACTION4)
Piece P (noaqoztjku at x=15,y=6): footprint (15..19, 6..9)
Targets T:
  (5,14) (4,14) (3,14)        (left cluster, row 14)
  (3,15) (3,16) (3,17) (2,17) (1,17)  (left cluster, rows 15-17)
```
Coordinate listing of placed non-target sprites: `noaqoztjku` at (15, 6); `zxikvwjsyl` at (12, -3).
- Mechanic introduced relative to the previous level: introduces a MOVABLE vertical mirror (the `zxikvwjsyl` `sys_click` mirror, distinct from L1's `pwbzvhvyzx` static mirror). The player must now coordinate two movable objects — piece and mirror — using ACTION5 cycling or ACTION6 clicks to switch focus.
- Specific challenge: the piece is on the right at (15, 6) and the targets are on the left (rows 14-17). The player must (a) move the mirror to the right x-position, (b) move the piece to the right y-position, so the mirror reflects the piece-shape exactly onto the 9-dot cluster. Mirror motion is restricted to horizontal (its `iyaddaovv` is forced to 0 in step()).
- Estimated optimal action count: ~15-25 moves (mirror translation + piece translation, ideally interleaved).

### Level 3
- `grid_size`: (21, 21)
- Number of sprites placed: 29 (2 pieces, 1 movable horizontal mirror, 26 targets) plus runtime overlays.
- Composition by role: 2 game pieces, 1 movable horizontal mirror, 26 targets, 0 fixed mirrors, 0 hazards.
- Level data:
  - `StepCounter`: 128 (doubled from L1/L2)
  - `edyhkfhkcf`: `["zxikvwjsyl", None]` (unused metadata)
- Spawn position(s): `jewbedvusb` (T-piece) at (15, 9); `jidgddyrxm` (L-piece) at (4, 7); `ezdsyuixsn` (horizontal mirror) at (-5, 16) — the mirror is at row y=16 extending past the left edge. Auto-selection picks the mirror first.
- Per-cell layout (coordinate listing because there are 29 placed sprites):

```
Mirror M (ezdsyuixsn at x=-5,y=16): row y=16, length 41, fully spans x=0..20
Piece A (jewbedvusb at x=15,y=9): T-shape, footprint (15..18, 9..10)
Piece B (jidgddyrxm at x=4,y=7):   L-shape, footprint (4..7, 7..10)
Targets T (26 of them):
  Row 1:  (11,1) (12,1) (13,1) (14,1)
  Row 2:  (11,2)
  Row 3:  (4,3) (5,3) (11,3)
  Row 4:  (3,4) (4,4) (5,4) (6,4) (11,4)
  Row 14: (3,14) (4,14) (5,14) (6,14) (11,14)
  Row 15: (4,15) (5,15) (11,15)
  Row 16: (11,16)
  Row 17: (11,17) (12,17) (13,17) (14,17)
```
- Mechanic introduced relative to the previous level: introduces (a) a HORIZONTAL movable mirror (`ezdsyuixsn`, perpendicular orientation to L1/L2 mirror — its `pshzrdxfu` is forced to 0, so it moves only vertically), (b) a SECOND game piece — so the player now manages three selectable objects (mirror + 2 pieces) and must cycle/click between them.
- Specific challenge: There are two target clusters above the mirror line (rows 1-4) and two clusters below (rows 14-17). The targets are arranged so that each piece's reflection across y=16 covers one half, and the pieces themselves cover the other half. The player must (a) move the mirror to a y-row that makes the geometry work, (b) position both pieces so all 26 targets get covered by the union of {real pixels, reflected pixels} from both pieces. Step budget is 128.
- Estimated optimal action count: ~30-50 moves.

(Levels 4-8 exist in the source but are excluded per skill scope.)

## Action handlers

### ACTION1 (UP)
- Trigger: `self.action.id == GameAction.ACTION1`.
- Branches inside `step()`: enters the directional-move branch (`iyaddaovv = -1`, `pshzrdxfu = 0`). If the currently-selected sprite (`self.llludejph`) is `pwbzvhvyzx`-tagged (e.g. L1's static mirror), the action is rejected via `complete_action()`. Else, computes new (x, y), checks playfield-edge gating (special-cased so a mirror-line that is `zxikvwjsyl`-tagged is allowed to be y-out-of-range, and one that is `ezdsyuixsn`-tagged is allowed to be x-out-of-range — because mirror lines extend past the grid by design). Pushes current state onto `self.usukvgwle` (undo stack), applies the move, runs the rotation-on-distance-change pass for any `xnpsicjqxc`/`dmfgetmeus` piece, recomputes the three reflection-buffer overlays via `hqiorgefxt`, checks win via `etzeptsuxx`, decrements energy via `self.zdrbnrjbr.tihzupejat()` and triggers `lose()` if energy hits 0. If the level-1 cue condition fires (level_index==1, current_steps<50, not yet shown), kicks off the blink animation by setting `self.cnlzdmmso = 1`.
- State mutations: reads `self.llludejph`, `self.action`, `self.huzumkfia`, `self.aqnahsxpq`, `self.hnepuikbu`, `self.hitrtbsoq`, `self.ueryufapb`, `self.zdrbnrjbr.current_steps`, `self.level_index`, `self.cnlzdmmso`, `self.mewxgwwty`. Writes `self.usukvgwle`, `self.llludejph` position, `self.ueryufapb` (rotation-tracking dict), `self.mllqetvjb` (win flag), `self.cnlzdmmso`, `self.zdrbnrjbr.current_steps`.
- Side effects on sprites: `self.llludejph.set_position(...)`; for any rotation-tracked piece, `vlnwxwcdzf` rotates the piece's pixel grid 90°. The three `flrtaztmgm` overlay sprites have their `pixels` overwritten by `hqiorgefxt`.
- Engine effects: may call `self.lose()` (if energy depletes) or set `self.mllqetvjb = True` (which on the next step causes `self.next_level()`).
- Pre-conditions / gating: rejected silently if `self.llludejph` is `pwbzvhvyzx`-tagged or None. Edge-bounds check rejects moves that would push a non-mirror sprite off-grid.

### ACTION2 (DOWN)
- Identical to ACTION1 except `iyaddaovv = +1`. Same gating, same state mutations, same side effects.

### ACTION3 (LEFT)
- Identical to ACTION1 except `pshzrdxfu = -1`, `iyaddaovv = 0`. Note that for a `zxikvwjsyl`-tagged mirror, `iyaddaovv` is force-set to 0 too, but this action's primary axis is x — so a vertical mirror moves left.
- A horizontal mirror (`ezdsyuixsn`) has `pshzrdxfu` zeroed by `if "ezdsyuixsn" in tags: pshzrdxfu = 0` — so ACTION3 is a no-op for it.

### ACTION4 (RIGHT)
- Identical to ACTION3 except `pshzrdxfu = +1`. Same axis-locking rules.

### ACTION5 (CYCLE / TAB-SELECT)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: increments `self.ijwojcjri`, sets `self.tikqecuwc = True`, computes `dnolnhhsxs = (current_index + 1) % len(self.xefwpvwoh)` and assigns the new sprite as `self.llludejph`. If selection actually changed, sets `self.mewxgwwty = True`.
- State mutations: writes `self.ijwojcjri`, `self.tikqecuwc`, `self.llludejph`, `self.mewxgwwty`. Reads `self.xefwpvwoh`. Decrements energy via `self.zdrbnrjbr.tihzupejat()` — so cycling COSTS A STEP (and can lose the game if energy depletes mid-cycle).
- Side effects on sprites: none directly.
- Engine effects: may `self.lose()` if energy depletes.
- Pre-conditions / gating: `_get_valid_actions` only allows ACTION5 if `len(xefwpvwoh) > 1` and `ijwojcjri < len(xefwpvwoh) - 1` — so the agent can't cycle past the full set in a single uninterrupted cycling burst. The `ijwojcjri` counter is reset on any non-ACTION5 action.

### ACTION6 (CLICK / POINT-SELECT)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: reads `(x, y)` from `self.action.data`, converts display→grid via `self.camera.display_to_grid`. Calls `self.joedjescta(grid_x, grid_y)` to find sprites under the cursor. Filters: prefers `gljpmsnsnx` (game piece) over `edyhkfhkcf` (mirror); among multiple game pieces, sorts by tag priority (`reflect_horizontal_only` → 1, `fmxjsieygg` → 2, default → 3) and picks the highest. If no piece at click, picks among mirrors with toggle behaviour: if multiple mirrors at the click cell, alternate between vertical and horizontal. Falls back: if `self.llludejph` is None after click, defaults to first non-`pwbzvhvyzx` mirror, else first non-`pwbzvhvyzx` piece.
- State mutations: writes `self.llludejph`, `self.mewxgwwty`.
- Side effects on sprites: none directly (just selection change).
- Engine effects: none beyond `complete_action`.
- Pre-conditions / gating: out-of-bounds clicks return no sprites; selection silently keeps current value.

### ACTION7 (UNDO)
- Trigger: `self.action.id == GameAction.ACTION7`.
- Branches: pops the most recent state from `self.usukvgwle` (a stack of `gluxplkybg` snapshots) and restores piece + mirror positions via `self.wmpufuwdcm(state)`, which also calls `self.hqiorgefxt()` to rebuild reflection overlays.
- State mutations: writes `self.usukvgwle`, every entry in `self.migkdsjrwk` and `self.khupblbrxc` positions (via `set_position`).
- Side effects on sprites: position rollback; reflection-buffer recompute.
- Engine effects: none — does NOT decrement energy.
- Pre-conditions / gating: if the stack is empty, becomes a no-op (still calls `complete_action`).

(No actions outside `available_actions` are referenced in the source.)

## HUD widgets

Two `RenderableUserDisplay` subclasses are defined and registered:

### `hpnnoufcuc` — energy bar (vertical strip on right edge)
- Class name (obfuscated): `hpnnoufcuc`.
- Render-pixel range: column x=63 (the rightmost pixel column of the 64×64 frame); rows y=0..63 (full vertical strip).
- What value it displays: `self.current_steps` (steps remaining), initialised from level data `StepCounter` and decremented per move/cycle.
- Visual style: depleting vertical strip with banded colour stages — palette cycle is `[11, 12, 15, 8, 14]` (indices 0..4). When max steps > 64, the bar partitions into multiple bands of 64 (using the `jwuswyyoje` calculation); the depleted portion is drawn in the next-band colour and the remaining portion in the current-band colour.
- Update points: written by `tihzupejat` (called once per directional move and once per ACTION5 cycle), reset by `iuxztfbzql` (called on level start via `tfeokrxpyi`), set by `qbypqckyqm`.
- Where it is registered: in `Camera(interfaces=[self.cxnxzbeld, self.zdrbnrjbr])` in `__init__`. The energy widget is `self.zdrbnrjbr`.

### `gdycxeziaj` — playfield projector / grid renderer
- Class name (obfuscated): `gdycxeziaj`.
- Render-pixel range: a centred sub-square of the 64×64 frame, sized to fit the 21×21 grid at integer scale (scale=3 typically: 21·3=63, leaves 1px margin). Drawn into roughly rows 2..63 cols 2..63 with a 1px border padding.
- What value it displays: a synthesised 21×21 cell grid combining (a) actual sprite pixels, (b) reflected ghost pixels from `self.tfvpyidngc()` look-ups, (c) target dots highlighted in palette `dqailkzmtf` (=11), (d) currently-selected piece highlighted in palette `xwfrtwinpo` (=0), (e) dimmed-pieces in palette `liirwepfdj` (=BACKGROUND_COLOR=9), (f) `pwbzvhvyzx` static-mirror in palette `tuovamceti` (=5).
- Visual style: full-grid mosaic at scale 3, 4, or 5 px-per-cell depending on grid size. Per-cell single-pixel paint at scale 3, 4-pixel block at scale 4, single-pixel at scale 5. Layered priority via `ujlfpharwy` ranks: target=4 > selected=2 > static-mirror=3 / piece=3 > background=1.
- Update points: re-rendered every frame; reads `self.huzumkfia`, `self.aqnahsxpq`, `self.tfvpyidngc()`, `self.llludejph`, `self.mqedygxur`, `self.khupblbrxc`.
- Where it is registered: same `Camera(interfaces=[...])` list in `__init__`. The widget is `self.cxnxzbeld`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `self.cxnxzbeld` | playfield-projector widget | `gdycxeziaj` | new instance | `__init__` | engine renderer | renders the 21×21 grid into the 64×64 frame |
| `self.zdrbnrjbr` | energy-bar widget | `hpnnoufcuc` | new instance with budget=0 | `__init__`, `tfeokrxpyi` | step gating, render | tracks step budget per level |
| `self.usukvgwle` | undo stack | `list[gluxplkybg]` | `[]` | `__init__`, `on_set_level`, ACTION1-4 (push), ACTION7 (pop) | ACTION7 | stores piece+mirror position snapshots |
| `self.ijwojcjri` | consecutive-cycle counter | `int` | 0 | `on_set_level`, ACTION5 | `_get_valid_actions` | gates how many times ACTION5 may fire in a row |
| `self.tikqecuwc` | last-action-was-cycle flag | `bool` | False | `on_set_level`, `step` (top), ACTION5 | (only written) | sticky flag for step-loop logic |
| `self.mewxgwwty` | selection-changed flag | `bool` | False | `on_set_level`, ACTION5, ACTION6 | level-1 cue gate (`step`) | suppresses the L1 step-warning blink once selection has been changed |
| `self.cnlzdmmso` | L1 cue-blink animation tick | `int` | 0 | `on_set_level`, ACTION1-4 (set to 1 when condition fires), step (incremented when >0) | `step` (animation loop) | drives the 8-tick blink overlay positioning |
| `self.uehyvizcj` | cue-blink overlay sprite | `Sprite` | clone of `sllpppnezc` | `on_set_level`, `step` (set_position) | renderer | the dark-Z blink at the player piece |
| `self.ueryufapb` | piece→last-distance-to-mirror dict | `dict[Sprite, int]` | `{}` | `on_set_level`, ACTION1-4 (after move) | ACTION1-4 (rotation trigger) | tracks rotation triggers for `xnpsicjqxc`/`dmfgetmeus` pieces |
| `self.mllqetvjb` | win-pending flag | `bool` | False | `on_set_level`, ACTION1-4 (set on win) | step (top) | one-frame delay before `next_level()` |
| `self.llludejph` | currently-selected sprite | `Sprite | None` | first non-`pwbzvhvyzx` mirror or piece | `on_set_level`, ACTION5, ACTION6 | step (move dispatch), `_get_valid_actions`, renderer | the focus piece for movement |
| `self.huzumkfia` | grid width | `int` | grid_size[0] | `on_set_level` | many | playfield width |
| `self.aqnahsxpq` | grid height | `int` | grid_size[1] | `on_set_level` | many | playfield height |
| `self.migkdsjrwk` | game-piece list | `list[Sprite]` | sprites tagged `gljpmsnsnx` | `on_set_level` | `step`, `tfvpyidngc`, `irtdqpexfv`, undo-snapshot | all movable player pieces |
| `self.mqedygxur` | target-dot list | `list[Sprite]` | sprites tagged `vrfjzqaker` | `on_set_level` | `etzeptsuxx`, renderer | the win-target dots |
| `self.vakuvqumo` | reflection overlay buffer (free) | `Sprite` (clone of `flrtaztmgm`) | level-added with layer 0 | `on_set_level`, `hqiorgefxt` | renderer | scratch buffer for default-reflection ghosts |
| `self.ehoxfqdzf` | reflection overlay buffer (vertical-only) | `Sprite` (clone of `flrtaztmgm`) | level-added with layer -1 | `on_set_level`, `hqiorgefxt` | renderer | scratch buffer for `fmxjsieygg`-pieces |
| `self.jgzwiwsnn` | reflection overlay buffer (horizontal-only) | `Sprite` (clone of `flrtaztmgm`) | level-added with layer -2 | `on_set_level`, `hqiorgefxt` | renderer | scratch buffer for `reflect_horizontal_only`-pieces |
| `self.khupblbrxc` | mirror-line list | `list[Sprite]` | sprites tagged `edyhkfhkcf` | `on_set_level` | step, reflection routines | all mirror axes (movable + static) |
| `self.hnepuikbu` | vertical-mirror reference | `Sprite | None` | first sprite with `zxikvwjsyl` tag in `khupblbrxc` | `on_set_level` | `zngkctyvrs`, ACTION1-4 | quick handle for vertical mirror |
| `self.hitrtbsoq` | horizontal-mirror reference | `Sprite | None` | first sprite with `ezdsyuixsn` tag in `khupblbrxc` | `on_set_level` | `zngkctyvrs`, ACTION1-4 | quick handle for horizontal mirror |
| `self.xefwpvwoh` | cycle-selection list | `list[Sprite]` | mirrors + pieces minus `pwbzvhvyzx` | `on_set_level` | ACTION5, `_get_valid_actions` | ordered list ACTION5 cycles through |

## Win condition

Plain-English: every target dot (sprite tagged `vrfjzqaker`) must, on the player's current frame, be covered by either a real piece pixel or a reflected piece-ghost pixel.

Literal condition (in `etzeptsuxx`):
```
mqrjslqocj = self.jhajdrieqn()      # 21x21 array of (max-of-three reflection layers + actual-pixel layer)
for each target dot:
    if mqrjslqocj[dot.y, dot.x] < 0:
        return False
return True
```
When `etzeptsuxx()` returns True at the end of a directional-move action, the game sets `self.mllqetvjb = True`. On the NEXT step (any action), the top of `step()` checks this flag and calls `self.next_level()`. (See lines 1690-1693 and 1746-1748.)

Win condition is the same across levels 1, 2, 3 — only the target arrangement changes.

## Lose condition

Plain-English: the player runs out of step budget. Each directional move (ACTION1/2/3/4) decrements steps by 1 if it actually moves a sprite (i.e. `pshzrdxfu != 0 or iyaddaovv != 0`); each ACTION5 cycle ALSO decrements by 1.

Literal condition (in `step()`, both the directional-move branch and the ACTION5 branch):
```
if not self.zdrbnrjbr.tihzupejat():    # tihzupejat decrements then returns current_steps > 0
    self.lose()
```

`tihzupejat` returns False when current_steps falls to 0 after a decrement, triggering `self.lose()`.

## Resource economy

- Depleting resource (energy / step counter / lives):
  - YES: a step counter. Variable: `self.zdrbnrjbr.current_steps`. Visual: vertical right-edge bar drawn by the `hpnnoufcuc` widget (banded palette cycle 11/12/15/8/14). Trigger to deplete: any directional move that actually translates a sprite (ACTION1-4 with non-zero displacement) and any ACTION5 cycle. Threshold for losing: 0 (when `current_steps` reaches 0, `self.lose()` fires).
- Accumulating resource (collected items, score, sequence progress):
  - NO accumulating counter. Win is a single-frame predicate evaluated each move (every target covered simultaneously). There is no partial-progress meter.
- Lives mechanic (respawn cost):
  - NO. There is one `self.lose()` call site; no life counter, no respawn.
- Resource interaction with win/lose: depleting steps is the sole losing condition. Win is unrelated to resource — winning with 1 step left is fine. ACTION7 (undo) does NOT refund a step (and energy was decremented on the prior move, so undo is a free reroll of position only).

## Action-budget signature

- Default budget per level: read from `level.get_data("StepCounter")` in `tfeokrxpyi`. Levels 1, 2 use 64; level 3 uses 128. (Levels 4-8 in source use 128/128/320/320/320 — out of scope.)
- Whether budget tightens or shifts across levels 1-3: budget DOUBLES from L2 (64) to L3 (128) — accommodating the extra piece and extra-axis-mirror.
- Per-level vs. per-environment: per-level — `tfeokrxpyi` runs once per `on_set_level` and resets the bar.
- Decrement rate per action: −1 per directional move that actually translates a sprite (i.e. not bounded out, not blocked by `pwbzvhvyzx` selection) and −1 per ACTION5 cycle. ACTION6 (click) and ACTION7 (undo) do NOT decrement.
- Refill mechanism: only `iuxztfbzql` (called from `tfeokrxpyi` on level start). No mid-level refills.

## Notable code patterns / techniques

- BFS-based reflection composition: `tfvpyidngc`, `irtdqpexfv`, `mbpwomuihy` use a `deque` BFS bounded at depth 12 to compose reflections through chains of mirrors. Each step of BFS reflects the current pixel across each `khupblbrxc` mirror in turn. This natively supports multi-mirror compositions (mirror-of-mirror) without explicit handling.
- Tag-based reflect-axis filtering: a single `fmxjsieygg` tag on a sprite says "only reflect across vertical mirrors"; `reflect_horizontal_only` (referenced in code, not on any defined sprite in this file) says the inverse. The reflection routine checks these inside the BFS loop (`if "fmxjsieygg" in sprite.tags and xqebhtjxoa != "zxikvwjsyl": continue`).
- Three-layer overlay buffer pattern: three runtime-cloned `flrtaztmgm` sprites at layers 0, -1, -2 hold three reflection maps (free / vertical-only / horizontal-only); layered with priority via `jhajdrieqn` so the renderer composites them correctly.
- Click-to-select with type-aware tie-breaking: in ACTION6, when the click hits multiple sprites at the same cell, a key function ranks pieces by tag (`reflect_horizontal_only` < `fmxjsieygg` < default), and when only mirrors are at the click cell, toggles between vertical and horizontal mirrors so a click on their intersection alternates the focus.
- Undo via state-snapshot stack: `gluxplkybg` TypedDict captures piece + mirror positions; ACTION1-4 push, ACTION7 pops and replays via `wmpufuwdcm`. Free undo (no step cost).
- Auto-rotate-on-distance-change: `ueryufapb` records each tagged piece's distance to its associated mirror at level start; after each move, re-checks and calls `vlnwxwcdzf` (numpy rot90 + recentre) when distance shifts. (Defined but never triggered in L1-3 because no `xnpsicjqxc`/`dmfgetmeus` pieces are placed there.)
- Mirror-axis movement-locking: in step(), `if "zxikvwjsyl" in self.llludejph.tags: iyaddaovv = 0` (vertical mirrors can only move horizontally) and the symmetric clause for `ezdsyuixsn` (horizontal mirrors can only move vertically). Bounds-checks also skip the perpendicular-axis bound to allow mirrors to extend past the playfield.
- Off-screen "hidden" position via x=500: the cue overlay sprite is parked at `_x = 500` (off-screen) and brought back during the blink animation by setting position to the player piece location — a cheap "show/hide" trick that avoids `set_visible` overhead.
- Render-time palette remapping: the `gdycxeziaj` renderer ignores each sprite's actual palette and reassigns based on role (selected = 0, target = 11, piece = 9 background-coloured to "blend in", static-mirror = 5). This means sprite palettes in the source mostly don't drive the on-screen colour.

## Anti-patterns / lessons

- Levels 4-8 push complexity well beyond a 3-level cap (320-step budgets, dozens of targets); a generated 3-level game should NOT inherit this depth.
- The static `dlcwjcwyoc` mirror in L1 is visually identical to L2's movable `zxikvwjsyl` mirror — same colour, same silhouette, same orientation — but cannot be selected. A player has no visual cue that L1's mirror is fixed; they discover it by failing to interact. A generated game should give static and movable mirrors visually distinct treatments (different palette, dashed vs solid).
- The renderer overrides sprite palette at render time, so the source-side sprite palette is misleading documentation: a piece declared as "palette 5" might render in palette 9 (background tint) or 0 (selected highlight) depending on state. A generated game should align declared palette with rendered palette so the source is self-documenting.
- Many sprites (≈30+) are defined but never placed (dead library entries: `ayrdgendzn`, `bdahvvicge`, `bvrpiabnip`, `bygbqopxpx`, `bzlvolgaii`, `cbisykcsod`, `cqudpppobe`, `dixkmhikii`, `fsiruetubh`, `fvjhjlhjuf`, `gpzuzhlrhg`, `gvfzzaatcv`, `hfkrronohx` (L7+ only), `hjulakxurp`, `mcboadguwj`, `nkambdndiv`, `nrgjumocvu`, `ogmsxhaplk`, `ozczvjrlvj`, `poltvpjvmx`, `qbnxtboqne`, `qipnjfgkkc`, `qmeteyzpbi`, `razhanllyi`, `rgxjiyepyh`, `rkowgfsvgp`, `siwmqkomrd`, `uheevkztwx`, `wexprfkuze`, `wfqvujekdi`, `wroxfpaeeo`, `wyxvlfjfoi`, `xjpqgyadus`, `ykqcrphnko`). A generated game's sprite roster should be tightly scoped to placed sprites only.
- ACTION5 (cycle selection) costs a step. A player who needs to cycle to find the right object pays for the cycling. This is harsh — a generated game might let cycling/clicking be free.
- The step counter combines "navigate" cost with "switch focus" cost; one step budget for both makes the failure mode opaque (player loses without knowing whether they were inefficient at moving or at switching). Splitting the budget would make the loss diagnosable.
- Level 1's "blink the piece after >14 wasted steps" is a one-shot cue tied to a hard-coded `level_index == 1` check. A generated game should either give every level the same hint scaffolding or none at all, not silently special-case L1.
- `vrfjzqaker` (target dot) shares palette 11 with three unplaced piece glyphs (`dixkmhikii`, `nkambdndiv`, `rgxjiyepyh`); if any of those glyphs were placed in the same level as targets, the target dots would visually merge with piece pixels. Cross-game palette-uniqueness for target sprites is the safer convention.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES — vertical strip on right edge, column x=63, drawn by `hpnnoufcuc`.
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`gljpmsnsnx`, `vrfjzqaker`, `edyhkfhkcf`).
- Uses ACTION5 (modal): YES — selection cycler.
- Uses ACTION6 (click): YES.
- Uses ACTION7: YES — undo last move.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES — `level.get_data("StepCounter")` only; `set_data` is not called in this source.
- Multi-mechanic per level (vs. single mechanic per level): NO — all levels share the same mechanic (reflect-piece-onto-targets); levels differ in geometry, count of pieces, and mirror axis, not in rules.
- Tutorial level appears solvable by random play: NO — Level 1 requires precise reflection across a fixed mirror; random moves on a 21×21 grid against a 5-target cluster within 64 steps is extremely unlikely.
- Has a depleting resource: YES — step counter (decrements −1 per move and per cycle).
- Has an accumulating resource: NO.
- Sprite shape convention used: mixed — single-cell targets, long thin lines for mirrors, multi-cell glyphs for pieces (mostly hollow/hatched silhouettes).
- HUD position: corner/right-edge — full-height vertical strip on the rightmost column.
- Palette size used: 9 distinct palette values appear in placed sprites across all 8 levels: {0, 5, 8, 9, 10, 11, 12, 14, 15} (renderer remaps several at draw time).
- Background colour value: 9.
- Padding / letter-box colour value: 5.
- Number of distinct mechanics introduced across levels 1-3: 3 — (L1) reflect-piece-onto-targets across a fixed vertical mirror; (L2) movable vertical mirror; (L3) horizontal-axis movable mirror plus a second piece.
- Number of levels documented: 3.

(End of file.)
