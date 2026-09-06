"""Cubiczan MeshCFO Control Tower — Streamlit demo for hackathon judges."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st

from meshcfo_control_tower.catalog import list_fixtures, load_fixture
from meshcfo_control_tower.config import get_settings
from meshcfo_control_tower.pipeline import run_brief
from meshcfo_control_tower.schemas import RemediationBrief

st.set_page_config(
    page_title="MeshCFO Control Tower — Cubiczan",
    page_icon="▣",
    layout="wide",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: "IBM Plex Sans", sans-serif; }
.stApp { background: radial-gradient(1200px 600px at 10% -10%, #16324a 0%, #0b1220 45%, #070b14 100%); color: #e8eef6; }
.block-container { padding-top: 1.2rem; }
.hero { border: 1px solid #2a3f55; background: linear-gradient(180deg, rgba(20,38,56,.92), rgba(10,16,26,.92)); border-radius: 16px; padding: 1.1rem 1.3rem 1rem; margin-bottom: 1rem; }
.hero h1 { margin: 0; font-size: 1.7rem; letter-spacing: .02em; color: #f4f7fb; }
.hero .sub { color: #9fb3c8; margin-top: .35rem; }
.badge-row { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .75rem; }
.badge { font-family: "IBM Plex Mono", monospace; font-size: .72rem; padding: .22rem .5rem; border-radius: 999px; border: 1px solid #3d6d7a; background: #12303a; color: #9ee7d4; }
.badge.warn { border-color: #8a6b2a; background: #2a210f; color: #f0d089; }
.badge.mute { border-color: #334155; background: #111827; color: #94a3b8; }
.card { border: 1px solid #243447; background: rgba(12,18,28,.82); border-radius: 12px; padding: .9rem 1rem; margin-bottom: .75rem; }
.card h3 { margin: 0 0 .45rem; font-size: .95rem; color: #d5e4f3; }
.seat { display: flex; justify-content: space-between; gap: 1rem; border-bottom: 1px solid #1c2a3a; padding: .4rem 0; font-size: .9rem; }
.seat:last-child { border-bottom: 0; }
.raci { font-family: "IBM Plex Mono", monospace; color: #7dd3c7; }
.small { color: #93a4b8; font-size: .82rem; }
.excerpt { font-family: "IBM Plex Mono", monospace; font-size: .78rem; color: #c9d6e5; background: #0a1220; border-left: 3px solid #2dd4bf; padding: .6rem .7rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

settings = get_settings()
fixtures = list_fixtures()
live = settings.live_llm_ready

st.markdown(
    f"""
<div class="hero">
  <div class="small">CUBICZAN · OFFICE OF THE CFO</div>
  <h1>MeshCFO Control Tower</h1>
  <div class="sub">Governed remediation briefs from SEC EDGAR material-weakness and restatement signals — ownership and provenance, not free-form advice.</div>
  <div class="badge-row">
    <span class="badge">NVIDIA Nemotron 3 Nano · {settings.nebius_model}</span>
    <span class="badge">Nebius Token Factory</span>
    <span class="badge warn">DEMO fixtures — not real registrants</span>
    <span class="badge mute">{"LIVE LLM ready" if live else "OFFLINE playbooks (set NEBIUS_API_KEY)"}</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Signal intake")
    labels = {f"{row['company']} · {row['signal_kind']}": row["fixture_id"] for row in fixtures}
    choice = st.selectbox("DEMO issuer", list(labels.keys()))
    fixture_id = labels[choice]
    fixture = load_fixture(fixture_id)
    st.caption(fixture.demo_disclaimer)
    offline = st.toggle("Offline playbooks only", value=not live)
    use_market = st.toggle("Attach Tavily market context (optional)", value=bool(settings.tavily_api_key))
    validator = st.text_input("Third-party validator (optional lock)", value="")
    run = st.button("Generate remediation brief", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("**How to judge this**")
    st.markdown(
        "1. Pick a DEMO fixture  \n"
        "2. Generate the brief  \n"
        "3. Open *Per-claim provenance*  \n"
        "4. Confirm CHP lock ≠ free-form chat"
    )
    st.caption("MIT · Cubiczan · Not legal, audit, or investment advice.")

if "brief" not in st.session_state:
    with st.spinner("Loading DEMO brief…"):
        st.session_state.brief = run_brief(
            fixture_id,
            offline=offline,
            use_market=False,
        )

if run:
    with st.spinner("Running MeshCFO agent mesh…"):
        st.session_state.brief = run_brief(
            fixture_id,
            offline=offline,
            use_market=use_market,
            lock_validator=validator.strip() or None,
        )

brief: RemediationBrief | None = st.session_state.brief

left, right = st.columns([1.15, 0.85])
with left:
    st.markdown("#### Filing excerpts (DEMO)")
    for excerpt in fixture.excerpts:
        st.markdown(
            f"<div class='card'><div class='small'>{excerpt.locator} · {excerpt.form} · {excerpt.filed_on}</div>"
            f"<div class='excerpt'>{excerpt.excerpt}</div></div>",
            unsafe_allow_html=True,
        )

with right:
    st.markdown("#### Structured facts")
    st.json(
        {
            "ticker": fixture.company.ticker,
            "cik": fixture.company.cik,
            "forms": fixture.forms,
            "signal": fixture.signal_kind,
            **fixture.structured_facts,
        }
    )

if brief is None:
    st.info("Select a DEMO fixture and generate a brief. Live mode uses NVIDIA Nemotron on Nebius Token Factory.")
    st.stop()

if brief.signal.fixture_id != fixture_id:
    st.warning(
        f"Showing the brief for `{brief.signal.fixture_id}`. "
        "Click Generate to refresh for the DEMO issuer selected in the sidebar."
    )

def _chip(label: str, value: str) -> str:
    return (
        f"<div class='card' style='margin-bottom:0.6rem'><div class='small'>{label}</div>"
        f"<div style='font-size:1.15rem;font-weight:600;letter-spacing:.02em'>{value}</div></div>"
    )


c_lock, c_r0, c_gaps, c_model = st.columns(4)
c_lock.markdown(_chip("Lock state", brief.lock_state), unsafe_allow_html=True)
c_r0.markdown(_chip("R0 provenance", f"{brief.chp.provenance_score:.0%}"), unsafe_allow_html=True)
c_gaps.markdown(_chip("ICFR gaps", str(len(brief.icfr_gaps))), unsafe_allow_html=True)
c_model.markdown(_chip("Model mode", brief.model.mode.upper()), unsafe_allow_html=True)

st.markdown(f"**{brief.signal.headline}**")
st.caption(
    f"{brief.brand} {brief.product} · {brief.model.provider} · {brief.model.model} · brief {brief.brief_id}"
)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='card'><h3>Why now</h3>", unsafe_allow_html=True)
    st.markdown(f"**Urgency:** {brief.why_now.urgency.replace('_', ' ')}")
    st.markdown(brief.why_now.regulatory_clock)
    for trigger in brief.why_now.triggers:
        st.markdown(f"- {trigger.text}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>ICFR gaps</h3>", unsafe_allow_html=True)
    for gap in brief.icfr_gaps:
        st.markdown(
            f"**{gap.process}** · {gap.severity.replace('_', ' ')} · {gap.coso_component}"
        )
        st.markdown(gap.claim.text)
        if gap.compensating_controls:
            st.caption("Compensating: " + "; ".join(gap.compensating_controls))
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'><h3>Buyer seats (MeshCFO ownership)</h3>", unsafe_allow_html=True)
    for seat in brief.buyer_seats:
        st.markdown(
            f"<div class='seat'><div><strong>{seat.seat}</strong> · {seat.named_role}<br>"
            f"<span class='small'>{seat.accountable_for}</span></div>"
            f"<div class='raci'>{seat.raci}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>Next actions</h3>", unsafe_allow_html=True)
    for action in brief.next_actions:
        st.markdown(f"**{action.owner_seat}** · due {action.due}")
        st.markdown(action.action)
        st.caption(f"Evidence: {action.evidence_required}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("#### Consensus Hardening Protocol")
chp1, chp2 = st.columns(2)
with chp1:
    st.markdown("**Foundation (what we actually have)**")
    for fact in brief.chp.foundation:
        st.markdown(f"- {fact}")
with chp2:
    st.markdown("**Adversarial attacks**")
    for attack in brief.chp.attacks:
        st.markdown(f"- {attack}")
st.caption(brief.chp.lock_rationale)
if brief.market_context_note:
    st.warning(brief.market_context_note)

with st.expander("Per-claim provenance", expanded=True):
    rows = []
    registry = brief.provenance_index()
    for claim in brief.claims:
        locators = "; ".join(
            registry[sid].locator for sid in claim.grounding_source_ids if sid in registry
        )
        rows.append(
            {
                "claim": claim.text,
                "agent": claim.agent,
                "step": claim.expansion_step,
                "epistemic": claim.epistemic,
                "sources": locators,
                "chp": claim.chp_finding or "",
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)

with st.expander("Agent pipeline"):
    st.dataframe(
        [{"ts": e.ts, "agent": e.agent, "phase": e.phase, "summary": e.summary} for e in brief.pipeline],
        use_container_width=True,
        hide_index=True,
    )

with st.expander("JSON brief (CLI-equivalent)"):
    st.code(brief.model_dump_json(indent=2), language="json")

st.markdown(
    "<div class='small' style='margin-top:1.2rem'>Cubiczan MeshCFO Control Tower · MIT · "
    "NVIDIA Nemotron on Nebius Token Factory · DEMO fixtures are not real SEC registrants · "
    "Per-claim provenance is not a legal, audit, or investment opinion.</div>",
    unsafe_allow_html=True,
)
