# Submission: What survives 4-bit? (first submission, results pending)

**Tracks:** 2b (primary), problem statement 7, safety-aware compression. 2a (secondary), problem statement 1, robustness evaluation with jailbreak wrappers and over-refusal.

## Abstract

Tiny Aya is sold as an on-device model, so what people run is a quantized GGUF, not the full-precision weights on which safety is normally measured. We test whether the refusal behaviour of Tiny Aya Global survives its official quantizations (q8_0, q4_k_m, q4_0) and two lower-bit builds we made (Q3_K_S, Q2_K), and whether keeping one block of layers at 8-bit inside a 3-bit model repairs what is lost. The design was preregistered and frozen before any model output was generated (git tag `prereg-v1`). Prompts come from JailbreakBench (harmful and benign) and are curated and deduplicated with CuratorKIT; generation and refusal detection run through AuditKIT against a local llama.cpp server at temperature 0; harm is scored by Llama Guard 3. A decoy arm tests whether any repair comes from the extra bits or from which layers hold them.

This submission was made before the main grid finished. A pilot on the dev split passed its controls: the f16 model refuses 86.7% of dev harmful prompts and 13.3% of dev benign prompts (a 73.3-point gap against a preregistered minimum of 20), Q2_K scores lower than f16 on 50 ARC-Easy items (76.0% against 84.0%), and two q4_k_m runs give identical refusal labels on 60 prompts. Main results (refusal rate, per-prompt flip rate against f16, attack success rate, capability, repair arms) are pending and will replace this text in a later submission.

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
