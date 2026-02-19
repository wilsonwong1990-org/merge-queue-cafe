#!/usr/bin/env python3
"""Create the 'Merge Queue' branch ruleset for the Merge Queue Café demo.

This is useful after forking the repo, since rulesets are not copied to forks.

Usage:
    python3 scripts/create_ruleset.py

Requires: gh CLI authenticated with admin access to the repo.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
REPO = os.environ["REPO"]

RULESET = {
    "name": "Merge Queue",
    "target": "branch",
    "enforcement": "active",
    "bypass_actors": [
        {
            "actor_id": 5,
            "actor_type": "RepositoryRole",
            "bypass_mode": "always",
        }
    ],
    "conditions": {
        "ref_name": {
            "include": ["refs/heads/main"],
            "exclude": [],
        }
    },
    "rules": [
        {
            "type": "merge_queue",
            "parameters": {
                "check_response_timeout_minutes": 60,
                "grouping_strategy": "ALLGREEN",
                "max_entries_to_build": 5,
                "max_entries_to_merge": 0,
                "merge_method": "MERGE",
                "min_entries_to_merge": 1,
                "min_entries_to_merge_wait_minutes": 5,
            },
        },
        {
            "type": "required_status_checks",
            "parameters": {
                "strict_required_status_checks_policy": False,
                "required_status_checks": [
                    {
                        "context": "test",
                    }
                ],
            },
        },
    ],
}


def main():
    print("📋 Creating 'Merge Queue' ruleset...\n")

    payload = json.dumps(RULESET)
    cmd = [
        "gh", "api",
        f"repos/{REPO}/rulesets",
        "-X", "POST",
        "-H", "Accept: application/vnd.github+json",
        "--input", "-",
    ]

    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, input=payload, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  Failed to create ruleset: {result.stderr.strip()}")
        sys.exit(1)

    print("\n✅ Ruleset created!\n")
    print(f"View it at: https://github.com/{REPO}/settings/rules")


if __name__ == "__main__":
    main()
