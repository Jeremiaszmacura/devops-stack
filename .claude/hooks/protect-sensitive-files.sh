#!/usr/bin/env bash
set -euo pipefail
file=$(jq -r '.tool_input.file_path // ""')

deny_globs=(".env*" "package-lock.json" ".git/*")

for g in "${deny_globs[@]}"; do
  if printf '%s\n' "$file" | grep -Eiq "^${g//\*/.*}$"; then
    echo "Edits to '$file' are blocked." 1>&2
    exit 2
  fi
done

exit 0