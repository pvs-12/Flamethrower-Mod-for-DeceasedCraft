# FLMTHRWR: NOTEBOOK 2 — Context Overview & Source Links

## What This Notebook Is For

**FLMTHRWR: NOTEBOOK 2** serves as the **Create Ecosystem & Industrial Machinery Research Library** for the **Flamethrower Mod** (planned for development with Google Antigravity). It consolidates official documentation, source repositories, community addon patterns, modpack verification references, and AI-agent tooling into a single engineering reference.

### Target Versions & Modpack Context
* **Minecraft Forge 1.18.2** — Legacy **DeceasedCraft v5.5.5**
* **Minecraft Forge 1.20.1** — Newer **DeceasedCraft Beta**

---

## Core Engineering Focus Areas

This notebook is structured to guide architecture, compatibility, and implementation across the following domains:

1. **Create Rotational Power & Kinetic Mechanics**
   * Rotational power integration, Stress Unit (SU) consumption, kinetic block entity behaviors (including flicker mechanics), and Create dependency setup (`Ponder`, `Registrate`, `Flywheel`).
2. **Fluid Pipe Compatibility & Industrial Addon Integration**
   * Interfacing with Create fluid pipes, Spouts, and tanks, alongside integration research for **Create: Diesel Generators** (fuel burn rates, datapack configs, and projectile ignition patterns).
3. **Multi-Mod Fuel Handling**
   * Functional modeling based on **Immersive Engineering's Chemthrower** to decouple weapon and turret mechanics from hard-coded fluid mods via standard Forge fluid capabilities and data-driven definitions.
4. **DeceasedCraft Power & Modpack Verification**
   * Verifying installed mods and electrical power bridges (such as **Create Crafts & Additions** for Forge Energy $\leftrightarrow$ Kinetic conversion) while avoiding false assumptions about uninstalled mods (such as *Create: Electro Energetics*).
5. **Create Conventions & Combat/Turret Reference Patterns**
   * Mechanical Crafting, Wrench interaction caveats (exact item vs. tag checks), Engineer's Goggle tooltips, Ponder tutorials, kinetic aiming/projectiles (*Create Big Cannons*), and entity targeting/turret control (*Create: Radar*).
6. **AI-Agent Skills, Templates & MCP Tooling**
   * Multi-version Create addon templates, Minecraft AI-agent skill bundles, `AGENTS.md` project orientation examples, and Model Context Protocol (MCP) servers for code retrieval, documentation lookup, Maven resolution, and repository management.

---

## Key Architecture Highlight: Multi-Fuel System (Section D)

A central technical specification captured in this notebook is the **Multi-Fuel Architecture**, modeled functionally after Immersive Engineering's Chemthrower and Chemthrower Turret:

* **Data-Driven Fuel Registry:** Stored at `data/<namespace>/flamethrower_fuels/*.json`.
* **Lookup Priority:**
  1. Exact fluid registry ID (`fluid`)
  2. Fluid tag (`fluid_tag`, e.g., `#forge:gasoline`, `#forge:diesel`, `#forge:biodiesel`, `#forge:ethanol`, `#forge:creosote`, `#forge:crude_oil`)
  3. Unregistered fluids rejected via `isFluidValid(FluidStack)` on the tank (unless explicitly allowed as non-combustible spray).
* **Schema Fields:**
  * *Mandatory:* `fluid` or `fluid_tag`, `consumption_mb_per_tick`, `damage_multiplier`, `range_multiplier`, `ignites_targets`, `requires_pilot_light`.
  * *Optional:* `fuel_classification`, `heat_intensity`, `particle_profile`, `sound_profile`, `special_effect`, `compatibility_source`.
* **Tank & Safety Rules:**
  * **No Mixing by Default:** Non-empty tanks only accept matching fluids (`FluidStack.isFluidEqual(...)`) until drained or flushed.
  * **Strict Simulation Compliance:** `FluidAction.SIMULATE` never mutates state or triggers sync packets.
  * **Server-Authoritative Persistence & Sync:** NBT serialization in `saveAdditional()` / `load()`, server-side fuel consumption, and threshold/menu-open client syncing.
  * **Handheld Refilling:** Implements `IFluidHandlerItem` capability backed by `ItemStack` NBT for Create Spouts, tanks, and right-click container filling.

---

## All Links in This Notebook

### 1. Official Create Docs, Core Repositories & Dependencies
* **Create Official Developer Wiki:** https://wiki.createmod.net/developers/
* **Create Forge 1.20.1 Dependency Guide:** https://wiki.createmod.net/developers/depend-on-create/forge-1.20.1
* **Creators-of-Create / Create Repository:** https://github.com/Creators-of-Create/Create
* **Create Releases:** https://github.com/Creators-of-Create/Create/releases
* **Create Wiki — 6.0.0 Changelog:** https://github.com/Creators-of-Create/Create/wiki/6.0.0
* **Create Wiki — 0.5.1i Changelog:** https://github.com/Creators-of-Create/Create/wiki/0.5.1i
* **Create Wiki — 0.5.1e Changelog:** https://github.com/Creators-of-Create/Create/wiki/0.5.1e
* **Create Wiki — Attaching TileEntity Behaviours:** https://github.com/Creators-of-Create/Create/wiki/Attaching-TileEntity-Behaviours
* **Create Wiki Git Repository:** https://github.com/Creators-of-Create/Create.wiki.git
* **Create Issue #10830 (Wrenches from other mods / tag caveats):** https://github.com/Creators-of-Create/Create/issues/10830
* **Create Issue #9251 (Flicker score / KineticBlockEntity mechanics):** https://github.com/Creators-of-Create/Create/issues/9251
* **Creators-of-Create / Ponder:** https://github.com/Creators-of-Create/Ponder
* **tterrag1098 / Registrate:** https://github.com/tterrag1098/Registrate
* **Engine-Room / Flywheel:** https://github.com/Engine-Room/Flywheel

### 2. Create: Diesel Generators & Industrial Create Addons
* **Create: Diesel Generators Repository:** https://github.com/george8188625/Create-Diesel-Generators
* **Create: Diesel Generators Releases:** https://github.com/george8188625/Create-Diesel-Generators/releases
* **Create: Diesel Generators Issue #183 (Datapack fuel burn rate):** https://github.com/george8188625/Create-Diesel-Generators/issues/183
* **Create: Diesel Generators Issue #95 (Chemical Sprayer projectile ignition):** https://github.com/george8188625/Create-Diesel-Generators/issues/95
* **Create Addons Wiki — Diesel Engine:** https://comprehensive-create-mod-addons.fandom.com/wiki/Diesel_Engine
* **george8188625 GitHub Profile (Create: Diesel Generators / Electro Energetics author):** https://github.com/george8188625
* **Create Crafts & Additions (`mrh0/createaddition`):** https://github.com/mrh0/createaddition
* **Create Big Cannons (`Cannoneers-of-Create/CreateBigCannons`):** https://github.com/Cannoneers-of-Create/CreateBigCannons
* **Create: Radar (`Arsenalists-of-Create/Create-Radar`):** https://github.com/Arsenalists-of-Create/Create-Radar
* **Create: Steam 'n' Rails (`Layers-of-Railways/Railway`):** https://github.com/Layers-of-Railways/Railway

### 3. Immersive Engineering & Modpack Verification
* **Immersive Engineering Repository (`BluSunrize/ImmersiveEngineering`):** https://github.com/BluSunrize/ImmersiveEngineering
* **Immersive Engineering Issue #3626 (Chemthrower Turret range behavior):** https://github.com/BluSunrize/ImmersiveEngineering/issues/3626
* **FTB Wiki — Chemical Thrower:** https://ftbwiki.org/Chemical_Thrower
* **DeceasedCraft Verified Version Manifest (MCMOD):** https://www.mcmod.cn/modpack/715.html
* **DeceasedCraft 1.20.1 Beta Overview Site:** https://millida.net

### 4. Create Addon Templates, AI-Agent Skills & MCP Servers
* **Fabricators-of-Create Multiloader Addon Template:** https://github.com/Fabricators-of-Create/create-multiloader-addon-template
* **StaticFX Create Addon Template:** https://github.com/StaticFX/create-addon-template
* **aesefficio Create Addon Template (Stonecutter):** https://github.com/aesefficio/CreateAddonTemplate
* **Create Electro Utilities (`adam8797/create-electro-utilities`):** https://github.com/adam8797/create-electro-utilities
* **Minecraft Agent Skills (`Jahrome907/minecraft-agent-skills`):** https://github.com/Jahrome907/minecraft-agent-skills
* **Minecraft Agent Skills Bundle (`AIKUSAN/minecraft-agent-skills-bundle`):** https://github.com/AIKUSAN/minecraft-agent-skills-bundle
* **ChronoDawn `AGENTS.md` Reference (`ksoichiro/ChronoDawn`):** https://github.com/ksoichiro/ChronoDawn/blob/main/AGENTS.md
* **GitHub MCP Server (`github/github-mcp-server`):** https://github.com/github/github-mcp-server
* **Serena MCP Toolkit (`oraios/serena`):** https://github.com/oraios/serena
* **Serena Documentation:** https://oraios.github.io/serena
* **Context7 MCP Server (`upstash/context7`):** https://github.com/upstash/context7
* **Context7 Website:** https://context7.com/
* **Maven Tools MCP (`arvindand/maven-tools-mcp`):** https://github.com/arvindand/maven-tools-mcp

### 5. Maven Endpoints & Referenced Supplementary Links in Sources
* **Create / Ponder / Flywheel Maven:** https://maven.createmod.net
* **Registrate Mirror Maven:** https://maven.ithundxr.dev/mirror
* **ForgeConfigAPIPort / Fuzss ModResources Maven:** https://raw.githubusercontent.com/Fuzss/modresources/main/maven/
* **License References Mentioned in Addon Sources:**
  * Quilt Standard Libraries License: https://github.com/QuiltMC/quilt-standard-libraries/blob/1.19.4/LICENSE
  * SecurityCraft License: https://github.com/Geforce132/SecurityCraft/blob/1.18.2/LICENSE
  * Neruina License: https://github.com/Bawnorton/Neruina/blob/multi-version/LICENSE.txt
  * FramedBlocks License: https://github.com/XFactHD/FramedBlocks/blob/17c8274ca380c3a868763b1b05657d07860c364b/LICENSE
  * MIT License Overview (referenced in `createaddition`): https://tldrlegal.com/license/mit-license
  * maxxq-maven (referenced in `maven-tools-mcp`): https://github.com/maxxq-org/maxxq-maven

> **Note on Additional Referenced Sources:** The notebook inventory also lists **Official Forge Documentation** (Capabilities, Server Tags, and SimpleChannel Networking for both 1.18.x and 1.20.1) and **`mcp-jetbrains`**, which are noted by name in the context summary without explicit raw URLs in the source excerpts.