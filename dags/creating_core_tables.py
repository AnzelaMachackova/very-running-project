from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery
from google.cloud import storage
from config import CREATE_CORE_TABLES_DAG, BUCKET_NAME, BQ_EVENTS_TABLE, BQ_ATHLETES_TABLE, BQ_RESULTS_TABLE, BQ_STAGE_TABLE, SQL_FILE_PATH_EVENTS
import logging
from airflow.exceptions import AirflowFailException

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 10)
}

def read_sql_from_bucket(file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    sql_query = blob.download_as_text()
    logging.info("SQL query downloaded successfully. Query is: \n" + sql_query)
    return sql_query

def create_events_table():
    query = read_sql_from_bucket(SQL_FILE_PATH_EVENTS)
    query_formatted = query.format(events_table = BQ_EVENTS_TABLE, ultrarunning_table = BQ_STAGE_TABLE)
    logging.info("Query formatted successfully. Query is: \n" + query_formatted)
    try:
        client = bigquery.Client()
        query_job = client.query(query_formatted)
        results = query_job.result()
        logging.info(f"Events table created successfully. Results: {results}")

    except Exception as e:
        logging.error(f"Error creating events table: {e}")
        raise AirflowFailException

# def create_athletes_table():


# def create_results_table()():


dag = DAG(
    CREATE_CORE_TABLES_DAG,
    default_args=default_args,
    description='A DAG with tasks to run BigQuery queries',
    schedule_interval=None,
)

events_table = PythonOperator(
    task_id='create_events_table',
    python_callable=create_events_table,
    dag=dag,
)


events_table 