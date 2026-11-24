#!/usr/bin/env python3
"""Filter to actual mods (logging all excluded non-mods) and perform multi-source
MC 1.20.1 (Forge) compatibility verification for every v5.5.5 mod."""

import concurrent.futures
import json
import re
import time
from collections import Counter
from pathlib import Path
import requests

SCRATCH = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p_devbox/03eb4a1d-2cfb-4f0e-b820-e5ef724e5ea6/scratch")
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "DeceasedCraft-Mod-Research/1.0"})


def has_forge_1201_cfwidget(cfw: dict) -> tuple[bool, str | None]:
    """Check if CFWidget versions['1.20.1'] has a Forge-compatible release."""
    versions = cfw.get("versions") or {}
    files_1201 = versions.get("1.20.1") or []
    for f in files_1201:
        vtags = set(f.get("versions") or [])
        fname = (f.get("name") or "").lower()
        if "Forge" in vtags:
            return True, f"CFWidget: {f.get('name')} ({f.get('id')})"
        # Some older/untagged uploads omit loader tags; only accept if not explicitly Fabric/Quilt/NeoForge
        loaders = vtags & {"Forge", "Fabric", "Quilt", "NeoForge", "Rift", "LiteLoader"}
        if not loaders and "fabric" not in fname and "quilt" not in fname and "neoforge" not in fname and fname.endswith(".jar"):
            return True, f"CFWidget (untagged loader): {f.get('name')} ({f.get('id')})"
    return False, None


def check_cf_live_files_1201(pid: int) -> tuple[bool, str | None, list[str]]:
    """Paginate live CurseForge API files to check for any 1.20.1 Forge release."""
    page_index = 0
    page_size = 50
    all_mc_versions = set()
    while True:
        url = f"https://www.curseforge.com/api/v1/mods/{pid}/files?pageIndex={page_index}&pageSize={page_size}"
        r = None
        for attempt in range(3):
            try:
                r = SESSION.get(url, timeout=15)
                if r.status_code == 200:
                    break
                time.sleep(1.0 * (attempt + 1))
            except Exception:
                time.sleep(1.0)
        if not r or r.status_code != 200:
            break
        payload = r.json()
        data = payload.get("data") or []
        if not data:
            break
        for f in data:
            gvs = set(f.get("gameVersions") or [])
            for gv in gvs:
                if re.match(r"^1\.\d+", gv):
                    all_mc_versions.add(gv)
            if "1.20.1" in gvs:
                fname = (f.get("fileName") or "").lower()
                if "Forge" in gvs:
                    return True, f"CF Live API: {f.get('fileName')} ({f.get('id')})", sorted(all_mc_versions)
                loaders = gvs & {"Forge", "Fabric", "Quilt", "NeoForge"}
                if not loaders and "fabric" not in fname and "quilt" not in fname and "neoforge" not in fname and fname.endswith(".jar"):
                    return True, f"CF Live API (untagged): {f.get('fileName')} ({f.get('id')})", sorted(all_mc_versions)
        pag = payload.get("pagination") or {}
        total = pag.get("totalCount", 0)
        if (page_index + 1) * page_size >= total or page_index >= 10:
            break
        page_index += 1
    return False, None, sorted(all_mc_versions)


def check_modrinth_1201(title: str, slug: str) -> list[dict]:
    """Search Modrinth for matching Forge 1.20.1 mod candidates (returns top candidates for verification)."""
    candidates = []
    seen_ids = set()
    queries = []
    if slug:
        queries.append(slug)
    if title and title.lower() != (slug or "").lower():
        queries.append(title)

    for q in queries:
        try:
            r = SESSION.get(
                "https://api.modrinth.com/v2/search",
                params={
                    "query": q,
                    "facets": json.dumps([["project_type:mod"], ["categories:forge"], ["versions:1.20.1"]]),
                    "limit": 5,
                },
                timeout=12,
            )
            if r.status_code != 200:
                continue
            for hit in r.json().get("hits", []):
                pid = hit.get("project_id")
                if pid in seen_ids:
                    continue
                seen_ids.add(pid)
                h_slug = (hit.get("slug") or "").lower()
                h_title = (hit.get("title") or "").lower()
                t_norm = re.sub(r"[^a-z0-9]", "", title.lower())
                s_norm = re.sub(r"[^a-z0-9]", "", (slug or "").lower())
                ht_norm = re.sub(r"[^a-z0-9]", "", h_title)
                hs_norm = re.sub(r"[^a-z0-9]", "", h_slug)
                exact = (ht_norm == t_norm) or (hs_norm == s_norm) or (ht_norm == s_norm) or (hs_norm == t_norm)
                partial = (t_norm and (t_norm in ht_norm or ht_norm in t_norm)) or (s_norm and (s_norm in hs_norm or hs_norm in s_norm))
                if exact or partial:
                    candidates.append({
                        "project_id": pid,
                        "slug": hit.get("slug"),
                        "title": hit.get("title"),
                        "author": hit.get("author"),
                        "url": f"https://modrinth.com/mod/{hit.get('slug')}",
                        "exact_match": exact,
                        "description": hit.get("description", ""),
                    })
        except Exception:
            pass
    # Sort exact matches first
    candidates.sort(key=lambda x: (not x["exact_match"], x["title"].lower()))
    return candidates[:3]


def main():
    raw = json.loads((SCRATCH / "extracted_data.json").read_text(encoding="utf-8"))
    packs = raw["packs"]
    cfwidget = raw["cfwidget"]
    cf_files = raw["cf_files"]
    modlist_by_pid = raw["modlist_by_pid"]

    v555_files = packs["v5.5.5"]["files"]
    v6_std_files = packs["beta_5.10.17"]["files"]
    v6_dh_files = packs["beta_dh_5.10.17"]["files"]

    all_pids = sorted(set(v555_files.keys()) | set(v6_std_files.keys()) | set(v6_dh_files.keys()), key=int)

    # 1. Inspect project types and filter Mods vs Non-Mods
    type_counts = Counter()
    non_mods = []
    mods = {}

    for pid_str in all_pids:
        cfw = cfwidget[pid_str]["data"]
        ptype = cfw.get("type", "Unknown")
        cf_url = (cfw.get("urls") or {}).get("curseforge") or f"https://www.curseforge.com/projects/{pid_str}"
        title = cfw.get("title") or (modlist_by_pid.get(pid_str) or {}).get("name") or f"Project {pid_str}"
        slug = cf_url.rstrip("/").split("/")[-1] if "/mc-mods/" in cf_url or "/texture-packs/" in cf_url or "/shaders/" in cf_url else ""

        # File info in each pack
        f_555 = cf_files.get(f"{pid_str}:{v555_files[pid_str]}", {}).get("data") if pid_str in v555_files else None
        f_std = cf_files.get(f"{pid_str}:{v6_std_files[pid_str]}", {}).get("data") if pid_str in v6_std_files else None
        f_dh = cf_files.get(f"{pid_str}:{v6_dh_files[pid_str]}", {}).get("data") if pid_str in v6_dh_files else None

        in_555 = pid_str in v555_files
        in_v6_std = pid_str in v6_std_files
        in_v6_dh = pid_str in v6_dh_files
        in_v6 = in_v6_std or in_v6_dh

        type_counts[ptype] += 1

        is_mod = (ptype == "Mods") or ("/mc-mods/" in cf_url)
        if not is_mod:
            non_mods.append({
                "pid": int(pid_str),
                "title": title,
                "type": ptype,
                "url": cf_url,
                "in_555": in_555,
                "in_v6_std": in_v6_std,
                "in_v6_dh": in_v6_dh,
                "file_555": f_555.get("fileName") if f_555 else None,
                "file_v6": (f_std or f_dh).get("fileName") if (f_std or f_dh) else None,
            })
            continue

        # Determine edition for v6
        if in_v6_std and in_v6_dh:
            v6_edition = "Standard"
        elif in_v6_dh and not in_v6_std:
            v6_edition = "DH Edition Extra"
        elif in_v6_std and not in_v6_dh:
            v6_edition = "Standard Only"
        else:
            v6_edition = None

        mods[pid_str] = {
            "pid": int(pid_str),
            "title": title,
            "slug": slug,
            "summary": (cfw.get("summary") or "").strip(),
            "cf_categories": cfw.get("categories") or [],
            "url": cf_url,
            "members": [m.get("username") for m in (cfw.get("members") or [])],
            "in_555": in_555,
            "in_v6": in_v6,
            "in_both": in_555 and in_v6,
            "v6_edition": v6_edition,
            "file_555": f_555.get("fileName") if f_555 else None,
            "display_555": f_555.get("displayName") if f_555 else None,
            "file_v6": (f_std or f_dh).get("fileName") if (f_std or f_dh) else None,
            "display_v6": (f_std or f_dh).get("displayName") if (f_std or f_dh) else None,
            "cfw_versions_keys": sorted((cfw.get("versions") or {}).keys()),
        }

    print("=== Project Type Breakdown ===")
    for k, v in type_counts.items():
        print(f"  {k}: {v}")
    print(f"\n=== Excluded Non-Mods ({len(non_mods)}) ===")
    for nm in non_mods:
        packs_str = ", ".join([p for p, b in [("v5.5.5", nm["in_555"]), ("v6_std", nm["in_v6_std"]), ("v6_dh", nm["in_v6_dh"])] if b])
        print(f"  [{nm['type']}] {nm['title']} (pid={nm['pid']}) | packs={packs_str} | file555={nm['file_555']} | fileV6={nm['file_v6']}")

    # 2. Verify MC 1.20.1 Forge support for all v5.5.5 mods
    v555_mod_pids = [pid for pid, m in mods.items() if m["in_555"]]
    v6_mod_pids = [pid for pid, m in mods.items() if m["in_v6"]]
    shared_mod_pids = [pid for pid, m in mods.items() if m["in_both"]]
    print(f"\n=== Filtered Mod Counts ===")
    print(f"  v5.5.5 Mods: {len(v555_mod_pids)}")
    print(f"  Beta 5.10.17 (+DH) Mods: {len(v6_mod_pids)}")
    print(f"  Shared Mods (by projectID): {len(shared_mod_pids)}")
    print(f"  Total Unique Mods: {len(mods)}")

    need_live_cf = []
    for pid in v555_mod_pids:
        m = mods[pid]
        if m["in_v6"]:
            m["supported_1201_forge"] = True
            m["compat_evidence"] = f"Included in Beta 5.10.17 ({m['file_v6']})"
            continue
        ok, ev = has_forge_1201_cfwidget(cfwidget[pid]["data"])
        if ok:
            m["supported_1201_forge"] = True
            m["compat_evidence"] = ev
        else:
            m["supported_1201_forge"] = False
            m["compat_evidence"] = None
            need_live_cf.append(pid)

    print(f"\nChecking {len(need_live_cf)} remaining v5.5.5 mods against Live CurseForge API...")
    need_modrinth = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(check_cf_live_files_1201, int(pid)): pid for pid in need_live_cf}
        for fut in concurrent.futures.as_completed(futs):
            pid = futs[fut]
            ok, ev, mc_vers = fut.result()
            mods[pid]["cf_live_mc_versions"] = mc_vers
            if ok:
                mods[pid]["supported_1201_forge"] = True
                mods[pid]["compat_evidence"] = ev
            else:
                need_modrinth.append(pid)

    print(f"Still 'No' after CurseForge Live API: {len(need_modrinth)} mods. Checking Modrinth...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(check_modrinth_1201, mods[pid]["title"], mods[pid]["slug"]): pid for pid in need_modrinth}
        for fut in concurrent.futures.as_completed(futs):
            pid = futs[fut]
            cands = fut.result()
            mods[pid]["modrinth_candidates"] = cands

    # Print summary of remaining 'No' mods and any Modrinth candidates
    yes_cnt = sum(1 for pid in v555_mod_pids if mods[pid]["supported_1201_forge"])
    no_pids = sorted([pid for pid in v555_mod_pids if not mods[pid]["supported_1201_forge"]], key=lambda p: mods[p]["title"].lower())
    print(f"\n=== Preliminary v5.5.5 -> 1.20.1 Forge Support ===")
    print(f"  Yes (CurseForge verified): {yes_cnt}")
    print(f"  Needs manual review / No on CF: {len(no_pids)}")
    print("\n--- Detailed List of Mods NOT found for 1.20.1 Forge on CurseForge ---")
    for pid in no_pids:
        m = mods[pid]
        mr = m.get("modrinth_candidates") or []
        mr_str = "; ".join([f"{'*EXACT* ' if c['exact_match'] else ''}{c['title']} ({c['url']})" for c in mr]) if mr else "None"
        latest_mc = m.get("cf_live_mc_versions") or m.get("cfw_versions_keys")
        print(f"  [{pid}] {m['title']} | CF versions: {latest_mc[-3:] if latest_mc else []} | Modrinth: {mr_str}")

    out = {
        "pack_metadata": {
            k: {mk: mv for mk, mv in v.items() if mk != "files"}
            for k, v in packs.items()
        },
        "excluded_non_mods": non_mods,
        "mods": mods,
    }
    out_path = SCRATCH / "compiled_mods.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved compiled catalog to {out_path}")


if __name__ == "__main__":
    main()
