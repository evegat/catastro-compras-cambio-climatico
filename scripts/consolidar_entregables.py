# consolidar_entregables.py
import os
import glob
import json
import re
from pathlib import Path
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

OUT_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output")
CHECKPOINTS_DIR = OUT_DIR / "checkpoints"

AXES_CONFIG = {
    "P089_CAMBIO_CLIMATICO": {
        "nombre": "Cambio Climático",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/Catastro_Cambio_Climatico_ChileCompra.xlsx"
    },
    "P049_INTELIGENCIA_ARTIFICIAL": {
        "nombre": "Inteligencia Artificial y Analítica",
        "output_excel": "D:/Proyectos/P049 - Compras publicas tecnologicas e IA publica/Catastro_IA_Tecnologia_ChileCompra.xlsx"
    },
    "P036_OPEN_SOURCE": {
        "nombre": "Software Libre y Open Source",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Open_Source_ChileCompra.xlsx"
    },
    "P005_TRANSFORMACION_DIGITAL": {
        "nombre": "Transformación Digital del Estado",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Transformacion_Digital_ChileCompra.xlsx"
    },
    "P080_CIBERSEGURIDAD": {
        "nombre": "Ciberseguridad y Continuidad Operacional",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Ciberseguridad_ChileCompra.xlsx"
    },
    "P087_DATOS_PERSONALES": {
        "nombre": "Protección de Datos Personales",
        "output_excel": "D:/Proyectos/P089 - Catastro Compras Cambio Climatico/output/Catastro_Datos_Personales_ChileCompra.xlsx"
    }
}

def clean_string(val):
    if isinstance(val, str):
        # Limpiar caracteres ilegales para Excel y bytes no imprimibles
        val = ILLEGAL_CHARACTERS_RE.sub("", val)
        val = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', val)
        return val.strip()
    return val

def main():
    print("=" * 80)
    print(" CONSOLIDADOR FINAL DE ENTREGABLES EXCEL (CHILECOMPRA 2007-2026)")
    print("=" * 80)
    
    chk_files = sorted(glob.glob(str(CHECKPOINTS_DIR / "*.json")))
    print(f"Cargando {len(chk_files)} checkpoints de disco...")
    
    accumulated_results = {eje: [] for eje in AXES_CONFIG.keys()}
    
    for chk_path in chk_files:
        try:
            with open(chk_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                for it in items:
                    accumulated_results[it["eje_codigo"]].append(it)
        except Exception as e:
            print(f"Error leyendo {chk_path}: {e}")
            
    print("\nResumen de registros extraídos:")
    for eje, data in AXES_CONFIG.items():
        print(f" - {data['nombre']}: {len(accumulated_results[eje]):,} registros")
        
    print("\nGenerando planillas Excel...")
    
    for eje, data in AXES_CONFIG.items():
        results = accumulated_results[eje]
        output_file = Path(data["output_excel"])
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not results:
            print(f" -> Sin registros para {data['nombre']}")
            continue
            
        print(f"\nProcesando Excel para: {data['nombre']} ({len(results):,} filas)...")
        df = pd.DataFrame(results)
        
        # Eliminar duplicados a nivel de proceso + subcategoria + tipo_registro
        df = df.drop_duplicates(subset=["codigo_proceso", "subcategoria", "tipo_registro"])
        
        # Limpiar caracteres ilegales en todas las columnas de texto
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].apply(clean_string)
                
        print(f" -> Registros únicos tras deduplicación: {len(df):,}")
        
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Pestaña 1: Catastro Completo
            df.to_excel(writer, sheet_name="Catastro Completo", index=False)
            
            # Pestaña 2: Resumen por Subcategoría y Tipo de Proceso
            resumen_subcat = df.groupby(["subcategoria", "tipo_registro"]).size().reset_index(name="Total Procesos")
            resumen_subcat.to_excel(writer, sheet_name="Resumen Subcategorias", index=False)
            
            # Pestaña 3: Top 50 Organismos Compradores
            resumen_org = df.groupby("organismo_comprador").size().reset_index(name="Total Procesos").sort_values(by="Total Procesos", ascending=False).head(50)
            resumen_org.to_excel(writer, sheet_name="Top 50 Organismos", index=False)
            
            # Pestaña 4: Términos Gatillantes Más Frecuentes
            resumen_terminos = df.groupby(["subcategoria", "termino_coincidente"]).size().reset_index(name="Frecuencia").sort_values(by="Frecuencia", ascending=False).head(100)
            resumen_terminos.to_excel(writer, sheet_name="Terminos Gatillantes", index=False)
            
        print(f" [OK] Guardado exitosamente en: {output_file}")
        
    print("\n" + "=" * 80)
    print(" CONSOLIDACIÓN EXITOSA. TODOS LOS ARCHIVOS EXCEL GENERADOS.")
    print("=" * 80)

if __name__ == "__main__":
    main()
