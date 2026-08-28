# Catastro de Compras Públicas y Cambio Climático en Chile (2007–julio 2026)

**Proyecto P089 · versión 1.1-harness**  
**Arquitectura de datos:** Eduardo Vega Toledo  
**A encargo de:** Valentina Cariaga Cerda  
**Fuente:** datos abiertos de ChileCompra / Mercado Público  
**Licencia:** CC BY 4.0

> **Estado:** auditado y reparado el 28-08-2026. El corpus histórico contiene **9.086 asignaciones proceso–subcategoría**, equivalentes a **8.894 procesos de compra distintos**. La documentación previa que trataba 9.086 como “procesos únicos” queda sustituida por esta versión.

## Métricas canónicas

| Métrica | Valor |
|---|---:|
| Asignaciones de clasificación | 9.086 |
| Procesos distintos | **8.894** |
| Licitaciones distintas | 2.175 |
| Órdenes de compra distintas | 6.719 |
| Procesos multicategoría | 178 |
| Asignaciones adicionales por multicategoría | 192 |
| Monto registrado en licitaciones distintas | **$249.813,979 millones CLP** |
| Monto registrado en OC distintas | **$105.536,060 millones CLP** |
| Procesos sin monto parsable | 289 |

**Regla monetaria:** no sumar montos de licitaciones y órdenes de compra. Son magnitudes administrativas diferentes: las licitaciones pueden representar marcos/presupuestos, mientras las OC representan transacciones registradas.

## Modelo de datos

`Catastro_Cambio_Climatico_ChileCompra.csv` se conserva como **tabla long de clasificación**. Su llave es:

```text
(tipo_registro, codigo_proceso, subcategoria)
```

Para análisis institucionales, temporales y de mecanismos de contratación, la unidad correcta es:

```text
(tipo_registro, codigo_proceso)
```

La vista de 8.894 procesos se construye de forma determinista con:

```bash
python scripts/build_process_level.py Catastro_Cambio_Climatico_ChileCompra.csv \
  --output output/Catastro_Procesos_Unicos_Cambio_Climatico_ChileCompra.csv
```

## Auditoría reproducible

```bash
python scripts/audit_dataset.py Catastro_Cambio_Climatico_ChileCompra.csv
python -m unittest discover -s tests -v
```

El contrato también corre en GitHub Actions en cada PR y push a `main`.

## Resultados descriptivos corregidos

Los procesos distintos pasan de **491 en 2022** a **749 en 2023** y **978 en 2024**. Esto equivale a +52,5% entre 2022–2023 y +99,2% entre 2022–2024. La Ley Marco de Cambio Climático (Ley 21.455) fue publicada en junio de 2022; la coincidencia temporal es una **hipótesis de cambio post-2022**, no una estimación causal. Un efecto causal requiere un diseño de identificación como ITSA, DiD/event study u otro contrafactual defendible.

Distribución de procesos distintos por nivel institucional:

| Nivel | Procesos |
|---|---:|
| Gobierno Central y Servicios Públicos | 4.808 |
| Municipalidades | 2.546 |
| Universidades y Academia | 910 |
| Sector Salud | 285 |
| Defensa y Fuerzas Armadas | 136 |
| Gobiernos Regionales | 132 |
| Empresas Públicas del Estado | 77 |

## Archivos principales

- `Catastro_Cambio_Climatico_ChileCompra.csv`: tabla long de 9.086 asignaciones.
- `01_Ficha_Metodologica_y_Codebook.md`: metodología y semántica de las unidades.
- `02_Brief_Estadistico_Compras_Climaticas.md`: resultados descriptivos y agenda de investigación.
- `HARNESS.md`: contrato de datos v1.1 y advertencias abiertas.
- `scripts/audit_dataset.py`: auditor independiente del contrato.
- `scripts/build_process_level.py`: construcción de la vista de procesos distintos.
- `tests/test_contract.py`: pruebas de regresión.
- `provenance/`: especificación para cerrar trazabilidad de las 470 fuentes declaradas.

## Advertencias abiertas

1. **10 asignaciones** tienen `termino_coincidente` vacío y requieren revisión contra el dato primario.
2. Se observan **466 nombres de archivo fuente** en filas con match. Esto no permite auditar por sí solo la declaración de 470 archivos procesados: un archivo puede tener cero coincidencias. Falta un manifest de ingestión con hashes.
3. `2026-4.csv` es un nombre de fuente no estándar y debe reconciliarse con ese manifest.
4. `Transicion_SBN` es una categoría amplia. Antes de inferencia sustantiva debe medirse precisión mediante muestra etiquetada.
5. La clasificación identifica **candidatos por lenguaje administrativo**; no demuestra impacto climático material ni ejecución física.

## Fuentes primarias

- Portal de datos abiertos ChileCompra: https://datosabiertos.chilecompra.cl/
- Mercado Público: https://www.mercadopublico.cl/
- Ley 21.455: https://www.bcn.cl/leychile/Navegar?idNorma=1177286
