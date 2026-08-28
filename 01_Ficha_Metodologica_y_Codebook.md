---
title: "Ficha Metodológica y Codebook — Catastro de Compras Públicas y Cambio Climático"
project: "P089 / P040"
version: "1.1-harness"
date: "2026-08-28"
author: "Eduardo Vega Toledo"
requested_by: "Valentina Cariaga Cerda"
license: "CC-BY-4.0"
---

# Ficha Metodológica y Codebook

## 1. Propósito y fuente

El catastro identifica registros de Mercado Público/ChileCompra cuyo lenguaje administrativo contiene expresiones asociadas a cambio climático, adaptación, mitigación, descarbonización, instrumentos de la Ley 21.455 y transición/SBN. La cobertura declarada es enero de 2007 a julio de 2026.

Fuente primaria: https://datosabiertos.chilecompra.cl/

## 2. Corrección Harness: unidad de análisis

La salida histórica **no contiene 9.086 procesos únicos**. Contiene **9.086 asignaciones de clasificación** con llave:

`tipo_registro + codigo_proceso + subcategoria`.

Al deduplicar sólo a nivel de proceso (`tipo_registro + codigo_proceso`) existen **8.894 procesos distintos**: 2.175 licitaciones y 6.719 órdenes de compra. Hay 178 procesos con más de una subcategoría, que generan 192 asignaciones adicionales.

Consecuencia analítica:

- Conteos por institución, año, mecanismo y proveedor: usar **procesos distintos**.
- Conteos por subcategoría: pueden usar la tabla long, pero **no sumar categorías** como si fueran mutuamente excluyentes.

## 3. Taxonomía léxica

| Subcategoría | Alcance |
|---|---|
| `Nucleo_Exacto` | cambio climático, adaptación, mitigación, resiliencia/acción climática |
| `Instrumentos_Ley21455` | Ley 21.455, PACCC/PARCC/ECLP y planes climáticos formales |
| `Gases_Descarbonizacion` | GEI, huella de carbono, neutralidad, mercados/presupuestos de carbono |
| `Transicion_SBN` | transición energética/justa, H2V, eficiencia energética, electromovilidad, infraestructura verde, SBN |

Exclusiones negativas incluyen `clima laboral`, `clima organizacional`, `ambiente laboral` y `aire acondicionado`.

**Limitación:** `Transicion_SBN` es deliberadamente amplia. Un match puede ser tangencial a política climática; se exige validación muestral antes de inferencia sustantiva.

## 4. Montos

La auditoría detectó valores textuales con coma decimal que eran coercionados a nulo por algunos scripts previos. La versión Harness normaliza coma decimal y conserva vacíos como nulos.

Montos a nivel de proceso distinto con valor disponible:

- Licitaciones: **CLP 249.813,979 millones**.
- Órdenes de compra: **CLP 105.536,060 millones**.
- Sin monto parsable: 289 procesos (279 licitaciones; 10 OC).

**No existe un total monetario combinado válido sumando licitaciones + OC.** Pueden representar etapas o magnitudes administrativas distintas.

## 5. Trazabilidad y provenance

El dataset de resultados muestra 466 nombres de archivo de origen entre filas con coincidencias. Esto no permite confirmar ni refutar la declaración de 470 fuentes procesadas, porque una fuente puede tener cero matches. El cierre de provenance requiere un manifest independiente con nombre de fuente, período, tamaño, hash SHA-256 y estado de ingestión.

Existe además un nombre no estándar `2026-4.csv` asociado a 46 filas, pendiente de reconciliación con ese manifest.

## 6. Codebook

| Variable | Definición |
|---|---|
| `archivo_origen` | archivo mensual desde el cual se obtuvo la fila |
| `tipo_registro` | `licitacion` u `orden_compra` |
| `mecanismo_compra` | mecanismo administrativo clasificado |
| `codigo_proceso` | identificador del proceso/OC |
| `link` | enlace de verificación en Mercado Público |
| `nombre` | nombre administrativo del proceso |
| `descripcion` | descripción administrativa |
| `organismo_comprador` | institución compradora |
| `unidad_compra` | unidad administrativa |
| `rut_comprador` | RUT institucional |
| `sector` | sector informado por la fuente |
| `region_comprador` | región del comprador |
| `fecha` | fecha de publicación/emisión según fuente |
| `monto_pesos` | monto registrado; interpretación depende del tipo de registro |
| `moneda` | moneda original cuando está informada |
| `proveedor` | proveedor adjudicado cuando aplica |
| `rut_proveedor` | RUT del proveedor |
| `eje_codigo` | código P089 |
| `eje_nombre` | Cambio Climático |
| `nivel_institucional` | tipología institucional derivada |
| `subcategoria` | clasificación temática |
| `termino_coincidente` | expresión que gatilló el match |
| `texto_fragmento` | contexto textual del match |

## 7. Controles de calidad

El Harness v1.1 valida:

- ausencia de duplicados en la llave long;
- 9.086 asignaciones y 8.894 procesos distintos;
- parsing independiente de montos con coma decimal;
- construcción determinista de la vista por proceso;
- advertencias abiertas sobre 10 términos vacíos, provenance y precisión de `Transicion_SBN`.

Ejecución:

```bash
python scripts/audit_dataset.py Catastro_Cambio_Climatico_ChileCompra.csv
python -m unittest discover -s tests -v
```
