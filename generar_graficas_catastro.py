"""
====================================================================================================
GENERADOR AUTÓNOMO DE GRÁFICAS Y VISUALIZACIONES: CATASTRO DE COMPRAS CLIMÁTICAS (2007–2026)
====================================================================================================
Autor / Data Architect: Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)
Contacto: evega.ap@gmail.com
Proyecto: P089 - Catastro Nacional de Compras Públicas en Cambio Climático de Chile
Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0)

OBJETIVO DEL SCRIPT:
Permitir que cualquier investigador reproduzca de forma manual y autónoma todas las figuras y gráficos
estadísticos del catastro a partir del archivo CSV abierto 'Catastro_Cambio_Climatico_ChileCompra.csv'.

REQUISITOS:
pip install pandas matplotlib

USO:
Coloque este script en la misma carpeta que 'Catastro_Cambio_Climatico_ChileCompra.csv' y ejecute:
python generar_graficas_catastro.py
====================================================================================================
"""

import os
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --------------------------------------------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS Y ESTILOS
# --------------------------------------------------------------------------------------------------
CURRENT_DIR = Path(__file__).parent if "__file__" in locals() else Path(".")
CSV_PATH = CURRENT_DIR / "Catastro_Cambio_Climatico_ChileCompra.csv"
OUTPUT_FIG_DIR = CURRENT_DIR / "figuras_catastro"
OUTPUT_FIG_DIR.mkdir(parents=True, exist_ok=True)

# Paleta editorial ejecutiva
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

COLOR_PRIMARY = '#1F497D'      # Azul oscuro
COLOR_SECONDARY = '#418AB3'    # Azul medio
COLOR_ALERT = '#C00000'        # Rojo / Trato Directo Excepcional
COLOR_ACCENT = '#E26B00'       # Naranja / Hitos
COLOR_LIGHT = '#8FAADC'        # Azul claro / Convenio Marco
COLOR_GREEN = '#385723'        # Verde oscuro / Compra Ágil
COLOR_DARK = '#262626'         # Gris oscuro texto

def cargar_y_preparar_datos():
    print(f"Cargando dataset desde: {CSV_PATH}")
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV en: {CSV_PATH}")
        
    df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8-sig', comment='#')
    
    # Extraer año de la fecha o del archivo de origen
    def get_year(row):
        if pd.notnull(row.get('fecha')) and str(row['fecha']) != '':
            s = str(row['fecha'])[:4]
            if s.isdigit() and 2000 <= int(s) <= 2026:
                return int(s)
        f = str(row.get('archivo_origen', ''))
        for y in range(2007, 2027):
            if str(y) in f:
                return y
        return None
        
    df['anio'] = df.apply(get_year, axis=1)
    df['monto_num'] = pd.to_numeric(df['monto_pesos'], errors='coerce').fillna(0)
    return df

def graficar_figura1_evolucion(df):
    print("Generando Figura 1: Evolución temporal y quiebre Ley 21.455...")
    t_year = df.groupby('anio').agg(
        licitaciones=('tipo_registro', lambda x: (x == 'licitacion').sum()),
        ordenes_compra=('tipo_registro', lambda x: (x == 'orden_compra').sum()),
        total=('codigo_proceso', 'count')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    ax1.bar(t_year['anio'], t_year['ordenes_compra'], label='Órdenes de Compra (OC)', color=COLOR_SECONDARY, width=0.65)
    ax1.bar(t_year['anio'], t_year['licitaciones'], bottom=t_year['ordenes_compra'], label='Licitaciones Públicas (Concursos)', color=COLOR_PRIMARY, width=0.65)
    
    ax1.set_ylabel('Número de Procesos de Compra', fontsize=10.5, fontweight='bold', color=COLOR_PRIMARY)
    ax1.set_xlabel('Año de Publicación / Emisión (2007 - 2026)', fontsize=10, fontweight='bold')
    ax1.set_xticks(t_year['anio'])
    ax1.set_xticklabels(t_year['anio'], rotation=45, ha='right', fontsize=8.5)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.set_ylim(0, 1250)
    
    ax1.axvline(x=2022, color=COLOR_ACCENT, linestyle=':', linewidth=1.5)
    ax1.annotate('Promulgación Ley Marco 21.455\n(Junio 2022: +105% hacia 2024)',
                 xy=(2022, 500), xytext=(2016.5, 950),
                 arrowprops=dict(facecolor=COLOR_ACCENT, shrink=0.05, width=1, headwidth=6),
                 fontsize=8.5, fontweight='bold', color=COLOR_ACCENT,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF2E6', edgecolor=COLOR_ACCENT, alpha=0.9))

    row_2024 = t_year[t_year['anio'] == 2024].iloc[0]
    ax1.text(2024, row_2024['total'] + 25, f"{int(row_2024['total']):,}\nproc.", ha='center', fontsize=8, fontweight='bold', color=COLOR_PRIMARY)

    ax1.set_title('Evolución Histórica de Compras Públicas en Cambio Climático en Chile (2007–2026)\nQuiebre Estructural tras la Ley Marco de Cambio Climático (Ley 21.455)',
                  fontsize=11.5, fontweight='bold', pad=15, color=COLOR_PRIMARY)
    ax1.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FIG_DIR / "fig1_evolucion_temporal_ley21455.png", dpi=300)
    plt.close()

def graficar_figura2_mecanismos(df):
    print("Generando Figura 2: Mecanismos de contratación y trato directo...")
    t_mec = df.groupby('mecanismo_compra').size().sort_values(ascending=True).reset_index(name='total')
    
    colors = []
    for m in t_mec['mecanismo_compra']:
        if 'Trato Directo' in m:
            colors.append(COLOR_ALERT)       # Rojo para trato directo excepcional
        elif 'Licitación Pública' in m:
            colors.append(COLOR_PRIMARY)     # Azul oscuro para licitación pública
        elif 'Convenio Marco' in m:
            colors.append(COLOR_LIGHT)       # Azul claro para convenio marco
        elif 'Compra Ágil' in m:
            colors.append(COLOR_GREEN)       # Verde para compra ágil
        else:
            colors.append(COLOR_SECONDARY)
            
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    bars = ax.barh(t_mec['mecanismo_compra'], t_mec['total'], color=colors, height=0.55)
    
    ax.set_xlabel('Número de Procesos', fontsize=10, fontweight='bold')
    ax.set_title('Mecanismos de Contratación en Compras Climáticas (2007–2026)\nIdentificación de Licitaciones, Convenio Marco y Trato Directo Excepcional',
                 fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    
    for b in bars:
        w = b.get_width()
        pct = w / len(df) * 100
        ax.text(w + 40, b.get_y() + b.get_height()/2, f"{int(w):,} ({pct:.1f}%)", va='center', fontsize=8.5, fontweight='bold', color=COLOR_DARK)
    ax.set_xlim(0, max(t_mec['total']) * 1.18)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FIG_DIR / "fig2_mecanismos_contratacion.png", dpi=300, bbox_inches='tight')
    plt.close()

def graficar_figura3_gobernanza(df):
    print("Generando Figura 3: Gobernanza multinivel...")
    t_gov = df.groupby('nivel_institucional').agg(
        procesos=('codigo_proceso', 'count'),
        monto_millones=('monto_num', lambda x: x.sum() / 1e6)
    ).sort_values(by='procesos', ascending=True).reset_index()

    fig, (ax_p, ax_m) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    
    bars_p = ax_p.barh(t_gov['nivel_institucional'], t_gov['procesos'], color=COLOR_PRIMARY, height=0.6)
    ax_p.set_title('A. Número de Procesos de Compra', fontsize=10.5, fontweight='bold', color=COLOR_PRIMARY)
    ax_p.set_xlabel('Total Procesos', fontsize=9, fontweight='bold')
    ax_p.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars_p:
        w = b.get_width()
        ax_p.text(w + 50, b.get_y() + b.get_height()/2, f"{int(w):,}", va='center', fontsize=8, color=COLOR_DARK)
    ax_p.set_xlim(0, max(t_gov['procesos']) * 1.18)

    t_gov_m = t_gov.sort_values(by='monto_millones', ascending=True)
    bars_m = ax_m.barh(t_gov_m['nivel_institucional'], t_gov_m['monto_millones'], color=COLOR_SECONDARY, height=0.6)
    ax_m.set_title('B. Monto Total Licitado (Millones CLP)', fontsize=10.5, fontweight='bold', color=COLOR_SECONDARY)
    ax_m.set_xlabel('Millones de Pesos (CLP)', fontsize=9, fontweight='bold')
    ax_m.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars_m:
        w = b.get_width()
        ax_m.text(w + 3000, b.get_y() + b.get_height()/2, f"${w:,.0f}M", va='center', fontsize=8, color=COLOR_DARK)
    ax_m.set_xlim(0, max(t_gov_m['monto_millones']) * 1.25)
    ax_m.set_yticklabels([])

    fig.suptitle('Gobernanza Multinivel de las Compras Climáticas del Estado de Chile (2007–2026)\nDistribución por Tipo de Organismo Comprador',
                 fontsize=12, fontweight='bold', y=1.02, color=COLOR_PRIMARY)
    plt.tight_layout()
    plt.savefig(OUTPUT_FIG_DIR / "fig3_gobernanza_multinivel.png", dpi=300, bbox_inches='tight')
    plt.close()

def graficar_figura4_subcategorias(df):
    print("Generando Figura 4: Subcategorías temáticas...")
    t_sub = df.groupby(['subcategoria', 'tipo_registro']).size().unstack(fill_value=0).reset_index()
    t_sub['total'] = t_sub['licitacion'] + t_sub['orden_compra']
    t_sub = t_sub.sort_values(by='total', ascending=True)

    labels_map = {
        'Nucleo_Exacto': 'Núcleo Exacto (Cambio/Adaptación/Mitigación)',
        'Transicion_SBN': 'Transición Energética y SBN (Eficiencia/H2V)',
        'Gases_Descarbonizacion': 'Gases y Descarbonización (Huella/GEI)',
        'Instrumentos_Ley21455': 'Instrumentos Ley 21.455 (PACCC/PARCC/ECLP)'
    }
    t_sub['subcat_nombre'] = t_sub['subcategoria'].map(labels_map)

    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    ax.barh(t_sub['subcat_nombre'], t_sub['orden_compra'], label='Órdenes de Compra (OC)', color=COLOR_SECONDARY, height=0.55)
    ax.barh(t_sub['subcat_nombre'], t_sub['licitacion'], left=t_sub['orden_compra'], label='Licitaciones Públicas', color=COLOR_PRIMARY, height=0.55)

    ax.set_xlabel('Número de Procesos', fontsize=9.5, fontweight='bold')
    ax.set_title('Distribución de Compras por Eje Temático y Modalidad de Registro',
                 fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.legend(loc='lower right', fontsize=8.5)

    for i, r in t_sub.reset_index().iterrows():
        ax.text(r['total'] + 60, i, f"{r['total']:,} ({r['total']/len(df)*100:.1f}%)", va='center', fontsize=8, fontweight='bold')
    ax.set_xlim(0, max(t_sub['total']) * 1.18)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIG_DIR / "fig4_subcategorias_tematicas.png", dpi=300, bbox_inches='tight')
    plt.close()

def graficar_figura5_top_compradores(df):
    print("Generando Figura 5: Top 12 instituciones compradoras...")
    t_org = df.groupby('organismo_comprador').size().sort_values(ascending=True).tail(12).reset_index(name='total')
    
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    bars = ax.barh(t_org['organismo_comprador'], t_org['total'], color=COLOR_PRIMARY, height=0.6)
    
    ax.set_xlabel('Número Total de Procesos Adjudicados', fontsize=9.5, fontweight='bold')
    ax.set_title('Top 12 Instituciones Públicas Compradoras en Cambio Climático (2007–2026)',
                 fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars:
        w = b.get_width()
        ax.text(w + 15, b.get_y() + b.get_height()/2, f"{int(w):,}", va='center', fontsize=8, fontweight='bold')
    ax.set_xlim(0, max(t_org['total']) * 1.12)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FIG_DIR / "fig5_top_organismos_compradores.png", dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("================================================================================")
    print(" GENERADOR DE FIGURAS Y GRÁFICAS ESTADÍSTICAS DEL CATASTRO")
    print("================================================================================")
    df = cargar_y_preparar_datos()
    graficar_figura1_evolucion(df)
    graficar_figura2_mecanismos(df)
    graficar_figura3_gobernanza(df)
    graficar_figura4_subcategorias(df)
    graficar_figura5_top_compradores(df)
    print(f"\n[OK] Todas las figuras fueron generadas con éxito en: {OUTPUT_FIG_DIR}")
    print("================================================================================")

if __name__ == "__main__":
    main()
