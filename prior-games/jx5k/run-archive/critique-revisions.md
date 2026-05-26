# critique-revisions.md (visit #2 of `critique_spec`)

Spec under review: `workspace/mechanic-spec.md` (revised after visit #1; game ID `jx5k`).

The visit-#1 issues are all RESOLVED in the current spec:
- M3 is now `multi-edge / 3-state cycle` (active verb, witness exercises it). ✓
- L3 layout is consolidated to a single concrete description (4 cardinal nodes, target `[4, 2, 4, 2]`). ✓
- L3 difficulty justification names a concrete post-discovery heuristic ("double every edge") that diverges from the witness and incurs ~5 extra correction actions. ✓
- §3 sprite roster collapsed pip variants and added multiplicity to edge sprites. ✓

Two **new issues** remain:

---

## Issue 1 — L2 target-degree / witness inconsistency (Checklist item 11 + item 16)

**(a) Violation.** §4 Level 2 declares `Target degrees: [2, 2, 2, 2, 4] (n4 = 4, all outer = 2)`. The witness then builds 8 edges (4 radials + 4 perimeter), which gives each outer node degree **3** (1 from radial + 2 from neighbouring perimeter edges), not the declared target of **2**. The witness as written would NOT satisfy `_check_win` because every outer node ends with `actual=3, target=2`.

**(b) Offending section + quote.** §4 Level 2 — *"Target degrees: `[2, 2, 2, 2, 4]` (n4 = 4, all outer = 2)."* combined with the listed witness ending at *"toggle edge n3–n0 — WIN (all degrees match)"*. The two statements are inconsistent.

**(c) Fix.** Change the L2 target degrees to `[3, 3, 3, 3, 4]` so the 8-edge witness satisfies every node:
- n0: 1 (radial) + 1 (n0–n1) + 1 (n3–n0) = 3 ✓
- n1: 1 + 1 + 1 = 3 ✓
- n2: 1 + 1 + 1 = 3 ✓
- n3: 1 + 1 + 1 = 3 ✓
- n4: 4 (4 radials) = 4 ✓

This keeps the witness count at 20 actions and the step budget at 50 (= 2.5× witness, generous). Update §4 L2's *Layout* line and *Mechanics required* explanation accordingly.

---

## Issue 2 — ACTION5 selection state semantics ambiguous (Checklist item 19 + item 5)

**(a) Violation.** §5 Action mapping describes ACTION5 as *"If a node is currently selected: cycle that node's colour through the level's palette."* — but does NOT specify whether the node remains selected after the cycle. The L2 and L3 witnesses BOTH assume that ACTION5 **auto-deselects** the node after cycling: e.g., L2 step 2 (`ACTION5` cycles n1) is followed at step 3 by `ACTION6@(16, 28)` which the spec describes as "select n3 (blue)". For step 3 to produce a select rather than an edge-attempt, n1 must have been deselected by ACTION5 in step 2.

If ACTION5 leaves n1 selected, step 3's click on n3 would attempt edge n1–n3 instead — and at that point n1 is red (just cycled) but n3 is still blue, so the edge would be **rejected for cross-colour**, deselecting both, and the witness state would diverge from the spec's claimed sequence.

**(b) Offending section + quote.** §5 Action mapping — *"`ACTION5`: If a node is currently selected: cycle that node's colour through the level's palette (L2/L3 palette = `[red, blue]`)."* — silent on post-cycle selection.

**(c) Fix.** Append to ACTION5's row: *"After successful colour cycling, deselect the node (set `node_halo` REMOVED, `self._selected_node = None`). Visible cue: halo disappears in the same frame the colour swaps."* This makes the state transition explicit and the witnesses correct.

Also update §6 *"Per-game state"*: the `self._selected_node` mutation rule should now read *"set to `None` on (i) successful ACTION5 cycle, (ii) successful ACTION6 edge-cycle, (iii) ACTION6 click on selected node / empty cell / out-of-grid; set to clicked-node-name on (iv) ACTION6 click on a node with no current selection."*

---

## Other items: PASS

All other checklist items continue to PASS as verified in visit #1, with the M3-walls → M3-multi-edge change producing strict-counterfactual cleanliness at L3 (item 12).

Novelty (items 13-15): unchanged. Multi-graph mechanics absent from taxonomy + prior-games corpus.

---

## Summary

- **Issue 1** (L2 target/witness inconsistency) — must fix for the witness to actually win.
- **Issue 2** (ACTION5 deselection semantics) — must fix for the witnesses to be unambiguously correct under the action mapping.

Both fixes are localized text edits. **Verdict**: REVISE. Transition back to `write_spec` for the targeted fixes.
