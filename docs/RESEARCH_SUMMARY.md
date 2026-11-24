# Walkthrough: DeceasedCraft v5.5.5 vs. Beta 5.10.17 Mod Research

## Deliverable

- **Excel Workbook**: [DeceasedCraft_Mod_Research.xlsx](file:///home/antigravity/DeceasedCraft_Mod_Research.xlsx) (`77.9 KB`)
- **Reproducible Research Pipeline** (stored in scratch):
  - [extract_and_research.py](file:///home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch/extract_and_research.py)
  - [verify_compat.py](file:///home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch/verify_compat.py)
  - [categorize_mods.py](file:///home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch/categorize_mods.py)
  - [build_workbook.py](file:///home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch/build_workbook.py)
  - [verify_workbook.py](file:///home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch/verify_workbook.py)

---

## Workbook Structure (3 Sheets)

1. **`v5.5.5 (MC 1.18.2)`** — All **224** mods from `DeceasedCraft-5.5.5.zip` (File ID `5525524`, `Forge 40.2.4`).
   - Columns: `Mod Name`, `Mod Category`, `Supported in MC 1.20.1 (Forge)` (`Yes`/`No`), `In Both Packs?`, `Mod Version / File`, `Short Description / Notes`, `CurseForge / Source URL`.
2. **`Beta 5.10.17 (MC 1.20.1)`** — All **307** mods from `DeceasedCraft_Beta-5.10.17.zip` (File ID `8448820`, `Forge 47.4.0`, `306` Standard mods) + `DeceasedCraft_Beta_DH_Edition-5.10.17.zip` (File ID `8448903`, adding **1** DH Edition extra: `Distant Horizons`).
   - Columns: `Mod Name`, `Mod Category`, `Edition` (`Standard` / `DH Edition Extra`), `In Both Packs?`, `Mod Version / File`, `Short Description / Notes`, `CurseForge / Source URL`.
3. **`Comparison & Mod-Dev Summary`** — Dynamic Excel formula tables (`COUNTA`, `COUNTIF`, `COUNTIFS`, `SUM`) covering pack metadata, category breakdown, a 12-domain **Dual-Version Mod Development Guide** (`MC 1.18.2 Forge` + `MC 1.20.1 Forge`), and the full audit log of the 15 excluded non-mod files (9 Resource Packs + 6 Shaders).

---

## Key Research Findings

### Pack Totals & Reconciliation
| Metric | v5.5.5 (MC 1.18.2) | Beta 5.10.17 (MC 1.20.1) |
| --- | :---: | :---: |
| **CurseForge File ID** | `5525524` | `8448820` (DH: `8448903`) |
| **Forge Loader** | `forge-40.2.4` | `forge-47.4.0` |
| **Total Actual Mods** | **224** | **307** (`306` Standard + `1` DH Extra) |
| **Excluded Non-Mods (Resource/Shader Packs)** | 6 | 11 |
| **Manifest Total (100% Reconciled)** | **230** | **317** Standard / **318** DH |
| **Mods Shared in Both Packs** | **151** | **151** |
| **v5.5.5 Supported on MC 1.20.1 (Forge)** | **207 (92.4%)** | — |
| **v5.5.5 NOT Supported on MC 1.20.1 (Forge)** | **17 (7.6%)** | — |

### Unified 17-Category Breakdown (`380` Unique Mods)
| Mod Category | v5.5.5 | v6 Beta (+DH) | Unique |
| --- | :---: | :---: | :---: |
| Core Libraries & APIs | 35 | 56 | 60 |
| Performance & Optimization | 24 | 35 | 42 |
| UI, HUD, Maps & Info | 20 | 29 | 35 |
| Audio, Visuals & Immersion | 16 | 22 | 31 |
| Bug Fixes & Stability | 12 | 21 | 28 |
| Building, Furniture & Decor | 10 | 21 | 23 |
| Firearms, Weapons & Combat | 13 | 18 | 22 |
| Multiplayer, Utility & Admin | 16 | 18 | 22 |
| Zombies, Mobs & Wildlife | 15 | 13 | 19 |
| Tech, Automation & Power | 9 | 15 | 17 |
| Worldgen, Cities & Structures | 9 | 10 | 14 |
| Food, Farming & Cooking | 9 | 12 | 14 |
| Quests, Progression & NPCs | 8 | 10 | 14 |
| Modpack Scripting & Control | 10 | 9 | 14 |
| Storage, Loot & Backpacks | 8 | 11 | 11 |
| Survival, Health & Environment | 8 | 3 | 9 |
| Vehicles & Transport | 2 | 4 | 5 |
| **TOTAL** | **224** | **307** | **380** |

### The 17 `v5.5.5` Mods Without Official `MC 1.20.1 (Forge)` Releases
Every single `No` entry was audited across CFWidget, live paginated CurseForge API, Modrinth API, and GitHub/web search:
1. **AutoRegLib** — Replaced by `Zeta` in `1.20.1` (Quark library).
2. **ContentTweaker** — Stopped at `1.19.2`; `v6` uses `KubeJS` exclusively.
3. **DCFixes** — No public `1.20.1` JAR release (a source-only `DeceasedCraft v6 Fixes` branch exists on GitHub `Bawnorton/DCFixes`); `Beta 5.10.17` uses `DeceasedCraft++` & `DCTweaks`.
4. **Dietary Statistics** — Stopped at `1.19.4`.
5. **Effective (Forge)** — Stopped at `1.19.2`; replaced by `Particular ✨ Reforged` & `Pretty Rain` in `v6`.
6. **Entity Collision FPS Fix** — Stopped at `1.19.2`.
7. **Fx Control!** — Merged directly into `In Control!` starting in `1.20.1+`.
8. **Lazy DataFixerUpper (LazyDFU) [FORGE]** — Stopped at `1.19.3` (obsoleted by vanilla `1.19.4+`).
9. **Lightspeed - Launch optimizations** — Original discontinued after `1.19.2` (unofficial `1.20.1` port `LightSpeedRe` exists; `v6` uses `FastBoot` & `lazyyyyy`).
10. **MrCrayfish's Gun Mod** — Official stopped at `1.19.4`; `v6` uses `MrCrayfish's Gun Mod [Unofficial]`.
11. **NoCube's Zombie Mobs** — Stopped at `1.19.2`.
12. **Ore Tweaker** — Stopped at `1.18.2`.
13. **Pluto** — Stopped at `1.19.3`.
14. **Shutup Experimental Settings!** — Stopped at `1.19.2`; replaced by `Yeetus Experimentus` in `v6`.
15. **SwingThroughGrass** — Original project skipped `1.20.1` (`1.19.2` -> `1.20.6`); separate rewrite exists.
16. **Timeless and Classics Guns** — Stopped at `1.18.2`; replaced by `[TaCZ] Timeless and Classics Zero Guns` in `v6`.
17. **True Darkness** — Original stopped at `1.19.3`.

---

## Verification Results

Ran `verify_workbook.py` against [DeceasedCraft_Mod_Research.xlsx](file:///home/antigravity/DeceasedCraft_Mod_Research.xlsx):
- **Manifest Reconciliation**: 100% exact match across all three official CurseForge archives (`224 + 6 = 230`, `306 + 11 = 317`, `307 + 11 = 318`; zero hidden JARs in `overrides/`).
- **Schema & Hyperlinks**: Zero blank required cells, zero invisible Unicode characters (cleaned zero-width space from `Sounds`), valid `Yes`/`No` and `Edition` values, and clickable `https://` hyperlinks on all `531` data rows.
- **Cross-Sheet Consistency**: All `151` shared mods match identically on `Mod Category`, `In Both Packs? == "Yes"`, and `Supported in MC 1.20.1 (Forge) == "Yes"`.
- **Formula Audit**: All dynamic formulas on `Comparison & Mod-Dev Summary` verified for exact range alignment and totals.
