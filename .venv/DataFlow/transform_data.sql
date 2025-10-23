CREATE OR REPLACE TABLE job_ads_dataset.job_ads_summary AS
SELECT
  occupation,
  municipality,
  COUNT(*) AS num_ads
FROM job_ads_dataset.job_ads_data
WHERE municipality IS NOT NULL
GROUP BY occupation, municipality
ORDER BY num_ads DESC;
