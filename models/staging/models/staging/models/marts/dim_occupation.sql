-- Dimension: Yrken
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['occupation_label']) }} as occupation_key,
    occupation_label,
    occupation_group_label
FROM {{ ref('stg_job_ads') }}
WHERE occupation_label IS NOT NULL