# mechanic-spec.md — `jx5k` (revised after critique-revisions.md visit #1)

## Sections changed in this revision (after critique visit #1)
- §3 sprite roster: collapsed pip variants to 2 (per visit-1 Issue 6); added multiplicity to edge-sprite pool (visit-1 Issue 7).
- §4 Level 3: REWRITTEN. Replaced M3 (walls) with **M3 = multi-edge / 3-state cycle** per visit-1 Issue 1; consolidated to one concrete layout per visit-1 Issue 2; added a concrete post-discovery heuristic-fail argument per visit-1 Issue 3.
- §5 action mapping: explicit per-level valid-action-set (visit-1 Issue 4 clarification).
- §9 novelty note: added one extra prior near-miss check against `qb84 bead-lift-swap` (which uses pair-clicks too) for completeness.

## Sections changed in this revision (after critique visit #2)
- §4 Level 2: target degrees corrected from `[2, 2, 2, 2, 4]` to `[3, 3, 3, 3, 4]` (per visit-2 Issue 1) so the 8-edge witness actually wins.
- §5 ACTION5 row: appended explicit "deselect after cycle" semantics (per visit-2 Issue 2).
- §6 `self._selected_node` mutation rule: explicit list of when it sets / clears.

## 1. Title
Constellation Edge-Link — connect coloured nodes into a graph (with parallel edges at L3) that satisfies every node's required-degree pip ring.

## 2. Mechanic family
`constellation-edge-link` — drawing only from §3.4 priors *Basic geometry & topology* (graph degree sequences, multigraph structure) and *Objectness* (nodes are persistent positioned entities; edges are persistent created sprites). No physics, no agentness.

The player constructs a multigraph by **pair-clicking** nodes: ACTION6 selects a node (a halo cue lights it); a second ACTION6 on a *different* node cycles the edge between them through the per-level edge-state cycle. Each node has a target *degree* — a small ring of pip-marks around its perimeter that progressively fills as edges attach. Win = every node's filled-pip count equals its target-pip count. L2 introduces a **node-colour-cycle** active verb (ACTION5 with a node selected cycles its colour) and the constraint that edges only connect same-colour nodes; the witness must recolour at least one node before the required edge becomes legal. L3 introduces **multi-edge support**: the per-pair edge-state cycle expands from `[no edge → single edge → no edge]` (L1/L2) to `[no edge → single edge → double edge → no edge]` (L3), and target degrees are tuned so a parallel edge is required.

## 3. Sprite roster

| Name | Pixel matrix | Palette values | Tags | Role |
|---|---|---|---|---|
| `node_blue` | 5×5 | 4, 9 | `node`, `colour_blue` | Node sprite, blue variant. Inner cross-pattern: 4-pixel border (palette 4), 1-pixel core cross (palette 4), remainder palette 9. Cloned per-node-position-per-level. |
| `node_red` | 5×5 | 4, 8 | `node`, `colour_red` | Node sprite, red variant. Same shape pattern, palette 9 → palette 8. |
| `node_yellow` | 5×5 | 4, 11 | `node`, `colour_yellow` | (Reserved; not used in the L1–L3 design but pre-built so future runs that fork this game can extend the palette.) Cloned per-position. Currently unused. |
| `node_halo` | 7×7 | -1, 12 | `halo` | Selection halo. 7×7 ring (border palette 12 orange, inner palette -1 transparent). One instance per level, INITIALLY `InteractionMode.REMOVED`; repositioned and TANGIBLE-flipped while a node is selected. |
| `pip_empty` | 1×1 | 3 | `pip_empty` | Empty pip-slot marker (palette 3 grey). Pre-placed around each node according to that node's required degree (one slot per required degree). |
| `pip_filled` | 1×1 | 12 | `pip_filled` | Filled pip-slot marker (palette 12 orange). Two-sprite-swap with `pip_empty`: each pip-slot has one `pip_empty` and one `pip_filled` pre-placed at the same cell; engagement of one edge incident on the parent node flips the next-empty slot from REMOVED-filled / TANGIBLE-empty to TANGIBLE-filled / REMOVED-empty. |
| `edge_strand_<pair>_<k>` | dynamic | 4, 15 | `edge`, `pair_<i>_<j>` | Pre-built edge-strand sprite for each pair `(i, j)` with `i < j` and each multiplicity index `k ∈ {0, 1}`. Sprite pixel matrix is the rasterised (Bresenham) line between nodes `i` and `j` centres, with the `k=1` variant offset by 1 pixel perpendicular to the edge axis so a double-edge renders as two visibly parallel strands. INITIALLY `InteractionMode.REMOVED`; toggled to TANGIBLE as edges attach. For 4-node L3 (the worst case in this game), pool size = `C(4, 2) × 2 = 12` strand sprites. |
| `wall_brick` | unused | — | — | Removed from spec (was L3 mechanic in v1; M3 replaced by multi-edge per critique). |

(`StepCounterHud(RenderableUserDisplay)` is a HUD widget, not a sprite; see §6.)

Total palette in active use: **{1 background, 3 pip-empty, 4 outline, 8 red, 9 blue, 12 halo + pip-filled, 14 step-bar fill, 15 edge-accent}** — 8 distinct values, distinct from any recent prior. Palette 11 (yellow) reserved but unused; palette 13 (maroon) reserved but unused (was L3 wall in v1).

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system

**Layout**:
- Grid: 32×32. Camera `width=height=32`.
- 4 nodes: `n_nw` at (8, 8), `n_ne` at (24, 8), `n_se` at (24, 24), `n_sw` at (8, 24). All `node_blue`.
- Target degrees: 2 each. Pip-slots: 2 `pip_empty` per node, positioned at grid offsets (0, -3) and (0, +3) relative to each node centre.
- Edge sprite pool: `C(4, 2) × 1 = 6` strands (multiplicity = 1 at L1).
- Step budget (`level.set_data("step_budget", 30)`): 30.

**Mechanics required by the witness** (N = 1):
- **M1 (edge-link)** — pair-click toggles an edge between the two clicked nodes. Edge-state cycle at L1 is `[no edge → single edge → no edge]` (i.e. `max_edge_multiplicity = 1`). Each active edge incident on a node fills one pip; win when every node's filled-pip count equals its target.

**Necessity per mechanic** (counterfactual):
- *L1 cannot be solved without triggering M1 because* the win predicate "every node's filled-pip count == target" evaluates `0 == 2` at level start (no edges, every node's filled-count is 0); only edge creation increments filled counts, and edge creation IS M1. Any winning sequence must call M1 at least 4 times (one per edge).

**Witness solution** (8 actions):
```
ACTION6@(8, 8)        # select n_nw (halo lights)
ACTION6@(24, 8)       # toggle edge n_nw–n_ne: no-edge → single
ACTION6@(24, 8)       # select n_ne
ACTION6@(24, 24)      # toggle edge n_ne–n_se: no-edge → single
ACTION6@(24, 24)      # select n_se
ACTION6@(8, 24)       # toggle edge n_se–n_sw: no-edge → single
ACTION6@(8, 24)       # select n_sw
ACTION6@(8, 8)        # toggle edge n_sw–n_nw: no-edge → single — WIN
```
After the 8th action every node has degree 2 (4-cycle); `_check_win` fires `self.next_level()`.

**Difficulty justification**:
- (a) **Random-resistance.** Random ACTION6 lands on a node with probability ≈ (4 nodes × 25 cells) / (32² display pixels with letter-box) ≪ 10%. The probability of stumbling into a covering 4-cycle within 30 actions is bounded by `(0.1)^8 × ordering odds ≪ 10⁻⁸`, well under the 10⁻⁴ threshold.
- (b) **Human-tractable.** ~ 1 minute. The pip-rings make the goal legible at a glance (each node "wants" 2 pips). After one exploratory click pair, the player sees an edge appear and a pip fill — the rule is learned. Building the 4-cycle is the obvious next move.
- (c) **Planning depth.** **No strict planning requirement** (per `difficulty-rules.md` § 2c L1). Mechanic discovery is the entire difficulty; once the rule is understood, *any* 4-cycle satisfies the predicate.
- (d) **Step budget.** 30 (≈ 3.75× the 8-action witness). Generous — lets the player experiment with edge add/remove without budget pressure.

### Level 2 — base system + 1 new mechanic

**Layout**:
- Grid: 32×32. Camera `width=height=32`.
- 5 nodes:
  - `n0` at (4, 16), starting colour `red`
  - `n1` at (16, 4), starting colour `blue`
  - `n2` at (28, 16), starting colour `red`
  - `n3` at (16, 28), starting colour `blue`
  - `n4` at (16, 16), starting colour `red`
- Target degrees: `[3, 3, 3, 3, 4]` (n4 = 4, all outer = 3). Pip-slots: 3 per outer node, 4 around n4.
- Edge sprite pool: `C(5, 2) × 1 = 10` strands (multiplicity = 1 at L2).
- Step budget: 50.

**Mechanics required by the witness** (= N + 1 = 2 — exactly 1 new mechanic introduced):
- **M1 (edge-link)** — carried forward from L1, still required. Edge-state cycle still `[no edge → single edge → no edge]`.
- **M2 (node-colour-cycle + same-colour-edge constraint)** — ACTION5 with a node selected cycles its colour through the level's palette `[red, blue]`. Edge-creation is **rejected** if the two endpoints have different current colours (visible cue: a brief 6-step palette-13-flash on the proposed edge strand; no edge created; both nodes deselect). The witness must recolour at least one node before the required edges become legal.

**Necessity per mechanic** (counterfactual):
- *L2 cannot be solved without triggering M1 because* the win predicate is identical to L1's (degree-pip match). Win predicate evaluates false at level start with zero edges; any winning sequence creates at least one edge via M1.
- *L2 cannot be solved without triggering M2 because* at level start the colours are `[red, blue, red, blue, red]`. The target graph (4 radials `n_i–n4` for i ∈ {0, 1, 2, 3} + 4 perimeter `n_i–n_(i+1 mod 4)` for i ∈ {0, 1, 2, 3}) requires every adjacent (radial OR perimeter) pair to be same-colour. At start, n0 (red) and n1 (blue) differ; n1 (blue) and n2 (red) differ; n2 (red) and n3 (blue) differ; n3 (blue) and n0 (red) differ; n4 (red) and n1 (blue) differ; n4 (red) and n3 (blue) differ. **Six of the eight target edges are cross-colour and rejected at start.** The witness must recolour to align colours; the recolouring verb is M2.

**Witness solution** (20 actions):
```
ACTION6@(16, 4)        # select n1 (blue)
ACTION5                # cycle n1: blue → red
ACTION6@(16, 28)       # select n3 (blue)
ACTION5                # cycle n3: blue → red — all 5 nodes are now red
ACTION6@(4, 16)        # select n0
ACTION6@(16, 16)       # toggle edge n0–n4: no-edge → single
ACTION6@(16, 4)        # select n1
ACTION6@(16, 16)       # toggle edge n1–n4
ACTION6@(28, 16)       # select n2
ACTION6@(16, 16)       # toggle edge n2–n4
ACTION6@(16, 28)       # select n3
ACTION6@(16, 16)       # toggle edge n3–n4 — n4 now degree 4
ACTION6@(4, 16)        # select n0
ACTION6@(16, 4)        # toggle edge n0–n1
ACTION6@(16, 4)        # select n1
ACTION6@(28, 16)       # toggle edge n1–n2
ACTION6@(28, 16)       # select n2
ACTION6@(16, 28)       # toggle edge n2–n3
ACTION6@(16, 28)       # select n3
ACTION6@(4, 16)        # toggle edge n3–n0 — WIN (all degrees match)
```

**Difficulty justification**:
- (a) **Random-resistance.** A vision-blind random sampler has ≈ 10% chance per click of landing on a node, and ACTION5 is only effective if a node is currently selected. Reaching the (recolour 2 nodes) + (8 specific edges) sequence within 60 actions is bounded by `(0.1)^16 × ordering odds × ACTION5 timing × P(recolour-only-the-blue-nodes) ≪ 10⁻¹⁶`.
- (b) **Human-tractable.** ~ 2 minutes. Cross-colour rejection is the only first-attempt feedback, and it teaches the rule in one click pair. After that, the central n4 with degree-pip ring of 4 telegraphs its role.
- (c) **Planning depth (post-discovery).** *Moderate planning required.* Decision space at level start (post-discovery): 5+ candidate first-actions — recolour any of {n1, n3} (to red, the majority colour), recolour any of {n0, n2, n4} (to blue), or attempt a same-colour edge first (e.g. n0–n2 directly is same-colour but the rasterised line passes through n4 — see *post-discovery wrong path* below). Plausible *wrong* path the post-discovery player would consider: **"go for the chord n0–n2 (both red) since they're same-colour"** — but the line from (4, 16) to (28, 16) passes through (16, 16) where n4 sits, and the engine's `_edge_legal` check rejects edges whose rasterised path overlaps another node's body. The player tries it, sees rejection, learns "edges through nodes are illegal", then chooses the perimeter or radial alternatives. Reasoning chain at each witness step: (1) before recolour: there are 2 blue nodes, recolouring both to red is fewer actions than recolouring 3 reds + n4 to blue (4 vs. 8 ACTION5 calls if you count select+cycle pairs); (2) before n4-radials: n4's degree-4 demand means *every* outer node must connect to n4, so build all radials first; (3) before perimeter: each outer node needs +2 degree from *neighbours* (not the centre, which is already saturated), so connecting both perimeter neighbours of each outer is forced.
- (d) **Step budget.** 50 (= 2.5× witness). Generous over 20-action witness; reflects discovery cost — a typical first-time player tries 4-6 cross-colour edges before generalising the colour rule, costing 8-12 actions before they start the canonical 20-action path.

### Level 3 — system + 1 new mechanic

**Layout**:
- Grid: 32×32. Camera `width=height=32`.
- 4 nodes:
  - `n0` at (8, 16), starting colour `red`
  - `n1` at (16, 8), starting colour `blue`
  - `n2` at (24, 16), starting colour `red`
  - `n3` at (16, 24), starting colour `blue`
- Target degrees: `[4, 2, 4, 2]` (n0 = 4, n1 = 2, n2 = 4, n3 = 2).
- Edge sprite pool: `C(4, 2) × 2 = 12` strands (multiplicity = 2 at L3 — each pair has `_0` and `_1` variants for the two parallel strands).
- Step budget: 50.

**Mechanics required by the witness** (= L2-count + 1 = 3 — exactly 1 new mechanic introduced):
- **M1 (edge-link)** — carried forward, still required.
- **M2 (node-colour-cycle + same-colour-edge constraint)** — carried forward, still required.
- **M3 (multi-edge / 3-state cycle)** — at L3 the per-pair edge-state cycle expands to `[no edge → single edge → double edge → no edge]` (`max_edge_multiplicity = 2`, set in `level.set_data`). A double-edge contributes +2 to each endpoint's degree (rather than +1 for a single). To remove a double, the player either (a) clicks the same pair a third time, advancing the cycle to `no edge`, or (b) clicks directly on the rendered edge sprite (a new click target tagged `edge`) which jumps directly to `no edge`.

**Necessity per mechanic** (counterfactual):
- *L3 cannot be solved without triggering M1 because* the win predicate is identical (degree-pip match), starting at all-zero. Any winning sequence must create at least one edge.
- *L3 cannot be solved without triggering M2 because* at level start the colours are `[red, blue, red, blue]`. EVERY pair (n0–n1, n0–n2, n0–n3, n1–n2, n1–n3, n2–n3) has at least one cross-colour endpoint (only n0–n2 and n1–n3 are same-colour, and BOTH are diagonals that pass through the playfield centre with no obstruction — but they still leave 4 needed edges with cross-colour endpoints). The target graph requires edges to nodes of the opposite starting colour; the witness must recolour both blue nodes to red (or all reds to blue) before those edges become legal.
- *L3 cannot be solved without triggering M3 because* n0 has target degree 4. The maximum single-edge degree of n0 in a 4-node graph is 3 (one edge each to {n1, n2, n3}). The 4th degree-unit MUST come from a parallel edge to one of {n1, n2, n3}, which is M3's distinguishing behaviour. A graph using only single edges (max_edge_multiplicity = 1) makes target degree 4 unsatisfiable on n0 (and symmetrically on n2). The witness uses exactly one double edge (n0–n2) to provide the +2 increment to both n0 and n2.

**Witness solution** (16 actions):
```
ACTION6@(16, 8)        # select n1 (blue)
ACTION5                # cycle n1: blue → red
ACTION6@(16, 24)       # select n3 (blue)
ACTION5                # cycle n3: blue → red — all 4 nodes red
ACTION6@(8, 16)        # select n0
ACTION6@(16, 8)        # edge n0–n1: no-edge → single
ACTION6@(8, 16)        # select n0
ACTION6@(16, 24)       # edge n0–n3: no-edge → single
ACTION6@(16, 8)        # select n1
ACTION6@(24, 16)       # edge n1–n2: no-edge → single
ACTION6@(24, 16)       # select n2
ACTION6@(16, 24)       # edge n2–n3: no-edge → single
ACTION6@(8, 16)        # select n0
ACTION6@(24, 16)       # edge n0–n2: no-edge → single
ACTION6@(8, 16)        # select n0
ACTION6@(24, 16)       # edge n0–n2: single → DOUBLE — WIN
```
At the 16th action: n0 has edges {n0–n1 (single, +1), n0–n3 (single, +1), n0–n2 (double, +2)} = degree 4 ✓; n1 has {n0–n1, n1–n2} = 2 ✓; n2 has {n1–n2, n2–n3, n0–n2 double} = 4 ✓; n3 has {n0–n3, n2–n3} = 2 ✓. `_check_win` fires `self.next_level()` (which, since this is the last level, fires `self.win()`).

**Difficulty justification**:
- (a) **Random-resistance.** Same-or-better than L2; the witness is 16 actions on 4 nodes with multi-edge nuance, so random discovery probability ≪ 10⁻¹⁶.
- (b) **Human-tractable.** ~ 3 minutes. The colour rule transfers from L2 (no re-discovery cost). The new multi-edge rule is discovered when the player clicks an existing edge a third time (out of habit from L1/L2 toggle expectation) and observes the line **thickening into a double strand** instead of disappearing — followed by another click which finally removes it. Discovery cost: 1-3 exploratory pair-clicks.
- (c) **Planning depth (post-discovery).** *Challenging for an attentive human.* Decision space at level start (post-discovery): 6+ candidate first-actions: recolour n1, recolour n3, attempt edges first, double the wrong pair first. **Trivial post-discovery heuristic that fails: "double every edge to maximise progress"** — a player who has discovered both M2 and M3 might think doubling every edge "earns" more progress per click. Doubling n0–n1, n0–n2, n0–n3 gives n0 = 6 (overshooting target 4 by 2), n1 = 2, n2 = 2, n3 = 2. n0 is **over** target — to reach n0 = 4 the player must remove 2 of those parallel edges, but the only removal verb costs 1 click per edge (cycle to no-edge) AND each removal subtracts +1 from the pair partner too: removing one parallel of n0–n1 takes n1 from 2 to 1 (under target), which forces re-adding an edge to n1, costing another 1-2 actions per re-add. The heuristic spirals into 4-6 corrective actions vs. the witness's clean 16. The **witness's correct choice is to double EXACTLY ONE pair (n0–n2) — the unique pair both of whose endpoints have target degree 4**; every other choice of which pair to double overshoots one endpoint and underflows another, irrecoverably forcing extra correction actions. This is the kind of "post-discovery reasoning the player must do" called for by `difficulty-rules.md` § 2c L3.
- (d) **Step budget.** 50 (≈ 3.1× witness). Generous over 16-action witness; reflects added discovery cost (multi-edge rule observation typically costs 2-4 actions of accidental over-clicking).

## 5. Action mapping

`available_actions = [5, 6]` (declared globally). Per-level valid-action gating via `_get_valid_actions`:

| Level | Valid actions | Notes |
|---|---|---|
| 1 | `[ACTION6]` | ACTION5 hidden — keeps L1 truly minimal so the player learns *only* M1 first. |
| 2 | `[ACTION5, ACTION6]` | ACTION5 surfaces; gated to fire only when a node is currently selected. |
| 3 | `[ACTION5, ACTION6]` | Same as L2; multi-edge mechanic uses ACTION6 only (no new action). |

Action semantics (full):

| Action | Effect | Gating |
|---|---|---|
| `ACTION5` | If a node is currently selected: cycle that node's colour through the level's palette (L2/L3 palette = `[red, blue]`), AND deselect the node (set `node_halo` REMOVED, `self._selected_node = None`). Visible cue: in the same frame, the node's colour-variant TANGIBLE-flips to the next colour AND the halo disappears. If no node is selected: no-op (the action still consumes a step via `complete_action`, but no observable state changes). | Listed in valid actions only at L2 and L3. |
| `ACTION6@(x, y)` | Click at display coords. Convert via `self.camera.display_to_grid(int(x), int(y))` to grid `(gx, gy)`. Dispatch: (a) if click coincides with a `node` sprite **and** no node currently selected → select clicked node (set TANGIBLE on `node_halo`, reposition halo to wrap clicked node, store `self._selected_node = clicked`). (b) If a node is selected and click coincides with a *different* `node` sprite → attempt to advance the edge-state cycle for that pair. Validate (same colour, no other-node body on rasterised line, multiplicity within `max_edge_multiplicity` cap); on validation pass advance cycle (`[no, single, double, no]` at L3, `[no, single, no]` at L1/L2); on validation fail set `_reject_flash_phase = 6` and play the cross-colour or invalid-line flash on the proposed edge strand sprite; deselect either way. (c) If click coincides with a rendered `edge` sprite (L3 only) → jump that pair's edge state directly to `no edge`. (d) If click on the same selected node, on a halo, on empty space, or on an out-of-grid cell → deselect. | Always available. |

## 6. HUD and per-game state

**HUD**: `StepCounterHud(RenderableUserDisplay)` draws a depleting horizontal bar at row 0 of the rendered frame. Bar width is `int(64 * remaining / max)` pixels of palette 14 (green); the rest of row 0 is palette 1 (off-white). One instance, registered via `Camera(interfaces=[step_counter_hud])`.

**Per-game state** (instance attributes on `Jx5k`):
- `self._selected_node: str | None` — name of the currently selected node, or `None` if no selection. Mutation rules: SET to clicked-node-name on ACTION6 (a) (click on a node with no current selection); CLEARED to `None` on (i) successful ACTION5 colour cycle, (ii) successful ACTION6 edge-cycle (whether on edge create, edge advance, or edge remove), (iii) rejected ACTION6 edge attempt (cross-colour or invalid line — both endpoints deselect), (iv) ACTION6 click on the currently selected node, on a halo, on empty space, or on an out-of-grid cell.
- `self._reject_flash_phase: int` — counts down from 6 to 0 each step. While > 0, the most-recently-attempted-but-rejected edge strand is rendered in palette 13 (maroon flash) instead of palette 15 (purple) — implemented via swapping the flash-variant sprite in / out, or via direct pixel mutation on the strand sprite.
- `self._step_remaining: int` — actions remaining; initialised in `on_set_level` from `level.get_data("step_budget")` and decremented at start of every step.
- `self._level_palette: list[int]` — palette of legal node-colour values for the current level. L1: `[9]` (no cycling). L2 / L3: `[8, 9]`.
- `self._max_edge_multiplicity: int` — read from `level.get_data("max_edge_multiplicity")`. L1 / L2: 1. L3: 2.
- `self._edge_state: dict[tuple[str, str], int]` — for each unordered pair `(name_i, name_j)` with `name_i < name_j`, the current edge multiplicity ∈ `{0, 1, 2}`. Initialised to 0 for all pairs in `on_set_level`.
- `self._node_color: dict[str, int]` — for each node name, the current palette value. Initialised in `on_set_level` from level data.

**Hidden state hook** (`_get_hidden_state` returns): a single 1×1 `np.int16` array containing `self._reject_flash_phase` — minimal stub per `code/universal-scaffold.md`'s pattern.

**Visible cue per state-change** (per checklist item 19):
- `self._selected_node` mutation → `node_halo` repositioning + TANGIBLE flip.
- `self._reject_flash_phase > 0` → maroon flash on the most-recent rejected strand for 6 frames.
- `self._step_remaining` mutation → HUD bar redraws every step.
- `self._node_color[name]` mutation → that node's TANGIBLE variant swaps from `node_blue` → `node_red` (or vice versa); all variants of each node are pre-placed at the same cell with the inactive variant set REMOVED.
- `self._edge_state[(i, j)]` mutation → `edge_strand_<pair>_0` (single) and / or `edge_strand_<pair>_1` (double parallel) flip TANGIBLE / REMOVED accordingly.

No state mutated by an action lacks a visible cue. Item 19 PASS.

## 7. Win condition

Concrete predicate (called after every successful ACTION6 edge-cycle):

```python
def _check_win(self) -> bool:
    for node in self.current_level.get_sprites_by_tag("node"):
        if node.interaction != InteractionMode.TANGIBLE:
            continue                                  # skip the inactive colour variants
        target = self._target_degree[node.name]
        actual = self._compute_node_degree(node.name)
        if actual != target:
            return False
    return True

def _compute_node_degree(self, name: str) -> int:
    deg = 0
    for (i, j), mult in self._edge_state.items():
        if name in (i, j):
            deg += mult
    return deg
```

If `_check_win()` returns True, fire `self.next_level()` (or `self.win()` on the last level). Win predicate is identical across L1, L2, L3 — the only thing that changes is the per-level target-degree map.

## 8. Lose condition

Concrete predicate (called at the top of `step()` before action dispatch):

```python
if self._step_remaining <= 0:
    self.lose()
    return
```

The energy bar drains 1 per action; reaching 0 fires `self.lose()`. No other lose path (no hazards, no chasers, no soft-locks — the multi-edge cycle is fully reversible at L3, so the player can always undo).

## 9. Novelty note

Closest taxonomy entries (per `mechanic-novelty/similarity-check.md` re-run on the FULL spec):
- **`bp35 procedural-graph-walk`** — bp35's player walks a token along a *pre-built* graph; jx5k's player *constructs* a multigraph from scratch. Different verb (step-along-track vs. pair-click-create-edge), different win condition (reach-token-configuration vs. degree-sequence match), different graph type (simple vs. multigraph at L3). **NOVEL**.
- **`lf52 procedural-graph-walk-undo`** — same family as bp35, same distinguishing rule. **NOVEL**.
- **`cn04 nub-pair-glyph`** — cn04 has spatial pieces with palette-8 nubs that physically *kiss* via slide+rotate of pixel sprites; jx5k's edges are abstract logical connections that don't depend on pixel coincidence. **NOVEL**.
- **`sb26 tile-place-commit`** — sb26 places tiles into slots and commits a row as a Mastermind guess; jx5k has no slots, no commit verb (each pair-click is immediate), no per-slot hint feedback. **NOVEL**.

Closest prior-game entries (per `prior-games/index.md` re-run on the FULL spec):
- **`pz4t anchor-pivot-place`** — pz4t tiles a region with coloured components via reflect/rotate; jx5k connects abstract nodes — no tiling, no spatial component placement, no rotation. **NOVEL**.
- **`qm4t convex-pen-trap`** — qm4t commits a polygon hull and captures critters strictly inside; jx5k builds a multigraph and matches a degree sequence — different win predicate (containment vs. degree match), different action vocabulary (vertex-post drop + ACTION5 commit vs. pair-click immediate). **NOVEL**.
- **`vn8d domino-cascade-topple`** — vn8d triggers chain reactions; jx5k clicks are local with no propagation. **NOVEL**.
- **`qb84 bead-lift-swap`** — qb84 also uses arrow-only chain navigation with lift/drop swaps colour with a peg; jx5k uses ACTION6 click-pairs (not arrows) and has no swap/peg semantics. Different action palette and no shared mechanic concept. **NOVEL**.

Negative-similarity walk-through against `qm4t`, `bx84`, and `bp35` was performed in `mechanic-pick.md` and showed 0 dimensions of overlap with each. The fleshed-out spec now adds same-colour-edge constraint (M2) and multi-edge support (M3) — both of which further differentiate jx5k from any near-miss; multi-graph mechanics are entirely absent from the existing taxonomy and prior-games corpus. **NOVEL**.

`prior-games/index.md` is **non-empty** — 36 entries — and none share family.
