FROM apache/airflow:latest

RUN pip3 install kaggle          

# RUN pip install requests

# copy dbt project into the Docker image
RUN pip3 install dbt
COPY dbt /dbt_project
WORKDIR /dbt_project