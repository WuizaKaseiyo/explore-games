# mechanic-pick — Run #5

## ID

**`dx8m`** — verified not in 25-ref, not in `prior-games/index.md` (30 entries), not a recognisable English word. Pascal class **`Dx8m`** (first-letter caps; rest preserved; no letter-case ambiguity since trailing `m` is preceded by digit `8`).

## Mechanic family tag

**`local-invariant-balance`**

## Skeleton-diversity declaration

| field | value |
|---|---|
| `family_class` | constraint-satisfaction |
| `primary_skeleton` | spatial-constraint |
| `secondary_skeleton` | classification-sorting |
| `interaction_type` | click |
| `state_surface` | visible |
| `state_model` | constraint-counters |
| `objective_shape` | satisfy-constraints |

## Skeleton-diversity verdict

| check | result |
|---|---|
| Recent-5 prior skeletons | cy3k=symbolic-rewrite, tw94=topology-transform, vy3m=multi-actor, ej4t=object-placement, tg6w=global-field-update |
| Candidate `primary_skeleton` (spatial-constraint) in recent-5? | **NO** ✓ |
| Full-corpus high-frequency? | global-field-update=6 (only). spatial-constraint count=2 (qz73, lv4k), not high-freq ✓ |
| Override needed? | NO |
| **Verdict** | **PASS** |

## One-paragraph description

A grid of small "cell" sprites in two visible states (off/on) plus several "region badges" overlaid on the grid. Each badge defines a region (a set of cells) with a visible *count invariant* — e.g., "exactly 2 cells of this region must be on" — encoded by a row of dots inside the badge (not digits). The player clicks cells to toggle them on/off; a cell may belong to multiple overlapping regions, so a single toggle can simultaneously satisfy one region while breaking another. Win when every region's count invariant is simultaneously satisfied. **M1 (L1)**: independent regions — toggling one cell affects exactly one region; trivial deduction per region. **M2 (L2)**: overlapping regions — at least one cell belongs to two regions; toggle propagates a constraint update to multiple regions, requiring the player to find a cell-state assignment that satisfies all regions at once. **M3 (L3)**: ordering / parity — adds a region whose invariant depends on the parity of how many neighbouring regions are satisfied (or a "must-toggle-twice" cell), introducing post-discovery planning where the order of clicks matters.

## Distinguishing rules

### Closest taxonomy: `lv4k` (lever-balance-torque) — same primary skeleton

**Shared**: spatial-constraint reasoning; click-place to satisfy a numerical invariant.

**Distinguishing rule**: lv4k is a SINGLE-axis torque equation (one beam, sum-of-mass-arm = 0). dx8m is MULTI-region overlapping local invariants (each region is independent in count, but cells overlap). lv4k has no overlapping constraints; cells/weights belong to one beam only. dx8m's load-bearing dynamic is overlap resolution — a satisfying assignment cannot be found by greedy per-region work.

### Closest prior: `ng52` (multiset-signature-classify) — secondary skeleton match

**Shared**: classification-sorting flavour (cells assigned to states satisfying a target signature).

**Distinguishing rule**: ng52 partitions a pool of objects into bins by signature; dx8m has stationary cells whose state (on/off) is toggled. Different cast (objects vs cells), different verb (place vs toggle), different objective (signature match vs invariant satisfaction).

### Closest prior: `qz73` (radial-cycle-lock) — same primary skeleton

**Shared**: spatial-constraint primary; alignment-style win.

**Distinguishing rule**: qz73 rotates a central rotor and locks individual tips; constraint is per-tip-to-socket alignment. dx8m has no rotation — only cell toggles — and constraint is region-based count invariants.

## Negative-similarity 7-dim test

vs **lv4k**: shared dim 4 (universal step budget). 1 dim shared, well under 3-dim threshold.
vs **qz73**: shared dim 4. 1 shared.
vs **ng52**: shared dims 4. 1 shared.

**Verdict: NOVEL.**

## Inspiration source

**PS-004 local-invariant-balance** from `skills/inspiration/extra-mechanic-seeds.md`. The seed describes "Clicks assign small symbols to cells, and each local region must satisfy a visible invariant such as balanced counts or paired colours; toggling one shared cell shows how overlapping regions can be fixed or broken by the same action." dx8m adopts this directly with binary on/off cells and count-invariant regions.

## Considered alternatives

| candidate | primary_skeleton | reject reason |
|---|---|---|
| PS-001 rule-rewrite-frontier | symbolic-rewrite | banned (recent-5) |
| PS-002 actor-role-grammar | multi-actor | banned (recent-5) |
| PS-003 wraparound-window | topology-transform | banned (recent-5) |
| **PS-004 local-invariant-balance** | spatial-constraint | **selected** |
| PS-005 inferred-switch-language | signal-routing | viable but PS-004 has cleaner counterfactuals + simpler implementation |

## Action mapping (preview)

`available_actions = [4, 6]` — ACTION6 click toggles a cell; ACTION4 declared but no-op (so the trivial-heuristic gate's "ACTION4 × N" sequence is valid input but ineffective).

## Per-level grid sizes (preview)

- L1: 8×8 grid; 6 active cells in 2 disjoint 3-cell regions
- L2: 10×10 grid; 8 active cells; 2 overlapping regions sharing 1 cell
- L3: 12×12 grid; 10 active cells; 3 regions with multi-overlap and an ordering constraint

## Lessons applied from cy3k post-mortem

- **Visual richness**: cells are 4×4 sprites with internal hollow/solid patterns (not 1×1 chunks scaling up to chunky blocks).
- **Strict counterfactual**: each level's witness must SOLVE all regions; any region unsatisfied → no win. M3 introduces a region whose invariant depends on others, so the L3 witness exercises the new constraint rule.
- **Discoverability**: clicking a cell shows immediate visible state change AND a visible "satisfied/unsatisfied" highlight on the affected region badges. Player learns by 1-2 clicks.
- **§3.4 ceiling**: count-constraint puzzles are a known family (Nonograms / Picross / Battleship), but dx8m's specific overlap + ordering structure is not a clone of any single commercial title.
