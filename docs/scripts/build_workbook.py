#!/usr/bin/env python3
"""Build the 3-sheet DeceasedCraft_Mod_Research.xlsx workbook with styling,
AutoFilters, freeze panes, clickable URLs, conditional fills, and dynamic formulas."""

import json
import math
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

SCRATCH = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch")
OUT_XLSX = Path("/home/antigravity/DeceasedCraft_Mod_Research.xlsx")

# Color Palette (clean slate/steel theme)
FILL_TITLE = PatternFill("solid", fgColor="1E293B")       # Slate 800
FILL_SUBTITLE = PatternFill("solid", fgColor="334155")    # Slate 700
FILL_HEADER = PatternFill("solid", fgColor="0F172A")      # Slate 900
FILL_SECTION = PatternFill("solid", fgColor="1E3A5F")     # Deep Navy
FILL_ZEBRA = PatternFill("solid", fgColor="F8FAFC")       # Slate 50
FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
FILL_TOTAL = PatternFill("solid", fgColor="E2E8F0")       # Slate 200

FILL_YES = PatternFill("solid", fgColor="DCFCE7")         # Soft Green
FILL_NO = PatternFill("solid", fgColor="FEE2E2")          # Soft Red
FILL_BOTH_YES = PatternFill("solid", fgColor="E0F2FE")    # Soft Sky Blue
FILL_BOTH_NO = PatternFill("solid", fgColor="F1F5F9")     # Light Gray
FILL_DH_EXTRA = PatternFill("solid", fgColor="FEF3C7")    # Soft Amber
FILL_STD = PatternFill("solid", fgColor="F1F5F9")         # Light Gray

FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="E2E8F0")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_BODY = Font(name="Calibri", size=10, color="0F172A")
FONT_BODY_BOLD = Font(name="Calibri", size=10, bold=True, color="0F172A")
FONT_MONO = Font(name="Consolas", size=9, color="334155")
FONT_LINK = Font(name="Calibri", size=10, color="1D4ED8", underline="single")
FONT_YES = Font(name="Calibri", size=10, bold=True, color="166534")
FONT_NO = Font(name="Calibri", size=10, bold=True, color="991B1B")
FONT_BOTH_YES = Font(name="Calibri", size=10, bold=True, color="0369A1")
FONT_BOTH_NO = Font(name="Calibri", size=10, color="64748B")
FONT_DH_EXTRA = Font(name="Calibri", size=10, bold=True, color="92400E")
FONT_STD = Font(name="Calibri", size=10, color="334155")

THIN_BORDER_SIDE = Side(style="thin", color="CBD5E1")
MED_BOTTOM_SIDE = Side(style="medium", color="475569")
BORDER_CELL = Border(left=THIN_BORDER_SIDE, right=THIN_BORDER_SIDE, top=THIN_BORDER_SIDE, bottom=THIN_BORDER_SIDE)
BORDER_TOTAL = Border(left=THIN_BORDER_SIDE, right=THIN_BORDER_SIDE, top=MED_BOTTOM_SIDE, bottom=MED_BOTTOM_SIDE)

ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center", wrap_text=True)


def estimate_row_height(texts_and_widths: list[tuple[str, int]], min_h: float = 20.0) -> float:
    max_lines = 1
    for text, col_w in texts_and_widths:
        if not text:
            continue
        usable = max(col_w - 3, 10)
        lines = 0
        for part in str(text).split("\n"):
            lines += max(1, math.ceil(len(part) / usable))
        if lines > max_lines:
            max_lines = lines
    return max(min_h, max_lines * 14.5 + 6)


def style_banner(ws, max_col: int, title: str, subtitle: str):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)
    c1 = ws.cell(row=1, column=1, value=title)
    c1.font = FONT_TITLE
    c1.fill = FILL_TITLE
    c1.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28

    c2 = ws.cell(row=2, column=1, value=subtitle)
    c2.font = FONT_SUBTITLE
    c2.fill = FILL_SUBTITLE
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 20


def build_v555_sheet(wb: Workbook, mods_555: list[dict]) -> int:
    ws = wb.active
    ws.title = "v5.5.5 (MC 1.18.2)"
    ws.views.sheetView[0].showGridLines = True

    style_banner(
        ws,
        7,
        "DeceasedCraft v5.5.5 (Latest Stable) — Mod Catalog",
        "Minecraft 1.18.2 | Forge 40.2.4 | CurseForge File ID: 5525524 (Uploaded 2024-07-12) | 224 Mods (6 Resource/Shader Packs Excluded)",
    )

    headers = [
        "Mod Name",
        "Mod Category",
        "Supported in MC 1.20.1 (Forge)",
        "In Both Packs?",
        "Mod Version / File",
        "Short Description / Notes",
        "CurseForge / Source URL",
    ]
    col_widths = [34, 28, 22, 16, 40, 58, 42]
    for idx, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=3, column=idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CENTER if idx in (3, 4) else ALIGN_LEFT
        cell.border = BORDER_CELL
        ws.column_dimensions[get_column_letter(idx)].width = w
    ws.row_dimensions[3].height = 26

    for i, m in enumerate(mods_555, start=4):
        fill_row = FILL_ZEBRA if i % 2 == 1 else FILL_WHITE
        sup = "Yes" if m["supported_1201_forge"] else "No"
        both = "Yes" if m["in_both"] else "No"
        fname = m["file_555"] or ""
        notes = m["notes_555"] or ""
        url = m["url"] or ""

        vals = [m["title_clean"], m["category"], sup, both, fname, notes, url]
        for col_idx, val in enumerate(vals, 1):
            c = ws.cell(row=i, column=col_idx, value=val)
            c.border = BORDER_CELL
            if col_idx == 1:
                c.font = FONT_BODY_BOLD
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 2:
                c.font = FONT_BODY
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 3:
                c.font = FONT_YES if sup == "Yes" else FONT_NO
                c.fill = FILL_YES if sup == "Yes" else FILL_NO
                c.alignment = ALIGN_CENTER
            elif col_idx == 4:
                c.font = FONT_BOTH_YES if both == "Yes" else FONT_BOTH_NO
                c.fill = FILL_BOTH_YES if both == "Yes" else FILL_BOTH_NO
                c.alignment = ALIGN_CENTER
            elif col_idx == 5:
                c.font = FONT_MONO
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 6:
                c.font = FONT_BODY
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 7:
                c.font = FONT_LINK
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
                if url:
                    c.hyperlink = url

        ws.row_dimensions[i].height = estimate_row_height(
            [(m["title_clean"], col_widths[0]), (fname, col_widths[4]), (notes, col_widths[5])]
        )

    last_row = 3 + len(mods_555)
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:G{last_row}"
    return last_row


def build_v6_sheet(wb: Workbook, mods_v6: list[dict]) -> int:
    ws = wb.create_sheet("Beta 5.10.17 (MC 1.20.1)")
    ws.views.sheetView[0].showGridLines = True

    style_banner(
        ws,
        7,
        "DeceasedCraft Beta-5.10.17 (Latest Public v6 Beta) — Mod Catalog",
        "Minecraft 1.20.1 | Forge 47.4.0 | Standard File ID: 8448820 & DH Edition File ID: 8448903 (2026-07-17) | 306 Standard + 1 DH Extra = 307 Mods (11 Resource/Shader Packs Excluded)",
    )

    headers = [
        "Mod Name",
        "Mod Category",
        "Edition",
        "In Both Packs?",
        "Mod Version / File",
        "Short Description / Notes",
        "CurseForge / Source URL",
    ]
    col_widths = [34, 28, 20, 16, 42, 58, 42]
    for idx, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=3, column=idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CENTER if idx in (3, 4) else ALIGN_LEFT
        cell.border = BORDER_CELL
        ws.column_dimensions[get_column_letter(idx)].width = w
    ws.row_dimensions[3].height = 26

    for i, m in enumerate(mods_v6, start=4):
        fill_row = FILL_ZEBRA if i % 2 == 1 else FILL_WHITE
        edition = m["v6_edition"] or "Standard"
        both = "Yes" if m["in_both"] else "No"
        fname = m["file_v6"] or ""
        notes = m["notes_v6"] or ""
        url = m["url"] or ""

        vals = [m["title_clean"], m["category"], edition, both, fname, notes, url]
        for col_idx, val in enumerate(vals, 1):
            c = ws.cell(row=i, column=col_idx, value=val)
            c.border = BORDER_CELL
            if col_idx == 1:
                c.font = FONT_BODY_BOLD
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 2:
                c.font = FONT_BODY
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 3:
                is_dh = edition == "DH Edition Extra"
                c.font = FONT_DH_EXTRA if is_dh else FONT_STD
                c.fill = FILL_DH_EXTRA if is_dh else FILL_STD
                c.alignment = ALIGN_CENTER
            elif col_idx == 4:
                c.font = FONT_BOTH_YES if both == "Yes" else FONT_BOTH_NO
                c.fill = FILL_BOTH_YES if both == "Yes" else FILL_BOTH_NO
                c.alignment = ALIGN_CENTER
            elif col_idx == 5:
                c.font = FONT_MONO
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 6:
                c.font = FONT_BODY
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
            elif col_idx == 7:
                c.font = FONT_LINK
                c.fill = fill_row
                c.alignment = ALIGN_LEFT
                if url:
                    c.hyperlink = url

        ws.row_dimensions[i].height = estimate_row_height(
            [(m["title_clean"], col_widths[0]), (fname, col_widths[4]), (notes, col_widths[5])]
        )

    last_row = 3 + len(mods_v6)
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:G{last_row}"
    return last_row


def build_summary_sheet(wb: Workbook, categories: list[str], last_555: int, last_v6: int, excluded_non_mods: list[dict]):
    ws = wb.create_sheet("Comparison & Mod-Dev Summary")
    ws.views.sheetView[0].showGridLines = True

    s1 = "'v5.5.5 (MC 1.18.2)'"
    s2 = "'Beta 5.10.17 (MC 1.20.1)'"

    col_widths = [34, 24, 24, 24, 22, 18, 20]
    for idx, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = w

    style_banner(
        ws,
        7,
        "DeceasedCraft Cross-Version Comparison & Dual-Version Mod Development Guide",
        "Targeting Simultaneous Compatibility with DeceasedCraft v5.5.5 (MC 1.18.2 Forge) & Latest Public v6 Open Beta 5.10.17 (MC 1.20.1 Forge)",
    )

    # --- SECTION 1: PACK OVERVIEW ---
    r = 4
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    sec1 = ws.cell(row=r, column=1, value="1. Modpack Metadata & Mod Count Summary (Dynamic Formulas)")
    sec1.font = FONT_SECTION
    sec1.fill = FILL_SECTION
    sec1.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r].height = 24

    r = 5
    ov_headers = ["Metric", "v5.5.5 (Latest Stable)", "Beta 5.10.17 (Latest Public v6)", "Notes / Context"]
    ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
    for col_idx, h in enumerate(ov_headers, 1):
        c = ws.cell(row=r, column=col_idx, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER if col_idx in (2, 3) else ALIGN_LEFT
        c.border = BORDER_CELL
    for col_idx in range(5, 8):
        ws.cell(row=r, column=col_idx).border = BORDER_CELL
        ws.cell(row=r, column=col_idx).fill = FILL_HEADER
    ws.row_dimensions[r].height = 24

    ex_555 = sum(1 for x in excluded_non_mods if x["in_555"])
    ex_v6 = sum(1 for x in excluded_non_mods if x["in_v6_std"] or x["in_v6_dh"])

    overview_rows = [
        ("CurseForge File ID", "5525524", "8448820 (DH: 8448903)", "CurseForge Project ID 490660 (v5.11 is Patreon-only)", None),
        ("Release Date", "2024-07-12", "2026-07-17", "Latest public stable vs. latest public v6 open beta", None),
        ("Minecraft Version", "1.18.2", "1.20.1", "Both run on Java 17 (LTS)", None),
        ("Mod Loader & Version", "Forge 40.2.4", "Forge 47.4.0", "Pure Forge on 1.18.2; Forge + Sinytra Connector on 1.20.1", None),
        ("Total Actual Mods", f"=COUNTA({s1}!A4:A{last_555})", f"=COUNTA({s2}!A4:A{last_v6})", "Mods only (excludes resource packs & shaders)", "#,##0"),
        ("Standard Edition Mods", f"=B10", f'=COUNTIF({s2}!C4:C{last_v6},"Standard")', "Mods in the main Standard edition archive", "#,##0"),
        ("DH Edition Extra Mods", 0, f'=COUNTIF({s2}!C4:C{last_v6},"DH Edition Extra")', "Distant Horizons (508933) is the sole DH Edition addition", "#,##0"),
        ("Mods Present in Both Packs (Shared)", f'=COUNTIF({s1}!D4:D{last_555},"Yes")', f'=COUNTIF({s2}!D4:D{last_v6},"Yes")', "Exact same CurseForge project present in both versions", "#,##0"),
        ("v5.5.5 Mods Supported on MC 1.20.1 (Forge)", f'=COUNTIF({s1}!C4:C{last_555},"Yes")', "N/A", "Verified across CurseForge + Modrinth + GitHub", "#,##0"),
        ("v5.5.5 -> MC 1.20.1 Support Rate (%)", "=B14/B10", "N/A", "High ecosystem continuity between 1.18.2 and 1.20.1 Forge", "0.0%"),
        ("v5.5.5 Mods NOT Supported on MC 1.20.1 (Forge)", f'=COUNTIF({s1}!C4:C{last_555},"No")', "N/A", "Legacy/discontinued/merged mods (see Notes on Sheet 1)", "#,##0"),
        ("Excluded Non-Mods (Resource Packs & Shaders)", ex_555, ex_v6, "Excluded from mod sheets; reconciles manifest totals (230 / 318)", "#,##0"),
    ]

    for offset, (metric, v1, v2, note, num_fmt) in enumerate(overview_rows):
        row_num = 6 + offset
        fill_r = FILL_ZEBRA if row_num % 2 == 1 else FILL_WHITE
        ws.merge_cells(start_row=row_num, start_column=4, end_row=row_num, end_column=7)
        c1 = ws.cell(row=row_num, column=1, value=metric)
        c2 = ws.cell(row=row_num, column=2, value=v1)
        c3 = ws.cell(row=row_num, column=3, value=v2)
        c4 = ws.cell(row=row_num, column=4, value=note)

        c1.font = FONT_BODY_BOLD
        c2.font = FONT_BODY_BOLD if str(v1).startswith("=") else FONT_BODY
        c3.font = FONT_BODY_BOLD if str(v2).startswith("=") else FONT_BODY
        c4.font = FONT_BODY
        c1.alignment = ALIGN_LEFT
        c2.alignment = ALIGN_CENTER
        c3.alignment = ALIGN_CENTER
        c4.alignment = ALIGN_LEFT

        if num_fmt:
            if isinstance(v1, (int, float)) or str(v1).startswith("="):
                c2.number_format = num_fmt
            if isinstance(v2, (int, float)) or str(v2).startswith("="):
                c3.number_format = num_fmt

        for col_idx in range(1, 8):
            cell = ws.cell(row=row_num, column=col_idx)
            cell.fill = fill_r
            cell.border = BORDER_CELL
        ws.row_dimensions[row_num].height = 20

    # --- SECTION 2: CATEGORY BREAKDOWN ---
    r = 19
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    sec2 = ws.cell(row=r, column=1, value="2. Category Breakdown Across Versions (Dynamic Formulas)")
    sec2.font = FONT_SECTION
    sec2.fill = FILL_SECTION
    sec2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r].height = 24

    r = 20
    cat_headers = [
        "Mod Category",
        "v5.5.5 Mods",
        "v5.5.5 Supported in 1.20.1",
        "v5.5.5 NOT in 1.20.1",
        "Beta 5.10.17 Mods",
        "Shared in Both",
        "Net Change (v6 - v5.5.5)",
    ]
    for col_idx, h in enumerate(cat_headers, 1):
        c = ws.cell(row=r, column=col_idx, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_LEFT if col_idx == 1 else ALIGN_CENTER
        c.border = BORDER_CELL
    ws.row_dimensions[r].height = 26

    cat_start_row = 21
    sorted_cats = sorted(categories)
    for idx, cat in enumerate(sorted_cats):
        rn = cat_start_row + idx
        fill_r = FILL_ZEBRA if rn % 2 == 1 else FILL_WHITE
        vals = [
            cat,
            f'=COUNTIF({s1}!$B$4:$B${last_555},A{rn})',
            f'=COUNTIFS({s1}!$B$4:$B${last_555},A{rn},{s1}!$C$4:$C${last_555},"Yes")',
            f'=COUNTIFS({s1}!$B$4:$B${last_555},A{rn},{s1}!$C$4:$C${last_555},"No")',
            f'=COUNTIF({s2}!$B$4:$B${last_v6},A{rn})',
            f'=COUNTIFS({s1}!$B$4:$B${last_555},A{rn},{s1}!$D$4:$D${last_555},"Yes")',
            f'=E{rn}-B{rn}',
        ]
        for col_idx, val in enumerate(vals, 1):
            c = ws.cell(row=rn, column=col_idx, value=val)
            c.border = BORDER_CELL
            c.fill = fill_r
            c.font = FONT_BODY_BOLD if col_idx == 1 else FONT_BODY
            c.alignment = ALIGN_LEFT if col_idx == 1 else ALIGN_CENTER
            if col_idx >= 2:
                c.number_format = "+#,##0;-#,##0;0" if col_idx == 7 else "#,##0"
        ws.row_dimensions[rn].height = 20

    cat_end_row = cat_start_row + len(sorted_cats) - 1
    tot_row = cat_end_row + 1
    tot_vals = [
        "TOTAL",
        f"=SUM(B{cat_start_row}:B{cat_end_row})",
        f"=SUM(C{cat_start_row}:C{cat_end_row})",
        f"=SUM(D{cat_start_row}:D{cat_end_row})",
        f"=SUM(E{cat_start_row}:E{cat_end_row})",
        f"=SUM(F{cat_start_row}:F{cat_end_row})",
        f"=SUM(G{cat_start_row}:G{cat_end_row})",
    ]
    for col_idx, val in enumerate(tot_vals, 1):
        c = ws.cell(row=tot_row, column=col_idx, value=val)
        c.font = FONT_BODY_BOLD
        c.fill = FILL_TOTAL
        c.border = BORDER_TOTAL
        c.alignment = ALIGN_LEFT if col_idx == 1 else ALIGN_CENTER
        if col_idx >= 2:
            c.number_format = "+#,##0;-#,##0;0" if col_idx == 7 else "#,##0"
    ws.row_dimensions[tot_row].height = 22

    # --- SECTION 3: DUAL-VERSION MOD DEVELOPMENT ARCHITECTURE GUIDE ---
    r = tot_row + 2
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    sec3 = ws.cell(row=r, column=1, value="3. Dual-Version Mod Development Guide (MC 1.18.2 Forge + MC 1.20.1 Forge)")
    sec3.font = FONT_SECTION
    sec3.fill = FILL_SECTION
    sec3.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r].height = 24

    r += 1
    dev_headers = [
        ("System / Domain", 1, 1),
        ("v5.5.5 (1.18.2 Forge)", 2, 2),
        ("Beta 5.10.17 (1.20.1 Forge)", 3, 3),
        ("Mod-Development Implications for Dual-Version Compatibility", 4, 7),
    ]
    for label, c_start, c_end in dev_headers:
        if c_end > c_start:
            ws.merge_cells(start_row=r, start_column=c_start, end_row=r, end_column=c_end)
        c = ws.cell(row=r, column=c_start, value=label)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_LEFT
        for ci in range(c_start, c_end + 1):
            ws.cell(row=r, column=ci).border = BORDER_CELL
            ws.cell(row=r, column=ci).fill = FILL_HEADER
    ws.row_dimensions[r].height = 24

    dev_rows = [
        (
            "Toolchain & Loader",
            "MC 1.18.2 | Forge 40.2.4 | Java 17",
            "MC 1.20.1 | Forge 47.4.0 | Java 17 (+ Sinytra Connector)",
            "Use a multi-version Forge setup (e.g., Stonecutter or shared common core + thin 1.18.2/1.20.1 Forge adapter modules). Key MC API deltas: ForgeRegistries/CreativeModeTab registration, GuiGraphics (1.20.1) vs PoseStack (1.18.2), Component.literal() vs new TextComponent(), and Biome/Tag changes.",
        ),
        (
            "Survival / Health / Thirst / Temp",
            "First Aid + Thirst Was Taken + Cold Sweat",
            "Legendary Survival Overhaul (all-in-one)",
            "CRITICAL DIVERGENCE: Do NOT hard-depend on First Aid, Thirst Was Taken, Cold Sweat, or LSO. If your mod interacts with limb health, thirst, temperature, or healing, expose an internal SurvivalBridge interface with optional runtime detection (ModList.get().isLoaded(...)) for both stacks.",
        ),
        (
            "Firearms & Combat",
            "Timeless and Classics Guns (TaC) + MrCrayfish's Gun Mod; Better Combat, Apocalypse Now, Create Big Cannons, ParCool!",
            "[TaCZ] Timeless and Classics Zero (+ Tweaks/Durability/Shots Fired) + MrCrayfish Unofficial; Better Combat, Apocalypse Now, Create Big Cannons, ParCool!",
            "CRITICAL DIVERGENCE: TaC (1.18.2) and TaCZ (1.20.1) have completely different APIs/data formats (TaCZ is data-driven gun packs). Interact via standard Forge DamageSource/LivingHurtEvent/tags when possible, or isolate gun-specific hooks behind optional compat modules.",
        ),
        (
            "Zombies, Hordes & AI",
            "The Hordes, THE UNDEAD REVAMPED, Zombie Awareness, Zombie Extreme, Enhanced AI, Enhanced Hordes, Mob Sunscreen, Lost Souls, Mutationcraft, NoCube's",
            "Same 8 core zombie/AI mods + Fungal Infection: Spore, Voiceless Survival (dropped Mutationcraft & NoCube's)",
            "HIGH CONTINUITY: Target vanilla Zombie/Monster tags, entity type tags, and Forge LivingEvent/EntityJoinLevelEvent. Core DeceasedCraft zombie mods exist on both versions, making mob/horde hooks cleanly portable.",
        ),
        (
            "Worldgen, Cities & Loot",
            "The Lost Cities, Biomes O' Plenty, TerraBlender, Lootr, Structure Essentials, Ore Tweaker",
            "The Lost Cities, Lost Worlds LC, Lost Radar, Biomes O' Plenty, TerraBlender, Lootr, Biome Replacer/Sizes",
            "HIGH CONTINUITY: The Lost Cities & Lootr power both packs. For custom loot, use Forge Global Loot Modifiers (GLMs) or Loot Table injection so Lootr automatically instances your loot chests in multiplayer on both versions.",
        ),
        (
            "Tech, Power & Automation",
            "Create (+5 addons), Immersive Engineering, Immersive Petroleum, Refined Storage, Pipez, Security Craft",
            "Create (+8 addons incl. Diesel Generators), Immersive Engineering, Extreme Reactors, Refined Storage (+Addons), Pipez, Security Craft",
            "HIGH CONTINUITY: Forge Energy (FE), FluidCapability, and IItemHandler work seamlessly with Create, Immersive Engineering, Pipez, and Refined Storage across both 1.18.2 and 1.20.1.",
        ),
        (
            "Vehicles & Transport",
            "Ultimate Car Mod, Simple Planes",
            "DragN's Valiant Vehicles! (+ Refueled), Simple Planes, Immersive Aircraft",
            "Only Simple Planes is shared; ground vehicles switched from Ultimate Car Mod to DragN's Valiant Vehicles!. Avoid hard dependencies on vehicle mods.",
        ),
        (
            "Quests, Skills & Accessories",
            "FTB Quests, FTB Teams, Pufferfish's Skills, Curios API, Artifacts, Nameless Trinkets",
            "FTB Quests, FTB Teams, Pufferfish's Skills, Pufferfish's Attributes, Curios API, CustomNPCs-Unofficial, Artifacts, Nameless & Fancy Trinkets",
            "HIGH CONTINUITY: Curios API is present in both versions (safe optional/required dependency for wearable gear). Standard Forge item/advancement/entity events integrate cleanly with FTB Quests and Pufferfish's Skills.",
        ),
        (
            "Pack Scripting & Config",
            "KubeJS + CraftTweaker + ContentTweaker + In Control! + Fx Control!",
            "KubeJS (+ KubeJS Create, EntityJS) + In Control! (CraftTweaker & Fx Control! removed)",
            "Use standard Minecraft datapacks, tags, JSON recipes, and Forge Config/Events (plus KubeJS compatibility if exposing script hooks). Do NOT rely on CraftTweaker/ZenScript since v6 dropped it.",
        ),
        (
            "Safe Shared Library APIs",
            "Curios, GeckoLib, Architectury, Cloth Config, Moonlight Lib, Patchouli, Bookshelf, playerAnimator, JEI, The One Probe, Xaero's World Map, Open Parties and Claims",
            "All 12 shared libraries remain in Beta 5.10.17 (note: GeckoLib 3 in 1.18.2 -> GeckoLib 4 in 1.20.1; AutoRegLib -> Zeta)",
            "Prefer zero-dependency Forge APIs where possible. If you need 3D animations or config GUIs, GeckoLib / Cloth Config / Curios / JEI / Patchouli are available in both packs (account for GeckoLib 3 -> 4 API refactor).",
        ),
        (
            "Rendering, Shaders & DH",
            "Embeddium, Oculus, Iris & Oculus Flywheel Compat, [ETF]",
            "Embeddium, Oculus, Colorwheel, Vanillin, ImmediatelyFast, [EMF], [ETF] + Distant Horizons (DH Edition)",
            "Avoid invasive vanilla renderer mixins that conflict with Embeddium/Oculus/ImmediatelyFast/Colorwheel. Keep custom block/entity renderers standard Forge/GeckoLib so shaders & Distant Horizons LODs render cleanly.",
        ),
        (
            "Custom Pack Patch Mods",
            "DCFixes (Bawnorton)",
            "DeceasedCraft++ (Bogdan_Off), DCTweaks (plus upcoming DeceasedCraft v6 Fixes on GitHub)",
            "Watch for overlapping mixins/tag overrides with DCFixes (v5.5.5) and DeceasedCraft++ / DCTweaks (v6) — especially around health sync, Hordes spawns, TaCZ, and Immersive/Create configs.",
        ),
    ]

    for idx, (domain, v5_txt, v6_txt, impl_txt) in enumerate(dev_rows):
        rn = r + 1 + idx
        fill_r = FILL_ZEBRA if rn % 2 == 1 else FILL_WHITE
        ws.merge_cells(start_row=rn, start_column=4, end_row=rn, end_column=7)
        c1 = ws.cell(row=rn, column=1, value=domain)
        c2 = ws.cell(row=rn, column=2, value=v5_txt)
        c3 = ws.cell(row=rn, column=3, value=v6_txt)
        c4 = ws.cell(row=rn, column=4, value=impl_txt)
        c1.font = FONT_BODY_BOLD
        c2.font = FONT_BODY
        c3.font = FONT_BODY
        c4.font = FONT_BODY
        for ci in range(1, 8):
            cell = ws.cell(row=rn, column=ci)
            cell.fill = fill_r
            cell.border = BORDER_CELL
            cell.alignment = ALIGN_LEFT

        merged_w = sum(col_widths[3:7])
        ws.row_dimensions[rn].height = estimate_row_height(
            [(domain, col_widths[0]), (v5_txt, col_widths[1]), (v6_txt, col_widths[2]), (impl_txt, merged_w)],
            min_h=28.0,
        )

    # --- SECTION 4: EXCLUDED NON-MODS AUDIT LOG ---
    r_ex = r + 1 + len(dev_rows) + 2
    ws.merge_cells(start_row=r_ex, start_column=1, end_row=r_ex, end_column=7)
    sec4 = ws.cell(row=r_ex, column=1, value="4. Excluded Non-Mods Audit Log (Resource Packs & Shaders Omitted from Mod Sheets)")
    sec4.font = FONT_SECTION
    sec4.fill = FILL_SECTION
    sec4.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r_ex].height = 24

    r_ex += 1
    ex_headers = [
        ("Item Name", 1, 1),
        ("Type", 2, 2),
        ("In v5.5.5?", 3, 3),
        ("In Beta 5.10.17?", 4, 4),
        ("CurseForge URL", 5, 7),
    ]
    for label, c_start, c_end in ex_headers:
        if c_end > c_start:
            ws.merge_cells(start_row=r_ex, start_column=c_start, end_row=r_ex, end_column=c_end)
        c = ws.cell(row=r_ex, column=c_start, value=label)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER if c_start in (2, 3, 4) else ALIGN_LEFT
        for ci in range(c_start, c_end + 1):
            ws.cell(row=r_ex, column=ci).border = BORDER_CELL
            ws.cell(row=r_ex, column=ci).fill = FILL_HEADER
    ws.row_dimensions[r_ex].height = 22

    for idx, nm in enumerate(sorted(excluded_non_mods, key=lambda x: (x["type"], x["title"].lower()))):
        rn = r_ex + 1 + idx
        fill_r = FILL_ZEBRA if rn % 2 == 1 else FILL_WHITE
        ws.merge_cells(start_row=rn, start_column=5, end_row=rn, end_column=7)
        c1 = ws.cell(row=rn, column=1, value=nm["title"])
        c2 = ws.cell(row=rn, column=2, value=nm["type"])
        c3 = ws.cell(row=rn, column=3, value="Yes" if nm["in_555"] else "No")
        c4 = ws.cell(row=rn, column=4, value="Yes" if (nm["in_v6_std"] or nm["in_v6_dh"]) else "No")
        c5 = ws.cell(row=rn, column=5, value=nm["url"])
        c1.font = FONT_BODY
        c2.font = FONT_BODY
        c3.font = FONT_BODY
        c4.font = FONT_BODY
        c5.font = FONT_LINK
        if nm["url"]:
            c5.hyperlink = nm["url"]
        c1.alignment = ALIGN_LEFT
        c2.alignment = ALIGN_CENTER
        c3.alignment = ALIGN_CENTER
        c4.alignment = ALIGN_CENTER
        c5.alignment = ALIGN_LEFT
        for ci in range(1, 8):
            ws.cell(row=rn, column=ci).fill = fill_r
            ws.cell(row=rn, column=ci).border = BORDER_CELL
        ws.row_dimensions[rn].height = 20

    ws.freeze_panes = "A4"


def main():
    data = json.loads((SCRATCH / "categorized_mods.json").read_text(encoding="utf-8"))
    mods = data["mods"]
    categories = data["categories"]
    excluded_non_mods = data["excluded_non_mods"]

    mods_555 = sorted(
        [m for m in mods.values() if m["in_555"]],
        key=lambda m: (m["category"].lower(), m["title_clean"].lower()),
    )
    mods_v6 = sorted(
        [m for m in mods.values() if m["in_v6"]],
        key=lambda m: (m["category"].lower(), m["title_clean"].lower()),
    )

    wb = Workbook()
    last_555 = build_v555_sheet(wb, mods_555)
    last_v6 = build_v6_sheet(wb, mods_v6)
    build_summary_sheet(wb, categories, last_555, last_v6, excluded_non_mods)

    wb.save(OUT_XLSX)
    print(f"Generated {OUT_XLSX} ({OUT_XLSX.stat().st_size / 1024:.1f} KB)")
    print(f"  Sheet 1 ('v5.5.5 (MC 1.18.2)'): {len(mods_555)} rows (rows 4..{last_555})")
    print(f"  Sheet 2 ('Beta 5.10.17 (MC 1.20.1)'): {len(mods_v6)} rows (rows 4..{last_v6})")
    print(f"  Sheet 3 ('Comparison & Mod-Dev Summary'): summary + {len(categories)} categories + 12 mod-dev guidelines + {len(excluded_non_mods)} excluded non-mods")


if __name__ == "__main__":
    main()
