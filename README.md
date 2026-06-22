# Pre-tool-use Hook — Block Destructive Bash Commands

**Bounty: $100** — Claude Code hook that intercepts dangerous commands.

## Installation

```bash
mkdir -p ~/.claude/hooks
cp pre-tool-use.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/pre-tool-use.py
```

Then add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/pre-tool-use.py"
      }
    ]
  }
}
```

## Blocked Patterns
- `rm -rf /` or `rm -rf ~` or `rm -rf *`
- `DROP TABLE`, `TRUNCATE TABLE`
- `DELETE FROM` without WHERE
- `git push --force` / `git push -f`
- `sudo rm`
- Fork bombs
- Direct device writes

## Logs
Blocked attempts are logged to `~/.claude/hooks/blocked.log` in JSON format.
