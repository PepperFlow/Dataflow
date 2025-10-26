-- Dimension: Arbetsgivare
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['employer_name']) }} as employer_key,
    employer_name
FROM {{ ref('stg_job_ads') }}
WHERE employer_name IS NOT NULL