"""Pre-generate OFFLINE remediation briefs for the static Vercel web demo.

Runs the real pipeline with offline=True and use_market=False (no API keys,
no network), and writes web/briefs/<fixture>.json + web/fixtures.json.
Usage: PYTHONPATH=src python scripts/build_web_demo.py
"""
from __future__ import annotations

import json
import os
from pathlib import Path

for k in ("NEBIUS_API_KEY", "TAVILY_API_KEY", "OPENAI_API_KEY"):
    os.environ.pop(k, None)

from meshcfo_control_tower.catalog import list_fixtures  # noqa: E402
from meshcfo_control_tower.pipeline import run_brief  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "web"
(OUT / "briefs").mkdir(parents=True, exist_ok=True)
fixtures = list_fixtures()
(OUT / "fixtures.json").write_text(json.dumps(fixtures, indent=2))
for f in fixtures:
    for locked in (False, True):
        b = run_brief(f["fixture_id"], offline=True, use_market=False,
                      lock_validator="demo-validator" if locked else None)
        assert b.model.mode == "offline"
        name = f["fixture_id"] + ("-locked" if locked else "")
        (OUT / "briefs" / f"{name}.json").write_text(b.model_dump_json(indent=2))
        print("wrote", name, b.lock_state, b.chp.provenance_score)
