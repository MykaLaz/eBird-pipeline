SELECT DISTINCT
     CAST(observed_at AS date) AS observation_date
     , EXTRACT(YEAR FROM observed_at) AS year
     , EXTRACT(MONTH FROM observed_at) AS month
     , EXTRACT(DAY FROM observed_at) AS day
     , DAYNAME(observed_at) AS day_of_week
     , EXTRACT(DOW FROM observed_at) AS day_of_week_number
  FROM {{ ref('stg_observations') }}
