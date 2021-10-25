# Glint Test
## Stack File
- docker-compose.yaml
- dag_trf_data.py
- runner.sh

## How to run
after clone this repository, it's just execute runner.sh.
first, you need add permission to execute file
```
chmod +x runner.sh
```

after that, you can execute runner.sh
```
./runner.sh
```

If you want stopped the service you can down the docker compose
```
docker-compose down
```

## How to run dag
After airflow running at docker compose, open your browser localhost:5884
and input credential
username: airflow
password: airflow

Run dag_trf_data with play button and click trigger DAG

## To see data source and target
Using database postgres client

### Source
    database: sources
    username: postgres
    password: postgres
    port: 5432
    host: postgres-source

### Target
    database: target
    username: postgres
    password: postgres
    port: 5433
    host: postgres-target