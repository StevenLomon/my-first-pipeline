from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_time': datetime(2024, 4, 14),
    'email': ['steven.lennartsson@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('spotify_global_top_50_dag',
         default_args=default_args,
         # schedule_interval= '@weekly',
         catchup=False) as dag:
    extract_spotify_global_top_50_raw_data = PythonOperator(
        task_id = 'tsk_spotify_top_50_raw',
        #python_callable=
    )