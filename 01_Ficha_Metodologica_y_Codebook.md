---
title: "Ficha Metodológica y Codebook: Catastro de Compras Públicas en Cambio Climático (2007–2026)"
author: "Eduardo Vega Toledo"
requested_by: "Valentina Cariaga Cerda"
data_architect: "Eduardo Vega Toledo"
project: "P089 / P040"
contact: "evega.ap@gmail.com"
license: "CC-BY-4.0"
date: "2026-08-25"
checksum_sha256: "6f7ae7f02b89d9f5ad695c13a06a6242a691dae809b3b57bcb7c4cead1e52820"
---

# Ficha Metodológica y Codebook: Catastro de Compras Públicas en Cambio Climático en Chile (2007–2026)

**Elaborado por:** Eduardo Vega Toledo (Administrador Público | M.Sc. | Data Engineer)  
**A encargo de:** Valentina Cariaga Cerda  
**Proyecto:** P089 (Catastro Compras Cambio Climático) / P040 (Gobernanza y Modelos Climáticos Municipales)  
**Fecha de corte:** Julio de 2026  
**Cobertura temporal:** Enero de 2007 a Julio de 2026 (235 meses continuos / 470 bases masivas)  
**Unidad de análisis:** Proceso de compra adjudicado / emitido en Mercado Público (Licitación u Orden de Compra).  

---

## 1. Fuentes de Información y Cobertura

El presente catastro se construye a partir de los registros masivos y abiertos de la **Dirección de Compras y Contratación Pública (ChileCompra)** a través de su plataforma transaccional Mercado Público.

* **Archivos procesados:** 470 bases masivas mensuales en formato CSV/Parquet (235 bases de Licitaciones Públicas `lic_` y 235 bases de Órdenes de Compra `oc_`).
* **Universo total escaneado:** ~2,5 millones de procesos licitatorios y ~28 millones de líneas de órdenes de compra.
* **Criterio de corte y exhaustividad:** Cierre formal a julio de 2026 tras descarga y verificación de integridad de las bases mensuales emitidas por la plataforma.

---

## 2. Estrategia de Extracción Léxica y Taxonomía

Debido a que Mercado Público no cuenta con un metadato o etiqueta nativa (*tag*) para clasificar compras climáticas, la identificación se realiza mediante **filtrado léxico con expresiones regulares compiladas (`regex`)** aplicadas sobre todos los campos de texto estructurado y no estructurado:

* **Campos escaneados en Licitaciones:** `Nombre`, `Descripcion`, `Nombre producto genérico`, `Nombre línea Adquisición`, `Descripción línea Adquisición`, `Rubro1`, `Rubro2`, `Rubro3`.
* **Campos escaneados en Órdenes de Compra:** `Nombre`, `Descripcion/Obervaciones`, `EspecificacionComprador`, `EspecificacionProveedor`, `NombreroductoGenerico`, `Categoria`, `RubroN1`, `RubroN2`, `RubroN3`.

### Árbol de Clasificación Temática (4 Subcategorías)

| Subcategoría | Justificación Conceptual | Patrón de Expresión Regular (`regex`) |
| :--- | :--- | :--- |
| **1. Núcleo Exacto** | Procesos formalmente orientados a la gestión, política o estudio directo del cambio climático y sus dos pilares clásicos (adaptación y mitigación). | `(?i)\b(cambio\s+clim[aá]tico\|adaptaci[oó]n\s+clim[aá]tica\|mitigaci[oó]n\s+clim[aá]tica\|resiliencia\s+clim[aá]tica\|emergencia\s+clim[aá]tica\|acci[oó]n\s+clim[aá]tica)\b` |
| **2. Instrumentos Ley 21.455** | Contrataciones vinculadas a los instrumentos formales de gestión pública creados o exigidos por la Ley Marco de Cambio Climático a nivel nacional, regional y comunal. | `(?i)\b(ley\s+(marco\s+de\s+)?cambio\s+clim[aá]tico\|ley\s+21\.?455\|plan(es)?\s+de\s+acci[oó]n\s+clim[aá]tic[ao]\|estrategia\s+clim[aá]tica\s+de\s+largo\s+plazo\|\beclp\b\|\bpamcc\b\|\bparcc\b\|plan(es)?\s+de\s+adaptaci[oó]n\s+al\s+cambio\s+clim[aá]tico\|planes\s+de\s+acci[oó]n\s+comunal\s+de\s+cambio\s+clim[aá]tico)\b` |
| **3. Gases y Descarbonización** | Medición de externalidades, inventarios de emisiones, contabilidad ambiental y metas de neutralidad de carbono. | `(?i)\b(huella\s+de\s+carbono\|descarbonizaci[oó]n\|gases?\s+de\s+efecto\s+invernadero\|\bgei\b\|neutralidad\s+de\s+carbono\|carbono\s+neutral(idad)?\|bonos?\s+de\s+carbono\|cr[eé]ditos?\s+de\s+carbono\|mercado\s+de\s+carbono\|presupuesto\s+de\s+carbono)\b` |
| **4. Transición y SBN** | Inversiones en soluciones tecnológicas o basadas en ecosistemas para la transición ecológica y eficiencia de recursos. | `(?i)\b(soluciones?\s+basadas?\s+en\s+la\s+naturaleza\|transici[oó]n\s+justa\|transici[oó]n\s+energ[eé]tica\|hidr[oó]geno\s+verde\|\bh2v\b\|eficiencia\s+energ[eé]tica\|electromovilidad\|infraestructura\s+verde)\b` |

---

## 3. Protocolo de Control de Falsos Positivos

Para evitar sesgos y contaminación de la muestra en compras públicas chilenas, se implementaron las siguientes reglas de depuración:

1. **Exclusión contextual negativa:** Se descartaron sistemáticamente expresiones como *«clima laboral»*, *«clima organizacional»*, *«ambiente laboral»* y compras operativas de *«aire acondicionado»*.
2. **Desambiguación de siglas cortas:**
   * La sigla `SBN` (que en municipios chilenos frecuentemente codifica *«Subvención»*) se eliminó como token aislado, exigiéndose la frase completa *«soluciones basadas en la naturaleza»*.
   * La sigla `PACC` (que en el sector aeronáutico y defensa corresponde a *«Puesto de Avanzada / Control»*) se restringió a contextos que incluyan explícitamente *«plan de adaptación / cambio climático»*.
3. **Deduplicación multi-nivel:** Cada proceso de compra se deduplica a nivel de `codigo_proceso + subcategoria + tipo_registro` para evitar sobreconteo derivado de compras con múltiples líneas de producto idénticas.

---

## 4. Alcance Ontológico y Limitaciones de los Datos

Para el análisis en ciencias sociales y políticas públicas, se deben considerar las siguientes delimitaciones del dato administrativo:

1. **Intención vs. Impacto:** El catastro mide **asignación y contratación de recursos públicos**, lo que constituye un indicador directo de *priorización de agenda y capacidad de compra*, pero no equivale automáticamente a la *evaluación de impacto ecológico* de la intervención.
2. **Sesgo de rotulado administrativo:** El registro depende del vocabulario utilizado por los funcionarios de adquisiciones al redactar las bases y órdenes de compra.
3. **Diferenciación de montos:**
   * En **Licitaciones (`licitacion`)**, el monto refleja el valor estimado o adjudicado del contrato marco global.
   * En **Órdenes de Compra (`orden_compra`)**, el monto corresponde a la transacción neta formalizada.

---

## 5. Codebook / Diccionario de Variables

| Variable | Tipo | Descripción Operacional | Ejemplo / Valores |
| :--- | :--- | :--- | :--- |
| `archivo_origen` | Texto | Nombre del archivo masivo mensual de donde proviene el registro. | `lic_2024-03.csv`, `oc_2022-11.csv` |
| `tipo_registro` | Categórica | Modalidad de contratación administrativa. | `licitacion`, `orden_compra` |
| `codigo_proceso` | Texto | Identificador único del proceso (`CodigoExterno` en licitaciones o `Codigo` en OCs). | `612227-1-LE26`, `2346-53-AG26` |
| `link` | URL | Enlace directo a la ficha pública en Mercado Público para auditoría. | `http://www.mercadopublico.cl/fichaLicitacion.html?idLicitacion=...` |
| `nombre` | Texto | Título formal del proceso o de la orden de compra. | *«Consultoría Plan de Acción Comunal de Cambio Climático»* |
| `descripcion` | Texto | Glosa descriptiva del requerimiento técnico. | *«Elaboración de inventario GEI y cartera de proyectos PACCC»* |
| `organismo_comprador` | Texto | Nombre de la entidad pública contratante. | `I MUNICIPALIDAD DE CONCEPCION`, `GOBIERNO REGIONAL DE ATACAMA` |
| `nivel_institucional` | Categórica | Tipología de gobernanza institucional del comprador. | `Municipalidades (Gobiernos Locales)`, `Gobiernos Regionales (GORE)`, `Gobierno Central y Servicios Públicos`, `Universidades y Academia`, `Sector Salud`, `Defensa y Fuerzas Armadas`, `Empresas Públicas del Estado` |
| `unidad_compra` | Texto | Dirección, secretaría o departamento solicitante. | `DIRECCION DE MEDIO AMBIENTE`, `DEPTO ADQUISICIONES` |
| `rut_comprador` | Texto | RUT institucional del organismo comprador. | `69.070.100-3` |
| `sector` | Categórica | Clasificación sectorial del Estado según ChileCompra. | `MUNICIPALIDADES`, `MINISTERIOS`, `UNIVERSIDADES` |
| `region_comprador` | Categórica | Región político-administrativa del comprador. | `Región del Biobío`, `Región Metropolitana de Santiago` |
| `fecha` | Fecha | Fecha de publicación, envío o aceptación del proceso. | `2024-05-18` |
| `monto_pesos` | Numérico | Monto en pesos chilenos registrado en la plataforma. | `15000000` |
| `moneda` | Categórica | Moneda original de la contratación. | `CLP`, `UF`, `USD`, `UTM` |
| `proveedor` | Texto | Razón social de la persona jurídica o natural adjudicada. | `DEUMAN SPA`, `UNIVERSIDAD DE CHILE` |
| `rut_proveedor` | Texto | RUT del proveedor adjudicado. | `76.123.456-7` |
| `eje_codigo` | Categórica | Código del eje temático. | `P089_CAMBIO_CLIMATICO` |
| `eje_nombre` | Categórica | Nombre formal del eje. | `Cambio Climático` |
| `subcategoria` | Categórica | Subclasificación temático-normativa. | `Nucleo_Exacto`, `Instrumentos_Ley21455`, `Gases_Descarbonizacion`, `Transicion_SBN` |
| `termino_coincidente` | Texto | Frase exacta que disparó la clasificación positiva. | `cambio climático`, `huella de carbono`, `PACCC`, `PARCC` |
| `texto_fragmento` | Texto | Extracto textual de 80 caracteres alrededor del término para validación cualitativa. | `...elaboración del plan de acción regional de cambio climático...` |

---

## 6. Protocolo de Reproducibilidad Paso a Paso (Replicabilidad Determinista)

Para garantizar la **reproducibilidad científica independiente**, este catastro fue diseñado bajo un **enfoque algorítmico 100% determinista**. Cualquier investigador puede replicar exactamente los 9.086 registros a partir de las fuentes oficiales públicas sin depender de modelos estocásticos o cajas negras de IA.

### Pasos para Replicar el Catastro desde Cero:

#### Paso 1: Descarga de Bases Primarias de ChileCompra
Las 470 bases mensuales de Licitaciones (`lic_YYYY-MM.csv.zip`) y Órdenes de Compra (`oc_YYYY-MM.csv.zip`) correspondientes al período 2007–2026 son de acceso público y gratuito desde el repositorio abierto de datos de ChileCompra:
* **Portal:** `https://datosabiertos.chilecompra.cl/`
* **Contenedor Blob:** `https://transparenciachc.blob.core.windows.net/oc-lic/{Año}-{Mes}.zip`
* **Procedimiento:** Descargar y descomprimir todos los archivos en un directorio local (ej. `DataCompleta/`).

#### Paso 2: Configuración del Entorno Computacional
El pipeline se ejecuta sobre un entorno estándar de código abierto:
```bash
# Requisitos: Python 3.10 o superior
pip install duckdb pandas openpyxl tqdm
```

#### Paso 3: Ejecución del Pipeline Determinista de Filtrado
Se ejecuta el script de extracción estructurada que:
1. Conecta con **DuckDB en memoria** para escanear las columnas de texto plano (`Nombre`, `Descripcion`, `Especificaciones`, `Rubros`).
2. Aplica la matriz de expresiones regulares compiladas (`regex`) definidas en la Sección 2.
3. Aplica los filtros de exclusión negativa de la Sección 3 (*clima laboral*, siglas ambiguas).
4. Realiza la deduplicación por clave compuesta `codigo_proceso + subcategoria + tipo_registro`.
5. Asigna la clasificación de gobernanza `nivel_institucional` (Municipalidades, GOREs, Gobierno Central, Universidades, etc.).
6. Exporta los resultados en formatos tabulares `.xlsx` (multi-pestaña) y `.csv` (`UTF-8-sig` delimitado por punto y coma).

```bash
# Comando de ejecución
python pipeline_catastro_unificado.py
```

#### Paso 4: Verificación y Auditoría de Calidad
Para verificar la paridad matemática y ausencia de anomalías:
```bash
python test_calidad_catastro.py
# Salida esperada: 16/16 pruebas superadas (100% consistencia)
```

---

## 7. Declaración de Rigor Metodológico y Autoría

* **Diseño Conceptual y Taxonomía Ontológica:** Eduardo Vega Toledo & Valentina Cariaga Cerda.
* **Arquitectura del Pipeline de Datos y QA:** Eduardo Vega Toledo (asistido computacionalmente para la optimización de código y paralelización multinúcleo).
* **Naturaleza del Procesamiento:** El algoritmo de clasificación es puramente léxico-simbólico y determinista (basado en reglas gramaticales y expresiones regulares estándar POSIX/PCRE), lo que garantiza que **mismas entradas producen siempre idénticos resultados**, cumpliendo con los estándares de la ciencia abierta (FAIR: *Findable, Accessible, Interoperable, Reusable*).
