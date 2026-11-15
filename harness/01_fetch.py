"""Fetch raw prompt sources to data/raw/*.jsonl."""
import json, pathlib
from datasets import load_dataset

RAW = pathlib.Path("data/raw"); RAW.mkdir(parents=True, exist_ok=True)

def dump(name, rows):
    with open(RAW / f"{name}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(name, len(rows))

jbb = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")
for split in ("harmful", "benign"):
    dump(f"jbb_{split}", [
        {"src_id": f"jbb_{split}_{r['Index']}", "instruction": r["Goal"], "output": r["Category"],
         "source": f"jbb_{split}"} for r in jbb[split]])

xs = load_dataset("Paul/XSTest")["train"]
for lab in ("safe", "unsafe"):
    dump(f"xs_{lab}", [
        {"src_id": f"xs_{lab}_{r['id']}", "instruction": r["prompt"], "output": r["type"],
         "source": f"xs_{lab}"} for r in xs if r["label"] == lab])

arc = load_dataset("allenai/ai2_arc", "ARC-Easy")["test"]
rows = []
for r in arc:
    opts = "\n".join(f"{l}. {t}" for l, t in zip(r["choices"]["label"], r["choices"]["text"]))
    rows.append({"src_id": f"arc_{r['id']}", "instruction": f"{r['question']}\n{opts}\nAnswer with the letter only.",
                 "output": r["answerKey"], "source": "arc_easy"})
dump("arc_easy", rows)
