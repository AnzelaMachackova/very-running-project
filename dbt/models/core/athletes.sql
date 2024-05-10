{{ config(materialized='table') }}

SELECT
  athlete_id,
  MAX(athlete_year_of_birth) AS athlete_year_of_birth,  
  ANY_VALUE(athlete_gender) AS athlete_gender,          
  ANY_VALUE(athlete_country) AS athlete_country                      
FROM 
  {{ source('running_stage_data', 'ultrarunning_data') }}
GROUP BY
  athlete_id