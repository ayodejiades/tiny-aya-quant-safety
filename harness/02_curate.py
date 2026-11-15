"""Pool raw prompts, run CuratorKIT (minhash dedup + clean), then build dev/test sets.
Toxicity / PII / guard gates are NOT enabled: they would delete the harmful test items."""
import json, pathlib, random, shutil, collections
from curatorkit import Curator, CuratorConfig

RAW = pathlib.Path("data/raw"); OUT = pathlib.Path("data/curated"); SETS = pathlib.Path("data/sets")
SEED = 20261115
SETS.mkdir(parents=True, exist_ok=True)

# Pool prompt sets (not ARC: multiple choice items are not subject to prompt dedup against safety prompts)
pool = RAW / "pool.jsonl"
n_in = 0
with open(pool, "w") as f:
    for name in ("jbb_harmful", "jbb_benign", "xs_safe", "xs_unsafe"):
        for line in open(RAW / f"{name}.jsonl"):
            f.write(line); n_in += 1

# min_tokens lowered from default 10: several XSTest prompts are shorter than 10 tokens.
cfg = CuratorConfig(dataset=str(pool), dedup="minhash", clean=True, min_tokens=1,
                    output_dir=str(OUT), name="lexsi_prompts", export_formats=["alpaca"],
                    toxicity_gate=False, guard_gate=False, pii_pseudonymize=False, secrets_gate=False)
res = Curator(cfg).run()
print("CuratorKIT result:", res)
