# Insumos web — P089

## Tarjeta de proyecto

**Catastro de Compras Públicas y Cambio Climático en Chile (2007–2026)**  
Pipeline reproducible de datos públicos para identificar y auditar adquisiciones asociadas a acción climática en Mercado Público.

**Métricas auditadas:**

- 8.894 procesos de compra distintos.
- 9.086 asignaciones temáticas en la tabla long.
- 20 años de cobertura declarada.
- Harness reproducible con pruebas de contrato y CI.

**Stack:** Python · DuckDB · regex · data QA · GitHub Actions · Open Data.

## Descripción breve

El proyecto procesa registros históricos de ChileCompra y aplica una taxonomía léxica de cuatro familias temáticas. Una auditoría posterior detectó que la exportación original sobrecontaba procesos multicategoría y que algunos montos con coma decimal no se incorporaban correctamente en resúmenes. La versión 1.1 corrige la unidad de análisis, separa licitaciones de órdenes de compra y documenta las advertencias de precisión/provenance.

## Hallazgo comunicable con cautela

Los procesos distintos aumentan de 491 en 2022 a 978 en 2024 (+99,2%). La Ley 21.455 se publica en 2022, por lo que existe una asociación temporal relevante para investigar. No se presenta como efecto causal hasta ejecutar un diseño específico de evaluación.

## SEO / Dataset copy

**Nombre:** Catastro de Compras Públicas y Cambio Climático en Chile (2007–2026)  
**Descripción:** Dataset y pipeline reproducible para analizar procesos de compra pública asociados a cambio climático, con 8.894 procesos distintos y 9.086 asignaciones temáticas auditadas.  
**Keywords:** ChileCompra, Mercado Público, cambio climático, compras públicas, municipios, Ley 21.455, data engineering, reproducibilidad.
