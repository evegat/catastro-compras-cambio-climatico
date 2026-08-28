"""
====================================================================================================
PIPELINE DE REPRODUCIBILIDAD Y EXTRACCIÓN DETERMINISTA: CATASTRO DE COMPRAS PÚBLICAS EN CAMBIO CLIMÁTICO
====================================================================================================
Autor / Data Architect: Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)
Contacto: evega.ap@gmail.com
Proyecto: P089 - Catastro Nacional de Compras Públicas en Cambio Climático de Chile
Cobertura: Enero 2007 a Julio 2026 (470 bases masivas de ChileCompra / Mercado Público)
Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0)

OBJETIVO DEL SCRIPT:
Permitir que cualquier investigador, analista o evaluador replique desde cero, de forma 100% manual,
transparente y determinista (sin modelos de lenguaje opacos ni cajas negras de IA), la extracción,
clasificación taxonómica y consolidación de las 9.086 compras y licitaciones del Estado de Chile.

REQUISITOS DE EJECUCIÓN:
1. Python 3.10 o superior instalado.
2. Librerías requeridas (instalar vía pip):
   pip install duckdb pandas openpyxl tqdm

INSTRUCCIONES DE USO:
1. Descargue las bases mensuales de licitaciones y órdenes de compra desde:
   https://datosabiertos.chilecompra.cl/ (o el contenedor oficial de ChileCompra).
2. Coloque los archivos descomprimidos (.csv) en una carpeta local (por defecto ./data/ o configure DATA_DIR).
3. Ejecute este script:
   python replicar_catastro_chilecompra.py
====================================================================================================
"""

import os
import sys
import glob
import re
from pathlib import Path
import duckdb
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# --------------------------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS Y DIRECTORIOS
# --------------------------------------------------------------------------------------------------
# Modifique DATA_DIR según la ubicación donde tenga sus archivos CSV descargados de ChileCompra
DATA_DIR = Path("D:/Proyectos/P049 - Compras publicas tecnologicas e IA publica/DataCompleta")
OUTPUT_DIR = Path("./output_catastro_reproducido")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXCEL_OUTPUT = OUTPUT_DIR / "Catastro_Cambio_Climatico_ChileCompra_Replicado.xlsx"
CSV_OUTPUT = OUTPUT_DIR / "Catastro_Cambio_Climatico_ChileCompra_Replicado.csv"

# --------------------------------------------------------------------------------------------------
# 2. TAXONOMÍA LÉXICA Y EXPRESIONES REGULARES DE CLASIFICACIÓN
# --------------------------------------------------------------------------------------------------
# Se definen 4 subcategorías conceptuales con sus respectivos patrones de búsqueda regex
TAXONOMIA_PATRONES = [
    (
        "Nucleo_Exacto",
        r"(?i)\b(cambio\s+clim[aá]tico|adaptaci[oó]n\s+clim[aá]tica|mitigaci[oó]n\s+clim[aá]tica|resiliencia\s+clim[aá]tica|emergencia\s+clim[aá]tica|acci[oó]n\s+clim[aá]tica)\b"
    ),
    (
        "Instrumentos_Ley21455",
        r"(?i)\b(ley\s+(marco\s+de\s+)?cambio\s+clim[aá]tico|ley\s+21\.?455|plan(es)?\s+de\s+acci[oó]n\s+clim[aá]tic[ao]|estrategia\s+clim[aá]tica\s+de\s+largo\s+plazo|\beclp\b|\bpamcc\b|\bparcc\b|plan(es)?\s+de\s+adaptaci[oó]n\s+al\s+cambio\s+clim[aá]tico|planes\s+de\s+acci[oó]n\s+comunal\s+de\s+cambio\s+clim[aá]tico)\b"
    ),
    (
        "Gases_Descarbonizacion",
        r"(?i)\b(huella\s+de\s+carbono|descarbonizaci[oó]n|gases?\s+de\s+efecto\s+invernadero|\bgei\b|neutralidad\s+de\s+carbono|carbono\s+neutral(idad)?|bonos?\s+de\s+carbono|cr[eé]ditos?\s+de\s+carbono|mercado\s+de\s+carbono|presupuesto\s+de\s+carbono)\b"
    ),
    (
        "Transicion_SBN",
        r"(?i)\b(soluciones?\s+basadas?\s+en\s+la\s+naturaleza|transici[oó]n\s+justa|transici[oó]n\s+energ[eé]tica|hidr[oó]geno\s+verde|\bh2v\b|eficiencia\s+energ[eé]tica|electromovilidad|infraestructura\s+verde)\b"
    )
]

# Exclusiones negativas obligatorias para control de falsos positivos en compras públicas chilenas
PATRONES_EXCLUSION = [
    r"(?i)\b(clima\s+laboral|clima\s+organizacional|ambiente\s+laboral|aire\s+acondicionado)\b"
]

# Compilación de expresiones regulares para máxima velocidad de ejecución
COMPILED_PATTERNS = [(subcat, re.compile(pat)) for subcat, pat in TAXONOMIA_PATRONES]
COMPILED_EXCLUDES = [re.compile(pat) for pat in PATRONES_EXCLUSION]
MASTER_REGEX = "|".join(f"({pat})" for _, pat in TAXONOMIA_PATRONES)

# --------------------------------------------------------------------------------------------------
# 3. FUNCIONES DE LIMPIEZA Y CLASIFICACIÓN
# --------------------------------------------------------------------------------------------------
def sanitizar_texto(val):
    """Elimina caracteres de control no imprimibles y sanitiza strings para Excel."""
    if val is None or pd.isna(val):
        return ""
    val_str = str(val)
    val_str = ILLEGAL_CHARACTERS_RE.sub("", val_str)
    val_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', val_str)
    return val_str.strip()

def clasificar_texto(texto):
    """
    Analiza un texto concatenado (Nombre + Descripción + Especificaciones),
    valida que no contenga términos excluidos y extrae los fragmentos coincidentes.
    """
    matches = []
    if not texto or not isinstance(texto, str):
        return matches
        
    # Descarte si contiene términos prohibidos (falsos positivos)
    if any(rx_ex.search(texto) for rx_ex in COMPILED_EXCLUDES):
        return matches
        
    for subcat, rx in COMPILED_PATTERNS:
        m = rx.search(texto)
        if m:
            matched_term = m.group(0)
            start = max(0, m.start() - 40)
            end = min(len(texto), m.end() + 40)
            fragmento = "..." + texto[start:end].replace("\n", " ").replace("\r", " ") + "..."
            matches.append({
                "subcategoria": subcat,
                "termino_coincidente": sanitizar_texto(matched_term),
                "texto_fragmento": sanitizar_texto(fragmento)
            })
    return matches

def clasificar_nivel_institucional(row):
    """
    Asigna la categoría de gobernanza según el nombre de la institución y el sector:
    - Municipalidades (Gobiernos Locales)
    - Gobiernos Regionales (GOREs)
    - Gobierno Central y Servicios Públicos
    - Universidades y Centros Académicos
    - Sector Salud
    - Defensa y Fuerzas Armadas
    - Empresas Públicas del Estado
    """
    org = str(row.get('organismo_comprador', '')).upper()
    sec = str(row.get('sector', '')).upper() if pd.notnull(row.get('sector')) else ''
    
    if 'MUNI' in org or 'MUNICIPAL' in sec or 'ILUSTRE MUNICIPALIDAD' in org:
        return 'Municipalidades (Gobiernos Locales)'
    elif 'GOBIERNO REGIONAL' in org or 'GORE' in org or 'G.R.' in org:
        return 'Gobiernos Regionales (GORE)'
    elif 'UNIVERSIDAD' in org or 'EDUCACION' in sec or 'CENTRO DE FORMACION' in org or 'INSTITUTO PROFESIONAL' in org:
        return 'Universidades y Academia'
    elif any(k in org for k in ['ARMADA', 'EJERCITO', 'FACH', 'CARABINEROS', 'PDI', 'DEFENSA', 'CAPREDENA', 'DIPRECA']):
        return 'Defensa y Fuerzas Armadas'
    elif any(k in org for k in ['HOSPITAL', 'SALUD', 'SERVICIO DE SALUD', 'CESFAM', 'CENABAST', 'FONASA', 'ISP']):
        return 'Sector Salud'
    elif any(k in org for k in ['EMPRESA', 'METRO', 'ENAP', 'CODELCO', 'CORREOS', 'BANCOESTADO', 'CASA DE MONEDA', 'FERROCARRILES', 'EFE', 'PUERTO', 'ASMAR', 'FAMAE']):
        return 'Empresas Públicas del Estado'
    else:
        return 'Gobierno Central y Servicios Públicos'

# --------------------------------------------------------------------------------------------------
# 4. MOTOR PRINCIPAL DE PROCESAMIENTO
# --------------------------------------------------------------------------------------------------
def procesar_archivos():
    print("=" * 80)
    print(" INICIANDO EXTRACCIÓN DETERMINISTA DE COMPRAS PÚBLICAS EN CAMBIO CLIMÁTICO")
    print("=" * 80)
    
    all_csvs = sorted(glob.glob(str(DATA_DIR / "*.csv")))
    data_files = [f for f in all_csvs if not Path(f).name.startswith("manifest") and not Path(f).name.startswith("download_log")]
    
    print(f"Total de archivos CSV a procesar: {len(data_files)}")
    if not data_files:
        print(f"ERROR: No se encontraron archivos CSV en {DATA_DIR}. Verifique la ruta.")
        return
        
    con = duckdb.connect()
    resultados_acumulados = []
    
    for idx, filepath_str in enumerate(data_files, 1):
        fname = Path(filepath_str).name
        is_lic = "lic" in fname.lower()
        print(f"[{idx}/{len(data_files)}] Analizando: {fname}...")
        
        try:
            # Inspeccionar esquema de columnas dinámicamente
            cols_df = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{filepath_str.replace(os.sep, '/')}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998') LIMIT 0").df()
            cols = list(cols_df["column_name"])
            
            def get_col(candidates):
                for c in candidates:
                    for actual in cols:
                        if c.lower() == actual.lower():
                            return f'"{actual}"'
                return "NULL"
                
            col_codigo = get_col(["CodigoExterno", "Codigo", "ID", "IDLicitacion"])
            col_link = get_col(["Link"])
            col_nombre = get_col(["Nombre"])
            col_desc = get_col(["Descripcion", "Descripcion/Obervaciones", "Observaciones"])
            col_org = get_col(["NombreOrganismo", "OrganismoPublico", "Organismo"])
            col_unidad = get_col(["NombreUnidad", "UnidadCompra", "Unidad"])
            col_rut_unidad = get_col(["RutUnidad", "RutUnidadCompra"])
            col_sector = get_col(["sector", "Sector"])
            col_region = get_col(["RegionUnidad", "RegionUnidadCompra", "Region"])
            col_fecha = get_col(["FechaPublicacion", "FechaCreacion", "FechaEnvio", "FechaAceptacion"])
            col_monto_pesos = get_col(["Monto Estimado Adjudicado", "MontoTotalOC_PesosChilenos", "MontoTotalOC", "TotalNetoOC"])
            col_moneda = get_col(["Moneda Adquisición", "TipoMonedaOC", "monedaItem"])
            col_proveedor = get_col(["NombreProveedor", "RazonSocialProveedor", "Proveedor"])
            col_rut_prov = get_col(["RutProveedor", "CodigoProveedor"])
            col_item_desc = get_col(["Descripción línea Adquisición", "DescripcionItem", "NombreroductoGenerico", "EspecificacionComprador", "EspecificacionProveedor"])
            
            text_concat = f"COALESCE({col_nombre}, '') || ' ' || COALESCE({col_desc}, '') || ' ' || COALESCE({col_item_desc}, '')"
            
            query = f"""
                SELECT 
                    '{fname}' as archivo_origen,
                    '{'licitacion' if is_lic else 'orden_compra'}' as tipo_registro,
                    {col_codigo} as codigo_proceso,
                    {col_link} as link,
                    {col_nombre} as nombre,
                    {col_desc} as descripcion,
                    {col_org} as organismo_comprador,
                    {col_unidad} as unidad_compra,
                    {col_rut_unidad} as rut_comprador,
                    {col_sector} as sector,
                    {col_region} as region_comprador,
                    {col_fecha} as fecha,
                    {col_monto_pesos} as monto_pesos,
                    {col_moneda} as moneda,
                    {col_proveedor} as proveedor,
                    {col_rut_prov} as rut_proveedor,
                    {text_concat} as texto_completo
                FROM read_csv_auto('{filepath_str.replace(os.sep, '/')}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998')
                WHERE regexp_matches({text_concat}, '{MASTER_REGEX}', 'i')
            """
            
            df_matches = con.execute(query).df()
            if not df_matches.empty:
                for _, row in df_matches.iterrows():
                    full_text = str(row["texto_completo"]) if pd.notnull(row["texto_completo"]) else ""
                    classifications = clasificar_texto(full_text)
                    for cl in classifications:
                        resultados_acumulados.append({
                            "archivo_origen": sanitizar_texto(row["archivo_origen"]),
                            "tipo_registro": sanitizar_texto(row["tipo_registro"]),
                            "codigo_proceso": sanitizar_texto(row["codigo_proceso"]),
                            "link": sanitizar_texto(row["link"]),
                            "nombre": sanitizar_texto(row["nombre"]),
                            "descripcion": sanitizar_texto(row["descripcion"]),
                            "organismo_comprador": sanitizar_texto(row["organismo_comprador"]),
                            "unidad_compra": sanitizar_texto(row["unidad_compra"]),
                            "rut_comprador": sanitizar_texto(row["rut_comprador"]),
                            "sector": sanitizar_texto(row["sector"]),
                            "region_comprador": sanitizar_texto(row["region_comprador"]),
                            "fecha": sanitizar_texto(row["fecha"]),
                            "monto_pesos": sanitizar_texto(row["monto_pesos"]),
                            "moneda": sanitizar_texto(row["moneda"]),
                            "proveedor": sanitizar_texto(row["proveedor"]),
                            "rut_proveedor": sanitizar_texto(row["rut_proveedor"]),
                            "eje_codigo": "P089_CAMBIO_CLIMATICO",
                            "eje_nombre": "Cambio Climático",
                            "subcategoria": cl["subcategoria"],
                            "termino_coincidente": cl["termino_coincidente"],
                            "texto_fragmento": cl["texto_fragmento"]
                        })
        except Exception as e:
            print(f"  [AVISO] Error procesando {fname}: {e}")
            
    print(f"\nTotal registros brutos extraídos: {len(resultados_acumulados):,}")
    
    # ----------------------------------------------------------------------------------------------
    # 5. DEDUPLICACIÓN Y ESTRUCTURACIÓN DE ENTREGABLES
    # ----------------------------------------------------------------------------------------------
    df_final = pd.DataFrame(resultados_acumulados)
    
    # Deduplicación por clave compuesta
    df_final = df_final.drop_duplicates(subset=["codigo_proceso", "subcategoria", "tipo_registro"])
    print(f"Total registros únicos tras deduplicación: {len(df_final):,}")
    
    # Asignar nivel institucional
    df_final["nivel_institucional"] = df_final.apply(clasificar_nivel_institucional, axis=1)
    
    # Exportar a CSV delimitado por punto y coma (UTF-8 con BOM)
    with open(CSV_OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        f.write("# dataset_id: P089_EVT_CHILECOMPRA_2007_2026\n")
        f.write("# data_architect: Eduardo Vega Toledo (evega.ap@gmail.com)\n")
        f.write("# project: P089 - Catastro Cambio Climatico Chile\n")
        df_final.to_csv(f, sep=";", index=False)
    print(f"[OK] Archivo CSV generado en: {CSV_OUTPUT}")
    
    # Exportar a Excel con pestañas de análisis
    with pd.ExcelWriter(EXCEL_OUTPUT, engine="openpyxl") as writer:
        # Pestaña 1: Portada
        meta_df = pd.DataFrame([
            ["PROYECTO", "P089 - Catastro Histórico de Compras Públicas en Cambio Climático de Chile"],
            ["COBERTURA TEMPORAL", "Enero 2007 a Julio 2026 (470 bases masivas de Mercado Público)"],
            ["TOTAL REGISTROS ÚNICOS", f"{len(df_final):,} procesos"],
            ["DISEÑO DE PIPELINE Y AUTORÍA", "Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)"],
            ["CONTACTO", "evega.ap@gmail.com"],
            ["LICENCIA", "Creative Commons Attribution 4.0 International (CC BY 4.0)"]
        ], columns=["METADATO", "VALOR"])
        meta_df.to_excel(writer, sheet_name="Ficha Técnica y Autoría", index=False)
        
        # Pestaña 2: Base Completa
        df_final.to_excel(writer, sheet_name="Catastro Completo", index=False)
        
        # Pestaña 3: Resumen Nivel Institucional
        resumen_nivel = df_final.groupby(["nivel_institucional", "tipo_registro"]).agg(
            total_procesos=("codigo_proceso", "count"),
            monto_millones=("monto_pesos", lambda x: round(pd.to_numeric(x, errors="coerce").fillna(0).sum() / 1e6, 2))
        ).reset_index()
        resumen_nivel.to_excel(writer, sheet_name="Resumen Nivel Institucional", index=False)
        
        # Pestaña 4: Resumen Subcategorías
        resumen_sub = df_final.groupby(["subcategoria", "tipo_registro"]).size().reset_index(name="Total Procesos")
        resumen_sub.to_excel(writer, sheet_name="Resumen Subcategorias", index=False)
        
        # Pestaña 5: Detalle GOREs
        gore_df = df_final[df_final["nivel_institucional"] == "Gobiernos Regionales (GORE)"].groupby(["organismo_comprador", "subcategoria"]).agg(
            total_procesos=("codigo_proceso", "count"),
            monto_millones=("monto_pesos", lambda x: round(pd.to_numeric(x, errors="coerce").fillna(0).sum() / 1e6, 2))
        ).reset_index().sort_values(by="total_procesos", ascending=False)
        gore_df.to_excel(writer, sheet_name="Detalle GOREs", index=False)
        
        # Pestaña 6: Top 50 Organismos
        top_org = df_final.groupby(["nivel_institucional", "organismo_comprador"]).size().reset_index(name="Total Procesos").sort_values(by="Total Procesos", ascending=False).head(50)
        top_org.to_excel(writer, sheet_name="Top 50 Organismos", index=False)
        
        # Pestaña 7: Términos Gatillantes
        terms = df_final.groupby(["subcategoria", "termino_coincidente"]).size().reset_index(name="Frecuencia").sort_values(by="Frecuencia", ascending=False).head(100)
        terms.to_excel(writer, sheet_name="Terminos Gatillantes", index=False)
        
    print(f"[OK] Archivo Excel generado en: {EXCEL_OUTPUT}")
    print("\n================================================================================")
    print(" REPLICACIÓN DETERMINISTA COMPLETADA CON ÉXITO.")
    print("================================================================================")

if __name__ == "__main__":
    procesar_archivos()
