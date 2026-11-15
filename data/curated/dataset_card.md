# Dataset Card: lexsi_prompts

## Summary

- **Run timestamp**: 2026-11-15T17:14:11.773406Z
- **Wall clock time**: 1.4s
- **Pipeline config hash**: `a37fdc6030064b60`

## Source Documents

  - Unknown

## Pipeline Stages

| Step | Input | Passed | Recovered | Rejected | Forward |
|------|-------|--------|-----------|----------|---------|
| JSONLReader | 650 | 650 | — | 0 | 650 |
| SchemaGate | 650 | 650 | 0 | 0 | 650 |
| ExactDeduplicator | 650 | 650 | — | — | 650 |
| MinHashDeduplicator | 650 | 649 | — | — | 649 |
| TextCleaner | 649 | 649 | — | — | 649 |
| AlpacaExporter | — | 649 | — | — | 649 |

## Gate Pass Rates and Rejection Breakdown

- **JSONLReader**: 650/0 passed (N/A), 0 rejected
- **SchemaGate**: 650/650 passed (100.0%), 0 rejected


**Rejection reasons:**
  - None

## Deduplication

  - near_duplicates_removed: 1
  - surviving_count: 649

## Known Limitations

- MinHash threshold used: **0.85** — this is a starting point, not a universal answer. Adjust per domain (legal, medical, and other domain-specific corpora may need a lower threshold to avoid losing structurally similar but semantically valid examples).
- Table extraction requires `extract_tables: true` on the PDF reader and MinerU with GPU support. Disabled by default.
- Token counting uses a whitespace tokenizer by default. For exact LLM context window
  enforcement, enable `use_tiktoken: true` in the SchemaGate config.
- Both within-run (MinHash/Diversity) and cross-run (EmbeddingDeduplicator) deduplication
  are available. Cross-run dedup persists an embedding index across runs; use
  `embedding_reset_index: true` to start fresh.

## Reproduction

```bash
pip install curatorkit
curatorkit run pipeline.yaml --output-dir ./out/
```

## Tool Versions

- **curatorkit**: 0.1.28
- **python**: 3.12.14
