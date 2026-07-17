#!/usr/bin/env bash
set -euo pipefail

marker=.claude/.cache/python-changed
[[ -f "$marker" ]] || exit 0
rm -f "$marker"

make test-unit-python
