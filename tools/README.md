# Asset Tooling (`mc-asset` + Headless `blockbench-mcp`)

This directory contains the reproducible asset-tooling setup and CLI bridge for **Create: Tactical ChemThrowers** (`modid: tacticalchemthrowers`).

External tools, `node_modules`, `.deb` installers, and smoke-test outputs are **never** stored inside this Git repository. They are installed under `~/.local/share/` and `~/.local/bin/`.

---

## Verified Versions

| Tool | Exact Tested Version | Install Location |
|---|---|---|
| `mc-asset` | `0.6.0` (npm, pinned) | `~/.local/share/mc-asset-tools` (symlink: `~/.local/bin/mc-asset`) |
| `sosadly/blockbench-mcp` | `0.4.0` (bridge plugin `0.3.1`, 86 MCP tools) | `~/.local/share/blockbench-mcp` |
| Blockbench Desktop | `5.2.2` (`Blockbench_5.2.2.deb`) | `/opt/Blockbench/blockbench` (`/usr/bin/blockbench`) |
| Runtime | Node.js `v22.23.5`, Ubuntu 24.04, `xvfb-run` | System / preinstalled |

---

## Quick Start (Cloud VM / Headless Linux)

### 1. Install and bootstrap all tools (idempotent)

```bash
./tools/setup_asset_tools.sh
```

What this does automatically without touching the Git repo:
1. Installs `mc-asset@0.6.0` into `~/.local/share/mc-asset-tools` and symlinks `~/.local/bin/mc-asset`.
2. Clones and builds `sosadly/blockbench-mcp` into `~/.local/share/blockbench-mcp`.
3. Installs Blockbench `v5.2.2` (`.deb`) and `xvfb` if missing.
4. Configures `~/.config/Blockbench/launch_settings.json` (`"hardware_acceleration": false`) and `~/.config/Blockbench/plugin_permissions.json` (`"net": true`, `"fs": true`).
5. Registers `blockbench_mcp` in Blockbench's persisted `StateMemory.installed_plugins` on first run (via local CDP on `127.0.0.1:9222`) so future launches auto-load the bridge plugin with zero UI clicks, verifies `http://127.0.0.1:8787/ping`, and stops the bootstrap process cleanly.

### 2. Manage headless Blockbench

```bash
# Start headless Blockbench under Xvfb (1920x1080x24) and wait for :8787/ping
./tools/setup_asset_tools.sh --start-blockbench

# Check installed versions and whether the HTTP bridge is live
./tools/setup_asset_tools.sh --status

# Stop headless Blockbench and its managed Xvfb cleanly (leaves zero orphans)
./tools/setup_asset_tools.sh --stop-blockbench
```

### 3. Invoke Blockbench MCP tools via CLI (`tools/bb_mcp_client.mjs`)

`tools/bb_mcp_client.mjs` is a zero-dependency Node.js CLI bridge that spawns `~/.local/share/blockbench-mcp/dist/index.js` and speaks MCP JSON-RPC 2.0 over stdio.

```bash
# Verify bridge connectivity (direct HTTP GET /ping)
node tools/bb_mcp_client.mjs ping

# List all 86 MCP tools (optional --filter or --json)
node tools/bb_mcp_client.mjs list_tools
node tools/bb_mcp_client.mjs list_tools --filter screenshot

# Inspect full JSON schema for a specific tool
node tools/bb_mcp_client.mjs describe screenshot

# Call any tool (inline JSON, @file.json, or - for stdin)
node tools/bb_mcp_client.mjs call get_status '{}'
node tools/bb_mcp_client.mjs call list_formats '{}'
node tools/bb_mcp_client.mjs call new_project '{"name":"nozzle","format":"java_block","texture_width":32,"texture_height":32}'

# Save returned image blocks (screenshot, screenshot_views, get_texture) as PNGs
node tools/bb_mcp_client.mjs call screenshot '{"view":"front_right","width":640,"height":480}' --save-images /tmp/bb_shots

# Run a multi-step build in one MCP server session
node tools/bb_mcp_client.mjs batch /tmp/build_steps.json --save-images /tmp/bb_shots
```

Environment overrides for `bb_mcp_client.mjs`:
- `BLOCKBENCH_MCP_DIR` (default `~/.local/share/blockbench-mcp`)
- `BLOCKBENCH_MCP_HOST` (default `127.0.0.1`)
- `BLOCKBENCH_MCP_PORT` (default `8787`)
- `BLOCKBENCH_MCP_TIMEOUT_MS` (default `180000`)

---

## Local Desktop Workflow (Windows / macOS / Linux GUI)

If you are authoring models interactively in Blockbench Desktop on your own machine:

1. Install **Blockbench Desktop** (`v5.2.2+` from `https://github.com/JannisX11/blockbench/releases`).
2. Clone and build `blockbench-mcp` outside this repo:
   ```bash
   git clone https://github.com/sosadly/blockbench-mcp.git ~/.local/share/blockbench-mcp
   cd ~/.local/share/blockbench-mcp && npm ci && npm run build
   ```
3. In Blockbench Desktop: **File -> Plugins -> Load Plugin from File** and choose `~/.local/share/blockbench-mcp/plugin/blockbench_mcp.js`.
4. When prompted for network permission (`net`), choose **Always allow for this plugin** (and allow `fs` if using `save_project` / `export_project`).
5. Verify the local bridge:
   ```bash
   curl http://127.0.0.1:8787/ping
   # {"ok":true,"protocol":1,"blockbench_version":"5.2.2","is_app":true,"has_project":false}
   ```
6. Either use `node tools/bb_mcp_client.mjs ...` from a terminal, or register the stdio MCP server in your AI client (Claude Code / Cursor / Claude Desktop):
   ```json
   {
     "mcpServers": {
       "blockbench": {
         "command": "node",
         "args": ["/absolute/path/to/blockbench-mcp/dist/index.js"],
         "env": { "BLOCKBENCH_MCP_PORT": "8787" }
       }
     }
   }
   ```
7. For `mc-asset` locally, install `npm install -g mc-asset@0.6.0` (or run `npx -y mc-asset@0.6.0 ...`).

---

## Verified Smoke-Test Commands

### `mc-asset` (2D textures, animation strips, `.mcmeta`, validation)

```bash
MC_ASSET="$HOME/.local/bin/mc-asset"
OUT="/tmp/mc_asset_smoke"
mkdir -p "$OUT/frames"

# Render 16x16 .grid frames to .mcpx + .png (repeat for frames 0..3)
$MC_ASSET render frame_0.grid \
  --output "$OUT/frames/frame_0.png" \
  --source "$OUT/frames/frame_0.mcpx" \
  --profile minecraft:particle --force

# Validate frame geometry, pack vertical 16x64 strip, generate .mcmeta
$MC_ASSET animate validate --frames-dir "$OUT/frames"
$MC_ASSET animate pack --frames-dir "$OUT/frames" --layout vertical \
  --output "$OUT/flame_to_smoke.png" --profile minecraft:particle --force
$MC_ASSET mcmeta animation "$OUT/flame_to_smoke.png" \
  --frame-size 16 --frametime 2 --minecraft-version 1.20.1 \
  --output "$OUT/flame_to_smoke.png.mcmeta" --force

# Validate texture + .mcmeta for Minecraft 1.20.1 (pack format 15.0)
$MC_ASSET validate "$OUT/flame_to_smoke.png" \
  --mcmeta "$OUT/flame_to_smoke.png.mcmeta" \
  --profile minecraft:particle --minecraft-version 1.20.1

# Verify byte-level determinism between two runs
$MC_ASSET compare "$OUT/flame_to_smoke.png" "$OUT/run2/flame_to_smoke.png" --json
```

### Headless Blockbench + `bb_mcp_client.mjs`

```bash
./tools/setup_asset_tools.sh --start-blockbench

node tools/bb_mcp_client.mjs ping
node tools/bb_mcp_client.mjs call get_status '{}'
node tools/bb_mcp_client.mjs call new_project '{"name":"smoke","format":"java_block","texture_width":32,"texture_height":32}'
node tools/bb_mcp_client.mjs call add_cubes '{"cubes":[{"name":"tank_body","from":[4,2,4],"to":[12,10,12]}]}'
node tools/bb_mcp_client.mjs call pack_uv '{}'
node tools/bb_mcp_client.mjs call create_texture '{"name":"smoke","width":32,"height":32,"fill":"#b58d3d"}'
node tools/bb_mcp_client.mjs call detail_cubes '{"base":"#b58d3d","material":"metal","noise":0.1}'
node tools/bb_mcp_client.mjs call screenshot '{"view":"front_right","width":640,"height":480}' --save-images /tmp/bb_shots
node tools/bb_mcp_client.mjs call save_project '{"path":"/tmp/bb_shots/smoke.bbmodel"}'
node tools/bb_mcp_client.mjs call export_project '{"path":"/tmp/bb_shots/smoke.json"}'

./tools/setup_asset_tools.sh --stop-blockbench
```

---

## Verified Headless Electron / WebGL Caveats & Troubleshooting

1. **Software WebGL 2.0 via SwiftShader (`launch_settings.json`)**:
   - Blockbench `v5.2.2`'s `electron/main.js` reads `~/.config/Blockbench/launch_settings.json`. When `"hardware_acceleration": false` is set, Blockbench calls `app.disableHardwareAcceleration()` and appends `--enable-unsafe-swiftshader` on Linux.
   - Under `xvfb-run`, this yields a working `WebGL 2.0 (OpenGL ES 3.0 Chromium)` context on `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))`, so `screenshot` and `screenshot_views` render real shaded 3D PNGs without a physical GPU.
   - Required Electron flags in Linux containers/VMs: `--no-sandbox --disable-dev-shm-usage`.

2. **Preventing headless permission-dialog deadlocks (`plugin_permissions.json`)**:
   - Blockbench's plugin sandbox pops up a synchronous Electron `dialog.showMessageBoxSync` the first time a plugin calls `require('net')` (to start the `127.0.0.1:8787` bridge) or `require('fs')` (for `save_project`, `export_project`, `export_model`, `load_project`). Under Xvfb, an unanswered modal dialog hangs the renderer thread.
   - `tools/setup_asset_tools.sh` pre-grants both `"net": true` and `"fs": true` for `blockbench_mcp` in `~/.config/Blockbench/plugin_permissions.json`.

3. **Screenshot resolution & orientation banner overlap**:
   - At smaller Xvfb resolutions without explicit screenshot dimensions, the Blockbench side panels narrow the 3D viewport and can cause the top/bottom orientation caption text to overlap.
   - `setup_asset_tools.sh` defaults Xvfb to `1920x1080x24`, and callers should pass explicit `"width": 640, "height": 480` (or larger) to `screenshot` / `screenshot_views`.

4. **Always run `pack_uv` before `detail_cubes` (and watch texture bounds)**:
   - Newly added cubes default to `[0, 0, 1, 1]` UV rectangles. Call `pack_uv` before `detail_cubes`, and check `check_model` for `uv_out_of_bounds` (increase `texture_width` / `texture_height` when a model needs more texels than `32x32`).

5. **Minecraft 1.20.1 Java model JSON compatibility**:
   - Blockbench `5.2.2`'s `java_block` exporter emits `"format_version": "26.3"` at the top of exported `.json` files. For Forge 1.20.1 (pack format `15`), validate exported models with `mc-asset model validate <model.json> --pack <pack_root> --minecraft-version 1.20.1` and ensure rotations/fields conform to 1.20.1 (single-axis 22.5-degree rotations for vanilla item/block models; Flywheel/Create partial models or GeckoLib for articulated parts).

6. **Clean shutdown (avoiding orphan `Xvfb` processes)**:
   - Always stop headless Blockbench via `./tools/setup_asset_tools.sh --stop-blockbench` (which signals the `blockbench` binary first so `xvfb-run` tears down its own virtual display and `/tmp/xvfb-run.*` auth directory before killing the process group).
   - Never run `pkill -f blockbench` from a command whose own shell line contains `blockbench`, and never kill an unrelated system `Xvfb :99`.

7. **D-Bus stderr warnings in `blockbench.log`**:
   - Messages such as `Failed to connect to the bus` in `~/.local/share/blockbench-mcp/.headless/blockbench.log` are harmless in headless Linux VMs without a desktop D-Bus session.
