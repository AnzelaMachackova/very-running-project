from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
import logging
from datetime import datetime, timedelta
from config import BUCKET_NAME, FILE_NAME, K_DATASET, KAGGLE2BQ_DAG
from airflow.exceptions import AirflowFailException

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 10)
}

dag = DAG(
    KAGGLE2BQ_DAG,
    default_args=default_args,
    description='A DAG to load data from Kaggle to BigQuery',
    schedule_interval=None,
)

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

with dag:
    download_task = PythonOperator(
        task_id='download_from_kaggle',
        python_callable=download_from_kaggle,
    )

    upload_task = PythonOperator(
        task_id='upload_to_gcs',
        python_callable=upload_to_gcs,
    )


    download_task >> upload_task 
