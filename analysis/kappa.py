"""Judge agreement: Cohen's kappa for RefusalDetector vs human_refused and Llama Guard vs human_harmful.
Writes claims only once all 60 rows of labels/to_label.csv are filled with 0 or 1."""
import csv, json, sys
sys.path.insert(0, "/Users/nifemi/researchops")
from rops.stats import claim, write_claims, cohen_kappa

rows = list(csv.DictReader(open("labels/to_label.csv"))); key = json.load(open("labels/key.json"))
if not rows or any(r["human_refused"].strip() not in ("0", "1") or r["human_harmful"].strip() not in ("0", "1") for r in rows):
    print("labels incomplete; no claims written"); sys.exit(0)
det, hum_r, gd, hum_h = [], [], [], []
for r in rows:
    k = key[r["row"]]; rec = next(x for x in map(json.loads, open(f"runs/{k['arm']}/{k['set']}.test.jsonl")) if x["id"] == k["id"])
    det.append(int(rec["refused"])); hum_r.append(int(r["human_refused"]))
    if "guard_unsafe" in rec: gd.append(int(rec["guard_unsafe"])); hum_h.append(int(r["human_harmful"]))
C = []
kr = cohen_kappa(det, hum_r); C.append(claim("judge.agreement.refusal_kappa", round(kr, 2), n=len(det), text="Cohen's kappa, keyword RefusalDetector vs human refusal labels", abstract=True))
C.append(claim("judge.agreement.refusal_percent", round(100 * sum(a == b for a, b in zip(det, hum_r)) / len(det), 1), n=len(det), text="raw agreement (%), RefusalDetector vs human refusal labels"))
if gd:
    kg = cohen_kappa(gd, hum_h); C.append(claim("judge.agreement.guard_kappa", round(kg, 2), n=len(gd), text="Cohen's kappa, Llama Guard vs human harmful labels (harmful-set rows only)", abstract=True))
    C.append(claim("judge.agreement.guard_percent", round(100 * sum(a == b for a, b in zip(gd, hum_h)) / len(gd), 1), n=len(gd), text="raw agreement (%), Llama Guard vs human harmful labels"))
write_claims("results/claims.partial/judge.json", C); print(len(C), "claims", kr)
