# P089 — Harness audit report

**Audit date:** 2026-08-28  
**Baseline:** `dcfc6715a6de8d030cd106c2187081d70d7f22dc`

## Findings repaired

| Finding | Baseline | Repair |
|---|---|---|
| Unit of analysis | 9,086 rows were called “unique processes” | 9,086 are classification assignments; **8,894** are distinct processes |
| Multicategory duplication | Hidden by composite-key language | **178** processes span >1 category, creating **192** extra classification rows |
| Monetary parsing | Comma-decimal values were coerced to missing in several summaries | Robust decimal-comma parser; missing values stay null |
| Monetary headline | Licitation + OC amounts were presented as one total | Amounts are reported separately and never added |
| Causal language | Descriptive post-2022 increase was described as causal | Rewritten as temporal association; causality requires ITSA/DiD or equivalent design |
| Automated audit | Previous tests could validate the same parsing bug they were meant to detect | Independent stdlib audit + contract tests + CI |
| Portability | QA scripts hard-coded `D:/...` paths | Harness audit/build scripts use relative/CLI paths |

## Corrected headline metrics

- Classification assignments: **9,086**.
- Distinct processes: **8,894** = 2,175 licitations + 6,719 purchase orders.
- Multicategory processes: **178**.
- Distinct-process amount recorded in licitations: **CLP 249,813.979 million** (framework/budget magnitude).
- Distinct-process amount recorded in purchase orders: **CLP 105,536.060 million** (transactional magnitude).
- Missing amount at process level: **289** records (279 licitations, 10 purchase orders).

## Open warnings — not silently “fixed”

1. **10** legacy classification rows have an empty `termino_coincidente`. They require review against the original source fields.
2. Only **466 source filenames** are observable among matched rows, while the project describes 470 monthly source files. This does not prove missing ingestion because a processed file can yield zero matches. A source manifest with hashes is required for full provenance certification.
3. `2026-4.csv` appears as a non-standard source filename for 46 purchase-order rows. It should be reconciled against the ingestion manifest.
4. `Transicion_SBN` is intentionally broad. Matches such as energy-efficiency certifications can be tangential to climate policy. Precision must be measured with a labelled validation sample before inferential use.

## Verification status

**PASS WITH WARNINGS.** Structural integrity and monetary interpretation are repaired. Semantic precision and source-manifest provenance remain explicit research tasks rather than hidden assumptions.
