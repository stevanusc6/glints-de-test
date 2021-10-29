#!/bin/sh

# Initialize airflow environment
rm -rf dags
rm -rf logs
rm -rf plugins
rm -rf postgres

mkdir dags
mkdir logs
mkdir plugins
mkdir postgres

chmod -R 775 dags
chmod -R 775 logs
chmod -R 775 plugins
chmod -R 775  postgres

docker-compose up airflow-init
docker-compose up airflow-connection-add-source
docker-compose up airflow-connection-add-target

cp dag_trf_data.py dags

docker-compose down airflow-connection-add-source
docker-compose down airflow-connection-add-target
docker-compose down airflow-init


docker-compose up -d
