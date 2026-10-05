# Contrato de dados — TSE Votação por Seção

## Fonte

- Origem: Tribunal Superior Eleitoral
- Arquivo: `votacao_secao_2022_ES.csv`
- Ano: 2022
- UF: Espírito Santo

## Formato

- Codificação: Latin-1
- Separador: ponto e vírgula (`;`)
- Campos delimitados por aspas
- Dados numéricos também aparecem entre aspas

## Valores especiais

| Valor | Significado |
|---|---|
| `#NULO` | Informação em branco |
| `-1` | Valor numérico correspondente a `#NULO` |
| `#NE` | Informação não registrada naquele ano |
| `-3` | Valor numérico correspondente a `#NE` |

## Valores especiais de UF

| Código | Significado |
|---|---|
| `BR` | Nacional |
| `VT` | Voto em trânsito |
| `ZZ` | Exterior |

## Regra de arquitetura

A camada raw deve preservar os dados originais.

As conversões e tratamentos devem ocorrer na camada staging:

- leitura com codificação Latin-1;
- `#NULO` convertido para nulo;
- `#NE` convertido para valor não registrado;
- conversão de datas;
- conversão dos tipos numéricos.

## Fonte da documentação

Arquivo `leiame.pdf` fornecido pelo Portal de Dados Abertos do TSE.
