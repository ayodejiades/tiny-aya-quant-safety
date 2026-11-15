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
