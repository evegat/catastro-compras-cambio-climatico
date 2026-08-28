# pipeline_catastro_unificado.py
import os
import sys
import glob
import json
import time
import re
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import duckdb
import pandas as pd
from tqdm import tqdm
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

DATA_DIR = Path("D:/Proyectos/P049 - Compras publicas tecnologicas e IA publica/DataCompleta")
OUT_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output")
CHECKPOINTS_DIR = OUT_DIR / "checkpoints"
PROGRESS_FILE = OUT_DIR / "progreso.json"

CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# TAXONOMÍAS Y EXPRESIONES REGULARES DE LOS 6 EJES
# ---------------------------------------------------------
AXES_CONFIG = {
    "P089_CAMBIO_CLIMATICO": {
        "nombre": "Cambio Climático",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/Catastro_Cambio_Climatico_ChileCompra.xlsx",
        "patterns": [
            ("Nucleo_Exacto", r"(?i)\b(cambio\s+clim[aá]tico|adaptaci[oó]n\s+clim[aá]tica|mitigaci[oó]n\s+clim[aá]tica|resiliencia\s+clim[aá]tica|emergencia\s+clim[aá]tica|acci[oó]n\s+clim[aá]tica)\b"),
            ("Instrumentos_Ley21455", r"(?i)\b(ley\s+(marco\s+de\s+)?cambio\s+clim[aá]tico|ley\s+21\.?455|plan(es)?\s+de\s+acci[oó]n\s+clim[aá]tic[ao]|estrategia\s+clim[aá]tica\s+de\s+largo\s+plazo|\beclp\b|\bpamcc\b|\bparcc\b|plan(es)?\s+de\s+adaptaci[oó]n\s+al\s+cambio\s+clim[aá]tico|planes\s+de\s+acci[oó]n\s+comunal\s+de\s+cambio\s+clim[aá]tico)\b"),
            ("Gases_Descarbonizacion", r"(?i)\b(huella\s+de\s+carbono|descarbonizaci[oó]n|gases?\s+de\s+efecto\s+invernadero|\bgei\b|neutralidad\s+de\s+carbono|carbono\s+neutral(idad)?|bonos?\s+de\s+carbono|cr[eé]ditos?\s+de\s+carbono|mercado\s+de\s+carbono|presupuesto\s+de\s+carbono)\b"),
            ("Transicion_SBN", r"(?i)\b(soluciones?\s+basadas?\s+en\s+la\s+naturaleza|transici[oó]n\s+justa|transici[oó]n\s+energ[eé]tica|hidr[oó]geno\s+verde|\bh2v\b|eficiencia\s+energ[eé]tica|electromovilidad|infraestructura\s+verde)\b"),
        ],
        "exclude_patterns": [
            r"(?i)\b(clima\s+laboral|clima\s+organizacional|ambiente\s+laboral|aire\s+acondicionado)\b"
        ]
    },
    "P049_INTELIGENCIA_ARTIFICIAL": {
        "nombre": "Inteligencia Artificial y Analítica",
        "output_excel": "D:/Proyectos/P049 - Compras publicas tecnologicas e IA publica/Catastro_IA_Tecnologia_ChileCompra.xlsx",
        "patterns": [
            ("IA_MachineLearning", r"(?i)\b(inteligencia\s+artificial|machine\s+learning|aprendizaje\s+autom[aá]tico|aprendizaje\s+de\s+m[aá]quina|deep\s+learning|aprendizaje\s+profundo|red(es)?\s+neuronales?|ia\s+generativa)\b"),
            ("NLP_Vision_LLM", r"(?i)\b(procesamiento\s+de\s+lenguaje\s+natural|\bpln\b|\bnlp\b|visi[oó]n\s+(por\s+computador|artificial)|reconocimiento\s+facial|reconocimiento\s+de\s+patrones|chatbots?|modelos?\s+de\s+lenguaje|\bllm\b|\brag\b|generative\s+ai)\b"),
            ("Analitica_Algoritmos_RPA", r"(?i)\b(anal[ií]tica\s+predictiva|algoritmos?\s+predictivos?|algoritmos?\s+de\s+decisi[oó]n|automatizaci[oó]n\s+rob[oó]tica\s+de\s+procesos|\brpa\b|modelamiento\s+predictivo)\b"),
        ],
        "exclude_patterns": [
            r"(?i)\b(inteligencia\s+militar|inteligencia\s+policial|polic[ií]a\s+de\s+investigaciones)\b"
        ]
    },
    "P036_OPEN_SOURCE": {
        "nombre": "Software Libre y Open Source",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Open_Source_ChileCompra.xlsx",
        "patterns": [
            ("Software_Libre_Codigo_Abierto", r"(?i)\b(software\s+libre|c[oó]digo\s+abierto|open\s+source|\bfloss\b|\bfoss\b|licencias?\s+abiertas?|gnu\s+gpl|licencia\s+mit|apache\s+2\.0)\b"),
            ("Ecosistema_Stack_Abierto", r"(?i)\b(gnu[\/\s]?linux|\blinux\b|\bubuntu\b|\bdebian\b|\bpostgresql\b|\bmariadb\b|\bdocker\b|\bkubernetes\b|\bgithub\b|\bgitlab\b)\b"),
            ("Datos_Estandares_Abiertos", r"(?i)\b(est[aá]ndares?\s+abiertos?|datos\s+abiertos|open\s+data|api\s+abierta|interoperabilidad\s+abierta)\b"),
        ],
        "exclude_patterns": []
    },
    "P005_TRANSFORMACION_DIGITAL": {
        "nombre": "Transformación Digital del Estado",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Transformacion_Digital_ChileCompra.xlsx",
        "patterns": [
            ("Marco_Ley21180_GobDigital", r"(?i)\b(ley\s+(de\s+)?transformaci[oó]n\s+digital|ley\s+21\.?180|gobierno\s+digital|divisi[oó]n\s+de\s+gobierno\s+digital|\bdgd\b)\b"),
            ("CeroPapel_Tramites", r"(?i)\b(cero\s+papel|gesti[oó]n\s+documental|\bdocdigital\b|firma\s+electr[oó]nica\s+(avanzada)?|\bfea\b|clave\s+[uú]nica|digitalizaci[oó]n\s+de\s+tr[aá]mites|ventanilla\s+[uú]nica\s+digital)\b"),
            ("Interoperabilidad_BPM", r"(?i)\b(interoperabilidad|plataforma\s+de\s+integraci[oó]n\s+de\s+servicios|\bpis\b|\bbpm\b|\bbpmn\b|redise[nñ]o\s+de\s+procesos)\b"),
        ],
        "exclude_patterns": []
    },
    "P080_CIBERSEGURIDAD": {
        "nombre": "Ciberseguridad y Continuidad Operacional",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Ciberseguridad_ChileCompra.xlsx",
        "patterns": [
            ("Ciberseguridad_Ley21663", r"(?i)\b(ciberseguridad|seguridad\s+de\s+la\s+informaci[oó]n|ley\s+(marco\s+de\s+)?ciberseguridad|ley\s+21\.?663|\bcsirt\b|\banci\b|iso\s*27001|\bnist\b)\b"),
            ("SOC_Auditoria_Vulnerabilidades", r"(?i)\b(centro\s+de\s+operaciones\s+de\s+seguridad|security\s+operations\s+center|\bsoc\s+(de\s+)?(ciberseguridad|seguridad)|\bservicio(s)?\s+soc\b|\bsiem\b|hacking\s+[eé]tico|pentesting|an[aá]lisis\s+de\s+vulnerabilidades|amenazas?\s+cibern[eé]ticas?)\b"),
            ("Continuidad_Operacional_DRP", r"(?i)\b(continuidad\s+operacional|continuidad\s+operativa|disaster\s+recovery|recuperaci[oó]n\s+ante\s+desastres|plan(es)?\s+de\s+continuidad|alta\s+disponibilidad|respaldo\s+y\s+recuperaci[oó]n)\b"),
        ],
        "exclude_patterns": []
    },
    "P087_DATOS_PERSONALES": {
        "nombre": "Protección de Datos Personales",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Datos_Personales_ChileCompra.xlsx",
        "patterns": [
            ("Normativa_Ley19628", r"(?i)\b(datos\s+personales|protecci[oó]n\s+de\s+datos|ley\s+19\.?628|agencia\s+de\s+protecci[oó]n\s+de\s+datos|\bgdpr\b|\brgpd\b|oficial\s+de\s+protecci[oó]n\s+de\s+datos|\bdpo\b)\b"),
            ("Tratamiento_Privacidad", r"(?i)\b(datos\s+sensibles|consentimiento\s+informado|anonimizaci[oó]n|seudonimizaci[oó]n|evaluaci[oó]n\s+de\s+impacto\s+en\s+privacidad|\beipd\b|privacidad\s+desde\s+el\s+dise[nñ]o)\b"),
        ],
        "exclude_patterns": []
    }
}

COMPILED_AXES = {}
ALL_PATTERNS_LIST = []
for eje, conf in AXES_CONFIG.items():
    compiled_patterns = [(subcat, re.compile(pat)) for subcat, pat in conf["patterns"]]
    compiled_excludes = [re.compile(pat) for pat in conf.get("exclude_patterns", [])]
    COMPILED_AXES[eje] = {
        "nombre": conf["nombre"],
        "output_excel": conf["output_excel"],
        "patterns": compiled_patterns,
        "excludes": compiled_excludes
    }
    for subcat, pat in conf["patterns"]:
        ALL_PATTERNS_LIST.append(pat)

MASTER_REGEX = "|".join(f"({p})" for p in ALL_PATTERNS_LIST)

def clean_string(val):
    if val is None or pd.isna(val):
        return ""
    val_str = str(val)
    val_str = ILLEGAL_CHARACTERS_RE.sub("", val_str)
    val_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', val_str)
    return val_str.strip()

def classify_text(text):
    matches = []
    if not text or not isinstance(text, str):
        return matches
        
    for eje, data in COMPILED_AXES.items():
        if any(rx_ex.search(text) for rx_ex in data["excludes"]):
            continue
            
        for subcat, rx in data["patterns"]:
            m = rx.search(text)
            if m:
                matched_term = m.group(0)
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                fragmento = "..." + text[start:end].replace("\n", " ").replace("\r", " ") + "..."
                matches.append({
                    "eje_codigo": eje,
                    "eje_nombre": data["nombre"],
                    "subcategoria": subcat,
                    "termino_coincidente": clean_string(matched_term),
                    "texto_fragmento": clean_string(fragmento)
                })
    return matches

def process_single_file(filepath_str):
    filepath = Path(filepath_str)
    fname = filepath.name
    chk_file = CHECKPOINTS_DIR / f"{fname}.json"
    
    # Validar checkpoint existente
    if chk_file.exists():
        try:
            with open(chk_file, "r", encoding="utf-8") as f:
                items = json.load(f)
            return {"fname": fname, "items": items, "cached": True}
        except Exception:
            pass
            
    is_lic = "lic" in fname.lower()
    chk_items = []
    
    try:
        con = duckdb.connect()
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
                classifications = classify_text(full_text)
                for cl in classifications:
                    item_dict = {
                        "archivo_origen": clean_string(row["archivo_origen"]),
                        "tipo_registro": clean_string(row["tipo_registro"]),
                        "codigo_proceso": clean_string(row["codigo_proceso"]),
                        "link": clean_string(row["link"]),
                        "nombre": clean_string(row["nombre"]),
                        "descripcion": clean_string(row["descripcion"]),
                        "organismo_comprador": clean_string(row["organismo_comprador"]),
                        "unidad_compra": clean_string(row["unidad_compra"]),
                        "rut_comprador": clean_string(row["rut_comprador"]),
                        "sector": clean_string(row["sector"]),
                        "region_comprador": clean_string(row["region_comprador"]),
                        "fecha": clean_string(row["fecha"]),
                        "monto_pesos": clean_string(row["monto_pesos"]),
                        "moneda": clean_string(row["moneda"]),
                        "proveedor": clean_string(row["proveedor"]),
                        "rut_proveedor": clean_string(row["rut_proveedor"]),
                        "eje_codigo": cl["eje_codigo"],
                        "eje_nombre": cl["eje_nombre"],
                        "subcategoria": cl["subcategoria"],
                        "termino_coincidente": cl["termino_coincidente"],
                        "texto_fragmento": cl["texto_fragmento"]
                    }
                    chk_items.append(item_dict)
                    
        # Escritura atómica a checkpoint
        tmp_chk = chk_file.with_suffix(".tmp")
        with open(tmp_chk, "w", encoding="utf-8") as f:
            json.dump(chk_items, f, ensure_ascii=False)
        if tmp_chk.exists():
            tmp_chk.replace(chk_file)
            
    except Exception as e:
        pass
        
    return {"fname": fname, "items": chk_items, "cached": False}

def update_progress(data):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def process_all_files():
    workers = min(16, (os.cpu_count() or 4))
    print("=" * 80)
    print(f" PIPELINE UNIFICADO CHILECOMPRA (2007-2026) — MODO MULTINÚCLEO ({workers} HILOS)")
    print("=" * 80)
    
    all_csvs = sorted(glob.glob(str(DATA_DIR / "*.csv")))
    data_files = [f for f in all_csvs if not Path(f).name.startswith("manifest") and not Path(f).name.startswith("download_log")]
    
    total_files = len(data_files)
    print(f"Total de archivos CSV: {total_files}")
    
    accumulated_results = {eje: [] for eje in AXES_CONFIG.keys()}
    t0_global = time.time()
    
    progress_info = {
        "status": "procesando_multiproceso",
        "workers": workers,
        "total_archivos": total_files,
        "archivos_procesados": 0,
        "archivo_actual": "",
        "porcentaje": 0.0,
        "matches_por_eje": {eje: 0 for eje in AXES_CONFIG.keys()},
        "tiempo_transcurrido_seg": 0,
        "inicio": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    update_progress(progress_info)
    
    completed_count = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_file = {executor.submit(process_single_file, f): f for f in data_files}
        
        with tqdm(total=total_files, desc="Escaneo paralelo masivo", unit="archivo") as pbar:
            for future in as_completed(future_to_file):
                completed_count += 1
                try:
                    res = future.result()
                    for item in res["items"]:
                        accumulated_results[item["eje_codigo"]].append(item)
                    
                    progress_info["archivos_procesados"] = completed_count
                    progress_info["archivo_actual"] = res["fname"]
                    progress_info["porcentaje"] = round(completed_count / total_files * 100, 2)
                    progress_info["tiempo_transcurrido_seg"] = round(time.time() - t0_global, 1)
                    progress_info["matches_por_eje"] = {eje: len(r) for eje, r in accumulated_results.items()}
                    
                    if completed_count % 5 == 0 or completed_count == total_files:
                        update_progress(progress_info)
                        
                    pbar.update(1)
                    pbar.set_postfix({
                        "Clima": len(accumulated_results["P089_CAMBIO_CLIMATICO"]),
                        "IA": len(accumulated_results["P049_INTELIGENCIA_ARTIFICIAL"]),
                        "TD": len(accumulated_results["P005_TRANSFORMACION_DIGITAL"])
                    })
                except Exception as e:
                    pbar.update(1)
                    
    print("\n" + "=" * 80)
    print(" EXTRACCIÓN PARALELA COMPLETADA. CONSOLIDANDO ENTREGABLES EN EXCEL...")
    print("=" * 80)
    
    for eje, data in COMPILED_AXES.items():
        results = accumulated_results[eje]
        output_file = Path(data["output_excel"])
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\nGenerando Excel para: {data['nombre']} ({len(results):,} registros)...")
        
        if results:
            df_eje = pd.DataFrame(results)
            df_eje = df_eje.drop_duplicates(subset=["codigo_proceso", "subcategoria", "tipo_registro"])
            
            for col in df_eje.columns:
                if df_eje[col].dtype == "object":
                    df_eje[col] = df_eje[col].apply(clean_string)
                    
            with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                df_eje.to_excel(writer, sheet_name="Catastro Completo", index=False)
                resumen_subcat = df_eje.groupby(["subcategoria", "tipo_registro"]).size().reset_index(name="Total Procesos")
                resumen_subcat.to_excel(writer, sheet_name="Resumen Subcategorias", index=False)
                resumen_org = df_eje.groupby("organismo_comprador").size().reset_index(name="Total Procesos").sort_values(by="Total Procesos", ascending=False).head(50)
                resumen_org.to_excel(writer, sheet_name="Top 50 Organismos", index=False)
                resumen_terminos = df_eje.groupby(["subcategoria", "termino_coincidente"]).size().reset_index(name="Frecuencia").sort_values(by="Frecuencia", ascending=False).head(100)
                resumen_terminos.to_excel(writer, sheet_name="Terminos Gatillantes", index=False)
                
            print(f" -> Guardado exitosamente: {output_file}")
        else:
            print(f" -> Sin registros para este eje.")
            
    progress_info["status"] = "completado"
    progress_info["porcentaje"] = 100.0
    progress_info["tiempo_total_seg"] = round(time.time() - t0_global, 1)
    update_progress(progress_info)
    print("\n" + "=" * 80)
    print(" PROCESO FINALIZADO CON ÉXITO.")
    print("=" * 80)

if __name__ == "__main__":
    process_all_files()
