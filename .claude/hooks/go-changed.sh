#!/usr/bin/env bash
set -euo pipefail

file=$(jq -r '.tool_input.file_path // ""')

[[ "$file" == *.go ]] || exit 0
case "$file" in
    */vendor/*|*/.git/*) exit 0 ;;
esac

mkdir -p .claude/.cache
touch .claude/.cache/go-changed
