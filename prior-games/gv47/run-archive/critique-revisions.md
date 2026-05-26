# critique-revisions (v1)

## Issue 1 — `wind_arrow` sprite risks reading as a letter / arrow glyph

**Checklist item violated.** §3.4 / `design-constraints/forbidden-elements.md`:
> Cultural conventions | Acquired association | Green-means-go;
> red-means-danger; an arrow shape implying direction.
> ABSTRACT shapes resembling letters/objects are OK only if they are
> not RECOGNISABLE as the language/object.

**Offending section.** `mechanic-spec.md` §3 sprite roster, row
`wind_arrow`:

> `wind_arrow` | 3×3 | `[[5,5,-1],[5,-1,-1],[5,-1,-1]]` then color-remapped per direction at level setup | `wind`, `sys_decoration` | An angular black hook glyph at the playfield edge whose corner orientation visually couples to a cardinal direction.

The pixel pattern renders as

```
■ ■ ·
■ · ·
■ · ·
```

— a 3-cell vertical column with a single perpendicular top-row cell.
That is unambiguously readable as the Roman letter "L" (and on rotation,
as a directional hook arrow), both forbidden.

**Suggested fix.** Replace `wind_arrow` with a non-letter,
non-arrow visual cue:

- New sprite `wind_strip`: a 1×8 vertical filled bar (palette `10`,
  light-blue) placed at column 11 (east edge), rows 2..9. The bar
  is a topology-neutral block that does not read as a letter or
  arrow. Its **position** alone (always at the east edge in L3,
  always running parallel to the playfield's east boundary) is the
  visual hint that "the east edge is special". The bias direction is
  fixed (always east) so colour-remapping per-direction is no longer
  needed.
- Update §4 L3 configuration to reference `wind_strip` instead of
  `wind_arrow`. Witness sequence is unchanged (the bias is still
  east-only).
- Update §6 per-game state: `self.wind_dir` becomes a fixed
  `(1, 0)` when a `wind_strip` sprite is in the level, else `None`.

## Other items checked

- Items 1, 2, 3, 4, 5, 6, 8, 9, 10, 10a, 11, 12, 13, 14, 15, 16: PASS.
- Negative-similarity re-walk vs lq5x and the other priors: PASS
  (the fleshed-out L3 with mix-table extension does not pull the
  candidate closer to any prior on dimensions 1, 2, 5, 6, 7, or 8).

Loop back to `write_spec` to address Issue 1, then re-enter
`critique_spec` (visit #2).
