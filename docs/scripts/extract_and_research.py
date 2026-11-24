#!/usr/bin/env python3
"""Extract all manifest entries from DeceasedCraft v5.5.5, Beta 5.10.17, and Beta DH 5.10.17
and enrich every unique CurseForge project with CFWidget + CurseForge API file metadata."""

import concurrent.futures
import html
import json
import os
import re
import time
import zipfile
from pathlib import Path
import requests

SCRATCH = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch")
ARCHIVES = {
    "v5.5.5": SCRATCH / "archives/DeceasedCraft-5.5.5.zip",
    "beta_5.10.17": SCRATCH / "archives/DeceasedCraft_Beta-5.10.17.zip",
    "beta_dh_5.10.17": SCRATCH / "archives/DeceasedCraft_Beta_DH_Edition-5.10.17.zip",
}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "DeceasedCraft-Mod-Research/1.0"})


def parse_modlist_html(content: str) -> dict:
    """Return mapping of project_id (if extractable) or normalized URL -> {name, author, url}."""
    entries = []
    # Standard CurseForge modlist.html format: <li><a href="https://www.curseforge.com/projects/12345">Mod Name (by Author)</a></li>
    for m in re.finditer(r'<li><a\s+href="([^"]+)">([^<]+)</a></li>', content, re.IGNORECASE):
        url = html.unescape(m.group(1)).strip()
        raw_text = html.unescape(m.group(2)).strip()
        # Extract project ID if URL ends in /projects/<id>
        pid_m = re.search(r'/projects/(\d+)', url)
        pid = int(pid_m.group(1)) if pid_m else None
        # Split "Name (by Author)"
        name_m = re.match(r'^(.*?)\s*\(by\s+([^)]+)\)\s*$', raw_text)
        if name_m:
            name, author = name_m.group(1).strip(), name_m.group(2).strip()
        else:
            name, author = raw_text, ""
        entries.append({"projectID": pid, "name": name, "author": author, "url": url})
    return entries


def fetch_cfwidget(pid: int) -> dict:
    url = f"https://api.cfwidget.com/{pid}"
    for attempt in range(4):
        try:
            r = SESSION.get(url, timeout=15)
            if r.status_code == 200:
                return {"status": 200, "data": r.json()}
            elif r.status_code == 202:
                # CFWidget queued a refresh; wait and retry
                time.sleep(2.0 + attempt * 1.5)
                continue
            else:
                return {"status": r.status_code, "data": None}
        except Exception as e:
            if attempt == 3:
                return {"status": -1, "error": str(e), "data": None}
            time.sleep(1.0)
    return {"status": 202, "data": None}


def fetch_cf_file(pid: int, fid: int) -> dict:
    url = f"https://www.curseforge.com/api/v1/mods/{pid}/files/{fid}"
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=15)
            if r.status_code == 200:
                return {"status": 200, "data": r.json().get("data")}
            elif r.status_code in (429, 500, 502, 503):
                time.sleep(1.5 * (attempt + 1))
                continue
            else:
                return {"status": r.status_code, "data": None}
        except Exception as e:
            if attempt == 2:
                return {"status": -1, "error": str(e), "data": None}
            time.sleep(1.0)
    return {"status": -1, "data": None}


def main():
    packs_meta = {}
    modlist_by_pid = {}
    unique_pids = set()
    file_pairs = set()

    for key, zip_path in ARCHIVES.items():
        with zipfile.ZipFile(zip_path) as zf:
            jar_entries = [n for n in zf.namelist() if n.lower().endswith(".jar")]
            manifest = json.loads(zf.read("manifest.json"))
            modlist_raw = zf.read("modlist.html").decode("utf-8", errors="replace") if "modlist.html" in zf.namelist() else ""
            modlist_entries = parse_modlist_html(modlist_raw)
            for e in modlist_entries:
                if e["projectID"] is not None:
                    modlist_by_pid[e["projectID"]] = e

            files_map = {}
            for f in manifest.get("files", []):
                pid, fid = int(f["projectID"]), int(f["fileID"])
                files_map[pid] = fid
                unique_pids.add(pid)
                file_pairs.add((pid, fid))

            packs_meta[key] = {
                "name": manifest.get("name"),
                "version": manifest.get("version"),
                "minecraft": manifest.get("minecraft"),
                "manifest_count": len(files_map),
                "modlist_count": len(modlist_entries),
                "jar_entries_in_zip": jar_entries,
                "files": {str(k): v for k, v in files_map.items()},
            }
            print(f"[{key}] manifest={len(files_map)}, modlist={len(modlist_entries)}, jars_in_zip={jar_entries}")

    print(f"Total unique projectIDs: {len(unique_pids)}, unique (pid, fid) pairs: {len(file_pairs)}")

    # 1. Fetch CFWidget metadata for all unique projectIDs
    print("Fetching CFWidget metadata...")
    cfwidget_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        fut_to_pid = {ex.submit(fetch_cfwidget, pid): pid for pid in sorted(unique_pids)}
        done = 0
        for fut in concurrent.futures.as_completed(fut_to_pid):
            pid = fut_to_pid[fut]
            cfwidget_results[str(pid)] = fut.result()
            done += 1
            if done % 100 == 0 or done == len(unique_pids):
                print(f"  CFWidget: {done}/{len(unique_pids)}")

    ok_cfw = sum(1 for v in cfwidget_results.values() if v["status"] == 200)
    print(f"CFWidget HTTP 200: {ok_cfw}/{len(unique_pids)}")

    # 2. Fetch exact CurseForge file metadata for all (pid, fid) pairs
    print("Fetching CurseForge exact file metadata...")
    cf_file_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        fut_to_pair = {ex.submit(fetch_cf_file, pid, fid): (pid, fid) for pid, fid in sorted(file_pairs)}
        done = 0
        for fut in concurrent.futures.as_completed(fut_to_pair):
            pid, fid = fut_to_pair[fut]
            cf_file_results[f"{pid}:{fid}"] = fut.result()
            done += 1
            if done % 100 == 0 or done == len(file_pairs):
                print(f"  CF File API: {done}/{len(file_pairs)}")

    ok_cff = sum(1 for v in cf_file_results.values() if v["status"] == 200 and v["data"])
    print(f"CF File API HTTP 200: {ok_cff}/{len(file_pairs)}")

    out = {
        "packs": packs_meta,
        "modlist_by_pid": {str(k): v for k, v in modlist_by_pid.items()},
        "cfwidget": cfwidget_results,
        "cf_files": cf_file_results,
    }
    out_path = SCRATCH / "extracted_data.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved extracted data to {out_path} ({out_path.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
