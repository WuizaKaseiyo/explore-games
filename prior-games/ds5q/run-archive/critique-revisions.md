# Critique revisions — round 1

The spec violates four checklist items. Transition back to `write_spec` to address each concretely.

## Issue 1 — checklist item 12 (strict counterfactual necessity), L1
- **Violated rule:** "For each mechanic M available at level L, no sequence of actions may win L within the step budget without triggering M's distinguishing behavior."
- **Spec section:** § 4 Level 1 → "Layout".
- **Quote:** L1 layout shows stones only at (3, 3), (3, 5), (5, 3), (5, 5); rows 0, 1, 2, 6, 7 are entirely floor.
- **Why the spec fails:** the avatar at (0, 4) can detour around the two grey walls by walking north to (0, 0), east through the unobstructed top row to (7, 0), then south through col 7 to the exit at (7, 4). No wall blocks this top detour. A symmetric bottom detour exists through rows 6 and 7. The witness exercises erode but the level is solvable without ever touching ACTION5, which violates the "no trivial fallback" rule for the erode mechanic.
- **Concrete fix:** seal rows 3 and 5 with `stone` at every column (replacing the four scattered stones with two full stone rows). The corridor at row 4 then becomes the only east-west passage; avatar entering (0, 4) is bounded by stone at (0, 3) and (0, 5) and must traverse east through both grey walls. State the new layout explicitly in the spec — eight `S` glyphs at row 3 and row 5.

## Issue 2 — checklist item 12, L2 (blue wall detour)
- **Violated rule:** same as Issue 1.
- **Spec section:** § 4 Level 2 → "Layout".
- **Quote:** stones at (3, 0)…(3, 7) except (3, 4); stones at (5, 3) and (5, 5) only.
- **Why the spec fails:** after eroding the red wall at (3, 4), the avatar at (4, 4) can reach the exit at (7, 4) without ever eroding the blue wall at (5, 4) by routing (4, 4) → (4, 3) → (4, 2) → (5, 2) → (6, 2) [blue pad] → (6, 3) → (6, 4) → (7, 4). The cells (5, 2), (6, 2), (6, 3), (6, 4) are all floor in the spec layout. The blue wall and the colour-pickaxe-match mechanic for blue are bypassable, so colour-pickaxe-match is not strictly counterfactually necessary at L2 (red-only would still solve the level).
- **Concrete fix:** add stone walls at (5, 1), (6, 3), (6, 5), and (7, 0), (7, 1), (7, 2), (7, 3), (7, 5), (7, 6), (7, 7) (i.e., col 7 sealed except for the exit at (7, 4) plus the missing (5, 1) and (6, 3) / (6, 5) gaps). The cell (6, 4) then becomes reachable only from (5, 4) [west, the blue wall] or from (7, 4) [east, the exit destination] — forcing the avatar to pass through the blue wall after charging blue at (6, 2). State the new layout explicitly.

## Issue 3 — checklist item 12, L3 (blue wall detour)
- **Violated rule:** same as Issue 1.
- **Spec section:** § 4 Level 3 → "Layout".
- **Quote:** L3 inherits L2's layout outside the red-wall-cell so the same blue-wall detour exists.
- **Why the spec fails:** identical to Issue 2 — colour-pickaxe-match for blue is bypassable at L3 too.
- **Concrete fix:** apply the same stone additions as Issue 2 (col 7 sealed except (7, 4); (6, 3), (6, 5), (5, 1) stones added).

## Issue 4 — checklist item 7 (forbidden elements: real-world clipart)
- **Violated rule:** "No real-world clipart" — `forbidden-elements.md` lists "a key sprite, a sword sprite; recognisable iconography" as examples.
- **Spec section:** § 3 Sprite roster → `avatar_uncharged` / `avatar_red` / `avatar_blue`, and § 2 / § 5 / § 9 mentions of "pickaxe".
- **Quote:** "8×8 pixels; body palette 13 (maroon) with palette 4 (off-black) outline; pickaxe shaft palette 4; pickaxe tip 1×1 pixel palette 0 (white)."
- **Why the spec fails:** a pickaxe is a recognisable real-world tool — the visual reads as iconography. Even a small-pixel pickaxe is identifiable and triggers acquired cultural association ("tool for breaking rock") which is the exact pattern §3.4 forbids.
- **Concrete fix:** redesign the avatar as an abstract sprite with no tool shape and no humanoid shape. Suggested: 6×6 pixel filled square palette 13 with a 2×2 corner indicator patch whose colour reflects the current charge state (white for `None`, red, blue). The corner indicator is a coloured square, not a tool. Update §§ 2, 3, 5, 6, 9 to remove the word "pickaxe" and substitute "charge indicator" / "charge state". This also benefits negative-similarity test by further dis-identifying ds5q from any "tool-wielding avatar" prior reading.

## Issue 5 — difficulty rule (c) post-discovery planning at L3
- **Violated rule:** `difficulty-rules.md` § 2c L3 — "planning is challenging even for an attentive human (post-discovery)... greedy / monotone-progress / follow-the-obvious-gradient strategies should not reliably win" and the stage-conflation guard "Reject if the named 'heuristic that fails' or wrong-path argument is a discovery-stage misstep".
- **Spec section:** § 4 Level 3 → "Difficulty justification" → bullet (c).
- **Quote:** "Trivial post-discovery heuristic that fails: *'After charging red, walk east; if blocked, erode once and continue.'* This greedy single-erode-per-wall strategy fails at L3 because `wall_red_h3` requires three consecutive erode-strikes…"
- **Why the spec fails:** a fully-informed L3 player KNOWS the wall has hardness 3 because the stripe count is visible in the rendered frame. They wouldn't try the "single-erode" heuristic — that's a discovery-stage attempt before the hardness-counter mechanic is internalised. The spec's heuristic-failure argument confuses the discovery stage (which is fine) with the planning stage (which is unmet — there's no real choice for a fully-informed player; the geometry forces one route, and the only "decision" is "press ACTION5 three times"). Per the operational test, the heuristic IS the witness for a fully-informed player, so (c) is unmet.
- **Concrete fix:** introduce a real post-discovery routing choice. Suggested redesign: add a second red wall in col 3 at row 1 (`wall_red_h3` at (3, 1)) accessible from (2, 1) on the avatar's reachable side, with stones sealing col 3 at every other row so col 3 has TWO openings — (3, 1) hardness 3 and (3, 4) hardness 3. The avatar can route via row 1 or row 4 to reach the right half. With both walls hardness 3, the layered-hardness mechanic is exercised either way, but the TOTAL path length differs (the row-1 route is shorter because the red pad at (1, 0) is closer to row 1 than row 4 and the blue pad at (6, 2) is closer to row 1 than row 4). The trivial post-discovery heuristic — "stay on row 4, the same row as the exit" (greedy-toward-exit, monotone-progress along the row containing the goal) — fails because routing via row 1 is several actions shorter (revised witness ≈ 23 actions vs 27 for the row-4 route). Spec § 4 L3 (c) must enumerate the new decision space (≥ 2 routes), name "row-4 monotone-progress" as the failing heuristic, and trace where it diverges from the witness.

---

After revisions, re-validate: items 1-21 all clean; difficulty bullets (a-d) per level; novelty distinguishing rules unchanged (the geometry changes don't affect the family-level distinguishing claims).
