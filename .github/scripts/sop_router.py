#!/usr/bin/env python3
"""
SOP Router - reads sop.yaml, detects changed files, calls the right webhook.
通用版：trigger 匹配、added_only、commit_message_guard 全部从 sop.yaml 读取。
"""
import os, sys, json, subprocess, yaml


def decode_git_path(path: str) -> str:
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
        import re
        def replace_octal(m):
            return bytes([int(m.group(0)[1:], 8)]).decode('latin-1')
        path = re.sub(r'\\[0-7]{3}', replace_octal, path)
    return path


def _run_git_diff(diff_filter, before_sha, after_sha):
    git_env = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1'}
    cmd = ["git", "-c", "core.quotepath=false", "diff", "--name-only", f"--diff-filter={diff_filter}"]
    for ref_range in [f"{before_sha}..{after_sha}", "HEAD~1..HEAD"]:
        try:
            r = subprocess.run(cmd + [ref_range], capture_output=True, text=True, check=True, env=git_env)
            return [decode_git_path(f) for f in r.stdout.strip().split("\n") if f.strip()]
        except subprocess.CalledProcessError:
            continue
    return []


def get_changed_files(before, after): return _run_git_diff("AM", before, after)
def get_added_files(before, after):   return _run_git_diff("A",  before, after)


def matches_pattern(filepath, pattern):
    import fnmatch
    return fnmatch.fnmatch(filepath, pattern)


def matches_any(files, pattern):
    return any(matches_pattern(f, pattern) for f in files)


def call_webhook(route, payload, base_url, secret):
    url = f"{base_url}/{route}"
    result = subprocess.run([
        "curl", "-sS", "-X", "POST", url,
        "-H", "Content-Type: application/json",
        "-H", f"X-Gitlab-Token: {secret}",
        "-H", f"X-Request-ID: {payload.get('run_id','unknown')}",
        "-H", "User-Agent: curl/7.81.0",
        "-d", json.dumps(payload),
        "-w", "\nHTTP_STATUS:%{http_code}",
        "--max-time", "30",
    ], capture_output=True, text=True)

    print(f"[sop_router] POST {url}\n{result.stdout[-300:]}")
    if result.returncode != 0:
        print(f"[sop_router] curl error: {result.stderr}")
        return False
    for line in result.stdout.split("\n"):
        if line.startswith("HTTP_STATUS:"):
            return 200 <= int(line.split(":")[1]) < 300
    return False


def main():
    base_urls = [u.strip() for u in os.environ.get(
        "HERMES_WEBHOOK_BASE", "https://hermes-webhooks.vyibc.com/webhooks"
    ).split(",") if u.strip()]
    secret     = os.environ.get("HERMES_SOP_SECRET", "")
    before_sha = os.environ.get("BEFORE_SHA", "")
    after_sha  = os.environ.get("AFTER_SHA", "HEAD")
    run_id     = os.environ.get("RUN_ID", "unknown")
    repo       = os.environ.get("REPO", "")

    with open("sop.yaml") as f:
        sop = yaml.safe_load(f)

    changed    = get_changed_files(before_sha, after_sha)
    added_only = get_added_files(before_sha, after_sha)
    print(f"[sop_router] Changed files (AM): {changed}")
    print(f"[sop_router] Added-only files (A): {added_only}")

    if not changed:
        print("[sop_router] No changed files, stopping.")
        return

    # 只有 terminal_paths 变化时停止
    terminal_paths = sop.get("terminal_paths", [])
    non_terminal = [f for f in changed if not any(matches_pattern(f, p) for p in terminal_paths)]
    if not non_terminal:
        print(f"[sop_router] Only terminal paths changed, stopping pipeline.")
        return

    # 匹配 stage
    matched_stage = None
    for stage in sop.get("pipeline", []):
        trigger    = stage.get("trigger", "")
        added_only_flag = stage.get("added_only", False)
        files_to_check = added_only if added_only_flag else changed
        if matches_any(files_to_check, trigger):
            matched_stage = stage
            break

    if not matched_stage:
        print(f"[sop_router] No stage matched for changed files: {changed}")
        return

    stage_name = matched_stage["stage"]

    # commit_message_guard：从 sop.yaml 的 stage 定义读取，不再硬编码
    guard = matched_stage.get("commit_message_guard", "")
    if guard:
        commit_msg = subprocess.run(
            ["git", "log", "-1", "--format=%s", after_sha],
            capture_output=True, text=True
        ).stdout.strip()
        if guard.lower() not in commit_msg.lower():
            print(f"[sop_router] Guard '{guard}' not in commit '{commit_msg}', skipping.")
            return
        print(f"[sop_router] Guard passed: '{guard}' in '{commit_msg}'")

    webhook_route = matched_stage["webhook_route"]
    stage_params  = matched_stage.get("params", {})
    notify        = sop.get("notify", {}).get("telegram", {})
    notebooklm_p  = stage_params.get("notebooklm", {})

    payload = {
        "stage":           stage_name,
        "wiki_local_path": sop.get("wiki_local_path", ""),
        "repo":            repo or sop.get("repo", ""),
        "repo_url":        f"https://github.com/{repo or sop.get('repo','')}",
        "sha":             after_sha,
        "before":          before_sha,
        "run_id":          run_id,
        "tg_token_env":    notify.get("token_env", "YOUTUBE_WIKI_TG_TOKEN"),
        "tg_chat_id":      notify.get("chat_id", ""),
        # NotebookLM params（youtube-wiki 专用，其他 wiki 忽略）
        "notebooklm_outputs":        notebooklm_p.get("outputs", []),
        "notebooklm_language":       notebooklm_p.get("language", "zh_Hans"),
        "notebooklm_notebook_title": notebooklm_p.get("notebook_title", ""),
        "notebooklm_report_prompt":  notebooklm_p.get("report_prompt", ""),
        "notebooklm_mindmap_prompt": notebooklm_p.get("mindmap_prompt", ""),
        # 通用 params
        "build_mode":      stage_params.get("build_mode", "incremental"),
        "params":          stage_params,
    }

    print(f"[sop_router] Matched stage: {stage_name} → route: {webhook_route}")

    results = [(u, call_webhook(webhook_route, payload, u, secret)) for u in base_urls]
    succeeded = [u for u, ok in results if ok]
    failed    = [u for u, ok in results if not ok]

    if failed:    print(f"[sop_router] Failed endpoints: {failed}")
    if not succeeded:
        print(f"[sop_router] All webhook calls failed for stage {stage_name}")
        sys.exit(1)

    print(f"[sop_router] Successfully triggered stage: {stage_name} → {len(succeeded)}/{len(results)} endpoints")


if __name__ == "__main__":
    main()
