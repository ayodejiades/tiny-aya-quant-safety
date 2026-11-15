# Deviations

## D1: benign test set has 69 items, not 70
CuratorKIT's MinHash near-duplicate dedup (threshold 0.85) removed one of the 100 JBB benign prompts
before the split, so `benign.test` has 69 items (dev is 30). Counts before and after are in
`data/sets/summary.json`. The design is otherwise unchanged. The 340 direct test prompts of the
guide are therefore 339.

## D2: CuratorKIT `min_tokens` lowered from 10 to 1
Several XSTest prompts are shorter than the default 10-token minimum. The default would have removed
valid items. Nothing else in the CuratorKIT config differs from the guide (dedup="minhash", clean=True,
no toxicity, PII or guard gates).

## D3: finish_reason and token counts are derived, not read from the response
`ak.evaluate` returns predictions without `finish_reason` or usage. Token counts are taken by sending the
returned text to the server's `/tokenize` endpoint; `finish_reason` is recorded as `length` when that count
is at least 128 (the `-n` cap), else `stop`. Retokenising can differ from the generated count by a token at
the boundary, so the truncation rate is approximate. `seconds` is chunk wall time divided by chunk size
(20 items, 4 in flight), so tokens/second is an aggregate rate per arm, not a per-request latency.

## D4 (note, not a design change): the GGUF chat template adds a default system preamble
With `--jinja` and no system message of our own, the rendered prompt (`runs/rendered_prompt.txt`) starts with
Cohere's built-in "contextual safety mode" system preamble. It is identical for every arm, so comparisons
are unaffected, but absolute refusal rates describe the model with this default preamble, not a bare prompt.

## D5: speed rule triggered; cuts 1, 3 and 4 applied (20:35 WAT, 15 Nov)
Measured aggregate speed at 4 requests in flight: f16 5.3 tok/s, Q2_K 13.4, q4_k_m 15.4 (`runs/pilot.json`).
Estimated essential overnight work with all sets was about 10 h, over the 7 h limit. Following the guide:
- **Cut 1:** wrapper W2 dropped; `wrapped` has 70 items (W1 only). The full 140-item file is kept in `data/sets/full/`.
- **Cut 3:** the sweep uses 3 blocks of 12 layers (B0 = 0-11, B1 = 12-23, B2 = 24-35) instead of 6 blocks of 6.
  F1 and F2 therefore protect 12 layers, not 6; "one block of six consecutive layers" in PREREG becomes twelve.
- **Cut 4:** XSTest items dropped (`xs_unsafe`, `xs_safe`, 100 each; files kept in `data/sets/full/`). The
  preregistered primary metric (harmful test, JBB + XSTest, n = 170) becomes JBB harmful test only (n = 70),
  and the flip rate is over the 139 direct JBB test prompts (70 harmful + 69 benign), not 339.
All these cuts reduce statistical power. If the overnight run ends early, XSTest may be added back for the
four essential arms and reported as an addition.

## D6: Llama Guard is called with the official response-classification prompt, not Ollama's chat template
The guide's smoke test failed with the `/api/chat` call: Ollama's `llama-guard3:8b` template ends with
"assessment for ONLY THE LAST User message", so it grades the prompt and returned `unsafe` for a plain refusal to a
pipe-bomb request and for a defamation refusal. `harness/05_judge.py` instead sends Meta's published Llama Guard 3
response-classification prompt ("ONLY THE LAST Agent message") to `/api/generate` with `raw: true`, same model,
temperature 0. Smoke test after the change: 2 refusals and 1 harmless answer `safe`, 2 compliant harmful answers
`unsafe`. The judge is still Llama Guard 3 8B through Ollama.

## D7: git history rewritten before the first push (15 Nov, ~20:45 WAT)
The author and committer address on the early commits was the author's personal email, which a public push
would have exposed. All commits and both annotated tags were rewritten to the GitHub noreply address; file
contents and commit order are unchanged, so every commit hash changed. The freeze commit recorded in
`.rops/prereg.json` as `3f61031eb16ac044753a95d3964b4cf3f14febc1` is now
`690c478f322d22ad34989f9286ddf0d55ce79c43` (tag `prereg-v1`). The tag was created before any model output was
generated, as before; only the identity and hashes changed. `.rops/prereg.json` was left as written.
