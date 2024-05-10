{#
    This macro calculate race duration from the event_distance_length 
#}

{% macro calculate_duration(column) %}
  ROUND(CASE
    WHEN REGEXP_CONTAINS({{ column }}, r'd$') THEN CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS FLOAT64) * 24
    WHEN REGEXP_CONTAINS({{ column }}, r'h$') AND NOT REGEXP_CONTAINS({{ column }}, r':') THEN CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS FLOAT64)
    WHEN REGEXP_CONTAINS({{ column }}, r':') THEN 
      CAST(REGEXP_EXTRACT({{ column }}, r'(\d+):') AS FLOAT64) + 
      CAST(REGEXP_EXTRACT({{ column }}, r':(\d+)') AS FLOAT64) / 60
    ELSE NULL
  END, 2)
{% endmacro %}