CREATE OR REPLACE TABLE`{events_table}` AS
SELECT DISTINCT
    year_of_event,
    event_dates,
    event_name,
    event_distance_length,
    event_num_finishers,
    event_type,
    distance_in_km
FROM
    `{ultrarunning_table}`;