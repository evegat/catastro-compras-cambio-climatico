---
title: "Brief Estadístico — Compras Públicas y Cambio Climático en Chile"
project: "P089 / P040"
version: "1.1-harness"
date: "2026-08-28"
author: "Eduardo Vega Toledo"
requested_by: "Valentina Cariaga Cerda"
---

# Brief Estadístico y de Gobernanza

## Resumen ejecutivo

La auditoría del catastro corrige la unidad de análisis del baseline. El corpus histórico contiene **9.086 asignaciones proceso–subcategoría**, pero corresponde a **8.894 procesos de compra distintos**. Por tanto, toda comparación institucional, temporal y de mecanismos debe usar 8.894 como denominador canónico.

Distribución por tipo de registro:

- 2.175 licitaciones distintas.
- 6.719 órdenes de compra distintas.

Los montos se reportan por separado: **$249.813,979 millones CLP en licitaciones** y **$105.536,060 millones CLP en OC**. No se suman.

## Evolución temporal

| Año | Procesos distintos |
|---:|---:|
| 2021 | 423 |
| 2022 | 491 |
| 2023 | 749 |
| 2024 | 978 |
| 2025 | 911 |
| 2026* | 369 |

`*` corte parcial a julio de 2026.

Entre 2022 y 2023 el número de procesos aumenta 52,5%; entre 2022 y 2024, 99,2%. La publicación de la Ley 21.455 en junio de 2022 coincide temporalmente con esta aceleración, pero **el catastro descriptivo no identifica causalidad**.

## Gobernanza multinivel — procesos distintos

| Nivel institucional | Procesos |
|---|---:|
| Gobierno Central y Servicios Públicos | 4.808 |
| Municipalidades | 2.546 |
| Universidades y Academia | 910 |
| Sector Salud | 285 |
| Defensa y Fuerzas Armadas | 136 |
| Gobiernos Regionales | 132 |
| Empresas Públicas del Estado | 77 |

La dimensión municipal sigue siendo sustantiva: 2.546 procesos distintos. Sin embargo, las cifras del baseline que usaban 2.605 correspondían a asignaciones de clasificación y sobrecontaban procesos multicategoría.

## Mecanismos de contratación — procesos distintos

| Mecanismo | Procesos |
|---|---:|
| Trato Directo (Excepcional) | 3.356 |
| Convenio Marco (Catálogo) | 2.266 |
| Licitación Pública | 2.138 |
| Compra Ágil (<30 UTM) | 993 |
| OC Ordinaria / Trato Directo | 104 |
| Licitación Privada | 37 |

Estas etiquetas describen el mecanismo registrado/clasificado. No deben interpretarse por sí solas como evidencia de emergencia climática: esa hipótesis requiere validación caso a caso o reglas adicionales.

## Subcategorías — asignaciones long

| Subcategoría | Asignaciones |
|---|---:|
| Núcleo Exacto | 4.438 |
| Transición/SBN | 3.843 |
| Gases/Descarbonización | 668 |
| Instrumentos Ley 21.455 | 137 |

Las categorías no son mutuamente excluyentes: 178 procesos pertenecen a más de una.

## Agenda de investigación recomendada

1. **Adopción municipal y capacidad estatal:** construir indicadores de primera compra/PACCC por municipio y cruzar con SINIM, FCM, dotación, ruralidad y vulnerabilidad.
2. **Evaluación normativa:** estimar ITSA mensual y, si existe un grupo de comparación defendible, DiD/event study. No etiquetar el quiebre descriptivo como efecto causal antes de esa estimación.
3. **Redes comprador–proveedor:** usar procesos distintos para enlaces bipartitos y evitar duplicar vínculos por multicategoría.
4. **Validación semántica:** etiquetar muestra estratificada por categoría/año/nivel institucional y estimar precisión, especialmente en `Transicion_SBN`.

## Advertencias de investigación

- 10 asignaciones tienen término gatillante vacío.
- La provenance de las 470 fuentes declaradas aún requiere manifest con hashes.
- `2026-4.csv` debe reconciliarse contra dicho manifest.
- El match léxico mide señal administrativa, no impacto ambiental ni ejecución material.
