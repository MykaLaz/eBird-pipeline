SELECT DISTINCT
     species_code
     , common_name
     , scientific_name
  FROM {{ ref('stg_observations') }}
