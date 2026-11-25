# Create: Tactical ChemThrowers

An original, Minecraft-EULA-compliant Forge mod (`modid: tacticalchemthrowers`) adding a heavy tactical, Create-styled modular handheld ChemThrower, pressurized multi-fuel canister logistics, and an automated Create-integrated Kinetic ChemThrower Turret—engineered natively for **DeceasedCraft**.

[![MC 1.18.2](https://img.shields.io/badge/Minecraft-1.18.2%20%7C%20Forge%2040.2.4-orange)](compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv)
[![MC 1.20.1](https://img.shields.io/badge/Minecraft-1.20.1%20%7C%20Forge%2047.4.0-blue)](compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv)
[![Mod ID](https://img.shields.io/badge/modid-tacticalchemthrowers-darkred)](SPECS.md)

---

## Supported DeceasedCraft Targets

| DeceasedCraft Release | Minecraft | Forge | CurseForge File ID(s) | Verified Mod Inventory |
| --- | :---: | :---: | --- | --- |
| **DeceasedCraft `v5.5.5`** *(Legacy Stable)* | `1.18.2` | `40.2.4` | `5525524` | **224 mods** (+6 packs) — [CSV Inventory](compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv) |
| **DeceasedCraft `Beta-5.10.17`** *(v6 Open Beta)* | `1.20.1` | `47.4.0` | Standard: `8448820`<br>DH Edition: `8448903` | **306 Standard** (+1 `Distant Horizons` = 307 mods, +11 packs) — [CSV Inventory](compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv) |

---

## Core Design Highlights

- **Heavy Tactical + Create Mod Aesthetic:** Bulky military-industrial silhouette (perforated heat-shielded barrel, underslung canister cradle, armored gimbal) crafted in Create's signature riveted andesite-iron, copper pressure pipes, brass valves, and mechanical pressure dials.
- **Modular Handheld ChemThrower (`15 → 25 → 35` Blocks):** One core weapon upgraded via swappable nozzle/pressure modules with visible barrel transformations, `+10%`/hit heat ramp (up to `2.0x`, `2.5s` reset), `≤ 4` block point-blank lava-like bonus damage + `3s` burn, Heavy Braced Creep stance (`~15%` walk speed, no sprint/jump), and pure 1st-person gun + hands recoil with zero camera pitch kick.
- **Canister-Only Multi-Fuel Logistics (Zero Duplicate Fluids):** `50 units = 1,000 mB` (`4 mB/tick` = `12.5s` continuous fire). Reloads strictly by swapping `IFluidHandlerItem` Pressurized Fuel Canisters (`R` or `Sneak+Right-Click`, `1.5s`, returns spent canister), fillable via Create Spouts/Tanks/Pipes and Immersive Engineering Bottling Machines/Tanks. Data-driven `flamethrower_fuels/*.json` bridges `Immersive Petroleum` (`v5.5.5`), `Create: Diesel Generators` (`Beta-5.10.17`), `Immersive Engineering`, and `Create Crafts & Additions` natively while coexisting alongside IE's Chemthrower.
- **Crisp Blocky 4-Stage Combustion VFX & Shaders:** Pixel-native blocky billboard particles (`0.18–0.55b`) transitioning from white-yellow pressurized core → roaring orange/amber flame + sparks → cooling crimson ember → rising dark/black hydrocarbon smoke, paired with `FULL_BRIGHT` emissivity, LabPBR `_s` maps, dynamic lighting (`Lucent` / `Sodium Dynamic Lights`), and Oculus shader validation (**BSL, Complementary Reimagined/Unbound + Euphoria, Photon, Bliss, Spooklementary**).
- **Automated Kinetic ChemThrower Turret:** Fixed industrial ports (**Left** = Create Shaft RPM/SU slew, **Right** = Forge Energy, **Back + Bottom** = Create Fluid Pipe), right-click configuration GUI, Create Wrench support, and Engineer's Goggles live telemetry.
- **Native DeceasedCraft Progression & Soft Hooks:** Mid-to-late Create Mechanical Crafting + IE Steel/Brass + Lootr-safe Lost Cities military/lab GLMs, plus soft optional hooks for `Open Parties & Claims`, `FTB Teams`, `Zombie Awareness`, `Cold Sweat` (`v5.5.5`), and `Legendary Survival Overhaul` (`Beta-5.10.17`).

---

## Repository Navigation

### Core Specification & Agent Guidelines
- **[SPECS.md](SPECS.md)** — Authoritative unified engineering specification, gameplay contract, architecture, and release gates.
- **[AGENTS.md](AGENTS.md)** — Engineering handbook, dual-version adapter boundaries, EULA guardrails, and asset workflow for AI coding agents.
- **[docs/LOCAL_EXECUTION_PROMPT.md](docs/LOCAL_EXECUTION_PROMPT.md)** — Optimal Antigravity configuration (`Orchestrator (Neon)` + `/teamwork`) plus two ready-to-paste prompts: **Prompt 1** (workspace-only skill/plugin cleanup, npm tools & project skill loader) and **Prompt 2** (full Phases 2–6 build).

### Archive-Verified Compatibility & Integration Audits (`compatibility/`)
- **[ECOSYSTEM_MATRIX.md](compatibility/ECOSYSTEM_MATRIX.md)** — Official CurseForge archive SHA-256 hashes and cross-version mod ecosystem matrix.
- **[RECIPE_AND_FLUID_AUDIT.md](compatibility/RECIPE_AND_FLUID_AUDIT.md)** — Pack-extracted fluid tags/IDs, `Beta-5.10.17` KubeJS `material.js` overrides, IE Chemthrower audit, and multi-fuel JSON profiles.
- **[COMBAT_AND_PROTECTION_AUDIT.md](compatibility/COMBAT_AND_PROTECTION_AUDIT.md)** — Global gamerules, claims/teams, Armor Set Bonuses, Zombie Awareness, and temperature/survival config audits.
- **[API_AND_INTEGRATION_RESEARCH.md](compatibility/API_AND_INTEGRATION_RESEARCH.md)** — Verified `1.18.2` vs `1.20.1` API reference for Create (`0.5.1.f` vs `6.0.6`), GeckoLib (`3` vs `4`), dynamic lighting, and soft compat bridges.
- **[deceasedcraft-5.5.5-1.18.2.csv](compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv)** & **[deceasedcraft-beta-5.10.17-1.20.1.csv](compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv)** — Complete, separate per-pack mod inventories.

### Asset Toolchain (`tools/`)
- **[tools/README.md](tools/README.md)** — Usage guide for `mc-asset` (2D textures, 4-stage particle strips, LabPBR `_s` maps) and headless `blockbench-mcp` (`tools/setup_asset_tools.sh`, `tools/bb_mcp_client.mjs`) for 3D GeckoLib models, animations, and PNG review renders.

### Research Libraries & Source Data (`docs/`)
- **[DeceasedCraft_Mod_Research.xlsx](docs/DeceasedCraft_Mod_Research.xlsx)** & **[RESEARCH_SUMMARY.md](docs/RESEARCH_SUMMARY.md)** — 3-sheet Excel catalog, 17-category breakdown, unported `1.18.2` mod audit, and reproducible extraction scripts in [docs/scripts/](docs/scripts/).
- **Primary-Source Reference Libraries (`docs/references/`):**
  - [Notebook 1 — Core Forge, Multi-Version Templates, GeckoLib, Flywheel & AI Tooling](docs/references/flmthrwr_notebook_1_overview.md)
  - [Notebook 2 — Create Kinetics, Fluids, Diesel Generators & Multi-Fuel Patterns](docs/references/flmthrwr_notebook_2_overview_links.md)
  - [Notebook 3 — Weapon/Turret Architectures, Rendering, Audio & Profiling](docs/references/flmthrwr_notebook_3_overview_links.md)
  - [Notebook 4 — Petroleum, Industrial Fuels & Combustion Properties](docs/references/flmthrwr_notebook_4_overview_links.md)
