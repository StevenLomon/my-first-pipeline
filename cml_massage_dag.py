from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from cml_massage_etl import extract_review_count

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 15),
    'email': ['steven.lennartsson@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('cml_massage_dag',
         default_args=default_args,
         schedule_interval= '@daily',
         catchup=False) as dag:
    
    extract_review_count = PythonOperator(
        task_id = 'tsk_cml_review_count',
        python_callable=extract_review_count
    )

    extract_review_count