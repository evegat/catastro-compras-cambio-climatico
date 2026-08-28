#!/usr/bin/env python3
"""Independent data-contract audit for P089.

The historical CSV is a LONG classification table: one row per
(tipo_registro, codigo_proceso, subcategoria), not one row per process.
"""
from __future__ import annotations
import argparse, csv, io
from collections import defaultdict, Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

EXPECTED = {
    "assignments": 9086,
    "processes": 8894,
    "licitaciones": 2175,
    "ordenes_compra": 6719,
    "multicategory_processes": 178,
    "extra_assignments": 192,
    "missing_trigger_terms": 10,
}


def read_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        lines = [line for line in fh if not line.startswith("#")]
    return list(csv.DictReader(io.StringIO("".join(lines)), delimiter=";"))


def parse_amount(value: str | None):
    s = "" if value is None else str(value).strip().replace("\xa0", "")
    if not s:
        return None
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    elif "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def audit(path: Path):
    rows = read_rows(path)
    failures, warnings = [], []
    required = {
        "tipo_registro", "codigo_proceso", "subcategoria", "monto_pesos",
        "nivel_institucional", "termino_coincidente", "archivo_origen",
    }
    if not rows:
        failures.append("dataset vacío")
        return failures, warnings, {}
    missing_cols = required - set(rows[0])
    if missing_cols:
        failures.append(f"faltan columnas: {sorted(missing_cols)}")
        return failures, warnings, {}

    composite = [(r["tipo_registro"], r["codigo_proceso"], r["subcategoria"]) for r in rows]
    if len(composite) != len(set(composite)):
        failures.append("hay duplicados en la llave long (tipo, codigo, subcategoria)")

    groups = defaultdict(list)
    for r in rows:
        groups[(r["tipo_registro"], r["codigo_proceso"])].append(r)

    counts = Counter(k[0] for k in groups)
    multicat = sum(len({x["subcategoria"] for x in g}) > 1 for g in groups.values())
    extra = sum(max(0, len({x["subcategoria"] for x in g}) - 1) for g in groups.values())
    missing_terms = sum(not (r.get("termino_coincidente") or "").strip() for r in rows)

    observed = {
        "assignments": len(rows), "processes": len(groups),
        "licitaciones": counts["licitacion"], "ordenes_compra": counts["orden_compra"],
        "multicategory_processes": multicat, "extra_assignments": extra,
        "missing_trigger_terms": missing_terms,
    }
    for key, expected in EXPECTED.items():
        if observed[key] != expected:
            failures.append(f"{key}: esperado {expected}, observado {observed[key]}")

    totals = {"licitacion": Decimal(0), "orden_compra": Decimal(0)}
    missing_amount = Counter()
    for (tipo, _codigo), g in groups.items():
        amount = parse_amount(g[0].get("monto_pesos"))
        if amount is None:
            missing_amount[tipo] += 1
        else:
            totals[tipo] += amount

    lic_m = totals["licitacion"] / Decimal(1_000_000)
    oc_m = totals["orden_compra"] / Decimal(1_000_000)
    if abs(lic_m - Decimal("249813.979143")) > Decimal("0.001"):
        failures.append(f"monto licitaciones inesperado: {lic_m} M CLP")
    if abs(oc_m - Decimal("105536.059873")) > Decimal("0.001"):
        failures.append(f"monto OC inesperado: {oc_m} M CLP")

    source_files = len({r["archivo_origen"] for r in rows})
    if source_files != 466:
        warnings.append(f"nombres de fuente observados={source_files}; baseline auditado=466")
    if missing_terms:
        warnings.append(f"{missing_terms} asignaciones con termino_coincidente vacío requieren revisión primaria")
    if any(r.get("archivo_origen") == "2026-4.csv" for r in rows):
        warnings.append("2026-4.csv es un nombre no estándar; reconciliar con manifest de ingestión")
    warnings.append("Transicion_SBN requiere validación muestral de precisión antes de inferencia")
    warnings.append("470 fuentes declaradas no pueden certificarse sólo desde filas con match; falta manifest con hashes")

    metrics = {
        **observed,
        "licitacion_amount_m_clp": str(lic_m),
        "oc_amount_m_clp": str(oc_m),
        "missing_amount_licitacion": missing_amount["licitacion"],
        "missing_amount_oc": missing_amount["orden_compra"],
        "observed_source_filenames": source_files,
    }
    return failures, warnings, metrics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", nargs="?", default="Catastro_Cambio_Climatico_ChileCompra.csv")
    args = ap.parse_args()
    failures, warnings, metrics = audit(Path(args.csv_path))
    print("P089 DATA CONTRACT AUDIT")
    for k, v in metrics.items(): print(f"  {k}: {v}")
    for w in warnings: print(f"WARN: {w}")
    if failures:
        for e in failures: print(f"FAIL: {e}")
        return 1
    print("PASS WITH WARNINGS" if warnings else "PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
