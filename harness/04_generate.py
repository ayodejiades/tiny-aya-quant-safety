"""Generate responses for one arm through AuditKIT. Expects llama-server for that arm on :8080.
Appends one JSON line per item to runs/<arm>/<set>.<split>.jsonl and skips ids already present.

finish_reason / tokens are not exposed by ak.evaluate, so they are derived from the server's
/tokenize endpoint on the returned text (see DEVIATIONS.md D3). `seconds` is the chunk wall time
divided by chunk size (amortised, 4 requests in flight)."""
import argparse, json, pathlib, re, time, urllib.request, warnings
warnings.filterwarnings("ignore")
import auditkit as ak
from auditkit import RunConfig
from auditkit.redteam.detectors.builtin import RefusalDetector

BASE = "http://127.0.0.1:8080"
MAX_TOKENS = 128
CHUNK = 20
det = RefusalDetector()

def tokenize_len(text):
    req = urllib.request.Request(f"{BASE}/tokenize", data=json.dumps({"content": text, "add_special": False}).encode(),
                                 headers={"Content-Type": "application/json"})
    return len(json.loads(urllib.request.urlopen(req, timeout=60).read())["tokens"])

def letter(out):
    m = re.search(r"\b([A-E])\b", out.upper())
    return m.group(1) if m else None

def run(arm, sets, split, limit=None):
    for name in sets:
        path = pathlib.Path(f"data/sets/{name}.{split}.jsonl")
        if not path.exists():
            print(f"[{arm}] no {path}, skipping"); continue
        items = [json.loads(l) for l in open(path)]
        if limit: items = items[:limit]
        outp = pathlib.Path(f"runs/{arm}/{name}.{split}.jsonl"); outp.parent.mkdir(parents=True, exist_ok=True)
        done = {json.loads(l)["id"] for l in open(outp)} if outp.exists() else set()
        pending = [it for it in items if it["id"] not in done]
        print(f"[{arm}] {name}.{split}: {len(done)} done, {len(pending)} to do", flush=True)
        for i in range(0, len(pending), CHUNK):
            chunk = pending[i:i + CHUNK]
            samples = [ak.Sample(input=it["prompt"], target="") for it in chunk]
            t0 = time.time()
            res = ak.evaluate(samples, model="api:tiny-aya", api_base=f"{BASE}/v1", api_key="EMPTY",
                              config=RunConfig(concurrency=4, max_tokens=MAX_TOKENS, temperature=0.0), cache=False)
            dt = time.time() - t0
            preds = {str(p.sample_id): p.raw_output for p in res.predictions}
            with open(outp, "a") as f:
                for j, it in enumerate(chunk):
                    out = preds.get(str(j))
                    if out is None: raise RuntimeError(f"missing prediction {j} in {name}")
                    ntok = tokenize_len(out) if out else 0
                    row = {"id": it["id"], "prompt": it["prompt"], "output": out,
                           "finish_reason": "length" if ntok >= MAX_TOKENS else "stop",
                           "refused": bool(det.detect(it["prompt"], out).detected),
                           "tokens": ntok, "seconds": dt / len(chunk)}
                    if "key" in it:
                        row["key"] = it["key"]; row["pred"] = letter(out); row["correct"] = letter(out) == it["key"]
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"[{arm}] {name}.{split}: {min(i + CHUNK, len(pending))}/{len(pending)}  {dt:.1f}s", flush=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    ap.add_argument("--sets", nargs="+", required=True)
    ap.add_argument("--split", default="test")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    run(a.arm, a.sets, a.split, a.limit)
