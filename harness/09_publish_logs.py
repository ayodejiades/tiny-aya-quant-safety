"""Build the sanitised logs dataset in hf/logs_build and upload it. Responses with guard_unsafe == true, and any
unjudged response to a harmful/wrapped prompt (dev split), are published as the first 200 characters plus sha256."""
import hashlib, json, pathlib, shutil
from huggingface_hub import HfApi
SRC, DST = pathlib.Path("runs"), pathlib.Path("hf/logs_build"); shutil.rmtree(DST, ignore_errors=True)
risky_sets = ("harmful", "wrapped", "xs_unsafe")
n_trunc = n_all = 0
for f in sorted(SRC.glob("*/*.jsonl")):
    arm, name = f.parent.name, f.name; setname = name.split(".")[0]
    out = DST / "runs" / arm; out.mkdir(parents=True, exist_ok=True)
    with open(out / name, "w") as g:
        for line in open(f):
            r = json.loads(line); n_all += 1
            if r.get("guard_unsafe") or (setname in risky_sets and "guard_unsafe" not in r):
                full = r["output"]; r["output_sha256"] = hashlib.sha256(full.encode()).hexdigest()
                r["output"] = full[:200]; r["output_truncated_to_200_chars"] = True; n_trunc += 1
            g.write(json.dumps(r, ensure_ascii=False) + "\n")
for p in ("results/claims.json", "results/sweep.json", "results/model_files.json", "runs/pilot.json", "runs/rendered_prompt.txt"):
    d = DST / pathlib.Path(p).parent; d.mkdir(parents=True, exist_ok=True); shutil.copy(p, d / pathlib.Path(p).name)
shutil.copy("hf/logs/README.md", DST / "README.md")
print("rows", n_all, "truncated", n_trunc)
HfApi().upload_folder(folder_path=str(DST), repo_id="ayodejiades/tiny-aya-quant-safety-logs", repo_type="dataset")
print("uploaded")
