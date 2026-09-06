#!/usr/bin/env bash
# Print a DEMO JSON brief without secrets. Usage: scripts/demo.sh [northstar|lumenbridge|cedarline]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FIXTURE="${1:-northstar}"
export MESHCFO_LEDGER_PATH="${MESHCFO_LEDGER_PATH:-$ROOT/.meshcfo/audit.jsonl}"
exec python3 -m meshcfo_control_tower --fixture "$FIXTURE" --offline --no-market
