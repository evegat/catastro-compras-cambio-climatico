#!/usr/bin/env python3
"""Generate P089 figures under the v1.1 Harness data contract.

Institutional, temporal, mechanism and top-buyer charts use DISTINCT processes.
Subcategory charts use the long classification table and are explicitly non-additive.
"""
from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "Catastro_Cambio_Climatico_ChileCompra.csv"
OUT = ROOT / "figuras_catastro"
OUT.mkdir(exist_ok=True)


def amount_numeric(series):
    s = series.fillna("").astype(str).str.strip()
    def one(v):
        if not v: return None
        if "," in v and "." not in v: v = v.replace(",", ".")
        elif "," in v and "." in v:
            if v.rfind(",") > v.rfind("."):
                v = v.replace(".", "").replace(",", ".")
            else:
                v = v.replace(",", "")
        try: return float(v)
        except ValueError: return None
    return s.map(one)


def load():
    long = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8-sig", comment="#")
    long["monto_num"] = amount_numeric(long["monto_pesos"])
    proc = long.sort_values(["tipo_registro","codigo_proceso"]).drop_duplicates(["tipo_registro","codigo_proceso"]).copy()
    proc["monto_num"] = amount_numeric(proc["monto_pesos"])
    def year(row):
        s = str(row.get("fecha", ""))[:4]
        if s.isdigit(): return int(s)
        m = re.search(r"(20\d{2})", str(row.get("archivo_origen", "")))
        return int(m.group(1)) if m else None
    proc["anio"] = proc.apply(year, axis=1)
    return long, proc


def fig1(proc):
    t = proc.groupby("anio").size()
    ax = t.plot(kind="bar", figsize=(10,5), title="Procesos distintos asociados a cambio climático (2007–2026)")
    ax.set_xlabel("Año"); ax.set_ylabel("Procesos distintos")
    plt.tight_layout(); plt.savefig(OUT/"fig1_evolucion_temporal.png", dpi=300); plt.close()


def fig2(proc):
    t = proc.groupby("mecanismo_compra").size().sort_values()
    ax = t.plot(kind="barh", figsize=(10,5), title="Mecanismos de contratación — procesos distintos")
    ax.set_xlabel("Procesos distintos"); ax.set_ylabel("")
    plt.tight_layout(); plt.savefig(OUT/"fig2_mecanismos_contratacion.png", dpi=300); plt.close()


def fig3(proc):
    t = proc.groupby("nivel_institucional").size().sort_values()
    ax = t.plot(kind="barh", figsize=(10,5), title="Gobernanza multinivel — procesos distintos")
    ax.set_xlabel("Procesos distintos"); ax.set_ylabel("")
    plt.tight_layout(); plt.savefig(OUT/"fig3_gobernanza_multinivel.png", dpi=300); plt.close()


def fig4(long):
    t = long.groupby("subcategoria").size().sort_values()
    ax = t.plot(kind="barh", figsize=(10,4.5), title="Asignaciones temáticas (categorías no aditivas)")
    ax.set_xlabel("Asignaciones proceso–subcategoría"); ax.set_ylabel("")
    plt.tight_layout(); plt.savefig(OUT/"fig4_subcategorias_tematicas.png", dpi=300); plt.close()


def fig5(proc):
    t = proc.groupby("organismo_comprador").size().nlargest(12).sort_values()
    ax = t.plot(kind="barh", figsize=(10,5), title="Top 12 organismos — procesos distintos")
    ax.set_xlabel("Procesos distintos"); ax.set_ylabel("")
    plt.tight_layout(); plt.savefig(OUT/"fig5_top_organismos_compradores.png", dpi=300); plt.close()


def main():
    long, proc = load()
    assert len(long) == 9086, len(long)
    assert len(proc) == 8894, len(proc)
    fig1(proc); fig2(proc); fig3(proc); fig4(long); fig5(proc)
    print(f"OK: figuras Harness generadas en {OUT}")

if __name__ == "__main__": main()
