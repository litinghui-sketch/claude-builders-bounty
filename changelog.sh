#!/bin/bash
# generate-changelog — structured CHANGELOG from git history
# Usage: bash changelog.sh [--since <tag>]

set -euo pipefail

SINCE_TAG="${2:-$(git describe --tags --abbrev=0 2>/dev/null || echo '')}"
OUTPUT="CHANGELOG.md"

if [ -z "$SINCE_TAG" ]; then
  echo "No git tags found. Using first commit."
  SINCE_TAG=$(git rev-list --max-parents=0 HEAD)
fi

echo "# Changelog" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "## $(date +%Y-%m-%d)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Fetch commits
COMMITS=$(git log "${SINCE_TAG}..HEAD" --pretty=format:"%s" 2>/dev/null || git log --pretty=format:"%s")

declare -a ADDED=()
declare -a FIXED=()
declare -a CHANGED=()
declare -a REMOVED=()

while IFS= read -r msg; do
  [[ -z "$msg" ]] && continue
  lower=$(echo "$msg" | tr '[:upper:]' '[:lower:]')
  if echo "$lower" | grep -qE '^(add|feat|new|introduce)'; then
    ADDED+=("- $msg")
  elif echo "$lower" | grep -qE '^(fix|bug|patch|resolve|close)'; then
    FIXED+=("- $msg")
  elif echo "$lower" | grep -qE '^(remove|drop|delete|deprecat)'; then
    REMOVED+=("- $msg")
  else
    CHANGED+=("- $msg")
  fi
done <<< "$COMMITS"

write_section() {
  local title="$1"
  shift
  local items=("$@")
  if [ ${#items[@]} -gt 0 ]; then
    echo "### $title" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    for item in "${items[@]}"; do
      echo "$item" >> "$OUTPUT"
    done
    echo "" >> "$OUTPUT"
  fi
}

write_section "Added" "${ADDED[@]}"
write_section "Fixed" "${FIXED[@]}"
write_section "Changed" "${CHANGED[@]}"
write_section "Removed" "${REMOVED[@]}"

echo "✅ CHANGELOG.md generated ($(wc -l < "$OUTPUT") lines)"
