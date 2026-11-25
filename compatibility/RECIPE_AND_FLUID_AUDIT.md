# DeceasedCraft Recipe, Fluid & Fuel Audit — Create: Tactical ChemThrowers

**Mod ID:** `tacticalchemthrowers`  
**Audited Archives:**
- `DeceasedCraft-5.5.5.zip` (`MC 1.18.2`, `forge-40.2.4`, SHA-256 `e93668e97a8061bebfdf16424bc3a1702f262b142cbf13ecd3b165eb246a9f1b`)
- `DeceasedCraft_Beta-5.10.17.zip` (`MC 1.20.1`, `forge-47.4.0`, SHA-256 `870ca9d83b05d9aaa3be032c0b741f46349acf8a8561666f93cf96b30645eb61`)
- `DeceasedCraft_Beta_DH_Edition-5.10.17.zip` (`overrides/` byte-for-byte identical to Standard Beta `5.10.17`)

---

## 1. Archive-Verified Fluid Inventory

DeceasedCraft completely swapped its petroleum refining backbone between `v5.5.5` (**Immersive Petroleum** + **Ultimate Car Mod**) and `Beta 5.10.17` (**Create: Diesel Generators** + **DragN's VV: Refueled**), while retaining **Immersive Engineering** and **Create Crafts & Additions** in both branches.

### 1.1 DeceasedCraft v5.5.5 (`1.18.2`) Fluid Inventory

**Primary Archive Evidence:**
- `overrides/kubejs/exported/tags/fluids.txt` (complete exported fluid tag registry)
- `overrides/defaultconfigs/car/fuel.toml` (vehicle fuel allowlist)
- `overrides/defaultconfigs/immersivepetroleum-server.toml` (Portable Generator & Motorboat fuels)
- `overrides/scripts/Generic/material.zs` (bioethanol, seed oil, `#car:gas_station` tags)
- `overrides/scripts/Removal/car_removal.zs` & `overrides/scripts/Removal/removal.zs` (fluid removals & JEI hiding)

| Mod Namespace | Verified Fluid IDs | Active Fluid Tags in `5.5.5` | Pack Status & Notes |
| --- | --- | --- | --- |
| `immersivepetroleum` | `napalm`, `gasoline`, `diesel`, `diesel_sulfur`, `kerosene`, `naphtha`, `naphtha_cracked`, `benzene`, `crudeoil`, `gasoline_additives`, `lubricant`, `lubricant_cracked`, `ethylene`, `propylene` | `#forge:napalm`, `#forge:gasoline`, `#forge:diesel`, `#forge:diesel_sulfur`, `#forge:kerosene`, `#forge:naphtha`, `#forge:naphtha_cracked`, `#forge:benzene`, `#forge:crude_oil`, `#immersivepetroleum:burnable_in_flarestack`, `#immersiveengineering:drill_fuel`, `#car:gas_station` (`gasoline`, `diesel`) | Active primary petroleum chain. `immersivepetroleum-server.toml` burns `naphtha`, `gasoline`, and `benzene` in Portable Generator & Motorboat; `car/fuel.toml` accepts `gasoline` (`100`) and `diesel` (`150`). `traps.snbt` lists `gasoline`, `naphtha`, `benzene`, and `napalm` for flame defense. |
| `immersiveengineering` | `biodiesel`, `ethanol`, `plantoil`, `creosote`, `redstone_acid`, `phenolic_resin`, `acetaldehyde`, `herbicide`, `concrete`, `potion` | `#forge:biodiesel`, `#forge:ethanol`, `#forge:plantoil`, `#forge:creosote`, `#immersiveengineering:drill_fuel` (`biodiesel`), `#car:gas_station` (`biodiesel`), `#immersivepetroleum:burnable_in_flarestack` (`plantoil`, `creosote`, `ethanol`) | Active bio/coal-coke fuel chain. `car/fuel.toml` accepts `biodiesel` (`50`); `traps.snbt` lists `biodiesel_bucket`. |
| `createaddition` | `bioethanol`, `seed_oil` | `#forge:biofuel`, `#forge:ethanol` (`bioethanol`); `#forge:plantoil` (`seed_oil`) | Active Create-side bio-fluids. `material.zs` L70–75 overrides recipes: `seed_oil` (`2x #forge:seeds -> 50 mB`), `bioethanol` (`biomass + sugar -> 60 mB`). `removal.zs` L32 strips `seed_oil` from `#minecraft:water`. |
| `car` *(Ultimate Car Mod)* | `bio_diesel`, `canola_oil`, `methanol`, `canola_methanol_mix`, `glycerin` | Stripped from `#minecraft:water` | **PACK-DISABLED.** `car_removal.zs` removes all `car` refining machines, hides all 5 fluids & buckets from JEI (`// Remove cars all fluid type, since only diesel from IE will be used.`). Must be **rejected** by our fuel registry. |
| `create` / `minecraft` / `biomesoplenty` | `minecraft:water`, `minecraft:lava`, `create:honey`, `create:chocolate`, `create:tea`, `biomesoplenty:blood` | `#create:bottomless/allow` (`water`, `lava`), `#forge:honey`, `#forge:chocolate`, `#forge:tea`, `#biomesoplenty:blood` | Non-fuel fluids (`removal.zs` L30–31 also strips `create:honey` and `create:chocolate` from `#minecraft:water`). Explicitly **rejected** as chemthrower fuels. |

### 1.2 DeceasedCraft Beta 5.10.17 (`1.20.1`) Fluid Inventory

**Primary Archive Evidence:**
- `overrides/kubejs/server_scripts/tags/fluids.js` (KubeJS fluid tag unifications)
- `overrides/defaultconfigs/refueled-server.toml` (vehicle fuel allowlist & canister capacity)
- `overrides/kubejs/server_scripts/tags/car_parts.js` (`#deceasedcraft:vehicle_fuels` bucket tag)
- `overrides/config/createdieselgenerators-common.toml` (CDG canister & tool capacities)
- `overrides/kubejs/server_scripts/recipes/deceasedcraft/material.js` (CDG ethanol & plant oil recipe removals, seed oil nerf, rubber & resistant fiber fluid usage)
- `overrides/kubejs/server_scripts/recipes/refueled/items.js` (redstone acid in diesel engine assembly)

| Mod Namespace | Verified Fluid IDs | Active Fluid Tags in `Beta 5.10.17` | Pack Status & Notes |
| --- | --- | --- | --- |
| `createdieselgenerators` | `gasoline`, `diesel`, `biodiesel`, `crude_oil`, `ethanol` *(recipe removed)*, `plant_oil` *(recipe removed)* | `#forge:gasoline` (`gasoline`), `#forge:diesel` (`diesel`), `#forge:biodiesel` (`biodiesel`), `#forge:crude_oil` (`crude_oil`) — reinforced explicitly by `tags/fluids.js` | Active primary petroleum chain replacing IP. `refueled-server.toml` accepts `gasoline` (`1.0`), `diesel` (`0.8`), and `biodiesel` (`0.6`). `material.js` L105–111 **removes** CDG's basin/bulk fermentation (`ethanol`) and compacting (`plant_oil`) recipes! `createdieselgenerators-common.toml` sets Canister capacity `4,000 mB` (+`1,000 mB`/level) and fluid tool capacity `200 mB`. |
| `immersiveengineering` | `biodiesel`, `ethanol`, `plantoil`, `creosote`, `redstone_acid`, `phenolic_resin`, `acetaldehyde`, `herbicide`, `concrete`, `potion` | `#forge:seed_oil` (`plantoil`, added in `tags/fluids.js` L3), `#forge:biodiesel`, `#forge:ethanol`, `#forge:plantoil`, `#forge:creosote` | Active bio/industrial fluid chain. `refueled-server.toml` accepts `immersiveengineering:biodiesel` (`0.6`). `material.js` uses `phenolic_resin` + `#forge:seed_oil` for `deceasedcraft:rubber_base`, and `redstone_acid` for `deceasedcraft:rubber` and CDG diesel engine Sequenced Assembly. |
| `createaddition` | `bioethanol`, `seed_oil` | `#forge:seed_oil` (`seed_oil`, added in `tags/fluids.js` L2), `#forge:biofuel`, `#forge:ethanol`, `#forge:plantoil` | Active Create-side bio-fluids. `material.js` L98–114 keeps `bioethanol` (`sugar + biomass -> 60 mB`) and nerfs `seed_oil` to `10x #forge:seeds -> 20 mB`. |
| `createbigcannons` | `molten_nethersteel` (plus molten bronze/cast iron/steel) | Molten metal tags | Industrial casting fluids (`material.js` L166 mixes `molten_nethersteel` + `phenolic_resin` for `deceasedcraft:resistant_fiber`). Explicitly **rejected** as flamethrower fuel. |
| `immersivepetroleum` | *(Mod NOT installed)* | *(None)* | Absent from `Beta 5.10.17` manifest. Note: `overrides/config/ftbquests/quests/chapters/machinery.snbt` still retains unmigrated WIP references to `immersivepetroleum:*` advancements/buckets because `5.10.17` is an incomplete v6 beta; `power_generation.snbt` has already transitioned to `createdieselgenerators:diesel_bucket`. |

---

## 2. Pack Script Recipe Removals & Modifications Audit

DeceasedCraft uses **CraftTweaker + CreateTweaker** (`.zs`) in `v5.5.5` and **KubeJS + KubeJS Create** (`.js`) in `Beta 5.10.17`. Every fuel, metal, component, and machine modification below was verified directly from the archive scripts:

| Domain | v5.5.5 (`overrides/scripts/...`) | Beta 5.10.17 (`overrides/kubejs/...`) | Impact on `tacticalchemthrowers` |
| --- | --- | --- | --- |
| **Seed Oil / Plant Oil** | `Generic/material.zs` L70–71: removes `createaddition:compacting/seed_oil`; replaces with `2x #forge:seeds -> 50 mB createaddition:seed_oil`. `Removal/removal.zs` L32 strips it from `#minecraft:water`. | `recipes/deceasedcraft/material.js` L110–114: removes **both** `createdieselgenerators:compacting/plant_oil` and `createaddition:compacting/seed_oil`; replaces with `10x #forge:seeds -> 20 mB createaddition:seed_oil`. `tags/fluids.js` L2–3 unifies `createaddition:seed_oil` and `immersiveengineering:plantoil` under `#forge:seed_oil`. | Never assume `createdieselgenerators:plant_oil` is craftable in `v6`. Match both `#forge:plantoil` and `#forge:seed_oil` in our fuel registry. |
| **Ethanol / Bioethanol** | `Generic/material.zs` L74–75: removes `createaddition:mixing/bioethanol`; replaces with `createaddition:biomass + minecraft:sugar -> 60 mB createaddition:bioethanol`. IE Fermenter (`immersiveengineering:ethanol`) untouched. | `recipes/deceasedcraft/material.js` L98–107: adds `deceasedcraft:mixing/bio_ethanol` (`sugar + biomass -> 60 mB createaddition:bioethanol`) and **removes all three CDG ethanol recipes** (`basin_fermenting/fermentable`, `basin_fermenting/fermented_spider_eye`, `bulk_fermenting/fermentable`). IE Fermenter untouched. | In `v6`, players obtain ethanol via `createaddition:bioethanol` or `immersiveengineering:ethanol`, **not** `createdieselgenerators:ethanol` (still keep `#forge:ethanol` tag fallback so custom servers work). |
| **Biodiesel & Vehicle Fuels** | `Removal/car_removal.zs`: hides & disables all `car:*` fluids (`car:bio_diesel`, `car:methanol`, etc.) and car refining blocks. `Generic/material.zs` L176–178 adds IP `gasoline`, IP `diesel`, and IE `biodiesel` to `#car:gas_station`. | `defaultconfigs/refueled-server.toml` & `tags/car_parts.js` L23–26 unify vehicle fuels around `createdieselgenerators:gasoline`, `createdieselgenerators:diesel`, `createdieselgenerators:biodiesel`, and `immersiveengineering:biodiesel`. `recipes/refueled/items.js` gates CDG diesel engines behind Sequenced Assembly (`immersiveengineering:redstone_acid`, `create:precision_mechanism`, `#forge:plates/steel`). | Supporting IE + IP (`5.5.5`) and IE + CDG (`v6`) fuels means players use the **exact same fuel infrastructure** for vehicles, generators, and our chemthrowers. |
| **Create Electron Tube → IE Electronic Component** | `Generic/material.zs` L125–155: **removes & JEI-hides `create:electron_tube`**; runs `Replacer` across `create` and `createaddition` replacing `create:electron_tube` with `immersiveengineering:component_electronic`. Rewrites `mechanical_arm` & `rotation_speed_controller` to require `immersiveengineering:component_electronic`. | `recipes/deceasedcraft/material.js` L46–73 & L124–142: globally replaces `create:electron_tube` inputs with `immersiveengineering:component_electronic`; adds Create Sequenced Assembly recipes for `immersiveengineering:component_electronic` and `component_electronic_adv`. | **CRITICAL RECIPE RULE:** Never use `create:electron_tube` in `tacticalchemthrowers` recipes! Use `immersiveengineering:component_electronic` / `component_electronic_adv` (with `forge:conditions` fallback to `create:electron_tube` only if IE is not loaded standalone). |
| **Steel Unification & Production** | `Generic/material.zs` L110: adds superheated Create Mixing (`#forge:dusts/coal_coke` + `#forge:ingots/iron` → `immersiveengineering:ingot_steel`). `Removal/removal.zs` removes `mapperbase` & `zombie_extreme`. `Removal/immersive_removal.zs` removes manual crafting of `stick_iron`, `stick_steel`, `stick_aluminum` & IE blueprints. | `recipes/deceasedcraft/material.js` L88–92 & L212–234: identical superheated Create Mixing for `immersiveengineering:ingot_steel`; replaces IE stick recipes with `ingot + immersiveengineering:wirecutter`. `tags/duplicate_items.js` strips `mapperbase` steel and `createbigcannons:steel_scrap` from steel tags; `startup_scripts/logics/ore_removal.js` removes `zombie_extreme` steel ores. | Always reference steel strictly via `#forge:ingots/steel`, `#forge:plates/steel`, and `#forge:rods/steel` (never hardcoded `mapperbase` or `zombie_extreme` IDs). |
| **Brass Production & Removals** | `Generic/material.zs` L94–95: adds shapeless `#forge:ingots/brass + immersiveengineering:hammer -> create:brass_sheet`. | `recipes/deceasedcraft/material.js` L20: identical hammer recipe for `create:brass_sheet`. `startup_scripts/removals.js` L16–19 removes `create_sa:brass_*` armor. | Use `#forge:plates/brass` and `#forge:ingots/brass` — reliably available in mid-game in both packs. |
| **Mechanical Crafting & Pipes** | `Mod/createbigcannons.zs`, `Mod/car_components.zs`, `Mod/simpleplanes.zs`: pack heavily uses `create:mechanical_crafting` for weapons, ordnance, and vehicles. `Mod/pipez.zs` gates `pipez:fluid_pipe` behind `create:fluid_pipe` + `immersiveengineering:fluid_pipe` + rubber/plastic. `Removal/mutationcraft_removal.zs` L5 removes `mutationcraft:flamethrower`. | `recipes/deceasedcraft/material.js` L253–297 rewrites `createaddition:alternator` and `electric_motor` as 5x5 `create:mechanical_crafting`. `recipes/pipez/items.js` gates `pipez:fluid_pipe` behind `create:fluid_pipe` + rubber/plastic. `material.js` L188–198 crafts `apocalypsenow:fire_module` from `refueled:canister` + `pipez:fluid_pipe` + `createdieselgenerators:gasoline_bucket` + `immersiveengineering:component_electronic`. | `create:mechanical_crafting` + `create:sequenced_assembly` is DeceasedCraft's canonical mid-to-late weapon/machinery gate. |

---

## 3. Immersive Engineering Chemthrower & Turret Audit + Coexistence Plan

### 3.1 Exact Archive Config & Quest Findings

Verified directly from `overrides/defaultconfigs/immersiveengineering-server.toml` and `overrides/config/ftbquests/quests/chapters/traps.snbt` in both archives:

| Config / Quest Key | v5.5.5 (`1.18.2`) | Beta 5.10.17 (`1.20.1`) | Archive Path |
| --- | :---: | :---: | --- |
| `[tools.chemthrower] consumption` | `10` mB/tick (`200 mB/s`) | `10` mB/tick (`200 mB/s`) | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L523` / `L521`) |
| `[tools.chemthrower] scroll` | `true` | `true` | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L525` / `L523`) |
| `[machines.turret] consumption` (idle) | `64` IF/tick | `64` IF/tick | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L186` / `L184`) |
| `[machines.turret] chem_consumption` (shoot) | `32` IF/tick | `32` IF/tick | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L189` / `L187`) |
| `[machines.turret] gun_consumption` (shoot) | `32` IF/tick | `32` IF/tick | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L192` / `L190`) |
| `[machines.squeezer / fermenter / refinery]` | `energyModifier=1.0`, `timeModifier=1.0` | `energyModifier=1.0`, `timeModifier=1.0` | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L244–264` / `L242–262`) |
| `dieselGen_output` | `12288` IF/tick | `8192` IF/tick | `overrides/defaultconfigs/immersiveengineering-server.toml` (`L92`) |
| **Removed/Disabled in Pack Scripts?** | **NO** (both `chemthrower` & `turret_chem` active) | **NO** (both `chemthrower` & `turret_chem` active) | Confirmed absent from `immersive_removal.zs`, `removal.zs`, `removals.js` |
| **FTB Quest Integration** | Quest `67E7EAB22901F74A` *"Tower Defense - Flame Turret"*: task `immersiveengineering:turret_chem`, reward **3x `turret_chem`**, followed by 5 fuel bucket sub-tasks (`ie:biodiesel`, `ip:gasoline`, `ip:naphtha`, `ip:benzene`, `ip:napalm`) | Quest `67E7EAB22901F74A` *"Tower Defense - Flame Turret"*: task `immersiveengineering:turret_chem`, reward **3x `turret_chem`**, followed by `ie:biodiesel_bucket` sub-task | `overrides/config/ftbquests/quests/chapters/traps.snbt` (`L329–485` / `L329–446`) |

### 3.2 Clean Coexistence Design

Because DeceasedCraft explicitly showcases `immersiveengineering:turret_chem` in its official Tower Defense quest line and leaves IE's handheld `immersiveengineering:chemthrower` enabled, **Create: Tactical ChemThrowers** MUST coexist without breaking or replacing IE:

1. **Zero IE Removals or Overrides:** Never remove, hide, or alter recipes, fluid handlers, or loot for `immersiveengineering:chemthrower` or `immersiveengineering:turret_chem`.
2. **Clear Functional Differentiation:**
   - **IE Chemical Thrower** (`10 mB/t`): raw industrial utility sprayer (sprays arbitrary IE-registered chemicals including water/potions/herbicide/acid, requires IE Fluid Tank/Shader bench workflow).
   - **`Create: Tactical ChemThrowers` Handheld** (`4 mB/t` baseline): combat-tuned, pressurized replaceable-cartridge (`50 units = 1,000 mB`, `12.5 s` continuous firing) thermal projector with configurable `15 / 25 / 35`-block range tiers, point-blank lava-like thermal burst, `+10%/hit` consecutive heat ramp (`2.0x` cap, `2.5 s` decay), GeckoLib animation, and `1.5 s` field cartridge swap (`R` / sneak+right-click).
   - **IE Chemthrower Turret** (`64 + 32 IF/t` electrical-only multiblock) vs **`Create: Tactical ChemThrowers` Automated Turret** (Create kinetic SU rotational traverse + FE ignition power + Create/Pipez fluid feed + GUI range/pilot/OPAC & FTB Teams target filtering + optional `Create: Radars` guidance in `v6`).
3. **Shared Fuel Economy:** Every burnable IE fluid (`biodiesel`, `ethanol`, `creosote`, `plantoil`) and petroleum fuel (IP in `5.5.5`, CDG in `Beta 5.10.17`) works seamlessly in both ecosystems with zero duplicate fluids.

---

## 4. Data-Driven Fuel Registry Specification

### 4.1 Registry Path, Unit Scaling & Lookup Precedence

- **Datapack Path:** `data/tacticalchemthrowers/flamethrower_fuels/*.json` (reloaded on `/reload`, synced to clients on login/reload for HUD color, fuel name, and particle rendering).
- **Zero Duplicate Custom Fluids:** `tacticalchemthrowers` registers **0** custom duplicate fluids (no `tacticalchemthrowers:gasoline` or `tacticalchemthrowers:napalm`). All fuels resolve directly to existing pack fluids via Forge fluid capabilities (`IFluidHandler` / `IFluidHandlerItem`).
- **Unit & Consumption Calibration:**
  - Standard cartridge capacity = **`50` fuel units = `1,000 mB`** (`20 mB` per unit).
  - Baseline consumption (`consumption_multiplier = 1.0`) = **`4 mB/tick`** (`0.2 units/tick` = `4 units/second` = `80 mB/second`) → **`250 ticks` (`12.5 seconds`)** of continuous firing per full `1,000 mB` cartridge.
  - Per-tick effective drain uses a sub-mB remainder accumulator: `drain_mb_per_tick = 4.0 * consumption_multiplier`, guaranteeing exact duration math even for fractional multipliers (e.g., `0.85x` or `1.25x`).
- **Deterministic Lookup Precedence:**
  1. **Exact Fluid Registry ID** (`"fluid": "namespace:path"`) — checked first; overrides any tag entry for the same fluid (enables pack-specific tuning, e.g., distinguishing `immersivepetroleum:diesel_sulfur` from refined `immersivepetroleum:diesel` even though both share `#forge:diesel` in `5.5.5`!).
  2. **Fluid Tag Match** (`"tag": "namespace:path"`) — checked second if no exact fluid ID rule exists (ordered by integer `"priority"`, highest first, tie-broken lexicographically by resource ID).
  3. **Reject** — any fluid with no matching entry, or matching an explicit `"rejected": true` rule, is refused by cartridges, filling spouts, and turrets (with clear client tooltip/HUD feedback).

### 4.2 Canonical JSON Schema (`data/tacticalchemthrowers/flamethrower_fuels/<name>.json`)

```json
{
  "type": "tacticalchemthrowers:flamethrower_fuel",
  "fluid": "createdieselgenerators:gasoline",
  "tag": "forge:gasoline",
  "priority": 100,
  "rejected": false,
  "tier": "high_volatile",
  "damage_multiplier": 1.15,
  "close_range_thermal_multiplier": 1.15,
  "range_multiplier": 1.15,
  "consumption_multiplier": 1.15,
  "burn_duration_ticks": 60,
  "heat_ramp_bonus": 0.02,
  "ground_fire_chance": 0.14,
  "ground_fire_duration_ticks": 80,
  "visual_profile": {
    "core_color": "#FFF4B8",
    "outer_color": "#FF6A00",
    "smoke_color": "#3A3A3A",
    "smoke_density": 0.35,
    "ember_density": 0.85,
    "sound_pitch": 1.12
  }
}
```

*(Rules use **either** `"fluid"` for an exact-ID rule **or** `"tag"` for a tag-fallback rule; exact-ID rules always outrank tag rules.)*

### 4.3 Per-Fuel Balance & Visual Profile Matrix (v5.5.5 & Beta 5.10.17)

Baseline (`1.00x`) corresponds to `4 mB/tick` (`12.5 s` / `1,000 mB` cartridge), `15 / 25 / 35`-block configured range tier, `60 ticks` (`3.0 s`) burn duration, and `+10%/hit` heat buildup (`2.0x` cap, `2.5 s` decay).

| Fuel Entry (Exact ID / Fallback Tag) | Pack Availability | Match Type | Damage Mult | Range Mult | Drain Mult (`mB/t`, `s/1000mB`) | Burn (`s`) | Ground Fire Chance / Life | Heat Ramp Bonus | Visual & Audio Profile |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| **`immersivepetroleum:napalm`** (`#forge:napalm`) | `5.5.5` only | Exact ID + Tag | `1.35x` | `1.05x` | `1.25x` (`5.0 mB/t`, `10.0 s`) | `5.0 s` | `0.30` / `7.0 s` *(sticky gel)* | `+0.04`/hit | Deep amber-crimson core `#FFD060` → `#D92B04`, heavy black-ochre gel smoke (`0.75`), viscous arcing droplets, low roaring pitch (`0.88`). |
| **`immersivepetroleum:gasoline`** / **`createdieselgenerators:gasoline`** (`#forge:gasoline`) | Both (`IP` in `5.5.5`, `CDG` in `v6`) | Exact ID + Tag | `1.15x` | `1.15x` | `1.15x` (`4.6 mB/t`, `10.9 s`) | `3.0 s` | `0.14` / `4.0 s` | `+0.02`/hit | Bright incandescent yellow-orange `#FFF4B8` → `#FF6A00`, light crisp smoke (`0.35`), high spark/ember density (`0.85`), sharp pressurized hiss (`1.12`). |
| **`immersivepetroleum:kerosene`** (`#forge:kerosene`) | `5.5.5` only | Exact ID + Tag | `1.20x` | `1.20x` | `1.10x` (`4.4 mB/t`, `11.4 s`) | `3.5 s` | `0.18` / `5.0 s` | `+0.03`/hit | Jet-grade white-gold core `#FFFCE0` → `#FF8C1A`, moderate dark trail (`0.40`), tight laminar cone, crisp turbine pitch (`1.18`). |
| **`immersivepetroleum:naphtha`** & **`naphtha_cracked`** (`#forge:naphtha`, `#forge:naphtha_cracked`) | `5.5.5` only | Exact ID + Tag | `1.10x` | `1.10x` | `1.20x` (`4.8 mB/t`, `10.4 s`) | `3.0 s` | `0.12` / `3.5 s` | `+0.01`/hit | Volatile pale-orange flare `#FFE699` → `#FF7B1A`, light soot (`0.30`), lively ember pop (`0.80`), elevated pitch (`1.15`). |
| **`immersivepetroleum:benzene`** (`#forge:benzene`) | `5.5.5` only | Exact ID + Tag | `1.15x` | `1.00x` | `1.05x` (`4.2 mB/t`, `11.9 s`) | `4.0 s` | `0.20` / `5.5 s` | `+0.02`/hit | Luminous amber-orange `#FFC94D` → `#E64500`, dense dark aromatic soot (`0.80`), heavy embers (`0.70`), throaty burn (`0.95`). |
| **`immersivepetroleum:diesel`** / **`createdieselgenerators:diesel`** (`#forge:diesel`) | Both (`IP` in `5.5.5`, `CDG` in `v6`) | Exact ID + Tag | **`1.00x`** | **`1.00x`** | **`1.00x`** (`4.0 mB/t`, `12.5 s`) | **`3.0 s`** | **`0.15` / `4.5 s`** | `0.00` | **Reference baseline:** rich orange-amber jet `#FFE082` → `#F55D00`, medium diesel soot (`0.50`), balanced embers (`0.65`), steady pitch (`1.00`). |
| **`immersivepetroleum:diesel_sulfur`** (`#forge:diesel_sulfur`) | `5.5.5` only | Exact ID *(overrides `#forge:diesel`)* | `0.95x` | `0.95x` | `1.10x` (`4.4 mB/t`, `11.4 s`) | `3.0 s` | `0.16` / `4.5 s` | `0.00` | Unrefined sour diesel: muted amber-ochre `#E6B84C` → `#CC4400`, thick sulfurous gray-yellow smoke (`0.75`), coarse sparks, rough pitch (`0.92`). |
| **`immersiveengineering:biodiesel`** / **`createdieselgenerators:biodiesel`** (`#forge:biodiesel`) | Both (`IE` in both, `CDG` in `v6`) | Exact ID + Tag | `1.00x` | `1.00x` | `1.00x` (`4.0 mB/t`, `12.5 s`) | `3.0 s` | `0.15` / `4.5 s` | `0.00` | Clean renewable workhorse: warm golden flame `#FFF099` → `#FF7700`, cleaner low-soot plume (`0.35`), smooth pitch (`1.02`). |
| **`immersiveengineering:ethanol`** / **`createaddition:bioethanol`** (`#forge:ethanol`, `#forge:biofuel`) | Both *(note: CDG ethanol recipes removed in `v6`, tag fallback kept)* | Exact ID + Tag | `0.90x` | `0.95x` | `1.15x` (`4.6 mB/t`, `10.9 s`) | `2.5 s` | `0.06` / `2.0 s` *(clean flash)* | `+0.01`/hit | Clean pale-blue-to-cyan-tipped alcohol jet `#A6E7FF` → `#FF9E3D`, minimal smoke (`0.12`), low visibility obstruction indoors, bright hiss (`1.20`). |
| **`immersivepetroleum:crudeoil`** / **`createdieselgenerators:crude_oil`** (`#forge:crude_oil`) | Both (`IP` in `5.5.5`, `CDG` in `v6`) | Exact ID + Tag | `0.85x` | `0.85x` | `1.25x` (`5.0 mB/t`, `10.0 s`) | `4.0 s` | `0.24` / `6.0 s` *(viscous oil slick)* | `-0.01`/hit | Unrefined heavy crude: dark roaring orange `#E07B1F` → `#A82800`, very dense black hydrocarbon soot (`0.95`), strong ballistic droop, heavy chugging pitch (`0.84`). |
| **`immersiveengineering:creosote`** (`#forge:creosote`) | Both | Exact ID + Tag | `0.75x` | `0.80x` | `0.90x` (`3.6 mB/t`, `13.9 s`) | `3.5 s` | `0.22` / `5.5 s` *(tarry)* | `-0.02`/hit | Early-game Coke Oven byproduct: dull crimson-orange `#D97A2B` → `#8C2D04`, heavy dark tar smoke (`0.90`), sputtery low pitch (`0.82`). |
| **`immersiveengineering:plantoil`** / **`createaddition:seed_oil`** (`#forge:plantoil`, `#forge:seed_oil`) | Both *(CDG `plant_oil` recipe removed in `v6`)* | Exact ID + Tag | `0.65x` | `0.75x` | `0.85x` (`3.4 mB/t`, `14.7 s`) | `2.5 s` | `0.10` / `3.0 s` | `-0.03`/hit | Emergency low-pressure vegetable oil: dim warm orange `#FFBB55` → `#CC5200`, thick white-gray oily vapor (`0.65`), heavy low sputtering (`0.80`). |

### 4.4 Explicitly Rejected Non-Fuel Fluids

| Fluid / Tag | Classification | Rationale |
| --- | --- | --- |
| `car:bio_diesel`, `car:canola_oil`, `car:methanol`, `car:canola_methanol_mix`, `car:glycerin` (`5.5.5`) | **Explicitly Rejected** | Explicitly disabled & JEI-hidden by DeceasedCraft (`overrides/scripts/Removal/car_removal.zs`). |
| `minecraft:lava`, `createbigcannons:molten_*` | **Explicitly Rejected** | Molten rock/metal cannot pass through pressurized fuel nozzles or cartridges; preserves balanced thermal progression. |
| `immersiveengineering:redstone_acid`, `phenolic_resin`, `acetaldehyde`, `herbicide`, `concrete`, `potion` | **Explicitly Rejected** | Non-flammable chemical reagents/construction fluids (IE's own Chemical Thrower already handles non-fuel chemical spraying). |
| `immersivepetroleum:lubricant`, `lubricant_cracked`, `gasoline_additives`, `ethylene`, `propylene` | **Explicitly Rejected** | Industrial lubricants, fuel-blending additives, and polymer feedstocks (used for plastic/engine assembly in `5.5.5`, not standalone flamethrower fuels). |
| `minecraft:water`, `create:honey`, `create:chocolate`, `create:tea`, `biomesoplenty:blood` | **Explicitly Rejected** | Water/food/environmental fluids (and flamethrower operation is blocked underwater). |

---

## 5. Recommended DeceasedCraft Crafting Progression & Lootr-Safe Loot Hooks

All recipes below are **strictly additive** (never overriding pack scripts), avoid pack-removed items (especially `create:electron_tube`, `mapperbase:*`, `zombie_extreme:*`, `undead_revamp2:*`), and use Forge tags (`#forge:plates/steel`, `#forge:rods/steel`, `#forge:plates/brass`, `#forge:plates/copper`) so identical progression gates work across both `v5.5.5` and `Beta 5.10.17`.

### 5.1 Mid-to-Late Technology Progression

| Progression Stage | Item / Block | Recipe Type | Verified Pack Ingredients (Both `5.5.5` & `Beta 5.10.17`) | Tech Gate Rationale |
| --- | --- | --- | --- | --- |
| **Stage 1: Early-Mid Tech** *(Create Brass + IE Coke Oven / Blast Furnace)* | **Pressurized Fuel Cartridge** (`50 units` / `1,000 mB`) | Shaped Crafting / Sequenced Assembly | `#forge:plates/brass`, `#forge:plates/copper`, `create:fluid_pipe`, `create:fluid_valve` | Reusable, refillable via Create Spout (`create:filling`), IE Bottling Machine / Tank, or any Forge fluid-handler dock (`IFluidHandlerItem`). No separate custom refueler block required. |
| **Stage 1: Mid-Game Combat** *(Tier 1 Handheld — `15` / `25` block nozzles)* | **Tactical ChemThrower** (Handheld) | **Create Mechanical Crafting** (`5x3` grid) | `#forge:plates/steel`, `#forge:rods/steel`, `#forge:plates/brass`, `create:fluid_pipe`, `create:precision_mechanism`, `immersiveengineering:component_electronic`<sup>1</sup>, `minecraft:flint_and_steel` | Matches DeceasedCraft's exact Mechanical Crafting gate used for `createbigcannons`, `simpleplanes`, and `createaddition:alternator`/`electric_motor`. |
| **Stage 2: Mid-Late Upgrade** *(Extended `35`-block Nozzle & Thermal Baffle)* | **High-Pressure Nozzle Assembly** | **Create Sequenced Assembly** (Deploying + Pressing) | Base `#forge:plates/steel` + `create:fluid_pipe` + `#forge:plates/brass` + `immersiveengineering:component_electronic_adv`<sup>1</sup> | Requires IE Advanced Electronic Component (craftable via IE Blueprint or DeceasedCraft's Create Sequenced Assembly in both packs). |
| **Stage 3: Late-Game Base Defense** *(Automated Rotary Turret)* | **Automated Flamethrower Turret** | **Create Mechanical Crafting** (`5x5` grid) | `create:brass_casing`, `create:precision_mechanism`, `create:mechanical_pump`, `#forge:plates/steel`, `#forge:rods/steel`, `immersiveengineering:component_electronic_adv`<sup>1</sup>, `#forge:wires/electrum` (or `immersiveengineering:coil_mv`), `create:fluid_tank` | Integrates cleanly into existing Create rotational shafts (SU), IE / Create Crafts & Additions / Pipez Forge Energy (`FE`), and Create / IE / Pipez fluid networks (`mB/t`). |

<sup>1</sup> *Standalone fallback:* Use Forge recipe conditions (`forge:mod_loaded` on `"immersiveengineering"`) so that when `tacticalchemthrowers` runs inside DeceasedCraft it uses `immersiveengineering:component_electronic` / `component_electronic_adv`, while standalone Create-only test instances automatically fall back to `create:electron_tube` / `create:precision_mechanism`.

### 5.2 Lootr-Safe Scavenging & Loot Table Hooks

Because `Lootr` (`0.3.25` in `5.5.5`, `0.7.35` in `Beta 5.10.17`) generates per-player instanced inventories through vanilla `LootTable` evaluation with `randomise_seed = true` and `loot_table_blacklist = []`, all loot additions MUST use **Forge Global Loot Modifiers (`GLM`)** (`data/forge/loot_modifiers/global_loot_modifiers.json`). Never place items by mutating chest block entities during chunk generation.

| Scavenge Tier | Loot Pool Contents | Verified DeceasedCraft Chest Loot Tables (`5.5.5` & `v6` Lost Cities) | Standalone Fallback Tables |
| --- | --- | --- | --- |
| **Industrial & Fuel Infrastructure** *(low-moderate chance)* | Empty or partially filled (`200–600 mB` diesel/creosote/ethanol) **Pressurized Fuel Cartridges**, spare igniter valves | `deceasedcraft:chests/gas_station/standard`, `deceasedcraft:chests/car_service/standard`, `deceasedcraft:chests/factory/standard`, `deceasedcraft:chests/factory_pumpjack/standard`, `deceasedcraft:chests/warehouse/standard` | `minecraft:chests/abandoned_mineshaft`, `minecraft:chests/village/village_weaponsmith` |
| **High-Risk Thermal & Military Sites** *(rare)* | Pre-filled gasoline/biodiesel cartridges, **High-Pressure Nozzle Assembly** components, rare worn handheld ChemThrower (never full automated turrets) | `deceasedcraft:chests/factory_blaze/standard`, `deceasedcraft:chests/military/armory_weapons`, `deceasedcraft:chests/military/armory_ammunitions`, `deceasedcraft:chests/military/blaze`, `deceasedcraft:chests/bunker/standard`, `deceasedcraft:chests/laboratory/decontaimination_room`, `deceasedcraft:chests/laboratory/power_room` | `minecraft:chests/nether_bridge`, `minecraft:chests/bastion_treasure`, `minecraft:chests/stronghold_corridor` |

*Note on Beta 5.10.17 loot tables:* In `v5.5.5`, all 102 `deceasedcraft:chests/*` tables live directly under `overrides/kubejs/data/deceasedcraft/loot_tables/chests/`. In `Beta 5.10.17`, worldgen/chest tables are packaged inside the `DeceasedCraft++` (`deceased_expansion-1.10-all.jar`) mod JAR rather than `overrides/kubejs/data/`. Using optional `loot_table_id` GLM predicates guarantees zero console errors if a specific table is renamed or absent across beta updates.
