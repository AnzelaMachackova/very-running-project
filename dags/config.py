# GCP config
BUCKET_NAME = 'de-running-project-bucket'
PROJECT_ID = 'de-running-project'

# DAGs
KAGGLE2BQ_DAG = 'kaggle_to_gcs'
CREATE_CORE_TABLES_DAG = 'create_core_tables'

# config for raw layer
FILE_NAME = 'TWO_CENTURIES_OF_UM_RACES.csv'
K_DATASET = 'aiaiaidavid/the-big-dataset-of-ultra-marathon-running' 

# config for staging layer
BQ_STAGE_TABLE = 'de-running-project.stage.ultrarunning_data'

# config for core layer
BQ_EVENTS_TABLE = 'de-running-project.core.events'
SQL_FILE_PATH_EVENTS = 'sql/events.sql'
BQ_ATHLETES_TABLE = 'de-running-project.core.athletes'
BQ_RESULTS_TABLE = 'de-running-project.core.results'

# config for report layer
