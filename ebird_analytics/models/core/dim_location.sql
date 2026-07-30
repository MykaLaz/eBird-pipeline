SELECT DISTINCT
     location_id
     , location_name
     , latitude
     , longitude
     , is_private_location
 FROM {{ ref('stg_observations') }}
