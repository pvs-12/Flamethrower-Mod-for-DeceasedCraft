# FLMTHRWR: NOTEBOOK 3 — Context Summary, Purpose & Reference Links

## 1. What This Notebook Is For

**FLMTHRWR: NOTEBOOK 3** serves as the **Flamethrower References & Weapon Systems Research Library** for the original **Flamethrower Mod**. It is dedicated to engineering, designing, and documenting handheld flamethrower and automated turret systems targeting two Minecraft Forge environments:

- **Minecraft Forge 1.18.2** (Legacy DeceasedCraft v5.5.5)
- **Minecraft Forge 1.20.1** (Newer DeceasedCraft beta)

The notebook synthesizes reference weapon architectures, combat and physics math, visual/audio pipelines, historical real-world flamethrower mechanics, and AI-agent/MCP development tooling into a single technical reference.

> **Licensing & Originality Mandate:** Every asset in the Flamethrower Mod—including Java code, 3D models, textures, animations, particle sheets, audio files, and GUI art—**must be independently authored**. Reference mods documented in this notebook are studied strictly for API interoperability, gameplay architecture, and engineering patterns.

---

## 2. Core Research Pillars & Technical Scope

### A. Weapon & Turret Reference Architectures
Studies existing Minecraft weapon and turret mods (such as Immersive Engineering's Chemthrower & Turret, Techguns, Create: Diesel Generators' Chemical Sprayer, MrCrayfish's Gun Mod, TACZ, Create: Radar, and Create Big Cannons) to establish clean design patterns, including:
- **Turret Block/BlockEntity Pattern:** Exposing Forge `IFluidHandler` (fluid pipes) and `IEnergyStorage` (power) alongside persistent targeting configuration (filters, whitelist/blacklist, range).
- **Range & Geometry Alignment:** Ensuring configured turret target acquisition range aligns directly with effective flame jet travel distance (addressing pitfalls such as Immersive Engineering Issue #3626).
- **Shared Fuel Lookup:** Sharing a unified fuel-effect backend between handheld weapons and automated turrets.

### B. Shared vs. Weapon-Specific Engineering Systems
Both the handheld Flamethrower and automated Turret query a synced `FuelRegistry` loaded from `data/<namespace>/flamethrower_fuels/*.json`. Each fuel definition specifies:
- `damage_multiplier` & `range_multiplier`
- `consumption_mb_per_tick` & `heat_intensity`
- `ignites_targets` & `requires_pilot_light`
- `particle_profile` (flame tint, smoke density, ember rate), `sound_profile`, and optional `special_effect`

| System Scope | Responsibilities |
| :--- | :--- |
| **Shared Systems** | `FuelRegistry`, `JetGeometry` capsule collision math, `HeatTracker`, safe `TemporaryFire` placement rules, `ParticleProfile` & `SoundProfile` renderers |
| **Handheld-Specific** | `ItemStack` fuel/reload handling (`R` key, bottle return), Tiers 1–3 progression, first-person BEWLR rendering, HUD |
| **Turret-Specific** | Create kinetic SU/RPM integration, Forge Energy buffer, side I/O config, target scanner, yaw/pitch slew limits, Create Wrench GUI |

### C. Rendering, 3D Animation, Audio & Performance
Covers Forge and vanilla mechanics alongside third-party pipelines for:
- Flame jet collision math, damage/heat scaling, and grief-safe temporary ground fire
- Layered particle rendering and custom particle sheets
- 3D weapon and player animations (GeckoLib 3/4, PlayerAnimator, Blockbench)
- Continuous looping audio design (`sounds.json`, Audacity, FFmpeg) and runtime performance profiling (`spark`)

### D. Historical Mechanical References
Provides real-world mechanical and ergonomic context (fuel pressurization, ignition/pilot lights, nozzle geometry, range, and burn-time profiles) from historical flamethrowers including the US M2 Flamethrower, German Flammenwerfer 35, and German Flammenwerfer 41.

### E. AI-Agent Skills & MCP Tooling
Collects Minecraft modding agent skill bundles, repository instructions (`AGENTS.md`), and Model Context Protocol (MCP) servers for live Blockbench modeling, GitHub management, semantic code navigation, IDE integration, and up-to-date library documentation.

---

## 3. All Links in This Notebook

### Primary Weapon & Turret References
- **Immersive Engineering (GitHub):** https://github.com/BluSunrize/ImmersiveEngineering
- **Immersive Engineering Issue #3626 (Chem Thrower Turret Range):** https://github.com/BluSunrize/ImmersiveEngineering/issues/3626
- **FTB Wiki — Chemthrower Turret:** https://ftbwiki.org/Chemthrower_Turret
- **Techguns (GitHub):** https://github.com/techguns/techguns
- **Create: Diesel Generators (GitHub):** https://github.com/george8188625/Create-Diesel-Generators
- **Create: Diesel Generators Issue #95 (Chemical Sprayer Projectiles):** https://github.com/george8188625/Create-Diesel-Generators/issues/95
- **MrCrayfish's Gun Mod (GitHub):** https://github.com/MrCrayfish/MrCrayfishGunMod
- **Timeless and Classics Zero / TACZ (GitHub):** https://github.com/MCModderAnchor/TACZ
- **Create: Radar (GitHub):** https://github.com/Arsenalists-of-Create/Create-Radar
- **Create Big Cannons (GitHub):** https://github.com/Cannoneers-of-Create/CreateBigCannons

### Vanilla Mechanics & Minecraft Wiki
- **Minecraft Wiki — Sounds.json:** https://minecraft.wiki/w/Sounds.json
- **Minecraft Wiki — JSON:** https://minecraft.wiki/w/JSON

### 3D Animation, Rendering & Modding References
- **GeckoLib (GitHub):** https://github.com/bernie-g/geckolib
- **GeckoLib Wiki:** https://github.com/bernie-g/geckolib/wiki
- **GeckoLib Wiki — Installation (GeckoLib 4):** https://github.com/bernie-g/geckolib/wiki/Installation-(Geckolib4)
- **PlayerAnimator (GitHub):** https://github.com/KosmX/minecraftPlayerAnimator
- **Blockbench Official Site:** https://www.blockbench.net/
- **Iron's Spells 'n Spellbooks (GitHub):** https://github.com/iron431/irons-spells-n-spellbooks
- **Iron's Spells 'n Spellbooks — NOTES.MD:** https://github.com/iron431/irons-spells-n-spellbooks/blob/1.21/NOTES.MD

### Historical Flamethrower References
- **Wikipedia — Flamethrower:** https://en.wikipedia.org/wiki/Flamethrower
- **Wikipedia — M2 Flamethrower:** https://en.wikipedia.org/wiki/M2_flamethrower
- **Wikipedia — Flammenwerfer 35:** https://en.wikipedia.org/wiki/Flammenwerfer_35
- **Wikipedia — Flammenwerfer 41:** https://en.wikipedia.org/wiki/Flammenwerfer_41

### AI-Agent Skills & MCP Tooling
- **Minecraft Agent Skills (Jahrome907):** https://github.com/Jahrome907/minecraft-agent-skills
- **Minecraft Agent Skills Bundle (AIKUSAN):** https://github.com/AIKUSAN/minecraft-agent-skills-bundle
- **ChronoDawn (GitHub):** https://github.com/ksoichiro/ChronoDawn
- **ChronoDawn — AGENTS.md:** https://github.com/ksoichiro/ChronoDawn/blob/main/AGENTS.md
- **Blockbench MCP (GitHub):** https://github.com/sosadly/blockbench-mcp
- **Model Context Protocol (Official Site):** https://modelcontextprotocol.io/
- **GitHub MCP Server:** https://github.com/github/github-mcp-server
- **Serena (GitHub):** https://github.com/oraios/serena
- **Context7 (GitHub):** https://github.com/upstash/context7
- **Context7 Platform:** https://context7.com/

### Embedded Modding Reference Links (from Iron's Spells `NOTES.MD`)
- **Iron's Spellbooks Legacy Repo:** https://github.com/iron431/irons_spellbooks
- **Iron's Spellbooks Miro Board:** https://miro.com/app/board/uXjVPvycxJQ=/
- **Iron's Spellbooks Spell Sheet:** https://docs.google.com/spreadsheets/d/1o0MyG9ok5Csf8_-77f-qH3VqOu6NtiuYcBb_SzDmA3M/edit#gid=1973083805
- **Iron's Spellbooks Trello:** https://trello.com/b/yzpLtJpQ/spell-book-mod
- **Immersive Engineering `build.gradle` Reference:** https://github.com/BluSunrize/ImmersiveEngineering/blob/7d49b2aa24b5759931db0220ecffec447dc854b9/build.gradle
- **OpenComputers `build.gradle` Reference:** https://github.com/MightyPirates/OpenComputers/blob/de8f207f3bc4ed5fc14c8e163263f3541bf30c2a/build.gradle#L30
- **McJty 1.18 Docs:** https://www.mcjty.eu/docs/1.18/
- **McJty TutorialV3 (Mana System):** https://github.com/McJty/TutorialV3/tree/98b824b6adfb318c19fe96ae41f504ade7d40dcf/src/main/java/com/example/tutorialv3/manasystem
- **Kaupenjoe Forge 1.18.1 Tutorial Repo:** https://github.com/Tutorials-By-Kaupenjoe/Forge-Tutorial-1.18.1/tree/main/src/main/java/net/kaupenjoe/tutorialmod
- **ModdingTutorials — 1.18.2 Environment Setup:** https://moddingtutorials.org/1.18.2/environment-setup
- **ModdingTutorials — 1.19.2 Advanced Items:** https://moddingtutorials.org/1.19.2/advanced-items/
- **Linkie Mappings:** https://linkie.shedaniel.me/mappings
- **Forge Gemwire Wiki — Particles:** https://forge.gemwire.uk/wiki/Particles
- **TelepathicGrunt Mixins Guide (Gist):** https://gist.github.com/TelepathicGrunt/3784f8a8b317bac11039474012de5fb4
- **YouTube — Entity Creation in Blockbench:** https://www.youtube.com/watch?v=XBIXn7s-fMo
- **YouTube — Item Stack:** https://www.youtube.com/watch?v=edcpW1zzUfk
- **YouTube — Creating Entities / Blockbench (Part 1):** https://www.youtube.com/watch?v=VlUwLXkwb2c
- **YouTube — Creating Entities / Blockbench (Part 2):** https://www.youtube.com/watch?v=kxzZ-oJKjcY
- **YouTube — General Modding Reference:** https://www.youtube.com/watch?v=prqMxqUtj-0
- **YouTube — Loading Values from Config:** https://www.youtube.com/watch?v=QN9jq3_V-I8
- **YouTube — Particles:** https://www.youtube.com/watch?v=DM69u76tXMI
- **Jekyll Docs — GitHub Actions:** https://jekyllrb.com/docs/continuous-integration/github-actions/
- **Jekyll Docs — Themes:** https://jekyllrb.com/docs/themes/
- **Publishing GitHub Pages with Jekyll:** https://idratherbewriting.com/documentation-theme-jekyll/mydoc_publishing_github_pages.html
- **Bulma Clean Theme:** https://github.com/chrisrhymes/bulma-clean-theme/#installation
- **GitHub Pages Gem:** https://github.com/github/pages-gem
- **GitHub Docs — GitHub Pages and Jekyll:** https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll

### Additional Notebook Inventory Sources (URLs Not Present in Current Excerpts)
The notebook's source inventory also lists the following resources whose direct URLs were not included in the retrieved source snippets:
- Immersive Engineering ReadTheDocs & FTB Wiki `Chemical_Thrower`
- Official Minecraft Forge 1.18.x & 1.20.1 Docs (Particles, Sounds, SimpleChannel Networking, Capabilities, Sides)
- Minecraft Wiki pages: `Damage`, `Fire`, `Model`, `Resource_pack`
- GeckoLib 3 (1.18.2) setup guide
- Blockbench Official Wiki
- Audacity Official Manual, FFmpeg Documentation, and spark Profiler Docs
- `mcp-jetbrains`