---
title: "Brief Estadístico y Gobernanza: Compras Públicas en Cambio Climático en Chile (2007–2026)"
author: "Eduardo Vega Toledo"
requested_by: "Valentina Cariaga Cerda"
data_architect: "Eduardo Vega Toledo"
project: "P089 / P040"
contact: "evega.ap@gmail.com"
license: "CC-BY-4.0"
date: "2026-08-25"
checksum_sha256: "6f7ae7f02b89d9f5ad695c13a06a6242a691dae809b3b57bcb7c4cead1e52820"
---

# Brief Estadístico y Gobernanza: Compras Públicas en Cambio Climático en Chile (2007–2026)

**Elaborado por:** Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)  
**A encargo de:** Valentina Cariaga Cerda  
**Proyecto:** P089 / P040  
**Fecha:** Agosto de 2026  
**Dataset analizado:** `Catastro_Cambio_Climatico_ChileCompra.xlsx` (9.086 procesos únicos)  

---

## 1. Resumen Ejecutivo

El análisis del gasto transaccional del Estado de Chile en cambio climático a lo largo de dos décadas (2007–2026) revela una **transformación profunda en la arquitectura institucional y en las prioridades de contratación pública**. Lo que durante 15 años constituyó una agenda marginal y predominantemente discursiva, experimentó un **quiebre estructural a partir de la promulgación de la Ley Marco de Cambio Climático (Ley 21.455)** en junio de 2022.

* **Volumen transado acumulado:** Superior a **$359.604 millones de pesos chilenos** (~USD 380 millones).
* **Composición de procesos:** 2.287 Licitaciones Públicas (25,2%) y 6.799 Órdenes de Compra directas o derivadas de convenios marco (74,8%).
* **Presencia territorial:** 2.604 compras ejecutadas directamente por gobiernos locales (municipalidades), cubriendo municipios de todas las regiones del país.

---

## 2. Dinámica Temporal: El Efecto Estructural de la Ley Marco (Ley 21.455)

La evolución anual del número de procesos evidencia con nitidez el impacto vinculante de la legislación ambiental sobre el aparato del Estado:

| Período | Año | N° Licitaciones | N° Órdenes de Compra | Total Procesos | Monto Total (Millones CLP) | Hito / Contexto Institucional |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Fase 1: Emergencia** | 2007 | 50 | 228 | 278 | $2.618M | Primeras consultorías de inventario GEI. |
| | 2011 | 143 | 222 | 365 | $4.791M | Creación formal del Ministerio del Medio Ambiente. |
| | 2015 | 54 | 396 | 450 | $8.009M | Compromisos NDC / Acuerdo de París. |
| **Fase 2: Visibilidad** | 2017 | 48 | 584 | 632 | $12.233M | Impulso de metas de electromovilidad y eficiencia. |
| | 2019 | 62 | 458 | 520 | $5.906M | Presidencia chilena de la COP25. |
| | 2021 | 134 | 295 | 429 | $16.079M | Tramitación legislativa de la Ley Marco. |
| **Fase 3: Vinculante (Ley 21.455)** | **2022** | **123** | **377** | **500** | **$8.178M** | **Promulgación Ley Marco de Cambio Climático.** |
| | **2023** | **207** | **570** | **777** | **$21.232M** | Implementación de metas sectoriales (+55% anual). |
| | **2024** | **237** | **790** | **1.027** | **$111.506M** | **Máximo histórico (+105% vs 2022).** |
| | **2025** | **286** | **666** | **952** | **$68.144M** | Maduración de carteras y licitaciones de obras. |
| | **2026\*** | **96** | **290** | **386** | **$30.269M** | *Cierre parcial a julio de 2026.* |

```
Evolución del Gasto Licitado Anual (Millones CLP)
120.000M ┤                                                ╭───╮ ($111.506M)
100.000M ┤                                                │   │
 80.000M ┤                                                │   │  ╭───╮ ($68.144M)
 60.000M ┤                                                │   │  │   │
 40.000M ┤                                                │   │  │   │  ╭───╮* ($30.269M)
 20.000M ┤ ╭───╮  ╭───╮  ╭───╮  ╭───╮  ╭───╮  ╭───╮  ╭───╮│   │  │   │  │   │
      0M ┴─┴───┴──┴───┴──┴───┴──┴───┴──┴───┴──┴───┴──┴───┴┴───┴──┴───┴──┴───┴─
          2015   2017   2019   2021   2022   2023     2024     2025     2026*
```

---

## 3. Radiografía Subnacional: Gobernanza Multinivel (Municipios y GOREs)

Uno de los hallazgos más relevantes para la sociología y ciencia política ambiental radica en la **distribución territorial y descentralizada de las compras climáticas**:

```
Distribución de Procesos por Nivel Institucional (Total: 9.086)
┌────────────────────────────────────────────────────────┬─────────────┬──────────────┐
│ Nivel Institucional                                    │ N° Procesos │ Monto (CLP)  │
├────────────────────────────────────────────────────────┼─────────────┼──────────────┤
│ 1. Gobierno Central y Servicios Públicos (CONAF/MMA)   │    4.897    │  $59.104M    │
│ 2. Municipalidades (Gobiernos Locales - 345 Comunas)   │    2.605    │ $197.285M    │
│ 3. Universidades y Centros Académicos                  │      930    │   $3.668M    │
│ 4. Sector Salud (Hospitales / Eficiencia Térmica)      │      288    │   $7.493M    │
│ 5. Gobiernos Regionales (GORE - 16 Regiones)           │      142    │   $2.917M    │
│ 6. Defensa y Fuerzas Armadas (Resiliencia / Antártica) │      139    │   $1.306M    │
│ 7. Empresas Públicas del Estado (Metro / EFE / ENAP)   │       85    │     $429M    │
└────────────────────────────────────────────────────────┴─────────────┴──────────────┘
```

---

### A. Nivel Intermedio: Los Gobiernos Regionales (GOREs) y los PARCC
Los **Gobiernos Regionales registran 142 procesos licitados ($2.917 millones)** orientados a la escala mesoterritorial:
* **Foco de contratación:** Elaboración de los **Planes de Acción Regional de Cambio Climático (PARCC)**, balances hídricos regionales, estrategias de mitigación en transporte interurbano y modelación de riesgo de desastres.
* **GOREs más activos:**
  1. *GORE O'Higgins* (18 procesos / $785M): Planes de adaptación agroclimática y gestión de cuencas.
  2. *GORE Metropolitano de Santiago* (17 procesos / $838M): Planes de arborización metropolitana e islas de calor.
  3. *GORE Atacama* (13 procesos / $238M): Infraestructura de contención aluvional y sequía extrema.
  4. *GORE La Araucanía* (12 procesos / $20M) y *GORE Coquimbo* (15 procesos / $32M).

---

### B. Nivel Local: Las Municipalidades y los PACCC
El **28,7% del total de compras del Estado (2.605 procesos)** proviene de municipalidades, concentrando el **54,8% del presupuesto licitado ($197.285 millones)** debido a grandes obras comunales de infraestructura verde y eficiencia:

* **Top Municipios Contratantes:**
  1. *I. Municipalidad de Concepción* (127 compras): Liderazgo en gestión de residuos, eficiencia energética en alumbrado y mitigación urbana.
  2. *I. Municipalidad de Copiapó* (91 compras): Adaptación hídrica y resiliencia ante eventos extremos de sequía/aluvión.
  3. *I. Municipalidad de Lampa* (66 compras): Conservación de humedales urbanos y Soluciones Basadas en la Naturaleza (SBN).
  4. *I. Municipalidad de El Bosque* (61 compras): Planes de arbolado urbano y eficiencia térmica.
  5. *I. Municipalidad de Temuco* (60 compras): Planes de descontaminación y recambio de calefacción.
* **Adopción de los PACCC (Planes de Acción Comunal de Cambio Climático):** La exigencia legal de la Ley 21.455 generó una ola de licitaciones de consultoría técnica comunal desde 2023, visibilizando **fuertes brechas de capacidad técnica y presupuestaria**: mientras municipios del cono oriente o capitales regionales licitan consultorías de $30 a $60 millones, municipios rurales o periféricos dependen de fondos SUBDERE o de la asistencia técnica de la AChM.

---

## 4. Ecosistema de Proveedores y Concentración de Mercado

El mercado proveedor estatal en cambio climático se estructura en tres capas diferenciadas:

```
                      ┌────────────────────────────────────────┐
                      │        ECOSISTEMA DE PROVEEDORES       │
                      └───────────────────┬────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        ▼                                 ▼                                 ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│  Consultoría de  │            │  Centros de I+D  │            │   Gremios y Red  │
│  Ingeniería      │            │  Universitaria   │            │   Municipal      │
│  Especializada   │            │                  │            │                  │
├──────────────────┤            ├──────────────────┤            ├──────────────────┤
│ - Deuman         │            │ - U. de Chile    │            │ - AChM           │
│ - Poch / WSP     │            │ - PUC            │            │ - Asoc. Regional │
│ - Consultoras    │            │ - U. del Bío-Bío │            │   de Municipios  │
│   Ambientales    │            │ - U. Magallanes  │            │                  │
└──────────────────┘            └──────────────────┘            └──────────────────┘
```

1. **Consultoría Privada Especializada:** Empresas de ingeniería ambiental como `Deuman` (69 procesos adjudicados por $1.765M) concentran los estudios de mayor complejidad técnica (inventarios de emisiones, balances de carbono y hojas de ruta de hidrógeno verde).
2. **Universidades como Asesores de Política Pública:** La `Universidad de Chile` (88 adjudicaciones por $1.380M) y la `Pontificia Universidad Católica de Chile` (55 adjudicaciones por $644M) actúan como validadores científicos para ministerios y agencias públicas.
3. **Intermediación Gremial Municipal:** La `Asociación Chilena de Municipalidades (AChM)` (105 contratos) cumple un rol estratégico capacitando a equipos técnicos locales y estandarizando propuestas de ordenanzas climáticas.

---

## 5. Preguntas de Investigación y Aproximaciones Metodológicas Propuestas

A partir del dataset consolidado (`Catastro_Cambio_Climatico_ChileCompra.csv`), se proponen 4 agendas de investigación empírica con sus respectivos diseños metodológicos y estrategias de cruce de datos:

---

### Agenda 1: Capacidad Estatal, Desigualdad Territorial y Brechas de Adopción Local
* **Pregunta de Investigación:** ¿En qué medida los ingresos propios comunales, la ruralidad, la dependencia del Fondo Común Municipal (FCM) y la presencia de direcciones ambientales locales condicionan la probabilidad y celeridad de licitar instrumentos climáticos (`PACCC`)?
* **Aproximación Metodológica:**
  1. **Modelos Econométricos de Elección Discreta (Logit / Probit):** Variable dependiente binaria $Y_i \in \{0, 1\}$ que indica si el municipio $i$ ha licitado un PACCC o compras de mitigación/adaptación.
  2. **Regresión Tobit / Poisson:** Para modelar el monto per cápita licitado y el conteo de procesos, controlando por censura a la izquierda (municipios con cero compras).
  3. **Análisis de Supervivencia (Cox Proportional Hazards Model):** Evaluar el tiempo transcurrido (en meses desde junio de 2022) hasta la primera licitación formal de un PACCC comunal.
* **Cruce de Datos Externos Recomendado:**
  * **SINIM (SUBDERE):** Ingresos Propios Permanentes (IPP), dependencia FCM, dotación de personal municipal y gasto en medio ambiente.
  * **CASEN / Censo (INE):** Índice de pobreza multidimensional, ruralidad y escolaridad comunal.
  * **CR2 (Centro de Ciencia del Clima y la Resiliencia):** Índice de riesgo climático y sequía a nivel comunal.

---

### Agenda 2: Evaluación de Impacto Normativo: El "Efecto Ley Marco 21.455"
* **Pregunta de Investigación:** ¿Cuál es el impacto causal de la entrada en vigencia de la Ley Marco de Cambio Climático sobre el volumen, montos y desconcentración regional de la contratación pública ambiental?
* **Aproximación Metodológica:**
  1. **Análisis de Series Temporales Interrumpidas (Interrupted Time Series Analysis - ITSA):** Modelar el quiebre de tendencia mensual en el gasto y número de licitaciones pre-2022 versus post-2022, testeando cambios de nivel y pendiente.
  2. **Diferencias en Diferencias (DiD) con Grupo de Control:** Comparar organismos formalmente obligados por la Ley (Ministerios sectoriales, MMA, GOREs, Municipalidades) contra organismos públicos con mandatos no climáticos.

---

### Agenda 3: Redes de Política Pública y Concentración de Mercado (Policy Networks)
* **Pregunta de Investigación:** ¿Cómo se estructura la red de gobernanza público-privada en compras climáticas y cuán concentrado está el mercado de consultoría técnica frente a la academia y los gremios municipales?
* **Aproximación Metodológica:**
  1. **Análisis de Redes Sociales Bipartitas (Two-Mode Network Analysis):** Grafo con dos conjuntos de nodos: *Organismos Compradores* ($U$) y *Proveedores Adjudicados* ($V$), con aristas ponderadas por el volumen transado.
  2. **Métricas Estructurales de Red:** Centralidad de intermediación (*Betweenness*), centralidad de autovalor (*Eigenvector*) y algoritmos de detección de comunidades (*Louvain Modularity*) para mapear clústeres cerrados de contratación.
  3. **Índice de Herfindahl-Hirschman (HHI):** Medir el nivel de concentración económica en submercados específicos (ej. inventarios GEI vs. luminarias LED vs. consultoría de ordenanzas).

---

### Agenda 4: Análisis Textual y Calidad de la Demanda Estatal (NLP & Topic Modeling)
* **Pregunta de Investigación:** ¿Qué prioriza discursiva y materialmente el Estado al comprar "clima"? ¿Predominan diagnósticos abstractos (*soft governance*) o infraestructura tangible (*hard adaptation*)?
* **Aproximación Metodológica:**
  1. **Modelado Estructural de Tópicos (Structural Topic Model - STM / BERTopic):** Aplicado sobre las columnas `descripcion` y `texto_fragmento`, utilizando `nivel_institucional` y `año` como covariables de prevalencia temática.
  2. **Clasificación Supervisada (Hard vs. Soft Adaptation):** Algoritmo de clasificación léxico-sintáctico para categorizar compras entre intervenciones tangibles (obras, recambio tecnológico, arbolado) versus intervenciones blandas (diagnósticos, eventos, capacitaciones, consultorías de diseño).
