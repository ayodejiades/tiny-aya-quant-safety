"""Record file size and bits per weight of every arm's GGUF to results/model_files.json (needs the GGUFs)."""
import json, pathlib, sys
from gguf import GGUFReader
FILES = {"f16": "official/tiny-aya-global-f16.gguf", "q8_0": "official/tiny-aya-global-q8_0.gguf", "q4_k_m": "official/tiny-aya-global-q4_k_m.gguf",
         "q4_0": "official/tiny-aya-global-q4_0.gguf", "Q3_K_S": "ours/tiny-aya-global-Q3_K_S.gguf", "Q2_K": "ours/tiny-aya-global-Q2_K.gguf",
         "F1": "ours/tiny-aya-global-Q3_K_S-protected.gguf", "F2": "ours/tiny-aya-global-Q3_K_S-decoy.gguf"}
out = {}
for a, f in FILES.items():
    p = pathlib.Path("models") / f; n = sum(int(t.n_elements) for t in GGUFReader(str(p)).tensors)
    out[a] = {"file": f, "bytes": p.stat().st_size, "tensor_elements": n, "bits_per_weight": round(p.stat().st_size * 8 / n, 2)}
json.dump(out, open("results/model_files.json", "w"), indent=1); print(out)
