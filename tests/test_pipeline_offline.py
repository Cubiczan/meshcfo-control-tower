from pathlib import Path

from meshcfo_control_tower.cli import main
from meshcfo_control_tower.pipeline import run_brief
from meshcfo_control_tower.schemas import RemediationBrief

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_northstar_offline_brief():
    brief = run_brief("northstar", offline=True, use_market=False)
    assert brief.demo is True
    assert brief.brand == "Cubiczan"
    assert brief.company.ticker == "NSMT-DEMO"
    assert "(DEMO)" in brief.company.display_name
    assert brief.model.mode == "offline"
    assert brief.why_now.urgency == "immediate"
    assert any("revenue" in gap.process.lower() for gap in brief.icfr_gaps)
    seats = {s.seat: s.raci for s in brief.buyer_seats}
    assert seats["CFO"] == "A"
    assert "Controller" in seats
    assert brief.next_actions
    assert all(c.grounding_source_ids for c in brief.claims)
    assert brief.lock_state in {"PROVISIONAL_LOCK", "LOCKED"}
    assert brief.chp.r0_passed is True


def test_lumenbridge_itgc_ownership():
    brief = run_brief("lumenbridge", offline=True, use_market=False)
    assert brief.company.ticker == "LMPC-DEMO"
    assert any("ITGC" in gap.process for gap in brief.icfr_gaps)
    assert any(s.seat == "CIO/CISO" and s.raci == "R" for s in brief.buyer_seats)


def test_cedarline_restatement():
    brief = run_brief("cedarline", offline=True, use_market=False)
    assert brief.signal.signal_kind == "both"
    assert any("inventory" in gap.process.lower() for gap in brief.icfr_gaps)


def test_validator_locks(monkeypatch, tmp_path):
    monkeypatch.setenv("MESHCFO_LEDGER_PATH", str(tmp_path / "audit.jsonl"))
    from meshcfo_control_tower.config import Settings

    brief = run_brief(
        "northstar",
        offline=True,
        use_market=False,
        settings=Settings(),
        lock_validator="demo_operator",
    )
    assert brief.lock_state == "LOCKED"


def test_committed_example_brief_validates():
    payload = (REPO_ROOT / "examples" / "northstar-brief.offline.json").read_text(encoding="utf-8")
    brief = RemediationBrief.model_validate_json(payload)
    assert brief.brand == "Cubiczan"
    assert brief.demo is True
    assert brief.company.ticker == "NSMT-DEMO"
    assert brief.lock_state == "PROVISIONAL_LOCK"
    assert brief.chp.r0_passed is True


def test_cli_prints_json(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("MESHCFO_LEDGER_PATH", str(tmp_path / "audit.jsonl"))
    code = main(["--fixture", "northstar", "--offline", "--no-market"])
    assert code == 0
    out = capsys.readouterr().out
    assert '"brand": "Cubiczan"' in out
    assert "NSMT-DEMO" in out
    assert "PROVISIONAL_LOCK" in out or "LOCKED" in out
