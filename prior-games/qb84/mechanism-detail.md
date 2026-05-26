# qb84 — bead-lift-swap

## Summary

A serpentine chain of single-cell coloured bead sprites lies along
a fixed snaking path on a 64×64 playfield, with peg sprites placed
in flanking "above" and "below" slots beside specific beads. The
player drives a logical cursor across the chain via ACTION3/4 and
fires ACTION1 ("lift") or ACTION2 ("drop") to swap the cursor's
bead colour with the corresponding above/below peg sprite — the
swap is bidirectional, so the peg also takes the bead's old
colour. Each level wins when the chain's bead-colour sequence
matches a per-level target sequence rendered as a small
horizontal strip in the playfield's bottom-right corner. The only
failure mode is exhausting the per-level step counter; ACTION1/2
on a bead with no associated peg slot is a free no-op.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | "lift" — swap the cursor's bead colour with the above-slot peg's body colour. Sticky peg locks the bead's colour after the swap. Pair peg additionally propagates the OTHER pair peg's colour into the cursor's chain neighbour (cursor+1, fallback cursor-1) at action start; propagation silently no-ops on a locked neighbour. | Always offered. Step consumed only if the swap was effective (peg present at slot AND bead not locked). |
| ACTION2 | "drop" — same as ACTION1 but uses the below-slot peg. | Same. |
| ACTION3 | Cursor index decrement, clamped to 0. | Always offered. Step consumed always. |
| ACTION4 | Cursor index increment, clamped to len(chain)-1. | Always offered. Step consumed always. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | lift-swap + drop-swap (base dynamic, N=2) | 6-bead S-curve, 3 plain pegs (2 above, 1 below). Witness exercises both lift (B0, B2) and drop (B5). Step budget 24; witness solution 8 actions. Random-resistant via 4²⁴ search space; mechanic-discovery is the difficulty. |
| 2 | + sticky-peg lock (N+1=3) | 8-bead extended S-curve, 5 pegs of which 2 are sticky. Witness must commit B2 and B5 to sticky pegs of correct colour — once a bead touches a sticky peg, its colour is permanently locked and cannot recover. Step budget 32; witness 12 actions. Spam-the-new-verb is defeated because every successful swap also changes the peg's colour to the bead's old colour — visiting a peg twice produces different effects. |
| 3 | + pair-peg propagation (N+2=4) | 10-bead double-S, 7 pegs including a pair-A/pair-B propagation pair, two sticky pegs, two plain pegs, and one sticky-trap below B6. The pair-propagation rule is the only way to set B6's target colour 15 — there is no plain peg of colour 15 reachable from B6. Adjacent commute failure: actions 8 (lift on B5 onto pair-A) and 9 (cursor 5→6) cannot be swapped — swapping fires the propagation at cursor=6, pushing the wrong colour into B7 and breaking B7's already-correct target. Step budget 60; witness 14 actions. Trivial heuristic "for each wrong-coloured bead, find a peg of target colour next to it" defeated because B6's target requires indirect propagation. |

## Win condition

After every action, walk the chain in cursor-index order. For each
bead at index `i`, compare its centre-pixel colour
(`bead.pixels[1, 1]`) to `level.get_data("TargetSequence")[i]`. If
every bead matches its target slot, fire `self.next_level()`. The
engine's `next_level()` automatically calls `self.win()` after the
final level (L3) completes.

## Lose condition

Single failure mode: `self._steps_used >= self._max_steps` AND the
win predicate is False. The lose check fires AFTER the win check
on each action so a final-action-completes-the-puzzle case wins.
No chasers, no hazards, no instant-fail collision.

## Internal state

- `self._chain: list[Sprite]` — bead sprites in chain index order (0 → cursor walks forward; len-1 → cursor walks backward).
- `self._cursor_index: int` — current logical cursor index. Reset to 0 on `on_set_level`.
- `self._pegs_above: dict[int, Sprite]` — chain-index → above-slot peg sprite (absent if no peg at that slot).
- `self._pegs_below: dict[int, Sprite]` — chain-index → below-slot peg sprite.
- `self._pair_partner: dict[Sprite, Sprite]` — for each pair-peg, its paired partner. Looked up by position in `level_data.PairPartners`.
- `self._bead_locked: dict[Sprite, bool]` — per-bead lock flag. Flipped True after any swap involving a sticky peg; never reset within a level.
- `self._target_seq: list[int]` — list of target colours per chain index, from `level_data.TargetSequence`.
- `self._max_steps: int` / `self._steps_used: int` — per-level step budget and tally; private counter advances only on effective actions (matches qz73 and kx14 priors).
- `self._step_bar: StepBarHud` — depleting-bar HUD widget rendered at row 0 of the frame.
- `self._cursor_hud: CursorHud` — 4-corner-pixel cursor indicator HUD rendered around the active bead.
- Hidden state shape: `(3, len(chain))` `np.int16` — row 0 = bead colours, row 1 = lock flags (0/1), row 2 = `[cursor_index, steps_used, max_steps, ...0...]`.

## Notable code patterns

- **Misclick-free model.** ACTION1/ACTION2 with no peg at the slot, or on a locked bead, return False from `_try_swap` and do not advance `self._steps_used`. Mirrors qz73's "ACTION6 misclick is free" convention. ACTION3/ACTION4 always consume a step (cursor walks are part of any plan).
- **Pair-peg propagation reads partner colour at action start.** `_try_swap` snapshots `partner_c_at_start = self._peg_color(partner)` BEFORE mutating the active peg, so the propagation onto the chain neighbour uses the partner's pre-action colour even though the swap has logically committed. Avoids self-interference between the two halves of the action.
- **Color reading from a guaranteed body cell.** Sticky pegs have palette-4 at the centre pixel `[1, 1]`; reading body colour from `pixels[1, 1]` would mistakenly return the marker colour for sticky pegs. The implementation reads `pixels[1, 0]` (left-centre), which is the body colour for ALL peg variants (plain, sticky, pair-A, pair-B). Reusable rule of thumb: never read from a marker-pixel position when extracting body colour from a sprite that has marker pixels.
- **One canonical sprite per role + per-instance `color_remap`.** The sprite bank declares one canonical bead and one canonical peg-per-kind, all with body colour 8 (red); each level clones the canonical sprite and applies `color_remap(8, target_color)` to set the per-instance hue. Mirrors qz73's "rkqbnzwlth tip definition cloned and recoloured" pattern.
- **Tag-based `on_set_level` introspection.** Beads, pegs, path markers, and target-ref strips are looked up via `level.get_sprites_by_tag` plus per-position lookup via `level.get_sprite_at(x, y, tag)`. The `_find_sprite_near` helper does a small-radius fallback search to tolerate ±3-pixel position noise (useful when peg positions are specified at the top-left of a 3×3 sprite).
- **Two-HUD camera registration.** The camera is constructed with `interfaces=[self._step_bar, self._cursor_hud]` so both HUDs render on top of the playfield each frame. The cursor HUD reads `self._chain` and `self._cursor_index` reactively each render — no manual update calls needed.
