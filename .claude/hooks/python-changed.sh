#!/usr/bin/env bash
set -euo pipefail

file=$(jq -r '.tool_input.file_path // ""')

[[ "$file" == *.py ]] || exit 0
case "$file" in
    */.venv/*|*/venv/*|*/.git/*) exit 0 ;;
esac

mkdir -p .claude/.cache
touch .claude/.cache/python-changed
