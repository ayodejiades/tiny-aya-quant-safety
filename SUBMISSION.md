# Submission: What survives 4-bit? (final results)

**Tracks:** 2b (primary), problem statement 7, safety-aware compression. 2a (secondary), problem statement 1, robustness evaluation with a jailbreak wrapper and over-refusal.

## Abstract

Tiny Aya is sold as an on-device model, so what people run is a quantized GGUF, not the full-precision weights on which safety is normally measured. We test whether the refusal behaviour of Tiny Aya Global survives its official quantizations (q8_0, q4_k_m, q4_0) and two lower-bit builds we made (Q3_K_S, Q2_K), and whether keeping one block of 12 of the 36 layers at 8-bit inside a 3-bit model repairs what is lost. The design was preregistered and frozen before any model output was generated (git tag `prereg-v1`). Prompts come from JailbreakBench (harmful and benign) and are curated and deduplicated with CuratorKIT; generation and refusal detection run through AuditKIT against a local llama.cpp server at temperature 0; harm is scored by Llama Guard 3. A decoy arm tests whether any repair comes from the extra bits or from which layers hold them.

Results for all eight arms and four hypotheses. On the 70 harmful prompts no arm differs from f16 after Holm correction. The official 4-bit file shows no erosion (harmful refusal 85.7% for f16, 87.1% for q4_k_m; H1 not supported), and q8_0 matches f16 on every refusal label. q4_0 raises over-refusal from 7.2% to 21.7% and flips 11.5% of the 139 direct labels against f16 (Holm p = 0.0036). Q2_K flips 13.7% (Holm p = 0.0266) and drops ARC-Easy from 82.0% to 72.7%. Its harmful refusal is lower (72.9%), but that drop is not significant after correction (raw p = 0.0225, Holm p = 0.1572). Its Llama Guard attack success rate is 20.0% against 10.0% for f16, with overlapping intervals and no test. H2 is not supported in its ordering: Q3_K_S flips 3.6%, less than q4_0, though the flip rate exceeds the net refusal change for 4 of the 5 uniform arms. The layer-protection repair failed (H3 not supported): F1 flips 7.2% of labels against 3.6% for plain Q3_K_S (p = 0.0625) and is not better than its decoy F2 (5.0%, p = 0.5078). F1 is 2254 MB, larger than the official q4_k_m file (2144 MB), which flips fewer labels (3.6%). F1 did not cost capability (82.7% against 82.0%; H4 supported). Judge check against 60 blind hand labels: the keyword refusal detector has kappa 0.87, Llama Guard has kappa 0.46 on 30 harmful-set outputs, so attack success rates are weak evidence. Intervals are wide. The 128-token cap truncated 87.0% to 95.7% of benign outputs and 62.9% to 100.0% of wrapped outputs depending on the arm, and 50.0% of Q2_K's harmful outputs against 15.7% for f16, so Llama Guard judged partial text of unequal length across arms.

Compute cuts forced by a speed estimate changed the preregistered design. Wrapper W2 and the XSTest sets were dropped, so the primary metric is JBB harmful only (n = 70, not 170) and the flip rate is over the 139 direct JBB prompts only, without the XSTest prompts the preregistration included. The sweep used three 12-layer blocks, so F1 and F2 protect 12 layers, not the preregistered 6.

## Links

- Write-up: https://github.com/ayodejiades/tiny-aya-quant-safety/blob/main/README.md
- GitHub: https://github.com/ayodejiades/tiny-aya-quant-safety
- Deviations from the preregistration: https://github.com/ayodejiades/tiny-aya-quant-safety/blob/main/DEVIATIONS.md
- Models collection: https://huggingface.co/collections/ayodejiades/tiny-aya-quantization-and-safety-models-6afa0afc9994d1dfbbc11ad1
- Datasets collection: https://huggingface.co/collections/ayodejiades/tiny-aya-quantization-and-safety-datasets-6afa0afda81fe397ad77a23a

## Hackathon repos and models used

- CuratorKIT: MinHash near-duplicate removal and text cleaning over the pooled prompt sets (no toxicity or PII gate, so harmful items are kept).
- AuditKIT: `ak.evaluate` against an OpenAI-compatible server, and the built-in `RefusalDetector`.
- llama.cpp: `llama-quantize` (including per-layer `--tensor-type`) and `llama-server`.
- Base model: `CohereLabs/tiny-aya-global-GGUF` (CC-BY-NC-4.0).
- Judge: Llama Guard 3 8B through Ollama.

## Changelog

- 16 Nov 2026: final results replace the first submission, which reported the pilot only.
- 16 Nov 2026: abstract revised. Test results added to the Q2_K and repair claims, truncation rates corrected per arm, H2 and H4 outcomes and the F1 file size added, and the changes to the preregistered primary metric stated.

## Contact

Email: ayodejiadesegun20@gmail.com
