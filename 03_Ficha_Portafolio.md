# Ficha de Portafolio — P089

**Proyecto:** Catastro de Compras Públicas y Cambio Climático en Chile (2007–julio 2026)  
**Rol:** Data Architect / Public Policy Data Engineer  
**Autor:** Eduardo Vega Toledo  
**A encargo de:** Valentina Cariaga Cerda

## Caso

Diseño de un pipeline reproducible para explorar datos masivos de Mercado Público y construir una taxonomía auditable de compras relacionadas con cambio climático. La auditoría Harness v1.1 distinguió correctamente entre **9.086 asignaciones de clasificación** y **8.894 procesos distintos**, detectó un error de parsing de coma decimal y sustituyó métricas monetarias combinadas por magnitudes administrativas separadas.

## Resultado auditado

- 8.894 procesos distintos: 2.175 licitaciones + 6.719 OC.
- 178 procesos multicategoría.
- $249.813,979 millones CLP registrados en licitaciones distintas.
- $105.536,060 millones CLP registrados en OC distintas.
- Suite de contrato reproducible + GitHub Actions.
- Advertencias explícitas de provenance y precisión semántica.

## Stack

Python, DuckDB, Pandas, regex, CSV/XLSX, automatización de QA, Git/GitHub Actions y principios de reproducibilidad.

## Aprendizaje metodológico

El principal valor del proyecto no es sólo el volumen procesado, sino el control de la **unidad de análisis**, la separación de magnitudes administrativas y la capacidad de auditar afirmaciones antes de publicarlas. El incremento post-2022 se presenta como asociación temporal; la causalidad se reserva para un diseño de identificación posterior.
