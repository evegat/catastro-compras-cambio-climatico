# Ficha de Portafolio: Catastro Nacional de Compras Públicas en Cambio Climático de Chile (2007–2026)

**Rol:** Data Architect & Public Policy Data Engineer  
**Autor:** Eduardo Vega Toledo  
**Cliente / Solicitante:** Valentina Cariaga Cerda  
**Proyecto:** P089 (Catastro Compras Cambio Climático) / P040 (Gobernanza Climática Subnacional)  
**Periodo:** 2007 – 2026 (20 años continuos / 235 meses / 470 bases masivas)  
**Repositorio / Entregable:** Base de Datos Abierta (CSV/XLSX), Informe Ejecutivo en Word (.docx), Suite de Visualizaciones y Pipeline de Replicabilidad en Python.  

---

## 1. Resumen del Proyecto / Case Study

Construcción del primer catastro histórico integral y determinista de compras públicas, licitaciones y órdenes de compra del Estado de Chile asociadas a **cambio climático, mitigación, adaptación, descarbonización y eficiencia energética**, cubriendo la totalidad del registro transaccional de Mercado Público (ChileCompra) desde enero de 2007 hasta julio de 2026.

El pipeline procesó **más de 470 bases de datos mensuales masivas (varios gigabytes de datos brutos)** para estructurar un corpus limpio de **9.086 procesos únicos deduplicados**, equivalentes a **$359.604 millones de pesos chilenos** (~USD 380 millones transados o presupuestados).

---

## 2. Desafíos Técnicos e Innovación Metodológica

1. **Ingeniería de Datos y Procesamiento de Alto Rendimiento:**
   - Implementación de un pipeline en **Python + DuckDB en memoria** con ejecución en paralelo (16 hilos de procesamiento) para escaneo regex sobre millones de líneas de transacciones en minutos.
2. **Taxonomía Léxica Multinivel y Control Estricto de Falsos Positivos:**
   - Clasificación en 4 subcategorías conceptuales (*Núcleo Exacto*, *Instrumentos Ley 21.455*, *Gases y Descarbonización*, *Transición y SBN*).
   - Filtro semántico de exclusión negativa para eliminar falsos positivos administrativos comunes en el sector público (*clima laboral*, *clima organizacional*, *aire acondicionado*, etc.).
3. **Desagregación de Mecanismos de Contratación y Gobernanza Multinivel:**
   - Clasificación institucional precisa: Municipalidades (2.605 compras), Gobierno Central (4.897), Academia/Universidades (930), Sector Salud (288), GOREs (142), Defensa (139) y Empresas Públicas (85).
   - Identificación de mecanismos legales: Licitación Pública (24,8%), Convenio Marco (25,1%), Compra Ágil (11,0%) y **Trato Directo Excepcional (37,6%)**, este último clave para analizar respuestas a emergencias y sequías.
4. **Prevención de Doble Contabilización:**
   - Tratamiento diferenciado entre **Licitaciones Públicas** (presupuestos marco plurianuales de concesiones y obras) y **Órdenes de Compra** (gasto transaccional unitario).
5. **Auditoría Automatizada Extrema:**
   - Desarrollo de una suite de pruebas automatizadas con **50/50 checks superados (100% de paridad, cuadratura matemática y cero duplicados)**.

---

## 3. Impacto y Hallazgos Clave

* **Quiebre Estructural por la Ley Marco de Cambio Climático (Ley 21.455 de 2022):** De un promedio histórico de 350-450 compras anuales, las contrataciones escalaron a 777 en 2023 (+55%) y alcanzaron su máximo histórico en 2024 con 1.027 compras (+105%), demostrando el impacto causal de la legislación en la demanda pública.
* **Liderazgo Presupuestario Municipal:** Los gobiernos locales concentran el 54,8% del gasto licitado ($192.888M) debido a grandes proyectos de infraestructura verde, recambio LED y planes comunales (PACCC).
* **Concentración del Ecosistema de Proveedores:** Mapeo de la interacción entre consultoría ambiental privada (`Deuman`), validación científica universitaria (`U. de Chile`, `PUC`) y gremios articuladores (`AChM`).

---

## 4. Stack Tecnológico Utilizado

* **Lenguajes y Procesamiento:** Python 3.13, DuckDB (OLAP in-memory SQL), Pandas, Regular Expressions (Regex).
* **Automatización y Entregables:** `python-docx` (generación de informes Word estilizados), `matplotlib` (visualizaciones vectoriales y 300 DPI), `openpyxl` (modelado multi-pestaña en Excel).
* **Metodología y Repositorios:** Open Science / FAIR data principles, metadatos estructurados, control de hashes SHA-256.

---

## 5. Skills Demostradas para el Portafolio

* *Data Engineering & Big Data ETL*
* *Public Procurement & Policy Analytics (ChileCompra / Mercado Público)*
* *Applied Econometrics & Causal Research Design (ITSA, DiD, Survival Analysis)*
* *Automated Quality Assurance & Data Auditing*
* *Executive & Scientific Reporting*
