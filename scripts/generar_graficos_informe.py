# generar_graficos_informe.py
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path("D:/Proyectos/P089 - Catastro Compras Cambio Climatico")
EXCEL_PATH = BASE_DIR / "Catastro_Cambio_Climatico_ChileCompra.xlsx"
FIG_DIR = BASE_DIR / "output" / "figuras"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Configuración global de estilos gráficos (Paleta sobria ejecutiva)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

COLOR_PRIMARY = '#1F497D'      # Azul oscuro
COLOR_SECONDARY = '#418AB3'    # Azul medio
COLOR_ACCENT = '#E26B00'       # Naranja cobrizo para hitos
COLOR_NEUTRAL = '#808080'      # Gris medio
COLOR_LIGHT = '#D9E1F2'        # Azul claro
COLOR_DARK = '#262626'         # Texto gris oscuro

def generate_all_charts():
    print("Cargando dataset para generación de gráficos...")
    df = pd.read_excel(EXCEL_PATH, sheet_name="Catastro Completo")
    
    # Extraer año
    def get_year(row):
        if pd.notnull(row['fecha']) and str(row['fecha']) != '':
            s = str(row['fecha'])[:4]
            if s.isdigit() and 2000 <= int(s) <= 2026:
                return int(s)
        f = str(row['archivo_origen'])
        for y in range(2007, 2027):
            if str(y) in f:
                return y
        return None
    df['anio'] = df.apply(get_year, axis=1)
    df['monto_num'] = pd.to_numeric(df['monto_pesos'], errors='coerce').fillna(0)

    # -------------------------------------------------------------
    # FIGURA 1: EVOLUCIÓN TEMPORAL Y EFECTO LEY 21.455
    # -------------------------------------------------------------
    print("Generando Figura 1: Evolución temporal...")
    t_year = df.groupby('anio').agg(
        licitaciones=('tipo_registro', lambda x: (x == 'licitacion').sum()),
        ordenes_compra=('tipo_registro', lambda x: (x == 'orden_compra').sum()),
        total=('codigo_proceso', 'count'),
        monto_millones=('monto_num', lambda x: x.sum() / 1e6)
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    
    # Barras apiladas de licitaciones y órdenes de compra
    p1 = ax1.bar(t_year['anio'], t_year['ordenes_compra'], label='Órdenes de Compra', color=COLOR_SECONDARY, width=0.65)
    p2 = ax1.bar(t_year['anio'], t_year['licitaciones'], bottom=t_year['ordenes_compra'], label='Licitaciones Públicas', color=COLOR_PRIMARY, width=0.65)
    
    ax1.set_ylabel('Número de Procesos de Compra', fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax1.set_xlabel('Año de Publicación / Emisión (2007 - 2026)', fontsize=10, fontweight='bold')
    ax1.set_xticks(t_year['anio'])
    ax1.set_xticklabels(t_year['anio'], rotation=45, ha='right', fontsize=9)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.set_ylim(0, 1250)
    
    # Anotación hito Ley 21.455
    ax1.axvline(x=2022, color=COLOR_ACCENT, linestyle=':', linewidth=1.5)
    ax1.annotate('Promulgación Ley Marco 21.455\n(Junio 2022: +105% hacia 2024)',
                 xy=(2022, 500), xytext=(2016.5, 950),
                 arrowprops=dict(facecolor=COLOR_ACCENT, shrink=0.05, width=1, headwidth=6),
                 fontsize=9, fontweight='bold', color=COLOR_ACCENT,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF2E6', edgecolor=COLOR_ACCENT, alpha=0.9))

    # Etiqueta de valor en barra 2024
    row_2024 = t_year[t_year['anio'] == 2024].iloc[0]
    ax1.text(2024, row_2024['total'] + 25, f"{int(row_2024['total']):,}\nproc.", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_PRIMARY)

    ax1.set_title('Evolución Histórica de Compras Públicas en Cambio Climático en Chile (2007–2026)\nQuiebre Estructural tras la Ley Marco de Cambio Climático (Ley 21.455)',
                  fontsize=12, fontweight='bold', pad=15, color=COLOR_PRIMARY)
    ax1.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    
    plt.tight_layout()
    fig1_path = FIG_DIR / "fig1_evolucion_temporal_ley21455.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # FIGURA 2: GOBERNANZA MULTINIVEL (MUNICIPAL VS CENTRAL VS GORE)
    # -------------------------------------------------------------
    print("Generando Figura 2: Gobernanza multinivel...")
    t_gov = df.groupby('nivel_institucional').agg(
        procesos=('codigo_proceso', 'count'),
        monto_millones=('monto_num', lambda x: x.sum() / 1e6)
    ).sort_values(by='procesos', ascending=True).reset_index()

    fig, (ax_p, ax_m) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    
    # 2A: Número de procesos
    bars_p = ax_p.barh(t_gov['nivel_institucional'], t_gov['procesos'], color=COLOR_PRIMARY, height=0.6)
    ax_p.set_title('A. Número de Procesos de Compra', fontsize=10.5, fontweight='bold', color=COLOR_PRIMARY)
    ax_p.set_xlabel('Total Procesos', fontsize=9.5, fontweight='bold')
    ax_p.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars_p:
        w = b.get_width()
        ax_p.text(w + 50, b.get_y() + b.get_height()/2, f"{int(w):,}", va='center', fontsize=8.5, color=COLOR_DARK)
    ax_p.set_xlim(0, max(t_gov['procesos']) * 1.18)

    # 2B: Monto licitado
    t_gov_m = t_gov.sort_values(by='monto_millones', ascending=True)
    bars_m = ax_m.barh(t_gov_m['nivel_institucional'], t_gov_m['monto_millones'], color=COLOR_SECONDARY, height=0.6)
    ax_m.set_title('B. Monto Total Licitado (Millones CLP)', fontsize=10.5, fontweight='bold', color=COLOR_SECONDARY)
    ax_m.set_xlabel('Millones de Pesos (CLP)', fontsize=9.5, fontweight='bold')
    ax_m.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars_m:
        w = b.get_width()
        ax_m.text(w + 3000, b.get_y() + b.get_height()/2, f"${w:,.0f}M", va='center', fontsize=8.5, color=COLOR_DARK)
    ax_m.set_xlim(0, max(t_gov_m['monto_millones']) * 1.25)
    ax_m.set_yticklabels([])

    fig.suptitle('Gobernanza Multinivel de las Compras Climáticas del Estado de Chile (2007–2026)\nDistribución por Tipo de Organismo Comprador',
                 fontsize=12, fontweight='bold', y=1.02, color=COLOR_PRIMARY)
    plt.tight_layout()
    fig2_path = FIG_DIR / "fig2_gobernanza_multinivel_montos.png"
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # FIGURA 3: SUBCATEGORÍAS TEMÁTICAS
    # -------------------------------------------------------------
    print("Generando Figura 3: Subcategorías temáticas...")
    t_sub = df.groupby(['subcategoria', 'tipo_registro']).size().unstack(fill_value=0).reset_index()
    t_sub['total'] = t_sub['licitacion'] + t_sub['orden_compra']
    t_sub = t_sub.sort_values(by='total', ascending=True)

    labels_map = {
        'Nucleo_Exacto': 'Núcleo Exacto (Cambio/Adaptación/Mitigación)',
        'Transicion_SBN': 'Transición Energética y SBN (Eficiencia/H2V/Electro)',
        'Gases_Descarbonizacion': 'Gases y Descarbonización (Huella/GEI)',
        'Instrumentos_Ley21455': 'Instrumentos Ley 21.455 (PACCC/PARCC/ECLP)'
    }
    t_sub['subcat_nombre'] = t_sub['subcategoria'].map(labels_map)

    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    b1 = ax.barh(t_sub['subcat_nombre'], t_sub['orden_compra'], label='Órdenes de Compra', color=COLOR_SECONDARY, height=0.55)
    b2 = ax.barh(t_sub['subcat_nombre'], t_sub['licitacion'], left=t_sub['orden_compra'], label='Licitaciones Públicas', color=COLOR_PRIMARY, height=0.55)

    ax.set_xlabel('Número de Procesos', fontsize=10, fontweight='bold')
    ax.set_title('Distribución de Compras por Eje Temático y Modalidad de Contratación',
                 fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.legend(loc='lower right', fontsize=9)

    for i, r in t_sub.reset_index().iterrows():
        ax.text(r['total'] + 60, i, f"{r['total']:,} ({r['total']/len(df)*100:.1f}%)", va='center', fontsize=8.5, fontweight='bold')
    ax.set_xlim(0, max(t_sub['total']) * 1.18)

    plt.tight_layout()
    fig3_path = FIG_DIR / "fig3_subcategorias_tematicas.png"
    plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # FIGURA 4: TOP 10 ORGANISMOS COMPRADORES
    # -------------------------------------------------------------
    print("Generando Figura 4: Top compradores...")
    t_org = df.groupby('organismo_comprador').size().sort_values(ascending=True).tail(12).reset_index(name='total')
    
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    bars = ax.barh(t_org['organismo_comprador'], t_org['total'], color=COLOR_PRIMARY, height=0.6)
    
    ax.set_xlabel('Número Total de Procesos Adjudicados', fontsize=10, fontweight='bold')
    ax.set_title('Top 12 Instituciones Públicas Compradoras en Cambio Climático (2007–2026)',
                 fontsize=11.5, fontweight='bold', pad=12, color=COLOR_PRIMARY)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    for b in bars:
        w = b.get_width()
        ax.text(w + 15, b.get_y() + b.get_height()/2, f"{int(w):,}", va='center', fontsize=8.5, fontweight='bold')
    ax.set_xlim(0, max(t_org['total']) * 1.12)
    
    plt.tight_layout()
    fig4_path = FIG_DIR / "fig4_top_organismos_compradores.png"
    plt.savefig(fig4_path, dpi=300, bbox_inches='tight')
    plt.close()

    print("Todas las figuras generadas exitosamente en:", FIG_DIR)

if __name__ == "__main__":
    generate_all_charts()
