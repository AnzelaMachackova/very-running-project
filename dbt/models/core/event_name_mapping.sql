{{ config(materialized='table') }}

WITH unique_events AS (
  SELECT DISTINCT event_name
  FROM {{ source('running_stage_data', 'ultrarunning_data') }} 
)

SELECT
  event_name,
  ROW_NUMBER() OVER() AS event_id
FROM unique_events