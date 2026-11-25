# FLMTHRWR: NOTEBOOK 4 — Petroleum, Industrial Fuels & Combustion Reference

## Purpose of This Notebook

**FLMTHRWR: NOTEBOOK 4** serves as the **Petroleum, Industrial Fuels & Combustion Research Library** for the original **Flamethrower Mod**, targeting two Minecraft Forge environments:

- **Minecraft Forge 1.18.2** — Legacy DeceasedCraft (`v5.5.5`)
- **Minecraft Forge 1.20.1** — Newer DeceasedCraft Beta

Its core objective is to anchor the mod's **data-driven multi-fuel system** in verified Minecraft mod fluid registries and Forge APIs, informed by authoritative real-world petroleum and combustion engineering references. All real-world engineering data in this notebook is strictly focused on general scientific/engineering principles and fictional Minecraft gameplay balance—never real-world weapon construction.

---

## Research Domains Covered

### 1. Create: Diesel Generators & DeceasedCraft Fuel Ecosystem
Establishes exact fluid ecosystems, datapack fuel definitions (such as `burn_rate`), distillation recipe syntax, fermentation workflows, and existing sprayer/thrower design references within DeceasedCraft and its core tech mods:
- **Create: Diesel Generators** (repository, releases, datapack fuel JSON, Bulk Fermenter ethanol, Chemical Sprayer ignition)
- **Immersive Engineering** (repository and Chemical Thrower mechanics)
- **DeceasedCraft** (1.20.1 Beta modlist and tech progression overview)
- **Create** (`0.5.1e` fluid interaction notes)

### 2. Optional Industrial Fluid Mods & Forge Fluid APIs
Supports cross-mod compatibility and Forge fluid/networking architecture across optional industrial mods:
- **Mekanism**
- **PneumaticCraft: Repressurized** (including 4-fraction refinery design notes)
- **CoFH Thermal Expansion**
- **Minecraft Forge (1.18.x & 1.20.1)** Capabilities, Server Tags, and `SimpleChannel` Networking

### 3. Real-World Petroleum & Combustion Engineering References
Provides physical and chemical benchmarks (calorific values, densities, flash points, autoignition temperatures, fractional distillation cuts, and soot formation vs. equivalence ratio $\lambda$) to inspire balanced, distinct gameplay profiles for each in-game fuel:
- **U.S. DOE Alternative Fuels Data Center (AFDC)** — Fuel Properties Comparison (March 2024, `DOE/GO-102024-6212`)
- **U.S. Energy Information Administration (EIA)** — Crude Oil Refining Process, Inputs/Outputs, and Petroleum Supply Definitions
- **The Engineering ToolBox** — Calorific Values, Densities, Alternative Fuel Properties, Flash Points, and Autoignition Temperatures
- **Wikipedia & DieselNet** — Combustion, Soot, Fractional Distillation, and soot formation vs. equivalence ratio ($\lambda$)

### 4. AI-Agent Skills & MCP Tooling
Catalogs coding-agent instructions, Minecraft-specific agent skill bundles, and Model Context Protocol (MCP) servers to accelerate mod development, dependency auditing, semantic code editing, and repository workflows:
- **Minecraft Agent Skills** (`Jahrome907/minecraft-agent-skills`, `AIKUSAN/minecraft-agent-skills-bundle`)
- **Project Agent Context Reference** (`ChronoDawn/AGENTS.md`)
- **MCP Servers** (GitHub MCP, Serena MCP, Context7 MCP, Maven Tools MCP, JetBrains MCP)

---

## Links in This Notebook

### Minecraft Modding, Fuel Ecosystems & Industrial Mods
- **Create: Diesel Generators (Repository):** https://github.com/george8188625/Create-Diesel-Generators
- **Create: Diesel Generators (Releases):** https://github.com/george8188625/Create-Diesel-Generators/releases
- **Create: Diesel Generators (Wiki):** https://github.com/george8188625/Create-Diesel-Generators/wiki
- **Create: Diesel Generators (Issue #392 — Bulk Fermenter):** https://github.com/george8188625/Create-Diesel-Generators/issues/392
- **Create (Repository):** https://github.com/Creators-of-Create/Create
- **Create Wiki (`0.5.1e`):** https://github.com/Creators-of-Create/Create/wiki/0.5.1e
- **Immersive Engineering (Repository):** https://github.com/BluSunrize/ImmersiveEngineering
- **FTB Wiki — Chemical Thrower:** https://ftbwiki.org/Chemical_Thrower
- **DeceasedCraft 1.20.1 Beta Modlist (MCMOD):** https://mcmod.cn/modpack/715.html
- **DeceasedCraft Tech Overview:** https://millida.net
- **Mekanism (Repository):** https://github.com/mekanism/Mekanism
- **PneumaticCraft: Repressurized (Repository):** https://github.com/TeamPneumatic/pnc-repressurized
- **PneumaticCraft: Repressurized (Issue #305 — 4-Fraction Refinery):** https://github.com/TeamPneumatic/pnc-repressurized/issues/305
- **CoFH Thermal Expansion (Repository):** https://github.com/CoFH/ThermalExpansion

### Real-World Petroleum & Combustion Engineering
- **U.S. DOE AFDC — Fuel Properties Comparison:** https://afdc.energy.gov/fuels/properties
- **U.S. EIA — Oil and Petroleum Products Explained:** https://www.eia.gov/energyexplained/oil-and-petroleum-products/
- **U.S. EIA — Refining Crude Oil:** https://www.eia.gov/energyexplained/oil-and-petroleum-products/refining-crude-oil.php
- **U.S. EIA — The Refining Process:** https://www.eia.gov/energyexplained/oil-and-petroleum-products/refining-crude-oil-the-refining-process.php
- **U.S. EIA — Refining Inputs and Outputs:** https://www.eia.gov/energyexplained/oil-and-petroleum-products/refining-crude-oil-inputs-and-outputs.php
- **U.S. EIA — Energy Use for Transportation:** https://www.eia.gov/energyexplained/use-of-energy/transportation.php
- **U.S. EIA — Petroleum FAQs:** https://www.eia.gov/tools/faqs/index.php#oil/petroleum
- **Engineering ToolBox — Higher Calorific Values of Common Fuels:** https://www.engineeringtoolbox.com/fuels-higher-calorific-values-d_169.html
- **Engineering ToolBox — Fuels and Chemicals Autoignition Temperatures:** https://www.engineeringtoolbox.com/fuels-ignition-temperatures-d_171.html
- **Engineering ToolBox — Alternative Fuels Properties:** https://www.engineeringtoolbox.com/alternative-fuels-d_1221.html
- **Engineering ToolBox — Combustion (Topic Hub):** https://www.engineeringtoolbox.com/combustion-boiler-fuels-t_9.html
- **Engineering ToolBox — Fossil vs. Alternative Fuels Energy Content:** https://www.engineeringtoolbox.com/fossil-fuels-energy-content-d_1298.html
- **Engineering ToolBox — Fuel Oils Densities vs. Temperature:** https://www.engineeringtoolbox.com/fuel-oil-density-temperature-gravity-volume-correction-ASTM-D1250-d_1942.html
- **Engineering ToolBox — Fuels Combustion Air and Flue Gases:** https://www.engineeringtoolbox.com/fuels-air-flue-gas-d_170.html
- **Engineering ToolBox — Fuels Properties Database:** https://www.engineeringtoolbox.com/fuels-properties-d_839.html
- **Engineering ToolBox — Octane Liquid Thermal Properties:** https://www.engineeringtoolbox.com/octane-thermal-properties-d_1760.html
- **Engineering ToolBox — Oil Lubrication Temperature Limits:** https://www.engineeringtoolbox.com/oil-temperature-limits-lubrication-d_1492.html
- **Wikipedia — Combustion:** https://en.wikipedia.org/wiki/Combustion
- **Wikipedia — Soot:** https://en.wikipedia.org/wiki/Soot
- **Wikipedia — Fractional Distillation:** https://en.wikipedia.org/wiki/Fractional_distillation
- **Methanol Institute — Physical Properties of Pure Methanol (PDF, cited in DOE AFDC):** https://www.methanol.org/wp-content/uploads/2016/06/Physical-Properties-of-Pure-Methanol.pdf
- **NREL/DOE — Overview of Biodiesel and Petroleum Diesel Life Cycles (PDF, cited in DOE AFDC):** https://www.nrel.gov/docs/legosti/fy98/24772.pdf
- **Argonne National Laboratory — Energy and GHG Emissions Impacts of Fuel Ethanol (cited in DOE AFDC):** https://www.researchgate.net/publication/228787542_Energy_and_greenhouse_gas_emissions_impacts_of_fuel_ethanol

### AI-Agent Skills & MCP Tooling
- **Jahrome907 — Minecraft Agent Skills:** https://github.com/Jahrome907/minecraft-agent-skills
- **Jahrome907 — Skill Audit Review Notes:** https://github.com/Jahrome907/minecraft-agent-skills/blob/main/docs/skill-audit-2026-10.md
- **AIKUSAN — Minecraft Agent Skills Bundle:** https://github.com/AIKUSAN/minecraft-agent-skills-bundle
- **ChronoDawn (Repository):** https://github.com/ksoichiro/ChronoDawn
- **ChronoDawn — `AGENTS.md`:** https://github.com/ksoichiro/ChronoDawn/blob/main/AGENTS.md
- **GitHub MCP Server:** https://github.com/github/github-mcp-server
- **Serena MCP (Repository):** https://github.com/oraios/serena
- **Serena MCP (Documentation):** https://oraios.github.io/serena
- **Serena MCP (User Guide):** https://oraios.github.io/serena/02-usage/000_intro.html
- **Serena MCP (Tools Reference):** https://oraios.github.io/serena/01-about/035_tools.html
- **Serena MCP (Workflow Guide):** https://oraios.github.io/serena/02-usage/040_workflow.html
- **Serena MCP (Configuration Guide):** https://oraios.github.io/serena/02-usage/050_configuration.html
- **Context7 MCP (Repository):** https://github.com/upstash/context7
- **Context7 (Platform Website):** https://context7.com/
- **Maven Tools MCP (Repository):** https://github.com/arvindand/maven-tools-mcp
- **Maven Tools MCP — Setup Docs:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/setup.md
- **Maven Tools MCP — Tools Catalog:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/tools.md
- **Maven Tools MCP — Examples & FAQ:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/examples.md
- **Maven Tools MCP — Architecture:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/architecture.md
- **JetBrains MCP Server:** https://github.com/JetBrains/mcp-jetbrains

### Additional Notebook Sources Referenced Without Direct URLs in Retrieved Excerpts
> The following items are listed in the Notebook 4 context inventory, though their exact page URLs were not included in the retrieved text snippets:
> - Create: Diesel Generators Issues `#183` (datapack fuel JSON & `burn_rate`) and `#95` (Chemical Sprayer ignition)
> - Create Addons Wiki (`Diesel_Engine`)
> - KubeJS Diesel Generators distillation recipe syntax reference
> - Official Minecraft Forge 1.18.x & 1.20.1 Documentation (Capabilities, Server Tags, `SimpleChannel` Networking)
> - U.S. EIA Petroleum Supply Definitions
> - Engineering ToolBox Densities & Flash Points pages
> - DieselNet — Soot Formation vs. Equivalence Ratio ($\lambda$)