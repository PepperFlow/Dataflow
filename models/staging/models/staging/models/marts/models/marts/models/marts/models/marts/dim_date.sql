-- Dimension: Datum
WITH dates AS (
    SELECT DISTINCT
        CAST(published_date AS DATE) as date_value
    FROM {{ ref('stg_job_ads') }}
    WHERE published_date IS NOT NULL
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['date_value']) }} as date_key,
    date_value,
    EXTRACT(YEAR FROM date_value) as year,
    EXTRACT(MONTH FROM date_value) as month,
    EXTRACT(DAY FROM date_value) as day,
    EXTRACT(QUARTER FROM date_value) as quarter,
    DAYNAME(date_value) as day_name,
    EXTRACT(WEEK FROM date_value) as week_number
FROM dates