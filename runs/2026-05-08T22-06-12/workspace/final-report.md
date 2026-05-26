# Game generation final report — Run #4

## Generated game

- **ID**: cy3k
- **Class**: `Cy3k` (Pascal-case verified)
- **Source**: `prior-games/cy3k/cy3k.py`
- **Metadata**: `prior-games/cy3k/metadata.json`
- **Lines of code**: ~310

## Mechanic

A 4-colour grid where the player walks a cursor and ACTION5 cycles the cursor's cell colour forward through the alphabet, propagating to every cell in the cursor's 4-connected same-colour cluster. Win = match target pattern. L1 base cluster-cycle. L2 adds fixed cells (don't cycle even within a cycling cluster). L3 adds transparent cells (preserve 4-connectivity bridges but don't cycle themselves).

## Skeleton-diversity verdict

| label | value |
|---|---|
| `primary_skeleton` | symbolic-rewrite |
| `secondary_skeleton` | classification-sorting |
| `interaction_type` | arrows |
| `state_model` | symbolic-state |
| `objective_shape` | match-pattern |

**Gate result**: PASS. Recent-5 skeletons (tw94, vy3m, ej4t, tg6w, pf3w) are all distinct from `symbolic-rewrite`. Full-corpus high-frequency skeleton is `global-field-update` (6/29) — not selected. Only 1 other prior uses `symbolic-rewrite` (pj7k rolling-cube-face-paint), making this a structurally novel direction for the corpus.

This is the **first run** to generate a game under the new `mechanic-novelty/skeleton-diversity-check.md` gate, which forced this skeleton diversification away from walk-and-push variants.

## Smoke test results

```
13 PASS, 0 FAIL, 1 SKIPPED

✅ CHECK_CAMERA_VIEWPORT
✅ CHECK_SPRITE_CONTENT
✅ CHECK_ACTION_BRANCHES
✅ CHECK_ACTION_RUNTIME
✅ CHECK_PALETTE_RANGE
✅ CHECK_WIN_PATH_EXISTS
✅ CHECK_WITNESS_WINS
✅ CHECK_TRIVIAL_FAILS
✅ CHECK_LOSE_PATH_EXISTS
✅ CHECK_CAMERA_DEFAULT
✅ CHECK_CLASS_NAME_LOADER
✅ custom_action5_cycles_cluster
✅ custom_l2_fixed_cell_doesnt_cycle
⏭️ CHECK_VISUAL_SANITY (manual)
```

## Notable run details

- **First non-walk-push game** in corpus: cy3k breaks the streak of 4 consecutive sokoban-variants (tg6w, ej4t, vy3m, tw94) by being a `symbolic-rewrite` game with no avatar pushing.
- **Witness-order subtlety in L3**: at L3, cycling clusters in arbitrary order can cause unintended fusion via transparent bridges — specifically, cycling C before B causes both to be purple at the same time, fused via transparent (3,3), and the next ACTION5 on either double-cycles both. The witness must use order A→B→C→D to avoid this. This kind of "order-dependent setup" is exactly the kind of post-discovery planning depth the trivial-fails gate verifies.
- **Trivial heuristic verified to fail**: `[ACTION4 × 14]` for L2 and `[ACTION4 × 20]` for L3 — neither calls ACTION5, so no cells cycle, no win possible.
- **Total run time**: ~50 minutes.

## Index update

```
| cy3k | cluster-cycle-rewrite | symbolic-rewrite | classification-sorting | arrows | symbolic-state | match-pattern | Cluster Cycle Pattern ... | <ts> | (autonomous) |
```
