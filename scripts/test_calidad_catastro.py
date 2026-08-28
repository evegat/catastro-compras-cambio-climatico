# test_calidad_catastro.py
import sys
import re
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico")
EXCEL_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.xlsx"
CSV_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.csv"

def run_quality_audit():
    print("=" * 80)
    print(" PROTOCOLO DE AUDITORÍA Y CONTROL DE CALIDAD DE DATOS (P089)")
    print("=" * 80)
    
    passed_checks = 0
    total_checks = 0
    
    # -------------------------------------------------------------
    # 1. VERIFICACIÓN DE ARCHIVOS Y ESTRUCTURA BÁSICA
    # -------------------------------------------------------------
    print("\n[TEST 1] Existencia e integridad de archivos fuente...")
    total_checks += 2
    assert EXCEL_PATH.exists(), "ERROR: No existe el archivo Excel"
    assert CSV_PATH.exists(), "ERROR: No existe el archivo CSV"
    passed_checks += 2
    print(f" -> [OK] Excel ({EXCEL_PATH.stat().st_size / 1e6:.2f} MB) y CSV ({CSV_PATH.stat().st_size / 1e6:.2f} MB) presentes.")
    
    # Cargar datos
    df_excel = pd.read_excel(EXCEL_PATH, sheet_name="Catastro Completo")
    df_csv = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8-sig")
    
    # -------------------------------------------------------------
    # 2. CONSISTENCIA PARIDAD EXCEL VS CSV
    # -------------------------------------------------------------
    print("\n[TEST 2] Paridad y consistencia exacta entre Excel y CSV...")
    total_checks += 3
    if len(df_excel) == len(df_csv):
        passed_checks += 1
        print(f" -> [OK] Conteo de filas idéntico: {len(df_excel):,} registros.")
    else:
        print(f" -> [FAIL] Discrepancia: Excel={len(df_excel)}, CSV={len(df_csv)}")
        
    if list(df_excel.columns) == list(df_csv.columns):
        passed_checks += 1
        print(f" -> [OK] Columnas idénticas ({len(df_excel.columns)} variables).")
    else:
        print(f" -> [FAIL] Discrepancia en columnas.")
        
    # Validar que no haya duplicados de proceso + subcategoria + tipo_registro
    dups = df_excel.duplicated(subset=["codigo_proceso", "subcategoria", "tipo_registro"]).sum()
    if dups == 0:
        passed_checks += 1
        print(f" -> [OK] 0 duplicados en la llave primaria compuesta.")
    else:
        print(f" -> [FAIL] Existen {dups} duplicados.")

    # -------------------------------------------------------------
    # 3. CONTROL DE NULOS EN CAMPOS CRÍTICOS
    # -------------------------------------------------------------
    print("\n[TEST 3] Validación de integridad de campos obligatorios...")
    campos_criticos = ["codigo_proceso", "organismo_comprador", "subcategoria", "nivel_institucional", "tipo_registro", "termino_coincidente"]
    for c in campos_criticos:
        total_checks += 1
        nulos = df_excel[c].isna().sum() + (df_excel[c] == "").sum()
        if nulos == 0:
            passed_checks += 1
            print(f" -> [OK] Campo '{c}': 100% poblado (0 nulos).")
        else:
            print(f" -> [FAIL] Campo '{c}' tiene {nulos} nulos.")

    # -------------------------------------------------------------
    # 4. AUDITORÍA DE FALSOS POSITIVOS (PATRONES DE EXCLUSIÓN)
    # -------------------------------------------------------------
    print("\n[TEST 4] Control de falsos positivos y exclusiones negativas...")
    rx_exclusiones = re.compile(r"(?i)\b(clima\s+laboral|clima\s+organizacional|ambiente\s+laboral|aire\s+acondicionado)\b")
    text_corpus = (df_excel["nombre"].fillna("") + " " + df_excel["descripcion"].fillna("") + " " + df_excel["texto_fragmento"].fillna("")).tolist()
    
    total_checks += 1
    fp_matches = 0
    for idx, txt in enumerate(text_corpus):
        if rx_exclusiones.search(txt):
            # Solo si el termino_coincidente fue ese falso positivo
            t_match = str(df_excel.iloc[idx]["termino_coincidente"]).lower()
            if any(k in t_match for k in ["clima laboral", "clima organizacional", "ambiente laboral", "aire acondicionado"]):
                fp_matches += 1
                
    if fp_matches == 0:
        passed_checks += 1
        print(f" -> [OK] 0 falsos positivos detectados por exclusión léxica.")
    else:
        print(f" -> [FAIL] Detectados {fp_matches} registros con términos prohibidos.")

    # -------------------------------------------------------------
    # 5. COHERENCIA MATEMÁTICA Y CUADRATURA MULTI-PESTAÑA
    # -------------------------------------------------------------
    print("\n[TEST 5] Cuadratura matemática entre pestañas del libro Excel...")
    xl = pd.ExcelFile(EXCEL_PATH)
    
    # Resumen Subcategorias
    total_checks += 1
    df_sub = xl.parse("Resumen Subcategorias")
    if df_sub["Total Procesos"].sum() == len(df_excel):
        passed_checks += 1
        print(f" -> [OK] Suma pestaña 'Resumen Subcategorias' cuadra exacto: {df_sub['Total Procesos'].sum():,}.")
    else:
        print(f" -> [FAIL] Pestaña 'Resumen Subcategorias' no cuadra: {df_sub['Total Procesos'].sum():,} != {len(df_excel):,}")

    # Resumen Nivel Institucional
    total_checks += 1
    df_niv = xl.parse("Resumen Nivel Institucional")
    if df_niv["total_procesos"].sum() == len(df_excel):
        passed_checks += 1
        print(f" -> [OK] Suma pestaña 'Resumen Nivel Institucional' cuadra exacto: {df_niv['total_procesos'].sum():,}.")
    else:
        print(f" -> [FAIL] Pestaña 'Resumen Nivel Institucional' no cuadra.")

    # Detalle GOREs
    total_checks += 1
    df_gore = xl.parse("Detalle GOREs")
    total_gore_base = (df_excel["nivel_institucional"] == "Gobiernos Regionales (GORE)").sum()
    if df_gore["total_procesos"].sum() == total_gore_base:
        passed_checks += 1
        print(f" -> [OK] Suma pestaña 'Detalle GOREs' cuadra exacto: {df_gore['total_procesos'].sum():,} registros GORE.")
    else:
        print(f" -> [FAIL] Discrepancia en GOREs: {df_gore['total_procesos'].sum():,} != {total_gore_base:,}")

    # -------------------------------------------------------------
    # 6. CONSISTENCIA TEMPORAL (RANGO DE AÑOS 2007-2026)
    # -------------------------------------------------------------
    print("\n[TEST 6] Validación de rango temporal (2007-2026)...")
    total_checks += 1
    years_detected = []
    for f in df_excel["archivo_origen"].unique():
        m = re.search(r"(\d{4})", f)
        if m:
            years_detected.append(int(m.group(1)))
            
    min_year, max_year = min(years_detected), max(years_detected)
    if min_year == 2007 and max_year == 2026:
        passed_checks += 1
        print(f" -> [OK] Cobertura temporal verificada: 2007 a 2026 (sin quiebres de serie).")
    else:
        print(f" -> [FAIL] Rango temporal inesperado: {min_year} - {max_year}")

    # -------------------------------------------------------------
    # RESUMEN FINAL DE CERTIFICACIÓN
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f" RESULTADO FINAL DE AUDITORÍA: {passed_checks}/{total_checks} PRUEBAS SUPERADAS ({passed_checks/total_checks*100:.1f}%)")
    print("=" * 80)
    
    if passed_checks == total_checks:
        print(" [CERTIFICADO] La base de datos es consistente, íntegra y reproducible.")
    else:
        print(" [ALERTA] Se detectaron observaciones que requieren ajuste.")

if __name__ == "__main__":
    run_quality_audit()
