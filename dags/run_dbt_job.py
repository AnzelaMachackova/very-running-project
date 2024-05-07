from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
#import requests
#import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_trigger',
    default_args=default_args,
    description='DAG to trigger dbt jobs via API',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False
)

# task to trigger dbt job via API (not implemented because of free tier limitations)
# def trigger_dbt_job_via_api(): 
#     url = f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/jobs/{job_id}/run/"
#     headers = {
#         "Authorization": f"Token {api_token}"
#     }
#     body = {
#         "cause": "Triggered by Airflow"}
    
#     logging.info(f"Triggering dbt job with URL: {url}")
#     response = requests.post(url, headers=headers, json=body)
#     if response.status_code == 200:
#         logging.info("dbt job triggered successfully")
#     else:
#         logging.info(f"Failed to trigger dbt job: {response.text}")

# trigger_job = PythonOperator(
#     task_id='trigger_dbt_job',
#     python_callable=trigger_dbt_job,
#     dag=dag,
# )

run_dbt = BashOperator(
    task_id='run_dbt_job',
    bash_command='dbt run',
    dag=dag,
)