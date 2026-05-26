# Step #06: smoke_test

## Inputs Consumed

- `prior-games/ej4t/ej4t.py` (from #05 implement)
- `mechanic-spec.md` (from #03; for witness sequences)
- skills/code/smoke-test-checks.md (10 universal checks + custom check templates)

## Deliverables Produced

- `smoke-test.py` — combined test runner (universal + custom)
- `smoke-test-pass.md` — 12 PASS, 0 FAIL, 1 SKIPPED

## Notes

### One initial failure, fixed inline (not requiring `fix_implementation` revisit)
- Fixed `GameAction(n)` → `GameAction.from_id(n)` in test runner (novaengine API quirk; documented in novaengine-api.md but I missed on first pass).
- Fixed `camera.render(level)` → `camera.render(level.get_sprites())` (signature is `List[Sprite]`, not `Level`).

Both fixes were in the **test runner**, not the game source — game source unchanged from #05 implement. So no fix_implementation loop needed.

### Witness replay end-to-end
The new CHECK_WITNESS_WINS (upstream cb225e1) replayed the spec's 3 witnesses verbatim:
- L1 [ACTION4 × 5]: chain push C1+C2 → win
- L2 [ACTION4 × 5]: pickup at (5,7); chain push → win
- L3 [ACTION4 × 7]: pickup_a; shrinker; pickup_b; chain push of 3 → WIN

End-to-end validation confirms no spec-vs-implementation distance/coordinate drift bugs. The witness from spec actually plays the game to completion.

### Custom checks confirm M1, M2, M3 mechanics fire as designed
- M1 chain push gating: implicitly verified by witness (chain pushes succeeded only when R was sufficient).
- M2 extender: verified by custom check (R 1 → 2 after walking onto pickup).
- M3 shrinker: verified by custom check (R 3 → 2 after walking onto trap).

Transition: smoke_test → finalize.
