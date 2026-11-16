"""Main metrics, paired tests and claims. Test split, direct prompts = JBB harmful (70) + JBB benign (69). Deterministic."""
import json, math, sys, pathlib
sys.path.insert(0, "/Users/nifemi/researchops")
from rops.stats import claim, write_claims, wilson_ci, holm

ARMS = ["f16", "q8_0", "q4_k_m", "q4_0", "Q3_K_S", "Q2_K", "F1", "F2"]
MF = json.load(open("results/model_files.json"))

def load(arm, s): return {r["id"]: r for r in map(json.loads, open(f"runs/{arm}/{s}.test.jsonl"))}
D = {a: {s: load(a, s) for s in ("harmful", "benign", "wrapped", "capability")} for a in ARMS}
direct_ids = [("harmful", i) for i in D["f16"]["harmful"]] + [("benign", i) for i in D["f16"]["benign"]]

def mcnemar(b, c):
    n = b + c
    if n == 0: return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)

C = []
def rate(id_, k, n, text, abstract=False, scale=100):
    p, lo, hi = wilson_ci(k, n)
    C.append(claim(id_, round(scale * p, 1), ci=[round(scale * lo, 1), round(scale * hi, 1)], n=n, text=text, abstract=abstract))
def val(id_, v, text, n=None, abstract=False): C.append(claim(id_, v, n=n, text=text, abstract=abstract))

flip = {}; net = {}
for a in ARMS:
    d = D[a]; r = d["harmful"]
    rate(f"{a}.harmful_refusal", sum(x["refused"] for x in r.values()), len(r), f"{a} refusal rate on JBB harmful test prompts (%)", abstract=a in ("f16", "q4_k_m", "Q3_K_S", "F1"))
    rate(f"{a}.overrefusal", sum(x["refused"] for x in d["benign"].values()), len(d["benign"]), f"{a} refusal rate on JBB benign test prompts, over-refusal (%)")
    rate(f"{a}.wrapped_refusal", sum(x["refused"] for x in d["wrapped"].values()), len(d["wrapped"]), f"{a} refusal rate on wrapper W1 prompts (%)")
    rate(f"{a}.asr_harmful", sum(x["guard_unsafe"] for x in r.values()), len(r), f"{a} Llama Guard attack success rate on harmful prompts (%)")
    rate(f"{a}.asr_wrapped", sum(x["guard_unsafe"] for x in d["wrapped"].values()), len(d["wrapped"]), f"{a} Llama Guard attack success rate on wrapped prompts (%)", abstract=a in ("f16", "q4_k_m", "Q3_K_S", "F1"))
    cap = d["capability"]; rate(f"{a}.capability", sum(x["correct"] for x in cap.values()), len(cap), f"{a} ARC-Easy accuracy (%)")
    for s in ("harmful", "benign", "wrapped"):
        rate(f"{a}.truncation_{s}", sum(x["finish_reason"] == "length" for x in d[s].values()), len(d[s]), f"{a} share of {s} responses hitting the 128-token cap (%)")
    f = sum(d[s][i]["refused"] != D["f16"][s][i]["refused"] for s, i in direct_ids)
    flip[a] = f; rate(f"{a}.flip_rate", f, len(direct_ids), f"{a} share of direct test prompts whose refusal label differs from f16 (%)", abstract=a in ("q4_k_m", "Q3_K_S", "F1"))
    kref = sum(d[s][i]["refused"] for s, i in direct_ids); kf16 = sum(D["f16"][s][i]["refused"] for s, i in direct_ids)
    net[a] = (kref - kf16) / len(direct_ids)
    val(f"{a}.net_change_points", round(100 * net[a], 1), f"{a} net change in refusal rate on direct prompts versus f16 (points)", n=len(direct_ids))
    toks = sum(x["tokens"] for s in D[a] for x in D[a][s].values()); secs = sum(x["seconds"] for s in D[a] for x in D[a][s].values())
    val(f"{a}.tokens_per_second", round(toks / secs, 1), f"{a} aggregate tokens per second, 4 requests in flight, M1")
    sz = MF[a]["bytes"]
    val(f"{a}.size_mb", round(sz / 1e6), f"{a} file size (MB)")

# bits per weight (from results/model_files.json, written by harness/08_model_files.py)
for a in ARMS:
    val(f"{a}.bits_per_weight", MF[a]["bits_per_weight"], f"{a} bits per weight (file bits over tensor elements)")

# paired tests vs f16: harmful refusal (H1) and all direct prompts, Holm across the 7 non-reference arms
others = [a for a in ARMS if a != "f16"]
for name, ids in (("harmful", [("harmful", i) for i in D["f16"]["harmful"]]), ("direct", direct_ids)):
    ps = []
    for a in others:
        b = sum(D[a][s][i]["refused"] and not D["f16"][s][i]["refused"] for s, i in ids)
        c = sum((not D[a][s][i]["refused"]) and D["f16"][s][i]["refused"] for s, i in ids)
        ps.append(mcnemar(b, c))
        val(f"{a}.vs_f16.{name}.discordant_more_refusal", b, f"{a} refuses where f16 does not, {name} prompts", n=len(ids))
        val(f"{a}.vs_f16.{name}.discordant_less_refusal", c, f"f16 refuses where {a} does not, {name} prompts", n=len(ids))
    for a, p, ph in zip(others, ps, holm(ps)):
        val(f"{a}.vs_f16.{name}.p_mcnemar", round(p, 4), f"exact McNemar p, {a} vs f16, {name} prompts")
        val(f"{a}.vs_f16.{name}.p_holm", round(ph, 4), f"Holm-adjusted p, {a} vs f16, {name} prompts")

# repair tests: label equals f16, paired over the direct prompts
def match(a): return {k: D[a][k[0]][k[1]]["refused"] == D["f16"][k[0]][k[1]]["refused"] for k in direct_ids}
def paired_match(x, y, tag):
    mx, my = match(x), match(y)
    b = sum(mx[k] and not my[k] for k in direct_ids); c = sum(my[k] and not mx[k] for k in direct_ids)
    val(f"repair.{tag}.only_first_matches", b, f"prompts where {x} matches f16 and {y} does not", n=len(direct_ids))
    val(f"repair.{tag}.only_second_matches", c, f"prompts where {y} matches f16 and {x} does not", n=len(direct_ids))
    val(f"repair.{tag}.p_mcnemar", round(mcnemar(b, c), 4), f"exact McNemar p, {x} vs {y}, label equals f16")
paired_match("F1", "Q3_K_S", "F1_vs_Q3_K_S"); paired_match("F1", "F2", "F1_vs_F2")
dcap = 100 * (sum(x["correct"] for x in D["F1"]["capability"].values()) - sum(x["correct"] for x in D["Q3_K_S"]["capability"].values())) / 150
val("repair.F1_minus_Q3_K_S.capability_points", round(dcap, 1), "F1 ARC-Easy accuracy minus Q3_K_S (points)", n=150)

# H2 ordering
order = ["q8_0", "q4_k_m", "q4_0", "Q3_K_S", "Q2_K"]
ok_order = flip["q8_0"] < flip["q4_k_m"] <= flip["q4_0"] < flip["Q3_K_S"] < flip["Q2_K"]
val("h2.order_holds", int(ok_order), "1 if flip rates are ordered q8_0 < q4_k_m <= q4_0 < Q3_K_S < Q2_K")
val("h2.arms_flip_exceeds_net", sum(flip[a] / len(direct_ids) > abs(net[a]) for a in order), "number of the five uniform arms whose flip rate exceeds the absolute net change in refusal rate", n=5)
write_claims("results/claims.partial/main.json", C); print(len(C), "claims; flips:", flip, "order", ok_order)
