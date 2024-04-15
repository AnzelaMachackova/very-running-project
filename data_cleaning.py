#!/usr/bin/env python
# coding: utf-8

import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.functions import col


spark = SparkSession.builder \
    .appName('GCSFilesRead') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west3-144277855254-qzbnsuza')

running_df = spark.read.csv('gs://de-running-project-bucket/raw/TWO_CENTURIES_OF_UM_RACES.csv', header=True)

column_mapping = {
    "Year of event": "year_of_event",
    "Event dates": "event_dates",
    "Event name": "event_name",
    "Event distance/length": "event_distance_length",
    "Event number of finishers": "event_num_finishers",
    "Athlete performance": "athlete_performance",
    "Athlete club": "athlete_club",
    "Athlete country": "athlete_country",
    "Athlete year of birth": "athlete_year_of_birth",
    "Athlete gender": "athlete_gender",
    "Athlete age category": "athlete_age_category",
    "Athlete average speed": "athlete_average_speed",
    "Athlete ID": "athlete_id"
}

for old_col, new_col in column_mapping.items():
    running_df = running_df.withColumnRenamed(old_col, new_col)


running_df = running_df.withColumn(
    "event_type",
    F.when(F.col("event_distance_length").rlike(r"\d+[kKmMi]"), "Distance")
    .when(F.col("event_distance_length").rlike(r"\d+[dh]"), "Time")
    .otherwise("Unknown")
)

max_reasonable_speed = 25.0  # km/h

running_df = running_df.withColumn(
    "athlete_average_speed",
    F.when(F.col("athlete_average_speed") <= max_reasonable_speed, F.col("athlete_average_speed"))
    .otherwise(F.col("athlete_average_speed") / 1000.0)  # Convert from m/s to km/h
)

running_df = running_df.withColumn('athlete_performance', F.split(F.col('athlete_performance'), ' ')[0])

running_df.createOrReplaceTempView('running_data')


sql_query = """
SELECT
    *,
    CASE 
        WHEN SUBSTRING_INDEX(event_distance_length, 'mi', 1) = event_distance_length THEN CAST(SUBSTRING_INDEX(event_distance_length, 'km', 1) AS INT)
        WHEN SUBSTRING_INDEX(event_distance_length, 'km', 1) = event_distance_length THEN CAST(SUBSTRING_INDEX(event_distance_length, 'km', 1) AS INT)
        ELSE 'Unknown'
    END AS distance_in_km
FROM running_data
"""

result_df = spark.sql(sql_query)

result_df.write.format('bigquery') \
    .option('table', 'stage.ultrarunning_data') \
    .save()






