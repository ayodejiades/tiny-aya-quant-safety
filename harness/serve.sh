#!/bin/bash
# usage: serve.sh <gguf> <log>   starts llama-server and waits for /health
pkill -f llama-server; sleep 2
nohup llama-server -m "$1" --port 8080 -c 8192 -np 4 -ngl 99 --jinja --temp 0 --seed 0 -n 128 > "$2" 2>&1 &
for i in $(seq 1 120); do curl -s http://127.0.0.1:8080/health | grep -q '"ok"' && exit 0; sleep 3; done
echo "server failed to start"; exit 1
