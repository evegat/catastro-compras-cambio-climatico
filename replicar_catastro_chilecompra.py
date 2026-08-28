#!/usr/bin/env python3
"""P089 v1.1-harness — reproducible extraction from ChileCompra raw CSV files.

Outputs:
1) Long classification table: one row per (tipo_registro, codigo_proceso, subcategoria).
2) Distinct-process view: one row per (tipo_registro, codigo_proceso).

This script does not claim that a lexical match proves climate impact.
"""
from __future__ import annotations
import argparse, glob, os, re
from pathlib import Path
import duckdb
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

TAXONOMY = [
    ("Nucleo_Exacto", r"(?i)\b(cambio\s+clim[aá]tico|adaptaci[oó]n\s+clim[aá]tica|mitigaci[oó]n\s+clim[aá]tica|resiliencia\s+clim[aá]tica|emergencia\s+clim[aá]tica|acci[oó]n\s+clim[aá]tica)\b"),
    ("Instrumentos_Ley21455", r"(?i)\b(ley\s+(marco\s+de\s+)?cambio\s+clim[aá]tico|ley\s+21\.?455|plan(es)?\s+de\s+acci[oó]n\s+clim[aá]tic[ao]|estrategia\s+clim[aá]tica\s+de\s+largo\s+plazo|\beclp\b|\bpamcc\b|\bparcc\b|plan(es)?\s+de\s+adaptaci[oó]n\s+al\s+cambio\s+clim[aá]tico|planes\s+de\s+acci[oó]n\s+comunal\s+de\s+cambio\s+clim[aá]tico)\b"),
    ("Gases_Descarbonizacion", r"(?i)\b(huella\s+de\s+carbono|descarbonizaci[oó]n|gases?\s+de\s+efecto\s+invernadero|\bgei\b|neutralidad\s+de\s+carbono|carbono\s+neutral(idad)?|bonos?\s+de\s+carbono|cr[eé]ditos?\s+de\s+carbono|mercado\s+de\s+carbono|presupuesto\s+de\s+carbono)\b"),
    ("Transicion_SBN", r"(?i)\b(soluciones?\s+basadas?\s+en\s+la\s+naturaleza|transici[oó]n\s+justa|transici[oó]n\s+energ[eé]tica|hidr[oó]geno\s+verde|\bh2v\b|eficiencia\s+energ[eé]tica|electromovilidad|infraestructura\s+verde)\b"),
]
EXCLUDES = [re.compile(r"(?i)\b(clima\s+laboral|clima\s+organizacional|ambiente\s+laboral|aire\s+acondicionado)\b")]
COMPILED = [(name, re.compile(rx)) for name, rx in TAXONOMY]
MASTER = "|".join(f"({rx})" for _, rx in TAXONOMY)


def clean(value):
    if value is None or pd.isna(value): return ""
    return ILLEGAL_CHARACTERS_RE.sub("", str(value)).strip()


def classify(text):
    if not text or any(rx.search(text) for rx in EXCLUDES): return []
    out = []
    for subcat, rx in COMPILED:
        m = rx.search(text)
        if m:
            a, b = max(0, m.start()-40), min(len(text), m.end()+40)
            out.append((subcat, clean(m.group(0)), clean("..." + text[a:b].replace("\n", " ") + "...")))
    return out


def institutional(row):
    org = str(row.get("organismo_comprador", "")).upper()
    sec = str(row.get("sector", "")).upper()
    if "MUNI" in org or "MUNICIPAL" in sec: return "Municipalidades (Gobiernos Locales)"
    if "GOBIERNO REGIONAL" in org or re.search(r"\bGORE\b", org): return "Gobiernos Regionales (GORE)"
    if "UNIVERSIDAD" in org or "EDUCACION" in sec: return "Universidades y Academia"
    if any(k in org for k in ["ARMADA","EJERCITO","FACH","CARABINEROS","PDI","DEFENSA","CAPREDENA","DIPRECA"]): return "Defensa y Fuerzas Armadas"
    if any(k in org for k in ["HOSPITAL","SERVICIO DE SALUD","CESFAM","CENABAST","FONASA"]): return "Sector Salud"
    if any(k in org for k in ["METRO","ENAP","CODELCO","CORREOS","BANCOESTADO","FERROCARRILES","EFE","ASMAR","FAMAE"]): return "Empresas Públicas del Estado"
    return "Gobierno Central y Servicios Públicos"


def mechanism(tipo, codigo):
    cod = str(codigo).upper().strip()
    m = re.search(r"-([A-Z0-9]{2,3})\d*$", cod)
    suf = m.group(1)[:2] if m else ""
    if tipo == "licitacion":
        return "Licitación Privada" if suf in {"CO","B2"} else "Licitación Pública"
    if suf == "AG": return "Compra Ágil (< 30 UTM)"
    if suf in {"CM","CC","CD"}: return "Convenio Marco (Catálogo)"
    if suf in {"TD","E2","SE"}: return "Trato Directo (Excepcional)"
    return "OC Ordinaria / Trato Directo"


def amount_value(v):
    s = "" if v is None else str(v).strip()
    if not s: return None
    if "," in s and "." not in s: s = s.replace(",", ".")
    elif "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    try: return float(s)
    except ValueError: return None


def process_file(path: Path):
    con = duckdb.connect()
    p = str(path).replace(os.sep, "/")
    desc = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{p}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998') LIMIT 0").df()
    cols = list(desc["column_name"])
    def col(*names):
        for n in names:
            for actual in cols:
                if n.lower() == actual.lower(): return f'"{actual}"'
        return "NULL"
    c = {
        "codigo": col("CodigoExterno","Codigo","ID","IDLicitacion"), "link": col("Link"), "nombre": col("Nombre"),
        "desc": col("Descripcion","Descripcion/Obervaciones","Observaciones"), "org": col("NombreOrganismo","OrganismoPublico","Organismo"),
        "unidad": col("NombreUnidad","UnidadCompra","Unidad"), "rut": col("RutUnidad","RutUnidadCompra"), "sector": col("sector","Sector"),
        "region": col("RegionUnidad","RegionUnidadCompra","Region"), "fecha": col("FechaPublicacion","FechaCreacion","FechaEnvio","FechaAceptacion"),
        "monto": col("Monto Estimado Adjudicado","MontoTotalOC_PesosChilenos","MontoTotalOC","TotalNetoOC"), "moneda": col("Moneda Adquisición","TipoMonedaOC","monedaItem"),
        "prov": col("NombreProveedor","RazonSocialProveedor","Proveedor"), "rutprov": col("RutProveedor","CodigoProveedor"),
        "item": col("Descripción línea Adquisición","DescripcionItem","NombreroductoGenerico","EspecificacionComprador","EspecificacionProveedor")
    }
    text = f"COALESCE({c['nombre']}, '') || ' ' || COALESCE({c['desc']}, '') || ' ' || COALESCE({c['item']}, '')"
    tipo = "licitacion" if "lic" in path.name.lower() else "orden_compra"
    q = f"""SELECT '{path.name}' archivo_origen, '{tipo}' tipo_registro, {c['codigo']} codigo_proceso, {c['link']} link,
    {c['nombre']} nombre, {c['desc']} descripcion, {c['org']} organismo_comprador, {c['unidad']} unidad_compra, {c['rut']} rut_comprador,
    {c['sector']} sector, {c['region']} region_comprador, {c['fecha']} fecha, {c['monto']} monto_pesos, {c['moneda']} moneda,
    {c['prov']} proveedor, {c['rutprov']} rut_proveedor, {text} texto_completo
    FROM read_csv_auto('{p}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998')
    WHERE regexp_matches({text}, '{MASTER}', 'i')"""
    return con.execute(q).df()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir", help="Directory containing raw ChileCompra CSV files")
    ap.add_argument("--output-dir", default="output_catastro_reproducido")
    args = ap.parse_args()
    files = [Path(x) for x in sorted(glob.glob(str(Path(args.data_dir)/"*.csv"))) if not Path(x).name.startswith(("manifest","download_log"))]
    out = []
    for i, path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {path.name}")
        try: df = process_file(path)
        except Exception as e:
            print(f"WARN {path.name}: {e}"); continue
        for _, row in df.iterrows():
            text = clean(row.get("texto_completo"))
            for subcat, term, frag in classify(text):
                r = {k: clean(row.get(k)) for k in ["archivo_origen","tipo_registro","codigo_proceso","link","nombre","descripcion","organismo_comprador","unidad_compra","rut_comprador","sector","region_comprador","fecha","monto_pesos","moneda","proveedor","rut_proveedor"]}
                r.update(eje_codigo="P089_CAMBIO_CLIMATICO", eje_nombre="Cambio Climático", subcategoria=subcat, termino_coincidente=term, texto_fragmento=frag)
                r["nivel_institucional"] = institutional(r); r["mecanismo_compra"] = mechanism(r["tipo_registro"], r["codigo_proceso"])
                out.append(r)
    long = pd.DataFrame(out).drop_duplicates(["tipo_registro","codigo_proceso","subcategoria"])
    od = Path(args.output_dir); od.mkdir(parents=True, exist_ok=True)
    long_path = od/"Catastro_Cambio_Climatico_ChileCompra.csv"
    with long_path.open("w", encoding="utf-8-sig", newline="") as fh:
        fh.write("# unit_of_analysis: classification assignment (tipo_registro + codigo_proceso + subcategoria)\n")
        long.to_csv(fh, sep=";", index=False)
    proc = long.sort_values(["tipo_registro","codigo_proceso"]).drop_duplicates(["tipo_registro","codigo_proceso"]).copy()
    cats = long.groupby(["tipo_registro","codigo_proceso"])["subcategoria"].agg(lambda s: " | ".join(sorted(set(s)))).rename("subcategorias")
    terms = long.groupby(["tipo_registro","codigo_proceso"])["termino_coincidente"].agg(lambda s: " | ".join(sorted({x for x in s if x}))).rename("terminos_coincidentes")
    proc = proc.drop(columns=["subcategoria","termino_coincidente","texto_fragmento"], errors="ignore").merge(cats, on=["tipo_registro","codigo_proceso"]).merge(terms, on=["tipo_registro","codigo_proceso"])
    proc["monto_pesos"] = proc["monto_pesos"].map(lambda v: "" if amount_value(v) is None else str(amount_value(v)))
    proc_path = od/"Catastro_Procesos_Unicos_Cambio_Climatico_ChileCompra.csv"
    with proc_path.open("w", encoding="utf-8-sig", newline="") as fh:
        fh.write("# unit_of_analysis: distinct process (tipo_registro + codigo_proceso)\n")
        proc.to_csv(fh, sep=";", index=False)
    print(f"OK long assignments={len(long):,}; distinct processes={len(proc):,}")
    print(long_path); print(proc_path)

if __name__ == "__main__": main()
