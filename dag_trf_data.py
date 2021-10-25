from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

dag_params = {
    'dag_id': 'dag-trf-data',
    'start_date':datetime(2021, 10, 23),
    'schedule_interval': '0 0 * * *'
}

with DAG(**dag_params) as dag:
    def input_data(ds, **kwargs):
        src = PostgresHook(postgres_conn_id='postgres-source')
        dest = PostgresHook(postgres_conn_id='postgres-target')
        src_conn = src.get_conn()
        cursor = src_conn.cursor()
        dest_conn = dest.get_conn()
        dest_cursor = dest_conn.cursor()

        
        dest_cursor.execute("SELECT MAX(id) FROM tbl_sales;")
        id = dest_cursor.fetchone()[0]
        if id is None:
            id = -1
        cursor.execute("SELECT * FROM tbl_sales WHERE id > %s", [id])
        dest.insert_rows(table="tbl_sales", rows=cursor)

    create_table_source = PostgresOperator(
        task_id = 'create_table_source',
        postgres_conn_id = 'postgres-source',
        sql = """
            CREATE TABLE IF NOT EXISTS public.tbl_sales
            (
                id integer PRIMARY KEY,
                creation_date character varying COLLATE pg_catalog."default",
                sale_value double precision
            )
        """
    )

    populate_sale_table = PostgresOperator(
        task_id="populate_sale_table",
        postgres_conn_id = 'postgres-source',
        sql="""
            TRUNCATE TABLE tbl_sales;
            INSERT INTO tbl_sales values ('0','12-12-21',1000);
            INSERT INTO tbl_sales values ('1','13-12-21',2000);
            """,
    )

    create_table_target = PostgresOperator(
        task_id = 'create_table_target',
        postgres_conn_id = 'postgres-target',
        sql = """
            CREATE TABLE IF NOT EXISTS public.tbl_sales
            (
                id integer PRIMARY KEY,
                creation_date character varying COLLATE pg_catalog."default",
                sale_value double precision
            )
        """
    )
    
    input_data = PythonOperator(
        task_id = 'input_data',
        python_callable = input_data
    )
    create_table_source >> populate_sale_table >> create_table_target >> input_data