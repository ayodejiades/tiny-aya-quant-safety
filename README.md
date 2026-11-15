# What survives 4-bit? Refusal behaviour of Tiny Aya Global across GGUF quantizations (results pending)

**Status: first submission, written before the main grid finished. Results are pending and will replace this text.**

## Tracks and problem statements

Track 2b, problem statement 7 (safety-aware compression). Secondary: Track 2a, problem statement 1 (robustness evaluation with jailbreak wrappers and over-refusal).

## Content warning

The prompt sets name harmful topics (JailbreakBench, XSTest). Model outputs judged unsafe are truncated in the published logs.

## Question and frozen design

Tiny Aya is sold as an on-device model, so what people run is a quantized GGUF, not the full-precision weights that safety is normally measured on. We ask whether refusal behaviour survives the official quantizations, and whether keeping one block of layers at 8-bit inside a 3-bit model repairs what is lost. The design is frozen in `PREREG.md` (git tag `prereg-v1`) before any model output was generated; changes are logged in `DEVIATIONS.md`.

Model: `CohereLabs/tiny-aya-global-GGUF` (CC-BY-NC-4.0). Arms: `f16` (reference), `q8_0`, `q4_k_m`, `q4_0` (official files), `Q3_K_S`, `Q2_K` (made with `llama-quantize` from the official f16 file), and two intervention arms `F1` (protected block) and `F2` (decoy block). Kits chained: CuratorKIT (dedupe and curate the prompt sets) then AuditKIT (generate and detect refusals), with llama.cpp for quantization.

## Pilot numbers (dev split, not test)

- Positive control: f16 refuses 86.7% of the 30 dev harmful prompts and 13.3% of the 30 dev benign prompts, a gap of 73.3 points (the preregistered minimum is 20). The instrument separates harmful from harmless requests.
- Sensitivity control: on the first 50 ARC-Easy items f16 scores 84.0% and Q2_K scores 76.0%, so the harness detects damage from quantization.
- Determinism: 0 of 60 refusal labels differ between two runs of q4_k_m.

## Deviations so far

See `DEVIATIONS.md`. In short: the speed rule triggered, so the wrapper W2 and the XSTest sets were dropped and the layer sweep uses three blocks; Llama Guard is called with Meta's published response-classification prompt because Ollama's template grades the prompt, not the response.

## Artifacts

Code, preregistration and deviations are in this repository. Models and datasets are on Hugging Face under `ayodejiades`. Main results are pending.

## LLM usage statement

Claude Fable designed the experiment and wrote the guide. Claude Sonnet 5.5 (Claude Code) wrote the code and drafted this text. The author runs, labels and checks the work.
