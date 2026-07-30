SELECT DISTINCT
     checklist_id
     , species_code
     , location_id
     , date
     , observed_at
     , observation_count
     , is_valid
     , is_reviewed
  FROM {{ ref('stg_observations') }}
