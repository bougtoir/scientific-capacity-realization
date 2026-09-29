#!/usr/bin/env python3
"""Fetch OECD MSTI series for all candidate countries (SDMX-CSV), persist raw + ledger."""
import requests, os, csv, hashlib, datetime, time

RAW = "data/raw/oecd"
os.makedirs(RAW, exist_ok=True)
LED = "data/raw/ACQUISITION_LEDGER.csv"
CC = """jpn kor gbr deu fra ita esp nld swe che aut bel dnk fin irl nor prt pol cze grc hun svk
can usa aus nzl isr chn ind bra zaf rus irn egy arg chl tha mys idn sau twn hkg sgp pak nga mex tur ukr
rou bgr hrv svn est lva ltu lux isl mlt cyp""".split()
MEASURES = ["H", "G", "GV", "C", "C_GUF", "T_RS", "H_RS", "PI", "PPP", "GDP", "TOT_POP"]

for cc in CC:
    for m in MEASURES:
        url = f"https://sdmx.oecd.org/public/rest/v1/data/OECD.STI.STP,DSD_MSTI@DF_MSTI/{cc.upper()}.A.{m}....?startPeriod=1995&dimensionAtObservation=AllDimensions"
        p = f"{RAW}/msti_{cc}_{m}.csv"
        if os.path.exists(p) and os.path.getsize(p) > 300:
            continue
        ok = False
        for a in range(4):
            try:
                r = requests.get(url, headers={"Accept": "text/csv"}, timeout=(10, 45))
                ok = True
                break
            except Exception as e:
                print("retry", cc, m, type(e).__name__, flush=True)
            time.sleep(2 ** a + 1)
        if not ok or r.status_code != 200:
            print("FAIL", cc, m, r.status_code if ok else "no-conn", flush=True)
            continue
        open(p, "wb").write(r.content)
        b = open(p, "rb").read()
        with open(LED, "a") as f:
            csv.writer(f).writerow([p, len(b), hashlib.sha256(b).hexdigest()[:16], url,
                                    datetime.datetime.now(datetime.timezone.utc).isoformat(), "MSTI"])
        print(cc, m, len(b), flush=True)
        time.sleep(0.2)
print("DONE")
