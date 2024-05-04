{{ config(materialized='table') }}

SELECT
  u.athlete_id,
  u.athlete_club,
  m.event_id
FROM 
  {{ source('running_stage_data', 'ultrarunning_data') }} u
LEFT JOIN {{ ref('event_name_mapping') }} m 
  ON u.event_name = m.event_name
WHERE
  athlete_club IS NOT NULL