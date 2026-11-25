# Mod-Dev API & Integration Research — Forge `1.18.2` & `1.20.1`

**Mod:** Create: Tactical ChemThrowers (`modid: tacticalchemthrowers`)  
**Dual Targets:**
- **Legacy Target:** Minecraft `1.18.2` / Forge `40.2.4` (**DeceasedCraft `v5.5.5`**)
- **Modern Target:** Minecraft `1.20.1` / Forge `47.4.0` (**DeceasedCraft `Beta-5.10.17`** & **`Beta DH Edition 5.10.17`**)

All mod JAR versions below were verified directly from `compiled_mods.json` and `categorized_mods.json` (extracted from the official DeceasedCraft CurseForge manifests). All API signatures, packages, and Maven coordinates were verified from official documentation and upstream repositories.

---

## 1. Critical Version Surprises (Read Before Writing Any Java)

1. **Create `0.5.1.f` (`1.18.2`) vs. Create `6.0.6` (`1.20.1`) — MASSIVE BREAKING API SPLIT:**
   - `DeceasedCraft v5.5.5` runs **Create `0.5.1.f`** (`Flywheel 0.6.x` embedded/bundled, monolithic Ponder inside Create, legacy `maven.tterrag.com`).
   - `DeceasedCraft Beta-5.10.17` runs **Create `6.0.6`** (**NOT `0.5.1.j`!**), which runs **Flywheel `1.0`**, extracts **Ponder** into a separate library JAR (`net.createmod.ponder`), exposes new `com.simibubi.create.api.*` public APIs, changes stress/spouting/display registries (`SimpleRegistry`), and uses **`https://maven.createmod.net`**!
   - **Impact:** Any Create-touching code (turret `KineticBlockEntity`, `IHaveGoggleInformation`, `BlockStressValues`, Ponder scenes, Flywheel visuals) **MUST** live behind version-specific adapter modules (`forge-1.18.2` vs. `forge-1.20.1`).
2. **GeckoLib `3.0.57` (`1.18.2`) vs. GeckoLib `4.7` (`1.20.1`) — FULL LIBRARY REWRITE:**
   - Complete rename and lifecycle overhaul (`IAnimatable` → `GeoItem`/`GeoBlockEntity`, `AnimationFactory` → `AnimatableInstanceCache`, `AnimationBuilder` → `RawAnimation`, `IItemRenderProperties` → `IClientItemExtensions`).
3. **Minecraft / Forge `1.18.2` → `1.20.1` Breaking Platform Deltas:**
   - `DamageSource` static constructors → data-driven `DamageType` JSON + tags (`#minecraft:is_fire`, `#minecraft:bypasses_armor`).
   - `GlobalLootModifierSerializer` (`List<ItemStack>`) → Codec-based `IGlobalLootModifier` (`ObjectArrayList<ItemStack>`).
   - `CapabilityFluidHandler` / `CapabilityEnergy` → unified `ForgeCapabilities`.
   - `ClientRegistry.registerKeyBinding` → `RegisterKeyMappingsEvent`.
   - `CreativeModeTab` constructor subclass → `DeferredRegister<CreativeModeTab>` + `BuildCreativeModeTabContentsEvent`.
   - `RenderLevelLastEvent` → `RenderLevelStageEvent`.
4. **Different Fuel, Survival & Dynamic-Light Stacks Across Packs:**
   - **Fuels:** `v5.5.5` ships **Immersive Petroleum `4.2.0-25`** (no Create: Diesel Generators); `Beta-5.10.17` ships **Create: Diesel Generators `1.3.5`** (no Immersive Petroleum). Fluid tag naming also diverges (`#forge:seedoil` in `v5.5.5` vs. `#forge:seed_oil` in `Beta-5.10.17`).
   - **Survival:** `v5.5.5` uses **First Aid + Cold Sweat + Thirst Was Taken**; `Beta-5.10.17` replaces all three with **Legendary Survival Overhaul `2.3.23.1`**.
   - **Dynamic Lights:** `v5.5.5` uses **Lucent `1.2.2`**; `Beta-5.10.17` uses **Sodium/Embeddium Dynamic Lights `1.0.10`** (`modid: sodiumdynamiclights`, with `self = true`, `entities = false`, `block_entities = false` by default).

---

## 2. Verified Mod & JAR Version Matrix

| Mod / Library | Mod ID | `v5.5.5` (`1.18.2`, Forge `40.2.4`) | `Beta-5.10.17` (`1.20.1`, Forge `47.4.0`) | Dependency Type |
| :--- | :--- | :--- | :--- | :--- |
| **Create** | `create` | `create-1.18.2-0.5.1.f.jar` | `create-1.20.1-6.0.6.jar` | **Core Integration** (Create 0.5 vs **6.0**) |
| **Flywheel** | `flywheel` | Bundled (`0.6.10` / `0.6.11` API) | Bundled JiJ (`1.0.x` API) | Transitive via Create |
| **Ponder** | `ponder` | Monolithic inside Create `0.5.1.f` | Bundled JiJ (`net.createmod.ponder` `1.0.x`) | Transitive via Create `6.0` |
| **Immersive Engineering** | `immersiveengineering` | `ImmersiveEngineering-1.18.2-8.4.0-161.jar` | `ImmersiveEngineering-1.20.1-10.2.0-183.jar` | Soft / Forge Cap Compat |
| **Immersive Petroleum** | `immersivepetroleum` | `ImmersivePetroleum-1.18.2-4.2.0-25.jar` | *(not installed)* | Data-driven fluid tags |
| **Create: Diesel Generators** | `createdieselgenerators` | *(not installed)* | `createdieselgenerators-1.20.1-1.3.5.jar` | Data-driven fluid tags |
| **Create Crafts & Additions** | `createaddition` | `createaddition-1.18.2-1.0.0.jar` | `createaddition-1.20.1-1.3.2.jar` | FE ↔ Kinetic bridge |
| **Create: Radars** | `create_radar` | *(not installed)* | `Radars 0.3.5.1-Create6.jar` | Reference / Coexistence |
| **GeckoLib** | `geckolib3` (`1.18`) / `geckolib` (`1.20`) | `geckolib-forge-1.18-3.0.57.jar` | `geckolib-forge-1.20.1-4.7.jar` | **Required (3D Weapon/Turret Anim)** |
| **playerAnimator** | `playeranimator` | `player-animation-lib-forge-1.0.2+1.18.jar` | `player-animation-lib-forge-1.0.2-rc1+1.20.jar` | Optional / Visual Reference |
| **Embeddium** | `embeddium` | `embeddium-0.3.10+mc1.18.2.jar` | `embeddium-0.3.31+mc1.20.1.jar` | Rendering Baseline |
| **Oculus** | `oculus` | `oculus-mc1.18.2-1.6.4.jar` *(+ `oculus-flywheel-compat 0.2.1`, `GeckoLibOculusCompat 1.0.1`, `oculusparticlefix 1.0`)* | `oculus-mc1.20.1-1.8.0.jar` | Shader Pipeline Target |
| **Lucent** | `lucent` | `lucent-1.18.2-1.2.2.jar` | *(not installed)* | Optional Client Dynamic Light |
| **Sodium/Embeddium Dynamic Lights** | `sodiumdynamiclights` | *(not installed)* | `sodiumdynamiclights-forge-1.0.10-1.20.1.jar` | Optional Client Dynamic Light |
| **Lootr** | `lootr` | `lootr-1.18.2-0.3.25.63.jar` | `lootr-forge-1.20-0.7.35.94.jar` | Automatic via Forge GLMs |
| **Open Parties and Claims** | `openpartiesandclaims` | `open-parties-and-claims-forge-1.18.2-0.20.1.jar` | `open-parties-and-claims-forge-1.20.1-0.25.8.jar` | Optional Server Protection |
| **FTB Teams** | `ftbteams` | `ftb-teams-forge-1802.2.9-build.88.jar` | `ftb-teams-forge-2001.3.1.jar` | Optional Server Team Guard |
| **Cold Sweat** | `cold_sweat` | `ColdSweat-2.2.5.1.jar` | *(not installed)* | Optional Warmth Hook (`1.18.2`) |
| **First Aid** | `firstaid` | `firstaid-1.11.1.jar` | *(not installed)* | Locational Damage Compat |
| **Legendary Survival Overhaul** | `legendarysurvivaloverhaul` | *(not installed)* | `legendarysurvivaloverhaul-1.20.1-2.3.23.1.jar` | Optional Warmth + Limb Compat |
| **Zombie Awareness** | `zombieawareness` | `zombieawareness-1.18.1-1.12.3.jar` | `zombieawareness-1.20.1-1.13.1.jar` | Sound/Light Sense Compat |
| **Armor Set Bonuses** | `armorsetbonuses` / `spacecatasb` | `spacecatasb-forge-18.13.1.jar` | `spacecatasb-forge-20.14.0.jar` | Firefighter Fire Resistance |
| **Curios API** | `curios` | `curios-forge-1.18.2-5.0.7.1.jar` | `curios-forge-5.14.1+1.20.1.jar` | Optional Backtank/Canister Slot |
| **JEI** | `jei` | `jei-1.18.2-forge-10.2.1.1005.jar` | `jei-1.20.1-forge-15.20.0.112.jar` | Recipe Integration |
| **Distant Horizons** | `distanthorizons` | *(not installed)* | `DistantHorizons-2.4.5-b-1.20.1-fabric-forge.jar` *(DH Edition only)* | LOD Render Coexistence |

---

## 3. Forge `1.18.2` (`40.2.4`) vs. `1.20.1` (`47.4.0`) Core API Deltas

| Subsystem | Forge `1.18.2` (`40.2.4`) | Forge `1.20.1` (`47.4.0`) | Implementation Guidance |
| :--- | :--- | :--- | :--- |
| **Capabilities** | `CapabilityFluidHandler.FLUID_HANDLER_CAPABILITY`, `CapabilityFluidHandler.FLUID_HANDLER_ITEM_CAPABILITY`, `CapabilityEnergy.ENERGY`, `CapabilityItemHandler.ITEM_HANDLER_CAPABILITY` | Unified `net.minecraftforge.common.capabilities.ForgeCapabilities`: `FLUID_HANDLER`, `FLUID_HANDLER_ITEM`, `ENERGY`, `ITEM_HANDLER` | Wrap capability token lookups in a tiny versioned `PlatformCapabilities` helper; always invalidate `LazyOptional` in `BlockEntity#invalidateCaps()`. |
| **Damage Sources & Fire Tagging** | Code-driven: `new EntityDamageSource("tacticalchemthrowers.chem_flame", attacker).setIsFire()` (and `.bypassArmor()` if needed). `DamageSource.IN_FIRE` / `ON_FIRE` are static constants. | **Data-driven `DamageType` JSON** at `data/tacticalchemthrowers/damage_type/chem_flame.json` (`exhaustion`, `message_id`, `scaling`) + `ResourceKey<DamageType>` via `Registries.DAMAGE_TYPE`. Fire/armor behavior is driven by vanilla tags: `data/minecraft/tags/damage_type/is_fire.json` and `bypasses_armor.json` (`"replace": false`). Construct `new DamageSource(level.registryAccess().registryOrThrow(Registries.DAMAGE_TYPE).getHolderOrThrow(KEY), directEntity, causingEntity)`. | Put `chem_flame` in `#minecraft:is_fire` (`1.20.1`) / `.setIsFire()` (`1.18.2`) so Firefighter armor (`minecraft:fire_resistance`), First Aid, and LSO work automatically. Never statically cache a datapack `Holder<DamageType>` before world load (causes crashes with mods like `DuMmmMmmy`/LSO!). |
| **Global Loot Modifiers (GLMs)** | Subclass `LootModifier` (`List<ItemStack> doApply(List<ItemStack>, LootContext)`) + subclass `GlobalLootModifierSerializer<T>` (`read`/`write`). Register serializer via `DeferredRegister.create(ForgeRegistries.Keys.LOOT_MODIFIER_SERIALIZERS, MOD_ID)` (or `RegistryEvent.Register<GlobalLootModifierSerializer<?>>`). | Subclass `LootModifier` (`ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack>, LootContext)` + `Codec<? extends IGlobalLootModifier> codec()`). Register `Codec` via `DeferredRegister.create(ForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, MOD_ID)` using `RecordCodecBuilder` + `LootModifier.codecStart(inst)`. | Both versions read `data/forge/loot_modifiers/global_loot_modifiers.json` (`"replace": false`) and `data/tacticalchemthrowers/loot_modifiers/*.json`. |
| **Creative Tabs** | Subclass `CreativeModeTab("tacticalchemthrowers")` overriding `makeIcon()`; attach to items via `new Item.Properties().tab(ModTabs.MAIN)`. | Register `CreativeModeTab.builder().title(...).icon(...).displayItems(...).build()` via `DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MOD_ID)` and/or listen to `BuildCreativeModeTabContentsEvent` on the MOD bus. `Item.Properties#tab(...)` was removed. | Keep item `Properties` tab-free in shared definitions; attach tabs inside versioned registration code. |
| **Key Mappings** | Register `KeyMapping` during `FMLClientSetupEvent` via `net.minecraftforge.client.ClientRegistry.registerKeyBinding(key)` (MOD bus). | Register `KeyMapping` via `net.minecraftforge.client.event.RegisterKeyMappingsEvent#register(...)` on the physical-client MOD bus; poll `consumeClick()` in `TickEvent.ClientTickEvent` (`Phase.END`) on the Forge bus. | Use `KeyConflictContext.IN_GAME` and `InputConstants.Type.KEYSYM` (GLFW tokens). |
| **Networking (`SimpleChannel`)** | `NetworkRegistry.newSimpleChannel(...)` + `PacketDistributor.TRACKING_ENTITY_AND_SELF`, `PacketDistributor.TRACKING_CHUNK`, `PacketDistributor.SERVER.noArg()`. | Identical `NetworkRegistry.newSimpleChannel(...)` + `PacketDistributor` API in Forge `47.4.0`. | Can share packet DTO encoding/decoding cleanly across both versions (`FriendlyByteBuf`). |
| **Level Rendering Event** | `net.minecraftforge.client.event.RenderLevelLastEvent` (Forge client bus). | `net.minecraftforge.client.event.RenderLevelStageEvent` (check `event.getStage() == RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS` or `AFTER_PARTICLES`). | Prefer standard Minecraft `Particle` / `BlockEntityRenderer` / `GeoItemRenderer` over raw world-render hooks for Iris/Oculus shader safety! |

---

## 4. Create API (`0.5.1.f` vs. `6.0.6`)

### 4.1 Maven Repositories & Gradle Dependencies

#### Target A — `1.18.2` (Create `0.5.1.f`, Flywheel `0.6.x`, Registrate `1.1.3`)
Verified from the official Create Wiki (`Depending on Create` for `0.5.1.x`):
```groovy
repositories {
    maven { name = "tterrag maven"; url = "https://maven.tterrag.com/" }
}
dependencies {
    // Pin to the 0.5.1.f (or binary-compatible 0.5.1.e/g) CI artifact matching release create-1.18.2-0.5.1.f.jar
    implementation fg.deobf("com.simibubi.create:create-1.18.2:${create_version}:slim") { transitive = false }
    implementation fg.deobf("com.jozufozu.flywheel:flywheel-forge-1.18.2:${flywheel_version}") // e.g. 0.6.10-105 or 0.6.11-107
    implementation fg.deobf("com.tterrag.registrate:Registrate:MC1.18.2-1.1.3")
}
```
*Production `mods.toml` range:* `versionRange="[0.5.1.f,0.6.0)"` (or `mandatory=false` if Create turret kinetic mode is soft-optional).

#### Target B — `1.20.1` (Create `6.0.6`, Ponder `1.0.x`, Flywheel `1.0.x`, Registrate `1.3.3`)
Verified from `https://wiki.createmod.net/developers/depend-on-create/forge-1.20.1`:
```groovy
repositories {
    maven { url = "https://maven.createmod.net" }           // Create 6, Ponder, Flywheel 1.0
    maven { url = "https://maven.ithundxr.dev/mirror" }     // Registrate
    maven { url = "https://raw.githubusercontent.com/Fuzss/modresources/main/maven/" } // ForgeConfigAPIPort
}
dependencies {
    // Use the exact 6.0.6 CI build number from maven.createmod.net (6.0.8-289 / ponder 1.0.91 / flywheel 1.0.5 is latest 1.20.1)
    implementation(fg.deobf("com.simibubi.create:create-1.20.1:${create_version}:slim")) { transitive = false }
    implementation(fg.deobf("net.createmod.ponder:Ponder-Forge-1.20.1:${ponder_version}"))
    compileOnly(fg.deobf("dev.engine-room.flywheel:flywheel-forge-api-1.20.1:${flywheel_version}"))
    runtimeOnly(fg.deobf("dev.engine-room.flywheel:flywheel-forge-1.20.1:${flywheel_version}"))
    implementation(fg.deobf("com.tterrag.registrate:Registrate:MC1.20-1.3.3"))
    compileOnly(annotationProcessor("io.github.llamalad7:mixinextras-common:0.4.1"))
    implementation("io.github.llamalad7:mixinextras-forge:0.4.1")
}
```
*Required in ForgeGradle `minecraft.runs.*` for BOTH versions (remaps Create's Mixin refmaps in dev):*
```groovy
property("mixin.env.remapRefMap", "true")
property("mixin.env.refMapRemappingFile", "${projectDir}/build/createSrgToMcp/output.srg")
```
*Production `mods.toml` range:* `versionRange="[6.0.6,6.1.0)"` (compatible with DeceasedCraft Beta's `create-1.20.1-6.0.6.jar` through `6.0.8+`).

### 4.2 Verified Create API Classes, Deltas & Gotchas

| Feature / Class | Create `0.5.1.f` (`1.18.2`) | Create `6.0.6` (`1.20.1`) | Engineering Notes & Verified Caveats |
| :--- | :--- | :--- | :--- |
| **`KineticBlockEntity`** | `com.simibubi.create.content.kinetics.base.KineticBlockEntity` | `com.simibubi.create.content.kinetics.base.KineticBlockEntity` | **Flicker Score Caveat (Create Issue #9251):** Repeatedly toggling kinetic network speed/connection (`non-zero → zero → non-zero`) adds `+10` flicker tally per update and breaks the block above `128`. Keep turret SU consumption steady while powered (or throttle speed/state changes to `≥ 10` ticks) rather than toggling kinetic state every shot! |
| **`IHaveGoggleInformation`** | `com.simibubi.create.content.equipment.goggles.IHaveGoggleInformation` | `com.simibubi.create.api.equipment.goggles.IHaveGoggleInformation` *(relocated to `api` package in Create 6.0; verify exact import against `6.0.6` compile classpath!)* | Implement `addToGoggleTooltip(List<Component> tooltip, boolean isPlayerSneaking)` to display turret fuel type, mB stored, FE/SU status, and active target mode. |
| **`IWrenchable`** | `com.simibubi.create.content.equipment.wrench.IWrenchable` | `com.simibubi.create.content.equipment.wrench.IWrenchable` | **Wrench Tag Caveat (Create Issue #10830):** Create checks its own wrench by exact item in `useItemOn` while third-party wrenches tagged `#forge:tools/wrench` / `#c:tools/wrench` route through `WrenchEventHandler` directly to `onWrenched` / `onSneakWrenched`. Implement our turret config GUI / rotation cleanly inside `onWrenched` and check `#forge:tools/wrench` (plus IE's `immersiveengineering:hammer`) so both Create's Wrench and other wrenches work reliably! |
| **`SmartFluidTankBehaviour`** | `com.simibubi.create.foundation.blockEntity.behaviour.fluid.SmartFluidTankBehaviour` | `com.simibubi.create.foundation.blockEntity.behaviour.fluid.SmartFluidTankBehaviour` | Attach via `addBehaviours(List<BlockEntityBehaviour>)` on `SmartBlockEntity` / `KineticBlockEntity`, or expose a standard Forge `IFluidHandler` backed by `FluidTank` with strict `isFluidValid(FluidStack)` fuel-registry validation and no-mixing rule. |
| **Stress Registration (`BlockStressValues`)** | `com.simibubi.create.content.kinetics.BlockStressValues` (`IStressValueProvider`) | `com.simibubi.create.api.stress.BlockStressValues` (`IMPACTS.register(...)` / `SimpleRegistry`) | Major Create 6.0 API cleanup (`BlockStressValues` moved to `api.stress`). Register turret stress impact per RPM (`16–32 SU/RPM`). |
| **Spout Filling (Handheld Canisters & ChemThrowers)** | Automatic for any item exposing `IFluidHandlerItem` (`CapabilityFluidHandler.FLUID_HANDLER_ITEM_CAPABILITY`) | Automatic for any item exposing `IFluidHandlerItem` (`ForgeCapabilities.FLUID_HANDLER_ITEM`) | Create's Spout (`GenericItemFilling`) automatically fills any `IFluidHandlerItem` stack on a Depot or Belt! **Requirement:** `fill(..., FluidAction.SIMULATE)` MUST be 100% side-effect free and reject invalid/mismatched fluids. |
| **Mechanical Crafting Recipe JSON** | `type: "create:mechanical_crafting"`, `pattern`, `key`, `result`, `acceptMirrored` (boolean) | Same JSON schema (`type: "create:mechanical_crafting"`, `pattern`, `key`, `result`, `acceptMirrored`) | Verified active in DeceasedCraft `Beta-5.10.17` KubeJS weapon/armor/vehicle recipes (`overrides/kubejs/server_scripts/recipes/deceasedcraft/*.js`). |

---

## 5. Immersive Engineering API (`8.4.0-161` vs. `10.2.0-183`)

- **Maven Repository (Verified):** `https://maven.blamejared.com`
  - `1.18.2`: `blusunrize.immersiveengineering:ImmersiveEngineering:1.18.2-8.4.0-161` *(optional `compileOnly`)*
  - `1.20.1`: `blusunrize.immersiveengineering:ImmersiveEngineering:1.20.1-10.2.0-183` *(optional `compileOnly`)*
- **Zero-Dependency Interoperability via Standard Forge Capabilities:**
  - **Bottling Machine Fluid Refilling:** IE's Bottling Machine dynamically fills **any** `ItemStack` exposing `IFluidHandlerItem` (`CapabilityFluidHandler.FLUID_HANDLER_ITEM_CAPABILITY` in `1.18.2` / `ForgeCapabilities.FLUID_HANDLER_ITEM` in `1.20.1`)—no custom IE recipes or hard IE dependency required!
  - **Turret Power (`IEnergyStorage`):** Exposing Forge's `IEnergyStorage` capability on our ChemThrower Turret makes it plug-and-play with IE LV/MV/HV Wire Connectors, Capacitors, and Create Crafts & Additions Alternators/Accumulators.
  - **Pipe Interop (`IFluidHandler`):** Exposing `IFluidHandler` connects seamlessly to Create Fluid Pipes, IE Fluid Pipes, and `Pipez` fluid pipes (all present in both DeceasedCraft packs).
- **Verified DeceasedCraft Crafting & Fluid Tag Conventions:**
  - **Metals** (verified in `Beta` `overrides/kubejs/server_scripts/recipes/deceasedcraft/material.js`):
    - `#forge:ingots/steel`, `#forge:plates/steel`, `#forge:rods/steel`
    - `#forge:ingots/brass`, `#forge:plates/brass` (`create:brass_sheet`), `#forge:plates/iron`, `create:brass_casing`
  - **Fluids** (verified in `v5.5.5` `overrides/scripts/Generic/tag.zs` and `Beta` `overrides/kubejs/server_scripts/tags/fluids.js`):
    - Include BOTH `#forge:seedoil` (`v5.5.5`) and `#forge:seed_oil` (`Beta`) in our data-driven fuel definitions alongside `#forge:gasoline`, `#forge:diesel`, `#forge:biodiesel`, `#forge:ethanol`, `#forge:creosote`, `#forge:crude_oil`, and `#forge:plantoil`.

---

## 6. GeckoLib 3 (`1.18.2`) vs. GeckoLib 4 (`1.20.1`)

### 6.1 Verified Maven Coordinates (Cloudsmith)

Verified directly from `https://github.com/bernie-g/geckolib/wiki/Installation-(Geckolib3)` and `Installation-(Geckolib4)`:

```groovy
repositories {
    maven {
        name = "GeckoLib"
        url = "https://dl.cloudsmith.io/public/geckolib3/geckolib/maven/"
        content {
            includeGroupByRegex("software\\.bernie.*")
            includeGroup("com.eliotlash.mclib") // Required for 1.20.1 Forge
        }
    }
}
```
- **`1.18.2` (Exact DeceasedCraft `v5.5.5` JAR):**
  ```groovy
  implementation fg.deobf("software.bernie.geckolib:geckolib-forge-1.18:3.0.57")
  ```
- **`1.20.1` (Exact DeceasedCraft `Beta-5.10.17` JAR — requires `mclib:20` + MixinGradle `0.7.+`):**
  ```groovy
  implementation fg.deobf("software.bernie.geckolib:geckolib-forge-1.20.1:4.7")
  implementation("com.eliotlash.mclib:mclib:20")
  ```

### 6.2 Class & First-Person Rendering Delta Table

| Concept | GeckoLib 3 (`3.0.57`, `1.18.2`) | GeckoLib 4 (`4.7`, `1.20.1`) |
| :--- | :--- | :--- |
| **Animatable Interface** | `IAnimatable` (items, blocks, entities) | Specialized: `GeoItem`, `GeoBlockEntity`, `GeoEntity` |
| **Instance Cache / Factory** | `AnimationFactory` (`GeckoLibUtil.createFactory(this)`) | `AnimatableInstanceCache` (`GeckoLibUtil.createInstanceCache(this)`) |
| **Controller Registration** | `registerControllers(AnimationData data)` | `registerControllers(AnimatableManager.ControllerRegistrar controllers)` |
| **Animation Builder** | `new AnimationBuilder().addAnimation("fire", ILoopType.EDefaultLoopTypes.LOOP)` | `RawAnimation.begin().thenLoop("fire")` (cache as `static final`!) |
| **Animation Event / State** | `AnimationEvent<T>` | `AnimationState<T>` (uses typed `DataTickets`) |
| **Model Base Class** | `AnimatedGeoModel<T>` | `GeoModel<T>` (or `DefaultedItemGeoModel` / `DefaultedBlockGeoModel`) |
| **First-Person Item Renderer Hook** | Override `Item#initializeClient(Consumer<IItemRenderProperties>)` → `getItemStackRenderer()` returning `GeoItemRenderer<T>` | Override `Item#initializeClient(Consumer<IClientItemExtensions>)` → `getCustomRenderer()` returning `GeoItemRenderer<T>` |
| **Server-Triggered Item Animations** | Manual `SimpleChannel` packet + `GeckoLibNetwork` / `ISyncable` | Built-in `SingletonGeoAnimatable.registerSyncedAnimatable(this)` + `triggerAnim(player, GeoItem.getOrAssignId(stack, serverLevel), controller, animName)` |
| **Emissive / Glowing Layer** | `LayerGlowingAreasGeo` / custom `RenderType.eyes(...)` pass | `AutoGlowingGeoLayer` (supports `*_glowmask.png`!) |
| **Custom Arm / Recoil Hooks** | Apply procedural recoil/sway transforms in `GeoItemRenderer#renderByItem` via `PoseStack` + `IClientItemExtensions`/`IItemRenderProperties#getArmPose` (`HumanoidModel.ArmPose.BOW_AND_ARROW` or `CROSSBOW_HOLD` for two-handed pose). | Same `PoseStack` recoil transform + `IClientItemExtensions#getArmPose(...)` (compatible with `playerAnimator` and `tp_shooting` in both packs!). |
| **Oculus Compatibility Note** | `v5.5.5` includes `GeckoLibOculusCompat-Forge-1.0.1.jar`; avoid custom non-standard vertex formats in GeoRenderers. | `Oculus 1.8.0` natively handles GeckoLib 4 standard `RenderType` passes (`entityCutoutNoCull`, `entityTranslucent`, `eyes`). |

---

## 7. VFX, Emissivity, Dynamic Lighting & Shader Pipeline

### 7.1 Iris / Oculus-Safe Custom Particle Rendering
DeceasedCraft ships **Oculus `1.6.4`** (`1.18.2`, with `oculusparticlefix-1.0.jar`) and **Oculus `1.8.0`** (`1.20.1`), pre-configured with `ComplementaryReimagined_r2.2.zip` (`overrides/config/oculus.properties`).

- **Strict Rule — NO Custom GLSL Particle Shaders:** Iris/Oculus replaces vanilla's `ShaderInstance` bindings with shaderpack G-buffer programs (`gbuffers_textured`, `gbuffers_textured_lit`, `gbuffers_particles`). A custom `ParticleRenderType` that binds a custom `ShaderInstance` or alters blend/depth state outside Iris's known pipeline causes black squares, invisible flames, or depth-sorting glitches under BSL, Complementary, Photon, Bliss, and Spooklementary.
- **Verified Safe Pipeline:**
  - Use **`ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT`** for soft layered volumetric flame plumes, sparks, and rising smoke billboards.
  - Use **`ParticleRenderType.PARTICLE_SHEET_LIT`** (or `PARTICLE_SHEET_OPAQUE`) for crisp core sparks/embers where alpha-blended sorting is unnecessary.
  - Override `Particle#getLightColor(float partialTick)` to return **`LightTexture.FULL_BRIGHT` (`0x00F000F0` / `15728880`)** for flame cores, nozzle flash, and glowing embers—this makes flames self-luminous in vanilla AND triggers bloom/emissive rendering cleanly under Iris/Oculus shaderpacks without custom shaders!
  - Let rising soot/smoke particles use standard `super.getLightColor(partialTick)` so smoke properly catches shadows and darkens at night.

### 7.2 LabPBR 1.3 Material Standard (`_s.png` & `_n.png`)
Verified from the official LabPBR 1.3 specification (`https://shaderlabs.org/wiki/LabPBR_Material_Standard`, `https://bonemeal.io/labpbr`) for full visual fidelity across **BSL, Complementary (Reimagined/Unbound + Euphoria), Photon, Bliss, and Spooklementary**:

- **Companion Textures:** Ship `*_s.png` (Specular) and optionally `*_n.png` (Normal) alongside every block, item, and GeckoLib weapon/turret albedo texture (`assets/tacticalchemthrowers/textures/...`).
- **LabPBR 1.3 `_s.png` (Linear RGBA, must preserve 8-bit Alpha channel!):**
  - **R (Perceptual Smoothness):** `0–255` (`1 - sqrt(roughness)`). Brushed brass/steel casings: `140–200`; matte soot-blackened nozzle shroud: `40–80`; glass fuel gauge: `240–255`.
  - **G (F0 / Hardcoded Metals):** Dielectrics `0–229` (rubber grips/hoses ≈ `10–14`, painted steel ≈ `12–15`); Hardcoded Metals **`230–237`** (`230` = Iron/Steel, `231` = Gold/Brass highlights, `234` = Copper, `233` = Chrome).
  - **B (Porosity / Subsurface Scattering):** `0–64` = porosity (matte/cloth/rust); `65–255` = SSS (0 for opaque metals).
  - **A (Emission — CRITICAL RULE):**
    - **`1–254`** = linear emissive intensity (pilot light flame tip, glowing heat-coil / superheated nozzle throat, pressure gauge backlight = **`220–254`**).
    - **`255`** (or `0`) = **emission disabled (zero glow)**. *Never leave non-emissive pixels at alpha `1–254`, or the entire weapon will glow neon under shaders!*
- **LabPBR 1.3 `_n.png`:** `R/G` = X/Y normal (DirectX Y-down convention), `B` = Ambient Occlusion (`255` = unoccluded), `A` = POM Height (`255` = surface).

### 7.3 Dynamic Lighting Integration (`Lucent` vs. `Sodium/Embeddium Dynamic Lights`)

| Pack & Mod | Mod ID & Maven | Integration Mechanism | Pack Config Caveat (Verified) |
| :--- | :--- | :--- | :--- |
| **`v5.5.5` (`1.18.2`) — Lucent `1.2.2`** | `lucent`<br>Maven: `https://maven.moddinglegacy.com/artifactory/modding-legacy/`<br>Artifact: `com.legacy:lucent:1.18.2-1.2.2` *(compileOnly)* | 1. **Code API:** Annotate a client plugin class with `@LucentPlugin` implementing `ILucentPlugin` to dynamically register held-item luminance (pilot light = `8`, active firing = `14–15`) and emissive nozzle textures.<br>2. **Resource Pack JSON:** `assets/tacticalchemthrowers/lucent/...` for static fallback. | `lucent-client.toml` has `heldItemsGlow = true`, `burningEntitiesGlow = true` (level `10`), `lightRefreshRate = 6`. |
| **`Beta-5.10.17` (`1.20.1`) — Sodium/Embeddium Dynamic Lights `1.0.10`** | `sodiumdynamiclights`<br>Repo: `https://github.com/txnimc/SodiumDynamicLights` *(multiloader port of LambDynamicLights; commit `1dd431d` restored `lambdynlights` API package compat)* | 1. **Resource Pack JSON (Zero-Code, Safest):** Provide LambDynamicLights-format item light JSONs (and `#lambdynlights:water_sensitive` tag so pilot-light flames extinguish underwater).<br>2. **Optional Soft API:** Guard with `ModList.get().isLoaded("sodiumdynamiclights")` for dynamic NBT-state luminance (pilot lit vs. firing vs. idle) via `DynamicLightHandlers` / `ItemLightSources` reflection/bridge. | **CRITICAL VERIFIED CONFIG:** `sodiumdynamiclights-client.toml` sets **`self = true`**, **`entities = false`**, **`block_entities = false`**, `water_sensitive_check = true`! Therefore, **held-item dynamic lighting (`self`) works out of the box**, whereas turret blocks MUST emit vanilla block light (`BlockBehaviour.Properties#lightLevel(state -> state.getValue(FIRING) ? 14 : 0)`) so turrets illuminate the battlefield even with `block_entities = false`! |

---

## 8. Soft-Dependency Integration APIs Reference

All hooks below MUST be strictly optional (`ModList.get().isLoaded("<modid>")` → isolated bridge class):

1. **Open Parties and Claims (`openpartiesandclaims`):**
   - **Maven:** `https://chocolateminecraft.com/maven`
   - **Artifact (Mojang mappings `< 1.21.1`, NO `fg.deobf` per upstream README!):**
     - `1.18.2`: `compileOnly "xaero.pac:open-parties-and-claims-forge-1.18.2:0.20.1:dev"`
     - `1.20.1`: `compileOnly "xaero.pac:open-parties-and-claims-forge-1.20.1:0.25.8:dev"`
   - **Entrypoints (Verified):**
     - `xaero.pac.common.server.api.OpenPACServerAPI.get(MinecraftServer)`
     - `getPartyManager()` → party membership & mutual ally checks (`getPartyByMember(UUID)`, `isAlly(UUID)`)
     - `getServerClaimsManager()` → `get(ResourceLocation dim, ChunkPos pos)` (`IPlayerChunkClaimAPI`)
     - `getChunkProtection()` → `IChunkProtectionAPI` (block placement, fire spread, and entity protection checks).
2. **FTB Teams (`ftbteams`):**
   - **API Package Delta:** `dev.ftb.mods.ftbteams.FTBTeamsAPI` (`1.18.2`) → `dev.ftb.mods.ftbteams.api.FTBTeamsAPI` (`1.20.1`, accessed via `FTBTeamsAPI.api().getManager().arePlayersInSameTeam(uuidA, uuidB)`).
   - **Usage:** Server-side teammate check inside `CombatProtectionResolver` when `friendlyFireTeams = false`.
3. **Cold Sweat (`cold_sweat`, `v5.5.5` `1.18.2` only):**
   - **Verified Official Docs (`Momo-Softworks/Cold-Sweat-Documentation`):**
     - Utility class `Temperature`: `get(LivingEntity, Trait)`, `set(LivingEntity, Trait, double)`, `add(LivingEntity, Trait, double)`, `Temperature.convert(double, Units, Units, boolean)`.
     - Use a bounded `TempModifier` (or subtle clamped `Trait.WORLD` / `Trait.CORE` bump capped well below `Maximum Habitable Temperature = 1.619`), skipped when player has `MobEffects.FIRE_RESISTANCE`.
4. **Legendary Survival Overhaul (`legendarysurvivaloverhaul`, `Beta-5.10.17` `1.20.1` only):**
   - **Upstream Repo (`sfiomn/LegendarySurvivalOverhaul`, branch `1.20.1`):**
     - Register a subtle `ModifierBase` / `TemperatureModifier` (or apply via LSO's `TemperatureUtil` API on its 20-tick update cadence) when actively firing a thermal chemthrower, capped at `+2.5` LSO degrees so it warms the player in winter without triggering hyperthermia.
5. **Zombie Awareness (`zombieawareness`, both packs):**
   - No compile-time dependency needed! Emit standard server-side `Level#playSound(...)` calls (`SoundSource.PLAYERS` / `SoundSource.BLOCKS`) at a throttled cadence (`10–20` ticks) plus real block light (`TemporaryFlameBlock` / turret `LIT` blockstate) so Zombie Awareness's built-in `awareness_Sound` and `awareness_Light` hooks respond organically.

---

## 9. Lootr-Safe Global Loot Modifiers (GLMs)

- **How Lootr Works:** Lootr converts vanilla/modded `RandomizableContainerBlockEntity` chests (when enabled, as in `v5.5.5` and multiplayer `Beta-5.10.17` servers) into per-player Lootr containers that store the original `ResourceLocation lootTable` and `long lootTableSeed`. When **each unique player** opens the container for the first time, Lootr calls vanilla's `LootTable#fill(...)` / `getRandomItems(...)` with a randomized per-player seed (`randomise_seed = true`).
- **Why Forge GLMs Are Automatically 100% Lootr-Safe:** Forge intercepts `LootTable#getRandomItems` and runs every registered `IGlobalLootModifier` whose `LootItemCondition[]` matches (e.g., `LootTableIdCondition` matching DeceasedCraft Lost Cities / industrial / military chest tables). Because Lootr delegates loot generation to `LootTable`, our GLM runs cleanly for every player in Lootr chests AND for standard chests when `lootr-common.toml` has `disable = true` (`Beta-5.10.17` singleplayer default).
- **Strict Anti-Pattern:** Never inject loot by mutating `ChestBlockEntity` inventories in `ChunkEvent.Load` or `PlayerInteractEvent.RightClickBlock`—doing so breaks Lootr conversion, duplicates items, or skips subsequent players.

---

## 10. Recommended Multi-Version Gradle Project Structure

### Architectural Decision: Shared Pure-Java Core + Versioned Forge Subprojects vs. Stonecutter

Because our two targets (`1.18.2` vs. `1.20.1`) span **three simultaneous major breaking rewrites**:
1. **Minecraft / Forge `1.18.2` → `1.20.1`** (`DamageType`, Codec GLMs, `ForgeCapabilities`, `CreativeModeTab`, `RegisterKeyMappingsEvent`, `RenderLevelStageEvent`),
2. **Create `0.5.1.f` → Create `6.0.6`** (Flywheel `0.6` → `1.0`, monolithic Ponder → `net.createmod.ponder`, `api.*` package relocations, `SimpleRegistry`), and
3. **GeckoLib `3.0.57` → GeckoLib `4.7`** (complete interface/renderer rewrite),

using heavy `#ifdef`-style comment preprocessing across every Create/GeckoLib/Forge class would become noisy and error-prone in IDE refactoring. Instead, we recommend a **Clean Multi-Project Gradle Layout** (with optional Stonecutter only if expanding later to `1.21.1 NeoForge`):

```text
tactical-chemthrowers/
├── settings.gradle                     // include("core", "forge-1.18.2", "forge-1.20.1")
├── build.gradle                        // Shared versioning, Java 17 toolchain, spotless/checkstyle
├── gradle.properties                   // mod_id=tacticalchemthrowers, mod_version=...
├── core/                               // Pure Java 17 (ZERO Minecraft/Forge/Create/GeckoLib imports!)
│   └── src/main/java/com/tacticalchemthrowers/core/
│       ├── fuel/                       // FuelProfile schema, lookup priority (exact ID -> tag -> reject), burn math
│       ├── physics/                    // JetGeometry capsule/cone raymarch & falloff math (unit-testable via JUnit 5!)
│       ├── combat/                     // HeatTracker ramp curves, hybrid armor-bypass math, overheat curves
│       └── turret/                     // Yaw/pitch slew rate math, lead/range alignment (aligned with jet distance!)
├── shared-assets/                      // Version-agnostic textures (+ LabPBR _s/_n), .ogg sounds, en_us.json, Blockbench geo/anim JSONs
├── forge-1.18.2/                       // ForgeGradle 5/6 | MC 1.18.2 | Forge 40.2.4 | Create 0.5.1.f | GeckoLib 3.0.57
│   ├── build.gradle                    // tterrag maven, Cloudsmith GeckoLib 3, BlameJared IE, ModdingLegacy Lucent, Xaero OPAC
│   └── src/main/java/com/tacticalchemthrowers/
│       ├── forge118/                   // Capabilities, DamageSource, GlobalLootModifierSerializer, ClientRegistry, RenderLevelLastEvent
│       ├── create05/                   // Create 0.5.1.f KineticBlockEntity, IHaveGoggleInformation, IWrenchable
│       ├── geckolib3/                  // IAnimatable, AnimationFactory, GeoItemRenderer (IItemRenderProperties)
│       └── compat/                     // Soft bridges: OPAC 0.20, FTB Teams 1802, Cold Sweat 2.2, Lucent 1.2
└── forge-1.20.1/                       // ForgeGradle 6   | MC 1.20.1 | Forge 47.4.0 | Create 6.0.6   | GeckoLib 4.7
    ├── build.gradle                    // maven.createmod.net, Ponder 1.0, Flywheel 1.0, GeckoLib 4 + mclib:20, Xaero OPAC
    └── src/main/java/com/tacticalchemthrowers/
        ├── forge120/                   // ForgeCapabilities, DamageType JSON, Codec GLM, CreativeModeTab, RegisterKeyMappingsEvent
        ├── create6/                    // Create 6.0.6 KineticBlockEntity, api.equipment.goggles, api.stress.BlockStressValues
        ├── geckolib4/                  // GeoItem/GeoBlockEntity, AnimatableInstanceCache, SingletonGeoAnimatable, IClientItemExtensions
        └── compat/                     // Soft bridges: OPAC 0.25, FTB Teams 2001, LSO 2.3, SodiumDynamicLights 1.0
```

**Why This Layout Wins for `tacticalchemthrowers`:**
- **100% Fast JUnit 5 Unit Tests in `:core`:** Fuel registry precedence, no-mixing tank rules, jet capsule collision math, heat-stacking curves, and turret yaw/pitch slew math run in milliseconds without launching Minecraft.
- **Zero Preprocessor Fragility:** `:forge-1.18.2` and `:forge-1.20.1` both compile cleanly in IntelliJ IDEA / CI simultaneously (`./gradlew :core:test :forge-1.18.2:build :forge-1.20.1:build`) with full IDE autocomplete against their true Create `0.5.1.f` vs. `6.0.6` and GeckoLib `3` vs. `4` classpaths.
- **Single Source of Truth for Art & Audio:** Both Forge modules include `shared-assets/` via Gradle `sourceSets.main.resources.srcDir("../shared-assets")` (with only version-specific `pack.mcmeta`, `damage_type/` JSONs, and GLM JSONs kept per version).
- *(Alternative Note)*: If a future milestone adds `1.21.1 NeoForge`, **Stonecutter** (`dev.kikugie.stonecutter`, template `rotgruengelb/stonecutter-mod-template`) is well-suited for keeping `1.20.1` + `1.21.1` unified while keeping `1.18.2` cleanly separated.

---

## 11. Primary Source Reference Index

- **Create Developer Wiki (`1.20.1` Forge / Create 6.0 Maven):** https://wiki.createmod.net/developers/depend-on-create/forge-1.20.1
- **Create `6.0.0` Official Changelog & API Changes:** https://github.com/Creators-of-Create/Create/wiki/6.0.0
- **Create `0.5.1.x` (`1.18.2`) Maven Guide:** https://github.com/Creators-of-Create/Create/wiki/Depending-on-Create/3bddd0e5ee4924778c6f1f6cbe90dc0b42b3ed26
- **Create Issue #10830 (Wrench exact-item vs. tag handling):** https://github.com/Creators-of-Create/Create/issues/10830
- **Create Issue #9251 (KineticBlockEntity flicker score):** https://github.com/Creators-of-Create/Create/issues/9251
- **MinecraftForge Official Docs — Capabilities (`1.20.1`):** https://docs.minecraftforge.net/en/latest/datastorage/capabilities/
- **MinecraftForge Official Docs — Global Loot Modifiers (`1.18.x` vs. `1.20.1`):** https://docs.minecraftforge.net/en/1.18.x/resources/server/glm/ and https://docs.minecraftforge.net/en/latest/resources/server/glm/
- **MinecraftForge Official Docs — Key Mappings (`1.20.1`):** https://docs.minecraftforge.net/en/latest/misc/keymappings/
- **MinecraftForge Official Docs — Creative Tabs & Items (`1.20.1`):** https://docs.minecraftforge.net/en/latest/items/
- **Data-Driven `DamageType` JSON & Tags (`1.19.4+` / `1.20.1`):** https://wiki.fabricmc.net/tutorial:damagetypes
- **GeckoLib 3 Installation (`1.18.2`):** https://github.com/bernie-g/geckolib/wiki/Installation-(Geckolib3)
- **GeckoLib 4 Installation (`1.20.1`):** https://github.com/bernie-g/geckolib/wiki/Installation-(Geckolib4)
- **GeckoLib 3 → 4 Migration & Class Renames:** https://github.com/bernie-g/geckolib/wiki/Geckolib-4-Changes
- **Immersive Engineering Repository & BlameJared Maven:** https://github.com/BluSunrize/ImmersiveEngineering (`https://maven.blamejared.com`)
- **Open Parties and Claims API & Xaero's Maven:** https://github.com/thexaero/open-parties-and-claims (`https://chocolateminecraft.com/maven`)
- **FTB Teams Repository:** https://github.com/FTBTeam/FTB-Teams
- **Cold Sweat Official Documentation:** https://github.com/Momo-Softworks/Cold-Sweat-Documentation
- **Legendary Survival Overhaul Repository (`1.20.1`):** https://github.com/sfiomn/LegendarySurvivalOverhaul
- **Lucent Dynamic Lighting Mod & API (`1.18.2`):** https://gitlab.com/modding-legacy/lucent
- **Sodium/Embeddium Dynamic Lights (`1.20.1`):** https://github.com/txnimc/SodiumDynamicLights
- **LabPBR 1.3 Material Standard:** https://shaderlabs.org/wiki/LabPBR_Material_Standard and https://bonemeal.io/labpbr
- **Stonecutter Multi-Version Template:** https://github.com/rotgruengelb/stonecutter-mod-template
