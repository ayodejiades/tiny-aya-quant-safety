---
license: cc-by-nc-4.0
base_model: CohereLabs/tiny-aya-global-GGUF
tags: [gguf, quantization, safety, tiny-aya]
---
# Tiny Aya Global, Q3_K_S with layers 0 to 11 protected at Q8_0 (F1)

Intervention arm of the study *What survives 4-bit?* (https://github.com/ayodejiades/tiny-aya-quant-safety). Base model `CohereLabs/tiny-aya-global-GGUF`, CC-BY-NC-4.0 (inherited).

Built with:
`llama-quantize --tensor-type "blk\.(0|1|2|3|4|5|6|7|8|9|10|11)\..*=q8_0" models/official/tiny-aya-global-f16.gguf tiny-aya-global-Q3_K_S-protected.gguf Q3_K_S`

The block was selected on 60 dev prompts (refusal-label agreement with f16: 1.0 for this block). **It did not repair 3-bit on the test split**: its flip rate against f16 was higher than plain Q3_K_S, and not better than a decoy block. This file is published so the null result can be checked, not as a recommended model.

## Results (test split; greedy, 128 tokens)

| Arm | Bits/weight | Size MB | Harmful refusal % | Over-refusal % | Flip rate vs f16 % | ASR on W1 wrapper % | ARC-Easy % |
|---|---|---|---|---|---|---|---|
| f16 | 16.03 | 6710 | 85.7 | 7.2 | 0.0 | 75.7 | 82.0 |
| Q3_K_S | 3.97 | 1661 | 88.6 | 8.7 | 3.6 | 52.9 | 82.0 |
| F1 | 5.38 | 2254 | 91.4 | 13.0 | 7.2 | 55.7 | 82.7 |
| F2 | 5.38 | 2254 | 84.3 | 7.2 | 5.0 | 74.3 | 82.7 |

See the repository README for intervals, paired tests and limitations.

## Intended use and risk

Research on compression and safety only.
