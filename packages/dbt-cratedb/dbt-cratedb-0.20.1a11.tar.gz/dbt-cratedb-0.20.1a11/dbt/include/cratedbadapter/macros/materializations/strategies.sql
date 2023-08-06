{#
    Core strategy definitions
#}
{% macro cratedbadapter__snapshot_timestamp_strategy(node, snapshotted_rel, current_rel, config, target_exists) %}
    {% set primary_key = config['unique_key'] %}
    {% set updated_at = config['updated_at'] %}
    {% set invalidate_hard_deletes = config.get('invalidate_hard_deletes', false) %}

    {#/*
        The snapshot relation might not have an {{ updated_at }} value if the
        snapshot strategy is changed from `check` to `timestamp`. We
        should use a dbt-created column for the comparison in the snapshot
        table instead of assuming that the user-supplied {{ updated_at }}
        will be present in the historical data.

        See https://github.com/fishtown-analytics/dbt/issues/2350
    */ #}
    {% set row_changed_expr -%}
        ({{ snapshotted_rel }}.dbt_valid_from < {{ current_rel }}.{{ updated_at }})
    {%- endset %}

    {% set scd_id_expr = snapshot_hash_arguments([primary_key, updated_at]) %}

    {% do return({
        "unique_key": primary_key,
        "updated_at": updated_at,
        "row_changed": row_changed_expr,
        "scd_id": scd_id_expr,
        "invalidate_hard_deletes": invalidate_hard_deletes
    }) %}
{% endmacro %}