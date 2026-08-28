# Provenance — pending certification

The result table contains matches, not an ingestion ledger. Therefore the 466 source filenames visible in matched rows cannot prove or disprove that 470 source files were processed.

To close provenance, produce `source_manifest.csv` with one row per raw ChileCompra source file and at least:

`source_file;source_type;period;bytes;sha256;download_url;downloaded_at;ingested_at;status;match_count`

Certification is closed only when the declared 470 inputs are reconciled to this manifest and hashes can be checked against the archived raw files.
