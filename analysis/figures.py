import json, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
C = {c["id"]: c for c in json.load(open("results/claims.partial/main.json"))}
arms = ["q8_0", "q4_k_m", "q4_0", "Q3_K_S", "Q2_K", "F1", "F2", "f16"]
fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharex=True)
for a in arms:
    x = C[f"{a}.bits_per_weight"]["value"]
    inter = a in ("F1", "F2"); mk = "*" if inter else "o"; col = "tab:red" if a == "F1" else ("tab:gray" if a == "F2" else "tab:blue")
    fl = C[f"{a}.flip_rate"]; hr = C[f"{a}.harmful_refusal"]
    ax[0].errorbar(x, fl["value"], yerr=[[fl["value"] - fl["ci"][0]], [fl["ci"][1] - fl["value"]]], fmt=mk, color=col, ms=11 if inter else 6, capsize=3)
    ax[1].errorbar(x, hr["value"], yerr=[[hr["value"] - hr["ci"][0]], [hr["ci"][1] - hr["value"]]], fmt=mk, color=col, ms=11 if inter else 6, capsize=3)
    for k in (0, 1): ax[k].annotate(a, (x, (fl if k == 0 else hr)["value"]), textcoords="offset points", xytext=(5, 6), fontsize=8)
ax[0].set_ylabel("flip rate vs f16 (% of 139 direct prompts)"); ax[1].set_ylabel("harmful refusal rate (% of 70, JBB)")
for k in (0, 1): ax[k].set_xlabel("bits per weight"); ax[k].grid(alpha=.3)
fig.suptitle("Tiny Aya Global: refusal behaviour against precision (F1 red star, F2 grey star; bars are Wilson 95% intervals)", fontsize=9)
fig.tight_layout(); fig.savefig("figures/precision_curve.png", dpi=150)
