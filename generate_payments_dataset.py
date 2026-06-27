import csv, random, datetime, math
random.seed(7)

RAILS = {
 "ACH":       (0.45, 0.55,   100,   50000, 0.010, 0.020, 0.030, 0.040),
 "RTP":       (0.20, 0.60,   100,  100000, 0.012, 0.030, 0.015, 0.000),
 "SWIFT":     (0.18, 0.50,  1000, 2000000, 0.040, 0.030, 0.080, 0.000),
 "Fedwire":   (0.12, 0.58, 10000, 5000000, 0.020, 0.020, 0.040, 0.000),
 "Stablecoin":(0.05, 0.55,  1000,  500000, 0.050, 0.035, 0.020, 0.000),
}
# exception_type -> (escalation_path, recommended_solution)
EXC = {
 "Sanctions hit (blocked)":   ("Screening L1 -> Sanctions officer -> block & OFAC report (<=10 bd)", "Golden sanctions data + tuned real-time screening (F1/F2)"),
 "Sanctions hit (cleared)":   ("Screening L1 clears (good-guy match)", "Tune matching / whitelist to cut false positives (F2)"),
 "AML alert":                 ("Investigator L1 -> Fin-crimes L2 -> SAR e-file FinCEN (30/60d) -> 90d review", "Behavioral tuning + case automation per rail (F6)"),
 "Format repair":             ("Repair queue L1 -> supervisor if aged", "ISO 20022 enrich + golden reference data (F1/F3)"),
 "Travel Rule incomplete":    ("Repair L1 -> compliance -> reject if non-compliant", "Enforce Travel Rule data at capture; auto-populate"),
 "Investigation/non-receipt": ("Investigations L1 -> correspondent L2 -> gpi trace", "gpi tracking + nostro reconciliation (F5)"),
 "Address risk review":       ("Crypto-ops -> compliance -> pre-send block; SAR if warranted", "Pre-send blockchain analytics + allow-listing"),
 "Return / NOC":              ("Auto-match L1 -> exceptions desk if unmatched", "Automated returns/NOC processing (A2)"),
}
CCY_SWIFT=["USD","EUR","GBP","JPY","CHF","CAD","SGD"]
CTRY_GLOBAL=["GB","DE","FR","JP","CH","CA","SG","AE","HK","BR","MX","IN"]
N=100000

def tdays(start,n):
    d=start;out=[]
    while len(out)<n:
        if d.weekday()<5: out.append(d)
        d+=datetime.timedelta(days=1)
    return out
DAYS=tdays(datetime.date(2026,5,18),20)

counts={r:int(round(N*cfg[0])) for r,cfg in RAILS.items()}
counts["ACH"]+=N-sum(counts.values())

rows=[]; pid=500000
for rail,cfg in RAILS.items():
    share,dout,lo,hi,shit,amlr,repr_,retr=cfg
    for _ in range(counts[rail]):
        di=random.randint(0,len(DAYS)-1); spike=(di==12); day=DAYS[di]
        cap=random.randint(0 if rail in("RTP","Stablecoin") else 9*60+30, 23*60+59 if rail in("RTP","Stablecoin") else 20*60+50)
        direction="Outbound" if random.random()<dout else "Inbound"
        amt=round(math.exp(random.uniform(math.log(lo),math.log(hi))),2)
        if rail=="SWIFT": ccy=random.choice(CCY_SWIFT); ctry=random.choice(CTRY_GLOBAL)
        else: ccy="USD"; ctry=random.choice(["US"] if random.random()<0.96 else CTRY_GLOBAL)
        sh=shit*(1.5 if spike else 1.0)
        screen="Pass"; exc=""; aml="N"; sar="N"; status="STP"; age=""
        r=random.random()
        if r<sh:
            if random.random()<0.12: screen="Hit-blocked"; exc="Sanctions hit (blocked)"; status="Blocked"; age=random.randint(30,400)
            else: screen="Hit-cleared"; exc="Sanctions hit (cleared)"; status="Repaired"; age=random.randint(10,180)
        elif r<sh+amlr:
            aml="Y"; exc="AML alert"; status="Investigated"; age=random.randint(60,900)
            if random.random()<0.18: sar="Y"
        elif r<sh+amlr+repr_:
            exc="Format repair" if rail!="SWIFT" else random.choice(["Format repair","Travel Rule incomplete","Investigation/non-receipt"])
            if rail=="Stablecoin" and random.random()<0.5: exc="Address risk review"
            status="Repaired"; age=random.randint(8,240)
        elif rail=="ACH" and r<sh+amlr+repr_+retr:
            exc="Return / NOC"; status="Returned"; age=random.randint(15,300)
        ep,rs = EXC.get(exc,("",""))
        rows.append([day.isoformat(), f"{cap//60:02d}:{cap%60:02d}", f"P{pid}", rail, direction,
                     amt, ccy, ctry, screen, aml, sar, exc, status, age, "Payment operations", ep, rs])
        pid+=1

random.shuffle(rows)
with open("/home/claude/payments_sample_transactions.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["value_date","capture_time","payment_id","rail","direction","amount_usd","currency",
        "counterparty_country","screening_result","aml_alert","sar_filed","exception_type","final_status",
        "age_minutes","desk","escalation_path","recommended_solution"])
    w.writerows(rows)

exc=sum(1 for r in rows if r[11]); blocked=sum(1 for r in rows if r[12]=="Blocked")
aml=sum(1 for r in rows if r[9]=="Y"); sar=sum(1 for r in rows if r[10]=="Y")
print(f"rows={len(rows):,}  exceptions={exc:,} ({exc/len(rows)*100:.1f}%)  blocked={blocked}  aml_alerts={aml:,}  sars={sar}")
from collections import Counter
for t,c in Counter(r[11] for r in rows if r[11]).most_common():
    print(f"  {t:28} {c:,}")
