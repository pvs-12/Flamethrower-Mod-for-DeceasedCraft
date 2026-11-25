#!/usr/bin/env bash
# Idempotent setup and headless lifecycle helper for Create: Tactical ChemThrowers
# asset tooling:
#   1. mc-asset (pinned 0.6.0) installed under ~/.local/share/mc-asset-tools
#   2. sosadly/blockbench-mcp built under ~/.local/share/blockbench-mcp
#   3. Blockbench Desktop v5.2.2 (.deb) + headless Xvfb/SwiftShader config
#
# Usage:
#   ./tools/setup_asset_tools.sh                    # Install & verify all tools (idempotent)
#   ./tools/setup_asset_tools.sh --install          # Same as default
#   ./tools/setup_asset_tools.sh --start-blockbench # Start headless Blockbench + wait for :8787/ping
#   ./tools/setup_asset_tools.sh --stop-blockbench  # Stop headless Blockbench + its Xvfb cleanly
#   ./tools/setup_asset_tools.sh --status           # Print installed versions & bridge status
#   ./tools/setup_asset_tools.sh --help

set -euo pipefail

MC_ASSET_VERSION="${MC_ASSET_VERSION:-0.6.0}"
MC_ASSET_DIR="${MC_ASSET_DIR:-$HOME/.local/share/mc-asset-tools}"
LOCAL_BIN_DIR="${LOCAL_BIN_DIR:-$HOME/.local/bin}"

BB_MCP_DIR="${BB_MCP_DIR:-$HOME/.local/share/blockbench-mcp}"
BB_MCP_REPO="${BB_MCP_REPO:-https://github.com/sosadly/blockbench-mcp.git}"
BB_VERSION="${BB_VERSION:-5.2.2}"
BB_DEB_URL="https://github.com/JannisX11/blockbench/releases/download/v${BB_VERSION}/Blockbench_${BB_VERSION}.deb"
BB_BIN="${BB_BIN:-/opt/Blockbench/blockbench}"
BB_CONFIG_DIR="${BB_CONFIG_DIR:-$HOME/.config/Blockbench}"
BB_HOST="${BLOCKBENCH_MCP_HOST:-127.0.0.1}"
BB_PORT="${BLOCKBENCH_MCP_PORT:-8787}"
BB_CDP_PORT="${BLOCKBENCH_CDP_PORT:-9222}"
BB_SCREEN="${BLOCKBENCH_XVFB_SCREEN:-1920x1080x24}"

BB_STATE_DIR="$BB_MCP_DIR/.headless"
BB_PGID_FILE="$BB_STATE_DIR/blockbench.pgid"
BB_LOG_FILE="$BB_STATE_DIR/blockbench.log"

log() {
  printf '[asset-tools] %s\n' "$*"
}

die() {
  printf '[asset-tools] ERROR: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage: tools/setup_asset_tools.sh [OPTIONS]

Options:
  --install           Install/verify mc-asset, blockbench-mcp, Blockbench v5.2.2,
                      and headless plugin auto-load config (default if no flag given).
  --start-blockbench  Start headless Blockbench under Xvfb and wait for HTTP bridge.
  --stop-blockbench   Stop the managed headless Blockbench + Xvfb process group.
  --status            Show installed versions and live Blockbench bridge status.
  -h, --help          Show this help message.

Environment overrides:
  MC_ASSET_VERSION          Default: 0.6.0
  MC_ASSET_DIR              Default: ~/.local/share/mc-asset-tools
  BB_MCP_DIR                Default: ~/.local/share/blockbench-mcp
  BB_VERSION                Default: 5.2.2
  BLOCKBENCH_MCP_PORT       Default: 8787
  BLOCKBENCH_XVFB_SCREEN    Default: 1920x1080x24
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"
}

install_mc_asset() {
  require_cmd node
  require_cmd npm
  mkdir -p "$MC_ASSET_DIR" "$LOCAL_BIN_DIR"

  local current=""
  if [[ -x "$MC_ASSET_DIR/node_modules/.bin/mc-asset" ]]; then
    current="$("$MC_ASSET_DIR/node_modules/.bin/mc-asset" --version 2>/dev/null || true)"
  fi

  if [[ "$current" == "$MC_ASSET_VERSION" ]]; then
    log "mc-asset $current already installed in $MC_ASSET_DIR"
  else
    log "Installing mc-asset@${MC_ASSET_VERSION} into $MC_ASSET_DIR ..."
    npm install --prefix "$MC_ASSET_DIR" --no-audit --no-fund "mc-asset@${MC_ASSET_VERSION}"
  fi

  ln -sf "$MC_ASSET_DIR/node_modules/.bin/mc-asset" "$LOCAL_BIN_DIR/mc-asset"
  local ver
  ver="$("$LOCAL_BIN_DIR/mc-asset" --version)"
  log "Verified mc-asset: $ver ($LOCAL_BIN_DIR/mc-asset)"
}

install_blockbench_mcp() {
  require_cmd git
  require_cmd node
  require_cmd npm
  mkdir -p "$(dirname "$BB_MCP_DIR")"

  if [[ ! -d "$BB_MCP_DIR/.git" ]]; then
    log "Cloning $BB_MCP_REPO into $BB_MCP_DIR ..."
    git clone "$BB_MCP_REPO" "$BB_MCP_DIR"
  else
    log "blockbench-mcp checkout already present at $BB_MCP_DIR"
  fi

  if [[ ! -f "$BB_MCP_DIR/dist/index.js" || ! -d "$BB_MCP_DIR/node_modules" ]]; then
    log "Building blockbench-mcp ..."
    (cd "$BB_MCP_DIR" && npm ci --no-audit --no-fund && npm run build)
  else
    log "blockbench-mcp already built at $BB_MCP_DIR/dist/index.js"
  fi
}

install_blockbench_deb() {
  require_cmd curl
  require_cmd dpkg

  if ! command -v xvfb-run >/dev/null 2>&1; then
    log "Installing xvfb ..."
    sudo apt-get update -qq
    sudo apt-get install -y xvfb
  fi

  local installed_ver=""
  if dpkg -s blockbench >/dev/null 2>&1; then
    installed_ver="$(dpkg-query -W -f='${Version}' blockbench 2>/dev/null || true)"
  fi

  if [[ "$installed_ver" == "$BB_VERSION" && -x "$BB_BIN" ]]; then
    log "Blockbench $installed_ver already installed at $BB_BIN"
    return 0
  fi

  local tmp_deb
  tmp_deb="$(mktemp /tmp/Blockbench_${BB_VERSION}.XXXXXX.deb)"
  trap 'rm -f "${tmp_deb:-}"' RETURN

  log "Downloading Blockbench v${BB_VERSION} from official GitHub release ..."
  curl -fSL -o "$tmp_deb" "$BB_DEB_URL"

  log "Installing Blockbench v${BB_VERSION} via apt-get ..."
  sudo apt-get update -qq
  sudo apt-get install -y "$tmp_deb"
  rm -f "$tmp_deb"
  trap - RETURN

  [[ -x "$BB_BIN" ]] || die "Blockbench binary not found at $BB_BIN after install"
  log "Verified Blockbench $(dpkg-query -W -f='${Version}' blockbench) at $BB_BIN"
}

configure_blockbench_headless() {
  mkdir -p "$BB_CONFIG_DIR"

  # 1. Disable hardware acceleration so Blockbench's electron/main.js natively
  #    enables SwiftShader software WebGL 2.0 on Linux under Xvfb.
  # 2. Pre-grant `net` (local HTTP bridge on 127.0.0.1:8787) and `fs`
  #    (save_project / export_project / export_model) permissions for
  #    blockbench_mcp so headless mode never blocks on native permission dialogs.
  node - "$BB_CONFIG_DIR" <<'NODE_EOF'
const fs = require("node:fs");
const path = require("node:path");

const cfgDir = process.argv[2];

function updateJson(filePath, mutator) {
  let obj = {};
  if (fs.existsSync(filePath)) {
    try {
      obj = JSON.parse(fs.readFileSync(filePath, "utf8")) || {};
    } catch {
      obj = {};
    }
  }
  mutator(obj);
  fs.writeFileSync(filePath, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

updateJson(path.join(cfgDir, "launch_settings.json"), (obj) => {
  obj.hardware_acceleration = false;
});

updateJson(path.join(cfgDir, "plugin_permissions.json"), (obj) => {
  if (!obj.blockbench_mcp || typeof obj.blockbench_mcp !== "object") {
    obj.blockbench_mcp = {};
  }
  if (!obj.blockbench_mcp.allowed || typeof obj.blockbench_mcp.allowed !== "object") {
    obj.blockbench_mcp.allowed = {};
  }
  obj.blockbench_mcp.allowed.net = true;
  obj.blockbench_mcp.allowed.fs = true;
});
NODE_EOF

  log "Configured $BB_CONFIG_DIR/{launch_settings.json,plugin_permissions.json}"
}

ping_bridge() {
  curl -sf "http://${BB_HOST}:${BB_PORT}/ping" 2>/dev/null
}

wait_for_ping() {
  local attempts="${1:-50}"
  local out=""
  for _ in $(seq 1 "$attempts"); do
    if out="$(ping_bridge)"; then
      printf '%s\n' "$out"
      return 0
    fi
    sleep 0.5
  done
  return 1
}

stop_pgid() {
  local pgid="$1"
  [[ -n "$pgid" ]] || return 0
  # Signal Blockbench first so xvfb-run cleanly tears down its own Xvfb + auth dir.
  pkill -g "$pgid" -x blockbench 2>/dev/null || true
  for _ in $(seq 1 10); do
    if ! kill -0 -- "-$pgid" 2>/dev/null; then
      return 0
    fi
    sleep 0.25
  done
  kill -TERM -- "-$pgid" 2>/dev/null || true
  sleep 0.5
  kill -KILL -- "-$pgid" 2>/dev/null || true
}

bootstrap_blockbench_plugin() {
  local plugin_js="$BB_MCP_DIR/plugin/blockbench_mcp.js"
  [[ -f "$plugin_js" ]] || die "Plugin file missing: $plugin_js"

  if ping_bridge >/dev/null; then
    log "Blockbench bridge already active on http://${BB_HOST}:${BB_PORT}/ping; skipping plugin bootstrap."
    return 0
  fi

  mkdir -p "$BB_STATE_DIR"
  local boot_log="$BB_STATE_DIR/bootstrap.log"
  log "Verifying / bootstrapping blockbench_mcp plugin in headless Blockbench ..."

  setsid xvfb-run -a -s "-screen 0 ${BB_SCREEN}" "$BB_BIN" \
    --no-sandbox --disable-dev-shm-usage --remote-debugging-port="$BB_CDP_PORT" \
    >"$boot_log" 2>&1 </dev/null &
  local boot_pgid=$!

  # Fast path: if blockbench_mcp is already persisted in StateMemory.installed_plugins,
  # it auto-loads within a few seconds and answers /ping with zero CDP interaction.
  local ping_json=""
  if ping_json="$(wait_for_ping 12)"; then
    log "Auto-load verified on startup: $ping_json"
    stop_pgid "$boot_pgid"
    log "Bootstrap instance stopped cleanly."
    return 0
  fi

  # Wait until Electron finishes loading index.html and exposes a page CDP target.
  local cdp_ready=0
  for _ in $(seq 1 30); do
    if curl -sf "http://127.0.0.1:${BB_CDP_PORT}/json" 2>/dev/null | grep -q 'index\.html'; then
      cdp_ready=1
      break
    fi
    sleep 0.5
  done

  if [[ "$cdp_ready" -ne 1 ]]; then
    stop_pgid "$boot_pgid"
    tail -n 30 "$boot_log" >&2 || true
    die "Blockbench CDP index.html target did not become ready on port ${BB_CDP_PORT}"
  fi

  if ! timeout 25 node - "$BB_CDP_PORT" "$plugin_js" <<'NODE_EOF'
const cdpPort = process.argv[2];
const pluginPath = process.argv[3];

(async () => {
  const targets = await fetch(`http://127.0.0.1:${cdpPort}/json`).then((r) => r.json());
  const page = targets.find(
    (t) => t.type === "page" && t.url && t.url.includes("index.html") && t.webSocketDebuggerUrl
  );
  if (!page) {
    throw new Error("No Blockbench index.html page target found on CDP");
  }
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("CDP WebSocket connect timeout")), 5000);
    ws.onopen = () => { clearTimeout(timer); resolve(); };
    ws.onerror = (e) => { clearTimeout(timer); reject(e); };
  });

  let reqSeq = 0;
  function evalJS(expression, timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
      const id = ++reqSeq;
      const timer = setTimeout(() => {
        ws.removeEventListener("message", onMsg);
        reject(new Error(`CDP Runtime.evaluate timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      const onMsg = (ev) => {
        const msg = JSON.parse(ev.data);
        if (msg.id === id) {
          clearTimeout(timer);
          ws.removeEventListener("message", onMsg);
          if (msg.error) reject(new Error(JSON.stringify(msg.error)));
          else if (msg.result?.exceptionDetails) {
            reject(new Error(JSON.stringify(msg.result.exceptionDetails)));
          } else {
            resolve(msg.result?.result?.value);
          }
        }
      };
      ws.addEventListener("message", onMsg);
      ws.send(
        JSON.stringify({
          id,
          method: "Runtime.evaluate",
          params: { expression, awaitPromise: true, returnByValue: true },
        })
      );
    });
  }

  for (let i = 0; i < 40; i++) {
    const ready = await evalJS(
      'typeof Plugins !== "undefined" && typeof Plugin !== "undefined" && typeof Blockbench !== "undefined"',
      3000
    );
    if (ready === true) break;
    await new Promise((r) => setTimeout(r, 250));
  }

  const res = await evalJS(`(async () => {
    if (Plugins.loading_promise) {
      await Promise.race([
        Plugins.loading_promise,
        new Promise((r) => setTimeout(r, 4000))
      ]).catch(() => {});
    }
    const existing = Plugins.installed.find((p) => p.id === "blockbench_mcp");
    if (!existing || existing.path !== ${JSON.stringify(pluginPath)}) {
      if (existing) {
        const idx = Plugins.installed.indexOf(existing);
        if (idx >= 0) Plugins.installed.splice(idx, 1);
      }
      const p = new Plugin("blockbench_mcp");
      await p.loadFromFile(
        { path: ${JSON.stringify(pluginPath)}, name: "blockbench_mcp.js", content: "" },
        false
      );
    }
    return {
      version: Blockbench.version,
      installed: Plugins.installed.map((p) => ({ id: p.id, source: p.source, path: p.path }))
    };
  })()`, 15000);

  console.log("[asset-tools] Plugin registration:", JSON.stringify(res));
  ws.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
NODE_EOF
  then
    stop_pgid "$boot_pgid"
    tail -n 30 "$boot_log" >&2 || true
    die "Failed to register blockbench_mcp via CDP"
  fi

  if ping_json="$(wait_for_ping 20)"; then
    log "Bootstrap bridge verified: $ping_json"
  else
    stop_pgid "$boot_pgid"
    tail -n 30 "$boot_log" >&2 || true
    die "Blockbench bridge did not respond on http://${BB_HOST}:${BB_PORT}/ping during bootstrap"
  fi

  stop_pgid "$boot_pgid"
  log "Bootstrap instance stopped cleanly."
}

start_blockbench() {
  [[ -x "$BB_BIN" ]] || die "Blockbench not installed at $BB_BIN. Run ./tools/setup_asset_tools.sh --install first."
  require_cmd xvfb-run

  local existing_ping=""
  if existing_ping="$(ping_bridge)"; then
    log "Blockbench bridge is already running: $existing_ping"
    return 0
  fi

  mkdir -p "$BB_STATE_DIR"
  log "Starting headless Blockbench (${BB_SCREEN}, SwiftShader WebGL) ..."
  setsid xvfb-run -a -s "-screen 0 ${BB_SCREEN}" "$BB_BIN" \
    --no-sandbox --disable-dev-shm-usage \
    >"$BB_LOG_FILE" 2>&1 </dev/null &
  local pgid=$!
  printf '%s\n' "$pgid" >"$BB_PGID_FILE"

  local ping_json=""
  if ping_json="$(wait_for_ping 50)"; then
    log "Headless Blockbench ready (pgid=$pgid): $ping_json"
    return 0
  fi

  stop_blockbench
  tail -n 40 "$BB_LOG_FILE" >&2 || true
  die "Headless Blockbench did not respond on http://${BB_HOST}:${BB_PORT}/ping"
}

stop_blockbench() {
  if [[ -f "$BB_PGID_FILE" ]]; then
    local pgid
    pgid="$(cat "$BB_PGID_FILE" 2>/dev/null || true)"
    if [[ -n "$pgid" ]]; then
      log "Stopping headless Blockbench process group (pgid=$pgid) ..."
      stop_pgid "$pgid"
    fi
    rm -f "$BB_PGID_FILE"
  else
    if pgrep -x blockbench >/dev/null 2>&1; then
      log "Stopping untracked blockbench process(es) ..."
      pkill -x blockbench 2>/dev/null || true
      sleep 1
    else
      log "No headless Blockbench process running."
    fi
  fi
}

print_status() {
  local mc_ver="not installed"
  if [[ -x "$LOCAL_BIN_DIR/mc-asset" ]]; then
    mc_ver="$("$LOCAL_BIN_DIR/mc-asset" --version 2>/dev/null || echo "error")"
  fi

  local bb_ver="not installed"
  if dpkg -s blockbench >/dev/null 2>&1; then
    bb_ver="$(dpkg-query -W -f='${Version}' blockbench 2>/dev/null || echo "unknown")"
  fi

  local mcp_status="not built"
  if [[ -f "$BB_MCP_DIR/dist/index.js" ]]; then
    mcp_status="built ($BB_MCP_DIR/dist/index.js)"
  fi

  local bridge_status="stopped"
  local ping_json=""
  if ping_json="$(ping_bridge)"; then
    bridge_status="running ($ping_json)"
  fi

  cat <<EOF
mc-asset:        $mc_ver ($LOCAL_BIN_DIR/mc-asset)
Blockbench:      $bb_ver ($BB_BIN)
blockbench-mcp:  $mcp_status
HTTP bridge:     $bridge_status (http://${BB_HOST}:${BB_PORT}/ping)
EOF
}

DO_INSTALL=0
DO_START=0
DO_STOP=0
DO_STATUS=0

if [[ $# -eq 0 ]]; then
  DO_INSTALL=1
else
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --install) DO_INSTALL=1 ;;
      --start-blockbench) DO_START=1 ;;
      --stop-blockbench) DO_STOP=1 ;;
      --status) DO_STATUS=1 ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option: $1 (use --help)" ;;
    esac
    shift
  done
fi

if [[ "$DO_STOP" -eq 1 ]]; then
  stop_blockbench
fi

if [[ "$DO_INSTALL" -eq 1 ]]; then
  install_mc_asset
  install_blockbench_mcp
  install_blockbench_deb
  configure_blockbench_headless
  bootstrap_blockbench_plugin
fi

if [[ "$DO_START" -eq 1 ]]; then
  start_blockbench
fi

if [[ "$DO_STATUS" -eq 1 ]]; then
  print_status
fi
