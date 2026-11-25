# Create: Tactical ChemThrowers — Engineering Specification

**Document:** `SPECS.md` (Authoritative Unified Specification)  
**Mod Display Name:** Create: Tactical ChemThrowers  
**Mod ID:** `tacticalchemthrowers`  
**Platform:** Minecraft Java Edition (Forge — Dual-Version Build)  
**Status:** Implementation-ready engineering contract (supersedes `SPECS_updated.md`)  
**Last Updated:** 2026-11-25

---

## 1. Mod Identity, Scope & EULA Compliance

### 1.1 Project Objective
Build **Create: Tactical ChemThrowers** (`modid: tacticalchemthrowers`), an original, polished, high-performance handheld tactical chem-thrower and automated Create-integrated turret mod designed specifically to feel native inside **DeceasedCraft**'s survival, scavenging, combat, and industrial technology progression.

The mod targets two distinct DeceasedCraft environments as separate compiled artifacts built from a shared design and common logic layer:

| Target Line | Minecraft | Forge | Java | Official Pack Release | CurseForge File ID(s) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **Legacy Stable** | `1.18.2` | `40.2.4` | 17 | `DeceasedCraft_v5.5.5` (2024-07-12) | `5525524` (224 mods + 6 packs) | Confirmed target |
| **v6 Open Beta** | `1.20.1` | `47.4.0` | 17 | `DeceasedCraft_Beta-5.10.17` (2026-07-17) | Standard: `8448820` (306 mods + 11 packs)<br>DH Edition: `8448903` (+1 `Distant Horizons`) | Confirmed target (beta caveats apply) |
| **Final v6.0** | TBD | TBD | TBD | Not yet publicly released | TBD | Revalidate upon public release |

> **Beta Caveat:** DeceasedCraft's authors designate the `5.10.x` line as an incomplete open beta for the `v6.0` overhaul and do not guarantee world or mod-list stability between `Beta-5.10.17` and final `v6.0`. Re-audit the manifest and overrides before publishing a final `v6.0` release.

### 1.2 Strict Minecraft EULA & Originality Mandate
- **100% Original Naming:** Every item, block, fluid profile, module, advancement, texture, model, sound, and documentation entry MUST use original fictional industrial/tactical naming (e.g., *Tactical ChemThrower*, *Pressurized Fuel Canister*, *High-Pressure Atomizer Nozzle*, *Extended Igniter Barrel*, *Kinetic ChemThrower Turret*).
- **Zero Real-World Weapon Trademarks or Model Designations:** Never reference real-world firearm/flamethrower brands, manufacturers, military designations, or model numbers anywhere in code, localization, tooltips, assets, or docs.
- **Zero Copyrighted IP References:** Never reference copyrighted movies, TV shows, video games, franchises, or characters in code, assets, or documentation. Describe visual inspiration purely through physical/industrial traits (heavy twin-operator tactical chem-thrower silhouette, perforated heat-shielded barrel, armored gimbal, riveted iron, copper tubing, brass valves).
- **Zero Plagiarism:** All Java source code, 3D Blockbench models, 2D textures, particle strips, animations, audio files, and GUI art must be independently authored. External open-source mods are referenced strictly for API interoperability and architectural learning.

---

## 2. Core Engineering Principles & Multi-Version Architecture

### 2.1 Performance as a First-Class Requirement
- Maintain high, stable client FPS and low server tick overhead **without stripping visual identity**.
- Achieve performance through disciplined engineering: capped client particle budgets, distance-based visual LOD, bounded entity queries, cached collision raycasts, event-driven or interval-throttled block-entity ticks, single managed looping audio instances per active source, and compact state-change network packets.
- Never spawn unbounded particles, run per-particle world queries, scan all loaded entities every tick, or emit continuous idle particles/sounds.

### 2.2 Compatibility-First Engineering
- Compatibility means verified interoperability across fluids, capabilities, recipes, KubeJS scripts, combat/damage rules, claims/teams, shaders, and survival mechanics—never merely "boots without crashing."
- Interoperate with existing **Create**, **Immersive Engineering**, **Immersive Petroleum** (`v5.5.5`), **Create: Diesel Generators** (`Beta-5.10.17`), **Create Crafts & Additions**, **Pipez**, and **Refined Storage** ecosystems via standard Forge capabilities (`IFluidHandler`, `IFluidHandlerItem`, `IEnergyStorage`, `IItemHandler`) and Forge tags.
- Keep optional integrations behind isolated runtime-detected adapters (`ModList.get().isLoaded(...)`). Missing optional mods must never crash startup or gameplay.
- Never modify DeceasedCraft pack files in place as an installation step, and never override pack recipes globally.

### 2.3 Dual-Version Source & Adapter Separation
Minecraft `1.18.2` (`Forge 40.2.4`) and `1.20.1` (`Forge 47.4.0`) cannot share a single runtime JAR. Separate pure gameplay logic from version- and mod-specific bindings:

| Layer | Responsibility | Version Coupling |
| --- | --- | --- |
| **Shared Common Logic** | `FuelRegistry` schema/lookup, `JetGeometry` capsule/raycast math, `HeatTracker` multiplier/decay rules, `TemporaryFire` safety logic, turret targeting/filter state machine, config clamping, shared balance constants | Version-agnostic Java 17 |
| **Platform Forge Adapter (`1.18.2` vs `1.20.1`)** | `DeferredRegister` / `CreativeModeTab`, `DamageSource` (class in `1.18.2` vs `Holder<DamageType>` in `1.20.1`), `PoseStack` vs `GuiGraphics`, `TextComponent` vs `Component.literal()`, `SimpleChannel` packets, Global Loot Modifiers (`GLM`) | Strict per-MC-version module |
| **Create & Rendering Adapter** | Create `0.5.1.f` (`1.18.2`) vs Create `6.0.6` (`1.20.1`, extracted Ponder & Flywheel 1.0/Colorwheel); GeckoLib 3 (`3.0.57`) vs GeckoLib 4 (`4.7`) | Strict per-MC-version module |
| **Optional Compat Bridges** | `DynamicLightBridge` (`Lucent` vs `Sodium Dynamic Lights`), `SurvivalBridge` (`Cold Sweat` vs `Legendary Survival Overhaul`), `ProtectionBridge` (`Open Parties & Claims`, `FTB Teams`), `AggroBridge` (`Zombie Awareness`) | Runtime-checked soft adapters |

### 2.4 Client/Server Isolation & Mixin Restraint
- Keep all client rendering, particles, shaders, audio, and keybind code strictly isolated from common/server code (`Dist.CLIENT` / client-only packages).
- All gameplay-critical state (fuel consumption, canister reload, heat stacks, hit validation, damage, block ignition, turret targeting/power) is **strictly server-authoritative**.
- Avoid mixins/coremods unless a documented requirement cannot be achieved through supported Forge events or mod APIs. Never add invasive vanilla renderer mixins that conflict with Embeddium, Oculus, Colorwheel, Vanillin, ImmediatelyFast, or Distant Horizons.

---

## 3. Target Environments & Verified Compatibility Artifacts

Both DeceasedCraft pack archives have been downloaded, reconciled 100% against their CurseForge `manifest.json` and `overrides/` directories, and audited into separate, version-pinned repository artifacts. Never merge the two inventories or infer mod presence across versions.

### 3.1 Canonical Compatibility Artifacts
- **v5.5.5 Full Mod Inventory (224 mods):** [deceasedcraft-5.5.5-1.18.2.csv](compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv)
- **Beta 5.10.17 Full Mod Inventory (306 Standard + 1 DH Extra = 307 mods):** [deceasedcraft-beta-5.10.17-1.20.1.csv](compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv)
- **Cross-Version Ecosystem Matrix & Archive Hashes:** [ECOSYSTEM_MATRIX.md](compatibility/ECOSYSTEM_MATRIX.md)
- **Recipes, Fluids & KubeJS Overrides Audit:** [RECIPE_AND_FLUID_AUDIT.md](compatibility/RECIPE_AND_FLUID_AUDIT.md)
- **Combat, Claims, Gamerules & Survival Audit:** [COMBAT_AND_PROTECTION_AUDIT.md](compatibility/COMBAT_AND_PROTECTION_AUDIT.md)
- **API & Mod Integration Research:** [API_AND_INTEGRATION_RESEARCH.md](compatibility/API_AND_INTEGRATION_RESEARCH.md)
- **Source Workbook & Statistical Summary:** [DeceasedCraft_Mod_Research.xlsx](docs/DeceasedCraft_Mod_Research.xlsx) and [RESEARCH_SUMMARY.md](docs/RESEARCH_SUMMARY.md)

### 3.2 High-Priority Ecosystem Comparison (Verified JARs)

| Ecosystem / Domain | DeceasedCraft `v5.5.5` (`MC 1.18.2` / `Forge 40.2.4`) | DeceasedCraft `Beta-5.10.17` (`MC 1.20.1` / `Forge 47.4.0`) | Engineering Impact |
| --- | --- | --- | --- |
| **Create Core** | `create-1.18.2-0.5.1.f.jar` | `create-1.20.1-6.0.6.jar` | Major Create `0.5.1` → `6.0.6` API shift (Ponder extracted, Flywheel 1.0). Isolate kinetic/goggle/wrench bindings per version. |
| **Create Addons** | `createaddition-1.18.2-1.0.0.jar`, `createbigcannons-forge-1.18.2-0.5.3.b.jar`, `Steam_Rails-1.4.8`, `createdeco-1.3.3`, `create-stuff-additions-v2.0.4a` | `createdieselgenerators-1.20.1-1.3.5.jar`, `createaddition-1.20.1-1.3.2.jar`, `Radars 0.3.5.1-Create6.jar`, `createbigcannons-5.9.1`, `createdeco-2.0.3`, `create-stuff-additions-v2.1.0` | **Create: Diesel Generators is ONLY in `Beta-5.10.17`**; `v5.5.5` does not have it. Never hard-depend on CDG. |
| **Immersive Engineering & Petroleum** | `ImmersiveEngineering-1.18.2-8.4.0-161.jar`, `ImmersivePetroleum-1.18.2-4.2.0-25.jar` | `ImmersiveEngineering-1.20.1-10.2.0-183.jar` (**No Immersive Petroleum**) | **Immersive Petroleum is ONLY in `v5.5.5`**. Data-driven fluid tags bridge both seamlessly. IE Chemthrower is enabled in both packs. |
| **Fluid & Item Logistics** | `pipez-1.18.2-1.1.5.jar`, `refinedstorage-1.10.6.jar` | `pipez-forge-1.20.1-1.2.21.jar`, `refinedstorage-1.12.4.jar` | Standard Forge `IFluidHandler`, `IEnergyStorage`, `IItemHandler` work across both. |
| **3D Animation** | `geckolib-forge-1.18-3.0.57.jar` (GeckoLib 3), `player-animation-lib-forge-1.0.2+1.18.jar` | `geckolib-forge-1.20.1-4.7.jar` (GeckoLib 4), `player-animation-lib-forge-1.0.2-rc1+1.20.jar` | GeckoLib 3 (`IAnimatable`) vs GeckoLib 4 (`GeoItem`/`GeoBlockEntity`) requires per-version animation adapters. |
| **Rendering & Shaders** | `embeddium-0.3.10`, `oculus-mc1.18.2-1.6.4`, `oculus-flywheel-compat-0.2.1`, `GeckoLibOculusCompat-1.0.1`, `oculusparticlefix-1.0` | `embeddium-0.3.31`, `oculus-mc1.20.1-1.8.0`, `colorwheel-1.1.1`, `vanillin-1.1.3`, `ImmediatelyFast-1.5.1`, `DistantHorizons-2.4.5-b` (DH Edition) | Use standard Forge/GeckoLib render types & Iris/Oculus-safe particle shaders; test with shaders ON and OFF + DH Edition. |
| **Dynamic Lighting** | `lucent-1.18.2-1.2.2.jar` | `sodiumdynamiclights-forge-1.0.10-1.20.1.jar` | Soft optional `DynamicLightBridge` per version for glowing nozzle, jet particles, and active turret pilot/fire. |
| **Survival & Temp** | `ColdSweat-2.2.5.1.jar`, `firstaid-1.11.1.jar`, `ThirstWasTaken-1.18.2-1.3.4.jar` | `legendarysurvivaloverhaul-1.20.1-2.3.23.1.jar` | Critical divergence; isolate subtle firing warmth behind optional `SurvivalBridge`. |
| **Claims, Teams & Protection** | `open-parties-and-claims-0.20.1`, `ftb-teams-1802.2.9`, `spacecatasb-18.13.1` (Armor Set Bonuses) | `open-parties-and-claims-0.25.8`, `ftb-teams-2001.3.1`, `spacecatasb-20.14.0` (Armor Set Bonuses) | Route damage, PvP, and temporary fire placement through Forge events + soft `ProtectionBridge`. |
| **Zombies, AI & Audio** | `zombieawareness-1.18.1-1.12.3`, `The-Hordes-1.5.3a`, `soundphysics-1.0.6` | `zombieawareness-1.20.1-1.13.1`, `The-Hordes-1.5.4c`, `sound-physics-remastered-1.4.10` | Target vanilla/Forge entity tags & events; add soft Zombie Awareness sound/light aggro hooks. |
| **Loot & Scripting** | `lootr-1.18.2-0.3.25.63`, `kubejs-1802.5.5`, `CraftTweaker-9.1.211`, `ContentTweaker-1.0.0` | `lootr-forge-1.20-0.7.35.94`, `kubejs-2001.6.5`, `kubejs-create-2001.3.0` (**No CraftTweaker**) | Use Forge Global Loot Modifiers (Lootr-safe) and standard JSON datapacks/recipes (never CraftTweaker). |
| **Pack Patch Mods** | `DeceasedCraftFixes-1.0.7+1.18.2.jar` (`DCFixes`) | `deceased_expansion-1.10-all.jar` (`DeceasedCraft++`), `DCTweaks_5.10.14.jar` | Watch for overlapping config/tag/event behavior; never conflict with pack patches. |

### 3.3 Cross-Version Engineering Rules (Mandatory)
1. **No hard dependencies on survival mods** (`Cold Sweat`, `First Aid`, `Thirst Was Taken`, `Legendary Survival Overhaul`).
2. **No hard dependencies on firearms mods** (`TaC` in `v5.5.5` vs `TaCZ` in `Beta-5.10.17`). Interact via standard Forge `DamageSource`/`DamageType`, `LivingHurtEvent`, and tags.
3. **No hard dependencies on fuel-provider addons** (`Immersive Petroleum`, `Create: Diesel Generators`). All fuel resolution goes through our data-driven registry and Forge fluid tags.
4. **No CraftTweaker/ZenScript reliance**—`Beta-5.10.17` removed CraftTweaker. Use standard JSON recipes, Forge tags, GLMs, and Forge configs.
5. **Account for Create `0.5.1.f` → `6.0.6` and GeckoLib `3` → `4` deltas** via per-version adapter modules.
6. **Avoid invasive renderer mixins** to preserve Embeddium, Oculus, Colorwheel, Vanillin, ImmediatelyFast, and Distant Horizons stability.
7. **Target entity-type tags & Forge events** so zombie/horde interactions stay portable across `The Hordes`, `THE UNDEAD REVAMPED`, `Zombie Extreme`, `Zombie Awareness`, `Enhanced AI`, and `Fungal Infection: Spore`.
8. **Use Forge Global Loot Modifiers (GLMs)** so `Lootr` automatically instances rare military/lab city loot per player in multiplayer on both versions.
9. **No hard dependencies on vehicle mods** (`Ultimate Car Mod` vs `DragN's Valiant Vehicles!`).
10. **Verify bundled resource & shader packs** (not counted in mod totals: `6` in `v5.5.5`, `11` in `Beta-5.10.17` including `Complementary Reimagined`, `Complementary Unbound`, `Photon`, `Bliss`, `Spooklementary`, `Insanity Shader`, `No Enchant Glint`, `Tissou's Zombie Pack`) during visual QA.

---

## 4. 3D Visual Direction, Flame VFX, Emissivity & Shaders

### 4.1 Heavy Tactical + Create Mod Aesthetic
Both the **Handheld Tactical ChemThrower** and the **Automated Kinetic ChemThrower Turret** share a unified industrial-tactical art direction:

- **Heavy Tactical Silhouette:** Bulky military-industrial chassis built for rugged close-to-mid-range containment—perforated heat-shielded barrel shroud, dual/underslung pressurized fuel canister cradle, hooded pilot igniter guard, ergonomic twin-grip receiver with tactical rails, and an armored gimbal mount for the turret.
- **Create Mod Material Language:** Seamless visual integration with Create machinery—riveted andesite-alloy and dark iron structural frames, oxidized and polished **copper** pressurized fuel conduits, machined **brass** regulator valves and fittings, and a live mechanical pressure dial + subtle rotating cogwheel/gearbox accents.
- **Visual Module Readability:** Swapping the handheld nozzle/pressure module visibly changes the barrel assembly and pressure hardware on the 3D model so players can identify range tier (`15b` / `25b` / `35b`) at a glance in both 1st- and 3rd-person.
- **No Unnecessary Enchant Glint Clutter:** Respect DeceasedCraft's bundled *No Enchant Glint* aesthetic; communicate weapon status via the live pressure gauge needle, fuel sight-glass/bar, and pilot flame tip rather than glowing overlays.

### 4.2 Flame Jet VFX: Crisp Pixel-Native Blocky 4-Stage Combustion
Flame visuals must look unmistakably crisp, pixel-native to Minecraft, violent and readable at night, and strictly bounded so FPS never degrades—even in dense zombie hordes or with multiple active throwers/turrets.

- **Geometry & Size:** Crisp pixel-art blocky billboard quad particles (`0.18` to `0.55` blocks in size, crisp nearest-neighbor pixel texels authored via `mc-asset`, zero soft-blurred photorealistic blobs).
- **4-Stage Combustion Lifecycle** (driven by normalized particle age `t ∈ [0.0, 1.0]` and fuel `particle_profile`):
  1. **Stage 1 — Pressurized Core (`t = 0.00 → 0.18`):** Blinding white-yellow pressurized stream erupting straight from the nozzle with subtle downward ballistic liquid droop (`gravity` scaled by fuel viscosity), compact scale (`0.18–0.28b`), maximum brightness.
  2. **Stage 2 — Roaring Combustion (`t = 0.18 → 0.55`):** Expanding blocky orange-amber flame clouds (`0.32–0.55b`) tumbling outward along the cone envelope, shedding sparse fast-moving bright-yellow pixel sparks/embers.
  3. **Stage 3 — Cooling Crimson Ember (`t = 0.55 → 0.78`):** Contracting deep crimson/red-orange charred flame clusters losing forward momentum and drifting slightly upward from thermal buoyancy.
  4. **Stage 4 — Hydrocarbon Black Smoke (`t = 0.78 → 1.00`):** Rising dark charcoal / black hydrocarbon soot puffs (density modulated by fuel `soot_factor`, e.g., thick dark soot for crude oil/diesel/napalm, lighter haze for ethanol) that drift upward and linger briefly (`0.6–1.2s`) after trigger release alongside a crisp nozzle vent puff.
- **First-Person Readability:** Offset nozzle emission slightly forward/right and keep early Stage 1 core particles compact so the center crosshair and zombie silhouettes remain clearly legible while firing.
- **Strict Client Particle Budgets & LOD:**
  - Hard client-side cap on active mod flame/smoke particles (configurable; default soft cap `350`, hard cap `600` active mod particles globally, with per-source throttling when multiple throwers/turrets fire simultaneously).
  - Respect Minecraft's `Particles` video setting: `ALL` = 100%, `DECREASED` = 55%, `MINIMAL` = 25% (preserving core silhouette readability while cutting secondary sparks/smoke).
  - Distance LOD: reduce spawn frequency smoothly beyond `24` blocks and cull cosmetic sparks/smoke beyond `48` blocks.
  - Zero per-particle block/entity raycasts—collision is strictly handled by server-authoritative jet geometry and cached client impact distance.

### 4.3 Night Glow, Dynamic Lighting & Shader Compatibility Matrix
DeceasedCraft relies heavily on dark nights and horror atmosphere; the flame jet and pilot burner must illuminate the darkness dramatically without breaking under Iris/Oculus shader pipelines.

- **Full-Bright Emissive Rendering:**
  - Stage 1–3 flame/spark particles and the weapon/turret pilot flame render with `LightTexture.FULL_BRIGHT` (`0xF000F0`) in a dedicated Iris/Oculus-safe translucent/additive particle render type (avoiding custom GL state mutations that break deferred G-buffer passes).
  - Stage 4 hydrocarbon smoke uses world-sampled lightmap values (`getLightColor`) so dark soot looks naturally lit against bright fire and sinister at night.
- **LabPBR Specular / Emissive Maps (`_s.png`):**
  - Author LabPBR 1.3 `_s` textures (using `mc-asset`) for the ChemThrower nozzle pilot tip, pressure gauge dial, turret igniter coil, and glowing fire surfaces so shader packs automatically apply bloom/emission cleanly.
- **Dynamic Lighting Bridges (Soft Optional):**
  - **`v5.5.5` (`1.18.2`):** Integrate with **Lucent** (`lucent-1.18.2-1.2.2.jar`) API to emit smooth dynamic light (level `10–15` while firing, `5–6` for active pilot burner) from firing players, flame jet focal points, and active turrets.
  - **`Beta-5.10.17` (`1.20.1`):** Integrate with **Sodium/Embeddium Dynamic Lights** (`sodiumdynamiclights-forge-1.0.10-1.20.1.jar`) item/entity dynamic light hooks. Because `Beta-5.10.17`'s `sodiumdynamiclights-client.toml` defaults to `self = true`, `entities = false`, and `block_entities = false`, held-weapon dynamic lighting works out of the box while the Kinetic ChemThrower Turret MUST also emit real blockstate light (`lightLevel = 14` while firing, `5` when pilot is active) so base defenses illuminate reliably without requiring players to edit client config.
  - **Fallback:** When neither dynamic light mod is installed, full-bright particles + turret blockstate light + temporary ground fire light (`lightLevel = 12–15`) still provide immediate local illumination.
- **Mandatory Shader Validation Matrix:**
  Every visual release gate must be tested with **Oculus** ON and OFF against:
  1. **BSL Shaders**
  2. **Complementary Shaders — Reimagined** (bundled in `v5.5.5`)
  3. **Complementary Shaders — Unbound** + **Euphoria Patches** (Unbound bundled in `Beta-5.10.17`)
  4. **Photon Shader** (bundled in `Beta-5.10.17`)
  5. **Bliss Shaders** (bundled in `Beta-5.10.17`)
  6. **Spooklementary** (bundled in `Beta-5.10.17`)
  - Ensure zero particle wall-blinking (`Oculus Particle Fix` aware), zero black-box alpha artifacts, zero GeckoLib entity-shadow freezes, and clean rendering alongside **Colorwheel** (`Beta-5.10.17`) and **Distant Horizons** (`DH Edition`).

### 4.4 Layered Audio & Sound Physics Integration
- **Layered Sound Events (`assets/tacticalchemthrowers/sounds.json`):**
  1. `chemthrower.ignite` — sharp gas valve click + pressurized whoosh on trigger press.
  2. `chemthrower.fire_loop` — seamless managed looping roar (`TickableSoundInstance`, 1 instance per active firing player/turret, pitch subtly modulated by nozzle pressure/heat, deterministically stopped on release, empty tank, slot switch, death, or unload).
  3. `chemthrower.extinguish` — crisp pressurized hiss/vent on trigger release or dry-fire sputter when empty.
  4. `chemthrower.reload_eject` / `chemthrower.reload_lock` — metallic clamp release, canister hiss, and heavy bayonet lock-in during the `1.5s` canister swap.
  5. `turret.slew_loop` / `turret.pilot_idle` — subtle mechanical gear hum when tracking and faint low-volume pilot hiss when armed (distance-culled cleanly).
- **Sound Physics Remastered Compatibility:** Both packs bundle `Sound Physics Remastered`. Use mono `.ogg` audio files (`44.1 kHz` / `48 kHz`) for all 3D world-positioned sounds so spatial attenuation, indoor reverb, and wall occlusion work natively.

---

## 5. Functional Specification: Handheld Tactical ChemThrower

### 5.1 Modular Progression & Range Tiers
There is **one core handheld weapon**—the **Tactical ChemThrower** (`tacticalchemthrowers:tactical_chemthrower`)—which accepts **swappable nozzle/pressure upgrade modules** to unlock three effective range tiers:

| Tier | Installed Module (Original Naming) | Effective Range (Default) | Cone Spread | Visual / Mechanical Identity |
| --- | --- | --- | --- | --- |
| **Tier 1 (Base)** | *Standard Dispersion Nozzle* (built-in / default) | **15 blocks** | Wide close-quarters fan | Compact perforated barrel shroud; balanced room-clearing sweep |
| **Tier 2** | *Pressurized Focus Nozzle* (`tacticalchemthrowers:focus_nozzle_module`) | **25 blocks** | Medium tactical stream | Extended copper pressure manifold + brass collar + reinforced shroud |
| **Tier 3** | *High-Velocity Lance Nozzle* (`tacticalchemthrowers:lance_nozzle_module`) | **35 blocks** | Tight long-reach stream | Heavy double-jacketed lance barrel + secondary brass pressure regulator |

- Effective range is further scaled by the loaded fuel's `range_multiplier` (clamped by server config max range).
- Modules are swappable via a clean crafting/workbench/anvil/tinkering step (documented in §8) without losing the ChemThrower's durability, upgrades, or NBT metadata.

### 5.2 Firing Loop, Jet Geometry & Server-Authoritative Hit Detection
- **Trigger Control:** Holding **Right-Click** ignites and sustains a continuous pressurized flame jet as long as the loaded canister has fuel (`≥ consumption_mb_per_tick`), the player is not reloading, and the weapon is not submerged.
- **Underwater Prohibition:** Firing is strictly blocked if the player's eyes/nozzle origin are submerged in water (`isEyeInFluid(FluidTags.WATER)` / water fluid state at nozzle). Attempting to fire underwater emits bubble particles and a muffled valve-click sound without consuming fuel.
- **Jet Geometry & Line-of-Sight:**
  - Server computes a segmented raycast + expanding swept capsule (`JetGeometry`) originating from the player's eye/nozzle vector out to `effectiveRange`, terminating immediately at the first solid occluding block (accounting for liquid droop over distance).
  - Entities intersecting the unobstructed capsule segments are collected once per damage tick interval (e.g., every `4–5` ticks, `4–5` damage pulses/sec, configurable) so server TPS remains minimal even inside 100+ zombie hordes.
  - All hit validation, obstruction checks, fuel deduction, heat stacking, and damage application occur strictly on the server.

### 5.3 Combat Mechanics: Heat Ramp, Point-Blank Lava Bonus & Burn
- **Base Stream Fire Damage:** Deals continuous fire-typed damage scaled by fuel `damage_multiplier` and current heat multiplier.
- **Consecutive-Hit Heat Ramp (Locked):**
  - Each valid consecutive hit on a target adds **`+10%` damage** (`+0.10` per stack).
  - Stacks up to a maximum **`2.0x` multiplier** (reached at **10 consecutive hits**).
  - Resets cleanly back to `1.0x` after **`2.5 seconds` (`50 ticks`)** without taking a hit from the ChemThrower (tracked server-side per target entity via lightweight expiring `HeatTracker` entries—pruned automatically on expiry/entity death/unload).
- **Point-Blank Lava-Like Bonus (Locked):**
  - Targets hit at **`≤ 4.0 blocks`** from the nozzle receive an additional close-range **lava-like high-intensity thermal damage component** (separate higher-impact fire/lava damage profile representing direct unatomized burning liquid impact), rewarding high-risk close-quarters bracing while respecting fire immunity and armor mitigation.
- **Afterburn:** Every non-immune hit sets targets ablaze for **`3.0 seconds`** (`60 ticks`), refreshing on subsequent hits.
- **Temporary Ground Fire:**
  - Impacts on flammable/solid top block faces have a bounded chance (fuel- and config-dependent) to place a short-lived, custom **Temporary Flame Block** (`tacticalchemthrowers:temporary_fire`, default lifetime `3–5s`, non-spreading, zero block destruction/griefing by default).
  - Strictly checks claims, spawn protection, Adventure mode, `doFireTick` / server admin toggles, and replaceable block tags (never overwrites non-air/non-replaceable blocks, water, chests, machines, or protected regions).
  - Cleaned up deterministically via scheduled ticks and chunk-unload/server-shutdown safeguards so orphan fire blocks never persist.

### 5.4 Heavy Braced Stance & Recoil Feel (Locked)
- **Heavy Braced Creep While Firing:**
  - While actively firing, the operator enters a heavy braced stance: movement speed drops to **`~15%` of normal walk speed** (applied via a clean transient server/client `AttributeModifier` on `MOVEMENT_SPEED`, removed immediately on trigger release, slot change, or disconnect).
  - **Sprinting and jumping are disabled** while firing (enforcing deliberate crowd-control positioning and making the weapon feel authentically heavy).
- **Zero Camera Pitch Kick / Pure 1st-Person Weapon Recoil:**
  - Firing introduces **ZERO camera pitch/yaw kick**—the player's crosshair and camera view remain rock-steady for smooth hose-sweeping control across zombie crowds.
  - Recoil and thrust are communicated purely through **1st-person GeckoLib animation + procedural transform**: heavy backward gun + hands kickback on ignition, sustained high-frequency barrel/nozzle vibration while firing, subtle heat shimmer/valve rattle, and a weighty forward settle upon trigger release.
  - Third-person posture renders a two-handed braced hip-fire stance (compatible with `playerAnimator` and `Shoulder Surfing Reloaded`).

### 5.5 Canister-Only Reload System (Locked)
- **Reload Inputs:** Press **`R`** (dedicated configurable Forge `KeyMapping`, checked for conflict clarity with `Controlling`) **OR** **`Sneak + Right-Click`** while holding the ChemThrower.
- **Reload Duration:** **`1.5 seconds` (`30 ticks`)** server-authoritative timer with animated 1st/3rd-person canister unlatch, swap, and pressurized lock-in audio/visual sequence.
- **Canister-Only Rule:**
  - The handheld ChemThrower **cannot** be filled directly from pipes, spouts, or buckets. It reloads **strictly by swapping Pressurized Fuel Canisters** (`tacticalchemthrowers:fuel_canister`).
  - On reload completion, the server locates the best filled canister in the player's inventory (preferring matching fuel type or fullest valid fuel canister), swaps its fluid payload into the ChemThrower's active canister cradle, and **returns the spent/previous canister** (empty or partially filled) back to the player's inventory (or drops safely at player feet if inventory is completely full).
  - Canceling reload (switching hotbar slots, dropping item) aborts cleanly without losing fuel or duplicating canisters.

### 5.6 HUD & Tooltip Readability
- Minimal, crisp diegetic/HUD indicator shown **only while holding the ChemThrower**:
  - Loaded fuel name & color-coded bar (`0–50 units` / `0–1,000 mB`) + spare filled canister count in inventory.
  - Active nozzle range tier indicator (`15m` / `25m` / `35m`) and current reload progress bar when reloading.
  - Tooltips display loaded fuel type, `mB` & equivalent `units` (`50 units = 1,000 mB`), installed nozzle module, and keybind hints (`[R]` or `[Sneak + Right-Click]` to swap canister).

---

## 6. Functional Specification: Multi-Fuel & Canister Ecosystem

### 6.1 Fuel Unit Equivalence & Baseline Consumption (Locked)
- **Canister Capacity:** **`50 units` = `1,000 mB`** (`1 bucket`; exact conversion: `1 unit = 20 mB`).
- **Baseline Consumption:** **`4 mB/tick`** (`80 mB/sec` = `4 units/sec`), yielding exactly **`12.5 seconds`** (`250 ticks`) of continuous fire per full `1,000 mB` canister at `1.0x` consumption modifier.
- Higher- or lower-grade fuels modify consumption rate via their JSON `consumption_mb_per_tick` value.

### 6.2 Pressurized Fuel Canister (`IFluidHandlerItem`)
- **Item:** `tacticalchemthrowers:fuel_canister` (max stack size `1` when containing fluid; stackable up to `16` when completely empty for convenient Create Spout automation).
- **Capability Contract:**
  - Exposes Forge `IFluidHandlerItem` backed by `ItemStack` NBT (`1,000 mB` capacity).
  - Fillable automatically via **Create Spouts**, **Create Fluid Tanks / Item Drains / Pipes**, and **Immersive Engineering Bottling Machine / Fluid Tanks** (plus standard fluid containers/pipes like `Pipez`).
  - **Strict Validation:** `isFluidValid(FluidStack)` queries `FuelRegistry`; unregistered/non-fuel fluids are rejected.
  - **No Mixing Rule:** A partially filled canister ONLY accepts matching fluid (`FluidStack.isFluidEqual(...)`) until completely drained or explicitly flushed.
  - **Strict Simulation Compliance:** `FluidAction.SIMULATE` never mutates `ItemStack` NBT or emits sync packets.

### 6.3 Zero Duplicate Custom Fluids & Pack-Split Resolution
- **Zero Duplicate Custom Fluids:** This mod registers **ZERO duplicate custom fluids** (no redundant custom gasoline/diesel/ethanol fluids). It exclusively consumes fluids already provided by DeceasedCraft's installed tech mods.
- **Explicit Pack-Split Strategy (Resolving Old §5.2 Bug):**
  - **In `DeceasedCraft v5.5.5` (`1.18.2`):** `Create: Diesel Generators` is **NOT installed**. Fuels are supplied by **Immersive Petroleum** (`immersivepetroleum:gasoline`, `immersivepetroleum:diesel`, `immersivepetroleum:diesel_sulfur`, `immersivepetroleum:napalm`, `immersivepetroleum:crudeoil`), **Immersive Engineering** (`immersiveengineering:biodiesel`, `immersiveengineering:ethanol`, `immersiveengineering:creosote`), and **Create Crafts & Additions** (`createaddition:bioethanol`, `createaddition:seed_oil`).
  - **In `DeceasedCraft Beta-5.10.17` (`1.20.1`):** `Immersive Petroleum` is **NOT installed**. Fuels are supplied by **Create: Diesel Generators** (`createdieselgenerators:gasoline`, `createdieselgenerators:diesel`, `createdieselgenerators:biodiesel`, `createdieselgenerators:crude_oil`), **Immersive Engineering** (`immersiveengineering:biodiesel`, `immersiveengineering:ethanol`, `immersiveengineering:creosote`), and **Create Crafts & Additions** (`createaddition:bioethanol`, `createaddition:seed_oil`).
  - **KubeJS `material.js` Compliance (`Beta-5.10.17`):** Pack scripts remove CDG fermenter ethanol & plant oil production in favor of `createaddition:bioethanol` and `createaddition:seed_oil`. Because our fuel registry matches Forge fluid tags (`#forge:ethanol`, `#forge:biofuel`, `#forge:biodiesel`, etc.) AND explicit fallback fluid IDs, `createaddition:bioethanol` works seamlessly out-of-the-box without fighting KubeJS unification.
- **Coexistence with Immersive Engineering's Chemthrower:** Both packs ship IE's Chemthrower and Chemthrower Turret enabled. **Create: Tactical ChemThrowers** never disables, nerfs, or overrides IE's weapons; instead, it offers a distinct, Create-integrated tactical progression path (pressurized canister logistics, `15/25/35b` modular nozzles, `2.0x` heat-ramp combat, point-blank lava bonus, heavy braced stance, 4-stage blocky combustion VFX, and a Create kinetic + FE + fluid turret).

### 6.4 Data-Driven Fuel Registry (`data/tacticalchemthrowers/flamethrower_fuels/*.json`)
All fuel definitions are loaded from datapacks (reloaded via `/reload` and synced from server to client on login/reload via `SimpleChannel` so client tooltips, HUD colors, and particle profiles always match server rules).

- **Lookup Priority (Strict):**
  1. **Exact Fluid Registry ID** (`"fluid": "namespace:path"`) — highest priority for pack-specific overrides or specialty fuels.
  2. **Forge Fluid Tag** (`"fluid_tag": "forge:diesel"`) — primary cross-pack portability layer.
  3. **Reject** — unregistered fluids return `false` from `isFluidValid(...)`.
- **JSON Schema:**
  ```json
  {
    "fluid_tag": "forge:diesel",
    "consumption_mb_per_tick": 4,
    "damage_multiplier": 1.15,
    "range_multiplier": 1.05,
    "burn_duration_ticks": 60,
    "heat_gain_multiplier": 1.0,
    "ignites_targets": true,
    "ignites_blocks": true,
    "requires_pilot_light": true,
    "fuel_classification": "distillate",
    "particle_profile": {
      "core_color": "#FFF6B8",
      "flame_color": "#FF7A1A",
      "ember_color": "#C92A1D",
      "smoke_color": "#1E1D1C",
      "soot_factor": 0.75,
      "droop_factor": 0.025
    },
    "sound_profile": "standard_hydrocarbon"
  }
  ```
- **Default Accepted Fuel Profiles** (cross-checked against [RECIPE_AND_FLUID_AUDIT.md](compatibility/RECIPE_AND_FLUID_AUDIT.md)):

| Fuel Family (Tag / ID) | Pack Availability | Burn Rate (`mB/t`) | Damage Mult | Range Mult | Soot & Visual Character |
| --- | --- | :---: | :---: | :---: | --- |
| `#forge:plantoil` / `#forge:seed_oil` / `#forge:seedoil` (`createaddition:seed_oil`, `immersiveengineering:plantoil`) | Both packs *(CDG `plant_oil` recipe removed in `v6`)* | `3.4` (`0.85x`) | `0.65x` | `0.75x` | Emergency low-pressure vegetable oil: warm orange sputter, oily gray vapor |
| `#forge:ethanol` / `#forge:biofuel` (`createaddition:bioethanol`, `immersiveengineering:ethanol`) | Both packs | `5.0` (`1.25x`) | `0.85x` | `0.90x` | Clean pale blue-white core, low soot, fast low-droop spray |
| `#forge:creosote` (`immersiveengineering:creosote`) | Both packs | `4.0` (`1.00x`) | `0.90x` | `0.95x` | Heavy oily amber flame, thick dark coal-tar black smoke |
| `#forge:biodiesel` (`immersiveengineering:biodiesel`, `createdieselgenerators:biodiesel`) | Both packs | `4.0` (`1.00x`) | `1.05x` | `1.00x` | Balanced golden-orange baseline flame, moderate black smoke |
| `#forge:diesel` / `#forge:diesel_sulfur` (`immersivepetroleum:diesel*`, `createdieselgenerators:diesel`) | Both packs | `4.0` (`1.00x`) | `1.15x` | `1.05x` | High-energy sustained orange jet, pronounced soot plume |
| `#forge:kerosene` / `#forge:naphtha` / `#forge:benzene` (`immersivepetroleum:*`) | `v5.5.5` only | `4.0–4.6` | `1.10–1.20x` | `1.05–1.15x` | Clean pressurized industrial distillate jets (`kerosene` tight/clean, `benzene` aromatic soot) |
| `#forge:gasoline` (`immersivepetroleum:gasoline`, `createdieselgenerators:gasoline`) | Both packs | `5.0` (`1.25x`) | `1.25x` | `1.15x` | High-pressure volatile white-yellow roar, wide ignition flash |
| `#forge:napalm` (`immersivepetroleum:napalm`) | `v5.5.5` only | `4.0` (`1.00x`) | `1.40x` | `1.20x` | Heavy sticky ballistic droop, intense crimson-gold burn, dense black smoke |

- **Explicitly Rejected Fluids (Default):** Raw unrefined `#forge:crude_oil` (`immersivepetroleum:crudeoil`, `createdieselgenerators:crude_oil`) is rejected by default so players refine crude via DeceasedCraft's Distillation Tower (`v5.5.5`) or Create: Diesel Generators Distillation Controller (`Beta-5.10.17`)—pack admins can enable it via datapack if desired. `car:*` (disabled in `v5.5.5`), lava, molten metals, acids, lubricants, and water/food fluids are always rejected.

---

## 7. Functional Specification: Automated Kinetic ChemThrower Turret

### 7.1 Block & Fixed Industrial Port Layout (Locked)
The **Kinetic ChemThrower Turret** (`tacticalchemthrowers:chemthrower_turret`) is a 2-block-tall (or 1x1 heavy pedestal + animated gimbal head) Create kinetic block entity with **fixed, visually color-coded industrial ports** relative to the block's horizontal facing direction (when standing behind the turret looking toward its front barrel):

| Face (Relative to Facing) | Connection Type | Capability / API | Purpose & Visual Cue |
| --- | --- | --- | --- |
| **Left** | Create Rotational Input | `KineticBlockEntity` (`hasShaftTowards`) | Drives yaw/pitch gimbal slew speed (`RPM` scales tracking angular velocity; consumes configured `SU`, e.g., `4 SU/RPM` active, `1 SU/RPM` idle) — riveted iron shaft collar + brass gear housing |
| **Right** | Forge Energy Input | `IEnergyStorage` (`ForgeCapabilities.ENERGY`) | Powers targeting optics, electric spark igniter, and pressure solenoid (`FE/t` idle + firing draw; internal buffer e.g. `16,000 FE`) — insulated copper-coil terminal block |
| **Back + Bottom** | Create Fluid Pipe Input | `IFluidHandler` (`ForgeCapabilities.FLUID_HANDLER`) | Accepts pressurized liquid fuels from Create Fluid Pipes/Pumps, IE Pipes, or Pipez into internal `4,000 mB` tank (no fluid mixing; rejects non-fuels) — copper flanged pipe coupling |

- **Electrical Ecosystem Compatibility:** Using standard Forge Energy (`IEnergyStorage`) works natively with **Immersive Engineering** wires/capacitors, **Create Crafts & Additions** Alternators/Accumulators, **Pipez** energy pipes, and **Extreme Reactors** (`Beta-5.10.17`)—with zero assumptions about uninstalled electrical addons.

### 7.2 Interactions: GUI, Create Wrench & Engineer's Goggles
- **Right-Click GUI (Server-Synced `AbstractContainerMenu`):**
  - **Effective Range Slider:** Configurable up to the turret's max range (`default 20b`, configurable cap `30b`). Configured target acquisition distance strictly aligns with effective flame jet travel distance (avoiding the mismatch where turrets lock targets outside actual flame reach).
  - **Target Filter Toggles:** Hostile Mobs (default ON), Neutral Mobs (default OFF), Players (default OFF — respects PvP, owner, `FTB Teams` allies, and `Open Parties & Claims`), Bosses (default ON), plus explicit entity-ID/tag allow/deny filter list.
  - **Operating Mode:** `ACTIVE` (pilot lit, auto-engage), `STANDBY` (pilot lit, holds fire), `MAINTENANCE / OFF` (pilot extinguished, zero FE/SU draw, safe for wrenching/piping).
  - **Live Status Readout:** Current fuel type & `mB`, FE buffer, kinetic `RPM`/`SU` state, and explicit diagnostic badges (`NO FUEL`, `NO POWER`, `NO ROTATION`, `UNDERWATER`, `MAINTENANCE OFF`).
- **Create Wrench Interaction:**
  - Right-clicking with a Create Wrench (checking both Create's wrench and `#forge:tools/wrench` tag for cross-mod convenience) rotates turret facing cleanly; `Sneak + Right-Click` picks up the turret safely (preserving configuration NBT and draining or retaining tank state per Create convention).
- **Create Engineer's Goggles (`IHaveGoggleInformation`):**
  - Looking at the turret while wearing Engineer's Goggles displays live industrial telemetry: Mode (`Active`/`Standby`/`Off`), Fuel (`mB / 4,000 mB` + fuel name), Kinetic Input (`RPM`, `SU` impact, slew rate), Forge Energy (`FE / 16,000 FE`), and current target lock / fault warning.

### 7.3 Targeting, Slew Physics & Safety
- **Bounded Target Scanner:** Never scans all entities every tick. Queries entities within an AABB bounded by configured range every **`10 ticks`** (`0.5s`, staggered by block-pos hash to prevent tick spikes when multiple turrets exist), validates line-of-sight and protection rules, and caches the locked target.
- **Kinetic Slew Tracking:** Gimbal smoothly interpolates yaw/pitch toward the target at an angular velocity proportional to input `|RPM|` (clamped between minimum operational RPM e.g. `16 RPM` and max `256 RPM`). The turret only opens the fuel valve once the barrel vector aligns within a tight cone (`≤ 8°`) of the target and clear line-of-sight is verified.
- **Shared Combat & Fuel Backend:** Reuses the exact same `FuelRegistry`, `JetGeometry`, `HeatTracker`, `TemporaryFire`, and `ParticleProfile` systems as the handheld ChemThrower, ensuring identical combat feel, night glow, and shader behavior.
- **Fail-Safe Shutdown:** Turret immediately extinguishes and stops firing if fuel runs dry, FE depletes, RPM drops below threshold (or overstressed), mode is set to `OFF`, block is submerged in water, or the chunk unloads.

---

## 8. Progression, Crafting & Loot Integration

### 8.1 DeceasedCraft Tech Tiering
Create: Tactical ChemThrowers is positioned in **mid-to-late DeceasedCraft survival progression**, rewarding players who have established Create rotational factories and Immersive Engineering steel/fluid refining rather than trivializing early-game scavenging:

- **Core Materials & Pack Recipe Rule:** Create **Brass Sheets/Casings**, **Copper Sheets/Fluid Pipes**, **Precision Mechanisms** (or Sturdy Sheets), and **Immersive Engineering Steel Ingots/Plates/Rods** (`#forge:plates/steel`, `#forge:ingots/steel`, `#forge:plates/brass`, `#forge:plates/copper` — using Forge tags so pack unification works identically across `v5.5.5` and `Beta-5.10.17`). **CRITICAL:** Both DeceasedCraft packs globally replace `create:electron_tube` with `immersiveengineering:component_electronic` (`material.zs` in `v5.5.5`, `material.js` in `Beta-5.10.17`)—use `immersiveengineering:component_electronic` / `component_electronic_adv` (with `forge:mod_loaded` standalone fallback to `create:electron_tube` if IE is absent) rather than raw `create:electron_tube`.
- **Crafting Pathways:**
  - **Tactical ChemThrower & Kinetic Turret:** Crafted via **Create Mechanical Crafting** (5x5 or 4x4 industrial assembly layout), with a standard 3x3 Forge fallback recipe only if Mechanical Crafting is disabled in config.
  - **Pressurized Fuel Canister:** Sequenced Assembly / Shaped Crafting from Copper Sheet + Steel Plate + Create Fluid Valve/Pipe.
  - **Nozzle Upgrade Modules (`Focus` 25b & `Lance` 35b):** Crafted via Create Mechanical Crafting / Sequenced Assembly using Steel, Brass, Blaze/Igniting components, and **also discoverable as rare high-tier loot**.
- **Rare Military & Lab City Loot (Lootr-Safe):**
  - Inject rare **Nozzle Modules**, pre-filled **Pressurized Fuel Canisters**, and ultra-rare damaged/blueprint **ChemThrower components** into Lost Cities military bunker and lab loot tables via **Forge Global Loot Modifiers (GLMs)**.
  - Using standard GLMs works seamlessly both when **Lootr** is active (`v5.5.5` and `Beta-5.10.17` multiplayer servers) and when Lootr is disabled by default (`Beta-5.10.17` singleplayer `lootr-common.toml: disable = true`), with zero Lootr mixin hacks.
- **Additive Recipe Discipline:** All recipes are purely additive datapack JSONs checked against `RECIPE_AND_FLUID_AUDIT.md`. Never override or delete existing DeceasedCraft/KubeJS recipes.

---

## 9. Combat Rules, World Protection & Soft Optional Hooks

### 9.1 Core Combat & World-Rule Compliance
The ChemThrower and Turret must strictly respect all vanilla, Forge, and DeceasedCraft rules:
- Fire immunity (`Entity.fireImmune()`), Fire Resistance potion effects, armor/enchantments, and DeceasedCraft **Armor Set Bonuses** (e.g., Firefighter armor set heat/fire protections audited in [COMBAT_AND_PROTECTION_AUDIT.md](compatibility/COMBAT_AND_PROTECTION_AUDIT.md)).
- Adventure mode restrictions, vanilla spawn protection, server `pvp=false` settings, entity invulnerability, and boss immunities.
- Temporary fire respects `doFireTick`, block flammability/replaceability, and server-admin kill switches (`allowBlockIgnition`, `allowPlayerDamage`).

### 9.2 Soft Optional Mod Bridges (Runtime-Detected)
All third-party integrations below are soft optional (`ModList.get().isLoaded(...)`), fail-safe, and individually toggleable in server config:

| Target Mod | Pack(s) | Integration Behavior |
| --- | --- | --- |
| **Open Parties & Claims** | Both | Query chunk claim ownership & party ally permissions before applying PvP damage or placing temporary fire blocks (for both player-held and owner-tagged turret fire). |
| **FTB Teams** | Both | Respect team membership for friendly-fire filtering on turrets and PvP checks. |
| **Zombie Awareness** | Both | Emit calibrated light and sound awareness stimuli when firing the ChemThrower or running an active turret—creating intense risk/reward horde attraction at night. |
| **Cold Sweat** | `v5.5.5` | Apply a subtle, bounded localized body-temperature warmth bonus while actively firing or standing directly beside an active pilot/firing turret (capped so firing never causes unfair instant hyperthermia). |
| **Legendary Survival Overhaul** | `Beta-5.10.17` | Equivalent subtle, bounded localized temperature warmth hook matching `Cold Sweat` behavior on `1.20.1`. |
| **Lucent** | `v5.5.5` | Dynamic light registration for active ChemThrower firing, flame stream focal illumination, and active turret. |
| **Sodium/Embeddium Dynamic Lights** | `Beta-5.10.17` | Dynamic light provider registration matching `Lucent` behavior on `1.20.1`. |

---

## 10. Networking, Persistence & Configuration

### 10.1 Compact Networking (`SimpleChannel`)
Never transmit individual particle positions over the network. Synchronize compact, rate-limited state transitions:
- `C2S_ChemThrowerActionPacket` — trigger start/stop, reload request (`R`), validated server-side against held item, underwater state, fuel, and cooldowns.
- `S2C_ChemThrowerStreamStatePacket` — compact broadcast to nearby tracking players (`entityId`, `isFiring`, `fuelIdHash`, `impactDistance`, `tier`) so clients render smooth predicted 4-stage particle streams and managed audio loops locally.
- `S2C_FuelRegistrySyncPacket` — syncs parsed datapack fuel definitions to clients on login and `/reload`.
- `C2S_TurretConfigPacket` — validates menu ownership/distance and updates turret range, target filter flags, and operating mode.
- `S2C_TurretStateSyncPacket` — syncs turret aim yaw/pitch target, firing flag, mode, fuel `mB`, FE, and fault flags only on meaningful threshold changes or menu open.

### 10.2 Persistence
- **Handheld ChemThrower NBT:** Stores loaded `FluidStack` (`FluidName` + `Amount` up to `1,000 mB`), installed `NozzleModule` ID, and reload state (reset cleanly if interrupted).
- **Pressurized Fuel Canister NBT:** Standard Forge `Fluid` compound serialized via `IFluidHandlerItem`.
- **Turret BlockEntity NBT:** Saves `FluidTank`, `EnergyStorage`, owner `UUID`, range setting, filter flags/lists, operating mode, and current yaw/pitch in `saveAdditional()` / `load()` (and exposes minimal sync payload in `getUpdateTag()`).

### 10.3 Configuration Specification (Validated & Clamped)
Split cleanly into **Server Config** (`tacticalchemthrowers-server.toml`, synced with world) and **Client Config** (`tacticalchemthrowers-client.toml`):

- **Server Config (Gameplay, Balance & Admin Controls):**
  - `weapon.rangeTier1` (`15`, clamp `5–48`), `weapon.rangeTier2` (`25`, clamp `5–48`), `weapon.rangeTier3` (`35`, clamp `5–64`)
  - `weapon.canisterCapacityMb` (`1000`, `= 50 units`, clamp `200–4000`)
  - `weapon.baseConsumptionMbPerTick` (`4`, clamp `1–50`)
  - `weapon.reloadDurationTicks` (`30` = `1.5s`, clamp `5–100`)
  - `combat.baseFireDamage` (configurable float), `combat.pointBlankDistance` (`4.0`, clamp `1.0–8.0`), `combat.pointBlankLavaBonusDamage` (configurable float)
  - `combat.heatGainPerHit` (`0.10`), `combat.heatMaxMultiplier` (`2.0`, clamp `1.0–5.0`), `combat.heatResetTicks` (`50` = `2.5s`, clamp `10–200`)
  - `combat.burnDurationTicks` (`60` = `3.0s`, clamp `0–200`)
  - `combat.firingWalkSpeedMultiplier` (`0.15`, clamp `0.05–1.0`), `combat.disableJumpAndSprintWhileFiring` (`true`)
  - `safety.allowTemporaryFire` (`true`), `safety.temporaryFireLifetimeTicks` (`80`, clamp `10–400`), `safety.allowPlayerDamage` (`true`), `safety.respectClaimsAndTeams` (`true`)
  - `turret.maxRange` (`20`, clamp `8–40`), `turret.minRpm` (`16`), `turret.stressPerRpmActive` (`4.0`), `turret.fePerTickFiring` (`40`), `turret.tankCapacityMb` (`4000`), `turret.scanIntervalTicks` (`10`, clamp `4–40`)
  - `compat.enableZombieAwarenessAggro` (`true`), `compat.enableTemperatureWarmth` (`true`), `compat.enableProtectionHooks` (`true`)
- **Client Config (Visuals & Budgets):**
  - `vfx.globalParticleSoftCap` (`350`, clamp `50–1000`), `vfx.globalParticleHardCap` (`600`, clamp `100–1500`)
  - `vfx.lodReduceDistance` (`24`), `vfx.lodCullDistance` (`48`)
  - `vfx.enableDynamicLights` (`true`), `vfx.recoilAnimationIntensity` (`1.0`, clamp `0.0–1.5`)
  - `hud.showFuelOverlay` (`true`)

---

## 11. Performance Engineering & Profiling Plan

Performance must be empirically measured with `spark` and frame-time captures on both target packs before release.

### 11.1 Mandatory Profiling Scenarios
1. Idle ChemThrower held in hand (zero firing particles, zero ticking overhead).
2. Continuous firing for a full `12.5s` canister in open terrain at night (shaders OFF and ON).
3. Four players firing ChemThrowers simultaneously in multiplayer.
4. Four active Kinetic ChemThrower Turrets tracking and firing in one loaded chunk cluster.
5. Dense DeceasedCraft zombie horde (`60+` active undead entities in Lost Cities).
6. Minecraft Particle settings: `ALL`, `DECREASED`, and `MINIMAL`.
7. Rapid chunk border crossing and chunk unload/reload while firing and with active temporary fire.
8. Multiplayer with simulated `150ms` latency (verifying server authority and smooth client VFX).
9. Dedicated server soak test (`30+` minutes) checking TPS stability, heap growth, and zero orphan fire blocks.
10. Constrained/integrated-graphics client profile with shaders enabled (BSL / Complementary / Photon).

### 11.2 Acceptance Criteria
- Zero crashes, deadlocks, memory leaks, or orphaned temporary fire blocks/sound loops across all 10 scenarios.
- Active mod particles never exceed `vfx.globalParticleHardCap`.
- Server tick impact remains bounded and negligible under dense hordes and multi-turret loads.
- Exact numeric FPS / frame-time budgets will be recorded in `PERFORMANCE_BUDGET.md` once baseline profiles are captured on the target DeceasedCraft instances.

---

## 12. Asset & Documentation-First Engineering Pipeline

### 12.1 Documentation-First Workflow
Before implementing any Minecraft, Forge, Create, GeckoLib, IE, or shader/rendering subsystem, coding agents MUST consult primary documentation and official reference repositories indexed in `docs/references/`:
- [Notebook 1 — Core Forge, Multi-Version Templates, GeckoLib, Flywheel & AI Tooling](docs/references/flmthrwr_notebook_1_overview.md)
- [Notebook 2 — Create Kinetics, Fluids, Diesel Generators & Multi-Fuel Patterns](docs/references/flmthrwr_notebook_2_overview_links.md)
- [Notebook 3 — Weapon/Turret Architectures, Rendering, Audio & Profiling](docs/references/flmthrwr_notebook_3_overview_links.md)
- [Notebook 4 — Petroleum, Industrial Fuels & Combustion Properties](docs/references/flmthrwr_notebook_4_overview_links.md)

Never guess API signatures across `1.18.2` vs `1.20.1`, Create `0.5.1.f` vs `6.0.6`, or GeckoLib `3` vs `4`.

### 12.2 Verified 2D & 3D Asset Generation Toolchain
Do not hand-code raw PNG bytes or hand-type raw GeckoLib `.geo.json` bone/UV geometry when dedicated deterministic tools are installed:

- **2D Textures, Particle Strips & LabPBR Maps (`mc-asset` CLI):**
  - Use `mc-asset` (installed via `tools/setup_asset_tools.sh`) for all 16x16 / 32x32 item textures, GUI sprites, 4-stage blocky flame/smoke animated particle strips + `.mcmeta` files, and LabPBR `_s` emissive/specular maps.
  - Validate every generated texture and animation strip with `mc-asset validate`.
- **3D GeckoLib Models, Animations & Visual QA (`blockbench-mcp`):**
  - Use headless Blockbench Desktop + `sosadly/blockbench-mcp` invoked through [`tools/bb_mcp_client.mjs`](tools/bb_mcp_client.mjs) (setup documented in [`tools/README.md`](tools/README.md)) to construct `.bbmodel` projects, UV-map textures, author GeckoLib 3/4 animations (idle, ignite, fire kickback/vibrate, canister reload, turret slew/recoil), export `.geo.json` + `.animation.json`, and capture multi-angle PNG screenshots for visual inspection before committing.
- **Audio Production:**
  - Author or synthesize original mono `.ogg` assets cleanly via Audacity/FFmpeg workflows and register in `sounds.json`.

---

## 13. Testing & Release Gates

A target build is not releasable until all applicable gates pass on the exact named DeceasedCraft pack release.

### Gate A — Inventories, Pack Audits & Toolchain Foundation *(Completed for v5.5.5 & Beta-5.10.17)*
- [x] Exact official CurseForge archives downloaded and SHA-256 hashed (`5525524`, `8448820`, `8448903`).
- [x] Separate complete mod inventories generated and reconciled 100% (`224` mods for `v5.5.5`, `306 + 1` mods for `Beta-5.10.17`).
- [x] Cross-version ecosystem matrix, recipe/fluid audit, combat/protection audit, and API research documented in `compatibility/`.
- [x] `mc-asset` and headless `blockbench-mcp` tooling configured and smoke-tested in `tools/`.

### Gate B — Handheld Functional Behavior
- [ ] Continuous right-click firing, stop-on-release, and underwater lockout verified.
- [ ] `50 units = 1,000 mB` canister capacity and `4 mB/tick` (`12.5s`) baseline burn rate verified.
- [ ] Canister-only reload (`R` and `Sneak+Right-Click`, `1.5s`, spent canister returned) verified; direct gun filling rejected.
- [ ] Modular range tiers (`15 / 25 / 35` blocks) and visual barrel swaps verified.
- [ ] Heat ramp (`+10%`/hit up to `2.0x`, `2.5s` reset), `≤4b` point-blank lava bonus, and `3s` burn verified.
- [ ] Heavy Braced Creep (`~15%` walk speed, no sprint/jump) and zero camera pitch kick / pure 1st-person gun+hands recoil verified.
- [ ] Temporary ground fire cleanup, non-griefing safety, and protection/claim/PvP/Adventure compliance verified.

### Gate C — Ecosystem & Turret Integrations
- [ ] Pressurized Fuel Canister `IFluidHandlerItem` filling tested via Create Spouts, Create Tanks/Pipes, IE Bottling Machine/Tanks, and Pipez (no fluid mixing).
- [ ] Multi-fuel datapack registry tested with `Immersive Petroleum` + `IE` + `Create Crafts & Additions` on `v5.5.5`, and `Create: Diesel Generators` + `IE` + `Create Crafts & Additions` (post-KubeJS `material.js`) on `Beta-5.10.17`.
- [ ] Coexistence with IE Chemthrower and IE Chemthrower Turret verified on both packs.
- [ ] Automated Turret fixed ports (**Left** Create Shaft, **Right** FE, **Back+Bottom** Fluid), right-click GUI, Create Wrench, and Engineer's Goggles telemetry verified on both Create `0.5.1.f` and Create `6.0.6`.
- [ ] Lootr-safe GLM military/lab loot generation verified in Lost Cities chests.
- [ ] Soft optional hooks verified both present and absent (`Open Parties & Claims`, `FTB Teams`, `Zombie Awareness`, `Cold Sweat` / `LSO`, `Lucent` / `Sodium Dynamic Lights`).

### Gate D — Visuals, Shaders, Performance & Multiplayer
- [ ] 4-stage blocky fire-to-black-smoke VFX, night glow, LabPBR `_s`, and dynamic lights verified with **BSL**, **Complementary (Reimagined / Unbound + Euphoria)**, **Photon**, **Bliss**, and **Spooklementary** (+ Distant Horizons Edition).
- [ ] All 10 profiling scenarios completed and recorded in `PERFORMANCE_BUDGET.md` and `compatibility/TEST_RESULTS.md`.
- [ ] Dedicated server startup, client/server parity, packet validation, and chunk unload cleanup verified on both `1.18.2` and `1.20.1`.

### Gate E — Packaging & Release Hygiene
- [ ] Separate versioned JARs built for `1.18.2 (Forge 40.2.4)` and `1.20.1 (Forge 47.4.0)`.
- [ ] EULA/originality scan passes with zero prohibited names or unoriginal assets.
- [ ] Server-admin controls, config defaults, fuel datapack schema, and known beta caveats documented for players and server owners.

---

## 14. Resolved Inconsistencies & Remaining Open Questions

### 14.1 Resolved Contradictions (Superseding `SPECS_updated.md` & Notebooks 1–4)

| # | Prior Contradiction / Ambiguity | Locked Resolution in `SPECS.md` |
| --- | --- | --- |
| 1 | `SPECS_updated.md` §7 marked both mod inventories as *"Pending / RESEARCH GATE"* while §16 already listed all 224 and 307 mods. | Both official archives are extracted, SHA-256 verified, and exported to `compatibility/inventory/*.csv` + 4 audit documents in `compatibility/`. |
| 2 | `SPECS_updated.md` §5.2 assumed `Create: Diesel Generators` as a core cross-pack dependency, but `v5.5.5` only has `Immersive Petroleum` while `Beta-5.10.17` only has `Create: Diesel Generators` (and removes CDG fermenter ethanol/plant oil in KubeJS `material.js`). | Zero hard dependency on either addon and zero duplicate custom fluids. Data-driven `flamethrower_fuels/*.json` (exact ID → Forge fluid tag → reject) bridges both packs cleanly and natively supports `createaddition:bioethanol`. |
| 3 | IE Chemthrower presence/configuration in DeceasedCraft was left unverified. | Confirmed enabled in both packs; **Create: Tactical ChemThrowers** coexists alongside IE without overriding or disabling IE items. |
| 4 | Range tiers (`15 / 25 / 35` blocks) were ambiguous between 3 separate weapons, modules, or config variants. | Locked to **1 modular handheld ChemThrower** upgraded via swappable nozzle/pressure modules (`15 → 25 → 35` blocks). |
| 5 | Fuel units (`50 units` vs `mB`) and reload mechanism (direct gun pipe filling vs canister/bottle swap) conflicted across `SPECS_updated.md`, Notebook 2, and Notebook 3. | Locked: **`50 units = 1,000 mB`**, `4 mB/tick` (`12.5s` burn), **canister-only reload** (`R` or `Sneak+Right-Click`, `1.5s`, returns spent canister). Only the Pressurized Fuel Canister implements `IFluidHandlerItem`. |
| 6 | Heat ramp (`+10%`, `2x / 2.5s`) and close-range lava-like bonus threshold were ambiguous (`SPECS_updated.md` §14 Q1–Q2). | Locked: `+10%`/hit up to **`2.0x` max** (10 hits), resetting after **`2.5s`** without hit; **`≤ 4 blocks`** triggers point-blank lava-like bonus + `3s` burn. |
| 7 | Turret electrical API and side/port mapping were provisional (`SPECS_updated.md` §6.1–6.2, §14 Q6–Q7). | Locked: standard **Forge Energy (`IEnergyStorage`)**; fixed ports **Left = Create Shaft**, **Right = FE**, **Back + Bottom = Fluid Pipe**; right-click GUI, Create Wrench, Engineer's Goggles telemetry. |
| 8 | Notebooks referenced Create `0.5.1` and GeckoLib 4 without separating `v5.5.5` (`Create 0.5.1.f`, `GeckoLib 3.0.57`) from `Beta-5.10.17` (`Create 6.0.6`, `GeckoLib 4.7`). | Isolated strictly into version-specific adapter modules (`1.18.2` vs `1.20.1`). |
| 9 | Flame VFX style, night illumination, shader compatibility, stance/recoil feel, and survival-mod interactions were unspecified. | Locked: 4-stage crisp blocky billboard particles (`0.18–0.55b`) to black hydrocarbon smoke, `FULL_BRIGHT` + LabPBR `_s` + `Lucent`/`Sodium Dynamic Lights`, 6-shader Oculus matrix, `~15%` heavy braced stance, zero camera pitch kick (1st-person gun+hands recoil only), and soft survival/protection bridges. |
| 10 | Working title was generic and Notebook 3 referenced historical real-world weapon designations. | Locked official name **Create: Tactical ChemThrowers** (`tacticalchemthrowers`) with strict EULA & zero-real-world-brand / zero-copyrighted-IP naming rules. |

### 14.2 Remaining Open Items (Strictly Runtime-Dependent)
Only items that genuinely require running code or future external releases remain open—do not fabricate values prematurely:
1. **Numeric FPS & Frame-Time Budgets (`PERFORMANCE_BUDGET.md`):** Establish exact numerical millisecond/FPS acceptance thresholds after capturing clean baseline profiles on both DeceasedCraft instances (Gate D).
2. **Exact Base Damage Tuning Constants:** Finalize exact float values for `combat.baseFireDamage` and `combat.pointBlankLavaBonusDamage` during playtesting against DeceasedCraft zombie health/armor scaling (`The Hordes`, `Zombie Extreme`, `THE UNDEAD REVAMPED`) in both packs.
3. **Final DeceasedCraft `v6.0` Release Validation:** Re-run archive extraction and compatibility audits if a final `v6.0` release supersedes `Beta-5.10.17` prior to release.

---

## 15. Definition of Done

**Create: Tactical ChemThrowers** is complete only when:
- Both `1.18.2 (Forge 40.2.4)` and `1.20.1 (Forge 47.4.0)` artifacts build cleanly and pass Gates A–E against the exact DeceasedCraft `v5.5.5` and `Beta-5.10.17` (Standard + DH Edition) releases.
- The modular handheld ChemThrower delivers the locked firing, canister-only reload, `15/25/35b` module, `2.0x/2.5s` heat ramp, `≤4b` point-blank lava bonus, `~15%` braced stance, zero-pitch-kick 1st-person recoil, and 4-stage blocky fire-to-black-smoke VFX experience.
- The Kinetic ChemThrower Turret operates reliably across Create Shaft, Forge Energy, and Create Fluid Pipe ports with full GUI, Wrench, and Engineer's Goggles support.
- All fuels interoperate cleanly via data-driven JSON + Forge capabilities without duplicating fluids or conflicting with pack KubeJS scripts.
- Shader compatibility (BSL, Complementary Reimagined/Unbound + Euphoria, Photon, Bliss, Spooklementary), dynamic lighting, multiplayer authority, and profiled performance budgets are empirically verified.
