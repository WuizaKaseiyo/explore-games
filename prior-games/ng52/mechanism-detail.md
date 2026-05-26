# ng52 — multiset-signature-classify

## Summary

Multiset Signature Classifier is a turn-based partition puzzle on
a 64×64 grid with no avatar and no spatial gameplay. Three
classification bins sit in a row above an object pool; each bin
shows its **signature** as a vertical stack of 1×L solid-colour
"sticks" that abstractly defines the target multiset of pixel-
colours the bin will accept. The player clicks pool objects to
select them, clicks bins to drop the selection, and presses
ACTION5 to commit; on match, the level advances; on mismatch,
every placed object snaps back to the pool. Difficulty grows
from single-colour single-stick bins (L1) to multi-stick
compositional bins requiring multiple objects per bin (L2) to a
configuration with a distractor object that must remain in the
pool (L3).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Commit. For every bin, aggregate the pixel-colour multiset of its placed objects and compare to its declared signature multiset. All bins match ⇒ `next_level()`. Any bin mismatches ⇒ every placed object across all bins snaps back to its original pool position; selection clears. | Always valid. |
| ACTION6 | Click at `(x, y)`. Pixel coords are converted via `camera.display_to_grid`. Hit-test priority: (1) pool object → select it (or switch selection); (2) bin-resident object → pick it up to the selection (it leaves the bin and hovers above the bin row at `HAND_Y`); (3) bin holding-area cell → place the current selection in that bin's next free 4×4 slot; (4) anywhere else → no-op. | Always valid. |

`available_actions = [5, 6]`.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | place-and-commit-classify | 3 single-stick single-colour bins (`{blue:3}`, `{blue:4}`, `{blue:5}`) and 3 single-colour blue objects (3-blue L, 4-blue T, 5-blue plus). The unique trivial assignment matches each object to the bin whose signature equals its pixel count. Witness `[ACTION6@O1, ACTION6@bin0, ACTION6@O2, ACTION6@bin1, ACTION6@O3, ACTION6@bin2, ACTION5]` (7 actions). Step budget 40. |
| 2 | + multi-stick compositional bin | Bins gain multi-stick multi-colour signatures (`{blue:6}`, `{blue:3, purple:3}`, `{blue:4, purple:2}`); 6 objects (three 3-blue, one 4-blue, one 3-purple, one 2-purple), none of which alone matches any bin. Each bin's signature is reachable only by combining 2 objects whose pixel-colour multisets sum to the signature. Witness 13 actions: `[click_O1, click_bin0, click_O2, click_bin0, click_O3, click_bin1, click_O5, click_bin1, click_O4, click_bin2, click_O6, click_bin2, ACTION5]`. Step budget 60. |
| 3 | + selective placement under distractors | Same bins as L2 with a 5-blue plus-shape **distractor** added to the pool. Pool pixel total exceeds bin capacity by exactly the distractor's 5 blues; the only feasible partition leaves the distractor in the pool throughout. Witness same 13 actions as L2 (placing the L2 objects into the L2 partition; the distractor is never clicked). Step budget 60. |

## Win condition

`self.next_level()` (and `self.win()` on L3) fires on ACTION5
when, for every bin, the bin's multiset of pixel-colour counts
(summed across all currently-placed objects) equals the bin's
declared signature multiset. Pseudocode:

```
def _check_win() -> bool:
    for bin_h in self.bins:
        observed = aggregate_multiset(bin_h.placed_objects)
        if observed != bin_h.signature_multiset:
            return False
    return True
```

## Lose condition

`self.lose()` fires when `self.steps_used >= self.max_steps` and
the win predicate has not been satisfied. Failed commits cause
`_snap_back_to_pool()` (returning every placed object to its
original pool position) but do not end the level — they simply
cost the step that fired ACTION5.

## Internal state

- `self.objects: list[ObjectHandle]` — each tracks its sprite, the
  per-colour pixel-count multiset, the original pool position, the
  current container (`"pool"` | `"bin_<i>"` | `"hand"`).
- `self.bins: list[BinHandle]` — each tracks its signature
  multiset, holding-area rectangle, and ordered list of placed
  `ObjectHandle`s.
- `self.selection: ObjectHandle | None` — the currently selected
  object (or None).
- `self.selection_ring: Sprite` — runtime-resized 1-pixel ring
  toggled around the selected object via `InteractionMode`.
- `self.steps_used`, `self.max_steps`.

## Notable code patterns

- **Per-cell multiset aggregation**. Each object's pixel-colour
  multiset is precomputed once in `on_set_level` from its
  `pixels` array (skipping `-1` transparent cells) and stored on
  the `ObjectHandle`. Per-bin aggregation in `_check_win` is a
  cheap dict-merge across all placed objects, avoiding any
  per-step pixel rescan.
- **Snap-back as a uniform reset primitive**. `_snap_back_to_pool`
  walks every object, removes it from any bin's `placed` list,
  resets its sprite position to `pool_position`, and clears the
  selection. This is used both as the failed-commit response and
  is reusable for any future "reset" affordance.
- **Bin slot packing with shift-on-removal**. `BinHandle.placed`
  is an ordered list; `next_slot_position` uses `len(placed)` to
  pick the next 4×4 slot in row-major order. On removal,
  `_remove_from_container` re-packs remaining placed objects so
  there are no visual holes.
- **Runtime-sized selection ring**. The selection ring is a
  single sprite whose `pixels` array is rewritten each step to a
  hollow rectangle of the current object's bbox + 1; toggled
  visible/REMOVED via `set_interaction`.
- **Static signature topology rendered as 1×L stripes**. Each
  signature stick is a 1-row sprite of length L painted with the
  stick's colour; multiple sticks stack vertically with a 1-pixel
  gap. The visible diagram IS the rule.
