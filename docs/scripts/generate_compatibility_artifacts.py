#!/usr/bin/env python3
"""Generate reproducible DeceasedCraft compatibility CSV inventories.

Reads the verified CurseForge mod metadata (`categorized_mods.json`) and
official pack archive manifests (`archives/*.zip::manifest.json`) to produce
two separate, complete, deterministic compatibility inventories:

  1. compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv          (224 mods)
  2. compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv   (307 mods: 306 Standard + 1 DH Edition Extra)

Usage:
  python3 docs/scripts/generate_compatibility_artifacts.py \
      --scratch-dir /path/to/scratch \
      --repo-root /path/to/repo
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

DEFAULT_SCRATCH_DIR = Path(
    "/home/antigravity/.gemini/jetski/brain/v1/default/"
    "jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch"
)
DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[2]

ARCHIVE_555 = "DeceasedCraft-5.5.5.zip"
ARCHIVE_V6_STD = "DeceasedCraft_Beta-5.10.17.zip"
ARCHIVE_V6_DH = "DeceasedCraft_Beta_DH_Edition-5.10.17.zip"

CSV_COLUMNS = [
    "project_id",
    "mod_name",
    "slug",
    "category",
    "edition",
    "in_both_packs",
    "supported_1201_forge",
    "file_id",
    "jar_filename",
    "curseforge_url",
    "notes",
]

EXPECTED_555_COUNT = 224
EXPECTED_V6_COUNT = 307
EXPECTED_V6_STD_COUNT = 306
EXPECTED_V6_DH_EXTRA_COUNT = 1
EXPECTED_SHARED_COUNT = 151

ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\ufeff]")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(value: Any) -> str:
    """Normalize whitespace and strip invisible zero-width Unicode characters."""
    if value is None:
        return ""
    text = ZERO_WIDTH_RE.sub("", str(value))
    return WHITESPACE_RE.sub(" ", text).strip()


def sha256_file(path: Path) -> str:
    """Return lowercase hex SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest_file_ids(archive_path: Path) -> dict[int, int]:
    """Extract {projectID: fileID} mapping directly from a CurseForge zip manifest."""
    if not archive_path.is_file():
        raise FileNotFoundError(f"Official CurseForge archive not found: {archive_path}")
    with zipfile.ZipFile(archive_path, "r") as zf:
        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
    mapping: dict[int, int] = {}
    for entry in manifest.get("files", []):
        pid = int(entry["projectID"])
        fid = int(entry["fileID"])
        if pid in mapping:
            raise ValueError(f"Duplicate projectID {pid} in {archive_path.name}")
        mapping[pid] = fid
    return mapping


def build_rows_555(
    mods: dict[str, dict[str, Any]],
    manifest_555: dict[int, int],
) -> list[dict[str, str]]:
    """Build deterministic CSV rows for DeceasedCraft v5.5.5 (MC 1.18.2 Forge)."""
    rows: list[dict[str, str]] = []
    for mod in mods.values():
        if not mod.get("in_555"):
            continue
        pid = int(mod["pid"])
        if pid not in manifest_555:
            raise KeyError(f"project_id {pid} missing from {ARCHIVE_555} manifest.json")
        rows.append(
            {
                "project_id": str(pid),
                "mod_name": clean_text(mod.get("title_clean") or mod.get("title")),
                "slug": clean_text(mod.get("slug")),
                "category": clean_text(mod.get("category")),
                "edition": "Standard",
                "in_both_packs": "Yes" if mod.get("in_both") else "No",
                "supported_1201_forge": "Yes" if mod.get("supported_1201_forge") else "No",
                "file_id": str(manifest_555[pid]),
                "jar_filename": clean_text(mod.get("file_555")),
                "curseforge_url": clean_text(mod.get("url")),
                "notes": clean_text(mod.get("notes_555") or mod.get("summary_clean")),
            }
        )
    rows.sort(key=lambda r: (r["category"].lower(), r["mod_name"].lower(), int(r["project_id"])))
    return rows


def build_rows_v6(
    mods: dict[str, dict[str, Any]],
    manifest_v6_std: dict[int, int],
    manifest_v6_dh: dict[int, int],
) -> list[dict[str, str]]:
    """Build deterministic CSV rows for DeceasedCraft Beta 5.10.17 (MC 1.20.1 Forge)."""
    # Verify DH edition is a strict superset of Standard with identical fileIDs for shared mods
    for pid, fid in manifest_v6_std.items():
        if manifest_v6_dh.get(pid) != fid:
            raise ValueError(
                f"Manifest mismatch between Standard and DH Edition for project_id {pid}: "
                f"{fid} vs {manifest_v6_dh.get(pid)}"
            )

    rows: list[dict[str, str]] = []
    for mod in mods.values():
        if not mod.get("in_v6"):
            continue
        pid = int(mod["pid"])
        if pid not in manifest_v6_dh:
            raise KeyError(f"project_id {pid} missing from {ARCHIVE_V6_DH} manifest.json")
        edition = clean_text(mod.get("v6_edition"))
        if edition == "Standard" and pid not in manifest_v6_std:
            raise KeyError(f"Standard mod project_id {pid} missing from {ARCHIVE_V6_STD}")
        if edition != "Standard" and pid in manifest_v6_std:
            raise ValueError(f"Non-Standard mod project_id {pid} unexpectedly in {ARCHIVE_V6_STD}")

        rows.append(
            {
                "project_id": str(pid),
                "mod_name": clean_text(mod.get("title_clean") or mod.get("title")),
                "slug": clean_text(mod.get("slug")),
                "category": clean_text(mod.get("category")),
                "edition": edition,
                "in_both_packs": "Yes" if mod.get("in_both") else "No",
                "supported_1201_forge": "Yes",
                "file_id": str(manifest_v6_dh[pid]),
                "jar_filename": clean_text(mod.get("file_v6")),
                "curseforge_url": clean_text(mod.get("url")),
                "notes": clean_text(mod.get("notes_v6") or mod.get("summary_clean")),
            }
        )
    rows.sort(key=lambda r: (r["category"].lower(), r["mod_name"].lower(), int(r["project_id"])))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write rows with UTF-8 encoding and LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=CSV_COLUMNS,
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(rows)


def verify_csv(path: Path, expected_rows: int) -> list[dict[str, str]]:
    """Re-read a generated CSV and assert schema, row count, and non-empty fields."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_COLUMNS:
            raise AssertionError(
                f"{path.name}: header mismatch {reader.fieldnames!r} != {CSV_COLUMNS!r}"
            )
        rows = list(reader)

    if len(rows) != expected_rows:
        raise AssertionError(f"{path.name}: expected {expected_rows} rows, got {len(rows)}")

    seen_pids: set[str] = set()
    for idx, row in enumerate(rows, start=2):
        for col in CSV_COLUMNS:
            val = row.get(col, "")
            if not val or not val.strip():
                raise AssertionError(f"{path.name} line {idx}: blank required column '{col}'")
        pid = row["project_id"]
        if pid in seen_pids:
            raise AssertionError(f"{path.name} line {idx}: duplicate project_id {pid}")
        seen_pids.add(pid)
        if row["in_both_packs"] not in {"Yes", "No"}:
            raise AssertionError(f"{path.name} line {idx}: invalid in_both_packs={row['in_both_packs']!r}")
        if row["supported_1201_forge"] not in {"Yes", "No"}:
            raise AssertionError(
                f"{path.name} line {idx}: invalid supported_1201_forge={row['supported_1201_forge']!r}"
            )
        if not row["curseforge_url"].startswith("https://"):
            raise AssertionError(f"{path.name} line {idx}: invalid URL {row['curseforge_url']!r}")
        int(row["project_id"])
        int(row["file_id"])

    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate DeceasedCraft compatibility CSV inventories from verified CurseForge archives."
    )
    parser.add_argument(
        "--scratch-dir",
        type=Path,
        default=DEFAULT_SCRATCH_DIR,
        help="Directory containing categorized_mods.json and archives/*.zip",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repository root where compatibility/inventory/*.csv will be written",
    )
    parser.add_argument(
        "--print-hashes",
        action="store_true",
        help="Also compute and print SHA-256 hashes of the three official archives",
    )
    args = parser.parse_args(argv)

    scratch_dir: Path = args.scratch_dir.resolve()
    repo_root: Path = args.repo_root.resolve()
    categorized_path = scratch_dir / "categorized_mods.json"
    archives_dir = scratch_dir / "archives"

    if not categorized_path.is_file():
        raise FileNotFoundError(f"Missing categorized_mods.json at {categorized_path}")

    with categorized_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    mods: dict[str, dict[str, Any]] = data["mods"]

    p555 = archives_dir / ARCHIVE_555
    pv6_std = archives_dir / ARCHIVE_V6_STD
    pv6_dh = archives_dir / ARCHIVE_V6_DH

    if args.print_hashes:
        for archive in (p555, pv6_std, pv6_dh):
            print(f"SHA256  {archive.name}: {sha256_file(archive)}")

    manifest_555 = load_manifest_file_ids(p555)
    manifest_v6_std = load_manifest_file_ids(pv6_std)
    manifest_v6_dh = load_manifest_file_ids(pv6_dh)

    rows_555 = build_rows_555(mods, manifest_555)
    rows_v6 = build_rows_v6(mods, manifest_v6_std, manifest_v6_dh)

    out_555 = repo_root / "compatibility" / "inventory" / "deceasedcraft-5.5.5-1.18.2.csv"
    out_v6 = repo_root / "compatibility" / "inventory" / "deceasedcraft-beta-5.10.17-1.20.1.csv"

    write_csv(out_555, rows_555)
    write_csv(out_v6, rows_v6)

    verified_555 = verify_csv(out_555, EXPECTED_555_COUNT)
    verified_v6 = verify_csv(out_v6, EXPECTED_V6_COUNT)

    v6_std_count = sum(1 for r in verified_v6 if r["edition"] == "Standard")
    v6_dh_count = sum(1 for r in verified_v6 if r["edition"] == "DH Edition Extra")
    if v6_std_count != EXPECTED_V6_STD_COUNT or v6_dh_count != EXPECTED_V6_DH_EXTRA_COUNT:
        raise AssertionError(
            f"Unexpected v6 edition split: Standard={v6_std_count}, DH Extra={v6_dh_count}"
        )

    pids_555 = {r["project_id"] for r in verified_555}
    pids_v6 = {r["project_id"] for r in verified_v6}
    shared_pids = pids_555 & pids_v6
    if len(shared_pids) != EXPECTED_SHARED_COUNT:
        raise AssertionError(
            f"Expected {EXPECTED_SHARED_COUNT} shared mods, got {len(shared_pids)}"
        )

    for r in verified_555:
        expected_both = "Yes" if r["project_id"] in shared_pids else "No"
        if r["in_both_packs"] != expected_both:
            raise AssertionError(f"5.5.5 in_both_packs mismatch for project_id {r['project_id']}")
    for r in verified_v6:
        expected_both = "Yes" if r["project_id"] in shared_pids else "No"
        if r["in_both_packs"] != expected_both:
            raise AssertionError(f"v6 in_both_packs mismatch for project_id {r['project_id']}")

    print(f"OK  {out_555} ({len(verified_555)} rows + header, 0 blanks)")
    print(
        f"OK  {out_v6} ({len(verified_v6)} rows + header: "
        f"{v6_std_count} Standard + {v6_dh_count} DH Edition Extra, 0 blanks)"
    )
    print(f"OK  Cross-pack reconciliation: {len(shared_pids)} shared mods verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
