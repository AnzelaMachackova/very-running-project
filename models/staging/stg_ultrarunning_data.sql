with 

source as (

    select * from {{ source('stage', 'ultrarunning_data') }}

),

renamed as (

    select
        year_of_event,
        event_dates,
        event_name,
        event_distance_length,
        event_num_finishers,
        athlete_performance,
        athlete_club,
        athlete_country,
        athlete_year_of_birth,
        athlete_gender,
        athlete_age_category,
        athlete_average_speed,
        athlete_id,
        event_type,
        distance_in_km

    from source

)

select * from renamed
