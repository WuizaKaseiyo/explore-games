# Critique revisions — visit 1

I walked all 18 checklist items + the difficulty-rules § 3 critique + similarity / negative-similarity checks against the now-concrete spec. Most items pass. Three substantive issues need to be fixed in `write_spec`.

## Issues to address

### Issue 1 — L2 win predicate inconsistency (checklist item 16, item 12)

**Violation**: §7 states "every `target_socket` in the current level is filled" is the win condition. But §4's L2 layout places **two** target sockets: `target_socket_blue` at `(28, 6)` and a `target_socket_yellow` at `(28, 54)` "as a decoy / forces the player to learn what colour-match means". L2 has only blue balls in either branch — the yellow socket can NEVER be filled, so under the spec's own win predicate, **L2 is unwinnable**.

**Offending quote (§4 L2 Layout)**:
> `target_socket_yellow` at `(28, 54)` — placed exactly one ball-width past the chain's right terminus … (Wrong colour — won't fill from blue-ball ejects. Acts as a decoy / forces the player to learn what colour-match means.)

**Suggested fix**: Drop the yellow decoy from L2. Replace with an empty cell (just playfield background) at `(28, 54)`. The "wrong-colour" lesson can be deferred to L3 if needed, or omitted entirely (the level still teaches junction-routing because the *only* socket is at the up-branch end). Update §4 L2 Layout, and confirm §7 win predicate still works (it now does — the only target_socket in L2 is the blue one). Also remove the corresponding line in the L2 counterfactual that talks about "wrong-coloured target socket".

### Issue 2 — `pusher_knob` "handle" reads as directional arrow (checklist item 7 / forbidden-elements)

**Violation**: §3 describes the pusher_knob with "a small handle protruding *toward* the chain end it shoves" and "The handle direction encodes which way the pulse travels." A 6×6 sprite that protrudes toward one side encodes direction visually — that is the cultural-convention pattern that `forbidden-elements.md` explicitly bans ("Cultural conventions … an arrow shape implying direction").

**Offending quotes (§3)**:
> A purple-rimmed (15) hexagonal knob with off-black (4) inset, with a small handle protruding *toward* the chain end it shoves.
> The handle direction encodes which way the pulse travels.

**Suggested fix**: Re-design `pusher_knob` as a symmetric button-shape with NO directional protrusion. Concretely, a 6×6 sprite with a hollow purple frame and an inset off-black core — looks like a "press button" without any handle:

```
[-1, 4, 4, 4, 4, -1]
[4, 15, 15, 15, 15, 4]
[4, 15, 4, 4, 15, 4]
[4, 15, 4, 4, 15, 4]
[4, 15, 15, 15, 15, 4]
[-1, 4, 4, 4, 4, -1]
```

This is symmetric (rotation- and reflection-invariant), so it does not embed direction. The pulse-direction is encoded by the pusher's *placement* — adjacent to one end of the chain — and by the chain's geometry. The placement adjacency is itself the directional cue (pure objectness); no glyph required.

Update §3 (pusher_knob row), §4 layouts (pusher knob references), and add a sentence to §6 noting that the chain's pulse direction is determined by the chain-axis-toward-the-pusher-adjacent ball.

### Issue 3 — L3 chain A down-branch positions extend off-grid (structural / spec correctness)

**Violation**: §4 L3 Layout (revised section) places chain A's down-branch at `(20, 56)` and `(20, 62)`. With 6×6 sprites, the ball at `(20, 62)` spans rows 62-67, but the playfield grid is `[0, 64)` — y=64..67 is off-grid. The level configuration would either crash on placement or render with the second down-branch ball clipped at the boundary.

**Offending quote (§4 L3 Layout)**:
> Down-branch (vertical, off-axis dead-end): `chain_ball_blue` ×2 at `(20, 56)`, `(20, 62)`. Eject lands at `(20, 68)` = off-grid → consumed.

**Suggested fix**: Shift the down-branch into bounds. Two options:
- Option A — shrink the down-branch to 1 ball at `(20, 56)`; the dead-end is now reached at the eject destination `(20, 62)` which is on-grid but contains nothing (empty cell at the playfield edge); the ejected ball lands there and is consumed *by an explicit "wall" sprite* placed at `(20, 62)` to give a clear "thump" visual.
- Option B (preferred) — explicitly add a `dead_end_wall` sprite at the eject destination of every dead-end branch. This is a 6×6 black (5) wall sprite, tagged `["wall"]`, placed at the cell where dead-end branch ejects land. Eject hits the wall sprite → ball is consumed; visual "blocked by wall" is clear.

Apply the same fix to L3 chain B's down-branch (`(38, 32), (38, 38)` → eject lands at `(38, 44)`, currently described as "empty cell"; place a `dead_end_wall` there for visual clarity).

Update §3 to add `dead_end_wall` sprite (6×6, black). Update L3 layout in §4. While there, also adjust positions so all sprites fit cleanly within `[0, 64)` on both axes — for instance, shift chain A's stem and junction up by 6 to (20, 44 → 38) so down-branch + walls fit.

## Items NOT flagged (pass on this visit)

For completeness — the rest of the checklist passes:

- **Item 1** (palette 0..15): all sprite definitions use only valid palette + `-1`. ✓
- **Item 2** (file structure scaffold): described, will be checked at `implement`. ✓
- **Item 3** (`available_actions` ⊆ [1..7]): `[6]`. ✓
- **Item 4** (exactly 3 levels with composition): yes. ✓
- **Item 5** (4-char ID, no collision): `qn7w`. ✓
- **Item 6** (mechanics from core priors only): yes (objectness, physics, geometry/topology). ✓
- **Item 8** (≥ 2 distinct mechanics): 3 (pulse-eject, junction-routing, merge-on-coincidence). ✓
- **Item 9** (L1 tutorial, base dynamic system, no on-screen text): ✓
- **Item 10** (L2 / L3 increase difficulty by composition, not size scaling): yes — L3 reuses L2's mechanics and adds merge. ✓
- **Item 11** (mechanic inheritance + 1-or-+2): L1=1, L2=2, L3=3. Each level inherits all earlier-level mechanics; +1 each step. ✓
- **Item 12** (strict counterfactual necessity): per-mechanic counterfactual lines stated for each (mechanic, level) pair; concrete cells/branches/rules cited. After fixing Issue 1 (yellow decoy), the L2 row remains valid (junction-routing still required because the only socket is on the up-branch and the default-active is the down-branch dead-end). ✓ (after Issue 1 fix)
- **Item 13** (mechanic absent from taxonomy): pulse-chain-eject — verified. ✓
- **Item 14** (mechanic absent from priors): verified. ✓
- **Item 15** (distinguishing rules for near-misses): §9 covers ka59, r11l, vc33, lp85, vn8d, kp9z, bx84, kn58, gx7m, xn5p, rk7x with concrete rules. ✓
- **Item 16** (win condition stated): yes — but adjust per Issue 1. ✓ (after fix)
- **Item 17** (lose condition stated): yes — budget exhaustion + soft-lock detection. ✓
- **Item 18** (difficulty floor / ceiling per level): for each level (a)/(b)/(c)/(d) all stated; L2/L3 planning-depth is concrete with named heuristics + decision-space counts + reasoning chains; L3's planning ≥ L2's. ✓
- **Item 19** (no hidden state): every state mutation has a persistent visual cue (junction tab, ball count, socket fill, merge_pad fill). ✓
- **Item 20** (no low-resolution): native 64×64; 6×6 sprites with internal pixel detail. ✓
- **Item 21** (UI teaches): Sprite-role mapping is explicit (button = press, ring = receive, tab = switch, pip = double-receiver). After Issue 2 fix, no glyph implies direction. ✓ (after fix)
- **Similarity check**: pass against all 25 + 33 entries (rules concrete). ✓
- **Negative similarity check**: closest prior is vn8d; shared on dimensions 2, 4 strongly + 3, 5 weakly; diverges on heavy axes 6, 7, 8. <3 strong shared. Pass. ✓

## Verdict

Three concrete fixable issues. Transition back to `write_spec` with this revisions list. Visit count is 1; budget is 10. Plenty of room.
