{{ config(materialized='table') }}

SELECT 
  ROW_NUMBER() OVER() AS performance_id,
  u.athlete_id,
  e.event_id,
  u.athlete_average_speed,
  u.athlete_performance,
  u.athlete_age_category,
  u.athlete_club
FROM 
  {{ source('running_stage_data', 'ultrarunning_data') }} u
LEFT JOIN 
  {{ ref('event_name_mapping') }} e ON u.event_name = e.event_name
