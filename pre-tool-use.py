#!/usr/bin/env python3
"""Claude Code pre-tool-use hook — blocks destructive bash commands."""

import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path.home() / ".claude" / "hooks" / "blocked.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

DANGEROUS_PATTERNS = [
    (r"rm\s+-rf\s+[/~]", "rm -rf on root/home — too dangerous"),
    (r"rm\s+-rf\s+\*", "rm -rf * — destructive wildcard"),
    (r"DROP\s+TABLE", "DROP TABLE — irreversible schema change"),
    (r"TRUNCATE\s+TABLE", "TRUNCATE TABLE — data loss"),
    (r"DELETE\s+FROM\s+\w+\s*;?\s*$", "DELETE FROM without WHERE clause"),
    (r"git\s+push\s+--force", "git push --force — overwrites remote history"),
    (r"git\s+push\s+-f", "git push -f — overwrites remote history"),
    (r"sudo\s+rm", "sudo rm — elevated destructive command"),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "fork bomb detected"),
    (r">\s*/dev/sda", "direct device write — hardware damage"),
]

def log_blocked(command, project_path):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "project": project_path,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    input_data = json.loads(sys.stdin.read())
    
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    project_path = input_data.get("cwd", "")
    
    if tool_name != "Bash":
        print(json.dumps({"continue": True}))
        return
    
    command = tool_input.get("command", "")
    
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            log_blocked(command, project_path)
            print(json.dumps({
                "continue": False,
                "reason": f"BLOCKED: {reason}\n\nCommand: {command}\n\nTo override, manually run this command in your terminal."
            }))
            return
    
    print(json.dumps({"continue": True}))

if __name__ == "__main__":
    main()
