# Payments Operations Automation — Build Requirements, Part 3

> **Scope of this part:** Wave 3 rails — **SWIFT** (SW) cross-border correspondent payments and **stablecoin** (SC) on-chain payments. SWIFT is the highest-risk AML surface (multi-hop, multi-party, sanctions-heavy); stablecoin is the most novel and the **long-lead** rail (custody, blockchain analytics, evolving rules) — its discovery should run in parallel with Wave 1.
> Builds on Parts 1–2. Conventions: `FR/DR/IR/NFR/CR`; **[confirm]** verify against current regulation; **[calibrate]** Phase-0 figure.

---

# SWIFT (cross-border correspondent — messaging, settled via nostro/vostro)

## SW1 — Cross-border origination, receipt & STP repair

| ID | Requirement | Acceptance |
|---|---|---|
| SW1-FR-01 | Ingest cross-border instructions, validate **ISO 20022 MX** (handle legacy **MT** during any residual coexistence [confirm]), enrich (BIC, correspondent routing, currency), and submit over SWIFT | Clean, fully-structured payments submit straight through |
| SW1-FR-02 | **Repair queue** for incomplete/unstructured cross-border messages (historically the highest repair-rate rail), routed to F4 with SLA | Repairs worked before correspondent cutoffs |
| SW1-FR-03 | **Pre-release** sanctions screening (F2) across **all parties and intermediaries** in the chain | No message released with an open hit on any party |
| SW1-FR-04 | Receive inbound, screen, monitor (F6), and post; capture **gpi UETR** for end-to-end tracking | Inbound posts with tracking reference retained |
| SW1-DR-01 | Canonical **ISO 20022 MX** object with gpi UETR and correspondent routing, mapped to F3 | Each payment traceable across hops |
| SW1-IR-01 | SWIFT connectivity; correspondent nostro accounts; call F2/F6; settle/reconcile via F5 | Screened, monitored, reconciled to nostro |
| SW1-CR-01 | OFAC (cross-border-heavy), correspondent due diligence, four-eyes on high-value, full audit | Cross-border controls enforced in-flow |

## SW2 — Nostro reconciliation & investigations (gpi)

| ID | Requirement | Acceptance |
|---|---|---|
| SW2-FR-01 | Reconcile nostro/vostro accounts; investigate non-receipt/delays using **gpi tracing**; handle recalls and charges/fees | Breaks and delays traced and resolved |
| SW2-IR-01 | Consume nostro statements (**camt.053 / MT940**) and gpi status | Nostro position accurate; status visible |
| SW2-CR-01 | Reconciliation completeness and investigation SLA; audit | No unreconciled nostro item left open |

## SWIFT — AML / SAR / FinCEN block (cross-border — highest risk)

| ID | Requirement | Acceptance |
|---|---|---|
| SW-AML-01 | Detect cross-border typologies — **nested correspondent**, shell/front companies, **trade-based money laundering**, high-risk-jurisdiction exposure | Cross-border typologies covered in F6 |
| SW-AML-02 | Screen and monitor **every party across the multi-hop chain** (ordering, intermediary, beneficiary institutions) | No party in the chain unscreened/unmonitored |
| SW-AML-03 | Enforce **Travel Rule** on cross-border transmittals; verify data completeness in MX (serial **and cover** payments) and **detect information stripping** | Incomplete/stripped messages flagged and repaired |
| SW-AML-04 | Maintain **correspondent banking due diligence** (respondent risk) as a monitoring input | Respondent risk feeds alerting |
| SW-AML-05 | Route alerts to F6; file SARs as obligated institution; OFAC block/reject and **report within 10 business days** [confirm] | SARs filed on the 30/60-day clock; blocks reported |

---

# STABLECOIN (on-chain — wallet-to-wallet, irreversible, 24/7) — long-lead

## SC1 — On-chain origination, receipt & wallet management

| ID | Requirement | Acceptance |
|---|---|---|
| SC1-FR-01 | Originate on-chain stablecoin payments; validate destination address; **pre-send** screen the address (F2 + **blockchain analytics**) and AML-score (F6) — **transfers are irreversible** | No transfer broadcast with an unresolved screen/score |
| SC1-FR-02 | Sign and broadcast the transaction, then confirm **on-chain finality** (block confirmations); receive inbound, screen, and credit | Settlement confirmed to required confirmations |
| SC1-FR-03 | **Wallet and key management / custody** (segregation; multi-sig or MPC; HSM); gas/fee management; supported-chain selection | Keys never single-controlled; custody auditable |
| SC1-DR-01 | Canonical on-chain object (tx hash, addresses, chain, token, confirmations) mapped to F3; wallet inventory | Each transfer and wallet position traceable |
| SC1-IR-01 | Blockchain nodes/infrastructure, custody/key platform, blockchain-analytics provider; call F2/F6; **on-chain ↔ off-chain** recon via F5 | On-ledger and book records reconcile |
| SC1-NFR-01 | 24/7 operation; irreversibility handling; finality-confirmation latency **[calibrate]** | No credit before required finality |
| SC1-CR-01 | Custody/key controls (segregation, multi-party approval), address screening, irreversibility safeguards, audit | Custody and pre-send controls enforced |

## SC2 — On/off-ramp & reconciliation

| ID | Requirement | Acceptance |
|---|---|---|
| SC2-FR-01 | Manage **fiat ↔ stablecoin** conversion (on/off-ramp) with **source-of-funds** checks; link the fiat leg to ACH/wire rails | Ramps controlled; fiat leg traceable |
| SC2-FR-02 | **On-chain ↔ off-chain reconciliation** and balance/reserve verification | On-chain balances tie to the book continuously |
| SC2-CR-01 | Source-of-funds evidence and reconciliation completeness; audit | Ramp activity evidenced and reconciled |

## Stablecoin — AML / SAR / FinCEN block (on-chain — novel)

| ID | Requirement | Acceptance |
|---|---|---|
| SC-AML-01 | **Pre-send** wallet/address risk scoring via blockchain analytics — **OFAC-listed addresses**, mixers, darknet, sanctioned-exposure tracing — because transfers cannot be reversed | High-risk addresses blocked before broadcast |
| SC-AML-02 | Enforce the **crypto Travel Rule (VASP-to-VASP)** — transmit/receive originator-beneficiary data at/above threshold [confirm]; identify the counterparty VASP | Non-compliant transfers held; counterparty VASP identified |
| SC-AML-03 | **Source-of-funds / source-of-wealth** on ramps; cross-chain transaction tracing | Ramp and cross-chain activity traced |
| SC-AML-04 | Route alerts to F6; file SARs (with crypto-specific data) as obligated institution; **OFAC block/report** on listed addresses | SARs filed; sanctioned-address activity blocked/reported |
| SC-AML-05 | Track **evolving FinCEN / federal stablecoin obligations** and adapt controls [confirm — framework still developing] | Controls updated as rules finalize |

---

## Long-lead flag — stablecoin discovery

Stablecoin has the most external dependencies of any rail — **custody/key infrastructure, a blockchain-analytics provider, node/chain infrastructure, on/off-ramp partners, and an unsettled regulatory framework**. Exactly as collateral did in the post-trade program, **its discovery should begin in Wave 1**, in parallel, so a build-vs-buy decision (custody, analytics, ramps) and the regulatory position are resolved before build. A dedicated stablecoin discovery spec — target architecture, custody model, analytics/Travel-Rule vendor assessment, and the regulatory map — is the recommended next deep-dive.

---

## Dependencies & sequencing

- Both rails depend on the **F1 → F2 → F6** spine, and both demand **pre-send** screening/AML (SWIFT because recalls aren't guaranteed; stablecoin because transfers are irreversible).
- SWIFT adds **multi-party, multi-hop** screening and **stripping detection** — the broadest sanctions surface in the program.
- Stablecoin adds **custody/key management** and **on-chain ↔ off-chain reconciliation** — capabilities with no analog on the other four rails.
- Sequence SWIFT ahead of stablecoin: SWIFT reuses ISO 20022 and the nostro-reconciliation pattern, while stablecoin requires net-new custody and analytics infrastructure that discovery must de-risk first.

---

*Build Requirements Part 3 (v0.1) — SWIFT + stablecoin with AML/SAR/FinCEN. Requirements now complete across all five rails (ACH, Fedwire, RTP, SWIFT, stablecoin) plus the F1–F6 foundation. Next in the arc: Phase 0 calibration workbook, then proposal, deck, and demo.*
