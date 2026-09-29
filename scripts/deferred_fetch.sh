#!/usr/bin/env bash
# Deferred OpenAlex fetch runner: waits for daily-budget reset (UTC midnight + 10 min),
# then runs funnel + field-intensity fetches at low rate. If the budget is exhausted
# again mid-run, sleeps until the next reset and resumes (scripts skip done keys).
cd "$(dirname "$0")/.." || exit 1
LOG=data/raw/deferred_fetch.log
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }

wait_for_budget(){
  while :; do
    code=$(python3 -c "
import requests
try:
    r=requests.get('https://api.openalex.org/works',params={'per-page':1,'mailto':'devin-research@cognition.ai'},timeout=30)
    print(r.status_code)
except Exception:
    print(0)")
    if [ "$code" = "200" ]; then return 0; fi
    say "budget check -> $code; sleeping 600s"
    sleep 600
  done
}

say "runner started; waiting for budget"
wait_for_budget
say "budget available; starting field-intensity fetch"
python3 scripts/fetch_field_intensity.py >> data/raw/field_intensity.log 2>&1
say "field-intensity done/exit; re-checking budget before funnel"
wait_for_budget
say "starting funnel fetch"
python3 scripts/fetch_openalex_funnel.py >> data/raw/openalex_funnel.log 2>&1
say "funnel done/exit; verifying coverage"
python3 - <<'EOF' >> "$LOG"
import glob,gzip,json
ok=0; cs=set()
for p in glob.glob("data/raw/openalex_funnel/*.json.gz"):
    b=json.load(gzip.open(p)); ok+=len(b["queries"]); cs.add(b["country"])
print("queries saved:",ok,"countries:",len(cs))
EOF
say "runner finished"
