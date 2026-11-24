#!/usr/bin/env python3
"""Automated verification and audit script for DeceasedCraft_Mod_Research.xlsx."""

import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

SCRATCH = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch")
XLSX_PATH = Path("/home/antigravity/DeceasedCraft_Mod_Research.xlsx")


def main():
    wb = load_workbook(XLSX_PATH, data_only=False)
    assert wb.sheetnames == [
        "v5.5.5 (MC 1.18.2)",
        "Beta 5.10.17 (MC 1.20.1)",
        "Comparison & Mod-Dev Summary",
    ], f"Unexpected sheet names: {wb.sheetnames}"

    ws1 = wb["v5.5.5 (MC 1.18.2)"]
    ws2 = wb["Beta 5.10.17 (MC 1.20.1)"]
    ws3 = wb["Comparison & Mod-Dev Summary"]

    # 1. Raw archive manifest counts
    def manifest_count(zip_name):
        with zipfile.ZipFile(SCRATCH / "archives" / zip_name) as zf:
            return len(json.loads(zf.read("manifest.json"))["files"])

    raw_555 = manifest_count("DeceasedCraft-5.5.5.zip")
    raw_v6_std = manifest_count("DeceasedCraft_Beta-5.10.17.zip")
    raw_v6_dh = manifest_count("DeceasedCraft_Beta_DH_Edition-5.10.17.zip")

    cat_data = json.loads((SCRATCH / "categorized_mods.json").read_text(encoding="utf-8"))
    excluded = cat_data["excluded_non_mods"]
    ex_555 = sum(1 for x in excluded if x["in_555"])
    ex_v6_std = sum(1 for x in excluded if x["in_v6_std"])
    ex_v6_dh = sum(1 for x in excluded if x["in_v6_dh"])

    # 2. Extract and validate Sheet 1 rows
    rows_1 = []
    for r in range(4, ws1.max_row + 1):
        vals = [ws1.cell(r, c).value for c in range(1, 8)]
        assert all(v is not None and str(v).strip() != "" for v in vals), f"Blank cell on Sheet 1 row {r}: {vals}"
        assert not re.search(r"[\u200b\u200c\u200d\ufeff]", vals[0]), f"Zero-width char in Sheet 1 row {r}"
        assert vals[2] in ("Yes", "No"), f"Invalid 1.20.1 support value on row {r}: {vals[2]}"
        assert vals[3] in ("Yes", "No"), f"Invalid In Both value on row {r}: {vals[3]}"
        assert vals[6].startswith("https://"), f"Invalid URL on Sheet 1 row {r}: {vals[6]}"
        assert ws1.cell(r, 7).hyperlink is not None, f"Missing hyperlink on Sheet 1 row {r}"
        rows_1.append(vals)

    # 3. Extract and validate Sheet 2 rows
    rows_2 = []
    for r in range(4, ws2.max_row + 1):
        vals = [ws2.cell(r, c).value for c in range(1, 8)]
        assert all(v is not None and str(v).strip() != "" for v in vals), f"Blank cell on Sheet 2 row {r}: {vals}"
        assert not re.search(r"[\u200b\u200c\u200d\ufeff]", vals[0]), f"Zero-width char in Sheet 2 row {r}"
        assert vals[2] in ("Standard", "DH Edition Extra", "Standard Only"), f"Invalid Edition on row {r}: {vals[2]}"
        assert vals[3] in ("Yes", "No"), f"Invalid In Both value on Sheet 2 row {r}: {vals[3]}"
        assert vals[6].startswith("https://"), f"Invalid URL on Sheet 2 row {r}: {vals[6]}"
        assert ws2.cell(r, 7).hyperlink is not None, f"Missing hyperlink on Sheet 2 row {r}"
        rows_2.append(vals)

    # 4. Reconcile manifest counts 100%
    std_v6_cnt = sum(1 for row in rows_2 if row[2] in ("Standard", "Standard Only"))
    dh_extra_cnt = sum(1 for row in rows_2 if row[2] == "DH Edition Extra")

    assert len(rows_1) + ex_555 == raw_555, f"v5.5.5 reconciliation failed: {len(rows_1)} + {ex_555} != {raw_555}"
    assert std_v6_cnt + ex_v6_std == raw_v6_std, f"v6 std reconciliation failed: {std_v6_cnt} + {ex_v6_std} != {raw_v6_std}"
    assert len(rows_2) + ex_v6_dh == raw_v6_dh, f"v6 DH reconciliation failed: {len(rows_2)} + {ex_v6_dh} != {raw_v6_dh}"

    # 5. Cross-sheet consistency
    map_1 = {row[6]: row for row in rows_1}  # key by CurseForge URL (unique per project)
    map_2 = {row[6]: row for row in rows_2}
    shared_urls = set(map_1.keys()) & set(map_2.keys())
    for url in shared_urls:
        r1, r2 = map_1[url], map_2[url]
        assert r1[1] == r2[1], f"Category mismatch for {r1[0]}: {r1[1]} vs {r2[1]}"
        assert r1[2] == "Yes", f"Shared mod {r1[0]} must be Supported in 1.20.1 == Yes!"
        assert r1[3] == "Yes" and r2[3] == "Yes", f"Shared mod {r1[0]} missing In Both flag!"

    for url, r1 in map_1.items():
        if url not in shared_urls:
            assert r1[3] == "No", f"Non-shared v5.5.5 mod {r1[0]} incorrectly marked In Both == Yes"
    for url, r2 in map_2.items():
        if url not in shared_urls:
            assert r2[3] == "No", f"Non-shared v6 mod {r2[0]} incorrectly marked In Both == Yes"

    # 6. Verify Sheet 3 formulas & row alignment
    assert ws3["A10"].value == "Total Actual Mods"
    assert ws3["B10"].value == f"=COUNTA('v5.5.5 (MC 1.18.2)'!A4:A{ws1.max_row})"
    assert ws3["C10"].value == f"=COUNTA('Beta 5.10.17 (MC 1.20.1)'!A4:A{ws2.max_row})"
    assert ws3["A14"].value == "v5.5.5 Mods Supported on MC 1.20.1 (Forge)"
    assert ws3["B15"].value == "=B14/B10"

    # Verify every category row on Sheet 3 has exact formulas & sums match
    cat_1_cnt = Counter(r[1] for r in rows_1)
    cat_1_yes = Counter(r[1] for r in rows_1 if r[2] == "Yes")
    cat_1_no = Counter(r[1] for r in rows_1 if r[2] == "No")
    cat_1_both = Counter(r[1] for r in rows_1 if r[3] == "Yes")
    cat_2_cnt = Counter(r[1] for r in rows_2)

    assert ws3["A20"].value == "Mod Category"
    checked_cats = 0
    for rn in range(21, 38):
        cat = ws3.cell(rn, 1).value
        assert cat in cat_data["categories"], f"Unexpected category at row {rn}: {cat}"
        assert ws3.cell(rn, 2).value == f"=COUNTIF('v5.5.5 (MC 1.18.2)'!$B$4:$B${ws1.max_row},A{rn})"
        assert ws3.cell(rn, 3).value == f"=COUNTIFS('v5.5.5 (MC 1.18.2)'!$B$4:$B${ws1.max_row},A{rn},'v5.5.5 (MC 1.18.2)'!$C$4:$C${ws1.max_row},\"Yes\")"
        assert ws3.cell(rn, 4).value == f"=COUNTIFS('v5.5.5 (MC 1.18.2)'!$B$4:$B${ws1.max_row},A{rn},'v5.5.5 (MC 1.18.2)'!$C$4:$C${ws1.max_row},\"No\")"
        assert ws3.cell(rn, 5).value == f"=COUNTIF('Beta 5.10.17 (MC 1.20.1)'!$B$4:$B${ws2.max_row},A{rn})"
        assert ws3.cell(rn, 6).value == f"=COUNTIFS('v5.5.5 (MC 1.18.2)'!$B$4:$B${ws1.max_row},A{rn},'v5.5.5 (MC 1.18.2)'!$D$4:$D${ws1.max_row},\"Yes\")"
        assert ws3.cell(rn, 7).value == f"=E{rn}-B{rn}"
        assert cat_1_yes[cat] + cat_1_no[cat] == cat_1_cnt[cat]
        checked_cats += 1
    assert checked_cats == 17
    assert ws3["A38"].value == "TOTAL"
    assert ws3["B38"].value == "=SUM(B21:B37)"
    assert ws3["E38"].value == "=SUM(E21:E37)"

    # 7. AutoFilter & Freeze Panes checks
    assert ws1.freeze_panes == "A4" and ws1.auto_filter.ref == f"A3:G{ws1.max_row}"
    assert ws2.freeze_panes == "A4" and ws2.auto_filter.ref == f"A3:G{ws2.max_row}"
    assert ws3.freeze_panes == "A4"

    yes_1201 = sum(1 for r in rows_1 if r[2] == "Yes")
    no_1201 = sum(1 for r in rows_1 if r[2] == "No")
    print("=== ALL VERIFICATION CHECKS PASSED ===")
    print(f"  v5.5.5: {len(rows_1)} mods + {ex_555} non-mods = {raw_555} manifest entries (100% match)")
    print(f"    -> Supported on MC 1.20.1 (Forge): {yes_1201} ({yes_1201/len(rows_1)*100:.1f}%)")
    print(f"    -> NOT supported on MC 1.20.1 (Forge): {no_1201} ({no_1201/len(rows_1)*100:.1f}%)")
    print(f"  Beta 5.10.17 Standard: {std_v6_cnt} mods + {ex_v6_std} non-mods = {raw_v6_std} manifest entries (100% match)")
    print(f"  Beta 5.10.17 DH Edition: {len(rows_2)} mods ({dh_extra_cnt} DH extra) + {ex_v6_dh} non-mods = {raw_v6_dh} manifest entries (100% match)")
    print(f"  Shared mods across both packs: {len(shared_urls)} (100% identical categories & flags)")
    print(f"  Unique mods total: {len(set(map_1.keys()) | set(map_2.keys()))}")
    print(f"  Sheet 3 formulas verified: overview + 17 category rows + TOTAL row")


if __name__ == "__main__":
    main()
