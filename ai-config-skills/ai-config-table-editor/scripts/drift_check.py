# -*- coding: utf-8 -*-
"""漂移巡检：本地表格导出的 JSON 与 Apollo 实际内容逐命名空间比对。只读。

用法:
  python drift_check.py --json-dir <服务端 JSON 目录> [--released] [--json]

环境变量:
  APOLLO_PORTAL_URL   Portal/OpenAPI 根地址，如 http://apollo.example.com:8080
  APOLLO_APP_ID       目标 AppId
  APOLLO_ENV          环境，如 DEV
  APOLLO_CLUSTER      集群，如 default
  APOLLO_TOKEN        该 App 的 OpenAPI Token（不要提交到仓库）

默认比对 Apollo 草稿；--released 额外报告"草稿是否已发布"。有漂移时退出码为 1。
"""
import glob
import json
import os
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def env(name, required=True, default=""):
    v = os.environ.get(name, default)
    if required and not v:
        raise SystemExit(f"缺少环境变量 {name}")
    return v


def api(path):
    base = env("APOLLO_PORTAL_URL").rstrip("/")
    req = urllib.request.Request(base + path, headers={"Authorization": env("APOLLO_TOKEN")})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", "replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"__error__": "非 JSON 响应"}
    except urllib.error.HTTPError as e:
        return {"__error__": e.code}


def ns_path(suffix=""):
    return (f"/openapi/v1/envs/{env('APOLLO_ENV', default='DEV')}"
            f"/apps/{env('APOLLO_APP_ID')}/clusters/{env('APOLLO_CLUSTER', default='default')}"
            f"/namespaces{suffix}")


def canon(obj):
    if isinstance(obj, dict):
        return "{" + ",".join(f'"{k}":{canon(obj[k])}' for k in sorted(obj)) + "}"
    if isinstance(obj, list):
        return "[" + ",".join(canon(x) for x in obj) + "]"
    return json.dumps(obj, ensure_ascii=False)


def key_of(e):
    if isinstance(e, dict):
        for k in ("sn", "param", "id"):
            if k in e:
                return str(e[k])
    return None


def summarize(local_text, apollo_text):
    a, b = json.loads(local_text), json.loads(apollo_text)
    if not isinstance(a, list) or not isinstance(b, list):
        return "非数组，内容不同"
    ha = {key_of(x): canon(x) for x in a}
    hb = {key_of(x): canon(x) for x in b}
    add = [k for k in ha if k not in hb]
    dele = [k for k in hb if k not in ha]
    mod = [k for k in ha if k in hb and ha[k] != hb[k]]
    parts = []
    if add:
        parts.append(f"本地多 {len(add)}({','.join(add[:6])}{'…' if len(add) > 6 else ''})")
    if dele:
        parts.append(f"Apollo 多 {len(dele)}({','.join(dele[:6])}{'…' if len(dele) > 6 else ''})")
    if mod:
        parts.append(f"字段不同 {len(mod)}({','.join(mod[:6])}{'…' if len(mod) > 6 else ''})")
    return "；".join(parts) or "内容一致（仅序列化差异）"


def main(argv):
    check_released = "--released" in argv
    as_json = "--json" in argv
    json_dir = None
    if "--json-dir" in argv:
        json_dir = argv[argv.index("--json-dir") + 1]
    if not json_dir:
        raise SystemExit("请用 --json-dir 指定服务端 JSON 目录")

    nss = api(ns_path())
    if isinstance(nss, dict) and nss.get("__error__"):
        raise SystemExit(f"读取 Apollo 命名空间失败: {nss}")
    apollo = {}
    for n in nss:
        v = [i["value"] for i in (n.get("items") or []) if i.get("key") == "content"]
        apollo[n["namespaceName"]] = v[0] if v else None

    rows = []
    for f in sorted(glob.glob(os.path.join(json_dir, "Conf*.json"))):
        ns = os.path.basename(f)[:-5]
        local = open(f, encoding="utf-8").read().strip()
        if ns not in apollo:
            rows.append({"ns": ns, "state": "无命名空间"})
            continue
        rem = apollo[ns]
        if rem is None:
            rows.append({"ns": ns, "state": "Apollo 无内容"})
            continue
        if local == rem:
            rows.append({"ns": ns, "state": "一致", "note": ""})
            continue
        try:
            same = canon(json.loads(local)) == canon(json.loads(rem))
        except Exception:
            same = False
        if same:
            rows.append({"ns": ns, "state": "一致(格式差异)", "note": ""})
        else:
            rows.append({"ns": ns, "state": "漂移", "note": summarize(local, rem)})

    pending = []
    if check_released:
        for r in rows:
            if r["state"] not in ("一致", "一致(格式差异)"):
                continue
            rel = api(ns_path(f"/{r['ns']}/releases/latest"))
            if isinstance(rel, dict) and rel.get("__error__"):
                r["release"] = "从未发布"
                pending.append((r["ns"], "从未发布"))
            elif (rel.get("configurations") or {}).get("content") != apollo.get(r["ns"]):
                r["release"] = "草稿未发布"
                pending.append((r["ns"], f"草稿未发布 releaseId={rel.get('id')}"))
            else:
                r["release"] = "已发布"

    if as_json:
        print(json.dumps({"rows": rows, "pending": pending}, ensure_ascii=False, indent=1))
        return 0

    drift = [r for r in rows if r["state"] == "漂移"]
    other = [r for r in rows if r["state"] in ("无命名空间", "Apollo 无内容")]
    print("=" * 64)
    print("表格 ↔ Apollo 漂移巡检（只读）")
    print("=" * 64)
    for r in drift:
        print(f"[漂移]     {r['ns']:<26} {r['note']}")
    for r in other:
        print(f"[{r['state']}] {r['ns']}")
    if check_released:
        for ns, why in pending:
            print(f"[待发布]   {ns:<26} {why}")
    print("-" * 64)
    print(f"共 {len(rows)} 个产物：一致 {len(rows) - len(drift) - len(other)}，漂移 {len(drift)}，其他 {len(other)}"
          + (f"，待发布 {len(pending)}" if check_released else ""))
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
