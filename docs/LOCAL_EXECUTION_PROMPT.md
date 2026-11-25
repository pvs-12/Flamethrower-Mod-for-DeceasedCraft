# Local Master Execution Guide & Single-Prompt Kickoff (Phases 2–6)

This document gives you **one single copy-paste prompt** to launch **Create: Tactical ChemThrowers** (`modid: tacticalchemthrowers`) from **Phase 2 through Phase 6** in a brand-new local Antigravity conversation inside **any new empty project folder**—tuned specifically for **Google AI Pro**, **minimal user inputs**, and **error-free multi-agent speed**.

---

## 1. The Optimal Antigravity Setup (30-Second Launch Checklist)

Before pasting the prompt below, set these four things in the **Google Antigravity App** (or CLI):

| Setting | Exact Value to Pick | Why |
| --- | --- | --- |
| **Model Selector** *(under prompt box)* | **`Orchestrator (Neon)`** *(default Pro quota saver)* — or **`Gemini 4 Neon (High)`** if you want zero executor handoffs on complex Java | `Orchestrator (Neon)` plans/reviews with **Gemini 4 Neon** and executes edits/tests with **Gemini 4 Hydrogen** (`~24%` less quota, `~19%` faster than monolithic heavy models, using your first-party Gemini quota). Do **not** select `Orchestrator (Carbon)` for the whole session—it burns ~32% more quota; the prompt reserves **Gemini 4 Carbon** selectively for high-stakes Gate C & Gate E audits. |
| **Multi-Agent Command** | **`/teamwork`** *(already at the top of the prompt below)* | `/teamwork` is built for multi-milestone builds spanning hours/days: its Project Orchestrator automatically hands off to a fresh successor between milestones (preventing 512K context rot), enforces exclusive file ownership, and runs independent Critic/Challenger/Auditor gates. **Never stack `/swarm` + `/teamwork` + `/goal` together.** |
| **Permissions** *(for minimal inputs)* | Allow safe command prefixes (`./gradlew`, `git`, `node`, `mc-asset`, `curl`) — or enable **Turbo** on the feature branch `dev/phases-2-6` | Prevents subagents from pausing repeatedly on terminal approvals (`Alt+J` / `Ctrl+K`). All work stays isolated on branch `dev/phases-2-6`. |
| **Local Prerequisites** | **Java 17 JDK**, **Node.js 22+**, `npm install -g mc-asset@0.6.0`, and **Blockbench Desktop `v5.2.2+`** open with `blockbench_mcp.js` loaded (`http://127.0.0.1:8787/ping` → `{"ok":true}`) | See [tools/README.md](../tools/README.md#local-desktop-workflow-windows--macos--linux-gui) for one-time Blockbench plugin setup. Keep Blockbench open for **Phases 3–4**. |

**Your total inputs across Phases 2 → 6:**
1. Open your new local project folder in Antigravity, select **`Orchestrator (Neon)`**, and paste the single prompt below.
2. Click **Approve** once when `/teamwork` displays its pre-filled brief artifact (all scoping questions are already answered inside the prompt).
3. When the team pauses cleanly after **Phase 5A**, drop the two built JARs into your local DeceasedCraft instances, run the guided live GPU/shader checklist, and reply with your results/logs so the team finishes **Phase 5C** and **Phase 6**.

---

## 2. The Single Copy-Paste Master Prompt (Phases 2 → 6)

Copy everything inside the fenced block below and paste it directly into your new local Antigravity conversation:

````markdown
/teamwork Build and release **Create: Tactical ChemThrowers** (`modid: tacticalchemthrowers`) across Phases 2 through 6 for DeceasedCraft v5.5.5 (MC 1.18.2 / Forge 40.2.4) and DeceasedCraft Beta-5.10.17 (MC 1.20.1 / Forge 47.4.0 Standard + DH Edition), pausing cleanly after Phase 5A for my live GPU/shader playtest before completing Phase 5C fixes and Phase 6 release packaging.

### TEAMWORK SCOPING PRE-FILL (SKIP REDUNDANT INTERVIEW QUESTIONS)
All design, architecture, compatibility, and verification requirements are ALREADY locked in the repository (`SPECS.md`, `AGENTS.md`, `compatibility/*.md`). Do NOT ask open-ended scoping questions—proceed directly to presenting the concise approval brief artifact with these exact settings:
- **Working Directory:** Operate directly inside this current local workspace folder (do NOT relocate to `~/teamwork_projects/...`). Keep all agent scratch/notes outside the git working tree (e.g. `~/.agents/teamwork/`) so zero agent metadata is ever committed.
- **Integrity Mode:** `development` (official Forge, Create, Immersive Engineering, GeckoLib, `mc-asset`, and `blockbench-mcp` libraries/tools are required and permitted; zero plagiarized third-party mod code or assets).
- **Git Branch Safety:** Create and work on branch `dev/phases-2-6` (never force-push or rewrite history).
- **Pause Point:** Pause after **Phase 5A** completes with both built JARs (`1.18.2` + `1.20.1`) and a guided **Phase 5B** live Minecraft/Oculus shader checklist. Once I reply with my live test results/logs/screenshots, immediately resume to execute **Phase 5C** bug fixes and **Phase 6** final release packaging.

---

### STEP 0: NEW-FOLDER BOOTSTRAP, PREFLIGHT & IDEMPOTENT RESUME (SEQUENTIAL — 1 AGENT)
Before spawning implementation waves:
1. **Bootstrap Repository:**
   - If the current folder is empty / not a git repo, run `git clone https://github.com/pvs-12/Flamethrower-Mod-for-DeceasedCraft.git .` (or clone into `./Flamethrower-Mod-for-DeceasedCraft` if the folder has unrelated files, then work inside it).
   - Otherwise run `git fetch origin && git pull --ff-only origin main`.
   - Switch to or create branch `dev/phases-2-6`.
2. **Preflight Tool Check:** Verify and report exact versions of:
   - Java 17 JDK (`java -version`) — required for both Forge `1.18.2` and `1.20.1`.
   - Node.js `22+` (`node -v`).
   - `mc-asset` (`mc-asset --version` — install via `npm install -g mc-asset@0.6.0` if missing).
   - Blockbench Desktop MCP bridge (`curl -s http://127.0.0.1:8787/ping`). If Blockbench is not running yet, note it and continue Phase 2, then pause/prompt me right before Wave 3A only if `:8787/ping` is still unreachable.
3. **Mandatory Context Ingestion:** Read `AGENTS.md`, `SPECS.md`, `compatibility/ECOSYSTEM_MATRIX.md`, `compatibility/RECIPE_AND_FLUID_AUDIT.md`, `compatibility/COMBAT_AND_PROTECTION_AUDIT.md`, `compatibility/API_AND_INTEGRATION_RESEARCH.md`, and `tools/README.md` in full before designing any Java class.
4. **Idempotent Crash/Quota Resume:** Inspect `git log --oneline -n 20` for phase checkpoint commits (`chore(checkpoint): phase-2-complete`, `phase-3-complete`, `phase-4-complete`, `phase-5a-complete`, `phase-6-complete`). Automatically skip any already-completed phase and resume cleanly at the next unfinished wave without redoing finished work.

---

### NON-NEGOTIABLE ENGINEERING & EULA GUARDRAILS (ALL AGENTS)
1. **Mod Identity & Strict EULA:** Official name `Create: Tactical ChemThrowers`, `modid: tacticalchemthrowers`. Use 100% original fictional industrial/tactical names everywhere. ZERO real-world firearm/flamethrower trademarks, manufacturer names, or model numbers. ZERO copyrighted movie/TV/game/franchise IP names anywhere in code, assets, lang files, or docs. ZERO plagiarized code/models/textures/audio.
2. **3D Aesthetic:** Heavy Tactical + Create Mod Aesthetic (perforated heat-shielded barrel, dual/underslung canister cradle, tactical rails, armored turret gimbal/chassis blended with riveted andesite/dark iron, copper pressure pipes, brass valves, mechanical pressure dial & cogwheels).
3. **Dual-Version Separation:** Multi-project Gradle layout (`:core` pure Java 17 + `shared-assets/` + `:forge-1.18.2` + `:forge-1.20.1`). NEVER leak client classes into common/server code. Strictly isolate:
   - Forge `40.2.4` (`CapabilityFluidHandler`, `DamageSource.setIsFire()`, `GlobalLootModifierSerializer`, `ClientRegistry`) vs Forge `47.4.0` (`ForgeCapabilities`, data-driven `DamageType` JSON + `#minecraft:is_fire`, Codec `IGlobalLootModifier`, `RegisterKeyMappingsEvent`, `DeferredRegister<CreativeModeTab>`).
   - Create `0.5.1.f` (Flywheel `0.6`, `maven.tterrag.com`) vs Create `6.0.6` (Flywheel `1.0`, extracted `net.createmod.ponder`, `com.simibubi.create.api.*`, `maven.createmod.net` + `MixinExtras`).
   - GeckoLib `3.0.57` (`IAnimatable`, `IItemRenderProperties`) vs GeckoLib `4.7` (`GeoItem`/`GeoBlockEntity`, `IClientItemExtensions`).
   - `Immersive Petroleum` (`1.18.2`, `#forge:seedoil`/`#forge:plantoil`, `#forge:napalm`, `#forge:crude_oil`, etc.) vs `Create: Diesel Generators` (`1.20.1`, `#forge:seed_oil`, `#forge:diesel`, `#forge:gasoline`, `#forge:crude_oil`, KubeJS `material.js` removes CDG ethanol/plant oil in favor of `createaddition:bioethanol` & `seed_oil`).
4. **Locked Gameplay & Fuel Rules:**
   - **1 modular handheld ChemThrower** with swappable nozzle/pressure modules (`15 → 25 → 35` block range) and visible 3D barrel changes.
   - **Canister-only reload:** `50 units = 1,000 mB`, `4 mB/tick` baseline (`12.5s` fire); reload via `R` or `Sneak+Right-Click` (`1.5s`, returns spent canister). Only `FuelCanisterItem` implements `IFluidHandlerItem` (fillable via Create Spouts/Tanks/Pipes & IE Bottling Machine/Tanks; no mixing; `FluidAction.SIMULATE` strictly side-effect-free).
   - **Zero duplicate custom fluids:** Data-driven `data/tacticalchemthrowers/flamethrower_fuels/*.json` (lookup: exact fluid ID → Forge fluid tag → reject). **Raw `#forge:crude_oil` IS burnable by default** (`0.85x` dmg, `0.85x` range, `5.0 mB/t`, heavy droop & very dense black soot) alongside all 11 other accepted pack fuel families in `SPECS.md §6.4`.
   - **Combat & Stance:** `+10%`/hit up to `2.0x` (10 hits), resets after `2.5s` without hit; `≤ 4` blocks point-blank lava bonus + `3s` burn; Heavy Braced Creep (`~15%` walk speed, no sprint/jump) while firing; ZERO camera pitch kick (pure 1st-person gun+hands kickback & vibration); underwater firing blocked; custom non-spreading `TemporaryFlameBlock` respecting `doFireTick` (`true` in both packs), `natural_regeneration = false`, claims, and `#minecraft:is_fire` (auto-honoring DeceasedCraft Firefighter armor set fire resistance).
   - **VFX & Night Glow:** Crisp pixel-native blocky billboard particles (`0.18–0.55b`) via `mc-asset` with 4-stage combustion lifecycle (white-yellow pressurized core → roaring orange flame + sparks → cooling crimson ember → rising dark/black hydrocarbon smoke lingering on trigger release), hard/soft client particle caps + LOD, `ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT`/`LIT` + `LightTexture.FULL_BRIGHT` (`0x00F000F0`), LabPBR 1.3 `_s.png` emissives, soft `Lucent` (`1.18.2`) & `Sodium Dynamic Lights` (`1.20.1`) bridges, and **real turret blockstate `lightLevel` (`14` firing / `5` pilot)** because Beta `5.10.17` sets `block_entities = false` in `sodiumdynamiclights-client.toml`.
   - **Automated Turret:** Fixed ports — **Left** = Create Shaft (`RPM`/`SU` slew), **Right** = Forge Energy (`IEnergyStorage`), **Back + Bottom** = Create Fluid Pipe (`IFluidHandler`); right-click GUI, Create Wrench rotate/pickup, Engineer's Goggles telemetry.
   - **Critical Recipe Rule:** NEVER use raw `create:electron_tube` in recipes (both packs globally replace it with `immersiveengineering:component_electronic`); use `immersiveengineering:component_electronic` / `component_electronic_adv` with a `forge:mod_loaded` standalone fallback. Never disable or override IE's Chemthrower or Chemthrower Turret.

---

### PARALLEL MULTI-AGENT RULES & GOOGLE AI PRO MODEL ROUTING
To maximize speed without collisions, quota waste, or errors:
- **Optimal Concurrency:** Cap parallel write workers at **2–4 per wave** (+1 independent Critic/Auditor). Never spawn overlapping file editors.
- **Strict Disjoint Write Ownership:** Every worker gets an explicit folder allowlist and must NOT edit outside it.
- **Single Build & Git Owner:** Workers write source/assets/tests ONLY—they NEVER run `git add`/`git commit` or full root `./gradlew build` concurrently. Only the Project Orchestrator / Auditor runs `./gradlew test build` and creates checkpoint commits after each wave converges.
- **Single Blockbench MCP Owner:** Never let two workers call `http://127.0.0.1:8787` at the same time (one active GUI session).
- **Google AI Pro Model Routing:**
  - **Gemini 4 Neon** (`High` for Wave 2A scaffold & tricky adapters; `Medium`/`High` for Java/VFX/3D workers): Gradle build graph, `:core`, `:forge-1.18.2`, `:forge-1.20.1`, Blockbench 3D modeling/animations, VFX/GeckoLib renderers, Create turret adapters.
  - **Gemini 4 Hydrogen:** JSON datapacks (12 fuel JSONs, additive recipes, Lootr GLMs), `en_us.json`, `:core` JUnit tests, `mc-asset` 2D/LabPBR textures, Phase 5A `runServer` log checks, Phase 6 hygiene & release docs.
  - **Gemini 4 Carbon (selective — high-leverage gates only):** Independent **Critic/Auditor** at **Gate C** (Create `0.5.1.f` vs `6.0.6` + compat bridges) and **Success Auditor** at **Gate E** (final release sign-off).

---

### WAVE-BY-WAVE EXECUTION SCHEDULE (PHASES 2 → 6)

#### PHASE 2 — Dual-Version Scaffolding & Handheld Core Vertical Slice (Gate B)
- **Wave 2A (1 Worker — Gemini 4 Neon High, Sequential):** Scaffold Gradle multi-project (`settings.gradle`, `build.gradle`, `:core`, `:forge-1.18.2`, `:forge-1.20.1`, `shared-assets/`) pinned to Forge `40.2.4` and `47.4.0` with Create, IE, and GeckoLib Maven coordinates from `compatibility/API_AND_INTEGRATION_RESEARCH.md`. Verify empty `./gradlew build` passes cleanly before Wave 2B.
- **Wave 2B (4 Parallel Workers + 1 Gate B Auditor):**
  1. `@core-engine` *(Gemini 4 Neon)* — owns `:core/src/main/**`: `FuelRegistry` (exact ID → tag → reject, `/reload` + sync DTO), `JetGeometry` swept capsule/droop math, `HeatTracker` (`+10%` to `2.0x`, `2.5s` reset), config clamping, shared combat/turret interfaces.
  2. `@forge-1182-handheld` *(Gemini 4 Neon)* — owns `:forge-1.18.2/**`: `TacticalChemThrowerItem`, `FuelCanisterItem` (`IFluidHandlerItem`, `1,000 mB` = `50 units`, no mixing), canister-only reload (`R` & `Sneak+Right-Click`, `1.5s`), modular nozzles (`15/25/35b`), `≤4b` lava bonus, `~15%` braced stance, underwater block, `TemporaryFlameBlock`, `SimpleChannel` sync, Forge server/client configs.
  3. `@forge-1201-handheld` *(Gemini 4 Neon)* — owns `:forge-1.20.1/**`: Exact parity on Forge `47.4.0` (`ForgeCapabilities`, data-driven `DamageType` JSON + `#minecraft:is_fire`, `RegisterKeyMappingsEvent`, `DeferredRegister<CreativeModeTab>`).
  4. `@data-and-tests` *(Gemini 4 Hydrogen)* — owns `shared-assets/data/**` & `:core/src/test/**`: All 12 `flamethrower_fuels/*.json` files (including burnable `#forge:crude_oil`), damage-type tags, `en_us.json`, and JUnit tests for `FuelRegistry`, `HeatTracker`, `JetGeometry`, and `SIMULATE` immutability.
- **Gate B Sign-Off (Orchestrator + Critic):** Run `./gradlew test build`, verify both JARs compile, confirm zero client imports in common/server packages, run EULA scan, and commit `chore(checkpoint): phase-2-complete`.

#### PHASE 3 — 3D Heavy Tactical + Create Assets, 4-Stage Flame VFX & Audio (Gate B/D)
- **Wave 3A (3 Parallel Workers + 1 Visual/Build Auditor):**
  1. `@modeler-3d` *(Gemini 4 Neon — SOLE Blockbench MCP owner via `tools/bb_mcp_client.mjs`)* — owns `shared-assets/assets/tacticalchemthrowers/geo/` & `animations/` (+ `.bbmodel` source in `assets-src/`): Build Heavy Tactical + Create handheld ChemThrower (with Tier 1/2/3 visible barrel/nozzle assemblies) and Pressurized Fuel Canister, author 1st-person gun+hands recoil/vibration + `1.5s` canister swap + 3rd-person braced animations, export GeckoLib `.geo.json` & `.animation.json`, and save multi-angle QA PNGs into scratch for auditor inspection.
  2. `@artist-2d` *(Gemini 4 Hydrogen — uses `mc-asset` CLI)* — owns `shared-assets/assets/tacticalchemthrowers/textures/`: Author crisp pixel-native 4-stage blocky flame-to-black-smoke animated particle strips + `.mcmeta`, item/HUD/GUI textures, and LabPBR 1.3 `_s.png` emissive maps (`A = 1–254`); pass `mc-asset validate` on every generated file.
  3. `@vfx-audio-lights` *(Gemini 4 Neon)* — owns client VFX/renderer/audio packages in `:forge-1.18.2` & `:forge-1.20.1`: Implement Iris/Oculus-safe 4-stage billboard particles (`LightTexture.FULL_BRIGHT` Stages 1–3, world-lit Stage 4 soot, soft/hard caps, distance LOD, `Particles` setting scaling), GeckoLib 3 (`1.18.2`) & GeckoLib 4 (`1.20.1`) item renderers with zero camera pitch kick, layered mono `.ogg` sounds + `sounds.json` + managed `TickableSoundInstance`, HUD bar/tooltip, and soft `Lucent` (`1.18.2`) / `Sodium Dynamic Lights` (`1.20.1`) bridges.
- **Phase 3 Sign-Off (Orchestrator + Auditor):** Verify `mc-asset validate` passes, visually inspect Blockbench QA PNG screenshots, verify `./gradlew build` succeeds on both targets, and commit `chore(checkpoint): phase-3-complete`.

#### PHASE 4 — Automated Kinetic Turret & DeceasedCraft Ecosystem Integrations (Gate C)
- **Wave 4A (4 Parallel Workers + 1 Carbon Gate C Auditor):**
  1. `@turret-model-core` *(Gemini 4 Neon — SOLE Blockbench MCP owner)* — owns `:core/.../turret/` & turret `.geo.json`/`.animation.json`: Build armored tactical gimbal + Create brass/copper/iron turret model with visually color-coded fixed ports (Left Shaft, Right FE, Back+Bottom Fluid) + QA screenshots, and implement version-agnostic bounded target scanner (`10t` staggered), filter state machine, and RPM-scaled slew math.
  2. `@forge-1182-turret-compat` *(Gemini 4 Neon)* — owns `:forge-1.18.2/**`: Create `0.5.1.f` `KineticBlockEntity`, `IHaveGoggleInformation`, `IWrenchable`, fixed-face capabilities, right-click GUI (`AbstractContainerMenu`), real blockstate `lightLevel` (`14` firing / `5` pilot), plus `ModList.isLoaded`-guarded soft bridges for `Open Parties & Claims`, `FTB Teams`, `Zombie Awareness`, `Cold Sweat`, and `1.18.2` `GlobalLootModifierSerializer`.
  3. `@forge-1201-turret-compat` *(Gemini 4 Neon)* — owns `:forge-1.20.1/**`: Create `6.0.6` (`com.simibubi.create.api.*`, Flywheel `1.0`) turret parity + `ModList.isLoaded`-guarded soft bridges for `Open Parties & Claims`, `FTB Teams`, `Zombie Awareness`, `Legendary Survival Overhaul`, and `1.20.1` Codec `IGlobalLootModifier`.
  4. `@recipes-and-loot` *(Gemini 4 Hydrogen)* — owns `shared-assets/data/tacticalchemthrowers/recipes/` & `loot_modifiers/`: Additive Create Mechanical Crafting, Sequenced Assembly, and shaped recipes using `immersiveengineering:component_electronic` / `component_electronic_adv` (with `forge:mod_loaded` standalone fallback — NEVER raw `create:electron_tube`), plus Lost Cities military/lab Lootr-safe GLMs.
- **Gate C Sign-Off (Orchestrator + Gemini 4 Carbon Critic/Auditor):** Run `./gradlew test build`, verify Create `0.5.1.f` & `6.0.6` integration, verify zero hard dependencies on optional mods, verify zero recipe overrides of DeceasedCraft scripts, and commit `chore(checkpoint): phase-4-complete`.

#### PHASE 5A — Automated Dedicated Server Soak & Pause for Live GPU Shader Testing (Gate D)
- **Wave 5A (2 Parallel Workers — Gemini 4 Hydrogen):** Launch `:forge-1.18.2:runServer` and `:forge-1.20.1:runServer` headlessly (eula=true in temp run dirs), verify clean startup with zero client-class crashes, confirm `flamethrower_fuels` datapack reload & zero missing-recipe/tag errors, and shut down cleanly.
- **Commit Checkpoint:** `chore(checkpoint): phase-5a-complete`.
- **PAUSE & HANDOFF FOR MY PHASE 5B LIVE TEST:** Stop autonomous execution here and present:
  1. Exact file paths to both built JARs (`1.18.2` & `1.20.1`).
  2. A concise, numbered **Phase 5B Live Test Checklist** for me to run in DeceasedCraft `v5.5.5` and `Beta-5.10.17` (Standard + DH Edition): Create Spout / IE Bottling Machine canister filling, raw crude oil + diesel/gasoline/napalm firing, 1st-person recoil & 4-stage flame-to-black-smoke look, night glow across **BSL**, **Complementary Reimagined / Unbound + Euphoria**, **Photon**, **Bliss**, **Spooklementary**, and **Distant Horizons**, turret Shaft/FE/Fluid ports + Wrench/Goggles, and `spark` horde FPS/TPS capture.
  3. Wait for my reply with test results, logs, or screenshots.

#### PHASE 5C & PHASE 6 — Live-Test Bug Fixes, Hygiene Audit & Release Packaging (Gate D/E — Runs Automatically After My Phase 5B Reply)
- **Phase 5C (If I report any issues):** Dispatch targeted `@fix-*` workers *(Gemini 4 Neon)* per version/subsystem to resolve every reported visual, shader, balance, or compatibility issue, re-run `./gradlew test build`, and record verified numbers in `PERFORMANCE_BUDGET.md` and `compatibility/TEST_RESULTS.md`.
- **Wave 6A (2 Parallel Workers — Gemini 4 Hydrogen):**
  1. `@hygiene-auditor`: Full EULA/trademark/IP scan, zero leftover debug logs/TODOs, verify `mods.toml` metadata, license, and versioned JAR naming (`tacticalchemthrowers-1.18.2-...jar` & `tacticalchemthrowers-1.20.1-...jar`).
  2. `@release-docs`: Write player guide, server-admin config reference, datapack fuel customization guide, and `CHANGELOG.md` (explicitly noting `Beta-5.10.17` beta caveats).
- **Gate E Final Sign-Off (Success Auditor — Gemini 4 Carbon):** Run clean `./gradlew clean test build`, compute SHA-256 checksums of both release JARs, confirm `git status` is clean, commit `chore(checkpoint): phase-6-complete`, and present the final release report.
````

---

## 3. Optional Power-Command Fallbacks (When You Want Manual Control)

Only use these **instead of** the `/teamwork` master prompt (never stacked on top of it):

- **Run just ONE phase on a live interactive board (`/swarm`):**
  > Select **`Orchestrator (Neon)`** or **`Gemini 4 Neon`**, then prompt:  
  > `/swarm Read AGENTS.md, SPECS.md, and compatibility/API_AND_INTEGRATION_RESEARCH.md. Execute ONLY Phase <N> using the worker split in docs/LOCAL_EXECUTION_PROMPT.md. Run Java/3D workers on Gemini 4 Neon, JSON/test/2D workers on Gemini 4 Hydrogen, and @verifier on Gemini 4 Carbon.`
- **Crush a single brutal Phase 5 bug (shader glitch, Flywheel 1.0 crash, concurrency race) with `/boost`:**
  > `/boost Diagnose and fix <paste exact crash log or shader symptom> in :forge-1.20.1 without adding invasive Embeddium/Oculus mixins. Verify with ./gradlew :forge-1.20.1:build.`
