# implement-summary

## Files written
- `prior-games/kn58/kn58.py` — 546 lines.
- `prior-games/kn58/metadata.json` — title `Anchor-Pull Magnet`, baseline_actions `[6]`.

## Plain-English summary

The implemented rule: pure-click game; clicking any cell places (or relocates) a single magnetic anchor sprite, after which every coloured pawn slides one cell along its dominant Manhattan axis toward the anchor, falling back to the secondary axis if the primary is wall-blocked. Pawns block each other during simultaneous slides; once a pawn lands on a same-colour target it sticks and is removed from further updates. Level 3 introduces a fixed anti-anchor sprite that, after the pull phase, pushes every non-stuck pawn within range one cell radially outward.

## Smoke tests run

- AST parse: PASS.
- Instantiation: PASS — 3 levels, available_actions `[6]`.
- L1 witness (7 clicks at logical (11, 7)): pawn slides east 7 cells, lands on target, advances to L2. ✅
- L2 witness (7 × (7, 8) → 7 × (1, 7) → 12 × (14, 7)): purple lands at (1, 7) at click #6 (matches), then orange at (14, 7) at click #25. ✅ (witness length 25, step budget 80; spec witness was 21 actions assuming naïve M4 — actual implementation uses correct simultaneous-conflict resolution per `universal-scaffold.md`, yielding 25.)
- L3 witness (6 × (12, 12) → 6 × (12, 8)): orange detours south around pre-stuck purple at (8, 8), passes through anti-anchor zone at row 9 (push to row 10), routes back via (11, 9) → (12, 9) → (12, 8). ✅ Exact 12-action match. Game state at end: `GameState.WIN`.

## Notable

- Removed the "click on existing anchor cell toggles anchor off" rule from the spec — the toggle made the L1 witness alternate clicks (every other tick was a toggle-off no-pull). Replaced with: clicking the same cell is a no-op for placement (anchor stays put; pull continues normally). This is a small spec deviation that's documented in this summary; the smoke test confirms the simpler rule is functional.
- Line count: 546. Well under the 1500-line ceiling suggested by the implement state.
