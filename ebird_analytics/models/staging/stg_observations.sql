SELECT
    "subId" AS checklist_id
    , "speciesCode" AS species_code
    , "comName" AS common_name
    , "sciName" AS scientific_name
    , "locId" AS location_id
    , "locName" AS location_name
    , cast("lat" AS double) AS latitude
    , cast("lng" AS double) AS longitude
    , cast("obsDt" AS timestamp) AS observed_at
    , cast("howMany" AS integer) AS observation_count
    , "obsValid" AS is_valid
    , "obsReviewed" AS is_reviewed
    , "locationPrivate" AS is_private_location
    , date            -- the hive-partitioned ingestion date column from Phase 2

FROM {{ source('raw', 'raw_observations') }}
