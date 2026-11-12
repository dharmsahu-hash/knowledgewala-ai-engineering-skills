#!/usr/bin/env sh
# Local quality gate (Linux/macOS). Run before every commit: sh scripts/check.sh
set -e
cd "$(dirname "$0")/.."
PY=python3; [ -x .venv/bin/python ] && PY=.venv/bin/python
export PYTHONPATH=tooling
$PY -m pytest -q -p no:cacheprovider
$PY -m kw_skills validate
$PY -m kw_skills compatibility
$PY -m kw_skills docs --check
echo "ALL CHECKS PASSED"
