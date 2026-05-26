# Game generation final report

## Generated game

- **ID**: ej4t
- **Source**: `prior-games/ej4t/ej4t.py`
- **Metadata**: `prior-games/ej4t/metadata.json`
- **Lines of code**: 512

## Mechanic

The player avatar is surrounded by a visible translucent Manhattan-distance ring of radius R, painted as a halo over every cell within R cells of the player. The player walks four cardinal directions; walking into a crate triggers a push, and chain pushes only commit when every crate in the chain (after the first) sits within R of the player's current cell. The level wins when every target sprite is covered by a crate. Two collectibles modify R as the player walks over them: extender pickups grow R by +1 (one-shot, sprite consumed) and shrinker traps reduce R by 1 (one-shot, the trap stays visible as a grey "spent" cell). Across the three levels, the player learns chain-push gating (L1), extender management (L2), and trap-aware planning (L3 forces collecting both extenders to compensate for an unavoidable shrinker on the only path).

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | walk player up; attempt push if destination has a crate |
| ACTION2 | walk player down; attempt push if destination has a crate |
| ACTION3 | walk player left; attempt push if destination has a crate |
| ACTION4 | walk player right; attempt push if destination has a crate |

`available_actions = [1, 2, 3, 4]` (cardinals only; ACTION5/6/7 not used).

## Levels

- **L1** (12×12, R=2): introduces M1 (radius-gated chain push). Single corridor, 2 crates in a row, single chain-push delivers both onto the target. Witness 5 actions.
- **L2** (14×14, R=1 init): introduces M2 (extender pickup grows R). Same corridor pattern; player must walk over the extender pickup at (5, 7) to grow R from 1 to 2 before the chain push works. Witness 5 actions.
- **L3** (16×16, R=2 init): introduces M3 (shrinker trap reduces R). Three crates require chain push with R=3; corridor forces player through ext_a (R 2→3), shrinker (R 3→2), ext_b (R 2→3), then chain push. Witness 7 actions.

## Novelty note

- Closest taxonomy entry: **lq5x** (lantern-cone-illuminate). Distinguishing rule: lq5x uses a directional cone projected from a stationary lantern, with the player rotating the lantern via ACTION5; this game uses an omnidirectional Manhattan ring centred on the player itself, moving with the player every step, with no rotation primitive — the core verb is "position the ring" not "rotate the cone".
- Closest prior-game entry: **kn58** (anchor-pull-magnet). Distinguishing rule: kn58 places a single magnetic anchor via click and globally pulls every coloured pawn one cell toward it; this game has no click action and no autonomous pull — the ring gates push permission only, and crates only move when the player walks INTO them with chain conditions met.

## Index update

Appended one row to `prior-games/index.md`:

```
| ej4t | radius-scope-influence | Radius-Scope Chain-Push — visible Manhattan ring around player gates chain pushes; pickups grow R, traps shrink R; chain-push crates onto matching targets across 3 levels. | 2026-05-08T14:00:44Z | (autonomous) |
```

## Run notes

- **NEW: study state input 5 (PuzzleScript demo web research)** completed successfully. Listed both `increpare/PuzzleScript` and `Auroriax/PuzzleScriptPlus` `src/demo/` directories via `gh api` (96 files each). Fetched 7 demos via WebFetch (collapse, dropswap, diesinthelight, ponies-jumping-synchronously, zenpuzzlegarden, plus_nonogram, plus_localradius), all successful.
- The selected mechanic was directly inspired by `plus_localradius.txt` from PuzzleScriptPlus — that demo's "crates push only within radius" core was composed into a 3-level NovaPlay progression by adding the extender (M2) and shrinker (M3) mechanics.
- All 10 universal smoke checks passed (CHECK_VISUAL_SANITY skipped — vision pass is manual). The new upstream CHECK_WITNESS_WINS validated the spec's witnesses against the implementation: L1 (5 actions) → L2 (5 actions) → L3 (7 actions, reached WIN state) deterministic.
- 3 custom checks passed (wall blocking, extender grows R, shrinker reduces R).
- No `fix_implementation` revisits required.
- Total run time: ~80 minutes (study heavy due to step 5 first-time exercise).
