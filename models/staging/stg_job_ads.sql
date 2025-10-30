--Staging: Rensa och strukturera rå data från JobTech API
WITH source AS (
    SELECT * FROM {{ source('job_ads_pipeline', 'job_ads_resource') }}
)

SELECT
    id,
    headline,
    description_text,
    employer_name,
    workplace_address_municipality,
    workplace_address_region,
    occupation_label,
    occupation_group_label,
    employment_type_label,
    published_date,
    application_deadline,
    number_of_vacancies,
    CURRENT_TIMESTAMP as loaded_at
FROM source
WHERE id IS NOT NULL