# Payments — Analysis Pipeline & Tooling

> **What turns a raw transaction into the final enriched result, and what tool does it.** This document answers a direct question: is the analysis done by an AI tool via an API key, or by built-in logic? It is part of the project deliverable so the method is transparent and auditable.

---

## 1. Direct answer

**No AI model and no API key are used to analyze the transactions.** The analysis is performed by **deterministic, rule-based logic written in plain Python** — a rules engine where every decision is an explicit, inspectable `if/elif` condition. There is no large language model, no machine-learning model, and no external AI service in the path.

To be precise about each tool in the project:

| Tool | Role | AI involved? |
|---|---|---|
| **Python rules engine** (`payments_analyzer.py`) | Analyzes raw transactions → screening result, exception type, AML/SAR flags, status, escalation, recommendation | **No** — explicit rules |
| **Python generator** (`generate_payments_dataset.py`) | Produces the synthetic sample dataset (seeded randomness + the same rules) | **No** |
| **Excel** (`payments_phase0_calibration.xlsx`) | Phase-0 prioritization model (scoring, weights) — **not** transaction analysis | **No** — formulas |
| **HTML/JS console** (the interactive demo) | UI to visualize and interact with the flow | **No** — deterministic JS |

Why rules and not AI: in a regulated payments/financial-crime context, **explainability and auditability are requirements**. A rule ("name matched the sanctions list", "amount fell in the structuring band") can be shown to an auditor or regulator and reproduced exactly. That is a deliberate design choice, not a limitation.

---

## 2. The pipeline — raw transaction to final result

```
 RAW TRANSACTION                       (rail, direction, amount, parties, country, account/address, ...)
        |
   [1] Ingestion        read the raw record (CSV / API / feed)
        |
   [2] Validation       required fields present? format valid?            -> Format repair
        |
   [3] Sanctions screen  party/address/country vs lists                   -> Hit-blocked / Hit-cleared
        |
   [4] AML monitoring    structuring, high-risk+large, typologies         -> AML alert (-> SAR)
        |
   [5] Rail-specific     Travel Rule completeness, wallet risk, returns   -> Travel Rule / Address risk / Return
        |
   [6] Classification    first rule that fires sets exception_type & final_status
        |
   [7] Routing lookup    exception_type -> escalation_path + recommended_solution  (Exception Matrix)
        |
   ENRICHED RESULT       + screening_result, aml_alert, sar_filed, exception_type, final_status, escalation, recommendation
        |
   [8] Visualization     dashboard (Tableau) and/or the interactive console (UI)
```

Steps 2–7 are the analysis, and they live in `payments_analyzer.py`. Step 8 is presentation only.

---

## 3. The rules (what each step actually checks)

Applied in priority order; the first match classifies the payment:

1. **Sanctions — blocked:** originator/beneficiary matches the sanctions watchlist → `Hit-blocked`, status **Blocked**.
2. **Sanctions — cleared:** counterparty country on the sanctioned-jurisdiction list → `Hit-cleared` (held, cleared after review).
3. **AML — structuring:** amount just under the reporting threshold (9,000–9,999) → **AML alert** (investigated; SAR filed only if substantiated).
4. **AML — high-risk + large:** high-risk jurisdiction and amount ≥ 1,000,000 → **AML alert**, SAR.
5. **Format repair:** a required field (beneficiary, account) missing → **Format repair**.
6. **Travel Rule:** amount ≥ threshold and Travel-Rule data incomplete → **Travel Rule incomplete**.
7. **Address risk (stablecoin):** destination wallet on the flagged-address list → **Address risk review**.
8. **Return / NOC (ACH):** inbound ACH carrying a return code → **Return / NOC**.
9. Otherwise → **STP** (clean, straight-through).

Reference lists (watchlist names, sanctioned/high-risk countries, flagged wallets, thresholds) are small **illustrative samples** embedded in the script; production replaces them with official OFAC/FATF data and live vendor feeds.

---

## 4. Two distinct Python tools (don't confuse them)

- **The analyzer** (`payments_analyzer.py`) is the real thing: **raw in → analyzed out**, by rules. Run it on `payments_raw_sample.csv` to produce `payments_analyzed_sample.csv`.
- **The generator** (`generate_payments_dataset.py`) fabricates a large *synthetic* sample for volume and dashboard demonstration, using seeded randomness plus the same classification rules. It exists only to populate analytics before real feeds are connected.

In production there is **only the analyzer's role**, fed by live payment feeds — the generator is scaffolding.

---

## 5. Worked example

`payments_raw_sample.csv` holds 16 raw transactions (raw fields only — no outcomes). Running the analyzer produces `payments_analyzed_sample.csv`, where each row gains its screening result, exception type, AML/SAR flags, status, escalation path, and recommendation. For example:

- A Fedwire payment to a watchlisted beneficiary → `Hit-blocked` → **Sanctions hit (blocked)** → escalation to the sanctions officer and OFAC report.
- An ACH payment of 9,500 → structuring rule → **AML alert** → financial-crimes investigation (a SAR is filed only if the activity is substantiated, so SARs are a subset of alerts — at scale, roughly a few percent).
- A SWIFT payment of 8,000 with incomplete Travel-Rule data → **Travel Rule incomplete** → repair → reject if unresolved.

Same raw input, same rules, same output — every time. That reproducibility is the point.

---

## 6. How this maps to the built program

The analyzer is a faithful, simplified stand-in for the production capabilities:

- Step 3 (sanctions) → the **shared screening service (F2)**.
- Step 4 (AML) → **AML monitoring + SAR/FinCEN case management (F6)**.
- Steps 2, 5, 6 → the **payment hub (F3)** and **exceptions platform (F4)**.
- Step 7 (routing) → the **Exception Handling Matrix** applied by F4.

Production systems are more sophisticated (and some AML engines add ML models for anomaly detection), but they are specialized, governed financial-crime systems — **not** a general AI tool called over an API. The explainable-rules approach shown here is the baseline those systems are held to.

---

*Analysis Pipeline & Tooling v0.1. Source of truth: `payments_analyzer.py`. All reference lists and thresholds are illustrative and flagged for Phase-0 calibration.*
