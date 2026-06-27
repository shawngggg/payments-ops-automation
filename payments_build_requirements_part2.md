# Payments Operations Automation — Build Requirements, Part 2

> **Scope of this part:** Wave 2 rails — **Fedwire** (FW) and **RTP** (RTP). Both are **irrevocable**: once executed there is no clawback, so sanctions screening *and* AML decisioning must complete **pre-send**, and AML case coverage and SAR obligations run **24/7**. Each rail carries its own real-time AML/SAR/FinCEN block.
> Builds on Part 1 (foundation F1–F6 + ACH). Same conventions: `FR/DR/IR/NFR/CR`; **[confirm]** verify against current regulation; **[calibrate]** Phase-0 figure.

---

# FEDWIRE (wholesale RTGS — high-value, irrevocable, final)

## FW1 — Fedwire origination, receipt & STP repair

| ID | Requirement | Acceptance |
|---|---|---|
| FW1-FR-01 | Ingest wire instructions (channel/file/API), validate **ISO 20022** and routing (ABA), enrich, and submit to the **Fedwire Funds Service** | Clean, complete wires submit straight through |
| FW1-FR-02 | **Pre-send** sanctions screening (F2): a wire may not be released until screening clears — it cannot be recalled | No wire released with an open screening hit |
| FW1-FR-03 | **Repair queue** for incomplete/unstructured wires, routed to the desk (F4) with SLA | Repairs worked before cutoff; nothing auto-released unrepaired |
| FW1-FR-04 | Receive inbound wires, screen, monitor (F6), and post to the beneficiary | Inbound posts straight through on the happy path |
| FW1-DR-01 | Canonical **ISO 20022** wire object mapped to the F3 lifecycle, with full status history | Each wire traceable end to end |
| FW1-IR-01 | Fedwire Funds Service connectivity; call F2 and F6; settle to the master account / nostro via F5 | Each wire screened, monitored, reconciled |
| FW1-NFR-01 | Throughput and **Fedwire operating-hours** adherence; screening latency within the release path | Meets volume **[calibrate]**; no missed release windows |
| FW1-CR-01 | **Reg J / UCC 4A**, **mandatory four-eyes on high-value release**, OFAC, and full audit | High-value wires dual-controlled; obligations enforced in-flow |

## FW2 — Intraday liquidity & throughput

| ID | Requirement | Acceptance |
|---|---|---|
| FW2-FR-01 | Monitor master-account balance, intraday liquidity, queueing/throughput, and **daylight-overdraft** exposure | Liquidity visible in real time; queues managed |
| FW2-IR-01 | Consume Fed account/position data; interface to treasury | Position accurate intraday |
| FW2-CR-01 | Liquidity limits and overdraft controls; audit | Limit breaches alerted and controlled |

## Fedwire — AML / SAR / FinCEN block (real-time, high-value)

| ID | Requirement | Acceptance |
|---|---|---|
| FW-AML-01 | **Pre-send** high-value wire risk scoring (F6): because wires are irrevocable, AML risk must be assessed before release, with high-risk diverted to review before send | High-risk wires held pre-send, not post-hoc |
| FW-AML-02 | Enforce **BSA Travel Rule** completeness on transmittals **≥ $3,000** [confirm] (originator/beneficiary/intermediary data); reject or repair incomplete | No non-compliant wire released |
| FW-AML-03 | Monitor correspondent/**nested-relationship** risk, high-risk-jurisdiction exposure, and large-value/round-amount typologies | Wholesale typologies covered |
| FW-AML-04 | Route alerts to F6 case management; file SARs as obligated institution; track the **30/60-day clock** [confirm] | Wire alerts investigable; SARs filed on time |

---

# RTP (instant — 24/7/365, credit-push, irrevocable, prefunded)

## RTP1 — Real-time origination, receipt & screening

| ID | Requirement | Acceptance |
|---|---|---|
| RTP1-FR-01 | Ingest **credit-push** payments 24/7, validate **ISO 20022**, and submit to **TCH RTP**, returning accept/reject within the network time limit | End-to-end within RTP's seconds-level SLA |
| RTP1-FR-02 | **Inline** sanctions screening (F2) and **inline** AML risk scoring (F6) that complete **before send** — there is no hold-and-review window on an irrevocable instant rail | No payment sent with an unresolved screen/score |
| RTP1-FR-03 | Real-time funding check against the **prefunded** position before send | No send when prefunded position is insufficient |
| RTP1-FR-04 | Receive inbound, screen, post, and return acknowledgement within the SLA; support **Request for Payment (RfP)** | Inbound acknowledged within network limits |
| RTP1-DR-01 | Canonical ISO 20022 RTP object and RfP records mapped to F3 | Each payment and RfP traceable |
| RTP1-IR-01 | TCH RTP connectivity; **real-time** calls to F2 and F6; prefunded-position view via F5 | Screened, scored, funded, reconciled in-line |
| RTP1-NFR-01 | **24/7/365** availability with no processing-halting maintenance windows; screening/scoring within the release latency budget **[calibrate]** | No downtime that blocks settlement |
| RTP1-CR-01 | Irrevocability handling, **authorized-push-payment (APP) fraud** controls, real-time OFAC, audit | Fraud/sanctions controls enforced pre-send |

## RTP2 — Prefunding & liquidity (24/7)

| ID | Requirement | Acceptance |
|---|---|---|
| RTP2-FR-01 | Monitor and replenish the **prefunded joint-account position 24/7**, including weekends/holidays, with alerting before depletion | Position never silently depletes |
| RTP2-IR-01 | Interface to the Fed prefund account and treasury for replenishment | Replenishment automated/alerted |
| RTP2-CR-01 | Liquidity controls and audit; no send when underfunded | Underfunded sends blocked |

## RTP — AML / SAR / FinCEN block (real-time — no review window)

| ID | Requirement | Acceptance |
|---|---|---|
| RTP-AML-01 | **Pre-send** real-time AML scoring: high-risk payments must be held/diverted **before** transmission, since RTP cannot be reversed | No high-risk payment sent unreviewed |
| RTP-AML-02 | Detect **APP/scam typologies**, mule activity, and velocity in real time | Instant-rail fraud typologies covered |
| RTP-AML-03 | **24/7 case coverage and SAR-clock management** — filing obligations run continuously, including nights/weekends | Cases worked and deadlines tracked off-hours |
| RTP-AML-04 | Enforce **Travel Rule** data on credit transfers at/above threshold [confirm]; route alerts to F6; file SARs as obligated institution | Compliant transmittals; SARs filed via F6 |

---

## Dependencies & sequencing

- Both rails depend on the **F1 → F2 → F6** spine from Part 1, but raise the bar: screening and AML must run **inside the release path** (pre-send), not post-event, because neither rail can be recalled.
- **RTP forces 24/7 operations** — prefunding (RTP2) and AML case coverage (RTP-AML-03) must run continuously; this is the operating-model change Wave 2 introduces.
- Fedwire's **Travel Rule completeness** (FW-AML-02) and mandatory **high-value four-eyes** (FW1-CR-01) are the wholesale-specific controls.
- Sequence Fedwire slightly ahead of RTP: it shares ISO 20022 and the release-path pattern but on business hours, making it the safer place to prove pre-send screening before going 24/7.

---

*Build Requirements Part 2 (v0.1) — Fedwire + RTP with real-time AML/SAR/FinCEN. Next: Part 3 — SWIFT (cross-border, nested-correspondent typologies, gpi) + stablecoin (wallet analytics, crypto Travel Rule, custody), each with its own AML/SAR/FinCEN block.*
