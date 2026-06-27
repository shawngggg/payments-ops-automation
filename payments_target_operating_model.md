# Payments Operations Automation — Target Operating Model (v0.1)

> How the payments back office should *run* once automated. Six dimensions, each contrasting today's pain with the target design. Built on the framing in `payments_scope.md` (bank seat, US + SWIFT, outbound and inbound, screening as the spine). **[confirm]** marks items to verify; **[calibrate]** marks Phase-0 figures.

---

## Operating philosophy

Three ideas hold the model together:

1. **Exception-based.** Straight-through on the happy path; people touch only what breaks or what compliance flags. Headcount scales with exceptions and alerts — not with payment volume.
2. **Screen once, screen well.** Sanctions/AML screening is a shared, real-time service every rail calls — not six rail-specific implementations. The control is the spine, and false positives are a first-class cost to engineer down.
3. **Reconcile to the settlement position.** With no single stock-record equivalent, every flow must reconcile to the **settlement/nostro position** per rail. That is the integrity anchor.

---

## 1. Process & workflow

**Today:** Rail-siloed. RTP, Fedwire, ACH, cross-border, and any crypto flow run on separate processes and teams, each re-keying, each repairing, each screening in its own way. Exceptions are worked off spreadsheets and email.

**Target:** One **canonical payment lifecycle** (capture → validate → screen → fund → execute → settle → advise → reconcile) with rail-specific adapters at the edges. The happy path is straight-through; breaks and alerts route to a single, queue-driven **exceptions and investigations desk** with SLAs, ownership, and audit. Outbound and inbound both flow through the same screening and reconciliation spine.

---

## 2. Organization & people

**Today:** Teams organized **by rail** (a wire team, an ACH team, a cross-border team), each duplicating capture, repair, screening, and recon.

**Target:** Teams organized **by function** across all rails:
- **Processing & repair** — works STP exceptions across rails.
- **Screening / compliance operations** — clears sanctions and AML alerts (the largest queue).
- **Investigations** — returns, recalls, non-receipt, fraud cases.
- **Reconciliation & liquidity** — settlement/nostro recon and funding/prefunding.

The role shifts from re-keying payments to **resolving exceptions and clearing alerts**. Reskilling and a phased transition are explicit **[confirm]**.

---

## 3. Technology & data architecture

**Today:** Point-to-point rail connections, duplicated reference data, screening bolted onto each rail, reconciliation after the fact.

**Target:**
- A **payment hub / orchestration layer** that owns the canonical lifecycle and routes to rail adapters (RTP, Fedwire, ACH, blockchain, SWIFT).
- A **shared screening service** (sanctions, AML, fraud) called in-flight by every rail, tuned for low latency on instant rails.
- **Golden reference data** — counterparties, accounts, routing (ABA/IBAN/BIC), wallet allow-lists, sanctions lists — mastered once.
- **Connectivity** via real integration where it exists (ISO 20022 APIs/feeds, SWIFT, on-chain nodes); **RPA only to bridge** operator/correspondent portals with no feed, each with a decommission path.
- A **reconciliation & ledger** capability tying executions to the settlement/nostro position, including on-chain ↔ off-chain for stablecoin.

---

## 4. Controls & risk

**Today:** Screening quality and timing vary by rail; high false-positive rates create manual load; fraud controls uneven; audit reconstructed after the fact.

**Target:** Controls embedded **in-flow**:
- **Sanctions screening** as a mandatory gate on every payment, real-time on instant/irrevocable rails (no hold-and-review window), with model-governed tuning to cut false positives.
- **AML monitoring and fraud** scoring inline, with stronger checks on irrevocable rails (authorized-push-payment fraud).
- **Regulatory obligations** mapped to specific controls: Reg E (ACH consumer), Reg J / UCC 4A (Fedwire), NACHA rules (ACH), Travel Rule (crypto + cross-border), evolving stablecoin framework **[confirm]**.
- **Four-eyes** on high-value release and on collateral-grade actions; **full audit and retention** end to end.

---

## 5. Governance & sourcing

**Today:** Change is rail-by-rail; vendor/utility relationships managed in silos; no single owner of the payments operating model.

**Target:** A single **payments operations product owner** governs the canonical lifecycle and the shared services. **Build-vs-buy** is deliberate: buy/utilize commoditized capability (screening engines, SWIFT connectivity, on-chain infrastructure, correspondent and operator rails); **build** the orchestration, reference-data, and exception/control layers that differentiate. A steering committee owns the roadmap, prioritization, and aged-exception/alert review.

---

## 6. Metrics & KPIs

**Today:** Reported per rail, mostly volume and headcount; quality and risk under-instrumented.

**Target:** A shared scorecard across rails **[calibrate targets in Phase 0]**:

| Metric | What it measures |
|---|---|
| **STP rate** (per rail + blended) | Payments processed with no manual touch |
| **Screening false-positive rate** | Efficiency of the screening spine (the largest queue) |
| **Repair rate** | Share needing manual repair before execution |
| **Returns / reversals rate** | Inbound and outbound returns (esp. ACH) |
| **Settlement breaks** | Recon breaks against the nostro/settlement position |
| **Investigation aging & SLA** | Open cases by age (non-receipt, recalls, fraud) |
| **Intraday liquidity / prefunding** | Funding efficiency (RTP prefund, Fedwire intraday) |
| **Cost per payment** | The bottom line — should fall as STP rises |

---

## The shift in one line

From **rail-siloed, volume-linked, screen-everywhere** operations → to a **single exception-based lifecycle with one real-time screening spine, reconciled to the settlement position**, where people clear alerts and exceptions rather than re-key payments.

---

*Target operating model v0.1. Next in the arc: the automation roadmap — scoring and sequencing the rails and capabilities by volume × risk × feasibility.*
