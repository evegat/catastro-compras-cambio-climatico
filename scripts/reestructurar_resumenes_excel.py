# reestructurar_resumenes_excel.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico")
EXCEL_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.xlsx"
CSV_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.csv"

def reestructurar():
    print("Cargando base de datos desde CSV...")
    df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8-sig', comment='#')
    df['monto_num'] = pd.to_numeric(df['monto_pesos'], errors='coerce').fillna(0)
    
    # 1. Pestaña Portada
    df_meta = pd.DataFrame([
        ["PROYECTO", "P089 - Catastro Histórico de Compras Públicas en Cambio Climático de Chile"],
        ["COBERTURA TEMPORAL", "Enero 2007 a Julio 2026 (470 bases masivas de Mercado Público)"],
        ["TOTAL REGISTROS ÚNICOS", f"{len(df):,} procesos"],
        ["DISEÑO DE PIPELINE Y AUTORÍA", "Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)"],
        ["CONTACTO", "evega.ap@gmail.com"],
        ["LICENCIA", "Creative Commons Attribution 4.0 International (CC BY 4.0)"],
        ["ADVERTENCIA DE MONTOS", "NO SUMAR montos de Licitaciones con Órdenes de Compra. Las licitaciones reflejan presupuestos marco plurianuales; las OCs reflejan gasto transaccional unitario."]
    ], columns=["METADATO", "VALOR"])

    # 2. Resumen Nivel Institucional (Columnas Separadas para Licitaciones vs OCs)
    res_nivel = []
    for nivel, g in df.groupby('nivel_institucional'):
        g_lic = g[g['tipo_registro'] == 'licitacion']
        g_oc = g[g['tipo_registro'] == 'orden_compra']
        
        n_lic = len(g_lic)
        m_lic = round(g_lic['monto_num'].sum() / 1e6, 2)
        
        n_oc = len(g_oc)
        m_oc = round(g_oc['monto_num'].sum() / 1e6, 2)
        
        res_nivel.append({
            'Nivel Institucional': nivel,
            'N° Licitaciones (Concursos)': n_lic,
            'Monto Licitaciones ($M CLP) [Marco Plurianual]': m_lic,
            'N° Órdenes de Compra (OC)': n_oc,
            'Monto Órdenes Compra ($M CLP) [Gasto Transaccional]': m_oc,
            'Total Procesos Combinados': n_lic + n_oc
        })
    df_nivel = pd.DataFrame(res_nivel).sort_values(by='Total Procesos Combinados', ascending=False)
    
    # Fila de Totales
    total_row = pd.DataFrame([{
        'Nivel Institucional': 'TOTAL CONSOLIDADO',
        'N° Licitaciones (Concursos)': df_nivel['N° Licitaciones (Concursos)'].sum(),
        'Monto Licitaciones ($M CLP) [Marco Plurianual]': round(df_nivel['Monto Licitaciones ($M CLP) [Marco Plurianual]'].sum(), 2),
        'N° Órdenes de Compra (OC)': df_nivel['N° Órdenes de Compra (OC)'].sum(),
        'Monto Órdenes Compra ($M CLP) [Gasto Transaccional]': round(df_nivel['Monto Órdenes Compra ($M CLP) [Gasto Transaccional]'].sum(), 2),
        'Total Procesos Combinados': df_nivel['Total Procesos Combinados'].sum()
    }])
    df_nivel = pd.concat([df_nivel, total_row], ignore_index=True)

    # 3. Resumen Mecanismos de Compra
    res_mec = df.groupby(['tipo_registro', 'mecanismo_compra']).agg(
        Total_Procesos=('codigo_proceso', 'count'),
        Monto_Millones_CLP=('monto_num', lambda x: round(x.sum() / 1e6, 2))
    ).reset_index()
    res_mec.columns = ['Tipo de Registro', 'Mecanismo Legal de Contratación', 'N° Procesos', 'Monto ($M CLP)']

    # 4. Resumen Subcategorías
    res_sub = df.groupby(['subcategoria', 'tipo_registro']).size().unstack(fill_value=0).reset_index()
    res_sub.columns = ['Subcategoría Temática', 'N° Licitaciones', 'N° Órdenes de Compra']
    res_sub['Total Procesos'] = res_sub['N° Licitaciones'] + res_sub['N° Órdenes de Compra']

    # 5. Detalle GOREs
    gore_df = df[df['nivel_institucional'] == 'Gobiernos Regionales (GORE)'].groupby(['organismo_comprador', 'subcategoria', 'tipo_registro']).agg(
        Total_Procesos=('codigo_proceso', 'count'),
        Monto_Millones=('monto_num', lambda x: round(x.sum() / 1e6, 2))
    ).reset_index().sort_values(by='Total_Procesos', ascending=False)

    # 6. Top 50 Organismos
    top_org = df.groupby(['nivel_institucional', 'organismo_comprador']).agg(
        Licitaciones=('tipo_registro', lambda x: (x == 'licitacion').sum()),
        Ordenes_Compra=('tipo_registro', lambda x: (x == 'orden_compra').sum()),
        Total_Procesos=('codigo_proceso', 'count')
    ).reset_index().sort_values(by='Total_Procesos', ascending=False).head(50)

    # 7. Términos Gatillantes
    terms = df.groupby(['subcategoria', 'termino_coincidente']).size().reset_index(name='Frecuencia').sort_values(by='Frecuencia', ascending=False).head(100)

    print("Guardando libro Excel con 8 pestañas reestructuradas...")
    with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
        df_meta.to_excel(writer, sheet_name='Ficha Técnica y Autoría', index=False)
        df.to_excel(writer, sheet_name='Catastro Completo', index=False)
        df_nivel.to_excel(writer, sheet_name='Resumen Nivel Institucional', index=False)
        res_mec.to_excel(writer, sheet_name='Resumen Mecanismos Compra', index=False)
        res_sub.to_excel(writer, sheet_name='Resumen Subcategorias', index=False)
        gore_df.to_excel(writer, sheet_name='Detalle GOREs', index=False)
        top_org.to_excel(writer, sheet_name='Top 50 Organismos', index=False)
        terms.to_excel(writer, sheet_name='Terminos Gatillantes', index=False)

    print(f"[OK] Excel generado exitosamente en: {EXCEL_PATH}")

if __name__ == "__main__":
    reestructurar()
