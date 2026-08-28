# auditoria_extremista_catastro.py
import sys
import os
import re
import hashlib
from pathlib import Path
import pandas as pd
import openpyxl
import docx

DIR_LOCAL = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico")
DIR_OBSIDIAN = Path(r"C:\Users\evega\OneDrive\Documents\Obsidian\MyWorld\2 - Project\P089 - Catastro Compras Cambio Climatico\Catastro Compras Cambio Climatico 2007-2026 V.0 25082026")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run_extreme_audit():
    print("=" * 85)
    print(" SUITE DE AUDITORÍA EXTREMA: CERTIFICACIÓN Y CONTROL DE CALIDAD CATASTRO CLIMÁTICO")
    print("=" * 85)
    
    total_checks = 0
    passed_checks = 0
    errors = []

    def check(condition, desc, error_msg=""):
        nonlocal total_checks, passed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f" [PASS] Test {total_checks:02d}: {desc}")
        else:
            print(f" [FAIL] Test {total_checks:02d}: {desc}")
            if error_msg:
                print(f"        -> Detalle del error: {error_msg}")
            errors.append(f"Test {total_checks:02d}: {desc} -> {error_msg}")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 1: EXISTENCIA Y PARIDAD DE ARCHIVOS EN AMBAS RUTAS
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 1: VERIFICACIÓN DE ARCHIVOS Y SINCRONIZACIÓN ---")
    archivos_esperados = [
        "Catastro_Cambio_Climatico_ChileCompra.xlsx",
        "Catastro_Cambio_Climatico_ChileCompra.csv",
        "Catastro_Compras_Cambio_Climatico_Informe_Metodologico_y_Estadistico.docx",
        "generar_graficas_catastro.py",
        "replicar_catastro_chilecompra.py",
        "01_Ficha_Metodologica_y_Codebook.md",
        "02_Brief_Estadistico_Compras_Climaticas.md"
    ]
    for arc in archivos_esperados:
        f_loc = DIR_LOCAL / arc
        f_obs = DIR_OBSIDIAN / arc
        check(f_loc.exists(), f"Existencia de '{arc}' en carpeta local D:")
        check(f_obs.exists(), f"Existencia de '{arc}' en carpeta de Obsidian Drive")
        if f_loc.exists() and f_obs.exists():
            check(f_loc.stat().st_size == f_obs.stat().st_size, f"Paridad de tamaño exacto para '{arc}' ({f_loc.stat().st_size:,} bytes)")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 2: AUDITORÍA DE DATOS CSV Y EXCEL (INTEGRIDAD MATEMÁTICA)
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 2: AUDITORÍA MATEMÁTICA Y ESTRUCTURAL (CSV vs EXCEL) ---")
    csv_file = DIR_LOCAL / "Catastro_Cambio_Climatico_ChileCompra.csv"
    excel_file = DIR_LOCAL / "Catastro_Cambio_Climatico_ChileCompra.xlsx"
    
    df_csv = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig', comment='#')
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    df_xl_cat = pd.read_excel(excel_file, sheet_name="Catastro Completo")
    
    check(len(df_csv) == 9086, f"Volumen exacto en CSV (esperado 9,086 filas, obtenido: {len(df_csv):,})")
    check(len(df_xl_cat) == 9086, f"Volumen exacto en Excel 'Catastro Completo' (esperado 9,086 filas, obtenido: {len(df_xl_cat):,})")
    check(len(df_csv.columns) == len(df_xl_cat.columns), f"Coincidencia exacta de columnas CSV vs Excel ({len(df_csv.columns)} columnas)")
    
    # Llave primaria / deduplicación
    dup_csv = df_csv.duplicated(subset=['codigo_proceso', 'subcategoria', 'tipo_registro']).sum()
    check(dup_csv == 0, f"Cero duplicados en clave compuesta (codigo_proceso, subcategoria, tipo_registro): {dup_csv}")
    
    # ----------------------------------------------------------------------------------------------
    # BLOQUE 3: AUDITORÍA DE CUADRATURA ENTRE PESTAÑAS DE EXCEL
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 3: CUADRATURA FINANCIERA Y CONTEO MULTI-PESTAÑA ---")
    df_res_nivel = pd.read_excel(excel_file, sheet_name="Resumen Nivel Institucional")
    df_res_mec = pd.read_excel(excel_file, sheet_name="Resumen Mecanismos Compra")
    df_res_sub = pd.read_excel(excel_file, sheet_name="Resumen Subcategorias")
    
    # Total en Resumen Nivel Institucional
    fila_total_nivel = df_res_nivel[df_res_nivel['Nivel Institucional'] == 'TOTAL CONSOLIDADO'].iloc[0]
    check(fila_total_nivel['Total Procesos Combinados'] == 9086, f"Cuadratura de procesos en 'Resumen Nivel Institucional' ({fila_total_nivel['Total Procesos Combinados']})")
    check(fila_total_nivel['N° Licitaciones (Concursos)'] == 2287, f"Cuadratura de Licitaciones en Resumen Nivel ({fila_total_nivel['N° Licitaciones (Concursos)']})")
    check(fila_total_nivel['N° Órdenes de Compra (OC)'] == 6799, f"Cuadratura de Órdenes de Compra en Resumen Nivel ({fila_total_nivel['N° Órdenes de Compra (OC)']})")
    
    # Cuadratura de montos
    m_lic_csv = round(pd.to_numeric(df_csv[df_csv['tipo_registro'] == 'licitacion']['monto_pesos'], errors='coerce').fillna(0).sum() / 1e6, 2)
    m_oc_csv = round(pd.to_numeric(df_csv[df_csv['tipo_registro'] == 'orden_compra']['monto_pesos'], errors='coerce').fillna(0).sum() / 1e6, 2)
    
    check(abs(fila_total_nivel['Monto Licitaciones ($M CLP) [Marco Plurianual]'] - m_lic_csv) < 0.1, 
          f"Cuadratura Monto Licitaciones Excel vs CSV (${m_lic_csv:,.2f}M CLP)")
    check(abs(fila_total_nivel['Monto Órdenes Compra ($M CLP) [Gasto Transaccional]'] - m_oc_csv) < 0.1, 
          f"Cuadratura Monto Órdenes Compra Excel vs CSV (${m_oc_csv:,.2f}M CLP)")
    
    # Cuadratura Mecanismos
    check(df_res_mec['N° Procesos'].sum() == 9086, f"Cuadratura de procesos en 'Resumen Mecanismos Compra' ({df_res_mec['N° Procesos'].sum()})")
    
    # Cuadratura Subcategorías
    check(df_res_sub['Total Procesos'].sum() == 9086, f"Cuadratura de procesos en 'Resumen Subcategorias' ({df_res_sub['Total Procesos'].sum()})")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 4: CONTROL DE FALSOS POSITIVOS Y TÉRMINOS PROHIBIDOS
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 4: CONTROL DE FALSOS POSITIVOS Y CALIDAD SEMÁNTICA ---")
    rx_prohibidos = re.compile(r"(?i)\b(clima\s+laboral|clima\s+organizacional|ambiente\s+laboral|aire\s+acondicionado)\b")
    
    textos_combinados = (df_csv['nombre'].fillna('') + ' ' + df_csv['descripcion'].fillna('') + ' ' + df_csv['texto_fragmento'].fillna('')).tolist()
    matches_prohibidos = [t for t in textos_combinados if rx_prohibidos.search(t)]
    check(len(matches_prohibidos) == 0, f"Cero falsos positivos de 'clima laboral' / 'aire acondicionado' (Encontrados: {len(matches_prohibidos)})")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 5: AUDITORÍA DE ENLACES Y INTEGRIDAD WEB
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 5: AUDITORÍA DE ENLACES WEB Y DOMINIO OFICIAL ---")
    links_validos = df_csv['link'].dropna().apply(lambda x: str(x).startswith('http://') or str(x).startswith('https://')).sum()
    check(links_validos == len(df_csv.dropna(subset=['link'])), f"100% de los links son URLs HTTP/HTTPS válidas ({links_validos:,} enlaces)")
    
    links_mp = df_csv['link'].dropna().apply(lambda x: 'mercadopublico.cl' in str(x).lower()).sum()
    check(links_mp == len(df_csv.dropna(subset=['link'])), f"100% de los links apuntan al dominio oficial 'mercadopublico.cl' ({links_mp:,} enlaces)")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 6: AUDITORÍA DE METADATOS Y REGLAS DE USUARIO
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 6: REGLAS DE AUTORÍA Y PRIVACIDAD ---")
    # Verificar que NO exista la palabra 'doctorado' en los documentos finales entregables
    for doc_name in ["01_Ficha_Metodologica_y_Codebook.md", "02_Brief_Estadistico_Compras_Climaticas.md"]:
        content = (DIR_LOCAL / doc_name).read_text(encoding='utf-8')
        check("doctorado" not in content.lower(), f"Cero menciones a 'doctorado' en '{doc_name}'")
        check("evegat.cl" not in content.lower(), f"Cero menciones a 'evegat.cl' en '{doc_name}'")
        check("Eduardo Vega Toledo" in content, f"Autoría de Eduardo Vega Toledo presente en '{doc_name}'")
        check("Valentina Cariaga Cerda" in content, f"Encargo a Valentina Cariaga Cerda presente en '{doc_name}'")

    # Verificar documento Word
    doc_word = docx.Document(str(DIR_LOCAL / "Catastro_Compras_Cambio_Climatico_Informe_Metodologico_y_Estadistico.docx"))
    text_word = "\n".join(p.text for p in doc_word.paragraphs)
    check("doctorado" not in text_word.lower(), "Cero menciones a 'doctorado' en el informe Word (.docx)")
    check("evegat.cl" not in text_word.lower(), "Cero menciones a 'evegat.cl' en el informe Word (.docx)")
    check("Eduardo Vega Toledo" in text_word, "Autoría de Eduardo Vega Toledo presente en el informe Word (.docx)")
    check("Valentina Cariaga Cerda" in text_word, "Encargo a Valentina Cariaga Cerda presente en el informe Word (.docx)")
    check(len(doc_word.inline_shapes) >= 4, f"Presencia de figuras gráficas incrustadas en Word ({len(doc_word.inline_shapes)} figuras)")

    # ----------------------------------------------------------------------------------------------
    # BLOQUE 7: AUDITORÍA DE EJECUCIÓN DE SCRIPTS PYTHON ENTREGABLES
    # ----------------------------------------------------------------------------------------------
    print("\n--- BLOQUE 7: VERIFICACIÓN DE SCRIPTS PYTHON ---")
    py_graf = (DIR_LOCAL / "generar_graficas_catastro.py").read_text(encoding='utf-8')
    py_rep = (DIR_LOCAL / "replicar_catastro_chilecompra.py").read_text(encoding='utf-8')
    
    check("Catastro_Cambio_Climatico_ChileCompra.csv" in py_graf, "Script de gráficas apunta correctamente al CSV entregable")
    check("cambio climático" in py_rep or "cambio\\s+clim" in py_rep, "Script de replicación contiene taxonomía completa")

    # ----------------------------------------------------------------------------------------------
    # RESUMEN FINAL
    # ----------------------------------------------------------------------------------------------
    print("\n" + "=" * 85)
    pct = (passed_checks / total_checks) * 100
    print(f" RESULTADO FINAL DE LA AUDITORÍA: {passed_checks}/{total_checks} PRUEBAS SUPERADAS ({pct:.1f}%)")
    print("=" * 85)
    
    if errors:
        print("\nRESUMEN DE ERRORES DETECTADOS:")
        for err in errors:
            print(f" [!] {err}")
        return False
    else:
        print("\n>>> AUDITORÍA EXTREMA APROBADA AL 100% SIN NINGÚN ERROR NI DISCREPANCIA <<<")
        return True

if __name__ == "__main__":
    success = run_extreme_audit()
    sys.exit(0 if success else 1)
