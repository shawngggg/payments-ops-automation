# Payments Operations Automation — Build Requirements, Part 1

> **Scope of this part:** Wave 0 foundation (**F1–F6**) and the Wave 1 **ACH** rail. AML, SAR, and FinCEN/BSA obligations are specified as a first-class foundation capability (**F6**) and carried as a **rail-specific block** within ACH. Parts 2–3 cover Fedwire + RTP and SWIFT + stablecoin, each with its own AML/SAR/FinCEN block.
> The bank files SARs **as the obligated institution**, so F6 includes the full case-management-through-FinCEN-e-filing workflow.

**Conventions.** Requirement IDs: `FR` functional · `DR` data · `IR` integration · `NFR` non-functional · `CR` control/compliance. **[confirm]** = verify against current regulation; **[calibrate]** = Phase-0 figure. Regulatory timers are flagged because they move.

---

# WAVE 0 — FOUNDATION

## F1 — Golden reference & sanctions data

Single source for the entities, accounts, routing, and lists every payment and every screen depends on.

| ID | Requirement | Acceptance |
|---|---|---|
| F1-FR-01 | Master counterparties, accounts, and routing identifiers (ABA, IBAN, BIC), plus wallet allow/deny lists | One golden record per entity; no duplicates |
| F1-FR-02 | Ingest, version, and **effective-date** sanctions/watchlists (OFAC SDN & consolidated, plus internal lists) | List changes versioned with full history |
| F1-DR-01 | Full change history and audit on every reference and list record | Any value reconstructable to a point in time |
| F1-IR-01 | Consume list updates from providers/OFAC; publish to F2 and F6 | Updates propagate intraday |
| F1-NFR-01 | List-update propagation latency | Within **[calibrate]** of source publication, intraday |
| F1-CR-01 | Four-eyes on reference-data and list-parameter changes; full audit | No single-actor change to lists or routing |

## F2 — Shared screening service (real-time sanctions)

A single, blocking sanctions screen every rail calls before execution.

| ID | Requirement | Acceptance |
|---|---|---|
| F2-FR-01 | Screen every payment — originator, beneficiary, intermediary banks, references, and **wallet addresses** — against F1 lists **pre-execution** | No payment executes unscreened |
| F2-FR-02 | Block/hold on a hit; route to alert clearing; support fuzzy matching and good-guy/whitelist | Hits stop the payment; cleared alerts release it |
| F2-DR-01 | Persist every screening decision, match score, and disposition | Full screen history per payment |
| F2-IR-01 | Called synchronously by F3 for all rails; consumes F1 lists | Single screening service, not per-rail copies |
| F2-NFR-01 | Real-time latency budget for instant rails (no hold-and-review window) | ≤ **[calibrate] ms** p99; 24/7 availability |
| F2-CR-01 | OFAC blocking/rejecting; **report blocked transactions to OFAC within 10 business days** [confirm]; zero false-negative tolerance; four-eyes on alert clearing | Blocks reported on time; alert dispositions audited |

## F3 — Payment hub / orchestration

Owns the canonical lifecycle and routes to rail adapters.

| ID | Requirement | Acceptance |
|---|---|---|
| F3-FR-01 | Canonical payment lifecycle (capture → validate → screen → fund → execute → settle → advise → reconcile) with rail adapters | One lifecycle, rail differences isolated to adapters |
| F3-FR-02 | Idempotency and **duplicate detection** on inbound and outbound | No double-spend / double-post |
| F3-DR-01 | Canonical, **ISO 20022-aligned** payment object with full status history | Status reconstructable end to end |
| F3-IR-01 | Adapters for RTP, Fedwire, ACH, blockchain, SWIFT; calls F2 and F6 in-flight | Every payment screened and monitored |
| F3-NFR-01 | Throughput and availability, 24/7 for instant rails | Meets per-rail volume **[calibrate]** |
| F3-CR-01 | Limit/authorization checks; **four-eyes on high-value release**; full audit | High-value payments dual-controlled |

## F4 — Exceptions & investigations platform

The queue-driven desk where breaks and operational cases are worked.

| ID | Requirement | Acceptance |
|---|---|---|
| F4-FR-01 | Case management for repairs, returns, recalls, and non-receipt — with owner, SLA, aging, and escalation | Every exception is an owned, aging case |
| F4-IR-01 | Receives cases from the hub, screening, reconciliation, and AML monitoring | No exception is lost to email/spreadsheets |
| F4-CR-01 | Segregation of duties and audit on case disposition | Maker/checker on material actions |

## F5 — Reconciliation & settlement-position ledger

Ties every execution to the settlement/nostro position.

| ID | Requirement | Acceptance |
|---|---|---|
| F5-FR-01 | Reconcile executions to the settlement/nostro position per rail; detect breaks | Breaks detected same cycle |
| F5-FR-02 | **On-chain ↔ off-chain** reconciliation for stablecoin flows | On-ledger and book balances tie out |
| F5-IR-01 | Consume rail settlement confirmations, nostro statements (camt/MT940), and on-chain data | All settlement sources ingested |
| F5-CR-01 | Breaks escalate to F4; recon completeness evidenced and audited | No unreconciled position left open |

## F6 — AML monitoring + SAR / FinCEN case management

> **Distinct from F2.** F2 is real-time, blocking **sanctions** screening. F6 is behavioral, mostly post-event **AML monitoring** that generates *alerts*, drives *investigations*, and produces *regulatory filings*. The bank is the obligated filer.

| ID | Requirement | Acceptance |
|---|---|---|
| F6-FR-01 | Behavioral transaction monitoring across **all rails** (structuring, velocity, mule activity, unusual patterns) generating risk-scored alerts | All in-scope payments monitored; alerts scored |
| F6-FR-02 | Alert triage and **case management**; link related alerts/subjects; **continuing-activity reviews** | Related alerts consolidated into one case |
| F6-FR-03 | **SAR workflow** — decision, draft, and **e-file to the FinCEN BSA E-Filing System**; track acknowledgement; file **continuing SARs (~every 90 days)** where activity persists [confirm] | SARs filed and acknowledged; continuing reviews tracked |
| F6-FR-04 | **CTR** filing for currency thresholds (> $10,000, within 15 days) [confirm] | CTRs generated and filed on time |
| F6-FR-05 | **314(a)** scanning against FinCEN/law-enforcement requests; **314(b)** information-sharing support | 314(a) lists scanned each cycle; matches actioned |
| F6-FR-06 | CDD / beneficial-ownership checks, interfaced to KYC, as monitoring inputs | Customer risk and ownership available to monitoring |
| F6-DR-01 | Immutable alert, case, and SAR records; **5-year retention** [confirm]; **SAR confidentiality** (restricted access, no tipping-off) | SAR data access-controlled and audited |
| F6-IR-01 | Consume payment events from the hub (all rails) and customer/KYC data; output to **FinCEN BSA E-Filing** | Every rail feeds monitoring; filings transmit |
| F6-NFR-01 | Near-real-time monitoring for instant rails; enforce **SAR clock (30 days; 60 if no subject identified)** [confirm] | Filing deadlines tracked and alerted before breach |
| F6-CR-01 | Segregation of duties, QA sampling of alert/SAR decisions, and full audit; regulatory-timer enforcement | Filing timeliness and decision quality evidenced |

---

# WAVE 1 — ACH RAIL

## A1 — ACH origination & receipt STP

| ID | Requirement | Acceptance |
|---|---|---|
| A1-FR-01 | Ingest ACH originations (file and API), validate **NACHA format** and routing, enrich, and submit to the operator (**FedACH / EPN**) | Clean originations submit straight through |
| A1-FR-02 | Receive inbound ACH, screen (F2), monitor (F6), and post to the beneficiary | Inbound posts without manual touch on the happy path |
| A1-FR-03 | Support **Same-Day ACH** windows and standard next-day settlement | Items routed to the correct window |
| A1-DR-01 | Canonical ACH object (batch, entry, addenda) mapped to the F3 lifecycle | Entries traceable end to end |
| A1-IR-01 | Operator connectivity (FedACH/EPN); call F2, F6; settle to F5 | Each entry screened, monitored, reconciled |
| A1-NFR-01 | Throughput and window cutoff adherence | No missed processing windows **[calibrate]** |
| A1-CR-01 | **Reg E** (consumer protection), NACHA Operating Rules, screening, and dual control | Consumer and rule obligations enforced in-flow |

## A2 — ACH returns, reversals & NOC

| ID | Requirement | Acceptance |
|---|---|---|
| A2-FR-01 | Process inbound returns (**R-codes**), reversals, and **NOCs**; auto-match and post | Returns/NOCs auto-applied; unmatched → F4 |
| A2-FR-02 | Generate outbound returns within NACHA timeframes | Returns issued inside the window [confirm] |
| A2-CR-01 | Return-window timeliness tracked; audit | No window breaches; full audit |

## ACH — AML / SAR / FinCEN block (rail-specific)

| ID | Requirement | Acceptance |
|---|---|---|
| ACH-AML-01 | Monitor ACH-specific typologies — **structuring across batches**, mule networks, and **unauthorized-return signals** as risk inputs — feeding F6 | ACH typologies covered in monitoring |
| ACH-AML-02 | Enforce **BSA Travel Rule** data completeness on transmittals at/above threshold (originator/beneficiary information) [confirm threshold] | Non-compliant transmittals flagged/repaired |
| ACH-AML-03 | Route ACH alerts to F6 case management; SAR where warranted | ACH alerts investigable; SARs filed via F6 |
| ACH-AML-04 | Treat **Reg E unauthorized claims** as an AML signal and coordinate with disputes | Unauthorized claims correlated to monitoring |

---

## Dependencies & sequencing

- **F1 → F2 → F6** is the compliance spine: reference/sanctions data, then real-time screening, then behavioral monitoring and filing. ACH cannot go live without all three.
- **F3** (hub) must exist before any rail; **F4** and **F5** before ACH cutover so exceptions and settlement are handled.
- ACH (A1/A2) is the Wave 1 pilot precisely because it exercises the entire foundation — including F6 — on the highest-volume, most-standardized rail.

---

*Build Requirements Part 1 (v0.1) — foundation F1–F6 + ACH. Next: Part 2 — Fedwire + RTP, each with a real-time AML/SAR/FinCEN block (real-time monitoring, no review window).*
