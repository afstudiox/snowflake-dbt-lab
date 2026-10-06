select
    sg_uf,
    cd_municipio,
    nm_municipio,
    cd_cargo,
    ds_cargo,
    sum(qt_votos) as total_votos,
    count(distinct nr_zona) as quantidade_zonas,
    count(*) as quantidade_registros
from {{ ref('stg_votacao_secao') }}
where qt_votos is not null
group by
    sg_uf,
    cd_municipio,
    nm_municipio,
    cd_cargo,
    ds_cargo
