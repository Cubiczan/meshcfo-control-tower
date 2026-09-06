# DEMO.md — ≤ 3 minute video script

**Track:** Nebius x NVIDIA Global AI Hackathon · Best Apps and Agents  
**Product:** Cubiczan MeshCFO Control Tower  
**Must say on camera:** NVIDIA Nemotron + Nebius Token Factory

**Published video (Release v0.1.0-demo):**
[`meshcfo-control-tower-demo.mp4`](https://github.com/Cubiczan/meshcfo-control-tower/releases/download/v0.1.0-demo/meshcfo-control-tower-demo.mp4)
· [release page](https://github.com/Cubiczan/meshcfo-control-tower/releases/tag/v0.1.0-demo)

Record in 1080p. Show the terminal first, then the Streamlit tower. Do not present DEMO issuers as real companies — say “demo fixture” every time you name one.

---

## 0:00–0:25 · The problem (talking head or title card)

> Audit committees do not need another chatbot. When an 8-K Item 4.02 or a 10-K Item 9A hits, the office of the CFO needs a **governed remediation brief**: why now, who owns it, which ICFR gaps, and what evidence closes them — with provenance on every claim.

Cut to README badges: **NVIDIA Nemotron 3 Nano** served on **Nebius Token Factory**.

---

## 0:25–0:55 · CLI JSON brief (terminal)

```bash
export NEBIUS_API_KEY=...   # do not show the secret; cut or blur
meshcfo-brief --fixture northstar | head
```

Voiceover:

> The CLI calls NVIDIA Nemotron-3-Nano-30B-A3B through Nebius Token Factory’s OpenAI-compatible API at api.tokenfactory.nebius.com. The output is not prose. It is a JSON brief with lock state, buyer seats, and source locators.

Scroll the JSON: `lock_state`, `buyer_seats`, `claims`, `chp`.

One line:

> Northstar Materials is a **DEMO** issuer. We do not fake real-company filings.

---

## 0:55–2:10 · Streamlit control tower

```bash
streamlit run app/streamlit_app.py
```

Click **Northstar Materials, Inc. (DEMO)** → **Generate remediation brief**.

Show, in order:

1. **Why now** — Item 4.02 non-reliance clock  
2. **ICFR gaps** — ASC 606 bill-and-hold / cutoff  
3. **Buyer seats** — CFO Accountable, Controller / process owner Responsible  
4. **Next actions** — evidence required, not “look into revenue”  
5. **Per-claim provenance** expander — agent, step, epistemic tag, excerpt locator  
6. **CHP** — foundation vs adversary; `PROVISIONAL_LOCK`

Switch fixture to **Lumenbridge Payments (DEMO)** (15 seconds): ITGC privileged access, CIO/CISO Responsible.

---

## 2:10–2:40 · How Token Factory + Nemotron are used

Over the pipeline diagram in the README or the Agent pipeline expander:

> Playbooks keep ownership deterministic. Nemotron on Token Factory writes the Audit Committee one-liner and the CHP attacks. The R0 gate still drops any claim that cannot point at a DEMO excerpt. That is Cubiczan MeshCFO — governance in front of generation.

Optional: flip **Offline playbooks only** to show the tower still works without a key, then flip back to live.

---

## 2:40–3:00 · Close

> Cubiczan MeshCFO Control Tower. NVIDIA Nemotron on Nebius Token Factory. MIT. Demo fixtures labeled DEMO. A CFO can tell you who owns the weakness before the next 10-Q.

End card:

```
Cubiczan · MeshCFO Control Tower
github.com/Cubiczan/meshcfo-control-tower
Nemotron 3 Nano · Token Factory
```

---

## Shot checklist

- [ ] Token Factory base URL visible in `/health` or README  
- [ ] Model id `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` visible  
- [ ] DEMO badge visible whenever a company name appears  
- [ ] Provenance table on screen for ≥ 8 seconds  
- [ ] No API keys in frame  
- [ ] Audio names **Nebius Token Factory** and **NVIDIA Nemotron** at least twice  

## Backup if the live key is down

```bash
meshcfo-brief --fixture northstar --offline --no-market
streamlit run app/streamlit_app.py
# toggle Offline playbooks only
```

Say on camera: live path is Token Factory; you are showing the same brief schema.
