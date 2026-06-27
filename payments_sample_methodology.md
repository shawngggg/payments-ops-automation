# Payments Sample — Generation Methodology & Data Dictionary

> How `payments_sample_transactions.csv` is produced, field by field. The dataset is **synthetic**: a generator encodes the operating model's rules with illustrative rates so the analytics and demo have realistic shape. The literal source is `generate_payments_dataset.py` (seed = 7, so the file is fully reproducible). **In production these fields are emitted by real systems**, not random draws — see §5.

---

## 1. Generation algorithm (per transaction)

For each of the 100,000 payments:

1. **Rail** is assigned by fixed share: ACH 45%, RTP 20%, SWIFT 18%, Fedwire 12%, stablecoin 5%.
2. **Date** is a random business day across a 20-day window (from 2026-05-18). Day 13 is a deliberate **spike day** — screening-hit rates run 1.5× — so trends and an all-time-high peak are visible.
3. **Time** is random within the rail's hours (RTP and stablecoin 00:00–23:59, i.e. 24/7; the others 09:30–20:50).
4. **Direction** is Outbound with a rail-specific probability, else Inbound.
5. **Amount** is drawn log-uniformly between the rail's min and max, so values span small to large the way real flow does.
6. **Currency / country**: SWIFT draws from a multi-currency and global-country set; the domestic rails are USD and mostly US counterparties.
7. **Exception outcome** is decided by a single random draw — see §3.
8. **Escalation path** and **recommended solution** are looked up from the resulting `exception_type` via the Exception Handling Matrix (§4).

---

## 2. Per-rail parameters (the rates that drive outcomes)

These are the illustrative probabilities each rail is generated with **[calibrate in Phase 0]**:

| Rail | Outbound | Screening hit | AML alert | Repair | Return (ACH) | Amount range (USD) |
|---|--:|--:|--:|--:|--:|---|
| ACH | 55% | 1.0% | 2.0% | 3.0% | 4.0% | 100 – 50,000 |
| RTP | 60% | 1.2% | 3.0% | 1.5% | — | 100 – 100,000 |
| SWIFT | 50% | 4.0% | 3.0% | 8.0% | — | 1,000 – 2,000,000 |
| Fedwire | 58% | 2.0% | 2.0% | 4.0% | — | 10,000 – 5,000,000 |
| Stablecoin | 55% | 5.0% | 3.5% | 2.0% | — | 1,000 – 500,000 |

The rates reflect the operating-model logic: SWIFT carries the highest repair and screening load (cross-border, multi-party); stablecoin the highest screening rate (address risk); RTP a higher AML rate (instant-rail / APP-fraud exposure).

---

## 3. Exception decision logic

A single uniform draw `r` in [0,1) is compared against cumulative bands built from the rail's rates `(hit, aml, repair, return)`:

```
if  r < hit (×1.5 on the spike day):     SCREENING HIT
        12% -> "Sanctions hit (blocked)"   screening_result = Hit-blocked,  final_status = Blocked
        88% -> "Sanctions hit (cleared)"   screening_result = Hit-cleared,  final_status = Repaired
elif r < hit + aml:                       AML ALERT
        aml_alert = Y,  final_status = Investigated
        18% -> sar_filed = Y
elif r < hit + aml + repair:              REPAIR
        SWIFT      -> one of {Format repair, Travel Rule incomplete, Investigation/non-receipt}
        Stablecoin -> 50% "Address risk review", else "Format repair"
        other      -> "Format repair"          final_status = Repaired
elif rail = ACH and r < hit+aml+repair+return:  "Return / NOC"   final_status = Returned
else:                                     CLEAN
        screening_result = Pass,  final_status = STP
```

`age_minutes` is then drawn from a branch-specific range (e.g. AML alerts 60–900 min, format repairs 8–240 min); STP rows have no age.

This is why the aggregates land where they do: ~9.7% exceptions, ~2,400 AML alerts, ~450 SARs (18% of alerts), ~220 sanctions blocks (12% of hits).

---

## 4. Escalation path & recommended solution

These two fields are **not random** — they are a deterministic lookup keyed on `exception_type`, using the mapping documented in `payments_exception_matrix.md`. Every row with a given exception type carries the same escalation path and recommended solution, which is what makes "group fails by type → see routing and fix" work directly in a dashboard.

---

## 5. Field derivation — data dictionary

| Column | How it is derived |
|---|---|
| `value_date` | Random business day in the 20-day window; day 13 is the spike. |
| `capture_time` | Random HH:MM within the rail's operating hours. |
| `payment_id` | Sequential identifier (P500000+). |
| `rail` | Assigned by fixed share (§1). |
| `direction` | Outbound with rail probability, else Inbound. |
| `amount_usd` | Log-uniform between the rail's min/max. |
| `currency` | SWIFT multi-currency; other rails USD. |
| `counterparty_country` | SWIFT global; other rails US 96% / global 4%. |
| `screening_result` | Pass / Hit-cleared / Hit-blocked — from the screening branch (§3). |
| `aml_alert` | Y when the AML branch fires. |
| `sar_filed` | Y for 18% of AML alerts. |
| `exception_type` | The branch outcome (one of eight types), or blank for STP. |
| `final_status` | STP / Blocked / Investigated / Repaired / Returned — mapped from the branch. |
| `age_minutes` | Branch-specific random range; blank for STP. |
| `desk` | Constant ("Payment operations"). |
| `escalation_path` | Lookup from `exception_type` (§4). |
| `recommended_solution` | Lookup from `exception_type` (§4). |

---

## 6. In production these fields are not synthetic

The generator stands in for real systems. In the built program, each field is emitted by the capability that owns it:

- `screening_result` → the **shared screening service (F2)**.
- `aml_alert`, `sar_filed` → **AML monitoring + SAR/FinCEN case management (F6)**.
- `exception_type`, `final_status`, `age_minutes` → the **exceptions & investigations platform (F4)**.
- `escalation_path`, `recommended_solution` → the **Exception Handling Matrix**, applied by F4 routing.

The sample reproduces the *shape* of that output — distributions, rates, and relationships — so the dashboard and demo are realistic before the real feeds exist.

---

*Methodology v0.1. Source: `generate_payments_dataset.py` (seed 7). All rates are illustrative and flagged for Phase-0 calibration.*
