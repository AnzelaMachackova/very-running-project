{{ config(materialized='table') }}

SELECT
  m.event_id,
  REGEXP_REPLACE(u.event_name, r' \([^)]+\)$', '') AS race_name,
  u.event_name,
  MAX(REGEXP_EXTRACT(u.event_name, r'\((.*?)\)')) AS event_country,
  MAX(u.event_type) AS event_type,
  u.event_dates,
  u.year_of_event,
  MAX(u.event_distance_length) AS event_distance_length,
  MAX(u.distance_in_km) as distance_in_km,
  u.event_num_finishers,
  MAX({{ calculate_duration('u.event_distance_length') }}) AS event_duration
FROM
  {{ source('running_stage_data', 'ultrarunning_data') }} u
LEFT JOIN
  {{ ref('event_name_mapping') }} m ON m.event_name = u.event_name
GROUP BY
  m.event_id, 
  REGEXP_REPLACE(u.event_name, r' \([^)]+\)$', ''),
  u.event_name,
  u.year_of_event,
  u.event_dates,
  u.event_num_finishers