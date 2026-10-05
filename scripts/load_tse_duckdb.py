from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "dbt_project"
    / "data_raw"
    / "votacao_secao_2022_ES.csv"
)

DATABASE_PATH = (
    PROJECT_ROOT
    / "dbt_project"
    / "dev.duckdb"
)

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Arquivo CSV não encontrado: {CSV_PATH}"
    )

print(f"CSV encontrado: {CSV_PATH}")
print(f"Banco DuckDB: {DATABASE_PATH}")

with duckdb.connect(str(DATABASE_PATH)) as connection:

    with duckdb.connect(str(DATABASE_PATH)) as connection:
        print("Conexão com DuckDB estabelecida.")

        connection.execute(
            """
            CREATE OR REPLACE TABLE raw_votacao_secao AS
            SELECT *
            FROM read_csv(
                ?,
                delim=';',
                quote='"',
                header=true,
                encoding='latin-1',
                all_varchar=true
            )
            """,
            [str(CSV_PATH)],
        )

        row_count = connection.execute(
            "SELECT COUNT(*) FROM raw_votacao_secao"
        ).fetchone()[0]

        print(f"Linhas carregadas: {row_count}")

        columns = connection.execute(
            "DESCRIBE raw_votacao_secao"
        ).fetchall()

        print("Colunas da tabela:")
        for column in columns:
            print(f"- {column[0]}: {column[1]}")


    print("Tabela raw_votacao_secao criada.")