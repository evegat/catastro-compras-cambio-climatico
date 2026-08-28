#!/usr/bin/env python3
"""Build the canonical distinct-process view from P089's long classification CSV."""
from __future__ import annotations
import argparse, csv, io
from collections import defaultdict
from pathlib import Path
from audit_dataset import parse_amount

FIELDS = [
    "archivo_origen","tipo_registro","mecanismo_compra","codigo_proceso","link","nombre","descripcion",
    "organismo_comprador","unidad_compra","rut_comprador","sector","region_comprador","fecha","monto_pesos",
    "moneda","proveedor","rut_proveedor","eje_codigo","eje_nombre","nivel_institucional",
    "subcategorias","terminos_coincidentes","n_clasificaciones"
]

def read_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        lines = [line for line in fh if not line.startswith("#")]
    return list(csv.DictReader(io.StringIO("".join(lines)), delimiter=";"))

def build(src: Path, dest: Path):
    rows = read_rows(src)
    groups = defaultdict(list)
    for r in rows:
        groups[(r["tipo_registro"], r["codigo_proceso"])].append(r)
    out = []
    for g in groups.values():
        r = dict(g[0])
        r["subcategorias"] = " | ".join(sorted({x["subcategoria"] for x in g if x["subcategoria"]}))
        r["terminos_coincidentes"] = " | ".join(sorted({x["termino_coincidente"] for x in g if x["termino_coincidente"]}))
        r["n_clasificaciones"] = str(len(g))
        amount = parse_amount(r.get("monto_pesos"))
        r["monto_pesos"] = "" if amount is None else format(amount, "f")
        out.append(r)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8-sig", newline="") as fh:
        fh.write("# dataset_id: P089_EVT_CHILECOMPRA_2007_2026_PROCESS_LEVEL\n")
        fh.write("# version: 1.1-harness\n")
        fh.write("# unit_of_analysis: unique procurement process by tipo_registro + codigo_proceso\n")
        fh.write("# amount_rule: decimal comma normalized; missing amounts remain blank\n")
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter=";", extrasaction="ignore")
        w.writeheader(); w.writerows(out)
    return len(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", nargs="?", default="Catastro_Cambio_Climatico_ChileCompra.csv")
    ap.add_argument("--output", default="output/Catastro_Procesos_Unicos_Cambio_Climatico_ChileCompra.csv")
    args = ap.parse_args()
    n = build(Path(args.csv_path), Path(args.output))
    print(f"OK: {n:,} distinct processes -> {args.output}")
    return 0 if n == 8894 else 1
if __name__ == "__main__": raise SystemExit(main())
