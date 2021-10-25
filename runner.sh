#!/bin/sh

# Initialize airflow environment
docker-compose up airflow-init
docker-compose up airflow-connection-add-source
docker-compose up airflow-connection-add-target

cp dag_trf_data.py dags

docker-compose down airflow-connection-add-source
docker-compose down airflow-connection-add-target
docker-compose down airflow-init

docker-compose up -d