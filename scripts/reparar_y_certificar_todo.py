# reparar_y_certificar_todo.py
import os
import re
import pandas as pd
import openpyxl
from pathlib import Path

BASE_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico")
EXCEL_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.xlsx"
CSV_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.csv"

def clasificar_nivel_institucional_robusto(row):
    org = str(row.get('organismo_comprador', '')).upper()
    sec = str(row.get('sector', '')).upper() if pd.notnull(row.get('sector')) else ''
    
    if any(k in org for k in ['MUNI', 'ILUSTRE MUNICIPALIDAD']) or 'MUNICIPAL' in sec:
        return 'Municipalidades (Gobiernos Locales)'
    elif any(k in org for k in ['GOBIERNO REGIONAL', 'GORE', 'G.R.']):
        return 'Gobiernos Regionales (GORE)'
    elif any(k in org for k in ['UNIVERSIDAD', 'CENTRO DE FORMACION', 'INSTITUTO PROFESIONAL']) or 'EDUCACION' in sec:
        return 'Universidades y Academia'
    elif any(k in org for k in ['ARMADA', 'EJERCITO', 'FACH', 'CARABINEROS', 'PDI', 'DEFENSA', 'CAPREDENA', 'DIPRECA']):
        return 'Defensa y Fuerzas Armadas'
    elif any(k in org for k in ['HOSPITAL', 'SALUD', 'SERVICIO DE SALUD', 'CESFAM', 'CENABAST', 'FONASA', 'ISP']):
        return 'Sector Salud'
    elif any(k in org for k in ['EMPRESA', 'METRO', 'ENAP', 'CODELCO', 'CORREOS', 'BANCOESTADO', 'CASA DE MONEDA', 'FERROCARRILES', 'EFE', 'PUERTO', 'ASMAR', 'FAMAE']):
        return 'Empresas Públicas del Estado'
    else:
        return 'Gobierno Central y Servicios Públicos'

def clasificar_mecanismo_robusto(row):
    cod = str(row.get('codigo_proceso', '')).upper().strip()
    tipo_reg = str(row.get('tipo_registro', '')).lower()
    
    m = re.search(r'-([A-Z0-9]{2,3})\d*$', cod)
    suf = m.group(1)[:2] if m else ''
    
    if tipo_reg == 'licitacion':
        if suf in ['LP', 'LE', 'L1', 'LR', 'LQ', 'LS']:
            return 'Licitación Pública'
        elif suf in ['CO', 'B2']:
            return 'Licitación Privada'
        else:
            return 'Licitación Pública'
    else: # orden_compra
        if suf in ['AG']:
            return 'Compra Ágil (< 30 UTM)'
        elif suf in ['CM', 'CC', 'CD']:
            return 'Convenio Marco (Catálogo)'
        elif suf in ['TD', 'E2', 'SE']:
            return 'Trato Directo (Excepcional)'
        else:
            return 'OC Ordinaria / Trato Directo'

def clasificar_subcategoria_robusto(row):
    sub = row.get('subcategoria')
    if pd.notnull(sub) and str(sub).strip() != '' and str(sub) != 'nan':
        return str(sub).strip()
        
    texto = str(row.get('nombre', '')) + ' ' + str(row.get('descripcion', ''))
    texto_low = texto.lower()
    
    if re.search(r'cambio\s+clim|adaptaci[oó]n\s+clim|mitigaci[oó]n\s+clim|resiliencia\s+clim', texto_low):
        return 'Nucleo_Exacto'
    elif re.search(r'ley\s+21\.?455|paccc|parcc|eclp|plan\s+de\s+acci[oó]n\s+clim', texto_low):
        return 'Instrumentos_Ley21455'
    elif re.search(r'huella\s+de\s+carbono|gei|gases\s+de\s+efecto|descarbonizaci[oó]n|carbono\s+neutral', texto_low):
        return 'Gases_Descarbonizacion'
    elif re.search(r'eficiencia\s+energ[eé]tica|hidr[oó]geno\s+verde|h2v|electromovilidad|soluciones\s+basadas\s+en\s+la\s+naturaleza', texto_low):
        return 'Transicion_SBN'
    else:
        return 'Nucleo_Exacto'

def procesar():
    print("1. Leyendo base CSV original...")
    df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8-sig', comment='#')
    
    print("2. Normalizando clasificación institucional, mecanismos y subcategorías...")
    df['nivel_institucional'] = df.apply(clasificar_nivel_institucional_robusto, axis=1)
    df['mecanismo_compra'] = df.apply(clasificar_mecanismo_robusto, axis=1)
    df['subcategoria'] = df.apply(clasificar_subcategoria_robusto, axis=1)
    df['monto_num'] = pd.to_numeric(df['monto_pesos'], errors='coerce').fillna(0)
    
    # Asegurar orden y tipos de columnas exactos
    columnas_ordenadas = [
        'archivo_origen', 'tipo_registro', 'mecanismo_compra', 'codigo_proceso', 'link',
        'nombre', 'descripcion', 'organismo_comprador', 'unidad_compra', 'rut_comprador',
        'sector', 'region_comprador', 'fecha', 'monto_pesos', 'moneda', 'proveedor',
        'rut_proveedor', 'eje_codigo', 'eje_nombre', 'subcategoria', 'termino_coincidente',
        'texto_fragmento', 'nivel_institucional'
    ]
    df_export = df[columnas_ordenadas].copy()
    
    print(f"Total registros a exportar: {len(df_export):,}")
    print("Verificando nulos en campos clave:")
    print(df_export[['tipo_registro', 'nivel_institucional', 'mecanismo_compra', 'subcategoria']].isna().sum())
    
    # 3. Guardar CSV
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('# dataset_id: P089_EVT_CHILECOMPRA_2007_2026\n')
        f.write('# data_architect: Eduardo Vega Toledo (evega.ap@gmail.com)\n')
        f.write('# requested_by: Valentina Cariaga Cerda\n')
        f.write('# project: P089 - Catastro Cambio Climatico Chile\n')
        df_export.to_csv(f, sep=';', index=False)
    print(f"[OK] CSV guardado: {CSV_PATH}")
    
    # 4. Generar Pestañas de Resumen Cuadradas al 100%
    df_meta = pd.DataFrame([
        ["PROYECTO", "P089 - Catastro Histórico de Compras Públicas en Cambio Climático de Chile"],
        ["COBERTURA TEMPORAL", "Enero 2007 a Julio 2026 (470 bases masivas de Mercado Público)"],
        ["TOTAL REGISTROS ÚNICOS", f"{len(df_export):,} procesos"],
        ["DISEÑO DE PIPELINE Y AUTORÍA", "Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)"],
        ["SOLICITADO POR", "Valentina Cariaga Cerda"],
        ["CONTACTO", "evega.ap@gmail.com"],
        ["LICENCIA", "Creative Commons Attribution 4.0 International (CC BY 4.0)"],
        ["ADVERTENCIA DE MONTOS", "NO SUMAR montos de Licitaciones con Órdenes de Compra. Las licitaciones reflejan presupuestos marco plurianuales; las OCs reflejan gasto transaccional unitario."]
    ], columns=["METADATO", "VALOR"])

    # Resumen Nivel Institucional
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
    total_row = pd.DataFrame([{
        'Nivel Institucional': 'TOTAL CONSOLIDADO',
        'N° Licitaciones (Concursos)': df_nivel['N° Licitaciones (Concursos)'].sum(),
        'Monto Licitaciones ($M CLP) [Marco Plurianual]': round(df_nivel['Monto Licitaciones ($M CLP) [Marco Plurianual]'].sum(), 2),
        'N° Órdenes de Compra (OC)': df_nivel['N° Órdenes de Compra (OC)'].sum(),
        'Monto Órdenes Compra ($M CLP) [Gasto Transaccional]': round(df_nivel['Monto Órdenes Compra ($M CLP) [Gasto Transaccional]'].sum(), 2),
        'Total Procesos Combinados': df_nivel['Total Procesos Combinados'].sum()
    }])
    df_nivel = pd.concat([df_nivel, total_row], ignore_index=True)

    # Resumen Mecanismos
    res_mec = df.groupby(['tipo_registro', 'mecanismo_compra']).agg(
        Total_Procesos=('codigo_proceso', 'count'),
        Monto_Millones_CLP=('monto_num', lambda x: round(x.sum() / 1e6, 2))
    ).reset_index()
    res_mec.columns = ['Tipo de Registro', 'Mecanismo Legal de Contratación', 'N° Procesos', 'Monto ($M CLP)']

    # Resumen Subcategorías
    res_sub = df.groupby(['subcategoria', 'tipo_registro']).size().unstack(fill_value=0).reset_index()
    res_sub.columns = ['Subcategoría Temática', 'N° Licitaciones', 'N° Órdenes de Compra']
    res_sub['Total Procesos'] = res_sub['N° Licitaciones'] + res_sub['N° Órdenes de Compra']

    # Detalle GOREs
    gore_df = df[df['nivel_institucional'] == 'Gobiernos Regionales (GORE)'].groupby(['organismo_comprador', 'subcategoria', 'tipo_registro']).agg(
        Total_Procesos=('codigo_proceso', 'count'),
        Monto_Millones=('monto_num', lambda x: round(x.sum() / 1e6, 2))
    ).reset_index().sort_values(by='Total_Procesos', ascending=False)

    # Top 50 Organismos
    top_org = df.groupby(['nivel_institucional', 'organismo_comprador']).agg(
        Licitaciones=('tipo_registro', lambda x: (x == 'licitacion').sum()),
        Ordenes_Compra=('tipo_registro', lambda x: (x == 'orden_compra').sum()),
        Total_Procesos=('codigo_proceso', 'count')
    ).reset_index().sort_values(by='Total_Procesos', ascending=False).head(50)

    # Términos Gatillantes
    terms = df.groupby(['subcategoria', 'termino_coincidente']).size().reset_index(name='Frecuencia').sort_values(by='Frecuencia', ascending=False).head(100)

    # Guardar Excel
    with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
        df_meta.to_excel(writer, sheet_name='Ficha Técnica y Autoría', index=False)
        df_export.to_excel(writer, sheet_name='Catastro Completo', index=False)
        df_nivel.to_excel(writer, sheet_name='Resumen Nivel Institucional', index=False)
        res_mec.to_excel(writer, sheet_name='Resumen Mecanismos Compra', index=False)
        res_sub.to_excel(writer, sheet_name='Resumen Subcategorias', index=False)
        gore_df.to_excel(writer, sheet_name='Detalle GOREs', index=False)
        top_org.to_excel(writer, sheet_name='Top 50 Organismos', index=False)
        terms.to_excel(writer, sheet_name='Terminos Gatillantes', index=False)
        
    print(f"[OK] Excel guardado: {EXCEL_PATH}")

if __name__ == "__main__":
    procesar()
