# Payments Operations Automation — Stablecoin Rail: Discovery Specification

> **Discovery spec for the program's long-lead, most novel rail.** Stablecoin delivers in Wave 3 but its discovery should run in parallel with Wave 1, because it depends on net-new infrastructure (custody/keys, node access, blockchain analytics, on/off-ramps) and an unsettled regulatory framework. This document scopes the domain, sketches the target data model and workflows, maps the integration landscape, and frames the build-vs-buy-vs-partner decisions discovery must close.
> **Scope:** Bank payment operations (per `payments_scope.md`), US infrastructure. **[confirm]** = verify against current rule / vendor landscape; **[calibrate]** = Phase-0 figure.

---

## 1. Why stablecoin is long-lead

- It is the only rail requiring **net-new core infrastructure** — wallets, key management/custody, node/RPC access, and blockchain analytics — none of which exist for the other four rails.
- Transfers are **irreversible**: an operational error or a missed screen is a permanent loss, with no return window and no recall.
- It depends on **external partners** that gate timelines — a custody platform, an analytics provider, a Travel Rule solution, on/off-ramp and issuer relationships.
- The **regulatory framework is still forming** (federal stablecoin legislation, FinCEN treatment, state money-transmitter overlay), so the legal position must be established before build **[confirm]**.

Discovery exists to resolve all of this before committing to the build.

---

## 2. Scope

**In scope**
- On-chain **stablecoin payments** — origination (outbound) and receipt (inbound), wallet-to-wallet.
- **Wallet and key management / custody.**
- **On/off-ramp** (fiat ↔ stablecoin) and the link to the fiat rails (ACH/Fedwire).
- **On-chain ↔ off-chain reconciliation** and treasury/reserve management.
- **AML for crypto** — wallet/address analytics, the crypto Travel Rule, sanctioned-address screening.

**Out of scope**
- Proprietary crypto trading, DeFi yield, and non-stablecoin token activity.
- Issuing the bank's own stablecoin (a separate strategic decision; assume **use of established issuers** for now **[confirm]**).
- Retail crypto custody as a product (this is payment operations, not a wallet product).

---

## 3. Business capabilities

1. **Wallet & key management / custody** — generate and safeguard keys; segregation; approval controls.
2. **Address validation & screening** — validate destination; screen against sanctioned/risky addresses **pre-send**.
3. **On-chain execution** — construct, sign, and broadcast transactions; manage gas/fees; select chain.
4. **Finality confirmation** — track confirmations to the required depth before crediting.
5. **On/off-ramp** — fiat ↔ stablecoin conversion with source-of-funds checks.
6. **Reconciliation** — on-chain balances vs the book; reserve/treasury position.
7. **Blockchain analytics / AML** — wallet risk scoring, transaction tracing, typology detection.
8. **Travel Rule compliance** — exchange originator/beneficiary data VASP-to-VASP.
9. **Treasury / proof of reserves** — manage stablecoin inventory across wallets and chains.

---

## 4. Target data model (key entities)

| Entity | Key attributes | Notes |
|---|---|---|
| **Wallet** | Wallet ID, chain, addresses, custody arrangement, purpose | House vs client; hot vs cold |
| **Address** | Address, chain, risk score, screening status | Screened pre-use |
| **Key / custody record** | Custody model (MPC/HSM/multisig), approvers, policy | Never single-controlled |
| **On-chain transaction** | Tx hash, chain, token, from/to, amount, gas, confirmations, status | Mapped to the F3 canonical object |
| **Token / chain** | Token (e.g., USDC), issuer, chain, decimals | Eligibility-governed |
| **Counterparty VASP** | VASP identity, Travel Rule endpoint, due-diligence status | For VASP-to-VASP data exchange |
| **Ramp / conversion** | Fiat leg ref, rate, source-of-funds, partner | Links to ACH/Fedwire |
| **On-chain position** | Token, chain, wallet, balance | Reconciled to the book |
| **Reconciliation record** | On-chain vs book, break, status | Feeds F4/F5 |

---

## 5. Core workflows

### 5.1 Outbound on-chain payment
Validate destination address → **screen the address (pre-send)** and AML-score → check funding/inventory → construct and **sign** the transaction (custody approval) → **broadcast** → confirm **finality** to required depth → reconcile on-chain to book → advise. Because it is irreversible, every control is **pre-broadcast**.

### 5.2 Inbound
Detect incoming transfer → screen origin address → confirm finality → credit beneficiary → reconcile → Travel Rule data capture.

### 5.3 On/off-ramp
Fiat in (ACH/wire) → source-of-funds check → mint/convert to stablecoin; or stablecoin → convert → fiat out. Each leg reconciled and screened.

### 5.4 Travel Rule exchange
Identify the counterparty VASP → exchange required originator/beneficiary data at/above threshold **[confirm]** → record and retain.

### 5.5 Custody / key operations
Key generation, rotation, and signing under **multi-party approval**; hot/cold segregation; policy-enforced limits.

---

## 6. Integration landscape

| Counterparty / system | Purpose | Build / buy / partner |
|---|---|---|
| Blockchain nodes / RPC | Read chain state, broadcast tx | **Buy** (node-as-a-service) or run |
| Custody / key platform (MPC / HSM) | Safeguard keys, sign | **Decide in discovery** (custodian vs MPC vendor vs build) |
| Blockchain analytics (e.g., Chainalysis / Elliptic / TRM) **[confirm]** | Wallet screening, tracing, risk scoring | **Buy** |
| Travel Rule solution (e.g., TRUST / Notabene / others) **[confirm]** | VASP-to-VASP data exchange | **Buy / join network** |
| Stablecoin issuer / on-ramp (e.g., USDC issuer) **[confirm]** | Mint/redeem, fiat ramp | **Partner** |
| Payment hub (F3) | Canonical lifecycle | **Build** (adapter) |
| Screening (F2) / AML (F6) | Sanctions + monitoring | **Reuse** foundation |
| Reconciliation (F5) | On-chain ↔ off-chain | **Build** |
| Reference data (F1) | Tokens, chains, VASPs, address lists | **Reuse** foundation |
| Treasury | Inventory / reserves | Interface |

---

## 7. Regulatory & control considerations

- **Federal stablecoin framework** (recent legislation) and **FinCEN** treatment of CVC as funds transmission **[confirm]**; possible **state money-transmitter** overlay **[confirm]**.
- **Crypto Travel Rule** — FATF Rec. 16 / FinCEN; VASP-to-VASP originator/beneficiary data at/above threshold **[confirm threshold]**.
- **OFAC** — sanctioned wallet addresses are blocked property; screen pre-send, **block and report** **[confirm timing]**.
- **Custody / safeguarding** — key segregation, multi-party approval, hot/cold separation; auditability.
- **Proof of reserves / treasury** — evidence of backing and inventory.
- **Irreversibility safeguards** — pre-broadcast four-eyes on value thresholds; address allow-listing.

---

## 8. Build vs buy vs partner (the decisions discovery must close)

| Component | Options | Indicative direction |
|---|---|---|
| **Custody / keys** | Qualified custodian · MPC vendor · build in-house | **Decide carefully** — most likely a qualified custodian or MPC vendor, not in-house |
| **Blockchain analytics** | Vendor (Chainalysis/Elliptic/TRM) | **Buy** — commoditized, deep coverage |
| **Travel Rule** | Join a network/solution | **Buy / join** — interoperability with counterparties matters |
| **Node / chain access** | Node-as-a-service vs self-run | **Buy** initially; revisit at scale |
| **Stablecoin / issuer** | Use established issuer(s) vs issue own | **Use established** — issuing own is a separate strategy |
| **Orchestration / recon / controls** | Build | **Build** — the differentiating layer tying to the payment hub, screening, AML, and the book |

**Recommendation (to confirm in discovery):** buy/partner the commoditized stack (analytics, Travel Rule, nodes, issuer), make a deliberate **custody** decision, and **build only** the orchestration, reconciliation, and control layer that integrates stablecoin into the same exception-based, screened, reconciled operating model as the other rails.

---

## 9. Discovery work plan & deliverables

1. **Use-case definition** — which flow first (cross-border B2B settlement, internal treasury movement, or client payments) **[confirm]**.
2. **Chain & stablecoin selection** — which chain(s) and issuer(s), with eligibility criteria.
3. **Custody decision** — custodian vs MPC vs build, with controls and cost.
4. **Vendor RFIs** — analytics, Travel Rule, node infrastructure, ramp/issuer.
5. **Regulatory/legal position** — federal + state, Travel Rule, OFAC, custody **[confirm]**.
6. **Reconciliation design** — on-chain ↔ off-chain and reserves.
7. **Target architecture & build-vs-buy recommendation** — with cost and timeline.

---

## 10. Open questions

- Which use case leads — cross-border settlement, treasury, or client payments?
- Which chain(s) and which stablecoin(s), and on what eligibility basis?
- Custody: qualified custodian, MPC vendor, or build — and what approval model?
- What is the firm's regulatory posture given the still-forming framework?
- Who are the expected counterparty VASPs, and are they reachable on a common Travel Rule network?

---

## 11. Risks specific to stablecoin

- **Irreversibility** — operational error or missed screen = permanent loss; demands pre-broadcast controls.
- **Key / custody compromise** — catastrophic; mandates multi-party, segregated custody.
- **Sanctioned-address exposure** — receiving from or sending to a listed address; pre-send analytics is the control.
- **Regulatory uncertainty** — the framework is still forming; the legal position can shift mid-build **[confirm]**.
- **Finality / reorg** — crediting before sufficient confirmations.
- **Concentration** — dependence on a single chain, issuer, or vendor.

---

## 12. Discovery exit criteria

Discovery is complete when: the lead use case is chosen; chain(s) and stablecoin(s) are selected; the **custody model is decided**; analytics and Travel Rule vendors are selected; the **regulatory/legal position is confirmed**; the on-chain↔off-chain reconciliation design is agreed; and a target architecture with build-vs-buy, cost, and timeline is ready to enter detailed requirements and build.

---

*Stablecoin Discovery Specification, v0.1. Feeds the Wave 3 build (requirements SC1/SC2 in Part 3); begin discovery in parallel with Wave 1.*
