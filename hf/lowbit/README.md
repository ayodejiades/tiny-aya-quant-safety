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

| `tiny-aya-global-Q3_K_S-decoy.gguf` (F2) | `llama-quantize --tensor-type "blk\.(24|25|26|27|28|29|30|31|32|33|34|35)\..*=q8_0" models/official/tiny-aya-global-f16.gguf tiny-aya-global-Q3_K_S-decoy.gguf Q3_K_S` (layers 24 to 35 kept at Q8_0; decoy block chosen by seeded draw) |

## Results (test split, 70 harmful and 69 benign JBB prompts, 70 wrapped, 150 ARC-Easy; greedy, 128 tokens)

| Arm | Bits/weight | Size MB | Harmful refusal % | Over-refusal % | Flip rate vs f16 % | ASR on W1 wrapper % | ARC-Easy % |
|---|---|---|---|---|---|---|---|
| f16 | 16.03 | 6710 | 85.7 | 7.2 | 0.0 | 75.7 | 82.0 |
| Q3_K_S | 3.97 | 1661 | 88.6 | 8.7 | 3.6 | 52.9 | 82.0 |
| Q2_K | 3.54 | 1482 | 72.9 | 1.4 | 13.7 | 88.6 | 72.7 |
| F2 | 5.38 | 2254 | 84.3 | 7.2 | 5.0 | 74.3 | 82.7 |

Intervals, paired tests and caveats (128-token cap truncates most benign and wrapped answers; keyword refusal detector; n is small) are in the repository README. Q2_K refuses fewer harmful prompts and loses accuracy; F2 is a control, not a recommended model.

## Intended use and risk

For research on compression and safety only. Quantized models can refuse less often than the full-precision model; do not deploy these where refusals matter.
