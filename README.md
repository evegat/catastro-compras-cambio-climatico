# Catastro Histórico de Compras Públicas en Cambio Climático de Chile (2007–2026)

[![Licencia](https://img.shields.io/badge/Licencia-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Cobertura](https://img.shields.io/badge/Cobertura-2007_a_2026_(470_bases)-green.svg)](https://datosabiertos.chilecompra.cl/)
[![Auditoría de Calidad](https://img.shields.io/badge/Auditor%C3%ADa-50%2F50_Tests_Superados_(100%25)-brightgreen.svg)]()
[![Stack](https://img.shields.io/badge/Stack-Python_|_DuckDB_|_Pandas-orange.svg)]()

> **Pipeline de Ingeniería de Datos y Catastro Nacional de Adquisiciones Públicas en Mitigación, Adaptación y Gobernanza Climática.**  
> **Elaborado por:** Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)  
> **Contacto:** `evega.ap@gmail.com`  
> **A encargo de:** Valentina Cariaga Cerda  
> **Proyecto:** `P089` (Catastro Cambio Climático) / `P040` (Gobernanza Climática Subnacional)  

---

## 1. Resumen Ejecutivo y Alcance

Este repositorio alberga el primer catastro determinista, exhaustivo y auditable de compras públicas y licitaciones del Estado de Chile orientadas a la acción climática, abarcando **20 años continuos de registros transaccionales en Mercado Público (ChileCompra) desde enero de 2007 hasta julio de 2026** (470 bases mensuales procesadas).

El dataset reúne **9.086 procesos únicos deduplicados** (2.287 licitaciones públicas y 6.799 órdenes de compra), que representan un volumen transado y presupuestado acumulado de **$359.604 millones de pesos chilenos (~USD 380 millones)**.

### Hallazgos Principales

1. **Quiebre Estructural tras la Ley Marco de Cambio Climático (Ley 21.455):**
   * Tras la promulgación de la ley en junio de 2022, las compras escalaron de un promedio histórico de 400 procesos anuales a **777 en 2023 (+55%)** y alcanzaron su **máximo histórico en 2024 con 1.027 contrataciones (+105%)**, transando más de $111.506 millones en un solo año.
2. **Liderazgo Presupuestario Municipal:**
   * Las **Municipalidades (Gobiernos Locales)** concentran el **54,8% del presupuesto licitado ($192.888 millones)** en grandes concesiones plurianuales de áreas verdes sustentables, eficiencia energética en alumbrado público y consultorías de Planes de Acción Comunal de Cambio Climático (`PACCC`).
3. **El Rol del Trato Directo como Mecanismo de Emergencia:**
   * El **37,6% de todas las compras (3.417 órdenes de compra por $24.476 millones)** corresponden a **Trato Directo (Mecanismo Excepcional)**, reflejando respuestas urgentes del Estado ante sequías extremas, aluviones, incendios y arriendo de camiones aljibe.

---

## 2. Estructura de Entregables del Repositorio

```
📁 P089-Catastro-Compras-Cambio-Climatico/
│
├── 📘 Catastro_Compras_Cambio_Climatico_Informe_Metodologico_y_Estadistico.docx
│     └── Informe ejecutivo completo imprimible en Word (con 5 figuras 300 DPI, codebook y advertencias).
│
├── 📊 Catastro_Cambio_Climatico_ChileCompra.xlsx
│     └── Libro de datos multi-pestaña (Catastro Completo, Resumen Institucional, Mecanismos, Subcategorías, GOREs, Top Organismos).
│
├── 📄 Catastro_Cambio_Climatico_ChileCompra.csv
│     └── Formato abierto (UTF-8 con BOM) delimitado por ';' con 23 variables, listo para R, Python o Stata.
│
├── 🐍 generar_graficas_catastro.py
│     └── Script autónomo para regenerar las 5 figuras estadísticas en alta resolución (300 DPI) con un solo comando.
│
├── 🐍 replicar_catastro_chilecompra.py
│     └── Script pedagógico y comentado para replicar la extracción de datos desde las bases masivas de ChileCompra.
│
├── 📑 01_Ficha_Metodologica_y_Codebook.md
│     └── Documentación FAIR, árboles de decisión regex y definiciones operacionales de variables.
│
├── 📈 02_Brief_Estadistico_Compras_Climaticas.md
│     └── Análisis de gobernanza multinivel, concentración de mercado y 4 agendas metodológicas de investigación.
│
├── 📂 figuras_catastro/
│     ├── fig1_evolucion_temporal_ley21455.png
│     ├── fig2_mecanismos_contratacion.png
│     ├── fig3_gobernanza_multinivel.png
│     ├── fig4_subcategorias_tematicas.png
│     └── fig5_top_organismos_compradores.png
│
└── 📂 scripts/
      ├── auditoria_extremista_catastro.py  (Suite de 50 pruebas de calidad superadas al 100%)
      └── generar_documento_word.py         (Compilador automático del informe .docx)
```

---

## 3. Radiografía de Mecanismos de Contratación

| Tipo de Registro | Mecanismo Legal de Contratación | N° Procesos | Monto Total (CLP) | % Participación | Relevancia en Políticas Públicas |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Licitación** | **Licitación Pública (LP / LE / LR)** | **2.250** | **$242.277M** | **24,8%** | Concursos abiertos y competitivos de grandes proyectos (`PACCC`, parques, obras). |
| **Licitación** | **Licitación Privada (CO / B2)** | **37** | **$139M** | **0,4%** | Concursos cerrados por invitación calificada. |
| **Orden de Compra** | **Trato Directo (Excepcional / TD / E2)** | **3.417** | **$24.476M** | **37,6%** | **Mecanismo Excepcional:** Emergencias climáticas, sequías, camiones aljibe y proveedor único. |
| **Orden de Compra** | **Convenio Marco (Catálogo / CM)** | **2.279** | **$3.671M** | **25,1%** | Adquisición directa por catálogo (luminarias LED, pasajes, consultorías estándar). |
| **Orden de Compra** | **Compra Ágil (< 30 UTM / AG)** | **999** | **$745M** | **11,0%** | Compras rápidas descentralizadas para micro-requerimientos comunales. |
| **Orden de Compra** | **Otras Órdenes de Compra** | **104** | **$894M** | **1,1%** | Órdenes de servicio y regularizaciones administrativas. |
| **TOTAL** | **Universo Consolidado** | **9.086** | **$359.604M** | **100.0%** | **Cero duplicados en clave compuesta.** |

---

## 4. Gobernanza Multinivel: Distribución por Tipo de Organismo

| Nivel Institucional | N° Licitaciones (Concursos) | Monto Licitaciones ($M CLP)<br>*(Presupuesto Marco Plurianual)* | N° Órdenes de Compra (OC) | Monto Órdenes Compra ($M CLP)<br>*(Gasto Transaccional Unitario)* | Total Procesos Combinados |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gobierno Central y Servicios Públicos** | 1.176 | $37.268,14M | 3.726 | $21.836,77M | **4.902** |
| **Municipalidades (Gobiernos Locales)** | 696 | **$192.888,08M** | 1.906 | **$4.397,11M** | **2.602** |
| **Universidades y Academia** | 165 | $1.834,53M | 763 | $1.833,57M | **928** |
| **Sector Salud** | 104 | $6.877,20M | 182 | $615,62M | **286** |
| **Gobiernos Regionales (GORE)** | 50 | $2.247,28M | 92 | $669,57M | **142** |
| **Defensa y Fuerzas Armadas** | 57 | $1.004,18M | 82 | $302,23M | **139** |
| **Empresas Públicas del Estado** | 39 | $296,98M | 48 | $131,52M | **87** |
| **TOTAL CONSOLIDADO** | **2.287** | **$242.416,40M** | **6.799** | **$29.732,08M** | **9.086** |

> [!WARNING]
> **ADVERTENCIA METODOLÓGICA CONTRA LA DOBLE CONTABILIZACIÓN:**  
> **NO SUMAR aritméticamente los montos de Licitaciones con los de Órdenes de Compra.**  
> * Las **Licitaciones** registran el *presupuesto marco plurianual* comprometido en bases de licitación (ej. contratos de mantención comunal de áreas verdes o luminarias por 5 años).  
> * Las **Órdenes de Compra** registran las *transacciones unitarias y despachos efectivamente pagados* en el catálogo electrónico.  
> * Para evaluar **gasto real pagado**, filtrar por `tipo_registro == 'orden_compra'`. Para evaluar **convocatorias a concursos y proyectos macro**, filtrar por `tipo_registro == 'licitacion'`.

---

## 5. Agendas de Investigación y Diseños Metodológicos Propuestos

Se formulan 4 agendas de investigación cuantitativa listas para ser ejecutadas sobre este corpus:

1. **Capacidad Estatal y Brechas Territoriales Locales:**
   * Modelos Logit/Probit de adopción y regresiones Tobit para modelar montos per cápita de planes comunales (`PACCC`).
   * Cruces recomendados: **SINIM (SUBDERE)** (ingresos propios y dependencia del Fondo Común Municipal) y **CASEN / Censo** (pobreza multidimensional y ruralidad).
2. **Evaluación de Impacto Normativo (Efecto Ley 21.455):**
   * Series Temporales Interrumpidas (ITSA) mensual y Diferencias en Diferencias (DiD) entre organismos directamente obligados versus no obligados.
3. **Redes de Política Pública y Concentración de Proveedores (Policy Networks):**
   * Análisis de redes bipartitas (Two-Mode Networks) entre organismos compradores y contratistas, midiendo centralidad de intermediación (*Betweenness*) e Índice HHI por submercados.
4. **Análisis Textual y Calidad de la Demanda Estatal (NLP):**
   * Structural Topic Modeling (STM) sobre glosas textuales y clasificación supervisada entre *soft governance* (diagnósticos y consultorías) versus *hard adaptation* (obras e infraestructura tangible).

---

## 6. Reproducibilidad y Uso Rápido

### Requisitos
```bash
pip install pandas matplotlib openpyxl duckdb
```

### 1. Regenerar todas las Figuras Gráficas (300 DPI)
```bash
python generar_graficas_catastro.py
```
*Generará automáticamente los 5 gráficos en la carpeta `figuras_catastro/`.*

### 2. Ejecutar la Suite de Auditoría de Calidad
```bash
python scripts/auditoria_extremista_catastro.py
```
*Ejecutará 50 pruebas deterministas de integridad, paridad CSV/Excel, control de falsos positivos y cuadratura matemática.*

---

## 7. Cita y Licencia

Este dataset y su documentación se distribuyen bajo la licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

```bibtex
@dataset{vega_toledo_2026_catastro_clima,
  author       = {Vega Toledo, Eduardo},
  title        = {Catastro Histórico de Compras Públicas en Cambio Climático de Chile (2007–2026)},
  year         = {2026},
  publisher    = {GitHub},
  version      = {1.0},
  note         = {Elaborado a encargo de Valentina Cariaga Cerda. Cobertura: 2007-2026, ChileCompra.}
}
```
