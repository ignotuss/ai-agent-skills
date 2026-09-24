# -*- coding: utf-8 -*-
"""发布状态自动回填：用 Apollo 的 releases/latest 核对草稿与线上版本，回填操作日志。

用法:
  python backfill_release_status.py --logs <日志目录> [--dry-run]

日志格式：每行一个 JSON 对象（JSONL），至少包含 logId 与 apollo 字段；
apollo 可以是对象或对象数组，每项形如：
  {"namespace": "ConfShop", "action": "PUT", "release": {"requested": false, "confirmed": false}}

判定：某命名空间的草稿内容 == 最新发布内容 → 该记录回填 confirmed=true + releaseId + 证据；
      不同 → 保持待发布。

环境变量: APOLLO_PORTAL_URL / APOLLO_APP_ID / APOLLO_ENV / APOLLO_CLUSTER / APOLLO_TOKEN
"""
import datetime
import glob
import json
import os
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def env(name, default=""):
    v = os.environ.get(name, default)
    if not v:
        raise SystemExit(f"缺少环境变量 {name}")
    return v


def api(path):
    base = env("APOLLO_PORTAL_URL").rstrip("/")
    req = urllib.request.Request(base + path, headers={"Authorization": env("APOLLO_TOKEN")})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return {"__error__": e.code}


def ns_path(suffix=""):
    return (f"/openapi/v1/envs/{env('APOLLO_ENV', 'DEV')}"
            f"/apps/{env('APOLLO_APP_ID')}/clusters/{env('APOLLO_CLUSTER', 'default')}"
            f"/namespaces{suffix}")


def records(entry):
    ap = entry.get("apollo")
    if isinstance(ap, dict):
        return [ap], "dict"
    if isinstance(ap, list):
        return ap, "list"
    return [], "none"


def main(argv):
    dry = "--dry-run" in argv
    log_dir = argv[argv.index("--logs") + 1] if "--logs" in argv else "logs"
    files = sorted(glob.glob(os.path.join(log_dir, "*.jsonl")))
    if not files:
        raise SystemExit(f"{log_dir} 下没有日志文件")

    need = set()
    parsed = []
    for path in files:
        entries = []
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            entries.append(e)
            for rec in records(e)[0]:
                if isinstance(rec, dict) and not (rec.get("release") or {}).get("confirmed"):
                    if rec.get("namespace"):
                        need.add(rec["namespace"])
        parsed.append((path, entries))

    print(f"日志文件 {len(files)} 个；待判定命名空间 {len(need)} 个")
    if not need:
        print("没有需要回填的记录")
        return 0

    nss = api(ns_path())
    if isinstance(nss, dict) and nss.get("__error__"):
        raise SystemExit(f"读取命名空间失败: {nss}")
    draft = {}
    for n in nss:
        v = [i["value"] for i in (n.get("items") or []) if i.get("key") == "content"]
        draft[n["namespaceName"]] = v[0] if v else None

    state = {}
    for ns in sorted(need):
        rel = api(ns_path(f"/{ns}/releases/latest"))
        if isinstance(rel, dict) and rel.get("__error__"):
            state[ns] = (None, "从未发布")
        elif draft.get(ns) is None:
            state[ns] = (rel.get("id"), "无 content 键")
        elif draft.get(ns) == (rel.get("configurations") or {}).get("content"):
            state[ns] = (rel.get("id"), "已发布(草稿=线上)")
        else:
            state[ns] = (rel.get("id"), "待发布(草稿!=线上)")

    live = {ns for ns, (_, st) in state.items() if st.startswith("已发布")}
    today = datetime.date.today().isoformat()
    changed_records = 0
    changed_files = 0
    pending = {}

    for path, entries in parsed:
        out = []
        touched = False
        for e in entries:
            recs, shape = records(e)
            for rec in recs:
                if not isinstance(rec, dict):
                    continue
                rel = rec.get("release") or {}
                if rel.get("confirmed"):
                    continue
                ns = rec.get("namespace")
                if ns in live:
                    rel["confirmed"] = True
                    rel["confirmedAt"] = rel.get("confirmedAt") or today
                    if state[ns][0] is not None:
                        rel["releaseId"] = state[ns][0]
                    rel["evidence"] = "auto: openapi releases/latest, draft == released"
                    rec["release"] = rel
                    touched = True
                    changed_records += 1
                elif ns:
                    pending.setdefault(ns, []).append(e.get("logId"))
            if shape == "dict":
                e["apollo"] = recs[0]
            out.append(json.dumps(e, ensure_ascii=False))
        if touched:
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(out) + "\n")
            changed_files += 1

    print(f"判定为已发布 {len(live)} 个命名空间；回填 {changed_records} 条记录，涉及 {changed_files} 个文件"
          + ("（dry-run 未写入）" if dry else ""))
    for ns, ids in sorted(pending.items()):
        print(f"  仍待发布: {ns} <- {', '.join(ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
