from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

TSE_URL = (
    "https://cdn.tse.jus.br/estatistica/sead/odsele/"
    "votacao_secao/votacao_secao_2022_ES.zip"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "dbt_project" / "data_raw"
ZIP_PATH = RAW_DIR / "votacao_secao_2022_ES.zip"

RAW_DIR.mkdir(parents=True, exist_ok=True)

if not ZIP_PATH.exists():
    print("Baixando arquivo do TSE...")

    with urlopen(TSE_URL) as response:
        ZIP_PATH.write_bytes(response.read())

    print(f"Download concluído: {ZIP_PATH}")
else:
    print("ZIP já existe. Download ignorado.")

with ZipFile(ZIP_PATH) as archive:
    archive.extractall(RAW_DIR)
    print("Arquivos extraídos:")
    for file_name in archive.namelist():
        print(f"- {file_name}")

print("Ingestão concluída.")
