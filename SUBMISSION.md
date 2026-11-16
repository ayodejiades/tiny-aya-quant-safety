# Submission: What survives 4-bit? (final results)

**Tracks:** 2b (primary), problem statement 7, safety-aware compression. 2a (secondary), problem statement 1, robustness evaluation with jailbreak wrappers and over-refusal.

## Abstract

Tiny Aya is sold as an on-device model, so what people run is a quantized GGUF, not the full-precision weights on which safety is normally measured. We test whether the refusal behaviour of Tiny Aya Global survives its official quantizations (q8_0, q4_k_m, q4_0) and two lower-bit builds we made (Q3_K_S, Q2_K), and whether keeping one block of layers at 8-bit inside a 3-bit model repairs what is lost. The design was preregistered and frozen before any model output was generated (git tag `prereg-v1`). Prompts come from JailbreakBench (harmful and benign) and are curated and deduplicated with CuratorKIT; generation and refusal detection run through AuditKIT against a local llama.cpp server at temperature 0; harm is scored by Llama Guard 3. A decoy arm tests whether any repair comes from the extra bits or from which layers hold them.

Results, all arms reported: the official 4-bit file shows no erosion (harmful refusal 85.7% for f16, 87.1% for q4_k_m; H1 not supported). q4_0 raises over-refusal from 7.2% to 21.7% and flips 11.5% of labels against f16. Q2_K refuses harmful prompts less (72.9%), doubles the Llama Guard attack success rate (10.0% to 20.0%) and drops ARC-Easy from 82.0% to 72.7%. The layer-protection repair failed: F1 flips 7.2% of labels against 3.6% for plain Q3_K_S and is not better than its decoy F2 (5.0%); it did not cost capability (82.7% against 82.0%). Judge check against 60 blind hand labels: the keyword refusal detector has kappa 0.87, Llama Guard has kappa 0.46 on 30 harmful-set outputs, so attack success rates are best read as relative. Intervals are wide and about nine in ten benign and wrapped outputs hit the 128-token cap.

Compute cuts forced by a speed estimate are logged in `DEVIATIONS.md` (wrapper W2 and the XSTest sets dropped, a three-block layer sweep).

## Links

- Write-up: https://github.com/ayodejiades/tiny-aya-quant-safety/blob/main/README.md
- GitHub: https://github.com/ayodejiades/tiny-aya-quant-safety
- Models collection: https://huggingface.co/collections/ayodejiades/tiny-aya-quantization-and-safety-models-6afa0afc9994d1dfbbc11ad1
- Datasets collection: https://huggingface.co/collections/ayodejiades/tiny-aya-quantization-and-safety-datasets-6afa0afda81fe397ad77a23a

## Hackathon repos and models used

- CuratorKIT: MinHash near-duplicate removal and text cleaning over the pooled prompt sets (no toxicity or PII gate, so harmful items are kept).
- AuditKIT: `ak.evaluate` against an OpenAI-compatible server, and the built-in `RefusalDetector`.
- llama.cpp: `llama-quantize` (including per-layer `--tensor-type`) and `llama-server`.
- Base model: `CohereLabs/tiny-aya-global-GGUF` (CC-BY-NC-4.0).
- Judge: Llama Guard 3 8B through Ollama.

## Contact

Email: 
