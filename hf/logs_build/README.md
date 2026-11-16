# Run logs for "What survives 4-bit?"

One JSONL file per arm and set under `runs/<arm>/<set>.<split>.jsonl`: prompt, response, `refused` (AuditKIT keyword detector), `finish_reason` (derived, see DEVIATIONS D3), token count, `guard_unsafe` (Llama Guard 3 8B) where judged. **Responses judged unsafe, and unjudged responses to harmful prompts, are truncated to the first 200 characters with a sha256 of the full text.** `results/` holds the claims table, sweep scores and file sizes; `runs/rendered_prompt.txt` is the rendered chat prompt. Hand labels will be added after the author labels them. Code and write-up: https://github.com/ayodejiades/tiny-aya-quant-safety

The prompts name harmful topics. Arms: f16, q8_0, q4_k_m, q4_0, Q3_K_S, Q2_K, F1, F2; `q4_k_m_rep` and `sweep-B*` are determinism and sweep runs on the dev split.
