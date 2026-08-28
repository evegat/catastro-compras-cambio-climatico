# Kit de Insumos Web para evegat.cl: Proyecto P089 (Compras Públicas en Cambio Climático)

Este documento reúne todos los textos, métricas, componentes modulares y metadatos listos para copiar y pegar en la futura página web personal / portafolio de **Eduardo Vega Toledo** (`evegat.cl`).

---

## 1. Hero & Tagline (Sección Principal / Home)

### Versión 1: Enfoque Data Engineer & Administrador Público (Recomendada)
> **Eduardo Vega Toledo**  
> *Administrador Público & Data Architect*  
> Especialista en ingeniería de datos, analítica de compras públicas (Mercado Público) y modernización del Estado. Construyo pipelines reproducibles de alto rendimiento para transformar datos públicos masivos en evidencia científica y decisiones estratégicas.

### Versión 2: One-Liner para Bio / Redes / Footer
> *Data Architect transformando millones de transacciones del Estado en política pública basada en evidencia.*

---

## 2. Featured Project Card (Tarjeta Bento / Portfolio Grid)

* **Título:** Catastro Nacional de Compras Públicas en Cambio Climático (2007–2026)
* **Subtítulo:** Pipeline masivo en DuckDB y auditoría algorítmica de 20 años de Mercado Público en Chile.
* **Categoría:** *Data Engineering / Public Policy Analytics / Open Science*
* **Métricas de Impacto (Stats Badges):**
  * `470 Bases Masivas` procesadas en paralelo.
  * `9.086 Procesos Únicos` deduplicados.
  * `$359.604M CLP (~USD 380M)` analizados.
  * `100% Determinista` (0% cajas negras, 50/50 tests superados).

### Texto Descriptivo del Proyecto (Card Copy):
> Procesamiento histórico de más de 470 archivos masivos de licitaciones y órdenes de compra de ChileCompra (2007–2026). Se diseñó una arquitectura de extracción léxica en DuckDB multinúcleo con control estricto de falsos positivos (*«clima laboral»*), clasificando el gasto en 4 subcategorías, identificando la gobernanza multinivel (Municipalidades, GOREs, Central) y modelando el quiebre estructural derivado de la Ley Marco de Cambio Climático (Ley 21.455).

* **Tech Stack Badges:** `Python` `DuckDB` `Pandas` `OpenPyXL` `Matplotlib` `Automated QA` `FAIR Data`

---

## 3. Estructura para Entrada de Blog / Caso de Estudio Detallado (Long-form Post)

* **Título sugerido:** *«20 años de compras climáticas en Chile: Cómo procesamos 470 bases masivas de Mercado Público con DuckDB»*
* **Tiempo de lectura estimado:** 6 min read.

### Secciones del Artículo:
1. **El Problema:** Mercado Público transa millones de registros al año, pero carece de un etiquetado unificado para cambio climático. ¿Cómo aislar las compras reales de mitigación, adaptación e instrumentos normativos sin incluir falsos positivos administrativos?
2. **La Arquitectura Técnica:**
   * Por qué DuckDB en memoria en lugar de bases SQL tradicionales para escaneos regex en paralelo.
   * La taxonomía en 4 ejes: Núcleo Climático, Instrumentos Ley 21.455 (`PACCC`/`PARCC`/`ECLP`), Descarbonización/GEI y Transición Justa/SBN.
3. **Los Hallazgos Contraintuitivos:**
   * **El Efecto Ley 21.455:** Las compras crecieron un +105% entre 2022 y 2024.
   * **El Peso Municipal:** Los gobiernos locales concentran el 54,8% del gasto licitado ($192.888 millones), liderado por mega-concesiones de áreas verdes y eficiencia energética.
   * **La Importancia del Trato Directo:** El 37,6% de los procesos fueron contrataciones directas excepcionales por decretos de sequía y emergencias climáticas.
4. **Reproducibilidad y Código Abierto:** Inclusión de scripts en Python para replicar los datos y gráficos sin dependencias opacas.

---

## 4. Galería Visual y Assets Listos para Incrustar

Los siguientes gráficos en 300 DPI ya se encuentran generados en la carpeta `figuras_catastro/` listos para ser usados como imágenes del post:

| Nombre del Archivo | Descripción para Web / Alt Text |
| :--- | :--- |
| `fig1_evolucion_temporal_ley21455.png` | Gráfico de barras de evolución histórica 2007–2026 con quiebre post Ley 21.455. |
| `fig2_mecanismos_contratacion.png` | Gráfico horizontal de mecanismos (Licitación, Convenio Marco, Trato Directo, Compra Ágil). |
| `fig3_gobernanza_multinivel.png` | Comparativa dual de procesos vs montos entre Municipalidades, Central y GOREs. |
| `fig4_subcategorias_tematicas.png` | Desglose taxonómico de las 4 subcategorías climáticas. |
| `fig5_top_organismos_compradores.png` | Ranking de los 12 organismos compradores más activos del Estado de Chile. |

---

## 5. Schema JSON-LD Estructurado (Para SEO en evegat.cl)

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Catastro Histórico de Compras Públicas en Cambio Climático de Chile (2007-2026)",
  "description": "Base de datos abierta y consolidada con 9.086 procesos de compra del Estado de Chile en cambio climático, mitigación, adaptación y eficiencia energética.",
  "creator": {
    "@type": "Person",
    "name": "Eduardo Vega Toledo",
    "jobTitle": "Data Architect & Public Administrator",
    "email": "evega.ap@gmail.com"
  },
  "temporalCoverage": "2007-01/2026-07",
  "spatialCoverage": "Chile",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "keywords": [
    "ChileCompra",
    "Mercado Público",
    "Cambio Climático",
    "Ley 21455",
    "Gobernanza Municipal",
    "Data Engineering",
    "DuckDB"
  ]
}
```
