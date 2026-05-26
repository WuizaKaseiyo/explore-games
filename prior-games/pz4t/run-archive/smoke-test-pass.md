# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | (10,10) / (12,12) / (14,14) — all match |
| CHECK_SPRITE_CONTENT | 5 | 6 | 7 | distinct non-letterbox palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 3 declared (5,6,7) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 0..11 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level resize present |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | components in palette below, target shadows above; HUD bottom |

### Visual sanity per-level

- **L1**: 2 components (red 3-bar, yellow 2-vbar) clearly visible at bottom-left/bottom-mid; matching dark-grey shadow shapes on the upper board (3-bar horizontal at top-left, 2-vbar vertical at top-right). HUD full white at bottom.
- **L2**: 3 components in palette (red vbar1×3, yellow L, green hbar) and 3 dark-grey shadow shapes (horizontal red bar, L, hbar). Red component is vertical but red shadow is horizontal — flagging the rotation requirement.
- **L3**: 4 components (red Z, yellow S, green T, magenta bar) in palette; 4 corresponding shadows on board including the chiral S-shaped red shadow (Z must flip) and T-rotated-CW green shadow.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_picks_up_component | held=comp_red_bar3 | ACTION6 click sets self.held_component |
| check_anchor_offset_recorded | anchor_offset=(1, 0) | clicking the middle cell records anchor relative to bbox |
| check_place_uses_anchor | comp.pos=(4,2) | place at click − anchor coordinates |
| check_rotate_transforms_anchor | anchor=(2, 0) width=3 | 90° CW rotates a 1×3 to 3×1 and updates anchor |
| check_flip_makes_z_into_s | rendered=[[-1, 8, 8], [8, 8, -1]] | flipping Z produces S |

Visit count: 1/3.
