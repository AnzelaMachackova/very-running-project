from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
import logging
import requests
from datetime import datetime, timedelta
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitPySparkJobOperator,
    DataprocStartClusterOperator,
    DataprocStopClusterOperator,
)
from airflow.exceptions import AirflowFailException
from config import BUCKET_NAME, FILE_NAME, K_DATASET, KAGGLE2BQ_DAG, PROJECT_ID, REGION, PYSPARK_URI, CLUSTER_NAME
from api_config import ACCOUNT_ID, API_TOCKEN, JOB_ID

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 10),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

def download_from_kaggle():
    try:
        api = KaggleApi()
        api.authenticate()
        logging.info("Downloading file from Kaggle...")
        api.dataset_download_files(dataset=K_DATASET, path='/tmp', unzip=True)
        logging.info("File downloaded successfully.")

    except Exception as e:
        logging.error(f"Error downloading file from Kaggle: {e}")
        raise AirflowFailException

def upload_to_gcs():
    try:
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        #blob = bucket.blob(FILE_NAME)
        blob_name = 'raw/' + FILE_NAME

        blob = bucket.blob(blob_name, chunk_size=10 * 1024 * 1024)
        with open('/tmp/' + FILE_NAME, 'rb') as f:
            blob.upload_from_file(f, rewind=True, content_type='text/csv')
        logging.info("File uploaded successfully.")

    except Exception as e:
        logging.error(f"Error uploading file to GCS: {e}")
        raise AirflowFailException 
    
def trigger_dbt_job_via_api(): 
    url = f"https://tn942.us1.dbt.com/api/v2/accounts/{ACCOUNT_ID}/jobs/{JOB_ID}/run/"
    headers = {
        "Authorization": f"Token {API_TOCKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "cause": "Triggered via API",}
    
    logging.info(f"Triggering dbt job with URL: {url}")
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        logging.info("dbt job triggered successfully")
    else:
        logging.error(f"Failed to trigger dbt job: {response.text}")
        raise AirflowFailException


with DAG('orchestration_workflow', default_args=default_args, schedule_interval=None) as dag:
    # task to download file from Kaggle and upload to GCS
    with TaskGroup(KAGGLE2BQ_DAG) as loading_file_group:
        download_task = PythonOperator(
        task_id='download_from_kaggle',
        python_callable=download_from_kaggle,
        )

        upload_task = PythonOperator(
            task_id='upload_to_gcs',
            python_callable=upload_to_gcs,
        )

        download_task >> upload_task

    # task to trigger pyspark Dataproc job
    with TaskGroup('pyspark_job_group') as pyspark_job_group:
        start_cluster = DataprocStartClusterOperator(
            task_id="start_cluster",
            project_id=PROJECT_ID,
            region=REGION,
            cluster_name=CLUSTER_NAME,
        ) 

        submit_pyspark_job = DataprocSubmitPySparkJobOperator(
            task_id="submit_pyspark_job",
            main=PYSPARK_URI,
            cluster_name=CLUSTER_NAME,
            region=REGION,
            project_id=PROJECT_ID,
            dag=dag,
        #    dataproc_jars=DATAPROC_JAR, 
        )

        stop_cluster = DataprocStopClusterOperator(
            task_id="stop_cluster",
            project_id=PROJECT_ID,
            region=REGION,
            cluster_name=CLUSTER_NAME,
        )
 
        start_cluster >> submit_pyspark_job >> stop_cluster

    # task to trigger dbt job via API 
    trigger_dbt_job = PythonOperator(
        task_id='trigger_dbt_job',
        python_callable=trigger_dbt_job_via_api,
        dag=dag,
    )

    loading_file_group >> pyspark_job_group >> trigger_dbt_job