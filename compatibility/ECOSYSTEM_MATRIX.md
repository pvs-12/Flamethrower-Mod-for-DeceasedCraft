# DeceasedCraft Ecosystem Matrix — Create: Tactical ChemThrowers

**Mod ID:** `tacticalchemthrowers`  
**Targets:** DeceasedCraft `v5.5.5` (`MC 1.18.2` Forge) & DeceasedCraft `Beta 5.10.17` (`MC 1.20.1` Forge — Standard & Distant Horizons Editions)  
**Verification Basis:** Direct inspection of official CurseForge pack archives (`manifest.json`, `overrides/`), verified mod metadata (`categorized_mods.json`), and SHA-256 checksums.  
**Full Machine-Readable Inventories:**
- [`deceasedcraft-5.5.5-1.18.2.csv`](inventory/deceasedcraft-5.5.5-1.18.2.csv) — **224** mods
- [`deceasedcraft-beta-5.10.17-1.20.1.csv`](inventory/deceasedcraft-beta-5.10.17-1.20.1.csv) — **307** mods (`306` Standard + `1` DH Edition Extra)

---

## 1. Official Archive Provenance

All mod counts, JAR filenames, CurseForge IDs, and configuration values in this document are verified directly against the three official CurseForge release archives (Project ID `490660`). Zero unlisted JARs exist in `overrides/` in any archive.

| Field | DeceasedCraft v5.5.5 | DeceasedCraft Beta 5.10.17 (Standard) | DeceasedCraft Beta 5.10.17 (DH Edition) |
| --- | --- | --- | --- |
| **Archive Filename** | `DeceasedCraft-5.5.5.zip` | `DeceasedCraft_Beta-5.10.17.zip` | `DeceasedCraft_Beta_DH_Edition-5.10.17.zip` |
| **CurseForge Project / File ID** | `490660` / `5525524` | `490660` / `8448820` | `490660` / `8448903` |
| **Manifest `name` / `version`** | `DeceasedCraft` / `5.5.5` | `DeceasedCraft_Beta` / `5.10.16`<sup>1</sup> | `DeceasedCraft_Beta_DH_Edition` / `5.10.16`<sup>1</sup> |
| **Minecraft Version** | `1.18.2` | `1.20.1` | `1.20.1` |
| **Forge Loader** | `forge-40.2.4` | `forge-47.4.0` | `forge-47.4.0` |
| **Java Toolchain Target** | Java 17 | Java 17 | Java 17 |
| **Manifest `recommendedRam`** | *(not set)* | `6144` MB | `10240` MB |
| **SHA-256 Digest** | `e93668e97a8061bebfdf16424bc3a1702f262b142cbf13ecd3b165eb246a9f1b` | `870ca9d83b05d9aaa3be032c0b741f46349acf8a8561666f93cf96b30645eb61` | `d5c74a514f42ec3329188f6eb6044b8e873012555014663732ac8ddb82bf4774` |
| **Manifest Entries Total** | **230** | **317** | **318** |
| **Actual Mods (`.jar`)** | **224** | **306** | **307** (`306` Standard + `1` DH Extra) |
| **Manifest Resource Packs** | **4** | **7** | **7** |
| **Manifest Shader Packs** | **2** | **4** | **4** |
| **Override Resource Packs** | **1** (`Quark Programmer Art.zip`) | **3** (`Lopy-Create-Pipez.zip`, `MandalasGUI+Dakmode_1.20.1.zip`, `Quark Programmer Art.zip`) | **3** *(identical to Standard)* |
| **Override Shader Presets** | **0** | **2** (`photon_v1.2a.zip.txt`, `photon_v1.2a + Clrwl_1.0.3.zip.txt`) | **2** *(identical to Standard)* |
| **Total ZIP Entries** | `4,733` | `6,449` | `6,449` |
| **Shared Mods Between Packs** | **151** (of 380 unique mods across both branches) | **151** | **151** |

<sup>1</sup> *Provenance note:* Both `DeceasedCraft_Beta-5.10.17.zip` and `DeceasedCraft_Beta_DH_Edition-5.10.17.zip` declare `"version": "5.10.16"` inside `manifest.json` despite being published on CurseForge as `5.10.17`. Byte-for-byte comparison confirms the Standard and DH Edition archives have **100% identical `overrides/`**; only `manifest.json` (adding `Distant Horizons`, Project `508933` / File `7375280`, and raising `recommendedRam` to `10240`) and `modlist.html` differ.

---

## 2. Side-by-Side Integration-Critical Ecosystem Matrix

### 2.1 Create & Create Addons

| Mod | Project ID | v5.5.5 (`1.18.2`) JAR & File ID | Beta 5.10.17 (`1.20.1`) JAR & File ID | Integration Surface & Impact |
| --- | :---: | --- | --- | --- |
| **Create** | `328085` | `create-1.18.2-0.5.1.f.jar` (`4835188`) | `create-1.20.1-6.0.6.jar` (`6641603`) | **MAJOR API BREAK:** `0.5.1.f` (Flywheel `0.6.x`) vs `6.0.6` (Flywheel `1.0.x` + Ponder split + refactored kinetic/registrate/fluid APIs). Provides mechanical rotation (SU), fluid pipes/tanks/pumps, Mechanical Crafting, Sequenced Assembly, Spout filling. |
| **Create Crafts & Additions** | `439890` | `createaddition-1.18.2-1.0.0.jar` (`4683727`) | `createaddition-1.20.1-1.3.2.jar` (`6901922`) | Primary Create-native Forge Energy (`IEnergyStorage`) bridge (Alternator, Electric Motor, Wires/Connectors, Accumulator) in **both** packs. Also provides `createaddition:bioethanol` and `createaddition:seed_oil`. |
| **Create Big Cannons** | `646668` | `createbigcannons-forge-1.18.2-0.5.3.b.jar` (`5000111`) | `createbigcannons-5.9.1-mc.1.20.1-forge.jar` (`6696635`) | Coexisting Create ordnance mod. Uses Mechanical Crafting & steel/nethersteel alloys. v6 adds `Ritchie's Projectile Library` (`1279407`, `ritchiesprojectilelib-2.1.0+mc.1.20.1-forge.jar`, `6612420`). |
| **Create: Diesel Generators** | `869316` | *Not installed* | `createdieselgenerators-1.20.1-1.3.5.jar` (`6920093`) | **v6 only.** Primary petroleum refining & fuel ecosystem (`crude_oil`, `diesel`, `gasoline`, `biodiesel`, Pumpjack, Distillation Controller, Canisters `4000 mB`). Replaces Immersive Petroleum from `5.5.5`. |
| **Create: Radars** | `1152836` | *Not installed* | `Radars 0.3.5.1-Create6.jar` (`7334729`) | **v6 only.** Create 6 radar/guidance addon (`radarLinkRange=128`, `radarBaseRange=20`, `radarFOV=90`). Optional future target-guidance interop for automated flamethrower turret; never a hard dependency. |
| **Create Stuff 'N Additions** | `466792` | `create-stuff-additions1.18.2_v2.0.4a.jar` (`4703282`) | `create-stuff-additions1.20.1_v2.1.0.jar` (`6412397`) | Adds portable fuel/steam tanks & tools. v6 pairs it with `CreateStuffAdditions Fix` (`1006676`, `createstuffadditionsfix-forge-1.20.1-0.0.0.1.jar`, `5278566`). Note: `create_sa:copper_propeler_recipe` removed in 5.5.5; brass armor removed in v6. |
| **Create Deco** | `509285` | `createdeco-1.3.3-1.18.2.jar` (`4554163`) | `createdeco-2.0.3-1.20.1-forge.jar` (`6373226`) | Decorative industrial blocks/sheets/catwalks; zero fluid/API conflicts. |
| **Create: Central Kitchen** | `820977` | `create_central_kitchen-1.18.2-for-create-0.5.1.f-1.3.9.d.jar` (`4970407`) | `create_central_kitchen-1.20.1-for-create-6.0.6-1.4.3b.jar` (`6987710`) | Food/Farmer's Delight Create bridge; verifies exact Create build compatibility (`0.5.1.f` vs `6.0.6`). |
| **Create: Steam 'n' Rails** | `688231` | `Steam_Rails-1.4.8+forge-mc1.18.2-build.23.jar` (`4944929`) | *Not installed* | 5.5.5 train addon (excluded in v6 due to Create 6 port status). |
| **Create: Hypertubes** | `1281336` | *Not installed* | `create_hypertube-0.2.5-FORGE.jar` (`6878308`) | v6 transport addon; no fluid/weapon conflict. |
| **Create: Interiors** | `906239` | *Not installed* | `interiors-0.5.6+forge-mc1.20.1-local.jar` (`6301533`) | v6 seating/decor addon; no conflict. |
| **Create Better FPS** | `1217518` | *Not installed* | `createbetterfps-1.20.1-1.1.1.jar` (`6716449`) | v6 client kinetic rendering optimizer; must ensure turret kinetic visuals follow standard Create/Flywheel block-entity rendering contracts. |
| **CreateTweaker / KubeJS Create** | `437717` / `429371` | `CreateTweaker-1.18.2-2.0.0.20.jar` (`4770434`) | `kubejs-create-forge-2001.3.0-build.8.jar` (`6265498`) | Pack recipe-scripting hooks: `5.5.5` uses CraftTweaker + CreateTweaker (`.zs`), while `Beta 5.10.17` uses KubeJS + KubeJS Create (`.js`). |

### 2.2 Immersive Engineering & Related Addons

| Mod | Project ID | v5.5.5 (`1.18.2`) JAR & File ID | Beta 5.10.17 (`1.20.1`) JAR & File ID | Integration Surface & Impact |
| --- | :---: | --- | --- | --- |
| **Immersive Engineering** | `231951` | `ImmersiveEngineering-1.18.2-8.4.0-161.jar` (`4412849`) | `ImmersiveEngineering-1.20.1-10.2.0-183.jar` (`6206989`) | Core tech partner in **both** packs. Provides Steel, Treated Wood, Electronic Components (`component_electronic` replaces `create:electron_tube` pack-wide!), IF/FE power, fluid pipes/tanks, `biodiesel`, `ethanol`, `plantoil`, `creosote`, and coexisting `chemthrower` + `turret_chem` (both enabled & quest-referenced). |
| **Immersive Petroleum** | `268250` | `ImmersivePetroleum-1.18.2-4.2.0-25.jar` (`4818720`) | *Not installed* | **5.5.5 only.** Primary petroleum refining ecosystem in `5.5.5`: `crudeoil`, `diesel`, `diesel_sulfur`, `gasoline`, `naphtha`, `naphtha_cracked`, `kerosene`, `benzene`, `napalm`, `lubricant`, `ethylene`, `propylene`, Pumpjack, Distillation Tower, Hydrotreater. |
| **Immersive Posts** | `314645` | `ImmersivePosts-1.18.2-4.3.0-3.jar` (`3800690`) | *Not installed* | 5.5.5 decorative metal posts; no fluid/combat overlap. |
| **Immersive Fixes** | `1326199` | *Not installed* | `immersivefixes-1.0.3-all.jar` (`7119124`) | **v6 only.** Bugfix companion for IE in `1.20.1`. |
| **Just Enough Immersive Multiblocks** | `634571` | `jeimultiblocks-1.18.2-0.0.2.jar` (`3903132`) | `jeimultiblocks-1.20.1-1.0.6.jar` (`7131221`) | JEI multiblock display helper; no conflict. |

*Disambiguation:* `Beta 5.10.17` also includes four unrelated mods containing "Immersive" in their name — `Immersive Aircraft` (`666014`, `immersive_aircraft-1.4.0+1.20.1-forge.jar`, `6972825`), `Immersive Optimization` (`1163206`, `immersive_optimization-forge-1.20.1-0.1.0.jar`, `6969713`), `Immersive UI` (`1021685`, `ImmersiveUI-FORGE-0.3.0.jar`, `6023593`), and `Toni's Immersive Lanterns` (`1116812`, `immersivelanterns-forge-1.0.6-1.20.1.jar`, `6052952`). None are IE addons.

### 2.3 Fluid Transport, Storage, Power & Vehicle Fuel Consumers

| Mod | Project ID | v5.5.5 (`1.18.2`) JAR & File ID | Beta 5.10.17 (`1.20.1`) JAR & File ID | Verified Config / Capability Notes |
| --- | :---: | --- | --- | --- |
| **Create** (Fluids & Kinetics) | `328085` | `create-1.18.2-0.5.1.f.jar` (`4835188`) | `create-1.20.1-6.0.6.jar` (`6641603`) | `fluidTankCapacity = 8` buckets/block (`8,000 mB`), `fluidTankMaxHeight = 32`, `mechanicalPumpRange = 16`, `bottomlessFluidMode = "ALLOW_BY_TAG"`, `disableStress = false`. Standard `ForgeCapabilities.FLUID_HANDLER` / `CapabilityFluidHandler`. |
| **Pipez** | `443900` | `pipez-1.18.2-1.1.5.jar` (`3819249`) | `pipez-forge-1.20.1-1.2.21.jar` (`6368313`) | Fluid transfer rates (`pipez-server.toml`): **5.5.5:** `50 / 100 / 500 / 2,000 / 10,000 mB/t`; **v6:** `100 / 200 / 1,000 / 5,000 / 20,000 mB/t`. Energy pipe: **5.5.5:** `8,192–131,072 FE/t`; **v6:** `16,384–524,288 FE/t`. Recipes gated behind `create:fluid_pipe` in both packs. |
| **Refined Storage** | `243076` | `refinedstorage-1.10.6.jar` (`4902316`) | `refinedstorage-1.12.4.jar` (`4844585`) | Fluid storage disks, Importers/Exporters, External Storage via Forge fluid capabilities. v6 adds `Refined Storage Addons` (`272302`), `Refined Polymorphism` (`943086`), and `Refined Storage (Fixes) Mixin` (`1431536`). |
| **Immersive Engineering** (Pipes & IF/FE) | `231951` | `ImmersiveEngineering-1.18.2-8.4.0-161.jar` (`4412849`) | `ImmersiveEngineering-1.20.1-10.2.0-183.jar` (`6206989`) | Fluid Pipes, Fluid Pump, Sheetmetal Tanks, LV/MV/HV Wire Connectors & Capacitors (standard Forge Energy `FE`). Diesel Generator outputs `12,288 IF/t` in `5.5.5` and `8,192 IF/t` in `Beta 5.10.17`. |
| **Extreme Reactors** | `250277` | *Not installed* | `ExtremeReactors2-1.20.1-2.0.94.jar` (`7028980`) | **v6 only.** Late-game FE generation (basic tier removed in `removals.js`; reinforced tier active). Exposes standard FE. |
| **Ultimate Car Mod** | `267458` | `car-1.18.2-1.0.1.jar` (`3707486`) | *Not installed* | **5.5.5 only.** Pack disables all native `car:*` fluids (`car_removal.zs`) and restricts vehicles (`defaultconfigs/car/fuel.toml`) to `immersivepetroleum:gasoline` (`100`), `immersivepetroleum:diesel` (`150`), and `immersiveengineering:biodiesel` (`50`). |
| **DragN's VV: Refueled** (+ Valiant Vehicles) | `1144170` / `1038652` | *Not installed* | `refueled-1.20.1-2.4.2.jar` (`6988874`) + `DragN_Vehicles-1.20.1-1.3.2.jar` (`6960896`) | **v6 only.** `refueled-server.toml` sets `canister_max = 6000` mB, `gas_station_capacity = 40000` mB, and accepts `createdieselgenerators:gasoline` (`1.0`), `createdieselgenerators:diesel` (`0.8`), `createdieselgenerators:biodiesel` (`0.6`), `immersiveengineering:biodiesel` (`0.6`). |
| **Sophisticated Backpacks** | `422301` | `sophisticatedbackpacks-1.18.2-3.19.1.959.jar` (`4913629`) | `sophisticatedbackpacks-1.20.1-3.24.10.1404.jar` (`7116643`) | Tank Upgrade & Refill Upgrade interact with `IFluidHandlerItem` cartridges/canisters; cartridges must cleanly implement Forge item fluid capabilities. |

### 2.4 Animation, Rendering, Shaders, Dynamic Lights & Audio

| Mod | Project ID | v5.5.5 (`1.18.2`) JAR & File ID | Beta 5.10.17 (`1.20.1`) JAR & File ID | Rendering / Shader / Perf Implications |
| --- | :---: | --- | --- | --- |
| **GeckoLib** | `388172` | `geckolib-forge-1.18-3.0.57.jar` (`4181370`) | `geckolib-forge-1.20.1-4.7.jar` (`6027567`) | **MAJOR API BREAK:** GeckoLib 3 (`IAnimatable`, `AnimationFactory`, `GeoItemRenderer`) vs GeckoLib 4 (`GeoItem`, `AnimatableInstanceCache`, `SingletonGeoAnimatable`, `GeoItemRenderer`). Isolate strictly behind a client animation adapter. |
| **playerAnimator** | `658587` | `player-animation-lib-forge-1.0.2+1.18.jar` (`4418152`) | `player-animation-lib-forge-1.0.2-rc1+1.20.jar` (`4587214`) | Present in both packs (dependency of Better Combat); optional two-handed third-person flamethrower hold/recoil pose support. |
| **Embeddium** (+ Extras/Options) | `908741` | `embeddium-0.3.10+mc1.18.2.jar` (`5175514`) + `rubidium-extra-0.4.18+mc1.18.2-build.86.jar` (`4513591`) + `textrues_embeddium_options-0.1.1+mc1.18.2.jar` (`4747651`) | `embeddium-0.3.31+mc1.20.1.jar` (`5681725`) + `sodiumextras-forge-1.0.7-1.20.1.jar` (`6041697`) + `sodiumoptionsapi-forge-1.0.10-1.20.1.jar` (`6100812`) | Sodium-derived renderer in **both** packs (standalone Rubidium is *not* installed; `rubidium-options.json` in `overrides/config/` is legacy config only). Avoid custom raw-GL state leaks; use standard `RenderType` and `ParticleRenderType`. |
| **Oculus** (+ Compat Fixes) | `581495` | `oculus-mc1.18.2-1.6.4.jar` (`4578744`) + `GeckoLibOculusCompat-Forge-1.0.1.jar` (`5018199`) + `oculusparticlefix-1.0.jar` (`4787564`) | `oculus-mc1.20.1-1.8.0.jar` (`6020952`) | Iris shader pipeline in both packs (`enableShaders=false` by default in `oculus.properties`, user-toggleable). Additive/translucent flame particles and GeckoLib emissive layers must be tested under Oculus shader packs. |
| **Flywheel** (Bundled in Create) & Shader Bridges | `659897` / `1254143` / `1285475` | Flywheel `0.6.x` (in Create `0.5.1.f`) + `oculus-flywheel-compat-1.18.2-0.2.1.jar` (`4631182`) | Flywheel `1.0.x` (in Create `6.0.6`) + `colorwheel-forge-1.1.1+mc1.20.1.jar` (`7152024`) + `colorwheel_patcher-forge-1.0.3+mc1.20.1.jar` (`7152028`) | **MAJOR RENDER BREAK:** Flywheel `0.6` (`BlockEntityInstance`) vs Flywheel `1.0` (`AbstractBlockEntityVisual`). In v6, Colorwheel patches Oculus shaders for Flywheel 1.0 instancing (bundled with `photon_v1.2a + Clrwl_1.0.3.zip.txt`). |
| **Dynamic Lights (`Lucent` vs `Sodium/Embeddium Dynamic Lights`)** | `493280` / `551736` | `lucent-1.18.2-1.2.2.jar` (`3776959`) | `sodiumdynamiclights-forge-1.0.10-1.20.1.jar` (`6044481`) | **Incompatible APIs & configs:** In `5.5.5`, `lucent-client.toml` sets `burningEntitiesGlow=true` (`10`), `heldItemsGlow=true`, `lightRefreshRate=6`, `smoothBlending=false`. In `v6`, `sodiumdynamiclights-client.toml` sets `mode="FAST"`, `self=true`, `entities=false`, `block_entities=false` — meaning held-weapon self-lighting works by default, but entity/block-entity dynamic lights are disabled unless user-enabled. |
| **Distant Horizons** | `508933` | *Not installed* | `DistantHorizons-2.4.5-b-1.20.1-fabric-forge.jar` (`7375280`) *(DH Edition Extra only)* | LOD chunk renderer. Custom particles/streams operate within standard entity tracking range (`<= 64` blocks) and must not mutate distant chunk data or emit unbounded block light updates. |
| **ImmediatelyFast** | `686911` | *Not installed* | `ImmediatelyFast-Forge-1.5.1+1.20.4.jar` (`6745706`) | **v6 only.** Batches immediate-mode GUI/HUD/entity draws; avoid bypassing `PoseStack`/`MultiBufferSource` in custom HUD fuel gauges or GeckoLib renderers. |
| **Entity Culling** | `448233` | `entityculling-forge-1.6.1-mc1.18.2.jar` (`4406217`) | `entityculling-forge-1.9.4-mc1.20.1.jar` (`7313354`) | Occlusion-culls entities and block entities; ensure turret AABB (`getRenderBoundingBox`) covers full rotating barrel & pilot flame so it is not culled prematurely. |
| **Sound Physics Remastered** | `535489` | `soundphysics-forge-1.18.2-1.0.6.jar` (`3775919`) | `sound-physics-remastered-forge-1.20.1-1.4.10.jar` (`6352920`) | Acoustic reverb/occlusion on `SoundEvent` playback; loop/ignition sounds should be clean mono `.ogg` assets with bounded concurrency so reverb tails do not clip or saturate channels. |

#### Bundled Shader Packs (All Archives)

| Shader Pack | Project ID | v5.5.5 (`1.18.2`) File | Beta 5.10.17 (`1.20.1`) File | Notes |
| --- | :---: | --- | --- | --- |
| **Complementary Shaders - Reimagined** | `627557` | `ComplementaryReimagined_r2.2.zip` | *Removed in v6* | Configured in `overrides/config/oculus.properties` (`enableShaders=false`). Note: `Beta 5.10.17` still carries a stale `shaderPack=ComplementaryReimagined_r2.2.zip` line in `oculus.properties`. |
| **Insanity Shader** | `618217` | `Insanity-Shader-Universal-v1.500.zip` | *Removed in v6* | Dark atmospheric horror shader in `5.5.5`; tests flame visibility & emissive legibility in near-total darkness. |
| **Complementary Shaders - Unbound** | `385587` | *Not in 5.5.5* | `ComplementaryUnbound_r5.6.1.zip` | Primary general-purpose shader in `v6`. |
| **Bliss Shaders** | `610844` | *Not in 5.5.5* | `Bliss_v2.1.2_(Chocapic13_Shaders_edit).zip` | Volumetric atmospheric/DH-compatible shader in `v6`. |
| **Spooklementary** | `921717` | *Not in 5.5.5* | `Spooklementary_v2.0.2.zip` | Horror-tuned Complementary fork in `v6`. |
| **Photon Shader** | `1312687` | *Not in 5.5.5* | `photon_v1.2a.zip` | Accompanied by two preset configs in `overrides/shaderpacks/`: `photon_v1.2a.zip.txt` and `photon_v1.2a + Clrwl_1.0.3.zip.txt` (Colorwheel-patched Flywheel 1.0 preset). |

### 2.5 Survival, Combat, Protection, Loot & Hostile Mobs

| Mod | Project ID | v5.5.5 (`1.18.2`) JAR & File ID | Beta 5.10.17 (`1.20.1`) JAR & File ID | Verified Config & Integration Requirements |
| --- | :---: | --- | --- | --- |
| **First Aid** | `276837` | `firstaid-1.11.1.jar` (`3860237`) | *Not installed* | **5.5.5 only.** Locational limb health (`causeDeathHead=true`, `allowNaturalRegeneration=false`, head armor multiplier `7.0x`). Fire/lava damage distributes across limbs via Forge `LivingHurtEvent`; do not bypass standard `Entity#hurt` with raw `setHealth`. |
| **Cold Sweat** | `506194` | `ColdSweat-2.2.5.1.jar` (`5015720`) | *Not installed* | **5.5.5 only.** Temperature survival (`Minimum Habitable = 0.4286`, `Maximum Habitable = 1.619`, `Fire Resistance Immunity = true`, `Cold Soul Fire = true`). Optional soft adapter can apply mild heat buildup near sustained nozzle/turret firing. |
| **Thirst Was Taken** | `679270` | `ThirstWasTaken-1.18.2-1.3.4.jar` (`4794519`) | *Not installed* | **5.5.5 only.** Hydration system; no direct fluid-tank conflict (do not tag industrial fuels as drinkable water — note pack explicitly strips fuels from `#minecraft:water`). |
| **Legendary Survival Overhaul** | `840254` | *Not installed* | `legendarysurvivaloverhaul-1.20.1-2.3.23.1.jar` (`7037397`) | **v6 only.** Replaces First Aid + Cold Sweat + Thirst Was Taken in a single mod (`Temperature=true`, `Thirst=true`, `Health Overhaul=true`, `Localized Body Damage=true`, `Difficulty="HARD"`, `Player On Fire Modifier = 12.5`, `Heat Thirst Effect Modifier = 0.5`). |
| **Open Parties and Claims** | `636608` | `open-parties-and-claims-forge-1.18.2-0.20.1.jar` (`4784620`) | `open-parties-and-claims-forge-1.20.1-0.25.8.jar` (`7112737`) | **Critical protection gate in both packs.** `openpartiesandclaims-server.toml` sets `primaryPartySystem = "ftb_teams"` and `default-player-config.toml` enables `protectClaimedChunks=true`, `fromFireSpread=true`, `entitiesFromFire=true`, `fluidBarrier=true`. Must query OPAC claim/party rules before igniting ground fire or damaging entities/players inside claims. |
| **FTB Teams** (+ FTB Quests) | `404468` / `289412` | `ftb-teams-forge-1802.2.9-build.88.jar` (`4229138`) + `ftb-quests-forge-1802.3.15-build.298.jar` (`4760361`) | `ftb-teams-forge-2001.3.1.jar` (`6130786`) + `ftb-quests-forge-2001.4.16.jar` (`7232023`) | Primary party/ally backend for OPAC in both packs; automated turret default friendly-fire exclusion must honor FTB Teams party & ally membership. |
| **Lootr** | `361276` | `lootr-1.18.2-0.3.25.63.jar` (`4596362`) | `lootr-forge-1.20-0.7.35.94.jar` (`7263076`) | Per-player instanced loot containers (`randomise_seed=true`, `loot_table_blacklist=[]`). Use standard Forge Global Loot Modifiers (GLMs) on vanilla/DeceasedCraft chest tables; never mutate placed chest block entities directly. |
| **The Hordes** (+ Enhanced Hordes) | `485779` / `899308` | `The-Hordes-1.18.2-1.5.3a.jar` (`5287529`) + `eh1.2-1.18.2.jar` (`5023161`) | `The-Hordes-1.20.1-1.5.4c.jar` (`6718502`) + `eh1.3.1-1.20.1.jar` (`5565963`) | Recurring 15-day siege events (`hordeSpawnMax = 75` in `5.5.5`, `100` in `v6`). Drives hard performance budgets: bounded cone/capsule queries, batched particle packets, capped temporary ground fire blocks, and server-authoritative tick intervals. |
| **Zombie Awareness** | `237754` | `zombieawareness-1.18.1-1.12.3.jar` (`3603741`) | `zombieawareness-1.20.1-1.13.1.jar` (`5096285`) | `awareness_Sound=true`, `awareness_Light=true`, `soundAlerts=true`, `soundInvestigates=true` in **both** packs. Emitting standard Minecraft sound events and `GameEvent`s makes firing naturally attract nearby zombies without custom hacks. |
| **THE UNDEAD REVAMPED** | `479710` | `THEUNDEADREVAMPED_0.9e_1.18.2.jar` (`4928215`) | `THEUNDEADREVAMPED_1.9O_1.20.1.jar` (`7446558`) | Core modded infected roster (heavy/special variants, boss-scale mobs). Pack hides its crafting items (`undead_revamp2` in `modRemoval`). Respect mob fire-immunity flags and armor attributes. |
| **Zombie Extreme** | `392809` | `Zombie Extreme 1.18.2 0.2.4.jar` (`4746394`) | `Zombie Extreme 1.20.1 0.2.6.jar` (`5602540`) | High-HP bosses (`demolisher`, `zero_patient`, `rat_king`). Pack hides its crafting items (`zombie_extreme` in `modRemoval`). Heat-buildup multiplier (`+10%/hit` up to `2x`) shines against high-HP targets. |
| **Fungal Infection: Spore** | `678295` | *Not installed* | `spore_2.1.5c_1.20.1.jar` (`6788610`) | **v6 only.** Adds fungal/biomass infected mobs susceptible to fire damage; ensures standard fire damage typing (`DamageTypes.IN_FIRE` / `ON_FIRE` / tagged `#minecraft:is_fire`) triggers Spore's native fire vulnerability multipliers! |
| **Firearms Ecosystem (`TaC` vs `TaCZ` & `CGM`)** | `491264` / `1028108` / `289479` / `945471` | `tac-0.3.10.1-1.18.2.jar` (`4886929`) + `cgm-1.3.3-1.18.2.jar` (`4344223`) | `tacz-1.20.1-1.1.6-hotfix.jar` (`6654541`) + `CGM-Unofficial-1.4.18+Forge+1.20.1.jar` (`5610926`) + `tacz-tweaks`, `taczammoquery`, `gundb` | **Complete firearm swap between packs.** Both packs bind **`R`** for firearm reload by default (`TaC` / `TaCZ`). Our flamethrower reload keybind MUST gracefully share or not conflict with `R` (trigger only when holding a `tacticalchemthrowers` weapon) and support sneak+right-click fallback. |
| **Better Combat** & **Curios API** | `639842` / `309927` | `bettercombat-forge-1.6.2+1.18.2.jar` + `curios-forge-1.18.2-5.0.7.1.jar` | `bettercombat-forge-1.8.6+1.20.1.jar` + `curios-forge-5.14.1+1.20.1.jar` | Present in both packs. Do not register melee `weapon_attributes` on the handheld flamethrower so Better Combat does not hijack left/right-click handling. Curios enables optional future pressurized backtank slot integration. |

---

## 3. Dual-Version (`1.18.2` + `1.20.1`) Adapter Boundary Architecture

Because `v5.5.5` (`1.18.2`, Forge `40.2.4`, Create `0.5.1.f`, GeckoLib `3`, IP, First Aid/Cold Sweat, Lucent) and `Beta 5.10.17` (`1.20.1`, Forge `47.4.0`, Create `6.0.6`, GeckoLib `4`, CDG, LSO, Sodium/Embeddium Dynamic Lights) diverge across **seven** major APIs, the codebase should separate version-agnostic domain logic from thin, explicit platform adapters:

| Subsystem | Shared Core (`common`) | `1.18.2` Forge Adapter (`v5.5.5`) | `1.20.1` Forge Adapter (`Beta 5.10.17`) |
| --- | --- | --- | --- |
| **Fuel Registry & Fluid Capabilities** | Data-driven `FlamethrowerFuelRegistry` (`data/tacticalchemthrowers/flamethrower_fuels/*.json`), 50 units = `1,000 mB` (`20 mB/unit`), exact-ID → fluid-tag → reject resolution. | `CapabilityFluidHandler` (`FLUID_HANDLER_CAPABILITY`, `FLUID_HANDLER_ITEM_CAPABILITY`), `FluidAttributes` color/viscosity, IP + IE + CreateAddition fuel defaults. | `ForgeCapabilities.FLUID_HANDLER` / `FLUID_HANDLER_ITEM`, `FluidType` / `IClientFluidTypeExtensions`, CDG + IE + CreateAddition fuel defaults. |
| **Create Kinetics & Turret Visuals** | Turret state machine (range, pilot burner, target filter, fuel/SU/FE gating, throttled cone acquisition, server-authoritative raycast). | Create `0.5.1.f` `KineticTileEntity` / `KineticBlockEntity`, Flywheel `0.6.x` `BlockEntityInstance` (`oculus-flywheel-compat` safe). | Create `6.0.6` `KineticBlockEntity`, Flywheel `1.0.x` `AbstractBlockEntityVisual` (`Colorwheel` / `Colorwheel Patcher` safe), optional soft `Create: Radars` link hook. |
| **Electrical Power (`FE`)** | Abstract `TurretEnergyBuffer` (idle pilot draw + active ignition/tracking draw). | `CapabilityEnergy.ENERGY` (interops seamlessly with IE wires/capacitors, Create Crafts & Additions, Pipez). | `ForgeCapabilities.ENERGY` (interops with IE, Create Crafts & Additions, Pipez, Extreme Reactors). |
| **Weapon Animation & Rendering** | Weapon state flags (`IDLE`, `IGNITING`, `FIRING`, `COOLING`, `RELOADING`, `EMPTY`) synced via compact network packets. | GeckoLib `3.0.57` (`IAnimatable`, `AnimationFactory`) + `GeckoLibOculusCompat` shader-safe render layers. | GeckoLib `4.7` (`GeoItem`, `SingletonGeoAnimatable`, `AnimatableInstanceCache`) + `ImmediatelyFast`/`Oculus 1.8` safe `MultiBufferSource` rendering. |
| **Dynamic Lighting** | Optional client-only `IDynamicLightBridge` with no-op fallback. | Soft `Lucent` (`1.2.2`) registration for active firing weapon / ignited nozzle; relies on pack's `burningEntitiesGlow=true`. | Soft `Sodium/Embeddium Dynamic Lights` (`1.0.10`) held-item emitter (works with pack's `self=true`, `entities=false` default). |
| **Damage Types & Survival Systems** | Base fire DPS + close-range thermal bonus + consecutive-hit heat ramp (`+10%/hit`, `2.0x` cap, `2.5s` decay) + `3s` burn. | `DamageSource` (`setIsFire()`), standard `Entity#hurt` so **First Aid** distributes limb damage; optional soft **Cold Sweat** heat hook. | Registry-driven `Holder<DamageType>` tagged in `#minecraft:is_fire` so **Legendary Survival Overhaul** (`Player On Fire Modifier = 12.5`) and **Fungal Infection: Spore** fire weaknesses trigger natively. |
| **Claims, PvP & Friendly-Fire** | `IProtectionGuard` (`canIgniteBlock`, `canDamageEntity`, `isAllied`). | Vanilla spawn/PvP/scoreboard + soft **Open Parties and Claims `0.20.1`** + soft **FTB Teams `1802.2.9`** hooks. | Vanilla spawn/PvP/scoreboard + soft **Open Parties and Claims `0.25.8`** + soft **FTB Teams `2001.3.1`** hooks. |
| **Recipes & Loot** | Additive JSON recipes + Forge Global Loot Modifiers (`GLM`). Never override pack recipes or mutate chest block entities. | `1.18.2` GLM (`loot_modifiers`) + `forge:conditions` (`mod_loaded`) guarding IP-specific extras; compatible with `Lootr 0.3.25`. | `1.20.1` GLM Codec + `forge:conditions` guarding CDG-specific extras; compatible with `Lootr 0.7.35`. |
