WITH all_ads AS (
    SELECT * FROM {{ ref('stg_job_ads_hr') }}
    UNION ALL
    SELECT * FROM {{ ref('stg_job_ads_data') }}
    UNION ALL
    SELECT * FROM {{ ref('stg_job_ads_ekonomi') }}
)
SELECT
    occupation,
    municipality,
    COUNT(*) AS antal_annons
FROM all_ads
GROUP BY occupation, municipality
ORDER BY antal_annons DESC
