with source_data as (

    select *
    from {{ source('tse_raw', 'raw_votacao_secao') }}

)

select
    {{ parse_tse_date('DT_GERACAO') }} as dt_geracao,

    nullif(HH_GERACAO, '#NULO') as hh_geracao,

    try_cast(
        nullif(ANO_ELEICAO, '#NULO')
        as integer
    ) as ano_eleicao,

    nullif(NM_TIPO_ELEICAO, '#NULO') as nm_tipo_eleicao,

    try_cast(
        nullif(NR_TURNO, '#NULO')
        as integer
    ) as nr_turno,

    {{ parse_tse_date('DT_ELEICAO') }} as dt_eleicao,

    nullif(SG_UF, '#NULO') as sg_uf,

    try_cast(
        nullif(CD_MUNICIPIO, '#NULO')
        as integer
    ) as cd_municipio,

    nullif(NM_MUNICIPIO, '#NULO') as nm_municipio,

    try_cast(
        nullif(NR_ZONA, '#NULO')
        as integer
    ) as nr_zona,

    try_cast(
        nullif(NR_SECAO, '#NULO')
        as integer
    ) as nr_secao,

    try_cast(
        nullif(CD_CARGO, '#NULO')
        as integer
    ) as cd_cargo,

    nullif(DS_CARGO, '#NULO') as ds_cargo,

    try_cast(
        nullif(NR_VOTAVEL, '#NULO')
        as integer
    ) as nr_votavel,

    nullif(NM_VOTAVEL, '#NULO') as nm_votavel,

    try_cast(
        nullif(QT_VOTOS, '#NULO')
        as integer
    ) as qt_votos

from source_data