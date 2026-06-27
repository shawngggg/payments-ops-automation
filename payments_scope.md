# Payments Operations Automation — Project Scope (v0.1)

> **Status:** Draft for confirmation. Items marked **[CONFIRM]** are assumptions that shape everything downstream — correct these first.
> Sister program to the post-trade automation work; same delivery arc (scope → target operating model → roadmap → requirements → calibration → proposal → deck → demo).

---

## 1. Framing & assumptions

| Dimension | Assumption | Note |
|---|---|---|
| **Perspective** | Payments operations at a **bank** — a direct participant across these rails, sitting between its customers and the payment networks **[CONFIRM]** | A fintech/PSP would access most rails via a sponsor bank, which reframes participation and settlement. |
| **Objective** | Automate back-office, post-initiation payment operations | Channel/front-end origination UX is **out of scope**. |
| **Reference market** | US infrastructure (TCH, the Federal Reserve) plus SWIFT cross-border **[CONFIRM]** | Settlement mechanics are rail- and jurisdiction-specific. |
| **Lifecycle** | Instruction received → settled → reconciled → investigated, on both the **outbound** and **inbound** path | "Payment operations" begins once an instruction is captured. |
| **The spine** | Every payment passes a **sanctions/AML screening gate** | Compliance is not a stage here — it's the choke point the whole operation is built around. |

---

## 2. The bank's structural position

The bank is an intermediary between its **customers** (originators and beneficiaries) and the **payment rails/networks**. Each payment runs one of two ways:

- **Outbound (origination):** customer instruction → validate → screen → fund → execute on the rail → settle → advise.
- **Inbound (receipt):** rail delivers a payment → screen → post to the beneficiary → advise → reconcile.

Two structural variables shape every rail: **direct vs indirect participation** (do we hold the settlement account, or reach the rail through a correspondent/operator), and **push vs pull** (credit-push only on RTP; debit-pull available on ACH). Unlike post-trade, there is no single golden ledger like the stock record — instead the anchor is the **settlement/nostro position** per rail, which all flows must reconcile to.

---

## 3. The common payments lifecycle (the spine)

1. **Capture** — instruction received (channel, file, API, or inbound from the rail).
2. **Validation & enrichment** — format, account/routing validation (ABA, IBAN, BIC, wallet), reference data.
3. **Screening & compliance** — **sanctions (OFAC), AML/transaction monitoring, fraud** — real-time for instant/irrevocable rails.
4. **Authorization & funding** — balance/limit checks, liquidity, prefunding (RTP).
5. **Execution / clearing** — format and submit to the rail.
6. **Settlement** — funds settle (RTGS, deferred net, or on-chain).
7. **Confirmation / advising** — status to the customer; tracking (gpi, RTP ack).
8. **Exceptions & investigations** — repairs, returns, reversals, recalls, non-receipt cases.
9. **Reconciliation** — settlement/nostro accounts; on-chain vs off-chain ledgers.
10. **Reporting** — regulatory and internal.

---

## 4. Rail-by-rail map

| | RTP | Fedwire | ACH | Stablecoin | SWIFT |
|---|---|---|---|---|---|
| **Operator / network** | TCH RTP | Federal Reserve (Fedwire Funds) | FedACH + EPN (TCH) | Public blockchains | SWIFT network (correspondent banking) |
| **Settlement model** | Real-time gross, **prefunded** (joint account at the Fed) | **RTGS** across Fed master accounts | **Deferred net**, batched | **On-chain** settlement finality | No central settlement — via **nostro/vostro** correspondents |
| **Speed / availability** | Instant, **24/7/365** | Same-day, real-time, business hours | Same-day windows + next-day | Near-instant, 24/7 | Variable (minutes–days), multi-hop |
| **Message standard** | ISO 20022 | ISO 20022 (migrated, 2025) **[confirm]** | NACHA format | On-chain tx + travel-rule msgs | ISO 20022 MX (MT→MX migration) **[confirm]** |
| **Value / use** | Low–mid, credit-**push** only, irrevocable | High-value/wholesale, final | Low-value, high-volume, push & **pull** | Variable, irreversible | Cross-border, multi-currency |
| **Reversibility** | Irrevocable; Request for Return | Irrevocable / final | Returns, reversals, NOCs (windows) | Irreversible (no chargeback) | Recalls via message; not guaranteed |
| **Automation hotspots** | Real-time screening, **prefunding/liquidity**, Request for Payment | STP **repair**, real-time screening, liquidity/throughput | **Returns/NOC** automation, batch exceptions, Same-Day windows | **On-chain ↔ off-chain recon**, wallet screening, travel rule, key/custody | **Repair/STP**, nostro recon, investigations (gpi) |

---

## 5. Compliance & control layer (the spine)

- **Sanctions screening (OFAC)** — the choke point; real-time and low-latency for instant rails, where there is no "hold and review" window.
- **AML / transaction monitoring** (BSA) and **fraud** — especially on instant, irrevocable rails (authorized-push-payment fraud).
- **Regulatory framework:** Reg E (ACH consumer), Reg J / UCC 4A (Fedwire), NACHA Operating Rules (ACH), **Travel Rule** (crypto + cross-border), and the **evolving federal stablecoin framework [confirm]**.
- **Returns, recalls, and investigations** — the rules and timeframes differ sharply by rail (ACH return windows vs irrevocable wires vs irreversible on-chain).

---

## 6. Where automation concentrates (cross-rail read)

- **Real-time screening** is the highest-stakes automation: instant + irrevocable rails remove the manual review window.
- **Exceptions & repair** drives STP rates — the core back-office lever.
- **Returns / reversals / investigations** are rail-specific and labor-heavy.
- **Reconciliation** — settlement/nostro and, for stablecoin, on-chain vs off-chain.
- **Liquidity & funding** — prefunding (RTP), intraday liquidity (Fedwire), on/off-ramp (stablecoin).

---

## 7. Open decisions

1. **[CONFIRM]** Bank vs PSP/fintech (sponsor-bank model).
2. **[CONFIRM]** Jurisdiction breadth (US + cross-border via SWIFT).
3. **House vs customer scope** — are bank-internal/treasury payments in, or customer flow only?
4. **Direct vs indirect participation** per rail.
5. **In/out of scope** — card rails, FX, and wallets/on-ramps: in or out?
6. **Pilot rail** — which rail leads Phase 1? (ACH = highest volume; RTP/stablecoin = highest real-time/irrevocable risk; SWIFT = highest cross-border complexity.)

---

## 8. Suggested phasing

- **Phase 0 — Framing & inventory:** ratify Section 1; inventory systems and, per rail, the actual access method (direct/API/operator/correspondent) and screening setup.
- **Phase 1 — Current-state mapping:** map the pilot rail end to end, both outbound and inbound, to the settlement/nostro position.
- **Phase 2 — Candidate identification:** tag each step integrate / RPA-bridge / leave-manual.
- **Phase 3 — Prioritize & roadmap:** rank by volume × risk (fraud/sanctions/regulatory) × feasibility.

---

*Document version 0.1 — payments program kickoff. Ratify Section 1 and answer Section 7 to lock scope.*
