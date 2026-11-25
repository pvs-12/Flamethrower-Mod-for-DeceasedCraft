#!/usr/bin/env node
/**
 * Zero-dependency CLI bridge for sosadly/blockbench-mcp.
 *
 * Spawns the built blockbench-mcp stdio server (default:
 * ~/.local/share/blockbench-mcp/dist/index.js) and speaks MCP JSON-RPC 2.0
 * over stdin/stdout so coding agents and scripts can call any Blockbench MCP
 * tool directly from the command line.
 *
 * Usage:
 *   node tools/bb_mcp_client.mjs ping
 *   node tools/bb_mcp_client.mjs list_tools [--json] [--filter <text>]
 *   node tools/bb_mcp_client.mjs describe <tool_name>
 *   node tools/bb_mcp_client.mjs call <tool_name> [json_args | @file.json | -] [--save-images <dir>] [--raw]
 *   node tools/bb_mcp_client.mjs batch <file.json | -> [--save-images <dir>] [--raw]
 *
 * Environment variables:
 *   BLOCKBENCH_MCP_DIR        Path to blockbench-mcp checkout (default: ~/.local/share/blockbench-mcp)
 *   BLOCKBENCH_MCP_HOST       Bridge host (default: 127.0.0.1)
 *   BLOCKBENCH_MCP_PORT       Bridge port (default: 8787)
 *   BLOCKBENCH_MCP_TIMEOUT_MS Per-request timeout in ms (default: 180000)
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const MCP_DIR =
  process.env.BLOCKBENCH_MCP_DIR ||
  path.join(os.homedir(), ".local", "share", "blockbench-mcp");
const SERVER_ENTRY = path.join(MCP_DIR, "dist", "index.js");
const HOST = process.env.BLOCKBENCH_MCP_HOST || "127.0.0.1";
const PORT = Number(process.env.BLOCKBENCH_MCP_PORT) || 8787;
const TIMEOUT_MS = Number(process.env.BLOCKBENCH_MCP_TIMEOUT_MS) || 180_000;

function printUsage(exitCode = 0) {
  const out = exitCode === 0 ? console.log : console.error;
  out(`Usage:
  node tools/bb_mcp_client.mjs ping
  node tools/bb_mcp_client.mjs list_tools [--json] [--filter <substr>]
  node tools/bb_mcp_client.mjs describe <tool_name>
  node tools/bb_mcp_client.mjs call <tool_name> [json_args | @file.json | -] [--save-images <dir>] [--raw]
  node tools/bb_mcp_client.mjs batch <file.json | -> [--save-images <dir>] [--raw]

Environment:
  BLOCKBENCH_MCP_DIR        Default: ~/.local/share/blockbench-mcp
  BLOCKBENCH_MCP_HOST       Default: 127.0.0.1
  BLOCKBENCH_MCP_PORT       Default: 8787
  BLOCKBENCH_MCP_TIMEOUT_MS Default: 180000`);
  process.exit(exitCode);
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}

async function parseJsonInput(spec, defaultValue = {}) {
  if (spec === undefined || spec === null || spec === "") {
    return defaultValue;
  }
  let raw;
  if (spec === "-") {
    raw = await readStdin();
  } else if (spec.startsWith("@")) {
    const filePath = spec.slice(1);
    raw = fs.readFileSync(filePath, "utf8");
  } else {
    raw = spec;
  }
  const trimmed = raw.trim();
  if (!trimmed) return defaultValue;
  try {
    return JSON.parse(trimmed);
  } catch (err) {
    throw new Error(`Invalid JSON input: ${err.message}`);
  }
}

class McpStdioClient {
  constructor(serverEntry, env) {
    if (!fs.existsSync(serverEntry)) {
      throw new Error(
        `blockbench-mcp server not found at ${serverEntry}. ` +
          `Run tools/setup_asset_tools.sh or set BLOCKBENCH_MCP_DIR.`
      );
    }
    this.proc = spawn(process.execPath, [serverEntry], {
      env,
      stdio: ["pipe", "pipe", "pipe"],
    });
    this.nextId = 1;
    this.pending = new Map();
    this.buffer = "";
    this.stderrLines = [];
    this.closed = false;

    this.proc.stdout.setEncoding("utf8");
    this.proc.stdout.on("data", (chunk) => this._onData(chunk));
    this.proc.stderr.setEncoding("utf8");
    this.proc.stderr.on("data", (chunk) => {
      this.stderrLines.push(chunk);
    });
    this.proc.on("exit", (code, signal) => {
      this.closed = true;
      for (const [, entry] of this.pending) {
        clearTimeout(entry.timer);
        entry.reject(
          new Error(
            `MCP server exited unexpectedly (code=${code}, signal=${signal}).\n` +
              this.stderrLines.join("")
          )
        );
      }
      this.pending.clear();
    });
    this.proc.on("error", (err) => {
      this.closed = true;
      for (const [, entry] of this.pending) {
        clearTimeout(entry.timer);
        entry.reject(err);
      }
      this.pending.clear();
    });
  }

  _onData(chunk) {
    this.buffer += chunk;
    let nl;
    while ((nl = this.buffer.indexOf("\n")) !== -1) {
      const line = this.buffer.slice(0, nl).replace(/\r$/, "");
      this.buffer = this.buffer.slice(nl + 1);
      if (!line.trim()) continue;
      let msg;
      try {
        msg = JSON.parse(line);
      } catch {
        continue;
      }
      if (msg.id !== undefined && this.pending.has(msg.id)) {
        const entry = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        clearTimeout(entry.timer);
        if (msg.error) {
          entry.reject(
            new Error(
              `MCP error ${msg.error.code ?? ""}: ${msg.error.message ?? JSON.stringify(msg.error)}`
            )
          );
        } else {
          entry.resolve(msg.result);
        }
      }
    }
  }

  request(method, params = {}, timeoutMs = TIMEOUT_MS) {
    if (this.closed) {
      return Promise.reject(new Error("MCP server process is closed."));
    }
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`MCP request "${method}" timed out after ${timeoutMs}ms.`));
      }, timeoutMs);
      this.pending.set(id, { resolve, reject, timer });
      const payload = JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n";
      this.proc.stdin.write(payload);
    });
  }

  notify(method, params = {}) {
    if (this.closed) return;
    const payload = JSON.stringify({ jsonrpc: "2.0", method, params }) + "\n";
    this.proc.stdin.write(payload);
  }

  async initialize() {
    const initResult = await this.request("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "tacticalchemthrowers-bb-cli", version: "1.0.0" },
    });
    this.notify("notifications/initialized", {});
    return initResult;
  }

  async close() {
    if (this.closed) return;
    this.closed = true;
    try {
      this.proc.stdin.end();
    } catch {}
    await new Promise((resolve) => {
      const timer = setTimeout(() => {
        try {
          this.proc.kill("SIGTERM");
        } catch {}
        resolve();
      }, 500);
      this.proc.once("exit", () => {
        clearTimeout(timer);
        resolve();
      });
    });
  }
}

function mimeToExt(mimeType = "") {
  if (mimeType.includes("png")) return ".png";
  if (mimeType.includes("jpeg") || mimeType.includes("jpg")) return ".jpg";
  if (mimeType.includes("webp")) return ".webp";
  if (mimeType.includes("gif")) return ".gif";
  return ".bin";
}

function renderCallResult(toolName, result, { saveImagesDir, raw, imageCounter }) {
  if (raw) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  const content = Array.isArray(result?.content) ? result.content : [];
  if (saveImagesDir) {
    fs.mkdirSync(saveImagesDir, { recursive: true });
  }
  for (const block of content) {
    if (block.type === "text") {
      console.log(block.text);
    } else if (block.type === "image" && typeof block.data === "string") {
      const buf = Buffer.from(block.data, "base64");
      const ext = mimeToExt(block.mimeType);
      const idx = ++imageCounter.count;
      if (saveImagesDir) {
        const safeTool = toolName.replace(/[^a-zA-Z0-9_-]/g, "_");
        const outPath = path.join(saveImagesDir, `${safeTool}_${idx}${ext}`);
        fs.writeFileSync(outPath, buf);
        console.log(`[image saved] ${outPath} (${buf.length} bytes, ${block.mimeType || "image/png"})`);
      } else {
        console.log(
          `[image omitted] ${buf.length} bytes (${block.mimeType || "image/png"}) — pass --save-images <dir> to write PNGs`
        );
      }
    } else {
      console.log(JSON.stringify(block, null, 2));
    }
  }
}

async function cmdPing() {
  const url = `http://${HOST}:${PORT}/ping`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 4000);
  try {
    const res = await fetch(url, { signal: controller.signal });
    const text = await res.text();
    if (!res.ok) {
      console.error(`HTTP ${res.status} from ${url}: ${text}`);
      process.exit(1);
    }
    console.log(text);
  } catch (err) {
    console.error(`Failed to reach Blockbench bridge at ${url}: ${err.message}`);
    process.exit(1);
  } finally {
    clearTimeout(timer);
  }
}

async function withClient(fn) {
  const env = {
    ...process.env,
    BLOCKBENCH_MCP_HOST: HOST,
    BLOCKBENCH_MCP_PORT: String(PORT),
  };
  const client = new McpStdioClient(SERVER_ENTRY, env);
  try {
    await client.initialize();
    return await fn(client);
  } finally {
    await client.close();
  }
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length === 0 || argv[0] === "-h" || argv[0] === "--help") {
    printUsage(0);
  }

  const command = argv[0];

  if (command === "ping") {
    await cmdPing();
    return;
  }

  if (command === "list_tools" || command === "list-tools") {
    let asJson = false;
    let filter = "";
    for (let i = 1; i < argv.length; i++) {
      if (argv[i] === "--json") asJson = true;
      else if (argv[i] === "--filter" && argv[i + 1]) filter = argv[++i].toLowerCase();
      else {
        console.error(`Unknown option: ${argv[i]}`);
        printUsage(2);
      }
    }
    await withClient(async (client) => {
      const res = await client.request("tools/list", {});
      let tools = res.tools || [];
      if (filter) {
        tools = tools.filter(
          (t) =>
            t.name.toLowerCase().includes(filter) ||
            (t.description || "").toLowerCase().includes(filter)
        );
      }
      if (asJson) {
        console.log(JSON.stringify(tools, null, 2));
      } else {
        console.log(`Available Blockbench MCP tools (${tools.length}):`);
        for (const t of tools) {
          const firstLine = (t.description || "").split("\n")[0].trim();
          const summary = firstLine.length > 96 ? firstLine.slice(0, 93) + "..." : firstLine;
          console.log(`  ${t.name.padEnd(26)} ${summary}`);
        }
      }
    });
    return;
  }

  if (command === "describe") {
    const toolName = argv[1];
    if (!toolName) {
      console.error("Missing <tool_name>.");
      printUsage(2);
    }
    await withClient(async (client) => {
      const res = await client.request("tools/list", {});
      const tool = (res.tools || []).find((t) => t.name === toolName);
      if (!tool) {
        console.error(`Tool not found: ${toolName}`);
        process.exit(1);
      }
      console.log(JSON.stringify(tool, null, 2));
    });
    return;
  }

  if (command === "call") {
    const toolName = argv[1];
    if (!toolName) {
      console.error("Missing <tool_name>.");
      printUsage(2);
    }
    let argsSpec;
    let saveImagesDir = null;
    let raw = false;
    for (let i = 2; i < argv.length; i++) {
      const tok = argv[i];
      if (tok === "--save-images" && argv[i + 1]) {
        saveImagesDir = argv[++i];
      } else if (tok === "--raw") {
        raw = true;
      } else if (argsSpec === undefined) {
        argsSpec = tok;
      } else {
        console.error(`Unexpected argument: ${tok}`);
        printUsage(2);
      }
    }
    const toolArgs = await parseJsonInput(argsSpec, {});
    const imageCounter = { count: 0 };
    await withClient(async (client) => {
      const result = await client.request("tools/call", {
        name: toolName,
        arguments: toolArgs,
      });
      renderCallResult(toolName, result, { saveImagesDir, raw, imageCounter });
      if (result?.isError) {
        process.exitCode = 1;
      }
    });
    return;
  }

  if (command === "batch") {
    const spec = argv[1];
    if (!spec) {
      console.error("Missing <file.json | -> for batch.");
      printUsage(2);
    }
    let saveImagesDir = null;
    let raw = false;
    for (let i = 2; i < argv.length; i++) {
      const tok = argv[i];
      if (tok === "--save-images" && argv[i + 1]) {
        saveImagesDir = argv[++i];
      } else if (tok === "--raw") {
        raw = true;
      } else {
        console.error(`Unexpected argument: ${tok}`);
        printUsage(2);
      }
    }
    const steps = await parseJsonInput(spec === "-" ? "-" : spec.startsWith("@") ? spec : `@${spec}`, []);
    if (!Array.isArray(steps)) {
      throw new Error("Batch input must be a JSON array of { tool, args } objects.");
    }
    const imageCounter = { count: 0 };
    await withClient(async (client) => {
      for (let idx = 0; idx < steps.length; idx++) {
        const step = steps[idx];
        const toolName = step.tool || step.name;
        const toolArgs = step.args || step.arguments || {};
        if (!toolName) {
          throw new Error(`Batch step ${idx} is missing "tool".`);
        }
        if (!raw) {
          console.log(`=== [${idx + 1}/${steps.length}] ${toolName} ===`);
        }
        const result = await client.request("tools/call", {
          name: toolName,
          arguments: toolArgs,
        });
        renderCallResult(toolName, result, { saveImagesDir, raw, imageCounter });
        if (result?.isError) {
          process.exitCode = 1;
          break;
        }
      }
    });
    return;
  }

  console.error(`Unknown command: ${command}`);
  printUsage(2);
}

main().catch((err) => {
  console.error(err?.message || String(err));
  process.exit(1);
});
