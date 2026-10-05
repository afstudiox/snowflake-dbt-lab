from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import shutil

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
    # Define um limite para evitar espera indefinida na conexão.
    with urlopen(TSE_URL, timeout=60) as response:
        # Copia o download em partes para não carregar todo o ZIP na memória.
        with ZIP_PATH.open("wb") as output_file:
            shutil.copyfileobj(response, output_file)

    print(f"Download concluído: {ZIP_PATH}")
else:
    print("ZIP já existe. Download ignorado.")

with ZipFile(ZIP_PATH) as archive:
    # Resolve o diretório permitido para impedir escrita fora de data_raw.
    raw_dir = RAW_DIR.resolve()

    print("Arquivos extraídos:")

    for member in archive.infolist():
        # Calcula o caminho final do arquivo extraído.
        destination = (RAW_DIR / member.filename).resolve()

        # Bloqueia caminhos maliciosos, como ../../arquivo.txt.
        if not destination.is_relative_to(raw_dir):
            raise ValueError(
                f"Caminho inválido encontrado no ZIP: {member.filename}"
            )

        # Extrai o arquivo somente depois da validação do caminho.
        archive.extract(member, RAW_DIR)
        print(f"- {member.filename}")


print("Ingestão concluída.")
