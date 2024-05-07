FROM apache/airflow:latest

RUN pip install kaggle          

RUN pip install requests
RUN pip install dbt