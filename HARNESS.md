# P089 Harness contract — v1.1

Baseline audited: `dcfc6715a6de8d030cd106c2187081d70d7f22dc` (2026-08-28).

## Source-of-truth model

1. `Catastro_Cambio_Climatico_ChileCompra.csv` is the **long classification table**. Its unit is `(tipo_registro, codigo_proceso, subcategoria)` and it contains **9,086 assignments**.
2. A procurement **process** is `(tipo_registro, codigo_proceso)`. There are **8,894 distinct processes**: 2,175 licitations and 6,719 purchase orders.
3. `scripts/build_process_level.py` derives the process-level view deterministically. Do not manually maintain two competing datasets.
4. Financial magnitudes for licitations and purchase orders are **not additive** and must be reported separately.

## Certified structural metrics

- 9,086 classification assignments.
- 8,894 distinct processes.
- 178 multicategory processes / 192 additional assignment rows.
- CLP 249,813.979 million recorded in distinct licitations.
- CLP 105,536.060 million recorded in distinct purchase orders.
- 289 distinct processes have no parsable amount (279 licitations; 10 purchase orders).

## Open warnings

- 10 long-table rows have empty `termino_coincidente`; review against original raw fields.
- 466 source filenames are observable among matched rows; this cannot certify the declared 470 processed sources. Build a source manifest with SHA-256, size and ingestion status.
- `2026-4.csv` is a non-standard source filename and must be reconciled against the manifest.
- `Transicion_SBN` is broad; estimate precision from a labelled stratified sample before inferential use.
- Post-2022 change is descriptive association. Causal attribution to Law 21.455 requires an identification design (e.g. ITSA/DiD/event study).

## Required checks

```bash
python scripts/audit_dataset.py Catastro_Cambio_Climatico_ChileCompra.csv
python -m unittest discover -s tests -v
python scripts/build_process_level.py Catastro_Cambio_Climatico_ChileCompra.csv --output output/processes.csv
```

GitHub Actions runs these checks on pull requests and `main`.
