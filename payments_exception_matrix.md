# Payments Operations — Exception Handling Matrix

> Escalation path and recommended solution for every exception type in the payments operating model. The same fields are carried per row in `payments_sample_transactions.csv` (`exception_type`, `escalation_path`, `recommended_solution`), so fails can be grouped by type and routed automatically. **[confirm]** = verify timer against current rule.

---

## How to read this

Each exception type has a **trigger** (what raises it), an **escalation path** (the tiers it moves through, with the owning function and any regulatory clock), and a **recommended solution** — the remediation now, and the capability that reduces recurrence. Escalation is SLA-driven: an item moves up a tier on breach, aging, or severity, not by discretion alone.

---

## Compliance-driven exceptions

### Sanctions hit — blocked
- **Trigger:** Screening (F2) matches a sanctioned party/address; payment held pre-send.
- **Escalation:** Screening L1 → **Sanctions/OFAC officer** (disposition) → block confirmed → **OFAC report (≤ 10 business days)** [confirm] → Compliance head for SAR consideration.
- **Owning function:** Sanctions compliance.
- **Recommended solution:** Golden sanctions/reference data (F1) and tuned real-time screening (F2); reduce wrongful blocks through list quality and good-guy lists.

### Sanctions hit — cleared (false positive)
- **Trigger:** Screening match that resolves to a non-sanctioned party (name/fuzzy collision).
- **Escalation:** **Screening L1** clears with good-guy evidence; no further tier unless pattern recurs.
- **Owning function:** Screening operations.
- **Recommended solution:** Tune matching thresholds and maintain whitelists (F2). This is the single largest manual-load reducer — false positives dominate screening volume.

### AML alert
- **Trigger:** Behavioral monitoring (F6) flags structuring, velocity, mule, or typology risk.
- **Escalation:** **Investigator L1** (triage) → **Financial-crimes L2** (investigation, link analysis) → **SAR decision** → **e-file to FinCEN (30 days; 60 if no subject)** [confirm] → **continuing review every ~90 days** [confirm].
- **Owning function:** Financial-crimes / BSA (bank files as obligated institution).
- **Recommended solution:** Behavioral-model tuning and case automation per rail (F6); real-time, pre-send scoring on irrevocable rails.

### Travel Rule incomplete
- **Trigger:** Transmittal at/above threshold missing required originator/beneficiary data [confirm].
- **Escalation:** **Repair L1** (complete from reference data) → **Compliance** if unresolved → **reject/return** if non-compliant pre-send.
- **Owning function:** Payment ops + compliance.
- **Recommended solution:** Enforce Travel Rule completeness at capture; auto-populate from golden reference data; block incomplete transmittals before send.

### Address risk review (stablecoin)
- **Trigger:** Blockchain analytics flags a wallet/address (sanctioned, mixer, high-risk exposure) pre-broadcast.
- **Escalation:** **Crypto-ops** review → **Compliance** → **pre-send block** if high-risk → **SAR** if warranted.
- **Owning function:** Crypto-ops + compliance.
- **Recommended solution:** Pre-send blockchain-analytics screening and allow-listing; custody multi-party approval. Because transfers are irreversible, the control must clear **before broadcast**.

---

## Operational exceptions

### Format repair
- **Trigger:** Validation fails (ISO 20022 / NACHA format, routing, missing fields).
- **Escalation:** **Repair queue L1** → **supervisor** if aged past SLA.
- **Owning function:** Processing & repair.
- **Recommended solution:** ISO 20022 enrichment and validation at capture (F3) plus golden reference data (F1) to auto-complete; drives the STP rate.

### Investigation / non-receipt (cross-border)
- **Trigger:** Customer or correspondent query on a delayed or unconfirmed cross-border payment.
- **Escalation:** **Investigations L1** → **correspondent/relationship L2** → **gpi trace** to locate.
- **Owning function:** Cross-border investigations.
- **Recommended solution:** SWIFT gpi tracking integration and nostro reconciliation (F5); automated status and tracing to cut investigation time.

### Return / NOC (ACH)
- **Trigger:** Inbound ACH return (R-code) or notification of change.
- **Escalation:** **Auto-match L1** posts/applies → **exceptions desk** if unmatched.
- **Owning function:** ACH operations.
- **Recommended solution:** Automated returns/NOC processing (A2); auto-apply NOC corrections to reference data to prevent repeat breaks.

---

## Summary table

| Exception type | Escalation (tiers) | Regulatory clock | Recommended solution |
|---|---|---|---|
| Sanctions hit — blocked | Screening → OFAC officer → report | OFAC ≤10 bd [confirm] | Golden lists + tuned screening (F1/F2) |
| Sanctions hit — cleared | Screening L1 | — | Tune matching / whitelist (F2) |
| AML alert | Investigator → Fin-crimes → SAR | SAR 30/60d; 90d review [confirm] | Behavioral tuning + case automation (F6) |
| Travel Rule incomplete | Repair → compliance → reject | — | Enforce data at capture; auto-populate |
| Address risk review | Crypto-ops → compliance → block | — (SAR if warranted) | Pre-send analytics + allow-list |
| Format repair | Repair L1 → supervisor | — | ISO 20022 enrich + ref data (F1/F3) |
| Investigation / non-receipt | Investigations → correspondent → gpi | — | gpi trace + nostro recon (F5) |
| Return / NOC | Auto-match → exceptions desk | NACHA windows [confirm] | Automated returns/NOC (A2) |

---

*Exception Handling Matrix v0.1. The fail-to-regulatory spine: a compliance exception that ages becomes a reportable event (OFAC) or a filing obligation (SAR), with the clock starting at detection — which is why escalation is SLA-driven and every type maps to a named remediation.*
