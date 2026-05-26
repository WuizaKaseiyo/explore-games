"""Validate inspiration seed files.

The validator intentionally uses only the Python standard library so it can
run in any agent environment before optional dependencies are installed.
It understands the small YAML subset used by SCHEMA.md: scalar values and
inline string lists such as `[kf42, ls20]`.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


FAMILY_CLASSES = {
    "symbolic-rewrite",
    "multi-actor",
    "topology-transform",
    "constraint-satisfaction",
    "hidden-state",
    "induction",
    "cellular-automaton",
    "set-or-recipe",
    "graph-traversal",
    "physics-leaning",
    "other",
}
EXPLORATION_PROFILES = {
    "rule-induction",
    "state-revelation",
    "tool-affordance",
    "system-dynamics",
    "topology-discovery",
    "resource-experiment",
    "multi-agent-discovery",
    "constraint-probing",
}
INTERACTION_TYPES = {"arrows", "click", "click+arrows", "global-tick", "modal"}
STATE_SURFACES = {"visible", "partially-hidden", "inferred-rule", "memory-required"}
IMPLEMENTATION_RISKS = {"low", "medium", "high"}
CLASSIC_OVERLAPS = {
    "none",
    "sokoban-like",
    "sliding-block-like",
    "pipe-routing-like",
    "baba-like",
    "other",
}
USABLE_AS = {"direct", "abstract-inspiration", "reject"}
REQUIRED_FIELDS = {
    "id",
    "source",
    "source_url",
    "fetched_via",
    "last_refreshed",
    "family_tag",
    "family_class",
    "exploration_profile",
    "interaction_type",
    "state_surface",
    "implementation_risk",
    "classic_overlap",
    "usable_as",
    "closest_prior_ids",
}
REQUIRED_SECTIONS = {
    "Core mechanic",
    "Interactive loop",
    "Exploration hook",
    "Progress signal",
    "Failure or pressure",
    "Novelty WRT corpus",
    "Composition directions",
}
IGNORED_FILES = {"README.md", "SCHEMA.md", "PLAN.md", "AUDIT.md", "SOURCE_CATALOG.md"}

SEED_HEADING_RE = re.compile(
    r"^###\s+(?P<id>[A-Z]{1,4}-\d{2,})\s+(?:-|--)\s+(?P<tag>[a-z0-9-]+)\s*$",
    re.MULTILINE,
)
FENCE_RE = re.compile(r"```yaml\s*\n(?P<body>.*?)\n```", re.DOTALL)
SECTION_RE = re.compile(r"^\*\*(?P<name>[^:*]+):\*\*", re.MULTILINE)


@dataclass
class Seed:
    path: str
    heading_id: str
    heading_tag: str
    yaml: dict[str, object]
    body: str


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("'\"") for part in inner.split(",")]
    return value.strip("'\"")


def parse_yaml_subset(text: str) -> dict[str, object]:
    out: dict[str, object] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = parse_scalar(value)
    return out


def iter_seed_blocks(path: Path) -> list[Seed]:
    text = path.read_text(encoding="utf-8")
    matches = list(SEED_HEADING_RE.finditer(text))
    seeds: list[Seed] = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        fence = FENCE_RE.search(block)
        yaml_data = parse_yaml_subset(fence.group("body")) if fence else {}
        seeds.append(
            Seed(
                path=str(path),
                heading_id=match.group("id"),
                heading_tag=match.group("tag"),
                yaml=yaml_data,
                body=block,
            )
        )
    return seeds


def seed_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.glob("*.md")
        if p.name not in IGNORED_FILES and p.is_file()
    )


def read_known_ids(repo_root: Path) -> set[str]:
    ids: set[str] = set()
    for base in (
        repo_root / "game_sources",
        repo_root / "game_sources_3_lvls",
    ):
        if base.exists():
            ids.update(p.name for p in base.iterdir() if p.is_dir())

    priors = repo_root / "prior-games"
    if priors.exists():
        ids.update(
            p.name
            for p in priors.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        )
    return ids


def section_names(seed: Seed) -> set[str]:
    return {
        match.group("name").strip()
        for match in SECTION_RE.finditer(seed.body)
    }


def validate_seed(seed: Seed, known_ids: set[str]) -> list[str]:
    errors: list[str] = []
    prefix = f"{seed.path}:{seed.heading_id}"
    data = seed.yaml

    missing = sorted(REQUIRED_FIELDS - set(data.keys()))
    if missing:
        errors.append(f"{prefix}: missing YAML fields: {', '.join(missing)}")

    if data.get("id") and data["id"] != seed.heading_id:
        errors.append(f"{prefix}: heading id and YAML id differ")
    if data.get("family_tag") and data["family_tag"] != seed.heading_tag:
        errors.append(f"{prefix}: heading tag and YAML family_tag differ")

    enum_checks = [
        ("family_class", FAMILY_CLASSES),
        ("exploration_profile", EXPLORATION_PROFILES),
        ("interaction_type", INTERACTION_TYPES),
        ("state_surface", STATE_SURFACES),
        ("implementation_risk", IMPLEMENTATION_RISKS),
        ("classic_overlap", CLASSIC_OVERLAPS),
        ("usable_as", USABLE_AS),
    ]
    for key, allowed in enum_checks:
        value = data.get(key)
        if value is not None and value not in allowed:
            errors.append(
                f"{prefix}: invalid {key}={value}; expected one of {sorted(allowed)}"
            )

    source_url = str(data.get("source_url", ""))
    if source_url and not source_url.startswith(("https://", "http://", "local:")):
        errors.append(f"{prefix}: source_url must be http(s) or local:")

    closest = data.get("closest_prior_ids")
    if closest is not None and not isinstance(closest, list):
        errors.append(f"{prefix}: closest_prior_ids must be an inline list")
    elif closest:
        unknown = [
            item
            for item in closest
            if item not in known_ids and not any(ch == "-" for ch in item)
        ]
        if unknown:
            errors.append(f"{prefix}: closest_prior_ids not found in known corpus: {unknown}")

    missing_sections = sorted(REQUIRED_SECTIONS - section_names(seed))
    if missing_sections:
        errors.append(f"{prefix}: missing markdown sections: {', '.join(missing_sections)}")

    return errors


def parse_readme_counts(root: Path) -> dict[str, int]:
    readme = root / "README.md"
    if not readme.exists():
        return {}
    counts: dict[str, int] = {}
    for line in readme.read_text(encoding="utf-8").splitlines():
        if "|" not in line or ".md" not in line:
            continue
        parts = [part.strip().strip("`") for part in line.split("|")]
        filename = next((part for part in parts if part.endswith(".md")), None)
        count = next((int(part) for part in parts if part.isdigit()), None)
        if filename and count is not None:
            counts[filename] = count
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skills/inspiration directory")
    parser.add_argument(
        "--min-seeds",
        type=int,
        default=1,
        help="Fail if total seed count is below this threshold.",
    )
    parser.add_argument(
        "--min-non-physics",
        type=float,
        default=0.0,
        help="Fail if non-physics seed ratio is below this value, e.g. 0.70.",
    )
    parser.add_argument(
        "--min-exploration-profiles",
        type=int,
        default=1,
        help="Fail if fewer distinct exploration_profile values are present.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    # skills/inspiration/ -> skills/ -> repo root
    repo_root = root.parents[1]
    known_ids = read_known_ids(repo_root)

    errors: list[str] = []
    seeds: list[Seed] = []
    for path in seed_files(root):
        seeds.extend(iter_seed_blocks(path))

    if not seeds:
        errors.append(f"{root}: no structured seed entries found")

    duplicate_ids = [
        seed_id
        for seed_id, count in Counter(seed.heading_id for seed in seeds).items()
        if count > 1
    ]
    if duplicate_ids:
        errors.append(f"duplicate seed ids: {duplicate_ids}")

    for seed in seeds:
        errors.extend(validate_seed(seed, known_ids))

    readme_counts = parse_readme_counts(root)
    actual_counts = Counter(Path(seed.path).name for seed in seeds)
    for filename, expected in readme_counts.items():
        actual = actual_counts.get(filename, 0)
        if actual != expected:
            errors.append(
                f"README count mismatch for {filename}: expected {expected}, got {actual}"
            )

    total = len(seeds)
    if total < args.min_seeds:
        errors.append(f"seed count {total} below required minimum {args.min_seeds}")

    classes = Counter(str(seed.yaml.get("family_class", "unknown")) for seed in seeds)
    exploration_profiles = Counter(
        str(seed.yaml.get("exploration_profile", "unknown")) for seed in seeds
    )
    non_physics = sum(
        count
        for family_class, count in classes.items()
        if family_class != "physics-leaning"
    )
    ratio = (non_physics / total) if total else 0.0
    if args.min_non_physics and ratio < args.min_non_physics:
        errors.append(
            f"non-physics ratio {ratio:.1%} below required {args.min_non_physics:.1%}"
        )
    if len(exploration_profiles) < args.min_exploration_profiles:
        errors.append(
            "exploration profile count "
            f"{len(exploration_profiles)} below required {args.min_exploration_profiles}"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {total} seeds")
    print("Family classes:")
    for family_class, count in sorted(classes.items()):
        print(f"  {family_class}: {count}")
    print("Exploration profiles:")
    for profile, count in sorted(exploration_profiles.items()):
        print(f"  {profile}: {count}")
    print(f"Non-physics ratio: {ratio:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
