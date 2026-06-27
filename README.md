# Payments Operations Automation — Design Program

> A self-directed, end-to-end design package for automating a bank's back-office payment operations across five rails — **RTP, Fedwire, ACH, stablecoin, and SWIFT** — with a working, in-browser demo and a transparent (no-AI) analysis engine.

> ⚠️ **Illustrative / portfolio project.** All data is **synthetic**, all figures are placeholders, and this is **not affiliated with or representing any employer**. No real or confidential information is used. Regulatory details are flagged for verification.

**🔗 [Live demo](https://shawngggg.github.io/payments-ops-automation/)**  ·  **📄 [Program profile](payments_program_profile.md)**  ·  **🧠 [How the analysis works](payments_analysis_pipeline.md)**

---

## Why payments operations is hard

A bank in payments sits **between its customers and the payment networks**, running every payment on both an outbound and an inbound path. Two things make it hard:

- **There's no single ledger.** The integrity anchor is the **settlement / nostro position per rail** — everything must reconcile to it.
- **Compliance is the spine, not a side process.** Every payment passes a mandatory **sanctions-screening gate**, and on irrevocable rails (RTP, Fedwire, SWIFT, stablecoin) it must clear **pre-send** — there's no hold-and-review window once the money moves.

The program is built on three principles: **exception-based** (headcount scales with exceptions, not volume), **screen once** (one real-time service every rail calls), and **reconcile to the settlement position**.

---

## The demo

`payments_stp_console.html` runs in any browser (open it locally, or use the live link above — it's self-contained, no internet needed). Press **Start** and payments stream through Capture → Screen → AML → Fund → Settle:

- Straight-through payments settle; exceptions peel to an **investigations desk** with their **escalation path** and **recommended solution** shown inline.
- Irrevocable rails tag exceptions **PRE-SEND** — the control clears before the money moves.
- Operational exceptions auto-clear via automation; **compliance-critical items** (sanctions blocks, AML alerts, address risk) wait for a person, with real decision buttons.

*(Tip: add a screen-recording GIF here — it's the single best thing for a README.)*

---

## How the analysis works — no AI, no API key

Classification (screening result, exception type, AML/SAR flags, status, escalation, recommendation) is produced by **deterministic, rule-based Python** you can read line by line in [`payments_analyzer.py`](payments_analyzer.py). Why rules and not AI: in a financial-crime context, **explainability and reproducibility are requirements** — a rule can be shown to a regulator and reproduced exactly.

Proven at scale: the engine classifies **1,000,000 transactions in ~16 seconds**, with realistic aggregates (~90.7% STP, ~34k AML alerts, ~900 SARs, ~4k sanctions blocks).

---

## What's inside

| Area | Files |
|---|---|
| **Strategy & design** | scope · target operating model · roadmap |
| **Build spec** | build requirements (3 parts) · stablecoin discovery · exception matrix |
| **Decision tools** | Phase-0 calibration model (Excel) |
| **Leadership materials** | program proposal (Word) · leadership deck (PowerPoint) |
| **Working demo** | interactive STP console (HTML) |
| **Data & analysis** | rules-engine analyzer · methodology · 100K sample · 1M analyzed (gzipped) |

See [`payments_program_profile.md`](payments_program_profile.md) for the full catalog and a recommended presentation flow.

---

## Quick start

```bash
# 1) Open the demo
open payments_stp_console.html      # or just double-click it

# 2) Run the rules engine on a raw sample
python payments_analyzer.py         # raw -> enriched, fully reproducible
```

---

## Status & disclaimers

This is an illustrative design package, not a production system. Sample data is synthetic; figures and rates are placeholders. Regulatory specifics (Travel Rule thresholds, OFAC windows, SAR clocks, the federal stablecoin framework, ISO 20022 dates) are marked for verification against current sources. Reference lists in the analyzer are illustrative; production uses official OFAC/FATF data and licensed feeds.

## License

Code: MIT. Documents: CC BY 4.0. *(Adjust to your preference.)*
