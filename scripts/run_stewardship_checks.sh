#!/usr/bin/env bash
# Run all stewardship doc gates locally (same set as CI).
# docs CI config pins after #83
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/check_badge_standard.py
python3 scripts/check_wiki_outline.py
python3 scripts/check_stewardship_schema.py
python3 scripts/check_relative_links.py
