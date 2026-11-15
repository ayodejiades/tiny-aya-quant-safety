---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global-GGUF
tags: [gguf, quantization, safety, tiny-aya]
---
# Tiny Aya Global, low-bit GGUF quantizations (safety study)

Research artifacts for the study *What survives 4-bit?* (code and preregistration: https://github.com/ayodejiades/tiny-aya-quant-safety).
Base model: `CohereLabs/tiny-aya-global-GGUF` (CC-BY-NC-4.0; this repository inherits that licence). These are **not** safety-tuned models. They exist to measure how refusal behaviour changes with precision.

| File | How it was made |
|---|---|
| `tiny-aya-global-Q3_K_S.gguf` | `llama-quantize models/official/tiny-aya-global-f16.gguf tiny-aya-global-Q3_K_S.gguf Q3_K_S` |
| `tiny-aya-global-Q2_K.gguf` | `llama-quantize models/official/tiny-aya-global-f16.gguf tiny-aya-global-Q2_K.gguf Q2_K` |

The decoy arm `F2` (Q3_K_S with one block of layers kept at Q8_0) will be added when the sweep finishes.

## Results

Results pending. See the GitHub repository for the current status; the main grid had not finished when this card was written.

## Intended use and risk

For research on compression and safety only. Quantized models can refuse less often than the full-precision model; do not deploy these where refusals matter.
