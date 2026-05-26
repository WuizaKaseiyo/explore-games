# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | Camera (32, 32) == grid (32, 32) on every level. |
| CHECK_SPRITE_CONTENT | 5 distinct | 6 distinct | 6 distinct | non-letter-box palette values per level (≥ 2 required). |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | Both `GameAction.ACTION5` and `GameAction.ACTION6` are referenced in source. |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | ACTION5 and ACTION6 both run without exception (tested with display click `(16, 16)` for ACTION6). |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | All within [0, 15]. |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` and `self.win()` (the latter via `next_level` on the last level) found. |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` is called when `self._step_remaining <= 0`. |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All 3 levels share `grid_size=(32, 32)`; per-level resize is not strictly required but `self.camera.width = gw` / `self.camera.height = gh` are present in `on_set_level` (defensive — keeps the per-level pattern even when grids agree). |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | All 3 spec witnesses replay against the loaded game. L1's 8 actions advance score 0→1; L2's 20 actions advance 1→2; L3's 16 actions reach state == WIN, score == 3. |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | See per-level inspection below. PNGs at `workspace/smoke-frames/level_{1,2,3}.png`. |

## CHECK_VISUAL_SANITY per-level inspection

**Level 1 (`smoke-frames/level_1.png`)** — PASS.
- Sprite count: 4 distinct blue node sprites at the 4 quadrants + 2 grey pip markers per node + green HUD strip at bottom. Matches spec's "4 nodes at corners, target degree 2 each".
- Sprite placement: corners (NW, NE, SE, SW) of the playfield. Spec calls for `n_nw (8, 8)`, `n_ne (24, 8)`, `n_se (24, 24)`, `n_sw (8, 24)`; rendered positions match.
- HUD presence: green bar visible at the bottom row.
- No catastrophic rendering bug; no glyph-shaped sprites; nodes have internal checker pattern (not uniform colour blobs); pips are 1×1 grey markers around each node.

**Level 2 (`smoke-frames/level_2.png`)** — PASS.
- Sprite count: 5 nodes (4 cardinal outer + 1 centre). Top (n1) and bottom (n3) are blue; left (n0), right (n2), and centre (n4) are red. Pip rings around each node show 3 pips for outers and 4 pips for centre.
- Sprite placement: cross-shape with centre. Matches spec's `n0 (5, 16)`, `n1 (16, 5)`, `n2 (27, 16)`, `n3 (16, 27)`, `n4 (16, 16)`.
- HUD presence: green bar bottom.
- No rendering bug; the colour mismatch (blue n1, n3 vs. red others) is the spec's intended starting state — the player must recolour them.

**Level 3 (`smoke-frames/level_3.png`)** — PASS.
- Sprite count: 4 nodes in a diamond. Top (n1) and bottom (n3) blue; left (n0) and right (n2) red. n0 and n2 each have 4 pips visible (target degree 4); n1 and n3 each have 2 pips (target degree 2).
- Sprite placement: diamond layout matching spec's `n0 (8, 16)`, `n1 (16, 8)`, `n2 (24, 16)`, `n3 (16, 24)`.
- HUD presence: green bar bottom.
- No rendering bug; the asymmetric pip counts (more pips on n0 / n2) telegraphs the higher target degree on those two nodes — visual cue for the multi-edge requirement.

All three levels render with internal sprite detail (checker-pattern node interiors, distinct grey pip markers, distinct HUD bar). No level renders a tiny patch in the corner / no level shows uniform colour blocks where game content should be.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_click_on_node_selects` | `selected=n_nw` | After clicking display (16, 16), `self._selected_node == "n_nw"` ✓ |
| `check_pair_click_creates_edge` | `edge_state[(n_ne, n_nw)] = 1` | Pair-click produces a single edge ✓ |
| `check_action5_cycles_color_at_l2` | `before=9 after=8` | ACTION5 cycles n1 from blue (9) to red (8) at L2 ✓ |
| `check_l3_double_edge_advances_cycle` | `after_first=1 after_second=2` | At L3, second pair-click advances single → double instead of removing ✓ |

Visit count: 1/6.
