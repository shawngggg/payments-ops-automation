# Payments Operations Automation — Roadmap (v0.1)

> Scores and sequences the five rails and the shared capabilities into delivery waves. Same method as the post-trade roadmap: **Volume × Risk × Feasibility**, foundation first, then rails in priority order. Scores are **indicative pending Phase-0 calibration [calibrate]**.

---

## 1. Scoring method

Each initiative is scored 1–5 on three axes:

- **Volume** — transaction volume and the manual workload it removes.
- **Risk** — sanctions, fraud, irrevocability, and regulatory exposure (the cost of getting it wrong).
- **Feasibility** — data quality, connectivity maturity, and standardization (how buildable it is now).

High volume **and** high feasibility → do early. High risk but low feasibility → sequence later on a mature platform, but **start discovery early**. Foundation capabilities are enablers — built first regardless of score, because nothing is straight-through until they exist.

---

## 2. Foundation (Wave 0 — enablers)

| ID | Capability | Why it gates everything |
|---|---|---|
| **F1** | Golden reference & sanctions data | Counterparties, accounts, routing (ABA/IBAN/BIC), wallet allow-lists, sanctions lists — every screen and every payment depends on it. |
| **F2** | Shared screening service | Real-time sanctions/AML/fraud, called by every rail. **The spine.** |
| **F3** | Payment hub / orchestration | The canonical lifecycle + rail adapters. |
| **F4** | Exceptions & investigations platform | The queue-driven desk where breaks and alerts are worked. |
| **F5** | Reconciliation & settlement-position ledger | Ties executions to the nostro/settlement position; on-chain ↔ off-chain. |

---

## 3. Scored backlog (rail initiatives)

| Initiative | Vol | Risk | Feas | Wave | Rationale |
|---|:--:|:--:|:--:|:--:|---|
| **ACH** origination/receipt STP | 5 | 3 | 5 | 1 | Highest volume, most standardized (NACHA), reversible — proves the model with the biggest cost-out. |
| **ACH** returns / NOC automation | 4 | 3 | 4 | 1 | High manual load; well-defined rules and windows. |
| **Fedwire** STP repair + screening | 4 | 5 | 4 | 2 | High-value, irrevocable, ISO 20022-mature — high risk, very buildable. |
| **Fedwire** intraday liquidity | 3 | 4 | 3 | 2 | Funding efficiency on the wholesale rail. |
| **RTP** real-time STP + screening | 3 | 5 | 3 | 2 | Instant + irrevocable, no review window — the real-time screening proof point. |
| **RTP** prefunding / liquidity | 3 | 4 | 3 | 2 | 24/7 prefunded settlement; liquidity automation. |
| **SWIFT** repair/STP, nostro recon, gpi | 4 | 4 | 3 | 3 | Cross-border volume and sanctions-heavy, but multi-hop and mid-migration (MT→MX). |
| **Stablecoin** on-chain recon, wallet screening, travel rule, custody | 2 | 5 | 2 | 3 | Lower volume today but irreversible, novel custody/key risk, evolving rules — **long-lead, start discovery now**. |

---

## 4. Delivery waves

- **Wave 0 — Foundation (F1–F5).** The screening spine, golden data, the hub, the exceptions desk, and reconciliation. Nothing automates safely until these exist.
- **Wave 1 — ACH (pilot).** Highest volume, most standardized, reversible. Proves the canonical lifecycle and the exceptions model on the safest, highest-cost-out rail.
- **Wave 2 — RTP + Fedwire.** The real-time domestic rails — instant and wholesale, both irrevocable. This is where **real-time screening at scale** (the crown capability) is proven and where the most risk is reduced.
- **Wave 3 — SWIFT + Stablecoin.** Cross-border complexity and on-chain novelty — the hardest and longest-lead, delivered last on a mature platform.

Indicative horizon: **~30 months** across the four waves, with waves overlapping once the foundation is stable **[calibrate]**.

---

## 5. Critical path — the screening spine

The chain that gates the highest-risk automation:

**F1 (sanctions/reference data) → F2 (shared screening) → real-time screening → RTP / Fedwire instant rails.**

Real-time screening on irrevocable rails is the single hardest, most gating capability — there is no hold-and-review window, so the screen must be both fast and accurate before any instant rail is automated. Everything on Wave 2 depends on this chain landing in Wave 0/early Wave 1. The secondary spine is **F3 (hub) → F5 (recon to settlement position)**, which gates settlement integrity on every rail.

---

## 6. Long-lead flag — stablecoin

Stablecoin scores lowest on feasibility and volume today but highest on risk, and it is the most novel (custody/key management, on-chain↔off-chain reconciliation, wallet screening, the Travel Rule, an evolving federal framework **[confirm]**). It delivers in Wave 3, but — exactly like collateral in the post-trade program — **its discovery should begin in Wave 1**, in parallel, so external dependencies (custody, on/off-ramp, node/infra, legal) are resolved before build.

---

## 7. Sequencing in one line

**Foundation first · ACH proves the model · RTP + Fedwire deliver the real-time screening value · SWIFT + stablecoin take the hardest cross-border and on-chain ground last.**

---

*Roadmap v0.1. Next in the arc: build requirements — starting with the Wave 0 foundation and the Wave 1 ACH rail.*
