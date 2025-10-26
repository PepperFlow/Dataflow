-- Fact table: Jobbannonser
SELECT
    s.id as job_ad_id,
    {{ dbt_utils.generate_surrogate_key(['s.occupation_label']) }} as occupation_key,
    {{ dbt_utils.generate_surrogate_key(['s.workplace_address_municipality', 's.workplace_address_region']) }} as location_key,
    {{ dbt_utils.generate_surrogate_key(['s.employer_name']) }} as employer_key,
    {{ dbt_utils.generate_surrogate_key(['CAST(s.published_date AS DATE)']) }} as published_date_key,
    s.headline,
    s.employment_type_label,
    s.number_of_vacancies,
    s.application_deadline,
    s.published_date,
    s.loaded_at
FROM {{ ref('stg_job_ads') }} s