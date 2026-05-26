# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): mechanic family, ID, distinguishing rules
- skills/code/spec-template.md (from this state): 9-section template
- skills/code/universal-scaffold.md (from this state): file structure + naming + scaffold reference
- skills/design-constraints/composition-and-tutorial.md (from study): 3-level structure, +1-or-+2 rule
- skills/design-constraints/difficulty-rules.md (from study): per-level difficulty bullets
- skills/design-constraints/checklist.md (from study): 22 critique items
- skills/global/action-enum.md (from study): action subset rules
- skills/global/color-legend.md (from study): palette 0-15

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for hb5n covering Title, Mechanic-family, Sprite roster (avatar L/J, walls, target slots, growth pickup, rotation-lock, step-counter HUD), Level progression for L1/L2/L3 with mechanic enumeration + necessity + witness solutions + difficulty justification, Action mapping `[1,2,3,4,5]`, HUD + state, Win condition (set-equality), Lose condition (step exhaustion), Novelty note.

## Notes
- Avatar = 3-cell L (L1), grows to 4-cell J via pickup (L2/L3). Rotation 90° CW about anchor.
- Mechanic ladder: L1 (M1 walk + M2 rotate, N=2), L2 (+M3 growth-pickup = 3), L3 (+M4 rotation-lock = 4). Per-level +1 each, satisfying the strict +1-or-+2 rule.
- L3's M4 necessity hinges on the lock-cell wall covering the upper-right region with one rotation island; without M4 the witness could be shorter or differently ordered. Argued concretely in §4.
- Witness lengths: L1 = 23, L2 = 22, L3 = 21 actions. Step budgets 50/60/80, non-shrinking, generous.
- The pickup-growth direction is FIXED at relative (-1, -1) in current rotation — this couples M2 and M3 (rotation before pickup changes growth's absolute target), giving L3 its post-discovery planning gate.
- Spec is ready for critique_spec. If revisions are flagged, the most likely soft spots are: L3's M4 necessity argument (the lock-cell layout is dense and may need a tighter geometric argument), and the per-level cell-pattern specification (sprite pixel arrays could be incomplete).
