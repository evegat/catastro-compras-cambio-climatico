import duckdb
import os
from pathlib import Path

con = duckdb.connect()
path = "D:/Proyectos/P049 - Compras publicas tecnologicas e IA publica/DataCompleta/lic_2026-01.csv"
try:
    cols_df = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{path}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998') LIMIT 0").df()
    print("Columns count:", len(cols_df))
    cols = list(cols_df["column_name"])
    print("First 5 cols:", cols[:5])
    
    # Test regex query
    q = f"""
    SELECT "CodigoExterno", "Nombre", "Descripcion"
    FROM read_csv_auto('{path}', delim=';', header=True, all_varchar=True, ignore_errors=True, encoding='iso-8859_1-1998')
    WHERE regexp_matches(COALESCE("Nombre", '') || ' ' || COALESCE("Descripcion", ''), '(?i)cambio\\s+clim[aá]tico', 'c')
    LIMIT 5
    """
    res = con.execute(q).fetchall()
    print("Matches found in lic_2026-01.csv:", len(res))
    for r in res:
        print("Match:", r[0], "-", r[1][:60])
except Exception as e:
    print("Error:", e)
