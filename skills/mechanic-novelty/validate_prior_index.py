"""Validate the prior-games index against the documented schema.

Schema is the 5-column table defined in
`skills/mechanic-novelty/prior-games-index-format.md` and
`skills/finalize/index-row-format.md`:

    | game_id | mechanic_family | description | timestamp | seed |

Checks: header matches; every data row has 5 cells; game_id is a
valid 4-char lowercase-alnum id and unique; description has no pipe;
timestamp and mechanic_family are non-empty. Reports the
mechanic-family distribution so a run can eyeball over-represented
families before picking a new mechanic.
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import Counter
from pathlib import Path

EXPECTED_HEADER = ["game_id", "mechanic_family", "description", "timestamp", "seed"]


def parse_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    rows = [parse_row(line) for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("|")]
    if len(rows) < 2:
        return [], []
    return rows[0], rows[2:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate prior-games/index.md")
    parser.add_argument("index", nargs="?", default="prior-games/index.md",
                        help="Path to prior-games index.")
    args = parser.parse_args()

    index_path = Path(args.index)
    errors: list[str] = []
    header, data_rows = table_rows(index_path)

    if header != EXPECTED_HEADER:
        errors.append(f"header mismatch: expected {EXPECTED_HEADER}, got {header}")

    seen_ids: set[str] = set()
    family_counts: Counter[str] = Counter()
    for row_number, row in enumerate(data_rows, start=3):
        if len(row) != len(EXPECTED_HEADER):
            errors.append(f"line {row_number}: expected {len(EXPECTED_HEADER)} cells, got {len(row)}")
            continue

        record = dict(zip(EXPECTED_HEADER, row))
        game_id = record["game_id"]
        if len(game_id) != 4 or not game_id.isalnum() or not game_id.islower():
            errors.append(f"line {row_number}: invalid game_id {game_id!r}")
        if game_id in seen_ids:
            errors.append(f"line {row_number}: duplicate game_id {game_id}")
        seen_ids.add(game_id)

        if not record["mechanic_family"]:
            errors.append(f"line {row_number}: missing mechanic_family")
        if not record["description"]:
            errors.append(f"line {row_number}: missing description")
        if not record["timestamp"]:
            errors.append(f"line {row_number}: missing timestamp")

        family_counts[record["mechanic_family"]] += 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    total = len(data_rows)
    threshold = max(math.ceil(total * 0.20), 5) if total else 5
    print(f"OK: {total} prior games")
    print(f"High-frequency threshold: {threshold}")
    dupes = [(fam, n) for fam, n in family_counts.most_common() if n > 1]
    if dupes:
        print("Repeated mechanic families:")
        for fam, n in dupes:
            print(f"  {fam}: {n}{'  HIGH' if n >= threshold else ''}")
    else:
        print("All mechanic families are unique.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
