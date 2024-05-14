from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitPySparkJobOperator,
    DataprocStartClusterOperator,
    DataprocStopClusterOperator,
)
from config import PROJECT_ID, REGION, PYSPARK_URI, CLUSTER_NAME, DATAPROC_JAR


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2024, 5, 10),
}


dag = DAG(
    'dataproc_spark_dag',
    default_args=default_args,
    description='Run Spark job on Dataproc',
    schedule_interval=timedelta(days=1),
)


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
