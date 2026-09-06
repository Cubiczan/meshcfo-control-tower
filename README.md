# MeshCFO Control Tower

> **Cubiczan** · Nebius x NVIDIA Global AI Hackathon · **Best Apps and Agents**

**The office-of-the-CFO control tower.** Turn SEC EDGAR material-weakness and restatement signals into a governed remediation brief — why now, who owns it, which ICFR gaps, what evidence closes them — with per-claim provenance.

This is MeshCFO-style **ownership**, not a chat window that invents advice.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Nebius Token Factory](https://img.shields.io/badge/Inference-Nebius%20Token%20Factory-0A84FF)](https://docs.tokenfactory.nebius.com/)
[![NVIDIA Nemotron](https://img.shields.io/badge/Model-NVIDIA%20Nemotron%203%20Nano-76B900)](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b)

---

## Demo video

≤ 3 minute walkthrough for Devpost judges (Nebius Token Factory + NVIDIA Nemotron on camera).

- **Release:** [v0.1.0-demo](https://github.com/Cubiczan/meshcfo-control-tower/releases/tag/v0.1.0-demo)
- **Asset:** [`meshcfo-control-tower-demo.mp4`](https://github.com/Cubiczan/meshcfo-control-tower/releases/download/v0.1.0-demo/meshcfo-control-tower-demo.mp4)

If the MP4 is not attached yet, the release tag is the placeholder — another agent is cutting and pushing the file. Shot list and voiceover: [`DEMO.md`](DEMO.md).

---

## Why this exists

An 8-K Item 4.02 or a 10-K Item 9A is not a blog post. It is a **clock**: non-reliance, restatement measurement, 302/404 certifications, Audit Committee narrative, and a material weakness that will still be there next year if nobody owns the evidence.

Generic copilots produce paragraphs. MeshCFO Control Tower produces a **brief a Controller can run**:

| Brief section | What judges should see |
|---|---|
| **Why now** | Regulatory clock from the filing item, not vibes |
| **Buyer seats** | RACI on CFO / Controller / IA / SOX PMO / process owner / AC / CIO |
| **ICFR gaps** | COSO component + process + design vs operating |
| **Next actions** | Owner seat + due + **evidence required** |
| **Provenance** | Every claim → agent, expansion step, epistemic tag, excerpt locator |
| **CHP** | Foundation disclosure → adversarial attack → R0 gate → lock |

Lock states follow Cubiczan MeshCFO / Consensus Hardening Protocol: `EXPLORING` → `PROVISIONAL_LOCK` → `LOCKED` (LOCKED only after a named validator).

---

## NVIDIA Nemotron on Nebius Token Factory

**This is the required inference path.** The app talks to the OpenAI-compatible Token Factory API.

| | |
|---|---|
| Base URL | `https://api.tokenfactory.nebius.com/v1/` |
| Env | `NEBIUS_API_KEY` (never committed) |
| Primary model | **`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`** |
| Fallback | `nvidia/Nemotron-3_5-Lightning` |

Token Factory is what makes the agent mesh shippable: one key, OpenAI SDK, NVIDIA open weights, no model hosting. Nemotron Nano is the fast specialist for intake synthesis and CHP attacks; the playbooks stay deterministic so a missing key never silently fabricates a company.

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ["NEBIUS_API_KEY"],
)
client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
    messages=[{"role": "user", "content": "Return JSON only."}],
)
```

`--offline` runs the same ownership mesh without calling Token Factory (CI / airplane mode). Live mode **refines** why-now language and the adversary pass with Nemotron, then R0 still drops anything that is not grounded in a DEMO excerpt.

---

## Quick start

```bash
git clone https://github.com/Cubiczan/meshcfo-control-tower.git
cd meshcfo-control-tower
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # put NEBIUS_API_KEY here
```

### CLI — prints a JSON brief

```bash
# Live (Nemotron on Token Factory)
meshcfo-brief --fixture northstar

# Deterministic playbooks (no API key)
meshcfo-brief --fixture lumenbridge --offline --no-market

# List DEMO issuers
meshcfo-brief --list
```

### Streamlit control tower

```bash
streamlit run app/streamlit_app.py
```

### FastAPI

```bash
uvicorn meshcfo_control_tower.api:app --reload --port 8000
# GET  /health
# GET  /fixtures
# POST /brief   {"fixture_id":"northstar","offline":false}
```

---

## DEMO fixtures (not real companies)

These are **labeled DEMO issuers**. They are not SEC registrants. They are not stand-ins for any public company. Every excerpt starts with `DEMO FILING TEXT`.

| ID | Demo issuer | Signal | Why it is in the tape |
|---|---|---|---|
| `northstar` | Northstar Materials, Inc. (DEMO) `NSMT-DEMO` | 8-K 4.02 + MW | ASC 606 bill-and-hold / revenue cutoff restatement |
| `lumenbridge` | Lumenbridge Payments Corp. (DEMO) `LMPC-DEMO` | 10-K Item 9A MW | ITGC access + SOD + emergency change after ledger cutover |
| `cedarline` | Cedarline Health Partners (DEMO) `CDLH-DEMO` | 8-K 4.02 + MW | Inventory NRV / obsolescence estimate restatement |

---

## Agent mesh

```
DEMO fixture → source registry
   Intake        expand identity + Item 4.02 / Item 9A facts
   Why-Now       compress into a regulatory clock
   ICFR          map excerpts → COSO + process gaps
   Ownership     MeshCFO buyer seats (RACI) + evidence-backed actions
   Composer      NVIDIA Nemotron (Token Factory) synthesis
   Adversary     CHP assumption attacks
   R0 gate       drop ungrounded claims → PROVISIONAL_LOCK
   Ledger        HMAC-SHA256 chained JSONL (.meshcfo/audit.jsonl)
```

Optional **Tavily** search attaches thematic SOX/ICFR *market context*. It is labeled `market_context` and is **not** treated as evidence about the DEMO issuer.

---

## Architecture

```
src/meshcfo_control_tower/
  catalog.py        DEMO fixture loader (refuses demo=false)
  llm.py            Nebius Token Factory + Nemotron JSON client
  playbooks.py      Deterministic ownership / ICFR / why-now mesh
  pipeline.py       Orchestrator + CHP
  provenance.py     R0 gate
  ledger.py         Signed append-only audit trail
  cli.py            meshcfo-brief
  api.py            FastAPI
app/streamlit_app.py
fixtures live under src/meshcfo_control_tower/fixtures/
```

---

## Environment

See [`.env.example`](.env.example).

| Variable | Required | Purpose |
|---|---|---|
| `NEBIUS_API_KEY` | Live demo | Token Factory auth |
| `NEBIUS_BASE_URL` | No | Default `https://api.tokenfactory.nebius.com/v1/` |
| `NEBIUS_MODEL` | No | Default `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` |
| `NEBIUS_FALLBACK_MODEL` | No | `nvidia/Nemotron-3_5-Lightning` |
| `TAVILY_API_KEY` | No | Optional market-context enrichment |
| `AUDIT_LEDGER_KEY` | No | HMAC key (demo default if unset) |

---

## Tests

```bash
pytest
```

CI runs the offline path only. No secrets in the repo.

---

## Cubiczan stack

This control tower is a specialized MeshCFO surface. Pair with:

- [meshcfo](https://github.com/Cubiczan/meshcfo) — auditable multi-agent CFO
- [consensus-hardening-protocol](https://github.com/Cubiczan/consensus-hardening-protocol) — CHP
- [Strata](https://github.com/Cubiczan/Strata) — maturity roadmaps
- [Metabocommand](https://github.com/Cubiczan/Metabocommand) — operational approval queues

Video script: [`DEMO.md`](DEMO.md) (≤ 3 minutes).

## License

MIT. See [`LICENSE`](LICENSE). Copyright (c) 2026 Shyam Desigan / Cubiczan.
