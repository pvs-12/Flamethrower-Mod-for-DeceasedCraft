#!/usr/bin/env python3
"""Explicitly classify all 380 unique DeceasedCraft mods into the finalized 17-category
taxonomy and attach concise mod-dev notes (including v5.5.5 -> v6 replacement notes)."""

import json
import re
from collections import Counter
from pathlib import Path

SCRATCH = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch")

CATEGORIES = [
    "Core Libraries & APIs",
    "Performance & Optimization",
    "Bug Fixes & Stability",
    "Firearms, Weapons & Combat",
    "Zombies, Mobs & Wildlife",
    "Survival, Health & Environment",
    "Worldgen, Cities & Structures",
    "Tech, Automation & Power",
    "Vehicles & Transport",
    "Storage, Loot & Backpacks",
    "Food, Farming & Cooking",
    "Building, Furniture & Decor",
    "Quests, Progression & NPCs",
    "UI, HUD, Maps & Info",
    "Audio, Visuals & Immersion",
    "Modpack Scripting & Control",
    "Multiplayer, Utility & Admin",
]

# Explicit mapping of all 380 CurseForge project IDs -> Category
CAT_MAP = {
    # --- Core Libraries & APIs ---
    864599: "Core Libraries & APIs",  # [Let's Do] API
    1115285: "Core Libraries & APIs", # Almanac Lib
    898963: "Core Libraries & APIs",  # Apothic Attributes
    419699: "Core Libraries & APIs",  # Architectury API
    463826: "Core Libraries & APIs",  # Atlas Lib
    250363: "Core Libraries & APIs",  # AutoRegLib
    1264423: "Core Libraries & APIs", # BaguetteLib
    531761: "Core Libraries & APIs",  # Balm
    228525: "Core Libraries & APIs",  # Bookshelf
    704113: "Core Libraries & APIs",  # Botarium
    331936: "Core Libraries & APIs",  # Citadel
    348521: "Core Libraries & APIs",  # Cloth Config API
    968456: "Core Libraries & APIs",  # Cobweb
    342584: "Core Libraries & APIs",  # Collective
    693313: "Core Libraries & APIs",  # CorgiLib
    237749: "Core Libraries & APIs",  # CoroUtil
    257814: "Core Libraries & APIs",  # CreativeCore
    326652: "Core Libraries & APIs",  # Cupboard
    309927: "Core Libraries & APIs",  # Curios API
    621463: "Core Libraries & APIs",  # Custom Portal API [Forge]
    465066: "Core Libraries & APIs",  # ExpandAbility
    889079: "Core Libraries & APIs",  # Forgified Fabric API
    549225: "Core Libraries & APIs",  # Framework
    404465: "Core Libraries & APIs",  # FTB Library
    889915: "Core Libraries & APIs",  # FTB XMod Compat
    388172: "Core Libraries & APIs",  # GeckoLib
    955399: "Core Libraries & APIs",  # GlitchCore
    520110: "Core Libraries & APIs",  # Iceberg
    465109: "Core Libraries & APIs",  # InsaneLib
    309674: "Core Libraries & APIs",  # Item Filters
    1186372: "Core Libraries & APIs", # JasonConfig
    303657: "Core Libraries & APIs",  # Kiwi
    410295: "Core Libraries & APIs",  # Konkrete
    351264: "Core Libraries & APIs",  # Kotlin for Forge
    367442: "Core Libraries & APIs",  # Mapper Base
    233105: "Core Libraries & APIs",  # McJtyLib
    938643: "Core Libraries & APIs",  # Melody
    499980: "Core Libraries & APIs",  # Moonlight Lib
    669659: "Core Libraries & APIs",  # MRU
    586157: "Core Libraries & APIs",  # Necronomicon API
    306770: "Core Libraries & APIs",  # Patchouli
    319596: "Core Libraries & APIs",  # Pehkui
    283644: "Core Libraries & APIs",  # Placebo
    658587: "Core Libraries & APIs",  # playerAnimator
    495476: "Core Libraries & APIs",  # Puzzles Lib
    416294: "Core Libraries & APIs",  # Rhino
    1279407: "Core Libraries & APIs", # Ritchie's Projectile Library
    858542: "Core Libraries & APIs",  # Searchables
    916747: "Core Libraries & APIs",  # ShatterLib | OctoLib
    890127: "Core Libraries & APIs",  # Sinytra Connector
    618298: "Core Libraries & APIs",  # Sophisticated Core
    438332: "Core Libraries & APIs",  # SuperMartijn642's Config Lib
    454372: "Core Libraries & APIs",  # SuperMartijn642's Core Lib
    563928: "Core Libraries & APIs",  # TerraBlender (Forge)
    1104882: "Core Libraries & APIs", # TxniLib
    1056812: "Core Libraries & APIs", # UniLib
    667299: "Core Libraries & APIs",  # YetAnotherConfigLib
    421850: "Core Libraries & APIs",  # YUNG's API
    247921: "Core Libraries & APIs",  # ZeroCore 2
    968868: "Core Libraries & APIs",  # Zeta

    # --- Performance & Optimization ---
    233019: "Performance & Optimization",  # AI Improvements
    548115: "Performance & Optimization",  # Alternate Current
    949555: "Performance & Optimization",  # BadOptimizations
    905450: "Performance & Optimization",  # Bocchium
    665658: "Performance & Optimization",  # Canary
    256717: "Performance & Optimization",  # Clumps
    1254143: "Performance & Optimization", # Colorwheel
    1285475: "Performance & Optimization", # Colorwheel Patcher
    1217518: "Performance & Optimization", # Create Better FPS
    840788: "Performance & Optimization",  # CullLessLeaves Reforged
    508933: "Performance & Optimization",  # Distant Horizons
    908741: "Performance & Optimization",  # Embeddium
    628345: "Performance & Optimization",  # Entity Collision FPS Fix
    448233: "Performance & Optimization",  # Entity Culling
    951499: "Performance & Optimization",  # Fast Async World Save
    1030285: "Performance & Optimization", # FastBoot
    299540: "Performance & Optimization",  # FastFurnace
    630620: "Performance & Optimization",  # Fastload
    475117: "Performance & Optimization",  # FastSuite
    288885: "Performance & Optimization",  # FastWorkbench
    429235: "Performance & Optimization",  # FerriteCore
    1142875: "Performance & Optimization", # Flerovium
    974774: "Performance & Optimization",  # Icterine
    686911: "Performance & Optimization",  # ImmediatelyFast
    1163206: "Performance & Optimization", # Immersive Optimization
    659897: "Performance & Optimization",  # Iris & Oculus Flywheel Compat
    460819: "Performance & Optimization",  # Lazy DataFixerUpper (LazyDFU)
    1142812: "Performance & Optimization", # lazyyyyy
    663477: "Performance & Optimization",  # Let Me Despawn
    821790: "Performance & Optimization",  # Lightspeed
    1310491: "Performance & Optimization", # MCreatorMemFix
    974401: "Performance & Optimization",  # Mobtimizations
    790626: "Performance & Optimization",  # ModernFix
    581495: "Performance & Optimization",  # Oculus
    682881: "Performance & Optimization",  # Pluto
    570017: "Performance & Optimization",  # Radium Reforged
    1191845: "Performance & Optimization", # Redirected
    670986: "Performance & Optimization",  # Saturn
    582327: "Performance & Optimization",  # Server Performance - Smooth Chunk Save
    633412: "Performance & Optimization",  # Smooth Boot (Reloaded)
    526854: "Performance & Optimization",  # Starlight (Forge)
    965702: "Performance & Optimization",  # Vanillin

    # --- Bug Fixes & Stability ---
    1091339: "Bug Fixes & Stability", # AllTheLeaks
    1348482: "Bug Fixes & Stability", # Apocalypse Patches
    280510: "Bug Fixes & Stability",  # AttributeFix
    547989: "Bug Fixes & Stability",  # Bee Fix
    446253: "Bug Fixes & Stability",  # Better Biome Blend
    1018276: "Bug Fixes & Stability", # Better Biome Reblend
    470193: "Bug Fixes & Stability",  # Connectivity
    1154099: "Bug Fixes & Stability", # Crash Assistant
    1006676: "Bug Fixes & Stability", # CreateStuffAdditions Fix
    1059881: "Bug Fixes & Stability", # DCFixes
    1400238: "Bug Fixes & Stability", # DCTweaks
    1315786: "Bug Fixes & Stability", # DeceasedCraft++
    882495: "Bug Fixes & Stability",  # fix GPU memory leak
    431430: "Bug Fixes & Stability",  # FlickerFix
    1201803: "Bug Fixes & Stability", # GPUTape
    1326199: "Bug Fixes & Stability", # Immersive Fixes
    959388: "Bug Fixes & Stability",  # Iris/Oculus & GeckoLib Compat
    656346: "Bug Fixes & Stability",  # Load My F***ing Tags
    492246: "Bug Fixes & Stability",  # Max Health Fix
    676136: "Bug Fixes & Stability",  # Model Gap Fix
    828656: "Bug Fixes & Stability",  # NaN Health Fixer
    1289695: "Bug Fixes & Stability", # NaNny Reforked
    920888: "Bug Fixes & Stability",  # Oculus Particle Fix
    689467: "Bug Fixes & Stability",  # Packet Fixer
    1431536: "Bug Fixes & Stability", # Refined Storage (Fixes) Mixin
    407174: "Bug Fixes & Stability",  # Shutup Experimental Settings!
    550678: "Bug Fixes & Stability",  # Too Fast
    635427: "Bug Fixes & Stability",  # Yeetus Experimentus

    # --- Firearms, Weapons & Combat ---
    1028108: "Firearms, Weapons & Combat", # [TaCZ] Timeless and Classics Zero Guns
    448410: "Firearms, Weapons & Combat",  # Apocalypse Now
    549892: "Firearms, Weapons & Combat",  # Armor Set Bonuses
    312353: "Firearms, Weapons & Combat",  # Artifacts
    639842: "Firearms, Weapons & Combat",  # Better Combat
    646668: "Firearms, Weapons & Combat",  # Create Big Cannons
    555300: "Firearms, Weapons & Combat",  # Crossbowverhaul
    725568: "Firearms, Weapons & Combat",  # Fancy Trinkets
    225738: "Firearms, Weapons & Combat",  # MmmMmmMmmMmm (Target Dummy)
    289479: "Firearms, Weapons & Combat",  # MrCrayfish's Gun Mod
    945471: "Firearms, Weapons & Combat",  # MrCrayfish's Gun Mod [Unofficial]
    541466: "Firearms, Weapons & Combat",  # Nameless Trinkets
    482378: "Firearms, Weapons & Combat",  # ParCool!
    1132901: "Firearms, Weapons & Combat", # ParCool+ / Compatibility Addon
    1185268: "Firearms, Weapons & Combat", # Shots Fired
    264353: "Firearms, Weapons & Combat",  # SwingThroughGrass
    1223006: "Firearms, Weapons & Combat", # TaCZ Ammo Query
    1193263: "Firearms, Weapons & Combat", # TaCZ Tweaks
    1065328: "Firearms, Weapons & Combat", # TACZ: Durability
    969378: "Firearms, Weapons & Combat",  # Third Person Shooting: Zero
    491264: "Firearms, Weapons & Combat",  # Timeless and Classics Guns
    408332: "Firearms, Weapons & Combat",  # Weapon Throw

    # --- Zombies, Mobs & Wildlife ---
    426558: "Zombies, Mobs & Wildlife",  # Alex's Mobs
    1206722: "Zombies, Mobs & Wildlife", # Animal Pens
    574913: "Zombies, Mobs & Wildlife",  # Critters and Companions
    515276: "Zombies, Mobs & Wildlife",  # Enhanced AI
    899308: "Zombies, Mobs & Wildlife",  # Enhanced Hordes
    678295: "Zombies, Mobs & Wildlife",  # Fungal Infection: Spore
    360203: "Zombies, Mobs & Wildlife",  # Guard Villagers
    271998: "Zombies, Mobs & Wildlife",  # Lost Souls
    298408: "Zombies, Mobs & Wildlife",  # Mob Sunscreen
    849595: "Zombies, Mobs & Wildlife",  # Mutationcraft
    627986: "Zombies, Mobs & Wildlife",  # Naturalist
    645456: "Zombies, Mobs & Wildlife",  # NoCube's Zombie Mobs
    686058: "Zombies, Mobs & Wildlife",  # Nyf's Spiders
    485779: "Zombies, Mobs & Wildlife",  # The Hordes
    479710: "Zombies, Mobs & Wildlife",  # THE UNDEAD REVAMPED
    622514: "Zombies, Mobs & Wildlife",  # VMH - Variable Mob Height
    1173633: "Zombies, Mobs & Wildlife", # Voiceless Survival
    237754: "Zombies, Mobs & Wildlife",  # Zombie Awareness
    392809: "Zombies, Mobs & Wildlife",  # Zombie Extreme

    # --- Survival, Health & Environment ---
    506194: "Survival, Health & Environment", # Cold Sweat
    276951: "Survival, Health & Environment", # Comforts
    438447: "Survival, Health & Environment", # Enhanced Celestials
    276837: "Survival, Health & Environment", # First Aid
    840254: "Survival, Health & Environment", # Legendary Survival Overhaul
    291874: "Survival, Health & Environment", # Serene Seasons
    308663: "Survival, Health & Environment", # Snow! Real Magic!
    679270: "Survival, Health & Environment", # Thirst Was Taken
    337243: "Survival, Health & Environment", # True Darkness

    # --- Worldgen, Cities & Structures ---
    910274: "Worldgen, Cities & Structures",  # Biome Replacer
    775502: "Worldgen, Cities & Structures",  # Biome Sizes
    695238: "Worldgen, Cities & Structures",  # Biome Spawn Point
    220318: "Worldgen, Cities & Structures",  # Biomes O' Plenty
    491794: "Worldgen, Cities & Structures",  # Explorer's Compass
    496520: "Worldgen, Cities & Structures",  # Horror Elements mod
    1274451: "Worldgen, Cities & Structures", # Lost Radar
    964100: "Worldgen, Cities & Structures",  # Lost Worlds LC
    252848: "Worldgen, Cities & Structures",  # Nature's Compass
    242436: "Worldgen, Cities & Structures",  # Ore Tweaker
    832882: "Worldgen, Cities & Structures",  # Structure Essentials
    269024: "Worldgen, Cities & Structures",  # The Lost Cities
    558126: "Worldgen, Cities & Structures",  # This Rocks!
    389665: "Worldgen, Cities & Structures",  # YUNG's Better Mineshafts

    # --- Tech, Automation & Power ---
    1170251: "Tech, Automation & Power", # CFM Refurbished: Watt About Power?
    298275: "Tech, Automation & Power",  # Click Machine
    328085: "Tech, Automation & Power",  # Create
    439890: "Tech, Automation & Power",  # Create Crafts & Additions
    466792: "Tech, Automation & Power",  # Create Stuff 'N Additions
    869316: "Tech, Automation & Power",  # Create: Diesel Generators
    1281336: "Tech, Automation & Power", # Create: Hypertubes
    1152836: "Tech, Automation & Power", # Create: Radars
    688231: "Tech, Automation & Power",  # Create: Steam 'n' Rails
    1207780: "Tech, Automation & Power", # Engineered Schematics
    250277: "Tech, Automation & Power",  # Extreme Reactors
    231951: "Tech, Automation & Power",  # Immersive Engineering
    268250: "Tech, Automation & Power",  # Immersive Petroleum
    1163529: "Tech, Automation & Power", # Item Scrapper
    443900: "Tech, Automation & Power",  # Pipez
    64760: "Tech, Automation & Power",   # Security Craft
    396803: "Tech, Automation & Power",  # Wormhole (Portals)

    # --- Vehicles & Transport ---
    1038652: "Vehicles & Transport", # DragN's Valiant Vehicles!
    1144170: "Vehicles & Transport", # DragN's VV: Refueled
    666014: "Vehicles & Transport",  # Immersive Aircraft
    388908: "Vehicles & Transport",  # Simple Planes
    267458: "Vehicles & Transport",  # Ultimate Car Mod

    # --- Storage, Loot & Backpacks ---
    316582: "Storage, Loot & Backpacks",  # Corpse
    1138130: "Storage, Loot & Backpacks", # Corpse x Curios API Compat
    361276: "Storage, Loot & Backpacks",  # Lootr
    943086: "Storage, Loot & Backpacks",  # Refined Polymorphism
    243076: "Storage, Loot & Backpacks",  # Refined Storage
    272302: "Storage, Loot & Backpacks",  # Refined Storage Addons
    422301: "Storage, Loot & Backpacks",  # Sophisticated Backpacks
    223852: "Storage, Loot & Backpacks",  # Storage Drawers
    394535: "Storage, Loot & Backpacks",  # Trash Cans
    235577: "Storage, Loot & Backpacks",  # TrashSlot
    344787: "Storage, Loot & Backpacks",  # XP Tome

    # --- Food, Farming & Cooking ---
    704465: "Food, Farming & Cooking",  # [Let's Do] Vinery
    318749: "Food, Farming & Cooking",  # AlwaysEat
    820977: "Food, Farming & Cooking",  # Create: Central Kitchen
    443570: "Food, Farming & Cooking",  # Diet
    623634: "Food, Farming & Cooking",  # Dietary Statistics
    1144296: "Food, Farming & Cooking", # Display Delight
    400514: "Food, Farming & Cooking",  # Easy Villagers
    861437: "Food, Farming & Cooking",  # Engineers Delight
    398521: "Food, Farming & Cooking",  # Farmer's Delight
    230976: "Food, Farming & Cooking",  # Fast Leaf Decay
    602171: "Food, Farming & Cooking",  # Harvest with ease
    886559: "Food, Farming & Cooking",  # Legacy: [Let's Do] Bakery
    277616: "Food, Farming & Cooking",  # Spice of Life: Carrot Edition
    367178: "Food, Farming & Cooking",  # Tree Harvester

    # --- Building, Furniture & Decor ---
    610492: "Building, Furniture & Decor",  # Another Furniture
    563734: "Building, Furniture & Decor",  # Builder's Delight
    237307: "Building, Furniture & Decor",  # Cosmetic Armor Reworked
    509285: "Building, Furniture & Decor",  # Create Deco
    906239: "Building, Furniture & Decor",  # Create: Interiors
    377281: "Building, Furniture & Decor",  # Dark Paintings
    317094: "Building, Furniture & Decor",  # EmbellishCraft
    883287: "Building, Furniture & Decor",  # Fast Paintings
    314645: "Building, Furniture & Decor",  # Immersive Posts
    896219: "Building, Furniture & Decor",  # Just Outdoor Stuffs
    701473: "Building, Furniture & Decor",  # MOA DECOR: ART
    853639: "Building, Furniture & Decor",  # MOA DECOR: BATH
    701517: "Building, Furniture & Decor",  # MOA DECOR: SCIENCE
    55438: "Building, Furniture & Decor",   # MrCrayfish's Furniture Mod (Legacy)
    897116: "Building, Furniture & Decor",  # MrCrayfish's Furniture Mod: Refurbished
    663141: "Building, Furniture & Decor",  # Paladin's Furniture
    990265: "Building, Furniture & Decor",  # Plushie Buddies
    243121: "Building, Furniture & Decor",  # Quark
    897377: "Building, Furniture & Decor",  # Re:Deco - Vanilla Furniture
    300331: "Building, Furniture & Decor",  # Simply Light
    749675: "Building, Furniture & Decor",  # Texels Paintings
    1116812: "Building, Furniture & Decor", # Toni's Immersive Lanterns
    724387: "Building, Furniture & Decor",  # Vertical Slabs Compat

    # --- Quests, Progression & NPCs ---
    670282: "Quests, Progression & NPCs",  # Anvil Never Too Expensive
    463402: "Quests, Progression & NPCs",  # Custom Villager Trades
    1052708: "Quests, Progression & NPCs", # CustomNPCs-Unofficial
    390913: "Quests, Progression & NPCs",  # Fixed Anvil Repair Cost
    289412: "Quests, Progression & NPCs",  # FTB Quests
    404468: "Quests, Progression & NPCs",  # FTB Teams
    627101: "Quests, Progression & NPCs",  # Merge Enchantments
    991341: "Quests, Progression & NPCs",  # Pufferfish's Attributes
    835091: "Quests, Progression & NPCs",  # Pufferfish's Skills
    1161828: "Quests, Progression & NPCs", # Quests Kill Task Tweaks
    1121234: "Quests, Progression & NPCs", # Resistance Balancer
    517272: "Quests, Progression & NPCs",  # Simple Shops
    390717: "Quests, Progression & NPCs",  # Starter Kit
    462128: "Quests, Progression & NPCs",  # Tax Free Levels

    # --- UI, HUD, Maps & Info ---
    499826: "UI, HUD, Maps & Info",  # Advancement Plaques
    248787: "UI, HUD, Maps & Info",  # AppleSkin
    396094: "UI, HUD, Maps & Info",  # Armor Points ++
    272515: "UI, HUD, Maps & Info",  # Better Advancements
    551894: "UI, HUD, Maps & Info",  # Better Compatibility Checker
    292038: "UI, HUD, Maps & Info",  # Better Ping Display
    459701: "UI, HUD, Maps & Info",  # Catalogue
    457570: "UI, HUD, Maps & Info",  # Configured
    250398: "UI, HUD, Maps & Info",  # Controlling
    559334: "UI, HUD, Maps & Info",  # Day Counter
    511770: "UI, HUD, Maps & Info",  # Drippy Loading Screen
    511040: "UI, HUD, Maps & Info",  # Durability Tooltip
    250419: "UI, HUD, Maps & Info",  # Enchantment Descriptions
    502561: "UI, HUD, Maps & Info",  # Equipment Compare
    367706: "UI, HUD, Maps & Info",  # FancyMenu
    1021685: "UI, HUD, Maps & Info", # Immersive UI
    357540: "UI, HUD, Maps & Info",  # Inventory HUD+
    521590: "UI, HUD, Maps & Info",  # Item Highlighter
    368718: "UI, HUD, Maps & Info",  # JEITweaker
    634571: "UI, HUD, Maps & Info",  # Just Enough Immersive Multiblocks
    238222: "UI, HUD, Maps & Info",  # Just Enough Items (JEI)
    417645: "UI, HUD, Maps & Info",  # Just Enough Professions (JEP)
    1172469: "UI, HUD, Maps & Info", # Legendary Tabs
    700723: "UI, HUD, Maps & Info",  # Loot Journal: Pickup Notifier
    918638: "UI, HUD, Maps & Info",  # Moderately Enough Effect Descriptions (MEED)
    738663: "UI, HUD, Maps & Info",  # Not Enough Recipe Book [NERB]
    961802: "UI, HUD, Maps & Info",  # Scholar
    543661: "UI, HUD, Maps & Info",  # Stylish Effects
    245211: "UI, HUD, Maps & Info",  # The One Probe
    306549: "UI, HUD, Maps & Info",  # Tips
    504908: "UI, HUD, Maps & Info",  # Traveler's Titles
    263420: "UI, HUD, Maps & Info",  # Xaero's Minimap
    263466: "UI, HUD, Maps & Info",  # Xaero's Minimap (Fair-play Edition)
    317780: "UI, HUD, Maps & Info",  # Xaero's World Map
    1414942: "UI, HUD, Maps & Info", # YTonGame

    # --- Audio, Visuals & Immersion ---
    844662: "Audio, Visuals & Immersion",  # [EMF] Entity Model Features
    568563: "Audio, Visuals & Immersion",  # [ETF] Entity Texture Features
    289310: "Audio, Visuals & Immersion",  # Camera Mod
    226889: "Audio, Visuals & Immersion",  # CleanView
    297038: "Audio, Visuals & Immersion",  # CraftPresence
    557796: "Audio, Visuals & Immersion",  # Effective (Forge)
    654373: "Audio, Visuals & Immersion",  # Embeddium (Rubidium) Extra
    284324: "Audio, Visuals & Immersion",  # Emojiful
    255389: "Audio, Visuals & Immersion",  # EnhancedVisuals
    915902: "Audio, Visuals & Immersion",  # Euphoria Patches
    1036246: "Audio, Visuals & Immersion", # Explosive Enhancement: Reforged
    871755: "Audio, Visuals & Immersion",  # Exposure
    937006: "Audio, Visuals & Immersion",  # Extra Gore
    363363: "Audio, Visuals & Immersion",  # Extreme sound muffler
    270441: "Audio, Visuals & Immersion",  # ItemPhysic Lite
    493280: "Audio, Visuals & Immersion",  # Lucent
    433760: "Audio, Visuals & Immersion",  # Not Enough Animations
    1219053: "Audio, Visuals & Immersion", # Particular Reforged
    442735: "Audio, Visuals & Immersion",  # Physics Mod
    433068: "Audio, Visuals & Immersion",  # Presence Footsteps (Forge)
    1163800: "Audio, Visuals & Immersion", # Pretty Rain
    243190: "Audio, Visuals & Immersion",  # Shoulder Surfing Reloaded
    551736: "Audio, Visuals & Immersion",  # Sodium/Embeddium Dynamic Lights
    558905: "Audio, Visuals & Immersion",  # Sodium/Embeddium Extras
    1103431: "Audio, Visuals & Immersion", # Sodium/Embeddium Options API
    535489: "Audio, Visuals & Immersion",  # Sound Physics Remastered
    925889: "Audio, Visuals & Immersion",  # Sounds
    910506: "Audio, Visuals & Immersion",  # TexTrue's Embeddium Options
    1302230: "Audio, Visuals & Immersion", # The Sound of Rain
    1217037: "Audio, Visuals & Immersion", # Vanilla Music Discs
    945479: "Audio, Visuals & Immersion",  # What Are They Up To (Watut)

    # --- Modpack Scripting & Control ---
    237065: "Modpack Scripting & Control",  # ContentTweaker
    239197: "Modpack Scripting & Control",  # CraftTweaker
    437717: "Modpack Scripting & Control",  # CreateTweaker
    232131: "Modpack Scripting & Control",  # Default Options
    676811: "Modpack Scripting & Control",  # Default Server Properties
    967617: "Modpack Scripting & Control",  # EntityJS
    313477: "Modpack Scripting & Control",  # Fx Control!
    227657: "Modpack Scripting & Control",  # Global GameRules
    257356: "Modpack Scripting & Control",  # In Control!
    238086: "Modpack Scripting & Control",  # KubeJS
    429371: "Modpack Scripting & Control",  # KubeJS Create
    641627: "Modpack Scripting & Control",  # KubeJS Offline Documentation
    1109365: "Modpack Scripting & Control", # Spawner Control
    1323738: "Modpack Scripting & Control", # Texture Locale Redirector

    # --- Multiplayer, Utility & Admin ---
    274259: "Multiplayer, Utility & Admin",  # Carry On
    533748: "Multiplayer, Utility & Admin",  # Chalk
    485681: "Multiplayer, Utility & Admin",  # Chunky
    888790: "Multiplayer, Utility & Admin",  # Client Crafting
    317269: "Multiplayer, Utility & Admin",  # Controllable
    568536: "Multiplayer, Utility & Admin",  # DRG Flares
    849519: "Multiplayer, Utility & Admin",  # e4mc
    904356: "Multiplayer, Utility & Admin",  # Fast IP Ping
    1099059: "Multiplayer, Utility & Admin", # Game Discs
    411045: "Multiplayer, Utility & Admin",  # Get It Together, Drops!
    1214525: "Multiplayer, Utility & Admin", # Keerdm's Binoculars
    623560: "Multiplayer, Utility & Admin",  # Log Begone
    913234: "Multiplayer, Utility & Admin",  # Longer Chat History
    60089: "Multiplayer, Utility & Admin",   # Mouse Tweaks
    451682: "Multiplayer, Utility & Admin",  # No Villager Death Messages
    636608: "Multiplayer, Utility & Admin",  # Open Parties and Claims
    388800: "Multiplayer, Utility & Admin",  # Polymorph
    907856: "Multiplayer, Utility & Admin",  # Recipe Essentials
    583228: "Multiplayer, Utility & Admin",  # Simple Backups
    416089: "Multiplayer, Utility & Admin",  # Simple Voice Chat
    361579: "Multiplayer, Utility & Admin",  # spark
    599436: "Multiplayer, Utility & Admin",  # StackablePotions
}

# Targeted cross-version / mod-dev notes appended to summaries where helpful
EXTRA_NOTES_555 = {
    250363: "Replaced by Zeta in MC 1.20.1 (Quark library).",
    237065: "Stopped at 1.19.2; v6 uses KubeJS for custom content instead of CraftTweaker/ContentTweaker.",
    239197: "Has 1.20.1 Forge support, but v6 migrated pack scripting to KubeJS.",
    437717: "Has 1.20.1 Forge support, but v6 uses KubeJS Create instead.",
    368718: "Has 1.20.1 Forge support, but v6 removed CraftTweaker stack.",
    1059881: "No public 1.20.1 Forge JAR (source-only 'DeceasedCraft v6 Fixes' branch exists on GitHub); v6 Beta 5.10.17 uses DeceasedCraft++ & DCTweaks.",
    623634: "Discontinued after 1.19.4 (Diet itself remains in v6).",
    557796: "Stopped at 1.19.2; replaced by Particular Reforged & Pretty Rain in v6.",
    628345: "Stopped at 1.19.2; MC-228976 optimization handled differently in 1.20.1.",
    313477: "Merged into In Control! starting in MC 1.20.1+.",
    460819: "Discontinued after 1.19.3 (vanilla 1.19.4+ implemented lazy DFU natively).",
    821790: "Discontinued after 1.19.2 (most optimizations merged into vanilla 1.20; unofficial port LightSpeedRe exists); v6 uses FastBoot & lazyyyyy.",
    289479: "Official mod stopped at 1.19.4; v6 uses MrCrayfish's Gun Mod [Unofficial] & TaCZ.",
    645456: "Stopped at 1.19.2; v6 adds Fungal Infection: Spore instead.",
    242436: "Stopped at 1.18.2 on CurseForge; worldgen/ore tweaks done via datapacks/KubeJS in 1.20.1.",
    682881: "Stopped at 1.19.3 (Forge fork of Krypton).",
    407174: "Stopped at 1.19.2; replaced by Yeetus Experimentus in v6.",
    264353: "Original project skipped 1.20.1 (1.19.2 -> 1.20.6); separate 1.20.1 Forge rewrite 'Swing Through Grass' exists.",
    491264: "Stopped at 1.18.2; replaced by full remaster [TaCZ] Timeless and Classics Zero Guns in v6.",
    337243: "Original stopped at 1.19.3.",
    276837: "Supports 1.20.1 Forge, but v6 replaced First Aid + Thirst Was Taken + Cold Sweat with Legendary Survival Overhaul.",
    679270: "Supports 1.20.1 Forge, but v6 consolidated thirst into Legendary Survival Overhaul.",
    506194: "Supports 1.20.1 Forge, but v6 consolidated temperature into Legendary Survival Overhaul.",
    665658: "Supports 1.20.1 Forge, but v6 uses Radium Reforged (Lithium fork) instead.",
    446253: "Supports 1.20.1 Forge, but v6 uses Better Biome Reblend.",
    882495: "Supports 1.20.1 Forge, but v6 uses GPUTape & AllTheLeaks.",
    828656: "Supports 1.20.1 Forge, but v6 uses NaNny Reforked.",
    654373: "Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Extras.",
    910506: "Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Options API.",
    493280: "Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Dynamic Lights.",
    659897: "Supports 1.20.1 Forge, but v6 uses Colorwheel & Colorwheel Patcher.",
    289310: "Supports 1.20.1 Forge, but v6 uses Exposure for cameras.",
    267458: "Supports 1.20.1 Forge, but v6 uses DragN's Valiant Vehicles! instead.",
    263466: "Supports 1.20.1 Forge, but v6 uses standard Xaero's Minimap.",
    526854: "Supports 1.20.1 Forge, but dropped in v6 (vanilla 1.20 overhauled lighting engine).",
    268250: "Supports 1.20.1 Forge, but v6 uses Create: Diesel Generators instead.",
}

EXTRA_NOTES_V6 = {
    508933: "ONLY included in DeceasedCraft_Beta_DH_Edition-5.10.17 (not in Standard Beta 5.10.17).",
    1028108: "Replaces Timeless and Classics Guns (v5.5.5) with rewritten 1.20.1 firearm engine.",
    945471: "Unofficial 1.20.1 Forge port replacing MrCrayfish's Gun Mod (v5.5.5).",
    840254: "Replaces First Aid + Thirst Was Taken + Cold Sweat from v5.5.5 (unified limbs, thirst, temperature).",
    968868: "Replaces AutoRegLib (v5.5.5) as Quark's required library in 1.20.1.",
    570017: "Replaces Canary (v5.5.5) as Lithium Forge fork.",
    1018276: "Replaces Better Biome Blend (v5.5.5).",
    1201803: "Replaces fix GPU memory leak (v5.5.5).",
    1289695: "Replaces NaN Health Fixer (v5.5.5).",
    635427: "Replaces Shutup Experimental Settings! (v5.5.5).",
    551736: "Replaces Lucent (v5.5.5) for dynamic lighting.",
    558905: "Replaces Embeddium (Rubidium) Extra (v5.5.5).",
    1103431: "Replaces TexTrue's Embeddium Options (v5.5.5).",
    1254143: "Replaces Iris & Oculus Flywheel Compat (v5.5.5) for Create + shaders.",
    1219053: "Replaces Effective (Forge) (v5.5.5) for ambient particles.",
    871755: "Replaces Camera Mod (v5.5.5).",
    1038652: "Replaces Ultimate Car Mod (v5.5.5) for ground vehicles.",
    263420: "Replaces Xaero's Minimap (Fair-play Edition) from v5.5.5.",
    1315786: "Custom DeceasedCraft expansion & bug-fix companion mod in v6 Beta.",
    1400238: "DeceasedCraft-specific tag fixes mod in v6 Beta.",
    890127: "Enables loading Fabric mods on Forge 1.20.1 (used alongside Forgified Fabric API).",
    257356: "In MC 1.20.1+, includes merged functionality of Fx Control! from v5.5.5.",
}


def clean_text(s: str) -> str:
    if not s:
        return ""
    # Strip invisible zero-width chars and normalize whitespace
    s = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main():
    data = json.loads((SCRATCH / "compiled_mods.json").read_text(encoding="utf-8"))
    mods = data["mods"]

    # Verify 100% coverage & valid categories
    mod_pids = {int(pid) for pid in mods.keys()}
    map_pids = set(CAT_MAP.keys())
    missing = mod_pids - map_pids
    extra = map_pids - mod_pids
    assert not missing, f"Unmapped project IDs: {missing}"
    assert not extra, f"Extra unused project IDs in CAT_MAP: {extra}"
    for pid, cat in CAT_MAP.items():
        assert cat in CATEGORIES, f"Invalid category {cat} for {pid}"

    cat_counts_all = Counter()
    cat_counts_555 = Counter()
    cat_counts_v6 = Counter()

    for pid_str, m in mods.items():
        pid = int(pid_str)
        cat = CAT_MAP[pid]
        m["title_clean"] = clean_text(m["title"])
        m["summary_clean"] = clean_text(m["summary"])
        m["category"] = cat

        # Build concise notes for each sheet
        base = m["summary_clean"]
        if len(base) > 160:
            base = base[:157].rstrip(" .,;:") + "..."

        note_555 = base
        if pid in EXTRA_NOTES_555:
            note_555 = f"{base} | Note: {EXTRA_NOTES_555[pid]}" if base else EXTRA_NOTES_555[pid]
        m["notes_555"] = note_555

        note_v6 = base
        if pid in EXTRA_NOTES_V6:
            note_v6 = f"{base} | Note: {EXTRA_NOTES_V6[pid]}" if base else EXTRA_NOTES_V6[pid]
        m["notes_v6"] = note_v6

        cat_counts_all[cat] += 1
        if m["in_555"]:
            cat_counts_555[cat] += 1
        if m["in_v6"]:
            cat_counts_v6[cat] += 1

    data["categories"] = CATEGORIES
    out_path = SCRATCH / "categorized_mods.json"
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"Successfully categorized all {len(mods)} unique mods across {len(CATEGORIES)} categories!")
    print(f"\n{'Category':34} | {'v5.5.5':>6} | {'v6 Beta':>7} | {'Unique':>6}")
    print("-" * 62)
    for cat in CATEGORIES:
        print(f"{cat:34} | {cat_counts_555[cat]:>6} | {cat_counts_v6[cat]:>7} | {cat_counts_all[cat]:>6}")
    print("-" * 62)
    print(f"{'TOTAL':34} | {sum(cat_counts_555.values()):>6} | {sum(cat_counts_v6.values()):>7} | {sum(cat_counts_all.values()):>6}")


if __name__ == "__main__":
    main()
