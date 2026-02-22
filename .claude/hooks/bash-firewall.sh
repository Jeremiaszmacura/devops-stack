#!/usr/bin/env bash
set -euo pipefail

cmd=$(jq -r '.tool_input.command // ""')

deny_patterns=(
  'rm\s+-rf\s+/'
  'git\s+reset\s+--hard'
  'git\s+push\s+--force'
  'DROP\s+TABLE'
  'DELETE\s+FROM'
)

for pat in "${deny_patterns[@]}"; do
  if echo "$cmd" | grep -Eiq "$pat"; then
    echo "Blocked: matches denied pattern '$pat'." 1>&2
    exit 2
  fi
done

exit 0