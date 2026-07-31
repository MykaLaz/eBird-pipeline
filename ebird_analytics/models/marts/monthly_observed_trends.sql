SELECT d.year  AS year
     , d.month AS month
     , COUNT(*)                      AS observation_number
  FROM {{ ref('fact_observation') }} AS f
  JOIN {{ ref('dim_date') }}         AS d
    ON f.date = d.observation_date
 GROUP BY d.year
     , d.month
 ORDER BY d.year
     , d.month
