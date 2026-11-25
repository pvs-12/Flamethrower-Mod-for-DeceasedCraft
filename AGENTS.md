# AGENTS.md — Engineering Handbook for AI Coding Agents

This file is the authoritative quick-start contract for all AI coding agents working on **Create: Tactical ChemThrowers** (`modid: tacticalchemthrowers`). Read this file and [SPECS.md](SPECS.md) before modifying code, data, or assets.

---

## 1. Mod Identity & Non-Negotiable Guardrails

- **Mod Name:** Create: Tactical ChemThrowers
- **Mod ID:** `tacticalchemthrowers`
- **Aesthetic Direction:** **Heavy Tactical + Create Mod Aesthetic** — bulky military-industrial silhouette (perforated heat-shielded barrel, underslung canister cradle, tactical rails, armored turret gimbal) blended with Create materials (riveted andesite/dark iron, copper pressure pipes, brass valves, mechanical pressure dial & cogwheel accents).
- **Strict Minecraft EULA & Originality Rule:**
  - Use **100% original fictional industrial/tactical names** everywhere (code, IDs, lang keys, tooltips, docs, assets).
  - **NEVER** use real-world firearm/flamethrower brands, manufacturers, or model numbers.
  - **NEVER** reference copyrighted movie, TV, video game, character, or franchise IP names anywhere in the repository.
  - **ZERO plagiarism:** Never copy source code, JSON models, textures, animations, or audio from third-party mods. Study external repositories strictly for API interoperability and architectural reference.
- **Server Authority:** All fuel consumption, canister swaps, heat stacks, hit detection, damage, temporary fire placement, and turret targeting MUST run authoritatively on the server.
- **Client/Server Isolation:** Never reference client-only classes (`Minecraft`, `Particle`, `GuiGraphics`, `PoseStack`, renderers, shaders, sound instances) from common or server code.
- **Mixin Restraint:** Prefer Forge events, capabilities, and supported mod APIs. Avoid invasive vanilla renderer mixins that conflict with Embeddium, Oculus, Colorwheel, Vanillin, ImmediatelyFast, or Distant Horizons.

---

## 2. Dual-Version Targets & Adapter Boundaries

Never build a single runtime JAR for both versions and never assume mod IDs, fluid IDs, or library APIs match across versions. Keep shared gameplay logic in a version-agnostic core and isolate platform/mod bindings into separate `1.18.2` and `1.20.1` adapter modules.

| Subsystem | `DeceasedCraft v5.5.5` (`MC 1.18.2` / `Forge 40.2.4`) | `DeceasedCraft Beta-5.10.17` (`MC 1.20.1` / `Forge 47.4.0`) | Adapter Rule |
| --- | --- | --- | --- |
| **Create** | `create-1.18.2-0.5.1.f.jar` | `create-1.20.1-6.0.6.jar` (Ponder extracted, Flywheel 1.0) | Separate kinetic/wrench/goggle adapters per version. |
| **Fuel Providers** | `Immersive Petroleum 4.2.0-25` + `IE 8.4.0-161` + `Create Crafts & Additions 1.0.0` (**No CDG**) | `Create: Diesel Generators 1.3.5` + `IE 10.2.0-183` + `Create Crafts & Additions 1.3.2` (**No IP**; KubeJS `material.js` prefers `createaddition:bioethanol` & `seed_oil`) | **Zero duplicate custom fluids.** Zero hard dependency on IP or CDG. Resolve via `data/tacticalchemthrowers/flamethrower_fuels/*.json` (exact ID → Forge fluid tag → reject). |
| **3D Animation** | `GeckoLib 3` (`3.0.57`) | `GeckoLib 4` (`4.7`) | Isolate `IAnimatable` (`1.18.2`) vs `GeoItem`/`GeoBlockEntity` (`1.20.1`). |
| **Dynamic Lights** | `Lucent` (`1.2.2`) | `Sodium/Embeddium Dynamic Lights` (`1.0.10`) | Soft optional `DynamicLightBridge` via `ModList.get().isLoaded(...)`. |
| **Survival / Temp** | `Cold Sweat` (`2.2.5.1`) + `First Aid` + `Thirst Was Taken` | `Legendary Survival Overhaul` (`2.3.23.1`) | Soft optional `SurvivalBridge` for subtle firing warmth only; zero hard deps. |
| **Shaders / Render** | `Embeddium`, `Oculus 1.6.4`, `oculus-flywheel-compat`, `GeckoLibOculusCompat`, `oculusparticlefix` | `Embeddium`, `Oculus 1.8.0`, `Colorwheel`, `Vanillin`, `ImmediatelyFast`, `Distant Horizons` (DH Edition) | Iris/Oculus-safe renderers + `FULL_BRIGHT` (`0xF000F0`) flame + LabPBR `_s` emissive maps. |
| **Scripting & Loot** | `KubeJS` + `CraftTweaker` + `Lootr` | `KubeJS` + `Lootr` (**No CraftTweaker**) | Use standard JSON recipes, Forge tags, and Forge GLMs (Lootr-safe). Never require CraftTweaker. |
| **Protection / AI** | `Open Parties & Claims`, `FTB Teams`, `Zombie Awareness`, `The Hordes` | Same 4 core mods (updated `1.20.1` builds) | Soft optional `ProtectionBridge` & `AggroBridge`. |

---

## 3. Locked Gameplay Invariants (Do Not Drift)

1. **Handheld Modularity:** **1 modular ChemThrower** upgraded via swappable nozzle/pressure modules unlocking **`15 → 25 → 35` block** effective ranges (with visible 3D barrel changes).
2. **Fuel & Canister-Only Reload:** **`50 units = 1,000 mB`** (`4 mB/tick` baseline = `12.5s` continuous fire). The gun reloads **ONLY** by swapping **Pressurized Fuel Canisters** (`R` or `Sneak+Right-Click`, `1.5s`, returns spent canister). Only the canister implements `IFluidHandlerItem` (fillable via Create Spouts/Tanks/Pipes & IE Bottling Machine/Tanks; no fluid mixing; `FluidAction.SIMULATE` never mutates state).
3. **Combat & Stance:** `+10%`/hit up to **`2.0x`** (10 hits), resetting after **`2.5s`** without hit; **`≤ 4 blocks`** point-blank lava-like bonus + `3s` burn; **Heavy Braced Creep (`~15%` walk speed, no sprint/jump)** while firing; **ZERO camera pitch kick** (pure 1st-person gun+hands kickback & vibration); no underwater firing; temporary non-griefing fire only.
4. **Flame VFX & Shaders:** Crisp pixel-native blocky billboard particles (`0.18–0.55b`) with **4-stage lifecycle** (white-yellow pressurized core with slight droop → roaring orange/amber blocky flame + sparks → cooling crimson ember → rising dark/black hydrocarbon smoke lingering briefly on release), strict client particle caps/LOD, `LightTexture.FULL_BRIGHT`, LabPBR `_s`, validated on **BSL, Complementary (Reimagined/Unbound + Euphoria), Photon, Bliss, and Spooklementary**.
5. **Automated Turret:** Fixed ports — **Left** = Create Shaft (`RPM`/`SU` slew), **Right** = Forge Energy (`IEnergyStorage`), **Back + Bottom** = Create Fluid Pipe (`IFluidHandler`). Right-click GUI (range, target filters, pilot burner / maintenance off), Create Wrench rotate/pickup, Engineer's Goggles live telemetry, and real blockstate `lightLevel` (`14` firing / `5` pilot) since `Beta-5.10.17` disables `block_entities` in `sodiumdynamiclights-client.toml` by default.
6. **IE Coexistence & Pack Recipe Discipline:** Never disable, nerf, or override Immersive Engineering's Chemthrower or Chemthrower Turret. **CRITICAL:** Both DeceasedCraft packs globally replace `create:electron_tube` with `immersiveengineering:component_electronic` — use `immersiveengineering:component_electronic` / `component_electronic_adv` (with `forge:mod_loaded` standalone fallback) in recipes, never raw `create:electron_tube`.

---

## 4. Documentation-First Workflow

Before writing code against Forge, Create, GeckoLib, IE, or shader pipelines, verify exact class/method signatures from primary sources indexed in `docs/references/` and `compatibility/`:

- [API & Integration Research](compatibility/API_AND_INTEGRATION_RESEARCH.md) — exact Forge, Create `0.5.1.f` vs `6.0.6`, GeckoLib `3` vs `4`, dynamic light, and compat API notes.
- [Notebook 1](docs/references/flmthrwr_notebook_1_overview.md) — Forge, multi-version templates, Mixin/MixinExtras, GeckoLib, Flywheel, mappings, `sounds.json`.
- [Notebook 2](docs/references/flmthrwr_notebook_2_overview_links.md) — Create kinetics, fluid pipes, Spouts, Ponder, Create: Diesel Generators, multi-fuel architecture.
- [Notebook 3](docs/references/flmthrwr_notebook_3_overview_links.md) — Weapon/turret reference architectures, collision geometry, particles, GeckoLib/PlayerAnimator, audio, `spark`.
- [Notebook 4](docs/references/flmthrwr_notebook_4_overview_links.md) — Industrial fuel ecosystems, combustion properties, soot/droop calibration.

---

## 5. Asset Creation Workflow (`mc-asset` + Headless `blockbench-mcp`)

Never hand-author raw PNG bytes or raw `.geo.json` bone/UV coordinates when our automated asset toolchain is available (see [tools/README.md](tools/README.md)):

1. **Bootstrap Tools (idempotent in cloud VMs):**
   ```bash
   bash tools/setup_asset_tools.sh --install
   bash tools/setup_asset_tools.sh --start-blockbench
   ```
2. **2D Textures, Particle Strips & LabPBR `_s` Maps (`mc-asset`):**
   - Generate all item icons, GUI textures, 4-stage blocky flame/smoke sprite strips + `.mcmeta`, and LabPBR `_s` maps with `mc-asset`.
   - Always validate output with `mc-asset validate` and visually inspect generated PNGs.
3. **3D GeckoLib Models, Animations & QA Renders (`blockbench-mcp`):**
   - Run headless Blockbench (`xvfb-run` + SwiftShader WebGL 2.0) listening on `127.0.0.1:8787` and invoke tools via:
     ```bash
     node tools/bb_mcp_client.mjs call <tool_name> '<json_args>'
     ```
   - Author `.bbmodel` projects, apply textures, rig GeckoLib animations, export `.geo.json` + `.animation.json`, and capture multi-angle `screenshot` / `screenshot_views` PNGs to verify proportions before committing.
4. **Audio Assets:** Author/process mono `.ogg` files (`44.1/48 kHz`) for 3D `Sound Physics Remastered` attenuation and wire them in `sounds.json`.

---

## 6. Repository Map

| Path | Purpose |
| --- | --- |
| [SPECS.md](SPECS.md) | Authoritative unified engineering specification & release gates |
| [AGENTS.md](AGENTS.md) | This agent engineering handbook |
| [README.md](README.md) | Project overview & navigation hub |
| `compatibility/inventory/` | Archive-verified CSV inventories (`deceasedcraft-5.5.5-1.18.2.csv`, `deceasedcraft-beta-5.10.17-1.20.1.csv`) |
| `compatibility/ECOSYSTEM_MATRIX.md` | SHA-256 hashes & cross-version mod ecosystem comparison |
| `compatibility/RECIPE_AND_FLUID_AUDIT.md` | Archive-extracted fluids, tags, KubeJS `material.js` overrides & fuel table |
| `compatibility/COMBAT_AND_PROTECTION_AUDIT.md` | Gamerules, claims, armor set bonuses, survival & horde configs |
| `compatibility/API_AND_INTEGRATION_RESEARCH.md` | Exact `1.18.2` vs `1.20.1` API reference for Create, GeckoLib, IE & bridges |
| `tools/` | `setup_asset_tools.sh`, `bb_mcp_client.mjs`, and [tools/README.md](tools/README.md) |
| `docs/references/` | Notebook 1–4 curated primary-source reference link libraries |
| `docs/` | `DeceasedCraft_Mod_Research.xlsx`, `RESEARCH_SUMMARY.md`, and audit scripts (`docs/scripts/`) |

---

## 7. Pre-Commit Verification Checklist

Before every commit or PR, verify:
- [ ] **EULA & Originality Scan:** Zero real-world weapon brands/model numbers, zero copyrighted IP/franchise names, zero plagiarized third-party assets or code.
- [ ] **Dual-Version Discipline:** No cross-version API leakage (`1.18.2` vs `1.20.1`, Create `0.5.1.f` vs `6.0.6`, GeckoLib `3` vs `4`); all optional mod hooks guarded by `ModList.get().isLoaded(...)`.
- [ ] **Client/Server Safety:** No client class imports in common/server packages; dedicated server build/launch clean.
- [ ] **Fluid & Capability Safety:** Zero duplicate custom fluids; `FluidAction.SIMULATE` is side-effect-free; no fluid mixing in canisters or turret tanks.
- [ ] **Asset Validation:** 2D strips pass `mc-asset validate`; 3D models visually verified via Blockbench screenshots; mono `.ogg` audio verified.
- [ ] **Clean Working Tree:** No temporary scratch outputs, downloaded archives, third-party tool clones, or `.deb` installers staged in git.
