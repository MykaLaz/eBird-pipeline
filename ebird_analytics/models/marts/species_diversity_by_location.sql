SELECT
     l.location_name
     , l.latitude
     , l.longitude
     , count(DISTINCT f.species_code)  AS unique_species_count
     , count(*)                        AS total_observations
  FROM {{ ref('fact_observation') }}   AS f
  JOIN {{ ref('dim_location') }}       AS l
    ON f.location_id = l.location_id
 GROUP BY l.location_name, l.latitude, l.longitude
 ORDER BY unique_species_count DESC
