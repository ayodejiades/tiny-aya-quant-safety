#!/bin/bash
# Resumable overnight run. Cuts 1,3,4 applied (DEVIATIONS D5): sets = harmful benign wrapped(W1) capability.
cd /Users/nifemi/Research/lexsi && source .venv/bin/activate
SETS="harmful benign wrapped capability"
arm() {  # arm <id> <gguf>
  echo "=== $(date) arm $1"
  if harness/serve.sh "$2" "runs/server_$1.log"; then
    python harness/04_generate.py --arm "$1" --sets $SETS --split test || echo "ARM $1 FAILED"
  else echo "ARM $1 server failed"; fi
  pkill -f llama-server; sleep 2
}
arm q4_k_m models/official/tiny-aya-global-q4_k_m.gguf
arm f16    models/official/tiny-aya-global-f16.gguf
arm Q3_K_S models/ours/tiny-aya-global-Q3_K_S.gguf
arm Q2_K   models/ours/tiny-aya-global-Q2_K.gguf
echo "=== $(date) sweep"; python harness/06_sweep.py || echo "SWEEP FAILED"
arm F1 models/ours/tiny-aya-global-Q3_K_S-protected.gguf
arm F2 models/ours/tiny-aya-global-Q3_K_S-decoy.gguf
echo "=== $(date) judge"; pkill -f llama-server
python harness/05_judge.py --arms q4_k_m f16 Q3_K_S Q2_K F1 F2 || echo "JUDGE FAILED"
python harness/07_labels.py || echo "LABELS FAILED"
arm q4_0 models/official/tiny-aya-global-q4_0.gguf
arm q8_0 models/official/tiny-aya-global-q8_0.gguf
echo "=== $(date) judge (nice-to-have arms)"; pkill -f llama-server
python harness/05_judge.py --arms q4_0 q8_0 || echo "JUDGE2 FAILED"
echo "=== $(date) DONE"
