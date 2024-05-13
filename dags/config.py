# GCP config
BUCKET_NAME = 'de-running-project-bucket'
PROJECT_ID = 'de-running-project'

# DAGs
KAGGLE2BQ_DAG = 'kaggle_to_gcs'
CREATE_CORE_TABLES_DAG = 'create_core_tables'

# config for raw layer
FILE_NAME = 'TWO_CENTURIES_OF_UM_RACES.csv'
K_DATASET = 'aiaiaidavid/the-big-dataset-of-ultra-marathon-running' 

# config for staging layer (PySpark job)
BQ_STAGE_TABLE = 'de-running-project.stage.ultrarunning_data'
REGION = 'europe-west3'
PYSPARK_URI = 'gs://de-running-project-bucket/code/data_cleaning.py' 
CLUSTER_NAME = 'de-running-cluster-9b9e'
DATAPROC_JAR = ["gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.11-0.23.2.jar"]
