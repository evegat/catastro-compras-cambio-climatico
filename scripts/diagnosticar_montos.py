import pandas as pd
csv_path = r'D:\Proyectos\P089 - Catastro Compras Cambio Climatico\Catastro_Cambio_Climatico_ChileCompra.csv'
df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig', comment='#')

df_muni_lic = df[(df['nivel_institucional'] == 'Municipalidades (Gobiernos Locales)') & (df['tipo_registro'] == 'licitacion')].copy()
df_muni_lic['monto_num'] = pd.to_numeric(df_muni_lic['monto_pesos'], errors='coerce').fillna(0)

print('=== TOP 10 LICITACIONES MUNICIPALES POR MONTO ===')
top_lic = df_muni_lic.sort_values(by='monto_num', ascending=False)[['codigo_proceso', 'organismo_comprador', 'nombre', 'monto_num', 'subcategoria', 'termino_coincidente']].head(10)
for idx, r in top_lic.iterrows():
    print(f"- {r['organismo_comprador']} | {r['codigo_proceso']} | ${r['monto_num']/1e6:,.1f}M CLP | {str(r['nombre'])[:60]} | {r['termino_coincidente']}")

print('\n=== MONTO TOTAL MUNICIPAL ===')
print('Suma de Licitaciones (Presupuestos Estimados/Adjudicados):', f"${df_muni_lic['monto_num'].sum()/1e6:,.2f}M CLP")
df_muni_oc = df[(df['nivel_institucional'] == 'Municipalidades (Gobiernos Locales)') & (df['tipo_registro'] == 'orden_compra')].copy()
df_muni_oc['monto_num'] = pd.to_numeric(df_muni_oc['monto_pesos'], errors='coerce').fillna(0)
print('Suma de Órdenes de Compra (Transacciones emitidas):', f"${df_muni_oc['monto_num'].sum()/1e6:,.2f}M CLP")
