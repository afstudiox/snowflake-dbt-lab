import os
from pathlib import Path

import snowflake.connector


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "dbt_project"
    / "data_raw"
    / "votacao_secao_2022_ES.csv"
)

SNOWFLAKE_ACCOUNT = "ZBHLGJN-YQ39911"
SNOWFLAKE_USER = "AFELIPES"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "TSE_ANALYTICS"
SNOWFLAKE_SCHEMA = "RAW"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"


if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Arquivo CSV não encontrado: {CSV_PATH}"
    )

print(f"CSV encontrado: {CSV_PATH}")
print(f"Conta Snowflake: {SNOWFLAKE_ACCOUNT}")
print(f"Database: {SNOWFLAKE_DATABASE}")
print(f"Schema: {SNOWFLAKE_SCHEMA}")

connection = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

print("Conexão com Snowflake estabelecida.")

cursor = connection.cursor()

cursor.execute(
    """
    CREATE OR REPLACE TABLE RAW_VOTACAO_SECAO (
        DT_GERACAO VARCHAR,
        HH_GERACAO VARCHAR,
        ANO_ELEICAO VARCHAR,
        CD_TIPO_ELEICAO VARCHAR,
        NM_TIPO_ELEICAO VARCHAR,
        NR_TURNO VARCHAR,
        CD_ELEICAO VARCHAR,
        DS_ELEICAO VARCHAR,
        DT_ELEICAO VARCHAR,
        TP_ABRANGENCIA VARCHAR,
        SG_UF VARCHAR,
        SG_UE VARCHAR,
        NM_UE VARCHAR,
        CD_MUNICIPIO VARCHAR,
        NM_MUNICIPIO VARCHAR,
        NR_ZONA VARCHAR,
        NR_SECAO VARCHAR,
        CD_CARGO VARCHAR,
        DS_CARGO VARCHAR,
        NR_VOTAVEL VARCHAR,
        NM_VOTAVEL VARCHAR,
        QT_VOTOS VARCHAR,
        NR_LOCAL_VOTACAO VARCHAR,
        SQ_CANDIDATO VARCHAR,
        NM_LOCAL_VOTACAO VARCHAR,
        DS_LOCAL_VOTACAO_ENDERECO VARCHAR
    )
    """
)

print("Tabela RAW_VOTACAO_SECAO criada.")

cursor.close()

cursor = connection.cursor()

csv_uri = f"file://{CSV_PATH.as_posix()}"

cursor.execute(
    f"""
    PUT '{csv_uri}'
    @%RAW_VOTACAO_SECAO
    AUTO_COMPRESS=TRUE
    OVERWRITE=TRUE
    """
)

print("CSV enviado para o stage interno do Snowflake.")

cursor.close()

cursor = connection.cursor()

copy_results = cursor.execute(
    """
    COPY INTO RAW_VOTACAO_SECAO
    FROM @%RAW_VOTACAO_SECAO
    FILE_FORMAT = (
        TYPE = CSV
        FIELD_DELIMITER = ';'
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        SKIP_HEADER = 1
        ENCODING = 'ISO88591'
        NULL_IF = ('')
    )
    ON_ERROR = 'ABORT_STATEMENT'
    PURGE = FALSE
    """
).fetchall()

print("Resultado do COPY INTO:")

for result in copy_results:
    print(result)

cursor.close()

connection.close()