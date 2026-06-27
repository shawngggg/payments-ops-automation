"""
Payments transaction analyzer — DETERMINISTIC RULES ENGINE (plain Python).
No AI model, no API key, no external service. Every decision below is an
explicit, inspectable rule. Reference lists are small ILLUSTRATIVE samples;
production replaces them with official OFAC/FATF data and real screening/AML systems.
"""
import csv

# --- illustrative reference data (production: official lists + vendor feeds) ---
WATCHLIST_NAMES     = {"ivan petrov", "global shell holdings", "red sea trading"}   # sample sanctioned parties
SANCTIONED_COUNTRY  = {"IR", "KP", "SY"}                                            # sample (illustrative only)
HIGH_RISK_COUNTRY   = {"NG", "AF", "YE"}                                            # sample (illustrative only)
BAD_WALLETS         = {"0xbadwallet01", "0xbadwallet02"}                            # sample flagged addresses
STRUCTURING_LO, STRUCTURING_HI = 9000.0, 9999.99                                   # just under CTR threshold
TRAVEL_RULE_THRESHOLD = 3000.0                                                      # [confirm]

# exception_type -> (escalation_path, recommended_solution)  [from the Exception Handling Matrix]
EXC = {
 "Sanctions hit (blocked)":   ("Screening L1 -> Sanctions officer -> block & OFAC report (<=10 bd)", "Golden sanctions data + tuned real-time screening (F1/F2)"),
 "Sanctions hit (cleared)":   ("Screening L1 clears (good-guy match)", "Tune matching / whitelist to cut false positives (F2)"),
 "AML alert":                 ("Investigator L1 -> Fin-crimes L2 -> SAR e-file FinCEN (30/60d) -> 90d review", "Behavioral tuning + case automation per rail (F6)"),
 "Format repair":             ("Repair queue L1 -> supervisor if aged", "ISO 20022 enrich + golden reference data (F1/F3)"),
 "Travel Rule incomplete":    ("Repair L1 -> compliance -> reject if non-compliant", "Enforce Travel Rule data at capture; auto-populate"),
 "Address risk review":       ("Crypto-ops -> compliance -> pre-send block; SAR if warranted", "Pre-send blockchain analytics + allow-listing"),
 "Return / NOC":              ("Auto-match L1 -> exceptions desk if unmatched", "Automated returns/NOC processing (A2)"),
 "":                          ("", ""),
}
STATUS = {"Sanctions hit (blocked)":"Blocked","Sanctions hit (cleared)":"Repaired","AML alert":"Investigated",
 "Format repair":"Repaired","Travel Rule incomplete":"Repaired","Address risk review":"Investigated",
 "Return / NOC":"Returned","":"STP"}

def analyze(tx):
    """Raw transaction dict -> enriched result dict. Rules applied in priority order."""
    amt = float(tx["amount_usd"])
    orig = tx["originator_name"].strip().lower()
    benef = tx["beneficiary_name"].strip().lower()
    ctry = tx["counterparty_country"].strip().upper()
    acct = tx["account_or_address"].strip()
    rail = tx["rail"]; direction = tx["direction"]
    screening = "Pass"; aml = "N"; sar = "N"; exc = ""

    # 1) Sanctions screening (blocking) — exact watchlist name match
    if orig in WATCHLIST_NAMES or benef in WATCHLIST_NAMES:
        screening, exc = "Hit-blocked", "Sanctions hit (blocked)"
    # 2) Sanctions screening — sanctioned jurisdiction (held, cleared after review here)
    elif ctry in SANCTIONED_COUNTRY:
        screening, exc = "Hit-cleared", "Sanctions hit (cleared)"
    # 3) AML monitoring — structuring, or high-risk jurisdiction + large value
    elif STRUCTURING_LO <= amt <= STRUCTURING_HI:
        aml, exc = "Y", "AML alert"                               # structuring -> alert (investigate; SAR only if substantiated)
    elif ctry in HIGH_RISK_COUNTRY and amt >= 1_000_000:
        aml, sar, exc = "Y", "Y", "AML alert"                     # high-risk + large -> alert + SAR
    # 4) Validation / repair — required fields missing
    elif benef == "" or acct == "":
        exc = "Format repair"
    # 5) Travel Rule completeness
    elif amt >= TRAVEL_RULE_THRESHOLD and tx["travel_rule_complete"].strip().upper() == "N":
        exc = "Travel Rule incomplete"
    # 6) Stablecoin wallet-address risk (pre-send)
    elif rail == "Stablecoin" and acct.lower() in BAD_WALLETS:
        exc = "Address risk review"
    # 7) ACH inbound return / NOC
    elif rail == "ACH" and direction == "Inbound" and tx.get("return_code","").strip():
        exc = "Return / NOC"
    # 8) else clean -> STP

    ep, rs = EXC[exc]
    out = dict(tx)
    out.update({"screening_result":screening, "aml_alert":aml, "sar_filed":sar,
                "exception_type":exc, "final_status":STATUS[exc],
                "escalation_path":ep, "recommended_solution":rs})
    return out

if __name__ == "__main__":
    raw = list(csv.DictReader(open("/home/claude/payments_raw_sample.csv")))
    enriched = [analyze(t) for t in raw]
    cols = list(raw[0].keys()) + ["screening_result","aml_alert","sar_filed","exception_type",
                                   "final_status","escalation_path","recommended_solution"]
    with open("/home/claude/payments_analyzed_sample.csv","w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(enriched)
    print(f"{'ID':4}{'RAIL':11}{'AMOUNT':>11}  {'CTRY':5}{'RESULT -> EXCEPTION TYPE':36}{'STATUS'}")
    for e in enriched:
        et = e["exception_type"] or "(clean)"
        print(f"{e['payment_id']:4}{e['rail']:11}{float(e['amount_usd']):>11,.0f}  {e['counterparty_country']:5}"
              f"{(e['screening_result']+' -> '+et):36}{e['final_status']}")
