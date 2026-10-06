{% macro parse_tse_date(column_name) %}

    {% if target.type == 'snowflake' %}

        TRY_TO_DATE(
            NULLIF({{ column_name }}, '#NULO'),
            'DD/MM/YYYY'
        )

    {% else %}

        TRY_STRPTIME(
            NULLIF({{ column_name }}, '#NULO'),
            '%d/%m/%Y'
        )::DATE

    {% endif %}

{% endmacro %}