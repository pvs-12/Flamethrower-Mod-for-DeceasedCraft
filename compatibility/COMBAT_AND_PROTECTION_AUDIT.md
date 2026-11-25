# Combat, Survival & Protection Audit — DeceasedCraft (`v5.5.5` & `Beta-5.10.17`)

**Mod:** Create: Tactical ChemThrowers (`modid: tacticalchemthrowers`)  
**Targets Verified:**
- **Legacy Pack:** `DeceasedCraft-5.5.5.zip` — Minecraft `1.18.2`, Forge `40.2.4` (230 mods)
- **Current Beta Pack:** `DeceasedCraft_Beta-5.10.17.zip` (manifest `5.10.16`, archive `5.10.17`) — Minecraft `1.20.1`, Forge `47.4.0` (317 mods)
- **Distant Horizons Edition:** `DeceasedCraft_Beta_DH_Edition-5.10.17.zip` — Identical `overrides/` tree to `DeceasedCraft_Beta-5.10.17.zip` (0 config/script diffs; adds `DistantHorizons-2.4.5-b-1.20.1-fabric-forge.jar` and raises recommended RAM to 10,240 MB).

Every parameter below was inspected directly from the official DeceasedCraft archive files (`overrides/config/`, `overrides/defaultconfigs/`, `overrides/kubejs/`, and `overrides/scripts/`).

---

## 1. Executive Summary & Pack Delta Matrix

| Domain | DeceasedCraft `v5.5.5` (`1.18.2`) | DeceasedCraft `Beta-5.10.17` (`1.20.1`) | Design Impact for `tacticalchemthrowers` |
| :--- | :--- | :--- | :--- |
| **Fire Tick & Fire Damage** | `do_fire_tick = true`, `fire_damage = true` | `do_fire_tick = true`, `fire_damage = true` | **CRITICAL:** Vanilla fire blocks WILL burn down Lost Cities wooden buildings and player bases. Our ground flames MUST use a custom non-spreading, non-consuming temporary flame system. |
| **Natural Regeneration** | `natural_regeneration = false` (Gamerule + First Aid) | `natural_regeneration = false` (Gamerule + LSO) | **HIGH:** Accidental self-ignition or friendly fire is punishing because players cannot passively heal. Friendly-fire guards and self-splash safety are mandatory. |
| **Claim & Party Protection** | Open Parties & Claims `0.20.1` + FTB Teams `1802.2.9` (NO FTB Chunks installed; leftover snbt only) | Open Parties & Claims `0.25.8` + FTB Teams `2001.3.1` (NO FTB Chunks) | **CRITICAL:** OPAC protects claimed blocks/entities from fire (`fromFireSpread = true`, `entitiesFromFire = true`), but **`playersFromPlayers = false`** by default. We MUST enforce party/team friendly-fire protection ourselves. |
| **Locational Health / Limbs** | First Aid `1.11.1` (`maxHealthHead = 6`, `causeDeathHead = true`) | Legendary Survival Overhaul `2.3.23.1` (`Head = 0.4×`, `Headshot = 1.5×`, broken hearts per injured limb) | **HIGH:** Flame damage MUST be tagged as fire damage so First Aid / LSO distribute thermal burn damage safely instead of instakilling a player's 6 HP head hitbox. |
| **Temperature System** | Cold Sweat `2.2.5.1` (`Fire Resistance Immunity = true`) | Legendary Survival Overhaul `2.3.23.1` (`Player On Fire Modifier = 12.5`) | **MEDIUM:** Soft runtime warmth hooks while firing must be subtle and capped so combat never induces unfair heatstroke. |
| **Firefighter Armor Set** | Armor Set Bonuses `18.13.1` (`apocalypsenow:fire_figther_*` → `minecraft:fire_resistance`) | Armor Set Bonuses `20.14.0` (`apocalypsenow:fire_figther_*` → `minecraft:fire_resistance`) | **HIGH:** Tagging thermal flames as vanilla fire damage automatically grants Firefighter set wearers full thermal immunity and Cold Sweat heat immunity. |
| **Mob HP & Armor Curve** | Vanilla + `incontrol/spawn.json` (`+15` to `+2000 HP`, `+2` to `+40` armor, Hard = `2.0× HP / 1.2× Armor`) | KubeJS `attribute.js` (`20–800 HP`, `2–60` armor) + Spore (`90–2500 HP`, `16–80` armor) + `AttributeFix` | **CRITICAL:** High-tier elites/bosses have **20–80 armor** (uncapped via `AttributeFix`). Pure armor-mitigated damage is crushed; thermal flames need controlled partial armor bypass / armor-shred mechanics. |
| **IE Chemthrower & Turret** | Installed & NOT removed (`10 mB/t`, Turret `64 IF/t` base + `32 IF/t` firing) | Installed & NOT removed (`10 mB/t`, Turret `64 IF/t` base + `32 IF/t` firing) | **HIGH:** Our mod coexists with IE; calibrate fuel burn rates, damage, range, and kinetic/FE costs cleanly alongside IE's baseline. |
| **Zombie AI & Hordes** | Zombie Awareness `1.12.3` (`maxPFRangeSense = 48`), The Hordes `1.5.3a` (`zombiesBurn = false`), Enhanced Celestials (Blood Moon `3.0×` / `4.5×`) | Zombie Awareness `1.13.1` (`maxPFRangeSense = 24`), The Hordes `1.5.4c` (`zombiesBurn = false`, `hordeSpawnMax = 100`) | **MEDIUM:** Emit standard Forge/vanilla sound events (throttled) so Zombie Awareness reacts naturally without spamming pathfind loops. Note zombies do NOT burn in sunlight (`zombiesBurn = false`), making player-applied fire uniquely valuable. |
| **Lootr** | `0.3.25.63` — **Active** (`convert_wooden_chests = true`, `randomise_seed = true`) | `0.7.35.94` — **Disabled by default** (`disable = true`, toggled on for MP servers) | **HIGH:** Use Forge Global Loot Modifiers (GLMs) only—never mutate chest block entities directly—so loot works identically whether Lootr is enabled or disabled. |

---

## 2. Verified Archive Configuration Audit

### 2.1 Global GameRules (`globalgamerules-common.toml`)

Verified from `overrides/config/globalgamerules-common.toml` in both archives:

| GameRule | `v5.5.5` (`1.18.2`) | `Beta-5.10.17` (`1.20.1`) | Notes |
| :--- | :--- | :--- | :--- |
| `do_fire_tick` | `true` | `true` | Fire spreads and destroys flammable blocks globally. |
| `fire_damage` | `true` | `true` | Entities take fire damage. |
| `natural_regeneration` | `false` | `false` | Players do NOT regenerate health from hunger. |
| `mob_griefing` | `true` | `true` | Hostile mobs can break/grief blocks. |
| `keep_inventory` | `false` | `false` | Hardcore survival economy. |
| `drowning_damage` / `fall_damage` / `freeze_damage` | `true` / `true` / `true` | `true` / `true` / `true` | All environmental hazards active. |
| `max_entity_cramming` | `36` | `24` | Large horde clusters form tightly—piercing flame cones excel here. |
| `flamethrower_natural_spawn` (Zombie Extreme) | `false` | *(absent)* | Pack disables Zombie Extreme's flamethrower mob natural spawn in 5.5.5. |
| `difficulty` / `set_difficulty` | `NORMAL` / `false` | `NORMAL` / `false` | Server/player chooses difficulty; `incontrol` scales mobs by difficulty. |

### 2.2 Claim & Team Protection (`openpartiesandclaims`, `ftbteams`, `ftbchunks`)

**Installed Mods Verified (`categorized_mods.json`):**
- **Open Parties and Claims:** `open-parties-and-claims-forge-1.18.2-0.20.1.jar` (`v5.5.5`) / `open-parties-and-claims-forge-1.20.1-0.25.8.jar` (`Beta-5.10.17`)
- **FTB Teams:** `ftb-teams-forge-1802.2.9-build.88.jar` (`v5.5.5`) / `ftb-teams-forge-2001.3.1.jar` (`Beta-5.10.17`)
- **FTB Chunks:** **NOT installed** in either pack. (`v5.5.5` retains an unused legacy config file `overrides/defaultconfigs/ftbchunks/ftbchunks-world.snbt` with `disable_protection: false`, `fake_players: "check"`, `protect_unknown_explosions: true`.)

**Open Parties and Claims Server & Default Player Configs**  
Verified from `overrides/defaultconfigs/openpartiesandclaims-server.toml`, `openpartiesandclaims-default-player-config.toml`, and `openpartiesandclaims-wilderness-config.toml` (identical key values across `v5.5.5` and `Beta-5.10.17`):

| Config File & Key | Verified Value | Operational Meaning |
| :--- | :--- | :--- |
| `openpartiesandclaims-server.toml`: `[serverConfig.parties].enabled` | `true` (`maxPartyMembers = 64`, `maxPartyAllies = 64`) | Players actively group into parties and allied parties. |
| `openpartiesandclaims-server.toml`: `[serverConfig.claims].enabled` | `true` (`maxPlayerClaims = 250`, `maxPlayerClaimForceloads = 10`) | Player bases are heavily claimed and chunk-loaded. |
| `openpartiesandclaims-server.toml`: `forcedBlockProtectionExceptionList` | `["minecraft:crafting_table", "lootr:lootr_chest", "simpleshops:simple_shop", "simpleshops:creative_simple_shop"]` | Lootr chests stay accessible even in claimed chunks. |
| `openpartiesandclaims-server.toml`: `friendlyChunkProtectedEntityList` | `ALL_BUT` `["minecraft:boat", "simpleplanes:*", "car:car", "corpse:corpse"]` | Vehicles/corpses are exempted; livestock, villagers, and friendly entities are protected. |
| `openpartiesandclaims-default-player-config.toml`: `protectClaimedChunks` | `true` | Claim protection is ON by default for all players. |
| `...default-player-config.toml`: `fromParty` / `fromAllyParties` | `false` / `true` | Party members bypass owner's claim lock; allies do NOT by default. |
| `...default-player-config.toml`: `blocksFromPlayers` / `blocksFromMobs` / `blocksFromOther` | `1` / `1` / `1` | Non-party players, mobs, and unowned machines/turrets (`Other`) cannot place/break blocks in claims. |
| `...default-player-config.toml`: `fromFireSpread` | `true` | Fire spread into or inside claimed chunks is blocked. |
| `...default-player-config.toml`: `entitiesFromPlayers` / `entitiesFromOther` / `entitiesFromFire` | `1` / `1` / `true` | Protected entities in claims cannot be burned by outsiders or unowned fire. |
| `...default-player-config.toml`: `playersFromPlayers` / `playersFromOther` | `false` / `false` | **CRITICAL:** PvP and unowned-source player damage are NOT blocked in claims by default. |
| `...wilderness-config.toml`: `protectClaimedChunks` | `false` | Wilderness is unprotected; turrets and handheld weapons can operate freely in Lost Cities ruins. |

### 2.3 Firefighter Armor Set Bonus (`overrides/config/armorsets/firefighter.json`)

Verified in BOTH `v5.5.5` (`spacecatasb-forge-18.13.1.jar`) and `Beta-5.10.17` (`spacecatasb-forge-20.14.0.jar`):

- **Armor Piece Registry IDs** *(note the upstream spelling `fire_figther` in `apocalypsenow`)*:
  - `apocalypsenow:fire_figther_helmet`
  - `apocalypsenow:fire_figther_chestplate`
  - `apocalypsenow:fire_figther_leggings`
  - `apocalypsenow:fire_figther_boots`
- **Partial Set Bonus (`partialBonusRequiredAmount = 4`, i.e., all 4 armor pieces without requiring an axe):**
  - Grants `minecraft:fire_resistance` (amplifier `0`, duration `100` ticks, refreshed continuously on self).
- **Full Set Bonus (4 armor pieces + Fire Axe / mix-and-match axe in `mainHand`):**
  - `v5.5.5`: `+150%` (`1.5`, op `1`) `generic.attack_damage` + `minecraft:fire_resistance`.
  - `Beta-5.10.17`: `+50%` (`0.5`, op `1`) `generic.attack_damage` + `+20%` (`0.2`, op `2`) `generic.attack_speed` + `minecraft:fire_resistance`.

**Key Takeaway:** Because the Firefighter set grants standard vanilla `minecraft:fire_resistance`, using a properly fire-tagged `DamageSource` (`setIsFire()` in `1.18.2` / `#minecraft:is_fire` in `1.20.1`) gives Firefighter wearers **automatic, zero-hardcoding immunity** to thermal flame streams and lingering ground fire, while still allowing distinct non-fire chemical/cryo/corrosive fluids (if configured via fuel JSON) to behave independently.

### 2.4 Health, Locational Damage & Temperature Systems

#### `v5.5.5` (`1.18.2`): First Aid + Cold Sweat + Thirst Was Taken
- **First Aid** (`overrides/defaultconfigs/firstaid-server.toml`):
  - Limb HP pools: `maxHealthHead = 6`, `maxHealthBody = 4`, `Left/Right Arm = 4`, `Left/Right Leg = 4`, `Left/Right Foot = 4`.
  - Lethality: **`causeDeathHead = true`**, `causeDeathBody = false`.
  - Locational Armor multipliers: Head `7.0× (+1.0)`, Chest `2.5×`, Legs `3.0×`, Feet `6.0×`; Toughness multipliers: Head `4.0×`, Chest `3.0×`, Legs `3.0×`, Feet `3.5×`.
  - Healing: `allowNaturalRegeneration = false`, `vanillaHealthCalculation = "AVERAGE_ALL"`, `armorEnchantmentMode = "LOCAL_ENCHANTMENTS"`, `enchantmentMultiplier = 4`, `resistanceReductionPercentPerLevel = 10`.
- **Cold Sweat** (`overrides/config/coldsweat/main.toml` & `world_settings.toml`):
  - `Difficulty = 2`, `"Fire Resistance Immunity" = true`, `"Ice Resistance Immunity" = true`.
  - Habitable world temperature band: `0.4286` to `1.6190` (Minecraft biome units); `"Temperature Damage" = 2.0`, `"Damage Scaling" = true`.
  - Reference `BlockTemps` (radius / max): `minecraft:fire` = `+0.476` (range `7`, max `0.8`), `create:blaze_burner (kindled)` = `+0.6` (range `5`, max `0.9`), `create:blaze_burner (seething)` = `+0.7` (range `5`, max `1.1`), `minecraft:soul_fire` = `-0.476` (cold soul fire enabled!).
  - Seasonal shifts (`Serene Seasons`): Summer `[+0.3, +0.5, +0.3]`, Winter `[-0.3, -0.5, -0.3]`.

#### `Beta-5.10.17` (`1.20.1`): Legendary Survival Overhaul + Resistance Balancer + Apothic Attributes
- **Legendary Survival Overhaul** (`overrides/config/legendarysurvivaloverhaul/legendarysurvivaloverhaul-common.toml`):
  - Core switches: `"Temperature Enabled" = true`, `"Thirst Enabled" = true`, `"Health Overhaul Enabled" = true`, `"Localized Body Damage Enabled" = true`, `"Temperature Difficulty Mode" = "HARD"`, `"Natural Regeneration Enabled" = false`, `"Initial Player Health" = 20.0`.
  - Temperature modifiers: `"Player On Fire Modifier" = 12.5` (very large heat spike if ignited!), `"Player Sprint Modifier" = 1.5`, `"Maximum Temperature Modification" = 1.0` per `"Temperature Tick Time" = 20` ticks; Serene Seasons Summer `+4.0 / +8.0 / +4.0`, Winter `-4.0 / -8.0 / -4.0`.
  - Localized Body Damage: `"Headshot Multiplier" = 1.5`, `"Body Damage Multiplier" = 1.0`, `"Body Part Health Mode" = "DYNAMIC"` (`Head = 0.4` [8 HP], `Arms = 0.4` [8 HP], `Chest = 0.6` [12 HP], `Legs = 0.6` [12 HP], `Feet = 0.4` [8 HP]).
  - Broken Hearts: `"Added Broken Hearts Per Injured Limb" = 0.15` (floor `5` hearts).
- **Resistance Balancer** (`overrides/config/resistance_balancer.json5`): `enable_custom_formula = false`, `percentile_reduction_fallback = 0.05` (reduces Resistance potion scaling from vanilla 20%/lvl to 5%/lvl).
- **AttributeFix** (`overrides/config/attributefix.json` in BOTH packs): Uncaps `generic.max_health` (`10,000,000`), `generic.armor` (`10,000,000`), `generic.armor_toughness` (`10,000,000`), and `generic.attack_damage` (`10,000,000`).
- **Apothic Attributes** (`Beta-5.10.17` only): `ApothicAttributes-1.20.1-1.3.7.jar` (modid `attributeslib`, no Apotheosis enchantment/affix mod installed).

### 2.5 Existing Weapon, Gun & IE Chemthrower Benchmarks

Verified from `overrides/defaultconfigs/immersiveengineering-server.toml` (BOTH packs) and gun configs:

| Mod & Config Path | Parameter | `v5.5.5` (`1.18.2`) | `Beta-5.10.17` (`1.20.1`) |
| :--- | :--- | :--- | :--- |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[tools.chemthrower].consumption` | `10` mB/tick | `10` mB/tick |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[tools.chemthrower].scroll` | `true` | `true` |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[machines.turret].consumption` | `64` IF/tick | `64` IF/tick |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[machines.turret].chem_consumption` | `32` IF/tick | `32` IF/tick |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[machines.turret].gun_consumption` | `32` IF/tick | `32` IF/tick |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[machines.teslacoil].damage` / active FE | `6.0` dmg / `512` IF/t | `6.0` dmg / `512` IF/t |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[tools.bullet_damage]` (Casull / AP / Dragon / Silver) | `15.0` / `25.0` / `15.0` / `20.0` | `15.0` / `25.0` / `15.0` / `20.0` |
| **IE** (`defaultconfigs/immersiveengineering-server.toml`) | `[machines.dieselGen_output]` | `12,288` IF/tick | `8,192` IF/tick |
| **Create: Diesel Generators** (`config/createdieselgenerators-common.toml`) | Tool fluid capacity / Canister capacity | *(not installed)* | `200 mB` (`+100` enchant) / `4,000 mB` (`+1,000` enchant) |
| **TaC** (`v5.5.5`: `config/tac-common.toml`) | `bulletsIgnoreStandardArmor` / percent | `true` / `0.5` (50% armor bypass!) | *(replaced by TaCZ)* |
| **TaC** (`v5.5.5`: `config/tac-common.toml`) | `aggro_mobs.unsilencedRange` | `40.0` blocks | *(replaced by TaCZ)* |
| **TaCZ** (`Beta`: `config/tacz-common.toml`) | `DefaultGunFireSoundDistance` / `IgniteBlock` / `IgniteEntity` | *(not installed)* | `64` blocks / `true` / `true` |
| **TaCZ Tweaks** (`Beta`: `config/tacztweaks.json`) | `firstAidCompat` / `lsoCompat` / `shootWhileSprinting` | *(not installed)* | `true` / `true` / `true` |
| **CGM** (`config/cgm-common.toml`) | `headShotDamageMultiplier` / `setFireToBlocks` / `unsilencedRange` | `1.25×` / `true` / `20.0` | `1.25×` / `true` / `20.0` |

> **Removal Check Verified:** Neither `overrides/scripts/Removal/immersive_removal.zs` (`v5.5.5`) nor `overrides/kubejs/startup_scripts/removals.js` (`Beta-5.10.17`) removes IE's Chemthrower or Chemthrower Turret. Both coexist with `tacticalchemthrowers`.

### 2.6 Mob HP, Armor Tiers, AI & Hordes Audit

#### Verified DeceasedCraft Enemy Stat Tiers
From `Beta-5.10.17` `overrides/kubejs/startup_scripts/entity/attribute.js` and `overrides/config/sporeconfig.toml` (mirrored by `v5.5.5` `overrides/config/incontrol/spawn.json` additive/multiplicative rules):

| Threat Tier | Representative DeceasedCraft Mobs | HP Range | Armor Range | Fire / Combat Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Shamblers & Swarmers** | `minecraft:zombie` (20/2), `zombie_extreme:crawler` (20/2), `undead_revamp2:thebidy` (10/0), `thesmoker` (25/2), `infected_police` (35/4), `bomber`/`thehunter`/`therod` (40/4) | `10 – 40 HP` | `0 – 6` | `hordes-common.toml`: `zombiesBurn = false` (immune to daylight burn, NOT immune to fire damage!). |
| **Tier 2: Armored & Tactical Specials** | `thespitter`/`theswarmer` (50/6), `clicker` (60/8), `boomer` (70/12), `infected_hazmat` (70/24), `infected_military` (80/20), `goon`/`revived`/`faceless`/`night_hunter` (90/26) | `50 – 90 HP` | `6 – 26` | Heavy armor (`20–26`) severely mitigates non-piercing hits. |
| **Tier 3: Elites & Spore Evolved** | `infected_juggernaut` (160/30), `ram` (160/30), `thelurker` (220/12), `spore:inf_human/husk/hazmat` (90/16–20), `spore:plagued`/`lacerator`/`knight` (110–120/22–24), `spore:leaper`/`stalker`/`volatile`/`brute` (180–220/24–40) | `90 – 250 HP` | `12 – 40` | `sporeconfig.toml`: Spore mobs are weak to cold (`"Should the infected be weak to cold?" = true`), and `spore:volatile` / `spore:braurei` can self-buff with **`minecraft:fire_resistance`** when hurt! |
| **Tier 4: Bosses & Calamities** | `zombie_extreme:demolisher` (500/60), `zero_patient` (600/40), `undead_revamp2:theheavy` (600/35), `rat_king` (700/30), `clogger` (800/40), `spore:sieger` (1200/80), `gazenbreacher` (1400/65), `hindenburg` (1600/65), `howitzer` (2500/65); `v5.5.5` `mutationcraft:the_intoxicator` (+2000 HP, +20 armor) | `500 – 2500+ HP` | `30 – 80` | Uncapped armor (`30–80`) + `v5.5.5` Hard difficulty (`2.0× HP`, `1.2× Armor`). Flamethrowers serve as sustained crowd-clear / DoT / armor-softening support, NOT instant boss one-shotters. |

#### Zombie Awareness, The Hordes & Enhanced Celestials
- **Zombie Awareness** (`overrides/config/zombieawareness/Features.toml` & `General.toml`):
  - Both packs enable `awareness_Sound = true`, `awareness_Scent = true`, `awareness_Light = true`, `noisyZombies = true`, `noisyPistons = true`, `soundAlerts = true`, `soundInvestigates = true`, `awareness_Light_OnlyZombies = true`, `tickRateAILoop = 40`, `tickCooldownBetweenPathfinds = 300`, `frequentSoundThreshold = 1000`.
  - Sense range delta: `v5.5.5` uses `maxPFRangeSense = 48`, `soundStrength = 48`, `scentStrength = 24`, `sightRange = 12`; `Beta-5.10.17` tightens to `maxPFRangeSense = 24`, `soundStrength = 4`, `scentStrength = 8`, `sightRange = 16`, `findSense_PercentChance = 10`.
- **The Hordes** (`overrides/config/hordes-common.toml`):
  - `enableHordeEvent = true`, `hordeSpawnDays = 15`, `hordeSpawnDuration = 10000`, `hordeSpawnInterval = 2000`.
  - Horde cap: `spawnAmount = 15`, `hordeSpawnMax = 75` (`v5.5.5`) → `spawnAmount = 20`, `hordeSpawnMax = 100` (`Beta-5.10.17`, `hordeMultiplayerScaling = 1.5`).
  - `zombiesBurn = false`, `skeletonsBurn = false`, `zombiePlayersFireImmune = false`.
- **Enhanced Celestials** (`v5.5.5` only, `overrides/config/enhancedcelestials/minecraft/overworld/lunar/events/`):
  - Blood Moon: `spawnCategoryMultiplier.monster = 3.0`, `blockSleeping = true`.
  - Super Blood Moon: `spawnCategoryMultiplier.monster = 4.5`, `blockSleeping = true`.

### 2.7 Lootr & Dynamic Lighting Defaults

- **Lootr (`overrides/config/lootr-common.toml`):**
  - `v5.5.5`: Active by default (`convert_wooden_chests = true`, `convert_trapped_chests = true`, `convert_mineshafts = true`, `convert_quark = true`, `randomise_seed = true`).
  - `Beta-5.10.17`: **`disable = true`** (`convert_wooden_chests = false`, `randomise_seed = true`, plus `overrides/config/deceased_expansion.cfg` sets `convert=false`), intended to stay off in singleplayer and be toggled on by multiplayer server admins.
- **Dynamic Lighting Client Configs:**
  - `v5.5.5` (`overrides/config/lucent-client.toml`): `vanillaDynamicLighting = true`, `lightRefreshRate = 6`, `maxVisibleDistance = 128`, `smoothBlending = false`, `burningEntitiesGlow = true` (level `10`), `heldItemsGlow = true`, `itemEntitiesGlow = true`.
  - `Beta-5.10.17` (`overrides/config/sodiumdynamiclights-client.toml`): `mode = "FAST"`, **`self = true`**, **`entities = false`**, **`block_entities = false`**, `water_sensitive_check = true`.
  - **Oculus (`overrides/config/oculus.properties` in BOTH packs):** `colorSpace=SRGB`, `maxShadowRenderDistance=16`, `shaderPack=ComplementaryReimagined_r2.2.zip`, `enableShaders=false` (bundled shaderpack ready for toggle).

---

## 3. Concrete Implementation Contracts

### Contract 1: Server-Authoritative Temporary Fire & Griefing Safety

Because `do_fire_tick = true` in both DeceasedCraft packs and Lost Cities buildings contain huge amounts of wood, wool, and player-built shelters, **spawning vanilla `minecraft:fire` blocks directly from flamethrower jets is FORBIDDEN by default.**

1. **Custom Non-Destructive Surface Flame (`tacticalchemthrowers:temporary_flame`):**
   - Implement a dedicated lightweight server-authoritative `TemporaryFlameBlock` (or pooled server-managed surface burn hazard block) that:
     - **Never spreads** to neighboring blocks (ignores `doFireTick` spread logic completely).
     - **Never consumes or destroys** supporting or adjacent flammable blocks (planks, logs, wool, leaves, furniture, Lootr chests, Create machinery).
     - Emits light level `11–13`, deals periodic fire-tagged DoT to entities standing in it, and **self-extinguishes deterministically** after a short configurable TTL (`40–100` ticks, scaled by fuel profile, default `60` ticks = 3s) via scheduled block ticks (`level.scheduleTick(...)`).
     - Immediately extinguishes on contact with water, rain (configurable chance), or water-based/cryo spray.
     - Only replaces `air` / `replaceable` non-fluid blocks (`state.canBeReplaced()` && `state.getFluidState().isEmpty()`) directly above a solid sturdy top face (`faceSturdy(level, belowPos, Direction.UP)`).
2. **Respecting `doFireTick` and Config Gates:**
   - Provide server config `allowGroundIgnition` (default `true` for `TemporaryFlameBlock`), `allowDestructiveVanillaFire` (default **`false`**—strictly opt-in for hardcore servers), and `respectDoFireTick` (default `true`: if a server sets `/gamerule doFireTick false`, suppress even `TemporaryFlameBlock` placement so admin fire-locks are honored).
3. **Claim-Boundary Enforcement Before Any Block Placement:**
   - Before placing `TemporaryFlameBlock` at `BlockPos targetPos`, the server MUST run `ProtectionBridge.canModifyBlock(ServerLevel, BlockPos, @Nullable UUID ownerUuid, @Nullable Entity actor)`:
     - If OPAC is loaded, check `IChunkProtectionAPI` for block modification AND fire spread protection on `targetPos`.
     - If the target chunk is claimed by another player/party whose claim protects blocks or fire spread (`blocksFromPlayers`, `blocksFromOther`, `fromFireSpread`), **refuse placement silently** (visual flame particles still play, zero block mutation).
   - For automated **ChemThrower Turrets**, persist `ownerUuid` (the placing player's UUID) in BlockEntity NBT so OPAC evaluates the turret under its owner's party permissions rather than falling back to blocked `Other` (`blocksFromOther = 1`) inside the owner's own base!

### Contract 2: Friendly Fire & Team / Claim Protection Hooks

Because OPAC ships with `playersFromPlayers = false` and `playersFromOther = false` in DeceasedCraft's default player config, relying solely on OPAC's default PvP hook would still burn teammates during co-op horde defenses where `natural_regeneration = false`.

Implement a unified server-side **`CombatProtectionResolver.canDamageEntity(ServerLevel level, @Nullable UUID attackerOwnerUuid, @Nullable Entity attackerEntity, LivingEntity target, boolean isTurret)`** evaluated on every flame jet tick and turret target-acquisition scan:

1. **Self-Protection Guard:**
   - Never damage `attackerEntity` or a player matching `attackerOwnerUuid` from their own jet or turret (prevents accidental self-ignition and LSO's `+12.5` on-fire temperature spike).
2. **Server PvP / Friendly-Fire Config Matrix:**
   - Server config options:
     - `friendlyFireTeams = false` (default: protect teammates)
     - `friendlyFireAllies = false` (default: protect allied parties)
     - `turretTargetPlayers = false` (default: turrets ignore players unless explicitly enabled in turret filter GUI AND server allows PvP)
     - `protectTamedAndVillagers = true` (default: jet & turrets skip tamed pets owned by self/team and claimed-chunk friendly entities)
3. **Layered Team/Party Resolution (Zero Hard Dependencies):**
   Evaluate in order; if ANY layer marks `attackerOwnerUuid` and `target` (or `target`'s tamed owner) as teammates/allies and friendly fire is disabled, **block damage and skip turret targeting**:
   - **Layer A — Vanilla Scoreboard Teams:** `attacker.isAlliedTo(target)` (`Team.isAllowFriendlyFire()` check).
   - **Layer B — FTB Teams (Soft Hook, `ModList.get().isLoaded("ftbteams")`):** Query `FTBTeamsAPI` to check whether `attackerOwnerUuid` and `targetPlayerUuid` share the same FTB Team (or are allied when `friendlyFireAllies = false`).
   - **Layer C — Open Parties and Claims (Soft Hook, `ModList.get().isLoaded("openpartiesandclaims")`):**
     - Query `OpenPACServerAPI.get(server).getPartyManager().getPartyByMember(attackerOwnerUuid)` to check same party (`party.getMemberInfo(targetUuid) != null`) and mutual ally parties (`party.isAlly(targetParty.getId())`).
     - Query `OpenPACServerAPI.get(server).getChunkProtection()` for entity damage protection (`onEntityInteraction` / `onEntityFire` / claim owner check) so non-party players and turrets NEVER burn livestock, villagers, or players protected inside a claimed chunk (`entitiesFromPlayers = 1`, `entitiesFromFire = true`).
4. **Turret Target Filtering:**
   - Turrets MUST filter targets through `CombatProtectionResolver` **before** slewing and firing, preventing wasted fuel and visual harassment against protected entities, teammates, vehicles (`car:car`, `simpleplanes:*`), and corpses (`corpse:corpse`).

### Contract 3: Combat Curve Calibration for DeceasedCraft

Calibrate `tacticalchemthrowers` so it occupies a distinct **short-to-medium range sustained crowd-control, horde-clear, and armor-softening** niche alongside DeceasedCraft's firearms (`TaC`/`TaCZ`/`CGM`) and `Immersive Engineering`'s Chemthrower:

| Role / Weapon | Target Range | Fuel Burn Rate | Effective DPS (Normal, Unarmored) | Armor Interaction | Design Rationale (Verified Against Pack) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **IE Chemthrower** *(Pack Baseline)* | ~8–10 blocks | `10 mB/t` (`200 mB/s`) | ~4–6 DPS + vanilla fire | Standard fire | Verified from `immersiveengineering-server.toml`; baseline industrial tool. |
| **Handheld Tier 1** *(Improvised / Brass Torch-Thrower)* | `7–8` blocks | `6–8 mB/t` | `8–10 DPS` + 4s burn | 40% armor bypass (fire-tagged) | Clears Tier 1 shamblers (`20–40 HP`) in 2–4s; fuel-efficient early Lost Cities defense. |
| **Handheld Tier 2** *(Pressurized Industrial ChemThrower)* | `10–12` blocks | `10–12 mB/t` | `14–18 DPS` + 6s burn + heat ramp | 50% armor bypass (mirrors TaC `0.5`!) | Matches IE's `10 mB/t` economy; shreds Tier 2 armored specials (`60–90 HP`, `20–26` armor) in 4–6s without outclassing high-caliber sniper/AP rifles on single targets. |
| **Handheld Tier 3** *(Heavy Tactical / Pressurized Napalm-Grade)* | `13–15` blocks | `14–16 mB/t` | `22–28 DPS` + sticky burn + mild armor-soften | 60% armor bypass + heat-stacking | Holds chokepoints against Tier 3 elites (`160–220 HP`, `30–40` armor) and 75–100 mob Hordes; bosses (`500–2500 HP`) still require team focus fire. |
| **Automated ChemThrower Turret** | `12–16` blocks *(strictly synced with jet travel distance!)* | `8–12 mB/t` (fuel-scaled) | `12–20 DPS` (RPM/pressure-scaled) | 50% armor bypass | Power cost calibrated to IE Turret (`64 IF/t` idle + `32 IF/t` firing) OR Create rotational `SU` (`16–32 SU/RPM`, min `32 RPM`, max `256 RPM` per `create-server.toml`). |

**Critical Damage-Type & Armor Contracts:**
1. **Fire-Tagged DamageSource / DamageType:**
   - Thermal flame jet damage MUST use a custom `DamageSource` (`tacticalchemthrowers:chem_flame`) marked as fire (`setIsFire()` in `1.18.2`; included in `#minecraft:is_fire` in `1.20.1`).
   - **Consequence 1 (Firefighter Armor Synergy):** Any player wearing DeceasedCraft's 4-piece Firefighter set (`apocalypsenow:fire_figther_*`) receives continuous `minecraft:fire_resistance` and is automatically immune to thermal flame streams.
   - **Consequence 2 (Spore Elite Counterplay):** In `Beta-5.10.17`, `spore:volatile` and `spore:braurei` can gain `minecraft:fire_resistance`; supporting non-fire fuel types (e.g., cryo/cold coolant or corrosive chemical sprays using a non-`#minecraft:is_fire` damage type—remember Spore mobs are explicitly `"weak to cold" = true`!) gives players tactical fuel-swapping counterplay!
   - **Consequence 3 (First Aid & LSO Locational Safety):** Fire-tagged damage bypasses headshot instakill (`maxHealthHead = 6` in First Aid; `1.5×` headshot in LSO) and distributes heat damage fairly across the body.
2. **Handling Uncapped Mob Armor (`AttributeFix`, 20–80 Armor):**
   - Do **not** apply full `bypasses_armor` (`100%` true damage) to players in PvP, as that would invalidate non-Firefighter tactical armors (`Juggernaut`, `SWAT`, `Spec Ops`).
   - Instead, split thermal stream damage into a **hybrid profile** or use a configurable **thermal armor-bypass ratio** (default `50%` armor-ignoring fire damage on hostile mobs, matching DeceasedCraft's `tac-common.toml` `percentDamageIgnoresStandardArmor = 0.5`, reduced to `25%` against players, and always `0` against `MobEffects.FIRE_RESISTANCE`).
   - Use **controlled hurt-invulnerability cadence** (e.g., damage tick every `4–5` ticks with `invulnerableTime` capped or scaled cleanly, rather than zeroing `invulnerableTime` every tick and breaking `LivingHurtEvent` / armor durability!). Note: capping armor durability damage per tick prevents a 20-tick/sec flame stream from shredding a player's entire armor set in 2 seconds!

### Contract 4: Optional Soft Runtime Hooks (Zero Hard Dependencies)

All cross-mod hooks MUST sit behind `ModList.get().isLoaded("<modid>")` guards and route through isolated static bridge classes so the JVM never loads optional third-party classes unless that mod is present.

1. **Zombie Awareness (`zombieawareness` in BOTH packs):**
   - Zombie Awareness listens to Minecraft's sound playback / Forge sound events (`awareness_Sound = true`) and block/entity light (`awareness_Light = true`).
   - **Contract:** Play firing ignition & continuous combustion audio via standard `Level#playSound(...)` on the server with `SoundSource.PLAYERS` (handheld) / `SoundSource.BLOCKS` (turret), throttled to every `10–20` ticks for server-side sound events (while client handles smooth looping audio). This naturally alerts Zombie Awareness within DeceasedCraft's configured `soundStrength` (`48` in `v5.5.5`, `4` in `Beta-5.10.17`) without tripping `frequentSoundThreshold = 1000` or causing pathfinding lag spikes.
2. **Cold Sweat (`cold_sweat`, `v5.5.5` only) & Legendary Survival Overhaul (`legendarysurvivaloverhaul`, `Beta-5.10.17` only):**
   - **Design Goal:** Subtle immersion—sustained firing gently warms the operator (helpful in winter/snowy biomes!), without ever pushing a healthy player into heatstroke during a 2-minute horde defense.
   - **Contract (`v5.5.5` Cold Sweat):** While actively firing a thermal fuel, apply a gentle, clamped temporary warmth modifier (max equivalent to `+0.15` to `+0.25` MC units—roughly half a campfire, far below `minecraft:fire`'s `+0.476` and capped so it never exceeds `Maximum Habitable Temperature = 1.619` on its own). Automatically skipped if the player has `MobEffects.FIRE_RESISTANCE` (`"Fire Resistance Immunity" = true`).
   - **Contract (`Beta-5.10.17` LSO):** While actively firing a thermal fuel, contribute a subtle capped modifier (e.g., `+2.0` to `+3.0` LSO degrees—comparable to `"Player Sprint Modifier" = 1.5`, nowhere near `"Player On Fire Modifier" = 12.5`), updated on LSO's 20-tick cadence and clamped below hyperthermia threshold.
   - Expose a single common config toggle `enableTemperatureWarmthIntegration = true` (plus warmth cap) so server admins can tune or disable it.
3. **Lootr-Safe Loot Injection (`lootr` in BOTH packs):**
   - **Contract:** Inject chemthrower blueprints, fuel canisters, nozzle parts, or rare components **exclusively** via Forge Global Loot Modifiers (`data/forge/loot_modifiers/global_loot_modifiers.json` + `data/tacticalchemthrowers/loot_modifiers/*.json`) targeting Lost Cities / industrial / military chest loot tables.
   - **Never** modify chest `BlockEntity` inventories on chunk generation or `PlayerInteractEvent`—Lootr intercepts `RandomizableContainerBlockEntity` and invokes the target `LootTable` (including all Forge GLMs) per-player upon opening. This guarantees 100% parity across `v5.5.5` (Lootr enabled), `Beta-5.10.17` singleplayer (`disable = true`), and `Beta-5.10.17` multiplayer servers (Lootr enabled).
