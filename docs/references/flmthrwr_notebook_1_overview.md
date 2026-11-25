# FLMTHRWR: NOTEBOOK 1 — Purpose & Reference Index

## What This Notebook Is For

**FLMTHRWR: NOTEBOOK 1** is a curated technical knowledge base and developer reference hub for **AI-assisted Minecraft mod development**. 

Its primary goal is to bridge two disciplines:
1. **Modern Minecraft Mod Engineering** — covering multi-loader project architecture (Forge, NeoForge, and Fabric), bytecode manipulation (Mixins), mappings, 3D modeling/animation, high-performance rendering, resource/sound formats, and flagship open-source tech/magic mod codebases.
2. **AI Coding Agent & MCP (Model Context Protocol) Workflows** — equipping AI assistants (such as Claude Code, Codex, and Cursor) with live documentation retrieval, semantic code editing, automated Blockbench 3D modeling, Maven dependency auditing, GitHub automation, and structured `AGENTS.md` / skill-bundle instructions.

Whether you are bootstrapping a new multi-loader Minecraft mod, studying how major tech mods implement energy/rendering/logistics, or configuring an AI coding agent to build, model, and maintain a mod without hallucinating outdated APIs, this notebook brings all the foundational documentation, templates, tools, and reference repositories into one place.

---

## Core Focus Areas

### 1. AI Coding Agents, MCP Tooling & Agent Context
A major pillar of this notebook is setting up reliable AI-assisted development pipelines so coding agents work accurately against real Minecraft APIs and repository rules:
- **Minecraft-Specific MCP Servers:** Real-time access to Fabric/NeoForge docs, Parchment mappings, and mod examples (`MCModding-MCP`), plus direct AI control over 3D modeling, texturing, rigging, and animation (`Blockbench MCP`).
- **General Developer MCP Servers:** IDE-level semantic symbol retrieval and refactoring (`Serena`), up-to-date library documentation injection (`Context7`), GitHub repository/PR/issue/workflow automation (`GitHub MCP Server`), and Maven dependency/CVE inspection (`Maven Tools MCP`).
- **Agent Skills & `AGENTS.md` Blueprints:** Pre-built Minecraft agent skill bundles (`minecraft-agent-skills`, `minecraft-agent-skills-bundle`) and concrete `AGENTS.md` examples (`ChronoDawn`, `billy-boarding`) demonstrating multi-version repo layouts, task loops, ADRs, privacy checks, and Modrinth publishing workflows.

### 2. Multi-Loader & Mod Project Templates
Resources for structuring clean, maintainable mods across Minecraft versions and mod loaders:
- **NeoForge + Fabric / Multi-Version Setups:** `MultiLoader-Template`, `stonecutter-mod-template`, and `architectury-templates`.
- **Mod Loader Core & Docs:** `MinecraftForge` repository and official documentation.

### 3. Core Modding Libraries, Mappings & Graphics
Low-level and visual foundations required for advanced mods:
- **Mixins & Compatibility:** `SpongePowered/Mixin` documentation and `MixinExtras` for safer bytecode injection.
- **Mappings:** `linkie-core` and Linkie/Parchment mappings for translating Minecraft class, method, and field names across versions.
- **3D Modeling, Animation & Rendering:** `Blockbench`, `GeckoLib 4` (entity/item/block animations), and `Flywheel` (GPU-instanced rendering and custom shaders).

### 4. Tutorials, Dev Notes & Vanilla Specifications
Hands-on learning paths and technical specifications:
- **Structured Modding Tutorials:** McJty's modding guides (covering core concepts like Definitions vs. `ItemStack` vs. `BlockState`/`BlockEntity`, networking, GUI, power, and baked models across 1.18–1.21+) and Kaupenjoe's Forge 1.20.X YouTube series.
- **Practical Modder Notes:** `Iron's Spells 'n Spellbooks` `NOTES.MD`, capturing real-world Gradle setups, particles, mixins, Blockbench workflows, configs, and Jekyll/GitHub Pages documentation sites.
- **Vanilla Data Formats:** Minecraft Wiki specifications for `JSON`, `Sounds.json`, block/item `Model`, `Resource_pack`, and `Pack_format`.

### 5. Reference Open-Source Mod Codebases
Production-grade Minecraft mods included as architectural and mechanical references (especially skewed toward **industrial/tech, logistics, magic, and custom-rendered** mods):
- **Tech, Machinery & Logistics:** `Create`, `Mekanism`, `Applied Energistics 2`, `Immersive Engineering`, and `Thermal Expansion` (CoFH).
- **Content, Magic & Multi-Version Structure:** `Iron's Spells 'n Spellbooks` and `ChronoDawn`.

---

## How to Use This Notebook

1. **Bootstrap & Architecture:** Start with `MultiLoader-Template`, `stonecutter-mod-template`, or `architectury-templates`, and use `ChronoDawn`'s or `billy-boarding`'s `AGENTS.md` as a template for your own project instructions.
2. **Wire Up AI Tooling:** Connect `mcmodding-mcp`, `blockbench-mcp`, `serena`, `context7`, `maven-tools-mcp`, and `github-mcp-server` to your AI coding client so the agent has grounded docs, mappings, and editor control.
3. **Implement Systems & Assets:** Cross-reference official Forge/NeoForge/Fabric docs, McJty/Kaupenjoe tutorials, Mixin/MixinExtras guides, GeckoLib 4, Flywheel, and reference mod repositories (`Create`, `Mekanism`, `AE2`, `Immersive Engineering`, `Thermal Expansion`) when designing machines, blocks, entities, particles, or custom renderers.

---

## All Links in This Notebook

### Primary Notebook Sources

#### AI Agents, MCP Servers & `AGENTS.md` Examples
- **ChronoDawn `AGENTS.md`:** https://github.com/ksoichiro/ChronoDawn/blob/main/AGENTS.md
- **Billy-Boarding `AGENTS.md`:** https://github.com/Hand-Lock/billy-boarding/blob/main/AGENTS.md
- **Serena (Semantic Coding Agent MCP):** https://github.com/oraios/serena
- **GitHub Official MCP Server:** https://github.com/github/github-mcp-server
- **MCModding-MCP (Minecraft Modding Docs MCP):** https://github.com/OGMatrix/mcmodding-mcp
- **Context7 (Up-to-Date Docs MCP):** https://github.com/upstash/context7
- **Blockbench MCP:** https://github.com/sosadly/blockbench-mcp
- **Maven Tools MCP:** https://github.com/arvindand/maven-tools-mcp
- **Minecraft Agent Skills Bundle (AIKUSAN):** https://github.com/AIKUSAN/minecraft-agent-skills-bundle
- **Minecraft Agent Skills (Jahrome907):** https://github.com/Jahrome907/minecraft-agent-skills

#### Mod Loaders, Templates & Core Modding Libraries
- **MinecraftForge Repository:** https://github.com/MinecraftForge/MinecraftForge
- **MinecraftForge Documentation Repo:** https://github.com/MinecraftForge/Documentation
- **MultiLoader-Template (NeoForge + Fabric):** https://github.com/jaredlll08/MultiLoader-Template
- **Stonecutter Mod Template:** https://github.com/rotgruengelb/stonecutter-mod-template
- **Architectury Templates (Releases):** https://github.com/architectury/architectury-templates/releases
- **SpongePowered Mixin Wiki:** https://github.com/SpongePowered/Mixin/wiki
- **SpongePowered Mixin — The Mixin Environment:** https://github.com/SpongePowered/Mixin/wiki/Introduction-to-Mixins---The-Mixin-Environment
- **MixinExtras:** https://github.com/LlamaLad7/MixinExtras
- **linkie-core (Mappings Core):** https://github.com/linkie/linkie-core
- **Flywheel (GPU Instancing / Rendering):** https://github.com/Engine-Room/Flywheel
- **GeckoLib 4 Installation Wiki:** https://github.com/bernie-g/geckolib/wiki/Installation-(Geckolib4)
- **Blockbench:** https://github.com/JannisX11/blockbench

#### Tutorials, Wikis & Developer Notes
- **Iron's Spells 'n Spellbooks `NOTES.MD` (1.21):** https://github.com/iron431/irons-spells-n-spellbooks/blob/1.21/NOTES.MD
- **McJty 1.20 Modding Tutorials:** https://www.mcjty.eu/docs/1.20
- **McJty 1.18 Episode 1 (Minecraft Concepts):** https://mcjty.eu/docs/1.18/ep1#minecraft-concepts
- **McJty 1.20 Episode 1 (Minecraft Concepts):** https://mcjty.eu/docs/1.20/ep1#minecraft-concepts
- **Kaupenjoe Forge 1.20.X Tutorial Repo:** https://github.com/Tutorials-By-Kaupenjoe/Forge-Tutorial-1.20.X
- **Minecraft Wiki — `Sounds.json`:** https://minecraft.wiki/w/Sounds.json?oldid=3834081
- **Minecraft Wiki — `JSON`:** https://minecraft.wiki/w/JSON

#### Reference Minecraft Mod Repositories & Wikis
- **Create Mod Wiki (0.5.1i):** https://github.com/Creators-of-Create/Create/wiki/0.5.1i
- **Mekanism:** https://github.com/mekanism/Mekanism
- **Immersive Engineering:** https://github.com/BluSunrize/ImmersiveEngineering
- **Applied Energistics 2:** https://github.com/AppliedEnergistics/Applied-Energistics-2
- **Thermal Expansion (CoFH):** https://github.com/CoFH/ThermalExpansion

---

### Embedded Reference Links (Found Inside Notebook Sources)

#### Official Modding Docs, Mappings & Specifications
- **MinecraftForge Official Docs:** https://docs.minecraftforge.net/
- **NeoForge Official Docs:** https://docs.neoforged.net/
- **NeoForge Getting Started:** https://docs.neoforged.net/docs/gettingstarted/
- **NeoForge GitHub Org:** https://github.com/neoforged
- **Fabric Official Docs:** https://docs.fabricmc.net/
- **Fabric Develop Docs:** https://docs.fabricmc.net/develop/
- **Fabric Community Wiki:** https://wiki.fabricmc.net/
- **ParchmentMC:** https://parchmentmc.org/
- **Linkie Mappings Web Tool:** https://linkie.shedaniel.me/mappings
- **Mixin Javadocs:** https://jenkins.liteloader.com/view/Other/job/Mixin/javadoc/index.html
- **Forge Gemwire Wiki — Particles:** https://forge.gemwire.uk/wiki/Particles
- **Minecraft Wiki — Block & Item Models:** https://minecraft.wiki/w/Model
- **Minecraft Wiki — Resource Pack Format:** https://minecraft.wiki/w/Resource_pack
- **Minecraft Wiki — Pack Format Numbers:** https://minecraft.wiki/w/Pack_format
- **Modrinth API v2 Docs:** https://docs.modrinth.com/api/
- **Modrinth PAT Settings:** https://modrinth.com/settings/pats
- **CurseForge API Tokens:** https://legacy.curseforge.com/account/api-tokens

#### MCP, AI Tooling & Project Docs
- **Model Context Protocol (MCP) Spec:** https://modelcontextprotocol.io/
- **Serena Website:** https://oraios.github.io/serena
- **Serena User Guide (Intro):** https://oraios.github.io/serena/02-usage/000_intro.html
- **Serena Project-Based Workflow:** https://oraios.github.io/serena/02-usage/040_workflow.html
- **Serena Configuration:** https://oraios.github.io/serena/02-usage/050_configuration.html
- **Context7 Website:** https://context7.com/
- **MCModding-MCP on npm:** https://www.npmjs.com/package/mcmodding-mcp/
- **Transformers.js Docs:** https://huggingface.co/docs/transformers.js
- **better-sqlite3:** https://github.com/WiseLibs/better-sqlite3
- **Blockbench Website:** https://www.blockbench.net/
- **Hand-Lock `mode-13h` (Shader Companion Repo):** https://github.com/Hand-Lock/mode-13h

#### Maven Tools MCP Documentation
- **Setup:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/setup.md
- **Tools Catalog:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/tools.md
- **Examples & FAQ:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/examples.md#faq
- **Dogfooding Workflow:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/dogfooding.md
- **Troubleshooting:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/troubleshooting.md
- **Architecture:** https://github.com/arvindand/maven-tools-mcp/blob/main/docs/architecture.md
- **Corporate Certificates:** https://github.com/arvindand/maven-tools-mcp/blob/main/CORPORATE-CERTIFICATES.md
- **Notice:** https://github.com/arvindand/maven-tools-mcp/blob/main/NOTICE
- **maxxq-maven (Reference Resolver):** https://github.com/maxxq-org/maxxq-maven

#### GitHub MCP Server Skill Catalog
- **account-and-team-context:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/account-and-team-context/SKILL.md
- **codebase-exploration:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/codebase-exploration/SKILL.md
- **copilot-task-delegation:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/copilot-task-delegation/SKILL.md
- **discussion-participation:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/discussion-participation/SKILL.md
- **issue-authoring:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/issue-authoring/SKILL.md
- **issue-backlog-triage:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/issue-backlog-triage/SKILL.md
- **label-scheme-management:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/label-scheme-management/SKILL.md
- **notification-triage:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/notification-triage/SKILL.md
- **project-planning:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/project-planning/SKILL.md
- **pull-request-authoring:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/pull-request-authoring/SKILL.md
- **pull-request-code-review:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/pull-request-code-review/SKILL.md
- **pull-request-review-feedback:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/pull-request-review-feedback/SKILL.md
- **release-preparation:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/release-preparation/SKILL.md
- **repository-content-changes:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/repository-content-changes/SKILL.md
- **repository-discovery:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/repository-discovery/SKILL.md
- **repository-health-review:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/repository-health-review/SKILL.md
- **security-alert-triage:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/security-alert-triage/SKILL.md
- **workflow-failure-triage:** https://github.com/github/github-mcp-server/blob/main/pkg/skills/catalog/skills/workflow-failure-triage/SKILL.md

#### SpongePowered Mixin Wiki Pages
- **Injection Point Reference:** https://github.com/SpongePowered/Mixin/wiki/Injection-Point-Reference
- **Obfuscation and Mixins:** https://github.com/SpongePowered/Mixin/wiki/Introduction-to-Mixins---Obfuscation-and-Mixins
- **Overwriting Methods:** https://github.com/SpongePowered/Mixin/wiki/Introduction-to-Mixins---Overwriting-Methods
- **Resolving Method Signature Conflicts:** https://github.com/SpongePowered/Mixin/wiki/Introduction-to-Mixins---Resolving-Method-Signature-Conflicts
- **Understanding Mixin Architecture:** https://github.com/SpongePowered/Mixin/wiki/Introduction-to-Mixins---Understanding-Mixin-Architecture
- **Mixin Java System Properties:** https://github.com/SpongePowered/Mixin/wiki/Mixin-Java-System-Properties
- **Mixins on Minecraft Forge:** https://github.com/SpongePowered/Mixin/wiki/Mixins-on-Minecraft-Forge
- **PSA: Forward Compatibility Features in Mixin:** https://github.com/SpongePowered/Mixin/wiki/PSA-Forward-Compatibility-Features-in-Mixin
- **Release Notes — Mixin 0.8:** https://github.com/SpongePowered/Mixin/wiki/Release-Notes---Mixin-0.8
- **Clone Mixin Wiki:** https://github.com/SpongePowered/Mixin.wiki.git
- **TelepathicGrunt Mixin Gist:** https://gist.github.com/TelepathicGrunt/3784f8a8b317bac11039474012de5fb4

#### Create Mod Wiki Pages
- **Create Wiki Home:** https://github.com/Creators-of-Create/Create/wiki
- **Changing Gears:** https://github.com/Creators-of-Create/Create/wiki/Changing-Gears
- **Chute:** https://github.com/Creators-of-Create/Create/wiki/Chute
- **Cogwheel:** https://github.com/Creators-of-Create/Create/wiki/Cogwheel
- **ComputerCraft Integration:** https://github.com/Creators-of-Create/Create/wiki/ComputerCraft-Integration
- **Content Observer:** https://github.com/Creators-of-Create/Create/wiki/Content-Observer
- **Copper:** https://github.com/Creators-of-Create/Create/wiki/Copper
- **Speedometer (Peripheral):** https://github.com/Creators-of-Create/Create/wiki/Speedometer-(Peripheral)
- **Spout:** https://github.com/Creators-of-Create/Create/wiki/Spout
- **Stress Units, Capacity and Impact:** https://github.com/Creators-of-Create/Create/wiki/Stress-Units,-Capacity-and-Impact
- **Stressometer (Peripheral):** https://github.com/Creators-of-Create/Create/wiki/Stressometer-(Peripheral)
- **Supporting the Project:** https://github.com/Creators-of-Create/Create/wiki/Supporting-the-Project
- **The Basics of Rotation in Create:** https://github.com/Creators-of-Create/Create/wiki/The-Basics-of-Rotation-in-Create
- **Wand of Symmetry:** https://github.com/Creators-of-Create/Create/wiki/Wand-of-Symmetry
- **Waterwheel:** https://github.com/Creators-of-Create/Create/wiki/Waterwheel
- **Zinc:** https://github.com/Creators-of-Create/Create/wiki/Zinc
- **Clone Create Wiki:** https://github.com/Creators-of-Create/Create.wiki.git

#### McJty Tutorials, Videos & Resources
- **McJty Intro:** https://www.mcjty.eu/docs/intro
- **McJty 1.20 Concepts:** https://www.mcjty.eu/docs/1.20/concepts
- **McJty 1.20 Episode 1 (Wiki / Video / Repo):**
  - https://www.mcjty.eu/docs/1.20/ep1
  - https://youtu.be/BpUbD0NXfp8
  - https://github.com/McJty/Tut4_1Basics
- **McJty 1.20 Episode 2 (Wiki / Video / Repo):**
  - https://www.mcjty.eu/docs/1.20/ep2
  - https://youtu.be/4IQLCHSoUN8
  - https://github.com/McJty/Tut4_2Block
- **McJty 1.20 Episode 3 (Wiki / Video):**
  - https://www.mcjty.eu/docs/1.20/ep3
  - https://youtu.be/jE68rw_sAXg
- **McJty 1.20 Episode 4 (Wiki / Video / Repo):**
  - https://www.mcjty.eu/docs/1.20/ep4
  - https://youtu.be/1MaePcTVisw
  - https://github.com/McJty/Tut4_3Power
- **McJty 1.20 Episode 5 (Wiki / Video):**
  - https://www.mcjty.eu/docs/1.20/ep5
  - https://youtu.be/WUhet8dOlAs
- **McJty Other Version Tutorials:**
  - 1.21.1 and 26.2 NeoForge: https://www.mcjty.eu/docs/1.21.1_26.2
  - 1.20.4 NeoForge: https://www.mcjty.eu/docs/1.20.4_neo
  - 1.19.3: https://www.mcjty.eu/docs/1.19.3
  - 1.19: https://www.mcjty.eu/docs/1.19
  - 1.18: https://www.mcjty.eu/docs/1.18/
  - 1.17: https://www.mcjty.eu/docs/1.17
  - 1.14–1.16: https://www.mcjty.eu/docs/1.14-1.15-1.16
  - 1.15: https://www.mcjty.eu/docs/1.15
  - 1.12: https://www.mcjty.eu/docs/1.12
- **McJty TutorialV3 (Mana System Example):** https://github.com/McJty/TutorialV3/tree/98b824b6adfb318c19fe96ae41f504ade7d40dcf/src/main/java/com/example/tutorialv3/manasystem
- **McJty Mod Docs:** https://www.mcjty.eu/docs/mods
- **McJty Control Validator:** https://www.mcjty.eu/control-validator
- **McJty Website Source:** https://github.com/McJtyMods/mcjty.eu
- **McJty Community Links:**
  - YouTube: https://www.youtube.com/channel/UCYMg1JQw3syJBgPeW6m68lA
  - Discord: https://discord.com/invite/YaWr7Zb
  - Twitter: https://twitter.com/McJty
  - Reddit: https://www.reddit.com/user/McJty
  - Twitch: https://www.twitch.tv/McJty
  - Patreon: https://www.patreon.com/McJty

#### Kaupenjoe & ModdingTutorials.org Links
- **Kaupenjoe Forge 1.20.X YouTube Playlist:** https://www.youtube.com/playlist?list=PLKGarocXCE1H9Y21-pxjt5Pt8bW14twa-
- **Kaupenjoe Forge 1.18.1 Tutorial Repo:** https://github.com/Tutorials-By-Kaupenjoe/Forge-Tutorial-1.18.1/tree/main/src/main/java/net/kaupenjoe/tutorialmod
- **ModdingTutorials.org — 1.18.2 Environment Setup:** https://moddingtutorials.org/1.18.2/environment-setup
- **ModdingTutorials.org — 1.19.2 Advanced Items (Teleport):** https://moddingtutorials.org/1.19.2/advanced-items/

#### Iron's Spells 'n Spellbooks Planning, Gradle & Video Links
- **Miro Board:** https://miro.com/app/board/uXjVPvycxJQ=/
- **Spell Sheet (Google Sheets):** https://docs.google.com/spreadsheets/d/1o0MyG9ok5Csf8_-77f-qH3VqOu6NtiuYcBb_SzDmA3M/edit#gid=1973083805
- **Trello Board:** https://trello.com/b/yzpLtJpQ/spell-book-mod
- **Original Repo Link:** https://github.com/iron431/irons_spellbooks
- **ImmersiveEngineering `build.gradle` Reference:** https://github.com/BluSunrize/ImmersiveEngineering/blob/7d49b2aa24b5759931db0220ecffec447dc854b9/build.gradle
- **OpenComputers `build.gradle` Reference:** https://github.com/MightyPirates/OpenComputers/blob/de8f207f3bc4ed5fc14c8e163263f3541bf30c2a/build.gradle#L30
- **YouTube — Entity Creation in Blockbench:** https://www.youtube.com/watch?v=XBIXn7s-fMo
- **YouTube — Item Stack:** https://www.youtube.com/watch?v=edcpW1zzUfk
- **YouTube — Creating Entities / Blockbench (1):** https://www.youtube.com/watch?v=VlUwLXkwb2c
- **YouTube — Creating Entities / Blockbench (2):** https://www.youtube.com/watch?v=kxzZ-oJKjcY
- **YouTube — General Modding Reference:** https://www.youtube.com/watch?v=prqMxqUtj-0
- **YouTube — Loading Values from Config:** https://www.youtube.com/watch?v=QN9jq3_V-I8
- **YouTube — Particles:** https://www.youtube.com/watch?v=DM69u76tXMI

#### Documentation Sites, Build & Dev Workflow Tools
- **Jekyll CI with GitHub Actions:** https://jekyllrb.com/docs/continuous-integration/github-actions/
- **Jekyll Themes:** https://jekyllrb.com/docs/themes/
- **Publishing Jekyll Docs to GitHub Pages:** https://idratherbewriting.com/documentation-theme-jekyll/mydoc_publishing_github_pages.html
- **Bulma Clean Theme:** https://github.com/chrisrhymes/bulma-clean-theme/#installation
- **GitHub Pages Gem:** https://github.com/github/pages-gem
- **GitHub Docs — About GitHub Pages and Jekyll:** https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
- **Pre-commit:** https://pre-commit.com/
- **Git Documentation:** https://git-scm.com/doc
- **Conventional Commits:** https://www.conventionalcommits.org/en/v1.0.0/
- **Semantic Versioning:** https://semver.org/
- **SemVer Pre-Release Spec:** https://semver.org/#spec-item-9
- **GitHub Actions Documentation:** https://docs.github.com/en/actions
- **Gradle User Guide:** https://docs.gradle.org/current/userguide/userguide.html
- **Git Cliff (Automatic Changelogs):** https://git-cliff.org/

#### Community & Reference Project Links
- **Applied Energistics 2 Website:** https://appliedenergistics.org/
- **Applied Energistics 2 GitHub Pages:** https://appliedenergistics.github.io/
- **Applied Energistics 2 Players Guide:** https://guide.appliedenergistics.org/
- **Applied Energistics 2 Discord:** https://discord.gg/Zd6t9ka7ne
- **Ridanisaurus (AE2 Textures/Models):** https://github.com/Ridanisaurus/
- **AE2 Guidebook Click Sound (Freesound):** https://freesound.org/people/EminYILDIRIM/sounds/536108/
- **Kiku's Realm Discord (Stonecutter):** https://discord.kikugie.dev/
- **Cascading Colors Discord (Stonecutter Template):** https://discord.gg/aunYJB4wz9
- **The Fabric Project Discord:** https://discord.gg/v6v4pMv