#!/usr/bin/env python3
"""Reset the Merge Queue Café repo for a fresh demo.

This script will:
1. Close all open PRs
2. Delete all non-main branches
3. Force-reset main to the initial commit
4. Re-run create_prs.py to recreate all 18 PRs

Usage:
    python3 scripts/reset_demo.py
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
REPO = os.environ["REPO"]


def run(cmd, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  STDERR: {result.stderr.strip()}")
        if check:
            sys.exit(1)
    return result.stdout.strip()


def main():
    print("🔄 Resetting Merge Queue Café demo...\n")

    # 1. Close all open PRs
    print("[1/5] Closing all open PRs...")
    prs = run(f"gh pr list --repo {REPO} --state open --json number --jq '.[].number'")
    if prs:
        for pr_num in prs.strip().split("\n"):
            run(f"gh pr close {pr_num} --repo {REPO} --delete-branch", check=False)
            print(f"       Closed PR #{pr_num}")
    else:
        print("       No open PRs found.")

    # 2. Checkout main locally
    print("\n[2/5] Checking out main...")
    run("git checkout main")
    run("git fetch origin")

    # 3. Force-reset main to the tagged base commit
    print("\n[3/5] Resetting main to demo-base tag...")
    run("git reset --hard demo-base")
    run("git push origin main --force")
    print("       Reset to demo-base")

    # 4. Delete remaining remote branches
    print("\n[4/5] Cleaning up remote branches...")
    remote_branches = run("git branch -r --list 'origin/*' --no-color")
    for line in remote_branches.strip().split("\n"):
        branch = line.strip().replace("origin/", "")
        if branch and branch not in ("main", "HEAD -> origin/main"):
            run(f"git push origin --delete {branch}", check=False)
            print(f"       Deleted origin/{branch}")

    # Clean local branches too
    local_branches = run("git branch --no-color")
    for line in local_branches.strip().split("\n"):
        branch = line.strip().lstrip("* ")
        if branch and branch != "main":
            run(f"git branch -D {branch}", check=False)

    # 5. Recreate all PRs
    print("\n[5/5] Recreating all 18 PRs...")
    repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    scripts_dir = os.path.join(repo_root, "scripts")
    result = subprocess.run(
        [sys.executable, os.path.join(scripts_dir, "create_prs.py")],
        cwd=repo_root,
    )
    if result.returncode != 0:
        print("  ❌ Failed to create PRs. Check create_prs.py output above.")
        sys.exit(1)

    print(f"\n✅ Demo reset complete! Visit https://github.com/{REPO}/pulls")


if __name__ == "__main__":
    main()
