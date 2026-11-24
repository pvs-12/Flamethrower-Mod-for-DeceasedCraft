# Minecraft Flamethrower — Project Specification

**Document:** `SPECS.md`  
**Project:** Minecraft Flamethrower (DeceasedCraft compatible)  
**Status:** Living technical specification / implementation contract  
**Last researched:** 2026-11-24  
**Primary target:** Minecraft Java Edition, Forge  

> This document consolidates the project decisions available from the prior planning discussions. Requirements marked **Confirmed** are user decisions. Items marked **Research gate**, **Provisional**, or **Open** must be verified before implementation; do not silently treat them as settled facts.

---

## 1. Project objective

Develop a polished, immersive, performant flamethrower and related fuel/defensive machinery for DeceasedCraft. The result should feel native to DeceasedCraft's survival, scavenging, combat, and technology progression rather than like a standalone weapon mod dropped into the pack.

The project has two compatibility targets:

1. **DeceasedCraft v5.5.5** — Minecraft 1.18.2, Forge; the complete/stable legacy branch.
2. **DeceasedCraft v6 development line** — currently represented by the latest public v6-development beta, **DeceasedCraft Beta 5.10.17**, Minecraft 1.20.1, Forge. This is not a final v6.0 release. The pack authors describe the 5.10.x line as an incomplete beta and state that it cannot currently be completed. Recheck the official project page before every compatibility release because the beta can change.

The two Minecraft versions are separate runtime targets. Do not assume a single compiled JAR can run on both. Prefer a shared design/specification and shared gameplay/data definitions with version-specific Forge adapters, source sets, or branches as technically appropriate.

## 2. Core design principles and priorities

### 2.1 Gameplay and visual direction

- **Performance is a first-class requirement.** Maintain high and stable game performance without compromising the intended visual quality, effects readability, model detail, animation, sound design, or creative direction.
- Do not solve performance by simply removing the visual identity. Optimize implementation: particle budgets, effect LOD, tick scheduling, entity queries, render layers, sound concurrency, and network synchronization.
- The weapon should communicate weight, heat, pressure, fuel consumption, and danger through coherent animation, sound, particles, and impact response.
- Visual effects must remain legible in combat and must not obscure the player's view excessively.
- Avoid excessive always-on particles, per-frame world scans, unnecessary block entities, or unbounded entity spawning.
- The weapon should fit DeceasedCraft's semi-realistic post-apocalyptic survival tone and technology progression.

### 2.2 Compatibility-first engineering

- DeceasedCraft compatibility is not limited to whether the mod launches. It includes recipe integration, fluid interoperability, item/tag conventions, progression, configuration, combat rules, and interactions with existing mods and their addons.
- Respect existing integrations and datapack/KubeJS/CraftTweaker-style recipe changes where present. Never replace or bypass pack recipes globally without a documented reason.
- Integrate with existing Create and Immersive Engineering ecosystems rather than implementing parallel, incompatible fluid or machine systems.
- Avoid hard dependencies on optional addons when a capability-based integration can provide graceful fallback.
- All integrations must be checked separately against the exact v5.5.5 and v6-beta manifests and configurations.

### 2.3 Maintainability

- Keep gameplay values configurable and centralized.
- Keep client-only rendering code isolated from common/server code.
- Use stable registries, namespaced IDs, data-driven recipes where practical, and explicit compatibility modules.
- Avoid reflection or mixins/coremods unless a documented integration requirement cannot be met through supported APIs/events.
- Never modify DeceasedCraft files in place as the normal installation method.

---

## 3. Target game environments and compatibility matrix

| Target | Minecraft | Loader | Pack release | Status |
|---|---:|---|---|---|
| Legacy stable | 1.18.2 | Forge | DeceasedCraft v5.5.5 | Confirmed target |
| v6 development beta | 1.20.1 | Forge | DeceasedCraft Beta 5.10.17 (latest public beta identified in research) | Confirmed target, beta caveats apply |
| Final v6.0 | To be verified | To be verified | Not yet established as a public final release | Open; revalidate before release |

### 3.1 Release/build strategy

- Maintain independent builds for 1.18.2 and 1.20.1.
- Pin the exact Minecraft, Forge, mappings, Java toolchain, and dependency versions for each build.
- Keep gameplay balance values and content definitions aligned between branches where possible.
- Record unavoidable platform differences in `COMPATIBILITY.md` or a version-specific integration note.
- Test against clean instances of the exact modpack release, not merely a development profile containing a few headline mods.

---

## 4. Functional requirements: handheld flamethrower

### 4.1 Weapon operation

**Confirmed requirements**

- The handheld flamethrower fires a continuous jet while the player holds right-click.
- The flame stream should have a clear origin at the nozzle and a readable forward direction.
- The weapon must support configurable effective range tiers: **15, 25, and 35 blocks**. These are design targets, not permission to ignore line-of-sight, obstruction, or server-authoritative hit validation.
- It deals fire damage and an additional close-range / point-blank lava-like damage component.
- Consecutive hits build heat: **+10% per consecutive hit**, up to the configured maximum multiplier. The planning discussion referenced **2x / 2.5 seconds**; preserve this as the current tuning target but verify the exact interpretation (2x cap reached through consecutive hits and a 2.5-second decay/reset window) before final balance lock.
- Targets burn for **3 seconds** after being hit, subject to fire immunity and other protections.
- The stream may create temporary ground fire. Temporary fire must be bounded, cleaned up, and safe around protected blocks and modded block states.
- Tank capacity: **50 units**.
- Consumption target: **50 units per 12.5 seconds** of continuous firing (4 units/second), unless playtesting justifies a documented adjustment.
- Reload action: press **R** or use **sneak + right-click**; reload duration target **1.5 seconds**.
- Reload uses a replaceable/refillable cartridge system. Exact item taxonomy and crafting progression remain to be finalized against each pack version.
- No operation underwater.

### 4.2 Combat and world-rule compliance

The flamethrower must respect, rather than bypass, the host game's and modpack's combat rules:

- Fire immunity and damage immunity.
- Armor, enchantments, resistance effects, and relevant damage-type mitigation.
- Claims, protected regions, spawn protection, and server protection systems.
- PvP enablement and team/faction rules.
- Adventure mode and other interaction restrictions.
- Entity invulnerability, boss immunities, and modded entity-specific protections.
- Block protection and grief-prevention rules for temporary fire and environmental ignition.
- Server-side hit and damage validation. The client may render a predicted stream, but cannot be authoritative for damage, fuel, or block ignition.

Do not assume that vanilla `isOnFire` or a single damage source captures every pack-specific protection rule. Research the exact installed protection and combat mods and integrate through supported APIs/events where available.

### 4.3 Presentation requirements

- Animated first-person and third-person weapon model/pose where supported by the chosen rendering approach.
- Layered effects: nozzle ignition, continuous flame jet, heat distortion/embers where feasible, impact flare, short-lived ground fire, and shutdown/venting feedback.
- Layered audio: ignition, sustained firing loop, fuel/pressure behavior, reload, and empty-tank feedback.
- Effects should respond to firing state and fuel state; do not play continuous audio or spawn particles when the weapon is idle.
- Provide sensible fallback effects on low settings and when optional client visual features are unavailable.

---

## 5. Functional requirements: fuel ecosystem

### 5.1 Fluid compatibility

- Support multiple fuel types rather than hard-coding one custom fuel.
- Fuel interoperability with fluids supplied by other mods is a core requirement, especially **Immersive Engineering** fluids and Create fluid handling.
- Use the platform's fluid capability/API and Forge fluid tags/registries appropriate to each target version.
- Do not compare fluids by display name. Use registry identity, tags, and explicit compatibility rules.
- Define fuel properties in a data-driven or centralized configuration structure: burn value/efficiency, consumption modifier, ignition behavior, and any special effects.
- Handle fluid containers, tanks, pipes, pumps, and transfer limits through supported capabilities. Avoid private implementation access.
- Document whether a fluid is accepted as a direct fuel, requires refining/blending, or is explicitly rejected.

### 5.2 Existing technology ecosystems

**Confirmed direction:** use **Create** and **Create: Diesel Generators** for the fuel/technology ecosystem. Do **not** use Create: Petrochem as the planned core integration.

- Create should provide relevant fluid transport, storage, automation, and mechanical integration where the installed version supports it.
- Create: Diesel Generators should be evaluated as a fuel-processing / generator ecosystem partner, not assumed to expose a compatible API without inspection.
- Immersive Engineering fluid compatibility is required where the target pack includes it.
- Addons may have pack-specific recipe unification and item/fluid conventions. Inspect their source/configuration and actual installed versions before adding recipes.
- If an addon is absent in one pack version, the base mod must still load and provide a sensible fallback.

### 5.3 Recipes and progression

- Recipes must fit DeceasedCraft progression, loot scarcity, and tech gates.
- Prefer additive recipes and tags over overriding existing recipes.
- Verify that no recipe duplicates or conflicts with the pack's custom recipe scripts.
- Recipe integration must be tested independently in v5.5.5 and the v6 beta.
- Do not assume item IDs or fluid IDs remain identical between Minecraft versions or addon releases.

---

## 6. Functional requirements: automated flamethrower turret

**Confirmed concept:** a Create-integrated flamethrower turret.

### 6.1 Mechanical and electrical interfaces

- Turret requires a Create pipe/fluid connection for fuel supply.
- Turret requires Create rotational input for aiming/operation as designed.
- Turret requires an electrical power input. The exact power API and source ecosystem must be selected after inspecting the installed pack; do not invent an electrical network if no compatible one exists.
- The turret should expose clear connection points and in-world feedback for missing fuel, rotation, or electrical power.

### 6.2 Controls and configuration

- GUI-configurable firing range.
- GUI-configurable target filters.
- GUI-configurable pilot burner / ignition state.
- Left/right rotation and electrical input behavior must be discoverable from the block model, tooltip, GUI, or documentation.
- The prior control concept associated left rotation, right electricity, and a back-side connection; treat exact face/side mapping as **provisional** until the block layout and Create/electrical integration are prototyped.
- Turret firing must use server-authoritative targeting and damage checks.
- Include configurable target categories and exclusions; default behavior must not attack protected players, allies, or entities excluded by server rules.
- Avoid scanning all entities every tick. Use bounded search intervals, range-limited queries, and cached state where safe.

### 6.3 Safety and feedback

- Turret must not fire without required fuel and ignition/power conditions.
- Include an explicit off/maintenance state.
- Provide visual/audio indication of active pilot burner and firing state.
- Prevent uncontrolled fire spread and respect claims/protection rules.

---

## 7. DeceasedCraft mod inventory and compatibility research

### 7.1 Mandatory inventory rule

The AI developer must maintain **two separate, complete inventories**. Never merge them into one combined list and never infer a mod's presence from its presence in another DeceasedCraft release.

1. **Inventory A — DeceasedCraft v5.5.5 / Minecraft 1.18.2 / Forge**
2. **Inventory B — DeceasedCraft Beta 5.10.17 / Minecraft 1.20.1 / Forge** (latest public v6-development beta identified as of 2026-11-24)

For each inventory, record:

- Mod display name.
- Mod ID.
- Exact installed JAR filename and version.
- Required dependencies and optional dependencies.
- Whether it is client-only, server-only, or both.
- Relevant integration surface: items, blocks, entities, fluids, capabilities, recipes, damage, rendering, world protection, config, or progression.
- Whether the mod is a core mod or an addon in an ecosystem (Create, Immersive Engineering, etc.).
- Evidence source and verification date.

**Do not use third-party modpack lists as the authoritative inventory.** Extract each official CurseForge modpack archive's `manifest.json` and resolve every `projectID` + `fileID` to its exact project/file/version. Also inspect the installed `mods/` directory and pack configs/scripts for overrides or manually bundled content. CurseForge manifests may omit overrides or non-CurseForge files, so the installed instance is the final verification source.

### 7.2 Inventory A — v5.5.5 (1.18.2 Forge)

**Official pack identity:** `DeceasedCraft_v5.5.5`, released 2024-07-12, Minecraft 1.18.2, Forge. The official project identifies this as the more complete/stable branch for a complete playthrough.

**Full mod list: RESEARCH GATE — not yet extracted in this document.**

| Field | Required value |
|---|---|
| Official archive | DeceasedCraft v5.5.5 CurseForge file (project 490660; file 5525524) |
| Minecraft | 1.18.2 |
| Loader | Forge |
| Manifest extraction | Pending |
| Installed-JAR verification | Pending |
| Total mod count | Pending; do not estimate |
| Full inventory file | `compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv` (to be generated) |

Known ecosystem areas that must be verified against this exact archive (presence is not inferred solely from the project description):

- Create and its installed addons.
- Immersive Engineering and its installed addons, including whether the Chemthrower is present/enabled.
- Create: Diesel Generators, if present in this release.
- Fluid transport/storage and fluid-capability providers.
- Damage/combat, fire, claims/protection, and PvP rule mods.
- Recipe scripting/unification and progression mods.
- Rendering, animation, and sound dependencies needed by this project.

### 7.3 Inventory B — v6 development beta (1.20.1 Forge)

**Official pack identity:** `DeceasedCraft_Beta-5.10.17`, released 2026-07-17, Minecraft 1.20.1, Forge. The official project describes 5.10.x as the open beta for the v6 overhaul and warns that the beta is incomplete and cannot currently be completed. The project also warns that beta-world compatibility with final v6 is not guaranteed.

**Full mod list: RESEARCH GATE — not yet extracted in this document.**

| Field | Required value |
|---|---|
| Official archive | DeceasedCraft Beta 5.10.17 CurseForge file (project 490660; resolve exact file ID from official file page/API) |
| Minecraft | 1.20.1 |
| Loader | Forge |
| Manifest extraction | Pending |
| Installed-JAR verification | Pending |
| Total mod count | Pending; do not estimate |
| Full inventory file | `compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv` (to be generated) |

Known ecosystem areas that must be verified against this exact archive (presence is not inferred solely from the project description):

- Create and its installed addons.
- Immersive Engineering and its installed addons, including Chemthrower availability/configuration.
- Create: Diesel Generators, if present in this release.
- Fluid transport/storage and fluid-capability providers.
- Damage/combat, fire, claims/protection, and PvP rule mods.
- Recipe scripting/unification and progression mods.
- Rendering, animation, and sound dependencies needed by this project.

### 7.4 Cross-version ecosystem comparison

After both inventories are generated, create a comparison matrix. Keep the underlying inventories separate.

| Ecosystem / capability | v5.5.5 (1.18.2) | v6 beta (1.20.1) | Required action |
|---|---|---|---|
| Create | Verify exact version/addons | Verify exact version/addons | Build against each version's actual API and recipes |
| Immersive Engineering | Verify exact version/addons | Verify exact version/addons | Verify fluid IDs, capabilities, Chemthrower, damage/effect behavior |
| Create: Diesel Generators | Verify presence/version | Verify presence/version | Integrate only where installed; no Petrochem substitution |
| Fluid transfer/storage | Inventory all providers | Inventory all providers | Test every supported fluid path |
| Recipe scripts/unification | Inspect pack overrides | Inspect pack overrides | Test recipes after all pack scripts load |
| Combat/protection | Inventory relevant mods | Inventory relevant mods | Verify damage and ignition compliance |
| Rendering/animation | Inventory relevant mods | Inventory relevant mods | Test model/effects with actual client stack |

### 7.5 Why the full lists are currently marked pending

The official CurseForge pages establish the exact pack releases and version targets, but the web-accessible project pages used during this research did not expose the complete per-mod manifest contents. A third-party page found during research describes a different derivative pack (“Deceased Craft But Better”), so its 250-mod list is **not** a valid substitute for the official DeceasedCraft v5.5.5 inventory. The lists must be extracted from the official archives or exact installed instances. This is an explicit research gate, not permission for an AI agent to fabricate or approximate the inventories.

---

## 8. Compatibility implementation requirements

### 8.1 Integration architecture

- Separate common gameplay logic from version-specific Forge registration and API bindings.
- Implement optional integrations behind isolated adapters or compatibility modules.
- Detect mods by mod ID and validate required API/version assumptions before enabling an integration.
- Missing optional addons must not crash startup.
- Log concise diagnostics when an integration is disabled or a fluid is unsupported.
- Do not hard-link to client classes from common/server code.

### 8.2 Item, fluid, and recipe conventions

- Use namespaced registry IDs owned by this mod.
- Use Forge tags and capabilities appropriate to each Minecraft version.
- Register custom fluids only where necessary; prefer interoperating with existing fluids when balance and semantics permit.
- Do not duplicate existing fluids under a new name solely to bypass compatibility.
- Use tags for fuel families only where semantics are truly interchangeable; preserve special-case behavior through explicit properties.
- Test fluid insertion/extraction from Create pipes/tanks and Immersive Engineering equipment where installed.
- Verify recipe unification and item equivalence in both packs.

### 8.3 Multiplayer and dedicated server

- All gameplay-critical state is server authoritative: fuel, reload, heat, damage, targeting, ignition, and turret operation.
- Synchronize only the state needed for client visuals/UI.
- Validate packet inputs and rate-limit actions.
- Test dedicated server startup and client/server parity for each target pack.
- Do not assume single-player success proves multiplayer correctness.

---

## 9. Performance requirements and profiling plan

Performance must be measured, not described only as an intention.

### 9.1 Runtime constraints

- No unbounded per-tick loops over all loaded entities or blocks.
- No per-particle world queries.
- No permanent ticking block entity when an event-driven or lower-frequency update is sufficient.
- Use a capped particle budget and distance-based visual LOD.
- Reduce or disable cosmetic effects under low particle settings and when entities are far from the player.
- Avoid excessive sound instances; sustain one managed loop per active weapon/turret and stop it deterministically.
- Batch or minimize network updates; do not send particle positions individually when a compact firing-state packet is sufficient.
- Ensure temporary fire and transient effects are cleaned up even if the weapon is unloaded, removed, or the server shuts down.

### 9.2 Required test scenarios

1. Idle weapon held in inventory.
2. Continuous firing for a full tank.
3. Multiple flamethrowers firing simultaneously.
4. Several turrets active in one loaded area.
5. Dense zombie/entity crowd.
6. High particle settings and reduced particle settings.
7. Chunk border crossing and chunk unload/reload.
8. Multiplayer with latency.
9. Dedicated server under sustained operation.
10. Low-end client profile representative of integrated graphics.

Record baseline and mod-enabled results: average FPS, 1% low FPS where available, frame-time spikes, client and server tick time, memory allocation/GC behavior, entity count, particle count, and network traffic. Compare the same world, location, view distance, and test sequence.

### 9.3 Acceptance criteria

- No reproducible crash, deadlock, or runaway memory growth in the required scenarios.
- No unbounded growth in particles, sounds, temporary blocks, entities, or scheduled tasks.
- Weapon and turret effects degrade gracefully under constrained settings.
- Performance regressions must be measured and justified against the visual/gameplay benefit. Do not accept a major regression merely because the effects look impressive.
- Establish numeric budgets after a baseline is measured on the target hardware and pack; do not invent FPS guarantees before profiling.

---

## 10. Configuration requirements

Expose configuration for at least:

- Weapon range tier values (defaults 15/25/35 blocks).
- Tank capacity (default 50 units).
- Fuel consumption (default 4 units/second; 12.5 seconds per full tank).
- Reload duration (default 1.5 seconds).
- Target burn duration (default 3 seconds).
- Heat gain per consecutive hit (default 10%).
- Heat cap and decay/reset timing (current target 2x and 2.5 seconds; exact interpretation to be finalized).
- Temporary fire duration, spread limits, and allowed block/entity interactions.
- Turret range, target filters, pilot burner, and operation requirements.
- Particle/effect quality and distance LOD.
- Optional compatibility toggles for integrations that may be disabled by server owners.

Configuration must be validated and clamped. Invalid values must not crash the game or permit extreme ranges, damage, or particle counts.

---

## 11. Security, grief prevention, and server administration

- Never trust client-reported hits, fuel amounts, reload completion, turret target selection, or ignition results.
- Apply server-side cooldowns and action validation.
- Respect server configuration and protection APIs.
- Temporary fire must not bypass claims or protected-region rules.
- Provide server-side configuration to disable block ignition and/or player damage independently.
- Avoid persistent world changes by default. If a future feature adds persistent burning or environmental damage, it requires a separate opt-in requirement and explicit admin controls.
- Provide clear logs for configuration errors and compatibility failures without flooding logs during normal operation.

---

## 12. Testing and release gates

A build is not ready to publish for a target pack until all applicable gates pass.

### Gate A — Inventory and environment

- [ ] Exact official pack archive downloaded.
- [ ] Manifest extracted.
- [ ] Installed mod JARs enumerated and reconciled with manifest/overrides.
- [ ] Separate complete inventory generated for this target.
- [ ] Minecraft, Forge, Java, and dependency versions pinned.
- [ ] Pack configs, scripts, tags, and recipe overrides inspected.

### Gate B — Functional behavior

- [ ] Continuous firing and release behavior correct.
- [ ] Fuel consumption and empty-tank behavior correct.
- [ ] Reload by R and sneak-right-click correct.
- [ ] Range tiers validated.
- [ ] Heat accumulation and reset behavior validated.
- [ ] Burn duration validated.
- [ ] Temporary fire cleanup and protection behavior validated.
- [ ] Underwater operation disabled.
- [ ] Damage immunity, armor, PvP, Adventure, spawn, and claims rules respected.

### Gate C — Integrations

- [ ] Create fluid transport/storage tested where installed.
- [ ] Immersive Engineering fluids tested where installed.
- [ ] Chemthrower presence and interaction researched; no assumptions based on a different pack release.
- [ ] Create: Diesel Generators integration tested where installed.
- [ ] Recipe unification and pack scripts tested after load.
- [ ] Optional addons absent/present cases tested.
- [ ] Turret rotational, fluid, and electrical interfaces tested.

### Gate D — Performance and multiplayer

- [ ] Required profiling scenarios completed.
- [ ] Particle and audio budgets validated.
- [ ] Dedicated server tested.
- [ ] Multiplayer synchronization and packet validation tested.
- [ ] Chunk unload/reload cleanup tested.

### Gate E — Packaging and documentation

- [ ] Separate artifact built for each Minecraft/Forge target.
- [ ] Dependencies and optional integrations documented.
- [ ] Config defaults and server-admin controls documented.
- [ ] Known incompatibilities and limitations documented.
- [ ] Tested against the exact named DeceasedCraft release.

---

## 13. AI-agent research and development workflow

The coding agent (planned workflow: Google Antigravity) must follow this sequence. NotebookLM may be used as a research workspace, but primary sources and repository files remain authoritative.

1. **Establish exact target artifacts.** Download official DeceasedCraft v5.5.5 and latest public v6-development beta archives. Record URLs, file IDs, hashes, and dates.
2. **Extract inventories separately.** Parse `manifest.json`; resolve every file reference; inspect overrides and actual installed JARs. Produce the two CSV inventories described in Section 7.
3. **Inspect source and documentation.** Prioritize official mod documentation, source repositories, API docs, changelogs, and the exact installed JAR metadata. Do not rely on generic tutorials for version-specific behavior.
4. **Build an integration map.** For each relevant mod/addon, record mod ID, version, API/capability, fluid IDs, recipe hooks, damage behavior, and known compatibility constraints.
5. **Compare pack configurations.** Inspect KubeJS/CraftTweaker/datapacks/configs/tags/loot/progression files that may alter recipes, item equivalence, fuel availability, or protection rules.
6. **Design the architecture before coding.** Separate common gameplay logic, version-specific platform code, client rendering, and optional compatibility adapters.
7. **Prototype vertical slices.** First prove one handheld firing loop, fuel transfer, damage/protection behavior, and one turret connection path before expanding content.
8. **Profile early.** Capture a baseline before high-fidelity VFX are implemented. Add visual features incrementally and profile after each major layer.
9. **Run the full acceptance gates.** Test each target independently on the exact modpack release.
10. **Maintain evidence.** Every compatibility claim must point to a source, test log, manifest entry, or code/API inspection. Mark unknowns as unknown.

### Required research artifacts

- `compatibility/inventory/deceasedcraft-5.5.5-1.18.2.csv`
- `compatibility/inventory/deceasedcraft-beta-5.10.17-1.20.1.csv`
- `compatibility/ECOSYSTEM_MATRIX.md`
- `compatibility/RECIPE_AND_FLUID_AUDIT.md`
- `compatibility/COMBAT_AND_PROTECTION_AUDIT.md`
- `compatibility/TEST_RESULTS.md`
- `PERFORMANCE_BUDGET.md`

---

## 14. Open decisions and unresolved questions

These are not to be guessed by the implementation agent.

1. Exact meaning of the heat mechanic's **2x / 2.5-second** notation: confirm whether 2.5 seconds is the combo reset window, decay duration, or maximum heat hold.
2. Exact damage values and split between ordinary fire damage and point-blank lava-like damage.
3. Whether the 15/25/35-block range tiers correspond to three weapon tiers, upgrade modules, or configurable variants.
4. Cartridge item design, crafting recipes, refill process, and progression costs.
5. Exact list of accepted fuels and their relative efficiencies.
6. Electrical power system for the turret, based on actual installed mods in each target pack.
7. Exact turret face/side mapping and rotation control behavior.
8. Exact archive-to-workbook reconciliation and inspection of pack configs, scripts, recipes, tags, and runtime behavior. This is a mandatory research gate.
9. Whether the final public v6.0 release has superseded Beta 5.10.17 by the time implementation begins.
10. Numeric performance budgets after baseline profiling on representative hardware.

---

## 15. Source references and research notes

Primary public references checked on 2026-11-24:

- User-supplied research workbook: `DeceasedCraft_Mod_Research.xlsx` (three sheets; full inventories and cross-version comparison reproduced in §16).

- Official DeceasedCraft CurseForge project page: https://www.curseforge.com/minecraft/modpacks/deceasedcraft
  - Identifies the project, Forge loader, v5.5.5 for 1.18.2, Beta 5.10.17 for 1.20.1, and describes 5.10+ as the open beta for v6.0. It warns that the beta is incomplete and cannot be completed and that beta compatibility with final v6.0 is not guaranteed.
- Official DeceasedCraft files page: https://www.curseforge.com/minecraft/modpacks/deceasedcraft/files/all
  - Lists Beta 5.10.17 (1.20.1, uploaded 2026-07-17) and v5.5.5 (1.18.2, uploaded 2024-07-12) as the relevant public files.
- Official v5.5.5 file page: https://www.curseforge.com/minecraft/modpacks/deceasedcraft/files/5525524
  - Confirms v5.5.5, file ID 5525524, 1.18.2, Forge, and its 2024-07-12 upload.

Prior project decisions consolidated from planning discussions:

- Handheld weapon: continuous right-click stream; 15/25/35-block configurable range targets; fire plus point-blank lava-like damage; +10% consecutive-hit heat; 2x / 2.5-second tuning notation; 3-second burn; temporary ground fire; 50-unit tank; 12.5-second continuous runtime; R or sneak-right-click reload in 1.5 seconds; animated model and layered VFX/audio; no underwater use; respect immunity, armor, protection, spawn/PvP/Adventure rules.
- Technology ecosystem: Create and Create: Diesel Generators are the intended integration direction; do not use Create: Petrochem as the core plan. Multiple fuels should interoperate with other-mod fluids, especially Immersive Engineering.
- Turret: Create pipe/fluid supply, Create rotation, electricity, GUI range/filters/pilot burner; exact connection-face mapping remains provisional.

---



---

## 16. DeceasedCraft compatibility inventories (source-backed baseline)

**Purpose:** This section is the mod-by-mod compatibility reference for the coding agent. The two release inventories are intentionally separate. Never merge them into one generic "DeceasedCraft mod list," and never assume that a mod, addon, API, registry name, recipe, or behavior is identical across the two Minecraft versions.

**Primary inventory source:** User-supplied workbook `DeceasedCraft_Mod_Research.xlsx`, sheets:
- `v5.5.5 (MC 1.18.2)`
- `Beta 5.10.17 (MC 1.20.1)`
- `Comparison & Mod-Dev Summary`

**Inventory scope and provenance**
- v5.5.5: 224 catalog entries; Minecraft 1.18.2; Forge 40.2.4; CurseForge file ID 5525524; uploaded 2024-07-12.
- Beta 5.10.17: 306 Standard entries plus 1 Distant Horizons edition extra, 307 total; Minecraft 1.20.1; Forge 47.4.0; Standard file ID 8448820 and DH Edition file ID 8448903; uploaded 2026-07-17.
- The workbook's catalog is the authoritative project baseline supplied for this specification. Its "Supported in MC 1.20.1" and "In Both Packs?" fields are research annotations, not proof that this project has passed runtime integration tests.
- The listed file names are the recorded mod file/version identifiers. They are not substitutes for inspecting the actual modpack archives, dependency metadata, configs, KubeJS scripts, datapacks, or runtime registries.
- Resource packs and shader packs are excluded from the two mod inventories and listed separately in §16.4.
- The workbook identifies Beta 5.10.17 as the latest public v6 open beta at the time of its research. It is not a guarantee of compatibility with a later v6.0 release.

### 16.1 DeceasedCraft v5.5.5 — Stable release (Minecraft 1.18.2 / Forge 40.2.4)

**224 catalog entries**

The following list is specific to v5.5.5. Preserve its recorded categories, file identifiers, descriptions, and research annotations.

|Mod|Category|1.20.1 Forge support (workbook)|In both packs?|Recorded file / version|Description / notes|Source|
|---|---|---|---|---|---|---|
|[ETF] Entity Texture Features - [Fabric & Forge]|Audio, Visuals & Immersion|Yes|Yes|entity_texture_features_forge_1.18.2-4.6.1.jar|Custom, Emissive and Varied mobs like Optifine and so much more.. +Player skin features!)|[Source](https://www.curseforge.com/minecraft/mc-mods/entity-texture-features-fabric)|
|Camera Mod|Audio, Visuals & Immersion|Yes|No|camera-1.18.2-1.0.5.jar|A working Camera in Minecraft! \| Note: Supports 1.20.1 Forge, but v6 uses Exposure for cameras.|[Source](https://www.curseforge.com/minecraft/mc-mods/camera-mod)|
|CleanView|Audio, Visuals & Immersion|Yes|Yes|CleanView-1.18.2-v1.jar|CleanView is a minecraft client mod that removes potion particles from your viewpoint|[Source](https://www.curseforge.com/minecraft/mc-mods/cleanview)|
|CraftPresence|Audio, Visuals & Immersion|Yes|Yes|CraftPresence-2.2.3+1.18.2.jar|Completely Customize the way others see you play in Discord!|[Source](https://www.curseforge.com/minecraft/mc-mods/craftpresence)|
|Effective (Forge)|Audio, Visuals & Immersion|No|No|effective_fg-1.2.4.jar|Effective, client sided mod that adds various visual and auditory effects to improve overall ambience \| Note: Stopped at 1.19.2; replaced by Particular Reforged & Pretty Rain in v6.|[Source](https://www.curseforge.com/minecraft/mc-mods/effective-forge)|
|Embeddium (Rubidium) Extra|Audio, Visuals & Immersion|Yes|No|rubidium-extra-0.4.18+mc1.18.2-build.86.jar|Port of Sodium Extra to work with Embeddium/Rubidium on (Neo)Forge \| Note: Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Extras.|[Source](https://www.curseforge.com/minecraft/mc-mods/rubidium-extra)|
|Emojiful|Audio, Visuals & Immersion|Yes|No|emojiful-1.18.2-3.0.1.jar|Emojis in minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/emojiful)|
|EnhancedVisuals|Audio, Visuals & Immersion|Yes|No|EnhancedVisuals_FORGE_v1.6.4_mc1.18.2.jar|Feel the pain!|[Source](https://www.curseforge.com/minecraft/mc-mods/enhancedvisuals)|
|Lucent|Audio, Visuals & Immersion|Yes|No|lucent-1.18.2-1.2.2.jar|A client-side dynamic lighting mod and API \| Note: Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Dynamic Lights.|[Source](https://www.curseforge.com/minecraft/mc-mods/lucent)|
|Not Enough Animations|Audio, Visuals & Immersion|Yes|No|notenoughanimations-forge-1.7.0-mc1.18.2.jar|Bringing first-person animations to the third-person|[Source](https://www.curseforge.com/minecraft/mc-mods/not-enough-animations)|
|Physics Mod|Audio, Visuals & Immersion|Yes|No|physics-mod-2.12.5-mc-1.18.2-forge.jar|Adds physics to Mobs and Blocks!|[Source](https://www.curseforge.com/minecraft/mc-mods/physics-mod)|
|Presence Footsteps (Forge)|Audio, Visuals & Immersion|Yes|Yes|PresenceFootsteps-1.18.2-1.5.1-forge.jar|An unofficial port of Presence Footsteps from Fabric to Forge|[Source](https://www.curseforge.com/minecraft/mc-mods/presence-footsteps-forge)|
|Shoulder Surfing Reloaded|Audio, Visuals & Immersion|Yes|Yes|ShoulderSurfing-Forge-1.18.2-2.8.1.jar|Shoulder Surfing Reloaded is a highly configurable third person camera mod for Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/shoulder-surfing-reloaded)|
|Sound Physics Remastered|Audio, Visuals & Immersion|Yes|Yes|soundphysics-forge-1.18.2-1.0.6.jar|A Minecraft mod that provides realistic sound attenuation, reverberation, and absorption through blocks.|[Source](https://www.curseforge.com/minecraft/mc-mods/sound-physics-remastered)|
|TexTrue's Embeddium Options|Audio, Visuals & Immersion|Yes|No|textrues_embeddium_options-0.1.1+mc1.18.2.jar|Unofficial port of Reese's Sodium Options to work with Embeddium on MinecraftForge/NeoForge. \| Note: Supports 1.20.1 Forge, but v6 uses Sodium/Embeddium Options API.|[Source](https://www.curseforge.com/minecraft/mc-mods/textrues-embeddium-options)|
|What Are They Up To (Watut)|Audio, Visuals & Immersion|Yes|Yes|watut-forge-1.18.2-1.0.14.jar|Lets you see if players are typing, in a GUI, idle, with cool ingame visuals|[Source](https://www.curseforge.com/minecraft/mc-mods/what-are-they-up-to)|
|AttributeFix|Bug Fixes & Stability|Yes|Yes|AttributeFix-Forge-1.18.2-14.0.2.jar|Removes arbitrary limits on Minecraft's attribute system.|[Source](https://www.curseforge.com/minecraft/mc-mods/attributefix)|
|Bee Fix|Bug Fixes & Stability|Yes|Yes|BeeFix-1.18-1.0.7.jar|Fixes Bee Related Bugs|[Source](https://www.curseforge.com/minecraft/mc-mods/bee-fix)|
|Better Biome Blend|Bug Fixes & Stability|Yes|No|betterbiomeblend-1.18.2-1.3.5-forge.jar|Improves and fixes biome color blending \| Note: Supports 1.20.1 Forge, but v6 uses Better Biome Reblend.|[Source](https://www.curseforge.com/minecraft/mc-mods/better-biome-blend)|
|Connectivity|Bug Fixes & Stability|Yes|Yes|connectivity-1.18.2-3.2.jar|Fix Login timeouts, Packet sizes errors, Payloads errors, ghostblocks and more.|[Source](https://www.curseforge.com/minecraft/mc-mods/connectivity)|
|DCFixes|Bug Fixes & Stability|No|No|DeceasedCraftFixes-1.0.7+1.18.2.jar|Unofficial companion mod for DeceasedCraft to fix various issues \| Note: No public 1.20.1 Forge JAR (source-only 'DeceasedCraft v6 Fixes' branch exists on GitHub); v6 Beta 5.10.17 uses DeceasedCraft++ & DCTweaks.|[Source](https://www.curseforge.com/minecraft/mc-mods/dcfixes)|
|fix GPU memory leak|Bug Fixes & Stability|Yes|No|gpumemleakfix-1.18.2-1.6.jar|A mod that fixes memory leaks on the client \| Note: Supports 1.20.1 Forge, but v6 uses GPUTape & AllTheLeaks.|[Source](https://www.curseforge.com/minecraft/mc-mods/fix-gpu-memory-leak)|
|Iris/Oculus & GeckoLib Compat (Deprecated)|Bug Fixes & Stability|Yes|No|GeckoLibOculusCompat-Forge-1.0.1.jar|ONLY WORKS FOR OLDER VERSIONS - Fixes GeckoLib animations not working if using a shaderpack with entity shadows.|[Source](https://www.curseforge.com/minecraft/mc-mods/geckoanimfix)|
|Max Health Fix|Bug Fixes & Stability|Yes|Yes|MaxHealthFix-Forge-1.18.2-5.0.4.jar|Fixes a bug with max health in Minecraft.|[Source](https://www.curseforge.com/minecraft/mc-mods/max-health-fix)|
|NaN Health Fixer|Bug Fixes & Stability|Yes|No|nanhealthfixer-1.18.2-0.0.1.jar|Try to kill an entity with NaN health. \| Note: Supports 1.20.1 Forge, but v6 uses NaNny Reforked.|[Source](https://www.curseforge.com/minecraft/mc-mods/nan-health-fixer)|
|Oculus Particle Fix|Bug Fixes & Stability|Yes|No|oculusparticlefix-1.0.jar|Fixes a visual glitch with the Oculus shader mod where particles are blinking through walls while picking up items|[Source](https://www.curseforge.com/minecraft/mc-mods/oculus-particle-fix)|
|Shutup Experimental Settings!|Bug Fixes & Stability|No|No|shutupexperimentalsettings-1.0.4-1.18+.jar|Removes the Experimental Settings prompt before world creation. \| Note: Stopped at 1.19.2; replaced by Yeetus Experimentus in v6.|[Source](https://www.curseforge.com/minecraft/mc-mods/shutup-experimental-settings)|
|Too Fast|Bug Fixes & Stability|Yes|Yes|toofast-1.18-0.0.1.3.jar|Fixes "moved too quickly".|[Source](https://www.curseforge.com/minecraft/mc-mods/too-fast)|
|Another Furniture|Building, Furniture & Decor|Yes|Yes|another_furniture-forge-1.2.2-1.18.2.jar|Another Furniture is a vanilla-styled furniture mod aiming to keep things simple while adding cute decoration!|[Source](https://www.curseforge.com/minecraft/mc-mods/another-furniture)|
|Builder's Delight (Forge)|Building, Furniture & Decor|Yes|Yes|BuildersDelight-1.18.2-v.1.0.jar|Adds ~700 new blocks, decoration and a chisel.|[Source](https://www.curseforge.com/minecraft/mc-mods/builders-delight-forge)|
|Cosmetic Armor Reworked|Building, Furniture & Decor|Yes|Yes|CosmeticArmorReworked-1.18.2-v2a.jar|This mod allows you to wear two sets of armor, one for display, one for function.|[Source](https://www.curseforge.com/minecraft/mc-mods/cosmetic-armor-reworked)|
|Create Deco|Building, Furniture & Decor|Yes|Yes|createdeco-1.3.3-1.18.2.jar|Industrial decoration themed for the Create mod.|[Source](https://www.curseforge.com/minecraft/mc-mods/create-deco)|
|EmbellishCraft|Building, Furniture & Decor|Yes|Yes|embellishcraft-1.18.2-5.0.1.0.jar|A mod about decoration for MC 1.13 - 1.21.1|[Source](https://www.curseforge.com/minecraft/mc-mods/embellishcraft)|
|Immersive Posts|Building, Furniture & Decor|Yes|No|ImmersivePosts-1.18.2-4.3.0-3.jar|Extendable treated-wood, aluminium, steel posts and more for ImmersiveEngineering.|[Source](https://www.curseforge.com/minecraft/mc-mods/immersiveposts)|
|MrCrayfish's Furniture Mod (Legacy)|Building, Furniture & Decor|Yes|Yes|cfm-7.0.0-pre35-1.18.2.jar|Adds over 80 unique pieces of furniture into Minecraft!|[Source](https://www.curseforge.com/minecraft/mc-mods/mrcrayfish-furniture-mod)|
|Paladin's Furniture|Building, Furniture & Decor|Yes|No|paladin-furniture-mod-1.2.1-forge-mc1.18.2.jar|A Modern Furniture mod for Minecraft where things are functional!|[Source](https://www.curseforge.com/minecraft/mc-mods/paladins-furniture)|
|Quark|Building, Furniture & Decor|Yes|Yes|Quark-3.2-358.jar|A Quark is a very small thing. This mod is a collection of small things that improve the vanilla minecraft experience.|[Source](https://www.curseforge.com/minecraft/mc-mods/quark)|
|Simply Light|Building, Furniture & Decor|Yes|Yes|simplylight-1.18.2-1.4.5-build.43.jar|Simple light for a complicated world.|[Source](https://www.curseforge.com/minecraft/mc-mods/simply-light)|
|Architectury API|Core Libraries & APIs|Yes|Yes|architectury-4.11.93-forge.jar|An intermediary api aimed to ease developing multiplatform mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/architectury-api)|
|Atlas Lib|Core Libraries & APIs|Yes|Yes|Atlas-Lib-1.18.2-1.1.8.jar|A serialzation and math libary for minecraft mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/atlas-lib)|
|AutoRegLib|Core Libraries & APIs|No|No|AutoRegLib-1.7-53.jar|A library to ease menial tasks in mod development. \| Note: Replaced by Zeta in MC 1.20.1 (Quark library).|[Source](https://www.curseforge.com/minecraft/mc-mods/autoreglib)|
|Balm|Core Libraries & APIs|Yes|Yes|balm-3.2.1+0.jar|Abstraction Layer for Multi-Loader Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/balm)|
|Bookshelf|Core Libraries & APIs|Yes|Yes|Bookshelf-Forge-1.18.2-13.3.56.jar|An open source library for other mods!|[Source](https://www.curseforge.com/minecraft/mc-mods/bookshelf)|
|Citadel|Core Libraries & APIs|Yes|No|citadel-1.11.3-1.18.2.jar|A Lightweight Library|[Source](https://www.curseforge.com/minecraft/mc-mods/citadel)|
|Cloth Config API (Fabric/Forge/NeoForge)|Core Libraries & APIs|Yes|Yes|cloth-config-6.4.90-forge.jar|Config Screen API for Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/cloth-config)|
|Collective|Core Libraries & APIs|Yes|Yes|collective-1.18.2-6.53.jar|🎓 Collective is a shared library with common code for all of Serilum's mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/collective)|
|CoroUtil|Core Libraries & APIs|Yes|Yes|coroutil-forge-1.18.2-1.3.6.jar|Library Mod for Weather/Tropicraft/ZombieAwareness/etc|[Source](https://www.curseforge.com/minecraft/mc-mods/coroutil)|
|CreativeCore|Core Libraries & APIs|Yes|Yes|CreativeCore_FORGE_v2.6.15_mc1.18.2.jar|a core mod|[Source](https://www.curseforge.com/minecraft/mc-mods/creativecore)|
|Cupboard|Core Libraries & APIs|Yes|Yes|cupboard-1.18.2-1.5.jar|Cupboard provides code, frameworks, and utilities for minecraft mods|[Source](https://www.curseforge.com/minecraft/mc-mods/cupboard)|
|Curios API|Core Libraries & APIs|Yes|Yes|curios-forge-1.18.2-5.0.7.1.jar|A flexible and expandable accessory/equipment API for users and developers.|[Source](https://www.curseforge.com/minecraft/mc-mods/curios)|
|Custom Portal API [Forge]|Core Libraries & APIs|Yes|Yes|customportalapi-0.0.5-forge-1.18.2.jar|Make Custom Portals via API|[Source](https://www.curseforge.com/minecraft/mc-mods/custom-portal-api-forge)|
|ExpandAbility|Core Libraries & APIs|Yes|Yes|expandability-6.0.0.jar|Library mod that provides increased control over vanilla effects and abilities|[Source](https://www.curseforge.com/minecraft/mc-mods/expandability)|
|Framework|Core Libraries & APIs|Yes|Yes|framework-0.4.2-1.18.2.jar|A common library powering all of MrCrayfish's Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/framework)|
|FTB Library (NeoForge)|Core Libraries & APIs|Yes|Yes|ftb-library-forge-1802.3.9-build.167.jar|Common code for all GUI stuff in FTB Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge)|
|GeckoLib|Core Libraries & APIs|Yes|Yes|geckolib-forge-1.18-3.0.57.jar|A 3D animation library for entities, blocks, items, armor, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/geckolib)|
|Iceberg [Neo/Forge]|Core Libraries & APIs|Yes|Yes|Iceberg-1.18.2-forge-1.0.49.jar|A modding library that contains new events, helpers, and utilities to make modder's lives easier.|[Source](https://www.curseforge.com/minecraft/mc-mods/iceberg)|
|InsaneLib|Core Libraries & APIs|Yes|Yes|InsaneLib-1.5.3-mc1.18.2.jar|A set of common classes and utilities used by Insane's mods|[Source](https://www.curseforge.com/minecraft/mc-mods/insanelib)|
|Item Filters|Core Libraries & APIs|Yes|Yes|item-filters-forge-1802.2.8-build.47.jar|Item Filters is a library mod that is used by mods like FTB Quests. It adds several filter items that let you precisely select which items to match.|[Source](https://www.curseforge.com/minecraft/mc-mods/item-filters)|
|Kiwi 🥝 (Neo/Forge)|Core Libraries & APIs|Yes|No|Kiwi-1.18.2-forge-6.1.3.jar|Minecraft modding library|[Source](https://www.curseforge.com/minecraft/mc-mods/kiwi)|
|Konkrete|Core Libraries & APIs|Yes|Yes|konkrete_forge_1.6.1_MC_1.18-1.18.2.jar|Just another boring library mod.|[Source](https://www.curseforge.com/minecraft/mc-mods/konkrete)|
|Kotlin for Forge|Core Libraries & APIs|Yes|Yes|kotlinforforge-3.10.0-all.jar|Adds a Kotlin language loader and provides some optional utilities.|[Source](https://www.curseforge.com/minecraft/mc-mods/kotlin-for-forge)|
|Mapper Base|Core Libraries & APIs|Yes|Yes|mapperbase-1.18.2-4.0.1.0.jar|A mod that provides basic elements for all my other mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/mapper-base)|
|Moonlight Lib|Core Libraries & APIs|Yes|Yes|selene-1.18.2-1.17.9.jar|Forge and Fabric lightweight library with utilities such as custom Villagers AI, data driven trades, global datapack, custom Map Markers, First and third per...|[Source](https://www.curseforge.com/minecraft/mc-mods/selene)|
|Patchouli|Core Libraries & APIs|Yes|Yes|Patchouli-1.18.2-71.1.jar|Accessible, Data-Driven, Dependency-Free Documentation for Minecraft Modders and Pack Makers|[Source](https://www.curseforge.com/minecraft/mc-mods/patchouli)|
|Pehkui|Core Libraries & APIs|Yes|No|Pehkui-3.7.11+1.18.2-forge.jar|Allows resizing of most entities, shrinking their scale smaller or growing their size larger|[Source](https://www.curseforge.com/minecraft/mc-mods/pehkui)|
|Placebo|Core Libraries & APIs|Yes|Yes|Placebo-1.18.2-6.6.6.jar|A library mod|[Source](https://www.curseforge.com/minecraft/mc-mods/placebo)|
|playerAnimator|Core Libraries & APIs|Yes|Yes|player-animation-lib-forge-1.0.2+1.18.jar|player animation library|[Source](https://www.curseforge.com/minecraft/mc-mods/playeranimator)|
|Rhino|Core Libraries & APIs|Yes|Yes|rhino-forge-1802.2.1-build.255.jar|A fork of Mozilla's Rhino library, modified for use in mods|[Source](https://www.curseforge.com/minecraft/mc-mods/rhino)|
|Sophisticated Core|Core Libraries & APIs|Yes|Yes|sophisticatedcore-1.18.2-0.5.106.502.jar|Library mod for Sophisticated mods|[Source](https://www.curseforge.com/minecraft/mc-mods/sophisticated-core)|
|SuperMartijn642's Config Lib|Core Libraries & APIs|Yes|Yes|supermartijn642configlib-1.1.6-forge-mc1.18.jar|Config Lib makes dealing with config files just a bit easier.|[Source](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-config-lib)|
|SuperMartijn642's Core Lib|Core Libraries & APIs|Yes|Yes|supermartijn642corelib-1.1.12-forge-mc1.18.jar|SuperMartijn642's Core Lib adds lots of basic implementations that allow for similar code between different Minecraft versions!|[Source](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-core-lib)|
|TerraBlender (Forge)|Core Libraries & APIs|Yes|Yes|TerraBlender-forge-1.18.2-1.2.0.126.jar|A library mod for adding biomes in a simple and compatible manner!|[Source](https://www.curseforge.com/minecraft/mc-mods/terrablender)|
|YUNG's API (Forge/NeoForge)|Core Libraries & APIs|Yes|Yes|YungsApi-1.18.2-Forge-2.2.9.jar|A library mod for YUNG's Minecraft mods|[Source](https://www.curseforge.com/minecraft/mc-mods/yungs-api)|
|Apocalypse Now - Post Apocalyptic Arsenal|Firearms, Weapons & Combat|Yes|Yes|Apocalyspe_Now_1.18.2_v2.0.7.jar|Apocalypse Now is a mod totally focused on an apocalyptic world that was taken over by creatures that only live to attack and eat anything alive in the world...|[Source](https://www.curseforge.com/minecraft/mc-mods/apocalypse-now)|
|Armor Set Bonuses (NeoForge /Forge)|Firearms, Weapons & Combat|Yes|Yes|spacecatasb-forge-18.13.1.jar|Adds bonuses for armor sets, and is fully customizable|[Source](https://www.curseforge.com/minecraft/mc-mods/armor-set-bonuses)|
|Artifacts|Firearms, Weapons & Combat|Yes|Yes|artifacts-1.18.2-4.2.0.jar|Adds various treasure items that can be found through exploration|[Source](https://www.curseforge.com/minecraft/mc-mods/artifacts)|
|Better Combat [Fabric & Forge]|Firearms, Weapons & Combat|Yes|Yes|bettercombat-forge-1.6.2+1.18.2.jar|⚔️ Easy, spectacular and fun melee combat system from Minecraft Dungeons.|[Source](https://www.curseforge.com/minecraft/mc-mods/better-combat-by-daedelus)|
|Create Big Cannons|Firearms, Weapons & Combat|Yes|Yes|createbigcannons-forge-1.18.2-0.5.3.b.jar|Artillery engineering comes to Create|[Source](https://www.curseforge.com/minecraft/mc-mods/create-big-cannons)|
|Crossbowverhaul|Firearms, Weapons & Combat|Yes|No|crossbowverhaul-1.18.2-1.4.1-universal.jar|move over vanilla, the original modded crossbow is back!|[Source](https://www.curseforge.com/minecraft/mc-mods/crossbowverhaul)|
|MmmMmmMmmMmm (Target Dummy)|Firearms, Weapons & Combat|Yes|Yes|MmmMmmMmmMmm-1.18.2-1.5.2.jar|Target Dummy that show damage dealt and can be equipped with armor. Damage numbers!|[Source](https://www.curseforge.com/minecraft/mc-mods/mmmmmmmmmmmm)|
|MrCrayfish's Gun Mod|Firearms, Weapons & Combat|No|No|cgm-1.3.3-1.18.2.jar|A new and exciting weapon mod with attachments and enchantments! \| Note: Official mod stopped at 1.19.4; v6 uses MrCrayfish's Gun Mod [Unofficial] & TaCZ.|[Source](https://www.curseforge.com/minecraft/mc-mods/mrcrayfishs-gun-mod)|
|Nameless Trinkets|Firearms, Weapons & Combat|Yes|Yes|Nameless Trinkets-1.18.2-1.7.5.jar|Add powerful trinkets, which you will find when exploring the world.|[Source](https://www.curseforge.com/minecraft/mc-mods/nameless-trinkets)|
|ParCool! ~ Minecraft Parkour ~|Firearms, Weapons & Combat|Yes|Yes|ParCool-1.18.2-3.1.0.6-R.jar|A Mod which add Cool actions and facilities for Parkour|[Source](https://www.curseforge.com/minecraft/mc-mods/parcool)|
|SwingThroughGrass|Firearms, Weapons & Combat|No|No|swingthroughgrass-1.18.2-1.9.1.jar|Kill mobs and players through grass \| Note: Original project skipped 1.20.1 (1.19.2 -> 1.20.6); separate 1.20.1 Forge rewrite 'Swing Through Grass' exists.|[Source](https://www.curseforge.com/minecraft/mc-mods/swingthroughgrass)|
|Third Person Shooting: Zero|Firearms, Weapons & Combat|Yes|Yes|tp_shooting-1.18.2-2.2.7.jar|Make TAC Guns Compatible with Shoulder Surfing|[Source](https://www.curseforge.com/minecraft/mc-mods/third-person-shooting)|
|Timeless and Classics Guns|Firearms, Weapons & Combat|No|No|tac-0.3.10.1-1.18.2.jar|A modern gun mod with a huge selection of weapons of well built and modeled firearms, full customizability, addon support, and a whole lot more! \| Note: Stopped at 1.18.2; replaced by full remaster [TaCZ] Timeless and Classics Zero Guns in v6.|[Source](https://www.curseforge.com/minecraft/mc-mods/timeless-and-classic-guns-tac)|
|Create: Central Kitchen|Food, Farming & Cooking|Yes|Yes|create_central_kitchen-1.18.2-for-create-0.5.1.f-1.3.9.d.jar|Automatic Kitchen Work & Integration|[Source](https://www.curseforge.com/minecraft/mc-mods/create-central-kitchen)|
|Diet (Fabric/Forge/Quilt)|Food, Farming & Cooking|Yes|Yes|diet-forge-1.18.2-1.3.2.1.jar|A customizable food group-based nutrition and diet system.|[Source](https://www.curseforge.com/minecraft/mc-mods/diet)|
|Dietary Statistics|Food, Farming & Cooking|No|No|DietaryStatistics 1.0.2.jar|Adds a new attribute called Food Max, which will allow you to eat more... \| Note: Discontinued after 1.19.4 (Diet itself remains in v6).|[Source](https://www.curseforge.com/minecraft/mc-mods/dietary-statistics)|
|Easy Villagers|Food, Farming & Cooking|Yes|No|easy_villagers-1.18.2-1.0.11.jar|Never get annoyed by villagers again!|[Source](https://www.curseforge.com/minecraft/mc-mods/easy-villagers)|
|Farmer's Delight|Food, Farming & Cooking|Yes|Yes|FarmersDelight-1.18.2-1.2.3.jar|A cozy expansion to farming and cooking!|[Source](https://www.curseforge.com/minecraft/mc-mods/farmers-delight)|
|Fast Leaf Decay|Food, Farming & Cooking|Yes|Yes|FastLeafDecay-28.jar|Makes leaves decay faster when a tree is cut down.|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-leaf-decay)|
|Harvest with ease|Food, Farming & Cooking|Yes|Yes|harvestwithease-1.18.2-6.1.0.0-forge.jar|Don't break crops, right click them!|[Source](https://www.curseforge.com/minecraft/mc-mods/harvest-with-ease)|
|Spice of Life: Carrot Edition|Food, Farming & Cooking|Yes|Yes|SoL-Carrot-1.18.1-1.12.0.jar|A mod based around food that rewards the player instead of punishing them for discovering new foods!|[Source](https://www.curseforge.com/minecraft/mc-mods/spice-of-life-carrot-edition)|
|Tree Harvester|Food, Farming & Cooking|Yes|Yes|treeharvester-1.18.2-8.1.jar|🌲 Harvest full trees and huge mushrooms instantly with an axe. Includes fast leaf decay and sapling placement. Also works for warped (nether) trees. Become a...|[Source](https://www.curseforge.com/minecraft/mc-mods/tree-harvester)|
|ContentTweaker|Modpack Scripting & Control|No|No|ContentTweaker-forge-1.18.2-1.0.0+13.jar|Allows you to add Items and Blocks \| Note: Stopped at 1.19.2; v6 uses KubeJS for custom content instead of CraftTweaker/ContentTweaker.|[Source](https://www.curseforge.com/minecraft/mc-mods/contenttweaker)|
|CraftTweaker|Modpack Scripting & Control|Yes|No|CraftTweaker-forge-1.18.2-9.1.211.jar|CraftTweaker allows modpacks and servers to customize the game. With CraftTweaker you can change recipes, script events, add new commands and even change ite... \| Note: Has 1.20.1 Forge support, but v6 migrated pack scripting to KubeJS.|[Source](https://www.curseforge.com/minecraft/mc-mods/crafttweaker)|
|CreateTweaker|Modpack Scripting & Control|Yes|No|CreateTweaker-1.18.2-2.0.0.20.jar|Adds CraftTweaker support for Create \| Note: Has 1.20.1 Forge support, but v6 uses KubeJS Create instead.|[Source](https://www.curseforge.com/minecraft/mc-mods/createtweaker)|
|Default Options|Modpack Scripting & Control|Yes|Yes|defaultoptions-forge-1.18.2-14.1.2.jar|Ship default options or keybinds without having to overwrite an existing options.txt.|[Source](https://www.curseforge.com/minecraft/mc-mods/default-options)|
|Default Server Properties|Modpack Scripting & Control|Yes|Yes|default-server-properties-1.0.1-build.10+mc1.18.2.jar|Allows modpack developers to define default server properties. Typically used for things like a default level type.|[Source](https://www.curseforge.com/minecraft/mc-mods/default-server-properties)|
|Fx Control!|Modpack Scripting & Control|No|No|fxcontrol-1.18-3.0.9.jar|Control Player Effects under various conditions \| Note: Merged into In Control! starting in MC 1.20.1+.|[Source](https://www.curseforge.com/minecraft/mc-mods/fx-control)|
|Global GameRules|Modpack Scripting & Control|Yes|Yes|GlobalGameRules-1.18.1-6.0.0.5.jar|A mod that allows for global/default gamerules|[Source](https://www.curseforge.com/minecraft/mc-mods/global-gamerules)|
|In Control!|Modpack Scripting & Control|Yes|Yes|incontrol-1.18-6.1.13.jar|Be In Control of mob spawns|[Source](https://www.curseforge.com/minecraft/mc-mods/in-control)|
|KubeJS|Modpack Scripting & Control|Yes|Yes|kubejs-forge-1802.5.5-build.567.jar|Edit recipes, add new custom items, script world events, all in JavaScript!|[Source](https://www.curseforge.com/minecraft/mc-mods/kubejs)|
|KubeJS Offline Documentation|Modpack Scripting & Control|Yes|No|kubejsoffline-1.1.7.jar|KubeJS Documentation files, generated dynamically via command, accessed with an html page.|[Source](https://www.curseforge.com/minecraft/mc-mods/kubejs-offline)|
|Carry On|Multiplayer, Utility & Admin|Yes|Yes|carryon-1.18.2-1.17.0.8.jar|Carry On allows you to pick up Tile Entities and Mobs and carry them around!|[Source](https://www.curseforge.com/minecraft/mc-mods/carry-on)|
|Chalk|Multiplayer, Utility & Admin|Yes|Yes|chalk-1.18.2-1.4.2.jar|Leave the mark!|[Source](https://www.curseforge.com/minecraft/mc-mods/chalk)|
|Chunky (Forge/NeoForge)|Multiplayer, Utility & Admin|Yes|Yes|Chunky-1.2.164.jar|Pre-generates chunks, quickly, efficiently, and safely|[Source](https://www.curseforge.com/minecraft/mc-mods/chunky-pregenerator-forge)|
|Client Crafting|Multiplayer, Utility & Admin|Yes|Yes|clientcrafting-1.18.2-1.6.jar|Clientside crafting without network delay|[Source](https://www.curseforge.com/minecraft/mc-mods/client-crafting)|
|DRG Flares (Forge)|Multiplayer, Utility & Admin|Yes|No|drg_flares-1.18-forge-1.2.2.jar|Adds Flares from Deep Rock Galactic (Forge Version)|[Source](https://www.curseforge.com/minecraft/mc-mods/drg-flares-forge)|
|Fast IP Ping|Multiplayer, Utility & Admin|Yes|No|fast-ip-ping-mc1.18.2-forge-v1.0.0.jar|Yeet the laggy reversed DNS lookup for literal IP server addresses|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-ip-ping)|
|Get It Together, Drops!|Multiplayer, Utility & Admin|Yes|Yes|getittogetherdrops-forge-1.18.2-1.3.jar|Adds tags and configuration options for defining how dropped items should combine.|[Source](https://www.curseforge.com/minecraft/mc-mods/get-it-together-drops)|
|Log Begone|Multiplayer, Utility & Admin|Yes|Yes|Log-Begone-Forge-1.18-1.0.4.jar|Fork of Shut Up Console - Tell those those annoy logs lines begone!|[Source](https://www.curseforge.com/minecraft/mc-mods/log-begone)|
|Mouse Tweaks|Multiplayer, Utility & Admin|Yes|Yes|MouseTweaks-forge-mc1.18-2.21.jar|Enhances inventory management by adding various functions to the mouse buttons.|[Source](https://www.curseforge.com/minecraft/mc-mods/mouse-tweaks)|
|No Villager Death Messages|Multiplayer, Utility & Admin|Yes|No|novillagerdm-1.18.1-3.0.0.jar|Removes the console spam from villager deaths|[Source](https://www.curseforge.com/minecraft/mc-mods/no-villager-death-messages)|
|Open Parties and Claims|Multiplayer, Utility & Admin|Yes|Yes|open-parties-and-claims-forge-1.18.2-0.20.1.jar|Adds the ability to claim chunks and make player parties, integrates with Xaero's Minimap and World Map|[Source](https://www.curseforge.com/minecraft/mc-mods/open-parties-and-claims)|
|Polymorph|Multiplayer, Utility & Admin|Yes|Yes|polymorph-forge-1.18.2-0.46.jar|No more recipe conflicts! Adds an option to choose the crafting result if more than one is available.|[Source](https://www.curseforge.com/minecraft/mc-mods/polymorph)|
|Simple Backups|Multiplayer, Utility & Admin|Yes|No|SimpleBackups-1.18.2-1.1.9.jar|A simple mod to create scheduled backups.|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-backups)|
|Simple Voice Chat|Multiplayer, Utility & Admin|Yes|Yes|voicechat-forge-1.18.2-2.4.28.jar|A working voice chat in Minecraft!|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-voice-chat)|
|spark|Multiplayer, Utility & Admin|Yes|Yes|spark-1.10.38-forge.jar|spark is a performance profiler for Minecraft clients, servers and proxies.|[Source](https://www.curseforge.com/minecraft/mc-mods/spark)|
|StackablePotions [Forge]|Multiplayer, Utility & Admin|Yes|Yes|StackablePotions-forge-1.18.2-1.0.0.jar|Allows vanilla potions to stack.|[Source](https://www.curseforge.com/minecraft/mc-mods/stackablepotions-forge)|
|AI Improvements: Performance Tuning|Performance & Optimization|Yes|Yes|AI-Improvements-1.18.2-0.5.2.jar|Performance and logic upgrades for mod AIs|[Source](https://www.curseforge.com/minecraft/mc-mods/ai-improvements)|
|Alternate Current|Performance & Optimization|Yes|Yes|alternate-current-mc1.18-1.2.1.jar|An efficient and non-locational redstone dust implementation|[Source](https://www.curseforge.com/minecraft/mc-mods/alternate-current)|
|Canary|Performance & Optimization|Yes|No|canary-mc1.18.2-0.3.3.jar|A performance mod designed to optimize Minecraft's general performance and unofficial fork of Lithium mod for Minecraft Forge. \| Note: Supports 1.20.1 Forge, but v6 uses Radium Reforged (Lithium fork) instead.|[Source](https://www.curseforge.com/minecraft/mc-mods/canary)|
|Clumps|Performance & Optimization|Yes|Yes|Clumps-forge-1.18.2-8.0.0+17.jar|Clumps XP orbs together to reduce lag|[Source](https://www.curseforge.com/minecraft/mc-mods/clumps)|
|CullLessLeaves Reforged (Unofficial)|Performance & Optimization|Yes|Yes|CullLessLeaves-Reforged-1.18.2-1.0.5.jar|Gives you a 9% fps improvement for leaves rendering|[Source](https://www.curseforge.com/minecraft/mc-mods/culllessleaves-reforged)|
|Embeddium|Performance & Optimization|Yes|Yes|embeddium-0.3.10+mc1.18.2.jar|A powerful, mod-friendly, FOSS client performance mod for NeoForge|[Source](https://www.curseforge.com/minecraft/mc-mods/embeddium)|
|Entity Collision FPS Fix|Performance & Optimization|No|No|Entity_Collision_FPS_Fix-forge-1.18.2-1.0.0.jar|Client Side mod that optimizes entity's on the render thread. Fixes https://bugs.mojang.com/browse/MC-228976 \| Note: Stopped at 1.19.2; MC-228976 optimization handled differently in 1.20.1.|[Source](https://www.curseforge.com/minecraft/mc-mods/entity-collision-fps-fix)|
|Entity Culling Fabric/Forge|Performance & Optimization|Yes|Yes|entityculling-forge-1.6.1-mc1.18.2.jar|Using async path-tracing to hide BlockEntities/Entities that are not visible|[Source](https://www.curseforge.com/minecraft/mc-mods/entityculling)|
|Fast Async World Save[Forge/Neo/Fabric]|Performance & Optimization|Yes|Yes|fastasyncworldsave-1.18.2-1.2.jar|Prevent lag-spikes and data loss during intermittent world saves|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-async-world-save-forge-fabric)|
|FastFurnace|Performance & Optimization|Yes|Yes|FastFurnace-1.18.2-6.0.3.jar|A performance upgrade for the furnace.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastfurnace)|
|FastSuite|Performance & Optimization|Yes|Yes|FastSuite-1.18.2-3.0.2.jar|A performance upgrade for the JSON recipe system.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastsuite)|
|FastWorkbench|Performance & Optimization|Yes|Yes|FastWorkbench-1.18.2-6.1.1.jar|A performance upgrade for the crafting table.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastworkbench)|
|FerriteCore ((Neo)Forge)|Performance & Optimization|Yes|Yes|ferritecore-4.2.2-forge.jar|Memory usage optimizations|[Source](https://www.curseforge.com/minecraft/mc-mods/ferritecore)|
|Iris & Oculus Flywheel Compat|Performance & Optimization|Yes|No|oculus-flywheel-compat-1.18.2-0.2.1.jar|Enable Flywheel's optimizations when use shaders. \| Note: Supports 1.20.1 Forge, but v6 uses Colorwheel & Colorwheel Patcher.|[Source](https://www.curseforge.com/minecraft/mc-mods/iris-flywheel-compat)|
|Lazy DataFixerUpper(LazyDFU) [FORGE]|Performance & Optimization|No|No|lazydfu-1.0-1.18+.jar|Makes the initialization of DataFixerUpper "lazy" \| Note: Discontinued after 1.19.3 (vanilla 1.19.4+ implemented lazy DFU natively).|[Source](https://www.curseforge.com/minecraft/mc-mods/lazy-dfu-forge)|
|Lightspeed - Launch optimizations|Performance & Optimization|No|No|lightspeed-1.18.2-1.0.5.jar|Reduces your waiting time by loading modpacks significantly faster (currently 48% - 71%) \| Note: Discontinued after 1.19.2 (most optimizations merged into vanilla 1.20; unofficial port LightSpeedRe exists); v6 uses FastBoot & lazyyyyy.|[Source](https://www.curseforge.com/minecraft/mc-mods/lightspeedmod)|
|Mobtimizations - Entity Performance Fixes|Performance & Optimization|Yes|Yes|mobtimizations-forge-1.18.2-1.0.0.jar|Optimizes a lot of tasks that Entity AI wastefully performs, minimal effect on gameplay.|[Source](https://www.curseforge.com/minecraft/mc-mods/mobtimizations)|
|ModernFix|Performance & Optimization|Yes|Yes|modernfix-forge-5.13.0+mc1.18.2.jar|All-in-one mod that improves performance, reduces memory usage, and fixes many bugs. Compatible with all your favorite performance mods!|[Source](https://www.curseforge.com/minecraft/mc-mods/modernfix)|
|Oculus|Performance & Optimization|Yes|Yes|oculus-mc1.18.2-1.6.4.jar|Unofficial Fork of "Iris", made to work with FML|[Source](https://www.curseforge.com/minecraft/mc-mods/oculus)|
|Pluto|Performance & Optimization|No|No|pluto-mc1.18.2-0.0.6.jar|Networking stack optimization mod and unofficial fork of Krypton mod for Minecraft Forge \| Note: Stopped at 1.19.3 (Forge fork of Krypton).|[Source](https://www.curseforge.com/minecraft/mc-mods/pluto)|
|Saturn|Performance & Optimization|Yes|Yes|saturn-mc1.18.2-0.1.3.jar|A performance mod designed to optimize Minecraft's memory usage.|[Source](https://www.curseforge.com/minecraft/mc-mods/saturn)|
|Server Performance - Smooth Chunk Save|Performance & Optimization|Yes|Yes|smoothchunk-1.18.2-1.9.jar|Enables lag-free continuous chunk saving, increasing server TPS|[Source](https://www.curseforge.com/minecraft/mc-mods/smooth-chunk-save)|
|Smooth Boot (Reloaded)|Performance & Optimization|Yes|Yes|smoothboot(reloaded)-mc1.18.2-0.0.4.jar|Tweaks for Minecraft CPU scheduling and unofficial fork of Smooth Boot mod for Minecraft Forge 1.18.2+|[Source](https://www.curseforge.com/minecraft/mc-mods/smooth-boot-reloaded)|
|Starlight (Forge)|Performance & Optimization|Yes|No|starlight-1.0.2+forge.546ae87.jar|Rewrites the light engine to fix lighting performance and lighting errors \| Note: Supports 1.20.1 Forge, but dropped in v6 (vanilla 1.20 overhauled lighting engine).|[Source](https://www.curseforge.com/minecraft/mc-mods/starlight-forge)|
|Anvil Never Too Expensive|Quests, Progression & NPCs|Yes|No|AnvilNeverTooExpensive-1.18-1.1.jar|Removes the level cap in the Anvil GUI|[Source](https://www.curseforge.com/minecraft/mc-mods/anvil-never-too-expensive)|
|Custom Villager Trades (Forge/NeoForge)|Quests, Progression & NPCs|Yes|No|customvillagertrades-forge-18.24.0.jar|Create your own villager trades|[Source](https://www.curseforge.com/minecraft/mc-mods/custom-villager-trades-forge)|
|Fixed Anvil Repair Cost|Quests, Progression & NPCs|Yes|No|fixedanvilrepaircost-1.18.2-3.1.jar|💰 Patches the anvil to set the default level cost, material cost and percentage repaired.|[Source](https://www.curseforge.com/minecraft/mc-mods/fixed-anvil-repair-cost)|
|FTB Quests (NeoForge)|Quests, Progression & NPCs|Yes|Yes|ftb-quests-forge-1802.3.15-build.298.jar|Questing Mod by FTB|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge)|
|FTB Teams (NeoForge)|Quests, Progression & NPCs|Yes|Yes|ftb-teams-forge-1802.2.9-build.88.jar|Library for mods that can utilize team progression|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-teams-forge)|
|Pufferfish's Skills [Fabric & Forge & NeoForge]|Quests, Progression & NPCs|Yes|Yes|puffish_skills-0.10.0-1.18.2-forge.jar|Adds a fully configurable skill system to the game.|[Source](https://www.curseforge.com/minecraft/mc-mods/puffish-skills)|
|Simple Shops|Quests, Progression & NPCs|Yes|No|simpleshops-1.2.1.jar|Adds simple and easy player shops and creative shops!|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-shops)|
|Starter Kit|Quests, Progression & NPCs|Yes|Yes|starterkit-1.18.2-5.2.jar|📦 Give all new players joining the world configurable starter gear, items, potion effects, Curios and Trinkets slots and/or commands. Compatible with FTB Tea...|[Source](https://www.curseforge.com/minecraft/mc-mods/starter-kit)|
|Corpse|Storage, Loot & Backpacks|Yes|Yes|corpse-1.18.2-1.0.1.jar|Never lose your items again!|[Source](https://www.curseforge.com/minecraft/mc-mods/corpse)|
|Lootr (Forge & NeoForge)|Storage, Loot & Backpacks|Yes|Yes|lootr-1.18.2-0.3.25.63.jar|A mod that makes it so nobody misses out on Loot! All loot chests are instanced per player and visually unique.|[Source](https://www.curseforge.com/minecraft/mc-mods/lootr)|
|Refined Storage|Storage, Loot & Backpacks|Yes|Yes|refinedstorage-1.10.6.jar|An elegant solution to your hoarding problem.|[Source](https://www.curseforge.com/minecraft/mc-mods/refined-storage)|
|Sophisticated Backpacks|Storage, Loot & Backpacks|Yes|Yes|sophisticatedbackpacks-1.18.2-3.19.1.959.jar|Yet another backpack mod this time with backpack you can place in world, color in different color combinations, upgrade with more inventory and enhance with...|[Source](https://www.curseforge.com/minecraft/mc-mods/sophisticated-backpacks)|
|Storage Drawers|Storage, Loot & Backpacks|Yes|Yes|StorageDrawers-1.18.2-10.2.1.jar|Interactive compartment storage for your workshops.|[Source](https://www.curseforge.com/minecraft/mc-mods/storage-drawers)|
|Trash Cans|Storage, Loot & Backpacks|Yes|Yes|trashcans-1.0.18-forge-mc1.18.jar|Trash Cans adds trash cans which can be used to void items, liquids, and energy!|[Source](https://www.curseforge.com/minecraft/mc-mods/trash-cans)|
|TrashSlot|Storage, Loot & Backpacks|Yes|Yes|trashslot-forge-1.18.2-11.0.3.jar|Adds a draggable trash slot to all inventory screens. Press T to toggle.|[Source](https://www.curseforge.com/minecraft/mc-mods/trashslot)|
|XP Tome|Storage, Loot & Backpacks|Yes|Yes|xptome-1.18.2-2.1.7.jar|Adds a book that can store a configurable amount of XP.|[Source](https://www.curseforge.com/minecraft/mc-mods/xp-tome)|
|Cold Sweat|Survival, Health & Environment|Yes|No|ColdSweat-2.2.5.1.jar|Adds a survival-focused temperature system to Minecraft, with lots of customization! \| Note: Supports 1.20.1 Forge, but v6 consolidated temperature into Legendary Survival Overhaul.|[Source](https://www.curseforge.com/minecraft/mc-mods/cold-sweat)|
|Comforts|Survival, Health & Environment|Yes|Yes|comforts-forge-1.18.2-5.0.0.6.jar|Adds sleeping bags and hammocks for, respectively, portability and turning day to night, without setting new spawns. Comes in 16 different colors!|[Source](https://www.curseforge.com/minecraft/mc-mods/comforts)|
|Enhanced Celestials - Blood, Blue, & Harvest (Super) Moons|Survival, Health & Environment|Yes|No|Enhanced_Celestials-forge-1.18.2-2.0.7.jar|A mod adding new Lunar Events like blood moons and harvest moons!|[Source](https://www.curseforge.com/minecraft/mc-mods/enhanced-celestials)|
|First Aid|Survival, Health & Environment|Yes|No|firstaid-1.11.1.jar|A minecraft mod that extends the minecraft health system \| Note: Supports 1.20.1 Forge, but v6 replaced First Aid + Thirst Was Taken + Cold Sweat with Legendary Survival Overhaul.|[Source](https://www.curseforge.com/minecraft/mc-mods/first-aid)|
|Serene Seasons|Survival, Health & Environment|Yes|Yes|Serene Seasons-1.18.2-7.0.0.13.jar|Seasons with changing colors, shifting temperatures, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/serene-seasons)|
|Snow! Real Magic! ⛄ (Neo/Forge)|Survival, Health & Environment|Yes|No|SnowRealMagic-1.18.2-forge-4.2.4.jar|Not a magic mod. \| Snow Gravity & Accumulation \| Snow-covered blocks \| Tweak snow behaviors|[Source](https://www.curseforge.com/minecraft/mc-mods/snow-real-magic)|
|Thirst Was Taken|Survival, Health & Environment|Yes|No|ThirstWasTaken-1.18.2-1.3.4.jar|Modern take on thirst, compatible with Create, Farmer's Delight & more \| Note: Supports 1.20.1 Forge, but v6 consolidated thirst into Legendary Survival Overhaul.|[Source](https://www.curseforge.com/minecraft/mc-mods/thirst-was-taken)|
|True Darkness|Survival, Health & Environment|No|No|darkness-forge-mc118-2.0.91.jar|Moonless nights and enclosed spaces are truly dark. (Fabric and Forge) \| Note: Original stopped at 1.19.3.|[Source](https://www.curseforge.com/minecraft/mc-mods/true-darkness)|
|Click Machine|Tech, Automation & Power|Yes|Yes|ClickMachine-1.18.2-6.0.5.jar|A simple, standalone, auto-clicker.|[Source](https://www.curseforge.com/minecraft/mc-mods/click-machine)|
|Create|Tech, Automation & Power|Yes|Yes|create-1.18.2-0.5.1.f.jar|Aesthetic Technology that empowers the Player|[Source](https://www.curseforge.com/minecraft/mc-mods/create)|
|Create Crafts & Additions|Tech, Automation & Power|Yes|Yes|createaddition-1.18.2-1.0.0.jar|Electrifying the Create mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/createaddition)|
|Create Stuff 'N Additions|Tech, Automation & Power|Yes|Yes|create-stuff-additions1.18.2_v2.0.4a.jar|🧲 Dominate your environment with Create technology|[Source](https://www.curseforge.com/minecraft/mc-mods/create-stuff-additions)|
|Create: Steam 'n' Rails|Tech, Automation & Power|Yes|No|Steam_Rails-1.4.8+forge-mc1.18.2-build.23.jar|Adding depth to Create's rail network & steam system|[Source](https://www.curseforge.com/minecraft/mc-mods/create-steam-n-rails)|
|Immersive Engineering|Tech, Automation & Power|Yes|Yes|ImmersiveEngineering-1.18.2-8.4.0-161.jar|A retro-futuristic tech mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-engineering)|
|Immersive Petroleum|Tech, Automation & Power|Yes|No|ImmersivePetroleum-1.18.2-4.2.0-25.jar|Adds oil and oil processing to Immersive Engineering \| Note: Supports 1.20.1 Forge, but v6 uses Create: Diesel Generators instead.|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-petroleum)|
|Pipez|Tech, Automation & Power|Yes|Yes|pipez-1.18.2-1.1.5.jar|Simple and efficient pipes|[Source](https://www.curseforge.com/minecraft/mc-mods/pipez)|
|Security Craft|Tech, Automation & Power|Yes|Yes|[1.18.2] SecurityCraft v1.9.7.jar|Adds plenty of blocks and items to defend and secure your base with.|[Source](https://www.curseforge.com/minecraft/mc-mods/security-craft)|
|AppleSkin|UI, HUD, Maps & Info|Yes|Yes|appleskin-forge-mc1.18.2-2.4.1.jar|Adds some useful information about food/hunger to the HUD|[Source](https://www.curseforge.com/minecraft/mc-mods/appleskin)|
|Armor Points ++|UI, HUD, Maps & Info|Yes|Yes|armorpointspp-forge-1.18.2-3.1.0.jar|Allows you to see armor values above 20 and stack multiple health bars onto one.|[Source](https://www.curseforge.com/minecraft/mc-mods/armorpoints)|
|Better Advancements|UI, HUD, Maps & Info|Yes|Yes|BetterAdvancements-1.18.2-0.1.2.125.jar|Successor to BetterAchievements for the new advancements system in minecraft 1.12+|[Source](https://www.curseforge.com/minecraft/mc-mods/better-advancements)|
|Better Compatibility Checker|UI, HUD, Maps & Info|Yes|Yes|BetterCompatibilityChecker-1.1.21-build.48+mc1.18.2.jar|Changes the default server compatability check to compare modpack versions|[Source](https://www.curseforge.com/minecraft/mc-mods/better-compatibility-checker)|
|Better Ping Display|UI, HUD, Maps & Info|Yes|No|BetterPingDisplay-1.18.2-1.1.jar|Displays ping in milliseconds in the player list in a configurable way|[Source](https://www.curseforge.com/minecraft/mc-mods/better-ping-display)|
|Configured|UI, HUD, Maps & Info|Yes|Yes|configured-2.0.0-1.18.2.jar|Automatic in-game configuration menus for every mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/configured)|
|Controlling|UI, HUD, Maps & Info|Yes|Yes|Controlling-forge-1.18.2-9.0+22.jar|Adds a search bar to the Key-Bindings menu|[Source](https://www.curseforge.com/minecraft/mc-mods/controlling)|
|Day Counter|UI, HUD, Maps & Info|Yes|No|day_counter_v3.0_1.18.2_[FORGE].jar|Day Counter is a fully customizable Minecraft mod that tracks the passage of time in your world and brings it to life. It adds a whole new layer of progressi...|[Source](https://www.curseforge.com/minecraft/mc-mods/day-counter)|
|Durability Tooltip|UI, HUD, Maps & Info|Yes|Yes|durabilitytooltip-1.1.4-forge-mc1.18.jar|Durability Tooltip shows you the durability of an item!|[Source](https://www.curseforge.com/minecraft/mc-mods/durability-tooltip)|
|Enchantment Descriptions|UI, HUD, Maps & Info|Yes|Yes|EnchantmentDescriptions-Forge-1.18.2-10.0.12.jar|Adds in-game descriptions for enchantments to tooltips.|[Source](https://www.curseforge.com/minecraft/mc-mods/enchantment-descriptions)|
|Equipment Compare [Neo/Forge]|UI, HUD, Maps & Info|Yes|Yes|EquipmentCompare-1.18.2-forge-1.3.3.jar|Makes it easier to compare equipment by showing a tooltip for what you're already wearing.|[Source](https://www.curseforge.com/minecraft/mc-mods/equipment-compare)|
|JEITweaker|UI, HUD, Maps & Info|Yes|No|JEITweaker-1.18.2-3.0.0.9.jar|Adds CraftTweaker support to Just Enough Items \| Note: Has 1.20.1 Forge support, but v6 removed CraftTweaker stack.|[Source](https://www.curseforge.com/minecraft/mc-mods/jeitweaker)|
|Just Enough Immersive Multiblocks|UI, HUD, Maps & Info|Yes|Yes|jeimultiblocks-1.18.2-0.0.2.jar|Immersive Engineering addon that adds JEI support for multiblocks.|[Source](https://www.curseforge.com/minecraft/mc-mods/just-enough-immersive-multiblocks)|
|Just Enough Items (JEI)|UI, HUD, Maps & Info|Yes|Yes|jei-1.18.2-forge-10.2.1.1005.jar|View Items and Recipes|[Source](https://www.curseforge.com/minecraft/mc-mods/jei)|
|Just Enough Professions (JEP)|UI, HUD, Maps & Info|Yes|No|JustEnoughProfessions-1.18.2-1.3.0.jar|A JEI addon that adds profession workstations|[Source](https://www.curseforge.com/minecraft/mc-mods/just-enough-professions-jep)|
|Not Enough Recipe Book [NERB]|UI, HUD, Maps & Info|Yes|Yes|nerb-1.18.2-0.3-FORGE.jar|Completely removes recipe book from the game, optimizing player data.|[Source](https://www.curseforge.com/minecraft/mc-mods/notenoughrecipebook)|
|The One Probe|UI, HUD, Maps & Info|Yes|Yes|theoneprobe-1.18-5.1.2.jar|More immersive alternative for WAILA|[Source](https://www.curseforge.com/minecraft/mc-mods/the-one-probe)|
|Tips|UI, HUD, Maps & Info|Yes|No|Tips-Forge-1.18.2-5.0.11.jar|Adds a tip section to various loading screens.|[Source](https://www.curseforge.com/minecraft/mc-mods/tips)|
|Xaero's Minimap (Fair-play Edition)|UI, HUD, Maps & Info|Yes|No|Xaeros_Minimap_FP23.9.4_Forge_1.18.2.jar|Fair-play edition of the Xaero's Minimap mod, designed for fair PVP against players without a minimap. \| Note: Supports 1.20.1 Forge, but v6 uses standard Xaero's Minimap.|[Source](https://www.curseforge.com/minecraft/mc-mods/xaeros-minimap-fair-play-edition)|
|Xaero's World Map|UI, HUD, Maps & Info|Yes|Yes|XaerosWorldMap_1.37.3_Forge_1.18.2.jar|Adds a fullscreen worldmap which shows you what you have explored in the world. Can work together with Xaero's Minimap.|[Source](https://www.curseforge.com/minecraft/mc-mods/xaeros-world-map)|
|Simple Planes (NeoForge)|Vehicles & Transport|Yes|Yes|simpleplanes-1.18.2-5.2.1.jar|Upgradeable planes and helicopters which you can fly with.|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-planes)|
|Ultimate Car Mod|Vehicles & Transport|Yes|No|car-1.18.2-1.0.1.jar|This mod brings cars, road construction and biodiesel production into your Minecraft world. \| Note: Supports 1.20.1 Forge, but v6 uses DragN's Valiant Vehicles! instead.|[Source](https://www.curseforge.com/minecraft/mc-mods/ultimate-car-mod)|
|Biome Spawn Point|Worldgen, Cities & Structures|Yes|Yes|biomespawnpoint-1.18.2-2.0.jar|🌲 Allows specifying which biome and dimension players will spawn in on new world creation.|[Source](https://www.curseforge.com/minecraft/mc-mods/biome-spawn-point)|
|Biomes O' Plenty|Worldgen, Cities & Structures|Yes|Yes|BiomesOPlenty-1.18.2-16.0.0.109-universal.jar|Adds 50+ unique biomes to enhance your world, with new trees, flowers, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty)|
|Explorer's Compass|Worldgen, Cities & Structures|Yes|No|ExplorersCompass-1.18.2-1.3.0-forge.jar|Explorer's Compass is an item that allows you to locate structures anywhere in the world.|[Source](https://www.curseforge.com/minecraft/mc-mods/explorers-compass)|
|Nature's Compass|Worldgen, Cities & Structures|Yes|Yes|NaturesCompass-1.18.2-1.9.7-forge.jar|Nature's Compass is an item that allows you to locate biomes anywhere in the world.|[Source](https://www.curseforge.com/minecraft/mc-mods/natures-compass)|
|Ore Tweaker|Worldgen, Cities & Structures|No|No|OreTweaker-1.18.2-3.4.0.jar|Disable, tweak and add your own ore generation features using JSON for Minecraft Forge - OreTweaker \| Note: Stopped at 1.18.2 on CurseForge; worldgen/ore tweaks done via datapacks/KubeJS in 1.20.1.|[Source](https://www.curseforge.com/minecraft/mc-mods/ore-tweaker)|
|Structure Essentials|Worldgen, Cities & Structures|Yes|No|structureessentials-1.18.2-3.0.jar|Essential features for structures: Faster locating, distance adjustments, nearby structure command, automatic structure biome compat, structure overlap preve...|[Source](https://www.curseforge.com/minecraft/mc-mods/structure-essentials-forge-fabric)|
|The Lost Cities|Worldgen, Cities & Structures|Yes|Yes|lostcities-1.18-5.3.29.jar|The Lost Cities is a world generation mod|[Source](https://www.curseforge.com/minecraft/mc-mods/the-lost-cities)|
|This Rocks! (Forge)|Worldgen, Cities & Structures|Yes|Yes|ThisRocks-1.18.2-1.0.4.jar|Adds little rocks, sticks, pinecones, seashells, starfish, and geysers to your minecraft world to make it feel more natural.|[Source](https://www.curseforge.com/minecraft/mc-mods/this-rocks-forge)|
|YUNG's Better Mineshafts (Forge/NeoForge)|Worldgen, Cities & Structures|Yes|No|YungsBetterMineshafts-1.18.2-Forge-2.2.jar|A long-awaited and much-needed abandoned mineshaft overhaul!|[Source](https://www.curseforge.com/minecraft/mc-mods/yungs-better-mineshafts-forge)|
|Alex's Mobs|Zombies, Mobs & Wildlife|Yes|No|alexsmobs-1.18.6.jar|85+ New mobs with stylistic quality above the default game.|[Source](https://www.curseforge.com/minecraft/mc-mods/alexs-mobs)|
|Critters and Companions|Zombies, Mobs & Wildlife|Yes|Yes|crittersandcompanions-1.18.2-1.0.2.jar|Adds a few new friends to your world!|[Source](https://www.curseforge.com/minecraft/mc-mods/critters-and-companions)|
|Enhanced AI|Zombies, Mobs & Wildlife|Yes|Yes|EnhancedAI-1.6.11-mc1.18.2.jar|Creepers Breaching, Zombies mining and Skeletons sniping. Customize their AI as you like!|[Source](https://www.curseforge.com/minecraft/mc-mods/enhanced-ai)|
|Enhanced Hordes|Zombies, Mobs & Wildlife|Yes|Yes|eh1.2-1.18.2.jar|Enhances zombie's ability to cooperate, among other mobs.|[Source](https://www.curseforge.com/minecraft/mc-mods/enhanced-hordes)|
|Guard Villagers|Zombies, Mobs & Wildlife|Yes|No|guardvillagers-1.18.2.1.4.3.jar|Guards that help with village pest control|[Source](https://www.curseforge.com/minecraft/mc-mods/guard-villagers)|
|Lost Souls|Zombies, Mobs & Wildlife|Yes|Yes|lostsouls-1.18-2.0.5.jar|Lost Souls is an addon mod for The Lost Cities to add more danger to the buildings|[Source](https://www.curseforge.com/minecraft/mc-mods/lost-souls)|
|Mob Sunscreen|Zombies, Mobs & Wildlife|Yes|Yes|mobsunscreen-1.18.1-3.0.4.jar|Stop Zombies and Skeletons from Burning in the Sun!|[Source](https://www.curseforge.com/minecraft/mc-mods/mob-sunscreen)|
|Mutationcraft|Zombies, Mobs & Wildlife|Yes|No|Mutationcraft_1.18.2_1.0.6.jar|Adds new terrifying parasite mutant creatures into the game!|[Source](https://www.curseforge.com/minecraft/mc-mods/mutationcraft)|
|NoCube's Zombie Mobs|Zombies, Mobs & Wildlife|No|No|nocube's_zombie_mobs_1.4.0_forge_1.18.2.jar|Adds hardcore zombie animals and creatures. Vanilla-style. \| Note: Stopped at 1.19.2; v6 adds Fungal Infection: Spore instead.|[Source](https://www.curseforge.com/minecraft/mc-mods/nocubes-zombie-mobs)|
|Nyf's Spiders|Zombies, Mobs & Wildlife|Yes|No|spiderstpo-1.18.2-2.0.3.jar|Modifes spiders to be more realistic.|[Source](https://www.curseforge.com/minecraft/mc-mods/nyfs-spiders)|
|The Hordes|Zombies, Mobs & Wildlife|Yes|Yes|The-Hordes-1.18.2-1.5.3a.jar|Horde Invasions and Zombie Infection|[Source](https://www.curseforge.com/minecraft/mc-mods/the-hordes)|
|THE UNDEAD REVAMPED|Zombies, Mobs & Wildlife|Yes|Yes|THEUNDEADREVAMPED_0.9e_1.18.2.jar|This mod add some new types of undeads.|[Source](https://www.curseforge.com/minecraft/mc-mods/theundead)|
|VMH - Variable Mob Height|Zombies, Mobs & Wildlife|Yes|No|vmh-1.2.2-1.18.2.jar|Varies mob height on spawn.|[Source](https://www.curseforge.com/minecraft/mc-mods/vmh)|
|Zombie Awareness|Zombies, Mobs & Wildlife|Yes|Yes|zombieawareness-1.18.1-1.12.3.jar|- Smarter more aware zombies (and skeletons), they track you down via blood scent, sound, and light source awareness|[Source](https://www.curseforge.com/minecraft/mc-mods/zombie-awareness)|
|Zombie Extreme|Zombies, Mobs & Wildlife|Yes|Yes|Zombie Extreme 1.18.2 0.2.4.jar|This is a Big Mod that adds a bunch of new mechanics and a large number of zombies and infected to your minecraft world. In order to study a new biome, you n...|[Source](https://www.curseforge.com/minecraft/mc-mods/zombie-extreme)|

### 16.2 DeceasedCraft Beta 5.10.17 — Public v6 open beta (Minecraft 1.20.1 / Forge 47.4.0)

**306 Standard + 1 DH Edition extra**

The following list is specific to Beta 5.10.17. The `Edition` column distinguishes Standard entries from the Distant Horizons edition extra. Do not treat the Distant Horizons edition-only mod as part of the Standard archive unless the selected target archive actually includes it.

|Mod|Category|Edition|In both packs?|Recorded file / version|Description / notes|Source|
|---|---|---|---|---|---|---|
|[EMF] Entity Model Features [Fabric & Forge]|Audio, Visuals & Immersion|Standard|No|entity_model_features_forge_1.20.1-2.2.jar|EMF is an, OptiFine format, Custom Entity Model replacement mod available for Fabric and Forge.|[Source](https://www.curseforge.com/minecraft/mc-mods/entity-model-features)|
|[ETF] Entity Texture Features - [Fabric & Forge]|Audio, Visuals & Immersion|Standard|Yes|entity_texture_features_forge_1.20.1-6.2.9.jar|Custom, Emissive and Varied mobs like Optifine and so much more.. +Player skin features!)|[Source](https://www.curseforge.com/minecraft/mc-mods/entity-texture-features-fabric)|
|CleanView|Audio, Visuals & Immersion|Standard|Yes|cleanview-1.20.1-v1.jar|CleanView is a minecraft client mod that removes potion particles from your viewpoint|[Source](https://www.curseforge.com/minecraft/mc-mods/cleanview)|
|CraftPresence|Audio, Visuals & Immersion|Standard|Yes|CraftPresence-2.7.0+1.20.1-forge.jar|Completely Customize the way others see you play in Discord!|[Source](https://www.curseforge.com/minecraft/mc-mods/craftpresence)|
|Euphoria Patches|Audio, Visuals & Immersion|Standard|No|EuphoriaPatcher-1.7.8-r5.6.1-forge.jar|Euphoria Patches is an add-on for Complementary Shaders, extending it with more optional features and settings.|[Source](https://www.curseforge.com/minecraft/mc-mods/euphoria-patches)|
|Explosive Enhancement: Reforged|Audio, Visuals & Immersion|Standard|No|explosiveenhancement-1.1.0-1.20.1-client-and-server.jar|Make the explosions look cooler. Now for (Neo)Forge.|[Source](https://www.curseforge.com/minecraft/mc-mods/explosive-enhancement-reforged)|
|Exposure|Audio, Visuals & Immersion|Standard|No|exposure-1.20.1-1.7.16-forge.jar|Camera mod with focus on process and aesthetics \| Note: Replaces Camera Mod (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/exposure)|
|Extra Gore|Audio, Visuals & Immersion|Standard|No|extragore-1.20.1-5.2.3.1.jar|More Blood!|[Source](https://www.curseforge.com/minecraft/mc-mods/extra-gore)|
|Extreme sound muffler - (Neo)Forge|Audio, Visuals & Immersion|Standard|No|ExtremeSoundMuffler-3.49.2-forge-1.20.1.jar|Forget about those nasty sounds! - Clientside sound muffler.|[Source](https://www.curseforge.com/minecraft/mc-mods/extreme-sound-muffler)|
|ItemPhysic Lite|Audio, Visuals & Immersion|Standard|No|ItemPhysicLite_FORGE_v1.6.6_mc1.20.1.jar|#spinning|[Source](https://www.curseforge.com/minecraft/mc-mods/itemphysic-lite)|
|Particular ✨ Reforged|Audio, Visuals & Immersion|Standard|No|particular-1.20.1-Forge-1.2.7.jar|Particular is a mod that enhances Minecraft's ambience with many hand-crafted visual effects. Forge Port ! \| Note: Replaces Effective (Forge) (v5.5.5) for ambient particles.|[Source](https://www.curseforge.com/minecraft/mc-mods/particular-reforged)|
|Presence Footsteps (Forge)|Audio, Visuals & Immersion|Standard|Yes|PresenceFootsteps-1.20.1-1.9.1-beta.1.jar|An unofficial port of Presence Footsteps from Fabric to Forge|[Source](https://www.curseforge.com/minecraft/mc-mods/presence-footsteps-forge)|
|Pretty Rain|Audio, Visuals & Immersion|Standard|No|Pretty Rain-1.20.1-Forge-1.1.3.jar|Pretty Rain replaces the default weather with prettier particle effects. Port of Particle Rain to NeoForge|[Source](https://www.curseforge.com/minecraft/mc-mods/pretty-rain)|
|Shoulder Surfing Reloaded|Audio, Visuals & Immersion|Standard|Yes|ShoulderSurfing-Forge-1.20.1-4.15.0.jar|Shoulder Surfing Reloaded is a highly configurable third person camera mod for Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/shoulder-surfing-reloaded)|
|Sodium/Embeddium Dynamic Lights|Audio, Visuals & Immersion|Standard|No|sodiumdynamiclights-forge-1.0.10-1.20.1.jar|Multiloader port of LambDynLights that adds Sodium/Embeddium settings support \| Note: Replaces Lucent (v5.5.5) for dynamic lighting.|[Source](https://www.curseforge.com/minecraft/mc-mods/dynamiclights-reforged)|
|Sodium/Embeddium Extras|Audio, Visuals & Immersion|Standard|No|sodiumextras-forge-1.0.7-1.20.1.jar|An add-on mod for Sodium (and Embeddium) that adds new features and customization. \| Note: Replaces Embeddium (Rubidium) Extra (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/magnesium-extras)|
|Sodium/Embeddium Options API|Audio, Visuals & Immersion|Standard|No|sodiumoptionsapi-forge-1.0.10-1.20.1.jar|Config API for adding Sodium/Embeddium options with a better categories menu \| Note: Replaces TexTrue's Embeddium Options (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/sodium-options-api)|
|Sound Physics Remastered|Audio, Visuals & Immersion|Standard|Yes|sound-physics-remastered-forge-1.20.1-1.4.10.jar|A Minecraft mod that provides realistic sound attenuation, reverberation, and absorption through blocks.|[Source](https://www.curseforge.com/minecraft/mc-mods/sound-physics-remastered)|
|Sounds|Audio, Visuals & Immersion|Standard|No|Sounds-2.2.1+1.20.1+forge.jar|Adds a wide range of new and improved sound effects to Minecraft, letting you customize everything from block interactions to UI events. Easily tweak or expa...|[Source](https://www.curseforge.com/minecraft/mc-mods/sound)|
|The Sound of Rain|Audio, Visuals & Immersion|Standard|No|soundofrain-0.5.0.jar|Material based rain sound effects and some cool thunder|[Source](https://www.curseforge.com/minecraft/mc-mods/the-sound-of-rain)|
|Vanilla Music Discs|Audio, Visuals & Immersion|Standard|No|vanilla_music_discs-1.6-forge-1.20.1.jar|With this mod you can listen to any minecraft music that previously played in the background|[Source](https://www.curseforge.com/minecraft/mc-mods/vanilla-music-discs)|
|What Are They Up To (Watut)|Audio, Visuals & Immersion|Standard|Yes|watut-forge-1.20.1-1.2.3.jar|Lets you see if players are typing, in a GUI, idle, with cool ingame visuals|[Source](https://www.curseforge.com/minecraft/mc-mods/what-are-they-up-to)|
|AllTheLeaks (Memory Leak Fix)|Bug Fixes & Stability|Standard|No|alltheleaks-1.1.1+1.20.1-forge.jar|This mod fixes memory leaks of some mods, Neoforge and Minecraft until they implement their fixes.|[Source](https://www.curseforge.com/minecraft/mc-mods/alltheleaks)|
|Apocalypse Patches|Bug Fixes & Stability|Standard|No|apoc_patches-1.0.4-all.jar|Patches for the ApocalypseNow mod to fix mod compatible and performance issues.|[Source](https://www.curseforge.com/minecraft/mc-mods/apocalypse-patches)|
|AttributeFix|Bug Fixes & Stability|Standard|Yes|AttributeFix-Forge-1.20.1-21.0.4.jar|Removes arbitrary limits on Minecraft's attribute system.|[Source](https://www.curseforge.com/minecraft/mc-mods/attributefix)|
|Bee Fix|Bug Fixes & Stability|Standard|Yes|BeeFix-1.20-1.0.7.jar|Fixes Bee Related Bugs|[Source](https://www.curseforge.com/minecraft/mc-mods/bee-fix)|
|Better Biome Reblend|Bug Fixes & Stability|Standard|No|betterbiomereblend-1.5.3.jar|Updated version of Better Biome Blend, a mod that improves and fixes biome color blending \| Note: Replaces Better Biome Blend (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/bbrb)|
|Connectivity|Bug Fixes & Stability|Standard|Yes|connectivity-1.20.1-7.2.jar|Fix Login timeouts, Packet sizes errors, Payloads errors, ghostblocks and more.|[Source](https://www.curseforge.com/minecraft/mc-mods/connectivity)|
|Crash Assistant|Bug Fixes & Stability|Standard|No|CrashAssistant-forge-1.19-1.20.1-1.10.27.jar|Shows a GUI after Minecraft crashes, immediately showing and analyzing all affected logs.|[Source](https://www.curseforge.com/minecraft/mc-mods/crash-assistant)|
|CreateStuffAdditions Fix|Bug Fixes & Stability|Standard|No|createstuffadditionsfix-forge-1.20.1-0.0.0.1.jar|Fixes off-hand item NBT manipulation caused by Create Stuff Additions when throwing items.|[Source](https://www.curseforge.com/minecraft/mc-mods/createstuffadditions-fix)|
|DCTweaks|Bug Fixes & Stability|Standard|No|DCTweaks_5.10.14.jar|Bunch of tag fixes for DeceasedCraft \| Note: DeceasedCraft-specific tag fixes mod in v6 Beta.|[Source](https://www.curseforge.com/minecraft/mc-mods/dctweaks)|
|DeceasedCraft++|Bug Fixes & Stability|Standard|No|deceased_expansion-1.10-all.jar|Expanding and patching up bugs in the DeceasedCraft modpack. \| Note: Custom DeceasedCraft expansion & bug-fix companion mod in v6 Beta.|[Source](https://www.curseforge.com/minecraft/mc-mods/deceasedcraft-expansion)|
|FlickerFix|Bug Fixes & Stability|Standard|No|flickerfix-1.20.1-4.0.1.jar|Disables nightvision flickering|[Source](https://www.curseforge.com/minecraft/mc-mods/flickerfix)|
|GPUTape|Bug Fixes & Stability|Standard|No|GPUTape-1.18x-1.21x-1.0.5.1-forge.jar|Fix VRAM leaks. Based on VideoTape. \| Note: Replaces fix GPU memory leak (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/gputape)|
|Immersive Fixes|Bug Fixes & Stability|Standard|No|immersivefixes-1.0.3-all.jar|Addon for Immersive Engineering, backporting critical bug fixes and minor content to 1.20.1|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-fixes)|
|Load My F***ing Tags|Bug Fixes & Stability|Standard|No|lmft-1.0.4+1.20.1-forge.jar|Prevents Incorrect Tag Entries from breaking an entire Tag|[Source](https://www.curseforge.com/minecraft/mc-mods/lmft)|
|Max Health Fix|Bug Fixes & Stability|Standard|Yes|MaxHealthFix-Forge-1.20.1-12.0.3.jar|Fixes a bug with max health in Minecraft.|[Source](https://www.curseforge.com/minecraft/mc-mods/max-health-fix)|
|Model Gap Fix|Bug Fixes & Stability|Standard|No|modelfix-1.15.jar|Fixes small gaps in item and block models|[Source](https://www.curseforge.com/minecraft/mc-mods/model-gap-fix)|
|NaNny Reforked|Bug Fixes & Stability|Standard|No|nanny-1.0.6.jar|Fork of the mod NaNny for MC Eternal 2 that adds emergency replacement damage in place of NaN values \| Note: Replaces NaN Health Fixer (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/nanny-reforked)|
|Packet Fixer|Bug Fixes & Stability|Standard|No|packetfixer-3.3.1-1.18-1.20.4-merged.jar|A simple mod to solve various problems with packets, NBTs and timeouts.|[Source](https://www.curseforge.com/minecraft/mc-mods/packet-fixer)|
|Refined Storage (Fixes) Mixin|Bug Fixes & Stability|Standard|No|MCT-RS-Mixin-1.20.1-1.0.0-b400-release.jar|Performance and bug fixes for Refined Storage. By MCT.|[Source](https://www.curseforge.com/minecraft/mc-mods/mct-refined-storage-mixin)|
|Too Fast|Bug Fixes & Stability|Standard|Yes|toofast-1.20-0.4.3.5.jar|Fixes "moved too quickly".|[Source](https://www.curseforge.com/minecraft/mc-mods/too-fast)|
|Yeetus Experimentus|Bug Fixes & Stability|Standard|No|YeetusExperimentus-Forge-2.3.1-build.6+mc1.20.1.jar|Yeetus Experimental Settings \| Note: Replaces Shutup Experimental Settings! (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/yeetusexperimentus)|
|Another Furniture|Building, Furniture & Decor|Standard|Yes|another_furniture-forge-1.20.1-3.0.4.jar|Another Furniture is a vanilla-styled furniture mod aiming to keep things simple while adding cute decoration!|[Source](https://www.curseforge.com/minecraft/mc-mods/another-furniture)|
|Builder's Delight (Forge)|Building, Furniture & Decor|Standard|Yes|BuildersDelight-1.20.1-v.1.3.jar|Adds ~700 new blocks, decoration and a chisel.|[Source](https://www.curseforge.com/minecraft/mc-mods/builders-delight-forge)|
|Cosmetic Armor Reworked|Building, Furniture & Decor|Standard|Yes|cosmeticarmorreworked-1.20.1-v1a.jar|This mod allows you to wear two sets of armor, one for display, one for function.|[Source](https://www.curseforge.com/minecraft/mc-mods/cosmetic-armor-reworked)|
|Create Deco|Building, Furniture & Decor|Standard|Yes|createdeco-2.0.3-1.20.1-forge.jar|Industrial decoration themed for the Create mod.|[Source](https://www.curseforge.com/minecraft/mc-mods/create-deco)|
|Create: Interiors|Building, Furniture & Decor|Standard|No|interiors-0.5.6+forge-mc1.20.1-local.jar|A functional suite of innovative and configurable utility blocks for the modern builder|[Source](https://www.curseforge.com/minecraft/mc-mods/interiors)|
|Dark Paintings|Building, Furniture & Decor|Standard|No|DarkPaintings-Forge-1.20.1-17.0.4.jar|Adds new paintings to Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/dark-paintings)|
|EmbellishCraft|Building, Furniture & Decor|Standard|Yes|embellishcraft-1.20.1-7.0.0.0.jar|A mod about decoration for MC 1.13 - 1.21.1|[Source](https://www.curseforge.com/minecraft/mc-mods/embellishcraft)|
|Fast Paintings|Building, Furniture & Decor|Standard|No|fastpaintings-1.20-1.2.7.jar|Fixes and optimizes painting performance by making them blocks. Also allows customizing their model|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-paintings)|
|Just Outdoor Stuffs|Building, Furniture & Decor|Standard|No|JustOutdoorStuffs-1.20.1-forge-v1.0.2.jar|Just a simple outdoor furniture and decor mod|[Source](https://www.curseforge.com/minecraft/mc-mods/just-outdoor-stuffs)|
|MOA DECOR: ART|Building, Furniture & Decor|Standard|No|MOAdecor ART 1.20.1.jar|Add new models of decorative art´s items for your constructions.|[Source](https://www.curseforge.com/minecraft/mc-mods/moa-decor-art)|
|MOA DECOR: BATH|Building, Furniture & Decor|Standard|No|MOAdecor BATH 1.20.1.jar|Add new models of decorative bath items to your builds.|[Source](https://www.curseforge.com/minecraft/mc-mods/moa-decor-bath)|
|MOA DECOR: SCIENCE|Building, Furniture & Decor|Standard|No|MOAdecor SCIENCE 1.20.1.jar|Add new models of decorative science items to your builds.|[Source](https://www.curseforge.com/minecraft/mc-mods/moa-decor-science)|
|MrCrayfish's Furniture Mod (Legacy)|Building, Furniture & Decor|Standard|Yes|cfm-forge-1.20.1-7.0.0-pre36.jar|Adds over 80 unique pieces of furniture into Minecraft!|[Source](https://www.curseforge.com/minecraft/mc-mods/mrcrayfish-furniture-mod)|
|MrCrayfish's Furniture Mod: Refurbished|Building, Furniture & Decor|Standard|No|refurbished_furniture-forge-1.20.1-1.0.20.jar|The next generation of MrCrayfish's Furniture Mod, redesigned from the ground up with new models, sounds, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/refurbished-furniture)|
|Plushie Buddies|Building, Furniture & Decor|Standard|No|plushie_buddies-0.1.6-1.20.1.jar|A light weight mod that adds plushies to your game.|[Source](https://www.curseforge.com/minecraft/mc-mods/plushie-buddies)|
|Quark|Building, Furniture & Decor|Standard|Yes|Quark-4.0-462.jar|A Quark is a very small thing. This mod is a collection of small things that improve the vanilla minecraft experience.|[Source](https://www.curseforge.com/minecraft/mc-mods/quark)|
|Re:Deco - Vanilla Furniture|Building, Furniture & Decor|Standard|No|redeco-1.14.1-forge-1.20.1.jar|Vanilla inspired functional furniture mod [Legacy] [New version -> Redecorate]|[Source](https://www.curseforge.com/minecraft/mc-mods/redeco)|
|Simply Light|Building, Furniture & Decor|Standard|Yes|simplylight-1.20.1-1.4.6-build.50.jar|Simple light for a complicated world.|[Source](https://www.curseforge.com/minecraft/mc-mods/simply-light)|
|Texels Paintings|Building, Furniture & Decor|Standard|No|TexelsPaintings-forge-1.20.1-10.3.1.jar|Adds paintings based on landscapes, natural environments, and structures to the game.|[Source](https://www.curseforge.com/minecraft/mc-mods/texels-paintings)|
|Toni's Immersive Lanterns|Building, Furniture & Decor|Standard|No|immersivelanterns-forge-1.0.6-1.20.1.jar|Adds dynamic lighting and Accessories support to lanterns, with physics!|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-lanterns)|
|Vertical Slabs Compat|Building, Furniture & Decor|Standard|No|v_slab_compat-1.20-2.5.jar|Adds automatic compatibility for Quark's (& others) Vertical Slabs|[Source](https://www.curseforge.com/minecraft/mc-mods/vertical-slabs-compat)|
|[Let's Do] API|Core Libraries & APIs|Standard|No|letsdo-API-forge-1.2.15-forge.jar|A Library for Forge and Fabric with utilities such as Render Features, Recipe Books and Wood API|[Source](https://www.curseforge.com/minecraft/mc-mods/do-api)|
|Almanac Lib|Core Libraries & APIs|Standard|No|almanac-1.20.x-forge-1.0.2.jar|A loader independent library containing shared code reused between mods and a fix for empty nbt issues.|[Source](https://www.curseforge.com/minecraft/mc-mods/almanac-lib)|
|Apothic Attributes|Core Libraries & APIs|Standard|No|ApothicAttributes-1.20.1-1.3.7.jar|A library mod providing Attributes and related things.|[Source](https://www.curseforge.com/minecraft/mc-mods/apothic-attributes)|
|Architectury API|Core Libraries & APIs|Standard|Yes|architectury-9.2.14-forge.jar|An intermediary api aimed to ease developing multiplatform mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/architectury-api)|
|Atlas Lib|Core Libraries & APIs|Standard|Yes|Atlas Lib-1.20.1-1.1.12.jar|A serialzation and math libary for minecraft mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/atlas-lib)|
|BaguetteLib|Core Libraries & APIs|Standard|No|baguettelib-1.20.1-Forge-1.0.0.jar|A simple but powerful event library that gives mod developers the control they actually need.|[Source](https://www.curseforge.com/minecraft/mc-mods/baguettelib)|
|Balm|Core Libraries & APIs|Standard|Yes|balm-forge-1.20.1-7.3.31-all.jar|Abstraction Layer for Multi-Loader Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/balm)|
|Bookshelf|Core Libraries & APIs|Standard|Yes|Bookshelf-Forge-1.20.1-20.2.13.jar|An open source library for other mods!|[Source](https://www.curseforge.com/minecraft/mc-mods/bookshelf)|
|Botarium|Core Libraries & APIs|Standard|No|botarium-forge-1.20.1-2.3.4.jar|A crossplatform API for devs that makes transfer and storage of items, fluids and energy easier, as well as some other helpful things|[Source](https://www.curseforge.com/minecraft/mc-mods/botarium)|
|Cloth Config API (Fabric/Forge/NeoForge)|Core Libraries & APIs|Standard|Yes|cloth-config-11.1.136-forge.jar|Config Screen API for Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/cloth-config)|
|Cobweb|Core Libraries & APIs|Standard|No|cobweb-forge-1.20.1-1.0.1.jar|Crystal Nest's multiloader API for modders and pack authors. Register content and build resource packs that adapt to your mod, world, and other packs.|[Source](https://www.curseforge.com/minecraft/mc-mods/cobweb)|
|Collective|Core Libraries & APIs|Standard|Yes|collective-1.20.1-8.3.jar|🎓 Collective is a shared library with common code for all of Serilum's mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/collective)|
|CorgiLib|Core Libraries & APIs|Standard|No|Corgilib-Forge-1.20.1-4.0.3.4.jar|A library mod containing code used across Corgi Taco's mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/corgilib)|
|CoroUtil|Core Libraries & APIs|Standard|Yes|coroutil-forge-1.20.1-1.3.7.jar|Library Mod for Weather/Tropicraft/ZombieAwareness/etc|[Source](https://www.curseforge.com/minecraft/mc-mods/coroutil)|
|CreativeCore|Core Libraries & APIs|Standard|Yes|CreativeCore_FORGE_v2.12.32_mc1.20.1.jar|a core mod|[Source](https://www.curseforge.com/minecraft/mc-mods/creativecore)|
|Cupboard|Core Libraries & APIs|Standard|Yes|cupboard-1.20.1-2.7.jar|Cupboard provides code, frameworks, and utilities for minecraft mods|[Source](https://www.curseforge.com/minecraft/mc-mods/cupboard)|
|Curios API|Core Libraries & APIs|Standard|Yes|curios-forge-5.14.1+1.20.1.jar|A flexible and expandable accessory/equipment API for users and developers.|[Source](https://www.curseforge.com/minecraft/mc-mods/curios)|
|Custom Portal API [Forge]|Core Libraries & APIs|Standard|Yes|customportalapi-0.0.1-forge-1.20.jar|Make Custom Portals via API|[Source](https://www.curseforge.com/minecraft/mc-mods/custom-portal-api-forge)|
|ExpandAbility|Core Libraries & APIs|Standard|Yes|expandability-9.0.4.jar|Library mod that provides increased control over vanilla effects and abilities|[Source](https://www.curseforge.com/minecraft/mc-mods/expandability)|
|Forgified Fabric API|Core Libraries & APIs|Standard|No|fabric-api-0.92.6+1.11.14+1.20.1.jar|Fabric API implemented on top of NeoForge|[Source](https://www.curseforge.com/minecraft/mc-mods/forgified-fabric-api)|
|Framework|Core Libraries & APIs|Standard|Yes|framework-forge-1.20.1-0.7.15.jar|A common library powering all of MrCrayfish's Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/framework)|
|FTB Library (NeoForge)|Core Libraries & APIs|Standard|Yes|ftb-library-forge-2001.2.10.jar|Common code for all GUI stuff in FTB Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge)|
|FTB XMod Compat|Core Libraries & APIs|Standard|No|ftb-xmod-compat-forge-2.1.3.jar|Official multi-mod integrations support for the FTB Mods|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-xmod-compat)|
|GeckoLib|Core Libraries & APIs|Standard|Yes|geckolib-forge-1.20.1-4.7.jar|A 3D animation library for entities, blocks, items, armor, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/geckolib)|
|GlitchCore|Core Libraries & APIs|Standard|No|GlitchCore-forge-1.20.1-0.0.1.1.jar|A library mod aimed at abstracting mod loaders and providing various utilities for our mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/glitchcore)|
|Iceberg [Neo/Forge]|Core Libraries & APIs|Standard|Yes|Iceberg-1.20.1-forge-1.1.25.jar|A modding library that contains new events, helpers, and utilities to make modder's lives easier.|[Source](https://www.curseforge.com/minecraft/mc-mods/iceberg)|
|InsaneLib|Core Libraries & APIs|Standard|Yes|insanelib-1.21.14.jar|A set of common classes and utilities used by Insane's mods|[Source](https://www.curseforge.com/minecraft/mc-mods/insanelib)|
|Item Filters|Core Libraries & APIs|Standard|Yes|item-filters-forge-2001.1.0-build.59.jar|Item Filters is a library mod that is used by mods like FTB Quests. It adds several filter items that let you precisely select which items to match.|[Source](https://www.curseforge.com/minecraft/mc-mods/item-filters)|
|JasonConfig|Core Libraries & APIs|Standard|No|jsconf-1.1.1.jar|A replacement for Forge's Config system, powered by JSON|[Source](https://www.curseforge.com/minecraft/mc-mods/jsconfig)|
|Konkrete|Core Libraries & APIs|Standard|Yes|konkrete_forge_1.8.0_MC_1.20-1.20.1.jar|Just another boring library mod.|[Source](https://www.curseforge.com/minecraft/mc-mods/konkrete)|
|Kotlin for Forge|Core Libraries & APIs|Standard|Yes|kotlinforforge-4.11.0-all.jar|Adds a Kotlin language loader and provides some optional utilities.|[Source](https://www.curseforge.com/minecraft/mc-mods/kotlin-for-forge)|
|Mapper Base|Core Libraries & APIs|Standard|Yes|mapperbase-1.20.1-6.0.0.0.jar|A mod that provides basic elements for all my other mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/mapper-base)|
|McJtyLib|Core Libraries & APIs|Standard|No|mcjtylib-1.20-8.0.7.jar|Companion mod for all mods by McJty (RFTools, XNet, Deep Resonance, Not Enough Wands, SignTastic, ...))|[Source](https://www.curseforge.com/minecraft/mc-mods/mcjtylib)|
|Melody|Core Libraries & APIs|Standard|No|melody_forge_1.0.3_MC_1.20.1-1.20.4.jar|OpenAL-based library mod for playing background music.|[Source](https://www.curseforge.com/minecraft/mc-mods/melody)|
|Moonlight Lib|Core Libraries & APIs|Standard|Yes|moonlight-1.20-2.14.13-forge.jar|Forge and Fabric lightweight library with utilities such as custom Villagers AI, data driven trades, global datapack, custom Map Markers, First and third per...|[Source](https://www.curseforge.com/minecraft/mc-mods/selene)|
|MRU|Core Libraries & APIs|Standard|No|MRU-1.0.4+1.20.1+forge.jar|A library mod used by Cassian and IMB11's mods to function.|[Source](https://www.curseforge.com/minecraft/mc-mods/mru)|
|Necronomicon API|Core Libraries & APIs|Standard|No|Necronomicon-Forge-1.6.0+1.20.1.jar|A personal utility library, making development in both platforms easier.|[Source](https://www.curseforge.com/minecraft/mc-mods/necronomicon)|
|Patchouli|Core Libraries & APIs|Standard|Yes|Patchouli-1.20.1-84.1-FORGE.jar|Accessible, Data-Driven, Dependency-Free Documentation for Minecraft Modders and Pack Makers|[Source](https://www.curseforge.com/minecraft/mc-mods/patchouli)|
|Placebo|Core Libraries & APIs|Standard|Yes|Placebo-1.20.1-8.6.3.jar|A library mod|[Source](https://www.curseforge.com/minecraft/mc-mods/placebo)|
|playerAnimator|Core Libraries & APIs|Standard|Yes|player-animation-lib-forge-1.0.2-rc1+1.20.jar|player animation library|[Source](https://www.curseforge.com/minecraft/mc-mods/playeranimator)|
|Puzzles Lib|Core Libraries & APIs|Standard|No|PuzzlesLib-v8.1.32-1.20.1-Forge.jar|Why is it called Puzzles? That's the puzzle.|[Source](https://www.curseforge.com/minecraft/mc-mods/puzzles-lib)|
|Rhino|Core Libraries & APIs|Standard|Yes|rhino-forge-2001.2.3-build.10.jar|A fork of Mozilla's Rhino library, modified for use in mods|[Source](https://www.curseforge.com/minecraft/mc-mods/rhino)|
|Ritchie's Projectile Library|Core Libraries & APIs|Standard|No|ritchiesprojectilelib-2.1.0+mc.1.20.1-forge.jar|A Minecraft modding library for better projectiles.|[Source](https://www.curseforge.com/minecraft/mc-mods/ritchies-projectile-library)|
|Searchables|Core Libraries & APIs|Standard|No|Searchables-forge-1.20.1-1.0.3.jar|Searchables is a library mod that adds helper methods that allow for searching and filtering elements based on components, as well as offering built in auto-...|[Source](https://www.curseforge.com/minecraft/mc-mods/searchables)|
|ShatterLib \| OctoLib|Core Libraries & APIs|Standard|No|OctoLib-FORGE-0.5.0.1+1.20.1.jar|Collection of shared code for Shatterbyte mods|[Source](https://www.curseforge.com/minecraft/mc-mods/shatterbyte-lib)|
|Sinytra Connector|Core Libraries & APIs|Standard|No|Connector-1.0.0-beta.47+1.20.1.jar|Lets you play Fabric mods on NeoForge \| Note: Enables loading Fabric mods on Forge 1.20.1 (used alongside Forgified Fabric API).|[Source](https://www.curseforge.com/minecraft/mc-mods/sinytra-connector)|
|Sophisticated Core|Core Libraries & APIs|Standard|Yes|sophisticatedcore-1.20.1-1.2.106.1235.jar|Library mod for Sophisticated mods|[Source](https://www.curseforge.com/minecraft/mc-mods/sophisticated-core)|
|SuperMartijn642's Config Lib|Core Libraries & APIs|Standard|Yes|supermartijn642configlib-1.1.8-forge-mc1.20.jar|Config Lib makes dealing with config files just a bit easier.|[Source](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-config-lib)|
|SuperMartijn642's Core Lib|Core Libraries & APIs|Standard|Yes|supermartijn642corelib-1.1.18-forge-mc1.20.1.jar|SuperMartijn642's Core Lib adds lots of basic implementations that allow for similar code between different Minecraft versions!|[Source](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-core-lib)|
|TerraBlender (Forge)|Core Libraries & APIs|Standard|Yes|TerraBlender-forge-1.20.1-3.0.1.10.jar|A library mod for adding biomes in a simple and compatible manner!|[Source](https://www.curseforge.com/minecraft/mc-mods/terrablender)|
|TxniLib|Core Libraries & APIs|Standard|No|txnilib-forge-1.0.23-1.20.1.jar|Multiversion library mod for Txni projects|[Source](https://www.curseforge.com/minecraft/mc-mods/txnilib)|
|UniLib|Core Libraries & APIs|Standard|No|UniLib-1.2.0+1.20.1-forge.jar|A common set of Utilities, designed for over 50 versions of Minecraft!|[Source](https://www.curseforge.com/minecraft/mc-mods/unilib)|
|YetAnotherConfigLib|Core Libraries & APIs|Standard|No|yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar|A builder-based configuration library for Minecraft.|[Source](https://www.curseforge.com/minecraft/mc-mods/yacl)|
|YUNG's API (Forge/NeoForge)|Core Libraries & APIs|Standard|Yes|YungsApi-1.20-Forge-4.0.6.jar|A library mod for YUNG's Minecraft mods|[Source](https://www.curseforge.com/minecraft/mc-mods/yungs-api)|
|ZeroCore 2|Core Libraries & APIs|Standard|No|ZeroCore2-1.20.1-2.1.47.jar|Utility mod and multiblock API|[Source](https://www.curseforge.com/minecraft/mc-mods/zerocore)|
|Zeta|Core Libraries & APIs|Standard|No|Zeta-1.0-31.jar|Comprehensive Load-Bearing Library for Modular Mods \| Note: Replaces AutoRegLib (v5.5.5) as Quark's required library in 1.20.1.|[Source](https://www.curseforge.com/minecraft/mc-mods/zeta)|
|[TaCZ] Timeless and Classics Zero Guns|Firearms, Weapons & Combat|Standard|No|tacz-1.20.1-1.1.6-hotfix.jar|The most Immersive and Customizable modern FPS experience in Minecraft - A complete Remaster of the TaC gun mod by the original team. \| Note: Replaces Timeless and Classics Guns (v5.5.5) with rewritten 1.20.1 firearm engine.|[Source](https://www.curseforge.com/minecraft/mc-mods/timeless-and-classics-zero)|
|Apocalypse Now - Post Apocalyptic Arsenal|Firearms, Weapons & Combat|Standard|Yes|apocalypsenow-3.0.4NS-forge-1.20.1.jar|Apocalypse Now is a mod totally focused on an apocalyptic world that was taken over by creatures that only live to attack and eat anything alive in the world...|[Source](https://www.curseforge.com/minecraft/mc-mods/apocalypse-now)|
|Armor Set Bonuses (NeoForge /Forge)|Firearms, Weapons & Combat|Standard|Yes|spacecatasb-forge-20.14.0.jar|Adds bonuses for armor sets, and is fully customizable|[Source](https://www.curseforge.com/minecraft/mc-mods/armor-set-bonuses)|
|Artifacts|Firearms, Weapons & Combat|Standard|Yes|artifacts-forge-9.5.16.jar|Adds various treasure items that can be found through exploration|[Source](https://www.curseforge.com/minecraft/mc-mods/artifacts)|
|Better Combat [Fabric & Forge]|Firearms, Weapons & Combat|Standard|Yes|bettercombat-forge-1.8.6+1.20.1.jar|⚔️ Easy, spectacular and fun melee combat system from Minecraft Dungeons.|[Source](https://www.curseforge.com/minecraft/mc-mods/better-combat-by-daedelus)|
|Create Big Cannons|Firearms, Weapons & Combat|Standard|Yes|createbigcannons-5.9.1-mc.1.20.1-forge.jar|Artillery engineering comes to Create|[Source](https://www.curseforge.com/minecraft/mc-mods/create-big-cannons)|
|Fancy Trinkets|Firearms, Weapons & Combat|Standard|No|fancytrinkets-1.20-3.0.5.jar|All kinds of helpful baubles (using curios) for various buffs|[Source](https://www.curseforge.com/minecraft/mc-mods/fancy-trinkets)|
|MmmMmmMmmMmm (Target Dummy)|Firearms, Weapons & Combat|Standard|Yes|dummmmmmy-1.20-2.0.9.jar|Target Dummy that show damage dealt and can be equipped with armor. Damage numbers!|[Source](https://www.curseforge.com/minecraft/mc-mods/mmmmmmmmmmmm)|
|MrCrayfish's Gun Mod [Unofficial]|Firearms, Weapons & Combat|Standard|No|CGM-Unofficial-1.4.18+Forge+1.20.1.jar|An unofficial port of MrCrayfish's Gun Mod \| Note: Unofficial 1.20.1 Forge port replacing MrCrayfish's Gun Mod (v5.5.5).|[Source](https://www.curseforge.com/minecraft/mc-mods/mrcrayfishs-gun-mod-unofficial)|
|Nameless Trinkets|Firearms, Weapons & Combat|Standard|Yes|Nameless Trinkets-1.20.1-1.8.5.jar|Add powerful trinkets, which you will find when exploring the world.|[Source](https://www.curseforge.com/minecraft/mc-mods/nameless-trinkets)|
|ParCool! ~ Minecraft Parkour ~|Firearms, Weapons & Combat|Standard|Yes|ParCool-1.20.1-3.4.1.5.jar|A Mod which add Cool actions and facilities for Parkour|[Source](https://www.curseforge.com/minecraft/mc-mods/parcool)|
|ParCool+ / Compatibility Addon|Firearms, Weapons & Combat|Standard|No|ParCool-CompatibilityAddon-1.20.1-3.4.1.5-1.1.jar|ParCool addon for compatibility with other mods|[Source](https://www.curseforge.com/minecraft/mc-mods/parcool-compatibility-addon)|
|Shots Fired|Firearms, Weapons & Combat|Standard|No|shotsfired-1.20.1-0.2.2.jar|An addon to TaC:Z, and eventually every gun mod, to have guns drop empty casings when fired.|[Source](https://www.curseforge.com/minecraft/mc-mods/shots-fired)|
|TaCZ Ammo Query|Firearms, Weapons & Combat|Standard|No|taczammoquery-1.20.1-1.0.0.jar|This mod allows you to check which gun the ammo is for in JEI|[Source](https://www.curseforge.com/minecraft/mc-mods/tacz-ammo-query)|
|TaCZ Tweaks|Firearms, Weapons & Combat|Standard|No|tacz-tweaks-2.10.0-all.jar|A collection of random tweaks and features to enhance my experience with TaCZ.|[Source](https://www.curseforge.com/minecraft/mc-mods/tacz-tweaks)|
|TACZ: Durability (Timeless and Classics Guns)|Firearms, Weapons & Combat|Standard|No|gundb-2.0.3-all.jar|Adds durability to the Timeless and Classics guns with a jamming and repairing system.|[Source](https://www.curseforge.com/minecraft/mc-mods/tacz-durability)|
|Third Person Shooting: Zero|Firearms, Weapons & Combat|Standard|Yes|tp_shooting-1.20.1-5.1.1+tacz1.1.6-all.jar|Make TAC Guns Compatible with Shoulder Surfing|[Source](https://www.curseforge.com/minecraft/mc-mods/third-person-shooting)|
|Weapon Throw|Firearms, Weapons & Combat|Standard|No|weaponthrow-1.20.1-6.0-beta.1.jar|Throw your Axes or Swords!|[Source](https://www.curseforge.com/minecraft/mc-mods/weapon-throw)|
|[Let's Do] Vinery|Food, Farming & Cooking|Standard|No|letsdo-vinery-forge-1.4.39.jar|Sun-warmed vineyards, creaking barrels and dusty bottles in a cool cellar. Grow your grapes, press your own wine and build the winery of your dreams.|[Source](https://www.curseforge.com/minecraft/mc-mods/lets-do-vinery)|
|AlwaysEat|Food, Farming & Cooking|Standard|No|AlwaysEat-5.2.jar|Gives you the ability to always eat!|[Source](https://www.curseforge.com/minecraft/mc-mods/alwayseat)|
|Create: Central Kitchen|Food, Farming & Cooking|Standard|Yes|create_central_kitchen-1.20.1-for-create-6.0.6-1.4.3b.jar|Automatic Kitchen Work & Integration|[Source](https://www.curseforge.com/minecraft/mc-mods/create-central-kitchen)|
|Diet (Fabric/Forge/Quilt)|Food, Farming & Cooking|Standard|Yes|diet-forge-2.1.1+1.20.1.jar|A customizable food group-based nutrition and diet system.|[Source](https://www.curseforge.com/minecraft/mc-mods/diet)|
|Display Delight|Food, Farming & Cooking|Standard|No|displaydelight-1.1.0.jar|Place all foods from Farmer's Delight in 3D!|[Source](https://www.curseforge.com/minecraft/mc-mods/display-delight)|
|Engineers Delight|Food, Farming & Cooking|Standard|No|Engineers Delight 1.20.1 B.1.4.jar|Adds a bit more integration between Farmers Delight and Immersive Engineering.|[Source](https://www.curseforge.com/minecraft/mc-mods/engineers-delight)|
|Farmer's Delight|Food, Farming & Cooking|Standard|Yes|FarmersDelight-1.20.1-1.2.9.jar|A cozy expansion to farming and cooking!|[Source](https://www.curseforge.com/minecraft/mc-mods/farmers-delight)|
|Fast Leaf Decay|Food, Farming & Cooking|Standard|Yes|FastLeafDecay-32.jar|Makes leaves decay faster when a tree is cut down.|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-leaf-decay)|
|Harvest with ease|Food, Farming & Cooking|Standard|Yes|harvest-with-ease-forge-1.20.1-9.4.0.jar|Don't break crops, right click them!|[Source](https://www.curseforge.com/minecraft/mc-mods/harvest-with-ease)|
|Legacy: [Let's Do] Bakery|Food, Farming & Cooking|Standard|No|letsdo-bakery-forge-1.1.15.jar|Bake many variations of Bread, Cupcakes and Cakes! Eatable, placeable.|[Source](https://www.curseforge.com/minecraft/mc-mods/lets-do-bakery)|
|Spice of Life: Carrot Edition|Food, Farming & Cooking|Standard|Yes|solcarrot-1.20.1-1.15.1.jar|A mod based around food that rewards the player instead of punishing them for discovering new foods!|[Source](https://www.curseforge.com/minecraft/mc-mods/spice-of-life-carrot-edition)|
|Tree Harvester|Food, Farming & Cooking|Standard|Yes|treeharvester-1.20.1-9.1.jar|🌲 Harvest full trees and huge mushrooms instantly with an axe. Includes fast leaf decay and sapling placement. Also works for warped (nether) trees. Become a...|[Source](https://www.curseforge.com/minecraft/mc-mods/tree-harvester)|
|Default Options|Modpack Scripting & Control|Standard|Yes|defaultoptions-forge-1.20.1-18.0.4.jar|Ship default options or keybinds without having to overwrite an existing options.txt.|[Source](https://www.curseforge.com/minecraft/mc-mods/default-options)|
|Default Server Properties|Modpack Scripting & Control|Standard|Yes|default-server-properties-forge-81.1.0.jar|Allows modpack developers to define default server properties. Typically used for things like a default level type.|[Source](https://www.curseforge.com/minecraft/mc-mods/default-server-properties)|
|EntityJS|Modpack Scripting & Control|Standard|No|entityjs-0.5.9-1.20.1.jar|This mod uses KubeJS to dynamically register entities with full AI/Animation/Spawn Control support!|[Source](https://www.curseforge.com/minecraft/mc-mods/entityjs)|
|Global GameRules|Modpack Scripting & Control|Standard|Yes|GlobalGameRules-1.20.1-8.1.0.12.jar|A mod that allows for global/default gamerules|[Source](https://www.curseforge.com/minecraft/mc-mods/global-gamerules)|
|In Control!|Modpack Scripting & Control|Standard|Yes|incontrol-1.20-9.4.5.jar|Be In Control of mob spawns \| Note: In MC 1.20.1+, includes merged functionality of Fx Control! from v5.5.5.|[Source](https://www.curseforge.com/minecraft/mc-mods/in-control)|
|KubeJS|Modpack Scripting & Control|Standard|Yes|kubejs-forge-2001.6.5-build.16.jar|Edit recipes, add new custom items, script world events, all in JavaScript!|[Source](https://www.curseforge.com/minecraft/mc-mods/kubejs)|
|KubeJS Create|Modpack Scripting & Control|Standard|No|kubejs-create-forge-2001.3.0-build.8.jar|KubeJS Create integration|[Source](https://www.curseforge.com/minecraft/mc-mods/kubejs-create)|
|Spawner Control|Modpack Scripting & Control|Standard|No|SpawnerControl-forge-1.20.[1-4]-v1.3.jar|Edit the Monter Spawner speed, delay, range and limit|[Source](https://www.curseforge.com/minecraft/mc-mods/spawner-control)|
|Texture Locale Redirector|Modpack Scripting & Control|Standard|No|Texture-Locale-Redirector-forge-1.20.1+1.6.0.jar|By extending the vanilla resource loading mechanism, it provides native multi-language texture support for resource packs, enabling localization of texture a...|[Source](https://www.curseforge.com/minecraft/mc-mods/texture-locale-redirector)|
|Carry On|Multiplayer, Utility & Admin|Standard|Yes|carryon-forge-1.20.1-2.1.2.7.jar|Carry On allows you to pick up Tile Entities and Mobs and carry them around!|[Source](https://www.curseforge.com/minecraft/mc-mods/carry-on)|
|Chalk|Multiplayer, Utility & Admin|Standard|Yes|chalk-1.20.1-1.6.7.jar|Leave the mark!|[Source](https://www.curseforge.com/minecraft/mc-mods/chalk)|
|Chunky (Forge/NeoForge)|Multiplayer, Utility & Admin|Standard|Yes|Chunky-1.3.146.jar|Pre-generates chunks, quickly, efficiently, and safely|[Source](https://www.curseforge.com/minecraft/mc-mods/chunky-pregenerator-forge)|
|Client Crafting|Multiplayer, Utility & Admin|Standard|Yes|clientcrafting-1.20.1-1.8.jar|Clientside crafting without network delay|[Source](https://www.curseforge.com/minecraft/mc-mods/client-crafting)|
|Controllable|Multiplayer, Utility & Admin|Standard|No|controllable-forge-1.20.1-0.21.7.jar|Play Minecraft Java Edition with a Controller / Gamepad|[Source](https://www.curseforge.com/minecraft/mc-mods/controllable)|
|e4mc|Multiplayer, Utility & Admin|Standard|No|e4mc_minecraft-forge-5.4.1.jar|Open a LAN server to anyone, anywhere, anytime.|[Source](https://www.curseforge.com/minecraft/mc-mods/e4mc)|
|Game Discs|Multiplayer, Utility & Admin|Standard|No|gamediscs-0.3.2-forge.jar|Play game classics inside Minecraft with new Game Console|[Source](https://www.curseforge.com/minecraft/mc-mods/game-discs)|
|Get It Together, Drops!|Multiplayer, Utility & Admin|Standard|Yes|getittogetherdrops-forge-1.20-1.3.jar|Adds tags and configuration options for defining how dropped items should combine.|[Source](https://www.curseforge.com/minecraft/mc-mods/get-it-together-drops)|
|Keerdm's Binoculars|Multiplayer, Utility & Admin|Standard|No|binocularsmod-1.02.jar|A mod that adds a realistic binoculars item.|[Source](https://www.curseforge.com/minecraft/mc-mods/keerdms-binoculars)|
|Log Begone|Multiplayer, Utility & Admin|Standard|Yes|Log-Begone-Forge-1.20.1-1.0.8.jar|Fork of Shut Up Console - Tell those those annoy logs lines begone!|[Source](https://www.curseforge.com/minecraft/mc-mods/log-begone)|
|Longer Chat History [Forge/NeoForge/Fabric]|Multiplayer, Utility & Admin|Standard|No|LongerChatHistory-1.3-Forge.jar|Makes chat history much longer|[Source](https://www.curseforge.com/minecraft/mc-mods/longer-chat-history)|
|Mouse Tweaks|Multiplayer, Utility & Admin|Standard|Yes|MouseTweaks-forge-mc1.20.1-2.25.1.jar|Enhances inventory management by adding various functions to the mouse buttons.|[Source](https://www.curseforge.com/minecraft/mc-mods/mouse-tweaks)|
|Open Parties and Claims|Multiplayer, Utility & Admin|Standard|Yes|open-parties-and-claims-forge-1.20.1-0.25.8.jar|Adds the ability to claim chunks and make player parties, integrates with Xaero's Minimap and World Map|[Source](https://www.curseforge.com/minecraft/mc-mods/open-parties-and-claims)|
|Polymorph|Multiplayer, Utility & Admin|Standard|Yes|polymorph-forge-0.49.10+1.20.1.jar|No more recipe conflicts! Adds an option to choose the crafting result if more than one is available.|[Source](https://www.curseforge.com/minecraft/mc-mods/polymorph)|
|Recipe Essentials|Multiplayer, Utility & Admin|Standard|No|recipeessentials-1.20.1-4.0.jar|Recipe Essentials improves recipe processing, item comparisons, and the vanilla recipe book|[Source](https://www.curseforge.com/minecraft/mc-mods/recipe-essentials-forge-fabric)|
|Simple Voice Chat|Multiplayer, Utility & Admin|Standard|Yes|voicechat-forge-1.20.1-2.5.34.jar|A working voice chat in Minecraft!|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-voice-chat)|
|spark|Multiplayer, Utility & Admin|Standard|Yes|spark-1.10.53-forge.jar|spark is a performance profiler for Minecraft clients, servers and proxies.|[Source](https://www.curseforge.com/minecraft/mc-mods/spark)|
|StackablePotions [Forge]|Multiplayer, Utility & Admin|Standard|Yes|Stackable Potions-forge-1.20.1-1.0.0.jar|Allows vanilla potions to stack.|[Source](https://www.curseforge.com/minecraft/mc-mods/stackablepotions-forge)|
|AI Improvements: Performance Tuning|Performance & Optimization|Standard|Yes|AI-Improvements-1.20-0.5.2.jar|Performance and logic upgrades for mod AIs|[Source](https://www.curseforge.com/minecraft/mc-mods/ai-improvements)|
|Alternate Current|Performance & Optimization|Standard|Yes|alternate_current-mc1.20-1.7.0.jar|An efficient and non-locational redstone dust implementation|[Source](https://www.curseforge.com/minecraft/mc-mods/alternate-current)|
|BadOptimizations|Performance & Optimization|Standard|No|BadOptimizations-2.2.3-1.20.1.jar|Optimization mod that focuses on things other than rendering|[Source](https://www.curseforge.com/minecraft/mc-mods/badoptimizations)|
|Bocchium|Performance & Optimization|Standard|No|bocchium-1.20.1-0.0.3.jar|Forge port of Bedrodium, culling bedrock sides for better performance.|[Source](https://www.curseforge.com/minecraft/mc-mods/bocchium)|
|Clumps|Performance & Optimization|Standard|Yes|Clumps-forge-1.20.1-12.0.0.4.jar|Clumps XP orbs together to reduce lag|[Source](https://www.curseforge.com/minecraft/mc-mods/clumps)|
|Colorwheel|Performance & Optimization|Standard|No|colorwheel-forge-1.1.1+mc1.20.1.jar|Allows you to use Iris Shaders with Flywheel \| Note: Replaces Iris & Oculus Flywheel Compat (v5.5.5) for Create + shaders.|[Source](https://www.curseforge.com/minecraft/mc-mods/colorwheel)|
|Colorwheel Patcher|Performance & Optimization|Standard|No|colorwheel_patcher-forge-1.0.3+mc1.20.1.jar|Autopatch supported shaderpacks for Colorwheel|[Source](https://www.curseforge.com/minecraft/mc-mods/colorwheel-patcher)|
|Create Better FPS|Performance & Optimization|Standard|No|createbetterfps-1.20.1-1.1.1.jar|Improve your Create FPS, up to 50%|[Source](https://www.curseforge.com/minecraft/mc-mods/create-better-fps)|
|CullLessLeaves Reforged (Unofficial)|Performance & Optimization|Standard|Yes|CullLessLeaves-Reforged-1.20.1-1.0.5.jar|Gives you a 9% fps improvement for leaves rendering|[Source](https://www.curseforge.com/minecraft/mc-mods/culllessleaves-reforged)|
|Distant Horizons: A Level of Detail mod|Performance & Optimization|DH Edition Extra|No|DistantHorizons-2.4.5-b-1.20.1-fabric-forge.jar|Massively increase render distance without harming performance. \| Note: ONLY included in DeceasedCraft_Beta_DH_Edition-5.10.17 (not in Standard Beta 5.10.17).|[Source](https://www.curseforge.com/minecraft/mc-mods/distant-horizons)|
|Embeddium|Performance & Optimization|Standard|Yes|embeddium-0.3.31+mc1.20.1.jar|A powerful, mod-friendly, FOSS client performance mod for NeoForge|[Source](https://www.curseforge.com/minecraft/mc-mods/embeddium)|
|Entity Culling Fabric/Forge|Performance & Optimization|Standard|Yes|entityculling-forge-1.9.4-mc1.20.1.jar|Using async path-tracing to hide BlockEntities/Entities that are not visible|[Source](https://www.curseforge.com/minecraft/mc-mods/entityculling)|
|Fast Async World Save[Forge/Neo/Fabric]|Performance & Optimization|Standard|Yes|fastasyncworldsave-1.20.1-2.6.jar|Prevent lag-spikes and data loss during intermittent world saves|[Source](https://www.curseforge.com/minecraft/mc-mods/fast-async-world-save-forge-fabric)|
|FastBoot|Performance & Optimization|Standard|No|fastboot-1.20.x-1.2.jar|FastBoot: Accelerate Your Game Loading Time|[Source](https://www.curseforge.com/minecraft/mc-mods/fastboot)|
|FastFurnace|Performance & Optimization|Standard|Yes|FastFurnace-1.20.1-8.0.2.jar|A performance upgrade for the furnace.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastfurnace)|
|Fastload|Performance & Optimization|Standard|No|Fastload-Reforged-mc1.20.1-3.4.0.jar|Modifies how worlds are loaded to speed up loading times.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastload)|
|FastSuite|Performance & Optimization|Standard|Yes|FastSuite-1.20.1-5.1.0.jar|A performance upgrade for the JSON recipe system.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastsuite)|
|FastWorkbench|Performance & Optimization|Standard|Yes|FastWorkbench-1.20.1-8.0.4.jar|A performance upgrade for the crafting table.|[Source](https://www.curseforge.com/minecraft/mc-mods/fastworkbench)|
|FerriteCore ((Neo)Forge)|Performance & Optimization|Standard|Yes|ferritecore-6.0.1-forge.jar|Memory usage optimizations|[Source](https://www.curseforge.com/minecraft/mc-mods/ferritecore)|
|Flerovium|Performance & Optimization|Standard|No|flerovium-forge-1.20.1-1.2.16-all.jar|Greatly improve your fps with virtually no side-effects on graphics quality|[Source](https://www.curseforge.com/minecraft/mc-mods/flerovium)|
|Icterine|Performance & Optimization|Standard|No|Icterine-forge-1.20.0-1-1.3.0.jar|Advancements optimization (specifically, InventoryChangeTrigger)|[Source](https://www.curseforge.com/minecraft/mc-mods/icterine)|
|ImmediatelyFast|Performance & Optimization|Standard|No|ImmediatelyFast-Forge-1.5.1+1.20.4.jar|Speed up immediate mode rendering in Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/immediatelyfast)|
|Immersive Optimization|Performance & Optimization|Standard|No|immersive_optimization-forge-1.20.1-0.1.0.jar|A lightweight entity-tick-scheduler for doubling your TPS.|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-optimization)|
|lazyyyyy|Performance & Optimization|Standard|No|lazyyyyy-lexforge-core-0.14.19.jar|Mainly optimize the game launching time for large pack|[Source](https://www.curseforge.com/minecraft/mc-mods/lazyyyyy)|
|Let Me Despawn|Performance & Optimization|Standard|No|letmedespawn-1.20.x-forge-1.5.0.jar|Improves performance by tweaking mob despawn rules.|[Source](https://www.curseforge.com/minecraft/mc-mods/let-me-despawn)|
|MCreatorMemFix|Performance & Optimization|Standard|No|MCreatorMemFix-1.0.4.jar|Fixes a large memory allocation bug in some MCreator mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/mcreatormemfix)|
|Mobtimizations - Entity Performance Fixes|Performance & Optimization|Standard|Yes|mobtimizations-forge-1.20.1-1.0.0.jar|Optimizes a lot of tasks that Entity AI wastefully performs, minimal effect on gameplay.|[Source](https://www.curseforge.com/minecraft/mc-mods/mobtimizations)|
|ModernFix|Performance & Optimization|Standard|Yes|modernfix-forge-5.25.1+mc1.20.1.jar|All-in-one mod that improves performance, reduces memory usage, and fixes many bugs. Compatible with all your favorite performance mods!|[Source](https://www.curseforge.com/minecraft/mc-mods/modernfix)|
|Oculus|Performance & Optimization|Standard|Yes|oculus-mc1.20.1-1.8.0.jar|Unofficial Fork of "Iris", made to work with FML|[Source](https://www.curseforge.com/minecraft/mc-mods/oculus)|
|Radium Reforged|Performance & Optimization|Standard|No|radium-mc1.20.1-0.12.4+git.26c9d8e.jar|Unofficial Fork of CaffeineMC's "Lithium", made to work with FML \| Note: Replaces Canary (v5.5.5) as Lithium Forge fork.|[Source](https://www.curseforge.com/minecraft/mc-mods/radium-reforged)|
|Redirected|Performance & Optimization|Standard|No|redirected-forge-1.0.0-1.20.1.jar|Memory optimization mod that prevents duplication of Enum values|[Source](https://www.curseforge.com/minecraft/mc-mods/redirected)|
|Saturn|Performance & Optimization|Standard|Yes|saturn-mc1.20.1-0.1.3.jar|A performance mod designed to optimize Minecraft's memory usage.|[Source](https://www.curseforge.com/minecraft/mc-mods/saturn)|
|Server Performance - Smooth Chunk Save|Performance & Optimization|Standard|Yes|smoothchunk-1.20.1-4.1.jar|Enables lag-free continuous chunk saving, increasing server TPS|[Source](https://www.curseforge.com/minecraft/mc-mods/smooth-chunk-save)|
|Smooth Boot (Reloaded)|Performance & Optimization|Standard|Yes|smoothboot(reloaded)-mc1.20.1-0.0.4.jar|Tweaks for Minecraft CPU scheduling and unofficial fork of Smooth Boot mod for Minecraft Forge 1.18.2+|[Source](https://www.curseforge.com/minecraft/mc-mods/smooth-boot-reloaded)|
|Vanillin|Performance & Optimization|Standard|No|vanillin-forge-1.20.1-1.1.3.jar|Instanced rendering for entities and block entities.|[Source](https://www.curseforge.com/minecraft/mc-mods/vanillin)|
|CustomNPCs-Unofficial|Quests, Progression & NPCs|Standard|No|CustomNPCs-1.20.1-GBPort-Unofficial-20251031.jar|Unofficial version of CustomNPCs mod ported to the newer versions of Minecraft|[Source](https://www.curseforge.com/minecraft/mc-mods/customnpcs-unofficial)|
|FTB Quests (NeoForge)|Quests, Progression & NPCs|Standard|Yes|ftb-quests-forge-2001.4.16.jar|Questing Mod by FTB|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge)|
|FTB Teams (NeoForge)|Quests, Progression & NPCs|Standard|Yes|ftb-teams-forge-2001.3.1.jar|Library for mods that can utilize team progression|[Source](https://www.curseforge.com/minecraft/mc-mods/ftb-teams-forge)|
|Merge Enchantments|Quests, Progression & NPCs|Standard|No|MergeEnchantments-FORGE-1.20.[0-4]-v4.3.jar|merge the enchants that could not be combined like Silk Touch with Fortune, Infinity with Mending, Frost Walker with Depth Strider|[Source](https://www.curseforge.com/minecraft/mc-mods/merge-enchantments)|
|Pufferfish's Attributes [Fabric & Forge & NeoForge]|Quests, Progression & NPCs|Standard|No|puffish_attributes-0.7.6-1.20-forge.jar|Adds more attributes to the game.|[Source](https://www.curseforge.com/minecraft/mc-mods/puffish-attributes)|
|Pufferfish's Skills [Fabric & Forge & NeoForge]|Quests, Progression & NPCs|Standard|Yes|puffish_skills-0.16.5-1.20-forge.jar|Adds a fully configurable skill system to the game.|[Source](https://www.curseforge.com/minecraft/mc-mods/puffish-skills)|
|Quests Kill Task Tweaks|Quests, Progression & NPCs|Standard|No|Quest Kill Task-0.2.0+1.20.1-forge.jar|Improves kill contribution tracking for FTB Quests|[Source](https://www.curseforge.com/minecraft/mc-mods/quests-kill-task-tweaks)|
|Resistance Balancer (Modpack Utils Series)|Quests, Progression & NPCs|Standard|No|ResistanceBalancer-(NEO)FORGE-1.0.0.jar|Allows to add a custom formula (or change the damge percentage it reduces) of the Resistance status effect.|[Source](https://www.curseforge.com/minecraft/mc-mods/resistance-balancer)|
|Starter Kit|Quests, Progression & NPCs|Standard|Yes|starterkit-1.20.1-7.4.jar|📦 Give all new players joining the world configurable starter gear, items, potion effects, Curios and Trinkets slots and/or commands. Compatible with FTB Tea...|[Source](https://www.curseforge.com/minecraft/mc-mods/starter-kit)|
|Tax Free Levels|Quests, Progression & NPCs|Standard|No|TaxFreeLevels-1.4.14-forge-1.20.1.jar|Flattens the ever-increasing anvil and enchantment costs and makes renaming items always cost 1 level|[Source](https://www.curseforge.com/minecraft/mc-mods/tax-free-levels)|
|Corpse|Storage, Loot & Backpacks|Standard|Yes|corpse-forge-1.20.1-1.0.21.jar|Never lose your items again!|[Source](https://www.curseforge.com/minecraft/mc-mods/corpse)|
|Corpse x Curios API Compat|Storage, Loot & Backpacks|Standard|No|corpsecurioscompat-1.20.1-Forge-3.1.2.jar|Adds Curios API support to Corpse|[Source](https://www.curseforge.com/minecraft/mc-mods/corpse-x-curios-api-compat)|
|Lootr (Forge & NeoForge)|Storage, Loot & Backpacks|Standard|Yes|lootr-forge-1.20-0.7.35.94.jar|A mod that makes it so nobody misses out on Loot! All loot chests are instanced per player and visually unique.|[Source](https://www.curseforge.com/minecraft/mc-mods/lootr)|
|Refined Polymorphism|Storage, Loot & Backpacks|Standard|No|refinedpolymorph-0.1.1-1.20.1.jar|Polymorph support for Refined Storage.|[Source](https://www.curseforge.com/minecraft/mc-mods/refined-polymorphism)|
|Refined Storage|Storage, Loot & Backpacks|Standard|Yes|refinedstorage-1.12.4.jar|An elegant solution to your hoarding problem.|[Source](https://www.curseforge.com/minecraft/mc-mods/refined-storage)|
|Refined Storage Addons|Storage, Loot & Backpacks|Standard|No|refinedstorageaddons-0.10.0.jar|An addon mod for Refined Storage.|[Source](https://www.curseforge.com/minecraft/mc-mods/refined-storage-addons)|
|Sophisticated Backpacks|Storage, Loot & Backpacks|Standard|Yes|sophisticatedbackpacks-1.20.1-3.24.10.1404.jar|Yet another backpack mod this time with backpack you can place in world, color in different color combinations, upgrade with more inventory and enhance with...|[Source](https://www.curseforge.com/minecraft/mc-mods/sophisticated-backpacks)|
|Storage Drawers|Storage, Loot & Backpacks|Standard|Yes|StorageDrawers-1.20.1-12.9.14.jar|Interactive compartment storage for your workshops.|[Source](https://www.curseforge.com/minecraft/mc-mods/storage-drawers)|
|Trash Cans|Storage, Loot & Backpacks|Standard|Yes|trashcans-1.0.18b-forge-mc1.20.jar|Trash Cans adds trash cans which can be used to void items, liquids, and energy!|[Source](https://www.curseforge.com/minecraft/mc-mods/trash-cans)|
|TrashSlot|Storage, Loot & Backpacks|Standard|Yes|trashslot-forge-1.20-15.1.2.jar|Adds a draggable trash slot to all inventory screens. Press T to toggle.|[Source](https://www.curseforge.com/minecraft/mc-mods/trashslot)|
|XP Tome|Storage, Loot & Backpacks|Standard|Yes|xptome-1.20.1-2.2.1.jar|Adds a book that can store a configurable amount of XP.|[Source](https://www.curseforge.com/minecraft/mc-mods/xp-tome)|
|Comforts|Survival, Health & Environment|Standard|Yes|comforts-forge-6.4.0+1.20.1.jar|Adds sleeping bags and hammocks for, respectively, portability and turning day to night, without setting new spawns. Comes in 16 different colors!|[Source](https://www.curseforge.com/minecraft/mc-mods/comforts)|
|Legendary Survival Overhaul|Survival, Health & Environment|Standard|No|legendarysurvivaloverhaul-1.20.1-2.3.23.1.jar|Temperature, thirst, limbs management, health overhaul for Survival game ! \| Note: Replaces First Aid + Thirst Was Taken + Cold Sweat from v5.5.5 (unified limbs, thirst, temperature).|[Source](https://www.curseforge.com/minecraft/mc-mods/legendary-survival-overhaul)|
|Serene Seasons|Survival, Health & Environment|Standard|Yes|SereneSeasons-forge-1.20.1-9.1.0.2.jar|Seasons with changing colors, shifting temperatures, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/serene-seasons)|
|CFM Refurbished: Watt About Power?|Tech, Automation & Power|Standard|No|cfm_wap-1.20.1-forge-1.2.0.jar|Introduces a circuit breaker block that powers the electricity network in "MrCrayfish's Furniture Mod: Refurbished" using energy from other mods.|[Source](https://www.curseforge.com/minecraft/mc-mods/cfm-wap)|
|Click Machine|Tech, Automation & Power|Standard|Yes|ClickMachine-1.20.1-8.0.2.jar|A simple, standalone, auto-clicker.|[Source](https://www.curseforge.com/minecraft/mc-mods/click-machine)|
|Create|Tech, Automation & Power|Standard|Yes|create-1.20.1-6.0.6.jar|Aesthetic Technology that empowers the Player|[Source](https://www.curseforge.com/minecraft/mc-mods/create)|
|Create Crafts & Additions|Tech, Automation & Power|Standard|Yes|createaddition-1.20.1-1.3.2.jar|Electrifying the Create mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/createaddition)|
|Create Stuff 'N Additions|Tech, Automation & Power|Standard|Yes|create-stuff-additions1.20.1_v2.1.0.jar|🧲 Dominate your environment with Create technology|[Source](https://www.curseforge.com/minecraft/mc-mods/create-stuff-additions)|
|Create: Diesel Generators|Tech, Automation & Power|Standard|No|createdieselgenerators-1.20.1-1.3.5.jar|A Create addon that adds compact diesel generators (engines), simple industrial features and crude oil refinery|[Source](https://www.curseforge.com/minecraft/mc-mods/create-diesel-generators)|
|Create: Hypertubes|Tech, Automation & Power|Standard|No|create_hypertube-0.2.5-FORGE.jar|Travel arround the world with tubes!|[Source](https://www.curseforge.com/minecraft/mc-mods/hypertubes)|
|Create: Radars|Tech, Automation & Power|Standard|No|Radars 0.3.5.1-Create6.jar|Adding advanced surveillance technologies to Create!|[Source](https://www.curseforge.com/minecraft/mc-mods/create-radars)|
|Engineered Schematics|Tech, Automation & Power|Standard|No|EngineeredSchematics-1.2.3.jar|A Mod desgined to make building multiblocks more clear.|[Source](https://www.curseforge.com/minecraft/mc-mods/engineered-schematics)|
|Extreme Reactors|Tech, Automation & Power|Standard|No|ExtremeReactors2-1.20.1-2.0.94.jar|This is a port of the Big Reactors mod by Erogenous Beef to the current Minecraft versions|[Source](https://www.curseforge.com/minecraft/mc-mods/extreme-reactors)|
|Immersive Engineering|Tech, Automation & Power|Standard|Yes|ImmersiveEngineering-1.20.1-10.2.0-183.jar|A retro-futuristic tech mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-engineering)|
|Item Scrapper|Tech, Automation & Power|Standard|No|item_scrapper-1.2.9.jar|Adds a scrapping workbench (Fully configureble with JSON data)|[Source](https://www.curseforge.com/minecraft/mc-mods/item-scrapper)|
|Pipez|Tech, Automation & Power|Standard|Yes|pipez-forge-1.20.1-1.2.21.jar|Simple and efficient pipes|[Source](https://www.curseforge.com/minecraft/mc-mods/pipez)|
|Security Craft|Tech, Automation & Power|Standard|Yes|[1.20.1] SecurityCraft v1.9.12.jar|Adds plenty of blocks and items to defend and secure your base with.|[Source](https://www.curseforge.com/minecraft/mc-mods/security-craft)|
|Wormhole (Portals)|Tech, Automation & Power|Standard|No|wormhole-1.1.16-forge-mc1.20.jar|Wormhole allows you to construct teleportation portals with the use of wormhole stabilizer technology!|[Source](https://www.curseforge.com/minecraft/mc-mods/wormhole-portals)|
|Advancement Plaques [Neo/Forge]|UI, HUD, Maps & Info|Standard|No|AdvancementPlaques-1.20.1-forge-1.6.9.jar|Replace those boring advancement popups with something flashier.|[Source](https://www.curseforge.com/minecraft/mc-mods/advancement-plaques)|
|AppleSkin|UI, HUD, Maps & Info|Standard|Yes|appleskin-forge-mc1.20.1-2.5.1.jar|Adds some useful information about food/hunger to the HUD|[Source](https://www.curseforge.com/minecraft/mc-mods/appleskin)|
|Armor Points ++|UI, HUD, Maps & Info|Standard|Yes|armorpointspp-forge-1.20-3.1.1.jar|Allows you to see armor values above 20 and stack multiple health bars onto one.|[Source](https://www.curseforge.com/minecraft/mc-mods/armorpoints)|
|Better Advancements|UI, HUD, Maps & Info|Standard|Yes|BetterAdvancements-Forge-1.20.1-0.4.2.10.jar|Successor to BetterAchievements for the new advancements system in minecraft 1.12+|[Source](https://www.curseforge.com/minecraft/mc-mods/better-advancements)|
|Better Compatibility Checker|UI, HUD, Maps & Info|Standard|Yes|BetterCompatibilityChecker-forge-4.0.8+mc1.20.1.jar|Changes the default server compatability check to compare modpack versions|[Source](https://www.curseforge.com/minecraft/mc-mods/better-compatibility-checker)|
|Catalogue|UI, HUD, Maps & Info|Standard|No|catalogue-forge-1.20.1-1.8.0.jar|A universal mod list menu for all modloaders!|[Source](https://www.curseforge.com/minecraft/mc-mods/catalogue)|
|Configured|UI, HUD, Maps & Info|Standard|Yes|configured-forge-1.20.1-2.2.3.jar|Automatic in-game configuration menus for every mod!|[Source](https://www.curseforge.com/minecraft/mc-mods/configured)|
|Controlling|UI, HUD, Maps & Info|Standard|Yes|Controlling-forge-1.20.1-12.0.2.jar|Adds a search bar to the Key-Bindings menu|[Source](https://www.curseforge.com/minecraft/mc-mods/controlling)|
|Drippy Loading Screen|UI, HUD, Maps & Info|Standard|No|drippyloadingscreen_forge_3.1.0_MC_1.20.1.jar|Addon for FancyMenu to customize the loading screen.|[Source](https://www.curseforge.com/minecraft/mc-mods/drippy-loading-screen)|
|Durability Tooltip|UI, HUD, Maps & Info|Standard|Yes|durabilitytooltip-1.1.6-forge-mc1.20.jar|Durability Tooltip shows you the durability of an item!|[Source](https://www.curseforge.com/minecraft/mc-mods/durability-tooltip)|
|Enchantment Descriptions|UI, HUD, Maps & Info|Standard|Yes|EnchantmentDescriptions-Forge-1.20.1-17.1.19.jar|Adds in-game descriptions for enchantments to tooltips.|[Source](https://www.curseforge.com/minecraft/mc-mods/enchantment-descriptions)|
|Equipment Compare [Neo/Forge]|UI, HUD, Maps & Info|Standard|Yes|EquipmentCompare-1.20.1-forge-1.3.7.jar|Makes it easier to compare equipment by showing a tooltip for what you're already wearing.|[Source](https://www.curseforge.com/minecraft/mc-mods/equipment-compare)|
|FancyMenu|UI, HUD, Maps & Info|Standard|No|fancymenu_forge_3.8.1_MC_1.20.1.jar|Customize Minecraft's menus with ease!|[Source](https://www.curseforge.com/minecraft/mc-mods/fancymenu)|
|Immersive UI|UI, HUD, Maps & Info|Standard|No|ImmersiveUI-FORGE-0.3.0.jar|Enhance your gameplay experience with animated UI components|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-ui)|
|Inventory HUD+|UI, HUD, Maps & Info|Standard|No|inventoryhud.forge.1.20.1-3.4.26.jar|Adds your main inventory, potion effects and your equipments to your HUD. And few other features.|[Source](https://www.curseforge.com/minecraft/mc-mods/inventory-hud-forge)|
|Item Highlighter [Neo/Forge]|UI, HUD, Maps & Info|Standard|No|Highlighter-1.20.1-forge-1.1.9.jar|Highlights newly picked-up items. Simple and convenient.|[Source](https://www.curseforge.com/minecraft/mc-mods/item-highlighter)|
|Just Enough Immersive Multiblocks|UI, HUD, Maps & Info|Standard|Yes|jeimultiblocks-1.20.1-1.0.6.jar|Immersive Engineering addon that adds JEI support for multiblocks.|[Source](https://www.curseforge.com/minecraft/mc-mods/just-enough-immersive-multiblocks)|
|Just Enough Items (JEI)|UI, HUD, Maps & Info|Standard|Yes|jei-1.20.1-forge-15.20.0.112.jar|View Items and Recipes|[Source](https://www.curseforge.com/minecraft/mc-mods/jei)|
|Legendary Tabs|UI, HUD, Maps & Info|Standard|No|legendarytabs-1.20.1-1.1.3.1.jar|Introducing tabs in your inventory to easily switch between menus|[Source](https://www.curseforge.com/minecraft/mc-mods/legendary-tabs)|
|Loot Journal: Pickup Notifier 🧩 Forge|UI, HUD, Maps & Info|Standard|No|Loot Journal-forge-1.20.1-5.0.1.jar|Ultimate item pick-up notifier featuring rich animations, full theming support, customizable layouts, and powerful filtering options!|[Source](https://www.curseforge.com/minecraft/mc-mods/loot-journal)|
|Moderately Enough Effect Descriptions (MEED)|UI, HUD, Maps & Info|Standard|No|MEED-1.20.1-6.7.jar|JEED/Emiffect addon with support for over 100 mods and 600 status effects!|[Source](https://www.curseforge.com/minecraft/mc-mods/moderately-enough-effect-descriptions-meed)|
|Not Enough Recipe Book [NERB]|UI, HUD, Maps & Info|Standard|Yes|Not Enough Recipe Book-FORGE-0.4.1+1.20.1.jar|Completely removes recipe book from the game, optimizing player data.|[Source](https://www.curseforge.com/minecraft/mc-mods/notenoughrecipebook)|
|Scholar|UI, HUD, Maps & Info|Standard|No|scholar-1.20.1-1.1.5.1-forge.jar|Two-page book editing/viewing, easy formatting, colored books, literate mobs and other book-related improvements|[Source](https://www.curseforge.com/minecraft/mc-mods/scholar)|
|Stylish Effects|UI, HUD, Maps & Info|Standard|No|StylishEffects-v8.0.2-1.20.1-Forge.jar|Status effect display overhaul: Display them in any menu! And way more compact.|[Source](https://www.curseforge.com/minecraft/mc-mods/stylish-effects)|
|The One Probe|UI, HUD, Maps & Info|Standard|Yes|theoneprobe-1.20.1-10.0.3.jar|More immersive alternative for WAILA|[Source](https://www.curseforge.com/minecraft/mc-mods/the-one-probe)|
|Traveler's Titles (Forge/NeoForge)|UI, HUD, Maps & Info|Standard|No|TravelersTitles-1.20-Forge-4.0.2.jar|Epic, RPG-like titles when entering biomes & dimensions!|[Source](https://www.curseforge.com/minecraft/mc-mods/travelers-titles)|
|Xaero's Minimap|UI, HUD, Maps & Info|Standard|No|Xaeros_Minimap_25.2.10_Forge_1.20.jar|Displays the nearby world terrain, players, mobs, entities in the corner of your screen. Lets you create waypoints which help you find the locations you've m... \| Note: Replaces Xaero's Minimap (Fair-play Edition) from v5.5.5.|[Source](https://www.curseforge.com/minecraft/mc-mods/xaeros-minimap)|
|Xaero's World Map|UI, HUD, Maps & Info|Standard|Yes|XaerosWorldMap_1.39.12_Forge_1.20.jar|Adds a fullscreen worldmap which shows you what you have explored in the world. Can work together with Xaero's Minimap.|[Source](https://www.curseforge.com/minecraft/mc-mods/xaeros-world-map)|
|YTonGame|UI, HUD, Maps & Info|Standard|No|ytongame_hostingmenu-1.0.1.jar|YTonGame Server List Integration Menu for Modpacks [FORGE ONLY]|[Source](https://www.curseforge.com/minecraft/mc-mods/ytongame)|
|DragN's Valiant Vehicles!|Vehicles & Transport|Standard|No|DragN_Vehicles-1.20.1-1.3.2.jar|A small mod that adds a few new, drivable vehicles and functional trailers! \| Note: Replaces Ultimate Car Mod (v5.5.5) for ground vehicles.|[Source](https://www.curseforge.com/minecraft/mc-mods/dragns-valiant-vehicles)|
|DragN's VV: Refueled|Vehicles & Transport|Standard|No|refueled-1.20.1-2.4.2.jar|Adding a way to fuel DragN's Valiant Vehicles and more|[Source](https://www.curseforge.com/minecraft/mc-mods/dragns-vv-refueled)|
|Immersive Aircraft|Vehicles & Transport|Standard|No|immersive_aircraft-1.4.0+1.20.1-forge.jar|A set of vanilla style, customizable and upgradable aircraft, from biplanes to airships|[Source](https://www.curseforge.com/minecraft/mc-mods/immersive-aircraft)|
|Simple Planes (NeoForge)|Vehicles & Transport|Standard|Yes|simpleplanes-1.20.1-5.3.3.jar|Upgradeable planes and helicopters which you can fly with.|[Source](https://www.curseforge.com/minecraft/mc-mods/simple-planes)|
|Biome Replacer|Worldgen, Cities & Structures|Standard|No|biomereplacer-2.1-hippo-forge.jar|A quick way to get rid of a biome. Useful for tweaking datapack-based generators (like Terralith) that don't have a convenient configuration.|[Source](https://www.curseforge.com/minecraft/mc-mods/biome-replacer)|
|Biome Sizes|Worldgen, Cities & Structures|Standard|No|biomesize-1.20.1-1.5.jar|Customize Biome Size settings per dimension|[Source](https://www.curseforge.com/minecraft/mc-mods/biomesize)|
|Biome Spawn Point|Worldgen, Cities & Structures|Standard|Yes|biomespawnpoint-1.20.1-2.4.jar|🌲 Allows specifying which biome and dimension players will spawn in on new world creation.|[Source](https://www.curseforge.com/minecraft/mc-mods/biome-spawn-point)|
|Biomes O' Plenty|Worldgen, Cities & Structures|Standard|Yes|BiomesOPlenty-forge-1.20.1-19.0.0.96.jar|Adds 50+ unique biomes to enhance your world, with new trees, flowers, and more!|[Source](https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty)|
|Horror Elements mod|Worldgen, Cities & Structures|Standard|No|horror_element_mod-1.6.2-forge-1.20.1.jar|A mod that adds decorative blocks for your horror maps and spooky structures for your survival world|[Source](https://www.curseforge.com/minecraft/mc-mods/horror-elements-mod)|
|Lost Radar|Worldgen, Cities & Structures|Standard|No|lostradar-1.20-1.1.0.jar|Lost Radar is a companion mod for Lost Cities that adds an item that can be used to find and discover buildings|[Source](https://www.curseforge.com/minecraft/mc-mods/lost-radar)|
|Lost Worlds LC|Worldgen, Cities & Structures|Standard|No|lostworlds-1.20-0.0.3.jar|Lost Worlds companion mod for Lost Cities|[Source](https://www.curseforge.com/minecraft/mc-mods/lost-worlds-lc)|
|Nature's Compass|Worldgen, Cities & Structures|Standard|Yes|NaturesCompass-1.20.1-1.11.2-forge.jar|Nature's Compass is an item that allows you to locate biomes anywhere in the world.|[Source](https://www.curseforge.com/minecraft/mc-mods/natures-compass)|
|The Lost Cities|Worldgen, Cities & Structures|Standard|Yes|lostcities-1.20-7.4.11.jar|The Lost Cities is a world generation mod|[Source](https://www.curseforge.com/minecraft/mc-mods/the-lost-cities)|
|This Rocks! (Forge)|Worldgen, Cities & Structures|Standard|Yes|ThisRocks-1.20.1-1.5.1.jar|Adds little rocks, sticks, pinecones, seashells, starfish, and geysers to your minecraft world to make it feel more natural.|[Source](https://www.curseforge.com/minecraft/mc-mods/this-rocks-forge)|
|Animal Pens|Zombies, Mobs & Wildlife|Standard|No|animal_pen-forge-1.20-1.6.1.jar|Reduce lag and keep your animals neatly stored while maintaining full interactivity!|[Source](https://www.curseforge.com/minecraft/mc-mods/animal-pens)|
|Critters and Companions|Zombies, Mobs & Wildlife|Standard|Yes|crittersandcompanions-forge-1.20.1-2.3.5.jar|Adds a few new friends to your world!|[Source](https://www.curseforge.com/minecraft/mc-mods/critters-and-companions)|
|Enhanced AI|Zombies, Mobs & Wildlife|Standard|Yes|enhancedai-2.6.8.jar|Creepers Breaching, Zombies mining and Skeletons sniping. Customize their AI as you like!|[Source](https://www.curseforge.com/minecraft/mc-mods/enhanced-ai)|
|Enhanced Hordes|Zombies, Mobs & Wildlife|Standard|Yes|eh1.3.1-1.20.1.jar|Enhances zombie's ability to cooperate, among other mobs.|[Source](https://www.curseforge.com/minecraft/mc-mods/enhanced-hordes)|
|Fungal Infection: Spore|Zombies, Mobs & Wildlife|Standard|No|spore_2.1.5c_1.20.1.jar|It adds an aggressive fungal infection|[Source](https://www.curseforge.com/minecraft/mc-mods/fungal-infection-spore)|
|Lost Souls|Zombies, Mobs & Wildlife|Standard|Yes|lostsouls-1.20-4.1.6.jar|Lost Souls is an addon mod for The Lost Cities to add more danger to the buildings|[Source](https://www.curseforge.com/minecraft/mc-mods/lost-souls)|
|Mob Sunscreen|Zombies, Mobs & Wildlife|Standard|Yes|mobsunscreen-forge-1.20.1-3.1.1.jar|Stop Zombies and Skeletons from Burning in the Sun!|[Source](https://www.curseforge.com/minecraft/mc-mods/mob-sunscreen)|
|Naturalist|Zombies, Mobs & Wildlife|Standard|No|naturalist-5.0pre2+forge-1.20.1.jar|Adds 47 animals *(and 66 variants)* to your world with immersive behaviors and drops.|[Source](https://www.curseforge.com/minecraft/mc-mods/naturalist)|
|The Hordes|Zombies, Mobs & Wildlife|Standard|Yes|The-Hordes-1.20.1-1.5.4c.jar|Horde Invasions and Zombie Infection|[Source](https://www.curseforge.com/minecraft/mc-mods/the-hordes)|
|THE UNDEAD REVAMPED|Zombies, Mobs & Wildlife|Standard|Yes|THEUNDEADREVAMPED_1.9O_1.20.1.jar|This mod add some new types of undeads.|[Source](https://www.curseforge.com/minecraft/mc-mods/theundead)|
|Voiceless Survival|Zombies, Mobs & Wildlife|Standard|No|ezvcsurvival-forge-1.20.1-1.4.2.jar|Be careful, the mobs can hear you🤫|[Source](https://www.curseforge.com/minecraft/mc-mods/voiceless-survival)|
|Zombie Awareness|Zombies, Mobs & Wildlife|Standard|Yes|zombieawareness-1.20.1-1.13.1.jar|- Smarter more aware zombies (and skeletons), they track you down via blood scent, sound, and light source awareness|[Source](https://www.curseforge.com/minecraft/mc-mods/zombie-awareness)|
|Zombie Extreme|Zombies, Mobs & Wildlife|Standard|Yes|Zombie Extreme 1.20.1 0.2.6.jar|This is a Big Mod that adds a bunch of new mechanics and a large number of zombies and infected to your minecraft world. In order to study a new biome, you n...|[Source](https://www.curseforge.com/minecraft/mc-mods/zombie-extreme)|

### 16.3 Cross-version engineering implications

The workbook's comparison sheet highlights the following areas. Treat these as architecture guidance and research leads; validate each against the exact target archive and API before implementation.

| System / domain | v5.5.5 (1.18.2 Forge) | Beta 5.10.17 (1.20.1 Forge) | Development implications |
|---|---|---|---|
| System / Domain | v5.5.5 (1.18.2 Forge) | Beta 5.10.17 (1.20.1 Forge) | Mod-Development Implications for Dual-Version Compatibility |
| Toolchain & Loader | MC 1.18.2 \| Forge 40.2.4 \| Java 17 | MC 1.20.1 \| Forge 47.4.0 \| Java 17 (+ Sinytra Connector) | Use a multi-version Forge setup (e.g., Stonecutter or shared common core + thin 1.18.2/1.20.1 Forge adapter modules). Key MC API deltas: ForgeRegistries/CreativeModeTab registration, GuiGraphics (1.20.1) vs PoseStack (1.18.2), Component.literal() vs new TextComponent(), and Biome/Tag changes. |
| Survival / Health / Thirst / Temp | First Aid + Thirst Was Taken + Cold Sweat | Legendary Survival Overhaul (all-in-one) | CRITICAL DIVERGENCE: Do NOT hard-depend on First Aid, Thirst Was Taken, Cold Sweat, or LSO. If your mod interacts with limb health, thirst, temperature, or healing, expose an internal SurvivalBridge interface with optional runtime detection (ModList.get().isLoaded(...)) for both stacks. |
| Firearms & Combat | Timeless and Classics Guns (TaC) + MrCrayfish's Gun Mod; Better Combat, Apocalypse Now, Create Big Cannons, ParCool! | [TaCZ] Timeless and Classics Zero (+ Tweaks/Durability/Shots Fired) + MrCrayfish Unofficial; Better Combat, Apocalypse Now, Create Big Cannons, ParCool! | CRITICAL DIVERGENCE: TaC (1.18.2) and TaCZ (1.20.1) have completely different APIs/data formats (TaCZ is data-driven gun packs). Interact via standard Forge DamageSource/LivingHurtEvent/tags when possible, or isolate gun-specific hooks behind optional compat modules. |
| Zombies, Hordes & AI | The Hordes, THE UNDEAD REVAMPED, Zombie Awareness, Zombie Extreme, Enhanced AI, Enhanced Hordes, Mob Sunscreen, Lost Souls, Mutationcraft, NoCube's | Same 8 core zombie/AI mods + Fungal Infection: Spore, Voiceless Survival (dropped Mutationcraft & NoCube's) | HIGH CONTINUITY: Target vanilla Zombie/Monster tags, entity type tags, and Forge LivingEvent/EntityJoinLevelEvent. Core DeceasedCraft zombie mods exist on both versions, making mob/horde hooks cleanly portable. |
| Worldgen, Cities & Loot | The Lost Cities, Biomes O' Plenty, TerraBlender, Lootr, Structure Essentials, Ore Tweaker | The Lost Cities, Lost Worlds LC, Lost Radar, Biomes O' Plenty, TerraBlender, Lootr, Biome Replacer/Sizes | HIGH CONTINUITY: The Lost Cities & Lootr power both packs. For custom loot, use Forge Global Loot Modifiers (GLMs) or Loot Table injection so Lootr automatically instances your loot chests in multiplayer on both versions. |
| Tech, Power & Automation | Create (+5 addons), Immersive Engineering, Immersive Petroleum, Refined Storage, Pipez, Security Craft | Create (+8 addons incl. Diesel Generators), Immersive Engineering, Extreme Reactors, Refined Storage (+Addons), Pipez, Security Craft | HIGH CONTINUITY: Forge Energy (FE), FluidCapability, and IItemHandler work seamlessly with Create, Immersive Engineering, Pipez, and Refined Storage across both 1.18.2 and 1.20.1. |
| Vehicles & Transport | Ultimate Car Mod, Simple Planes | DragN's Valiant Vehicles! (+ Refueled), Simple Planes, Immersive Aircraft | Only Simple Planes is shared; ground vehicles switched from Ultimate Car Mod to DragN's Valiant Vehicles!. Avoid hard dependencies on vehicle mods. |
| Quests, Skills & Accessories | FTB Quests, FTB Teams, Pufferfish's Skills, Curios API, Artifacts, Nameless Trinkets | FTB Quests, FTB Teams, Pufferfish's Skills, Pufferfish's Attributes, Curios API, CustomNPCs-Unofficial, Artifacts, Nameless & Fancy Trinkets | HIGH CONTINUITY: Curios API is present in both versions (safe optional/required dependency for wearable gear). Standard Forge item/advancement/entity events integrate cleanly with FTB Quests and Pufferfish's Skills. |
| Pack Scripting & Config | KubeJS + CraftTweaker + ContentTweaker + In Control! + Fx Control! | KubeJS (+ KubeJS Create, EntityJS) + In Control! (CraftTweaker & Fx Control! removed) | Use standard Minecraft datapacks, tags, JSON recipes, and Forge Config/Events (plus KubeJS compatibility if exposing script hooks). Do NOT rely on CraftTweaker/ZenScript since v6 dropped it. |
| Safe Shared Library APIs | Curios, GeckoLib, Architectury, Cloth Config, Moonlight Lib, Patchouli, Bookshelf, playerAnimator, JEI, The One Probe, Xaero's World Map, Open Parties and Claims | All 12 shared libraries remain in Beta 5.10.17 (note: GeckoLib 3 in 1.18.2 -> GeckoLib 4 in 1.20.1; AutoRegLib -> Zeta) | Prefer zero-dependency Forge APIs where possible. If you need 3D animations or config GUIs, GeckoLib / Cloth Config / Curios / JEI / Patchouli are available in both packs (account for GeckoLib 3 -> 4 API refactor). |
| Rendering, Shaders & DH | Embeddium, Oculus, Iris & Oculus Flywheel Compat, [ETF] | Embeddium, Oculus, Colorwheel, Vanillin, ImmediatelyFast, [EMF], [ETF] + Distant Horizons (DH Edition) | Avoid invasive vanilla renderer mixins that conflict with Embeddium/Oculus/ImmediatelyFast/Colorwheel. Keep custom block/entity renderers standard Forge/GeckoLib so shaders & Distant Horizons LODs render cleanly. |
| Custom Pack Patch Mods | DCFixes (Bawnorton) | DeceasedCraft++ (Bogdan_Off), DCTweaks (plus upcoming DeceasedCraft v6 Fixes on GitHub) | Watch for overlapping mixins/tag overrides with DCFixes (v5.5.5) and DeceasedCraft++ / DCTweaks (v6) — especially around health sync, Hordes spawns, TaCZ, and Immersive/Create configs. |


**Implementation rules derived from the inventory comparison**
1. **Do not hard-depend on survival/health implementations.** v5.5.5 uses First Aid, Thirst Was Taken, and Cold Sweat; Beta 5.10.17 uses Legendary Survival Overhaul. If weapon effects need to interact with health, thirst, temperature, or healing, route through an internal adapter/bridge and make pack-specific integrations optional.
2. **Do not hard-depend on one firearms API.** The catalog distinguishes Timeless and Classics Guns in v5.5.5 from Timeless and Classics Zero (TaCZ) in v6 beta. Prefer vanilla/Forge damage events, tags, and isolated optional adapters.
3. **Target stable entity and damage interfaces for zombie interactions.** Use Forge entity/living events and entity-type tags where possible. Test against The Hordes, THE UNDEAD REVAMPED, Zombie Awareness, Zombie Extreme, Enhanced AI, Enhanced Hordes, and other installed hostile-mob mods in each separate pack.
4. **Use standard Forge capabilities for technology interoperability.** Prefer Forge Energy (FE), fluid capabilities, and `IItemHandler` where applicable. Validate actual Create, Immersive Engineering, Pipez, and Refined Storage versions and their addons in both packs.
5. **Treat recipe unification as a pack-level behavior.** Inspect KubeJS scripts, tags, datapacks, recipe serializers, and addon integrations before adding recipes. Do not assume a recipe ID or item/fluid tag from one version exists in the other.
6. **Do not require CraftTweaker / ZenScript.** The workbook records CraftTweaker and ContentTweaker in v5.5.5 but not Beta 5.10.17. Use datapacks, tags, JSON recipes, Forge config/events, and optional KubeJS compatibility hooks instead.
7. **Account for GeckoLib major-version differences.** The workbook records GeckoLib 3 on 1.18.2 and GeckoLib 4 on 1.20.1. Keep animation integration behind version-specific source sets/adapters.
8. **Avoid invasive rendering mixins.** The workbook lists Embeddium/Oculus in both targets and additional rendering components in the beta. Use supported Forge/GeckoLib rendering paths and test with shaders enabled and disabled.
9. **Guard against patch-mod conflicts.** v5.5.5 lists DCFixes; the beta lists DeceasedCraft++, DCTweaks, and a developing v6 fixes project. Inspect mixins, event priorities, tags, and config overrides before adding overlapping behavior.
10. **Do not hard-depend on a vehicle mod.** The vehicle ecosystems differ between versions. Fuel interoperability, if later desired, must be optional and separately tested.

### 16.4 Excluded resource packs and shaders (not mods)

These entries are included in the workbook's audit log but are not part of either mod count. They may affect visual testing and compatibility validation, especially shader and entity appearance tests.

| Item | Type | In v5.5.5? | In Beta 5.10.17? | Source |
|---|---|---|---|---|
| Adelink's Ultimate Car - Custom textures | Resource Packs | Yes | No | [Source](https://www.curseforge.com/minecraft/texture-packs/adelinks-ultimate-car-custom-textures) |
| DeceasedCraft Chinese Translation Resource | Resource Packs | No | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/deceasedcraft-chinese-translation-resource) |
| DeceasedCraft Screen Tweak | Resource Packs | No | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/deceasedcraft-screen-tweak) |
| Fresh Moves | Resource Packs | No | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/fresh-moves) |
| Legs and Arm's UNDEAD Pack | Resource Packs | No | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/legs-and-arms-undead-pack) |
| No Enchant Glint | Resource Packs | Yes | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/no-enchant-glint) |
| No Potion Particles | Resource Packs | No | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/no-potion-particles) |
| Remove Potion Particles | Resource Packs | Yes | No | [Source](https://www.curseforge.com/minecraft/texture-packs/remove-potion-particles) |
| Tissou's Zombie Pack | Resource Packs | Yes | Yes | [Source](https://www.curseforge.com/minecraft/texture-packs/tissous-zombie-pack-optifine-1-7x-1-20) |
| Bliss Shaders | Shaders | No | Yes | [Source](https://www.curseforge.com/minecraft/shaders/bliss-shader) |
| Complementary Shaders - Reimagined | Shaders | Yes | No | [Source](https://www.curseforge.com/minecraft/shaders/complementary-reimagined) |
| Complementary Shaders - Unbound | Shaders | No | Yes | [Source](https://www.curseforge.com/minecraft/shaders/complementary-unbound) |
| Photon Shader | Shaders | No | Yes | [Source](https://www.curseforge.com/minecraft/shaders/photon-shader) |
| Spooklementary | Shaders | No | Yes | [Source](https://www.curseforge.com/minecraft/shaders/spooklementary) |
| 🎃 Insanity Shader | Shaders | Yes | No | [Source](https://www.curseforge.com/minecraft/shaders/insanity-shader) |


### 16.5 Mandatory inventory verification before implementation

The workbook provides a detailed researched catalog, but the implementation agent must still verify the exact target pack archives before claiming full compatibility.

For each target version:
- Obtain the exact official archive and record its file ID, download date, and SHA-256.
- Compare the archive manifest/mod files against the corresponding inventory above. Report missing, extra, renamed, or version-mismatched entries.
- Separate client-only, server-only, library, content, and compatibility/patch mods where identifiable.
- Inspect relevant `mods.toml`, dependency declarations, mixin configs, Forge capabilities, configs, datapacks, KubeJS scripts, and recipe/tag data.
- Build an ecosystem map for Create and every installed Create addon; Immersive Engineering and its addons; fluids and fuel containers; power/FE; recipe unification; combat, damage, and protection; and zombie/horde entity interactions.
- Mark every integration as **verified by code/API inspection**, **verified in runtime**, **not applicable**, or **unknown**. Do not label a mod "compatible" merely because it appears in the inventory.
- If a later v6 release supersedes Beta 5.10.17, create a new third inventory or replace §16.2 only after preserving the beta inventory as a historical baseline.

### 16.6 Inventory-driven priority integrations for this project

The following are high-priority ecosystem checks because they directly affect the flamethrower, fuel, recipes, or turret requirements:

- **Create ecosystem:** identify the exact Create version and all installed addons in each pack; inspect rotational input, kinetic stress/rotation interfaces, fluid transport, recipe integration, and any addon-specific fuel behavior.
- **Create: Diesel Generators:** confirm presence, version, fluid identifiers, fuel registry/recipe model, and whether the mod exposes a supported API or only data-driven recipes. Do not assume the same identifiers across MC 1.18.2 and 1.20.1.
- **Immersive Engineering:** inspect fluid containers, fluid capabilities, chemical/flammable fluid semantics, damage/fire interactions, and any installed addons. Do not infer that a fluid is a valid flamethrower fuel solely because it is combustible in-world.
- **Other fluid and storage mods:** test Forge fluid capability interoperability and container transfer with the actual installed versions of Pipez, Refined Storage, and any relevant addons.
- **Combat and zombie systems:** test damage type/source behavior, fire immunity, armor, entity tags, horde interactions, spawn protection, PvP, Adventure mode, and server-side authority.
- **Recipe unification and progression:** inspect KubeJS, tags, datapacks, and pack-specific recipe modifications before finalizing crafting, fuel, cartridge, or turret recipes.

---


## 17. Definition of done

The project is complete only when it has:

- A stable, polished handheld flamethrower with the specified firing, fuel, reload, heat, damage, and protection behavior.
- A functional Create-integrated turret with validated fluid, rotation, electrical, filter, and pilot-burner behavior.
- Verified fluid and recipe interoperability with the actual installed technology ecosystems.
- Separate, complete, evidence-backed mod inventories for DeceasedCraft v5.5.5 and the target v6-development/final release.
- Separate tested builds for the supported Minecraft/Forge versions.
- Demonstrated performance discipline without sacrificing the creative visual direction.
- Passing functional, integration, multiplayer, performance, and packaging gates.

**No compatibility claim is valid merely because the mod launches. Compatibility requires the relevant integration tests to pass on the exact target pack build.**
