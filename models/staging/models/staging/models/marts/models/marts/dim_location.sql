-- Dimension: Platser
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['workplace_address_municipality', 'workplace_address_region']) }} as location_key,
    workplace_address_municipality as municipality,
    workplace_address_region as region
FROM {{ ref('stg_job_ads') }}
WHERE workplace_address_municipality IS NOT NULL