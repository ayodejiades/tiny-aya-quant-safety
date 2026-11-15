"""Write labels/to_label.csv: 60 rows (30 harmful, 30 benign), arms f16 / q4_k_m / Q3_K_S in rotation, shuffled, arm hidden."""
import csv, json, random, pathlib
rng = random.Random(20261115); arms = ["f16", "q4_k_m", "Q3_K_S"]
pathlib.Path("labels").mkdir(exist_ok=True); rows = []
for s in ("harmful", "benign"):
    ids = [json.loads(l)["id"] for l in open(f"data/sets/{s}.test.jsonl")]
    pick = rng.sample(ids, 30)
    for k, i in enumerate(pick):
        arm = arms[k % 3]
        r = next(json.loads(l) for l in open(f"runs/{arm}/{s}.test.jsonl") if json.loads(l)["id"] == i)
        rows.append({"set": s, "arm": arm, "id": i, "prompt": r["prompt"], "response": r["output"]})
rng.shuffle(rows)
with open("labels/to_label.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["row", "prompt", "response", "human_refused", "human_harmful"])
    for n, r in enumerate(rows, 1): w.writerow([n, r["prompt"], r["response"], "", ""])
json.dump({str(n): {k: r[k] for k in ("set", "arm", "id")} for n, r in enumerate(rows, 1)}, open("labels/key.json", "w"), indent=1)
print(len(rows), "rows")
